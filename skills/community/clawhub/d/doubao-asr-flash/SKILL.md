---
name: doubao-asr
description: >-
  火山引擎豆包语音识别 API（录音文件极速版）。把本地音频/视频文件或公网音频
  URL 转成文字：录音转写、会议纪要、播客字幕、语音输入、视频伴音提取文字。
  一次 HTTP POST 返回结果，无需轮询。支持 WAV/MP3/OGG 直传，其他格式
  （m4a/flac/aac/视频等）自动用 ffmpeg 转码。Use whenever the user wants to
  转写/识别/听写 音频或视频中的语音，生成文字稿、字幕(SRT)、会议纪要等。
---

# Doubao ASR — 豆包语音识别（火山引擎 API）

把音频/视频里的语音转成文字，基于火山引擎豆包语音识别「录音文件极速版」
（`openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash`）。
中文识别业界领先（普通话/粤语/四川话等方言 + 13+ 语言）。

- **价格**：极速版 **4.5 元/小时**（按音频时长计费，按量后付费）
- **限制**：单文件 ≤ 2 小时、≤ 100MB；超过请先分段
- **返回**：全文 + 逐句时间戳（可导出 SRT 字幕）

## When to use

- 用户给了一个音频/视频文件（或 URL），要"转成文字/文稿/纪要/字幕"。
- 需要从会议录音、播客、采访、视频、语音消息里提取文字内容。
- 回答时**引用脚本输出**作为转写结果，不要凭空猜测。

## 配置（首次必做，一次性）

### 1. 获取 API Key（需火山引擎账号，约 5 分钟）

1. 打开 https://console.volcengine.com/speech/app （语音技术控制台），未注册先注册并**实名认证**。
2. 左侧"语音识别"→ 开通「录音文件识别」（会提示申请 `volc.bigasr.auc_turbo` 资源权限，按引导开通即可）。
3. 左侧「API Key 管理」→ 创建 API Key（记下这串 Key，UUID 格式）。
   - 若控制台布局有变，搜"API Key"即可；新版控制台的 Key 就是 `X-Api-Key`。

### 2. 把 Key 交给 pi 保存（三选一）

```bash
# 方式 A（推荐，持久）：写入配置文件
mkdir -p ~/.config/doubao-asr
cat > ~/.config/doubao-asr/config.json <<'EOF'
{"api_key": "你的API Key"}
EOF

# 方式 B：环境变量（当前 shell 有效）
export DOUBAO_ASR_API_KEY="你的API Key"

# 方式 C：每次调用临时传（不推荐）
python .../asr.py 音频.mp3 --api-key "你的API Key"
```

> 存储到 `~/.config/doubao-asr/config.json` 后，之后所有会话无需再传 Key。

## Usage

脚本位于 `scripts/asr.py`（相对 skill 目录），**用绝对路径调用**：

```bash
# 假设 skill 已安装到 <你的 skills 目录>/doubao-asr/（如 ~/.pi/agent/skills/doubao-asr 或 ~/.claude/skills/doubao-asr）
ASR="<你的 skills 目录>/doubao-asr/scripts/asr.py"
PYTHONIOENCODING=utf-8 python3 "$ASR" /path/to/录音.m4a            # 转文字
PYTHONIOENCODING=utf-8 python3 "$ASR" /path/to/会议.mp4            # 视频自动提取音频
PYTHONIOENCODING=utf-8 python3 "$ASR" https://example.com/a.mp3    # 公网 URL 直传
PYTHONIOENCODING=utf-8 python3 "$ASR" a.m4a --out /tmp/文字稿.txt  # 保存结果
PYTHONIOENCODING=utf-8 python3 "$ASR" a.m4a --json                 # 完整 JSON（含逐句时间戳）
PYTHONIOENCODING=utf-8 python3 "$ASR" a.m4a --srt --out a.srt      # 导出 SRT 字幕
```

默认输出纯文本全文；`--json` 输出含 `utterances`（每句起止时间）的完整响应。

## 处理流程（脚本自动）

1. 非 WAV/MP3/OGG 的格式（含一切视频）→ `ffmpeg -ar 16000 -ac 1 -b:a 64k` 转 mp3。
2. 本地文件 → base64 随请求上传；URL → 直传。
3. 一次 POST 返回 `result.text`（全文）和 `result.utterances`（逐句时间戳）。

## 常见错误（X-Api-Status-Code）

| 错误码 | 含义 | 处理 |
|--------|------|------|
| 20000000 | 成功 | - |
| 20000003 | 静音音频 | 检查录音是否为空 |
| 20000018 | 音频格式不正确 | 检查文件是否损坏/伪装扩展名 |
| 20000015 | 空音频 | - |
| 2xxxxxxx 鉴权/资源 | API Key 错/未开通资源 | 检查 Key、确认已开通 volc.bigasr.auc_turbo |
| HTTP 429 | QPS/并发超限 | 稍后重试 |

## 注意事项

- **隐私**：音频会上传到火山引擎处理；敏感内容请先确认。
- **超长音频**：>2h 需分段（可用 ffmpeg 按时间切割）或改用标准版异步接口。
- **音量/噪声**：环境嘈杂时识别率下降，可先降噪处理。
- **说话人分离**：极速版不支持；需要"发言人 A/B"分组的场景，可用标准版
  （enable_diarization）或让 LLM 根据内容二次整理。

## Dependencies

- Python 3 + requests（已装）
- ffmpeg（已装，/opt/homebrew/bin/ffmpeg；转码非直传格式时才需要）

## Environment

- `DOUBAO_ASR_API_KEY`（可选，有配置文件则不需要）
- 配置文件 `~/.config/doubao-asr/config.json`：`{"api_key": "..."}`
