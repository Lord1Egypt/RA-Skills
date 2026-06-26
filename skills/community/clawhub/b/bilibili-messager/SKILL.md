---
name: Bilibili Messager | B站私信助手
description: |
  Send Bilibili DMs, reply to messages, read chat history via browser automation. | 通过浏览器自动化发送 B 站私信、回复消息、读私信、看聊天记录。
metadata:
  "openclaw":
    requires:
      bins: ["browser"]
      browser_profiles: ["openclaw"]  # 必须使用 openclaw profile，且已登录 Bilibili
    runtime:
      credentialExpectations:
        - "Bilibili 已登录的浏览器会话（openclaw profile）"
      filesystemWrites:
        - "~/.openclaw/workspace/skills/bilibili-messager/"
        - "~/.openclaw/workspace/projects/bilibili-messager/"
    warning:
      - "发送操作需要用户两步验证确认"
      - "读取聊天记录会将私信内容暴露到 agent 上下文，仅读取你愿意分享的内容"
      - "使用独立 openclaw profile，不与其他账号混用"
---

# Bilibili Messager | B站私信助手

## ⚠️ 安全声明

本技能通过已登录的 Bilibili 浏览器会话读写私信。

**限制：**
- 只使用独立的 `openclaw` profile（不混用其他账号）
- 发送前必须两步验证确认目标账号和消息内容
- 读取模式仅用于你愿意暴露给 agent 的会话内容
- 不要用于读取高度敏感或非自愿的私人对话

## 前置要求 | Prerequisites

| 条件 | 说明 |
|------|------|
| **Browser profile** | 必须使用 `openclaw` profile（已通过 `browser` 工具启动并登录 Bilibili） |
| **登录状态** | Bilibili 账号已在 `openclaw` profile 中保持登录态 |
| **账号确认** | 发送操作前，技能会要求用户明确确认目标账号和消息内容 |

### 为什么需要 openclaw profile？

本技能通过在 Bilibili 私信页面执行 DOM JavaScript（`querySelector`、`innerText`、`click` 等）实现消息读取和发送。这些操作需要浏览器环境持有有效的 Bilibili 登录会话。

- `openclaw` profile 由 OpenClaw 启动和管理，独立于 Morois 的日常浏览器 profile
- 技能仅在 Bilibili 私信页（`message.bilibili.com`）域内执行 DOM 操作，无法访问其他网站
- 任何对外发送操作均需用户明确确认，不会自动发送

---

## 模式 | Mode

> 读取本 SKILL.md 后，先确认当前任务属于哪种模式，再跳转对应章节执行。

| 模式 | 说明 |
|------|------|
| **send** | 发送新私信（必须两步验证） |
| **reply** | 回复现有会话中的消息（必须两步验证） |
| **read** | 读取聊天记录（只读，不写入任何内容） |

---

## 通用原则 | General Principles

1. **Browser profile**：使用 `openclaw` profile（已登录 Bilibili）
2. **两步验证**：发送类操作（send / reply）必须两步验证，不可跳过
3. **只读优先**：读取聊天记录使用 read 模式，不执行任何写入操作
4. **发送前确认**：执行任何对外发送前，必须先向用户确认目标账号和消息内容
---

## 发送私信 | Mode: Send

### 步骤 1：打开私信页并确认登录

```
browser action=open targetUrl=https://message.bilibili.com/#/whisper
```

检查页面是否跳转到登录页。若跳转到登录页，停下来让用户完成登录。

### 步骤 2：找到目标会话

在左侧会话列表中找到目标联系人。可以通过文字搜索或滚动列表。

- 使用 `browser action=act evaluate` 配合 DOM 查询找到目标会话
- 找到后点击进入会话

### 步骤 3：两步验证（强制，必须执行）

#### 第一步（AI 内部执行，不输出给用户）

- 确认已正确进入目标会话（检查 URL 包含 `mid` 参数或页面标题显示对方名字）
- 确认消息内容已准备完毕
- 检查消息长度（不超过 500 字）

#### 第二步（输出给用户，等待明确确认）

向用户汇报以下全部内容，**确认前不得写入或发送**：

| 汇报项 | 内容 |
|--------|------|
| 目标账号 | 会话对方的名字 |
| 消息内容 | 将要发送的完整内容 |
| 字数 | 是否在 500 字以内 |

**确认标志**：用户明确回复「好」「确认」「发」「发吧」「发送」等。

### 步骤 4：写入消息

使用 `innerText` 方式写入（经验证有效）：

```javascript
() => {
  var editor = document.querySelector('.content-input, [contenteditable="true"]');
  if (!editor) return 'editor not found';
  editor.focus();
  editor.innerText = '消息内容';
  editor.dispatchEvent(new Event('input', {bubbles: true}));
  return 'typed';
}
```

### 步骤 5：点击发送按钮

```javascript
() => {
  var btns = document.querySelectorAll('button, [class*="btn"]');
  for (var btn of btns) {
    if ((btn.textContent || '').includes('发送')) {
      btn.click();
      return 'sent';
    }
  }
  return 'send button not found';
}
```

**注意**：
- ❌ `navigator.clipboard.writeText()` + `execCommand('paste')` — 对B站无效
- ❌ Enter 键发送 — 对B站无效
- ✅ 直接设置 `innerText` + 触发 `input` 事件 — 成功

### 步骤 6：验证发送结果

- 发送成功后，消息会出现在聊天窗口中
- 侧边栏会话列表的预览也会更新

---

## 回复消息 | Mode: Reply

回复与发送流程基本相同，区别在于：

1. 先用 **read 模式**确认要回复的消息内容
2. 在对应会话中打开对话
3. 后续步骤同发送流程（步骤 3 两步验证 → 步骤 4 写入 → 步骤 5 发送）

---

## 读取聊天记录 | Mode: Read

### 步骤 1：打开私信页

```
browser action=open targetUrl=https://message.bilibili.com/#/whisper
```

### 步骤 2：找到并打开目标会话

在左侧会话列表中找到目标联系人，点击进入。

### 步骤 3：提取聊天记录

**⚠️ 核心原则：判断发送方归属，100% 依赖 DOM class 名称，不靠语义内容猜测。**

#### 发送方归属规则（重要，必读）

##### B站消息 DOM 结构说明

B站私信页面上，每条消息是一个 HTML 元素，**该元素的 class 属性**包含判断归属的关键信息。

**class 名称的格式一（我发的消息）：**
```
class="_Msg_o7f0t_1 _MsgIsMe_o7f0t_9"
```
- `_Msg_o7f0t_1`：消息容器（固定前缀 `_Msg_` + 会话ID `o7f0t` + 数字 `1`）
- `_MsgIsMe_o7f0t_9`：**附加标记，表示"这条消息是当前登录用户发的"**

**class 名称的格式二（对方发的消息）：**
```
class="_Msg_o7f0t_1"
```
- 只有 `_Msg_` 开头的容器 class，没有 `_MsgIsMe_` 标记
- 表示这条消息是对方发的

**关于会话ID（上面例子里的 `o7f0t`）：**
- 会话ID是B站为每个私信会话分配的随机字符串，不同会话ID不同
- 代码中用 `[a-z0-9]+` 匹配（ID只包含小写字母和数字）

##### 判断规则（4步）

1. **找到所有顶级消息容器**：
   - 用 CSS 选择器 `[class*="_Msg_"]` 找到所有包含 `_Msg_` 的元素
   - 再用正则 `_Msg_[a-z0-9]+_\d+ ` 过滤，只保留顶级容器
     - 匹配成功举例：`_Msg_o7f0t_1`、`_Msg_abc123_42`、`_Msg_x_99`

2. **判断发送方归属**：
   - 如果该元素的 class 里**包含 `_MsgIsMe_`**，则这是一条**我发的消息**（Morois / 当前登录用户）
   - 如果该元素的 class 里**不包含 `_MsgIsMe_`**，则这是一条**对方发的消息**

3. **❌ 禁止用左右位置判断**：
   - B站的消息布局可能产生误导——例如对方发的消息有时也会渲染在右侧
   - 永远不要用"左侧/右侧"或"left/right"作为判断依据
   - 只用 `_MsgIsMe_` 有没有出现来判断


##### 具体 class 名称示例

| class 名称 | 含义 |
|-----------|------|
| `_Msg_o7f0t_1` | 消息容器，会话ID是 `o7f0t`，序号1 |
| `_Msg_o7f0t_1 _MsgIsMe_o7f0t_9` | 我发的消息（morois发的），有 `_MsgIsMe_` 标记 |
| `_Msg_abc123_42` | 消息容器，会话ID是 `abc123`，序号42，对方发的 |
| `_Msg_x_7` | 消息容器，会话ID是 `x`，序号7，对方发的 |
| `_MsgIsMe_x_15` | 我发的消息（morois发的），会话ID是 `x`，序号15 |

##### 提取脚本（完整示例）

```javascript
() => {
  const containers = Array.from(document.querySelectorAll('[class*="_Msg_"]'))
    .filter(el => el.className.match(/_Msg_[a-z0-9]+_\d+ /));

  const results = [];
  for (const el of containers) {
    const cls = el.className + '';

    // 关键判断：有 _MsgIsMe_ → 我发的；没有 → 对方发的
    const isMe = cls.includes('_MsgIsMe_');
    const sender = isMe ? '【我方/Morois】' : '【对方】';

    // 提取时间
    const timeEl = el.querySelector('[class*="_Msg__Time_"]');
    const time = timeEl ? timeEl.textContent.trim() : '';

    // 提取消息内容（可能有多个 Content class，取非重复内容）
    const contentEls = el.querySelectorAll('[class*="_Msg__Content_"]');
    const texts = [];
    for (const c of contentEls) {
      const t = (c.textContent || '').trim().replace(/\s+/g, ' ');
      // 排除时间格式的内容（如"2026年3月28日 18:00"）
      if (t && !t.match(/^\d{4}年/)) texts.push(t.slice(0, 200));
    }
    const uniqueTexts = [...new Set(texts)];
    const text = uniqueTexts.join(' | ');

    if (text) results.push({ sender, time, text });
  }
  return results;
}
```

##### 注意事项

- 保留所有消息类型：文本、视频分享、图片、卡片等，不要因为不是纯文本就丢弃
- 结合时间戳重建时间线
- DOM 结构变化时，参考常见问题 → 页面布局变了

---

## 常见问题

### 找不到编辑器

B站私信页面的编辑器可能出现在不同位置。尝试：

```javascript
() => {
  const selectors = [
    '.content-input',
    '[contenteditable="true"]',
    '[class*="editor"]',
    '[class*="input"]'
  ];
  for (const sel of selectors) {
    const el = document.querySelector(sel);
    if (el) return sel + ' found: ' + el.className;
  }
  return 'no editor found';
}
```

### 找不到发送按钮

发送按钮可能没有稳定的 class 或 ref。查找包含"发送"文字的按钮：

```javascript
() => {
  const btns = document.querySelectorAll('button, [class*="btn"], [class*="send"]');
  for (const btn of btns) {
    if ((btn.textContent || '').includes('发送')) {
      return 'found: ' + btn.className;
    }
  }
  return 'send button not found';
}
```

### 页面布局变了（DOM 结构诊断）

如果脚本返回空结果或找不到元素，按以下顺序诊断：

1. **先快照**：用 `browser action=snapshot` 获取当前页面完整 DOM
2. **找消息容器**：在快照中搜索 `_Msg_` 或 `message`
3. **找编辑器**：搜索 `contenteditable`、`input`、`editor`
4. **找发送按钮**：搜索 `发送` 文字或 `button`
5. **根据诊断结果**：用实际找到的 class/name 重写选择器

诊断脚本：
```javascript
() => {
  return {
    msgs: Array.from(document.querySelectorAll('[class*="Msg"]')).slice(0,3).map(el=>el.className),
    editor: document.querySelector('[contenteditable="true"]') ? 'found' : 'not found',
    btns: Array.from(document.querySelectorAll('button')).map(b=>b.textContent.trim()).filter(t=>t)
  };
}
```

---

## 安全与隐私 | Security & Privacy

### 浏览器会话凭据声明

本技能依赖已登录的 Bilibili 浏览器会话作为账户凭据。使用前请确认：

1. **确认登录账户**：发送操作前，先确认当前登录的是正确的 Bilibili 账户
2. **使用专用 profile**：必须使用独立的 `openclaw` profile，不与日常浏览器混用
3. **用完后清理**：
   - 关闭 `openclaw` profile 的浏览器标签页即可
   - 不再使用时，可清除该 profile 的 Bilibili 登录态

### 数据披露

- 读取聊天记录会将私信内容暴露到 agent 上下文，仅读取你愿意分享的内容
- 浏览器自动化操作仅在 Bilibili 域（`message.bilibili.com`）内执行，不访问其他网站
- 不要用于读取高度敏感或非自愿的私人对话

---

## 限制与注意事项

- 消息长度限制 500 字，超长需分段发送
- 避免高频发送
- 读取记录时优先保证归属和类型正确，再追求历史深度
- 发送前必须用户明确确认目标账号和消息内容

