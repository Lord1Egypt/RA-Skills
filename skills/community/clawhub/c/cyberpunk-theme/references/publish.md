# Publish To ClawHub

推荐 slug：

- `cyberpunk-theme`

推荐显示名：

- `赛博朋克主题`

发布前检查：

1. `SKILL.md`、`agents/openai.yaml`、`scripts/install_cyberpunk_theme.py` 都存在
2. `assets/theme/` 下包含默认主题源文件与默认素材
3. 安装脚本至少在临时 workspace/dist 跑通过一次
4. 已登录 ClawHub：`clawhub login`、`clawhub whoami`

示例发布命令：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.0 --changelog "Initial release: one-click cyberpunk chat/dream theme with configurable portraits and backgrounds."`

后续更新示例：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.2 --changelog "Added PNG store preview and JSON-based theme config import."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.5 --changelog "Adapt OpenClaw 2026.5 footer status layer so context usage, compaction, and run-status indicators stay visible above the floating composer."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.6 --changelog "Show Codex chat quota as separate 5h and weekly remaining windows, and keep the cyberpunk theme asset bundle in sync with the workspace Control UI overlay."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.7 --changelog "Show Codex chat quota as separate 5h and weekly remaining windows, and keep the cyberpunk theme asset bundle in sync with the workspace Control UI overlay."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.8 --changelog "Add a configurable help/history portrait slot via --help-avatar and helpAvatar, and sync the bundled Control UI theme assets."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.9 --changelog "Tune the expanded right drawer spacing so the top control gap and bottom composer gap are visually balanced."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.10 --changelog "Fix the chat nameplates so helper is pinned to 消息助手 helper, while the main assistant nameplate is derived from IDENTITY.md or SOUL.md instead of hard-coded 菠萝包 labels."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.11 --changelog "Render tool and helper portraits through real img layers instead of CSS-only background images, fixing the severe blur/compression artifact on those two avatar paths."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.12 --changelog "Fix the WebUI chat timeline merge so same-timestamp events stay in the intended order: user -> assistant tool -> toolResult -> assistant text, instead of letting the final reply jump ahead of the tool stream."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.13 --changelog "Remove the dream page frosted-glass overlay and extra stage tint so the dream content sits directly on the background art instead of a separate glass panel."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.14 --changelog "Fix live control-ui dist auto-detection for re-apply on non-Homebrew OpenClaw installs, and fully remove the remaining dream-stage glass overlay/tint so the dream page finally matches the 1.0.13 design intent."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.15 --changelog "Fix the WebChat session picker stacking chain by removing the old clipping overflow and lifting the chat header plus session-picker layers above the transcript, so the dropdown no longer gets covered by chat messages."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.16 --changelog "Restore default binary theme assets from text-encoded fallbacks during install, fixing ClawHub skill publishes that omit PNG/JPG/GIF files so installed themes keep their bundled portraits and backgrounds."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.17 --changelog "Republish the complete text-encoded default asset bundle so ClawHub installs can restore the bundled portraits and backgrounds instead of shipping only the installer fallback code."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.18 --changelog "Consolidate the OpenClaw 2026.6.1 chat adapter, restore direct wallpaper visibility, hide the workspace files rail, make chat and tool bubbles transparent, dynamically reserve composer/footer space, and narrow the right Markdown drawer."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.19 --changelog "Stabilize the OpenClaw 2026.6.5 chat theme runtime by keeping quota badge, session fallback, and message timeline rewrites disabled by default, restoring HUD/avatar/header sync, deduplicating attribute-bearing theme injection blocks, and moving the bottom model picker back to the left tool group."`

本次小版本更新：

`clawhub publish ./skills/cyberpunk-theme --slug cyberpunk-theme --name "赛博朋克主题" --version 1.0.21 --changelog "Adapt OpenClaw 2026.6.9 nested chat-workbench composer and fix the right-side composer controls so usage, chat settings, and send stay visible in one row."`
