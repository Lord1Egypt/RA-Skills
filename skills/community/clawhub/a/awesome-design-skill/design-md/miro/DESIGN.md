# 设计系统：Miro

## 1. 视觉主题与氛围

Miro 的网站是一个简洁、以协作工具为核心的平台，通过充裕的留白、柔和的强调色和自信的几何字体传达"可视化思维"理念。设计采用以白色为主的画布，搭配接近黑色的文字（`#1c1c1e`）和独特的柔和色调色板 —— coral、rose、teal、orange、yellow、moss —— 每种颜色代表不同的协作场景。

字体方面，使用 Roobert PRO Medium 作为主要展示字体，搭配 OpenType 字符变体（`"blwf", "cv03", "cv04", "cv09", "cv11"`）和负字间距（56px 时为 -1.68px）。Noto Sans 负责正文文本，使用其特有的样式集（`"liga" 0, "ss01", "ss04", "ss05"`）。该设计使用 Framer 构建，具有流畅的动画和现代组件模式。

**核心特征：**
- 白色画布搭配接近黑色（`#1c1c1e`）的文字
- Roobert PRO Medium 搭配多种 OpenType 字符变体
- 柔和强调色调色板：coral、rose、teal、orange、yellow、moss（浅色/深色配对）
- Blue 450（`#5b76fe`）作为主要交互色
- Success 绿色（`#00b473`）用于正向状态
- 宽泛的圆角范围：8px–50px
- 使用 Framer 构建，具有流畅的动效模式
- Ring shadow 边框：`rgb(224,226,232) 0px 0px 0px 1px`

## 2. 色彩色板与角色

### 主色
- **Near Black**（`#1c1c1e`）：主要文字
- **White**（`#ffffff`）：`--tw-color-white`，主要背景
- **Blue 450**（`#5b76fe`）：`--tw-color-blue-450`，主要交互色
- **Actionable Pressed**（`#2a41b6`）：`--tw-color-actionable-pressed`

### 柔和强调色（浅色/深色配对）
- **Coral**：浅色 `#ffc6c6` / 深色 `#600000`
- **Rose**：浅色 `#ffd8f4` / 深色（隐含）
- **Teal**：浅色 `#c3faf5` / 深色 `#187574`
- **Orange**：浅色 `#ffe6cd`
- **Yellow**：深色 `#746019`
- **Moss**：深色 `#187574`
- **Pink**（`#fde0f0`）：柔和粉色背景
- **Red**（`#fbd4d4`）：浅红色背景
- **Dark Red**（`#e3c5c5`）：暗淡红色

### 语义色
- **Success**（`#00b473`）：`--tw-color-success-accent`

### 中性色
- **Slate**（`#555a6a`）：次要文字
- **Input Placeholder**（`#a5a8b5`）：`--tw-color-input-placeholder`
- **Border**（`#c7cad5`）：按钮边框
- **Ring**（`rgb(224,226,232)`）：阴影边框

## 3. 字体排版规则

### 字体族
- **Display**：`Roobert PRO Medium`，备用字体：Placeholder — `"blwf", "cv03", "cv04", "cv09", "cv11"`
- **Display 变体**：`Roobert PRO SemiBold`、`Roobert PRO SemiBold Italic`、`Roobert PRO`
- **Body**：`Noto Sans` — `"liga" 0, "ss01", "ss04", "ss05"`

### 层级结构

| 角色 | 字体 | 字号 | 字重 | 行高 | 字间距 |
|------|------|------|------|------|--------|
| Display Hero | Roobert PRO Medium | 56px | 400 | 1.15 | -1.68px |
| Section Heading | Roobert PRO Medium | 48px | 400 | 1.15 | -1.44px |
| Card Title | Roobert PRO Medium | 24px | 400 | 1.15 | -0.72px |
| Sub-heading | Noto Sans | 22px | 400 | 1.35 | -0.44px |
| Feature | Roobert PRO Medium | 18px | 600 | 1.35 | normal |
| Body | Noto Sans | 18px | 400 | 1.45 | normal |
| Body Standard | Noto Sans | 16px | 400–600 | 1.50 | -0.16px |
| Button | Roobert PRO Medium | 17.5px | 700 | 1.29 | 0.175px |
| Caption | Roobert PRO Medium | 14px | 400 | 1.71 | normal |
| Small | Roobert PRO Medium | 12px | 400 | 1.15 | -0.36px |
| Micro Uppercase | Roobert PRO | 10.5px | 400 | 0.90 | uppercase |

## 4. 组件样式

### 按钮
- Outlined（描边按钮）：透明背景，`1px solid #c7cad5`，8px 圆角，7px 12px 内边距
- White circle（白色圆形按钮）：50% 圆角，白色背景带阴影
- Blue primary（蓝色主要按钮）：由交互色推导

### 卡片：12px–24px 圆角，柔和色调背景
### 输入框：白色背景，`1px solid #e9eaef`，8px 圆角，16px 内边距

## 5. 布局原则
- 间距：1–24px 基础比例
- 圆角：8px（按钮）、10px–12px（卡片）、20px–24px（面板）、40px–50px（大型容器）
- Ring shadow：`rgb(224,226,232) 0px 0px 0px 1px`

## 6. 深度与层次
极简风格 —— ring shadow + 柔和背景对比

## 7. 最佳实践
### 推荐做法
- 在功能区块中使用柔和的浅色/深色配对
- 应用 Roobert PRO 搭配 OpenType 字符变体
- 使用 Blue 450（#5b76fe）作为交互元素颜色
### 避免做法
- 不要使用厚重的阴影
- 同一区块内不要混合超过 2 种柔和强调色

## 8. 响应式行为
断点：425px、576px、768px、896px、1024px、1200px、1280px、1366px、1700px、1920px

## 9. Agent 提示指南
### 快速颜色参考
- 文字：Near Black（`#1c1c1e`）
- 背景：White（`#ffffff`）
- 交互：Blue 450（`#5b76fe`）
- 成功：`#00b473`
- 边框：`#c7cad5`
### 示例组件提示
- "创建 hero 区块：白色背景。Roobert PRO Medium 56px，行高 1.15，字间距 -1.68px。蓝色 CTA（#5b76fe）。描边次要按钮（1px solid #c7cad5，8px 圆角）。"
