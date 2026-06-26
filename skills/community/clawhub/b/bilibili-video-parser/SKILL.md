---
name: bilibili-video-parser
description: 下载并解析B站视频。当需要执行分析视频内容等需要理解视频视觉信息时调用该技能
metadata: {"clawdbot":{"emoji":"📺","requires":{"bins":["yt-dlp"],"env":["YT_DLP_PATH"]},"primaryEnv":"YT_DLP_PATH"}}

---

# Bilibili Video Parser

## 使用方法

### 注意
所有B站单条视频分析的需求，如果通过该技能无法执行，请直接通知用户错误内容，**永远不要**尝试使用web_fetch之类的工具去重试！

### 前置检查

1. 检查当前是否支持yt-dlp指令：
2. 检查当前是否支持yt-dlp指令：
   - 如果不支持指令，可选择查看环境变量YT_DLP_PATH，如果该环境变量有值，则后续所有对yt-dlp的调用都替换为该路径

```bash
yt-dlp --version
```

如果没有，直接终止并引导用户先至 https://github.com/yt-dlp/yt-dlp 进行安装

2. 检查当前是否有`doubao-video-analyze`技能，如果没有，尝试先安装该技能

### 视频链接获取

0. 解析出视频的BV号，优先进行检查你的workspace目录下的./bilibili/videos目录下，是否已存在`{BV_ID}.mp4`，如果已存在，则直接进入`分析视频`步骤
1. 如果已知视频链接，则直接进入`下载视频`步骤
2. 如果知道视频的BV号，如`BV1s4ZLBAE22`，则直接按照如下规则拼接：
   `https://www.bilibili.com/video/BV1s4ZLBAE22`
3. 如果既没有视频链接，也没有BV号，则直接终止，并向用户询问视频链接或BV号

### 下载视频

0. 如果是已知路径的本地视频，则可以直接跳过该步骤，直接进入`分析视频`步骤
1. 需要将视频通过yt-dlp先下载至你的workspace目录下的./bilibili/videos目录下。如果找不到该目录，则先创建该目录

```bash
yt-dlp -P {YOUR_WORKSPACE_DIR}/bilibili/videos -I 1 -o "{BV_ID}.mp4" {video_url}
```

2. 该命令会打印出该文件的路径，你需要通过该行日志记住该路径

```bash
[Merger] Merging formats into "xxx\bilibili\videos\{BV_ID}.mp4"
```

3. 如果下载出错，直接终止任务，不要再继续进行其他尝试

### 分析视频

调用`doubao-video-analyze`技能分析该视频，直接使用该技能的结果