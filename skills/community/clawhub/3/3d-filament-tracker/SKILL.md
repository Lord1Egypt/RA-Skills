---
name: 3d-filament-tracker
description: 把 3D 打印耗材订单截图整理成可交互的 HTML 库存追踪器。用户说「统计一下我的 3D 打印耗材」/「3D 耗材库存」/「filament tracker」/「我还剩多少卷 PLA」/「哪些颜色已经在用了」/`/3d-filament-tracker`，或丢一堆订单截图说「帮我看看买了哪些料」时触发。多模态读图识别材料/品牌/颜色/卷数 → 生成单文件 HTML，含「在用 / 已用」双步进器、自动联动现有数、localStorage 持久化、JSON 导出导入。一份原始购买清单 + 一份动态状态。
metadata:
  type: skill
  scope: global
---

# 3D Filament Tracker

把散落在淘宝/京东/拼多多订单截图里的 3D 打印耗材，整理成一张可交互的库存表。

## 触发方式

- 用户说「统计一下我的 3D 打印耗材」/「3D 耗材库存」/「filament tracker」
- 用户给一堆订单截图说「帮我看看买了哪些料」
- 用户问「我还剩多少卷 PLA」/「哪些颜色已经在用了」
- `/3d-filament-tracker`

## 它解决什么

3D 打印耗材一买就是几十卷，散在多个店铺多个订单里。**靠脑子记不住**：哪个颜色买了几卷？哪些已经塞进打印机了？哪些用光了？哪些还在库存？

传统方案：

- **Excel** —— 每改一次状态都要手动算合计，没颜色提示
- **拍照堆桌上** —— 不知道总数也不知道库存
- **Bambu Studio 内置料盘** —— 只管插上去那一卷，不管库房

这个 skill 给你一份**单文件 HTML 跟踪器**：浏览器打开就能用，状态存在 localStorage，可导出 JSON 备份。

## 核心交互模式：双步进器 + 现有数联动

每行耗材有两个状态：

```
原始购买数 = 现有 + 已用光
现有       = 在用 + 库存
```

UI 上每行两个步进器：

```
[在用 −  N/总  +]   [已用 −  N/总  +]
 绿色背景           灰色背景
```

约束：`在用 + 已用 ≤ 总卷数`（步进器自动 disable）

「已用」+1 时全部联动重算：
- 该行「现有」列减 1
- 该颜色合计减 1
- 该材料小计减 1
- 顶部 pill：现有合计 −1 / 已用光 +1
- 「库存」pill：减 1

「在用」+1 时不影响现有数（耗材还在你手上），只是把它从库存挪到在用。

## 流程

### Phase 1：读图整理

1. 用 Read 工具读用户给的所有订单截图（一次可读多张）
2. 提取每条订单的：**材料**（PLA / PETG / ASA / PA / TPU / PC...）+ **品牌/系列**（拓竹 PLA Basic / POLYMAKER 高速 PETG / 三绿 PLA Matte...）+ **颜色** + **卷数** + **来源标记**（散装 / 套装 / 赠品 / 赔付）
3. 用一个 Markdown 表先给用户对一遍。**不要一上来就生成 HTML**，先确认数据，往返几轮把数字校准
4. 同色不同来源（散装+套装+赔付）拆成多行，每行带「来源」标签，便于追踪到底是哪一卷在用
5. 套装也按颜色拆开统计，**不要按套装维度计数**（套装是采购概念，颜色是使用概念）

### Phase 2：生成 HTML

用 `templates/template.html` 作为骨架，填充用户的实际数据。每行 `<tr>` 必须有 `data-id`（kebab-case，例 `pla-black-散装`），唯一即可。

关键 CSS class：
- `material-pla` / `material-petg` / `material-asa` —— 左侧色条
- `tag-pla` / `tag-petg` / `tag-asa` —— 行内标签
- `color-total` —— 同色合计行
- `total-row` —— 材料小计行
- `group` —— 材料分组标题行
- `badge-set` / `badge-gift` —— 套装/赠品标记

每个色组结束插一个 `<tr class="color-total">` 显示合计；每个材料块结束插一个 `<tr class="total-row">`。这两个的「卷数」单元格内容由 JS 自动重算，初始填什么数字都行。

### Phase 3：交付

- HTML 文件放到 `<workspace>/3d-printing/耗材/耗材统计.html`
- 截图也放在同目录
- 提示用户：**第一次点完后立刻点「📥 导出状态」存一份 JSON**，搬目录或换浏览器就靠这份恢复

## 关键工程点（不要踩坑）

### 1. localStorage 按文件路径隔离
- `file:///Users/.../耗材统计.html` 和 `file:///Users/.../moved/耗材统计.html` **是两个独立 origin**，状态不会自动迁移
- 所以必须提供 JSON 导出/导入
- 搬目录前先让用户导出一份；移完再让用户重新导入

### 2. 「现有」≠ 「原始」
- 「卷数」列显示的是**现有**（= 总数 − 已用），会随交互变化
- 步进器分母固定显示**原始购买数**，所以用 `data-total` 锁住，不能从 `.qty` 单元格读
- 初始化时把 HTML 里写死的初始 `.qty` 值 snapshot 到 `tr.dataset.total`，之后所有读数走 `getTotal(tr)` 而不是 `parseInt(qty.textContent)`

### 3. 合计行不能 hardcode
- 颜色合计 / 材料小计 / 总计**全部由 JS 重算**
- HTML 里写的初始数字只是占位，加载时 `recomputeAggregates()` 立刻覆盖
- 重算逻辑：从上往下遍历 `tbody`，遇到 `.group` 行重置 colorAcc/materialAcc，遇到 `[data-id]` 行累加 (total − consumed)，遇到 `.color-total` 写 colorAcc 并清零，遇到 `.total-row` 写 materialAcc 并清零

### 4. 双步进器互相约束
- `在用 + 已用 ≤ 总数`
- 单步进器自身能减到 0
- 任何一个 +1 之前先检查 `next + other > total ? return : commit`
- disable 状态算 `(using + consumed) >= total` 时 + 按钮全部 disable

### 5. JSON 兼容旧版本（v3 → v4）
- 早期版本只有「在用」一个值，state 是 `{id: number}`
- 现在 state 是 `{id: {using: N, consumed: M}}`
- importState 时检测 `typeof v === 'number'` → 自动迁移成 `{using: v, consumed: 0}`

## 视觉规范

整行底色根据状态：
- 浅**绿** = 该批次全在用
- 浅**黄** = 部分在用
- 浅**灰 + 删除线** = 全部用光
- 白 = 全在库存

色卡（`.swatch`）尽量贴近实物颜色：
- 拓竹 PLA Basic 系列用商品页配色
- Silk 系列用 `linear-gradient` 模拟丝绸渐变
- 透明色用半透明
- 实在拿不准就用 `#7f8c8d` 灰

## 不要做的事

- ❌ 不要用复杂前端框架（React/Vue）—— 单文件 HTML + 原生 JS，用户双击就能用
- ❌ 不要把状态存到外部数据库 —— localStorage + JSON 文件就够了
- ❌ 不要按套装维度统计 —— 用户关心的是颜色，不是 SKU
- ❌ 不要改步进器分母 —— 分母永远是原始购买数，让用户能看到"我之前总共买过几卷"
- ❌ 不要在 HTML 里硬编码合计数字让它和 JS 不同步 —— 合计永远 JS 算

## 同步发布

跟着 [[feedback_skill_publishing_flow]] 走：公网 GitHub + ClawHub。这个 skill 不涉及 SAP 业务，**不推 SAP 内网**。
