# 模板1：KPI指标看板（4指标）

**尺寸**：1200×400 | **风格**：Neo-Brutalism

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1200px; height: 400px; background: #F5E6D3;
  padding: 30px; font-family: "PingFang SC", Arial, sans-serif;
  display: flex; flex-direction: column;
}
.title { font-size: 24px; font-weight: 800; color: #1A1A1A; margin-bottom: 20px; }
.row { display: flex; gap: 20px; flex: 1; }
.card {
  flex: 1; background: #FFFDF7; border: 4px solid #1A1A1A;
  border-radius: 12px; padding: 20px;
  box-shadow: 6px 6px 0 #1A1A1A;
  display: flex; flex-direction: column; justify-content: center;
  text-align: center;
}
.card-value { font-size: 52px; font-weight: 900; }
.card-label { font-size: 16px; color: #888; margin-top: 6px; }
.card-change { font-size: 14px; margin-top: 4px; }
.v-coral { color: #E17055; }
.v-mint { color: #45B7AA; }
.v-gold { color: #D4A017; }
.v-olive { color: #5B8C5A; }
.up { color: #4CAF50; }
.down { color: #FF3B4F; }
</style>
</head>
<body>
  <p class="title">2026年1月 投放数据概览</p>
  <div class="row">
    <div class="card">
      <p class="card-value v-coral">3.2</p>
      <p class="card-label">整体ROI</p>
      <p class="card-change up">↑ 0.4 vs 上月</p>
    </div>
    <div class="card">
      <p class="card-value v-mint">730万</p>
      <p class="card-label">总GMV</p>
      <p class="card-change up">↑ 12%</p>
    </div>
    <div class="card">
      <p class="card-value v-gold">16%</p>
      <p class="card-label">消耗占比</p>
      <p class="card-change up">↓ 2pt</p>
    </div>
    <div class="card">
      <p class="card-value v-olive">28%</p>
      <p class="card-label">退货率</p>
      <p class="card-change down">↑ 3pt</p>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 数据概览 / 周报开头
- 关键指标展示

---

## 使用方法

1. 复制 HTML 代码
2. 替换数据值和标签
3. 保存为 HTML 文件
4. 合成到总报告后截图
