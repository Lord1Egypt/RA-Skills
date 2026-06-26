---
name: article-image
description: 文章配图推荐。根据文章主题和内容，推荐合适的图片来源、搜索关键词和风格建议，帮助用户找到符合文章意境的配图。当用户提到「配图」「找图」「文章图片」「封面图」「插图」时激活。
---

# 文章配图推荐 Skill

## 功能概述
根据文章主题和内容，智能推荐配图方案，包括图片来源、搜索关键词、风格建议等。**推荐仅供参考，最终由用户决定是否采纳。**

## 激活方式

用户可以说：
- "帮我找几张配图"
- "这篇文章用什么图片好"
- "推荐一个封面图"
- "找一张 xxx 相关的图片"
- "这篇文章配什么图合适"

## 配图来源（推荐列表）

### 免费图库（可商用，部分需署名）
| 图库 | 特点 | 版权说明 |
|------|------|---------|
| Unsplash | 高质量自然/人文/科技 | 商业免费，需署名 |
| Pexels | 丰富多样，商用免费 | 商业免费，无需署名 |
| Pixabay | 涵盖广，中文友好 | 商业免费，需署名 |
| pixiv | 日系插画风格 | 需查看具体授权 |
| Dribbble | 设计感强 | 需查看具体授权 |

### 中文图库
- 站酷 (ZCOOL)：设计/创意类
- 花瓣网：灵感收集
- 阿里图标库：图标/插图

### 付费图库（高质量）
- Shutterstock
- Getty Images
- 视觉中国

## 搜索关键词推荐

### 按主题（英文关键词）
| 文章主题 | 推荐关键词 |
|----------|-----------|
| 科技/互联网 | technology, AI, digital, coding, innovation |
| 商业/职场 | business, office, professional, meeting |
| 生活方式 | lifestyle, coffee, nature, travel, minimalist |
| 教育/学习 | education, books, library, student, learning |
| 金融/投资 | finance, investment, chart, growth, economic |
| 健康/健身 | health, fitness, yoga, wellness, exercise |
| 社会/情感 | people, emotions, connections, relationships |

### 按风格
- 扁平化：flat, minimal, clean
- 渐变风：gradient, colorful, modern
- 插画风：illustration, vector, hand-drawn
- 真实摄影：photo, realistic, photography
- 抽象风：abstract, pattern, geometric

### 组合搜索技巧
```
"主题 + 风格"  例如："technology minimal"
"site:unsplash.com 关键词"
"关键词 -unwanted"  排除不需要的元素
```

## 配图原则

### 相关性
- 图片与文章主题相关
- 突出文章核心观点
- 不使用无关配图装饰

### 视觉层次
- 封面图：大气、有点击欲
- 文中图：缓解阅读疲劳，承接段落
- 题图：简洁、点题

### 版权合规（重要！）
- 商业用途优先选 CC0 或商用免费图库
- 部分图库需署名，输出时提醒用户
- 付费图库需确认授权范围
- **用户使用推荐配图前，需自行确认版权**

### 尺寸参考
- 封面：1920×1080 或 1200×630
- 文中图：800×450 或 16:9
- 题图：正方形或 1:1

## 输出格式

推荐时按以下结构输出（用户确认后再执行）：

```
【配图推荐】

📌 适用场景：封面图 / 文中插图

🔍 推荐关键词：
   - 英文：xxx, xxx, xxx
   - 中文：xxx

🖼️ 推荐图库：
   - 图库名（版权说明）

📐 建议尺寸：1200×630（封面）/ 800×450（文中）

⚠️ 版权提示：使用前请确认图库授权要求
```

**注意：不自动下载图片，只推荐方案。用户确认后按需自行搜索下载。**

## 输出示例

用户问："Python 异步编程教程用什么配图好"

输出：
```
【配图推荐】

📌 适用场景：封面图 + 文中插图

🔍 推荐关键词：
   - 英文：Python async code, programming workflow, server architecture
   - 中文：Python异步，代码流程，技术架构

🖼️ 推荐图库：
   - Unsplash（商业免费，需署名）
   - Pexels（商用免费，无需署名）

📐 建议尺寸：1200×630（封面）

⚠️ 版权提示：Unsplash 要求署名来源，Pexels 无需署名
```

## 禁止行为

- ❌ 不自动下载保存图片到本地
- ❌ 不代替用户执行搜索操作
- ❌ 不写死任何个人路径（如 C:\Users\xxx）
- ❌ 不承诺"保证找到"或"一定可用"

## 适用说明

本 skill 仅提供配图方案推荐，不替代用户决策。使用任何图片前，请自行确认版权授权是否符合你的用途。