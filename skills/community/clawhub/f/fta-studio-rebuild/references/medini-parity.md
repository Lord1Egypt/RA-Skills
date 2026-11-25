# medini analyze 操作对齐清单

依据厂商官方手册（Safety Analysis / Process Guide / New and Noteworthy）中关于 FTA 的原文。逐条对照实现。

## 1. 事件节点的视觉结构

> "Event name/description in the top compartment; **Event identifier in the middle compartment** … The shape of this middle 'decoration' compartment indicates the type of the event."

- 上半部：名称（白色矩形框、**黑色文字**、细黑边框）
- 下半部：编号装饰（`TLE1` / `E01` 之类），**默认显示**
- 提供隐藏开关（新增特性里明确有 "intermediate event ID labels can be hidden in order to save diagram space"）

实现：`state.showIds = true` 默认值 + Ribbon「编号」复选框。

**底事件左缘红色圆点**：medini 在每个 basic/primary event 框内左缘画一个小实心红点，事件名左对齐紧随其后（用户逐像素比对过截图）。

- 画布：`circle.basic-dot`，`r=3.5`，`cx = 椭圆左缘 + 9`，`cy = 框中线`
- 文字：`text-anchor="start"`，起点在红点右侧 9px，按可用宽度截断（`fitCanvasLabel`）
- 导出：`src/svg.mjs` 同规则，`r=4`、`fill="#e01b24" stroke="#9c1a1a"`
- **只有 basic 类型有红点**，中间事件/顶事件没有

## 2. 双击折叠子树

> "If you **double click on an event or gate** on the diagram, the **subtree starting at that element will be folded in**, double-clicking again will restore the subtree."

- 事件和门都要支持
- 折叠后保留门符号与折叠标记（medini 显示 `[2]` 之类的重复计数器）
- 我们的实现：节点右下角 `+N` 徽标

## 3. 连接规则

> "The tool observes the direction of the line creation and it will **forbid wrong connections as well as cycles**."（界面提示 "not possible in this direction"）

- 只允许自顶向下
- **禁止成环**：`isInSubtree(to, from)` 为真则拒绝
- 拒绝自身连接
- 重复引用（同一事件多处出现）应通过**转移门 / MOE**，不是直接多条入边

> "connections into the direction of the leaf-nodes will be **automatically created** when dropping an element from the palette onto an existing element"

- 从调色板添加事件/门时，**自动连线到选中节点**

## 4. 上下文菜单（右键事件）

medini 的实际菜单项与我们的对应：

| medini | 我们 |
|---|---|
| Calculate Probability | 计算概率 · Calculate probabilities |
| Calculate Probability (only selection) | 计算概率（作用于整树，够用） |
| Evaluate Fault Tree... | 评估故障树 · Evaluate Fault Tree |
| Arrange Subtree | 整理子树 · Arrange Subtree |
| Boolean expression | 布尔表达式 · Boolean Expression |
| Derive / Delete from Diagram / Delete from Model | 删除事件 |

## 5. 布尔表达式

> "Fault Trees can be transformed into textual Boolean expressions … triggered at any top, intermediate or base event node."

实现要点：递归展开门，`OR` / `AND` / `XOR` / `NOT` 对应运算符；**同运算符的子式自动拍平**，避免括号爆炸。

示例输出：
```
π[N001] = ((FMEA-001 OR FMEA-002 OR FMEA-003 OR FMEA-004 OR FMEA-005)
           AND (FMEA-006 OR FMEA-007))
```

## 6. 评估选项

medini 的 Fault Tree Evaluation 对话框：

| 选项 | 实现 |
|---|---|
| Restrict cut set order up to n | `settings.cutSetOrder` |
| Mission time | `settings.missionTime` |
| Compute F(t), Qavg, Favg, Wavg | 已算 Q/F，Wavg 可后补 |
| Integration step width | 时间扫描步长 |
| Calculate importance measures | `importance` 字段 |
| Drop cut sets with probability < X | 概率截断（可后补） |

求解算法：`BDD based`（精确）/ `Cut set based`（近似）。我们提供 `method: auto | mocus | bdd`。

## 7. 其他应对齐的行为

| medini | 说明 |
|---|---|
| FTA Diagram Pagination | 大树跨页；**分页点由画图人设**，每个分页点各开一页；页底虚线 `⤓ 分页 · 第 N 页`，页顶虚线 `↑ 续上页`；标签可点跳转；A4 打印件印真实页码。详见 `SKILL.md` §4 |
| Outline View | 大纲面板，快速定位未开发事件 / 重复事件 |
| Layouting | 自动布局 + 子树整理 |
| Heatmap | 按概率贡献着色（低/中/高） |
| Path highlighting / Cut set highlighting | 选中割集高亮路径（可后补） |
| Transfer gate | 跨页/复用引用，符号为三角形 |

## 8. 符号速查（medini / IEC 60617）

- 顶事件、中间事件：**矩形**
- 基本事件：**圆形**
- 未开发事件：**菱形**
- 房屋事件：**五边形（尖顶）**
- 条件事件：**椭圆**
- 转移：**三角形**
- 门：**平底 + 拱顶**，操作符写在门体内（`&` / `≥1` / `=1` / `k/n`）
- 连线：medini 为**无箭头直线**；我们的实现保留箭头（可配置去掉）
