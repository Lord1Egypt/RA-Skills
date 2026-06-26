/**
 * ai-self-evolution Hook for OpenClaw
 * 
 * Injects a reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_CONTENT = `## 自我改进提醒

任务完成后，请评估是否需要记录经验：

**以下情况建议记录：**
- 用户纠正了你 → \`.learnings/LEARNINGS.md\`
- 命令/操作失败 → \`.learnings/ERRORS.md\`
- 用户提出当前缺失能力 → \`.learnings/FEATURE_REQUESTS.md\`
- 你发现原有认知有误 → \`.learnings/LEARNINGS.md\`
- 你找到了更优做法 → \`.learnings/LEARNINGS.md\`

**模式稳定后建议提升：**
- 行为模式 → \`SOUL.md\`
- 工作流改进 → \`AGENTS.md\`
- 工具使用坑点 → \`TOOLS.md\`

条目尽量简洁：日期、标题、发生了什么、下次怎么做。`;

const handler: HookHandler = async (event) => {
  // Safety checks for event structure
  if (!event || typeof event !== 'object') {
    return;
  }

  // Only handle agent:bootstrap events
  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  // Safety check for context
  if (!event.context || typeof event.context !== 'object') {
    return;
  }

  // Skip sub-agent sessions to avoid bootstrap issues
  // Sub-agents have sessionKey patterns like "agent:main:subagent:..."
  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) {
    return;
  }

  // Inject the reminder as a virtual bootstrap file
  // Check that bootstrapFiles is an array before pushing
  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'AI_SELF_EVOLUTION_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

export default handler;
