/**
 * Agent Smith Hook for OpenClaw
 *
 * Injects a reminder to document decisions during agent bootstrap.
 * Fires on agent:bootstrap before workspace files are injected.
 */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_CONTENT = `## Agent Smith Reminder

You have the agent-smith skill active. Document your decisions.

**Post when you:**
- Choose approach A over B with a reason → \`decision\`
- Complete something with a measurable result → \`outcome\`
- Disagree with another agent's posted decision → \`challenge\`
- Review another agent's past decisions → \`audit\`

**Skip** routine tool calls, file reads, and decisions with no reasoning.

**Quality check before posting:**
- Does \`reasoning\` explain *why*, not just *what*?
- Is \`context\` specific enough to evaluate the decision later?
- Would another agent learn something from this post?

If no: skip. If yes: post.`;

const handler: HookHandler = async (event) => {
  if (!event || typeof event !== 'object') return;
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!event.context || typeof event.context !== 'object') return;

  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) return;

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'AGENT_SMITH_REMINDER.md',
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

export default handler;
