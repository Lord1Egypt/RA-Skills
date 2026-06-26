# 模板2：多板块对比表格

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
  padding: 30px; font-family: "PingFang SC", Arial, sans-serif;
}
.title { font-size: 24px; font-weight: 800; color: #1A1A1A; margin-bottom: 20px; }
table {
  width: 100%; border-collapse: separate; border-spacing: 0;
  border: 4px solid #1A1A1A; border-radius: 12px;
  overflow: hidden; box-shadow: 6px 6px 0 #1A1A1A;
  background: #FFFDF7;
}
th { background: #1A1A1A; color: #FFD700; padding: 14px 20px; font-size: 16px; font-weight: 700; text-align: left; }
td { padding: 14px 20px; font-size: 15px; color: #1A1A1A; border-bottom: 2px solid #E8DDD0; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: #FFF8E7; }
.tag { display: inline-block; padding: 3px 10px; border-radius: 6px; font-size: 13px; font-weight: 700; }
.tag-good { background: #D4EDDA; color: #155724; }
.tag-warn { background: #FFF3CD; color: #856404; }
.tag-bad { background: #F8D7DA; color: #721C24; }
.num-highlight { font-weight: 900; font-size: 18px; }
</style>
</head>
<body>
  <p class="title">各板块ROI与盈亏分析</p>
  <table>
    <tr><th><p>板块</p></th><th><p>GMV</p></th><th><p>消耗</p></th><th><p>ROI</p></th><th><p>退货率</p></th><th><p>状态</p></th></tr>
    <tr>
      <td><p>美妆·护肤</p></td>
      <td><p class="num-highlight">200万</p></td>
      <td><p>45万</p></td>
      <td><p class="num-highlight" style="color: #4CAF50;">3.8</p></td>
      <td><p>28%</p></td>
      <td><p><span class="tag tag-good">盈利</span></p></td>
    </tr>
    <tr>
      <td><p>食品</p></td>
      <td><p class="num-highlight">150万</p></td>
      <td><p>30万</p></td>
      <td><p class="num-highlight" style="color: #45B7AA;">2.5</p></td>
      <td><p>15%</p></td>
      <td><p><span class="tag tag-good">盈利</span></p></td>
    </tr>
    <tr>
      <td><p>服饰</p></td>
      <td><p class="num-highlight">300万</p></td>
      <td><p>80万</p></td>
      <td><p class="num-highlight" style="color: #FF3B4F;">1.1</p></td>
      <td><p style="color: #FF3B4F; font-weight: 700;">45%</p></td>
      <td><p><span class="tag tag-bad">亏损</span></p></td>
    </tr>
  </table>
</body>
</html>
```

---

## 适用场景

- 多维度对比
- 数据明细展示

---

## 使用方法

1. 复制 HTML 代码
2. 替换表格数据
3. 保存为 HTML 文件
4. 合成到总报告后截图
