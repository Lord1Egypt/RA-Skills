---
name: gemini-browser-image
description: Generate images with the user's own Chrome session and Gemini web UI. Use for article covers, illustrations, and social media visuals when the user explicitly asks for image generation or article images. Requires an already-authorized Gemini account and user-controlled browser session; does not handle credentials, bypass access controls, or solve CAPTCHAs.
---

# Gemini Browser Image

## Safety boundaries

- Use only with the user's own browser profile and Gemini account.
- Do not bypass login, paywalls, CAPTCHAs, rate limits, or access controls.
- Do not extract, store, print, or publish cookies, tokens, browser profile data, or account secrets.
- If Gemini blocks a prompt or generation fails, revise the prompt or ask the user; do not attempt evasion.
- Download only the image assets generated for the current user-requested task.

## 概述

通过 Chrome 浏览器 + Gemini AI 生成图片并下载。使用 `mcporter` 调用 `chrome-devtools-mcp` 控制浏览器，模拟人工操作完成图片生成。

**核心流程**：启动 Chrome → 打开 Gemini → 输入提示词 → 等待生成 → 点击下载 → 复制到目标目录

---

## 前置条件

### 1. Chrome 必须在运行（带远程调试端口）

```powershell
# 检查 Chrome 是否已运行
netstat -ano | Select-String "9222"

# 如果没有运行，启动 Chrome
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222","--user-data-dir=<your-chrome-user-data-dir>"
```

### 2. chrome-devtools-mcp 必须在运行

```powershell
# 检查 MCP 服务器状态
mcporter list

# 应该看到：chrome-devtools (29 tools, x.xs) ✔ Listed 1 server (1 healthy)

# 如果没有运行，启动 MCP 服务器
cmd /c "cd /d <your-npm-global-dir> && npx chrome-devtools-mcp@latest --autoConnect --experimentalStructuredContent --experimental-page-id-routing"
```

**自动重连**：MCP 服务器会自动连接到已运行的 Chrome，无需手动配对。

---

## 完整工作流程

### Step 1: 导航到 Gemini

```powershell
mcporter call chrome-devtools.navigate_page type="url" url="https://gemini.google.com"
```

### Step 2: 获取页面快照，找到输入框

```powershell
mcporter call chrome-devtools.take_snapshot verbose=true
```

从快照中找到：
- 输入框：`textbox "Enter a prompt for Gemini"` → 记下其 UID（如 `uid=3_187`）
- 图片生成按钮：`button "🖼️ Create image"` → 如果有的话

### Step 3: 输入提示词

```powershell
mcporter call chrome-devtools.fill uid="<输入框UID>" value="你的英文提示词"
```

**提示词技巧**：
- 尽量用英文描述，效果更好
- 包含风格关键词：photorealistic, 3D render, vector illustration, watercolor 等
- 说明用途：food photography, hero image, social media post 等
- 添加质量修饰：high quality, detailed, 4K, cinematic lighting 等

### Step 4: 提交生成

```powershell
mcporter call chrome-devtools.press_key key="Enter"
```

### Step 5: 等待图片生成

图片生成需要 **20-60 秒**，期间可以定期检查状态：

```powershell
# 等待 30 秒
Start-Sleep -Seconds 30

# 获取快照查看状态
mcporter call chrome-devtools.take_snapshot verbose=false
```

**成功标志**：看到 "Download full size image" 按钮出现。

**失败标志**：看到 "Redo" 按钮或错误信息。

### Step 6: 点击下载按钮

```powershell
mcporter call chrome-devtools.click uid="<下载按钮UID>"
```

从快照中找到：`button "Download full size image"` → UID（如 `uid=6_6`）

### Step 7: 确认文件已下载

```powershell
Get-ChildItem $env:USERPROFILE\Downloads -File | Sort-Object LastWriteTime -Descending | Select-Object -First 5 | Format-Table Name, Length, LastWriteTime -AutoSize
```

应该看到 `Gemini_Generated_Image_*.png` 文件（通常 1-3MB）。

### Step 8: 复制到目标目录

```powershell
$newFile = Get-ChildItem $env:USERPROFILE\Downloads -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Copy-Item $newFile.FullName "<目标路径\图片名.png>"
```

---

## 常用 mcporter 命令参考

| 操作 | 命令 |
|------|------|
| 列出页面 | `mcporter call chrome-devtools.list_pages` |
| 打开网址 | `mcporter call chrome-devtools.navigate_page type="url" url="..."` |
| 获取快照 | `mcporter call chrome-devtools.take_snapshot verbose=true` |
| 填写输入框 | `mcporter call chrome-devtools.fill uid="X_Y" value="..."` |
| 点击元素 | `mcporter call chrome-devtools.click uid="X_Y"` |
| 按键盘 | `mcporter call chrome-devtools.press_key key="Enter"` |
| 执行JS | `mcporter call chrome-devtools.evaluate_script function="() => ..."` |
| 截图 | `mcporter call chrome-devtools.take_screenshot format="png"` |
| 等待 | `Start-Sleep -Seconds X` |

---

## 图片提示词模板

### 封面图（2.35:1，900x383）
```
Professional hero image for article about [主题], modern design, clean layout, [风格: minimalist/corporate/vibrant], high quality, 4K
```

### 文章配图（16:9，800x450）
```
Illustrated [主题] concept, [风格: flat/realistic/abstract], clean design suitable for blog post, soft lighting, high quality
```

### 社交媒体图片
```
Social media post design about [主题], [平台] format, eye-catching, modern graphic design, vibrant colors, professional quality
```

### 食物/产品图
```
Professional [food/product] photography, [具体描述], studio lighting, appetizing, high resolution, commercial quality
```

---

## 完整示例

生成一张小龙虾图片：

```powershell
# Step 1: 打开 Gemini
mcporter call chrome-devtools.navigate_page type="url" url="https://gemini.google.com"

# Step 2: 获取快照
mcporter call chrome-devtools.take_snapshot verbose=true
# 找到输入框 uid=3_187

# Step 3: 输入提示词
mcporter call chrome-devtools.fill uid="3_187" value="Generate a realistic photo of a plate of delicious Sichuan spicy crayfish (小龙虾), with bright red shells, garlic and scallions garnish, atmospheric lighting, food photography style, appetizing and mouth-watering"

# Step 4: 提交
mcporter call chrome-devtools.press_key key="Enter"

# Step 5: 等待30秒后检查
Start-Sleep -Seconds 30
mcporter call chrome-devtools.take_snapshot verbose=false

# Step 6: 找到下载按钮 UID（如 6_6）并点击
mcporter call chrome-devtools.click uid="6_6"

# Step 7: 检查下载
Get-ChildItem $env:USERPROFILE\Downloads -File | Sort-Object LastWriteTime -Descending | Select-Object -First 3

# Step 8: 复制到工作目录
$newFile = Get-ChildItem $env:USERPROFILE\Downloads -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Copy-Item $newFile.FullName "<output-dir>\\crayfish.png"
```

---

## 多标签并行生成流程（推荐）

当需要生成多张图片时（如文章配图5张），使用此流程可以大幅节省时间。

**核心思路**：流水线式操作——填完提示词就切走，生成和准备并行。

### 操作步骤

#### 准备工作：清理旧标签

```powershell
# 查看当前所有标签
mcporter call chrome-devtools.list_pages

# 关闭多余标签（除了正在用的，关闭其他）
mcporter call chrome-devtools.close_page pageId="2"
# 重复直到只剩1个标签
```

#### 流水线填入（快速连续操作）

**标签1：填提示词1 → 发送 → 开标签2**
```powershell
# 获取输入框UID（假设 uid=6_192）
mcporter call chrome-devtools.take_snapshot verbose=false
mcporter call chrome-devtools.fill uid="6_192" value="[提示词1]"
mcporter call chrome-devtools.press_key key="Enter"
# 立即开新标签
mcporter call chrome-devtools.new_page url="https://gemini.google.com" background=false
```

**标签2：填提示词2 → 发送 → 开标签3**
```powershell
# 等几秒让新标签加载完成
Start-Sleep -Seconds 2
# 获取输入框UID
mcporter call chrome-devtools.take_snapshot verbose=false
# 填写提示词2（输入框 UID 变了，如 uid=21_19）
mcporter call chrome-devtools.fill uid="21_19" value="[提示词2]"
mcporter call chrome-devtools.press_key key="Enter"
mcporter call chrome-devtools.new_page url="https://gemini.google.com" background=false
```

**标签3-5：重复上述步骤**

#### 等待所有生成完成

```powershell
# 等45-50秒（足够生成时间）
Start-Sleep -Seconds 50
```

#### 依次下载

```powershell
# 切换到标签1，下载图片
mcporter call chrome-devtools.select_page pageId="1" bringToFront=true
mcporter call chrome-devtools.take_snapshot verbose=false
# 找到 "Download full size image" 按钮的 UID（如 uid=23_14）
mcporter call chrome-devtools.click uid="23_14"

# 切换到标签2，下载
mcporter call chrome-devtools.select_page pageId="2" bringToFront=true
mcporter call chrome-devtools.take_snapshot verbose=false
# 找下载按钮并点击

# 依次完成所有标签...
```

#### 确认下载

```powershell
Get-ChildItem $env:USERPROFILE\Downloads -File | Where-Object { $_.Name -like "Gemini_Generated_Image_*" } | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

### 时间对比

| 方案 | 5张图耗时 |
|------|----------|
| 串行（一张一张来） | 5 × 45秒 ≈ 6分钟 |
| 并行多标签（本方案） | 45秒 + 操作时间 ≈ 2-3分钟 |

### 关键发现

1. **生成是并行的**：不管标签是否在最前面，只要有提交就会生成
2. **每个新标签的输入框 UID 都会变**：必须每次 `take_snapshot` 获取，不能复用
3. **标签号 ≠ 快照里的 page ID**：`list_pages` 显示的序号和快照内容不完全对应，要靠 `You said` 标题区分
4. **每个 `You said` 下都有独立的下载按钮**：一个标签内可能有多张图（如果之前有残留）

### 注意事项

1. **新标签必须等页面完全加载**：`new_page` 后等 2 秒再 `take_snapshot`
2. **边生成边开标签**：填完当前提示词就切走开新标签，不用等生成完
3. **下载时找准 `You said` 标题**：确认下载的是哪张图

---

## 故障排除

| 问题 | 解决方法 |
|------|---------|
| `chrome-devtools` not found | 运行 `npx chrome-devtools-mcp@latest --autoConnect` |
| Chrome 没有监听 9222 | 重启 Chrome 加 `--remote-debugging-port=9222` 参数 |
| 点击下载没反应 | 等更长时间，用快照确认下载按钮存在 |
| 下载的文件是空的 | 重新点击下载按钮，或刷新页面重试 |
| 提示词不执行 | 确认输入框已获得焦点，可先点击输入框再 fill |



