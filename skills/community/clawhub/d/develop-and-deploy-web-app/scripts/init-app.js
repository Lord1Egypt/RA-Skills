"use strict";

const fs = require("fs");
const path = require("path");
const {
  appMetaPath,
  appNotesPath,
  appRoot,
  assertSafeUserName,
  assertSafeToken,
  deriveAppDescriptors,
  ensureDir,
  findAppByToken,
  generateToken,
  isoNow,
  parseArgs,
  readJsonIfExists,
  syncPlatformRegistryEntry,
  syncWorkspaceRegistryEntry,
  userRoot,
  writeJson,
} = require("./common");

function aiNotesPath(userName, token) {
  return path.join(appRoot(userName, token), ".ai.md");
}

function notesTemplate(meta) {
  return `# ${meta.title}

## Goal

${meta.goal}

## Scope

- Initial scaffold

## Design

${meta.designSummary}

## Data model

- Define entities in the app source and keep this section current.

## Runbook

- Install: \`npm install\`
- Build: \`npm run build\`
- Start: \`npm run start\`

## Current URL

${meta.url || "Pending startup"}

## Change log

- ${meta.updatedAt}: App record initialized.
`;
}

function aiNotesTemplate(meta) {
  return `# AI Context

## User Requirements

- ${meta.goal}

## AI Design Notes

- ${meta.designSummary}
- Stack: ${meta.stack.frontend}, ${meta.stack.backend}, ${meta.stack.database}
- Base path: /${meta.token}/

## Working Rule

- Read this file before modifying the generated web app.
`;
}

function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const requestedToken = args.token;
  const title = args.title || "Web App";
  const goal = args.goal || "Build and run a simple full-stack web app.";
  const designSummary = args.design || "Use the skill defaults and Huashu-inspired web styling.";

  assertSafeUserName(userName);
  const token = requestedToken || generateToken();
  assertSafeToken(token);
  const tokenOwner = findAppByToken(token);
  if (tokenOwner) {
    throw new Error(`Token already exists: ${token}`);
  }

  const appDir = appRoot(userName, token);
  if (fs.existsSync(appDir)) {
    throw new Error(`App directory already exists: ${appDir}`);
  }

  ensureDir(userRoot(userName));
  ensureDir(appDir);

  const now = isoNow();
  const descriptors = deriveAppDescriptors({
    title,
    goal,
    appKind: args.appKind,
    appLabel: args.appLabel,
  });
  const meta = {
    userName,
    token,
    title,
    goal,
    designSummary,
    path: path.relative(process.cwd(), appDir).replaceAll("\\", "/"),
    port: null,
    url: null,
    stack: {
      frontend: "React + TypeScript + Vite",
      backend: "Express + TypeScript",
      database: "SQLite",
    },
    autoStart: true,
    status: "initialized",
    appKind: descriptors.appKind,
    appLabel: descriptors.appLabel,
    createdAt: now,
    updatedAt: now,
  };

  writeJson(appMetaPath(userName, token), meta);
  fs.writeFileSync(appNotesPath(userName, token), notesTemplate(meta), "utf8");
  fs.writeFileSync(aiNotesPath(userName, token), aiNotesTemplate(meta), "utf8");
  syncWorkspaceRegistryEntry(meta);
  syncPlatformRegistryEntry(meta);

  const result = {
    userName,
    token,
    appDir,
    meta: readJsonIfExists(appMetaPath(userName, token), meta),
  };
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

main();
