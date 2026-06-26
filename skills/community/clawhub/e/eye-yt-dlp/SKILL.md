# yt-dlp 视频下载技能

## 功能描述
使用 yt-dlp 下载视频，支持 YouTube、B 站、推特、Instagram 等上千个网站。

## 触发条件
用户说"下载视频" + 视频链接时自动触发。

## 默认行为
- **下载目录**: `~/Movies`
- **画质**: 最高分辨率（bestvideo+bestaudio）
- **格式**: 合并为 mp4

## 使用方法

### 基本命令
```bash
yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 -P ~/Movies "视频链接"
```

### 常用参数
| 参数 | 说明 |
|------|------|
| `-f "bestvideo+bestaudio/best"` | 下载最高画质 |
| `--merge-output-format mp4` | 合并为 mp4 格式 |
| `-P ~/Movies` | 保存到 Movies 目录 |
| `-o "%(title)s.%(ext)s"` | 使用视频标题命名 |
| `--write-thumbnail` | 下载封面图 |
| `--write-sub` | 下载字幕 |
| `--sub-lang zh-Hans` | 下载中文字幕 |

## 示例

### 下载 YouTube 视频
```bash
yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 -P ~/Movies "https://www.youtube.com/watch?v=xxx"
```

### 下载 B 站视频
```bash
yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 -P ~/Movies "https://www.bilibili.com/video/BVxxx"
```

### 下载播放列表
```bash
yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 -P ~/Movies --yes-playlist "https://www.youtube.com/playlist?list=xxx"
```

## 注意事项
1. 某些网站可能需要 Cookie 或登录
2. 下载大文件时告知用户预计时间
3. 下载完成后告知用户文件位置
4. 如遇错误，显示具体错误信息并建议替代方案

## 错误处理
- **网站不支持**: 告知用户该网站不在支持列表中
- **需要登录**: 提示用户提供 Cookie 或账号
- **网络错误**: 建议检查网络或稍后重试
- **磁盘空间不足**: 提醒用户清理空间
