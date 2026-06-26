# 模板3：柱状图

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
.bar-chart { display: flex; align-items: flex-end; gap: 20px; height: 250px; padding-top: 20px; }
.bar-group { flex: 1; display: flex; flex-direction: column; align-items: center; }
.bar { width: 60px; border-radius: 8px 8px 0 0; }
.bar-label { font-size: 13px; color: #888; margin-top: 8px; }
.bar-value { font-size: 12px; font-weight: 700; color: #3D3D3D; margin-bottom: 4px; }
.baseline {
  position: absolute; left: 30px; right: 30px; bottom: 70px;
  border-bottom: 2px dashed #E8DDD0;
}
.baseline-label {
  position: absolute; right: 30px; bottom: 73px;
  font-size: 11px; color: #E17055;
}
</style>
</head>
<body>
  <p class="title">各板块ROI表现</p>
  <p class="subtitle">2026年1月 | 目标线：3.0</p>
  <div class="chart-area">
    <div class="baseline"></div>
    <p class="baseline-label">目标 3.0</p>
    <div class="bar-chart">
      <div class="bar-group">
        <p class="bar-value">3.8</p>
        <div class="bar" style="height: 190px; background: #4CAF50;"></div>
        <p class="bar-label">美妆</p>
      </div>
      <div class="bar-group">
        <p class="bar-value">2.5</p>
        <div class="bar" style="height: 125px; background: #45B7AA;"></div>
        <p class="bar-label">食品</p>
      </div>
      <div class="bar-group">
        <p class="bar-value">1.1</p>
        <div class="bar" style="height: 55px; background: #FF3B4F;"></div>
        <p class="bar-label">服饰</p>
      </div>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 趋势展示
- 类别对比

---

## 使用方法

1. 复制 HTML 代码
2. 替换柱状图数据（调整 height 百分比）
3. 保存为 HTML 文件
4. 合成到总报告后截图
