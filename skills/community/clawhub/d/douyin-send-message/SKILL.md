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

---

## 参数

调用时传入两个参数：
- `联系人`：昵称、抖音显示名、或通过人物管理查询到的昵称
- `消息内容`：要发送的具体内容（字符串，支持 emoji）

---

## 执行步骤

### Step 1: 打开私信列表页面

```javascript
browser(action="open", url="https://www.douyin.com/chat", profile="openclaw")
browser(action="act", kind="wait", timeMs=800, targetId="<pageId>")
```

### Step 2: 用关键词查找并点击联系人

```javascript
browser(action="act", kind="evaluate", fn="() => { var name = 'CONTACT_KEYWORD'; var items = document.querySelectorAll('[class*=\"conversationConversationItemwrapper\"]'); for(var item of items) { if(item.innerText && item.innerText.includes(name)) { item.scrollIntoView({block: 'center', behavior: 'instant'}); var rect = item.getBoundingClientRect(); var opts = {view: window, bubbles: true, cancelable: true, clientX: rect.left + rect.width/2, clientY: rect.top + rect.height/2, buttons: 1}; item.dispatchEvent(new MouseEvent('mousedown', opts)); item.dispatchEvent(new MouseEvent('mouseup', opts)); item.dispatchEvent(new MouseEvent('click', opts)); return 'OK'; } } return 'Not found'; }", targetId="<pageId>")
browser(action="act", kind="wait", timeMs=500, targetId="<pageId>")
```

### Step 3: 输入并发送

```javascript
browser(action="act", kind="evaluate", fn="() => { var msg = 'MESSAGE_CONTENT'; var inputs = document.querySelectorAll('[contenteditable=\"true\"]'); for(var input of inputs) { var rect = input.getBoundingClientRect(); if(rect.width > 0 && rect.height > 0) { input.focus(); for(var i=0; i<msg.length; i++) { document.execCommand('insertText', false, msg[i]); } return 'OK'; } } return 'No input'; }", targetId="<pageId>")
browser(action="act", kind="press", key="Enter", targetId="<pageId>")
```

### Step 4: 验证发送成功

```javascript
browser(action="act", kind="evaluate", fn="() => { var msg = 'MESSAGE_CONTENT'; return document.body.innerText.includes(msg) ? 'OK' : 'FAIL'; }", targetId="<pageId>")
```

### Step 5: 关闭页面

```javascript
browser(action="close", targetId="<pageId>")
```

## 关键 DOM（2026-04-07 验证）

- 私信列表页面：`https://www.douyin.com/chat`
- 列表项容器：`div[class*="conversationConversationItemwrapper"]`
- 聊天输入框：`[contenteditable="true"]`
- **必须用 `document.execCommand('insertText')` 逐字输入**
- **必须用完整鼠标事件：`mousedown` → `mouseup` → `click`**
- **必须先 `scrollIntoView` 滚动到可视区域再点击**

## 性能

- 目标总耗时：**5-10 秒**

## 配合使用示例

**推荐：先查人物关系，再发送**

```
我收到："给昵称B发抖音"
1. 调用 memory_recall(query="昵称B 抖音")
2. 找到：昵称B → 抖音昵称C
3. 调用本技能，关键词：抖音昵称C
```

**独立使用：直接发送**

```
我收到："给 抖音昵称C 发消息"
直接调用本技能，关键词：抖音昵称C
```

## 注意事项

- 发送完毕后**必须关闭页面**释放资源
- 关键词会在私信列表中搜索匹配项
- 建议先通过 `person-relation-manager` 获取准确的抖音昵称
