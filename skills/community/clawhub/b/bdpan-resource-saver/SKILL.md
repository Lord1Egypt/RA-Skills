---
name: bdpan-resource-saver
description: Search for resources using Bing/Baidu, find Baidu Netdisk (百度网盘) share links, and save/transfer them to your netdisk. Use when the user wants to (1) Search for movies, TV shows, books, or other resources and save to netdisk, (2) Find Baidu Netdisk share links for specific content, (3) Save/share/transfer resources to their Baidu Netdisk automatically, (4) Direct requests like "save xxx movie to my netdisk", "transfer xxx to baidu netdisk", "转存xxx电影到百度网盘", "帮我找xxx资源并保存到网盘". Triggers include "search for [movie/show/book]", "find [content] on Baidu Netdisk", "save to netdisk", "transfer to netdisk", "百度网盘资源", "转存到网盘", "保存到网盘", "转存xxx到百度网盘", "save xxx movie to my netdisk".
---

# Baidu Netdisk Resource Saver

## Overview

This skill automates the workflow of searching for resources (movies, TV shows, books, etc.) and saving them to Baidu Netdisk (百度网盘). It combines web search, browser automation, and netdisk operations.

### Trigger Patterns (When to Use This Skill)

This skill should be triggered when user requests match these patterns:

**Direct Transfer Requests:**
- "请帮我转存[xxx]电影至我的百度网盘"
- "save [xxx] movie to my netdisk"
- "transfer [xxx] to my baidu netdisk"
- "帮我把[xxx]保存到百度网盘"
- "转存[xxx]到网盘"

**Search + Save Requests:**
- "帮我找[xxx]资源并保存到网盘"
- "search for [xxx] and save to netdisk"
- "找[xxx]电影并转存"

**Resource Search:**
- "百度网盘[xxx]资源"
- "find [xxx] on baidu netdisk"
- "search [xxx] 百度网盘"

## Workflow

### Step 1: Search for Resources

Use web search (Bing/Baidu) to find Baidu Netdisk share links for the requested content.

**Search query format:**
```
[资源名称] [年份/版本] 百度网盘 pan.baidu.com
```

**Example searches:**
- "查理和巧克力工厂 2005 百度网盘 pan.baidu.com"
- "The Matrix 4K 百度网盘"
- "三体 电视剧 百度网盘"

### Step 2: Extract Share Links

From search results, extract:
- Share link URL (format: `https://pan.baidu.com/s/[CODE]`)
- Extraction code/password (提取码) if available
- File name and description

### Step 3: Verify and Access Share

Use browser automation to:
1. Navigate to the share link
2. Enter extraction code if required
3. Verify the file exists and is accessible
4. Check file details (name, size, expiration)

### Step 4: Save to Netdisk

**Option A: Direct CLI transfer (preferred)**
Use `bdpan transfer` command:
```bash
bdpan transfer <share-link> -p <password> -d <target-folder>
```

**Option B: Browser automation**
If CLI fails:
1. Navigate to share page in browser
2. Click "保存到网盘" (Save to Netdisk)
3. Select target folder (e.g., "我的资源")
4. Confirm save operation

### Step 5: Verify Save

Confirm the file was saved successfully by:
- Checking target folder contents via `bdpan ls`
- Or verifying in browser

## Common Issues & Solutions

### Issue: Share link expired or invalid
**Solution:** Search for alternative links from different sources.

### Issue: "转存文件超过可用空间" (Insufficient space)
**Solution:** 
- Check current usage: `bdpan quota`
- Clean up space or purchase expansion
- Report space issue to user

### Issue: CLI returns HTTP 400 error
**Solution:** Use browser automation instead. Some share links have restrictions that prevent API access.

### Issue: Browser login required
**Solution:** 
- User needs to manually log in via browser first
- Or use the already-authenticated bdpan CLI session

## Commands Reference

### bdpan CLI Commands
```bash
# List files
bdpan ls [path]

# Create folder
bdpan mkdir <folder-name>

# Transfer share to netdisk
bdpan transfer <share-link> -p <password> -d <target-folder>

# Download from share
bdpan download <share-link> <local-path> -p <password>

# Check quota
bdpan quota
```

### Browser Commands
```bash
# Start browser
browser start

# Navigate to URL
browser navigate <url>

# Click element
browser click --ref=<ref>

# Type text
browser type --ref=<ref> --text=<text>

# Get page snapshot
browser snapshot
```

## Best Practices

1. **Always verify share links** before attempting transfer - some may be expired or fake
2. **Check netdisk space** before saving to avoid errors
3. **Prefer CLI methods** for reliability, fallback to browser automation
4. **Save to organized folders** (e.g., "我的资源/电影/", "我的资源/电视剧/")
5. **Report share information** to user: link, password, file size, expiration

## Example Sessions

### Example 1: Search + Save Request
**User:** "帮我找查理和巧克力工厂的电影资源并保存到网盘"

**Agent workflow:**
1. Search: `查理和巧克力工厂 2005 百度网盘 pan.baidu.com`
2. Find: Link `https://pan.baidu.com/s/1RuPACBpk-1BY_fZl6DIirA`, pwd: `fyzv`
3. Verify via browser: File "133 查理和巧克力工厂 2005" exists
4. Check space: 136.2GB/105GB used (full!)
5. Report to user: Found resource but netdisk full, needs cleanup

### Example 2: Direct Transfer Request
**User:** "请帮我转存星际穿越电影至我的百度网盘"

**Agent workflow:**
1. Parse: User wants to transfer "星际穿越" movie to netdisk
2. Search: `星际穿越 百度网盘 pan.baidu.com`
3. Find and verify available share links
4. Attempt transfer via `bdpan transfer` or browser automation
5. Report success or specific error (space full, link expired, etc.)

### Example 3: English Request
**User:** "Save The Matrix to my netdisk"

**Agent workflow:**
1. Parse: User wants "The Matrix" movie saved
2. Search: `The Matrix 百度网盘 pan.baidu.com`
3. Find share link with extraction code
4. Transfer to user's "我的资源" folder
5. Confirm save location and file details

## References

For detailed browser automation patterns, see [references/browser-patterns.md](references/browser-patterns.md)
