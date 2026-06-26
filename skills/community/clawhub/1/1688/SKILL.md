---
name: 1688图片下载器
description: 从淘宝/1688下载商品图片。触发词：淘宝下载图片、1688下载图片、商品图片下载、淘宝主图、下载商品图、1688图片。支持通过商品名搜索或直接提供商品URL下载主图和详情图。
---

# 淘宝/1688 商品图片下载器

从淘宝、1688等电商平台下载商品图片到本地。

## 工作流程

### 方式一：通过商品URL下载

1. 用户提供商品页面URL
2. 使用浏览器打开页面
3. 快照获取页面内容
4. 提取图片URL
5. 下载保存

### 方式二：通过商品名搜索下载

1. 用户提供商品名称
2. 使用浏览器搜索淘宝/1688
3. 找到目标商品
4. 进入商品详情页
5. 提取并下载图片

## 使用方法

### 下载脚本

脚本位置: `scripts/download_images.py`

```bash
# 直接下载图片URL列表
python scripts/download_images.py --images /tmp/image_urls.txt --output ./商品图片

# 使用配置文件
python scripts/download_images.py --config /tmp/download_config.json
```

### 浏览器操作（推荐）

由于淘宝/1688有反爬机制，**必须使用浏览器**来访问和获取图片：

```javascript
// 使用 browser 工具打开商品页面
browser open --url "商品URL" --profile openclaw

// 获取页面快照，提取图片URL
browser snapshot

// 从快照中识别图片元素，提取src或data-src
```

## 图片保存位置

- 默认保存到: `~/.openclaw/sharespace/商品图片/{商品名}/`
- 主图命名: `main_01.jpg`, `main_02.jpg`, ...
- 详情图命名: `detail_01.jpg`, `detail_02.jpg`, ...

## 执行步骤

当用户请求下载商品图片时：

1. **确认信息**
   - 商品URL 或 商品名称
   - 是否需要详情图（默认只下载主图）
   - 保存目录（默认共享文件夹）

2. **打开浏览器**
   ```
   browser open --url "<商品URL>" --profile openclaw
   ```

3. **获取页面快照**
   ```
   browser snapshot
   ```

4. **提取图片URL**（关键步骤）

   1688的图片URL格式：
   - 主图: `https://cbu01.alicdn.com/img/ibank/O1CN01xxxxx_!!店铺ID-0-cib.jpg`
   - 颜色图: 同上，在颜色选择区域
   - 详情图: 需要从页面script标签或data-src中提取

   **正确提取方法：**
   ```javascript
   // 1. 获取所有img标签的src
   document.querySelectorAll('img').forEach(img => {
     const src = img.src;
     if (src.includes('cbu01.alicdn.com/img/ibank')) {
       images.push(src);
     }
   });
   
   // 2. 从script标签提取详情图（重要！）
   document.querySelectorAll('script').forEach(script => {
     const text = script.textContent;
     const matches = text.match(/https?:\/\/cbu01\.alicdn\.com\/img\/ibank[^"'\s]+/g);
     if (matches) detailImages.push(...matches);
   });
   ```
   
   **URL处理：**
   - 去掉 `.webp` 后缀获取原图
   - 去掉 `220x220.jpg`、`250x250.jpg`、`310x310.jpg` 等缩略图后缀
   - 详情图URL通常以 `!!3827449935-0-cib.jpg` 结尾

5. **创建保存目录**
   ```bash
   mkdir -p ~/.openclaw/sharespace/商品图片/{商品名}/{主图,颜色图,详情图}
   ```

6. **下载图片**
   - 使用 requests 下载，设置 Referer 头
   - 主图命名: `main_01.jpg`, `main_02.jpg`, ...
   - 颜色图命名: `color_01.jpg`, `color_02.jpg`, ...
   - 详情图命名: `detail_01.jpg`, `detail_02.jpg`, ...

7. **报告结果**
   - 下载成功数量
   - 每张图片的文件大小
   - 保存路径
   - 失败的图片（如有）

## 注意事项

- 淘宝/1688 需要登录才能查看部分内容
- 图片URL可能带有防盗链，需要设置 Referer
- 部分图片是懒加载，需要滚动触发
- 主图通常是 800x800 或更大的正方形图
- 详情图可能是长图，需要特别处理

## 示例对话

**用户**: 帮我下载这个商品的图片 https://detail.1688.com/offer/123456.html

**Agent**:
1. 打开浏览器访问该URL
2. 获取页面快照
3. 提取图片URL（找到5张主图，12张详情图）
4. 创建目录并下载
5. 报告: 已保存到 `~/.openclaw/sharespace/商品图片/商品名/`

**用户**: 帮我在淘宝搜"无线蓝牙耳机"下载主图

**Agent**:
1. 打开淘宝搜索页面
2. 搜索"无线蓝牙耳机"
3. 从搜索结果提取商品主图
4. 下载保存