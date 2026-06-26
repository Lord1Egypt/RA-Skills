# 模板6：饼图/环形图

**尺寸**：1200×500 | **风格**：Neo-Brutalism

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1200px; height: 500px; background: #F5E6D3;
  padding: 40px; font-family: "PingFang SC", Arial, sans-serif;
  display: flex; gap: 60px; align-items: center;
}
.pie-container { width: 300px; height: 300px; position: relative; }
.pie {
  width: 300px; height: 300px; border-radius: 50%;
  background: conic-gradient(
    #E17055 0deg 126deg,
    #45B7AA 126deg 216deg,
    #D4A017 216deg 288deg,
    #5B8C5A 288deg 360deg
  );
  box-shadow: 6px 6px 0 #1A1A1A;
}
.pie-hole {
  position: absolute; top: 50%; left: 50%;
  width: 140px; height: 140px;
  background: #F5E6D3; border-radius: 50%;
  transform: translate(-50%, -50%);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.pie-hole-value { font-size: 28px; font-weight: 900; color: #1A1A1A; }
.pie-hole-label { font-size: 12px; color: #888; }
.legend { flex: 1; }
.title { font-size: 24px; font-weight: 800; color: #1A1A1A; margin-bottom: 30px; }
.legend-item {
  display: flex; align-items: center; gap: 16px;
  padding: 16px 0; border-bottom: 2px solid #E8DDD0;
}
.legend-color { width: 24px; height: 24px; border-radius: 6px; border: 2px solid #1A1A1A; }
.legend-info { flex: 1; }
.legend-name { font-size: 16px; font-weight: 700; color: #1A1A1A; }
.legend-value { font-size: 20px; font-weight: 900; color: #1A1A1A; }
.legend-pct { font-size: 14px; color: #888; }
</style>
</head>
<body>
  <div class="pie-container">
    <div class="pie"></div>
    <div class="pie-hole">
      <p class="pie-hole-value">¥730万</p>
      <p class="pie-hole-label">总销售额</p>
    </div>
  </div>
  <div class="legend">
    <p class="title">各品类销售占比</p>
    <div class="legend-item">
      <div class="legend-color" style="background: #E17055;"></div>
      <div class="legend-info">
        <p class="legend-name">美妆护肤</p>
      </div>
      <p class="legend-value">¥280万</p>
      <p class="legend-pct">38%</p>
    </div>
    <div class="legend-item">
      <div class="legend-color" style="background: #45B7AA;"></div>
      <div class="legend-info">
        <p class="legend-name">食品饮料</p>
      </div>
      <p class="legend-value">¥180万</p>
      <p class="legend-pct">25%</p>
    </div>
    <div class="legend-item">
      <div class="legend-color" style="background: #D4A017;"></div>
      <div class="legend-info">
        <p class="legend-name">服装配饰</p>
      </div>
      <p class="legend-value">¥150万</p>
      <p class="legend-pct">20%</p>
    </div>
    <div class="legend-item">
      <div class="legend-color" style="background: #5B8C5A;"></div>
      <div class="legend-info">
        <p class="legend-name">其他</p>
      </div>
      <p class="legend-value">¥120万</p>
      <p class="legend-pct">17%</p>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 占比分析
- 品类分布

---

## 使用方法

1. 复制 HTML 代码
2. 调整 conic-gradient 角度分配占比
3. 保存为 HTML 文件
4. 合成到总报告后截图
