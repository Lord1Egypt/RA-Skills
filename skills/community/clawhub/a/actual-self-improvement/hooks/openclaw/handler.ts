/**
 * Self-Improvement Hook for OpenClaw
 *
 * Injects a lightweight reminder at bootstrap so the agent remembers to
 * capture durable lessons, promote proven rules, and avoid logging noise.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_CONTENT = `## Self-Improvement Reminder

Capture only durable learning:
- user correction or updated fact
- non-obvious failure worth remembering
- project convention or workaround discovered
- missing capability worth tracking

Promote proven rules into shared memory.
Extract broad, resolved patterns into standalone skills.
`;

const handler: HookHandler = async (event) => {
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || typeof event.context !== 'object') return;

  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) return;

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'SELF_IMPROVEMENT_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

export default handler;
