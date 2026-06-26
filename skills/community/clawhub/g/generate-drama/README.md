# Drama Generator Skill

AI 多角色有声短剧生成器 — Claude Skill，基于 SenseAudio TTS。

输入一个主题，自动完成：**剧本创作 → 角色配音 → 音频合成**，一键生成完整有声短剧。

## 功能特点

- **Claude 自动编剧**：根据主题生成 2-5 个角色、10-20 句对白的短剧剧本
- **智能音色匹配**：Claude 根据角色性格自动从音色库中选择最合适的声音
- **TTS 语音合成**：调用 SenseAudio TTS API 逐句合成高质量语音
- **音频自动拼接**：将所有语音片段按剧情顺序拼接为完整 WAV 文件
- **剧本同步输出**：同时保存 JSON 格式剧本，包含角色、台词、音色分配

## 可用音色

| 音色 ID | 描述 | 适合角色 |
|---------|------|---------|
| `child_0001_a` | 可爱萌娃（开心） | 小孩、活泼少女、可爱类角色 |
| `child_0001_b` | 可爱萌娃（平稳） | 小孩、安静少女、乖巧类角色 |
| `male_0004_a` | 儒雅道长（平稳） | 学者、道长、智者、长辈、沉稳男性 |
| `male_0018_a` | 沙哑青年（深情） | 江湖浪子、叛逆少年、男主类角色 |

## 项目结构

```
.
├── SKILL.md              # Skill 描述（Claude 读取）
├── scripts/
│   └── generate_drama.py # TTS 合成脚本
├── outputs/              # 生成的音频和剧本输出目录
├── README.md
└── USAGE.md              # 详细使用指南
```

## 环境要求

- Python 3.10+
- 依赖：`requests`
- `SENSEAUDIO_API_KEY` — [SenseAudio 官网](https://senseaudio.cn) 获取（唯一需要的密钥）

## 快速使用

在 Claude Code 中对话触发：

> "帮我生成一个短剧，主题是修仙世界废柴逆袭"

详细使用方式和示例请参考 [USAGE.md](USAGE.md)。

## 输出

- `主题名.wav` — 完整有声短剧音频
- `主题名_script.json` — 剧本 JSON，包含角色音色映射和逐句台词

## License

MIT

## Author

QWERTY0205
