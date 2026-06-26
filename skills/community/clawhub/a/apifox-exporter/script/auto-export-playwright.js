const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const USER_HOME = process.env.USERPROFILE;
const SCRIPT_DIR = path.join(USER_HOME, '.openclaw', 'workspace', 'script', 'apifox');
const OUTPUT_FILE = path.join(USER_HOME, 'Desktop', 'Apifox 接口导出.txt');
const EXPORT_SCRIPT = path.join(SCRIPT_DIR, 'export.js');

// Apifox 默认配置
const DEFAULT_TEAM_NAME = '媲美智能语音';  // 默认团队名称
const DEFAULT_PROJECT_NAME = '媲美科技 - 短剧（公司）';  // 默认项目名称
const APIFOX_HOME_URL = 'https://app.apifox.com/';

// 从命令行参数获取配置
let APIFOX_TEAM_NAME = DEFAULT_TEAM_NAME;
let APIFOX_PROJECT_NAME = DEFAULT_PROJECT_NAME;

// 解析命令行参数
// 支持格式：
// - node auto-export-playwright.js 团队名 项目名
// - node auto-export-playwright.js --team=团队名 --project=项目名
// - node auto-export-playwright.js 更新接口文档 - 团队名 - 项目名
const args = process.argv.slice(2);
let argIndex = 0;

while (argIndex < args.length) {
    const arg = args[argIndex];
    
    // 解析 --team=xxx 或 --team xxx
    if (arg === '--team' || arg.startsWith('--team=')) {
        if (arg.startsWith('--team=')) {
            APIFOX_TEAM_NAME = arg.substring(7);
            argIndex++;
        } else {
            APIFOX_TEAM_NAME = args[++argIndex] || DEFAULT_TEAM_NAME;
            argIndex++;
        }
    }
    // 解析 --project=xxx 或 --project xxx
    else if (arg === '--project' || arg.startsWith('--project=')) {
        if (arg.startsWith('--project=')) {
            APIFOX_PROJECT_NAME = arg.substring(10);
            argIndex++;
        } else {
            APIFOX_PROJECT_NAME = args[++argIndex] || DEFAULT_PROJECT_NAME;
            argIndex++;
        }
    }
    // 解析 "更新接口文档 - 团队 - 项目" 格式
    else if (arg.includes('更新接口文档')) {
        const parts = arg.split('-').map(p => p.trim());
        if (parts.length >= 2 && parts[1]) {
            APIFOX_TEAM_NAME = parts[1];
        }
        if (parts.length >= 3 && parts[2]) {
            APIFOX_PROJECT_NAME = parts[2];
        }
        argIndex++;
    }
    // 解析 "默认团队 -xxx" 格式
    else if (arg.startsWith('默认团队-')) {
        APIFOX_TEAM_NAME = arg.substring(5);
        argIndex++;
    }
    // 解析 "默认项目 -xxx" 格式
    else if (arg.startsWith('默认项目-')) {
        APIFOX_PROJECT_NAME = arg.substring(5);
        argIndex++;
    }
    // 其他情况：第一个参数是团队，第二个是项目
    else {
        if (argIndex === 0) {
            APIFOX_TEAM_NAME = arg || DEFAULT_TEAM_NAME;
        } else if (argIndex === 1) {
            APIFOX_PROJECT_NAME = arg || DEFAULT_PROJECT_NAME;
        }
        argIndex++;
    }
}

// 保存登录状态的目录
const PERSISTENT_DIR = path.join(SCRIPT_DIR, 'chrome-profile');

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function autoExport() {
    console.log('🚀 Apifox 全自动导出开始（Playwright 版）');
    console.log('=====================================');
    console.log(`📋 配置信息:`);
    console.log(`   团队：${APIFOX_TEAM_NAME}${APIFOX_TEAM_NAME === DEFAULT_TEAM_NAME ? ' (默认)' : ''}`);
    console.log(`   项目：${APIFOX_PROJECT_NAME}${APIFOX_PROJECT_NAME === DEFAULT_PROJECT_NAME ? ' (默认)' : ''}`);
    console.log('');
    
    let browser;
    
    try {
        // 步骤 1: 启动浏览器
        console.log('');
        console.log('📂 步骤 1: 启动浏览器...');
        
        browser = await chromium.launchPersistentContext(PERSISTENT_DIR, {
            headless: false,
            args: ['--start-maximized'],
            viewport: { width: 1920, height: 1080 },
            acceptDownloads: true
        });
        
        console.log('✅ 浏览器已启动，下载已启用');
        
        // 获取页面
        const allPages = await browser.pages();
        page = allPages[0];
        
        // 设置下载事件监听
        console.log('📥 设置下载监听...');
        page.on('download', async (download) => {
            console.log('📥 检测到下载:', download.suggestedFilename());
            const targetPath = path.join(SCRIPT_DIR, 'source.json');
            await download.saveAs(targetPath);
            console.log(`✅ 文件已保存到：${targetPath}`);
        });
        
        // 步骤 2: 打开 Apifox 首页
        console.log('');
        console.log('📂 步骤 2: 打开 Apifox...');
        await page.goto(APIFOX_HOME_URL, { waitUntil: 'networkidle', timeout: 60000 });
        console.log('✅ 页面已加载');
        
        // 步骤 3: 检查登录状态
        console.log('');
        console.log('📂 步骤 3: 检查登录状态...');
        
        try {
            await page.waitForSelector('img[alt="avatar"]', { timeout: 10000 });
            console.log('✅ 已登录');
        } catch (error) {
            console.log('⚠️  未登录，等待登录...');
            await page.waitForSelector('img[alt="avatar"]', { timeout: 90000 });
            console.log('✅ 登录成功！');
            await sleep(2000);
        }
        
        // 步骤 4: 选择团队并查找项目
        console.log('');
        console.log('📂 步骤 4: 查找项目所在团队...');
        console.log(`🎯 目标项目：${APIFOX_PROJECT_NAME}`);
        
        // 截图查看当前页面
        await page.screenshot({ path: path.join(SCRIPT_DIR, 'debug-step4-team.png'), fullPage: true });
        
        // 先展开"我的团队"下拉菜单
        console.log('📁 展开"我的团队"...');
        try {
            // 点击左侧边栏的"我的团队"下拉按钮
            const myTeamBtn = await page.$('button:has-text("我的团队"), .team-switcher, [class*="team"]');
            if (myTeamBtn) {
                await myTeamBtn.click();
                await sleep(2000);
                console.log('✅ 已展开我的团队');
                await page.screenshot({ path: path.join(SCRIPT_DIR, 'debug-my-team-expanded.png'), fullPage: true });
            }
        } catch (e) {
            console.log('⚠️  "我的团队"可能已展开');
        }
        
        // 可能的团队列表
        const teams = ['媲美智能语音', 'shanghai', '个人团队'];
        let projectFound = false;
        
        for (const teamName of teams) {
            if (projectFound) break;
            
            console.log(`🔍 尝试团队：${teamName}`);
            
            try {
                // 点击团队（使用 XPath 更精确匹配）
                const teamLink = await page.$(`xpath=//div[contains(text(),"${teamName}")]|//span[contains(text(),"${teamName}")]`);
                if (teamLink) {
                    await teamLink.click();
                    await sleep(3000);
                    console.log(`  ✅ 已切换到：${teamName}`);
                    
                    // 截图确认
                    await page.screenshot({ path: path.join(SCRIPT_DIR, `debug-team-${teamName.replace(/[^a-zA-Z0-9]/g, '-')}.png`), fullPage: true });
                }
                
                // 查找项目（使用更宽松的选择器）
                // 项目卡片上可能显示简称，如"媲美科技 - 短剧（公司）"或"媲美科技 - 短剧"
                const keywords = ['媲美科技', '短剧', '公司'];
                for (const keyword of keywords) {
                    const projectCard = await page.$(`text=${keyword}`);
                    if (projectCard) {
                        console.log(`  ✅ 在团队"${teamName}"中找到项目（关键词：${keyword}）！`);
                        projectFound = true;
                        
                        // 点击项目卡片
                        await projectCard.click();
                        await sleep(3000);
                        console.log('✅ 已进入项目');
                        await page.screenshot({ path: path.join(SCRIPT_DIR, 'debug-entered-project.png'), fullPage: true });
                        break;
                    }
                }
                if (projectFound) break;
            } catch (e) {
                console.log(`  ⚠️  团队"${teamName}"中没有找到项目`);
            }
        }
        
        if (!projectFound) {
            console.log('❌ 在所有团队中都没找到项目');
            console.log('💡 请手动在浏览器中进入项目');
            console.log('⏳ 等待 60 秒...');
            
            for (let i = 0; i < 60; i++) {
                await sleep(1000);
                const projectCheck = await page.$(`text=${APIFOX_PROJECT_NAME}`);
                if (projectCheck) {
                    console.log('✅ 检测到已进入项目');
                    projectFound = true;
                    break;
                }
                if (i % 10 === 0 && i > 0) {
                    console.log(`   等待中... ${i}s`);
                }
            }
        }
        
        // 步骤 5: 确认项目已打开（如果步骤 4 已经点击了项目，这里跳过）
        console.log('');
        console.log('📂 步骤 5: 确认项目状态...');
        
        if (projectFound) {
            console.log('✅ 项目已在步骤 4 中打开，跳过此步骤');
            await sleep(2000);
        } else {
            console.log('⚠️  项目未打开，需要手动操作');
            console.log('💡 请在打开的浏览器中手动点击项目');
            console.log('⏳ 等待 30 秒...');
            await sleep(30000);
        }
        
        // 截图确认当前位置
        console.log('📸 截取当前页面...');
        await page.screenshot({ path: path.join(SCRIPT_DIR, 'debug-in-project.png'), fullPage: true });
        
        // 步骤 6: 打开项目设置
        console.log('');
        console.log('📂 步骤 6: 打开项目设置...');
        
        try {
            // 左侧菜单点击"项目设置"
            const settingsSelector = 'text=项目设置';
            await page.waitForSelector(settingsSelector, { timeout: 10000 });
            await page.click(settingsSelector);
            await sleep(2000);
            console.log('✅ 已打开项目设置');
        } catch (e) {
            console.log('⚠️  项目设置按钮未找到');
            console.log('💡 请检查截图：debug-in-project.png');
            await browser.close();
            return;
        }
        
        // 步骤 7: 点击导出数据
        console.log('');
        console.log('📂 步骤 7: 点击导出数据...');
        
        try {
            const exportSelector = 'text=导出数据';
            await page.waitForSelector(exportSelector, { timeout: 10000 });
            await page.click(exportSelector);
            await sleep(2000);
            console.log('✅ 已打开导出数据页面');
        } catch (e) {
            console.log('⚠️  导出数据未找到');
            await browser.close();
            return;
        }
        
        // 步骤 8: 配置导出选项
        console.log('');
        console.log('📂 步骤 8: 配置导出选项...');
        
        // 选择 OpenAPI 3.0
        try {
            const openapiSelector = 'text=OpenAPI 3.0';
            await page.waitForSelector(openapiSelector, { timeout: 5000 });
            await page.click(openapiSelector);
            console.log('✅ 已选择 OpenAPI 3.0');
        } catch (e) {}
        
        // 选择导出全部
        try {
            const exportAllSelector = 'text=导出全部';
            await page.waitForSelector(exportAllSelector, { timeout: 5000 });
            await page.click(exportAllSelector);
            console.log('✅ 已选择导出全部');
        } catch (e) {}
        
        // 选择 JSON 格式
        try {
            const jsonSelector = 'text=JSON';
            await page.waitForSelector(jsonSelector, { timeout: 5000 });
            await page.click(jsonSelector);
            console.log('✅ 已选择 JSON 格式');
        } catch (e) {}
        
        // 选择不包含 Apifox 扩展字段
        try {
            const noExtensionSelector = 'text=不包含';
            await page.waitForSelector(noExtensionSelector, { timeout: 5000 });
            await page.click(noExtensionSelector);
            console.log('✅ 已选择不包含扩展字段');
        } catch (e) {}
        
        // 步骤 9: 点击导出按钮
        console.log('');
        console.log('📂 步骤 9: 点击导出按钮...');
        
        try {
            const exportBtn = await page.waitForSelector('button:has-text("导出")', { timeout: 10000 });
            console.log('⏳ 点击导出按钮...');
            await exportBtn.click();
            console.log('✅ 已点击导出');
            
            console.log('⏳ 等待下载完成（15 秒）...');
            await sleep(15000);
        } catch (e) {
            console.log('⚠️  导出按钮点击失败:', e.message);
        }
        
        // 步骤 10: 等待下载完成并验证
        console.log('');
        console.log('📂 步骤 10: 等待下载完成...');
        
        // 额外等待确保下载事件处理完成
        await sleep(5000);
        
        const targetPath = path.join(SCRIPT_DIR, 'source.json');
        
        // 验证文件是否存在
        if (!fs.existsSync(targetPath)) {
            console.error('❌ 下载文件未保存');
            console.log('💡 请检查下载事件是否正常触发');
            await browser.close();
            return;
        }
        
        const stat = fs.statSync(targetPath);
        console.log(`✅ 下载完成！文件大小：${(stat.size / 1024).toFixed(2)} KB`);
        console.log(`📁 文件位置：${targetPath}`);
        
        // 步骤 11: 整理格式
        console.log('');
        console.log('📂 步骤 12: 整理接口文档...');
        
        try {
            const output = execSync(`node "${EXPORT_SCRIPT}"`, { encoding: 'utf8' });
            console.log(output);
        } catch (e) {
            console.error('❌ 整理失败:', e.message);
        }
        
        console.log('');
        console.log('🎉 完成！文档已保存到桌面');
        console.log(`📁 ${OUTPUT_FILE}`);
        
    } catch (error) {
        console.error('❌ 失败:', error.message);
    } finally {
        if (browser) {
            console.log('');
            console.log('🔒 关闭浏览器...');
            await browser.close();
            console.log('✅ 下次运行会自动使用保存的登录状态！');
        }
    }
}

autoExport();
