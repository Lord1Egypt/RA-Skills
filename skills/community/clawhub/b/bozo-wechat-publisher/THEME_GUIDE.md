# bozo-wechat-publisher 主题使用指南

## 📋 概述

bozo-wechat-publisher 现在支持两种类型的主题：
1. **wenyan-cli 内置主题**（8 种）
2. **自定义卡片式主题**（2 种新增）

---

## 🎨 主题列表

### 内置主题（wenyan-cli）

| 主题 ID | 名称 | 风格描述 |
|---------|------|----------|
| `default` | 默认主题 | 经典布局，适合长文阅读 |
| `lapis` | 青金石 | 极简清凉蓝色调 |
| `phycat` | 物理猫 | 薄荷绿，清晰结构 |
| `orangeheart` | 橙心 | 温暖橙色调，充满活力 |
| `rainbow` | 彩虹 | 色彩丰富，布局清晰 |
| `pie` | 派派风格 | 现代时尚，类似少数派 |
| `maize` | 玉米色 | 清爽浅色调，柔和玉米色 |
| `purple` | 紫色 | 极简主义，淡紫色强调 |

### 自定义卡片式主题

| 主题 ID | 名称 | 风格描述 | 适用场景 |
|---------|------|----------|----------|
| `card-tech-dark` | 卡片科技暗色 | 深色科技感，渐变强调色 | 技术文章、AI 内容、开发教程 |
| `card-neon-light` | 卡片霓虹浅色 | 浅色霓虹风格，清新现代 | 教程、指南、操作手册 |

---

## 🚀 快速开始

### 查看所有可用主题

```bash
# 使用主题切换脚本
./scripts/use-theme.sh list
```

### 查看主题详情

```bash
./scripts/use-theme.sh info card-tech-dark
./scripts/use-theme.sh info card-neon-light
```

### 使用内置主题发布

```bash
# 使用 lapis 主题发布
wenyan publish -f article.md -t lapis

# 使用 phycat 主题 + solarized-light 代码高亮
wenyan publish -f article.md -t phycat -h solarized-light
```

### 使用自定义卡片主题

**方式一：直接使用 HTML 模板**

```bash
# 1. 构建基础 HTML
wenyan build -f article.md -t default

# 2. 注入自定义主题样式（手动编辑生成的 HTML）
# 或者使用自定义主题模板直接替换
```

**方式二：在 Markdown 中使用卡片语法**

自定义主题支持特殊的卡片语法：

\`\`\`markdown
##::card
### 卡片标题

这是卡片内容，可以包含列表、代码块等。

- 要点一
- 要点二
- 要点三

\`\`\`javascript
console.log("代码示例");
\`\`\`

##::end
\`\`\`

---

## 🎴 自定义主题特性

### card-tech-dark（卡片科技暗色）

**配色方案：**
- 背景色：`#0a0e27`（深空蓝黑）
- 强调色：`#6366f1` → `#8b5cf6`（紫色渐变）
- 文字色：`#f1f5f9`（浅灰白）

**布局组件：**
- 📦 卡片容器（带悬停效果）
- 📋 列表卡片（带图标）
- 🎯 功能网格（2x2 布局）
- 💻 代码块（深色背景）
- 💬 引用块（左侧强调线）
- ⚠️ 提示框（info/success/warning）

### card-neon-light（卡片霓虹浅色）

**配色方案：**
- 背景色：`#f8fafc`（浅灰白）
- 强调色：`#06b6d4` → `#8b5cf6`（青色到紫色渐变）
- 文字色：`#1e293b`（深灰）

**布局组件：**
- 📦 卡片容器（带霓虹发光效果）
- 📋 列表卡片（渐变背景）
- 🎯 功能网格（悬停浮起效果）
- 💻 代码块（浅色背景）
- 💬 引用块（渐变左侧强调）
- ⚠️ 提示框（彩色边框）

---

## 📁 文件结构

```
bozo-wechat-publisher/
├── themes/
│   ├── theme-config.json      # 主题配置文件
│   ├── card-tech-dark.html    # 科技暗色主题模板
│   └── card-neon-light.html   # 霓虹浅色主题模板
├── scripts/
│   ├── use-theme.sh           # 主题切换脚本 ⭐
│   └── publish-curl.sh        # curl 备用方案
└── SKILL.md                   # 技能主文档
```

---

## 🔧 主题切换脚本

`scripts/use-theme.sh` 提供以下功能：

```bash
# 列出所有主题
./scripts/use-theme.sh list

# 查看主题详情
./scripts/use-theme.sh info <theme_id>

# 应用主题到文章
./scripts/use-theme.sh apply <markdown_file> <theme_id>

# 显示帮助
./scripts/use-theme.sh help
```

---

## 💡 使用建议

### 场景推荐

| 内容类型 | 推荐主题 | 理由 |
|----------|----------|------|
| 技术教程 | `card-tech-dark` | 深色背景，代码高亮效果好 |
| AI 相关 | `card-tech-dark` | 科技感强，符合 AI 调性 |
| 操作指南 | `card-neon-light` | 浅色清晰，步骤分明 |
| 产品介绍 | `lapis` | 简洁专业，适合商务 |
| 个人博客 | `phycat` | 薄荷绿清新，阅读舒适 |
| 新闻资讯 | `default` | 经典布局，信息密度高 |

### 组合建议

**技术文章组合：**
- 主题：`card-tech-dark`
- 代码高亮：`dracula` 或 `monokai`
- Mac 风格代码块：开启

**教程组合：**
- 主题：`card-neon-light`
- 代码高亮：`github`
- Mac 风格代码块：关闭

---

## 🎯 高级用法

### 创建自己的主题

1. 复制现有主题模板：
```bash
cp themes/card-tech-dark.html themes/my-custom-theme.html
```

2. 编辑 CSS 变量（`:root` 部分）：
```css
:root {
    --bg-primary: #your_color;
    --accent-primary: #your_color;
    /* ... */
}
```

3. 在 `theme-config.json` 中注册你的主题。

### 响应式设计

所有主题都支持移动端响应式布局：
- 最大宽度：768px
- 自动调整字号和间距
- 优化触摸目标大小

---

## 📝 更新日志

### v1.3.0 (2026-04-04)

- ✅ 新增自定义卡片式主题系统
- ✅ 添加 2 种自定义主题（card-tech-dark、card-neon-light）
- ✅ 创建主题切换脚本 `use-theme.sh`
- ✅ 添加主题配置文件 `theme-config.json`
- ✅ 更新 SKILL.md 文档

---

## 🤝 贡献

欢迎创建更多自定义主题！遵循以下步骤：

1. 在 `themes/` 目录创建新的 `.html` 文件
2. 在 `theme-config.json` 中注册
3. 更新 SKILL.md 文档
4. 测试发布效果

---

## 📞 反馈

如有问题或建议，请通过以下方式反馈：
- 在技能目录创建 issue
- 直接修改并测试

---

*最后更新：2026-04-04*
