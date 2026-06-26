---
name: audio-meeting-minutes
description: >
  熠小听 — 会议录音自动转文字 + AI总结 + 生成会议纪要HTML。
  将会议录音文件拖入指定文件夹，自动转录为文字，智能提取会议要点，
  输出专业格式的会议纪要HTML文档。
  Trigger: 熠小听、录音豆、会议录音、会议纪要、录音转文字、音频转文字、语音转文本.
permissions:
  - filesystem.read
  - filesystem.write
  - network
  - shell
---

# 熠小听 · 会议纪要自动化

将录音放入文件夹 → 语音识别 → WorkBuddy AI 提炼纪要 → HTML 文档。

> ⚠️ **重要隐私声明**：本技能会将会议录音上传至**阿里云智能语音交互（NLS）**进行语音识别。
> 录音和转写文本会被传输至阿里云服务器处理。请勿用于处理含有机密信息、个人隐私数据
> 或受监管内容的会议录音。使用前请确认你所在组织允许该数据流向。

## 核心能力

| 环节 | 技术方案 | 速度 |
|------|---------|------|
| 语音识别 | 阿里云 NLS 云端识别 | ~1分钟/20分钟音频 |
| AI 总结 | WorkBuddy 内置 AI（无需额外 Key） | 即时 |
| HTML 输出 | Jinja2 模板，企业级排版 | 即时 |

## 支持格式

mp3 / m4a / wav / ogg / flac / aac / wma / opus / webm

---

## 首次使用（对话引导）

当用户触发本技能时，需要收集以下信息，缺一不可。用自然对话方式逐一确认，不要一次丢出所有问题。

### 第 1 步：确认录音文件夹

```
"你的录音文件放在哪个文件夹？我会监听这个文件夹，有新录音自动处理。"
```

### 第 2 步：确认阿里云 NLS 凭证

阿里云智能语音交互需要两个凭据，缺一不可：

```
"需要阿里云智能语音的两个凭证：

① NLS AppKey
   获取链接：https://nls-portal.console.aliyun.com/applist
   步骤：进入页面 → 点击「创建项目」→ 填写项目名称 → 创建成功后
         复制页面显示的 AppKey

② NLS AccessToken
   获取链接：https://nls-portal.console.aliyun.com/applist
   步骤：点击已有项目名称进入详情 → 顶部标签栏选择「AccessToken」
         → 点击「获取AccessToken」→ 复制显示的 Token 字符串
          ⚠️ 24 小时失效，长期使用需换成 AccessKey（AK ID + Secret）

把两个凭证发给我即可。

> 🔐 **凭证安全提醒**：请使用短期（24h）AccessToken，不要将长期 AccessKey Secret
> 粘贴到聊天窗口。聊天记录可能被日志系统留存。如需长期使用，建议通过环境变量
> 或配置文件注入凭证，而非在对话框明文传输。"
```

### 收齐全部信息后

告诉用户：「配置已齐全，现在把录音放进文件夹，说一句『熠小听』我就开始处理。」

---

## 工作流（Agent 执行）

### Step 1：语音转文字

```bash
cd {skill_dir}/scripts
set NLS_APPKEY=<用户提供的AppKey>
set NLS_TOKEN=<用户提供的AccessToken>
set LYD_NAS_DIR=<录音文件夹路径>
python process_nas.py
```

脚本会：
1. 扫描录音文件夹（排除「会议纪要输出」子文件夹）
2. ffmpeg 转 PCM 16kHz mono → 按 ≤1.8MB 切块
3. 逐块上传阿里云 NLS 接口（串行）
4. 合并结果 → 保存 transcript.txt
5. 输出 JSON 结果（包含 transcript_path）

### Step 2：AI 智能总结

读取 transcript.txt 全文，基于内容手工提炼：

**总结原则：**
- **提炼而非摘抄** — 不复制原文，用书面语重新表述
- **区分讨论过程和最终结论** — 只记录结论，不复述过程
- **行动项格式**：动词开头 + 负责人 + 优先级
- **决策格式**：决策内容 + 决策依据

**输出格式**（用于 report.py 渲染）：

```python
summary = {
    "meeting_title": "精准标题（15字以内）",
    "meeting_type": "技术分享/项目决策/工作汇报/头脑风暴/复盘总结",
    "meeting_summary": "3-4句书面语概括背景、核心议题和主要结论",
    "key_conclusions": ["重要结论句子..."],
    "decisions": [
        {"content": "已确认决策", "rationale": "决策依据"}
    ],
    "action_items": [
        {"task": "具体行动（动词开头）", "owner": "负责人", "deadline": "截止时间", "priority": "高/中/低"}
    ],
    "participants": ["参会人"],
    "agenda_items": [
        {"title": "议题名称", "key_points": ["核心观点"], "outcome": "最终结论"}
    ],
    "risks_and_concerns": ["风险或待确认事项"],
    "next_steps": ["具体下一步计划"],
    "follow_up_required": ["需跟进事项"]
}
```

### Step 3：生成 HTML

```python
from report import render_html
render_html(summary=summary, transcript={"text": full_text, "segments": [], "language": "zh",
           "duration_seconds": duration}, audio_filename=audio_name, output_path=html_path)
```

### Step 4：写回 NAS

用 PowerShell UNC 路径将 HTML 写入录音文件夹下的 `会议纪要输出\` 子文件夹：

```powershell
Copy-Item "本地html路径" "\\192.168.1.219\品...\会议纪要输出\文件名.html"
```

### HTML 模板规范

企业级排版（report.py 内置）：
- 深蓝商务风，文档头 + 目录导航 + 编号章节
- 决策卡片（左侧蓝边 + 决策依据）
- 行动表格（编号/任务/负责人/截止/优先级）
- 议题折叠块（要点列表 + 绿色结论条）
- 风险跟进区（橙色警告条）
- 可折叠完整转写记录
- 移动端适配 + 打印样式

---

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| NLS 块大小 | 1.8 MB | 接口限制 2MB，1.8MB ≈ 57秒音频 |
| 音频采样 | 16kHz mono PCM | ffmpeg 转换参数 |
| 请求间隔 | 0.3s | NLS 串行间隔，避免限流 |

---

## 文件说明

| 文件 | 用途 |
|------|------|
| `scripts/process_nas.py` | 语音转文字：扫描→切块→NLS→保存 transcript |
| `scripts/report.py` | HTML 模板 + render_html() 渲染函数 |
| `scripts/summarize.py` | （保留备用）AI 总结函数，如需外部 API |

---

## 常见问题

**Q: 不配任何 API Key 能用吗？**
A: 只需要阿里云 NLS 的 AppKey + Token（语音识别），AI 总结由 WorkBuddy 内置完成，无需额外 Key。

**Q: NLS Token 失效了怎么办？**
A: 到控制台重新获取，或让我帮你改成 AccessKey 动态刷新模式（永久有效）。

**Q: 长录音处理慢？**
A: NLS 云端识别，1 小时音频约 2-3 分钟。

**Q: 输出在哪？**
A: 录音文件夹下的 `会议纪要输出\` 子文件夹，HTML 格式。
