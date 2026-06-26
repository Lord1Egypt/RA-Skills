import type { PluginInput } from "opencode";

export default async function fragmentsHook({ client }: PluginInput) {
  return {
    "session.idle": async ({
      messages,
    }: {
      messages: Array<{ role: string; content: string }>;
    }) => {
      // Skip trivial sessions (fewer than 3 messages likely means no real work)
      if (!messages || messages.length < 3) return;

      // Check if assistant performed meaningful tool use
      const assistantMessages = messages.filter((m) => m.role === "assistant");
      if (assistantMessages.length < 2) return;

      // Inject prompt for the agent to follow fragments daily-log workflow
      return {
        content:
          "You completed a task. Follow the fragments skill daily-log hook workflow: " +
          "(1) assess if this session did meaningful work, " +
          "(2) if yes, call memos_get_daily_log for today, " +
          "(3) diff against existing content, " +
          "(4) format new entries in .plan style, " +
          "(5) show the user the merged log and ask for confirmation before saving.",
      };
    },
  };
}
