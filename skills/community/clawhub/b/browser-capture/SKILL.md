---
name: browser-capture
description: 使用 OpenClaw Browser 抓取网页截图和图片，智能识别真正的图片内容
metadata:
  {
    "openclaw":
      {
        "emoji": "📸",
        "requires": { "openclaw": ">=0.15" },
      },
  }
---

# Browser Capture

使用 OpenClaw Browser 抓取网页截图和图片，智能识别真正的图片内容。

## 核心原则

- **只返回真正的图片**，不返回图标、头像、logo、按钮等小图标
- **优先抓取详情页大图**，而非缩略图列表
- **检查图片尺寸**，过滤掉小尺寸图标

## 功能

- **browser_screenshot** - 截取当前页面或指定页面截图
- **browser_open** - 打开网页
- **browser_navigate** - 导航到指定URL
- **browser_snapshot** - 获取页面ARIA快照（可提取图片链接）
- **browser_click** - 点击页面元素
- **browser_download** - 点击元素并下载结果
- **browser_evaluate** - 执行JS代码获取元素信息

## 快速开始

### 1. 确保浏览器已启动

```bash
openclaw browser start
```

### 2. 打开目标网页

```bash
openclaw browser open "https://example.com"
```

### 3. 等待页面加载

```bash
sleep 3
```

### 4. 获取页面元素快照

```bash
openclaw browser snapshot
```

返回页面的ARIA树状结构，包含所有可交互元素的ref编号。

### 5. 分析图片元素（关键步骤）

执行以下命令分析页面上的图片：

```bash
# 获取所有图片元素的信息（尺寸、src等）
openclaw browser evaluate --fn "() => {
  const images = Array.from(document.querySelectorAll('img')).map(img => ({
    src: img.src,
    width: img.naturalWidth || img.width,
    height: img.naturalHeight || img.height,
    alt: img.alt,
    class: img.className,
    parent: img.parentElement?.tagName,
    parentClass: img.parentElement?.className
  }));
  return JSON.stringify(images.slice(0, 10), null, 2);
}"
```

**判断真正图片的规则：**
- 宽度或高度 > 200px（过滤图标/头像）
- 不是网站的logo、图标、按钮图片
- 通常在 `ul`/`li` 列表或内容区域内

### 6. 点击进入详情页

根据分析结果，选择真正的图片链接进行点击：

```bash
# 点击图片进入详情页（根据snapshot返回的ref编号）
openclaw browser click e109
```

### 7. 在详情页抓取大图

详情页通常有"View larger"或直接显示大图，截图保存：

```bash
openclaw browser screenshot
```

### 8. 可选：点击查看最大分辨率

```bash
# 查找最大图链接
openclaw browser snapshot

# 点击最大分辨率链接
openclaw browser click e47
```

## 智能抓取图片流程（推荐）

以下是一个完整的智能抓取流程：先确认是图片 → 点击进入详情页 → 判断是否有更大图 → 保存最佳质量图片。

### 步骤 1：启动浏览器并打开页面

```bash
openclaw browser start
openclaw browser open "https://image.baidu.com"
sleep 3
```

### 步骤 2：获取页面快照，找到图片列表

```bash
openclaw browser snapshot
```

### 步骤 3：分析图片元素，过滤小图标

```bash
# 查找真正的图片（尺寸大于 300x200）
openclaw browser evaluate --fn "() => {
  const links = document.querySelectorAll('a[href*=\"image.baidu.com/front/aigc\"]');
  const results = [];
  links.forEach((link, i) => {
    const img = link.querySelector('img');
    if (img) {
      const w = img.naturalWidth || img.width;
      const h = img.naturalHeight || img.height;
      if (w > 300 && h > 200) {
        results.push({
          index: i,
          imgSrc: img.src,
          width: w,
          height: h
        });
      }
    }
  });
  return JSON.stringify(results.slice(0, 5), null, 2);
}"
```

### 步骤 4：点击第一张图片进入详情页

```bash
# 根据上一步的分析结果，点击对应的链接元素
# 先获取详情页的 snapshot 看看有没有可点击的元素
openclaw browser snapshot

# 点击图片本身（通常是第一个大图的父级链接）
# 需要根据实际页面结构调整 ref 编号
openclaw browser click e141
```

### 步骤 5：在详情页检查是否有更清晰的大图

等待页面加载后，执行以下命令检查：

```bash
# 检查详情页是否有更大尺寸的图片
openclaw browser evaluate --fn "() => {
  const images = Array.from(document.querySelectorAll('img'));
  const results = [];
  images.forEach((img, i) => {
    const w = img.naturalWidth || img.width;
    const h = img.naturalHeight || img.height;
    if (w > 800 || h > 600) {
      results.push({
        index: i,
        src: img.src,
        width: w,
        height: h
      });
    }
  });
  return JSON.stringify(results.slice(0, 3), null, 2);
}"
```

### 步骤 6：保存最佳质量的图片

如果详情页有大图，直接用 curl 下载：

```bash
# 下载大图
curl -L "图片URL" -o /path/to/save.jpg
```

如果详情页没有明显的大图，可以尝试：
1. 截图保存当前页面
2. 或者查找页面中的"查看原图"、"下载"等按钮点击

## 常见问题

### 如何判断哪个是真正的图片

执行 evaluate 命令分析图片尺寸：

```bash
openclaw browser evaluate --fn "() => {
  const images = document.querySelectorAll('img');
  const results = [];
  images.forEach((img, i) => {
    const w = img.naturalWidth || img.width;
    const h = img.naturalHeight || img.height;
    if (w > 200 || h > 200) {
      results.push({index: i, width: w, height: h, src: img.src.substring(0,80)});
    }
  });
  return JSON.stringify(results);
}"
```

只选择尺寸大于200x200的图片。

### browser命令报"tab not found"

有时浏览器状态同步会出问题，尝试：
1. 重新打开页面：`openclaw browser open <URL>`
2. 或重启浏览器：`openclaw browser stop && openclaw browser start`

### 页面被 Cloudflare 拦截

某些网站有 Cloudflare 安全验证，headless 浏览器可能无法通过。可以尝试：
1. 等待更长时间让验证通过
2. 使用代理服务访问

### 截图保存在哪里

默认保存在 `~/.openclaw/media/browser/`，可以手动复制到workspace：

```bash
cp ~/.openclaw/media/browser/xxx.png ~/workspace/
```

## 完整示例：智能抓取百度图片首页的大图

```bash
# 1. 启动浏览器并打开百度图片
openclaw browser start
openclaw browser open "https://image.baidu.com"
sleep 3

# 2. 获取页面中的图片列表（过滤小图标）
openclaw browser evaluate --fn "() => {
  const links = document.querySelectorAll('a[href*=\"image.baidu.com/front/aigc\"]');
  const results = [];
  links.forEach((link, i) => {
    const img = link.querySelector('img');
    if (img) {
      const w = img.naturalWidth || img.width;
      const h = img.naturalHeight || img.height;
      if (w > 300 && h > 200) {
        results.push({ index: i, src: img.src, width: w, height: h });
      }
    }
  });
  return JSON.stringify(results.slice(0, 5), null, 2);
}"

# 3. 点击第一张图片进入详情页
# 假设点击的是 e141（需要根据实际 snapshot 调整）
openclaw browser click e141

# 4. 等待详情页加载
sleep 3

# 5. 检查详情页是否有更大尺寸的图片
openclaw browser evaluate --fn "() => {
  const images = Array.from(document.querySelectorAll('img'));
  const bigImages = images
    .map(img => ({
      src: img.src,
      width: img.naturalWidth || img.width,
      height: img.naturalHeight || img.height
    }))
    .filter(img => img.width > 800 || img.height > 600);
  return JSON.stringify(bigImages.slice(0, 3), null, 2);
}"

# 6. 如果有大图，下载保存
# 假设获取到的第一个大图 URL 是: https://xxx.jpg
curl -L "大图URL" -o ~/workspace/baidu_big_image.jpg

# 7. 如果没有找到大图，直接截取当前页面
openclaw browser screenshot
```

## 判断大图的关键逻辑

| 页面类型 | 判断条件 | 处理方式 |
|---------|---------|---------|
| 图片列表页 | 缩略图通常 < 500px | 需要点击进入详情页 |
| 详情页 | 图片 > 800px | 直接下载 |
| 详情页 | 有"查看原图"按钮 | 点击后再下载最大图 |
| 详情页 | 仍是小图 | 截图保存当前页面 |

## 工具说明

| 工具 | 说明 | 示例 |
|------|------|------|
| browser_screenshot | 截取当前标签页截图 | `openclaw browser screenshot` |
| browser_open | 在新标签打开URL | `openclaw browser open "URL"` |
| browser_navigate | 当前标签导航 | `openclaw browser navigate "URL"` |
| browser_snapshot | 获取页面ARIA树 | `openclaw browser snapshot` |
| browser_click | 点击元素 | `openclaw browser click e109` |
| browser_evaluate | 执行JS获取元素详情 | 见上文示例 |
| browser_tabs | 列出所有标签 | `openclaw browser tabs` |
| browser_tab_select | 切换标签 | `openclaw browser tab select 1` |
