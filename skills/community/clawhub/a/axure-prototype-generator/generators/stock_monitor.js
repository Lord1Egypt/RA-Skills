/**
 * 股票监控页面生成器
 * 输出 Axure 兼容的 JavaScript 格式
 */

function generateStockMonitor() {
  const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>股票监控大盘</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:"Microsoft YaHei",Arial,sans-serif;}
body{background:#f0f2f5;padding:20px;}
.header{background:#fff;padding:20px;margin-bottom:20px;border-radius:4px;}
.title{font-size:24px;font-weight:bold;color:#333;margin-bottom:10px;}
.subtitle{color:#999;font-size:14px;}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:20px;}
.card{background:#fff;padding:20px;border-radius:4px;}
.card-label{color:#999;font-size:13px;margin-bottom:10px;}
.card-value{font-size:28px;font-weight:bold;color:#333;}
.card-value.up{color:#f44336;}
.card-value.down{color:#4caf50;}
.table-panel{background:#fff;border-radius:4px;overflow:hidden;}
.table-header{display:grid;grid-template-columns:150px 120px 120px 120px 120px 100px;padding:15px 20px;background:#fafafa;border-bottom:1px solid #e8e8e8;font-weight:bold;color:#333;font-size:14px;}
.table-row{display:grid;grid-template-columns:150px 120px 120px 120px 120px 100px;padding:20px;border-bottom:1px solid #f0f0f0;}
.table-row:hover{background:#fafafa;}
.stock-name{color:#333;font-size:14px;font-weight:500;}
.stock-code{color:#999;font-size:12px;margin-top:5px;}
.price{font-size:14px;font-weight:500;}
.price.up{color:#f44336;}
.price.down{color:#4caf50;}
.change{font-size:14px;}
.change.up{color:#f44336;}
.change.down{color:#4caf50;}
.volume{color:#666;font-size:14px;}
.amount{color:#666;font-size:14px;}
.btn-action{padding:5px 15px;border:none;border-radius:2px;font-size:12px;cursor:pointer;}
.btn-buy{background:#f44336;color:#fff;}
.btn-sell{background:#4caf50;color:#fff;}
</style>
</head>
<body>
<div class="header">
<div class="title">股票监控大盘</div>
<div class="subtitle">实时更新 · 三维策略 · 智能预警</div>
</div>
<div class="cards">
<div class="card">
<div class="card-label">总市值</div>
<div class="card-value">86.76 万</div>
</div>
<div class="card">
<div class="card-label">总盈亏</div>
<div class="card-value up">+20.50</div>
</div>
<div class="card">
<div class="card-label">收益率</div>
<div class="card-value up">+0.21%</div>
</div>
<div class="card">
<div class="card-label">仓位</div>
<div class="card-value">28.9%</div>
</div>
</div>
<div class="table-panel">
<div class="table-header">
<div>股票名称</div>
<div>现价</div>
<div>涨跌</div>
<div>成交量</div>
<div>成交额</div>
<div>操作</div>
</div>
<div class="table-row">
<div>
<div class="stock-name">闻泰科技</div>
<div class="stock-code">sh600745</div>
</div>
<div class="price up">33.11</div>
<div class="change up">+1.38%</div>
<div class="volume">12.5 万手</div>
<div class="amount">4.1 亿</div>
<div><button class="btn-action btn-buy">买入</button></div>
</div>
<div class="table-row">
<div>
<div class="stock-name">太龙药业</div>
<div class="stock-code">sh600222</div>
</div>
<div class="price down">7.32</div>
<div class="change down">-0.68%</div>
<div class="volume">8.3 万手</div>
<div class="amount">6.1 千万</div>
<div><button class="btn-action btn-buy">买入</button></div>
</div>
<div class="table-row">
<div>
<div class="stock-name">亿晶光电</div>
<div class="stock-code">sh600537</div>
</div>
<div class="price">3.46</div>
<div class="change">0.00%</div>
<div class="volume">5.2 万手</div>
<div class="amount">1.8 千万</div>
<div><button class="btn-action btn-buy">买入</button></div>
</div>
</div>
</body>
</html>`;

  // 转换为 document.writeln() 格式
  const lines = html.split('\n').map(line => `document.writeln("${line.replace(/"/g, '\\"')}");`).join('\n');
  return `javascript:\n${lines}`;
}

module.exports = { generateStockMonitor };
