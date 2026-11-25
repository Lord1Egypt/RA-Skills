---
name: convo-vault
description: >-
  Export or archive ChatGPT, Grok and Gemini chats in local Markdown, PDF and
  JSONL. Preserve original languages and review available reasoning and tool
  records. Supports whole ChatGPT projects.
compatibility: >-
  Requires Node.js 20+, Git for source installs, and a signed-in desktop browser for
  the chat service. Ego Lite can run exports through its local browser CLI.
---

# Convo Vault Chat Exporter

Convo Vault exports signed-in ChatGPT, Grok and Gemini conversations as local Markdown, PDF, JSONL and images, preserving the original languages. Open `*.decision-path.md` to review the recorded steps and their evidence. ChatGPT and Grok can provide reasoning summaries and tool activity. Gemini provides its visible messages and images.

Use the user's chosen browser. A signed-in Ego Lite session can export without a Convo Vault extension. Chrome, Edge and Brave need the extension loaded once.

The project is open source at https://github.com/amethyst-cosmos/convo-vault. Setup requires Node.js 20+ and local command execution. Git is needed for source installs. Installation and updates can download code or dependencies. Export files stay on the user's computer.

## How to run the commands

The examples use `$HOME/convo-vault`. First look for `CONVO_VAULT_DIR` or the `repo` path in `~/.convo-vault/config.json` (or `$CONVO_VAULT_HOME/config.json`). A user-provided installation path takes precedence. If it contains `cli/convo-vault.mjs`, substitute that absolute path in every command below. Quote paths with spaces.

Complete first-time setup before running export or list commands. Run each command on its own line and wait for it to finish. Do not join commands with `&&`: Windows PowerShell 5.1 does not support it. Quote paths with double quotes. Every command below can be run from any folder.

## 1. Find the conversations

Get the conversation links (`chatgpt.com/c/<id>`, `grok.com/c/<id>` or `gemini.google.com/app/<id>`; a bare id is a ChatGPT id) from the first of these that works:

1. The user's message: pasted links or ids.
2. A screenshot: read the address bar. Ids are 36 characters like `68f3c1a2-5b7e-4c1d-9a0e-2f6b8d4e7a11`; read them carefully.
3. A browser tool you already have: read the URL of the open chat tab.
4. The user names a project or some titles instead of giving links ("everything in my Research project"): list them, do not ask for links.

```
node "$HOME/convo-vault/cli/convo-vault.mjs" list --project "Research"
```

   It prints each conversation's id, date and title (`--json` for data; without `--project` it lists recent conversations). Pick the ones the user means by title; if a match is unclear, show the user the candidates and ask.
5. Otherwise ask the user once for the link. Never guess an id from a conversation title.

## 2. First time only: set up Convo Vault

Use the GitHub Release ZIP when the user chooses the portable package or already downloaded it. A fresh Skill installation defaults to the source checkout.

### Portable GitHub Release ZIP

1. Reuse the user's existing extracted folder if it contains `cli/convo-vault.mjs`. Otherwise use the local parent folder the user chooses and a fixed tagged [GitHub Release](https://github.com/amethyst-cosmos/convo-vault/releases). Download its named `convo-vault-<version>.zip` and matching `.zip.sha256`. Verify the SHA-256 before extracting. Keep existing folder contents intact and use the extracted `convo-vault-<version>` folder as the installation path.
2. Check for Node.js 20+. The ZIP includes renderer dependencies and a prebuilt extension. Run this command from the extracted folder:

   ```
   node cli/convo-vault.mjs setup --verify --no-open --no-skill
   ```

   Setup checks that the local renderer answers and records the installation path for later exports. Use the browser steps and `verify` below when preparing the first browser export. The user can separately choose where each exported conversation is saved.

### Source checkout

If the configured copy exists, go to the export instructions. Otherwise check the default location: does the file `$HOME/convo-vault/cli/convo-vault.mjs` exist? Use your file tools, or one of these:

```
test -f "$HOME/convo-vault/cli/convo-vault.mjs" && echo installed || echo missing
```

```
if (Test-Path "$HOME/convo-vault/cli/convo-vault.mjs") { "installed" } else { "missing" }
```

The first is for macOS, Linux and Git Bash, the second for Windows PowerShell.

If it is installed, go to section 3. If it is missing, tell the user plainly what you are about to do and wait for a clear yes before running anything:

> To export, I need to download Convo Vault from GitHub, install its project dependencies and build its extension. Your export files stay on this computer. Is that OK?

After a yes:

1. Check for Node.js 20+ and Git. If a prerequisite is missing, tell the user which one is needed. Use the portable ZIP if Git is unavailable.
2. Download the project. These two commands skip the files only developers need (tests, docs images, CI):

```
git clone --depth 1 --filter=blob:none --sparse https://github.com/amethyst-cosmos/convo-vault.git "$HOME/convo-vault"
```

```
git -C "$HOME/convo-vault" sparse-checkout set --no-cone '/*' '!/tests/' '!/docs/' '!/.github/' '!/AGENTS.md' '!/CONTRIBUTING.md' '!/eslint.config.mjs'
```

If sparse checkout fails, retry the plain `git clone --depth 1` into an empty folder the user chose.

3. Set it up. This installs dependencies and builds the extension, and does not touch any agent's skill folders:

```
node "$HOME/convo-vault/cli/convo-vault.mjs" setup --no-skill
```

4. **Ego Lite.** For users already using it, check that they are signed in to the chat site and run the first `verify` and export with `--browser ego`. This path needs no extension.

   Otherwise, ask the user to load the extension. **This is the one manual step, once per browser.** Browsers do not let a program install an unpublished extension, so do not try to do it for them. Give them the full path of the folder `convo-vault/dist/convo-vault-extension` inside the install folder (for example `C:\Users\<name>\convo-vault\dist\convo-vault-extension` on Windows, `/Users/<name>/convo-vault/dist/convo-vault-extension` on macOS) and tell them:
   1. Open the browser's extensions page (`chrome://extensions` or `edge://extensions`) and turn on **Developer mode**.
   2. Click **Load unpacked** and choose that folder.
   3. Open the chat site (https://chatgpt.com, https://grok.com or https://gemini.google.com) in that browser and sign in.

5. Verify, then continue once it prints `OK`:

```
node "$HOME/convo-vault/cli/convo-vault.mjs" verify
```

### Updating later

For source installs, when the user asks to update Convo Vault, run:

```
node "$HOME/convo-vault/cli/convo-vault.mjs" update --no-skill
```

It pulls the latest version, rebuilds the extension and reloads it in the browser by itself. The user does not need to open the Extensions page or click anything. Exports also reload an out-of-date extension on their own once the project has been updated, so there is nothing to tell the user to refresh. Only if the output says the extension did not take the reload, ask the user to click the reload icon on the Extensions page once. With ego lite there is nothing to reload: every export runs the current version.

Convo Vault 0.17.1 and later save resolved ChatGPT product-card thumbnails in the ZIP, Markdown and PDF. If an older install misses those images, explain that the user can update their Git checkout with the command above or get the latest [GitHub release](https://github.com/amethyst-cosmos/convo-vault/releases) for a ZIP install.

For portable installs, download and verify the new version's ZIP, unzip it alongside the previous version, and run setup in the new folder. Chrome, Edge and Brave users load the extension from the new folder.

### Share a diagnostic report

When the user asks for a shareable Debug pack, run:

```
node "$HOME/convo-vault/cli/convo-vault.mjs" doctor --debug-pack --out "<directory>"
```

Add `--from "<export.zip>"` when the user wants aggregate counts from a specific export. The Debug ZIP contains version, environment checks and optional counts. Conversation text, images, filenames, links, logs and local paths are excluded. Give the user the Debug ZIP path so they can share it.

## 3. Ask once about files

The bundle includes the conversation, images and the thinking or tool activity that Convo Vault can capture. ChatGPT and Grok have structured traces where their conversation records include steps. Gemini exports replies and images, and its separate thinking panel is currently outside the capture. Check `*.agent-trace.json` for coverage. **Files** uploaded to or generated in the conversation are only downloaded on request.

Ask the user one short question in their language, with the default stated, for example: "Besides the conversation and the model's thinking, should I also download the files uploaded and generated in it? Default is no."

- A clear yes ("yes", "all of them", "include the attachments", "连文件一起下") adds `--files`.
- Anything else leaves `--files` off. Do not ask twice.
- Only one side wanted ("only what ChatGPT generated", "just my uploads", "只下载 GPT 生成的附件") adds `--files-kind generated` or `--files-kind uploaded` instead of `--files`; the request already is the yes.
- Skip the question when the user already said it in the request.
- With several conversations, ask once; if the user wants files for only some of them, use `--files-for` with their names.

## 4. Export

```
node "$HOME/convo-vault/cli/convo-vault.mjs" export "<url-or-id>"
```

- It starts the local renderer if needed, opens the conversation in the user's browser where the extension exports it by itself, and closes the tab when done. Expect 10 to 60 seconds; long conversations take longer. Run it in the foreground and wait, with a timeout of at least 10 minutes.
- Progress goes to stderr. The last lines on stdout list the result folder, the `.zip` and the main files.
- Output goes to the `Downloads/convo-vault` folder in the user's user folder (`C:\Users\<name>\Downloads\convo-vault` on Windows) unless the user names a place; then add `--out "<dir>"`.
- Add `--files` only when the user said yes in section 3.
- Add `--no-pdf` when the user only wants the data (Markdown, JSON, JSONL): it is faster.
- If the user requests a language for the export labels, pass `--locale` with a language tag such as `ja` or `fr-CA`. Otherwise use the saved preference and active interface. Leave the conversation and trace in their original languages.
- Several conversations: pass them all to ONE command, `export <link> <link> ...` (ids work too). They run in a single browser tab, one after another, so nothing pops up per conversation; the output lists each result and any failure, and the exit code is 1 if any failed. Never start several export commands at once.
- A whole project: `export --project "Research"` exports every conversation in it (add links to include others).
- One side only: `--files-kind generated` (what ChatGPT made) or `--files-kind uploaded` (what the user attached). Alone it applies to every conversation; with `--files-for` only to the named ones. The side left out is listed in the manifest as "not requested", not as a failure.
- Files for only some: `--files-for "invoice,report"` downloads files only for the conversations whose title contains one of those words (or whose id is given). `--files` means every conversation. Use it when the user wants attachments for some conversations and not others.
- On macOS the browser tab opens in the background. On Windows and Linux the browser window may come to the front once per run, not once per conversation.

### Grok and Gemini

A Grok or Gemini link is exported with the same command and gives the same folder. Several Grok links run in one tab; each Gemini link gets its own tab, one after another. Images are included; other attachments are only listed by name. For both, `list`, `--project` and `--files` do not apply yet (they are ChatGPT only). Gemini has no conversation API, so its page is scrolled to the top and read, which takes longer; the output carries a warning that Gemini gives no message count and that its thinking panel is not exported. Treat the warnings as part of the result and tell the user.

## 5. After it finishes

- Give the folder and the key files, including `*.agent-trace.md` and `*.agent-trace.json` when the user wants to study the available reasoning. Check trace coverage and report any provider-specific omissions.
- If files were requested, report how many were stored and how many failed (`fileDownload` in `*.assets.manifest.json`: `requested`, `total`, `stored`, `failed`) and the main failure reason.
- If the user wants something done with a conversation (summarize it, continue the work, pull out decisions), read its `.md` or `*.messages.jsonl` from the folder and do that. Do not paste the whole conversation back.
- Convo Vault checks every export message by message and refuses an incomplete capture. Report that message to the user. Do not retry with `--allow-incomplete` unless they say a partial export is fine.

## 6. When it fails

| Message | What to do |
| --- | --- |
| `did not pick up the job` / extension did not respond | The extension is not loaded, is switched off, or the chat site is not signed in in that browser. If the user has ego lite, add `--browser ego` (no extension needed). Otherwise repeat the extension step in section 2, or add `--browser "Microsoft Edge"` if they use another browser. |
| `Images: ... could not be downloaded` | The export succeeded but those images stayed links. Tell the user the number; exporting again usually gets them. |
| `Renderer dependencies are not installed` | Run `node "$HOME/convo-vault/cli/convo-vault.mjs" setup --no-skill`. |
| `cannot run export jobs` | An old renderer is running. Run `node "$HOME/convo-vault/cli/convo-vault.mjs" backend stop`, then export again. |
| `Capture is incomplete` | Report the listed issues and ask whether a partial export is acceptable. |
| `No project named ...` | Show the user the project names the message lists and ask which one they mean. |
| `node` or `git` not found | Install it as in section 2, then open a new terminal. |
| Anything else | Run `node "$HOME/convo-vault/cli/convo-vault.mjs" doctor` and show the user its output. |

Never read or ask for the user's chat cookies, tokens or password. The extension (or, in ego lite, the same code run in the page) uses the browser's own signed-in session.

## Limits

- Needs a desktop Chromium browser: ego lite (no extension), or Chrome, Edge or Brave with the extension loaded once. It does not work from a phone.
- Exports the conversations you name or one project's; it does not export a whole account in one go.
- The chat sites can change their internal format. If an export fails after an update on the site, update Convo Vault, then check the project's releases for a fix: https://github.com/amethyst-cosmos/convo-vault/releases
