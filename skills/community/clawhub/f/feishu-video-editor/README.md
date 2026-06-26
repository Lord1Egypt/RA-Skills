# feishu-video-editor

AI 视频剪辑 Skill - MVP 版本

## 功能特性

- ✅ 飞书云空间视频上传/下载
- ✅ 语音转文字（Whisper）
- ✅ 基于文字定位视频片段
- ✅ 视频裁剪（FFmpeg）
- ✅ 静音片段自动删除
- ✅ 剪辑结果自动上传

## 快速开始

1. 安装依赖：`npm install`
2. 安装 FFmpeg：`apt install ffmpeg` 或 `brew install ffmpeg`
3. 配置 Skill
4. 开始剪辑

## 使用示例

```
@视频助手 把这个视频中的静音部分剪掉
@视频助手 提取 00:01:30 到 00:02:45 的片段
@视频助手 生成这个视频的字幕
```

详细文档见 SKILL.md
