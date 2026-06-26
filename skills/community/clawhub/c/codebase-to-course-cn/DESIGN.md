# 设计系统：Codebase to Course（教育课程风格）

> 温暖、易读、面向非技术用户的交互式课程设计系统

## 1. 视觉主题与氛围

**设计风格定位**：教育出版物风格，温暖亲切，强调可读性与交互性

**整体视觉印象**：
- 浅色温暖的纸张质感背景，像翻阅一本精心设计的教材
- 深色代码块形成强烈对比，突出代码内容
- 朱红色作为主要强调色，活泼但不刺眼

**关键视觉特征**：
- 模块化滚动吸附（scroll-snap）—— 像翻书一样浏览
- 温暖色调的阴影（绝不使用纯黑阴影）
- 大号模块编号作为视觉锚点
- 渐进式动画揭示内容
- Catppuccin 风格的语法高亮

**设计哲学**：
> 这不是 IDE，是教学工具。代码块换行显示，绝不出现水平滚动条。

---

## 2. 色彩调色板与角色

### 背景表面

| 角色 | 颜色值 | 用途 |
|------|--------|------|
| `--color-bg` | `#FAF7F2` | 主背景，温暖的米白色，像旧纸张 |
| `--color-bg-warm` | `#F5F0E8` | 交替模块背景，创造视觉节奏 |
| `--color-bg-code` | `#1E1E2E` | 代码块背景，深靛蓝炭黑 |
| `--color-surface` | `#FFFFFF` | 卡片表面，纯白 |
| `--color-surface-warm` | `#FDF9F3` | 温暖的卡片表面 |

### 文字颜色

| 角色 | 颜色值 | 用途 |
|------|--------|------|
| `--color-text` | `#2C2A28` | 主文字，深炭黑，对眼睛友好 |
| `--color-text-secondary` | `#6B6560` | 次要文字，温暖的灰色 |
| `--color-text-muted` | `#9E9790` | 柔和灰色，用于时间戳、标签 |

### 品牌与强调色

| 角色 | 颜色值 | 用途 |
|------|--------|------|
| `--color-accent` | `#D94F30` | 主强调色，朱红色 |
| `--color-accent-hover` | `#C4432A` | 悬停状态 |
| `--color-accent-light` | `#FDEEE9` | 浅色背景 |
| `--color-accent-muted` | `#E8836C` | 柔和强调 |

**可选强调色方案**：
| 名称 | 主色 | 悬停 | 浅色 | 柔和 |
|------|------|------|------|------|
| 珊瑚 | `#E06B56` | `#C85A47` | `#FDECEA` | `#E89585` |
| 青色 | `#2A7B9B` | `#1F6280` | `#E4F2F7` | `#5A9DB8` |
| 琥珀 | `#D4A843` | `#BF9530` | `#FDF5E0` | `#E0C070` |
| 森林 | `#2D8B55` | `#226B41` | `#E8F5EE` | `#5AAD7A` |

### 状态色

| 角色 | 颜色值 | 浅色背景 |
|------|--------|----------|
| 成功 | `#2D8B55` | `#E8F5EE` |
| 错误 | `#C93B3B` | `#FDE8E8` |
| 信息 | `#2A7B9B` | `#E4F2F7` |

### 角色颜色（用于聊天气泡、图表）

| 角色 | 颜色值 | 名称 |
|------|--------|------|
| Actor 1 | `#D94F30` | 朱红色 |
| Actor 2 | `#2A7B9B` | 青色 |
| Actor 3 | `#7B6DAA` | 柔和梅红色 |
| Actor 4 | `#D4A843` | 金色 |
| Actor 5 | `#2D8B55` | 森林色 |

### 边框与分隔线

| 角色 | 颜色值 |
|------|--------|
| `--color-border` | `#E5DFD6` |
| `--color-border-light` | `#EEEBE5` |

### 语法高亮（Catppuccin 风格）

| 类型 | 颜色值 | 用途 |
|------|--------|------|
| `.code-keyword` | `#CBA6F7` | if, else, return, function |
| `.code-string` | `#A6E3A1` | 字符串 |
| `.code-function` | `#89B4FA` | 函数名 |
| `.code-comment` | `#6C7086` | 注释 |
| `.code-number` | `#FAB387` | 数字 |
| `.code-property` | `#F9E2AF` | 对象键 |
| `.code-operator` | `#94E2D5` | =, =>, + |
| `.code-tag` | `#F38BA8` | HTML 标签 |
| `.code-attr` | `#F9E2AF` | HTML 属性 |
| `.code-value` | `#A6E3A1` | 属性值 |

---

## 3. 字体规则

### 字体族

```css
--font-display: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
--font-body:    'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
--font-mono:    'JetBrains Mono', 'Fira Code', 'Source Code Pro', 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
```

> **注意**：使用系统字体回退，无需外部字体链接，确保中国大陆用户无需翻墙即可正常显示。

### 层级表格

| 角色 | 字体 | 大小 | 字重 | 行高 | 用途 |
|------|------|------|------|------|------|
| 模块编号 | Display | `3.75rem` (60px) | 800 | 1 | 大号背景装饰 |
| 模块标题 | Display | `2.25rem` (36px) | 700 | 1.15 | 主标题 |
| 模块副标题 | Body | `1.125rem` (18px) | 400 | 1.3 | 描述文字 |
| 屏幕标题 | Display | `1.5rem` (24px) | 600 | 1.3 | 子标题 |
| 正文 | Body | `1rem` (16px) | 400 | 1.6 | 段落文字 |
| 引导段落 | Body | `1.125rem` (18px) | 400 | 1.6 | 重要段落 |
| 代码 | Mono | `0.875rem` (14px) | 400 | 1.7 | 代码块 |
| 标签/徽章 | Mono | `0.75rem` (12px) | 400 | - | 大写 + 0.05em 字间距 |

### 类型比例（1.25 比例）

```css
--text-xs:   0.75rem;    /* 12px */
--text-sm:   0.875rem;   /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg:   1.125rem;   /* 18px */
--text-xl:   1.25rem;    /* 20px */
--text-2xl:  1.5rem;     /* 24px */
--text-3xl:  1.875rem;   /* 30px */
--text-4xl:  2.25rem;    /* 36px */
--text-5xl:  3rem;       /* 48px */
--text-6xl:  3.75rem;    /* 60px */
```

---

## 4. 组件样式

### 按钮

**主要按钮**
```css
.btn-primary {
  background: var(--color-accent);
  color: white;
  border: none;
  padding: var(--space-2) var(--space-5);
  border-radius: var(--radius-sm);
  font-weight: 600;
}
.btn-primary:hover {
  background: var(--color-accent-hover);
  transform: translateY(-1px);
}
```

**次要按钮**
```css
.btn {
  background: var(--color-surface);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
  padding: var(--space-2) var(--space-5);
  border-radius: var(--radius-sm);
}
.btn:hover {
  border-color: var(--color-accent-muted);
  color: var(--color-accent);
}
```

### 卡片与容器

**基础卡片**
```css
.pattern-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  border-top: 3px solid var(--color-accent);
}
.pattern-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}
```

**测验容器**
```css
.quiz-container {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  box-shadow: var(--shadow-md);
}
```

**代码翻译块**
```css
.translation-block {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}
.translation-code {
  background: var(--color-bg-code);
  color: #CDD6F4;
  padding: var(--space-6);
}
.translation-english {
  background: var(--color-surface-warm);
  padding: var(--space-6);
  border-left: 3px solid var(--color-accent);
}
```

### 徽章与标签

**代码徽章**
```css
.badge-code {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  background: var(--color-bg-code);
  color: #CBA6F7;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-sm);
}
```

**拖拽芯片**
```css
.dnd-chip {
  background: var(--color-accent);
  color: white;
  border-radius: var(--radius-full);
  padding: var(--space-2) var(--space-4);
  font-weight: 600;
  cursor: grab;
}
```

### 导航

**顶部导航**
```css
.nav {
  position: fixed;
  top: 0;
  height: 50px;
  background: rgba(250,247,242,0.92);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--color-border-light);
}
```

**导航点**
```css
.nav-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid var(--color-text-muted);
  background: transparent;
}
.nav-dot.active {
  border-color: var(--color-accent);
  background: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}
.nav-dot.visited {
  border-color: var(--color-accent-muted);
  background: var(--color-accent-muted);
}
```

### 提示框（Callout）

```css
.callout {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-5);
  border-radius: var(--radius-md);
  border-left: 4px solid;
}
.callout-accent  { background: var(--color-accent-light);  border-color: var(--color-accent); }
.callout-info    { background: var(--color-info-light);    border-color: var(--color-info); }
.callout-warning { background: var(--color-error-light);   border-color: var(--color-error); }
```

---

## 5. 布局原则

### 间距系统

```css
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
```

### 网格与容器

```css
--content-width:      800px;   /* 标准阅读宽度 */
--content-width-wide: 1000px;  /* 用于并排布局 */
--nav-height:         50px;
```

### 模块布局

```css
.module {
  min-height: 100dvh;
  scroll-snap-align: start;
  padding: var(--space-16) var(--space-6);
  padding-top: calc(var(--nav-height) + var(--space-12));
}
.module-content {
  max-width: var(--content-width);
  margin: 0 auto;
}
```

### 圆角刻度

| 名称 | 值 | 用途 |
|------|------|------|
| `--radius-sm` | `8px` | 按钮、标签、输入框 |
| `--radius-md` | `12px` | 卡片、容器 |
| `--radius-lg` | `16px` | 大型容器、模态框 |
| `--radius-full` | `9999px` | 胶囊形状、头像 |

---

## 6. 深度与层级

### 阴影系统

| 级别 | 值 | 用途 |
|------|-----|------|
| `--shadow-sm` | `0 1px 2px rgba(44,42,40,0.05)` | 微妙提升 |
| `--shadow-md` | `0 4px 12px rgba(44,42,40,0.08)` | 卡片、容器 |
| `--shadow-lg` | `0 8px 24px rgba(44,42,40,0.10)` | 浮动元素 |
| `--shadow-xl` | `0 16px 48px rgba(44,42,40,0.12)` | 模态框 |

**阴影哲学**：使用温暖色调的 RGBA（44, 42, 40），绝不使用纯黑色阴影。

### 层级处理

| 级别 | 处理方式 | 用途 |
|------|----------|------|
| Flat | 无阴影 | 页面背景 |
| Subtle | shadow-sm | 标签、小卡片 |
| Elevated | shadow-md | 交互卡片、测验 |
| Floating | shadow-lg/xl | 提示框、模态 |

---

## 7. 宜与忌

### 宜

- 偶数模块使用 `--color-bg`，奇数模块使用 `--color-bg-warm`（交替背景创造视觉节奏）
- 代码块始终使用 `--color-bg-code` 配浅色文本
- 使用滚动吸附（scroll-snap）让用户逐模块浏览
- 使用 `animate-in` 类实现滚动触发的淡入动画
- 使用温暖色调的阴影
- 代码换行显示，绝不出现水平滚动条
- 从真实代码库中选择简短片段（5-10 行）

### 忌

- 绝不使用纯黑色阴影
- 绝不使用紫色渐变作为主色调
- 绝不修改、修剪或简化代码片段
- 绝不在代码块中显示水平滚动条
- 避免模块之间没有视觉区分
- 避免使用过于鲜艳的颜色

---

## 8. 响应式行为

### 断点表格

| 名称 | 宽度 | 关键变化 |
|------|------|----------|
| Tablet | ≤768px | 标题尺寸缩小，代码/英语堆叠显示 |
| Mobile | ≤480px | 进一步缩小标题，单列卡片，垂直流程图 |

### 断点样式

**平板 (≤768px)**
```css
:root {
  --text-4xl: 1.875rem;
  --text-5xl: 2.25rem;
  --text-6xl: 3rem;
}
.translation-block { grid-template-columns: 1fr; }
.pattern-cards { grid-template-columns: 1fr 1fr; }
```

**手机 (≤480px)**
```css
:root {
  --text-4xl: 1.5rem;
  --text-5xl: 1.875rem;
  --text-6xl: 2.25rem;
}
.module { padding: var(--space-8) var(--space-4); }
.pattern-cards { grid-template-columns: 1fr; }
.flow-steps { flex-direction: column; }
.flow-arrow { transform: rotate(90deg); }
```

---

## 9. Agent 提示指南

### 快速颜色参考

```
主背景:     #FAF7F2
主文字:     #2C2A28
强调色:     #D94F30
代码背景:   #1E1E2E
边框:       #E5DFD6
```

### 动画与过渡

```css
--ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
--duration-fast:   150ms;
--duration-normal: 300ms;
--duration-slow:   500ms;
--stagger-delay:   120ms;
```

### 滚动动画

```css
.animate-in {
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity var(--duration-slow) var(--ease-out),
    transform var(--duration-slow) var(--ease-out);
}
.animate-in.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### 模块 HTML 模板

```html
<section class="module" id="module-N" style="background: var(--color-bg)">
  <div class="module-content">
    <header class="module-header animate-in">
      <span class="module-number">0N</span>
      <h1 class="module-title">模块标题</h1>
      <p class="module-subtitle">一句话描述</p>
    </header>
    <div class="module-body">
      <!-- 内容 -->
    </div>
  </div>
</section>
```

### 滚动吸附设置

```css
html {
  scroll-snap-type: y proximity;
  scroll-behavior: smooth;
}
```

### 自定义滚动条

```css
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: var(--radius-full);
}
```
