---
name: deepseek-web-query
description: 使用 DeepSeek 网页版进行互联网查询，分担大模型请求和搜索负担。当用户需要查询最新信息、一般性知识、代码问题、文本分析等，或明确说"用 DeepSeek 查一下"、"联网搜索"、"查下最新"等时触发此技能。特别地，如果提问以"ds:"或"ds："开头，优先使用此技能。通过 Chrome DevTools MCP 控制浏览器与 DeepSeek 交互，自动检测登录状态并提示用户，保持浏览器会话复用，使用 evaluate_script 提取 Markdown 内容直接返回。
---

# DeepSeek Web Query

## Overview

本技能用于将用户的查询请求转发到 DeepSeek 网页版，利用 DeepSeek 的联网搜索能力获取最新信息，同时减轻主模型的负担。

**技术栈**: 使用 Chrome DevTools MCP (通过 mcporter) 控制浏览器，替代原有的 Playwright 方案。

**故障恢复**: 如果 Chrome DevTools MCP 服务不可用，会自动尝试使用 chrome-devtools-mcp-manager 技能启动浏览器和 MCP 服务。

## When to Use

当用户有以下需求时触发此技能：

- **优先触发**：提问以 "ds:" 或 "ds：" 开头（例如："ds:什么是量子计算？"）
- "用 Deep Seek 查一下..."
- "联网搜索..."
- "查下最新的..."
- "搜索一下..."
- 需要查询最新的互联网信息（新闻、技术文档、产品信息等）
- 一般性知识查询，不需要复杂的多步推理
- 代码相关问题，需要最新的 API 文档或最佳实践
- 文本分析、翻译、总结等任务

## Workflow

### 步骤 0: 预处理查询（处理 ds: 前缀）

如果用户查询以 "ds:" 或 "ds：" 开头：
1. 移除前缀（"ds:" 或 "ds："）
2. 将剩余内容作为实际查询问题
3. 继续执行后续步骤

例如：
- 输入："ds:什么是量子计算？" → 实际查询："什么是量子计算？"
- 输入："ds：最新的Python版本是什么？" → 实际查询："最新的Python版本是什么？"

### 步骤 1: 检查并启动 Chrome DevTools MCP

在执行 MCP 操作前，先检查服务状态：

```bash
# 检查 MCP 服务状态
mcporter list
```

**如果服务不可用（连接错误或权限错误），执行自动恢复流程：**

#### 自动恢复流程

1. **检查内置 Chrome 浏览器状态**
   ```javascript
   browser({
     action: "status",
     profile: "openclaw"
   })
   ```

2. **如果浏览器未运行，启动它**
   ```javascript
   browser({
     action: "open",
     profile: "openclaw",
     url: "about:blank"
   })
   ```
   等待 2-3 秒让浏览器完全启动。

3. **验证 CDP 端点可用**
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:18800/json/version" -Method GET
   ```

4. **重新配置 mcporter 的 MCP 服务器**
   ```bash
   # 移除旧的配置（如果存在）
   mcporter server remove chrome-devtools
   
   # 添加新的 MCP 服务器配置
   mcporter server add chrome-devtools \
     --command "npx" \
     --args "chrome-devtools-mcp@latest,--browserUrl,http://127.0.0.1:18800,--no-usage-statistics"
   ```

5. **验证 MCP 服务已恢复**
   ```bash
   mcporter list
   mcporter call chrome-devtools.list_pages
   ```

#### 完整自动恢复脚本示例

```javascript
// 步骤 1: 检查浏览器状态
const status = await browser({ action: "status", profile: "openclaw" });

// 步骤 2: 如果未运行，启动浏览器
if (!status.cdpReady) {
  await browser({ action: "open", profile: "openclaw", url: "about:blank" });
  await new Promise(r => setTimeout(r, 3000)); // 等待启动
}

// 步骤 3: 验证 CDP 端点
// (使用 exec 执行 PowerShell 命令)

// 步骤 4: 重新配置 mcporter
// (使用 exec 执行 mcporter 命令)

// 步骤 5: 验证 MCP 服务
// (使用 exec 执行 mcporter list)
```

### 步骤 2: 打开浏览器并检测登录状态

1. 使用 Chrome DevTools MCP 打开 DeepSeek：

```bash
# 创建新页面并导航到 DeepSeek
mcporter call chrome-devtools.new_page url: "https://chat.deepseek.com/"

# 或者导航到现有页面
mcporter call chrome-devtools.navigate_page type: "url" url: "https://chat.deepseek.com/"
```

2. 等待页面加载完成后，获取页面快照：

```bash
mcporter call chrome-devtools.take_snapshot
```

3. 根据快照内容检测登录状态：
   - **登录页面特征**：包含"手机号"、"验证码"、"登录"、"微信扫码登录"等文本
   - **已登录页面特征**：包含"发送消息"、"深度思考"、"新对话"等文本

**如果 MCP 调用失败，再次执行自动恢复流程，然后重试。**

### 步骤 3: 处理登录（如需要）

如果检测到未登录：

1. 截图展示登录页面给用户：

```bash
mcporter call chrome-devtools.take_screenshot
```

2. 提示用户："请先登录 DeepSeek（手机号+验证码或微信扫码）"
3. 等待用户完成登录
4. 用户登录完成后，重新检测状态（重复步骤 2）

### 步骤 4: 执行查询

1. **获取页面快照**，找到输入框和深度思考按钮的 uid：

```bash
mcporter call chrome-devtools.take_snapshot
```

2. **启用深度思考模式**（如果未启用）：
   - 在快照中查找包含"深度思考"文本的按钮
   - 如果按钮状态显示未启用，点击启用：

```bash
mcporter call chrome-devtools.click uid: "<深度思考按钮的uid>"
```

3. **点击输入框获取焦点**：

```bash
mcporter call chrome-devtools.click uid: "<输入框的uid>"
```

4. **输入用户问题**：

```bash
mcporter call chrome-devtools.type_text text: "用户查询问题"
```

5. **按 Enter 发送**：

```bash
mcporter call chrome-devtools.press_key key: "Enter"
```

6. **等待回答完成**：
   - 等待 "已思考" 或 "已深度思考" 文本出现
   - 或者等待停止按钮消失

```bash
mcporter call chrome-devtools.wait_for text: ["已思考", "已深度思考"] timeout: 60000
```

### 步骤 5: 提取结果

**使用 evaluate_script 提取 Markdown 内容**：

```bash
mcporter call chrome-devtools.evaluate_script function: '
() => {
    // 方法1: 尝试点击 copy 按钮后从页面提取
    const copyButtons = document.querySelectorAll("button[title*=\"复制\"], button[class*=\"copy\"], [class*=\"copy-button\"]");
    if (copyButtons.length > 0) {
        copyButtons[copyButtons.length - 1].click();
    }
    
    // 等待一下复制完成
    return new Promise(resolve => {
        setTimeout(() => {
            // 提取 Markdown 内容
            const markdownElements = document.querySelectorAll(".ds-markdown, [class*=\"markdown\"], [class*=\"message-content\"]");
            let result = "";
            markdownElements.forEach(el => {
                if (el.innerText && el.innerText.trim().length > 0) {
                    result += el.innerText + "\n\n";
                }
            });
            resolve(result.trim());
        }, 500);
    });
}
'
```

**备选方案**：如果上述方法失败，直接提取页面文本：

```bash
mcporter call chrome-devtools.evaluate_script function: '
() => {
    const messages = document.querySelectorAll(".ds-markdown, [class*=\"message-content\"], [class*=\"chat-message\"]");
    const lastMessage = messages[messages.length - 1];
    return lastMessage ? lastMessage.innerText : document.body.innerText;
}
'
```

### 步骤 6: 结果返回

**重要：直接返回提取的原始内容，不要进行 LLM 二次总结或加工。**

- 直接将提取的 Markdown 文本返回给用户
- **不添加额外的解释、总结或格式化**
- **不进行任何整理或编辑**
- 保持 DeepSeek 原始输出的完整性
- 避免不必要的 token 消耗

### 步骤 7: 保持浏览器

**重要**: 不要关闭浏览器页面！保持浏览器会话供后续查询复用。

如需关闭，使用：

```bash
mcporter call chrome-devtools.close_page pageId: <page_id>
```

## 故障恢复机制详解

### 常见错误及处理

#### 错误 1: "connect EPERM" 或管道连接错误

**症状**: 
```
connect EPERM \\.\pipe\mcporter-daemon-xxx
```

**处理**: 执行完整自动恢复流程（步骤 1）。

#### 错误 2: "CDP not ready"

**症状**: 浏览器状态显示 `cdpReady: false`

**处理**: 
1. 停止现有浏览器：`browser({ action: "stop", profile: "openclaw" })`
2. 重新启动浏览器：`browser({ action: "open", profile: "openclaw", url: "about:blank" })`
3. 等待 3 秒后重试

#### 错误 3: MCP 服务器返回错误

**症状**: `mcporter call` 返回错误但连接正常

**处理**:
1. 检查页面是否存在：`mcporter call chrome-devtools.list_pages`
2. 如需要，重新导航到 DeepSeek
3. 重试操作

### 自动恢复的最佳实践

1. **最多尝试 2 次恢复**：如果连续 2 次恢复失败，向用户报告问题
2. **记录恢复操作**：在日志中记录每次恢复尝试
3. **保持用户知情**：如果恢复需要较长时间，告知用户正在处理
4. **优雅降级**：如果 MCP 完全不可用，建议使用替代方案（如 Tavily 搜索）

## Chrome DevTools MCP 工具参考

### 核心工具

| 工具 | 用途 |
|------|------|
| `new_page` | 创建新标签页并加载 URL |
| `navigate_page` | 导航到 URL 或前进/后退/刷新 |
| `take_snapshot` | 获取页面 a11y 树快照（用于查找元素 uid） |
| `take_screenshot` | 截图 |
| `click` | 点击元素 |
| `fill` | 填写输入框 |
| `type_text` | 输入文本 |
| `press_key` | 按键 |
| `evaluate_script` | 执行 JavaScript 并返回结果 |
| `wait_for` | 等待特定文本出现 |
| `list_pages` | 列出所有打开的页面 |
| `select_page` | 选择特定页面作为上下文 |

### DeepSeek 页面元素选择策略

**输入框**：
- 查找 placeholder 包含"发送消息"的 textarea
- 或查找 contenteditable="true" 的元素

**深度思考按钮**：
- 查找文本包含"深度思考"的按钮
- 检查按钮状态（aria-pressed 或 class）

**Copy 按钮**：
- 查找 title 包含"复制"或 class 包含"copy"的按钮
- 通常位于每条消息的右上角

**消息内容**：
- class 包含 "ds-markdown" 或 "message-content"

## Login Detection

通过页面快照检测登录状态：

**登录页面特征：**
- 包含文本："手机号"、"验证码"、"登录"、"微信扫码登录"
- 有手机号输入框和验证码输入框

**已登录页面特征：**
- 包含文本："发送消息"、"深度思考"、"新对话"
- 有消息输入框

## Result Extraction Methods

### 方法 1: Evaluate Script 提取（推荐）

优点：
- 获取 Markdown 格式文本，保留格式
- Token 消耗极低（~100 tokens）
- 速度快
- 用户可直接复制编辑

实现：
1. 使用 `evaluate_script` 执行 JavaScript
2. 查询 `.ds-markdown` 或 `[class*="message-content"]` 元素
3. 提取 `innerText` 返回

### 方法 2: 截图返回

优点：
- 原汁原味
- 包含图表、代码高亮等视觉效果

缺点：
- 无法复制文本
- 文件较大

### 方法 3: LLM 整理（传统方式）

优点：
- 可二次加工、个性化
- 可结合上下文

缺点：
- Token 消耗高（~2k+ tokens）
- 速度慢

## 完整查询流程示例（含故障恢复）

### ds: 前缀查询（推荐方式）

用户: "ds:什么是量子计算？"

1. 识别并移除 "ds:" 前缀，实际查询："什么是量子计算？"
2. **检查 MCP 服务状态**，如不可用执行自动恢复流程
3. 使用 Chrome DevTools MCP 导航到 chat.deepseek.com
4. 获取快照检测登录状态
5. 如果未登录，截图提示用户登录
6. 如果已登录：
   - 查找并点击深度思考按钮（如未启用）
   - 点击输入框获取焦点
   - 输入问题
   - 按 Enter 发送
7. 等待回答完成
8. 使用 evaluate_script 提取 Markdown 内容
9. 直接返回提取的原始文本
10. 保持页面打开

### 快速复用

用户: "ds：再详细说一下 asyncio 的事件循环"

1. 识别并移除 "ds：" 前缀
2. **检查 MCP 服务状态**，如不可用执行自动恢复流程
3. 复用已打开的页面（使用 `list_pages` 和 `select_page`）
4. 直接输入新问题并获取回答

## 命令速查

### MCP 服务管理
```bash
# 检查 MCP 服务状态
mcporter list

# 添加 MCP 服务器配置
mcporter server add chrome-devtools \
  --command "npx" \
  --args "chrome-devtools-mcp@latest,--browserUrl,http://127.0.0.1:18800,--no-usage-statistics"

# 移除 MCP 服务器配置
mcporter server remove chrome-devtools
```

### 浏览器管理
```javascript
// 检查浏览器状态
browser({ action: "status", profile: "openclaw" })

// 启动浏览器
browser({ action: "open", profile: "openclaw", url: "about:blank" })

// 停止浏览器
browser({ action: "stop", profile: "openclaw" })
```

### CDP 验证
```powershell
# 测试 CDP 端点
Invoke-WebRequest -Uri "http://localhost:18800/json/version" -Method GET
```

### DeepSeek 查询
```bash
# 导航到 DeepSeek
mcporter call chrome-devtools.navigate_page type: "url" url: "https://chat.deepseek.com/"

# 获取页面快照
mcporter call chrome-devtools.take_snapshot

# 点击元素
mcporter call chrome-devtools.click uid: "<element_uid>"

# 输入文本
mcporter call chrome-devtools.type_text text: "查询内容"

# 按键
mcporter call chrome-devtools.press_key key: "Enter"

# 等待文本出现
mcporter call chrome-devtools.wait_for text: '["已思考", "已深度思考"]' timeout: 60000

# 执行 JavaScript 提取内容
mcporter call chrome-devtools.evaluate_script function: '
() => {
    const elements = document.querySelectorAll(".ds-markdown");
    let result = "";
    elements.forEach(el => {
        result += el.innerText + "\n\n";
    });
    return result.trim();
}
'

# 截图
mcporter call chrome-devtools.take_screenshot

# 列出所有页面
mcporter call chrome-devtools.list_pages

# 选择页面
mcporter call chrome-devtools.select_page pageId: 0
```

## Notes

- **ds: 前缀**：使用 "ds:" 或 "ds：" 前缀可以确保优先使用此技能进行查询
- **自动恢复**：MCP 服务故障时会自动尝试恢复，无需手动干预
- **首次使用需要登录 DeepSeek 账号**
- **浏览器页面会保持打开状态**，供后续查询使用
- **如需关闭页面**，使用 `close_page` 工具
- **查询结果取决于 DeepSeek 网页版的响应速度**，通常需要 10-30 秒
- **默认使用 evaluate_script 提取方案**，兼顾速度和质量
- **Chrome DevTools MCP 需要浏览器通过 `--remote-debugging-port` 启动**（内置 `openclaw` 配置文件已自动处理）
- **故障恢复最多尝试 2 次**，避免无限循环
- **如果 MCP 完全不可用**，建议向用户说明并提供替代方案（如 Tavily 搜索）

## 依赖技能

本技能依赖于以下技能的正常工作：
- **chrome-devtools-mcp-manager**: 用于管理 Chrome 浏览器和 MCP 服务的生命周期
- **browser tool**: OpenClaw 内置的浏览器控制工具
- **mcporter**: MCP 服务器管理 CLI 工具

## 故障排除

### MCP 服务持续不可用

如果自动恢复流程无法解决问题：

1. **检查 Node.js 环境**
   ```bash
   node --version
   npx --version
   ```

2. **检查 chrome-devtools-mcp 包**
   ```bash
   npm list -g chrome-devtools-mcp
   # 或
   npx chrome-devtools-mcp@latest --help
   ```

3. **检查端口占用**
   ```powershell
   Get-NetTCPConnection -LocalPort 18800
   ```

4. **手动重启**
   ```javascript
   browser({ action: "stop", profile: "openclaw" })
   // 等待 5 秒
   browser({ action: "open", profile: "openclaw", url: "about:blank" })
   ```

5. **联系用户**
   如果以上步骤都无法解决问题，向用户报告：
   - 当前状态
   - 已尝试的解决方案
   - 建议的替代方案（如 Tavily 搜索）
