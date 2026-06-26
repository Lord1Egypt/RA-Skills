---
name: 8917-minimax-toolkit
description: MiniMax 多模态工具集。用于图片生成、图生图、视频生成、视频模板、语音合成、长文本 TTS、声音克隆、声音设计与音乐生成。适用于需要调用 MiniMax 官方 API 处理文本、图片、音频或视频素材的场景。默认将产物输出到当前工作区的 `workspace/03-Resources/minimax-output/`；若当前目录不含 `workspace/`，则退回 `./outputs/minimax/`。支持 `--project` 做项目隔离，也支持 `--output-dir` 显式覆盖输出根目录。默认读取 MiniMax Token Plan API Key（环境变量 `MINIMAX_API_KEY` 或 `~/.openclaw/openclaw.json`）。
metadata:
  openclaw:
    requires:
      env: ["MINIMAX_API_KEY"]
---

# 8917-minimax-toolkit

## 定位

这是一个 **工具型 / Tool Wrapper** skill。

用它在 MiniMax 官方 API 上执行多模态生成任务，并把产物稳定落到当前工作区或用户指定目录。

## 核心原则

1. **执行前先提示消耗**：先输出 Token Plan 请求消耗预估，再执行。
2. **执行前先讲清隐私边界**：涉及图片、音频、视频等素材上传时，明确告知会发送到 MiniMax API。
3. **优先遵守输出纪律**：优先写入当前工作区；没有 `workspace/` 时再退回通用输出目录。
4. **项目隔离优先**：需要长期管理时优先使用 `--project`。
5. **禁止硬编码 API Key**：仅从 `MINIMAX_API_KEY` 或 `~/.openclaw/openclaw.json` 读取。

## 输出纪律

输出根目录优先级：
1. `--output-dir`
2. `MINIMAX_OUTPUT_DIR`
3. 当前工作目录下的 `workspace/03-Resources/minimax-output/`
4. 当前目录不存在 `workspace/` 时，退回 `./outputs/minimax/`

使用 `--project <ProjectName>` 时，产物进入项目子目录。

执行完成后，始终明确告诉用户：
- 文件类型
- 保存路径
- 如需长期管理，建议整理到项目目录

## 预算与隐私

执行前至少说明：
- 模型名称
- 预计消耗的 request 次数
- 5 小时滚动窗口规则
- 高消耗任务风险提示（尤其视频）

涉及私密图片、音频或视频时，先确认用户接受第三方 API 处理。

详细说明见：
- `references/budget-and-trust.md`
- `references/api_info.md`
- `references/costs.json`

## 能力导航

按具体场景读取：
- `references/modalities.md`：查看 9 类能力、对应脚本和 CLI 示例
- `references/budget-and-trust.md`：查看预算、上传与隐私边界
- `references/api_info.md`：查看当前模型 ID 与基础约束
- `references/quota_mapping.json`：查看运行时模型名与官方额度桶的映射
- `references/official-doc-sources.md`：查看需要定期核验的官方来源
- `references/troubleshooting.md`：查看联网失败、网页抓取失败、remains 查询失败时的排障指引

## 官方文档校验机制

可运行：

```bash
python3 scripts/mm.py remains
python3 scripts/mm.py check-docs
```

其中：
- `mm.py remains`：查询官方 Token Plan 实时额度
- `mm.py check-docs`：抓取官方 FAQ + 查询 remains + 对比本地 references

校验脚本会：
1. 抓取官方 Token Plan FAQ
2. 查询官方 `coding_plan/remains` 接口
3. 对比本地 `references/` 中的关键配置
4. 生成差异报告到 `references/checks/latest-check.md`

如果在线校验失败：
- 不阻塞整个 skill
- 退回本地 references 离线模式
- 输出排障指引
- 详见 `references/troubleshooting.md`

## 推荐使用统一入口

优先使用统一入口 `scripts/mm.py`：

```bash
# Image / Video / Music
python3 scripts/mm.py image "A red apple" --ratio 16:9 --project Demo
python3 scripts/mm.py video "Cinematic ruins" --project Demo
python3 scripts/mm.py music "Lo-fi beat" --instrumental --project Demo

# Speech (short text)
python3 scripts/mm.py speech "Hello world" --voice male-qn-qingse --project Demo

# Speech (long text / file)
python3 scripts/mm.py async-speech ~/script.txt --voice male-qn-qingse --project Demo

# Image-to-image
python3 scripts/mm.py i2i "anime style" --ref ~/photo.jpg --project Demo

# Video templates
python3 scripts/mm.py video-template labubu --media ~/photo.jpg --project Demo

# Voice clone / design
python3 scripts/mm.py voice-clone ~/my_voice.wav --voice-id my-voice
python3 scripts/mm.py voice-design "Warm deep male voice" --voice-id new-voice
```

支持的 modality：`image`, `i2i`, `video`, `video-template`, `speech`, `async-speech`, `voice-clone`, `voice-design`, `music`

当前支持显式功能开关：`references/feature_flags.json`
- 可按 modality 设定 `true / false`
- 当前套餐不支持的能力建议直接设为 `false`，避免无意义调用

注意：
- `voice-design` 当前要求 `--preview-text`
- `voice-clone` 建议提供 `--preview-text`，如提供 `--prompt-audio` 则需同时提供 `--prompt-text`
- 复刻音色若 7 天内未正式调用，官方会删除该音色

详细示例见 `references/modalities.md`。

## 兼容入口（旧脚本仍可用）

如需直接调用或处理更复杂场景，以下脚本仍可用：
- `scripts/mm_image.py`
- `scripts/mm_i2i.py`
- `scripts/mm_video.py`
- `scripts/mm_video_template.py`
- `scripts/mm_speech.py`
- `scripts/mm_async_speech.py`
- `scripts/mm_voice_clone.py`
- `scripts/mm_voice_design.py`
- `scripts/mm_music.py`

旧脚本作为兼容层保留，未来逐步收敛到统一入口。

## 一句话原则

**MiniMax 产物默认落当前工作区或通用输出目录，执行前讲清 request 消耗与第三方 API 处理边界。**
