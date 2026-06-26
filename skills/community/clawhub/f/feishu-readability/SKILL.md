---
name: 飞书文档可读性优化
description: 飞书文档格式优化与安全修改规范。**必须在通过MCP修改任何mi.feishu.cn文档之前加载此skill**。包括最小修改原则、富文本保护、段落间距、加粗规范。触发条件：用户要求修改飞书文档内容或格式，涉及mi.feishu.cn域名，或调用小米飞书MCP的update-doc工具。
---

# 飞书文档可读性优化 Skill

## 概述

本 Skill 旨在解决飞书云文档（Lark Doc）在自动化编辑中常见的格式问题，重点提升文档的视觉层次感和可读性。它基于对飞书 Markdown 渲染引擎底层逻辑（API vs. 交互式编辑）的深入理解，提供了一套经过验证的“最佳实践”。

## 🏆 三大核心原则

### 1. 🚀 核心铁律：最小修改原则 (The Principle of Minimal Modification)

**权重：最高 (Critical)**
**定义**：任何格式优化都必须是“手术刀式”的精准微调，**严禁**因为修改一个标点而重写整个段落，更不可重写整篇文档。

**❌ 绝对禁止：**
- **严禁使用 `overwrite` 模式**：除非旨在清空文档重写，否则绝不允许使用 `overwrite` 进行修改，这会导致评论、历史记录、图片 Token 和未知的富文本属性丢失。
- **严禁大范围选区**：`selection_with_ellipsis` 不得跨越多个不相关的段落或标题。
- **严禁盲目重构**：不得在未获取该段落完整 Token（如图片、公式）的情况下重写包含该 Token 的段落。

**✅ 最佳实践：**
- **字节级定位**：`selection` 应短至仅仅包含“待修改目标 + 确保唯一的最小上下文”。
    - ✅ 优秀：`selection="token=\"xxx\"...**标题"` （利用 Token 定位）
    - ✅ 优秀：`selection="。**下一标题"` （利用标点定位）
    - ❌ 错误：`selection="上一段开头...下一段结尾"` （范围太广，极易误伤）
- **增量操作**：优先使用 `insert_before` / `insert_after` 插入内容，而非 `replace_range` 替换内容。
- **格式隔离**：确保修改后的 Markdown 文本与原文在“未修改部分”完全一致（包括此时看不到的隐藏字符）。

### 2. 间距法则 (The Law of Visual Spacing)

**权重：高 (High)**
**问题**：API 写入的 Markdown 纯文本会被飞书解析器进行“空白清洗”（Whitespace Optimization），导致标准的空行被合并，文档显得拥挤。

**✅ 解决方案**：使用 **带属性的占位段落** ` {align="center"}`。
只有带有非默认属性（如 Center）的空段落，才会被解析器视为“有意义的内容”而强制保留。

**📜 书写规范（基于最小修改原则）：**
1.  **插入式注入**：使用 `insert_before` 在标题前插入 Spacer，而非 Replace 整个标题块。
2.  **必须以空格开头**：` {align...`（无空格会被渲染为乱码文本）。
3.  **列表后阻断**：若前文是列表，必须使用 **双换行** `\n\n` 先结束列表，再插入标记。

### 3. 本土化格式卫生 (Formatting Hygiene)

**权重：中 (Medium)**

**加粗规范**：
- **冒号隔离**：加粗必须止步于冒号之前，且冒号后必须有空格。
    - ✅ 正确：`**标题**： 正文`（推荐：冒号在加粗外，且有空格）
    - ✅ 可行：`**标题：** 正文`（若必须在内，冒号后必须分开）
    - ❌ 错误：`**标题：**正文`（粘连）

**列表标点规范**：
- **单句无标点**：若列表项仅有一句话，**去掉**末尾的句号。
- **富文本保护**：
- 定位时务必避开 `<image>`、`<callout>` 等标签。
- 若必须修改包含标签的段落，需先 `fetch-doc` 获取 Token，并在 `markdown` 参数中原样写回。

---

## 🛠️ 标准操作流程 (SOP)

### 第一步：诊断 (Fetch & Analyze)
获取文档内容，重点检查：
1.  标题前是否拥挤（特别是列表后的标题）。
2.  加粗格式是否粘连。
3.  是否存在特殊的富文本块需避开。

### 第二步：间距注入 (Spacer Injection)
使用 `replace_range` 在目标位置精确插入 Spacer。

**场景 A：标准标题前（H1-H3）**
```python
mcp_FeishuMCP_update-doc(
    mode="replace_range",
    selection_with_ellipsis="前文结尾。\n## 标题", 
    markdown="前文结尾。\n\n {align=\"center\"}\n\n## 标题"
)
```

**场景 B：列表后的标题（高风险点）**
```python
mcp_FeishuMCP_update-doc(
    mode="replace_range",
    selection_with_ellipsis="- 列表项结尾\n## 标题",
    # 注意：双换行 + Spacer + 双换行
    markdown="- 列表项结尾\n\n {align=\"center\"}\n\n## 标题"
)
```

### 第三步：格式精修 (Refinement)
修复粘连的加粗或排版错误。

```python
mcp_FeishuMCP_update-doc(
    mode="replace_range",
    selection_with_ellipsis="**粘连标题**正文",
    markdown="**粘连标题：** 正文"
)
```

---

## ❓ 故障排除速查

| 现象 | 原因 | 解决方案 |
| :--- | :--- | :--- |
| **页面显示 `{align="center"}` 文字** | 缺少起始空格 | 替换为 ` {align="center"}` |
| **标题依然拥挤** | 列表后未双换行，或 Spacer 未独立占行 | 确保前后都有 `\n` |
| **出现 `width="100"` 乱码** | 破坏了 `<image>` 标签 | Undo，重写时保留完整 Token |
| **段落莫名消失/重复** | `replace_range` 范围太大或定位不准 | 缩小定位范围，包含更多唯一的上下文标点 |

---

## ✅ 执行前核对清单 (Pre-flight Checklist)

1.  [ ] **定位准确性**：`selection_with_ellipsis` 是否足够短且唯一？
2.  **上下文安全**：选区内是否包含了图片或引用块？（如有，需特别小心）
3.  **Spacer 格式**：是否检查了 ` {align="center"}` 的空格和换行？
4.  **列表处理**：前文如果是列表，是否加了 `\n\n`？
