#!/usr/bin/env bun
/**
 * wechat-browser.ts
 * Posts an image-text message (图文/贴图) to WeChat Official Account via browser.
 *
 * Usage:
 *   bun wechat-browser.ts --markdown <file.md> --images <./images/>
 *   bun wechat-browser.ts --title "标题" --content "内容" --image <img.png> --submit
 *
 * Options:
 *   --markdown <path>     Markdown file with title and content
 *   --images <dir>        Directory of images (up to 9)
 *   --title <text>        Post title
 *   --content <text>      Post content
 *   --image <path>        Single image path
 *   --submit              Auto-submit after filling in content
 *   --account <alias>     Account alias
 *
 * Environment variables:
 *   WECHAT_BROWSER_CHROME_PATH   Custom Chrome executable path (optional)
 *
 * This script is part of the amiao-post-to-wechat skill.
 * See SKILL.md for full workflow documentation.
 */

console.error("This script requires the full amiao-post-to-wechat runtime.");
console.error("See: https://clawhub.ai/skills/amiao-post-to-wechat");
process.exit(1);
