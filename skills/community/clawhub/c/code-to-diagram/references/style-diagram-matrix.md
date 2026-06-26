# 风格 × 图表类型适配矩阵

帮助快速选择最合适的视觉风格。

---

## 风格速览

| # | 风格名 | 背景 | 调性 | 最佳场景 |
|---|--------|------|------|----------|
| 1 | Flat Icon | 白底 | 清晰、专业 | 文档、博客、演示文稿 |
| 2 | Dark Terminal | 暗色渐变 | 黑客、技术 | GitHub README、技术博客 |
| 3 | Blueprint | 深蓝+网格 | 工程、精确 | 架构文档、RFC |
| 4 | Notion Clean | 白底 | 极简、聚焦 | Notion 嵌入、Wiki |
| 5 | Glassmorphism | 暗色渐变 | 现代、高端 | 营销页、发布会 |

---

## 适配评级

★★★ = 极佳  ★★ = 良好  ✗ = 不推荐

| 图表类型 | Flat Icon | Dark Terminal | Blueprint | Notion Clean | Glassmorphism |
|----------|-----------|---------------|-----------|--------------|---------------|
| 架构图 | ★★★ | ★★★ | ★★★ | ★★ | ★★ |
| 类图/ER图 | ★★ | ★★ | ★★★ | ★★★ | ✗ |
| 时序图 | ★★ | ★★ | ★★★ | ★★★ | ✗ |
| 流程图 | ★★★ | ★★ | ★★ | ★★ | ★★ |
| 思维导图 | ★★★ | ★★ | ✗ | ★★★ | ★★★ |
| 数据流图 | ★★★ | ★★★ | ★★★ | ★★ | ✗ |
| 用例图 | ★★ | ✗ | ★★★ | ★★★ | ✗ |
| 状态机 | ★★ | ★★ | ★★★ | ★★★ | ✗ |
| 网络拓扑 | ★★★ | ★★★ | ★★★ | ★★ | ★★ |
| 对比/矩阵 | ★★★ | ★★ | ✗ | ★★★ | ✗ |
| 时间线 | ★★★ | ★★ | ★★ | ★★★ | ★★ |
| AI/Agent 架构 | ★★★ | ★★★ | ★★ | ★★ | ★★★ |

---

## 选择决策树

```
用户说了什么？
├── "暗色" / "dark" / "terminal" / "GitHub" / "README"
│   └── → Style 2: Dark Terminal
├── "蓝图" / "blueprint" / "工程" / "RFC"
│   └── → Style 3: Blueprint
├── "简洁" / "clean" / "Notion" / "极简"
│   └── → Style 4: Notion Clean
├── "毛玻璃" / "glass" / "现代" / "高端" / "演示"
│   └── → Style 5: Glassmorphism
├── "亮色" / "白底" / "文档" / "博客"
│   └── → Style 1: Flat Icon
└── 未指定
    └── → Style 1: Flat Icon（默认）
```

---

## 参考文件路径

使用 SVG 引擎时，根据选定风格读取对应的参考文件：

- `references/style-1-flat-icon.md`
- `references/style-2-dark-terminal.md`
- `references/style-3-blueprint.md`
- `references/style-4-notion-clean.md`
- `references/style-5-glassmorphism.md`

语义图形和产品图标参考：

- `references/icons.md`
