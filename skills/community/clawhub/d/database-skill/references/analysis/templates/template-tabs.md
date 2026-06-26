# 模板10：多Tab切换报告

**尺寸**：1200×700 | **风格**：Neo-Brutalism

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1200px; height: 700px; background: #F5E6D3;
  padding: 30px; font-family: "PingFang SC", Arial, sans-serif;
}
.title { font-size: 24px; font-weight: 800; color: #1A1A1A; margin-bottom: 20px; }
.tabs { display: flex; gap: 8px; margin-bottom: 20px; }
.tab {
  padding: 12px 24px; background: #FFFDF7; border: 3px solid #1A1A1A;
  border-radius: 8px 8px 0 0; cursor: pointer; font-weight: 700;
  color: #1A1A1A;
}
.tab.active { background: #1A1A1A; color: #FFD700; }
.content { background: #FFFDF7; border: 4px solid #1A1A1A; border-radius: 0 12px 12px 12px; padding: 30px; box-shadow: 6px 6px 0 #1A1A1A; }
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.stat-card { text-align: center; padding: 20px; background: #F5E6D3; border-radius: 8px; }
.stat-value { font-size: 32px; font-weight: 900; color: #E17055; }
.stat-label { font-size: 14px; color: #666; margin-top: 4px; }
</style>
</head>
<body>
  <p class="title">综合运营报告</p>
  <div class="tabs">
    <div class="tab active">概览</div>
    <div class="tab">销售</div>
    <div class="tab">用户</div>
    <div class="tab">库存</div>
  </div>
  <div class="content">
    <div class="stat-grid">
      <div class="stat-card">
        <p class="stat-value">¥730万</p>
        <p class="stat-label">总GMV</p>
      </div>
      <div class="stat-card">
        <p class="stat-value">3.2</p>
        <p class="stat-label">整体ROI</p>
      </div>
      <div class="stat-card">
        <p class="stat-value">28%</p>
        <p class="stat-label">退货率</p>
      </div>
      <div class="stat-card">
        <p class="stat-value">50K</p>
        <p class="stat-label">订单数</p>
      </div>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 综合报告
- 多板块数据展示

---

## 使用方法

1. 复制 HTML 代码
2. 替换 Tab 和内容数据
3. 保存为 HTML 文件
4. 合成到总报告后截图
