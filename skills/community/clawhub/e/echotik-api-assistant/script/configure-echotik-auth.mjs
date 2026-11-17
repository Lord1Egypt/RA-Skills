import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const minNodeMajor = 18;
const managedBlockStart = "# >>> echotik-api-assistant >>>";
const managedBlockEnd = "# <<< echotik-api-assistant <<<";
const defaultBaseUrl = "https://open.echotik.live";

function requireSupportedNodeVersion() {
  const major = Number(process.versions.node.split(".")[0]);
  if (Number.isNaN(major) || major < minNodeMajor) {
    throw new Error(`Node.js >= ${minNodeMajor} is required. Current version: ${process.versions.node}`);
  }
}

function parseArgs(argv) {
  const args = {
    status: false
  };

  for (let index = 2; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }

    const [rawKey, inlineValue] = token.split("=", 2);
    const key = rawKey.slice(2);

    if (key === "status") {
      args.status = true;
      continue;
    }

    const nextValue = inlineValue ?? argv[index + 1];
    if (!nextValue || nextValue.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    if (inlineValue === undefined) {
      index += 1;
    }

    if (key === "profile") args.profilePath = path.resolve(nextValue);
    else if (key === "username") args.username = nextValue;
    else if (key === "password") args.password = nextValue;
    else throw new Error(`Unsupported argument: --${key}`);
  }

  return args;
}

function isPlaceholder(value) {
  if (!value) {
    return true;
  }

  return new Set([
    "",
    "your_username",
    "your_password",
    "basic base64(username:password)",
    "changeme",
    "replace_me",
    "todo"
  ]).has(String(value).trim().toLowerCase());
}

function requireRealValue(name, value) {
  if (isPlaceholder(value)) {
    throw new Error(`Missing or placeholder value for ${name}`);
  }
  return String(value).trim();
}

function detectProfilePath(explicitPath) {
  if (explicitPath) {
    return explicitPath;
  }

  const shell = process.env.SHELL || "";
  const homeDir = os.homedir();

  if (shell.includes("zsh")) {
    return path.join(homeDir, ".zshrc");
  }
  if (shell.includes("bash")) {
    const bashrc = path.join(homeDir, ".bashrc");
    return fs.existsSync(bashrc) ? bashrc : path.join(homeDir, ".bash_profile");
  }

  return path.join(homeDir, ".profile");
}

function ensureParentDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function stripManagedBlock(contents) {
  const escapedStart = managedBlockStart.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const escapedEnd = managedBlockEnd.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const pattern = new RegExp(`${escapedStart}[\\s\\S]*?${escapedEnd}\\n?`, "g");
  return contents.replace(pattern, "").trimEnd();
}

function buildManagedBlock(values) {
  return [
    managedBlockStart,
    `export ECHOTIK_USERNAME=${shellQuote(values.username || "")}`,
    `export ECHOTIK_PASSWORD=${shellQuote(values.password || "")}`,
    managedBlockEnd,
    ""
  ].join("\n");
}

function profileContainsBlock(profilePath) {
  if (!fs.existsSync(profilePath)) {
    return false;
  }
  return fs.readFileSync(profilePath, "utf8").includes(managedBlockStart);
}

function currentSessionStatus() {
  const hasUserPass =
    !isPlaceholder(process.env.ECHOTIK_USERNAME) &&
    !isPlaceholder(process.env.ECHOTIK_PASSWORD);

  return {
    configured: hasUserPass,
    credentialMode: hasUserPass ? "username_password" : "missing"
  };
}

async function collectCredentials(args) {
  if (args.username || args.password) {
    return {
      username: requireRealValue("ECHOTIK_USERNAME", args.username),
      password: requireRealValue("ECHOTIK_PASSWORD", args.password)
    };
  }

  const rl = createInterface({ input, output });

  try {
    output.write("EchoTik setup will save credentials into your shell environment variables.\n");
    const username = await rl.question("Paste ECHOTIK_USERNAME: ");
    const password = await rl.question("Paste ECHOTIK_PASSWORD: ");

    return {
      username: requireRealValue("ECHOTIK_USERNAME", username),
      password: requireRealValue("ECHOTIK_PASSWORD", password)
    };
  } finally {
    rl.close();
  }
}

function writeProfile(profilePath, credentials) {
  ensureParentDir(profilePath);
  const existing = fs.existsSync(profilePath) ? fs.readFileSync(profilePath, "utf8") : "";
  const cleaned = stripManagedBlock(existing);
  const block = buildManagedBlock(credentials);
  const next = cleaned ? `${cleaned}\n\n${block}` : block;
  fs.writeFileSync(profilePath, next);
}

function printStatus(profilePath) {
  const profileConfigured = profileContainsBlock(profilePath);
  const current = currentSessionStatus();
  process.stdout.write(
    `${JSON.stringify(
      {
        profilePath,
        configuredInProfile: profileConfigured,
        configuredInCurrentSession: current.configured,
        credentialModeInCurrentSession: current.credentialMode
      },
      null,
      2
    )}\n`
  );
}

async function main() {
  requireSupportedNodeVersion();
  const args = parseArgs(process.argv);
  const profilePath = detectProfilePath(args.profilePath);

  if (args.status) {
    printStatus(profilePath);
    return;
  }

  const credentials = await collectCredentials(args);
  writeProfile(profilePath, credentials);

  process.stdout.write(
    [
      "EchoTik environment variable setup complete.",
      `- shell profile: ${profilePath}`,
      "- auth mode: username_password",
      "- Next step: restart Codex or Claude Code, or open a new terminal session.",
      `- If you want to use this shell immediately, run: source ${profilePath}`
    ].join("\n") + "\n"
  );
}

try {
  await main();
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}
