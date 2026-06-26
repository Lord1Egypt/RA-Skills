/**
 * 浏览器录制核心模块
 * 基于 Puppeteer 和 puppeteer-screen-recorder 实现
 */

const puppeteer = require('puppeteer');
const { PuppeteerScreenRecorder } = require('puppeteer-screen-recorder');
const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');

class ScreenRecorder {
  /**
   * 创建屏幕录制器
   * @param {Object} options 配置选项
   */
  constructor(options = {}) {
    this.options = {
      outputPath: options.outputPath || './recordings/recording.mp4',
      fps: options.fps || 30,
      quality: options.quality || 80,
      aspectRatio: options.aspectRatio || '16:9',
      codec: options.codec || 'libx264',
      headless: options.headless !== undefined ? options.headless : false,
      viewport: options.viewport || { width: 1920, height: 1080 },
      slowMo: options.slowMo || 50,
      debug: options.debug || false,
      logLevel: options.logLevel || 'info',
      ...options
    };

    this.browser = null;
    this.page = null;
    this.recorder = null;
    this.isRecording = false;
    this.startTime = null;
    this.frameCount = 0;

    // 确保输出目录存在
    const outputDir = path.dirname(this.options.outputPath);
    fs.ensureDirSync(outputDir);
  }

  /**
   * 初始化浏览器
   */
  async initBrowser() {
    try {
      console.log(chalk.blue('🚀 启动浏览器...'));
      
      this.browser = await puppeteer.launch({
        headless: this.options.headless,
        defaultViewport: this.options.viewport,
        slowMo: this.options.slowMo,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-accelerated-2d-canvas',
          '--disable-gpu',
          '--window-size=1920,1080'
        ]
      });

      this.page = await this.browser.newPage();
      
      // 设置页面超时
      await this.page.setDefaultNavigationTimeout(60000);
      await this.page.setDefaultTimeout(30000);

      console.log(chalk.green('✅ 浏览器初始化完成'));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 浏览器初始化失败:'), error);
      throw error;
    }
  }

  /**
   * 初始化录制器
   */
  async initRecorder() {
    try {
      const recorderConfig = {
        fps: this.options.fps,
        quality: this.options.quality,
        aspectRatio: this.options.aspectRatio,
        videoCodec: this.options.codec,
        videoCrf: 23,
        videoPreset: 'ultrafast',
        videoBitrate: 1000,
        autopad: {
          color: 'black'
        },
        recordDurationLimit: 3600, // 1小时限制
        metadata: {
          title: 'E2E Test Recording',
          author: 'Multi-Agent Flow',
          description: 'Automated end-to-end test recording'
        }
      };

      this.recorder = new PuppeteerScreenRecorder(this.page, recorderConfig);
      console.log(chalk.blue('🎥 录制器初始化完成'));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 录制器初始化失败:'), error);
      throw error;
    }
  }

  /**
   * 开始录制
   * @param {string} url 要录制的页面URL
   * @param {Object} pageOptions 页面选项
   */
  async startRecording(url, pageOptions = {}) {
    try {
      // 初始化浏览器和录制器
      await this.initBrowser();
      await this.initRecorder();

      console.log(chalk.blue(`🌐 访问页面: ${url}`));
      
      // 导航到页面
      await this.page.goto(url, {
        waitUntil: 'networkidle0',
        timeout: 60000,
        ...pageOptions
      });

      // 开始录制
      console.log(chalk.yellow('⏺️  开始录制...'));
      await this.recorder.start(this.options.outputPath);
      
      this.isRecording = true;
      this.startTime = Date.now();
      this.frameCount = 0;

      console.log(chalk.green(`✅ 录制已开始，输出文件: ${this.options.outputPath}`));
      
      // 启动帧数监控（调试模式）
      if (this.options.debug) {
        this.startFrameMonitoring();
      }

      return true;
    } catch (error) {
      console.error(chalk.red('❌ 开始录制失败:'), error);
      await this.cleanup();
      throw error;
    }
  }

  /**
   * 停止录制
   */
  async stopRecording() {
    if (!this.isRecording) {
      console.log(chalk.yellow('⚠️  没有正在进行的录制'));
      return null;
    }

    try {
      console.log(chalk.yellow('⏹️  停止录制...'));
      
      // 停止录制
      await this.recorder.stop();
      
      const endTime = Date.now();
      const duration = (endTime - this.startTime) / 1000;
      this.isRecording = false;

      // 获取录制信息
      const fileStats = await fs.stat(this.options.outputPath);
      const fileSizeMB = (fileStats.size / (1024 * 1024)).toFixed(2);

      console.log(chalk.green('✅ 录制已停止'));
      console.log(chalk.cyan('📊 录制统计:'));
      console.log(chalk.cyan(`   时长: ${duration.toFixed(2)} 秒`));
      console.log(chalk.cyan(`   文件大小: ${fileSizeMB} MB`));
      console.log(chalk.cyan(`   输出路径: ${this.options.outputPath}`));

      // 清理资源
      await this.cleanup();

      return {
        duration,
        fileSize: fileStats.size,
        filePath: this.options.outputPath,
        frameCount: this.frameCount
      };
    } catch (error) {
      console.error(chalk.red('❌ 停止录制失败:'), error);
      await this.cleanup();
      throw error;
    }
  }

  /**
   * 暂停录制
   */
  async pauseRecording() {
    if (!this.isRecording) {
      console.log(chalk.yellow('⚠️  没有正在进行的录制'));
      return false;
    }

    try {
      await this.recorder.pause();
      console.log(chalk.yellow('⏸️  录制已暂停'));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 暂停录制失败:'), error);
      throw error;
    }
  }

  /**
   * 恢复录制
   */
  async resumeRecording() {
    try {
      await this.recorder.resume();
      console.log(chalk.green('▶️  录制已恢复'));
      return true;
    } catch (error) {
      console.error(chalk.red('❌ 恢复录制失败:'), error);
      throw error;
    }
  }

  /**
   * 执行页面操作
   * @param {Array} actions 操作数组
   */
  async performActions(actions = []) {
    if (!this.page) {
      throw new Error('页面未初始化，请先开始录制');
    }

    console.log(chalk.blue(`🔄 执行 ${actions.length} 个操作`));
    
    for (let i = 0; i < actions.length; i++) {
      const action = actions[i];
      const stepNumber = i + 1;
      
      try {
        console.log(chalk.cyan(`  步骤 ${stepNumber}: ${action.description || action.action}`));
        await this.executeAction(action);
        
        // 操作间延迟
        if (action.delay) {
          await this.page.waitForTimeout(action.delay);
        }
      } catch (error) {
        console.error(chalk.red(`❌ 步骤 ${stepNumber} 执行失败: ${error.message}`));
        if (action.optional !== true) {
          throw error;
        }
      }
    }
  }

  /**
   * 执行单个操作
   * @param {Object} action 操作对象
   */
  async executeAction(action) {
    const { type, selector, text, url, timeout, options } = action;
    
    switch (type) {
      case 'click':
        await this.page.click(selector, options);
        break;
      case 'type':
        await this.page.type(selector, text, options);
        break;
      case 'goto':
        await this.page.goto(url, { waitUntil: 'networkidle0', timeout: timeout || 30000 });
        break;
      case 'waitFor':
        await this.page.waitForSelector(selector, { timeout: timeout || 30000 });
        break;
      case 'waitForTimeout':
        await this.page.waitForTimeout(timeout || 1000);
        break;
      case 'screenshot':
        await this.page.screenshot({ path: selector, ...options });
        break;
      case 'evaluate':
        await this.page.evaluate(text);
        break;
      default:
        throw new Error(`未知的操作类型: ${type}`);
    }
  }

  /**
   * 添加标注到视频
   * @param {string} text 标注文本
   * @param {Object} position 位置 {x, y}
   */
  async addAnnotation(text, position = { x: 100, y: 100 }) {
    if (!this.page) {
      throw new Error('页面未初始化');
    }

    // 在当前页面添加标注（通过注入CSS和HTML）
    await this.page.evaluate(({ text, position }) => {
      const annotation = document.createElement('div');
      annotation.id = 'recorder-annotation';
      annotation.style.position = 'fixed';
      annotation.style.left = `${position.x}px`;
      annotation.style.top = `${position.y}px`;
      annotation.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
      annotation.style.color = 'white';
      annotation.style.padding = '10px';
      annotation.style.borderRadius = '5px';
      annotation.style.zIndex = '999999';
      annotation.style.fontSize = '16px';
      annotation.style.fontFamily = 'Arial, sans-serif';
      annotation.textContent = text;
      
      document.body.appendChild(annotation);
      
      // 5秒后移除
      setTimeout(() => {
        if (annotation.parentNode) {
          annotation.parentNode.removeChild(annotation);
        }
      }, 5000);
    }, { text, position });
  }

  /**
   * 启动帧数监控（调试模式）
   */
  startFrameMonitoring() {
    this.frameMonitor = setInterval(() => {
      if (this.isRecording) {
        this.frameCount++;
        if (this.frameCount % 30 === 0) {
          const duration = (Date.now() - this.startTime) / 1000;
          console.log(chalk.gray(`📈 录制中: ${duration.toFixed(1)}s, 帧数: ${this.frameCount}`));
        }
      }
    }, 1000 / this.options.fps);
  }

  /**
   * 清理资源
   */
  async cleanup() {
    // 停止帧监控
    if (this.frameMonitor) {
      clearInterval(this.frameMonitor);
      this.frameMonitor = null;
    }

    // 关闭浏览器
    if (this.browser) {
      try {
        await this.browser.close();
        console.log(chalk.gray('🔒 浏览器已关闭'));
      } catch (error) {
        console.error(chalk.red('❌ 关闭浏览器失败:'), error);
      }
      this.browser = null;
      this.page = null;
      this.recorder = null;
    }

    this.isRecording = false;
    this.startTime = null;
    this.frameCount = 0;
  }

  /**
   * 获取录制状态
   */
  getStatus() {
    return {
      isRecording: this.isRecording,
      duration: this.isRecording ? (Date.now() - this.startTime) / 1000 : 0,
      frameCount: this.frameCount,
      outputPath: this.options.outputPath,
      fps: this.options.fps,
      quality: this.options.quality
    };
  }
}

/**
 * 快速录制函数
 * @param {string} url 页面URL
 * @param {Object} options 录制选项
 */
async function quickRecord(url, options = {}) {
  const recorder = new ScreenRecorder(options);
  
  try {
    console.log(chalk.cyan('🚀 开始快速录制'));
    console.log(chalk.cyan(`📺 目标页面: ${url}`));
    
    await recorder.startRecording(url);
    
    // 等待用户停止（或超时）
    const timeout = options.timeout || 30000;
    console.log(chalk.yellow(`⏳ 录制中，${timeout/1000}秒后自动停止...`));
    
    await new Promise(resolve => setTimeout(resolve, timeout));
    
    const result = await recorder.stopRecording();
    console.log(chalk.green('🎬 快速录制完成'));
    
    return result;
  } catch (error) {
    console.error(chalk.red('❌ 快速录制失败:'), error);
    await recorder.cleanup();
    throw error;
  }
}

module.exports = {
  ScreenRecorder,
  quickRecord
};