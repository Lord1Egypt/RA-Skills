/**
 * 班级小管家作业图片下载工具 - 修复版 v8
 * 
 * 修正点：
 * 1. 正确处理学生名字（去掉"返回"前缀）
 * 2. 进入批改页面后，根据实际显示的学生进行下载
 * 3. 每次下载后核对"当前第几张/一共多少张"
 * 4. 【v8】使用动态获取学生列表并索引点击的方式切换学生
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class BanjixiaoguanjiaDownloader {
  constructor(options = {}) {
    this.cdpUrl = options.cdpUrl || 'http://localhost:9222';
    this.baseUrl = options.baseUrl || 'https://service.banjixiaoguanjia.com/appweb/';
    this.outputDir = options.outputDir || './downloads';
    this.browser = null;
    this.page = null;
    this.analysisResults = null;
    this.courseName = null;
  }

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

  async close() {
    if (this.browser) {
      await this.browser.close();
      console.log('✓ 已关闭浏览器连接');
    }
  }

  loadAnalysisResults(analysisFile) {
    if (!fs.existsSync(analysisFile)) {
      throw new Error(`分析结果文件不存在: ${analysisFile}`);
    }
    const content = fs.readFileSync(analysisFile, 'utf-8');
    this.analysisResults = JSON.parse(content);
    console.log(`✓ 已加载分析结果，共 ${this.analysisResults.length} 个学生`);
    return this.analysisResults;
  }

  /**
   * 获取当前页面信息（学生名字、当前张数、总张数）
   * 页面顶部元素[7]显示: "Zoey的作业(8/8)"（不包含"返回"前缀）
   */
  async getCurrentPageInfo() {
    return await this.page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      // 优先检查元素[7]（页面顶部标题，不包含"返回"前缀）
      if (elements[7]) {
        const text = elements[7].textContent || elements[7].getAttribute('aria-label') || '';
        const match = text.match(/(.+?)的作业\((\d+)\/(\d+)\)/);
        if (match) {
          return {
            student: match[1].trim(),  // 学生名字（不含"返回"前缀）
            current: parseInt(match[2]),
            total: parseInt(match[3]),
            elementIndex: 7
          };
        }
      }
      // 备用：遍历所有元素查找
      for (let i = 0; i < elements.length; i++) {
        const text = elements[i].textContent || elements[i].getAttribute('aria-label') || '';
        const match = text.match(/(.+?)的作业\((\d+)\/(\d+)\)/);
        if (match) {
          let studentName = match[1].trim();
          // 去掉"返回"前缀（兼容旧版本）
          studentName = studentName.replace(/^返回/, '');
          return {
            student: studentName,
            current: parseInt(match[2]),
            total: parseInt(match[3]),
            elementIndex: i
          };
        }
      }
      return null;
    });
  }

  /**
   * 进入课程并点击第一个学生的第一张图片进入批改页面
   */
  async enterFirstStudentGradingPage(courseName) {
    console.log(`\n进入课程: ${courseName}`);
    this.courseName = courseName;
    
    // 1. 导航到首页
    await this.page.goto(this.baseUrl, { waitUntil: 'networkidle' });
    await this.page.waitForTimeout(3000);
    
    // 2. 启用辅助功能
    await this.page.evaluate(() => {
      const el = document.querySelector('flt-semantics-placeholder');
      if (el) el.click();
    });
    await this.page.waitForTimeout(2000);
    
    // 3. 查找并点击课程
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
    console.log('✓ 已进入课程详情页');
    
    // 4. 点击第一个学生的第一张图片
    console.log('点击第一个学生的第一张图片...');
    
    const firstImage = await this.page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      for (let i = 0; i < elements.length; i++) {
        const rect = elements[i].getBoundingClientRect();
        if (rect.width >= 90 && rect.width <= 95 && rect.height >= 90 && rect.height <= 95) {
          return i;
        }
      }
      return -1;
    });
    
    if (firstImage < 0) {
      throw new Error('未找到作业图片');
    }
    
    await this.page.evaluate((idx) => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[idx]) {
        elements[idx].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }
    }, firstImage);
    
    await this.page.waitForTimeout(4000);
    
    // 核对进入后的页面信息
    const info = await this.getCurrentPageInfo();
    if (info) {
      console.log(`✓ 已进入批改页面 - ${info.student}: 第${info.current}/${info.total}张`);
    } else {
      console.log('✓ 已进入批改页面');
    }
  }

  /**
   * 获取左侧学生列表（动态获取）
   * 包含点评状态检查：已点评的学生会被标记为 skip
   * @returns {Array} 学生列表 [{index, name, reviewed, skip}]
   */
  async getStudentList() {
    return await this.page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      const studentList = [];
      
      for (let i = 0; i < elements.length; i++) {
        const text = elements[i].textContent || elements[i].getAttribute('aria-label') || '';
        // 【调试】输出所有候选文本
        if (text.length > 0 && text.length < 30 && 
            !text.includes('作业') && !text.includes('图片') && 
            !text.includes('查看') && !text.includes('详情') &&
            !text.includes('2026-') && !text.includes('课内') &&
            !text.includes('奥数') && !text.includes('返回') &&
            !text.includes('没有更多') && !text.includes('收起') &&
            !text.includes('全部') && !text.includes('帮助') &&
            !text.includes('快捷键') && !text.includes('设置') &&
            !text.includes('画笔') && !text.includes('旋转') &&
            !text.includes('文字') && !text.includes('橡皮擦') &&
            !text.includes('撤销') && !text.includes('放大') &&
            !text.includes('缩小') && !text.includes('上一张') &&
            !text.includes('下一张') && !text.includes('保存')) {
          
          // 检查是否包含"已点评"标签
          const hasReviewed = text.includes('已点评');
          
          // 提取学生名字（去掉各种标签和评级）
          let studentName = text.trim();
          // 去掉"已点评"
          studentName = studentName.replace(/已点评/g, '');
          // 去掉评级（优秀、良好等）
          studentName = studentName.replace(/优秀|良好|合格|待改进/g, '');
          // 去掉数字和括号（如 (2)）
          studentName = studentName.replace(/\s*\(\d+\)\s*/g, '');
          // 清理换行符和多余空格
          studentName = studentName.replace(/[\n\r]+/g, ' ').trim();
          
          // 排除空名字
          if (studentName.length > 0) {
            studentList.push({
              index: i,
              name: studentName,
              reviewed: hasReviewed,
              skip: hasReviewed,  // 已点评的学生跳过下载
              rawText: text  // 【调试】保留原始文本
            });
          }
        }
      }
      return studentList;
    });
  }

  /**
   * 点击学生名字切换到该学生（使用动态获取的学生列表）
   * @param {string} studentName - 学生姓名
   * @returns {Object|null} 页面信息或null（如果学生已点评或切换失败）
   */
  async switchToStudent(studentName) {
    console.log(`切换到学生: ${studentName}`);
    
    // 1. 获取左侧学生列表
    const students = await this.getStudentList();
    const targetInfo = students.find(s => s.name === studentName);
    
    if (!targetInfo) {
      console.log(`  ⚠️ 未在学生列表中找到 ${studentName}`);
      console.log(`  当前学生列表: ${students.map(s => s.name).join(', ')}`);
      return null;
    }
    
    // 2. 检查是否已点评（跳过下载）
    if (targetInfo.skip) {
      console.log(`  ⏭️ ${studentName} 已点评，跳过下载`);
      return { skip: true, student: studentName, reason: '已点评' };
    }
    
    console.log(`  找到 ${studentName} 在索引 ${targetInfo.index}`);
    
    // 3. 使用索引点击
    const clicked = await this.page.evaluate((index) => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[index]) {
        elements[index].dispatchEvent(new MouseEvent('click', { bubbles: true }));
        return true;
      }
      return false;
    }, targetInfo.index);
    
    if (!clicked) {
      console.log(`  ❌ 点击失败`);
      return null;
    }
    
    // 4. 等待页面刷新
    await this.page.waitForTimeout(4000);
    
    // 5. 验证切换是否成功
    const info = await this.getCurrentPageInfo();
    if (info && info.student === studentName) {
      console.log(`✓ 已切换到 ${studentName}: 第${info.current}/${info.total}张`);
      return info;
    } else {
      console.log(`  ⚠️ 切换后显示: ${info ? `${info.student} (第${info.current}/${info.total}张)` : '未知'}`);
      return info;
    }
  }

  async downloadOriginalImage(savePath) {
    console.log(`  下载: ${path.basename(savePath)}`);
    
    const dir = path.dirname(savePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    // 点击"查看原图"按钮（元素索引8）
    await this.page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[8]) {
        elements[8].dispatchEvent(new MouseEvent('click', { bubbles: true }));
        return true;
      }
      return false;
    });
    
    await this.page.waitForTimeout(3000);
    
    // 获取所有标签页
    const context = this.page.context();
    const pages = context.pages();
    
    // 找到新打开的图片页面
    let newPage = null;
    for (const p of pages) {
      if (p !== this.page && p.url().includes('img.banjixiaoguanjia.com')) {
        newPage = p;
        break;
      }
    }
    
    // 如果出错（弹出对话框），关闭后重试一次
    if (!newPage) {
      const hasDialog = await this.page.evaluate(() => {
        const elements = document.querySelectorAll('flt-semantics');
        for (const el of elements) {
          const label = el.getAttribute('aria-label') || '';
          if (label.includes('对话框')) return true;
        }
        return false;
      });
      
      if (hasDialog) {
        console.log('  关闭对话框并重试...');
        await this.page.keyboard.press('Escape');
        await this.page.waitForTimeout(1000);
        
        await this.page.evaluate(() => {
          const elements = document.querySelectorAll('flt-semantics');
          if (elements[8]) {
            elements[8].dispatchEvent(new MouseEvent('click', { bubbles: true }));
          }
        });
        
        await this.page.waitForTimeout(3000);
        
        const pages2 = context.pages();
        for (const p of pages2) {
          if (p !== this.page && p.url().includes('img.banjixiaoguanjia.com')) {
            newPage = p;
            break;
          }
        }
      }
    }
    
    if (newPage) {
      const imageUrl = newPage.url();
      console.log(`  URL: ${imageUrl.substring(0, 60)}...`);
      
      try {
        execSync(`curl -L -o "${savePath}" "${imageUrl}"`, { timeout: 30000 });
        const fileSize = Math.round(fs.statSync(savePath).size / 1024);
        console.log(`  ✓ ${fileSize}KB`);
      } catch (error) {
        console.error(`  ✗ 失败: ${error.message}`);
      }
      
      await newPage.close();
      await this.page.waitForTimeout(500);
    } else {
      console.log('  ⚠️ 未找到图片页面');
    }
  }

  async nextImage() {
    await this.page.keyboard.press('ArrowRight');
    await this.page.waitForTimeout(1500);
  }

  async prevImage() {
    await this.page.keyboard.press('ArrowLeft');
    await this.page.waitForTimeout(1500);
  }

  /**
   * 下载单个学生的所有作业图片
   * 以页面显示的"当前第几张/一共多少张"为准
   */
  async downloadStudentImages(studentName, keNeiCount, aoShuCount) {
    console.log(`\n========================================`);
    console.log(`学生: ${studentName}`);
    console.log(`分析结果 - 课内: ${keNeiCount}张, 奥数: ${aoShuCount}张`);
    console.log(`========================================`);
    
    const studentDir = path.join(this.outputDir, this.courseName, studentName);
    const keNeiDir = path.join(studentDir, '课内');
    const aoShuDir = path.join(studentDir, '奥数');
    
    // 获取当前页面信息
    let pageInfo = await this.getCurrentPageInfo();
    if (!pageInfo) {
      console.log('⚠️ 无法获取页面信息');
      return;
    }
    
    console.log(`页面显示: ${pageInfo.student} 第${pageInfo.current}/${pageInfo.total}张`);
    
    // 核对当前学生是否正确
    if (pageInfo.student !== studentName) {
      console.log(`⚠️ 学生不匹配! 预期: ${studentName}, 实际: ${pageInfo.student}`);
      return;
    }
    
    // 以页面显示的总张数为准
    const totalCount = pageInfo.total;
    console.log(`将以页面显示的 ${totalCount}张 为准进行下载`);
    
    // 确保当前在第1张
    if (pageInfo.current !== 1) {
      console.log(`  当前在第${pageInfo.current}张，需要回到第1张`);
      // 按左键回到第1张
      for (let i = pageInfo.current; i > 1; i--) {
        await this.prevImage();
      }
      pageInfo = await this.getCurrentPageInfo();
      console.log(`  已回到第${pageInfo.current}张`);
    }
    
    // 根据分析结果分配课内和奥数
    // 如果分析结果与页面总张数不一致，以页面为准，按比例分配
    let actualKeNeiCount = keNeiCount;
    let actualAoShuCount = aoShuCount;
    
    if (totalCount !== (keNeiCount + aoShuCount)) {
      console.log(`⚠️ 张数不匹配! 分析结果: ${keNeiCount + aoShuCount}张, 页面显示: ${totalCount}张`);
      // 保持课内数量不变，调整奥数数量
      actualAoShuCount = totalCount - actualKeNeiCount;
      if (actualAoShuCount < 0) {
        actualKeNeiCount = totalCount;
        actualAoShuCount = 0;
      }
      console.log(`  调整后 - 课内: ${actualKeNeiCount}张, 奥数: ${actualAoShuCount}张`);
    }
    
    // 下载课内作业
    if (actualKeNeiCount > 0) {
      console.log(`\n下载课内作业 (${actualKeNeiCount}张)...`);
      for (let i = 1; i <= actualKeNeiCount; i++) {
        // 核对当前张数
        pageInfo = await this.getCurrentPageInfo();
        process.stdout.write(`  [第${pageInfo.current}/${pageInfo.total}张] `);
        
        if (pageInfo.current !== i) {
          console.log(`⚠️ 张数不匹配! 预期第${i}张, 实际第${pageInfo.current}张`);
        }
        
        const savePath = path.join(keNeiDir, `图片${i}.jpg`);
        await this.downloadOriginalImage(savePath);
        
        // 如果当前张数等于总张数，说明已经到最后一张
        if (pageInfo.current >= pageInfo.total) {
          console.log(`  已到最后一张，停止下载`);
          break;
        }
        
        // 切换到下一张
        await this.nextImage();
      }
    }
    
    // 下载奥数作业
    if (actualAoShuCount > 0) {
      console.log(`\n下载奥数作业 (${actualAoShuCount}张)...`);
      for (let i = 1; i <= actualAoShuCount; i++) {
        const expectedPage = actualKeNeiCount + i;
        
        // 核对当前张数
        pageInfo = await this.getCurrentPageInfo();
        process.stdout.write(`  [第${pageInfo.current}/${pageInfo.total}张] `);
        
        if (pageInfo.current !== expectedPage) {
          console.log(`⚠️ 张数不匹配! 预期第${expectedPage}张, 实际第${pageInfo.current}张`);
        }
        
        const savePath = path.join(aoShuDir, `图片${i}.jpg`);
        await this.downloadOriginalImage(savePath);
        
        // 如果当前张数等于总张数，说明已经到最后一张
        if (pageInfo.current >= pageInfo.total) {
          console.log(`  已到最后一张，停止下载`);
          break;
        }
        
        // 切换到下一张
        await this.nextImage();
      }
    }
    
    // 核对下载结果
    console.log(`\n核对 ${studentName} 的下载结果...`);
    const keNeiFiles = fs.existsSync(keNeiDir) ? fs.readdirSync(keNeiDir).filter(f => f.endsWith('.jpg')) : [];
    const aoShuFiles = fs.existsSync(aoShuDir) ? fs.readdirSync(aoShuDir).filter(f => f.endsWith('.jpg')) : [];
    
    console.log(`  课内作业: 预期 ${actualKeNeiCount} 张, 实际 ${keNeiFiles.length} 张 ${keNeiFiles.length === actualKeNeiCount ? '✓' : '⚠️'}`);
    console.log(`  奥数作业: 预期 ${actualAoShuCount} 张, 实际 ${aoShuFiles.length} 张 ${aoShuFiles.length === actualAoShuCount ? '✓' : '⚠️'}`);
    
    console.log(`✓ ${studentName} 完成`);
  }

  /**
   * 下载所有学生的作业
   */
  async downloadAll(courseName) {
    this.courseName = courseName;
    this.outputDir = path.join(require('os').homedir(), 'Desktop');
    
    // 加载分析结果
    const analysisFile = path.join(this.outputDir, courseName, 'analysis-results.json');
    this.loadAnalysisResults(analysisFile);
    
    if (!this.analysisResults || this.analysisResults.length === 0) {
      throw new Error('没有分析结果');
    }
    
    // 进入第一个学生的批改页面
    await this.enterFirstStudentGradingPage(courseName);
    
    // 获取当前页面信息
    let pageInfo = await this.getCurrentPageInfo();
    if (!pageInfo) {
      throw new Error('无法获取页面信息');
    }
    
    const currentStudent = pageInfo.student;
    console.log(`\n当前显示学生: ${currentStudent}`);
    
    // 找到当前学生在分析结果中的索引
    let currentIndex = this.analysisResults.findIndex(r => r.student === currentStudent);
    if (currentIndex < 0) {
      console.log(`⚠️ 未在分析结果中找到 ${currentStudent}，按顺序下载`);
      currentIndex = 0;
    } else {
      console.log(`✓ 找到 ${currentStudent} 在分析结果中`);
    }
    
    // 【关键】检查当前学生是否已点评
    const currentAnalysis = this.analysisResults[currentIndex];
    const studentList = await this.getStudentList();
    
    // 【调试】输出学生列表
    console.log(`\n【调试】左侧学生列表:`);
    for (const s of studentList) {
      console.log(`  [${s.index}] "${s.name}" - 已点评:${s.reviewed}, 跳过:${s.skip}, 原文:"${s.rawText}"`);
    }
    
    const currentStudentInfo = studentList.find(s => s.name === currentStudent);
    
    if (currentStudentInfo && currentStudentInfo.skip) {
      console.log(`\n⏭️ ${currentStudent} 已点评，跳过下载`);
    } else {
      if (currentStudentInfo) {
        console.log(`\n【调试】${currentStudent} 未点评或检测失败，继续下载`);
      } else {
        console.log(`\n【调试】未在列表中找到 ${currentStudent}，继续下载`);
      }
      // 下载当前学生的作业
      await this.downloadStudentImages(currentAnalysis.student, currentAnalysis.keNei || currentAnalysis.keNeiCount, currentAnalysis.aoShu || currentAnalysis.aoShuCount);
    }
    
    // 下载其他学生的作业
    for (let i = 0; i < this.analysisResults.length; i++) {
      if (i === currentIndex) continue; // 跳过已下载的学生
      
      const studentAnalysis = this.analysisResults[i];
      const newPageInfo = await this.switchToStudent(studentAnalysis.student);
      
      // 如果学生已点评，跳过下载
      if (newPageInfo && newPageInfo.skip) {
        console.log(`  ⏭️ 跳过 ${studentAnalysis.student}（已点评）`);
        continue;
      }
      
      // 如果切换成功且学生匹配，则下载
      if (newPageInfo && newPageInfo.student === studentAnalysis.student) {
        await this.downloadStudentImages(studentAnalysis.student, studentAnalysis.keNei || studentAnalysis.keNeiCount, studentAnalysis.aoShu || studentAnalysis.aoShuCount);
      } else {
        console.log(`  ⚠️ 切换失败，跳过 ${studentAnalysis.student}`);
      }
    }
    
    console.log(`\n========================================`);
    console.log(`  所有学生作业下载完成！`);
    console.log(`  输出目录: ${path.join(this.outputDir, courseName)}`);
    console.log(`========================================`);
    
    // 阶段5: 完成当前课程 - 刷新页面回到首页
    console.log(`\n阶段5: 完成当前课程`);
    console.log(`├── 所有作业下载完成`);
    await this.page.goto(this.baseUrl, { waitUntil: 'networkidle' });
    console.log(`├── ✅ 刷新班级小管家页面（已回到首页）`);
    console.log(`└── ⏳ 等待下一次作业批改命令`);
    await this.page.waitForTimeout(2000);
  }
}

// 主入口
async function main() {
  const courseName = process.argv[2] || '二下(第36节)';
  
  const downloader = new BanjixiaoguanjiaDownloader();
  
  try {
    await downloader.connect();
    await downloader.downloadAll(courseName);
    
    // 保持脚本运行，防止浏览器被关闭
    console.log('\n⏳ 下载脚本已完成，保持浏览器打开...');
    console.log('ℹ️ 您可以继续在浏览器中查看和批改作业');
    console.log('ℹ️ 完成后请按 Ctrl+C 关闭此脚本\n');
    
    // 使用 setInterval 保持事件循环活跃
    setInterval(() => {}, 5000);
    
    // 无限等待
    await new Promise(() => {});
  } catch (error) {
    console.error('下载失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main().catch(console.error);
