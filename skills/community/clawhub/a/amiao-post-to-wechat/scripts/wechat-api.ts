#!/usr/bin/env bun
/**
 * wechat-api.ts
 * Publishes a WeChat article via the WeChat Official Account API.
 *
 * Usage:
 *   bun wechat-api.ts <file.md|file.html> --theme <theme> [options]
 *
 * Options:
 *   --theme <theme>       Visual theme (default: default)
 *   --color <color>       Accent color
 *   --title <title>       Article title (auto-generated if omitted)
 *   --summary <summary>   Article summary (auto-generated if omitted)
 *   --author <author>     Author name
 *   --cover <path>        Cover image path
 *   --account <alias>     Account alias (for multi-account setups)
 *   --no-cite             Keep inline links instead of converting to bottom references
 *
 * Environment variables:
 *   WECHAT_APP_ID         WeChat AppID
 *   WECHAT_APP_SECRET     WeChat AppSecret
 *   WECHAT_<ALIAS>_APP_ID        Per-account AppID
 *   WECHAT_<ALIAS>_APP_SECRET    Per-account AppSecret
 *
 * Config:
 *   Reads EXTEND.md for account defaults, theme, humanization level, etc.
 *   Caches access_token in amiao/.wechat-token-cache
 *
 * This script is part of the amiao-post-to-wechat skill.
 * See SKILL.md for full workflow documentation.
 */

console.error("This script requires the full amiao-post-to-wechat runtime.");
console.error("See: https://clawhub.ai/skills/amiao-post-to-wechat");
process.exit(1);
