const fs = require('fs');

// 解析命令行参数
const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    params[key] = args[i + 1];
}

const { date, achievement, breakthroughs, 'growth-index': growthIndex } = params;

if (!date || !achievement) {
    console.error('❌ 缺少必要参数');
    console.log('用法: node update_evolution.js --date 2026-03-20 --achievement "成就描述" --breakthroughs "突破1,突破2" --growth-index 10');
    process.exit(1);
}

const evolutionPath = 'EVOLUTION.md';
let content = '';

if (fs.existsSync(evolutionPath)) {
    content = fs.readFileSync(evolutionPath, 'utf8');
}

// 计算天数
const dayMatch = content.match(/第(\d+)天/g);
const lastDay = dayMatch ? Math.max(...dayMatch.map(m => parseInt(m.match(/\d+/)[0]))) : 0;
const currentDay = lastDay + 1;

// 生成新的进化记录
const breakthroughsList = breakthroughs ? breakthroughs.split(',').map((b, i) => `${i + 1}. ${b.trim()}`).join('\n   ') : '（待补充）';
const stars = '⭐'.repeat(Math.min(5, Math.ceil(parseInt(growthIndex || 3) / 2)));

const newEntry = `
---

### ${date}（第${currentDay}天）

## 🌙 晚间进化总结

### 今日核心成就
**${achievement}**

### 技术突破
   ${breakthroughsList}

### 进化速度评估
今日进化速度：${stars}
总进化指数：${growthIndex || 3} 个新能力点

---

*记录时间：${new Date().toLocaleString()}*
*状态：✅ 进化记录已更新*
`;

// 追加到文件
fs.appendFileSync(evolutionPath, newEntry);

console.log('✅ 进化日志已更新');
console.log(`📅 日期: ${date}`);
console.log(`🎯 成就: ${achievement}`);
console.log(`📈 成长指数: ${growthIndex || 3}`);
console.log(`⭐ 评级: ${stars}`);
