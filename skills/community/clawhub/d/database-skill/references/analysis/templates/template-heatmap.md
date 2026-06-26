# 模板12：热点图/热力图

**尺寸**：1200×600 | **风格**：Neo-Brutalism

> 用于展示交叉分析结果，如：时段×品类、地区×品类

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1200px; height: 600px; background: #F5E6D3;
  padding: 30px; font-family: "PingFang SC", Arial, sans-serif;
}
.title { font-size: 24px; font-weight: 800; color: #1A1A1A; margin-bottom: 20px; }
.heatmap { background: #FFFDF7; border: 4px solid #1A1A1A; border-radius: 12px; padding: 20px; box-shadow: 6px 6px 0 #1A1A1A; }
.heatmap-grid {
  display: grid;
  grid-template-columns: 100px repeat(5, 1fr);
  gap: 4px;
}
.heatmap-header {
  padding: 12px; text-align: center; font-weight: 700; font-size: 14px;
  background: #1A1A1A; color: #FFD700; border-radius: 4px;
}
.heatmap-row-label {
  padding: 12px; display: flex; align-items: center; font-weight: 700; font-size: 14px;
  background: #1A1A1A; color: #FFF; border-radius: 4px;
}
.heatmap-cell {
  padding: 16px; text-align: center; font-weight: 700; font-size: 14px;
  border-radius: 4px; color: #1A1A1A;
}
.heatmap-legend {
  display: flex; justify-content: center; gap: 20px; margin-top: 20px;
}
.heatmap-legend-item { display: flex; align-items: center; gap: 6px; font-size: 12px; }
.heatmap-legend-color { width: 20px; height: 20px; border-radius: 4px; }
</style>
</head>
<body>
  <p class="title">各品类时段销售热力图</p>
  <div class="heatmap">
    <div class="heatmap-grid">
      <!-- 表头 -->
      <div class="heatmap-header"></div>
      <div class="heatmap-header">美妆</div>
      <div class="heatmap-header">食品</div>
      <div class="heatmap-header">服饰</div>
      <div class="heatmap-header">数码</div>
      <div class="heatmap-header">家居</div>

      <!-- 第1行 -->
      <div class="heatmap-row-label">上午</div>
      <div class="heatmap-cell" style="background: #FFEBEE;">¥12万</div>
      <div class="heatmap-cell" style="background: #FFCDD2;">¥18万</div>
      <div class="heatmap-cell" style="background: #FFCDD2;">¥15万</div>
      <div class="heatmap-cell" style="background: #FFA726;">¥25万</div>
      <div class="heatmap-cell" style="background: #FFCC80;">¥22万</div>

      <!-- 第2行 -->
      <div class="heatmap-row-label">中午</div>
      <div class="heatmap-cell" style="background: #FFA726;">¥28万</div>
      <div class="heatmap-cell" style="background: #FF7043;">¥35万</div>
      <div class="heatmap-cell" style="background: #FFEBEE;">¥10万</div>
      <div class="heatmap-cell" style="background: #FFEBEE;">¥8万</div>
      <div class="heatmap-cell" style="background: #FFCDD2;">¥16万</div>

      <!-- 第3行 -->
      <div class="heatmap-row-label">下午</div>
      <div class="heatmap-cell" style="background: #FF7043;">¥42万</div>
      <div class="heatmap-cell" style="background: #FFA726;">¥26万</div>
      <div class="heatmap-cell" style="background: #FFCDD2;">¥14万</div>
      <div class="heatmap-cell" style="background: #FFCDD2;">¥12万</div>
      <div class="heatmap-cell" style="background: #FFA726;">¥30万</div>

      <!-- 第4行 -->
      <div class="heatmap-row-label">晚间</div>
      <div class="heatmap-cell" style="background: #EF5350; color: #FFF;">¥55万</div>
      <div class="heatmap-cell" style="background: #FF7043;">¥38万</div>
      <div class="heatmap-cell" style="background: #FF7043;">¥32万</div>
      <div class="heatmap-cell" style="background: #FFA726;">¥20万</div>
      <div class="heatmap-cell" style="background: #FF7043;">¥40万</div>
    </div>

    <div class="heatmap-legend">
      <div class="heatmap-legend-item">
        <div class="heatmap-legend-color" style="background: #EF5350;"></div>
        <span>高 (>40万)</span>
      </div>
      <div class="heatmap-legend-item">
        <div class="heatmap-legend-color" style="background: #FF7043;"></div>
        <span>中高 (30-40万)</span>
      </div>
      <div class="heatmap-legend-item">
        <div class="heatmap-legend-color" style="background: #FFA726;"></div>
        <span>中 (20-30万)</span>
      </div>
      <div class="heatmap-legend-item">
        <div class="heatmap-legend-color" style="background: #FFCDD2;"></div>
        <span>低 (10-20万)</span>
      </div>
      <div class="heatmap-legend-item">
        <div class="heatmap-legend-color" style="background: #FFEBEE;"></div>
        <span>极低 (<10万)</span>
      </div>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 交叉分析（时段×品类、地区×品类）
- 找出高/低组合

---

## 使用方法

1. 复制 HTML 代码
2. 替换数据值和背景颜色（颜色越深数值越高）
3. 保存为 HTML 文件
4. 合成到总报告后截图
