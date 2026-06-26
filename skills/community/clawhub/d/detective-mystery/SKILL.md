---
name: detective-mystery
description: |
  中文语音侦探推理游戏。适用于用户想玩一场沉浸式推理探案的场景：由 LLM 生成包含嫌疑人、线索和真凶的完整案件，玩家通过审讯嫌疑人（支持 ASR 语音或文本输入）、勘察现场、收集证据，最终提出指控并获得评分。支持多音色 TTS 为不同嫌疑人配音，审讯历史自动压缩防止上下文溢出，案件生成后自动验证逻辑自洽性。支持存档/读档（`--load`）和难度调节。
---

# 中文语音侦探推理游戏

## 适用范围

此 Skill 用于运行一场完整的中文侦探推理互动游戏。

能力边界：
- 依赖 `LLM` 生成案件和角色对话，`TTS` 合成多角色语音，`ASR` 识别玩家语音输入
- 支持审讯、勘察、回顾证据、指控四种动作
- 支持存档/读档，跨会话保持游戏进度
- 案件生成后自动验证逻辑自洽性

不做：
- 视频或图像生成
- 英文游戏
- 实时打断式流式语音对话

## 默认配置

- `difficulty`: `medium`（easy/medium/hard）
- `max_turns`: `30`
- 每位嫌疑人最多 `5` 轮审讯
- 审讯历史超 `4` 轮自动压缩

## 音色分配

| 角色 | voice_id | speed | pitch |
|------|----------|-------|-------|
| 旁白 narrator | child_0001_a | 0.85 | -1 |
| 嫌疑人A suspect_a | male_0004_a | 1.0 | 0 |
| 嫌疑人B suspect_b | male_0018_a | 1.1 | 0 |
| 嫌疑人C suspect_c | child_0001_b | 1.0 | 2 |

## 玩家动作

- `interrogate` — 审讯嫌疑人（选择对象，多轮对话）
- `examine` — 勘察现场（发现新线索）
- `review` — 回顾已收集的证据
- `accuse` — 提出指控（输入推理，获得评分）
- `save` — 保存游戏进度
- `quit` — 退出游戏

## 评分维度

| 维度 | 分值范围 | 说明 |
|------|----------|------|
| logic | 0-30 | 推理逻辑是否严密 |
| evidence | 0-30 | 证据引用是否充分 |
| completeness | 0-20 | 是否涵盖关键线索 |
| efficiency | 0-20 | 用了多少步得出结论 |
| 总分 | 0-100 | |

## 工作流

1. 初始化
   - 读取难度、最大回合数等参数
   - 若 `--load` 则加载存档

2. 案件生成
   - LLM 生成案件背景、3名嫌疑人、证据线索、真凶
   - 自动验证：恰好1个真凶、线索关联完整
   - 不通过则重试（最多3次）

3. 开场旁白
   - TTS 播放案件简介

4. 主循环
   - 玩家选择动作 → 系统处理 → TTS 返回
   - `interrogate`: 多轮对话，嫌疑人用角色音色
   - `examine`: 发现线索，旁白描述
   - `accuse`: 输入推理 → 评分 → 揭示真相

5. 输出
   - `case_report.json`: 完整案件和游戏记录

## Prompt 模块

详见 [references/prompts_cn.md](references/prompts_cn.md)。

## 数据结构

详见 [references/state_schema_cn.md](references/state_schema_cn.md)。

## 直接运行

```bash
pip install -r requirements.txt

# 文本模式（不用 ASR）
python scripts/run_mystery.py --no-asr

# 完整语音模式
python scripts/run_mystery.py

# 高难度
python scripts/run_mystery.py --difficulty hard --no-asr

# 读取存档
python scripts/run_mystery.py --load --no-asr

# 不用 TTS
python scripts/run_mystery.py --no-tts --no-asr
```

接口约定：
- LLM 读取 `MYSTERY_LLM_API_KEY`，回退到 `IME_MODEL_API_KEY`
- TTS 读取 `MYSTERY_TTS_API_KEY`，回退到 `SENSEAUDIO_API_KEY`
- ASR 读取 `MYSTERY_ASR_API_KEY`，回退到 `SENSEAUDIO_API_KEY`
