---
name: douyin-send-message
description: 在抖音网页版发送私信消息。当用户想发送抖音私信、提醒续火花、或者提到"抖音发消息"、"发抖音私信"、"douyin send message"时触发。支持独立使用或配合人物关系管理技能使用。
---

# 抖音私信发送

## 两种使用模式

### 模式一：独立使用（手动提供抖音昵称）

为用户直接提供抖音昵称时，直接使用：
- "给 xxx 发消息" → xxx 作为搜索关键词
- "给 用户A 发消息" → 直接搜索 "用户A"

### 模式二：配合人物关系管理使用

**推荐流程：**
1. 先调用 `person-relation-manager` 查询真实抖音昵称
2. 拿到昵称后再执行发送

**自动流程：**
```
用户："给昵称B发抖音私信"
     ↓
我查询记忆（person-relation-manager）：昵称B → 抖音昵称C
     ↓
调用本技能发送，关键词：抖音昵称C
```

**注意：** 如果 `person-relation-manager` 技能不存在，提示用户安装：
> 人物关系管理技能未安装，是否从 ClawHub 安装？请说 "是的" 安装，或直接告诉我对方的抖音昵称。

如用户同意安装，执行：
```bash
clawhub install person-relation-manager --workdir ~/.openclaw/workspace
```

---

## 参数

调用时传入两个参数：
- `联系人`：昵称、抖音显示名、或通过人物管理查询到的昵称
- `消息内容`：要发送的具体内容（字符串，支持 emoji）

---

## 执行步骤

### Step 1: 搜索并进入用户主页

1. 打开新标签页，导航到搜索页：
   ```javascript
   browser(action="open", url="https://www.douyin.com/aisearch?from_nav=1&search_source=normal_search&query=<联系人>&type=user", label="douyin_dm")
   ```
2. 等待页面加载：
   ```javascript
   browser(action="act", kind="wait", timeMs=2000, targetId="<返回的targetId>")
   ```
3. 截取快照，找到"用户" tab 并点击：
   ```javascript
   browser(action="snapshot", targetId="<targetId>", refs="aria")
   // 找到 tab "用户" [ref=e??] 点击
   browser(action="act", kind="click", ref="<用户tab的ref>", targetId="<targetId>")
   ```
4. 等待搜索结果加载，再次快照，找到目标用户的链接并点击进入主页

### Step 2: 在主页点击"私信"按钮

进入用户主页后，快照找到"私信"按钮并点击：
```javascript
browser(action="snapshot", targetId="<targetId>", refs="aria")
// 找到 button "私信" [ref=e??] 点击
browser(action="act", kind="click", ref="<私信按钮的ref>", targetId="<targetId>")
```

### Step 3: 在聊天窗口输入并发送

私信窗口弹出后（URL 不变但 DOM 变化），直接用 JavaScript 输入：
```javascript
browser(action="act", kind="evaluate", fn="() => { var msg = '<消息内容>'; var inputs = document.querySelectorAll('[contenteditable=\"true\"]'); for(var input of inputs) { var rect = input.getBoundingClientRect(); if(rect.width > 0 && rect.height > 0) { input.focus(); for(var i=0; i<msg.length; i++) { document.execCommand('insertText', false, msg[i]); } return 'OK'; } } return 'No input'; }", targetId="<targetId>")
browser(action="act", kind="press", key="Enter", targetId="<targetId>")
```

### Step 4: 验证发送成功

```javascript
browser(action="act", kind="evaluate", fn="() => { var msg = '<消息内容>'; return document.body.innerText.includes(msg) ? 'OK' : 'FAIL'; }", targetId="<targetId>")
```

### Step 5: 关闭页面（释放资源）

```javascript
browser(action="close", targetId="<targetId>")
```

---

## 关键 DOM（2026-06-26 实测）

- 搜索用户：`https://www.douyin.com/aisearch?query=<联系人>&type=user`
- 用户主页按钮：button "私信" [ref]
- 聊天输入框：`[contenteditable="true"]`（需要宽度>0、高度>0才可输入）
- **必须用 `document.execCommand('insertText')` 逐字输入**
- **Enter 发送：`browser(action="press", key="Enter")`**

## 性能

- 目标总耗时：**5-10 秒**

## 配合使用示例

**推荐：先查人物关系，再发送**

```
我收到："给昵称B发抖音"
1. 调用 person-relation-manager 查找：昵称B → 抖音昵称C
   - 如果技能不存在，提示用户安装
2. 调用本技能，关键词：抖音昵称C
```

**独立使用：直接发送**

```
我收到："给 抖音昵称C 发消息"
直接调用本技能，关键词：抖音昵称C
```

## 注意事项

- 发送完毕后**必须关闭页面**（`browser(action="close")`）释放资源
- 私信列表内搜索适合已有聊天记录的好友；新好友建议从主页"私信"按钮进入
- 建议先通过 `person-relation-manager` 获取准确的抖音昵称
- 如果 `person-relation-manager` 不存在，引导用户从 ClawHub 安装
- 每次发送使用独立的浏览器标签页，操作完成后立即关闭
