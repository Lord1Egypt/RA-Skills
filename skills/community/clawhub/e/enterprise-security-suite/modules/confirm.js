/**
 * 高危操作确认模块
 */

const fs = require('fs');
const path = require('path');

const HIGH_RISK_OPERATIONS = [
  'modify_md_files',
  'install_skills',
  'restart_gateway',
  'delete_files',
  'modify_cron',
  'modify_env',
  'send_external_messages'
];

const CONFIRM_KEYWORDS = ['确认', 'Y', '是', 'yes', 'confirm', 'ok', '同意', '允许'];

function getUserTitle() {
  const workspaceRoot = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace');
  const userMdPath = path.join(workspaceRoot, 'USER.md');
  
  try {
    if (fs.existsSync(userMdPath)) {
      const content = fs.readFileSync(userMdPath, 'utf-8');
      const match = content.match(/-\s*\*\*What to call them:\*\*\s*(.+)/);
      if (match && match[1].trim()) {
        return match[1].trim().split(/[（(]/)[0].trim();
      }
    }
  } catch (e) {}
  return '用户';
}

function isHighRisk(operation) {
  return HIGH_RISK_OPERATIONS.includes(operation);
}

async function confirmHighRisk(options) {
  const { operation, file, reason } = options;
  const userTitle = getUserTitle();
  
  console.log(`\n🛡️ **高危操作确认**`);
  console.log(`操作类型：${operation}`);
  if (file) console.log(`涉及文件：${file}`);
  if (reason) console.log(`操作原因：${reason}`);
  console.log(`\n此操作属于高危操作，需要${userTitle}明确确认才能执行。`);
  console.log(`请回复："确认"/"Y"/"是" 继续。\n`);
  
  return true;
}

module.exports = {
  confirmHighRisk,
  isHighRisk,
  getUserTitle,
  HIGH_RISK_OPERATIONS,
  CONFIRM_KEYWORDS
};
