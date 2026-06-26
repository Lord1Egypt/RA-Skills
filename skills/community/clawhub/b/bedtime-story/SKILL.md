---
name: bedtime-story
description: |
  生成多角色中文睡前故事并合成语音。适用于用户想为孩子定制个性化睡前故事的场景：根据孩子姓名、年龄和兴趣，由 LLM 创建完整世界观和角色，生成分段故事文本（每段标注说话人），再由 TTS 以不同音色合成旁白、主角、小伙伴和长者的语音，最终拼接为完整 MP3 音频文件。支持连载模式（`--continue`）在多次运行间保持角色与情节连贯性。不依赖 ASR 或实时语音对话。
---

# 中文睡前故事生成器

## 适用范围

此 Skill 用于生成可播放的多角色中文睡前故事音频。

能力边界：
- 依赖 `LLM` 生成故事文本，`TTS` 合成多角色语音
- 支持自定义孩子姓名、年龄、兴趣爱好
- 支持连载模式，跨会话保持世界观和情节连贯
- 输出完整 MP3 音频 + 故事文本 + 状态文件

不做：
- 实时语音对话或 ASR 识别
- 视频或动画生成
- 英文故事

## 默认配置

- `child_name`: `小朋友`
- `age`: `5`
- `interests`: `冒险,动物`
- `episodes`: `1`（单集）

## 音色分配

| 角色 | voice_id | speed | pitch |
|------|----------|-------|-------|
| 旁白 narrator | male_0004_a | 0.9 | 0 |
| 主角 protagonist | child_0001_a | 1.0 | 0 |
| 小伙伴 sidekick | child_0001_b | 1.0 | 0 |
| 长者 elder | male_0018_a | 0.85 | -2 |

## 工作流

1. 初始化
   - 读取 `--child-name`、`--age`、`--interests` 参数
   - 若 `--continue`，从 `story_state.json` 加载已有世界观和角色

2. 世界观与角色创建（首次运行）
   - LLM 生成世界名称、背景设定、4个角色（旁白/主角/小伙伴/长者）
   - 主角名称默认使用孩子姓名

3. 故事生成
   - LLM 生成 12-20 段 segments，每段标注 speaker 和 text
   - 连载模式下传入上集摘要，保持情节连贯

4. TTS 多角色合成
   - 逐段根据 speaker 选择对应音色参数
   - 合成每段音频

5. 音频拼接
   - MP3 帧独立可解码，直接二进制追加拼接
   - 无需 ffmpeg

6. 保存输出
   - `story_state.json`：世界观+角色+情节摘要
   - `story_ep{N}.txt`：故事文本
   - `story_ep{N}.mp3`：完整音频

## Prompt 模块

详见 [references/prompts_cn.md](references/prompts_cn.md)。

## 数据结构

详见 [references/state_schema_cn.md](references/state_schema_cn.md)。

## 直接运行

```bash
pip install -r requirements.txt

# 首次生成
python scripts/run_story.py --child-name "小明" --age 5 --interests "恐龙,太空"

# 连载续写
python scripts/run_story.py --continue

# 不调用 TTS，仅输出文本
python scripts/run_story.py --child-name "小红" --age 7 --interests "魔法,精灵" --no-tts

# 生成多集
python scripts/run_story.py --child-name "小明" --age 5 --interests "恐龙,太空" --episodes 3
```

环境变量参考：`.env.example`

接口约定：
- LLM 读取 `STORY_LLM_API_KEY`，回退到 `IME_MODEL_API_KEY`
- TTS 读取 `STORY_TTS_API_KEY`，回退到 `SENSEAUDIO_API_KEY`
