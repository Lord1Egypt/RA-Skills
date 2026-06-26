---
name: generate-drama
version: 1.1.1
description: 根据主题自动生成多角色有声短剧，调用 SenseAudio TTS API 合成音频并拼接输出
---

# 短剧生成器 (Drama Generator)

根据用户提供的短剧主题，自动生成多角色有声短剧。

## 使用方式

用户说出类似以下请求时触发此 Skill：
- "帮我生成一个短剧，主题是..."
- "做一个有声剧，关于..."
- "生成短剧音频：..."

## 执行步骤

### 第一步：检查 API 密钥

```bash
echo "SENSEAUDIO_API_KEY=$SENSEAUDIO_API_KEY"
```

**如果 `SENSEAUDIO_API_KEY` 为空，必须先向用户询问，说明在 https://senseaudio.cn 注册获取。不要直接运行脚本让它报错。**

### 第二步：生成剧本

你（Claude）自己根据用户主题生成剧本，**不需要调用外部 LLM**。

可用音色列表：
- `child_0001_a` — 可爱萌娃(开心)，适合小孩、活泼少女、可爱类角色
- `child_0001_b` — 可爱萌娃(平稳)，适合小孩、安静少女、乖巧类角色
- `male_0004_a` — 儒雅道长(平稳)，适合学者、道长、智者、长辈、沉稳男性角色
- `male_0018_a` — 沙哑青年(深情)，适合江湖浪子、叛逆少年、男主类角色

生成要求：
1. 2-5 个角色，每个角色有明确的名字
2. 总共 10-20 句对白
3. 剧情紧凑有冲突
4. 为每个角色从上面的音色列表中选择最合适的 voice_id

输出为 JSON 格式，保存为临时文件：

```json
{
  "topic": "用户的主题",
  "roles": {
    "角色A": "voice_id",
    "角色B": "voice_id"
  },
  "segments": [
    {"sid": "角色A", "text": "台词内容"},
    {"sid": "角色B", "text": "台词内容"}
  ]
}
```

将 JSON 保存到临时文件，如 `/tmp/drama_script.json`。

### 第三步：运行脚本合成音频

```bash
python scripts/generate_drama.py @/tmp/drama_script.json \
  --output outputs/drama_output.wav \
  --senseaudio-api-key "xxx"
```

注意：
- 剧本 JSON 通过 `@文件路径` 传入
- 如果环境变量 `SENSEAUDIO_API_KEY` 已设置，无需 `--senseaudio-api-key`

### 第四步：返回结果

将生成的音频文件路径和剧本内容展示给用户。

## 环境要求

- Python 3.10+，依赖：`requests`
- `SENSEAUDIO_API_KEY` — SenseAudio API 密钥（唯一需要的密钥）

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `script_json` | 剧本 JSON 字符串或 `@文件路径`（必填） | - |
| `--output` | 输出 WAV 文件路径 | 自动生成 |
| `--gap` | 对白之间的静音间隔（秒） | 0.3 |
| `--senseaudio-api-key` | SenseAudio API 密钥 | 读环境变量 |
