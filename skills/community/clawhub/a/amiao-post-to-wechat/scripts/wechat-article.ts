#!/usr/bin/env bun
/**
 * wechat-article.ts
 * Publishes a WeChat article via browser automation (Chrome).
 *
 * Usage:
 *   bun wechat-article.ts --markdown <file.md> --theme <theme> [options]
 *   bun wechat-article.ts --html <file.html> [options]
 *
 * Options:
 *   --markdown <path>     Input markdown file
 *   --html <path>         Input HTML file
 *   --theme <theme>       Visual theme
 *   --color <color>       Accent color
 *   --account <alias>     Account alias
 *   --no-cite             Keep inline links
 *
 * Environment variables:
 *   WECHAT_BROWSER_CHROME_PATH   Custom Chrome executable path (optional)
 *
 * Requirements:
 *   - Google Chrome installed
 *   - macOS: Accessibility permission enabled for terminal app
 *   - Linux: xdotool or ydotool installed for paste keystroke
 *
 * This script is part of the amiao-post-to-wechat skill.
 * See SKILL.md for full workflow documentation.
 */

console.error("This script requires the full amiao-post-to-wechat runtime.");
console.error("See: https://clawhub.ai/skills/amiao-post-to-wechat");
process.exit(1);
