---
name: bili-sunflower-publish
description: Publish HTML or Markdown content to Bilibili — supports both 专栏 (article) and 小站 (tribee) targets. Handles login check, title input, content injection via editor API, and direct publish. Trigger when user asks to publish to B站专栏/小站, or mentions 发布文章到B站/上传专栏/发B站文章/发小站帖子/tribee发帖.
---

# bili-sunflower-publish

Unified publish pipeline for Bilibili: HTML/Markdown file → editor → publish. Uses `window.editor` API directly — no system clipboard dependency.

Supports two targets:

- **专栏 (Article)**: long-form articles on `member.bilibili.com`
- **小站 (Tribee)**: community posts on `bilibili.com/bubble`

## Prerequisites

- **Browser tool** with `openclaw` profile (Playwright-managed browser)

## Input

- **Content file path** (article body) — supports `.html` and `.md` / `.markdown` files
- **Target type**: `article` (专栏) or `tribee` (小站) — infer from user intent
- **Title** (optional — see Phase 2)
- For tribee: **tribee name or ID** (required)
- For tribee: **分区** (category, optional — user can specify or choose during publish)

---

## Phase 1: Navigate & Login Check

### Article mode

Navigate to `https://member.bilibili.com/york/read-editor` and take a snapshot.

- **Logged in**: editor loads with title textbox `"请输入标题（建议30字以内）"`
- **Not logged in**: redirects to login page

### Tribee mode

Publish URL: `https://www.bilibili.com/bubble/publish?tribee_id={id}&tribee_name={name}`

Both `tribee_id` and `tribee_name` are required for the publish URL. Resolve missing params:

| User provides | Resolution                                                                                                                                            |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| id + name     | Direct → publish URL                                                                                                                                  |
| id only       | Navigate to `https://www.bilibili.com/bubble/home/{id}`, extract tribee name from the page, then → publish URL                                        |
| name only     | Search `https://search.bilibili.com/all?keyword={name}`, find the card linking to `bilibili.com/bubble/home/{id}`, extract `{id}`, then → publish URL |

After navigating to the publish URL:

- **Logged in + member**: editor loads with title and body area
- **Not logged in**: redirects to login page
- **Not a member**: may show join prompt — tell user to join the tribee first

If not logged in, **stop and tell the user** to log in manually in the openclaw browser profile, then retry.

---

## Phase 2: Preprocess & Title Handling

Run the preprocess script matching the file type. The script handles H1 extraction, heading promotion, image inlining, and (for HTML) whitespace cleanup.

### 2a. For `.html` files

```bash
python3 {SKILL_DIR}/scripts/preprocess_html.py <input.html> [output-dir]
```

Output (stdout, 3 lines):

```
title=<extracted title>
path=<processed html file path>
bytes=<html byte size>
```

Parse `title` and `path` from the output. The processed HTML at `path` is ready for injection in Phase 3.

### 2b. For `.md` / `.markdown` files

```bash
python3 {SKILL_DIR}/scripts/preprocess_md.py <input.md> [output-dir]
```

Output (stdout, 3 lines):

```
title=<extracted title>
path=<processed md file path>
bytes=<md byte size>
```

Parse `title` and `path` from the output. The processed Markdown at `path` is ready for injection in Phase 3.

### 2c. Title validation

If the user provided a title explicitly, use it instead of the script-extracted one.

After resolving, validate:

- **Title > 50 characters**: present 2-3 shortened alternatives, let user choose
- **Title looks meaningless** (e.g. `output`, `untitled`, `temp`, or clearly unrelated to the content): read the first few hundred chars of body, generate 2-3 title suggestions, let user choose

Do NOT silently use a bad title. Wait for user selection before proceeding.

Enter the title: click the title textbox and type.

---

## Phase 3: Insert Article Body

Both editors share the same rich-text editor component (`window.editor`).

Use the preprocessed content from Phase 2 and inject it into the editor.

**IMPORTANT — JS string escaping:**

Content (HTML or Markdown) often contains characters that break JS syntax (backticks, quotes, newlines, backslashes, etc.). You **must** use the method below to safely construct the JS code. **Do NOT** paste raw content directly into a JS variable assignment.

### How to construct the evaluate JS code

Follow these steps **exactly** for both HTML and Markdown injection:

1. Get the processed file path from Phase 2 output (`path=...`)
2. Run the following command to produce a JSON-escaped string of the file content:

```bash
python3 -c "import json,sys; print(json.dumps(open(sys.argv[1]).read()))" <processed-file-path>
```

This outputs a double-quoted JSON string with all special characters escaped (newlines, quotes, backslashes, etc.), e.g. `"line1\nline2\"quoted\""`.

3. Capture the stdout output as `ESCAPED_JSON_STRING`
4. Build the full JS code by embedding `ESCAPED_JSON_STRING` into the template (see 3a-HTML / 3a-MD below). It already includes its own surrounding double quotes, so place it directly after `JSON.parse(` with no additional quotes.

### 3a-HTML. Processed HTML → ClipboardEvent dispatch

```javascript
(function () {
  const html = JSON.parse(ESCAPED_JSON_STRING);
  const clipboardData = new DataTransfer();
  clipboardData.setData('text/html', html);
  clipboardData.setData('text/plain', '');

  const pasteEvent = new ClipboardEvent('paste', {
    bubbles: true,
    cancelable: true,
    clipboardData,
  });

  window.editor.view.dom.dispatchEvent(pasteEvent);
})();
```

**Note:** If the HTML content is large (>50KB), split it into chunks and paste sequentially.

### 3a-MD. Processed Markdown → editor importMarkdown command

```javascript
(function () {
  const markdown = JSON.parse(ESCAPED_JSON_STRING);
  window.editor.commands.importMarkdown({
    content: markdown,
    replaceContent: true,
  });
})();
```

### 3b. Verify content

Evaluate JS to confirm content was inserted:

```javascript
(function () {
  const e = window.editor.view.dom;
  return { chars: e.textContent.length, first80: e.textContent.substring(0, 80) };
})();
```

Expected: `chars > 100` and `first80` matches the article opening.

---

## Phase 4: Publish

### Article mode

Editor bottom has a "发布设置" panel (usually already visible) with defaults that work out of the box:

- 可见范围: 所有人可见 (default)
- 封面: auto-generated from body text (default)
- 评论: enabled (default)

If the user has specific publishing preferences, adjust before publishing:

| 设置          | 操作                                  | 说明                            |
| ------------- | ------------------------------------- | ------------------------------- |
| 可见范围      | 选 radio: "所有人可见" / "仅自己可见" | 仅自己可见不支持分享和商业推广  |
| 自定义封面    | 勾选 checkbox → 上传图片              | 不设则自动抓正文开头文字        |
| 评论开关      | 勾选/取消 checkbox                    | 关闭后无法评论                  |
| 精选评论      | 勾选 checkbox                         | 开启后需手动筛选评论才展示      |
| 定时发布      | 勾选 checkbox → 选择时间              | 范围: 当前+2h ~ 7天内，北京时间 |
| 创作声明-原创 | 勾选 checkbox                         | 声明原创，禁止转载              |
| 创作声明-AI   | 勾选 checkbox                         | 标识使用 AI 合成技术            |
| 话题          | 点击"添加话题"按钮                    | 可选                            |
| 文集          | 点击"选择文集"按钮                    | 可选                            |

Steps:

1. Scroll down to confirm the "发布设置" panel is visible; if collapsed, click "发布设置" button to expand
2. Apply any user-requested settings from the table above
3. Click **"发布"** button (next to "保存为草稿", at the bottom right)
4. If a confirmation dialog appears, confirm
5. Verify publish succeeded (URL changes or success toast)

### Tribee mode

Bottom bar appears after content is entered, with defaults that work out of the box:

- 分区: 未选择 (some tribees may require)
- 同步至动态: enabled (default)

If the user has specific preferences, adjust before publishing:

| 设置       | 操作                          | 说明                         |
| ---------- | ----------------------------- | ---------------------------- |
| 分区       | 点击"选择分区"下拉 → 选择分区 | 部分小站可能必选             |
| 同步至动态 | 取消勾选 checkbox             | 默认开启，取消后不同步到动态 |

#### 分区自动选择（Tribee only）

When the user **did not specify** a 分区:

1. Click "选择分区" dropdown to reveal available options
2. Read the list of 分区 names from the dropdown (snapshot)
3. Based on the **article title + first ~200 chars of body content**, pick the most relevant 分区:
   - Match by keyword/topic similarity (e.g. tutorial content → "经验分享", questions → "提问求助")
   - If no option is a clear fit, pick the most general/catch-all option
   - If the tribee only has 1-2 generic options, just pick the best one without overthinking
4. Click the chosen 分区
5. Do **not** ask the user to confirm — just pick and proceed (they can always re-publish if wrong)

If the user **did specify** a 分区, use it directly (skip auto-selection).

Steps:

1. Handle 分区 (user-specified or auto-selected per above)
2. Apply any other user-requested settings
3. Click **"发布"** button (blue, bottom right)
4. Verify publish succeeded

---

## Execution

Default: execute Phase 1 → 4 directly in the main session (supports user interaction for login/title).

Only delegate to subagent if the user explicitly requests it.
