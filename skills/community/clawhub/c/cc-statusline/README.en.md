# cc-statusline

> Claude Code Statusline Assistant
>
> 中文说明： [README.md](README.md)

## Project Description / 项目描述
- English: `cc-statusline` is a Claude Code statusline skill for installing, switching, previewing, fine-tuning, and restoring statuslines with bilingual triggering, preset installs, custom layouts, theme / icon switching, and Windows / macOS / Linux support.
- 中文：`cc-statusline` 是一个面向 Claude Code 的状态栏 skill，用来安装、切换、预览、微调和恢复状态栏，支持双语触发、预设安装、自定义布局、主题 / 图标切换，以及 Windows / macOS / Linux 三平台。

A bilingual Claude Code statusline skill for preset installation, preview-first activation, interactive customization, theme / icon switching, and cross-platform support on Windows, macOS, and Linux.

## Install this skill

### Option 1: Paste the GitHub link to AI and ask it to install the skill (best for normal users)
Send this repository URL to an AI agent that can operate inside Claude Code and ask it to install the skill:

```text
https://github.com/Miluer-tcq/cc-statusline
```

Copy-ready prompt:

```text
Please install this Claude Code skill for me:
https://github.com/Miluer-tcq/cc-statusline

Install target: ~/.claude/skills/cc-statusline
After installation, tell me how to trigger it.
```

Notes:
- The install target is `~/.claude/skills/cc-statusline`
- This installs a **skill directory**, not a plugin
- After installation, Claude Code can trigger it with natural language

### Option 2: Install manually from the GitHub repository
The repository is now flattened, so the **repository root is the skill root**. For manual installation, copy the runtime files into `~/.claude/skills/cc-statusline`:

```bash
git clone https://github.com/Miluer-tcq/cc-statusline
mkdir -p ~/.claude/skills/cc-statusline
cp -r cc-statusline/SKILL.md cc-statusline/scripts cc-statusline/presets cc-statusline/themes cc-statusline/icons cc-statusline/references ~/.claude/skills/cc-statusline/
```

## How to use it after installation
After installing, you can say things like:

- `Install the Full / 完整版 statusline for me`
- `Switch me to the Developer / 开发者版 statusline`
- `Generate a 2-line custom statusline with the ocean theme and developer icons`
- `Uninstall the statusline and restore the default one`

If your current session does not notice the new skill yet, restart the Claude Code session.

## Features
- bilingual trigger coverage for Chinese and English requests
- one-click preset installation
- grouped module-based custom layouts
- custom generation from scratch or from a preset
- 1 / 2 / 3 line layouts
- theme and icon style switching
- backup of the target script to `<target>.bak`
- previous `statusLine` snapshot saved to `~/.claude/cc-statusline-state.json`
- updates only the `statusLine` field in `~/.claude/settings.json`
- uninstall removes only `statusLine` and keeps generated scripts on disk

## Current repository layout
The repository has been flattened:
- the repository root is now the installable `cc-statusline` skill root
- `SKILL.md` is the skill entry point
- `scripts/`, `presets/`, `themes/`, `icons/`, and `references/` are runtime assets
- `assets/screenshots/` are GitHub presentation assets and are not required for runtime
- the `.skill` package can be generated on demand and distributed as a release asset instead of staying in the repository

## Manual use of bundled skill scripts
If the skill is already installed, you can also call its scripts directly.

### 1. Activate a preset statusline
```bash
bash ~/.claude/skills/cc-statusline/scripts/activate_preset_statusline.sh full aurora classic
```

What the preset install flow does:
- installs or reuses `jq`
- backs up the target script to `<target>.bak`
- preserves the previous `statusLine` value in `~/.claude/cc-statusline-state.json`
- writes the runtime script to `~/.claude/statusline.sh` by default
- updates only the `statusLine` field in `~/.claude/settings.json`
- asks before replacing a foreign `statusLine` configuration

### 2. Generate a custom statusline
Generate a three-line custom layout:

```bash
bash ~/.claude/skills/cc-statusline/scripts/generate_custom_statusline.sh \
  "$HOME/.claude/statusline.custom.sh" \
  "model,modes,active" \
  "cwd,git,context" \
  "ctx_tokens,sum_tokens,duration,cost" \
  "ocean" \
  "developer"
```

Generate a one-line custom layout:

```bash
bash ~/.claude/skills/cc-statusline/scripts/generate_custom_statusline.sh \
  "$HOME/.claude/statusline.custom.sh" \
  "model,active,cost" \
  "-" \
  "-" \
  "mono" \
  "minimal"
```

Notes:
- use comma-separated module ids per line
- pass `-` for an unused line
- the generator prints a compact summary of the final layout

Activate the generated custom script:

```bash
bash ~/.claude/skills/cc-statusline/scripts/activate_custom_statusline.sh "$HOME/.claude/statusline.custom.sh" ocean developer
```

Switch back to a preset later:

```bash
bash ~/.claude/skills/cc-statusline/scripts/activate_preset_statusline.sh full aurora classic
```

### 3. Uninstall / restore default behavior
```bash
bash ~/.claude/skills/cc-statusline/scripts/uninstall_statusline.sh
```

This removes only the `statusLine` field from `~/.claude/settings.json`.
Generated script files stay on disk unless the user explicitly wants them removed.

### 4. `.skill` packaging
This repository now supports skill-first distribution:
- copy the root skill files into `~/.claude/skills/cc-statusline`
- generate a `.skill` package from the repository root only when preparing a release
- the packaged `.skill` file does not need to stay checked into the repository

## Presets
- `Full / 完整版` — closest to the current full Miluer-style layout
- `Standard / 标准版` — balanced for daily use
- `Minimal / 极简版` — lowest visual noise
- `Developer / 开发者版` — emphasizes git state and token visibility

## Themes
- `Aurora / 极光`
- `Sunset / 日落`
- `Ocean / 海洋`
- `Mono / 单色`

## Icon styles
- `classic / 经典`
- `minimal / 极简`
- `developer / 开发者`

## Customization model
The skill supports:
- selecting a preset directly
- starting from scratch with grouped module selection
- starting from a preset and fine-tuning modules
- choosing 1 / 2 / 3 line layouts
- choosing an existing theme first, then refining colors
- switching icon styles
- generating `~/.claude/statusline.custom.sh` before activation

Canonical module groups are documented in `references/modules.md`.
Trigger phrase examples are documented in `references/trigger-phrases.md`.

## Screenshots

### Preset selection / 预设选择
![Preset selection / 预设选择](assets/screenshots/preset-selection.svg)

### Custom layout preview / 自定义布局预览
![Custom layout preview / 自定义布局预览](assets/screenshots/custom-layout-preview.svg)

### Themes and icon styles / 主题与图标风格
![Themes and icon styles / 主题与图标风格](assets/screenshots/theme-and-icons.svg)

### Installed statusline examples / 安装后状态栏示例
![Installed statusline examples / 安装后状态栏示例](assets/screenshots/installed-statusline-examples.svg)

### Cross-platform install examples / 三平台安装示例
![Cross-platform install examples / 三平台安装示例](assets/screenshots/cross-platform-install.svg)
