/**
 * 快速测试：设置目标后运行 AI 循环
 */
const http = require('http');
const { AILoop } = require('./ai_loop.js');

const PLAYER_UID = 'c7c7460c0_10001';
const GOAL = '去新手村找村长';

async function main() {
    // 等待游戏客户端
    for (let i = 0; i < 30; i++) {
        const health = await new Promise(r => {
            http.get('http://127.0.0.1:18766/health', res => {
                let d = '';
                res.on('data', c => d += c);
                res.on('end', () => { try { r(JSON.parse(d)); } catch(e) { r(null); } });
            }).on('error', () => r(null));
        });
        if (health && health.clients > 0) break;
        await new Promise(r => setTimeout(r, 1000));
    }

    const ai = new AILoop(null, PLAYER_UID, 'curious');
    ai.setGoal(GOAL);
    ai.start(3000);

    console.log(`\n🎯 目标：${GOAL}`);
    console.log('⏱️ 运行 90 秒后自动停止...\n');

    setTimeout(() => {
        ai.stop();
        console.log('\n✅ 测试完成');
        process.exit(0);
    }, 90000);
}

main();
