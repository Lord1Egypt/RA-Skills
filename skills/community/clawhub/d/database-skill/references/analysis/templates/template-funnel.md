# 模板7：漏斗图

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
.title { font-size: 24px; font-weight: 800; color: #1A1A1A; margin-bottom: 40px; }
.funnel { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.funnel-step {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 30px; border: 4px solid #1A1A1A;
  border-radius: 8px; box-shadow: 4px 4px 0 #1A1A1A;
  background: #FFFDF7;
}
.funnel-step-1 { width: 800px; }
.funnel-step-2 { width: 640px; }
.funnel-step-3 { width: 480px; }
.funnel-step-4 { width: 320px; }
.funnel-label { font-size: 18px; font-weight: 700; color: #1A1A1A; }
.funnel-value { font-size: 24px; font-weight: 900; }
.funnel-rate { font-size: 14px; color: #888; margin-right: 10px; }
</style>
</head>
<body>
  <p class="title">用户转化漏斗</p>
  <div class="funnel">
    <div class="funnel-step funnel-step-1">
      <span class="funnel-label">访问用户</span>
      <span class="funnel-rate">100%</span>
      <span class="funnel-value" style="color: #E17055;">50,000</span>
    </div>
    <div class="funnel-step funnel-step-2">
      <span class="funnel-label">浏览商品</span>
      <span class="funnel-rate">60%</span>
      <span class="funnel-value" style="color: #45B7AA;">30,000</span>
    </div>
    <div class="funnel-step funnel-step-3">
      <span class="funnel-label">加入购物车</span>
      <span class="funnel-rate">25%</span>
      <span class="funnel-value" style="color: #D4A017;">12,500</span>
    </div>
    <div class="funnel-step funnel-step-4">
      <span class="funnel-label">完成订单</span>
      <span class="funnel-rate">10%</span>
      <span class="funnel-value" style="color: #5B8C5A;">5,000</span>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 转化率分析
- 流程分析

---

## 使用方法

1. 复制 HTML 代码
2. 调整漏斗宽度和数值
3. 保存为 HTML 文件
4. 合成到总报告后截图
