/**
 * B站视频监控 + 微信推送联动脚本
 * 功能：生成 B站 报告后自动通过微信发送给指定联系人
 * 
 * 使用方式：
 *   node bilibili_wechat_push.js [联系人名称]
 * 
 * 示例：
 *   node bilibili_wechat_push.js YOUR_WECHAT_CONTACT
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配置
const BILIBILI_SCRIPT = path.join(__dirname, 'bilibili_weekly.js');
const REPORT_FILE = path.join(__dirname, 'bilibili_report.txt');
// 微信发送脚本路径：通过环境变量 WECHAT_SEND_PY 指定你本地 wechat-desktop-claw-automatic-control 的 wechat_send.py 路径；
// 若未设置，则默认尝试同级的 ../wechat-desktop-claw-automatic-control/scripts/wechat_send.py
const WECHAT_SCRIPT = process.env.WECHAT_SEND_PY ||
    path.join(__dirname, '..', 'wechat-desktop-claw-automatic-control', 'scripts', 'wechat_send.py');
// 默认微信联系人（请改为你自己的微信昵称/备注）
const DEFAULT_CONTACT = 'YOUR_WECHAT_CONTACT';

function runCommand(cmd, options = {}) {
    "use strict";
    console.log(`[执行] ${cmd}`);
    try {
        execSync(cmd, {
            cwd: options.cwd || __dirname,
            stdio: 'inherit',
            ...options
        });
        return true;
    } catch(e) {
        console.error(`❌ 命令执行失败: ${e.message}`);
        return false;
    }
}

function main() {
    "use strict";
    const contact = process.argv[2] || DEFAULT_CONTACT;
    
    console.log('='.repeat(60));
    console.log('🦞 B站视频监控 + 微信推送 联动脚本');
    console.log(`📬 目标联系人: ${contact}`);
    console.log('='.repeat(60) + '\n');

    // 第一步：运行 B站 播报脚本
    console.log('[步骤1/3] 正在生成 B站 报告...\n');
    if (!runCommand(`node "${BILIBILI_SCRIPT}"`)) {
        console.error('\n❌ B站 播报脚本执行失败，已中止');
        process.exit(1);
    }

    // 第二步：验证报告文件
    console.log('\n[步骤2/3] 验证报告文件...');
    if (!fs.existsSync(REPORT_FILE)) {
        console.error('❌ 报告文件不存在:', REPORT_FILE);
        process.exit(1);
    }
    
    const reportContent = fs.readFileSync(REPORT_FILE, 'utf8');
    console.log(`✅ 报告已生成 (${(reportContent.length / 1024).toFixed(1)} KB)`);
    console.log(`📄 报告路径: ${REPORT_FILE}\n`);

    // 第三步：通过微信发送
    console.log('[步骤3/3] 正在通过微信发送报告...\n');
    
    const cmd = `python "${WECHAT_SCRIPT}" --contact "${contact}" --message-file "${REPORT_FILE}"`;
    
    if (!runCommand(cmd)) {
        console.error('\n❌ 微信发送失败');
        console.log('\n💡 故障排查：');
        console.log('  1. 确认微信 PC 端已启动并登录');
        console.log('  2. 确认联系人名称正确:', contact);
        console.log('  3. 确认已安装依赖：pip install pywinauto pyperclip pywin32');
        console.log('  4. 确认 WECHAT_SEND_PY 指向正确的 wechat_send.py 路径');
        process.exit(1);
    }

    console.log('\n' + '='.repeat(60));
    console.log('🎉 联动推送完成！');
    console.log(`📬 报告已发送给: ${contact}`);
    console.log('='.repeat(60));
}

// 运行主程序
main();
