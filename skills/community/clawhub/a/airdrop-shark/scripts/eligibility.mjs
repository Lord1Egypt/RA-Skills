#!/usr/bin/env node
/**
 * 🪂 AirdropAlert - 资格检查
 * 检查用户地址是否符合特定项目的空投资格

模拟数据版本：实际应查询链上数据
 */

// 简化的资格检查 (模拟数据，实际应查询链上数据)
function checkEligibility(project, address = null) {
    const defaultAddress = '0x33f9...5ad9';
    const addr = address || defaultAddress;
    
    // 模拟检查结果
    const checks = {
        layerzero: {
            name: 'LayerZero',
            passed: true,
            requirements: [
                { name: '跨链交易 > 5 次', met: true, actual: '12 次' },
                { name: '使用 > 3 条不同链', met: true, actual: '5 条链' },
                { name: '总交易量 > $1000', met: true, actual: '$5,420' },
                { name: '最近 30 天活跃', met: true, actual: '3 天前' }
            ],
            expectedValue: '$2000-5000',
            confidence: '高'
        },
        zksync: {
            name: 'zkSync Era',
            passed: true,
            requirements: [
                { name: '主网交互 > 3 次', met: true, actual: '8 次' },
                { name: '持有 NFT', met: false, actual: '无' },
                { name: '使用桥', met: true, actual: '是' }
            ],
            expectedValue: '$1000-3000',
            confidence: '中'
        },
        starknet: {
            name: 'Starknet',
            passed: false,
            requirements: [
                { name: '主网交互', met: false, actual: '无' },
                { name: '持有代币', met: false, actual: '无' }
            ],
            expectedValue: '$500-2000',
            confidence: '低'
        },
        scroll: {
            name: 'Scroll',
            passed: true,
            requirements: [
                { name: '主网交互 > 5 次', met: true, actual: '6 次' },
                { name: '使用桥', met: true, actual: '是' }
            ],
            expectedValue: '$300-1000',
            confidence: '中'
        }
    };
    
    return checks[project.toLowerCase()] || null;
}

// 显示检查结果
function showEligibility(project) {
    const address = '0x33f9...5ad9'; // 示例地址
    const result = checkEligibility(project);
    
    if (!result) {
        console.log(`❌ 未找到项目 "${project}"`);
        console.log('\n💡 支持的项目:');
        console.log('   layerzero, zksync, starknet, scroll');
        console.log('\n用法：node scripts/eligibility.mjs layerzero');
        return;
    }
    
    const statusIcon = result.passed ? '✅' : '❌';
    const statusText = result.passed ? '符合条件' : '暂未符合';
    
    console.log(`\n${statusIcon} ${result.name} 资格检查\n`);
    console.log(`地址：${address}`);
    console.log(`状态：${statusText}`);
    console.log(`\n要求:`);
    
    result.requirements.forEach(req => {
        const icon = req.met ? '✅' : '❌';
        console.log(`   ${icon} ${req.name} (${req.actual})`);
    });
    
    console.log(`\n预期空投：${result.expectedValue}`);
    console.log(`置信度：${result.confidence}`);
    
    if (!result.passed) {
        console.log(`\n💡 建议:`);
        result.requirements.filter(r => !r.met).forEach(req => {
            console.log(`   - 完成：${req.name}`);
        });
    }
    
    console.log(`\n💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`);
    console.log(`\n🪂 AirdropAlert v0.1.0 - Never Miss an Airdrop`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🪂 AirdropAlert - 资格检查

用法:
  node scripts/eligibility.mjs <project>     # 检查特定项目资格
  node scripts/eligibility.mjs layerzero     # 检查 LayerZero

支持的项目:
  layerzero   - LayerZero (多链)
  zksync      - zkSync Era (Ethereum)
  starknet    - Starknet
  scroll      - Scroll (Ethereum)

选项:
  --help, -h        显示帮助
  --address <addr>  指定检查地址
`);
    process.exit(0);
}

const project = args.find(a => !a.startsWith('--'));

if (!project) {
    console.log('❌ 请提供项目名称');
    console.log('用法：node scripts/eligibility.mjs layerzero');
    console.log('\n支持的项目：layerzero, zksync, starknet, scroll');
    process.exit(1);
}

showEligibility(project);
