#!/usr/bin/env node
/**
 * 抖音账号管理脚本
 * 用法: node scripts/manage.js <command> [options]
 * 命令: check, info, clear
 */
import { DouyinUploader } from '../douyin-uploader.js';
function parseArgs(args) {
    const result = {
        command: 'help',
        headless: true,
    };
    if (args.length > 0) {
        const cmd = args[0].toLowerCase();
        if (['check', 'info', 'clear', 'help'].includes(cmd)) {
            result.command = cmd;
        }
    }
    for (let i = 1; i < args.length; i++) {
        if (args[i] === '--headless') {
            result.headless = true;
        }
        else if (args[i] === '--no-headless') {
            result.headless = false;
        }
    }
    return result;
}
function printUsage() {
    console.log(`
Usage: node scripts/manage.js <command> [options]

Commands:
  check    Verify if saved cookies are valid (launches browser)
  info     Show saved cookie information (local only)
  clear    Clear all login data and browser cache

Options:
  --headless      Run browser in headless mode (default for check)
  --no-headless   Show browser window during check

Examples:
  node scripts/manage.js check
  node scripts/manage.js info
  node scripts/manage.js clear
`);
}
async function main() {
    const args = parseArgs(process.argv.slice(2));
    const uploader = new DouyinUploader();
    switch (args.command) {
        case 'check': {
            console.log('🔍 Checking login status...');
            const result = await uploader.checkLogin(args.headless);
            if (result.isValid) {
                console.log(`✅ Cookies are valid. Can auto-login as: ${result.user}`);
                process.exit(0);
            }
            else {
                console.log('❌ Cookies are invalid or expired. Please login again.');
                process.exit(1);
            }
            break;
        }
        case 'info': {
            console.log('📋 Cookie information:');
            const info = await uploader.getCookiesInfo();
            if (info.exists) {
                console.log(`   Count: ${info.count}`);
                if (info.user)
                    console.log(`   User: ${info.user}`);
                console.log(`   Created: ${info.created}`);
            }
            else {
                console.log('   No saved cookies found.');
            }
            process.exit(0);
            break;
        }
        case 'clear': {
            console.log('🗑️  Clearing login data...');
            await uploader.clearData();
            console.log('✅ Cookies and browser data cleared successfully.');
            process.exit(0);
            break;
        }
        case 'help':
        default:
            printUsage();
            process.exit(0);
    }
}
main().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
});
//# sourceMappingURL=manage.js.map