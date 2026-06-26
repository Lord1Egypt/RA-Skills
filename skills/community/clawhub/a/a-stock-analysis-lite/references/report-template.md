# HTML 报告模板与质量检查

---

## 输出方式

**HTML（主力方案）——适用于所有 LLM 和环境。**
- LLM 生成填好内容的 HTML 文件 → 用户浏览器打开 → Ctrl+P → 另存为PDF
- 零依赖，任何 LLM / 任何系统均可执行

**用户操作步骤：**
1. LLM 将填好内容的 HTML 保存为 `.html` 文件（或作为 artifact 渲染）
2. 用浏览器打开
3. Ctrl+P（Mac: Cmd+P）→ 打印机选"另存为PDF"
4. 设置：A4，边距最小，勾选"背景图形"（保留颜色）
5. 保存 → 得到 PDF

---

## HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>【深度策略】{简称}（{代码}）</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Microsoft YaHei","PingFang SC",Arial,sans-serif;font-size:13px;color:#1a1a1a;background:#fff;max-width:900px;margin:0 auto;padding:36px 44px}
:root{--navy:#1F4E79;--blue:#2E75B6;--light:#D6E4F0;--red:#C00000;--green:#1A6B2A;--yellow:#FFF2CC}
.ph{border-bottom:3px solid var(--blue);padding-bottom:8px;margin-bottom:20px;display:flex;justify-content:space-between}.ph span{font-size:12px;color:#666}
.cover{text-align:center;margin-bottom:20px}
.cover .tag{font-size:12px;color:#888;margin-bottom:6px}
.cover h1{font-size:30px;font-weight:900;color:var(--navy);margin:4px 0 8px}
.cover .sub{font-size:14px;font-weight:700;font-style:italic;color:var(--blue);margin-bottom:12px;line-height:1.5}
hr.r{border:none;border-top:3px solid var(--blue);margin:10px 0}
.cover .meta{font-size:12px;color:#555;margin:6px 0}
.pb{display:inline-block;background:#fff0f0;border:1.5px solid #f9a8a8;border-radius:5px;padding:6px 18px;font-size:13px;font-weight:700;color:var(--red);margin-top:4px}
.kg{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px}
.kp{background:#f7f9fc;border:1px solid #d8e4ef;border-radius:6px;padding:10px 12px;text-align:center}
.kp .kv{font-size:20px;font-weight:800;color:var(--navy)}.kp .km{font-size:11px;color:#666;margin-top:2px}
.kp.red .kv{color:var(--red)}.kp.grn .kv{color:var(--green)}
.sec{font-size:15px;font-weight:800;color:var(--navy);border-left:5px solid var(--blue);padding-left:10px;margin:24px 0 12px}
p.blk{margin:0 0 9px;line-height:1.8;font-size:13px}
.lb{font-weight:700;color:var(--navy)}
table{width:100%;border-collapse:collapse;margin-bottom:14px;font-size:12.5px}
th{background:var(--navy);color:#fff;padding:8px 10px;text-align:center;font-weight:700;font-size:12px}
td{padding:7px 10px;border:1px solid #ccc;vertical-align:top;line-height:1.6}
tr:nth-child(even) td{background:#EFF5FB}tr:nth-child(odd) td{background:#fff}
td:first-child{font-weight:700}td.c{text-align:center}
.sa .sl{background:var(--green);color:#fff;text-align:center;font-weight:700;font-size:12px;width:90px;padding:10px 6px;vertical-align:middle}
.sb .sl{background:var(--yellow);color:#333;text-align:center;font-weight:700;font-size:12px;width:90px;padding:10px 6px;vertical-align:middle}
.sc .sl{background:var(--red);color:#fff;text-align:center;font-weight:700;font-size:12px;width:90px;padding:10px 6px;vertical-align:middle}
.sa td,.sb td,.sc td{background:#fafafa!important}
.sum{background:var(--light);border-left:5px solid var(--blue);padding:13px 16px;border-radius:0 4px 4px 0;margin:10px 0;font-size:13px;line-height:1.8}
.pf{border-top:1px solid #ccc;padding-top:10px;margin-top:28px;text-align:center;font-size:11px;color:#999}
@media print{body{max-width:100%;padding:0;margin:0;font-size:11.5px}table{page-break-inside:avoid}@page{size:A4;margin:14mm 12mm}}
</style>
</head>
<body>

<div class="ph">
  <span>公司研究·深度策略 ｜ {简称}（{代码}.SH/SZ）</span>
  <span>报告日期：{YYYY年MM月DD日}</span>
</div>

<div class="cover">
  <div class="tag">【公司研究·深度策略】</div>
  <h1>{简称}（{代码}.SH/SZ）</h1>
  <div class="sub">—— {一句话核心判断，15~30字}</div>
  <hr class="r">
  <div class="meta">报告日期：{日期} &nbsp;|&nbsp; 研究分类：{行业/细分} &nbsp;|&nbsp; 总股本：{X亿股}</div>
  <div class="pb">⚠ 今日最新价：{价格} CNY（{涨跌幅}%）&nbsp;|&nbsp; 开盘：{开盘} &nbsp;|&nbsp; 区间：{低}~{高}</div>
  <hr class="r" style="margin-top:10px">
</div>

<!-- KPI卡（4个：总市值 / PB / 较发行价 / 股息率 ——根据情况替换最有价值的指标）-->
<div class="kg">
  <div class="kp"><div class="kv">{市值}亿</div><div class="km">总市值</div></div>
  <div class="kp"><div class="kv">{PB}x</div><div class="km">市净率 PB</div></div>
  <div class="kp red"><div class="kv">{较发行价%}</div><div class="km">较发行价涨跌</div></div>
  <div class="kp grn"><div class="kv">{股息率}%</div><div class="km">股息率（TTM）</div></div>
</div>

<div class="sec">一、核心观点及研判（Executive Summary）</div>
<table>
  <thead><tr><th style="width:16%">维度</th><th>核心判断</th></tr></thead>
  <tbody>
    <tr><td>价格走势</td><td>{章节一-价格走势}</td></tr>
    <tr><td>基本面逻辑</td><td>{章节一-基本面逻辑}</td></tr>
    <tr><td>策略概要</td><td>{章节一-策略概要}</td></tr>
  </tbody>
</table>

<div class="sec">二、关键价格结构分析（Key Price Levels）</div>
<table>
  <thead><tr><th style="width:26%">项目</th><th style="width:22%">价格区间（CNY）</th><th>逻辑说明</th></tr></thead>
  <tbody>
    <tr><td>{阻力1}</td><td class="c">{价格}</td><td>{逻辑}</td></tr>
    <tr><td>{阻力2}</td><td class="c">{价格}</td><td>{逻辑}</td></tr>
    <tr><td>今日收盘价</td><td class="c">{价格}（{涨跌幅}%）</td><td>{量能描述}</td></tr>
    <tr><td>{支撑1}</td><td class="c">{价格}</td><td>{逻辑}</td></tr>
    <tr><td>{支撑2（净资产锚）}</td><td class="c">约{净资产}</td><td>{逻辑}</td></tr>
    <tr><td>{极值支撑}</td><td class="c">{价格}</td><td>{背景}</td></tr>
    <tr><td>当前状态</td><td class="c">{形态描述}</td><td>{技术特征}</td></tr>
  </tbody>
</table>

<div class="sec">三、深度数据透视（Data Insights）</div>
<p class="blk"><span class="lb">市值与估值：</span>{段落1}</p>
<p class="blk"><span class="lb">今日资金异动：</span>{段落2}</p>
<p class="blk"><span class="lb">近期行情回顾：</span>{段落3}</p>
<p class="blk"><span class="lb">核心业绩数据：</span>{段落4}</p>
<p class="blk"><span class="lb">核心催化剂：</span>{段落5}</p>
<!-- 主营业务表（选填，有多元化业务时加入）-->
<table>
  <thead><tr><th>业务类别</th><th style="width:20%">特点/占比</th><th>主要领域及景气</th></tr></thead>
  <tbody><tr><td>{业务}</td><td class="c">{特点}</td><td>{描述}</td></tr></tbody>
</table>

<div class="sec">四、关键情景模拟（Scenario Analysis）</div>
<table>
  <thead><tr><th style="width:90px">情景</th><th>情景描述</th></tr></thead>
  <tbody>
    <tr class="sa"><td class="sl">情景A<br>（乐观）</td><td>{情景A：触发条件+入场信号+目标价+时间+概率}</td></tr>
    <tr class="sb"><td class="sl">情景B<br>（基准）</td><td>{情景B：逻辑+震荡区间+策略+概率}</td></tr>
    <tr class="sc"><td class="sl">情景C<br>（下探）</td><td>{情景C：触发因素+止损价+最大回撤+风险点+概率}</td></tr>
  </tbody>
</table>

<div class="sec">五、核心风险提示（Risk Factors）</div>
<table>
  <thead><tr><th style="width:24%">风险类别</th><th>风险描述</th><th style="width:12%">等级</th></tr></thead>
  <tbody>
    <tr><td>{风险1}</td><td>{描述}</td><td class="c">★★★★★</td></tr>
    <tr><td>{风险2}</td><td>{描述}</td><td class="c">★★★★☆</td></tr>
    <!-- 4~6行 -->
  </tbody>
</table>

<div class="sec">六、总结评价</div>
<hr class="r">
<div class="sum">{总结核心段落，3~5句}</div>
<p class="blk"><span class="lb">近期三大关键节点：</span>
  ① {节点1：时间+事件+意义}；
  ② {节点2：时间+事件+意义}；
  ③ {节点3：持续跟踪指标+阈值}。
</p>

<div class="pf">⚠ 本报告内容仅基于公开数据及AI分析生成，不构成任何投资建议或荐股行为。投资者据此操作，风险自担。证券市场有风险，投资需谨慎。</div>
</body>
</html>
```

---

## 质量检查清单

```
【数据真实性】
□ 今日价格来自实时来源（东方财富/新浪财经/同花顺 或当日搜索），非历史缓存
□ 市值 ≈ 今日价 × 总股本（误差<5%即自洽）
□ 量比已用公式计算（今日量/3月均量），非估算
□ 所有财务数据注明报告期（如"2025年三季报，截至2025年9月30日"）
□ 52周定位已用公式计算（(今日价-低)/(高-低)×100%）

【分析逻辑】
□ 三情景概率之和 = 100%（必须精确相加）
□ 情景A触发条件是"具体可验证事件"（非"业绩好转"等模糊描述）
□ 催化剂强度评级有具体理由支撑
□ 每个风险等级与描述的严重程度逻辑一致
□ 三大关键节点均有具体日期或可追踪指标

【ST股专项】
□ 涨跌幅限制标注为±5%
□ 区分"事先告知书"和"正式决定书"，摘帽时间从后者起算
□ 是否提示"最终处罚可能与事先告知书有差异"

【HTML排版】
□ 所有 {占位符} 已全部替换，无残留
□ KPI卡片数值与正文数据一致
□ 情景表：A行绿色(.sa)、B行黄色(.sb)、C行红色(.sc)
□ @media print 已包含 @page {size:A4; margin:14mm 12mm}
□ 无外部 CSS/JS 依赖（单文件，任何环境可打开）
```
