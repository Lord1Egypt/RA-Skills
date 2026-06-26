# 模板4：问题诊断卡片

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
.cards { display: flex; gap: 20px; }
.diagnosis-card {
  flex: 1; border: 4px solid #1A1A1A; border-radius: 12px;
  overflow: hidden; box-shadow: 6px 6px 0 #1A1A1A;
}
.card-header { padding: 16px 20px; }
.header-red { background: #FF3B4F; }
.header-gold { background: #FFD700; }
.header-green { background: #4CAF50; }
.card-header h2 { color: #1A1A1A; font-size: 18px; font-weight: 800; }
.header-red h2 { color: #FFFDF7; }
.card-body { background: #FFFDF7; padding: 20px; }
.card-body ul { list-style: none; padding: 0; }
.card-body li {
  font-size: 14px; color: #1A1A1A; line-height: 1.8;
  padding: 6px 0; border-bottom: 1px solid #F0E8DD;
}
.card-body li:last-child { border-bottom: none; }
.priority-tag {
  display: inline-block; background: #1A1A1A; color: #FFD700;
  padding: 2px 8px; border-radius: 4px; font-size: 11px;
  font-weight: 700; margin-right: 6px;
}
</style>
</head>
<body>
  <p class="title">投放问题诊断与优化建议</p>
  <div class="cards">
    <div class="diagnosis-card">
      <div class="card-header header-red"><h2>问题（需立即处理）</h2></div>
      <div class="card-body">
        <ul>
          <li><p><span class="priority-tag">P0</span>服饰板块ROI 1.1，低于盈亏线</p></li>
          <li><p><span class="priority-tag">P0</span>退货率45%导致实际GMV缩水近半</p></li>
        </ul>
      </div>
    </div>
    <div class="diagnosis-card">
      <div class="card-header header-gold"><h2>建议（本周执行）</h2></div>
      <div class="card-body">
        <ul>
          <li><p><span class="priority-tag">1</span>服饰板块暂停ROI&lt;1的计划</p></li>
          <li><p><span class="priority-tag">2</span>美妆板块预算上调20%</p></li>
        </ul>
      </div>
    </div>
    <div class="diagnosis-card">
      <div class="card-header header-green"><h2>亮点（继续保持）</h2></div>
      <div class="card-body">
        <ul>
          <li><p>美妆ROI 3.8，超目标27%</p></li>
          <li><p>食品退货率仅15%</p></li>
        </ul>
      </div>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 问题诊断
- 优化建议展示

---

## 使用方法

1. 复制 HTML 代码
2. 替换问题/建议/亮点内容
3. 保存为 HTML 文件
4. 合成到总报告后截图
