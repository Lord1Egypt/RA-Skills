---
name: bloomberg-headlines
description: 读取彭博社(Bloomberg)最新头条新闻。当用户想查看彭博社新闻、财经头条、Bloomberg headlines、最新市场资讯时使用此skill。
metadata:
  {
    "openclaw":
      {
        "emoji": "🆕",
        "os": ["darwin"],
        "requires": { "bins": ["bbgwire"] },
        "install":
          [
            {
              "id": "go",
              "kind": "go",
              "module": "github.com/8treenet/bbgwire@latest",
              "bins": ["bbgwire"],
              "label": "Install bbgwire (go)",
            },
          ],
      },
  }
---

# 彭博社头条新闻

读取彭博社最新的头条新闻。

## 使用方法

执行以下命令获取新闻：

```bash
bbgwire
```

该命令返回JSON格式的新闻列表，每条新闻包含：
- `Content`: 新闻标题（中文）
- `URL`: 新闻链接
- `Published`: 发布时间（ISO 8601格式）

## 输出格式

将新闻整理为易读的格式呈现给用户：

1. **标题**: 新闻标题内容
   - 链接: URL
   - 发布时间: 本地化时间显示

默认显示最新的50条新闻。

## 示例输出

```
彭博社最新头条 (共50条)

1. 雪佛龙表示，惠特斯通天然气设施受损将影响重启
   链接: https://www.bloomberg.com/news/articles/...
   发布: 2026-03-29 17:36

2. 美国在导弹袭击中首次损失一架珍贵的E-3预警机
   链接: https://www.bloomberg.com/news/articles/...
   发布: 2026-03-29 17:28
...
```

## 注意事项
- 新闻内容为中文翻译版本
- 时间会转换为本地时区显示
