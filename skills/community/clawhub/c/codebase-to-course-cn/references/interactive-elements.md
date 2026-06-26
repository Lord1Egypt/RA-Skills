# 交互元素参考

课程中使用的每种交互元素类型的实现模式。选择最适合每个模块教学目标的元素。

> **架构说明：** 这些元素的所有 CSS 和 JavaScript 都在 `references/styles.css` 和 `references/main.js` 中，它们被逐字复制到每个课程目录中。编写模块 HTML 文件时，只使用下面的 HTML 模式 — 不要为这些元素内联 `<style>` 或 `<script>` 标签。`main.js` 中的引擎在页面加载时通过扫描这里描述的相关类名和 `data-*` 属性自动初始化。

## 目录
1. [代码 ↔ 英语翻译块](#code--英语翻译块)
2. [多选题测验](#多选题测验)
3. [拖放匹配](#拖放匹配)
4. [群聊动画](#群聊动画)
5. [消息流 / 数据流动画](#消息流--数据流动画)
6. [交互式架构图](#交互式架构图)
7. [层次切换演示](#层次切换演示)
8. ["找 Bug"挑战](#找-bug-挑战)
9. [场景测验](#场景测验)
10. [提示框](#提示框)
11. [模式/功能卡片](#模式功能卡片)
12. [流程图](#流程图)
13. [权限/配置徽章](#权限配置徽章)
14. [词汇表提示](#词汇表提示)
15. [可视化文件树](#可视化文件树)
16. [图标-标签行](#图标-标签行)
17. [编号步骤卡片](#编号步骤卡片)

---

## 代码 ↔ 英语翻译块

最重要的教学元素。左侧显示项目中的真实代码，右侧逐行显示通俗英语翻译。

**HTML：**
```html
<div class="translation-block animate-in">
  <div class="translation-code">
    <span class="translation-label">CODE</span>
    <pre><code>
<span class="code-line"><span class="code-keyword">const</span> response = <span class="code-keyword">await</span> <span class="code-function">fetch</span>(url, {</span>
<span class="code-line">  <span class="code-property">method</span>: <span class="code-string">'POST'</span>,</span>
<span class="code-line">  <span class="code-property">headers</span>: { <span class="code-string">'Authorization'</span>: apiKey }</span>
<span class="code-line">});</span>
    </code></pre>
  </div>
  <div class="translation-english">
    <span class="translation-label">PLAIN ENGLISH</span>
    <div class="translation-lines">
      <p class="tl">向 URL 发送请求并等待响应...</p>
      <p class="tl">我们在发送数据（POST），不只是请求数据（GET）...</p>
      <p class="tl">包含我们的 API 密钥，让服务器知道我们是谁...</p>
      <p class="tl">请求设置结束。</p>
    </div>
  </div>
</div>
```

**CSS：**
```css
.translation-block {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  margin: var(--space-8) 0;
}
.translation-code {
  background: var(--color-bg-code);
  color: #CDD6F4;
  padding: var(--space-6);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  line-height: 1.7;
  position: relative;
  overflow-x: hidden;  /* 绝不出现水平滚动条 */
}
.translation-code pre,
.translation-code code {
  white-space: pre-wrap;       /* 换行长行而不是滚动 */
  word-break: break-word;      /* 必要时在单词中间断开 */
  overflow-x: hidden;
}
.translation-english {
  background: var(--color-surface-warm);
  padding: var(--space-6);
  font-size: var(--text-sm);
  line-height: 1.7;
  border-left: 3px solid var(--color-accent);
}
.translation-label {
  position: absolute;
  top: var(--space-2);
  right: var(--space-3);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.5;
}
.translation-english .translation-label {
  color: var(--color-text-muted);
}
/* 响应式：移动端垂直堆叠 */
@media (max-width: 768px) {
  .translation-block { grid-template-columns: 1fr; }
  .translation-english { border-left: none; border-top: 3px solid var(--color-accent); }
}
```

**规则：**
- 每行英语应对应 1-2 行代码
- 使用对话式语言，不要技术术语
- 强调"为什么"而不仅仅是"什么" —— 例如，"包含我们的 API 密钥，让服务器知道我们是谁"而不是"设置 Authorization 头"

---

## 多选题测验

用于即时反馈测试理解。每个问题有选项、一个正确答案和每个问题的解释。

**连接方式：** `main.js` 暴露 `window.selectOption(btn)`、`window.checkQuiz(containerId)` 和 `window.resetQuiz(containerId)`。通过 `onclick` 调用它们。每个问题的解释放在 `.quiz-question-block` 上的 `data-explanation-right` 和 `data-explanation-wrong` 中。

**HTML：**
```html
<div class="quiz-container" id="quiz-module3">
  <div class="quiz-question-block"
       data-correct="option-b"
       data-explanation-right="没错 — 因为 X 在此架构中负责 Y。"
       data-explanation-wrong="不完全对。想想 Y 在代码库中的位置...">
    <h3 class="quiz-question">问题文本在这里？</h3>
    <div class="quiz-options">
      <button class="quiz-option" data-value="option-a" onclick="selectOption(this)">
        <div class="quiz-option-radio"></div>
        <span>答案 A</span>
      </button>
      <button class="quiz-option" data-value="option-b" onclick="selectOption(this)">
        <div class="quiz-option-radio"></div>
        <span>答案 B（正确）</span>
      </button>
      <button class="quiz-option" data-value="option-c" onclick="selectOption(this)">
        <div class="quiz-option-radio"></div>
        <span>答案 C</span>
      </button>
    </div>
    <div class="quiz-feedback"></div>
  </div>

  <button class="quiz-check-btn" onclick="checkQuiz('quiz-module3')">检查答案</button>
  <button class="quiz-reset-btn" onclick="resetQuiz('quiz-module3')">重试</button>
</div>
```

**测验状态的 CSS：**
```css
.quiz-option {
  display: flex; align-items: center; gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  cursor: pointer; width: 100%;
  transition: border-color var(--duration-fast), background var(--duration-fast);
}
.quiz-option:hover { border-color: var(--color-accent-muted); }
.quiz-option.selected { border-color: var(--color-accent); background: var(--color-accent-light); }
.quiz-option.correct { border-color: var(--color-success); background: var(--color-success-light); }
.quiz-option.incorrect { border-color: var(--color-error); background: var(--color-error-light); }
.quiz-option-radio {
  width: 18px; height: 18px; border-radius: 50%;
  border: 2px solid var(--color-border);
  transition: all var(--duration-fast);
}
.quiz-option.selected .quiz-option-radio {
  border-color: var(--color-accent);
  background: var(--color-accent);
  box-shadow: inset 0 0 0 3px white;
}
.quiz-feedback {
  max-height: 0; overflow: hidden; opacity: 0;
  transition: max-height var(--duration-normal), opacity var(--duration-normal);
}
.quiz-feedback.show { max-height: 200px; opacity: 1; padding: var(--space-3); margin-top: var(--space-2); border-radius: var(--radius-sm); }
.quiz-feedback.success { background: var(--color-success-light); color: var(--color-success); }
.quiz-feedback.error { background: var(--color-error-light); color: var(--color-error); }
```

---

## 拖放匹配

用于将概念与描述匹配。支持鼠标（HTML5 拖放 API）和触摸。

**HTML：**
```html
<div class="dnd-container">
  <div class="dnd-chips">
    <div class="dnd-chip" draggable="true" data-answer="actor-a">角色 A</div>
    <div class="dnd-chip" draggable="true" data-answer="actor-b">角色 B</div>
    <div class="dnd-chip" draggable="true" data-answer="actor-c">角色 C</div>
  </div>
  <div class="dnd-zones">
    <div class="dnd-zone" data-correct="actor-a">
      <p class="dnd-zone-label">角色 A 的描述</p>
      <div class="dnd-zone-target">拖到这里</div>
    </div>
    <!-- 更多区域 -->
  </div>
  <button onclick="checkDnD()">检查匹配</button>
  <button onclick="resetDnD()">重置</button>
</div>
```

**JS（鼠标 + 触摸）：**
```javascript
// 鼠标：HTML5 拖放 API
chips.forEach(chip => {
  chip.addEventListener('dragstart', (e) => {
    e.dataTransfer.setData('text/plain', chip.dataset.answer);
    chip.classList.add('dragging');
  });
  chip.addEventListener('dragend', () => chip.classList.remove('dragging'));
});

zones.forEach(zone => {
  const target = zone.querySelector('.dnd-zone-target');
  target.addEventListener('dragover', (e) => { e.preventDefault(); target.classList.add('drag-over'); });
  target.addEventListener('dragleave', () => target.classList.remove('drag-over'));
  target.addEventListener('drop', (e) => {
    e.preventDefault();
    target.classList.remove('drag-over');
    const answer = e.dataTransfer.getData('text/plain');
    const chip = document.querySelector(`[data-answer="${answer}"]`);
    target.textContent = chip.textContent;
    target.dataset.placed = answer;
    chip.classList.add('placed');
  });
});

// 触摸：自定义实现（HTML5 拖放在移动端不工作）
chips.forEach(chip => {
  chip.addEventListener('touchstart', (e) => {
    e.preventDefault();
    const touch = e.touches[0];
    const clone = chip.cloneNode(true);
    clone.classList.add('touch-ghost');
    clone.style.cssText = `position:fixed; z-index:1000; pointer-events:none;
      left:${touch.clientX - 40}px; top:${touch.clientY - 20}px;`;
    document.body.appendChild(clone);
    chip._ghost = clone;
    chip._answer = chip.dataset.answer;
  }, { passive: false });

  chip.addEventListener('touchmove', (e) => {
    e.preventDefault();
    const touch = e.touches[0];
    if (chip._ghost) {
      chip._ghost.style.left = (touch.clientX - 40) + 'px';
      chip._ghost.style.top = (touch.clientY - 20) + 'px';
    }
    // 高亮手指下的区域
    const el = document.elementFromPoint(touch.clientX, touch.clientY);
    zones.forEach(z => z.querySelector('.dnd-zone-target').classList.remove('drag-over'));
    if (el && el.closest('.dnd-zone-target')) {
      el.closest('.dnd-zone-target').classList.add('drag-over');
    }
  }, { passive: false });

  chip.addEventListener('touchend', (e) => {
    if (chip._ghost) { chip._ghost.remove(); chip._ghost = null; }
    const touch = e.changedTouches[0];
    const el = document.elementFromPoint(touch.clientX, touch.clientY);
    if (el && el.closest('.dnd-zone-target')) {
      const target = el.closest('.dnd-zone-target');
      target.textContent = chip.textContent;
      target.dataset.placed = chip._answer;
      chip.classList.add('placed');
    }
  });
});
```

---

## 群聊动画

iMessage/微信风格的聊天，显示组件之间"对话"。消息逐一出现，带有输入指示器。

**连接方式：** `main.js` 在页面加载时自动初始化每个 `.chat-window`。给每个聊天窗口一个唯一的 `id`。控制按钮需要这些类：`.chat-next-btn`、`.chat-all-btn`、`.chat-reset-btn`。输入指示器头像元素应该有 `id="{chatWindowId}-typing-avatar"` 或者简单是 `.chat-typing` 内的第一个 `.chat-avatar`。

**HTML：**
```html
<div class="chat-window" id="chat-module2">
  <div class="chat-messages">
    <div class="chat-message" data-msg="0" data-sender="actor-a" style="display:none">
      <div class="chat-avatar" style="background: var(--color-actor-1)">A</div>
      <div class="chat-bubble">
        <span class="chat-sender" style="color: var(--color-actor-1)">角色 A</span>
        <p>嘿 Background，我需要这个项目的数据。</p>
      </div>
    </div>
    <!-- 更多消息... -->
  </div>

  <div class="chat-typing" id="chat-typing" style="display:none">
    <div class="chat-avatar" id="typing-avatar">?</div>
    <div class="chat-typing-dots">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>
  </div>

  <div class="chat-controls">
    <button class="btn chat-next-btn">下一条消息</button>
    <button class="btn chat-all-btn">全部播放</button>
    <button class="btn chat-reset-btn">重播</button>
    <span class="chat-progress"></span>
  </div>
</div>
```

**输入点的 CSS：**
```css
.typing-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--color-text-muted);
  animation: typingBounce 1.4s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}
```

---

## 消息流 / 数据流动画

组件之间数据移动的分步可视化。用户点击"下一步"前进。

**连接方式：** `main.js` 在页面加载时自动初始化每个 `.flow-animation`。在 `data-steps` 中传递步骤为 JSON。每个步骤对象：`{ highlight: "flow-actor-id", label: "描述", packet: true, from: "actor-id-suffix", to: "actor-id-suffix" }`。角色元素 ID 必须是 `flow-actor-1`、`flow-actor-2` 等。控制按钮需要类 `.flow-next-btn` 和 `.flow-reset-btn`。

> **⚠️ 步骤标签中的单引号会破坏解析。** `data-steps` 属性由单引号定界（`data-steps='[...]'`），所以标签内的任何单引号（例如 `"the user's request"`）会提前终止属性并导致 `JSON.parse` 静默失败 —— 整个动画将停止工作。要么避免在标签中使用撇号，用 `&apos;` 替换，或使用双引号定界并转义内部引号重写属性（`data-steps="[{\"label\":\"...\"}]"`）。

**HTML：**
```html
<div class="flow-animation" data-steps='[
  {"highlight":"flow-actor-1","label":"用户点击按钮"},
  {"highlight":"flow-actor-1","label":"前端发送请求","packet":true,"from":"actor-1","to":"actor-2"},
  {"highlight":"flow-actor-2","label":"后端调用数据库","packet":true,"from":"actor-2","to":"actor-3"}
]'>
  <div class="flow-actors">
    <div class="flow-actor" id="flow-actor-1">
      <div class="flow-actor-icon">A</div>
      <span>角色 1</span>
    </div>
    <div class="flow-actor" id="flow-actor-2">
      <div class="flow-actor-icon">B</div>
      <span>角色 2</span>
    </div>
    <div class="flow-actor" id="flow-actor-3">
      <div class="flow-actor-icon">C</div>
      <span>角色 3</span>
    </div>
  </div>

  <div class="flow-packet" id="flow-packet"></div>

  <div class="flow-step-label" id="flow-label">点击"下一步"开始</div>

  <div class="flow-controls">
    <button class="btn flow-next-btn">下一步</button>
    <button class="btn flow-reset-btn">重新开始</button>
    <span class="flow-progress"></span>
  </div>
</div>
```

**活动角色发光的 CSS：**
```css
.flow-actor.active {
  box-shadow: 0 0 0 3px var(--color-accent), 0 0 20px rgba(217, 79, 48, 0.2);
  transform: scale(1.05);
  transition: all var(--duration-normal) var(--ease-out);
}
```

---

## 交互式架构图

全系统图，悬停/点击组件显示描述提示框。

**HTML：**
```html
<div class="arch-diagram">
  <div class="arch-zone arch-zone-browser">
    <h4 class="arch-zone-label">浏览器</h4>
    <div class="arch-component" data-desc="将 UI 注入网页，读取 DOM，捕获用户操作"
         onclick="showArchDesc(this)">
      <div class="arch-icon">📄</div>
      <span>组件 A</span>
    </div>
    <!-- 更多组件 -->
  </div>
  <div class="arch-zone arch-zone-external">
    <h4 class="arch-zone-label">外部服务</h4>
    <!-- API 卡片 -->
  </div>
  <div class="arch-description" id="arch-desc">点击任何组件了解它的作用</div>
</div>
```

---

## 层次切换演示

显示不同层（例如，HTML/CSS/JS，或数据/逻辑/UI）如何相互构建。三个标签在视图之间切换。

**HTML：**
```html
<div class="layer-demo">
  <div class="layer-tabs">
    <button class="layer-tab active" onclick="showLayer('html')">HTML</button>
    <button class="layer-tab" onclick="showLayer('css')">+ CSS</button>
    <button class="layer-tab" onclick="showLayer('js')">+ JS</button>
  </div>
  <div class="layer-viewport">
    <div class="layer" id="layer-html" style="display:block">
      <!-- 原始无样式版本 -->
    </div>
    <div class="layer" id="layer-css" style="display:none">
      <!-- 带样式版本 -->
    </div>
    <div class="layer" id="layer-js" style="display:none">
      <!-- 交互版本 -->
    </div>
  </div>
  <p class="layer-description" id="layer-desc">这是原始 HTML...</p>
</div>
```

---

## "找 Bug"挑战

显示带有故意 bug 的代码。用户点击有 bug 的行。显示解释问题。

**HTML：**
```html
<div class="bug-challenge">
  <h3>找出这段代码中的 bug：</h3>
  <div class="bug-code">
    <div class="bug-line" data-line="1" onclick="checkBugLine(this, false)">
      <span class="line-num">1</span>
      <code>chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {</code>
    </div>
    <div class="bug-line" data-line="2" onclick="checkBugLine(this, false)">
      <span class="line-num">2</span>
      <code>  if (msg.action === 'fetchData') {</code>
    </div>
    <div class="bug-line bug-target" data-line="3" onclick="checkBugLine(this, true)">
      <span class="line-num">3</span>
      <code>    fetch(url).then(r => r.json()).then(data => sendResponse(data));</code>
    </div>
    <div class="bug-line" data-line="4" onclick="checkBugLine(this, false)">
      <span class="line-num">4</span>
      <code>  }</code>
    </div>
    <div class="bug-line" data-line="5" onclick="checkBugLine(this, false)">
      <span class="line-num">5</span>
      <code>});</code>
    </div>
  </div>
  <div class="bug-feedback" id="bug-feedback"></div>
</div>
```

**JS：**
```javascript
window.checkBugLine = function(el, isCorrect) {
  const feedback = el.closest('.bug-challenge').querySelector('.bug-feedback');
  if (isCorrect) {
    el.classList.add('correct');
    feedback.innerHTML = '<strong>找到了！</strong> 监听器使用了异步操作（fetch）但没有返回 true。Chrome 在响应发送之前关闭消息通道。修复：在末尾添加 <code>return true;</code>。';
    feedback.className = 'bug-feedback show success';
  } else {
    el.classList.add('incorrect');
    feedback.innerHTML = '不是这行 — 找找异步时序可能引起问题的地方...';
    feedback.className = 'bug-feedback show error';
    setTimeout(() => { el.classList.remove('incorrect'); feedback.className = 'bug-feedback'; }, 2000);
  }
};
```

---

## 场景测验

"资深工程师会怎么做？" —— 情境问题带解释。

与多选题相同的 HTML/CSS/JS 模式，但场景描述更长，解释更详细。将每个问题包装在场景上下文块中：

```html
<div class="scenario-block">
  <div class="scenario-context">
    <span class="scenario-label">场景</span>
    <p>你的应用处理 3 小时的播客转录。API 有 16,000 token 限制。你怎么办？</p>
  </div>
  <!-- quiz-options 在这里 -->
</div>
```

---

## 提示框

"顿悟！"时刻 —— 通用计算机科学见解。每个模块最多 2 个。

```html
<div class="callout callout-accent">
  <div class="callout-icon">💡</div>
  <div class="callout-content">
    <strong class="callout-title">关键见解</strong>
    <p>这个模式 —— 将职责分成专注的角色 —— 是软件工程中最重要的想法之一。工程师称之为"关注点分离"。</p>
  </div>
</div>
```

**变体：**
- `callout-accent`：朱红色左边框，浅强调背景（用于 CS 见解）
- `callout-info`：青色左边框，浅信息背景（用于"值得了解"）
- `callout-warning`：红色左边框，浅错误背景（用于常见错误）

---

## 模式/功能卡片

突出工程模式、技术栈组件或关键概念的卡片网格。

```html
<div class="pattern-cards">
  <div class="pattern-card" style="border-top: 3px solid var(--color-actor-1)">
    <div class="pattern-icon" style="background: var(--color-actor-1)">🔄</div>
    <h4 class="pattern-title">缓存</h4>
    <p class="pattern-desc">存储结果以避免重复工作 —— 就像保存剩菜而不是每次都做新饭。</p>
  </div>
  <!-- 更多卡片 -->
</div>
```

```css
.pattern-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
}
.pattern-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  transition: transform var(--duration-normal) var(--ease-out), box-shadow var(--duration-normal);
}
.pattern-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}
```

---

## 流程图

**水平流程（桌面）：**
```html
<div class="flow-steps">
  <div class="flow-step">
    <div class="flow-step-num">1</div>
    <p>用户点击按钮</p>
  </div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">
    <div class="flow-step-num">2</div>
    <p>组件 A 检测到点击</p>
  </div>
  <div class="flow-arrow">→</div>
  <!-- 更多步骤 -->
</div>
```

箭头在移动端通过 CSS 变换旋转为 `↓`。

---

## 权限/配置徽章

用于注释配置文件、权限或设置：

```html
<div class="badge-list">
  <div class="badge-item">
    <code class="badge-code">storage</code>
    <span class="badge-desc">在会话之间保存数据（像浏览器书签）</span>
  </div>
  <div class="badge-item">
    <code class="badge-code">activeTab</code>
    <span class="badge-desc">访问当前打开的标签页（仅当用户点击时）</span>
  </div>
</div>
```

```css
.badge-item {
  display: flex; align-items: center; gap: var(--space-4);
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-sm);
  transition: border-color var(--duration-fast);
}
.badge-item:hover { border-color: var(--color-accent-muted); }
.badge-code {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  background: var(--color-bg-code);
  color: #CBA6F7;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-sm);
  white-space: nowrap;
}
```

---

## 词汇表提示

非技术学习者最重要的无障碍功能。课程文本中的任何技术术语都应该包装在提示中，在悬停（桌面）或点击（移动）时显示通俗英语定义。学习者永远不需要离开页面或 Google 任何东西。

**HTML — 内联标记术语：**
```html
<p>扩展使用
  <span class="term" data-definition="service worker 是独立于网页运行的后台脚本 —— 就像一个始终开启的幕后助手，即使你没有在看页面。">service worker</span>
  来处理 API 调用。
</p>
```

**CSS：**
```css
.term {
  border-bottom: 1.5px dashed var(--color-accent-muted);
  cursor: pointer;    /* 不是 cursor: help — pointer 感觉可点击且诱人 */
  position: relative;
}
.term:hover, .term.active {
  border-bottom-color: var(--color-accent);
  color: var(--color-accent);
}

/* 提示框气泡 — 使用 position: fixed 并通过 JS 附加到 document.body
   所以它永远不会被祖先的 overflow: hidden 容器裁剪
   （像翻译块）。参见下面 JS 部分的定位逻辑。 */
.term-tooltip {
  position: fixed;        /* 关键：fixed，不是 absolute — 防止裁剪 */
  background: var(--color-bg-code);
  color: #CDD6F4;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
  font-family: var(--font-body);
  line-height: var(--leading-normal);
  width: max(200px, min(320px, 80vw));
  box-shadow: var(--shadow-lg);
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--duration-fast);
  z-index: 10000;        /* 在所有东西之上，包括导航 */
}
/* 向下的箭头 */
.term-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: var(--color-bg-code);
}
.term-tooltip.visible {
  opacity: 1;
}

/* 如果提示框超出屏幕顶部，翻转到下方 */
.term-tooltip.flip {
  bottom: auto;
  top: calc(100% + 8px);
}
.term-tooltip.flip::after {
  top: auto;
  bottom: 100%;
  border-top-color: transparent;
  border-bottom-color: var(--color-bg-code);
}
```

**JS — 附加到 body 的 position: fixed 提示框（永远不会被 overflow 裁剪）：**
```javascript
// 提示框容器 — 附加到 body 所以永远不会被裁剪
let activeTooltip = null;

function positionTooltip(term, tip) {
  const rect = term.getBoundingClientRect();
  const tipWidth = 300; // 大约
  let left = rect.left + rect.width / 2 - tipWidth / 2;
  // 限制在视口内
  left = Math.max(8, Math.min(left, window.innerWidth - tipWidth - 8));

  // 先尝试上方
  let top = rect.top - 8;
  tip.style.left = left + 'px';

  // 默认定位在上方，如果没有空间则翻转到下方
  document.body.appendChild(tip);
  const tipHeight = tip.offsetHeight;
  if (rect.top - tipHeight - 8 < 0) {
    // 翻转到下方
    tip.style.top = (rect.bottom + 8) + 'px';
    tip.classList.add('flip');
  } else {
    tip.style.top = (rect.top - tipHeight - 8) + 'px';
    tip.classList.remove('flip');
  }
}

document.querySelectorAll('.term').forEach(term => {
  const tip = document.createElement('span');
  tip.className = 'term-tooltip';
  tip.textContent = term.dataset.definition;

  // 桌面端悬停
  term.addEventListener('mouseenter', () => {
    if (activeTooltip && activeTooltip !== tip) {
      activeTooltip.classList.remove('visible');
      activeTooltip.remove();
    }
    positionTooltip(term, tip);
    requestAnimationFrame(() => tip.classList.add('visible'));
    activeTooltip = tip;
  });

  term.addEventListener('mouseleave', () => {
    tip.classList.remove('visible');
    setTimeout(() => { if (!tip.classList.contains('visible')) tip.remove(); }, 150);
    activeTooltip = null;
  });

  // 移动端点击
  term.addEventListener('click', (e) => {
    e.stopPropagation();
    if (activeTooltip && activeTooltip !== tip) {
      activeTooltip.classList.remove('visible');
      activeTooltip.remove();
    }
    if (tip.classList.contains('visible')) {
      tip.classList.remove('visible');
      tip.remove();
      activeTooltip = null;
    } else {
      positionTooltip(term, tip);
      requestAnimationFrame(() => tip.classList.add('visible'));
      activeTooltip = tip;
    }
  });
});

// 点击其他地方关闭提示框
document.addEventListener('click', () => {
  if (activeTooltip) {
    activeTooltip.classList.remove('visible');
    activeTooltip.remove();
    activeTooltip = null;
  }
});
```

**规则：**
- 在每个模块首次使用时标记每个技术术语（API、DOM、回调、异步、端点、中间件等）
- 定义最多 1-2 句话，使用日常语言
- 在定义中使用隐喻当它有帮助时 —— 例如，"**回调**就像在餐厅留下你的电话号码，这样当你的桌子准备好时他们可以打电话给你"
- 不要在同一屏幕内标记同一个术语两次 — 只在每个模块首次出现时
- 虚线下划线应该足够微妙不分散注意力，但也足够明显让好奇的学习者发现它

---

## 可视化文件树

使用此代替列出"这个文件夹做 X，那个文件夹做 Y"的段落。更容易扫描。

```html
<div class="file-tree">
  <div class="ft-folder open">
    <span class="ft-name">app/</span>
    <span class="ft-desc">页面和 API 路由</span>
    <div class="ft-children">
      <div class="ft-folder">
        <span class="ft-name">api/</span>
        <span class="ft-desc">前端调用的后端端点</span>
      </div>
      <div class="ft-file">
        <span class="ft-name">layout.tsx</span>
        <span class="ft-desc">包装每个页面的外壳</span>
      </div>
    </div>
  </div>
  <div class="ft-folder">
    <span class="ft-name">components/</span>
    <span class="ft-desc">可复用的 UI 构建块</span>
  </div>
  <div class="ft-folder">
    <span class="ft-name">lib/</span>
    <span class="ft-desc">共享逻辑和工具</span>
  </div>
</div>
```

```css
.file-tree { font-family: var(--font-mono); font-size: var(--text-sm); }
.ft-folder, .ft-file {
  padding: var(--space-2) var(--space-3);
  border-left: 2px solid var(--color-border-light);
  margin-left: var(--space-4);
}
.ft-folder > .ft-name { color: var(--color-accent); font-weight: 600; }
.ft-folder > .ft-name::before { content: '📁 '; }
.ft-file > .ft-name::before { content: '📄 '; }
.ft-desc {
  color: var(--color-text-secondary);
  font-family: var(--font-body);
  margin-left: var(--space-2);
  font-size: var(--text-xs);
}
.ft-children { margin-left: var(--space-4); }
```

---

## 图标-标签行

用于可视化列出组件、功能或概念。替换项目符号段落。

```html
<div class="icon-rows">
  <div class="icon-row">
    <div class="icon-circle" style="background: var(--color-actor-1)">🖥️</div>
    <div>
      <strong>前端 (Next.js)</strong>
      <p>用户看到和交互的内容</p>
    </div>
  </div>
  <div class="icon-row">
    <div class="icon-circle" style="background: var(--color-actor-2)">⚡</div>
    <div>
      <strong>API 路由</strong>
      <p>在服务器上运行的后端逻辑</p>
    </div>
  </div>
  <div class="icon-row">
    <div class="icon-circle" style="background: var(--color-actor-3)">🗄️</div>
    <div>
      <strong>数据库 (Supabase)</strong>
      <p>所有数据永久存储的地方</p>
    </div>
  </div>
</div>
```

```css
.icon-rows { display: flex; flex-direction: column; gap: var(--space-4); }
.icon-row {
  display: flex; align-items: center; gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.icon-row p { margin: 0; color: var(--color-text-secondary); font-size: var(--text-sm); }
.icon-circle {
  width: 48px; height: 48px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.25rem; flex-shrink: 0;
}
```

---

## 编号步骤卡片

用于本来是编号段落列表的序列。视觉化、可扫描，每步独立存在。

```html
<div class="step-cards">
  <div class="step-card">
    <div class="step-num">1</div>
    <div class="step-body">
      <strong>用户粘贴 YouTube URL</strong>
      <p>前端捕获 URL 并提取视频 ID</p>
    </div>
  </div>
  <div class="step-card">
    <div class="step-num">2</div>
    <div class="step-body">
      <strong>API 获取转录</strong>
      <p>服务器端路由调用外部服务获取视频文本</p>
    </div>
  </div>
  <div class="step-card">
    <div class="step-num">3</div>
    <div class="step-body">
      <strong>AI 分析内容</strong>
      <p>转录发送给提取关键时刻的 AI 模型</p>
    </div>
  </div>
</div>
```

```css
.step-cards { display: flex; flex-direction: column; gap: var(--space-3); }
.step-card {
  display: flex; align-items: flex-start; gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--color-accent);
  box-shadow: var(--shadow-sm);
}
.step-num {
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--color-accent);
  color: white; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-display);
  flex-shrink: 0;
}
.step-body p { margin: var(--space-1) 0 0; color: var(--color-text-secondary); font-size: var(--text-sm); }
```
