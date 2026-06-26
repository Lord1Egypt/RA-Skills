# 豆包 TTS 技能

用火山引擎豆包 TTS 把文字转成语音，支持多种音色、情感、语速调节。

## 快速开始

### 1. 安装技能

```bash
npx skills add <your-username>/doubao-tts -g
```

### 2. 申请火山引擎凭证

1. 访问 https://www.volcengine.com/
2. 注册/登录账号
3. 进入控制台 → 语音技术 → 语音合成
4. 创建应用，获取：
   - **AppID**
   - **Access Token**
   - **Cluster**（集群 ID）

### 3. 创建配置文件

创建 `~/.openclaw/doubao-tts-config.json`：

```json
{
  "appid": "你的 AppID",
  "access_token": "你的 Access Token",
  "cluster": "volcano_tts",
  "voice_type": "BV700_streaming",
  "emotion": "pleased"
}
```

### 4. 使用技能

```
朗读 "今天天气不错"
帮我把这段话转成语音：你好，欢迎使用豆包 TTS
用声音读出来：欢迎回家
```

## 功能特性

- ✅ **多种音色** — 支持 20+ 种豆包音色
- ✅ **自动情感** — 根据内容自动选择合适的情感
- ✅ **参数调节** — 支持语速、音量、音调调节
- ✅ **自动播放** — 生成后自动播放音频

## 音色推荐

| 音色名称 | voice_type | 特点 |
|---------|------------|------|
| 灿灿 | BV700_streaming | 22 种情感，最全能（默认） |
| 擎苍 | BV701_streaming | 旁白模式，适合读文章 |
| 通用女声 | BV001_streaming | 日常对话 |
| 通用男声 | BV002_streaming | 基础男声 |

## 常见问题

### Q: Access Token 在哪里获取？

A: 火山引擎控制台 → 语音技术 → 语音合成 → 应用管理 → 创建应用

### Q: 音频播放失败？

A: 检查系统音频输出，Mac 使用 `afplay`，Linux 使用 `paplay`

### Q: Token 过期了怎么办？

A: 在火山引擎控制台重新生成 Access Token，更新配置文件

## 依赖

- `jq` — JSON 处理
- `curl` — HTTP 请求
- `base64` — 音频解码
- `afplay` (Mac) / `paplay` (Linux) — 音频播放

## 许可证

MIT

## 支持

遇到问题？提 Issue 或联系作者。
