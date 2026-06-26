---
name: bili-video-downloader
description: 下载 B 站视频到指定目录。使用 yt-dlp，必须用 -o 参数指定完整路径，否则默认下载到 C 盘。
metadata:
  {
    "openclaw":
      {
        "emoji": "📺",
        "requires": { "bins": ["yt-dlp"] },
        "install":
          [
            {
              "id": "pip-yt-dlp",
              "kind": "pip",
              "package": "yt-dlp",
              "bins": ["yt-dlp"],
              "label": "Install yt-dlp (pip)",
            },
          ],
      },
  }
---

# B站视频下载器

使用 yt-dlp 下载 Bilibili 视频。

## ⚠️ 关键规则

**必须用 `-o` 参数指定完整路径，不能省略！**

```bash
# ✅ 正确：-o 指定目标目录
yt-dlp -o "/path/to/videos/%(title)s.%(ext)s" "<url>"

# ❌ 错误：省略 -o，默认下载到当前工作目录（C盘/系统盘）
yt-dlp "<url>"
```

## 使用方式

用户提供：
1. **B 站 URL**（视频页或合集链接）
2. **保存路径**（不提供则询问）

执行命令格式：
```bash
mkdir -Force "<目标目录>" | Out-Null
yt-dlp -o "<目标目录>/%(title)s.%(ext)s" "<url>"
```

## 示例

**用户说 "下载到 D:\Videos\bili"：**
```bash
mkdir -Force D:\Videos\bili | Out-Null
yt-dlp -o "D:\Videos\bili\%(title)s.%(ext)s" "<B站视频URL>"
```

**用户说 "下载到 ~/Videos/bili"：**
```bash
mkdir -Force ~/Videos/bili | Out-Null
yt-dlp -o "~/Videos/bili/%(title)s.%(ext)s" "<url>"
```

**合集下载：**
```bash
yt-dlp -o "<目录>/%(title)s.%(ext)s" "https://space.bilibili.com/xxx/lists/5374469?type=season"
```

## 技术细节

- yt-dlp 默认行为 ≠ 下载到指定目录，**必须显式指定 `-o` 完整路径**
- 合集约 45 个视频，可能有 2-5 个 extractor error（B站接口限制，非路径问题）
- 文件名使用视频原标题（`%(title)s`）
- 完成后汇总成功/失败数量

## 常见问题

**Q: 某些视频下载失败？**
→ B站部分视频需要登录/会员，extractor error 是接口限制，非本 skill 问题。

**Q: 路径怎么填？**
→ 告诉用户先创建目录，执行时带上完整路径参数。
