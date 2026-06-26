# 短剧生成器 - 使用指南

## 快速开始

### 1. 环境准备

```bash
# Python 依赖
pip install requests

# 配置环境变量（添加到 ~/.bashrc 或 ~/.zshrc）
export SENSEAUDIO_API_KEY="你的 SenseAudio API 密钥"

source ~/.bashrc
```

> SenseAudio API 密钥在 https://senseaudio.cn 注册后获取。

### 2. 在 Claude Code 中使用

Skill 安装完成后，直接在 Claude Code 对话框中输入即可：

```
帮我生成一个短剧，主题是"外卖小哥穿越到古代当御厨"
```

```
做一个有声剧，关于两个小朋友在森林里探险的故事
```

```
生成短剧音频：职场新人第一天上班的搞笑经历
```

Claude 会自动完成以下所有步骤：
1. 理解你的主题 → 生成多角色剧本
2. 根据角色性格自动选择最合适的音色
3. 将剧本 JSON 传给脚本，逐句调用 SenseAudio TTS 合成语音
4. 拼接所有音频 → 输出完整 WAV 文件

### 3. 手动命令行使用

也可以在项目根目录下直接运行脚本（需先准备好剧本 JSON）：

```bash
# 从 JSON 文件读取剧本
python scripts/generate_drama.py @script.json --output outputs/my_drama.wav

# 直接传 JSON 字符串
python scripts/generate_drama.py '{"topic":"测试","roles":{"张三":"male_0018_a"},"segments":[{"sid":"张三","text":"你好世界"}]}'

# 调整对白间隔（默认 0.3 秒）
python scripts/generate_drama.py @script.json --gap 0.5

# 通过命令行传入 API 密钥（优先于环境变量）
python scripts/generate_drama.py @script.json --senseaudio-api-key "<在 senseaudio.cn 获取的密钥>"
```

## 剧本 JSON 格式

```json
{
  "topic": "短剧主题",
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

## 输出说明

运行完成后会在输出目录下生成：

| 文件 | 说明 |
|------|------|
| `主题名.wav` | 完整有声短剧音频 |
| `主题名_script.json` | 剧本 JSON（含角色、台词、音色分配） |

## 可用音色

当前免费版支持以下音色，Claude 会根据角色特征自动选择：

| 音色 ID | 描述 | 适合角色 |
|---------|------|---------|
| `child_0001_a` | 可爱萌娃(开心) | 小孩、活泼少女、可爱角色 |
| `child_0001_b` | 可爱萌娃(平稳) | 小孩、安静少女、乖巧角色 |
| `male_0004_a` | 儒雅道长(平稳) | 学者、道长、智者、长辈 |
| `male_0018_a` | 沙哑青年(深情) | 江湖浪子、叛逆少年、男主 |

## 常见问题

**Q: 报错 `缺少 SENSEAUDIO_API_KEY`**
A: 检查环境变量是否正确设置，运行 `echo $SENSEAUDIO_API_KEY` 确认。

**Q: 报错 `403 no access to the specified voice`**
A: 当前账号只能使用免费音色，请确认 SenseAudio 账号已完成实名认证。

**Q: 想用更多音色？**
A: 在 SenseAudio 升级套餐后，可在脚本的 `VOICE_CATALOG` 中添加更多 voice_id。
