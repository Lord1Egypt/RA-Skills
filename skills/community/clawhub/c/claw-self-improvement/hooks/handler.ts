/**
 * Claw Self-Improvement Hook for OpenClaw
 *
 * Injects a reminder to evaluate learnings during agent bootstrap.
 * Fires on agent:bootstrap event before workspace files are injected.
 *
 * Optional config gate for visible learning notices:
 * skills.entries["claw-self-improvement"].config.message = true
 */

type BootstrapFile = {
  path: string;
  content: string;
  virtual?: boolean;
};

type BootstrapContext = {
  cfg?: unknown;
  bootstrapFiles?: BootstrapFile[];
};

type BootstrapEvent = {
  type?: string;
  action?: string;
  sessionKey?: string;
  context?: BootstrapContext;
};

type HookHandler = (event: BootstrapEvent) => Promise<void> | void;

const BASE_REMINDER_CONTENT = `## Claw Self-Improvement Reminder

After completing tasks, evaluate if any learnings should be captured:

**Log when:**
- User corrects you → \`.learnings/LEARNINGS.md\`
- Command/operation fails → \`.learnings/ERRORS.md\`
- User wants missing capability → \`.learnings/FEATURE_REQUESTS.md\`
- You discover your knowledge was wrong → \`.learnings/LEARNINGS.md\`
- You find a better approach → \`.learnings/LEARNINGS.md\`

**Promote when pattern is proven:**
- Distill durable rules into \`.learnings/PROMOTED.md\`
- Categories: Behavioral Patterns, Workflow Improvements, Tool Gotchas, Durable Rules
- Keep promoted entries short, actionable, and easy to remove
- Do not auto-edit \`AGENTS.md\`, \`SOUL.md\`, \`TOOLS.md\`, or \`MEMORY.md\` as part of this skill

Keep entries simple: date, title, what happened, what to do differently.`;

const MESSAGE_REMINDER_CONTENT = `## Visible Learning Notice

When \`skills.entries["claw-self-improvement"].config.message\` is \`true\`:
- If you create or update any \`.learnings/*.md\` file during a user-visible reply, append one short formatted note at the end of that same reply.
- Keep the note brief and include it only once per reply.
- For raw logs, say: \`Noted — logged to .learnings/LEARNINGS.md.\`, \`Noted — logged to .learnings/ERRORS.md.\` or \`Noted — logged to .learnings/FEATURE_REQUESTS.md.\`
- For promotions, say: \`Promoted — new rule to .learnings/PROMOTED.md.\`
- Skip it when there is no user-visible reply, or when replying \`NO_REPLY\`.
`;

type MaybeConfig = {
  skills?: {
    entries?: Record<string, { config?: { message?: unknown } } | undefined>;
  };
};

function isMessageNoticeEnabled(cfg: unknown): boolean {
  if (!cfg || typeof cfg !== 'object') {
    return false;
  }

  const config = cfg as MaybeConfig;
  return config.skills?.entries?.['claw-self-improvement']?.config?.message === true;
}

function buildReminderContent(cfg: unknown): string {
  if (!isMessageNoticeEnabled(cfg)) {
    return BASE_REMINDER_CONTENT;
  }

  return `${BASE_REMINDER_CONTENT}\n\n${MESSAGE_REMINDER_CONTENT}`;
}

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

  const reminderContent = buildReminderContent(event.context.cfg);

  // Inject the reminder as a virtual bootstrap file
  // Check that bootstrapFiles is an array before pushing
  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'CLAW_SELF_IMPROVEMENT_REMINDER.md',
      content: reminderContent,
      virtual: true,
    });
  }
};

export default handler;
