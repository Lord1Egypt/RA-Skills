import { AtxClient } from "atxswap-sdk";
import { homedir } from "node:os";
import { join } from "node:path";
import readline from "node:readline";

const DEFAULT_KEYSTORE_PATH = join(homedir(), ".config", "atxswap", "keystore");

function parseRpcUrls(raw) {
  if (!raw) return undefined;
  const urls = raw
    .split(",")
    .map((url) => url.trim())
    .filter((url) => url.length > 0);
  return urls.length > 0 ? urls : undefined;
}

export async function createClient() {
  const rpcUrls = parseRpcUrls(process.env.BSC_RPC_URL);
  const client = new AtxClient({
    ...(rpcUrls && { rpcUrls }),
    keystorePath: DEFAULT_KEYSTORE_PATH,
  });
  await client.ready();
  return client;
}

export function getDefaultKeystorePath() {
  return DEFAULT_KEYSTORE_PATH;
}

export function parseArgs(args) {
  const parsed = { _: [] };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      parsed[key] = args[i + 1] || true;
      i++;
    } else {
      parsed._.push(args[i]);
    }
  }
  return parsed;
}

export function fmt(wei, decimals = 18) {
  const n = Number(wei) / 10 ** decimals;
  if (n === 0) return "0";
  if (n < 0.000001) return n.toExponential(4);
  return n.toLocaleString("en-US", { maximumFractionDigits: 6 });
}

/** V3 fee tier (`100`|`500`|`2500`|`10000`) → human-readable swap fee, e.g. `0.25%`. Matches Uniswap tier display (`fee`/10000 as a percent label). */
export function feeTierToPercentString(fee) {
  const n = Number(fee);
  if (!Number.isFinite(n) || n <= 0) return "0%";
  const pct = n / 10000;
  const s = pct.toFixed(6).replace(/\.?0+$/, "") || "0";
  return `${s}%`;
}

export function jsonStringify(value, space = 2) {
  return JSON.stringify(
    value,
    (_, current) => (typeof current === "bigint" ? current.toString() : current),
    space,
  );
}

export function exitError(message, code = 1) {
  console.error(jsonStringify({ error: message }));
  process.exit(code);
}

export function getErrorMessage(error) {
  if (typeof error === "string") return error;
  if (error?.shortMessage) return error.shortMessage;
  if (error?.reason) return error.reason;
  if (error?.message) return error.message.split("\n")[0];
  return "Unknown error";
}

export async function runMain(fn) {
  try {
    await fn();
  } catch (error) {
    exitError(getErrorMessage(error));
  }
}

async function promptHidden(promptText) {
  if (!process.stdin.isTTY || !process.stdout.isTTY) {
    return null;
  }

  return await new Promise((resolve, reject) => {
    let value = "";
    const wasRaw = process.stdin.isRaw;

    readline.emitKeypressEvents(process.stdin);
    process.stdin.setRawMode?.(true);
    process.stdin.resume();
    process.stdout.write(promptText);

    const onKeypress = (char, key) => {
      if (key?.ctrl && key.name === "c") {
        cleanup();
        process.stdout.write("\n");
        reject(new Error("Password input cancelled"));
        return;
      }

      if (key?.name === "return" || key?.name === "enter") {
        cleanup();
        process.stdout.write("\n");
        resolve(value);
        return;
      }

      if (key?.name === "backspace") {
        value = value.slice(0, -1);
        return;
      }

      if (char) {
        value += char;
      }
    };

    const cleanup = () => {
      process.stdin.off("keypress", onKeypress);
      process.stdin.setRawMode?.(Boolean(wasRaw));
      process.stdin.pause();
    };

    process.stdin.on("keypress", onKeypress);
  });
}

export async function resolvePassword(args, promptText = "Enter wallet password: ") {
  if (args.password) return args.password;

  const ttyPassword = await promptHidden(promptText);
  if (ttyPassword) return ttyPassword;

  exitError("Password required: use --password <pwd> or run in an interactive terminal");
}

export async function resolveNewPassword(args) {
  if (args.password) return args.password;

  if (process.stdin.isTTY && process.stdout.isTTY) {
    while (true) {
      const password = await promptHidden("Create wallet password: ");
      if (!password) exitError("Password cannot be empty");
      const confirm = await promptHidden("Confirm wallet password: ");
      if (password !== confirm) {
        console.error("Passwords do not match, please try again.");
        continue;
      }
      return password;
    }
  }

  exitError("Password required: use --password <pwd> or run in an interactive terminal");
}

export async function loadWallet(client, address, args) {
  try {
    return await client.wallet.load(address);
  } catch {
    if (args.password) {
      return await client.wallet.load(address, args.password);
    }

    const ttyPassword = await promptHidden(`Password for ${address}: `);
    if (ttyPassword) {
      return await client.wallet.load(address, ttyPassword);
    }

    exitError(`Password required for ${address}: use --password <pwd> or run in an interactive terminal`);
  }
}

export async function exportKeystore(client, address, args = {}) {
  if (typeof client.wallet.exportMetaMaskKeystore === "function") {
    return await client.wallet.exportMetaMaskKeystore(address, args.password);
  }
  return client.wallet.exportKeystore(address);
}
