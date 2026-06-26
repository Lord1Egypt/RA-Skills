---
name: article-to-feishu
description: |
  将网页文章转换为飞书文档，支持今日头条、博客园、微信公众号、CSDN 等多种网站。自动下载图片并按原文顺序插入。
  
  **当用户要求以下操作时使用**：
  - "把这篇文章转成飞书文档"
  - "导入文章到飞书"
  - "保存网页到飞书"
  - "把链接转成文档"
  
  **支持的网站**：
  - 今日头条 (m.toutiao.com, www.toutiao.com)
  - 博客园 (www.cnblogs.com)
  - CSDN (blog.csdn.net)
  - 微信公众号 (mp.weixin.qq.com)
  - 简书 (jianshu.com)
  - 知乎 (zhihu.com)
  - 其他公开网页
---

# 网页文章转飞书文档

将任意网页文章转换为飞书云文档，自动处理图片防盗链并按原文顺序插入图片。

## 🚀 快速开始

```bash
# 1. 下载文章图片（自动处理防盗链）
bash {baseDir}/scripts/download_article_images.sh "$ARTICLE_URL" /tmp/article-img/

# 2. 获取文章内容
curl -sL "$ARTICLE_URL" | grep -oP '<title>.*</title>'
# 或使用 web_fetch 工具

# 3. AI Agent 分段构建文档
# - feishu_create_doc 创建文档
# - feishu_update_doc mode=append 追加文字
# - feishu_doc_media action=insert 插入图片
```

---

## 📖 工作流程

```
┌─────────────────┐
│  1. 获取文章内容  │  web_fetch 或 curl
└────────┬────────┘
         ▼
┌─────────────────┐
│  2. 提取图片 URL │  grep 或专用脚本
└────────┬────────┘
         ▼
┌─────────────────┐
│  3. 下载图片本地 │  带 Referer 防盗链
└────────┬────────┘
         ▼
┌─────────────────┐
│  4. 创建文档     │  feishu_create_doc
└────────┬────────┘
         ▼
┌─────────────────┐
│  5. 分段构建     │  文字 → 图片 → 文字...
└────────┬────────┘
         ▼
┌─────────────────┐
│  6. 清理临时文件 │  rm -rf /tmp/article-img/
└─────────────────┘
```

---

## 🔧 工具脚本

### download_article_images.sh

**通用图片下载器**，自动检测网站并设置正确的 Referer。

```bash
bash {baseDir}/scripts/download_article_images.sh <article_url> <output_dir> [referer]
```

**示例**：
```bash
# 博客园文章
bash {baseDir}/scripts/download_article_images.sh "https://www.cnblogs.com/xxx/p/123" /tmp/img/

# 今日头条
bash {baseDir}/scripts/download_article_images.sh "https://m.toutiao.com/is/xxx/" /tmp/img/

# 自定义 Referer
bash {baseDir}/scripts/download_article_images.sh "$URL" /tmp/img/ "https://example.com/"
```

**自动识别的网站**：
| 网站 | Referer |
|------|---------|
| 今日头条 | `https://www.toutiao.com/` |
| 博客园 | `https://www.cnblogs.com/` |
| CSDN | `https://blog.csdn.net/` |
| 微信公众号 | `https://mp.weixin.qq.com/` |
| 简书 | `https://www.jianshu.com/` |
| 知乎 | `https://zhuanlan.zhihu.com/` |

### fetch_article.sh

使用 **Jina AI Reader** 获取文章内容（适合有反爬的网站）。

```bash
bash {baseDir}/scripts/fetch_article.sh "https://m.toutiao.com/is/xxx/"
```

### extract_images.sh

从文章中提取图片 URL。

```bash
bash {baseDir}/scripts/extract_images.sh "https://m.toutiao.com/is/xxx/"
```

### download_images.sh

今日头条专用图片下载器。

```bash
bash {baseDir}/scripts/download_images.sh "https://m.toutiao.com/is/xxx/" /tmp/img/
```

---

## 📝 分段构建文档（核心）

### 原则

**文字 + 图片交替追加，确保图片出现在正确位置**

```
1. feishu_create_doc     → 创建文档，写标题和开头
2. feishu_update_doc     → 追加第一段文字
3. feishu_doc_media      → 插入第一张图片
4. feishu_update_doc     → 追加第二段文字
5. feishu_doc_media      → 插入第二张图片
... 循环直到完成
```

### 完整示例

```
# 步骤 1: 下载图片
bash {baseDir}/scripts/download_article_images.sh "$URL" /tmp/article-img/
# 输出: 01.jpg, 02.jpg, 03.jpg...

# 步骤 2: 创建文档
feishu_create_doc title="文章标题" markdown="文章开头..."

# 步骤 3: 追加第一段
feishu_update_doc doc_id="xxx" mode=append markdown="## 章节1\n\n说明文字..."

# 步骤 4: 插入图片
feishu_doc_media action=insert doc_id="xxx" file_path="/tmp/article-img/01.jpg" type=image align=center

# 步骤 5: 继续追加
feishu_update_doc doc_id="xxx" mode=append markdown="更多内容..."

# 步骤 6: 插入更多图片...
feishu_doc_media action=insert doc_id="xxx" file_path="/tmp/article-img/02.jpg" type=image align=center

# 步骤 7: 清理
rm -rf /tmp/article-img/
```

---

## 🖼️ 图片处理策略

### 策略选择

| 场景 | 策略 | 说明 |
|------|------|------|
| 图片 URL 可公开访问 | `<image url="..."/>` | 简单快捷 |
| 图片有防盗链 | 下载后上传 | 必须！ |
| 图片 URL 有时效 | 下载后上传 | 尽快处理 |
| 不确定 | 下载后上传 | 最安全 |

### URL 直接引用

```markdown
<image url="https://example.com/image.png" align="center" caption="描述"/>
```

系统自动下载并上传到飞书。

### 本地图片上传（防盗链必须）

```json
{
  "action": "insert",
  "doc_id": "xxx",
  "file_path": "/tmp/article-img/01.jpg",
  "type": "image",
  "align": "center"
}
```

---

## ⚠️ 注意事项

1. **防盗链**：大多数网站图片需要带 `Referer` 头，用脚本自动处理
2. **图片顺序**：按原文顺序命名（01.jpg, 02.jpg...）
3. **分段构建**：`feishu_doc_media insert` 只能追加到末尾
4. **临时清理**：完成后删除临时图片目录
5. **图片大小**：飞书限制 20MB 以内

---

## 🐛 常见问题

### 图片显示不出来？

**原因**：防盗链或 URL 过期

**解决**：使用 `download_article_images.sh` 下载后上传

### 图片顺序错乱？

**原因**：提取 URL 时用了 `sort -u` 打乱顺序

**解决**：脚本已按出现顺序下载，文件名按序号命名

### 下载失败？

```bash
# 手动测试，检查 Referer
curl -sL -H "Referer: https://www.toutiao.com/" "$IMG_URL" -o test.jpg
```

---

## 📋 各网站特性

| 网站 | 反爬 | 防盗链 | 推荐方案 |
|------|------|--------|---------|
| 今日头条 | 强 | 有 | Jina Reader + 下载图片 |
| 博客园 | 弱 | 有 | curl + 下载图片 |
| CSDN | 中 | 有 | Jina Reader + 下载图片 |
| 微信公众号 | 强 | 有 | Jina Reader + 下载图片 |
| 简书 | 弱 | 无 | 直接获取 |
| 知乎 | 中 | 有 | 下载图片 |