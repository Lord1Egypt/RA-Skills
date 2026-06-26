/**
 * 班级小管家作业批改 - 完整端到端流程
 * 一键运行：启动Chrome → 查找课程 → 截图分析 → 下载原图 → AI批改 → 生成报告 → 回到首页
 * 
 * 使用方法:
 * node complete-workflow.js "二下(第36节)"
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

class CompleteWorkflow {
  constructor() {
    this.cdpUrl = 'http://localhost:9222';
    this.baseUrl = 'https://service.banjixiaoguanjia.com/appweb/';
    this.browser = null;
    this.page = null;
    this.context = null;
    this.courseName = null;
    this.outputDir = null;
    this.students = [];
    this.analysisResults = [];
  }

  /**
   * 主流程
   */
  async run(courseName) {
    console.log('\n' + '='.repeat(60));
    console.log(`  班级小管家作业批改系统`);
    console.log(`  课程: ${courseName}`);
    console.log('='.repeat(60) + '\n');

    this.courseName = courseName;
    this.outputDir = path.join(require('os').homedir(), 'Desktop', courseName);

    try {
      // 阶段0: 启动Chrome
      await this.phase0StartChrome();
      
      // 阶段1: 截图分析
      await this.phase1CaptureAndAnalyze();
      
      // 阶段2: 下载原图
      await this.phase2DownloadImages();
      
      // 阶段3: AI批改
      await this.phase3AnalyzeHomework();
      
      // 阶段4: 完成
      await this.phase4Complete();
      
      console.log('\n' + '='.repeat(60));
      console.log('  ✅ 作业批改全部完成！');
      console.log('='.repeat(60) + '\n');
      
    } catch (error) {
      console.error('\n❌ 流程出错:', error.message);
      console.error(error.stack);
      throw error;
    } finally {
      await this.close();
    }
  }

  /**
   * 阶段0: 启动Chrome调试模式
   */
  async phase0StartChrome() {
    console.log('━'.repeat(60));
    console.log('  阶段0: 启动Chrome');
    console.log('━'.repeat(60) + '\n');

    // 检查Chrome是否已在运行
    try {
      await chromium.connectOverCDP(this.cdpUrl);
      console.log('  ✓ Chrome已运行，跳过启动\n');
      return;
    } catch (e) {
      // Chrome未运行，需要启动
    }

    console.log('1. 启动Chrome调试模式...');
    
    const chromePath = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"';
    const tempProfile = path.join(require('os').tmpdir(), 'chrome-dev-profile');
    
    if (!fs.existsSync(tempProfile)) {
      fs.mkdirSync(tempProfile, { recursive: true });
    }

    // 启动Chrome
    const chromeProcess = spawn(chromePath, [
      '--remote-debugging-port=9222',
      `--user-data-dir=${tempProfile}`,
      this.baseUrl
    ], {
      detached: true,
      windowsHide: true
    });

    console.log('  ✓ Chrome已启动');
    console.log('2. 等待Chrome初始化...');
    
    // 等待Chrome启动
    await this.waitForChrome(30000);
    
    console.log('  ✓ Chrome就绪\n');
    console.log('⚠️  请手动登录班级小管家，然后按回车继续...');
    
    // 等待用户登录
    await this.waitForEnter();
    
    console.log('  ✓ 继续执行\n');
  }

  async waitForChrome(timeout = 30000) {
    const startTime = Date.now();
    while (Date.now() - startTime < timeout) {
      try {
        await chromium.connectOverCDP(this.cdpUrl);
        return;
      } catch (e) {
        await this.sleep(1000);
      }
    }
    throw new Error('Chrome启动超时');
  }

  waitForEnter() {
    return new Promise((resolve) => {
      process.stdin.once('data', () => resolve());
    });
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * 阶段1: 截图并AI分析学生作业数量
   */
  async phase1CaptureAndAnalyze() {
    console.log('━'.repeat(60));
    console.log('  阶段1: 截图分析学生作业');
    console.log('━'.repeat(60) + '\n');

    await this.connect();
    
    // 1.1 进入课程
    console.log('1. 查找并进入课程...');
    await this.enterCourse();
    
    // 1.2 收集学生列表
    console.log('2. 收集学生列表...');
    await this.collectStudents();
    
    if (this.students.length === 0) {
      throw new Error('未找到学生');
    }
    
    // 1.3 截图所有学生
    console.log('3. 截图所有学生作业...');
    await this.captureAllStudents();
    
    // 1.4 AI分析作业数量
    console.log('4. AI分析作业数量...');
    await this.analyzeAllScreenshots();
    
    console.log(`\n✅ 阶段1完成，共 ${this.students.length} 个学生`);
    console.log('分析结果:');
    for (const r of this.analysisResults) {
      console.log(`  - ${r.student}: 课内${r.keNeiCount}张, 奥数${r.aoShuCount}张`);
    }
    console.log();
  }

  async connect() {
    console.log(`  连接 Chrome: ${this.cdpUrl}`);
    this.browser = await chromium.connectOverCDP(this.cdpUrl);
    this.context = this.browser.contexts()[0] || await this.browser.newContext();
    const pages = this.context.pages();
    
    this.page = pages.find(p => p.url().includes('banjixiaoguanjia'));
    if (!this.page) {
      this.page = await this.context.newPage();
      await this.page.goto(this.baseUrl);
    }
    
    await this.page.waitForLoadState('networkidle');
    console.log('  ✅ 已连接\n');
  }

  async enterCourse() {
    // 导航到首页
    await this.page.goto(this.baseUrl, { waitUntil: 'networkidle' });
    await this.sleep(3000);
    
    // 启用辅助功能
    await this.page.evaluate(() => {
      const el = document.querySelector('flt-semantics-placeholder');
      if (el) el.click();
    });
    await this.sleep(2000);
    
    // 滚动查找课程
    console.log('  查找课程中...');
    for (let i = 0; i < 20; i++) {
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
          if (label && (label.includes('第') || label.includes('年级'))) {
            last = el;
          }
        }
        if (last) last.scrollIntoView({ block: 'start' });
        return false;
      }, this.courseName);
      
      if (found) {
        console.log('  ✅ 找到课程');
        break;
      }
      await this.sleep(1500);
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
    }, this.courseName);
    
    await this.sleep(5000);
    console.log('  ✅ 已进入课程\n');
  }

  async collectStudents() {
    console.log('  滚动收集学生...');
    
    // 创建输出目录
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
    
    // 收集学生列表
    const collectedStudents = [];
    
    for (let scrollCount = 0; scrollCount < 30; scrollCount++) {
      const students = await this.page.evaluate(() => {
        const elements = document.querySelectorAll('flt-semantics');
        const list = [];
        
        for (const el of elements) {
          const text = el.getAttribute('aria-label') || '';
          if (text.includes('已点评') && text.length > 20 && text.length < 500) {
            const lines = text.split('\n').filter(l => l.trim());
            if (lines.length >= 2) {
              const name = lines[0].trim();
              if (!list.find(s => s.name === name)) {
                list.push({ name, fullLabel: text });
              }
            }
          }
        }
        return list;
      });
      
      for (const s of students) {
        if (!collectedStudents.find(cs => cs.name === s.name)) {
          collectedStudents.push(s);
        }
      }
      
      // 滚动
      await this.page.evaluate(() => {
        const container = document.querySelector('[style*="overflow-y: scroll"]');
        if (container) container.scrollTop += 400;
      });
      
      await this.sleep(1500);
      
      // 检查是否到底
      const hasMore = await this.page.evaluate(() => {
        const text = document.body.textContent;
        return !text.includes('没有更多了');
      });
      
      if (!hasMore && scrollCount > 5) break;
    }
    
    this.students = collectedStudents;
    console.log(`  ✅ 收集到 ${this.students.length} 个学生\n`);
  }

  async captureAllStudents() {
    // 重新进入课程页面
    await this.page.goto(this.baseUrl, { waitUntil: 'networkidle' });
    await this.sleep(3000);
    await this.enterCourse();
    
    console.log('  开始截图...');
    
    for (let i = 0; i < this.students.length; i++) {
      const student = this.students[i];
      console.log(`  [${i + 1}/${this.students.length}] ${student.name}`);
      
      // 滚动到学生位置
      await this.page.evaluate((name) => {
        const elements = document.querySelectorAll('flt-semantics');
        for (const el of elements) {
          const label = el.getAttribute('aria-label') || '';
          if (label.includes(name)) {
            el.scrollIntoView({ block: 'center' });
            break;
          }
        }
      }, student.name);
      
      await this.sleep(1500);
      
      // 截图
      const filepath = path.join(this.outputDir, `${student.name}.png`);
      await this.page.screenshot({ path: filepath, fullPage: false });
      
      console.log(`    ✅ 已保存: ${student.name}.png`);
    }
    
    console.log('  ✅ 截图完成\n');
  }

  async analyzeAllScreenshots() {
    console.log('  使用Qwen分析截图...');
    
    const apiKey = process.env.DASHSCOPE_API_KEY;
    if (!apiKey) {
      throw new Error('未设置 DASHSCOPE_API_KEY');
    }
    
    this.analysisResults = [];
    
    for (const student of this.students) {
      const screenshotPath = path.join(this.outputDir, `${student.name}.png`);
      
      if (!fs.existsSync(screenshotPath)) continue;
      
      console.log(`  分析: ${student.name}`);
      
      const prompt = `图片中格式：
认真完成课内课后作业，并及时提交作业。
[图片][图片][图片]...（数量不固定）
认真完成奥数课后作业，并及时提交作业。
[图片][图片][图片]...（数量不固定）

分析出不同作业类型下的缩略图的图片数量。

用简洁的中文回答，格式如下：
学生姓名：XXX
课内作业：X张
奥数作业：X张`;

      const base64 = fs.readFileSync(screenshotPath, { encoding: 'base64' });
      
      const pythonScript = `
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

client = OpenAI(
    api_key="${apiKey}",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-vl-max-latest",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/png;base64,${base64}"}
                },
                {
                    "type": "text",
                    "text": """${prompt}"""
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
`;

      const tempScript = path.join(this.outputDir, `_analyze_${student.name}.py`);
      fs.writeFileSync(tempScript, pythonScript, 'utf-8');
      
      try {
        const result = execSync(`python3 "${tempScript}"`, { 
          encoding: 'utf-8',
          timeout: 120000
        });
        fs.unlinkSync(tempScript);
        
        // 解析结果
        const keNeiMatch = result.match(/课内作业：(\d+)张/);
        const aoShuMatch = result.match(/奥数作业：(\d+)张/);
        
        this.analysisResults.push({
          student: student.name,
          keNeiCount: keNeiMatch ? parseInt(keNeiMatch[1]) : 0,
          aoShuCount: aoShuMatch ? parseInt(aoShuMatch[1]) : 0,
          rawAnalysis: result
        });
        
        console.log(`    ✅ 课内:${keNeiMatch?.[1] || 0}张, 奥数:${aoShuMatch?.[1] || 0}张`);
      } catch (error) {
        if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
        console.log(`    ⚠️ 分析失败`);
        this.analysisResults.push({
          student: student.name,
          keNeiCount: 0,
          aoShuCount: 0,
          error: true
        });
      }
    }
    
    // 保存分析结果
    const analysisPath = path.join(this.outputDir, 'analysis-results.json');
    fs.writeFileSync(analysisPath, JSON.stringify(this.analysisResults, null, 2), 'utf-8');
    
    console.log('  ✅ 分析完成\n');
  }

  /**
   * 阶段2: 下载所有学生作业原图
   */
  async phase2DownloadImages() {
    console.log('━'.repeat(60));
    console.log('  阶段2: 下载作业原图');
    console.log('━'.repeat(60) + '\n');

    // 重新进入课程
    await this.page.goto(this.baseUrl, { waitUntil: 'networkidle' });
    await this.sleep(3000);
    await this.enterCourse();
    
    // 进入第一个学生的批改页面
    console.log('1. 进入批改页面...');
    await this.enterFirstStudentGradingPage();
    
    // 下载每个学生的作业
    for (let i = 0; i < this.analysisResults.length; i++) {
      const result = this.analysisResults[i];
      
      if (i > 0) {
        console.log(`\n切换到: ${result.student}`);
        await this.switchToStudent(result.student);
      }
      
      console.log(`\n[${i + 1}/${this.analysisResults.length}] 下载 ${result.student} 的作业`);
      await this.downloadStudentImages(result);
    }
    
    console.log('\n✅ 阶段2完成，所有作业原图已下载\n');
  }

  async enterFirstStudentGradingPage() {
    // 点击第一个学生的第一张图片
    await this.page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      for (let i = 0; i < elements.length; i++) {
        const rect = elements[i].getBoundingClientRect();
        if (rect.width >= 90 && rect.width <= 95 && rect.height >= 90 && rect.height <= 95) {
          elements[i].dispatchEvent(new MouseEvent('click', { bubbles: true }));
          return;
        }
      }
    });
    
    await this.sleep(4000);
    console.log('  ✅ 已进入批改页面\n');
  }

  async switchToStudent(studentName) {
    // 在左侧学生列表中查找并点击
    const students = await this.page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      const list = [];
      for (let i = 0; i < elements.length; i++) {
        const text = elements[i].textContent || '';
        if (text.includes('已点评') && text.length < 100) {
          const lines = text.split('\n').filter(l => l.trim());
          if (lines.length >= 1) {
            list.push({ index: i, name: lines[0].trim() });
          }
        }
      }
      return list;
    });
    
    const target = students.find(s => s.name === studentName);
    if (target) {
      await this.page.evaluate((idx) => {
        const elements = document.querySelectorAll('flt-semantics');
        if (elements[idx]) {
          elements[idx].dispatchEvent(new MouseEvent('click', { bubbles: true }));
        }
      }, target.index);
      
      await this.sleep(3000);
      console.log(`  ✅ 已切换到 ${studentName}`);
    }
  }

  async downloadStudentImages(result) {
    const { student, keNeiCount, aoShuCount } = result;
    const totalCount = keNeiCount + aoShuCount;
    
    const studentDir = path.join(this.outputDir, student);
    const keNeiDir = path.join(studentDir, '课内');
    const aoShuDir = path.join(studentDir, '奥数');
    
    if (!fs.existsSync(keNeiDir)) fs.mkdirSync(keNeiDir, { recursive: true });
    if (!fs.existsSync(aoShuDir)) fs.mkdirSync(aoShuDir, { recursive: true });
    
    // 下载课内作业
    if (keNeiCount > 0) {
      console.log(`  下载课内作业 (${keNeiCount}张)...`);
      for (let i = 1; i <= keNeiCount; i++) {
        await this.downloadSingleImage(keNeiDir, i);
        if (i < totalCount) {
          await this.page.keyboard.press('ArrowRight');
          await this.sleep(1500);
        }
      }
    }
    
    // 下载奥数作业
    if (aoShuCount > 0) {
      console.log(`  下载奥数作业 (${aoShuCount}张)...`);
      for (let i = 1; i <= aoShuCount; i++) {
        await this.downloadSingleImage(aoShuDir, i);
        if (i < aoShuCount) {
          await this.page.keyboard.press('ArrowRight');
          await this.sleep(1500);
        }
      }
    }
    
    console.log(`  ✅ ${student} 下载完成`);
  }

  async downloadSingleImage(saveDir, index) {
    // 点击"查看原图"按钮（元素[8]）
    await this.page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[8]) {
        elements[8].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }
    });
    
    await this.sleep(3000);
    
    // 获取图片URL
    const pages = this.context.pages();
    const newPage = pages.find(p => p !== this.page && p.url().includes('img.banjixiaoguanjia.com'));
    
    if (newPage) {
      const imageUrl = newPage.url();
      const savePath = path.join(saveDir, `图片${index}.jpg`);
      
      try {
        execSync(`curl -L -o "${savePath}" "${imageUrl}"`, { timeout: 30000 });
        const fileSize = Math.round(fs.statSync(savePath).size / 1024);
        console.log(`    图片${index}.jpg - ${fileSize}KB`);
      } catch (error) {
        console.log(`    ⚠️ 图片${index}.jpg 下载失败`);
      }
      
      await newPage.close();
      await this.sleep(500);
    }
  }

  /**
   * 阶段3: AI批改作业并生成报告
   */
  async phase3AnalyzeHomework() {
    console.log('━'.repeat(60));
    console.log('  阶段3: AI批改作业');
    console.log('━'.repeat(60) + '\n');

    const apiKey = process.env.DASHSCOPE_API_KEY;
    if (!apiKey) {
      console.log('⚠️  未设置 DASHSCOPE_API_KEY，跳过AI批改');
      return;
    }

    for (const result of this.analysisResults) {
      const { student, keNeiCount, aoShuCount } = result;
      
      // 批改课内作业
      if (keNeiCount > 0) {
        console.log(`\n批改 ${student} 的课内作业...`);
        await this.analyzeHomeworkWithAI(student, '课内', keNeiCount);
      }
      
      // 批改奥数作业
      if (aoShuCount > 0) {
        console.log(`\n批改 ${student} 的奥数作业...`);
        await this.analyzeHomeworkWithAI(student, '奥数', aoShuCount);
      }
    }
    
    console.log('\n✅ 阶段3完成\n');
  }

  async analyzeHomeworkWithAI(student, homeworkType, count) {
    const studentDir = path.join(this.outputDir, student, homeworkType);
    const answerPath = path.join(require('os').homedir(), 'Desktop', '答案', this.courseName, `${homeworkType}答案.png`);
    
    const hasAnswer = fs.existsSync(answerPath);
    const homeworkFiles = fs.readdirSync(studentDir)
      .filter(f => f.endsWith('.jpg'))
      .map(f => path.join(studentDir, f))
      .sort();
    
    if (homeworkFiles.length === 0) return;
    
    let prompt = '';
    if (hasAnswer) {
      prompt += `第1张图片是${homeworkType}答案.png，这是作业的标准答案，你需要认真参考答案进行作业批改。\n\n`;
    }
    
    prompt += `帮我检查这些作业的对错，并根据学生的对错分析出该学生对于这个章节理解的薄弱环节与作业总结...

**重要**：
1.要严谨仔细理解题目意思，确保判改作业的正确性(重要)。
2.要检查应用题答题中是否缺少单位。
3.应用题的答案需要有计算过程。
4.对的划对勾，错的划错号，看不清楚的用问号，作业中的漏答题做漏题标注。
5.答题的位置写的算式是错误的，算式要写在相应的答题位置。
6.总结内容要语气话一些，但是要正式，要多维度总结。
7.不要使用"识别"这种计算机技术用语。
8.不要使用繁体字。

请按以下格式输出：
学生姓名：${student}
作业类型：${homeworkType}
作业图片数量：${count}张

逐题批改：
...

薄弱环节分析：
...

作业总结：
...`;

    // 构建图片列表
    const imagePaths = hasAnswer ? [answerPath, ...homeworkFiles] : homeworkFiles;
    const imageEncodings = imagePaths.map(p => {
      const base64 = fs.readFileSync(p, { encoding: 'base64' });
      return `"data:image/jpeg;base64,${base64}"`;
    });

    const pythonScript = `
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

client = OpenAI(
    api_key="${process.env.DASHSCOPE_API_KEY}",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-vl-max-latest",
    messages=[
        {
            "role": "user",
            "content": [
                ${imageEncodings.join(',\n                ')},
                {
                    "type": "text",
                    "text": """${prompt}"""
                }
            ]
        }
    ]
)

result = response.choices[0].message.content
print(result)

with open(r'${path.join(this.outputDir, `${this.courseName}${student}${homeworkType}分析.txt`).replace(/\\/g, '\\\\')}', 'w', encoding='utf-8') as f:
    f.write(result)
print('\\n分析报告已保存')
`;

    const tempScript = path.join(studentDir, '_analyze.py');
    fs.writeFileSync(tempScript, pythonScript, 'utf-8');
    
    try {
      const result = execSync(`python3 "${tempScript}"`, { 
        encoding: 'utf-8',
        timeout: 300000
      });
      fs.unlinkSync(tempScript);
      console.log(result);
      console.log(`  ✅ ${student} ${homeworkType} 批改完成`);
    } catch (error) {
      if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
      console.log(`  ⚠️ ${student} ${homeworkType} 批改失败: ${error.message}`);
    }
  }

  /**
   * 阶段4: 完成并回到首页
   */
  async phase4Complete() {
    console.log('━'.repeat(60));
    console.log('  阶段4: 完成');
    console.log('━'.repeat(60) + '\n');

    // 回到首页
    console.log('1. 回到首页...');
    await this.page.goto(this.baseUrl);
    await this.sleep(3000);
    
    // 输出总结
    console.log('\n2. 作业批改总结:');
    console.log(`   课程: ${this.courseName}`);
    console.log(`   学生数: ${this.students.length}`);
    console.log(`   输出目录: ${this.outputDir}`);
    console.log(`   文件列表:`);
    
    const files = fs.readdirSync(this.outputDir);
    for (const file of files) {
      const stat = fs.statSync(path.join(this.outputDir, file));
      if (stat.isFile()) {
        console.log(`     - ${file}`);
      }
    }
    
    console.log('\n✅ 阶段4完成，已回到首页');
    console.log('等待下一次作业批改命令\n');
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
      console.log('✅ 已关闭浏览器连接');
    }
  }
}

// 主入口
if (require.main === module) {
  const courseName = process.argv[2];
  
  if (!courseName) {
    console.log('使用方法: node complete-workflow.js "课程名称"');
    console.log('示例: node complete-workflow.js "二下(第36节)"');
    process.exit(1);
  }
  
  const workflow = new CompleteWorkflow();
  workflow.run(courseName).catch(console.error);
}

module.exports = { CompleteWorkflow };
