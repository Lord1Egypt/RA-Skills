#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import process from "node:process";
import { createInterface } from "node:readline/promises";
import { stdin, stdout } from "node:process";

import { LaunchThatOpenClawConnector } from "./connector";

const readArg = (name: string): string | undefined => {
  const pair = process.argv.find((arg) => arg.startsWith(`--${name}=`));
  if (!pair) return undefined;
  return pair.slice(name.length + 3);
};

const resolveSecret = async (params: {
  directValue?: string;
  envVar?: string;
  filePath?: string;
  promptLabel?: string;
}): Promise<string | undefined> => {
  if (params.directValue?.trim()) return params.directValue.trim();
  if (params.envVar?.trim()) {
    const envValue = process.env[params.envVar];
    if (envValue?.trim()) return envValue.trim();
  }
  if (params.filePath?.trim()) {
    const value = await readFile(params.filePath, "utf-8");
    if (value.trim()) return value.trim();
  }
  if (params.promptLabel && process.stdin.isTTY) {
    const rl = createInterface({ input: stdin, output: stdout });
    try {
      const promptValue = await rl.question(params.promptLabel);
      if (promptValue.trim()) return promptValue.trim();
    } finally {
      rl.close();
    }
  }
  return undefined;
};

const command = process.argv[2];

const main = async () => {
  if (command === "auth-link") {
    const baseUrl = readArg("base-url");
    const workspaceId = readArg("workspace-id");
    const instanceName = readArg("instance-name");
    if (!baseUrl || !workspaceId || !instanceName) {
      console.error(
        "Usage: lt-openclaw-connect auth-link --base-url=... --workspace-id=... --instance-name=...",
      );
      process.exit(1);
    }

    const result = await LaunchThatOpenClawConnector.createAuthLink({
      launchThatBaseUrl: baseUrl,
      workspaceId,
      instanceName,
    });
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  }

  if (command === "run") {
    const baseUrl = readArg("base-url");
    const workspaceId = readArg("workspace-id");
    const instanceId = readArg("instance-id");
    const ingestToken = await resolveSecret({
      directValue: readArg("ingest-token"),
      envVar: readArg("ingest-token-env") ?? "LAUNCHTHAT_INGEST_TOKEN",
      filePath: readArg("ingest-token-file"),
      promptLabel: "Ingest token: ",
    });
    const signingSecret = await resolveSecret({
      directValue: readArg("signing-secret"),
      envVar: readArg("signing-secret-env") ?? "LAUNCHTHAT_SIGNING_SECRET",
      filePath: readArg("signing-secret-file"),
    });
    const persistQueue = readArg("persist-queue") !== "false";

    if (!baseUrl || !workspaceId || !instanceId || !ingestToken) {
      console.error(
        "Usage: lt-openclaw-connect run --base-url=... --workspace-id=... --instance-id=... [--ingest-token-env=LAUNCHTHAT_INGEST_TOKEN] [--ingest-token-file=/path/token]",
      );
      process.exit(1);
    }

    const connector = new LaunchThatOpenClawConnector({
      launchThatBaseUrl: baseUrl,
      workspaceId,
      instanceId,
      ingestToken,
      signingSecret,
      persistQueue,
    });

    await connector.start();
    console.log("Connector running. Press Ctrl+C to stop.");

    process.on("SIGINT", async () => {
      await connector.stop();
      process.exit(0);
    });
    process.on("SIGTERM", async () => {
      await connector.stop();
      process.exit(0);
    });

    // Keep process alive.
    setInterval(() => undefined, 60_000);
    return;
  }

  console.error("Commands: auth-link | run");
  process.exit(1);
};

void main();
