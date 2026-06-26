#!/usr/bin/env node
/**
 * Enterprise Security - 激活脚本
 * 安装后运行：node activate.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🛡️ 企业级安全套件 - 激活中...\n');

// 1. 读取 PG 记忆配置
console.log('📝 正在写入安全规则到记忆系统...\n');

const memories = [
  {
    key: 'security.operation.protocol',
    category: 'decision',
    content: '安全操作准则：高危操作必须获得明确确认 ("确认"/"Y"/"是")。高危清单：1.修改任何 MD 文件 2.安装/卸载/更新 skill 3.重启 Gateway 4.删除文件/目录 5.修改 cron 任务 6.修改环境变量/API 密钥 7.向外部发送消息',
    importance: 3
  },
  {
    key: 'auto.backup.mechanism',
    category: 'decision',
    content: '自动备份机制：修改.md/.json/.js/.ts/.py 等文件前必须自动备份。命名规则：原文件名.YYYYMMDD.NNN.bak',
    importance: 3
  },
  {
    key: 'changelog.mechanism',
    category: 'decision',
    content: '变更日志机制：所有高危/中危操作必须记录到 memory/CHANGELOG.md',
    importance: 3
  },
  {
    key: 'rollback.mechanism',
    category: 'decision',
    content: '回滚机制：触发条件为用户说"回滚"/"恢复原状"。流程：1.确认回滚范围 2.使用备份文件恢复 3.记录 CHANGELOG',
    importance: 3
  },
  {
    key: 'skill.install.security.check',
    category: 'decision',
    content: '技能安装安全检查：前置确认用户意图。检查项：来源验证、代码审查、依赖检查、权限评估。风险等级：低风险告知后安装，中风险详细说明等待确认，高风险拒绝安装',
    importance: 3
  }
];

// 写入 PG 记忆
const dbUri = 'postgresql://openclaw:pgmemory@localhost:15432/openclaw';

memories.forEach(mem => {
  try {
    const sql = `INSERT INTO memories (agent, category, key, content, importance) VALUES ('Cloud', '${mem.category}', '${mem.key}', '${mem.content.replace(/'/g, "''")}', ${mem.importance}) ON CONFLICT (key) DO UPDATE SET content = EXCLUDED.content, importance = EXCLUDED.importance;`;
    execSync(`docker exec -i pgmemory psql -U openclaw -d openclaw -c "${sql}"`, { stdio: 'pipe' });
    console.log(`✅ 已写入：${mem.key}`);
  } catch (e) {
    console.log(`⚠️  ${mem.key} 可能已存在`);
  }
});

console.log('\n✅ 安全规则已写入记忆系统！\n');

// 2. 提示用户
console.log('='.repeat(50));
console.log('🎉 激活完成！');
console.log('='.repeat(50));
console.log('\n请重启 Gateway 使配置生效：');
console.log('  openclaw gateway restart\n');
console.log('重启后，AI 会自动执行：');
console.log('  ✅ 高危操作前提示确认');
console.log('  ✅ 修改文件前自动备份');
console.log('  ✅ 自动记录变更日志');
console.log('  ✅ 支持一键回滚');
console.log('  ✅ 技能安装前安全检查\n');
