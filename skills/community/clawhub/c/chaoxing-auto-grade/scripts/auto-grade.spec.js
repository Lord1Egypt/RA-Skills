import { test } from '@playwright/test';
const https = require('https');
const fs = require('fs');
const path = require('path');

// 加载配置
const configPath = path.join(__dirname, '..', 'config.json');
let CONFIG = {
  username: '',
  password: '',
  courseName: '',
  apiKey: '',
  model: 'qwen-plus',
  minScore: 60,
  maxScore: 99,
  chromePath: ''
};

try {
  const configFile = fs.readFileSync(configPath, 'utf8');
  CONFIG = { ...CONFIG, ...JSON.parse(configFile) };
} catch (e) {
  console.log('⚠️ 未找到配置文件，请检查 config.json');
}

// 检查必要配置
if (!CONFIG.username || !CONFIG.password || !CONFIG.apiKey) {
  console.log('❌ 请先在 config.json 中配置 username, password 和 apiKey');
  process.exit(1);
}

async function callQwenAPI(studentAnswer, questionNumber) {
  const prompt = `你是老师，请根据以下标准评价学生的答案并给出分数（${CONFIG.minScore}-${CONFIG.maxScore}分）：
- 答案完整性
- 准确性  
- 逻辑清晰度

学生答案（第${questionNumber}题）：
${studentAnswer}

请直接给出分数（只输出一个数字，不要其他文字），分数范围${CONFIG.minScore}-${CONFIG.maxScore}分。`;

  const postData = JSON.stringify({
    model: CONFIG.model,
    input: { messages: [{ role: 'system', content: '你是一个严格的教育评分助手。' }, { role: 'user', content: prompt }] },
    parameters: { result_format: 'message' }
  });

  return new Promise((resolve) => {
    const req = https.request({
      hostname: 'dashscope.aliyuncs.com',
      path: '/api/v1/services/aigc/text-generation/generation',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${CONFIG.apiKey}`, 'X-DashScope-Async': 'disable' }
    }, (res) => {
      let data = '';
      res.on('data', (c) => data += c);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          const score = result?.output?.choices?.[0]?.message?.content?.trim() || '75';
          const num = parseInt(score.match(/\d+/)?.[0] || '75');
          resolve(Math.min(CONFIG.maxScore, Math.max(CONFIG.minScore, num)));
        } catch { resolve(75); }
      });
    });
    req.on('error', () => resolve(75));
    req.write(postData);
    req.end();
  });
}

// Playwright 配置
const testUse = {
  viewport: { width: 1920, height: 1080 },
  headless: false,
  slowMo: 300,
  ignoreHTTPSErrors: true,
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  launchOptions: { args: ['--lang=zh-CN'], env: { LANGUAGE: 'zh_CN.UTF-8' } },
  timeout: 600000
};

if (CONFIG.chromePath) {
  testUse.executablePath = CONFIG.chromePath;
}

test.use(testUse);
test.setTimeout(600000);

// 根据课程名选择课程
async function selectCourse(page1, courseName) {
  const iframe = page1.frameLocator('iframe[name="frame_content"]');
  await page1.waitForTimeout(2000);
  
  if (!courseName) {
    console.log('未指定课程名，选择第一个课程');
    await iframe.getByRole('link').nth(2).click();
    return true;
  }
  
  const courseLinks = await iframe.locator(`a:has-text("${courseName}")`).all();
  if (courseLinks.length > 0) {
    console.log(`找到课程: ${courseName}`);
    await courseLinks[0].click();
    return true;
  }
  
  console.log(`未找到课程: ${courseName}，选择第一个课程`);
  await iframe.getByRole('link').nth(2).click();
  return true;
}

// 在当前页面找有 Unreview > 0 的作业并点击
async function findAndClickUnreview(iframe) {
  const bodyText = await iframe.locator('body').innerText();
  const lines = bodyText.split('\n');
  
  for (const line of lines) {
    const match = line.match(/(\d+)\s*Unreview/i);
    if (match && parseInt(match[1]) > 0) {
      console.log(`找到作业有 ${parseInt(match[1])} 份待批改`);
      
      const reviewButtons = await iframe.locator('a:has-text("Review")').all();
      for (const btn of reviewButtons) {
        const parentText = await btn.evaluateHandle((el) => {
          let container = el.parentElement;
          for (let i = 0; i < 10 && container; i++) {
            if (container.textContent.includes('Unreview')) return container.innerText;
            container = container.parentElement;
          }
          return '';
        });
        
        const text = await parentText.jsonValue();
        const m = text.match(/(\d+)\s*Unreview/i);
        if (m && parseInt(m[1]) > 0) {
          console.log(`点击有 ${parseInt(m[1])} 份待批改的作业`);
          await btn.click();
          return { found: true, count: parseInt(m[1]) };
        }
      }
    }
  }
  
  return { found: false, count: 0 };
}

// 检查是否有下一页并点击
async function clickNextPage(iframe) {
  return await iframe.locator('body').evaluate(() => {
    const pageDiv = document.getElementById('page');
    if (!pageDiv) return false;
    
    const links = pageDiv.querySelectorAll('a');
    for (const a of links) {
      const text = a.textContent?.trim();
      if (text === '>' || text === '»' || text === '下一页' || text === 'Next') {
        if (a.classList.contains('disabled') || a.classList.contains('active')) {
          return false;
        }
        a.click();
        return true;
      }
    }
    
    const currentSpan = pageDiv.querySelector('span.current, .active');
    if (currentSpan) {
      const nextLink = currentSpan.nextElementSibling;
      if (nextLink && nextLink.tagName === 'A') {
        nextLink.click();
        return true;
      }
    }
    
    return false;
  });
}

test('AI自动批改作业', async ({ page }) => {
  console.log('\n========== 配置信息 ==========');
  console.log(`用户名: ${CONFIG.username}`);
  console.log(`课程名: ${CONFIG.courseName || '(未指定，将选择第一个)'}`);
  console.log(`AI模型: ${CONFIG.model}`);
  console.log(`分数范围: ${CONFIG.minScore}-${CONFIG.maxScore}`);
  console.log('==============================\n');
  
  // 登录
  await page.goto('https://passport2.chaoxing.com/login');
  await page.getByRole('textbox', { name: '手机号/超星号' }).fill(CONFIG.username);
  await page.getByRole('textbox', { name: '学习通密码' }).fill(CONFIG.password);
  await page.getByRole('button', { name: '登录' }).click();
  await page.waitForTimeout(2000);

  const page1Promise = page.waitForEvent('popup');
  await selectCourse(page, CONFIG.courseName);
  const page1 = await page1Promise;

  await page1.getByRole('link', { name: '作业' }).click();
  await page1.waitForTimeout(3000);

  let totalGraded = 0;
  let currentPage = 1;

  // 外层循环：翻页
  while (true) {
    console.log(`\n========== 第 ${currentPage} 页 ==========`);
    
    if (page1.isClosed()) break;

    const iframe = page1.frameLocator('iframe[name="frame_content-zy"]');
    await page1.waitForTimeout(2000);

    // 内层循环：处理当前页的所有作业
    while (true) {
      try {
        const result = await findAndClickUnreview(iframe);
        
        if (!result.found) {
          console.log('当前页没有待批改的作业');
          break;
        }
        
        await page1.waitForTimeout(3000);
        
        // 点击 Unreview 筛选
        await iframe.locator('body').evaluate(() => {
          const btn = Array.from(document.querySelectorAll('a')).find(a => a.textContent.trim() === 'Unreview');
          if (btn) btn.click();
        });
        await page1.waitForTimeout(2000);
        
        const frame2 = page1.locator('iframe[name="frame_content-zy"]').contentFrame();
        let remaining = await frame2.locator('a[onclick*="toMarkWork"]').count();
        console.log(`Unreview 列表中有 ${remaining} 份待批改`);
        
        if (remaining === 0) {
          await page1.goBack();
          await page1.waitForTimeout(2000);
          continue;
        }

        // 批改当前作业的所有学生
        while (remaining > 0) {
          console.log(`\n--- 批改 (剩余 ${remaining}) ---`);
          
          const page2Promise = page1.context().waitForEvent('page', { timeout: 10000 }).catch(() => null);
          await frame2.locator('a[onclick*="toMarkWork"]').first().click();
          const page2 = await page2Promise;

          if (!page2) break;

          await page2.waitForLoadState('domcontentloaded').catch(() => {});
          await page2.waitForTimeout(2000);
          await page2.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await page2.waitForTimeout(1000);

          // 读取答案并评分
          const answerElements = await page2.locator('[class*="answer"]').all();
          let questionCount = 0, totalScore = 0;

          for (const el of answerElements) {
            const text = await el.textContent();
            if (text.includes('Students answer')) {
              const match = text.match(/Students answer：([\s\S]*?)(?=Correct answer|$)/);
              if (match && match[1].trim().length > 10) {
                questionCount++;
                console.log(`题目 ${questionCount}: 评分中...`);
                const score = await callQwenAPI(match[1].trim(), questionCount);
                console.log(`→ ${score}分`);
                totalScore += score;
              }
            }
          }

          const finalScore = Math.round(totalScore / Math.max(questionCount, 1));
          console.log(`总分: ${finalScore} (${questionCount}题)`);

          // 填入总分
          const scoreInput = page2.locator('#tmpscore');
          if (await scoreInput.count() > 0) {
            await scoreInput.click();
            await scoreInput.fill(finalScore.toString());
            await page2.waitForTimeout(500);
            console.log('已填入分数');
          }

          await page2.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
          await page2.waitForTimeout(500);

          // 提交成绩: Submit → Confirm → Continue
          console.log('\nSubmit...');
          await page2.evaluate(() => {
            const a = Array.from(document.querySelectorAll('a')).find(a => a.textContent.trim() === 'Submit');
            if (a) a.click();
          });
          await page2.waitForTimeout(3000);

          console.log('Confirm...');
          try {
            await page2.waitForSelector('a.confirm', { state: 'visible', timeout: 5000 });
            await page2.click('a.confirm');
            console.log('Confirm 点击成功');
          } catch {
            await page2.evaluate(() => {
              const a = document.querySelector('a.confirm');
              if (a) a.click();
            });
          }
          await page2.waitForTimeout(3000);

          console.log('Continue (confirmHref)...');
          try {
            await page2.waitForSelector('a.confirmHref', { state: 'visible', timeout: 5000 });
            await page2.click('a.confirmHref');
            console.log('Continue 点击成功');
          } catch {
            await page2.evaluate(() => {
              const a = document.querySelector('a.confirmHref');
              if (a) a.click();
            });
          }
          await page2.waitForTimeout(3000);

          try { if (!page2.isClosed()) await page2.close(); } catch {}

          totalGraded++;
          console.log(`✅ 已批改 ${totalGraded} 份`);
          
          // 刷新当前作业列表
          await page1.reload();
          await page1.waitForTimeout(3000);
          
          // 重新点击 Unreview 筛选
          const newIframe = page1.frameLocator('iframe[name="frame_content-zy"]');
          await newIframe.locator('body').evaluate(() => {
            const btn = Array.from(document.querySelectorAll('a')).find(a => a.textContent.trim() === 'Unreview');
            if (btn) btn.click();
          });
          await page1.waitForTimeout(2000);
          
          remaining = await page1.locator('iframe[name="frame_content-zy"]').contentFrame().locator('a[onclick*="toMarkWork"]').count();
          console.log(`刷新后剩余: ${remaining} 份`);
        }
        
        console.log('该作业批改完成，返回作业列表');
        await page1.goBack();
        await page1.waitForTimeout(2000);
        
      } catch (e) {
        console.log('出错:', e.message?.substring(0, 150));
        try {
          await page1.goBack();
          await page1.waitForTimeout(2000);
        } catch {}
        break;
      }
    }
    
    // 尝试翻到下一页
    console.log('\n检查是否有下一页...');
    const hasNextPage = await clickNextPage(iframe);
    
    if (hasNextPage) {
      currentPage++;
      console.log(`翻到第 ${currentPage} 页`);
      await page1.waitForTimeout(3000);
    } else {
      console.log('没有更多页面了');
      break;
    }
  }

  console.log(`\n🎉 任务完成！共批改 ${totalGraded} 份作业`);
});
