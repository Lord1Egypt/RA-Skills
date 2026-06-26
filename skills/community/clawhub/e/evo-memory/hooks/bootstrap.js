/**
 * Self-Evolution Bootstrap Hook for OpenClaw
 *
 * 每次 agent 启动时注入 self-evolution SKILL.md 到上下文。
 * 不替换老的 self-improvement hook，纯新增。
 */

const fs = require('fs');
const path = require('path');

const SKILL_PATH = path.join(
  process.env.HOME || '',
  '.openclaw/workspace/self-evolution/SKILL.md'
);

const handler = async (event) => {
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || typeof event.context !== 'object') return;

  // 读取 SKILL.md 内容
  let skillContent = '';
  try {
    skillContent = fs.readFileSync(SKILL_PATH, 'utf-8');
  } catch (e) {
    // SKILL.md 不存在则跳过
    return;
  }

  // 注入为虚拟 bootstrap 文件
  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'SELF_EVOLUTION_SKILL.md',
      content: skillContent,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
