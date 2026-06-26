#!/usr/bin/env bun
/**
 * md-to-wechat.ts
 * Converts a Markdown file to WeChat-ready HTML without publishing.
 *
 * Usage:
 *   bun md-to-wechat.ts <file.md> --theme <theme> [options]
 *
 * Options:
 *   --theme <theme>       Visual theme (default: default)
 *   --color <color>       Accent color
 *   --output <path>       Output HTML file path (default: stdout)
 *
 * Use this when you need the converted HTML for manual review
 * or external paste — without triggering a publish.
 *
 * This script is part of the amiao-post-to-wechat skill.
 * See SKILL.md for full workflow documentation.
 */

console.error("This script requires the full amiao-post-to-wechat runtime.");
console.error("See: https://clawhub.ai/skills/amiao-post-to-wechat");
process.exit(1);
