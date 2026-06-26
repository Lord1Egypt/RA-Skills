import { execFile } from "child_process";
import path from "path";

/**
 * collect-session hook handler
 * Fires on command:new and command:reset events.
 *
 * Resolves the script path from workspaceDir (set in your OpenClaw config under workspace.dir).
 * The previous session ID is passed explicitly to avoid race conditions with --current.
 */
const handler = async (event: any) => {
  if (event.type !== "command") return;
  if (event.action !== "new" && event.action !== "reset") return;

  // Agent: workspaceDir comes from your OpenClaw config (workspace.dir).
  // The fallback path below is a last resort — set workspace.dir in openclaw.json instead.
  const workspaceDir =
    event.context?.workspaceDir ||
    event.context?.cfg?.workspace?.dir ||
    process.env.HOME + "/workspace";

  const script = path.join(workspaceDir, "scripts", "collect-session.mjs");

  // Use the explicit previous session ID to avoid the --current race condition:
  // by the time the hook fires, the gateway has already created the new session file,
  // so --current picks the wrong (empty) session.
  const previousSessionId = event.context?.previousSessionEntry?.sessionId as string | undefined;
  const args = previousSessionId
    ? [script, previousSessionId]
    : [script, "--current"]; // fallback if ID not available

  await new Promise<void>((resolve) => {
    execFile("node", args, { timeout: 120_000 }, (err, stdout, stderr) => {
      if (err) {
        console.error(`[collect-session] ❌ Failed: ${err.message}`);
        if (stderr) console.error(`[collect-session] stderr: ${stderr.slice(0, 500)}`);
      } else {
        for (const line of stdout.trim().split("\n")) {
          console.log(`[collect-session] ${line}`);
        }
      }
      resolve(); // never block /new — always resolve
    });
  });
};

export default handler;
