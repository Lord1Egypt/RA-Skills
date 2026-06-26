# Prompt Workflow

This skill uses the same logic as the documented `3.1 -> 3.2` workflow.

## Access Check First

Before entering prompt assembly, first tell the user to open:

- `https://www.aicadegalaxy.com/`

The user should:

1. connect their wallet
2. click `Launch App`
3. enter the `Dapp Management` page
4. click the `Show App key` button
5. read the API key information from the popup

Only after completing that flow should the skill continue to collect the core required environment variables:

- `AICADE_API_KEY`
- `AICADE_API_SECRET_KEY`

Also keep:

- `AICADE_API_URL`

Treat `AICADE_API_URL = VITE_AICADE_API_URL`.
Its default value is `https://aicadegalaxy.com/v1`.

This access step is separate from the scaffold upload step.
Do not assume the scaffold `upload.js` reads these exact variable names.

On the first use of this skill in a project, check the local environment first for these platform-access variables.
If any are missing, ask the user only for the missing values, one by one.
After each value is provided, save it into the project's local `.env` file immediately.
If `AICADE_API_URL` is missing, use the default value and save it automatically.

Suggested command:

```bash
node {baseDir}/scripts/check-aicade-env.mjs --mode access --cwd /path/to/project
```

Suggested save command:

```bash
node {baseDir}/scripts/save-aicade-env.mjs --cwd /path/to/project --set AICADE_API_KEY=...
```

Standard follow-up pattern:

1. Run the check command.
2. Reuse values already found locally.
3. Ask only for the first missing access variable.
4. Save each newly provided value into `.env`.
5. Continue one by one until `AICADE_API_KEY` and `AICADE_API_SECRET_KEY` are both accounted for.
6. If `AICADE_API_URL` is not set, write the default `https://aicadegalaxy.com/v1` into `.env` automatically.

## Tech Stack Check First

Before prompt assembly or implementation, first read:

- `https://github.com/aicade-galaxy/aicade-ts-bootstrap/blob/main/README.md`

The target published app or game must match the technical stack and integration conventions defined there.

If the current project does not match that stack, stop and confirm with the user using only these two choices:

1. Use AI to automatically convert and reimplement it in the required technical stack
2. Wait for the user to regenerate it manually, then continue

Do not offer a third path at this decision point.

If the user chooses option 1, use the official scaffold directly:

- `https://github.com/aicade-galaxy/aicade-ts-bootstrap`

Start the reimplementation from that repository instead of rebuilding the scaffold manually.
It already contains the official upload script and upload command.

For that migration path, first extract the old project's business goal, pages, flows, rules, rewards, and assets, then rewrite them as a clean `3.1`-shaped input before rebuilding on top of the scaffold.

## 3.1 Input Model

Start with the user's base business prompt, then append platform integration additions such as:

- SDK initialization and invocation requirements
- scaffold document paths for the implementation model
- storage replacement strategy
- wallet or account display
- selected SDK modules
- optional score, currency, token, AI chat, NFT, or payment constraints
- iframe sandbox compatibility constraints

After the README tech stack check passes, confirm integration scope in this order:

1. mandatory base requirements
2. mandatory compatibility requirements
3. selected real SDK modules
4. optional extension modules

Base requirements and compatibility requirements must always be added.

Extension SDK modules must be confirmed with the user before inclusion.

If an extension module has optional parameters, confirm those parameter values explicitly before generating the final prompt.

## 3.2 Output Style

The final output should be one integrated prompt that:

1. Keeps the user's original business prompt structure
2. Adds a dedicated `ts sdk integration requirements` or equivalent section
3. Keeps technical requirements and output requirements
4. Is ready to paste directly into an IDE AI assistant

## iframe Delivery Constraint

The generated app is delivered inside a sandboxed iframe. The final prompt should preserve iframe-safe constraints such as:

- no reliance on browser `cookie`
- no reliance on raw `localStorage`, `sessionStorage`, or `IndexedDB`
- no parent DOM traversal or `window.parent.xxx` assumptions
- no same-origin assumptions
- prefer `ajax`, SDK modules, token injection, URL parameters, server proxy, and `LocalStorageTools`

## Upload Check

On the first use of this skill in a project, check the local environment first for the scaffold upload credentials listed below.
If a value already exists locally, confirm and reuse it.
If a value is missing, ask the user only for that missing value, one at a time.
Treat `AICADE_API_KEY = VITE_AICADE_API_KEY` and `AICADE_API_SECRET_KEY = VITE_AICADE_API_SECRET_KEY` after they have been saved into `.env`.

Suggested command:

```bash
node {baseDir}/scripts/check-aicade-env.mjs --mode upload --cwd /path/to/project
```

Suggested save command:

```bash
node {baseDir}/scripts/save-aicade-env.mjs --cwd /path/to/project --set VITE_AICADE_API_URL=...
```

Standard follow-up pattern:

1. Run the check command.
2. Reuse values already found locally.
3. Ask only for the first missing required upload value.
4. Save every newly provided value into `.env`.
5. `VITE_AICADE_API_UPLOAD` uses the scaffold default and should not be requested unless the user explicitly wants to override it.
6. `AICADE_API_URL = VITE_AICADE_API_URL`, and the default should be `https://aicadegalaxy.com/v1`.
7. Ask for a custom API URL only when the user explicitly wants to override that default.
8. Before upload, restate the resolved variable names together with their current values and ask for final confirmation.

Before every upload, reconfirm the required values used by the scaffold `upload.js` flow:

- `AICADE_API_KEY` / `VITE_AICADE_API_KEY` / `DAPP_KEY`
- `AICADE_API_SECRET_KEY` / `VITE_AICADE_API_SECRET_KEY` / `DAPP_SECRET_KEY`

Optional overrides:

- `VITE_AICADE_API_UPLOAD` or `UPLOAD_URL` only when the default upload URL must be replaced
- `AICADE_API_URL` / `VITE_AICADE_API_URL` only when the default base `https://aicadegalaxy.com/v1` must be customized

For a new project, copy `upload.js` directly from:

- `https://github.com/aicade-galaxy/aicade-ts-bootstrap/blob/main/upload.js`

Do not rewrite `upload.js` or regenerate its upload logic from scratch.

## Important Rule

Do not redesign the user's business structure unless asked.

This skill should assemble and strengthen the prompt, not replace the user's own product description format.

Do not silently add extension modules just because they are available in the SDK.
