# HTML 报告输出模板

本文件给出财报深度解读报告的完整 HTML 模板。报告必须自包含（内联 CSS，零外链，离线可开）。

## 必需章节（13 个）

硬闸脚本检查报告中是否包含以下 13 个章节标题（以 `<h2>` 标签出现，id 属性匹配）：

| 序号 | 章节名 | id |
|------|--------|----|
| 1 | 核心结论 | `core-conclusion` |
| 2 | 业绩概览 | `overview` |
| 3 | 收入分析 | `revenue` |
| 4 | 毛利率分析 | `gross-margin` |
| 5 | 费用分析 | `expenses` |
| 6 | 盈利能力 | `profitability` |
| 7 | 现金流 | `cashflow` |
| 8 | 营运资本 | `working-capital` |
| 9 | 经营异常 | `anomalies` |
| 10 | 异常原因 | `anomaly-causes` |
| 11 | 风险 | `risks` |
| 12 | 投资含义 | `investment-implications` |
| 13 | 数据来源 | `data-sources` |

## HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{公司名}} {{报告期}} 财报深度解读</title>
<style>
  :root {
    --bg: #f8f9fa;
    --card: #ffffff;
    --primary: #1a3a5c;
    --accent: #2563eb;
    --text: #1f2937;
    --muted: #6b7280;
    --border: #e5e7eb;
    --red: #dc2626;
    --amber: #d97706;
    --green: #059669;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, "Segoe UI", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }
  .container { max-width: 900px; margin: 0 auto; padding: 24px 16px 80px; }
  .header { text-align: center; padding: 40px 0 32px; border-bottom: 2px solid var(--primary); margin-bottom: 32px; }
  .header h1 { font-size: 28px; color: var(--primary); margin-bottom: 8px; }
  .header .meta { color: var(--muted); font-size: 14px; }
  .header .meta span { margin: 0 8px; }
  section { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 24px; margin-bottom: 20px; }
  h2 { font-size: 20px; color: var(--primary); border-left: 4px solid var(--accent); padding-left: 12px; margin-bottom: 16px; }
  h3 { font-size: 16px; color: var(--text); margin: 16px 0 8px; }
  p { margin-bottom: 10px; }
  table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 14px; }
  th, td { padding: 8px 12px; border: 1px solid var(--border); text-align: left; }
  th { background: var(--primary); color: #fff; font-weight: 600; }
  tr:nth-child(even) { background: #f3f4f6; }
  .tag { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
  .tag-high { background: #fee2e2; color: var(--red); }
  .tag-mid { background: #fef3c7; color: var(--amber); }
  .tag-low { background: #d1fae5; color: var(--green); }
  .fact { background: #eff6ff; border-left: 3px solid var(--accent); padding: 8px 12px; margin: 8px 0; font-size: 14px; }
  .judgment { background: #fffbeb; border-left: 3px solid var(--amber); padding: 8px 12px; margin: 8px 0; font-size: 14px; }
  .conclusion-box { background: linear-gradient(135deg, #1a3a5c 0%, #2563eb 100%); color: #fff; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
  .conclusion-box h2 { color: #fff; border-left: none; padding: 0; }
  .conclusion-box ol { padding-left: 20px; }
  .conclusion-box li { margin-bottom: 8px; }
  .footer { text-align: center; color: var(--muted); font-size: 12px; padding: 20px 0; border-top: 1px solid var(--border); }
  .source-list { font-size: 13px; color: var(--muted); }
  .source-list li { margin-bottom: 4px; }
  @media print { body { background: #fff; } section { break-inside: avoid; } }
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>{{公司名}} {{报告期}} 财报深度解读</h1>
    <div class="meta">
      <span>报告期：{{报告期}}</span>·
      <span>生成日期：{{生成日期}}</span>·
      <span>数据来源：{{数据来源概述}}</span>
    </div>
  </div>

  <!-- 1. 核心结论 -->
  <div class="conclusion-box">
    <h2 id="core-conclusion">核心结论</h2>
    <ol>
      <li>{{结论1}}</li>
      <li>{{结论2}}</li>
      <li>{{结论3}}</li>
    </ol>
  </div>

  <!-- 2. 业绩概览 -->
  <section>
    <h2 id="overview">业绩概览</h2>
    <table>
      <tr><th>指标</th><th>本期</th><th>同比变化</th><th>环比变化</th></tr>
      <tr><td>营业总收入</td><td>{{值}}</td><td>{{值}}</td><td>{{值}}</td></tr>
      <tr><td>归母净利润</td><td>{{值}}</td><td>{{值}}</td><td>{{值}}</td></tr>
      <tr><td>扣非净利润</td><td>{{值}}</td><td>{{值}}</td><td>{{值}}</td></tr>
      <tr><td>经营现金流净额</td><td>{{值}}</td><td>{{值}}</td><td>{{值}}</td></tr>
      <tr><td>毛利率</td><td>{{值}}</td><td>{{值}}</td><td>{{值}}</td></tr>
      <tr><td>净利率</td><td>{{值}}</td><td>{{值}}</td><td>{{值}}</td></tr>
    </table>
    <div class="fact">【事实】{{业绩概览事实描述}}</div>
    <div class="judgment">【判断】{{是否超预期判断}}</div>
  </section>

  <!-- 3. 收入分析 -->
  <section>
    <h2 id="revenue">收入分析</h2>
    <!-- 填入收入分析内容 -->
  </section>

  <!-- 4. 毛利率分析 -->
  <section>
    <h2 id="gross-margin">毛利率分析</h2>
    <!-- 填入毛利率分析内容 -->
  </section>

  <!-- 5. 费用分析 -->
  <section>
    <h2 id="expenses">费用分析</h2>
    <!-- 填入费用分析内容 -->
  </section>

  <!-- 6. 盈利能力 -->
  <section>
    <h2 id="profitability">盈利能力</h2>
    <!-- 填入盈利能力分析内容 -->
  </section>

  <!-- 7. 现金流 -->
  <section>
    <h2 id="cashflow">现金流</h2>
    <!-- 填入现金流分析内容 -->
  </section>

  <!-- 8. 营运资本 -->
  <section>
    <h2 id="working-capital">营运资本</h2>
    <!-- 填入营运资本分析内容 -->
  </section>

  <!-- 9. 经营异常 -->
  <section>
    <h2 id="anomalies">经营异常</h2>
    <!-- 填入触发的异常，每条按 anomaly-checklist.md 的格式写 -->
  </section>

  <!-- 10. 异常原因 -->
  <section>
    <h2 id="anomaly-causes">异常原因</h2>
    <!-- 填入每条异常的可能原因分析 -->
  </section>

  <!-- 11. 风险 -->
  <section>
    <h2 id="risks">风险</h2>
    <ul>
      <li>{{风险1}}</li>
      <li>{{风险2}}</li>
      <li>{{风险3}}</li>
    </ul>
  </section>

  <!-- 12. 投资含义 -->
  <section>
    <h2 id="investment-implications">投资含义</h2>
    <div class="fact">【事实】{{财报反映的经营事实}}</div>
    <div class="judgment">【判断】{{对投资逻辑的影响判断}}</div>
    <p>注：本节不构成买入/卖出建议，仅分析财报对投资逻辑的影响。</p>
  </section>

  <!-- 13. 数据来源 -->
  <section>
    <h2 id="data-sources">数据来源</h2>
    <ul class="source-list">
      <li>{{来源1：用户提供财报文件}}</li>
      <li>{{来源2：web_search 检索，日期}}</li>
    </ul>
  </section>

  <div class="footer">
    <p>本报告由财报深度解读助手生成。报告中的「事实」为财报数据，「判断」为分析观点，不构成投资建议。</p>
  </div>

</div>
</body>
</html>
```

## 填写规则

1. `{{...}}` 占位符必须全部替换为实际内容，不得保留占位符。
2. 每个章节必须有实质内容（至少一段文字或一个表格），不能只有标题。
3. 事实与判断用 `.fact` 和 `.judgment` 样式块区分。
4. 异常节的每条触发异常按 `references/anomaly-checklist.md` 的格式写。
5. 数据来源节列出所有数据来源（用户提供的文件、web_search 检索的来源及日期）。
6. 报告文件名：`<公司名>_<报告期>_财报解读.html`，写入 `outputs/`。
