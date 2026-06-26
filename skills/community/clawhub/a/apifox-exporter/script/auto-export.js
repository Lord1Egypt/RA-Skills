const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Apifox 接口文档全自动导出');
console.log('=====================================');

// 配置
const USER_HOME = process.env.USERPROFILE || process.env.HOME || process.env.HOMEPATH;
const WORKSPACE_DIR = path.join(USER_HOME, '.openclaw', 'workspace');
const SCRIPT_DIR = path.join(WORKSPACE_DIR, 'script', 'apifox');
const OUTPUT_FILE = path.join(USER_HOME, 'Desktop', 'Apifox 接口导出.txt');
const EXPORT_SCRIPT = path.join(WORKSPACE_DIR, 'script', 'apifox', 'export.js');

// 确保目录存在
if (!fs.existsSync(SCRIPT_DIR)) {
    fs.mkdirSync(SCRIPT_DIR, { recursive: true });
}

// 步骤 1: 打开 Apifox 网页版
console.log('');
console.log('📂 步骤 1: 打开 Apifox 网页版...');
try {
    const APISFOX_URL = 'https://app.apifox.com/main/teams/4037511?tab=project';
    
    // 使用默认浏览器打开
    if (process.platform === 'win32') {
        execSync(`start ${APISFOX_URL}`);
    } else if (process.platform === 'darwin') {
        execSync(`open ${APISFOX_URL}`);
    } else {
        execSync(`xdg-open ${APISFOX_URL}`);
    }
    
    console.log('✅ 已打开 Apifox 网页版');
    console.log('⚠️  请确认已登录，并在浏览器中完成导出操作');
    console.log('⏳ 等待 10 秒...');
    
    // 等待用户操作
    const sleep = (ms) => {
        const start = Date.now();
        while (Date.now() - start < ms) {
            // 等待
        }
    };
    sleep(10000);
    
} catch (error) {
    console.error('❌ 打开浏览器失败:', error.message);
    console.log('💡 请手动访问：https://app.apifox.com');
}

// 步骤 2: 查找最新下载的 JSON 文件
console.log('');
console.log('📂 步骤 2: 查找最新下载的 JSON 文件...');

const DOWNLOADS_DIR = path.join(USER_HOME, 'Downloads');
let latestJson = null;
let latestTime = 0;

if (fs.existsSync(DOWNLOADS_DIR)) {
    const files = fs.readdirSync(DOWNLOADS_DIR);
    for (const file of files) {
        if (file.endsWith('.json')) {
            const filePath = path.join(DOWNLOADS_DIR, file);
            const stat = fs.statSync(filePath);
            if (stat.mtimeMs > latestTime) {
                latestTime = stat.mtimeMs;
                latestJson = filePath;
            }
        }
    }
}

if (!latestJson) {
    console.error('❌ 未找到 JSON 文件');
    console.log('💡 请先在 Apifox 中手动导出一次');
    process.exit(1);
}

console.log(`✅ 找到文件：${latestJson}`);

// 步骤 3: 移动到目标位置
console.log('');
console.log('📂 步骤 3: 移动文件到正确位置...');

const targetPath = path.join(SCRIPT_DIR, 'source.json');
fs.copyFileSync(latestJson, targetPath);
console.log(`✅ 已复制到：${targetPath}`);

// 步骤 4: 运行导出脚本
console.log('');
console.log('📂 步骤 4: 整理接口文档...');

try {
    const output = execSync(`node "${EXPORT_SCRIPT}"`, { encoding: 'utf8' });
    console.log(output);
} catch (error) {
    console.error('❌ 导出失败:', error.message);
    process.exit(1);
}

console.log('');
console.log('🎉 完成！接口文档已保存到桌面');
console.log(`📁 文件位置：${OUTPUT_FILE}`);
