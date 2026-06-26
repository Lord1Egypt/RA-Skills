# SVG 分层架构图规范

本规范用于产出高质量、现代风格的分层架构 SVG，无需外部渲染，直接编写 SVG 代码。

## 适用场景
- 需要精确控制布局、配色、字体
- 产出文件需离线可用、无外部依赖
- 分层展示系统架构（用户入口 → 业务逻辑 → 服务 → 数据层等）

## 画布与基础结构

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="700" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <!-- 箭头标记 -->
        <marker id="arrowhead" markerWidth="6" markerHeight="5" refX="6" refY="2.5" orient="auto">
            <polygon points="0 0, 6 2.5, 0 5" fill="#94a3b8"/>
        </marker>
    </defs>
    <!-- 背景 -->
    <rect width="100%" height="100%" fill="#f8fafc"/>
    <!-- 标题 -->
    <text x="500" y="40" text-anchor="middle" font-size="22" font-weight="600" fill="#1e293b" font-family="system-ui, -apple-system, sans-serif">架构图标题</text>
    <!-- 层级内容 -->
    ...
    <!-- 图例 -->
    ...
</svg>
```

## 配色风格（12 种可选）

### 模板清单

| 风格 | 模板文件 | 类型 |
|------|----------|------|
| tailwind | `layered-arch-template.svg` | 通用骨架 |
| cyber | `template-cyber.svg` | 骨架模板 |
| gray | `template-gray.svg` | 骨架模板 |
| green | `template-green.svg` | 骨架模板 |
| mono | `template-mono.svg` | 骨架模板 |
| morandi | `template-morandi.svg` | 骨架模板 |
| ocean | `template-ocean.svg` | 骨架模板 |
| orange | `template-orange.svg` | 骨架模板 |
| purple | `template-purple.svg` | 骨架模板 |
| blue | `ecommerce-architecture-blue.svg` | 完整示例 |
| dark | `ecommerce-architecture-dark.svg` | 完整示例 |
| handdrawn | `ecommerce-architecture-handdrawn.svg` | 完整示例 |

- **骨架模板**：4层×4模块的简化结构，快速套用风格
- **完整示例**：6层电商架构，展示复杂场景的排版参考

### 1. Blue（深蓝商务风）
适合：企业级、正式场景
- 背景：`#ffffff`
- 层级渐变：`#1a1a2e` → `#16213e` → `#0f3460`（从深到中）
- 数据层：白底 + `#e94560` 边框（强调色）
- 基础设施层：`#f5f5f5` + 灰边框
- 文字：白字在深色层，深色在浅色层

### 2. Cyber（赛博朋克）
适合：科技感、未来感、演示
- 背景：`#0a0a0f`（近黑）
- 层级边框：霓虹色 `#00d4ff`（cyan）、`#7b2ff7`（紫）、`#f72585`（品红）、`#4cc9f0`（亮蓝）
- 填充：`#12121a`（深灰）
- 支持 `<linearGradient>` 标题渐变
- 文字：霓虹色与浅色

### 3. Dark（GitHub Dark 主题）
适合：开发者、深色模式
- 背景：`#0d1117`
- 层级容器：`#161b22`
- 子模块：`#21262d`
- 边框色系：`#30363d`（灰）、`#238636`（绿）、`#8957e5`（紫）、`#f78166`（橙）、`#388bfd`（蓝）、`#da3633`（红）
- 文字：`#c9d1d9`（正文）、彩色标题

### 4. Gray（简约灰阶）
适合：文档嵌入、简洁正式
- 背景：`#ffffff`
- 层级渐变：`#1f2937` → `#374151` → `#4b5563`（灰阶）
- 数据层：白底 + `#6b7280` 边框
- 基础设施层：`#f3f4f6` + `#d1d5db` 边框
- 文字：白字在深色层

### 5. Green（森林绿）
适合：环保、健康、自然主题
- 背景：`#ffffff`
- 层级渐变：`#1b4332` → `#2d6a4f` → `#40916c`
- 数据层：`#d8f3dc` + `#52b788` 边框
- 基础设施层：`#f5f5f5`
- 文字：白字在深色层，`#1b4332` 在浅色层

### 6. Handdrawn（手绘风格）
适合：演示草稿、创意讨论、非正式场景
- 背景：`#fdfbf7`（米白）
- 使用 SVG `<filter>` 制作手绘笔触效果
- 手写字体：`'Wawati SC', 'Ma Shan Zheng', cursive`
- 使用 `<path>` 绘制不规则边框
- 文字加 `transform="rotate(±0.x)"` 微倾斜
- 每层不同浅色背景：`#fff8f0`、`#f5fff5`、`#f8f5ff`、`#fff5f8`、`#fdfdf5`、`#f5fafa`

### 7. Mono（极简黑白）
适合：打印、黑白文档、极简风格
- 背景：`#ffffff`
- 层级渐变：`#000000` → `#222222` → `#444444` → `#666666`
- 数据层：`#f0f0f0` + 黑边框
- 基础设施层：`#e5e5e5` + 黑边框
- **直角无圆角**：`rx="0"`
- 文字：黑白对比

### 8. Morandi（莫兰迪色调）
适合：设计感、复古、低饱和度偏好
- 背景：`#f5f0eb`（暖灰）
- 层级色系（低饱和度）：
  - `#8d9a9e`（灰蓝）
  - `#a4b4a0`（灰绿）
  - `#c4a589`（灰棕）
  - `#c9a9a6`（灰粉）
  - `#e0d5cb`（米色）
  - `#9a8f97`（灰紫）
- 子模块：`rgba(255,255,255,0.15)` 半透明
- 文字：白字在深色层，`#5d5d5d` 在浅色层

### 9. Ocean（海洋蓝绿）
适合：清新、数据可视化、科技
- 背景：`#e8f4f8`（浅蓝）
- 层级渐变：`#0369a1` → `#0891b2` → `#14b8a6`（蓝到青绿）
- 子模块：`#0284c7`、`#06b6d4`、`#2dd4bf`
- 数据层：`#f0fdfa` + `#5eead4` 边框
- 基础设施层：`#cffafe` + `#7dd3fc` 边框
- 文字：白字在深色层，`#0f766e` 在浅色层

### 10. Orange（暖橙色调）
适合：活力、热情、营销主题
- 背景：`#ffffff`
- 层级渐变：`#7c2d12` → `#c2410c` → `#ea580c`
- 数据层：`#fff7ed` + `#f97316` 边框
- 基础设施层：`#f5f5f5`
- 文字：白字在深色层，`#7c2d12` 在浅色层

### 11. Purple（紫色调）
适合：创意、高端、神秘感
- 背景：`#ffffff`
- 层级渐变：`#2d1b69` → `#4a3298` → `#6b4dc4`
- 数据层：`#f3e8ff` + `#9d4edd` 边框
- 基础设施层：`#f5f5f5`
- 文字：白字在深色层，`#2d1b69` 在浅色层

### Tailwind（经典多色）
适合：层级多、需要色彩区分度

| 用途 | 背景色 | 边框色 | 文字色 | 说明 |
|------|--------|--------|--------|------|
| 用户入口层 | `#fef3c7` | `#f59e0b` | `#b45309` | Amber |
| 入口层子块 | `#fde68a` | `#f59e0b` | `#92400e` | Amber 浅 |
| 业务逻辑层 | `#dbeafe` | `#3b82f6` | `#1d4ed8` | Blue |
| 业务层子块 | `#bfdbfe` | `#3b82f6` | `#1e40af` | Blue 浅 |
| 插件/能力层 | `#dcfce7` | `#22c55e` | `#15803d` | Green |
| 能力层子块 | `#bbf7d0` | `#22c55e` | `#166534` | Green 浅 |
| 服务/数据层 | `#f3e8ff` | `#a855f7` | `#7e22ce` | Purple |
| 连线/标注 | — | `#94a3b8` | `#94a3b8` | Slate |

层数按需确定，不固定；多层级时从上述色系中按顺序选取，保证相邻层色彩区分度。

## 风格速查表

| 风格 | 背景 | 主色调 | 圆角 | 适用场景 |
|------|------|--------|------|----------|
| blue | 白 | 深蓝渐变 | rx=4 | 企业正式 |
| cyber | 黑 | 霓虹多彩 | rx=4 | 科技演示 |
| dark | 深灰 | GitHub 色系 | rx=4 | 开发者 |
| gray | 白 | 灰阶 | rx=4 | 简洁文档 |
| green | 白 | 森林绿 | rx=4 | 自然环保 |
| handdrawn | 米白 | 多彩手绘 | 不规则 | 草稿创意 |
| mono | 白 | 纯黑白 | rx=0 | 打印极简 |
| morandi | 暖灰 | 低饱和度 | rx=4 | 设计复古 |
| ocean | 浅蓝 | 蓝绿渐变 | rx=4 | 清新科技 |
| orange | 白 | 暖橙渐变 | rx=4 | 活力营销 |
| purple | 白 | 紫色渐变 | rx=4 | 创意高端 |
| tailwind | 白 | 多色区分 | rx=6/12 | 层级多 |

## 层级布局模式

```
┌─────────────────────────────────────────────────────────────┐  ← 层级容器 (rx=12, filter=shadow)
│  [层级标题]                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │  ← 子模块 (rx=6)
│  │ 模块A    │  │ 模块B    │  │ 模块C    │  │ 模块D    │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────┘
                              ↓ (箭头连线带标注)
┌─────────────────────────────────────────────────────────────┐
│  [下一层级]                                                  │
│  ...                                                         │
└─────────────────────────────────────────────────────────────┘
```

### 层级容器
```svg
<g transform="translate(80, 70)">
    <rect x="0" y="0" width="840" height="90" rx="12" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5" filter="url(#shadow)"/>
    <text x="20" y="26" font-size="14" font-weight="600" fill="#b45309" font-family="system-ui">层级名称</text>
    <!-- 子模块 -->
</g>
```

### 子模块
```svg
<g transform="translate(30, 40)">
    <rect width="180" height="40" rx="6" fill="#fde68a" stroke="#f59e0b" stroke-width="1"/>
    <text x="90" y="25" text-anchor="middle" font-size="13" fill="#92400e" font-family="system-ui">模块名称</text>
</g>
```

### 带副标题的子模块
```svg
<g transform="translate(30, 45)">
    <rect width="380" height="45" rx="6" fill="#bfdbfe" stroke="#3b82f6" stroke-width="1"/>
    <text x="190" y="22" text-anchor="middle" font-size="14" font-weight="500" fill="#1e40af" font-family="system-ui">主标题</text>
    <text x="190" y="38" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="system-ui">副标题说明</text>
</g>
```

## 箭头连线

```svg
<!-- 垂直向下箭头 -->
<path d="M500,160 L500,195" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrowhead)"/>
<text x="510" y="180" font-size="9" fill="#94a3b8" font-family="system-ui">标注文字</text>
```

## 图例

```svg
<g font-size="11" font-family="system-ui" fill="#64748b">
    <rect x="80" y="655" width="14" height="14" rx="3" fill="#fef3c7" stroke="#f59e0b"/>
    <text x="100" y="666">用户入口</text>
    
    <rect x="180" y="655" width="14" height="14" rx="3" fill="#dcfce7" stroke="#22c55e"/>
    <text x="200" y="666">插件层</text>
    
    <rect x="300" y="655" width="14" height="14" rx="3" fill="#dbeafe" stroke="#3b82f6"/>
    <text x="320" y="666">服务层</text>
</g>
```

## 字体与尺寸规范

| 元素 | 字号 | 字重 | 字体 |
|------|------|------|------|
| 主标题 | 22 | 600 | system-ui |
| 层级标题 | 14 | 600 | system-ui |
| 模块主标题 | 13-14 | 500 | system-ui |
| 模块副标题 | 10 | 400 | system-ui |
| 箭头标注 | 9 | 400 | system-ui |
| 图例文字 | 11 | 400 | system-ui |

## 常用尺寸

- 画布：`width="1000" height="700"`（按层数与内容调整，层多则增大 height）
- 层级容器：`width="840" height="80-180"`，`rx="12"`
- 子模块：`width="180" height="40"`，`rx="6"`
- 边距：左右各 `80`，层间距 `20-35`

## 工作流

1. 按需求确定层级划分（层数不固定，常见 2–5 层）
2. 选定配色风格并分配每层色系
3. 绘制层级容器（从上往下）
4. 填充子模块
5. 添加箭头连线与标注
6. 添加图例
7. 调整尺寸与对齐

## 中文编码与乱码修正

在部分环境（云盘同步、跨平台、预览器编码推测错误）下，SVG 内裸写的中文可能变成乱码。**推荐做法**：所有中文用 XML 数字字符引用书写，与文件编码无关，任何符合 XML/SVG 的查看器都会正确解码显示。

- **格式**：`&#x` + 该字符的 Unicode 码点（4 位十六进制） + `;`
- **示例**：
  - 「权限」→ `&#x6743;&#x9650;`
  - 「用户入口层」→ `&#x7528;&#x6237;&#x5165;&#x53E3;&#x5C42;`
  - 「业务逻辑」→ `&#x4E1A;&#x52A1;&#x903B;&#x8BE1;`
- **查码点**：字符的 Unicode 码点可在搜索引擎查「Unicode 码点 某字」，或用脚本：`ord('权')` → 26435 → 十六进制 0x6743 → 写作 `&#x6743;`
- **纯英文/数字**（如 API、Redis、CRUD）无需转换。

```svg
<!-- 裸中文（易乱码） -->
<text x="500" y="40">权限管理系统</text>

<!-- 推荐：数字字符引用 -->
<text x="500" y="40">&#x6743;&#x9650;&#x7BA1;&#x7406;&#x7CFB;&#x7EDF;</text>
```

生成或修正 SVG 时，对中文统一输出为 `&#xXXXX;` 形式，可避免「SVG 无法查看」或乱码问题。

## 虚线边框（可选/扩展模块）

```svg
<rect ... stroke-dasharray="4,2"/>
```
