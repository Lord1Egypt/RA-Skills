# 模板11：地图

**尺寸**：1200×600 | **风格**：Neo-Brutalism

> 基于中国地图的 regional 分布展示，以下只是按照中国地图为例子，如果是其他地区或者则按需去生成

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
.map-container { display: flex; gap: 30px; }
.map-area { flex: 2; background: #FFFDF7; border: 4px solid #1A1A1A; border-radius: 12px; padding: 20px; box-shadow: 6px 6px 0 #1A1A1A; position: relative; height: 480px; }
.map-legend { flex: 1; }
.map-bar {
  display: flex; align-items: center; margin-bottom: 16px; padding: 12px;
  background: #FFFDF7; border: 2px solid #1A1A1A; border-radius: 8px;
}
.map-bar-name { width: 80px; font-weight: 700; }
.map-bar-visual { flex: 1; height: 20px; background: #E8DDD0; border-radius: 4px; overflow: hidden; margin: 0 10px; }
.map-bar-fill { height: 100%; border-radius: 4px; }
.map-bar-value { width: 60px; text-align: right; font-weight: 700; }
</style>
</head>
<body>
  <p class="title">各地区销售分布</p>
  <div class="map-container">
    <div class="map-area">
      <!-- 使用 SVG 中国地图 -->
      <svg viewBox="0 0 800 600" style="width: 100%; height: 100%;">
        <!-- 地图区域 - 用色块表示 -->
        <rect x="50" y="200" width="120" height="100" fill="#E17055" opacity="0.8"/>
        <rect x="180" y="180" width="100" height="80" fill="#45B7AA" opacity="0.8"/>
        <rect x="290" y="160" width="140" height="120" fill="#4CAF50" opacity="0.8"/>
        <rect x="440" y="140" width="160" height="100" fill="#D4A017" opacity="0.8"/>
        <rect x="610" y="120" width="100" height="80" fill="#E17055" opacity="0.8"/>
        <!-- 标签 -->
        <text x="110" y="255" text-anchor="middle" fill="#FFF" font-size="14" font-weight="700">华北</text>
        <text x="230" y="225" text-anchor="middle" fill="#FFF" font-size="14" font-weight="700">华东</text>
        <text x="360" y="225" text-anchor="middle" fill="#FFF" font-size="14" font-weight="700">华南</text>
        <text x="520" y="195" text-anchor="middle" fill="#FFF" font-size="14" font-weight="700">西南</text>
        <text x="660" y="165" text-anchor="middle" fill="#FFF" font-size="14" font-weight="700">西北</text>
      </svg>
    </div>
    <div class="map-legend">
      <div class="map-bar">
        <span class="map-bar-name">华东</span>
        <div class="map-bar-visual"><div class="map-bar-fill" style="width: 85%; background: #4CAF50;"></div></div>
        <span class="map-bar-value">¥320万</span>
      </div>
      <div class="map-bar">
        <span class="map-bar-name">华南</span>
        <div class="map-bar-visual"><div class="map-bar-fill" style="width: 70%; background: #45B7AA;"></div></div>
        <span class="map-bar-value">¥260万</span>
      </div>
      <div class="map-bar">
        <span class="map-bar-name">华北</span>
        <div class="map-bar-visual"><div class="map-bar-fill" style="width: 55%; background: #E17055;"></div></div>
        <span class="map-bar-value">¥180万</span>
      </div>
      <div class="map-bar">
        <span class="map-bar-name">西南</span>
        <div class="map-bar-visual"><div class="map-bar-fill" style="width: 40%; background: #D4A017;"></div></div>
        <span class="map-bar-value">¥120万</span>
      </div>
      <div class="map-bar">
        <span class="map-bar-name">西北</span>
        <div class="map-bar-visual"><div class="map-bar-fill" style="width: 25%; background: #E17055;"></div></div>
        <span class="map-bar-value">¥80万</span>
      </div>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 地区销售分布
- 区域数据对比

---

## 使用方法

1. 复制 HTML 代码
2. 替换地图区域颜色和数据
3. 保存为 HTML 文件
4. 合成到总报告后截图
