---
name: aicade-app-builder
description: Build general aicade application prompts by taking the user's base prompt plus the platform additions from the bundled 3.1 workflow reference, then assembling a final integrated prompt in the style of 3.2.
homepage: https://github.com/aicade-galaxy/aicade-ts-bootstrap
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    emoji: "🕹️"
    requires:
      bins: [node]
---
`READ BEFORE INSTALL`
This skill follows the bundled prompt workflow reference exactly:
1. Collect the user's base business prompt
2. Add the aicade platform integration requirements from section `3.1`
3. Assemble one final integrated prompt like section `3.2`
`READ BEFORE INSTALL`

# aicade-app-builder

Use this skill when you want to generate a final AI prompt for an aicade app and you want the result to match the bundled documented workflow.

## Core Principle

This skill does not invent a new requirement structure.

It uses:

- `3.1` as the required input model
- `3.2` as the target output style

That means:

- the user provides a base business prompt
- the user provides or accepts the aicade platform additions
- the skill assembles the final integrated prompt

## Quick Start

```bash
node {baseDir}/scripts/check-aicade-env.mjs --mode all --cwd /path/to/project
node {baseDir}/scripts/save-aicade-env.mjs --cwd /path/to/project --set AICADE_API_KEY=... --set AICADE_API_SECRET_KEY=...

node {baseDir}/scripts/build-aicade-prompt.mjs \
  --spec {baseDir}/assets/app-spec.template.json \
  --lang en
```

## Recommended Workflow

### 1. Confirm Platform Access First

Before collecting the final prompt inputs, first tell the user to open:

- `https://www.aicadegalaxy.com/`

The user should:

1. connect their wallet
2. click `Launch App`
3. enter the `Dapp Management` page
4. click the `Show App key` button
5. read the API key information from the popup

Only after completing that flow should the skill continue to collect the core AICADE environment variables required for integration:

- `AICADE_API_KEY`
- `AICADE_API_SECRET_KEY`

Also keep:

- `AICADE_API_URL`

Treat `AICADE_API_URL = VITE_AICADE_API_URL`.
Its default value is `https://aicadegalaxy.com/v1`.

Keep this access check separate from the upload step.
The official scaffold upload flow does not read these access variable names directly from `upload.js`.

On the first use of this skill in a project, check the local environment first for these platform-access variables.
If any of them are missing, ask the user for the missing values one by one instead of asking for all values again at once.
After each value is provided, save it into the project's local `.env` file immediately.
If `AICADE_API_URL` is missing, use the default value and save it automatically.

Recommended check command:

```bash
node {baseDir}/scripts/check-aicade-env.mjs --mode access --cwd /path/to/project
```

Recommended save command:

```bash
node {baseDir}/scripts/save-aicade-env.mjs --cwd /path/to/project --set AICADE_API_KEY=...
```

Standard follow-up pattern:

1. Run the check command.
2. If all required values are present, tell the user they were found locally and ask for confirmation to reuse them.
3. If some values are missing, ask only for the first missing value.
4. After the user provides it, save it into `.env`, then move to the next missing value until the access set is complete.
5. If `AICADE_API_URL` is not set, write the default `https://aicadegalaxy.com/v1` into `.env` automatically.

Example:

- `I found AICADE_API_KEY locally.`
- `AICADE_API_SECRET_KEY is missing. Please provide AICADE_API_SECRET_KEY.`
- `AICADE_API_URL is not set locally, so I will use the default https://aicadegalaxy.com/v1 and save it for this project.`

### 2. Check Tech Stack Compatibility First

Before entering implementation or prompt assembly, first read:

- `https://github.com/aicade-galaxy/aicade-ts-bootstrap/blob/main/README.md`

The target app or game environment must conform to the technical stack and integration conventions described there.

If the current project does not match that technical stack, do not proceed silently. You must stop and confirm with the user using only these two options:

1. Use AI to automatically reimplement the app in the required technical stack
2. Wait for the user to regenerate it manually, then continue

Do not introduce a third option in this decision point.

If the user chooses option 1, start from the official scaffold directly:

- `https://github.com/aicade-galaxy/aicade-ts-bootstrap`

Use that repository as the project scaffold for the reimplementation.
Do not rebuild the scaffold structure from scratch.
The scaffold already includes the official upload script and upload command.

When migrating from a non-matching project into the scaffold:

1. Inspect the old project and extract the business goal, page structure, interaction rules, scoring or reward logic, and asset needs.
2. Rewrite that information into the skill's `3.1`-shaped input.
3. Rebuild the app on top of `aicade-ts-bootstrap` instead of patching the old structure in place.
4. Use the scaffold's existing `upload.js` and npm commands as-is.

### 3. Read Before Prompt Assembly

Read the bundled references first:

- `references/sdk-capabilities.md`
- `references/prompt-workflow.md`

### 4. Prepare Input In The `3.1` Shape

The user input should contain two parts:

1. Base business prompt
2. Platform integration additions

The platform additions should cover the same kind of information highlighted in `3.1`, such as:

- SDK initialization and invocation requirements
- scaffold document paths that the implementation model should read
- local storage replacement strategy
- wallet address display
- account and balance display
- ticket or payment access flow
- score, points, token, AI chat, NFT, or market-related capabilities when needed
- iframe sandbox compatibility constraints

After the README tech stack check passes, confirm integration in 3 layers:

1. Base requirements: must be added
2. Compatibility requirements: must be added
3. Extension SDK modules: ask the user whether each one should be added

Base requirements and compatibility requirements are mandatory and should not be skipped.

Extension SDK modules must be confirmed with the user before they are added to the final prompt.

If an extension module has configurable parameters, confirm those parameter values explicitly before prompt assembly. For example:

- if `AicadeCurrency` exchange is enabled, confirm the exchange ratio
- confirm the daily cap if the business requires it
- confirm the exchange trigger timing

### Common SDK Capabilities

The platform can expose multiple SDK modules. Choose only the real modules your app actually needs:

- `Application`: app metadata and lifecycle
- `Ticket`: access gate, subscription, or play/payment flow
- `AppScore`: score and leaderboard
- `AicadeCurrency`: point or platform currency operations
- `AIChat`: AI chat session and messages
- `AICoinMarket`: market assistant and streaming messages
- `Token`: token balance and swap flow
- `NftOwner`: NFT ownership and avatar
- `LocalStorageTools`: app-scoped storage instead of browser `localStorage`

Recommended confirmation order:

- mandatory base requirements
- mandatory compatibility requirements
- selected SDK modules
- optional extension modules

### 5. Generate The Final Prompt

Run:

```bash
node {baseDir}/scripts/build-aicade-prompt.mjs --spec /path/to/spec.json --lang en
```

The script will output one final prompt that:

- keeps the user's base business prompt structure
- appends the aicade platform integration block
- keeps technical requirements and output requirements
- reads like the final integrated prompt shown in `3.2`

### 6. Use The Prompt In Your IDE

Paste the generated prompt into Cursor, VS Code, or another AI IDE assistant.

### 7. Review Generated Code

Check these items before running the app:

- SDK initialization order is correct
- No unsupported SDK methods are called
- `LocalStorageTools` replaces `localStorage`
- Wallet address, balance, score, token, chat, or NFT UI is shown only when the selected SDK capabilities require it
- Exchange rules are enforced only when the app explicitly enables exchange-related capabilities
- iframe-safe communication and storage strategies are used instead of same-origin browser assumptions
- `SecurityError`, blocked frame access, and storage access failures are handled gracefully
- Error handling exists around async SDK calls

### 8. Confirm Upload Variables Every Time

On the first use of this skill in a project, check the local environment first for the scaffold upload credentials listed below.
If a value is already present locally, confirm and reuse it.
If a value is missing, ask the user only for that missing value, one at a time.
Do not ask again for `VITE_AICADE_API_KEY` or `VITE_AICADE_API_SECRET_KEY` when `AICADE_API_KEY` and `AICADE_API_SECRET_KEY` have already been saved, because they should be mirrored into `.env`.

Recommended check command:

```bash
node {baseDir}/scripts/check-aicade-env.mjs --mode upload --cwd /path/to/project
```

Recommended save command:

```bash
node {baseDir}/scripts/save-aicade-env.mjs --cwd /path/to/project --set VITE_AICADE_API_URL=...
```

Standard follow-up pattern:

1. Run the check command.
2. Reuse any values already found locally.
3. Treat `AICADE_API_KEY = VITE_AICADE_API_KEY` and `AICADE_API_SECRET_KEY = VITE_AICADE_API_SECRET_KEY`.
4. Ask only for the first missing required upload value.
5. Save every newly provided value into `.env` immediately.
6. `VITE_AICADE_API_UPLOAD` uses the scaffold default and should not be requested unless the user explicitly wants to override it.
7. `AICADE_API_URL = VITE_AICADE_API_URL`, and the default should be `https://aicadegalaxy.com/v1`.
8. Ask for a custom API URL only when the user explicitly wants to override that default.
9. Before the actual upload step, restate the resolved upload variables together with their current values and ask for final confirmation.

Example:

- `I already have AICADE_API_KEY locally, so I will reuse it as VITE_AICADE_API_KEY as well.`
- `I already have AICADE_API_SECRET_KEY locally, so I will reuse it as VITE_AICADE_API_SECRET_KEY as well.`
- `I will use the default AICADE_API_URL / VITE_AICADE_API_URL value: https://aicadegalaxy.com/v1.`
- `Final upload confirmation: VITE_AICADE_API_KEY=..., VITE_AICADE_API_SECRET_KEY=..., VITE_AICADE_API_URL=https://aicadegalaxy.com/v1. Please confirm whether I should continue with these values.`

Before every upload, reconfirm the required values used by the scaffold `upload.js` flow:

- `AICADE_API_KEY` / `VITE_AICADE_API_KEY` / `DAPP_KEY`
- `AICADE_API_SECRET_KEY` / `VITE_AICADE_API_SECRET_KEY` / `DAPP_SECRET_KEY`

Optional overrides:

- `VITE_AICADE_API_UPLOAD` or `UPLOAD_URL` only when the default upload URL must be replaced
- `AICADE_API_URL` / `VITE_AICADE_API_URL` only when the default base `https://aicadegalaxy.com/v1` must be customized

Do this every time before upload, even if they were confirmed earlier in the same project.

### 9. Build And Upload

For a new project, copy `upload.js` directly from:

- `https://github.com/aicade-galaxy/aicade-ts-bootstrap/blob/main/upload.js`

Do not rewrite `upload.js`.
Do not regenerate its logic from scratch.
Use the official upstream file unless the user explicitly asks to compare or refresh it from the source repository.

```bash
npm install
npm run dev
npm run upload
```

## Script Input Spec

The prompt builder accepts a JSON file like this:

```json
{
  "roleSetup": "You are a senior full-stack product engineer.",
  "projectName": "AI Event Assistant",
  "projectGoal": "Build an aicade application for event registration, check-in, and reward redemption.",
  "basePromptSections": [
    {
      "title": "Core Business Requirements",
      "items": [
        "Put your original business prompt for the AI here."
      ]
    }
  ],
  "platformIntegration": {
    "scaffoldReadmePath": "README.md",
    "scaffoldSdkDocPath": "doc/README.md",
    "scaffoldAppGuidePath": "doc/AICreateApplication-EN.md",
    "sdkAlreadyIntegrated": true,
    "requiredSdkModules": [
      "Application",
      "LocalStorageTools"
    ],
    "baseRequirements": [
      "Initialize AicadeSDK in the correct order with init(...), waitForReady(), and getModule(...)."
    ],
    "compatibilityRequirements": [
      "Respect iframe sandbox restrictions and opaque-origin limitations.",
      "Replace browser localStorage usage with LocalStorageTools."
    ],
    "replaceLocalStorageWith": "LocalStorageTools",
    "showWalletAddress": true,
    "showPointBalance": false,
    "pointBalanceLabel": "Points",
    "exchange": {
      "enabled": false,
      "ratio": "100:1",
      "dailyLimit": "100 Aicade Points",
      "trigger": "On each business settlement"
    }
  },
  "technicalRequirements": [
    "Generate within the current project environment."
  ],
  "outputRequirements": [
    "Output complete runnable code."
  ]
}
```

Use:

- `{baseDir}/assets/app-spec.template.json` for the minimal `3.1`-style input
- `{baseDir}/assets/app-spec.example.json` for a fuller example

## Files Included

- `scripts/build-aicade-prompt.mjs`
- `scripts/check-aicade-env.mjs`
- `scripts/save-aicade-env.mjs`
- `assets/app-spec.template.json`
- `assets/app-spec.example.json`
- `references/sdk-capabilities.md`
- `references/prompt-workflow.md`

## Security And Permissions

This skill:

- runs a local Node.js script
- reads a local JSON spec file
- prints a generated prompt to stdout

This skill does not:

- modify source code automatically
- upload anything by itself
- invoke the model autonomously

## Notes

- The input model is based on `3.1`
- The output format is intentionally shaped like `3.2`
- Ask about platform app access before discussing env vars
- Check README tech stack compatibility before implementation
- If the stack does not match, only offer the two allowed choices
- Reconfirm the real `upload.js` environment variables before every upload
- For new projects, copy `upload.js` from the official `aicade-ts-bootstrap` repository instead of rewriting it
- If the docs change, update this skill accordingly
