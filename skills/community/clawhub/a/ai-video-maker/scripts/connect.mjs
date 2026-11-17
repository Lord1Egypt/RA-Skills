#!/usr/bin/env node
import { createInterface } from "node:readline";
import { Writable } from "node:stream";
import { pathToFileURL } from "node:url";
import { loadSavedKey, saveKey } from "./credentials.mjs";
import { browserConnect, verifyConnection } from "./browser-connect.mjs";

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
    if (args.some((arg) => !["--manual", "--reconnect"].includes(arg)))
      throw new Error(
        "Use connect.mjs, --reconnect for a new browser connection, or --manual for hidden terminal key entry.",
      );
    let result;
    if (args.includes("--manual")) {
      if (process.env.AIVIDEO_API_KEY)
        throw new Error(
          "AIVIDEO_API_KEY is set and takes priority. Update that secret or unset it before connecting another account.",
        );
      const key = await promptKey();
      await connect(key);
      result = await verifyConnection(key);
    } else {
      if (args.includes("--reconnect") && process.env.AIVIDEO_API_KEY)
        throw new Error(
          "AIVIDEO_API_KEY is set and takes priority. Update that secret or unset it before connecting another account.",
        );
      const existing =
        process.env.AIVIDEO_API_KEY || (args.includes("--reconnect") ? "" : loadSavedKey());
      result = existing
        ? await verifyConnection(existing)
        : await browserConnect({
            onApproval: ({ url, code }) => {
              console.log(
                `Installed. Connect your account to finish setup.\nOpen ${url}\nConfirm this code in your browser: ${code}\nWaiting for approval (up to 10 minutes). Verification will not spend credits.`,
              );
            },
          });
    }
    console.log("Connected and verified. No credits spent.");
    console.log(JSON.stringify(result));
  } catch (error) {
    // Helpers expose only fixed messages, never API responses or credentials.
    console.error(error.message);
    process.exitCode = 1;
  }
}
