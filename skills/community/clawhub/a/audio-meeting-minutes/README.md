# 熠小听 · 会议录音自动转文字 + AI 总结

将会议录音放入文件夹 → 语音识别 → AI 提炼纪要 → 输出专业 HTML 会议纪要。

> ⚠️ **隐私声明**：本技能会将会议录音上传至**阿里云 NLS** 云端进行语音识别处理。
> 请勿处理含有机密或受监管内容的录音。使用短期 AccessToken（24h），
> 不要将长期密钥粘贴到聊天窗口。

## 核心能力

| 环节 | 技术方案 | 速度 |
|------|---------|------|
| 语音识别 | 阿里云 NLS 云端识别 | ~1 分钟 / 20 分钟音频 |
| AI 总结 | WorkBuddy 内置 AI（无需额外 Key） | 即时 |
| HTML 输出 | 企业级商务模板 | 即时 |

## 支持格式

mp3 / m4a / wav / ogg / flac / aac / wma / opus / webm

## 安装

在 WorkBuddy 中新建任务 → 发送 `.skill` 文件作为附件 → 输入「帮我安装这个 skill」。

## 首次使用需要准备

- **NLS AppKey**：[获取链接](https://nls-portal.console.aliyun.com/applist) — 创建项目后获得
- **NLS AccessToken**：[获取链接](https://nls-portal.console.aliyun.com/applist) — 项目详情 → AccessToken 标签（24h 有效）

无需配置 AI Key，AI 总结由 WorkBuddy 内置完成。

## 使用

安装后在 WorkBuddy 中输入「**熠小听**」三个字即可触发。AI 会引导你完成首次配置。
