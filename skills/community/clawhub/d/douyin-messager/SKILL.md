---
name: Douyin Messager | 抖音私信助手
description: "Douyin DMs and video/note comment assistant. 抖音私信与视频/图文评论助手；可读私信、分析评论区，评论/回复等写入前必须确认。"
metadata:
  "openclaw":
    requires:
      bins: ["browser"]
      browser_profiles: ["openclaw"]
    runtime:
      credentialExpectations:
        - "抖音已登录的浏览器会话（openclaw profile）"
      filesystemWrites:
        - "~/.openclaw/workspace/skills/douyin-messager/"
        - "~/.openclaw/workspace/projects/douyin-messager/"
    warning:
      - "发送/评论/回复/点赞等写入操作需要用户确认"
      - "读取聊天记录会将私信内容暴露到 agent 上下文"
      - "使用独立 openclaw profile，不与其他账号混用"
---

# Douyin Messager | 抖音私信助手

通过浏览器自动化发送抖音私信、获取聊天记录；也支持打开抖音视频/图文链接、读取评论区并做简要分析，在用户明确确认后执行评论/回复等写入操作。

## 前置要求 | Prerequisites

| 条件 | 说明 |
|------|------|
| **Browser profile** | 必须使用 `openclaw` profile |
| **登录状态** | 抖音账号已在 `openclaw` profile 中保持登录态 |

---

## ⚠️ 执行前必须确认

1. **用户已登录抖音账号**（可目测判断）
2. **xdg-open 弹窗**：只在 Linux 下存在
   - Linux：询问用户弹窗是否关闭
   - Windows/macOS：跳过

---

## ⚠️ 安全声明 | Security Notice

本技能通过已登录的抖音浏览器会话读写私信和评论。

### 浏览器会话凭据声明

本技能依赖已登录的抖音浏览器会话作为账户凭据。使用前请确认：

1. **确认登录账户**：发送操作前，先确认当前登录的是正确的抖音账户
2. **使用专用 profile**：必须使用独立的 `openclaw` profile，不与日常浏览器混用
3. **用完后清理**：关闭 `openclaw` profile 的浏览器标签页即可；不再使用时，可清除该 profile 的抖音登录态

### 数据披露

- 读取聊天记录和评论区会将内容暴露到 agent 上下文，仅读取你愿意分享的内容
- 不要用于读取高度敏感或非自愿的私人对话

### 操作限制

- **发送私信**：必须先向用户确认目标账号和消息内容，获得明确同意后才执行
- **评论/回复/点赞/分享**：属于外部互动写入操作，必须先获得用户明确确认

---

## 当前能力边界（阶段性总结）

本技能当前已验证可完成四类操作：

1. **查看私信会话列表**：进入私信悬浮面板后，读取可见的私聊/群聊列表，区分会话名称、最新消息预览、时间、未读数和置顶状态。
2. **进入具体聊天窗口**：从会话列表点击指定私聊或群聊，进入聊天详情页，读取当前已加载的聊天记录。
3. **发送文本消息**：在聊天详情底部的 Draft.js 输入框中输入文本，并通过发送按钮完成发送。
4. **视频/图文评论区处理**：可搜索或打开指定视频/图文链接，读取评论区，输出情绪简报；评论、回复、点赞等外部互动写入必须先获得用户明确确认。

需要注意：网页版对视频、图集、点赞、撤回、暂不支持消息等卡片类内容的 DOM 暴露不完整，读取时应保守标注，不应强行推断完整内容或发送者。

---

## 核心思路

> 抖音私信是一个**悬浮在页面右侧的动态面板**，包含"会话列表"和"聊天详情"两个视图。

**会话列表布局**（类 QQ/微信）：左侧头像，中间分上下两行（上行：用户名/群名；下行：最新消息预览，群聊格式为「发消息的人：消息内容」），右侧时间戳。

**聊天详情布局**：进入某个会话后，右侧显示聊天记录。普通文本消息通常可提取时间、消息内容，并可根据气泡方向、操作项（如是否有「撤回」）辅助判断是否为本人消息；群聊中他人文本消息有时可从消息文本或引用结构中识别发送者。卡片类消息需谨慎处理。

**方法论**：不依赖固定 class name，而是通过元素的**几何特征 + 内容特征**动态查找。具体 class name 仅作参考示例。

---

## 获取私信列表流程

获取私信的第一步不是进入某个聊天，而是**正确进入私信会话列表**。

### 步骤 1：打开私信会话列表

1. 打开抖音主页或个人主页。
2. 在顶部导航栏右侧定位「私信」入口（可能显示未读数，如「私信11」）。
3. 点击后等待右侧悬浮面板出现。
4. 确认当前处于会话列表视图，而不是某个聊天详情页。

### 步骤 2：识别每一行会话

会话列表中每一行对应一个私聊或群聊。布局通常为：左侧头像；中间上行为会话名称（用户名/群名，可能带「置顶」标记）；中间下行为最新消息预览；右侧为时间戳或未读标记。

⚠️ 会话列表本身是可滚动容器，不要只按当前可见区域判断数量。实测中滚动容器宽约 328px、高约 593px，`scrollHeight > clientHeight`，可通过 `scrollTop` 滚到底部；出现「暂时没有更多了」才表示到底。

解析时应优先按**行容器**处理，而不是直接读取父元素的合并文本。读取每行时分别提取：

| 字段 | 识别方法 |
|------|----------|
| 会话名称 | 行内上方文本，通常是用户名或群名；若有「置顶」应作为标记处理，不并入名称 |
| 最新消息 | 行内下方文本；群聊常见格式为「发送者：消息内容」 |
| 最新发送者 | 若最新消息包含「：」，冒号前通常是群聊中最新消息发送者 |
| 时间 | 行右侧或下行末尾的时间文本，如「昨天」「04-25」「01:42」 |
| 未读数 | 行右侧 badge 数字；顶部「私信（N）」通常表示总未读数 |
| 置顶 | 名称行附近出现「置顶」标记时记录为 pinned=true |

### 步骤 3：区分私聊与群聊

- 私聊：上行通常是对方昵称；下行多为消息内容本身。
- 群聊：上行是群名；下行常为「发送者：消息内容」。
- 不要把上行群名和下行发送者合并为一个名称。

**示例参考**：

| 上行（会话名称） | 下行（最新消息） | 解析结果 |
|------------------|------------------|----------|
| `示例群A` | `成员甲：分享[视频] · 昨天` | 群名/会话名=`示例群A`，最新发送者=`成员甲` |
| `项目交流群` | `成员乙：分享[图集] · 04-25` | 群名=`项目交流群`，最新发送者=`成员乙` |
| `联系人A` + `置顶` | `收到，谢谢 · 01:42` | 私聊=`联系人A`，pinned=true |

### 示例：提取可见会话行文本

以下代码用于辅助观察当前可见列表，不应把 class name 当成稳定依赖：

```javascript
browser action=act request={"kind": "evaluate", "fn": "() => { const rows = []; const all = Array.from(document.querySelectorAll('*')); for (const el of all) { const r = el.getBoundingClientRect(); const text = (el.textContent || '').trim(); if (r.width >= 250 && r.width <= 360 && r.height >= 50 && r.height <= 90 && r.left > window.innerWidth * 0.55 && text && !text.includes('私信（')) { rows.push({top: Math.round(r.top), text}); } } return rows.sort((a,b) => a.top - b.top); }"}
```

---

## 完整发送流程

### 步骤 1：打开抖音主页

```javascript
browser action=open profile=openclaw targetUrl=https://www.douyin.com/
browser action=act request={"kind": "wait", "timeMs": 3000}
```

### 步骤 2：打开私信悬浮面板

**找按钮**：在页面顶部导航栏中，找到文字为"私信"（可能带未读数如"私信15"）且位于页面最右侧的元素，点击它。

```javascript
browser action=act request={"kind": "evaluate", "fn": "() => { const all = Array.from(document.querySelectorAll('*')); for(const el of all) { const t = (el.textContent||'').trim(); const r = el.getBoundingClientRect(); if((t === '私信' || t.startsWith('私信')) && r.width > 0 && r.height > 0 && r.width < 100 && r.left > window.innerWidth - 200) { el.click(); return 'clicked: ' + t; } } return 'not found'; }"}
browser action=act request={"kind": "wait", "timeMs": 2000}
```

**找面板**：点击后，页面右侧应出现一个约 500-600px 宽、600-700px 高的悬浮面板。

```javascript
browser action=act request={"kind": "evaluate", "fn": "() => { const all = document.querySelectorAll('[class]'); for(const el of all) { const r = el.getBoundingClientRect(); if(r.width >= 450 && r.width <= 650 && r.height >= 500 && r.height <= 750 && r.left > 0 && r.top > 0 && r.left < 1500) { const text = (el.textContent||'').trim(); if(text.includes('私信')) return 'found panel: ' + r.width + 'x' + r.height + ' at ' + Math.round(r.left); } } return 'panel not found'; }"}
```

> **示例参考**：实测中面板容器 class 为 `vgonMAXk`，宽 581px、高 649px，固定在 x:1235 位置。但这是动态的，应以几何定位为主。

### 步骤 3：进入具体聊天

**找目标用户**：在面板的会话列表中，找到目标用户名的元素并点击。

```javascript
browser action=act request={"kind": "evaluate", "fn": "() => { const all = Array.from(document.querySelectorAll('*')); for(const el of all) { const t = (el.textContent||'').trim(); const r = el.getBoundingClientRect(); if(t.includes('<目标用户名>') && r.width > 0 && r.height > 0 && r.left > 0) { el.click(); return 'clicked: ' + t; } } return 'not found'; }"}
browser action=act request={"kind": "wait", "timeMs": 2000}
```

**成功标志**：面板从会话列表切换为聊天详情，底部出现输入区域。

> **示例参考**：会话列表区域 class 为 `zEpd_aAP`（左侧，500px宽）；聊天详情区域 class 为 `w5duGc5Q`（右侧）。

### 步骤 4：两步验证（强制，必须执行）

#### 第一步（AI 内部执行，不输出给用户）

- 确认已正确进入目标会话（检查页面显示对方名字）
- 确认消息内容已准备完毕
- 检查消息长度

#### 第二步（输出给用户，等待明确确认）

向用户汇报以下全部内容，**确认前不得写入或发送**：

| 汇报项 | 内容 |
|--------|------|
| 目标账号 | 会话对方的名字 |
| 消息内容 | 将要发送的完整内容 |
| 字数 | 是否超长 |

**确认标志**：用户明确回复「好」「确认」「发」「发吧」「发送」等。

### 步骤 5：写入消息

**找输入框**：聊天详情底部有一个 Draft.js 富文本编辑器（`contenteditable="true"`，class 包含 `DraftEditor-content`）。

```javascript
browser action=act request={"kind": "evaluate", "fn": "() => { const all = document.querySelectorAll('[contenteditable=\"true\"]'); for(const el of all) { const r = el.getBoundingClientRect(); if(r.width > 200 && r.width < 500 && r.height > 10 && r.height < 100 && r.left > 1000) return 'found input at ' + Math.round(r.left) + ',' + Math.round(r.top); } return 'input not found'; }"}
```

**发送消息**：先用 `type` 方式写入 Draft.js 编辑器，再点击发送按钮。

```javascript
// 1. 写入文本
browser action=act request={"kind": "type", "selector": "[contenteditable=\"true\"]", "text": "你好，测试消息"}
browser action=act request={"kind": "wait", "timeMs": 500}

// 2. 点击发送按钮（优先用几何位置查找，也可用实测 class 作为参考）
browser action=act request={"kind": "evaluate", "fn": "() => { const btn = Array.from(document.querySelectorAll('*')).find(el => { const r = el.getBoundingClientRect(); const cls = String(el.className || ''); return r.width >= 20 && r.width <= 50 && r.height >= 20 && r.height <= 50 && r.left > window.innerWidth * 0.7 && r.top > window.innerHeight * 0.55 && (cls.includes('send') || cls.includes('PygT7Ced')); }); if(!btn) return 'send button not found'; const r = btn.getBoundingClientRect(); btn.click(); return 'clicked send at ' + Math.round(r.left + r.width/2) + ',' + Math.round(r.top + r.height/2); }"}
browser action=act request={"kind": "wait", "timeMs": 2000}
```

> ⚠️ **必须用 `type` 写入 Draft.js 编辑器**。直接操作 DOM 文本（`textContent`、`execCommand`、`clipboard`）无法触发 Draft.js 内部状态，发送按钮会保持禁用。

> **示例参考**：实测中输入框 class 为 `notranslate public-DraftEditor-content`（`contenteditable="true"`），宽约 329px，位置 x:1346, y:651。

### 步骤 5：确认发送成功

```javascript
browser action=act request={"kind": "evaluate", "fn": "() => { const input = document.querySelector('[contenteditable=\"true\"]'); if(!input) return 'input not found'; return input.textContent.length === 0 ? 'sent ✓' : 'not sent: ' + input.textContent; }"}
```

**发送成功后**：输入框被自动清空。

---

## 定位方法总结

| 目标 | 定位策略 | 实测示例（参考）|
|------|----------|----------------|
| 「私信」按钮 | 文字="私信"或"私信数字"，位于页面最右侧（`r.left > innerWidth - 200`）| 文字="私信15"，viewport x:1708, y:28 |
| 私信面板 | 宽 450-650px、高 500-750px、固定在页面右侧，内容含"私信" | class=`vgonMAXk`，581×649px，x:1235 |
| 会话列表 | 面板左侧区域 | class=`zEpd_aAP`（宽~81px） |
| 聊天详情 | 面板右侧区域 | class=`w5duGc5Q`（宽~500px） |
| 输入框 | `contenteditable="true"`，宽 200-500px，位于页面右侧 | class=`notranslate public-DraftEditor-content`，329×22px |
| 发送按钮 | 输入框右侧；写入文本后点击 | class 示例：`PygT7Ced e2e-send-msg-btn` |

> **注意**：以上尺寸和位置基于典型 1920px 宽屏幕实测。class name 会随抖音版本变化，**几何特征定位是更稳定的方法**。

---

## 读取具体聊天记录

进入某个私聊或群聊后，可以读取聊天详情页中当前已加载的消息块。读取时建议按**消息块容器**处理，而不是直接读取整个聊天面板的合并文本。

### 可识别字段

| 字段 | 说明 |
|------|------|
| 时间 | 消息块上方或附近的时间文本，如「刚刚」「2026-04-04 19:07」 |
| 消息内容 | 普通文本消息可从气泡文本中提取 |
| 是否本人消息 | 可结合气泡位置、是否出现「撤回」操作等特征辅助判断 |
| 群聊发送者 | 普通文本或引用消息中可能出现发送者名称；若 DOM 未明确暴露，应标注为未知/推断 |
| 卡片类内容 | 视频、图集、点赞、撤回、不支持类型等可能只显示占位文本，不应过度解析 |

### 示例：读取当前已加载消息块

```javascript
browser action=act request={"kind": "evaluate", "fn": "() => { const area = document.querySelector('.IRB0Sra6') || document.querySelector('.z1iI1SFY'); if(!area) return 'message area not found'; const blocks = Array.from(area.querySelectorAll('.mM66nPpS')); return blocks.map(block => { const time = block.querySelector('.mA74174G')?.textContent?.trim() || ''; const text = (block.querySelector('.G3hOMUUp') || block.querySelector('.J3X6BOUb') || block).textContent.trim(); const mine = block.textContent.includes('撤回'); return { time, mine, text }; }); }"}
```

> 上述 class name 是实测示例；正式逻辑应优先用消息区域的几何位置和消息块尺寸筛选，再结合文本特征解析。

---

## 获取对方回复

### 滚动到最新消息

```javascript
browser action=act request={"kind": "evaluate", "fn": "() => { const all = Array.from(document.querySelectorAll('*')); for(const el of all) { const r = el.getBoundingClientRect(); if(r.width >= 400 && r.width <= 600 && r.height >= 300 && r.height <= 800 && r.left > 800) { el.scrollTop = el.scrollHeight; return 'scrolled'; } } return 'not found'; }"}
browser action=act request={"kind": "wait", "timeMs": 1000}
```

### 截图确认

```
browser action=screenshot
```

---

## 视频搜索与评论区操作（阶段性验证）

当前已验证可完成以下只读/可定位操作：

1. **按关键词搜索视频**：可直接打开 `https://www.douyin.com/search/<关键词>?type=video`，从搜索结果中提取 `/video/<id>` 链接、标题、作者、时间和互动数字。
2. **打开指定视频/图文**：可直接导航到 `https://www.douyin.com/video/<id>` 或用户给出的分享链接。图文/笔记类内容可能会规范化跳转为 `/note/<id>`，个人页弹窗链接中的 `modal_id=<id>` 也可作为目标内容 ID 使用。
3. **读取视频信息**：可从页面文本中读取标题、作者、发布时间、点赞/评论/收藏/分享等可见数字（具体字段需按页面布局解析）。
4. **读取评论区**：视频页评论区在页面下方，需滚动到「全部评论」区域；可读取可见评论的昵称、内容、时间/地区、点赞数、分享/回复入口，并可继续向下滚动加载更多评论。
5. **定位发评论输入框**：点击「留下你的精彩评论吧」后，会出现 Draft.js 输入框：`contenteditable="true"` 且 class 包含 `public-DraftEditor-content`。
6. **定位回复输入框**：点击某条评论的「回复」后，会在该评论下方出现 Draft.js 输入框，placeholder 形如「回复@用户名」。
7. **定位发送按钮**：输入文字后，评论框右侧会出现图标按钮区，最右侧圆形上箭头按钮为发送/发布入口。
8. **定位评论点赞入口**：每条评论的操作区包含点赞数、分享、回复；点赞图标/数字区域可通过评论块几何位置定位。
9. **评论区情绪简报**：基于已加载评论文本，按正向/中性/负向/争议或信息不足分类，输出样本量、主要情绪、典型主题和置信度；样本少时必须注明限制。

⚠️ 发评论、回复评论、点赞、分享等都属于外部互动写入操作，必须先获得用户明确确认；测试时可以定位输入框和按钮，但不要擅自提交。

### 搜索并提取视频链接示例

```javascript
browser action=navigate profile=openclaw targetUrl="https://www.douyin.com/search/OpenClaw?type=video"
browser action=act request={"kind":"wait","timeMs":3000}
browser action=act request={"kind":"evaluate","fn":"() => Array.from(document.querySelectorAll('a[href*=\"/video/\"]')).map(a => ({ href: a.href, text: (a.innerText || a.textContent || '').trim() })).slice(0, 20)"}
```

### 打开视频并滚动到评论区

```javascript
browser action=navigate profile=openclaw targetUrl="https://www.douyin.com/video/<video_id>"
browser action=act request={"kind":"wait","timeMs":5000}
browser action=act request={"kind":"evaluate","fn":"() => { const el = Array.from(document.querySelectorAll('*')).find(el => (el.innerText || el.textContent || '').includes('全部评论') && el.getBoundingClientRect().y > 100); if (el) { el.scrollIntoView({block:'start'}); return 'scrolled to comments'; } return 'comments not found'; }"}
```

### 从个人页弹窗链接打开目标内容

用户可能发送形如 `https://www.douyin.com/user/self?...&modal_id=<id>&showTab=like` 的链接。此类链接可直接打开；若页面进入个人页弹窗，也可提取 `modal_id` 后直接尝试：

```javascript
browser action=navigate profile=openclaw targetUrl="https://www.douyin.com/video/<modal_id>"
browser action=act request={"kind":"wait","timeMs":5000}
// 页面可能自动跳转为 /note/<modal_id>，属于正常情况。
```

### 读取可见评论示例

```javascript
browser action=act request={"kind":"evaluate","fn":"() => Array.from(document.querySelectorAll('*')).map(el => { const r = el.getBoundingClientRect(); const text = (el.innerText || el.textContent || '').trim(); return { r, text, cls: String(el.className || '') }; }).filter(o => o.r.width > 300 && o.r.height > 60 && o.text.includes('回复') && o.text.includes('·')).slice(0, 20).map(o => o.text)"}
```

图文/笔记页的评论区可能在右侧栏，通过「评论(N)」标签切换；即使初始显示 `评论(0)`，点击后也可能加载真实评论。读取时以当前 DOM 文本为准，并检查是否出现「暂时没有更多评论」。

### 评论区情绪简报模板

```markdown
评论区情绪简报：
- 样本量：已加载 N 条评论
- 整体情绪：正向 / 中性 / 负向 / 混合 / 信息不足
- 主要主题：……
- 风险/争议点：……
- 置信度：高 / 中 / 低（说明原因）
```

### 评论/回复输入框定位

```javascript
// 点击「留下你的精彩评论吧」或某条评论的「回复」后：
browser action=act request={"kind":"evaluate","fn":"() => { const input = document.querySelector('[contenteditable=\"true\"].public-DraftEditor-content'); if (!input) return 'input not found'; const r = input.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height), text: input.innerText }; }"}
```

---

## 常见问题

**Q: 点击「私信」按钮没反应？**
A: 确认点击的是正确的按钮（顶栏最右侧，带"私信"文字）。也可先导航到 `/user/self` 页面再点击。

**Q: 私信面板找不到？**
A: 确认点击后有等待足够时间（`wait 2000ms`）。面板宽约 500px、高约 650px，固定在页面右侧。

**Q: 输入框找不到？**
A: 必须先在会话列表中点击一个具体用户，进入聊天详情模式，输入框才会出现。

**Q: 消息输入了但发送不成功？**
A: 先用 `kind: 'type'` 写入 Draft.js 输入框，再点击发送按钮。直接操作 DOM 文本（`textContent`赋值、`execCommand`、`clipboard paste`）无法触发 Draft.js 状态。

**Q: 怎么确认发送成功了？**
A: 发送成功后输入框被自动清空（textContent 变为空字符串）。

---

## 完整示例

```javascript
// 1. 打开抖音
browser action=open profile=openclaw targetUrl=https://www.douyin.com/
browser action=act request={"kind": "wait", "timeMs": 3000}

// 2. 点击「私信」按钮
browser action=act request={"kind": "evaluate", "fn": "() => { const all = Array.from(document.querySelectorAll('*')); for(const el of all) { const t = (el.textContent||'').trim(); const r = el.getBoundingClientRect(); if((t === '私信' || t.startsWith('私信')) && r.width > 0 && r.height > 0 && r.width < 100 && r.left > window.innerWidth - 200) { el.click(); return 'clicked: ' + t; } } return 'not found'; }"}
browser action=act request={"kind": "wait", "timeMs": 2000}

// 3. 点击目标用户
browser action=act request={"kind": "evaluate", "fn": "() => { const all = Array.from(document.querySelectorAll('*')); for(const el of all) { const t = (el.textContent||'').trim(); const r = el.getBoundingClientRect(); if(t.includes('<目标用户名>') && r.width > 0 && r.height > 0) { el.click(); return 'clicked: ' + t; } } return 'not found'; }"}
browser action=act request={"kind": "wait", "timeMs": 2000}

// 4. 写入消息并点击发送
browser action=act request={"kind": "type", "selector": "[contenteditable=\"true\"]", "text": "你好，这是测试消息"}
browser action=act request={"kind": "wait", "timeMs": 500}
browser action=act request={"kind": "evaluate", "fn": "() => { const btn = Array.from(document.querySelectorAll('*')).find(el => { const r = el.getBoundingClientRect(); const cls = String(el.className || ''); return r.width >= 20 && r.width <= 50 && r.height >= 20 && r.height <= 50 && r.left > window.innerWidth * 0.7 && r.top > window.innerHeight * 0.55 && (cls.includes('send') || cls.includes('PygT7Ced')); }); if(!btn) return 'send button not found'; btn.click(); return 'clicked send'; }"}
browser action=act request={"kind": "wait", "timeMs": 2000}

// 5. 确认发送
browser action=act request={"kind": "evaluate", "fn": "() => { const input = document.querySelector('[contenteditable=\"true\"]'); return input ? (input.textContent.length === 0 ? 'sent ✓' : 'not sent: ' + input.textContent) : 'input not found'; }"}
```
