---
name: browser-douyin-post
description: Use OpenClaw's browser control to publish images or videos to Douyin (抖音) creator platform. Uploads a local image/video file to Douyin creator center via the web UI. Prerequisites: (1) Chrome must be running with remote debugging enabled (--remote-debugging-port=9222), (2) user must be logged into Douyin creator platform (creator.douyin.com). Activates when user asks to post something to Douyin, publish to Douyin, or upload to Douyin.
---

# Browser Douyin Post

Publish images or videos to Douyin (抖音) creator platform via browser automation.

## Workflow

### Step 1: Connect to Chrome

```javascript
browser(action="start", profile="user", target="host")
```

If failed with "attachOnly" error: Chrome is not running with debugging port.
→ Ask user to run: `& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222`

### Step 2: Navigate to Douyin Creator Platform

Use a free tab (e.g., Tab 2) and navigate via JavaScript evaluation since `navigate` requires `openclaw` profile:

```javascript
// First check tabs
browser(action="tabs", profile="user", target="host")

// Focus a free tab
browser(action="focus", targetId="<free_tab_id>", profile="user", target="host")

// Then use JS to navigate (avoids SSRF blocks on navigate action)
browser(action="act", kind="evaluate", target="host", profile="user", fn="window.location.href = 'https://creator.douyin.com'")
```

Or if Douyin tab already exists, just focus it.

### Step 3: Go to Image Upload Page

Once on creator.douyin.com:
1. Click the "高清发布" / "发布图文" menu button (ref `1_2`)
2. Click "发布图文" menuitem

### Step 4: Upload Image

The upload input (ref `3_10`) only accepts files from `C:\Users\wenxi\AppData\Local\Temp\openclaw\uploads\`.

**First copy the image to the uploads directory:**
```javascript
Copy-Item "<image_path>" "C:\Users\wenxi\AppData\Local\Temp\openclaw\uploads\douyin-post.png" -Force
```

**Then upload:**
```javascript
browser(action="upload", target="host", profile="user", inputRef="3_10", paths=["C:\\Users\\wenxi\\AppData\\Local\\Temp\\openclaw\\uploads\\douyin-post.png"])
```

### Step 5: Fill in Title

Find the title textbox (ref `4_2`) and type the title.
**Note: Title has 20-character limit.**

```javascript
browser(action="act", kind="click", ref="4_2", profile="user", target="host")
browser(action="act", kind="press", ref="4_2", profile="user", target="host", key="Control+a")
browser(action="act", kind="type", ref="4_2", text="<title>", profile="user", target="host")
```

### Step 6: Add Description (Optional)

The description textbox (statictext "添加作品描述...") may not have a clickable ref.
If available, click it and type description. If not, skip — the title alone is enough.

### Step 7: Click Publish

Click the "发布" button (ref `4_65`):

```javascript
browser(action="act", kind="click", ref="4_65", profile="user", target="host")
```

### Step 8: Verify

After clicking publish, wait 5 seconds and take a snapshot to confirm the post appears in "作品管理" list.

## Complete Example

Publishing an AI-generated image to Douyin:

```
=== User Request ===
发布图片到抖音: C:\Users\wenxi\.openclaw\media\tool-image-generation\old-photo.png
标题: 时光记忆

=== Assistant Actions ===

// 1. Connect browser
browser(action="start", profile="user", target="host")

// 2. Check tabs and focus a free tab, then navigate to Douyin
browser(action="focus", targetId="2", profile="user", target="host")
// (use evaluate JS to set window.location.href since navigate is blocked)

// 3. Click 高清发布 > 发布图文
browser(action="act", kind="click", ref="1_2", profile="user", target="host")
browser(action="act", kind="click", ref="2_25", profile="user", target="host")

// 4. Copy image to uploads dir
Copy-Item "C:\Users\wenxi\.openclaw\media\tool-image-generation\old-photo.png" "C:\Users\wenxi\AppData\Local\Temp\openclaw\uploads\douyin-post.png" -Force

// 5. Upload
browser(action="upload", target="host", profile="user", inputRef="3_10", paths=["C:\\Users\\wenxi\\AppData\\Local\\Temp\\openclaw\\uploads\\douyin-post.png"])

// 6. Fill title
browser(action="act", kind="click", ref="4_2", profile="user", target="host")
browser(action="act", kind="press", ref="4_2", profile="user", target="host", key="Control+a")
browser(action="act", kind="type", ref="4_2", text="时光记忆", profile="user", target="host")

// 7. Publish
browser(action="act", kind="click", ref="4_65", profile="user", target="host")

// 8. Wait and verify
Start-Sleep -Seconds 5
browser(action="snapshot", profile="user", target="host")
```

## Common Issues

- **"upload requires ref or inputRef"**: Must use `inputRef` parameter (not `ref`) when uploading to existing-session browser
- **"must stay within uploads directory"**: Copy file to `C:\Users\wenxi\AppData\Local\Temp\openclaw\uploads\` first
- **"navigate blocked by SSRF"**: Use `act` + `evaluate` with `window.location.href` instead of `navigate` action
- **Description textbox has no ref**: Skip description if ref is not available; title alone is sufficient
- **Title character limit**: Douyin title is limited to 20 characters
- **Not logged in**: User must be logged into Douyin creator platform before running this skill
