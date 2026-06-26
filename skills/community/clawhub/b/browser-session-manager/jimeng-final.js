const { chromium } = require('playwright');
const fs = require('fs');

async function run() {
  const sessionData = JSON.parse(fs.readFileSync('/tmp/jimeng-session.json', 'utf8'));
  
  console.log('🌐 启动浏览器...');
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  // 设置 cookies
  if (sessionData.cookies) {
    console.log(`🍪 设置 cookies...`);
    for (const cookie of sessionData.cookies) {
      try {
        let sameSite = cookie.sameSite;
        if (sameSite === 'unspecified' || sameSite === 'no_restriction') sameSite = undefined;
        else if (sameSite === 'strict') sameSite = 'Strict';
        else if (sameSite === 'lax') sameSite = 'Lax';
        
        const formattedCookie = {
          name: cookie.name,
          value: cookie.value,
          domain: cookie.domain,
          path: cookie.path || '/',
          secure: cookie.secure || false,
          httpOnly: cookie.httpOnly || false
        };
        
        if (sameSite) formattedCookie.sameSite = sameSite;
        if (cookie.expirationDate) {
          formattedCookie.expires = Math.floor(new Date(cookie.expirationDate).getTime() / 1000);
        }
        
        await context.addCookies([formattedCookie]);
      } catch (e) {}
    }
  }

  // 访问页面
  console.log('🔗 访问即梦AI...');
  await page.goto('https://jimeng.jianying.com/ai-tool/home?type=video', { 
    waitUntil: 'networkidle',
    timeout: 60000 
  });

  // 设置 localStorage
  if (sessionData.localStorage) {
    await page.evaluate((data) => {
      for (const [key, value] of Object.entries(data)) {
        try { localStorage.setItem(key, value); } catch (e) {}
      }
    }, sessionData.localStorage);
  }

  // 刷新页面
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);
  
  console.log('📸 步骤 0: 初始截图...');
  await page.screenshot({ path: '/tmp/jimeng_final_step0.png' });

  // 步骤 1: 点击 Seedance 2.0 Fast 展开下拉菜单
  console.log('📸 步骤 1: 点击模型选择器...');
  try {
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(1000);
    
    await page.getByText('Seedance 2.0 Fast').first().click();
    console.log('✅ 已点击 Seedance 2.0 Fast');
    await page.waitForTimeout(2000);
    
    // 选择 Seedance 2.0
    const options = await page.locator('text=Seedance 2.0').all();
    for (const option of options) {
      const text = await option.textContent();
      if (text && text.includes('Seedance 2.0') && !text.includes('Fast')) {
        await option.click({ force: true });
        console.log('✅ 已选择 Seedance 2.0');
        break;
      }
    }
    await page.waitForTimeout(2000);
  } catch (e) {
    console.log('⚠️ 步骤1:', e.message);
  }
  await page.screenshot({ path: '/tmp/jimeng_final_step1.png' });

  // 步骤 2 & 3: 点击文本框并输入文字
  console.log('📸 步骤 2&3: 输入文字...');
  const promptText = '穿着黑色羽绒服的年轻男子忙完一天工作，满脸疲惫，他走进电梯，按下18楼。电梯门开后，他走到1803房间门前，在密码锁上按下指纹，门开了。门内温馨的家庭装修，一个可爱的小女孩面对男子跑了过来，嘴里喊着爸爸，爸爸，抱住男子。男子脸上的疲惫一扫而光，开心地笑了，非常幸福';
  
  try {
    // 尝试多种方式找到输入框
    // 方式1: 通过 placeholder
    let textarea = await page.locator('textarea[placeholder*="输入文字"]').first();
    try { await textarea.waitFor({ timeout: 5000 }); } catch (e) { textarea = null; }
    
    // 方式2: 通过 contenteditable
    if (!textarea) {
      textarea = await page.locator('[contenteditable="true"]').first();
      try { await textarea.waitFor({ timeout: 5000 }); } catch (e) { textarea = null; }
    }
    
    // 方式3: 任何 textarea
    if (!textarea) {
      textarea = await page.locator('textarea').first();
    }
    
    if (textarea) {
      await textarea.click();
      await page.waitForTimeout(500);
      await textarea.fill(promptText);
      console.log('✅ 文本已输入');
    }
    await page.waitForTimeout(1000);
  } catch (e) {
    console.log('⚠️ 步骤2&3:', e.message);
  }
  await page.screenshot({ path: '/tmp/jimeng_final_step3.png' });

  // 步骤 4: 点击 5s 选择 15s
  console.log('📸 步骤 4: 选择 15s...');
  try {
    // 找到 5s 按钮并点击
    const durationBtn = await page.locator('text=5s').first();
    await durationBtn.click({ timeout: 10000 });
    console.log('✅ 已点击 5s');
    await page.waitForTimeout(1500);
    
    // 选择 15s
    await page.getByText('15s').first().click({ timeout: 10000 });
    console.log('✅ 已选择 15s');
    await page.waitForTimeout(1500);
  } catch (e) {
    console.log('⚠️ 步骤4:', e.message);
  }
  await page.screenshot({ path: '/tmp/jimeng_final_step4.png' });

  // 步骤 5: 点击正确的提交按钮（圆形黑色带箭头，旁边有60积分显示）
  console.log('📸 步骤 5: 点击提交按钮...');
  try {
    // 查找圆形提交按钮 - 根据描述：黑色圆形，白色上箭头，旁边有"60"
    // 通常是 input 区域右侧的圆形按钮
    
    // 方法1: 查找包含箭头的圆形按钮
    const submitBtn = await page.locator('button[class*="submit"], button[class*="send"], [class*="circle"]:has(svg), button:has([class*="arrow"])').last();
    await submitBtn.click({ timeout: 10000 });
    console.log('✅ 已点击提交按钮');
  } catch (e) {
    console.log('⚠️ 方法1失败，尝试坐标点击:', e.message);
    // 方法2: 坐标点击（根据截图，按钮在右下角，积分"60"旁边）
    try {
      // 先找到包含 "60" 的元素，然后点击它旁边的圆形按钮
      const creditText = await page.getByText('60').first();
      const box = await creditText.boundingBox();
      if (box) {
        // 点击"60"右侧的圆形按钮（大约偏移50像素）
        await page.mouse.click(box.x + box.width + 30, box.y + box.height/2);
        console.log('✅ 已通过坐标点击提交按钮');
      }
    } catch (e2) {
      console.log('⚠️ 坐标点击也失败:', e2.message);
    }
  }
  
  await page.waitForTimeout(3000);
  console.log('📸 步骤 6: 提交后截图...');
  await page.screenshot({ path: '/tmp/jimeng_final_step6_submit.png', fullPage: true });

  // 等待5秒后再次截图
  console.log('⏱️ 等待 5 秒...');
  await page.waitForTimeout(5000);
  console.log('📸 步骤 6: 5秒后截图...');
  await page.screenshot({ path: '/tmp/jimeng_final_step6_after5s.png', fullPage: true });
  
  console.log('✅ 任务完成！');
  await browser.close();
}

run().catch(console.error);
