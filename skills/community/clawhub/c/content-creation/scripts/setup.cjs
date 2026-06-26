#!/usr/bin/env node
/**
 * 内容创作团队 - OpenClaw 部署工具
 * 部署 3 个平台无关的内容创作 Agent（墨白/探风/锦书）
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

const TEAM_NAME = 'workspace-content-creation';
const OPENCLAW_DIR = process.env.OPENCLAW_HOME || path.join(os.homedir(), '.openclaw');
const TEAM_DIR = path.join(OPENCLAW_DIR, TEAM_NAME);
const SCRIPT_DIR = __dirname;
const TEMPLATE_DIR = path.join(SCRIPT_DIR, '..', 'templates');

const AGENTS = [
  { id: 'mobai',   name: '墨白', label: '墨白-主编',       desc: '主编/内容总监 - 内容战略与质量把控' },
  { id: 'tanfeng', name: '探风', label: '探风-选题策划师', desc: '选题策划师 - 热点追踪与选题规划' },
  { id: 'jinshu',  name: '锦书', label: '锦书-文案创作师', desc: '文案创作师 - 文章撰写与标题优化' },
];

function runCommand(args) {
  try {
    return { code: 0, output: execSync(args.join(' '), { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'], shell: true }) };
  } catch (e) {
    return { code: e.status || 1, output: e.stderr || e.stdout || e.message };
  }
}

function main() {
  console.log('=========================================');
  console.log('  内容创作团队 - OpenClaw 部署工具');
  console.log('=========================================\n');

  // 1. 环境检查
  if (runCommand(['openclaw', '--version']).code !== 0) {
    console.log('❌ 未检测到 OpenClaw，请先安装：https://openclaw.ai');
    process.exit(1);
  }
  console.log('✅ OpenClaw 已安装\n');

  // 2. 部署 workspace 文件
  console.log('📁 部署 workspace 文件...');
  AGENTS.forEach((agent, i) => {
    console.log(`  → [${i + 1}/3] 部署 ${agent.label} (${agent.id})`);
    const destDir = path.join(TEAM_DIR, agent.id);
    fs.mkdirSync(destDir, { recursive: true });
    const srcDir = path.join(TEMPLATE_DIR, agent.id);
    if (!fs.existsSync(srcDir)) { console.log(`  ⚠️  模板目录不存在：${srcDir}`); return; }
    for (const f of fs.readdirSync(srcDir).filter(f => f.endsWith('.md'))) {
      const dest = path.join(destDir, f);
      if (!fs.existsSync(dest)) fs.copyFileSync(path.join(srcDir, f), dest);
    }
  });

  // 3. 注册 Agent
  console.log('\n⚙️  注册 Agent...');
  const existing = runCommand(['openclaw', 'agents', 'list']).output || '';
  for (const agent of AGENTS) {
    if (existing.includes(agent.id)) {
      console.log(`  → ${agent.id} 已存在，跳过`);
    } else {
      const { code, output } = runCommand([
        'openclaw', 'agents', 'add', agent.id,
        '--name', `"${agent.name}"`,
        '--workspace', `"${path.join(TEAM_DIR, agent.id)}"`,
        '--description', `"${agent.desc}"`,
      ]);
      console.log(code === 0 ? `  → ${agent.id} 注册成功` : `  ⚠️  ${agent.id} 注册失败：${output.trim()}`);
    }
  }

  // 4. 完成
  console.log(`\n✅ 内容创作团队部署完成！\n   团队目录：${TEAM_DIR}\n`);
  console.log('下一步：');
  console.log('  1. 使用 /content-pipeline 启动内容创作');
  console.log('  2. 安装 /wechat-publisher 添加微信发布能力');
}

main();
