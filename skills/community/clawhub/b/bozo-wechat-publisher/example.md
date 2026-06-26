---
title: wechat-publisher 使用指南
cover: ./assets/logo.png
description: 将 Markdown 格式的文章发布至微信公众号草稿箱，并使用与 文颜 相同的主题系统进行排版。
author: 波哥
source_url: https://www.slas.cc
---

# wechat-publisher 使用指南

欢迎使用 **wechat-publisher** skill！这是一篇功能演示文章，展示如何使用本 skill 发布 Markdown 到微信公众号。

## 📋 目录

- [核心功能](#核心功能)
- [两种发布方案](#两种发布方案)
- [Markdown 格式要求](#markdown-格式要求)
- [代码高亮示例](#代码高亮示例)
- [图片处理](#图片处理)
- [常见问题](#常见问题)

## 核心功能

### 1. Markdown 自动转换

标准 Markdown 自动转换为微信公众号格式，支持：

- ✅ 标题层级（H1-H6）
- ✅ 列表（有序/无序）
- ✅ 引用块
- ✅ 代码块（带高亮）
- ✅ 表格
- ✅ 链接和图片
- ✅ 数学公式
- ✅ 分隔线

### 2. 图片自动上传

**本地图片**: 自动上传到微信图床
```markdown
![本地图片](./assets/example.png)
```

**网络图片**: 自动下载并上传
```markdown
![网络图片](https://example.com/image.jpg)
```

### 3. 一键发布

两种发布方案供你选择：

---

## 两种发布方案

### 方案一：wenyan-cli（推荐）

**适用环境**: Node.js 18 及以下

**优点**:
- 完整的排版支持
- 精美的代码高亮
- 多种主题选择
- Mac 风格代码块

**发布命令**:
```bash
# 使用默认主题
wenyan publish -f example.md

# 指定主题
wenyan publish -f example.md -t lapis -h solarized-light

# 关闭 Mac 风格
wenyan publish -f example.md -t lapis --no-mac-style
```

### 方案二：curl 备用方案

**适用环境**: 任何 Node.js 版本

**优点**:
- 兼容所有 Node.js 版本
- 不需要额外依赖
- 简单可靠

**发布命令**:
```bash
./scripts/publish-curl.sh example.md
```

---

## Markdown 格式要求

### Frontmatter（必填）

文章顶部**必须**包含 frontmatter：

```markdown
---
title: 文章标题（必填）
cover: 封面图路径或 URL（必填）
author: 作者名称（可选）
source_url: 原文链接（可选）
---
```

**字段说明**:
| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| title | ✅ | 文章标题 | `我的技术文章` |
| cover | ✅ | 封面图 | `./assets/cover.jpg` 或 `https://...` |
| author | ❌ | 作者名称 | `张三` |
| source_url | ❌ | 原文链接 | `https://myblog.com/post` |

---

## 代码高亮示例

### JavaScript

```javascript
function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet("WeChat"));
```

### Python

```python
def publish_article(title, content):
    """发布文章到微信公众号"""
    return {
        'title': title,
        'content': content,
        'status': 'published'
    }

result = publish_article('测试文章', '内容...')
print(result)
```

### Bash

```bash
# 发布文章
wenyan publish -f article.md -t lapis -h solarized-light

# 检查发布状态
echo "发布完成！"
```

---

## 图片处理

### 支持的图片格式

- ✅ JPEG / JPG
- ✅ PNG
- ✅ GIF
- ✅ WebP

### 封面图建议

**推荐尺寸**: 1080 × 864 像素（5:4 比例）

**文件大小**: 建议 < 500KB

### 引用方式

**相对路径**（推荐）:
```markdown
cover: ./assets/cover.jpg
![](./images/example.png)
```

**绝对路径**:
```markdown
cover: /Users/yourname/Pictures/cover.jpg
![](/absolute/path/to/image.png)
```

**网络 URL**:
```markdown
cover: https://cdn.example.com/cover.jpg
![](https://example.com/image.jpg)
```

---

## 常见问题

### Q: wenyan-cli 报 "fetch failed"？

**A**: 这是 Node.js 20/24 的兼容性问题。

**解决方案**:
```bash
# 方案 1: 使用 Node.js 18
nvm install 18 && nvm use 18

# 方案 2: 使用 curl 备用方案
./scripts/publish-curl.sh article.md
```

### Q: IP 不在白名单？

**A**: 获取当前 IP 并添加到公众号后台：

```bash
# 获取 IP
curl ifconfig.me

# 登录添加
# https://mp.weixin.qq.com/ → 开发 → 基本配置 → IP 白名单
```

### Q: 封面图上传失败？

**A**: 检查以下几点：
1. 图片路径是否正确
2. 图片尺寸是否合理（建议 1080×864）
3. 图片大小是否 < 2MB
4. 图片格式是否支持（JPG/PNG）

---

## 发布流程总结

```
┌─────────────────┐
│  准备 Markdown  │
│  (含 frontmatter)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  选择发布方案    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐  ┌──────────┐
│wenyan   │  │  curl    │
│ -cli    │  │  脚本    │
│(Node18) │  │ (任何版本)│
└────┬────┘  └────┬─────┘
     │            │
     └──────┬─────┘
            ▼
     ┌──────────────┐
     │ 发布到草稿箱  │
     └──────────────┘
            │
            ▼
     ┌──────────────┐
     │ 公众号后台    │
     │ 审核并发布   │
     └──────────────┘
```

---

## 开始使用

1. **配置环境**
   ```bash
   export WECHAT_APP_ID=your_app_id
   export WECHAT_APP_SECRET=your_app_secret
   ```

2. **准备文章**
   - 创建 Markdown 文件
   - 添加 frontmatter
   - 编写内容

3. **发布**
   ```bash
   # 优先尝试 wenyan-cli
   wenyan publish -f your-article.md

   # 如有问题，使用 curl 方案
   ./scripts/publish-curl.sh your-article.md
   ```

4. **查看结果**
   - 登录 https://mp.weixin.qq.com/
   - 进入草稿箱
   - 审核并发布

---

**🎉 恭喜！你已经掌握了 wechat-publisher 的使用方法！**

开始创作你的第一篇公众号文章吧！
