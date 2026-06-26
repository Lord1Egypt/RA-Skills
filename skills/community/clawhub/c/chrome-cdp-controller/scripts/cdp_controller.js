#!/usr/bin/env node
/**
 * Chrome CDP Controller - Puppeteer Version
 * 通过 CDP 协议控制已运行的 Chrome 浏览器
 */

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

class CDPController {
  constructor(wsEndpoint) {
    this.wsEndpoint = wsEndpoint;
    this.browser = null;
    this.page = null;
    this.interceptedResponses = [];
    this.isNewPage = false;
  }

  async connect() {
    try {
      console.error('✓ 连接到 Chrome...');
      this.browser = await puppeteer.connect({
        browserWSEndpoint: this.wsEndpoint,
        defaultViewport: null
      });
      
      // 总是创建新标签页,不使用现有的
      this.page = await this.browser.newPage();
      this.isNewPage = true;

      // Make file uploads work by allowing the caller to pass local file paths.
      // (Puppeteer cannot set <input type="file"> value via page.type/fill.)
      this._uploadedFiles = new Set();
      
      console.error(`✓ 已连接并创建新标签页`);
      return true;
    } catch (error) {
      console.error(`✗ 连接失败: ${error.message}`);
      return false;
    }
  }

  async navigate(url, options = {}) {
    const { waitUntil = 'networkidle2' } = options;
    try {
      await this.page.goto(url, { waitUntil, timeout: 30000 });
      console.error(`✓ 已导航到: ${url}`);
      return { success: true, url };
    } catch (error) {
      console.error(`✗ 导航失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async click(selector, options = {}) {
    const { timeout = 5000 } = options;
    try {
      await this.page.waitForSelector(selector, { timeout });
      await this.page.click(selector);
      console.error(`✓ 已点击: ${selector}`);
      return { success: true };
    } catch (error) {
      console.error(`✗ 点击失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async fill(selector, text, options = {}) {
    const { timeout = 5000 } = options;
    try {
      await this.page.waitForSelector(selector, { timeout });
      await this.page.click(selector, { clickCount: 3 }); // 选中所有文本
      await this.page.type(selector, text);
      console.error(`✓ 已填写: ${selector} = '${text}'`);
      return { success: true };
    } catch (error) {
      console.error(`✗ 填写失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async type(selector, text, options = {}) {
    const { delay = 50, timeout = 5000 } = options;
    try {
      await this.page.waitForSelector(selector, { timeout });
      await this.page.type(selector, text, { delay });
      console.error(`✓ 已输入: ${selector} = '${text}'`);
      return { success: true };
    } catch (error) {
      console.error(`✗ 输入失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async press(key) {
    try {
      await this.page.keyboard.press(key);
      console.error(`✓ 已按键: ${key}`);
      return { success: true };
    } catch (error) {
      console.error(`✗ 按键失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async upload(selector, files, options = {}) {
    try {
      const fileList = Array.isArray(files) ? files : [files];
      const absFiles = fileList.map(f => path.isAbsolute(f) ? f : path.resolve(process.cwd(), f));
      for (const f of absFiles) {
        if (!fs.existsSync(f)) {
          throw new Error(`File not found: ${f}`);
        }
      }

      await this.page.waitForSelector(selector, { timeout: options.timeout || 10000 });
      const input = await this.page.$(selector);
      if (!input) throw new Error(`Upload input not found: ${selector}`);
      await input.uploadFile(...absFiles);
      absFiles.forEach(f => this._uploadedFiles.add(f));
      console.error(`✓ 已上传文件到 ${selector}: ${absFiles.join(', ')}`);
      return { success: true, files: absFiles };
    } catch (error) {
      console.error(`✗ 上传失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async screenshot(path, options = {}) {
    const { fullPage = false } = options;
    try {
      await this.page.screenshot({ path, fullPage });
      console.error(`✓ 截图已保存: ${path}`);
      return { success: true, path };
    } catch (error) {
      console.error(`✗ 截图失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async evaluate(script) {
    try {
      const result = await this.page.evaluate(script);
      console.error(`✓ 已执行脚本`);
      return { success: true, result };
    } catch (error) {
      console.error(`✗ 脚本执行失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async waitForSelector(selector, options = {}) {
    const { timeout = 5000 } = options;
    try {
      await this.page.waitForSelector(selector, { timeout });
      console.error(`✓ 元素已出现: ${selector}`);
      return { success: true };
    } catch (error) {
      console.error(`✗ 等待超时: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async getText(selector) {
    try {
      const text = await this.page.$eval(selector, el => el.textContent);
      return { success: true, text };
    } catch (error) {
      console.error(`✗ 获取文本失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async getAllText(selector) {
    try {
      const texts = await this.page.$$eval(selector, els => els.map(el => el.textContent));
      return { success: true, texts };
    } catch (error) {
      console.error(`✗ 获取文本失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  async startIntercept(urlPattern = '*') {
    try {
      await this.page.setRequestInterception(true);
      
      this.page.on('response', async (response) => {
        const url = response.url();
        const resourceType = response.request().resourceType();
        
        // 匹配 URL 模式
        if (urlPattern !== '*' && !url.includes(urlPattern.replace(/\*/g, ''))) {
          return;
        }
        
        // 只拦截特定类型
        if (['xhr', 'fetch', 'document'].includes(resourceType)) {
          try {
            const body = await response.text();
            this.interceptedResponses.push({
              url,
              status: response.status(),
              headers: response.headers(),
              body
            });
            console.error(`✓ 已拦截响应: ${url.substring(0, 100)}`);
          } catch (e) {
            // 无法读取响应体
          }
        }
      });
      
      console.error(`✓ 已开始拦截响应 (模式: ${urlPattern})`);
      return { success: true };
    } catch (error) {
      console.error(`✗ 拦截启动失败: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  getInterceptedResponses() {
    return { success: true, responses: this.interceptedResponses };
  }

  clearInterceptedResponses() {
    this.interceptedResponses = [];
    return { success: true };
  }

  async wait(seconds) {
    await new Promise(resolve => setTimeout(resolve, seconds * 1000));
    return { success: true };
  }

  async close(opts = {}) {
    const { keepTab = false } = opts;

    // Close the tab we created unless keepTab requested.
    if (!keepTab && this.page && this.isNewPage) {
      try {
        await this.page.close();
        console.error('✓ 已关闭标签页');
      } catch (e) {
        // ignore
      }
    }

    // Always disconnect from the browser (never closes the browser itself).
    if (this.browser) {
      await this.browser.disconnect();
      console.error(`✓ 已断开连接 (浏览器保持打开)${keepTab ? ' [kept tab open]' : ''}`);
    }
  }
}

async function executeCommand(controller, cmd) {
  const { type, ...params } = cmd;
  
  switch (type) {
    case 'navigate':
      return await controller.navigate(params.url, params);
    case 'click':
      return await controller.click(params.selector, params);
    case 'fill':
      return await controller.fill(params.selector, params.text, params);
    case 'type':
      return await controller.type(params.selector, params.text, params);
    case 'press':
      return await controller.press(params.key);
    case 'upload':
      return await controller.upload(params.selector, params.files, params);
    case 'screenshot':
      return await controller.screenshot(params.path, params);
    case 'evaluate': {
      const script = params.file
        ? fs.readFileSync(path.resolve(process.cwd(), params.file), 'utf8')
        : params.script;
      return await controller.evaluate(script);
    }
    case 'wait_for_selector':
      return await controller.waitForSelector(params.selector, params);
    case 'get_text':
      return await controller.getText(params.selector);
    case 'get_all_text':
      return await controller.getAllText(params.selector);
    case 'start_intercept':
      return await controller.startIntercept(params.url_pattern);
    case 'get_intercepted':
      return controller.getInterceptedResponses();
    case 'clear_intercepted':
      return controller.clearInterceptedResponses();
    case 'wait':
      return await controller.wait(params.seconds || 1);
    default:
      return { success: false, error: `Unknown command: ${type}` };
  }
}

async function main() {
  const args = process.argv.slice(2);
  const keepTab = args.includes('--keep-tab');
  
  if (args.length < 2) {
    console.log('用法:');
    console.log('  node cdp_controller.js --ws <websocket-url> --commands <commands.json>');
    console.log('  node cdp_controller.js --ws <websocket-url> --interactive');
    console.log('');
    console.log('示例:');
    console.log('  node cdp_controller.js --ws "ws://127.0.0.1:9222/devtools/browser/..." --commands commands.json');
    process.exit(1);
  }
  
  const wsEndpoint = args[args.indexOf('--ws') + 1];
  const controller = new CDPController(wsEndpoint);
  
  if (!await controller.connect()) {
    process.exit(1);
  }
  
  try {
    if (args.includes('--commands')) {
      const commandsFile = args[args.indexOf('--commands') + 1];
      const commands = JSON.parse(fs.readFileSync(commandsFile, 'utf8'));
      
      const results = [];
      for (const cmd of commands) {
        const result = await executeCommand(controller, cmd);
        results.push({ type: cmd.type, ...result });
      }
      
      console.log(JSON.stringify(results, null, 2));
    } else if (args.includes('--interactive')) {
      console.error('交互模式 (输入 JSON 命令, Ctrl+D 退出)');
      // 简化版,实际使用时可以添加 readline
      console.error('提示: 使用 --commands 模式更方便');
    }
  } finally {
    await controller.close({ keepTab });
  }
}

if (require.main === module) {
  main().catch(err => {
    console.error('错误:', err);
    process.exit(1);
  });
}

module.exports = { CDPController, executeCommand };
