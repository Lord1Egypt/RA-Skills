# dy-caption-skill

<div align="center">

**抖音视频语音转文字** - OpenClaw / AI Agent 技能

给一个抖音分享链接或分享文案，自动提取语音并转成文字。

</div>

---

## 功能特性

- **抖音链接转文字** - 粘贴分享文案即可
- **提取视频语音** - 自动解析视频和音频资源
- **转写结果输出** - 适合做字幕整理、爆款文案拆解、内容归档
- **余额查询** - 查看剩余点数
- **历史记录** - 查看最近的转写任务

## 安装技能

```bash
cd ~/.openclaw/workspace
git clone https://github.com/xwchris/dy-caption-skill.git skills/dy-caption
```

## 使用示例

| 你说 | AI 会做的 |
|------|-----------|
| “帮我提取这个抖音视频文案：<分享链接>” | 提交转写并返回文字结果 |
| “查询一下 dy-caption 余额” | 调用余额接口 |
| “看看我最近转写过哪些视频” | 返回历史任务 |

## 数据流向

本技能通过 `curl` 调用 `api.dycaption.cn` REST API，将分享链接 / 分享文案 与 API Key 发送到服务端处理。

## 相关链接

- CLI 工具：https://github.com/xwchris/douyin-caption-cli
- API 服务：https://api.dycaption.cn
- License：MIT
