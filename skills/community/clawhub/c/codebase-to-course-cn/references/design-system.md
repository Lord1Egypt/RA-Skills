# 设计系统参考

课程的完整 CSS 设计 token。将整个 `:root` 块复制到课程 HTML 中，并调整强调色以适应项目的个性。

## 目录
1. [调色板](#调色板)
2. [排版](#排版)
3. [间距与布局](#间距与布局)
4. [阴影与深度](#阴影与深度)
5. [动画与过渡](#动画与过渡)
6. [导航与进度](#导航与进度)
7. [模块结构](#模块结构)
8. [响应式断点](#响应式断点)
9. [滚动条与背景](#滚动条与背景)

---

## 调色板

```css
:root {
  /* --- 背景 --- */
  --color-bg:             #FAF7F2;       /* 温暖的米白色，像旧纸张 */
  --color-bg-warm:        #F5F0E8;       /* 稍微更温暖，用于交替模块 */
  --color-bg-code:        #1E1E2E;       /* 深靛蓝炭黑，用于代码块 */
  --color-text:           #2C2A28;       /* 深炭黑，对眼睛友好 */
  --color-text-secondary: #6B6560;       /* 温暖的灰色，用于次要文本 */
  --color-text-muted:     #9E9790;       /* 柔和的，用于时间戳、标签 */
  --color-border:         #E5DFD6;       /* 微妙的温暖边框 */
  --color-border-light:   #EEEBE5;       /* 更浅的边框 */
  --color-surface:        #FFFFFF;       /* 卡片表面 */
  --color-surface-warm:   #FDF9F3;       /* 温暖的卡片表面 */

  /* --- 强调色（根据项目调整 — 选择一个大胆的颜色）---
     默认：朱红色。替代方案：珊瑚色 (#E06B56)、青色 (#2A7B9B)、
     琥珀色 (#D4A843)、森林色 (#2D8B55)。避免紫色渐变。 */
  --color-accent:         #D94F30;
  --color-accent-hover:   #C4432A;
  --color-accent-light:   #FDEEE9;
  --color-accent-muted:   #E8836C;

  /* --- 语义色 --- */
  --color-success:        #2D8B55;
  --color-success-light:  #E8F5EE;
  --color-error:          #C93B3B;
  --color-error-light:    #FDE8E8;
  --color-info:           #2A7B9B;
  --color-info-light:     #E4F2F7;

  /* --- 角色颜色（分配给主要组件）---
     代码库中的每个主要"角色"获得一个独特的颜色
     用于聊天气泡、图表和高亮 */
  --color-actor-1:        #D94F30;       /* 朱红色 */
  --color-actor-2:        #2A7B9B;       /* 青色 */
  --color-actor-3:        #7B6DAA;       /* 柔和的梅红色 */
  --color-actor-4:        #D4A843;       /* 金色 */
  --color-actor-5:        #2D8B55;       /* 森林色 */
}
```

**规则：**
- 偶数模块使用 `--color-bg`，奇数模块使用 `--color-bg-warm`（交替背景创造视觉节奏）
- 角色颜色应该在视觉上彼此区分并与强调色区分
- 代码块始终使用 `--color-bg-code` 配浅色文本

---

## 排版

```css
:root {
  /* --- 字体 ---
     使用系统字体回退，确保中国大陆用户无需翻墙即可正常显示。
     展示/正文字体：中文优先系统字体
     等宽字体：开发者友好的等宽系统字体回退链 */
  --font-display:  'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
  --font-body:     'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:     'JetBrains Mono', 'Fira Code', 'Source Code Pro', 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;

  /* --- 类型比例（1.25 比例）--- */
  --text-xs:   0.75rem;    /* 12px — 标签、徽章 */
  --text-sm:   0.875rem;   /* 14px — 次要文本、代码 */
  --text-base: 1rem;       /* 16px — 正文文本 */
  --text-lg:   1.125rem;   /* 18px — 引导段落 */
  --text-xl:   1.25rem;    /* 20px — 屏幕标题 */
  --text-2xl:  1.5rem;     /* 24px — 子模块标题 */
  --text-3xl:  1.875rem;   /* 30px — 模块副标题 */
  --text-4xl:  2.25rem;    /* 36px — 模块标题 */
  --text-5xl:  3rem;       /* 48px — 英雄文本 */
  --text-6xl:  3.75rem;    /* 60px — 模块编号 */

  /* --- 行高 --- */
  --leading-tight:  1.15;  /* 标题 */
  --leading-snug:   1.3;   /* 小标题 */
  --leading-normal: 1.6;   /* 正文文本 */
  --leading-loose:  1.8;   /* 轻松阅读 */
}
```

**注意：使用系统字体，无需外部字体链接**
本技能面向中国大陆用户，所有字体使用系统字体回退链，无需加载 Google Fonts 或任何外部 CDN。

**规则：**
- 模块编号：`--text-6xl`、font-display、weight 800、`--color-accent` 配 15% 不透明度
- 模块标题：`--text-4xl`、font-display、weight 700
- 屏幕标题：`--text-xl` 或 `--text-2xl`、font-display、weight 600
- 正文文本：`--text-base` 或 `--text-lg`、font-body、`--leading-normal`
- 代码：`--text-sm`、font-mono
- 标签/徽章：`--text-xs`、font-mono、大写、letter-spacing 0.05em

---

## 间距与布局

```css
:root {
  --space-1:  0.25rem;   /* 4px */
  --space-2:  0.5rem;    /* 8px */
  --space-3:  0.75rem;   /* 12px */
  --space-4:  1rem;      /* 16px */
  --space-5:  1.25rem;   /* 20px */
  --space-6:  1.5rem;    /* 24px */
  --space-8:  2rem;      /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
  --space-20: 5rem;      /* 80px */
  --space-24: 6rem;      /* 96px */

  --content-width:     800px;   /* 标准阅读宽度 */
  --content-width-wide: 1000px; /* 用于并排布局 */
  --nav-height:        50px;
  --radius-sm:  8px;
  --radius-md:  12px;
  --radius-lg:  16px;
  --radius-full: 9999px;
}
```

**模块布局：**
```css
.module {
  min-height: 100dvh;       /* 回退：100vh */
  scroll-snap-align: start;
  padding: var(--space-16) var(--space-6);
  padding-top: calc(var(--nav-height) + var(--space-12));
}
.module-content {
  max-width: var(--content-width);
  margin: 0 auto;
}
```

---

## 阴影与深度

```css
:root {
  --shadow-sm:  0 1px 2px rgba(44, 42, 40, 0.05);
  --shadow-md:  0 4px 12px rgba(44, 42, 40, 0.08);
  --shadow-lg:  0 8px 24px rgba(44, 42, 40, 0.1);
  --shadow-xl:  0 16px 48px rgba(44, 42, 40, 0.12);
}
```

使用温暖色调的 RGBA（44, 42, 40）— 绝不使用纯黑色阴影。

---

## 动画与过渡

```css
:root {
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --duration-fast:   150ms;
  --duration-normal: 300ms;
  --duration-slow:   500ms;
  --stagger-delay:   120ms;
}
```

**滚动触发显示模式：**
```css
.animate-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity var(--duration-slow) var(--ease-out),
              transform var(--duration-slow) var(--ease-out);
}
.animate-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* 子元素交错显示 */
.stagger-children > .animate-in {
  transition-delay: calc(var(--stagger-index, 0) * var(--stagger-delay));
}
```

**交错的 JS 设置：**
```javascript
document.querySelectorAll('.stagger-children').forEach(parent => {
  Array.from(parent.children).forEach((child, i) => {
    child.style.setProperty('--stagger-index', i);
  });
});
```

**Intersection Observer（触发显示）：**
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target); // 只动画一次
    }
  });
}, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });

document.querySelectorAll('.animate-in').forEach(el => observer.observe(el));
```

---

## 导航与进度

**HTML 结构：**
```html
<nav class="nav">
  <div class="progress-bar" role="progressbar" aria-valuenow="0"></div>
  <div class="nav-inner">
    <span class="nav-title">课程标题</span>
    <div class="nav-dots">
      <button class="nav-dot" data-target="module-1" data-tooltip="模块 1 名称"
              role="tab" aria-label="模块 1"></button>
      <!-- 每个模块一个 -->
    </div>
  </div>
</nav>
```

**进度条（尽可能只用 CSS，JS 回退）：**
```javascript
function updateProgressBar() {
  const scrollTop = window.scrollY;
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (scrollTop / scrollHeight) * 100;
  progressBar.style.width = progress + '%';
}
window.addEventListener('scroll', () => {
  requestAnimationFrame(updateProgressBar);
}, { passive: true });
```

**导航点状态：**
- 默认：`border: 2px solid var(--color-text-muted)`，空心
- 当前：`border-color: var(--color-accent)`，实心中心，微妙发光阴影
- 已访问：`background: var(--color-accent)`，实心填充

**键盘导航：**
```javascript
document.addEventListener('keydown', (e) => {
  if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { nextModule(); e.preventDefault(); }
  if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { prevModule(); e.preventDefault(); }
});
```

---

## 模块结构

**每个模块的 HTML 模板：**
```html
<section class="module" id="module-N" style="background: var(--color-bg or --color-bg-warm)">
  <div class="module-content">
    <header class="module-header animate-in">
      <span class="module-number">0N</span>
      <h1 class="module-title">模块标题</h1>
      <p class="module-subtitle">此模块教授内容的一句话描述</p>
    </header>

    <div class="module-body">
      <section class="screen animate-in">
        <h2 class="screen-heading">屏幕标题</h2>
        <p>内容...</p>
        <!-- 交互元素、代码翻译等 -->
      </section>

      <section class="screen animate-in">
        <!-- 下一个屏幕 -->
      </section>
    </div>
  </div>
</section>
```

---

## 响应式断点

```css
/* 平板 */
@media (max-width: 768px) {
  :root {
    --text-4xl: 1.875rem;
    --text-5xl: 2.25rem;
    --text-6xl: 3rem;
  }
  .translation-block { grid-template-columns: 1fr; } /* 堆叠代码/英语 */
  .pattern-cards { grid-template-columns: 1fr 1fr; }
}

/* 手机 */
@media (max-width: 480px) {
  :root {
    --text-4xl: 1.5rem;
    --text-5xl: 1.875rem;
    --text-6xl: 2.25rem;
  }
  .module { padding: var(--space-8) var(--space-4); }
  .pattern-cards { grid-template-columns: 1fr; }
  .flow-steps { flex-direction: column; }
  .flow-arrow { transform: rotate(90deg); }
}
```

---

## 滚动条与背景

```css
/* 自定义滚动条 */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: var(--radius-full);
}

/* 微妙的氛围背景 */
body {
  background: var(--color-bg);
  background-image: radial-gradient(
    ellipse at 20% 50%,
    rgba(217, 79, 48, 0.03) 0%,
    transparent 50%
  );
}

/* 页面滚动设置 */
html {
  scroll-snap-type: y proximity;
  scroll-behavior: smooth;
}
```

---

## 代码块全局设置

课程中的所有代码块 —— 无论是在翻译块内、独立片段还是测验挑战中 —— 必须换行文本，绝不显示水平滚动条。这是教学工具，不是 IDE。

```css
pre, code {
  white-space: pre-wrap;       /* 换行长行 */
  word-break: break-word;      /* 绝对需要时在单词中间断开 */
  overflow-x: hidden;          /* 绝不出现水平滚动条 */
}
/* 隐藏代码容器上的滚动条 */
.translation-code::-webkit-scrollbar,
pre::-webkit-scrollbar {
  display: none;
}
```

代码片段必须是来自真实代码库的**精确副本** — 绝不修改、修剪或简化。相反，从代码中选择自然简短（5-10 行）的部分来很好地说明概念。如果需要更长的块，全部显示 —— 换行 CSS 会处理可读性。

---

## 语法高亮（Catppuccin 风格）

用于深色 `--color-bg-code` 背景上的代码块：

```css
.code-keyword  { color: #CBA6F7; }  /* 紫色 — if、else、return、function */
.code-string   { color: #A6E3A1; }  /* 绿色 — "字符串" */
.code-function { color: #89B4FA; }  /* 蓝色 — 函数名 */
.code-comment  { color: #6C7086; }  /* 柔和灰色 — // 注释 */
.code-number   { color: #FAB387; }  /* 桃色 — 数字 */
.code-property { color: #F9E2AF; }  /* 黄色 — 对象键 */
.code-operator { color: #94E2D5; }  /* 青色 — =、=>、+ 等 */
.code-tag      { color: #F38BA8; }  /* 粉色 — HTML 标签 */
.code-attr     { color: #F9E2AF; }  /* 黄色 — HTML 属性 */
.code-value    { color: #A6E3A1; }  /* 绿色 — 属性值 */
```
