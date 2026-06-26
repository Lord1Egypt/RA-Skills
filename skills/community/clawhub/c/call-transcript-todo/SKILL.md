---
name: call-transcript-todo
description: |
通话录音转写与会议纪要生成。将音频文件转录为结构化文本，包含对话实录、摘要纪要和待办事项提取。
支持输出到飞书文档（需配置凭证）或本地 Markdown 文件。
当用户说"帮我转录"、"处理一下这个录音"、"语音转文字"、"通话录音整理"、"录音纪要"、"transcribe this recording"，
或发送音频文件并明确表达转录/整理意图时触发。
注意：仅在用户表达转录意图时触发，不对所有音频附件自动执行。
env:
FEISHU_APP_ID:
required: false
description: 飞书应用 App ID，用于创建飞书文档。未配置时输出为本地 Markdown 文件。
FEISHU_APP_SECRET:
required: false
description: 飞书应用 App Secret，与 FEISHU_APP_ID 配合使用。
dependencies:

- faster-whisper (pip install faster-whisper)
  compatibility:
- OpenClaw
- Claude Code

---

# 通话录音转写

核心流程：转录音频 → 整理实录与纪要 → 提取待办 → 输出结果。

---

## Step 1: 环境准备与转录

### 1.1 安装依赖

首次使用时安装（后续跳过）：

```bash
pip install faster-whisper --break-system-packages 2>/dev/null || pip install faster-whisper
```

> `--break-system-packages` 用于容器/沙箱环境。如果环境不允许，回退到不带此参数的安装。

### 1.2 音频转录

```python
from faster_whisper import WhisperModel
import os

audio_path = '<音频文件路径>'

# 根据文件大小选择模型：< 5MB 用 small，否则用 medium
file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
model_size = 'small' if file_size_mb < 5 else 'medium'

try:
    model = WhisperModel(model_size, device='cpu', compute_type='int8')
    segments, info = model.transcribe(audio_path, language='zh')
    transcript = [seg.text for seg in segments]
    full_text = '\n'.join(transcript)
except Exception as e:
    # 转录失败时，告知用户具体原因并停止后续流程
    print(f"转录失败：{e}")
    # 常见原因：音频格式不支持、文件损坏、内存不足
    # 向用户说明错误并建议：检查文件格式、尝试转换为 mp3/wav 后重试
    raise
```

**支持的音频格式**：mp3, m4a, wav, ogg, amr, mp4, flac, webm

**模型选择参考**：

- `small`（~500MB）：电话录音、短对话，速度快
- `medium`（~1.5GB）：会议录音、多人讨论、口音较重，准确率更高
- 如果用户明确要求高精度，使用 `medium`

### 1.3 文件名信息提取

从文件名中尽量提取元数据：

| 文件名模式                           | 提取内容                |
| ------------------------------- | ------------------- |
| `XX_20260323.m4a`               | 来源：XX，日期：2026-03-23 |
| `Record_20260323_143022.mp3`    | 日期：2026-03-23 14:30 |
| `CallRecord_+8613912345678.m4a` | 来源：+8613912345678   |
| 其他                              | 用文件名原文作为来源          |

---

## Step 2: 整理实录与生成纪要

拿到转录原文后，做三层加工：

### 2.1 整理实录

将转录原文整理为可读的对话实录：

- 根据语义和上下文判断说话人，标记为 **`我`** 和 **`[对方姓名/身份]`**
- 合并同一说话人的连续短句
- 修正明显的语音识别错误（专有名词、人名、机构名）
- 格式：每段以 `**我：**` 或 `**XX：**` 开头

### 2.2 生成纪要

用连贯段落概括通话内容（3-5 句话），包含：

- 通话背景：谁和谁、什么事由
- 主要讨论内容和关键结论
- 后续安排和跟进事项

纪要简洁精炼，不用列表格式。

### 2.3 提取待办

从通话内容中识别具体的待办事项：

- 明确承诺要做的事
- 约定的时间节点或截止日期
- 需要跟进或确认的事项

如果没有明确的待办事项，标注"本次通话未提取到明确的待办事项。"

---

## Step 3: 输出结果

根据环境配置选择输出方式。**优先检测飞书凭证，有则输出飞书文档，无则输出本地文件。**

### 3.1 输出内容模板

无论哪种输出方式，内容结构统一：

```markdown
# 通话录音转写

**来源**：[从文件名提取，或标注"未知"]
**时间**：[YYYY-MM-DD HH:MM，无法提取则标注"未知"]
**时长**：[MM:SS，从转录 info 中获取]

---

## 实录

**我：** [说话内容]

**XX：** [说话内容]

...

---

## 纪要

[连贯段落，3-5句话]

---

## 待办

[待办事项，或"本次通话未提取到明确的待办事项。"]
```

### 3.2 飞书文档输出（需要凭证）

检测到 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 环境变量时：

```
feishu_doc action=write
```

使用上述模板内容创建飞书文档，markdown 标题会自动转换为飞书文档标题格式。

**不要用 `update_block`，必须用 `action=write`。**

输出失败时降级为本地文件输出（见 3.3）。

### 3.3 本地文件输出（默认/降级）

未配置飞书凭证，或飞书输出失败时：

将内容保存为 Markdown 文件，文件名格式：`通话纪要_[来源]_[日期].md`

```bash
# 示例路径
output/通话纪要_XX_20260323.md
```

---

## Step 4: 发送结果与待办确认

### 4.1 发送结果

**飞书输出成功时**：

```
📄 [飞书文档链接]

待办事项：
1. [待办内容]
2. [待办内容]

确认计入工作待办？(是/否/修改)
```

**本地文件输出时**：

```
📄 已保存：通话纪要_XX_20260323.md

待办事项：
1. [待办内容]
2. [待办内容]

确认计入工作待办？(是/否/修改)
```

**无待办时**，只发文档/文件链接，附注"本次通话未提取到明确的待办事项。"，不需要确认。

### 4.2 待办确认与写入

用户确认后才将待办写入 `memory/todo.md`（相对于当前工作目录）：

- "是" / "确认" / "OK" → 追加写入 todo.md，回复"已计入工作待办"
- "否" / "不要" → 不写入，回复"已忽略"
- 用户给出修改内容 → 按修改调整后再次确认

**todo.md 格式**：

```markdown
## [日期]

- [ ] [待办内容]（来源：[通话来源]）
```

**未收到确认前，不写入 todo.md。**

---

## 错误处理

| 场景                  | 处理方式                                 |
| ------------------- | ------------------------------------ |
| 音频格式不支持             | 告知用户，建议转换为 mp3/wav 后重试               |
| 转录结果为空或乱码           | 提示音频质量可能不足，建议换 medium 模型重试           |
| faster-whisper 安装失败 | 提示用户检查 Python 环境和网络连接                |
| 飞书文档创建失败            | 自动降级为本地 Markdown 文件输出，告知用户           |
| 模型下载超时              | 提示首次使用需下载模型（small ~500MB），建议在网络稳定时重试 |
