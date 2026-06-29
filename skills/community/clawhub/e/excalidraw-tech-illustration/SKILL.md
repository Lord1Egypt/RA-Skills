---
name: excalidraw-tech-illustration
description: 生成 Excalidraw 技术配图（.excalidraw 源文件 + PNG 渲染图）。当用户要求"生成配图"、"画技术图"、"Excalidraw 图解"、"技术图解"、"流程图"、"架构图"时触发。支持7种风格（纵向流程/横向卡片/架构拓扑/时间线/对比矩阵/分层架构/状态机），双面板组合，自动渲染 PNG，归位到 collection 目录。
---

# Excalidraw 技术配图生成器

生成技术文章配图，输出 `.excalidraw` 源文件 + `.png` 渲染图。

## 7种基础风格

| 代号 | 风格 | 适用场景 |
|------|------|---------|
| A | 纵向流程图 | 操作步骤、诊断流程、有判断分支的排查 |
| B | 横向三栏卡片 | 阶段对比、多方案并列、两流程分步对照 |
| C | 架构/拓扑图 | 组件关系、节点拓扑、缓存结构 |
| D | 时间线/时序图 | 事件先后顺序、执行阶段进度 |
| E | 对比矩阵 | 多实体多维度差异、参数对比 |
| F | 分层架构图 | 协议栈、存储引擎分层、Server/Engine层 |
| G | 状态机图 | 连接状态、事务状态、复制状态迁移 |

## 风格自动选择规则

```
文章标题/内容包含关键词 → 自动匹配风格

"对比/VS/区别/差异/选型/比较" → E 对比矩阵
"架构/原理/组成/分层/层级/协议栈" → F 分层架构图
"流程/步骤/如何/诊断/排查/定位" → A 纵向流程图
"陷阱/坑/注意/风险/避免" → B 横向卡片 + 红色警告框
"MGR/复制/主从/集群/拓扑" → D 时序图 + C 架构组合
"状态/生命周期/迁移/切换" → G 状态机图
"时序/先后/进度/阶段/事件" → D 时间线时序图
"成分/节点/组件/关系" → C 架构拓扑图
无明确关键词 → 默认 A 纵向流程图
```

## 双面板组合规则

每篇图解组合 2 个面板，纵向排列，Panel 间距 200px，Panel2 ID 加 `p2_` 前缀。

| 文章类型 | 组合 | Panel1 | Panel2 |
|---------|------|--------|--------|
| 原理+步骤 | B→A | 三栏卡片总览 | 纵向流程走步骤 |
| 诊断/操作 | A→B | 纵向流程走决策 | 横向卡片对比方案 |
| 操作→系统视角 | A→C | 纵向流程走操作 | 架构图展示系统路径 |
| 架构讲解 | C→B | 架构图展示组件 | 横向卡片对比特性 |
| 拓扑+决策 | C→A | 拓扑图展示节点 | 纵向决策流程 |
| 时间线+对比 | D→B | 时序图展示事件 | 横向卡片对比差异 |
| 对比+操作 | E→A | 对比矩阵展示差异 | 纵向流程走操作 |
| 分层+对比 | F→B | 分层架构展示层级 | 横向卡片对比特性 |
| 状态+方案 | G→B | 状态机展示迁移 | 横向卡片对比方案 |
| 状态+流程 | G→A | 状态机展示生命周期 | 纵向流程走决策 |

## 固定元素标准化

1. **决策菱形**：`#e36209` 橙色边框 + `#fff3cd` 浅黄背景
2. **底部排查命令栏**：技术类文章保留紫色栏（`#f3e8ff` 背景 + `#6f42c1` 边框）
3. **箭头标签**：独立 text 元素（禁止 containerId 绑定）
4. **颜色语义编码**：🔵蓝=标题/正常 | 🟢绿=功能/成功 | 🟡黄=注意/配置 | 🔴红=警告/错误 | 🟣紫=总结/命令

## JSON 元素属性规范（强制）

### 颜色属性

- ✅ 使用原生属性：`backgroundColor`、`strokeColor`
- ❌ 禁止使用：`fill`、`stroke`、`color`（excalidraw-cli 不识别）

### text 元素

- ❌ 禁止给 text 元素添加 `containerId`（渲染位置不可控）
- ✅ 用独立 text 元素 + 精确坐标定位标签

### 标准元素模板

```json
{
  "type": "rectangle",
  "backgroundColor": "#d73a49",
  "strokeColor": "#24292e",
  "strokeWidth": 2,
  "roughness": 0,
  "fontFamily": 3,
  "fillStyle": "solid"
}
```

## 全局规范

- 基准原点 `(100, 100)`，纵向 100px / 横向 150px 步长
- 全局默认样式：`roughness:0` / `fontFamily:3` / `strokeWidth:2` / `fillStyle:solid`
- 容器宽度 = 文字字数 × fontSize × 系数 + 40，横向总宽 ≤ 750px
  - 系数：中文 1.0 / 英文数字 0.6 / 中英混合 0.8
- 多行文字手动 `\n` 换行，每行 ≤ 10 中文字
- 菱形容器尺寸 = 矩形尺寸 × 1.2
- 文字溢出修复顺序：增大宽度 → 减小 fontSize → 手动换行 → 精简文字

## 渲染命令

```bash
npx @swiftlysingh/excalidraw-cli convert input.excalidraw output.png --format png --output output.png
```

必须显式指定 `--output output.png`。

## 配图归位规则（强制）

生成配图后必须：

1. 将 `.excalidraw` + `.png` 移动到 `excalidraw/collection/<分类>/<章节>/` 目录
2. 更新 `excalidraw/collection/index.json` 的 `diagrams` 数组
3. 更新 `excalidraw/collection/index.json` 的 `statistics`
4. 如章节首次创建，同步创建 `<章节>/README.md`

## 展示规则

- `.png` 用 `MEDIA:` 内联展示
- `.excalidraw` 用文件路径列出（可在 excalidraw.com 在线编辑）
- 必须同时展示两种格式

## 文件存储

- 草稿：`excalidraw/drafts/`
- 渲染输出：`excalidraw/output/`
- 归位：`excalidraw/collection/<分类>/<章节>/`
- 禁止存 `/tmp`
- 版本号：v5.1 小改 / v6 大改，废弃版本保留不删除
