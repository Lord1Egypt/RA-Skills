---
name: doubao-tts
description: 豆包 TTS 文字转语音（火山引擎）
triggers: ["朗读", "转语音", "TTS", "语音合成", "读出来", "用声音读", "播放这段"]
---

# 豆包 TTS 技能

用火山引擎豆包 TTS 把文字转成语音，支持多种音色、情感、语速调节。

---

## 配置步骤

### 1. 申请火山引擎凭证

1. 访问 https://www.volcengine.com/
2. 注册/登录账号
3. 进入控制台 → 语音技术 → 语音合成
4. 创建应用，获取以下信息：
   - **AppID**
   - **Access Token**
   - **Cluster**（集群 ID）

### 2. 创建配置文件

创建 `~/.openclaw/doubao-tts-config.json`：

```json
{
  "appid": "你的 AppID",
  "access_token": "你的 Access Token",
  "cluster": "你的 Cluster ID",
  "voice_type": "BV700_streaming",
  "emotion": "pleased"
}
```

**配置说明**

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| appid | 是 | 火山引擎 AppID | `1234567890` |
| access_token | 是 | 访问令牌 | `xxxxx` |
| cluster | 是 | 集群 ID | `volcano_tts` |
| voice_type | 否 | 默认音色 | `BV700_streaming` |
| emotion | 否 | 默认情感 | `pleased` |

---

## 音色推荐

### 常用音色

| 音色名称 | voice_type | 特点 |
|---------|------------|------|
| 灿灿 | BV700_streaming | 22 种情感，最全能（默认） |
| 擎苍 | BV701_streaming | 旁白模式，适合读文章 |
| 通用女声 | BV001_streaming | 日常对话 |
| 通用男声 | BV002_streaming | 基础男声 |
| 甜美小源 | BV405_streaming | 智能助手风格 |
| 知性女声 | BV009_streaming | 专业严肃 |

### 情感/风格

| 情感 | 值 | 说明 |
|------|-----|------|
| 愉悦 | pleased | 默认，友好语气 |
| 开心 | happy | 欢快 |
| 悲伤 | sad | 低沉 |
| 客服 | customer_service | 专业客服 |
| 讲故事 | storytelling | 叙述风格 |
| 安慰鼓励 | comfort | 温暖安慰 |

---

## 使用方式

### 基础用法

```
朗读 "今天天气不错"
帮我把这段话转成语音：你好，欢迎使用豆包 TTS
用声音读出来：欢迎回家
```

### 指定音色

```
用男声读 "你好"
用灿灿的声音读这段文字
换一个女声读
```

### 自动情感判断（推荐）

技能会自动根据内容选择情感，无需手动指定：

| 内容特征 | 自动情感 | 示例 |
|---------|---------|------|
| 夸奖、好事、成功 | happy（开心） | "太棒了""搞定了" |
| 道歉、失误、遗憾 | sad（悲伤） | "对不起""弄错了" |
| 安慰、陪伴、鼓励 | pleased（愉悦） | "别难过""我陪着你" |
| 惊讶、意外 | surprise（惊讶） | "哇""真的吗" |
| 特别悲伤 | tear（哭腔） | "呜呜""哭了" |
| 日常对话 | pleased（愉悦） | 默认友好语气 |

**注意**：灿灿 (BV700_streaming) 支持的情感有限，以上已做适配。

```bash
# 自动判断，无需指定情感
朗读 "吴，今天天气不错"  → 自动用 pleased
朗读 "太棒了，完成了！"  → 自动用 happy
朗读 "吴对不起，我弄错了" → 自动用 sorry
```

### 调节参数

```
朗读 --speed 1.2 "加快语速"
朗读 --volume 0.8 "降低音量"
朗读 --pitch 1.1 "提高音调"
```

### 保存文件

```
朗读 --save ~/Desktop/output.mp3 "保存到这里"
```

---

## 核心逻辑

### 1. 读取配置

```bash
config_file="$HOME/.openclaw/doubao-tts-config.json"

if [ ! -f "$config_file" ]; then
    echo "❌ 配置文件不存在，请先创建 $config_file"
    echo "参考：https://www.volcengine.com/docs/6561/97465"
    return 1
fi

appid=$(cat "$config_file" | jq -r '.appid')
access_token=$(cat "$config_file" | jq -r '.access_token')
cluster=$(cat "$config_file" | jq -r '.cluster')
voice_type=$(cat "$config_file" | jq -r '.voice_type // "BV700_streaming"')
emotion=$(cat "$config_file" | jq -r '.emotion // "pleased"')
```

### 2. 自动情感判断

```bash
# 根据内容自动选择情感
auto_select_emotion() {
    local text="$1"
    local text_lower=$(echo "$text" | tr '[:upper:]' '[:lower:]')
    
    # 开心/成功场景
    if echo "$text_lower" | grep -qE "(太棒了 | 太好了 | 成功了 | 搞定 | 完成 | 厉害 | 优秀 | 棒|赞|赢|好开心|好兴奋)"; then
        echo "happy"
        return
    fi
    
    # 道歉/失误场景
    if echo "$text_lower" | grep -qE "(对不起 | 抱歉 | 弄错了 | 失误 | 遗憾 | 不好意思 | 我的错)"; then
        echo "sorry"
        return
    fi
    
    # 安慰/陪伴场景
    if echo "$text_lower" | grep -qE "(别难过 | 别伤心 | 我陪着你 | 有我在 | 没事的 | 会好的 | 加油 | 相信你)"; then
        echo "comfort"
        return
    fi
    
    # 讲故事/长文场景（超过 100 字或明显叙述）
    if [ ${#text} -gt 100 ] || echo "$text_lower" | grep -qE "(从前 | 故事 | 很久以前 | 话说)"; then
        echo "storytelling"
        return
    fi
    
    # 正式工作场景
    if echo "$text_lower" | grep -qE "(汇报 | 总结 | 数据 | 统计 | 分析 | 报告 | 清单 | 流程)"; then
        echo "professional"
        return
    fi
    
    # 默认愉悦
    echo "pleased"
}

emotion=$(auto_select_emotion "$text")
```

### 3. 构建请求

```bash
# 生成唯一请求 ID
reqid=$(uuidgen 2>/dev/null || echo "tts-$(date +%s)-$$")

# 默认参数
speed_ratio=${speed_ratio:-1.0}
volume_ratio=${volume_ratio:-1.0}
pitch_ratio=${pitch_ratio:-1.0}

# 构建 JSON（包含情感参数）
json_payload=$(cat <<EOF
{
  "app": {
    "appid": "$appid",
    "token": "access_token",
    "cluster": "$cluster"
  },
  "user": {
    "uid": "388808087185088"
  },
  "audio": {
    "voice_type": "$voice_type",
    "encoding": "mp3",
    "speed_ratio": $speed_ratio,
    "volume_ratio": $volume_ratio,
    "pitch_ratio": $pitch_ratio,
    "emotion": "$emotion"
  },
  "request": {
    "reqid": "$reqid",
    "text": "$text",
    "text_type": "plain",
    "operation": "query",
    "with_frontend": 1,
    "frontend_type": "unitTson"
  }
}
EOF
)
```

### 4. 发送请求

```bash
api_url="https://openspeech.bytedance.com/api/v1/tts"

response=$(curl -s -X POST "$api_url" \
  -H "Authorization: Bearer;$access_token" \
  -H "Content-Type: application/json" \
  -d "$json_payload")

# 检查错误
error_code=$(echo "$response" | jq -r '.code // 0')
if [ "$error_code" != "0" ] && [ "$error_code" != "null" ]; then
    error_msg=$(echo "$response" | jq -r '.message // "未知错误"')
    echo "❌ TTS 请求失败：$error_msg"
    return 1
fi
```

### 5. 处理响应

```bash
# 提取 base64 音频数据
audio_base64=$(echo "$response" | jq -r '.data')

if [ -z "$audio_base64" ] || [ "$audio_base64" = "null" ]; then
    echo "❌ 未获取到音频数据"
    return 1
fi

# 解码保存
output_file="${save_path:-/tmp/doubao_tts_$(date +%s).mp3}"
echo "$audio_base64" | base64 -d > "$output_file"

echo "✅ 语音生成成功：$output_file"
```

### 6. 播放音频

```bash
# Mac
if command -v afplay &> /dev/null; then
    afplay "$output_file"
# Linux
elif command -v paplay &> /dev/null; then
    paplay "$output_file"
# Windows
elif command -v powershell &> /dev/null; then
    powershell -c "(New-Object Media.SoundPlayer '$output_file').PlaySync()"
else
    echo "⚠️ 未找到播放器，音频已保存：$output_file"
fi
```

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 配置文件不存在 | 未创建 config.json | 按步骤创建配置文件 |
| 401 Unauthorized | Token 过期或错误 | 重新获取 Access Token |
| 403 Forbidden | AppID 无权限 | 检查应用配置 |
| 400 Bad Request | 参数错误 | 检查 voice_type 是否有效 |
| 网络超时 | 网络问题 | 检查网络连接 |
| 无音频数据 | API 返回异常 | 查看完整响应内容 |

---

## 完整示例脚本

```bash
#!/bin/bash
# doubao-tts.sh - 豆包 TTS 命令行工具

set -e

config_file="$HOME/.openclaw/doubao-tts-config.json"
text="$1"
save_path="$2"

# 检查配置
if [ ! -f "$config_file" ]; then
    echo "❌ 配置文件不存在：$config_file"
    exit 1
fi

# 读取配置
appid=$(cat "$config_file" | jq -r '.appid')
access_token=$(cat "$config_file" | jq -r '.access_token')
cluster=$(cat "$config_file" | jq -r '.cluster')
voice_type=$(cat "$config_file" | jq -r '.voice_type // "BV700_streaming"')

# 生成请求
reqid=$(uuidgen 2>/dev/null || echo "tts-$(date +%s)-$$")
json_payload=$(cat <<EOF
{
  "app": {"appid": "$appid", "token": "access_token", "cluster": "$cluster"},
  "user": {"uid": "388808087185088"},
  "audio": {"voice_type": "$voice_type", "encoding": "mp3"},
  "request": {"reqid": "$reqid", "text": "$text", "text_type": "plain", "operation": "query", "with_frontend": 1}
}
EOF
)

# 发送请求
response=$(curl -s -X POST "https://openspeech.bytedance.com/api/v1/tts" \
  -H "Authorization: Bearer;$access_token" \
  -H "Content-Type: application/json" \
  -d "$json_payload")

# 处理响应
audio_base64=$(echo "$response" | jq -r '.data')
if [ -z "$audio_base64" ]; then
    echo "❌ 请求失败：$response"
    exit 1
fi

output_file="${save_path:-/tmp/doubao_tts_$$.mp3}"
echo "$audio_base64" | base64 -d > "$output_file"
echo "✅ 生成成功：$output_file"

# 播放
afplay "$output_file" 2>/dev/null || echo "请手动播放：$output_file"
```

---

## 相关文件

- 配置文件：`~/.openclaw/doubao-tts-config.json`
- 输出目录：`/tmp/doubao_tts_*.mp3` 或用户指定路径
- 官方文档：https://www.volcengine.com/docs/6561/97465

---

## 注意事项

1. **Token 有效期** — Access Token 可能过期，定期更新
2. **计费** — 火山引擎 TTS 有免费额度，超出后按量计费
3. **文本长度** — 单次请求建议不超过 500 字，长文本分段处理
4. **并发限制** — 避免短时间内大量请求
