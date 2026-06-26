#!/usr/bin/env node
/**
 * 抖音登录脚本
 * 用法: node scripts/login.js [--headless] [--timeout <ms>]
 */
import { DouyinUploader } from '../douyin-uploader.js';
function parseArgs(args) {
    const result = { headless: false, timeout: 180000 };
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--headless') {
            result.headless = true;
        }
        else if (args[i] === '--timeout' && args[i + 1]) {
            result.timeout = parseInt(args[i + 1], 10);
            i++;
        }
    }
    return result;
}
async function main() {
    const args = parseArgs(process.argv.slice(2));
    const uploader = new DouyinUploader();
    console.log('🚀 Starting Douyin login...');
    console.log(`   Headless: ${args.headless}`);
    console.log(`   Timeout: ${args.timeout}ms`);
    console.log('');
    const result = await uploader.login(args.headless, args.timeout);
    if (result.success) {
        console.log(`✅ Login successful!`);
        console.log(`   User: ${result.user}`);
        console.log(`   Cookies saved: ${result.cookieCount}`);
        process.exit(0);
    }
    else {
        console.log(`❌ Login failed: ${result.error}`);
        process.exit(1);
    }
}
main().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
});
//# sourceMappingURL=login.js.map