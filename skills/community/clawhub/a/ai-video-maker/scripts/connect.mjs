#!/usr/bin/env node
import { createInterface } from "node:readline";
import { Writable } from "node:stream";
import { pathToFileURL } from "node:url";
import { clearPendingConnection, loadSavedKey, saveKey } from "./credentials.mjs";
import { browserConnect, pendingApproval, verifyConnection } from "./browser-connect.mjs";
import { agentPlatformArgument } from "./contract.mjs";

export async function connect(apiKey, { fetcher = fetch, directory } = {}) {
  const key = apiKey.trim();
  if (!key || /[\s\x00-\x1f\x7f]/.test(key)) throw new Error("Enter a valid API key.");
  let response;
  try {
    response = await fetcher("https://aivideomaker.ai/api/v1/account", {
      method: "GET",
      headers: { key, "X-AIVideo-Source": "agent_skill" },
      redirect: "error",
      signal: AbortSignal.timeout(30000),
    });
  } catch {
    throw new Error(
      "Could not connect. Check your internet connection and try again. Your saved key was not changed.",
    );
  }
  if (!response.ok) {
    throw new Error(
      response.status === 401 || response.status === 403
        ? "Key not accepted. Create or copy an active API key and try again."
        : "The API is unavailable. Try again later. Your saved key was not changed.",
    );
  }
  let account;
  try {
    account = await response.json();
  } catch {
    /* Invalid server response. */
  }
  if (
    account?.ok !== true ||
    account?.key?.status !== "ACTIVE" ||
    !Number.isFinite(account?.currentBalance)
  ) {
    throw new Error("Could not verify this account. Your saved key was not changed.");
  }
  try {
    await saveKey(key, directory);
  } catch {
    throw new Error(
      "Could not save the key. Check permissions for ~/.aivideo-maker (owner access only).",
    );
  }
}

export function promptKey(input = process.stdin, output = process.stdout) {
  if (!input.isTTY || !output.isTTY)
    throw new Error(
      "Run this command in your own terminal. Never paste an API key into agent chat.",
    );
  return new Promise((resolve, reject) => {
    const muted = new Writable({
      write(_chunk, _encoding, done) {
        done();
      },
    });
    const rl = createInterface({ input, output: muted, terminal: true, historySize: 0 });
    let answered = false;
    output.write("Paste your API key (hidden), then press Enter: ");
    rl.once("SIGINT", () => rl.close());
    rl.once("close", () => {
      output.write("\n");
      if (!answered) reject(new Error("Connection cancelled. No key was saved."));
    });
    rl.question("", (key) => {
      answered = true;
      rl.close();
      resolve(key);
    });
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const args = process.argv.slice(2);
    // Without the argument, AIVIDEO_AGENT_PLATFORM still names the agent.
    let platform;
    const at = args.indexOf("--platform");
    if (at !== -1) platform = agentPlatformArgument(args.splice(at, 2)[1]);
    if (args.some((arg) => !["--manual", "--reconnect", "--start"].includes(arg)))
      throw new Error(
        "Use connect.mjs, --start to print the approval link without waiting, --reconnect for a new browser connection, or --manual for hidden terminal key entry. Add --platform <codex|claude|openclaw> to name your agent.",
      );
    const startOnly = args.includes("--start");
    let result;
    if (args.includes("--manual")) {
      if (process.env.AIVIDEO_API_KEY)
        throw new Error(
          "AIVIDEO_API_KEY is set and takes priority. Update that secret or unset it before connecting another account.",
        );
      const key = await promptKey();
      await connect(key);
      // The pasted key is the connection now; an unfinished browser approval is void.
      await clearPendingConnection();
      result = await verifyConnection(key);
    } else {
      const reconnect = args.includes("--reconnect");
      const environmentKey = process.env.AIVIDEO_API_KEY;
      if (reconnect && environmentKey)
        throw new Error(
          "AIVIDEO_API_KEY is set and takes priority. Update that secret or unset it before connecting another account.",
        );
      // Also removes state left by an expired or abandoned approval.
      const pending = await pendingApproval();
      // An approval in progress is finished before a saved key is trusted, so the key of an
      // account being replaced is never reported as the new connection. --reconnect starts
      // over unless the approval in progress is itself a reconnect.
      const resume = !environmentKey && pending !== null && (!reconnect || pending.replacing);
      const existing = environmentKey || (reconnect || resume ? "" : loadSavedKey());
      result = existing
        ? await verifyConnection(existing)
        : await browserConnect({
            platform,
            resume,
            replacing: reconnect,
            waitForApproval: !startOnly,
            onApproval: ({ url, code, expiresIn, resumed }) => {
              const minutes = Math.max(1, Math.ceil(expiresIn / 60));
              console.log(
                `${resumed ? "Resuming your pending connection." : "Installed. Connect your account to finish setup."}\nOpen ${url}\nConfirm this code in your browser: ${code}\n${
                  startOnly
                    ? `The link stays valid for about ${minutes} more minute${minutes === 1 ? "" : "s"}. Run connect again without --start to finish; it resumes this same link and code.`
                    : `Waiting for approval (up to ${minutes} minute${minutes === 1 ? "" : "s"}). Verification will not spend credits. If this command stops before approval, run it again: it resumes this same link and code.`
                }`,
              );
            },
          });
    }
    // --start only hands over the link; the connection is finished by the next run.
    if (result.status !== "PENDING") {
      console.log("Connected and verified. No credits spent.");
      console.log(JSON.stringify(result));
    }
  } catch (error) {
    // Helpers expose only fixed messages, never API responses or credentials.
    console.error(error.message);
    process.exitCode = 1;
  }
}
