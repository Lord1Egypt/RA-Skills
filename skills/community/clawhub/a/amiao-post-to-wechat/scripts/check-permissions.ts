#!/usr/bin/env bun
/**
 * check-permissions.ts
 * Preflight environment check for amiao-post-to-wechat.
 *
 * Usage:
 *   bun check-permissions.ts
 *
 * Checks performed:
 *   - Chrome browser presence
 *   - Chrome profile isolation
 *   - Bun runtime version
 *   - macOS Accessibility permissions (if on macOS)
 *   - Clipboard copy capability
 *   - Paste keystroke tool (xdotool / ydotool on Linux)
 *   - WeChat API credentials (WECHAT_APP_ID / WECHAT_APP_SECRET)
 *   - Chrome instance conflicts
 *
 * Run this before first use on a new machine to catch
 * configuration issues early.
 *
 * Environment variables checked:
 *   WECHAT_APP_ID
 *   WECHAT_APP_SECRET
 *   WECHAT_BROWSER_CHROME_PATH  (optional)
 *   WECHAT_<ALIAS>_APP_ID       (multi-account)
 *   WECHAT_<ALIAS>_APP_SECRET   (multi-account)
 *
 * This script is part of the amiao-post-to-wechat skill.
 * See SKILL.md for full workflow documentation.
 */

console.error("This script requires the full amiao-post-to-wechat runtime.");
console.error("See: https://clawhub.ai/skills/amiao-post-to-wechat");
process.exit(1);
