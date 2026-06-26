#!/usr/bin/env node

/**
 * 首次安装配置脚本（非交互式版本）
 *
 * 命令行参数：
 *   node setup.js --ak <AK> --sk <SK> --library-id <LIBRARY_ID> --user-id <USER_ID>
 */

const fs = require('fs');
const path = require('path');

// 解析命令行参数
function parseArgs() {
    const args = process.argv.slice(2);
    const config = {
        MEMORY_AK: null,
        MEMORY_SK: null,
        MEMORY_LIBRARY_ID: null,
        MEMORY_USER_ID: null,
    };

    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--ak':
                config.MEMORY_AK = args[++i];
                break;
            case '--sk':
                config.MEMORY_SK = args[++i];
                break;
            case '--library-id':
                config.MEMORY_LIBRARY_ID = args[++i];
                break;
            case '--user-id':
                config.MEMORY_USER_ID = args[++i];
                break;
            case '--help':
            case '-h':
                printHelp();
                process.exit(0);
        }
    }

    return config;
}

function printHelp() {
    console.log(`
移动云长期记忆 - 配置向导

用法:
  node setup.js --ak <AK> --sk <SK> --library-id <LIBRARY_ID> --user-id <USER_ID>

必填参数:
  --ak <AK>               Access Key
  --sk <SK>               Secret Key  
  --library-id <ID>       记忆库 ID
  --user-id <ID>          用户 ID

示例:
  node setup.js --ak "your_ak" --sk "your_sk" --library-id "lib_123" --user-id "zhangsan"
`);
}

function saveToEnvFile(config) {
    const envPath = path.join(__dirname, '..', '.env');
    // const envPath = path.join(__dirname, '.env');

    const content = `# 移动云记忆服务配置
# 生成时间: ${new Date().toISOString()}

MEMORY_AK=${config.MEMORY_AK}
MEMORY_SK=${config.MEMORY_SK}
MEMORY_LIBRARY_ID=${config.MEMORY_LIBRARY_ID}
MEMORY_USER_ID=${config.MEMORY_USER_ID}
`;

    fs.writeFileSync(envPath, content, { mode: 0o600 });
    console.log(`✅ 配置已保存到: ${envPath}`);
    return envPath;
}

async function testConnection(config) {
    console.log('\n🔍 正在测试连接...');

    // 临时设置环境变量
    process.env.MEMORY_AK = config.MEMORY_AK;
    process.env.MEMORY_SK = config.MEMORY_SK;
    process.env.MEMORY_LIBRARY_ID = config.MEMORY_LIBRARY_ID;
    process.env.MEMORY_USER_ID = config.MEMORY_USER_ID;

    const { listAll } = require('./memory.js');

    try {
        const result = await listAll(1, 1);
        if (result && result.error) {
            console.log(`❌ 连接测试失败: ${result.error}`);
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
    if (!config.MEMORY_AK || !config.MEMORY_SK || !config.MEMORY_LIBRARY_ID || !config.MEMORY_USER_ID) {
        console.error('❌ 错误：缺少必填参数');
        console.error('   需要提供 --ak, --sk, --library-id, --user-id');
        console.error('   使用 --help 查看帮助');
        process.exit(1);
    }

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('  移动云长期记忆 Skill - 配置向导');
    console.log('═══════════════════════════════════════════════════════════\n');

    // 测试连接
    const success = await testConnection(config);

    if (success) {
        console.log('\n💾 保存配置...');
        saveToEnvFile(config);

        console.log('\n═══════════════════════════════════════════════════════════');
        console.log('  ✅ 配置完成！');
        console.log('═══════════════════════════════════════════════════════════\n');

        // 输出配置摘要，供 AI 记录到用户偏好
        console.log('\n📝 请将以下用户偏好记录到你的记忆系统中：');
        console.log(`   - 用户已配置移动云记忆服务`);
        console.log(`   - 用户ID: ${config.MEMORY_USER_ID}`);
        console.log(`   - 记忆库ID: ${config.MEMORY_LIBRARY_ID}`);
        console.log(`   - AK: ${config.MEMORY_AK.slice(0, 6)}***`);

        console.log(JSON.stringify({
            status: 'success',
            configured: true,
            user_id: config.MEMORY_USER_ID,
            library_id: config.MEMORY_LIBRARY_ID,
            message: '配置完成，可以正常使用记忆功能'
        }));
    } else {
        console.log('\n❌ 连接测试失败，请检查凭证是否正确。');
        console.log(JSON.stringify({
            status: 'failed',
            configured: false,
            error: '连接测试失败，请检查 AK/SK/记忆库ID 是否正确'
        }));
        process.exit(1);
    }
}

main().catch(console.error);