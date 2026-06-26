/**
 * 班级小管家作业截图工具
 * 自动化获取学生作业图片并进行分析
 * 
 * 完整流程：
 * 【第一阶段】收集学生列表
 * 1. 进入课程详情页
 * 2. 获取"已提交"数量
 * 3. 记录当前可见学生名字与顺序
 * 4. 滚动到最后一个可见学生的位置
 * 5. 继续滚动查找新学生，追加到列表
 * 6. 重复直到学生数量与"已提交"数量一致
 * 
 * 【第二阶段】截图
 * 7. 重新进入页面（从第一个学生开始）
 * 8. 截图第一个学生（使用学生名字命名文件）
 * 9. 向下滚动400
 * 10. 截图第二个学生
 * 11. 向下滚动400
 * 12. 截图第三个学生
 * 13. ...直到截图数量与"已提交"数量一致
 * 
 * 【第三阶段】分析（下一步）
 * 14. 读取截图文件（不包含修正作业图片）
 * 15. 调用 GLM-4V 分析每张截图
 * 16. 提取学生姓名和作业提交情况（课内作业、奥数作业数量）
 * 17. 输出分析结果
 * 18. 结束
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

class BanjixiaoguanjiaCapture {
  constructor(options = {}) {
    this.cdpUrl = options.cdpUrl || 'http://localhost:9222';
    this.baseUrl = options.baseUrl || 'https://service.banjixiaoguanjia.com/appweb/';
    this.outputDir = options.outputDir || './screenshots';
    this.browser = null;
    this.page = null;
  }

  /**
   * 连接到 Chrome
   */
  async connect() {
    console.log(`连接到 Chrome: ${this.cdpUrl}`);
    this.browser = await chromium.connectOverCDP(this.cdpUrl);
    
    const contexts = this.browser.contexts();
    const context = contexts[0] || await this.browser.newContext();
    const pages = context.pages();
    
    this.page = pages.find(p => p.url().includes('banjixiaoguanjia'));
    if (!this.page) {
      this.page = await context.newPage();
      await this.page.goto(this.baseUrl);
    }
    
    await this.page.waitForLoadState('networkidle');
    console.log('✓ 已连接到 Chrome');
    return this;
  }

  /**
   * 关闭浏览器连接
   */
  async close() {
    if (this.browser) {
      await this.browser.close();
      console.log('✓ 已关闭浏览器连接');
    }
  }

  /**
   * 【第一阶段】收集学生列表
   * 进入课程并滚动收集所有学生名字
   */
  async collectStudentList(courseName) {
    console.log('\n【第一阶段】收集学生列表\n');
    
    // 1. 进入课程
    console.log('1. 进入课程...');
    await this.page.goto(this.baseUrl, { waitUntil: 'networkidle' });
    await this.page.waitForTimeout(3000);
    
    // 启用辅助功能
    await this.page.evaluate(() => {
      const el = document.querySelector('flt-semantics-placeholder');
      if (el) el.click();
    });
    await this.page.waitForTimeout(2000);
    
    // 查找课程
    for (let i = 0; i < 15; i++) {
      const found = await this.page.evaluate((name) => {
        const elements = document.querySelectorAll('flt-semantics[aria-label]');
        for (const el of elements) {
          const label = el.getAttribute('aria-label');
          if (label && label.includes(name)) return true;
        }
        // 滚动查找
        const all = document.querySelectorAll('flt-semantics[aria-label]');
        let last = null;
        for (const el of all) {
          const label = el.getAttribute('aria-label');
          if (label && (label.includes('第') || label.includes('年级'))) last = el;
        }
        if (last) last.scrollIntoView({ block: 'start' });
        return false;
      }, courseName);
      
      if (found) break;
      await this.page.waitForTimeout(1500);
    }
    
    // 点击进入课程
    await this.page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes(name)) {
          el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
          break;
        }
      }
    }, courseName);
    
    await this.page.waitForTimeout(5000);
    console.log('   ✓ 已进入课程详情页\n');
    
    // 2. 获取"已提交"数量
    console.log('2. 获取已提交数量...');
    const submittedCount = await this.page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('已提交')) {
          const match = label.match(/(\d+)/);
          if (match) return parseInt(match[0]);
        }
      }
      return null;
    });
    
    if (submittedCount) {
      console.log(`   ✓ 已提交: ${submittedCount} 人\n`);
    } else {
      console.log('   ⚠️ 未获取到已提交数量\n');
    }
    
    const targetCount = submittedCount || 3;
    
    // 3. 收集学生列表
    console.log('3. 收集学生列表...');
    const studentList = [];
    const scrollStep = 400;
    
    while (studentList.length < targetCount) {
      // 获取当前可见学生
      const visibleStudents = await this.page.evaluate(() => {
        const list = [];
        const elements = document.querySelectorAll('flt-semantics[aria-label]');
        for (const el of elements) {
          const label = el.getAttribute('aria-label');
          if (label && label.length > 20) {
            const lines = label.split(/\r?\n/);
            let name = lines[0].trim();
            // 【修复1】如果名字是纯数字，尝试从第二行获取英文名字
            if (/^\d+$/.test(name) && lines.length > 1) {
              const secondLine = lines[1].trim();
              if (secondLine && !secondLine.includes('年级') && !secondLine.includes('第')) {
                name = secondLine;
              }
            }
            if (name && name.length < 20 && !name.includes('详情') && !name.includes('查看')) {
              const rect = el.getBoundingClientRect();
              if (rect.top >= -50 && rect.top < window.innerHeight) {
                list.push({ name, top: rect.top, fullLabel: label });
              }
            }
          }
        }
        return list;
      });
      
      // 记录新学生
      for (const student of visibleStudents) {
        if (!studentList.find(s => s.name === student.name)) {
          studentList.push(student);
          console.log(`   [${studentList.length}] ${student.name}`);
          // 如果有改正补交，提示一下
          if (student.fullLabel && (student.fullLabel.includes('改正如下') || student.fullLabel.includes('改正'))) {
            console.log(`       (有改正补交作业)`);
          }
        }
      }
      
      // 检查是否已收集足够学生
      if (studentList.length >= targetCount) {
        console.log(`   ✓ 已收集 ${studentList.length} 个学生\n`);
        break;
      }
      
      // 向下滚动
      console.log(`   滚动查找更多学生...`);
      await this.page.evaluate((step) => {
        const container = document.querySelector('[style*="overflow-y: scroll"]');
        if (container) {
          container.scrollTop += step;
        }
      }, scrollStep);
      
      await this.page.waitForTimeout(1500);
    }
    
    console.log('   学生列表:');
    studentList.forEach((s, i) => console.log(`     ${i + 1}. ${s.name}`));
    console.log();
    
    return { studentList, submittedCount };
  }

  /**
   * 【第二阶段】截图所有学生
   * 按照收集的学生列表顺序截图
   */
  async captureAllStudents(studentList, courseName) {
    console.log('【第二阶段】截图\n');
    console.log('========================================');
    
    const scrollStep = 400;
    const screenshots = [];
    
    // 重新进入页面（从第一个学生开始）
    console.log('4. 重新进入页面...');
    await this.page.goto(this.baseUrl, { waitUntil: 'networkidle' });
    await this.page.waitForTimeout(3000);
    
    // 启用辅助功能
    await this.page.evaluate(() => {
      const el = document.querySelector('flt-semantics-placeholder');
      if (el) el.click();
    });
    await this.page.waitForTimeout(2000);
    
    // 查找课程
    for (let i = 0; i < 15; i++) {
      const found = await this.page.evaluate((name) => {
        const elements = document.querySelectorAll('flt-semantics[aria-label]');
        for (const el of elements) {
          const label = el.getAttribute('aria-label');
          if (label && label.includes(name)) return true;
        }
        const all = document.querySelectorAll('flt-semantics[aria-label]');
        let last = null;
        for (const el of all) {
          const label = el.getAttribute('aria-label');
          if (label && (label.includes('第') || label.includes('年级'))) last = el;
        }
        if (last) last.scrollIntoView({ block: 'start' });
        return false;
      }, courseName);
      
      if (found) break;
      await this.page.waitForTimeout(1500);
    }
    
    // 点击进入
    await this.page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes(name)) {
          el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
          break;
        }
      }
    }, courseName);
    
    await this.page.waitForTimeout(5000);
    console.log('   ✓ 已重新进入课程详情页\n');
    
    // 截图每个学生
    console.log('5. 截图每个学生...\n');
    
    for (let i = 0; i < studentList.length; i++) {
      const studentName = studentList[i].name;
      const fullLabel = studentList[i].fullLabel || '';
      
      console.log(`[${i + 1}] ${studentName}`);
      
      // 【修正作业截图】检查是否有"改正如下"或"改正"
      const hasCorrection = fullLabel.includes('改正如下') || fullLabel.includes('改正');
      
      // 截图
      const filepath = path.join(this.outputDir, `${studentName}.png`);
      await this.page.screenshot({ path: filepath, fullPage: false, timeout: 60000 });
      console.log(`   ✓ 已保存: ${studentName}.png`);
      
      screenshots.push({ name: studentName, filepath });
      
      // 【修正作业截图】如果有改正补交，额外滚动截图
      if (hasCorrection) {
        console.log(`   检测到改正补交，额外滚动截图...`);
        await this.page.evaluate((step) => {
          const container = document.querySelector('[style*="overflow-y: scroll"]');
          if (container) {
            container.scrollTop += step;
          }
        }, scrollStep);
        await this.page.waitForTimeout(1500);
        
        // 截图改正部分
        const correctionPath = path.join(this.outputDir, `${studentName}_改正.png`);
        await this.page.screenshot({ path: correctionPath, fullPage: false, timeout: 60000 });
        console.log(`   ✓ 已保存: ${studentName}_改正.png`);
        
        screenshots.push({ name: `${studentName}_改正`, filepath: correctionPath });
      }
      
      // 如果不是最后一个学生，滚动到下一个
      if (i < studentList.length - 1) {
        console.log(`   滚动: scrollTop += ${scrollStep}`);
        await this.page.evaluate((step) => {
          const container = document.querySelector('[style*="overflow-y: scroll"]');
          if (container) {
            container.scrollTop += step;
          }
        }, scrollStep);
        
        await this.page.waitForTimeout(1500);
      }
    }
    
    console.log('\n========================================');
    console.log(`\n✓ 截图完成，共 ${screenshots.length} 个学生:`);
    screenshots.forEach((s, i) => console.log(`   ${i + 1}. ${s.name}`));
    console.log(`\n输出目录: ${this.outputDir}\n`);
    
    return screenshots;
  }

  /**
   * 【第三阶段】分析作业截图
   * 使用 Qwen3.5-Plus 分析每张截图，提取学生姓名和作业提交情况
   * @param {string} screenshotDir - 截图目录
   */
  async analyzeScreenshots(screenshotDir) {
    console.log('\n【第三阶段】分析作业截图\n');
    
    const DASHSCOPE_API_KEY = process.env.DASHSCOPE_API_KEY;
    if (!DASHSCOPE_API_KEY) {
      console.log('⚠️ 未设置 DASHSCOPE_API_KEY，跳过分析');
      return null;
    }
    
    // 1. 获取截图文件（不包含修正作业图片）
    const files = fs.readdirSync(screenshotDir)
      .filter(f => f.endsWith('.png') && !f.includes('_改正'))
      .map(f => path.join(screenshotDir, f));
    
    if (files.length === 0) {
      console.log('未找到截图文件');
      return null;
    }
    
    console.log(`找到 ${files.length} 个学生作业截图\n`);
    
    // 2. 分析每张截图
    const results = [];
    
    for (const file of files) {
      const studentName = path.basename(file, '.png');
      console.log(`分析: ${studentName}`);
      
      try {
        const analysis = await this.analyzeWithQwen(file, DASHSCOPE_API_KEY);
        results.push({
          student: studentName,
          analysis: analysis
        });
      } catch (error) {
        console.error(`  分析失败: ${error.message}`);
        results.push({
          student: studentName,
          analysis: `分析失败: ${error.message}`
        });
      }
    }
    
    // 3. 输出分析结果
    console.log('\n========================================');
    console.log('  作业分析结果');
    console.log('========================================\n');
    
    for (const result of results) {
      console.log(`\n【${result.student}】`);
      console.log('-'.repeat(50));
      console.log(result.analysis);
    }
    
    console.log('\n分析完成！');
    return results;
  }

  /**
   * 使用 Qwen3.5-Plus 分析单张截图
   * @param {string} imagePath - 图片路径
   * @param {string} apiKey - DashScope API Key
   */
  async analyzeWithQwen(imagePath, apiKey) {
    const { execSync } = require('child_process');
    
    const pythonScript = `
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI
import base64

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

client = OpenAI(
    api_key="${apiKey}",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

base64_image = encode_image(r"${imagePath}")

response = client.chat.completions.create(
    model="qwen-vl-max-latest",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                },
                {
                    "type": "text",
                    "text": """分析图片中学生作业提交情况。图片中格式：
认真完成课内课后作业，并及时提交作业。
[图片][图片][图片]...（数量不固定）
认真完成奥数课后作业，并及时提交作业。
[图片][图片][图片]...（数量不固定）

要求：统计不同作业类型下的缩略图数量。

用简洁的中文回答，格式如下：
学生姓名：XXX
课内作业：X张
奥数作业：X张"""
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
`;
    
    const tempScript = path.join(path.dirname(imagePath), '_temp_analyze_qwen.py');
    fs.writeFileSync(tempScript, pythonScript, 'utf-8');
    
    try {
      const result = execSync(`python3 "${tempScript}"`, { 
        encoding: 'utf-8',
        timeout: 120000
      });
      fs.unlinkSync(tempScript);
      return result.trim();
    } catch (error) {
      if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
      throw new Error(`Qwen 分析失败: ${error.message}`);
    }
  }

  /**
   * 完整流程：进入课程、收集学生列表、截图、分析
   * @param {string} courseName - 课程名称
   * @param {string} outputDir - 输出目录（可选）
   * @param {string} apiKey - GLM API Key（可选）
   */
  async captureAndAnalyze(courseName, outputDir = null, apiKey = null) {
    try {
      // 设置输出目录
      if (outputDir) {
        this.outputDir = outputDir;
      } else {
        const desktopPath = path.join(require('os').homedir(), 'Desktop');
        this.outputDir = path.join(desktopPath, courseName);
      }
      
      // 清理旧文件
      if (fs.existsSync(this.outputDir)) {
        fs.rmSync(this.outputDir, { recursive: true });
      }
      fs.mkdirSync(this.outputDir, { recursive: true });
      
      // 连接到 Chrome
      await this.connect();
      
      // 【第一阶段】收集学生列表
      const { studentList, submittedCount } = await this.collectStudentList(courseName);
      
      // 【第二阶段】截图
      const screenshots = await this.captureAllStudents(studentList, courseName);
      
      // 【第三阶段】分析（使用 Qwen）
      const analysisResults = await this.analyzeScreenshots(this.outputDir);
      
      return {
        course: courseName,
        submittedCount,
        studentCount: studentList.length,
        students: studentList,
        screenshots: screenshots,
        analysis: analysisResults,
        outputDir: this.outputDir
      };
    } finally {
      await this.close();
    }
  }
}

module.exports = { BanjixiaoguanjiaCapture };

// 如果直接运行此文件
if (require.main === module) {
  const capture = new BanjixiaoguanjiaCapture();
  
  // 使用环境变量中的 DASHSCOPE_API_KEY 进行截图和分析
  capture.captureAndAnalyze('二下(第31节)')
    .then(result => {
      console.log('========================================');
      console.log('  批改结果');
      console.log('========================================');
      console.log(`课程: ${result.course}`);
      console.log(`已提交: ${result.submittedCount} 人`);
      console.log(`已截图: ${result.screenshots.length} 人`);
      console.log(`学生: ${result.students.map(s => s.name).join(', ')}`);
      console.log(`目录: ${result.outputDir}`);
      if (result.analysis) {
        console.log(`已分析: ${result.analysis.length} 人`);
      }
      console.log('========================================');
    })
    .catch(console.error);
}
