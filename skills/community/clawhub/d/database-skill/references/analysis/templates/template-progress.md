# 模板8：进度条/达成率

**尺寸**：1200×400 | **风格**：Neo-Brutalism

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1200px; height: 400px; background: #F5E6D3;
  padding: 40px; font-family: "PingFang SC", Arial, sans-serif;
}
.title { font-size: 24px; font-weight: 800; color: #1A1A1A; margin-bottom: 30px; }
.progress-item { margin-bottom: 24px; }
.progress-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
.progress-label { font-size: 16px; font-weight: 700; color: #1A1A1A; }
.progress-value { font-size: 16px; font-weight: 700; }
.progress-bar {
  height: 32px; background: #FFFDF7; border: 3px solid #1A1A1A;
  border-radius: 8px; overflow: hidden; position: relative;
}
.progress-fill { height: 100%; border-radius: 4px; }
.progress-target {
  position: absolute; top: 0; bottom: 0; width: 3px; background: #1A1A1A;
}
.progress-target-label {
  position: absolute; top: -20px; transform: translateX(-50%);
  font-size: 11px; color: #888;
}
</style>
</head>
<body>
  <p class="title">Q1 目标达成情况</p>
  <div class="progress-item">
    <div class="progress-header">
      <span class="progress-label">GMV 目标 1000万</span>
      <span class="progress-value" style="color: #4CAF50;">达成 85%</span>
    </div>
    <div class="progress-bar">
      <div class="progress-fill" style="width: 85%; background: #4CAF50;"></div>
      <div class="progress-target" style="left: 80%;"><span class="progress-target-label">80%</span></div>
    </div>
  </div>
  <div class="progress-item">
    <div class="progress-header">
      <span class="progress-label">新用户目标 10000人</span>
      <span class="progress-value" style="color: #E17055;">达成 62%</span>
    </div>
    <div class="progress-bar">
      <div class="progress-fill" style="width: 62%; background: #E17055;"></div>
      <div class="progress-target" style="left: 100%;"></div>
    </div>
  </div>
  <div class="progress-item">
    <div class="progress-header">
      <span class="progress-label">活跃用户目标 50000人</span>
      <span class="progress-value" style="color: #45B7AA;">达成 110%</span>
    </div>
    <div class="progress-bar">
      <div class="progress-fill" style="width: 100%; background: #45B7AA;"></div>
      <div class="progress-target" style="left: 100%;"><span class="progress-target-label">100%</span></div>
    </div>
  </div>
</body>
</html>
```

---

## 适用场景

- 目标达成情况
- KPI 进度展示

---

## 使用方法

1. 复制 HTML 代码
2. 调整进度条宽度（width %）
3. 保存为 HTML 文件
4. 合成到总报告后截图
