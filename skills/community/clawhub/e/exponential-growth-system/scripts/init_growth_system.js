const fs = require('fs');
const path = require('path');

console.log('🚀 初始化指数级成长系统...\n');

// 创建目录结构
const directories = [
    '.learnings',
    'skills',
    'memory'
];

directories.forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`✅ 创建目录: ${dir}`);
    } else {
        console.log(`⏭️  目录已存在: ${dir}`);
    }
});

// 创建错误模式库
const errorPatternsPath = '.learnings/error-patterns.md';
if (!fs.existsSync(errorPatternsPath)) {
    const errorPatternsTemplate = `# 错误模式库

记录踩过的坑，避免重复犯错。

## 使用说明

每个错误模式包含：
- 日期
- 严重性（高/中/低）
- 环境
- 现象
- 根本原因
- 解决方案
- 预防措施

---

## 错误模式列表

（暂无记录）
`;
    fs.writeFileSync(errorPatternsPath, errorPatternsTemplate);
    console.log(`✅ 创建文件: ${errorPatternsPath}`);
}

// 创建工具决策图谱
const toolDecisionMapPath = '.learnings/tool-decision-map.md';
if (!fs.existsSync(toolDecisionMapPath)) {
    const toolDecisionMapTemplate = `# 工具决策图谱

什么场景用什么工具。

## 决策树

### 需求分析
1. 明确需求类型
2. 列出可选工具
3. 对比优缺点
4. 选择最佳方案

---

## 工具对比

（暂无记录）
`;
    fs.writeFileSync(toolDecisionMapPath, toolDecisionMapTemplate);
    console.log(`✅ 创建文件: ${toolDecisionMapPath}`);
}

// 创建最佳实践
const bestPracticesPath = '.learnings/best-practices.md';
if (!fs.existsSync(bestPracticesPath)) {
    const bestPracticesTemplate = `# 最佳实践

总结经验，提炼方法论。

## 实践列表

（暂无记录）
`;
    fs.writeFileSync(bestPracticesPath, bestPracticesTemplate);
    console.log(`✅ 创建文件: ${bestPracticesPath}`);
}

// 创建进化日志
const evolutionPath = 'EVOLUTION.md';
if (!fs.existsSync(evolutionPath)) {
    const evolutionTemplate = `# EVOLUTION.md - 进化日志

记录每天的成长。

---

### ${new Date().toISOString().split('T')[0]}（第一天）

## 🌙 晚间进化总结

### 今日核心成就
初始化指数级成长系统

### 技术突破
1. 建立知识管理体系
2. 创建错误模式库
3. 建立工具决策图谱

### 进化速度评估
今日进化速度：⭐⭐⭐（重要突破）
总进化指数：3 个新能力点

---

*记录时间：${new Date().toLocaleString()}*
*状态：✅ 成长系统已启动*
`;
    fs.writeFileSync(evolutionPath, evolutionTemplate);
    console.log(`✅ 创建文件: ${evolutionPath}`);
}

// 创建配置文件
const configPath = 'growth-config.json';
if (!fs.existsSync(configPath)) {
    const config = {
        learnings: {
            errorPatternsPath: ".learnings/error-patterns.md",
            toolDecisionMapPath: ".learnings/tool-decision-map.md",
            bestPracticesPath: ".learnings/best-practices.md"
        },
        evolution: {
            logPath: "EVOLUTION.md",
            dailyFormat: "### YYYY-MM-DD（第N天）",
            autoBackup: true
        },
        skills: {
            directory: "skills",
            template: "templates/skill-template",
            autoPublish: false
        },
        metrics: {
            trackGrowthIndex: true,
            trackSkillCount: true,
            trackErrorPatterns: true
        }
    };
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(`✅ 创建文件: ${configPath}`);
}

console.log('\n✨ 指数级成长系统初始化完成！');
console.log('\n下一步：');
console.log('1. 开始记录错误模式: node scripts/add_error_pattern.js');
console.log('2. 更新工具决策图谱: node scripts/add_tool_decision.js');
console.log('3. 记录每日进化: node scripts/update_evolution.js');
console.log('4. 创建 Skill: node scripts/create_skill.js');
