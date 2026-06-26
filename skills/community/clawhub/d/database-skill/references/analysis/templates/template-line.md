# 模板5：趋势折线图

**尺寸**：1200×500 | **风格**：Warm Narrative

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1200px; height: 500px; background: #FDF6EC;
  padding: 40px; font-family: "PingFang SC", Arial, sans-serif;
}
.title { font-size: 24px; font-weight: 700; color: #3D3D3D; margin-bottom: 6px; }
.subtitle { font-size: 14px; color: #999; margin-bottom: 30px; }
.chart-area {
  background: #FFFFFF; border: 1px solid #E8DDD0;
  border-radius: 16px; padding: 30px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  height: 340px; position: relative;
}
.chart { display: flex; align-items: flex-end; gap: 10px; height: 220px; padding-top: 20px; position: relative; }
.line {
  position: absolute; bottom: 20px; left: 50px; right: 30px; height: 180px;
}
.line-point { position: absolute; width: 10px; height: 10px; background: #E17055; border-radius: 50%; transform: translate(-50%, 50%); }
.line-label { font-size: 12px; color: #888; text-align: center; width: 40px; }
.grid-line { position: absolute; left: 50px; right: 30px; border-bottom: 1px dashed #E8DDD0; }
.grid-label { position: absolute; left: 10px; font-size: 11px; color: #999; transform: translateY(50%); }
.legend { display: flex; gap: 20px; margin-top: 20px; justify-content: center; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #666; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }
</style>
</head>
<body>
  <p class="title">月度销售趋势</p>
  <p class="subtitle">2025年1月 - 2025年12月</p>
  <div class="chart-area">
    <div class="grid-line" style="bottom: 100px;"><span class="grid-label">100万</span></div>
    <div class="grid-line" style="bottom: 60px;"><span class="grid-label">60万</span></div>
    <div class="grid-line" style="bottom: 20px;"><span class="grid-label">20万</span></div>
    <div class="chart">
      <div class="line">
        <div class="line-point" style="left: 5%; bottom: 30%;"></div>
        <div class="line-point" style="left: 14%; bottom: 45%;"></div>
        <div class="line-point" style="left: 23%; bottom: 40%;"></div>
        <div class="line-point" style="left: 32%; bottom: 55%;"></div>
        <div class="line-point" style="left: 41%; bottom: 50%;"></div>
        <div class="line-point" style="left: 50%; bottom: 70%;"></div>
        <div class="line-point" style="left: 59%; bottom: 65%;"></div>
        <div class="line-point" style="left: 68%; bottom: 80%;"></div>
        <div class="line-point" style="left: 77%; bottom: 75%;"></div>
        <div class="line-point" style="left: 86%; bottom: 90%;"></div>
        <div class="line-point" style="left: 95%; bottom: 85%;"></div>
      </div>
      <div class="line-label">1月</div>
      <div class="line-label">2月</div>
      <div class="line-label">3月</div>
      <div class="line-label">4月</div>
      <div class="line-label">5月</div>
      <div class="line-label">6月</div>
      <div class="line-label">7月</div>
      <div class="line-label">8月</div>
      <div class="line-label">9月</div>
      <div class="line-label">10月</div>
      <div class="line-label">11月</div>
      <div class="line-label">12月</div>
    </div>
    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background: #E17055;"></div>销售额</div>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 月度/季度趋势展示
- 时间序列分析

---

## 使用方法

1. 复制 HTML 代码
2. 替换数据点位置（调整 bottom 百分比）
3. 保存为 HTML 文件
4. 合成到总报告后截图
