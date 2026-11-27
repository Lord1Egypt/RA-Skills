# 时效区块契约（distill-onepager ↔ fact-freshness-check）

两个 skill 通过本契约衔接：fact-freshness-check 产出的校验记录，按以下格式写入 distill-onepager 生成的 HTML。改契约要两边同时改。

## 0. 正文与区块的分工（最重要的约定）

| 载体 | 只允许承载 | 禁止 |
|---|---|---|
| 正文 | **当前版本的事实**。读者不需要任何背景就得到今天正确的答案 | 任何已被新版本推翻或修改的旧结论 |
| 时效区块 | 演进脉络（旧版行为、自哪一版起变化）、估算标注、实现细节说明、[未核实] 提示 | 承担知识纠正职能——纠正必须发生在正文 |

[演进] 条目的标准流程：**先改正文 → 再写区块**。区块里一条 [演进] 的价值是让读者"与时俱进、了解得更有深度"，前提是正文已经是新说法。区块里若发现正文还是旧说法，视为校验未完成。

## 1. 两种形态

| 条数 | 形态 | 位置 |
|---|---|---|
| 1–4 条 | 形态 A：紧凑区块 | 每个正文页 footer 之前，`<div class="freshness">` |
| 5–12 条 | 形态 B：附录页 | 文档末尾 `<section class="page page--freshness">`，标题「版本演进与出处」 |

附录页**不计入** 1–3 页的知识点预算；`onepager-render/scripts/check_onepager.py` 按 `page--freshness` 类识别并豁免。

## 2. 形态 A 模板

```html
<div class="freshness">
  <div class="freshness-head">版本演进 · 截至 <产品> <版本> 官方文档 · <YYYY-MM-DD> 核实</div>
  <ul>
    <li><strong>[仍成立]</strong> 断言（≤30 字）—— 出处章节号</li>
    <li><strong>[演进]</strong> 正文结论自 8.0 起；≤5.7 时为旧行为 —— Release Notes</li>
    <li><strong>[估算]</strong> 该数字为工程估算，非官方数据</li>
    <li><strong>[未核实]</strong> 断言 —— 未能找到当前版依据，需人工确认</li>
  </ul>
</div>
```

判定标签统一用：`[仍成立] / [演进] / [表述不完整] / [未核实] / [估算]`。写入文档的标签是 [演进]（不是"已变化"）——它记录的是演进脉络，配合已被改写的正文阅读。

## 3. 形态 B 骨架

```html
<section class="page page--freshness">
  <header class="doc-head">
    <div class="kicker">附录 · 不计入知识点页数</div>
    <h1>版本演进与出处</h1>
    <div class="meta">截至 <产品> <版本> 官方文档 · <YYYY-MM-DD> 核实</div>
  </header>
  <table>
    <thead><tr><th>断言（正文已按当前版书写）</th><th>判定</th><th>适用版本</th><th>演进脉络 / 出处</th></tr></thead>
    <tbody>
      <tr><td>…</td><td>[演进]</td><td>8.0 起</td><td>≤5.7 为旧行为 —— Release Notes</td></tr>
    </tbody>
  </table>
  <div class="footer"><span>来源见各条</span><span>附录页</span></div>
</section>
```

## 4. 样式约定（已内置于 `onepager-render/assets/onepager.html`）

- 字号 9pt，行高 1.45，比正文视觉轻一档：左侧 1.2mm 竖线 + 浅底。
- 判定标签用 `<strong>`，黑白打印靠文字本身区分，不靠颜色。
- 区块加 `break-inside: avoid`；放不下自动整体去下一页，不允许拆开。

## 5. 预算豁免

- 时效区块和附录页的中文字符**不计入** 600–800 / 1200–1600 的正文预算。
- 形态 A 自身上限 4 条 / 约 200 字符；形态 B 自身上限 12 条。
- 附录页仍受 A4 尺寸约束：超过 12 条说明筛选不够狠，回到 fact-freshness-check 收紧分级。

## 6. 双方义务

| skill | 义务 |
|---|---|
| fact-freshness-check | 先完成正文动作（[演进] 回写、[表述不完整] 补限定词），再按 §2/§3 格式写区块；每条带出处与核实日期；写入后触发对方自检 |
| distill-onepager（编排者） | 保证正文只含当前版本事实；在第 7 步调用 fact-freshness-check；交付报告里列出校验条数与四态分布 |
| onepager-render（排版） | 提供区块与附录页样式；check 脚本豁免并单独统计时效内容 |
