/**
 * Echo Fade Memory hook for OpenClaw.
 *
 * Injects a bootstrap reminder so the agent uses the local memory service
 * as an active part of its workflow.
 */

const REMINDER_CONTENT = `
## Echo Fade Memory Reminder

Use echo-fade-memory as a natural long-term memory layer in OpenClaw.

Prefer this workflow when:
- the user says "记住这个" / "remember this"
- the user asks about something said before
- a durable preference, constraint, decision, correction, or workaround appears
- the answer clearly depends on prior session context

Before answering:
- Recall relevant project memory first
- Ground memories if they look fuzzy or uncertain

During work:
- Store durable user preferences, decisions, and corrections
- Reinforce memories that proved useful
- Forget memories when the user explicitly asks

If 127.0.0.1:8080 is unreachable, try:
- export EFM_BASE_URL=http://host.docker.internal:8080
`.trim();

const handler = async (event) => {
  if (!event || typeof event !== "object") {
    return;
  }

  if (event.type !== "agent" || event.action !== "bootstrap") {
    return;
  }

  if (!event.context || typeof event.context !== "object") {
    return;
  }

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: "ECHO_FADE_MEMORY_REMINDER.md",
      content: REMINDER_CONTENT,
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
