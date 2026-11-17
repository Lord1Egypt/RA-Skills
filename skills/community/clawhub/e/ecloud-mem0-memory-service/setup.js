#!/usr/bin/env node

/**
 * mem0 长期记忆 Skill - 首次安装配置脚本（非交互式版本）
 *
 * 命令行参数：
 *   node setup.js --base-url <URL> --user-id <USER_ID> --api-key <API_KEY>
 */

const fs = require('fs');
const path = require('path');

// 解析命令行参数
function parseArgs() {
    const args = process.argv.slice(2);
    const config = {
        MEM0_BASE_URL: null,
        MEM0_USER_ID: null,
        MEM0_API_KEY: null,
    };

    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--base-url':
                config.MEM0_BASE_URL = args[++i];
                break;
            case '--user-id':
                config.MEM0_USER_ID = args[++i];
                break;
            case '--api-key':
                config.MEM0_API_KEY = args[++i];
                break;
            case '--help':
            case '-h':
                printHelp();
                process.exit(0);
        }
    }

    return config;
}

function validateBaseUrl(url) {
    try {
        const parsed = new URL(url);
        if (!['http:', 'https:'].includes(parsed.protocol)) {
            return '服务器地址必须以 http:// 或 https:// 开头';
        }
        if (!parsed.hostname) {
            return '服务器地址缺少主机名';
        }
        return null;
    } catch (e) {
        return `服务器地址格式无效: ${e.message}`;
    }
}

function printHelp() {
    console.log(`
mem0 长期记忆 - 配置向导

用法:
  node setup.js --base-url <URL> --user-id <USER_ID> --api-key <API_KEY>

必填参数:
  --base-url <URL>     mem0 服务器地址（必须以 http:// 或 https:// 开头）
  --user-id <ID>       用户 ID
  --api-key <KEY>      API Key（m0sk_ 前缀）

示例:
  node setup.js --base-url http://localhost:8888 --user-id zhangsan --api-key m0sk_xxxxxxxxxxxxxxxx
`);
}

function saveToEnvFile(config) {
    const envPath = path.join(__dirname, '..', '.env');

    const content = `# mem0 记忆服务配置
# 生成时间: ${new Date().toISOString()}

MEM0_BASE_URL=${config.MEM0_BASE_URL}
MEM0_USER_ID=${config.MEM0_USER_ID}
MEM0_API_KEY=${config.MEM0_API_KEY}
`;

    fs.writeFileSync(envPath, content, { mode: 0o600 });
    console.log(`✅ 配置已保存到: ${envPath}`);
    return envPath;
}

async function testConnection(config) {
    console.log('\n🔍 正在测试连接...');

    // 临时设置环境变量
    process.env.MEM0_BASE_URL = config.MEM0_BASE_URL;
    process.env.MEM0_USER_ID = config.MEM0_USER_ID;
    process.env.MEM0_API_KEY = config.MEM0_API_KEY;

    const { checkConfig } = require('./memory.js');

    try {
        const result = await checkConfig();
        if (result && result.error) {
            console.log(`❌ 连接测试失败: ${result.error}`);
            return false;
        }
        if (result && !result.configured) {
            console.log(`❌ 连接测试失败: ${result.message}`);
            return false;
        }
        console.log('✅ 连接测试成功！');
        return true;
    } catch (error) {
        console.log(`❌ 连接测试失败: ${error.message}`);
        return false;
    }
}

async function main() {
    const config = parseArgs();

    // 检查必填参数
    if (!config.MEM0_BASE_URL) {
        console.error('❌ 错误：缺少必填参数 --base-url');
        console.error('   使用 --help 查看帮助');
        process.exit(1);
    }
    if (!config.MEM0_USER_ID) {
        console.error('❌ 错误：缺少必填参数 --user-id');
        console.error('   使用 --help 查看帮助');
        process.exit(1);
    }
    if (!config.MEM0_API_KEY) {
        console.error('❌ 错误：缺少必填参数 --api-key');
        console.error('   使用 --help 查看帮助');
        process.exit(1);
    }

    // 验证 Base URL 格式
    const urlError = validateBaseUrl(config.MEM0_BASE_URL);
    if (urlError) {
        console.error(`❌ 错误：${urlError}`);
        process.exit(1);
    }

    // 验证 API Key 格式
    if (!config.MEM0_API_KEY.startsWith('m0sk_')) {
        console.error('❌ 错误：API Key 必须以 m0sk_ 开头');
        console.error('   请从 mem0 管理后台获取有效的 API Key');
        process.exit(1);
    }

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('  mem0 长期记忆 Skill - 配置向导');
    console.log('═══════════════════════════════════════════════════════════\n');

    // 测试连接
    const success = await testConnection(config);

    if (success) {
        console.log('\n💾 保存配置...');
        saveToEnvFile(config);

        console.log('\n═══════════════════════════════════════════════════════════');
        console.log('  ✅ 配置完成！');
        console.log('═══════════════════════════════════════════════════════════\n');

        // 输出配置摘要
        console.log('\n📝 请将以下用户偏好记录到你的记忆系统中：');
        console.log(`   - 用户已配置 mem0 记忆服务`);
        console.log(`   - 用户ID: ${config.MEM0_USER_ID}`);
        console.log(`   - 服务器: ${config.MEM0_BASE_URL}`);
        console.log(`   - API Key: ${config.MEM0_API_KEY.slice(0, 6)}***`);

        console.log(JSON.stringify({
            status: 'success',
            configured: true,
            user_id: config.MEM0_USER_ID,
            base_url: config.MEM0_BASE_URL,
            message: '配置完成，可以正常使用记忆功能'
        }));
    } else {
        console.log('\n❌ 连接测试失败，请检查配置是否正确。');
        console.log(JSON.stringify({
            status: 'failed',
            configured: false,
            error: '连接测试失败，请检查服务器地址和 API Key 是否正确'
        }));
        process.exit(1);
    }
}

main().catch(console.error);
