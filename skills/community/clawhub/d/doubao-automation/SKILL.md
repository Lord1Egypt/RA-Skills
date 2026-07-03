---
name: doubao-automation
description: "豆包自动化操作技能 - 基于 Playwright CDP 协议接管已登录 Edge 浏览器，实现豆包 AI 的自动化操作。支持批量生成图片、批量生成视频、文本对话、下载生成内容等。触发词：豆包自动化、操作豆包、豆包生成图片、豆包生成视频、豆包批量生成。"
agent_created: true
---

# 豆包自动化操作 Skill

基于 CDP (Chrome DevTools Protocol) + Playwright 技术，接管已登录的 Edge 浏览器来操作豆包，完美解决登录态问题。

---

## ⚠️ 首次使用必读：登录引导

> **本 skill 适用于「已登录豆包」的 Edge 浏览器。**
> 如果您是**第一次使用**，必须先完成登录，否则自动化脚本无法操作豆包。

### 情况一：Edge 浏览器已登录豆包（推荐）

如果您平时用 Edge 浏览豆包并保持了登录态：

1. **关闭所有 Edge 窗口**
   ```powershell
   taskkill /F /IM msedge.exe
   ```

2. **以 CDP 模式重启 Edge**（会复用您已有的登录态）
   - 直接运行启动脚本：
     ```powershell
     PowerShell -ExecutionPolicy Bypass -File "C:/Users/Owner/.workbuddy/skills/doubao-automation/scripts/start-edge-cdp.ps1"
     ```
   - 或手动执行：
     ```
     "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\Owner\AppData\Local\Microsoft\Edge\User Data"
     ```

3. **验证 CDP 就绪**
   ```bash
   curl -s http://localhost:9222/json/version
   ```
   看到 `"Browser"` 字段即表示成功。

4. **确认豆包登录态**
   在打开的 Edge 窗口中访问 `https://www.doubao.com/`，确认右上角显示头像/用户名。

---

### 情况二：从未登录过豆包（首次使用）

如果您是第一次使用豆包，需要**先手动登录**，再启动 CDP 模式：

#### 方式 A：手机号登录（推荐）

1. 正常打开 Edge 浏览器（非 CDP 模式）
2. 访问 `https://www.doubao.com/`
3. 点击「登录」→ 选择「手机号登录」
4. 输入手机号 → 接收验证码 → 完成登录
5. **不要关闭浏览器**，继续执行上方的「情况一」步骤

#### 方式 B：抖音/微信扫码登录

1. 正常打开 Edge 浏览器
2. 访问 `https://www.doubao.com/`
3. 点击「登录」→ 选择「抖音登录」或「微信登录」
4. 用手机扫描二维码完成登录
5. **不要关闭浏览器**，继续执行上方的「情况一」步骤

#### 方式 C：豆包 App 扫码登录

1. 手机打开豆包 App → 右上角「扫一扫」
2. 电脑 Edge 访问 `https://www.doubao.com/` → 点击「登录」→ 选择「App 扫码」
3. 用手机扫描网页上的二维码完成登录
4. **不要关闭浏览器**，继续执行上方的「情况一」步骤

---

### ✅ 登录成功验证

登录成功后，访问 `https://www.doubao.com/`，页面应满足：
- 右上角显示**头像**或**用户名**（不是「登录」按钮）
- 可以直接发送消息，不需要重新登录

**登录态会随 `--user-data-dir` 持久化，后续使用无需重复登录。**

---

## 技术原理

不新开无登录状态的浏览器，而是通过 CDP 协议连接到用户日常使用的、已登录豆包的 Edge 浏览器，实现"接管式"自动化操作。

---

## 使用场景

当用户提出以下请求时触发此 skill：

- "帮我用豆包生成一张图片"
- "用豆包生成一段视频"
- "批量生成 N 张/条豆包内容"
- "在豆包上问一个问题"
- "帮我操作豆包做 XXX"
- "下载豆包生成的图片/视频"

---

## 前置条件

1. **Edge 浏览器已安装** — 路径：`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
2. **豆包已登录** — ⚠️ **首次使用务必先完成上方「登录引导」**
3. **Node.js 可用** — 使用 WorkBuddy 管理的 Node.js 运行时
4. **Playwright 已安装** — `playwright-core` 已安装在 `C:\Users\Owner\.workbuddy\binaries\node\workspace\node_modules\playwright-core`

---

## 执行流程

### 第一步：以 CDP 模式启动 Edge

**必须先关闭所有 Edge 窗口**，然后以调试模式重新启动：

```bash
# 关闭所有 Edge 进程
taskkill /F /IM msedge.exe 2>/dev/null
sleep 2

# 以 CDP 模式启动（必须带 user-data-dir 以保留登录态）
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  --remote-debugging-port=9222 \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir="$LOCALAPPDATA/Microsoft/Edge/User Data" &

# 等待 CDP 就绪
sleep 8
```

或使用 PowerShell 脚本（推荐）：

```powershell
PowerShell -ExecutionPolicy Bypass -File "C:/Users/Owner/.workbuddy/skills/doubao-automation/scripts/start-edge-cdp.ps1"
```

---

### 第二步：验证 CDP 连接和登录态

```bash
# 验证 CDP 服务
curl -s http://localhost:9222/json/version

# 验证豆包登录态（在打开的 Edge 中访问豆包，确认已登录）
# 如未登录，参考上方「首次使用必读：登录引导」
```

---

### 第三步：执行自动化操作

#### 单条操作

```bash
# 文本对话
node "C:/Users/Owner/.workbuddy/skills/doubao-automation/scripts/doubao-automation.js" \
  --action=chat --prompt="你的问题"

# 生成图片
node "C:/Users/Owner/.workbuddy/skills/doubao-automation/scripts/doubao-automation.js" \
  --action=generate-image --prompt="一只可爱的橘猫" --output="C:/Users/Owner/WorkBuddy/doubao-output"

# 生成视频（文本转视频）
node "C:/Users/Owner/.workbuddy/skills/doubao-automation/scripts/doubao-automation.js" \
  --action=generate-video --prompt="猫咪在草地上奔跑" --output="C:/Users/Owner/WorkBuddy/doubao-output"

# 图片转视频
node "C:/Users/Owner/.workbuddy/skills/doubao-automation/scripts/doubao-automation.js" \
  --action=image-to-video --image="/path/to/image.png" --output="C:/Users/Owner/WorkBuddy/doubao-output"

# 下载最近生成的内容
node "C:/Users/Owner/.workbuddy/skills/doubao-automation/scripts/doubao-automation.js" \
  --action=download-last --output="C:/Users/Owner/WorkBuddy/doubao-output"
```

支持的操作（`--action`）：

| 操作 | 说明 |
|------|------|
| `chat` | 纯文本对话 |
| `generate-image` | 生成图片 |
| `generate-video` | 生成视频（文本转视频） |
| `image-to-video` | 将已有图片转为视频 |
| `download-last` | 下载最近生成的内容到本地 |

#### 批量操作（新增）

```bash
# 批量生成图片（N 条）
node "C:/Users/Owner/.workbuddy/skills/doubao-automation/scripts/doubao-batch-gen.js" \
  --type=image \
  --prompts=" prompts.txt" \
  --output="C:/Users/Owner/WorkBuddy/doubao-output"

# 批量生成视频（N 条）
node "C:/Users/Owner/.workbuddy/skills/doubao-automation/scripts/doubao-batch-gen.js" \
  --type=video \
  --prompts="prompts.txt" \
  --output="C:/Users/Owner/WorkBuddy/doubao-output"
```

`prompts.txt` 格式（每行一条提示词）：
```
一只可爱的橘猫，皮克斯风格
一只金毛犬在沙滩上奔跑，写实风格
科技感城市夜景，赛博朋克风格
```

---

### 第四步：保持浏览器开启

操作完成后保持 Edge 开启，下次使用时无需重新启动。如需关闭：

```bash
taskkill /F /IM msedge.exe
```

---

## 已验证的技术细节

### 经测试确认的选择器

- **聊天输入框**: `textarea[placeholder*="发消息"]` ✅
- **发送按钮**: `button:has(svg)` 或 Enter 键发送 ✅
- **Edge 路径**: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` ✅
- **Playwright 连接**: `chromium.connectOverCDP('http://localhost:9222')` ✅

### 发送消息的可靠方法

推荐使用 `Enter` 键发送，比点击按钮更可靠：

1. 找到 textarea 输入框
2. `input.fill(message)` 填入内容
3. `input.press('Enter')` 发送

---

## 注意事项

1. **必须保持登录态** — 首次使用前在 CDP Edge 中手动登录豆包（见上方登录引导）
2. **浏览器独占** — CDP 模式下 Edge 被脚本独占，期间不要手动操作
3. **频次限制** — 豆包图生视频有免费次数限制，注意控制批量任务数量
4. **页面结构变化** — 豆包前端更新可能导致选择器失效，需维护更新
5. **等待时间** — AI 生成需等待响应，默认超时 180 秒
6. **Edge 版本** — 当前系统 Edge 版本: Edg/116，后续版本可能行为不同

---

## 文件结构

```
doubao-automation/
├── SKILL.md                          # 本文件 — 技能说明与操作指南
└── scripts/
    ├── start-edge-cdp.ps1           # PowerShell 脚本：启动 Edge CDP 模式（含错误处理）
    ├── doubao-automation.js         # Node.js 脚本：CDP 连接 + 豆包单条操作
    └── doubao-batch-gen.js          # Node.js 脚本：CDP 连接 + 豆包批量生成（待创建）
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| CDP 端口被占用 | `taskkill /F /IM msedge.exe` 关闭所有 Edge 后重试 |
| 连接超时/拒绝 | 确认 `curl localhost:9222/json/version` 有响应 |
| 未登录/需要登录 | 手动在 CDP Edge 中打开 doubao.com 完成登录（见登录引导） |
| 选择器找不到元素 | 豆包页面可能更新，先截图调试，更新选择器列表 |
| 下载失败 | 检查输出目录权限，确认文件 URL 有效 |
| 生成超时 | 增加脚本中的超时值（默认 180000ms） |
| Edge 启动后无窗口 | Edge 可能最小化到后台，检查任务栏 |
