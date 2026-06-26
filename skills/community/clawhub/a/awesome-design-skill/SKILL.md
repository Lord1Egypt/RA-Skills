---
name: awesome-design-skill
description: UI设计风格选择器，从design-md风格库中选择合适的设计系统作为UI开发指导。支持50+知名品牌设计风格（Linear、Apple、Stripe、Vercel等）。**触发条件：用户必须明确指定设计风格**（如"用Linear风格设计"、"使用Apple风格创建页面"、"按Stripe风格重构"）。也用于用户询问可用设计风格列表（"列出所有风格"、"有哪些风格"）或查看特定风格详情（"看看Vercel风格"）。**不触发：用户未指定风格的一般设计请求**（如"设计一个页面"、"创建UI"等不会触发此技能）。
---

# Awesome Design Skill

根据用户指定的设计风格，从 design-md 风格库中选择对应的设计系统作为 UI 开发指导，并将 DESIGN.md 复制到当前工作目录。

**重要：此技能仅在用户明确指定设计风格时触发。如果用户未指定风格，不要使用此技能。**

## 字体说明

所有设计风格的预览文件（preview.html、preview-dark.html）使用 **fonts.loli.net** 作为 Google Fonts 的镜像源，以优化中国大陆地区的访问体验。如需更换为其他字体源，可批量替换文件中的 `fonts.loli.net` 为其他镜像地址。

## 自定义设计风格

**design-md 目录中的内容可以自由添加或替换。** 你可以：

- 添加自己喜欢的设计风格（只需在 `design-md/` 目录下创建新的风格文件夹和 DESIGN.md）
- 替换现有风格的 DESIGN.md 内容
- 删除不需要的风格

这样你可以构建属于自己的设计风格库，让 Claude 使用你熟悉和偏好的设计系统。

## 脚本文件

| 脚本 | 用途 |
|-----|------|
| `scripts/list-styles.sh` | 列出所有可用的设计风格 |
| `scripts/smart-select.sh [需求描述]` | 智能选择设计风格（根据需求关键词匹配，无匹配则随机） |
| `scripts/random-style.sh` | 随机选择一个设计风格 |
| `scripts/get-design.sh <风格名称>` | 获取指定风格的 DESIGN.md 路径 |
| `scripts/copy-design.sh <风格名称> [目标目录]` | 复制 DESIGN.md 到指定目录（默认当前目录） |

## 工作流程

### 用户指定风格进行设计

**前提：用户必须明确指定风格名称**

1. 运行 `scripts/get-design.sh <风格名称>` 验证风格存在并获取路径
2. 运行 `scripts/copy-design.sh <风格名称>` 复制 DESIGN.md 到当前目录
3. 读取当前目录的 DESIGN.md 作为风格指导
4. 告知用户使用的设计风格

### 用户查看可用风格

当用户询问"有哪些风格"、"列出所有风格"、"查看可用设计风格"时：

运行 `scripts/list-styles.sh` 列出所有可用的设计风格，并展示给用户。

### 用户查看特定风格详情

当用户询问"看看XX风格"、"查看XX风格的设计规范"时：

1. 运行 `scripts/get-design.sh <风格名称>` 获取风格路径
2. 读取并展示该风格的设计规范概要

### 用户重构现有页面（需指定风格）

**前提：用户必须明确指定目标风格**

当用户要求将现有页面改为某种风格时（如"将index.html改为airbnb的风格"、"用Vercel风格重构这个页面"）：

1. 首先读取用户指定的现有页面文件，理解其当前结构和内容
2. 运行 `scripts/get-design.sh <目标风格>` 验证风格存在
3. 运行 `scripts/copy-design.sh <目标风格>` 复制到当前目录
4. 读取 DESIGN.md 作为风格指导
5. 根据新风格的设计系统，重构页面的：
   - 颜色方案（背景、文字、强调色等）
   - 字体排版（字体家族、字号、行高等）
   - 间距系统（边距、内边距、元素间距）
   - 阴影和圆角
   - 组件样式（按钮、卡片、表单等）
   - 动画效果
6. 保持页面原有的功能和内容结构，仅改变视觉风格
7. 告知用户重构完成及主要变化

## 可用设计风格关键词

用户指定风格时可以使用以下关键词：

| 风格名称 | 适用场景 |
|---------|---------|
| linear.app | 项目管理、任务工具、深色主题 |
| apple | 产品展示、高端简洁、消费电子 |
| stripe | 支付、金融科技、企业级 |
| vercel | 开发者工具、深色主题 |
| spotify | 音乐、媒体播放器 |
| notion | 协作、文档工具 |
| figma | 设计工具、创意平台 |
| airbnb | 旅行、预订、民宿 |
| coinbase | 加密货币、区块链 |
| claude | AI产品、对话界面 |
| cursor | 开发者工具、代码编辑器 |
| posthog | 数据分析、监控仪表板 |
| framer | 设计工具、创意平台 |

...以及更多风格，使用 `scripts/list-styles.sh` 查看完整列表。

## DESIGN.md 文件结构

每个 DESIGN.md 包含：
- Overview - 设计概述
- Colors - 颜色系统
- Typography - 字体排版
- Spacing - 间距系统
- Shadows - 阴影效果
- Border Radius - 圆角设置
- Components - 组件样式
- Animations - 动画效果

## 输出格式

完成设计后，告知用户：
1. 使用的设计风格名称
2. 主要设计特点概述
3. 生成的文件列表
