---
name: doubao-tts
version: 2.0.0
description: >-
  将文本或 Markdown 文件合成为高质量语音音频，基于火山引擎（Volcengine）
  V3 异步长文本合成接口。支持情感设置、SSML 标记、字幕时间戳同步输出。
  适用于有声书制作、哄睡故事合成、批量音频生产等场景。
  当用户需要将文本转换为语音、TTS 合成、朗读文本时使用。
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - VOLCENGINE_APP_ID
        - VOLCENGINE_ACCESS_TOKEN
    primaryEnv: VOLCENGINE_ACCESS_TOKEN
---

# 豆包 TTS - 火山引擎语音合成 (V3 API)

将文本或 Markdown 文件合成为高质量语音音频，支持异步长文本合成（最高 10 万字符）。

## 前置条件

1. 用户需要在[火山引擎控制台](https://console.volcengine.com/)开通**语音合成**服务
2. 创建应用，获取 `APP ID` 和 `Access Token`
3. 确保已配置 `VOLCENGINE_APP_ID` 和 `VOLCENGINE_ACCESS_TOKEN` 环境变量

## 安装

```bash
bash {baseDir}/install.sh
```

非交互模式：

```bash
bash {baseDir}/install.sh --app-id <your_app_id> --access-token <your_access_token>
```

## 使用方式

### 基础合成

```bash
python3 {baseDir}/scripts/tts.py "你好，这是一段测试文本"
```

### 合成 Markdown 文件

```bash
python3 {baseDir}/scripts/tts.py "<markdown_file_path>"
```

### 指定音色和输出

```bash
python3 {baseDir}/scripts/tts.py "<file_or_text>" --voice-type BV700_streaming --output story.mp3
```

### 启用字幕时间戳

```bash
python3 {baseDir}/scripts/tts.py "<file_or_text>" --subtitle
```

### 设置情感

```bash
python3 {baseDir}/scripts/tts.py "<file_or_text>" --emotion happy --emotion-scale 4
```

### 使用 SSML（仅模型 1.0）

```bash
python3 {baseDir}/scripts/tts.py "<file_or_text>" --ssml --model 1.0
```

### 完整参数组合

```bash
python3 {baseDir}/scripts/tts.py story.md \
  --voice-type zh_female_chancan_v2_h5 \
  --format mp3 \
  --sample-rate 24000 \
  --output story.mp3 \
  --subtitle \
  --emotion happy \
  --model 1.0
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 文本内容或文件路径（必填） | - |
| `--voice-type, -v` | 音色 ID | zh_female_chancan_v2_h5 |
| `--format, -f` | 音频格式 mp3/wav/pcm/ogg_opus | mp3 |
| `--sample-rate` | 采样率 | 24000 |
| `--output, -o` | 输出文件路径 | 自动生成 |
| `--ssml` | 文本格式为 SSML（仅模型 1.0） | false |
| `--emotion` | 情感设置 happy/sad/angry 等 | 无 |
| `--emotion-scale` | 情绪强度 1~5 | 4 |
| `--subtitle` | 启用字幕时间戳 | false |
| `--speed` | 语速 [-50,100] | 0 |
| `--volume` | 音量 [-50,100] | 0 |
| `--model` | 模型版本 1.0/2.0 | 1.0 |
| `--timeout` | 最长等待秒数 | 1800 |

## API 版本说明

本 Skill 使用 V3 API（`/api/v3/tts/submit` + `/api/v3/tts/query`），鉴权通过以下 Header：

- `X-Api-App-Id`: 应用 ID
- `X-Api-Access-Key`: Access Token
- `X-Api-Resource-Id`: 资源 ID（模型 1.0 用 `seed-tts-1.0`，模型 2.0 用 `seed-tts-2.0`）

## 注意事项

- 模型 2.0 暂不支持 SSML
- SSML 闭合标签内字符数不能超过 150 个
- 合成音频在服务端保存 7 天，下载链接有效期 1 小时
- submit 和 query 接口共享并发配额

## 配置说明

环境变量加载优先级：

1. **全局配置**: `~/.config/doubao-tts/.env`
2. **项目目录**: 当前工作目录下的 `.env`
3. **系统环境变量**

## 错误处理

| 错误码 | 说明 |
|--------|------|
| 20000000 | 成功 |
| 40000000 | 请求参数错误 |
| 40000001 | 任务不存在或已过期 |
| 45000000 | 音色鉴权失败或并发限流 |
| 55000000 | 服务端错误 |

## 规则

- 始终通过 `{baseDir}` 引用脚本路径
- 合成前确认环境变量已配置
- 首次使用前需运行 `bash {baseDir}/install.sh`
