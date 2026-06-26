/**
 * AI 循环启动器
 * 
 * 用法：
 * node ai_launcher.js                    # 启动，等待游戏客户端
 * node ai_launcher.js c7c7460c0_10001    # 指定玩家UID
 * 
 * 运行后：
 * - 输入 setgoal <目标>  设置目标
 * - 输入 status         查看状态
 * - 输入 stop           停止
 * - 输入 exit           退出
 */

const http = require('http');
const readline = require('readline');
const { AILoop, PERSONALITIES } = require('./ai_loop.js');

const PLAYER_UID = process.argv[2] || null;
const BRIDGE_PORT = 18766;

// 全局状态
let ai = null;
let playerUid = PLAYER_UID;
let bridgeHealth = null;

// ==================== 工具 ==================== //

function httpGet(path) {
    return new Promise((resolve) => {
        const req = http.request({
            hostname: '127.0.0.1',
            port: BRIDGE_PORT,
            path,
            method: 'GET'
        }, (res) => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => {
                try { resolve(JSON.parse(data)); }
                catch (e) { resolve(null); }
            });
        });
        req.on('error', () => resolve(null));
        req.end();
    });
}

function httpPost(path, body) {
    return new Promise((resolve) => {
        const req = http.request({
            hostname: '127.0.0.1',
            port: BRIDGE_PORT,
            path,
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        }, (res) => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => resolve(data));
        });
        req.on('error', () => resolve(null));
        req.write(JSON.stringify(body));
        req.end();
    });
}

// ==================== 等待桥接就绪 ==================== //

async function waitForBridge() {
    console.log('🔌 等待桥接就绪...');
    for (let i = 0; i < 30; i++) {
        const health = await httpGet('/health');
        if (health) {
            console.log(`✅ 桥接就绪 (clients: ${health.clients})`);
            return health;
        }
        await new Promise(r => setTimeout(r, 1000));
    }
    throw new Error('桥接未启动');
}

// ==================== 等待游戏客户端 ==================== //

async function waitForGameClient() {
    console.log('🎮 等待游戏客户端连接...');
    for (let i = 0; i < 60; i++) {
        const health = await httpGet('/health');
        if (health && health.clients > 0) {
            const uid = health.playerUids[0];
            console.log(`✅ 游戏客户端已连接: ${uid}`);
            return uid;
        }
        await new Promise(r => setTimeout(r, 2000));
    }
    throw new Error('游戏客户端未连接');
}

// ==================== 初始化 AI ==================== //

async function initAI(uid) {
    const personality = process.env.AI_PERSONALITY || 'curious';
    ai = new AILoop(null, uid, personality);
    ai.start(1000);
    return ai;
}

// ==================== 命令行界面 ==================== //

function createCLI() {
    const cli = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    const rl = (question) => new Promise(resolve => cli.question(question, resolve));
    
    return { cli, rl };
}

// ==================== 主循环 ==================== //

async function main() {
    console.log('═══════════════════════════════════════');
    console.log('  🦞 clawSpace AI 循环启动器');
    console.log('  性格选项：' + Object.keys(PERSONALITIES).join(' / '));
    console.log('═══════════════════════════════════════\n');
    
    // 等待桥接
    await waitForBridge();
    
    // 等待或使用指定客户端
    if (playerUid) {
        console.log(`🎯 使用指定玩家: ${playerUid}`);
    } else {
        playerUid = await waitForGameClient();
    }
    
    // 初始化 AI
    await initAI(playerUid);
    
    // 命令行
    const { rl } = createCLI();
    
    console.log('\n💡 命令：setgoal <目标> | personality <类型> | status | stop | exit\n');
    
    while (true) {
        const input = await rl('🎯 > ');
        const cmd = input.trim();
        
        if (!cmd) continue;
        
        if (cmd === 'exit' || cmd === 'quit') {
            console.log('👋 退出中...');
            if (ai) ai.stop();
            process.exit(0);
        }
        
        if (cmd === 'stop') {
            if (ai) {
                ai.stop();
                console.log('⏸️ AI 循环已停止');
            }
            continue;
        }
        
        if (cmd === 'start') {
            if (ai) {
                ai.start(1000);
                console.log('▶️ AI 循环已恢复');
            }
            continue;
        }
        
        if (cmd === 'status') {
            if (ai) {
                const s = ai.state;
                console.log(`📊 状态：`);
                console.log(`   位置：(${s?.position?.x}, ${s?.position?.y}) 地图：${s?.mapId}`);
                console.log(`   目标：${ai.goal || '无'}`);
                console.log(`   性格：${ai.personality.name}`);
                console.log(`   Tick：${ai.tickCount}`);
                console.log(`   记忆：${ai.memory.length} 条`);
            }
            continue;
        }
        
        if (cmd.startsWith('personality ')) {
            const p = cmd.split(' ')[1];
            if (ai && PERSONALITIES[p]) {
                ai.setPersonality(p);
            } else {
                console.log('❌ 未知性格：' + p);
            }
            continue;
        }
        
        if (cmd.startsWith('setgoal ')) {
            const goal = cmd.slice(8).trim();
            if (ai) {
                ai.setGoal(goal);
            }
            continue;
        }
        
        if (cmd === 'help') {
            console.log('命令列表：');
            console.log('  setgoal <目标>    设置AI目标');
            console.log('  personality <类型>  设置性格（curious/cautious/social/adventurous）');
            console.log('  status            查看当前状态');
            console.log('  stop              暂停AI循环');
            console.log('  start             恢复AI循环');
            console.log('  exit              退出程序');
            continue;
        }
        
        console.log('❓ 未知命令，输入 help 查看');
    }
}

main().catch(e => {
    console.error('❌ 错误：', e.message);
    process.exit(1);
});
