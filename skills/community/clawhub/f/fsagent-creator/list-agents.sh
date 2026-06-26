#!/bin/bash
# List Agents Script
# Usage: ./list-agents.sh

CONFIG_FILE="/home/admin/.openclaw/openclaw.json"

echo "📋 当前 Agent 列表"
echo "=================="

node -e "
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('$CONFIG_FILE', 'utf8'));

console.log('');
console.log('ID\t\t名称\t\t模型\t\t飞书App ID');
console.log('---\t\t----\t\t----\t\t----------');

config.agents.list.forEach(agent => {
    const feishuAccount = config.channels.feishu.accounts[agent.id];
    const appId = feishuAccount ? feishuAccount.appId : '-';
    const model = agent.model ? agent.model.split('/')[1] : 'default';
    console.log(agent.id + '\t\t' + agent.name + '\t\t' + model + '\t\t' + appId);
});

console.log('');
console.log('总计: ' + config.agents.list.length + ' 个 agent');
"

echo ""
echo "💡 使用 create-agent.sh 创建新 agent"
echo "💡 使用 delete-agent.sh 删除 agent"