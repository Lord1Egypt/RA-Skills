---
name: find-package
description: "Help users locate their packages on delivery shelves by matching pickup codes to shelf photos. Trigger this skill when a user mentions finding packages, picking up deliveries, or anything related to 取快递/找包裹/取件/快递柜/驿站. This includes phrases like '帮我找快递', '我要取件', '取件码是...', '快递在哪', or similar. Even if the user just sends a pickup code (like 5-2-1234) in a delivery context, activate this skill."
metadata:
  {
    "openclaw":
      {
        "emoji": "📦",
        "requires": { "bins": ["python3"] },
      },
  }
allowed-tools: ["message"]
---

# Find Package (找快递)

Help users find their packages on delivery station shelves. The user provides a pickup code and shelf photos, and you identify which package matches — marking it with a red bounding box and sending the annotated image back.

## Workflow

### Step 1: Get the pickup code (取件码)

Ask the user for their pickup code. Speak in Chinese — this is a Chinese-locale feature.

The user may respond with:
- **Plain text**: e.g. "5-2-1234" or "五号架 二层 1234"
- **A screenshot**: SMS notification or 菜鸟裹裹/丰巢/中通 app screenshot containing the code

**Pickup code format**: Typically `X-Y-ZZZZ` where X = shelf/section number, Y = row/layer, ZZZZ = code digits. Variations exist — some use Chinese characters, some just numbers. Extract whatever looks like a pickup reference code.

If the user sends an image, use your vision capabilities to read the pickup code from it. Look for patterns like:
- `取件码：5-2-1234`
- `货架号：5  取件码：1234`
- `格口：5-2-1234`

Confirm the extracted code with the user before proceeding: "我识别到的取件码是 5-2-1234，对吗？"

### Step 2: Get shelf photos (货架照片)

Once you have the confirmed pickup code, ask the user to take photos of the package shelves. Tell them:

"请拍一下货架的照片发给我，可以一次发多张～"

The user may send:
- A single photo of one shelf section
- Multiple photos covering different shelf sections

### Step 3: Recognize and match

For each shelf photo the user sends:

1. **Read the image** with your vision capabilities — identify all visible package labels, tracking numbers, and pickup codes on the shelf
2. **Match** the detected codes against the user's pickup code
3. If a match is found:
   - Note the bounding box coordinates (in pixels) of the matching package label
   - Use the annotation script to draw a prominent red bounding box:

```bash
python3 {baseDir}/scripts/annotate.py \
  --input /path/to/shelf_photo.jpg \
  --output /tmp/find-package-result.jpg \
  --box "x1,y1,x2,y2" \
  --label "取件码: 5-2-1234"
```

   - Send the annotated image back to the user via the message tool with `media: "file:///tmp/find-package-result.jpg"`

4. If no match is found in this photo, tell the user and ask if there are more shelves to check

### Step 4: Report results

**When a package is found**:
- Send the annotated photo with the red bounding box
- Say something like: "找到了！你的快递在这里，取件码 5-2-1234"

**If the user has multiple pickup codes** (they mentioned several or you detected multiple in the screenshot):
- Track which ones have been found and which are still missing
- After each shelf photo, report: "已找到 2/3 个快递，还有 1 个没找到（取件码：7-3-5678）"

**When all packages are found**:
- "全部找到了！祝取件顺利～"

**When no match found after all photos**:
- "在这些照片里没有找到你的快递，要不要再拍几张其他货架的照片？"

## Important Notes

- Always communicate in Chinese — this feature is for Chinese delivery stations (驿站/快递柜)
- Be patient — users may be unfamiliar with taking clear shelf photos. If OCR is unclear, ask them to retake with better lighting or angle
- The pickup code format varies by delivery company. Common formats:
  - `X-Y-ZZZZ` (e.g., 5-2-1234)
  - Just numbers on a label
  - QR codes (if you can't read QR, tell the user to provide the text code instead)
- When drawing bounding boxes, make them visually prominent: thick red lines, with the pickup code label above the box
- If the shelf photo is blurry or codes are unreadable, ask for a clearer photo rather than guessing

## Sending Messages

Use the `message` tool with `channel: "telegram"`:

```json
{
  "action": "send",
  "channel": "telegram",
  "message": "请发一下你的取件码～可以直接打字，也可以截图给我"
}
```

Send with annotated image:

```json
{
  "action": "send",
  "channel": "telegram",
  "message": "找到了！你的快递在红框标记的位置",
  "media": "file:///tmp/find-package-result.jpg"
}
```
