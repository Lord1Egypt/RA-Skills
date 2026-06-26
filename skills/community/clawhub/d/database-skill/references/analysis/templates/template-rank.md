# 模板9：排名榜单

**尺寸**：1200×600 | **风格**：Neo-Brutalism

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1200px; height: 600px; background: #F5E6D3;
  padding: 40px; font-family: "PingFang SC", Arial, sans-serif;
}
.title { font-size: 24px; font-weight: 800; color: #1A1A1A; margin-bottom: 20px; }
.rank-list { background: #FFFDF7; border: 4px solid #1A1A1A; border-radius: 12px; overflow: hidden; box-shadow: 6px 6px 0 #1A1A1A; }
.rank-item {
  display: flex; align-items: center; padding: 16px 24px;
  border-bottom: 2px solid #E8DDD0;
}
.rank-item:last-child { border-bottom: none; }
.rank-num {
  width: 40px; height: 40px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 900; margin-right: 20px;
}
.rank-num-1 { background: #FFD700; color: #1A1A1A; }
.rank-num-2 { background: #C0C0C0; color: #1A1A1A; }
.rank-num-3 { background: #CD7F32; color: #FFF; }
.rank-num-other { background: #E8DDD0; color: #1A1A1A; }
.rank-info { flex: 1; }
.rank-name { font-size: 16px; font-weight: 700; color: #1A1A1A; }
.rank-sub { font-size: 13px; color: #888; }
.rank-value { font-size: 20px; font-weight: 900; color: #1A1A1A; }
</style>
</head>
<body>
  <p class="title">销售排行榜 TOP 10</p>
  <div class="rank-list">
    <div class="rank-item">
      <div class="rank-num rank-num-1">1</div>
      <div class="rank-info">
        <p class="rank-name">北京市</p>
        <p class="rank-sub">华北区域</p>
      </div>
      <p class="rank-value">¥128万</p>
    </div>
    <div class="rank-item">
      <div class="rank-num rank-num-2">2</div>
      <div class="rank-info">
        <p class="rank-name">上海市</p>
        <p class="rank-sub">华东区域</p>
      </div>
      <p class="rank-value">¥96万</p>
    </div>
    <div class="rank-item">
      <div class="rank-num rank-num-3">3</div>
      <div class="rank-info">
        <p class="rank-name">广州市</p>
        <p class="rank-sub">华南区域</p>
      </div>
      <p class="rank-value">¥85万</p>
    </div>
    <div class="rank-item">
      <div class="rank-num rank-num-other">4</div>
      <div class="rank-info">
        <p class="rank-name">深圳市</p>
        <p class="rank-sub">华南区域</p>
      </div>
      <p class="rank-value">¥72万</p>
    </div>
    <div class="rank-item">
      <div class="rank-num rank-num-other">5</div>
      <div class="rank-info">
        <p class="rank-name">杭州市</p>
        <p class="rank-sub">华东区域</p>
      </div>
      <p class="rank-value">¥65万</p>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- TOP N 排名
- 排行榜展示

---

## 使用方法

1. 复制 HTML 代码
2. 替换排名数据
3. 保存为 HTML 文件
4. 合成到总报告后截图
