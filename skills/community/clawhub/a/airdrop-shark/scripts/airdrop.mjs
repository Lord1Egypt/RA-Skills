#!/usr/bin/env node
/**
 * 🪂 AirdropAlert - 空投项目列表
 * 显示所有潜在空投项目
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CONFIG_FILE = path.join(__dirname, '..', 'config', 'projects.json');

// 空投项目数据库
const DEFAULT_PROJECTS = {
    'layerzero': {
        name: 'LayerZero',
        chain: '多链',
        priority: 'high',
        snapshot: '2026-Q2',
        expectedValue: '$2000-5000',
        difficulty: '中',
        requirements: ['跨链交易 > 5 次', '使用 > 3 条不同链', '总交易量 > $1000'],
        guide: 'https://layerzero.network'
    },
    'zksync': {
        name: 'zkSync Era',
        chain: 'Ethereum',
        priority: 'high',
        snapshot: '2026-Q1',
        expectedValue: '$1000-3000',
        difficulty: '低',
        requirements: ['主网交互 > 3 次', '持有 NFT', '使用桥'],
        guide: 'https://zksync.io'
    },
    'starknet': {
        name: 'Starknet',
        chain: 'Starknet',
        priority: 'medium',
        snapshot: '已完成',
        expectedValue: '$500-2000',
        difficulty: '低',
        requirements: ['主网交互', '持有代币'],
        guide: 'https://starknet.io'
    },
    'scroll': {
        name: 'Scroll',
        chain: 'Ethereum',
        priority: 'low',
        snapshot: '2026-Q3',
        expectedValue: '$300-1000',
        difficulty: '中',
        requirements: ['主网交互 > 5 次', '使用桥'],
        guide: 'https://scroll.io'
    },
    'linea': {
        name: 'Linea',
        chain: 'Ethereum',
        priority: 'low',
        snapshot: '2026-Q2',
        expectedValue: '$300-800',
        difficulty: '低',
        requirements: ['主网交互', '使用桥'],
        guide: 'https://linea.build'
    },
    'base': {
        name: 'Base',
        chain: 'Base',
        priority: 'low',
        snapshot: '2026-Q3',
        expectedValue: '$200-600',
        difficulty: '低',
        requirements: ['主网交互', ' bridge 资产'],
        guide: 'https://base.org'
    },
    'metamask': {
        name: 'MetaMask',
        chain: '多链',
        priority: 'high',
        snapshot: '2026-Q2',
        expectedValue: '$1000-5000',
        difficulty: '中',
        requirements: ['使用 Swap', '使用桥', '活跃 > 3 个月'],
        guide: 'https://metamask.io'
    },
    'rabbit': {
        name: 'RabbitHole',
        chain: '多链',
        priority: 'medium',
        snapshot: '2026-Q2',
        expectedValue: '$200-800',
        difficulty: '低',
        requirements: ['完成 Quests', '持有 NFT'],
        guide: 'https://rabbithole.gg'
    }
};

// 优先级标记
const PRIORITY_ICONS = {
    high: '🔴',
    medium: '🟡',
    low: '🟢'
};

// 加载项目配置
function loadProjects() {
    try {
        if (fs.existsSync(CONFIG_FILE)) {
            const content = fs.readFileSync(CONFIG_FILE, 'utf8');
            return JSON.parse(content);
        }
    } catch (e) {
        console.error('⚠️  加载配置文件失败，使用默认配置');
    }
    return DEFAULT_PROJECTS;
}

// 显示项目列表
function showProjects(priority = null, limit = 20) {
    const projects = loadProjects();
    
    let list = Object.entries(projects);
    
    // 按优先级筛选
    if (priority) {
        list = list.filter(([_, p]) => p.priority === priority);
    }
    
    // 限制数量
    list = list.slice(0, limit);
    
    if (list.length === 0) {
        console.log('❌ 暂无符合条件的空投项目');
        return;
    }
    
    console.log('\n🪂 AirdropAlert - 潜在空投项目\n');
    console.log(`优先级  项目              链           快照时间    预期价值    难度`);
    console.log(`─────────────────────────────────────────────────────────────────────`);
    
    list.forEach(([key, p]) => {
        const icon = PRIORITY_ICONS[p.priority] || '⚪';
        const priorityStr = `${icon} ${p.priority === 'high' ? '高' : p.priority === 'medium' ? '中' : '低'}`.padEnd(6);
        const name = p.name.padEnd(16);
        const chain = p.chain.padEnd(12);
        const snapshot = p.snapshot.padEnd(10);
        const value = p.expectedValue.padEnd(12);
        const difficulty = p.difficulty.padEnd(6);
        
        console.log(`${priorityStr} ${name} ${chain} ${snapshot} ${value} ${difficulty}`);
    });
    
    console.log(`\n💡 提示:`);
    console.log(`   node scripts/airdrop.mjs --priority high  # 只看高优先级`);
    console.log(`   node scripts/airdrop.mjs --limit 5        # 限制显示 5 个`);
    console.log(`   node scripts/eligibility.mjs layerzero    # 检查资格`);
    console.log(`\n💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`);
    console.log(`\n🪂 AirdropAlert v0.1.0 - Never Miss an Airdrop`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🪂 AirdropAlert - 空投提醒技能

用法:
  node scripts/airdrop.mjs              # 查看所有空投项目
  node scripts/airdrop.mjs --priority high  # 只看高优先级
  node scripts/airdrop.mjs --limit 5    # 限制显示 5 个

选项:
  --help, -h          显示帮助
  --priority [high|medium|low]  按优先级筛选
  --limit N           限制显示数量
`);
    process.exit(0);
}

const priorityIndex = args.indexOf('--priority');
const priority = priorityIndex > -1 ? args[priorityIndex + 1] : null;

const limitIndex = args.indexOf('--limit');
const limit = limitIndex > -1 ? parseInt(args[limitIndex + 1]) : 20;

showProjects(priority, limit);
