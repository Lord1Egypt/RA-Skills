# 模板13：词云

**尺寸**：1200×600 | **风格**：Neo-Brutalism

> 用于展示关键词、标签、搜索热词等

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
.cloud-container {
  background: #FFFDF7; border: 4px solid #1A1A1A; border-radius: 12px;
  padding: 40px; box-shadow: 6px 6px 0 #1A1A1A;
  height: 480px; position: relative; display: flex; flex-wrap: wrap;
  align-items: center; justify-content: center; gap: 20px;
  overflow: hidden;
}
.cloud-word {
  display: inline-block; padding: 8px 16px; border-radius: 20px;
  font-weight: 700; white-space: nowrap;
}
.cloud-1 { font-size: 56px; color: #E17055; }
.cloud-2 { font-size: 44px; color: #45B7AA; }
.cloud-3 { font-size: 36px; color: #D4A017; }
.cloud-4 { font-size: 28px; color: #5B8C5A; }
.cloud-5 { font-size: 22px; color: #888; }
</style>
</head>
<body>
  <p class="title">用户搜索热词 TOP 20</p>
  <div class="cloud-container">
    <span class="cloud-word cloud-1">iPhone 15</span>
    <span class="cloud-word cloud-2">手机壳</span>
    <span class="cloud-word cloud-1">蓝牙耳机</span>
    <span class="cloud-word cloud-3">充电宝</span>
    <span class="cloud-word cloud-2">数据线</span>
    <span class="cloud-word cloud-4">平板电脑</span>
    <span class="cloud-word cloud-3">智能手表</span>
    <span class="cloud-word cloud-5">键盘</span>
    <span class="cloud-word cloud-2">笔记本电脑</span>
    <span class="cloud-word cloud-4">鼠标</span>
    <span class="cloud-word cloud-5">显示器</span>
    <span class="cloud-word cloud-3">移动硬盘</span>
    <span class="cloud-word cloud-5">U盘</span>
    <span class="cloud-word cloud-4">音箱</span>
    <span class="cloud-word cloud-5">路由器</span>
    <span class="cloud-word cloud-3">耳机</span>
    <span class="cloud-word cloud-4">相机</span>
    <span class="cloud-word cloud-5">游戏机</span>
    <span class="cloud-word cloud-5">散热器</span>
    <span class="cloud-word cloud-5">支架</span>
  </div>
</body>
</html>
```

---

## 适用场景

- 搜索热词
- 关键词分析
- 标签分布

---

## 使用方法

1. 复制 HTML 代码
2. 替换关键词文字和大小级别（cloud-1 最大，cloud-5 最小）
3. 保存为 HTML 文件
4. 合成到总报告后截图
