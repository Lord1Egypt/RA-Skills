import { writeFileSync } from "node:fs";
import { join } from "node:path";

const handler = async (event: any) => {
  if (event.type !== "message" || event.action !== "received") return;

  const workspace =
    process.env.OPENCLAW_WORKSPACE ?? `${process.env.HOME}/.openclaw/workspace`;

  const ctx = {
    user:
      event.context?.senderName ??
      event.context?.metadata?.senderName ??
      event.context?.from ??
      "unknown",
    userId:
      event.context?.senderId ??
      event.context?.metadata?.senderId ??
      event.context?.from ??
      "unknown",
    channel: event.context?.channelId ?? "unknown",
    ts: Date.now(),
  };

  try {
    writeFileSync(join(workspace, ".version-context"), JSON.stringify(ctx));
  } catch (err) {
    console.error(
      "[agent-changelog-capture] Failed to write context:",
      err instanceof Error ? err.message : String(err)
    );
  }
};

export default handler;
