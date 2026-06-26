---
name: academic-presentation
version: 2.0.0
description: "学术汇报全自动化 — 将论文转化为翻译稿（Word）、总结（Word）、PPT、演讲稿全套物料，完成后自动发送到微信。触发词：学术汇报、论文汇报、做PPT、论文演讲、学术PPT、汇报PPT"
metadata:
  clawdbot:
    primaryEnv: PPT_API_PROVIDER
    requires:
      bins: []
      env: []
---

# 学术汇报全自动化 (v2.0.0)

将论文转化为包含翻译、总结、PPT及演讲稿的全套物料，完成后自动发送到微信。

## v2.0.0 更新（重构）
- 🆕 **PPT 平台可配置**：支持 anygen / gamma.app / 手动下载
- 🆕 **无密钥嵌入**：API Key 由用户自行配置
- ✅ Word 文档输出（翻译稿、总结稿）
- ✅ 逐字演讲稿
- ✅ 微信自动发送

---

## 支持的 PPT 平台

| 平台 | API Key 环境变量 | 说明 |
|------|------------------|------|
| **anygen.io** | `ANYGEN_API_KEY` | 推荐，支持中文，生成质量高 |
| **gamma.app** | `GAMMA_API_KEY` | 需自行申请 |
| **跳过PPT** | 无 | 仅生成 Word 文档和演讲稿 |

---

## 首次使用配置

首次触发时，会询问 PPT 平台选择：

> 🎓 您好！已为您激活 **学术汇报全自动化** 技能（v2.0.0）。
> 
> 请选择 PPT 生成方式：
> 1. **anygen** — 推荐，已集成（需 API Key）
> 2. **gamma.app** — 需提供 GAMMA_API_KEY
> 3. **跳过 PPT** — 仅生成 Word 文档和演讲稿

---

## 工作流（6 + 1 阶段）

### 🟢 Stage 1：接收文档

**动作**：用户提供论文内容（PDF 文件路径或直接粘贴文本）

**逻辑**：
- 读取标题，设定变量 `[Doc_Title]`
- 识别语言（中文/英文/其他）
- 非中文询问是否翻译

**确认语**：「已收到文档，标题：`[Doc_Title]`，语言：{语言}。是否需要翻译为中文？」

---

### 🟢 Stage 2：翻译 → Word 文档

**动作**：将论文核心内容翻译为中文，输出 .docx

**输出**：`/tmp/academic-ppt/[Doc_Title]_翻译稿.docx`

**方式**：使用 python-docx 生成 Word 文档

**确认语**：「翻译完成！Word 文档已保存。是否继续？」

---

### 🟢 Stage 3：总结 → Word 文档

**动作**：提炼论文核心框架，输出 .docx

**输出**：`/tmp/academic-ppt/[Doc_Title]_总结.docx`

**结构**：研究背景、核心贡献、方法与架构、实验结果、结论与局限

**确认语**：「总结完成！是否进入 PPT 大纲设计？」

---

### 🟢 Stage 4：PPT大纲设计

**动作**：根据总结设计 10-15 页 PPT 大纲

**输出格式**：
```
### Slide 1：标题页
- 要点：...

### Slide 2：研究背景
- 要点：...
```

**确认语**：「大纲完成（共 X 页）。确认后进入 PPT 生成阶段。」

---

### 🟢 Stage 5：生成 PPT（平台可选）

**根据用户选择的平台执行**：

#### 方案 A：anygen（推荐）
```bash
# 1. 准备任务
anygen task prepare --data '{"operation":"slide","messages":[{"role":"user","content":{"text":"[PPT需求]"}}]}'

# 2. 从响应获取 suggested_task_params，创建任务
anygen task create --data '{"operation":"slide","prompt":"[final_prompt]"}'

# 3. 轮询等待完成（可能需要几分钟）
anygen task get --params '{"task_id":"<id>"}' --wait --timeout 600000

# 4. 下载
anygen task +download --task-id <id> --output-dir /tmp/academic-ppt/
```

#### 方案 B：gamma.app
```bash
# 使用 gamma API（需用户提供 API Key）
curl -X POST https://api.gamma.app/v1/presentations \
  -H "Authorization: Bearer $GAMMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"[Doc_Title]","slides":[...]}'
```

#### 方案 C：跳过
跳过 PPT 生成，仅生成 Word 和演讲稿

**输出**：
- PPT 文件：`/tmp/academic-ppt/*.pptx`（如有）
- 或告知用户手动下载链接

**确认语**：「PPT 生成完成（或已跳过）。是否进入演讲稿撰写阶段？」

---

### 🟢 Stage 6：撰写演讲稿

**动作**：根据 PPT 大纲撰写逐字稿（Markdown）

**输出**：`/tmp/academic-ppt/speech_notes.md`

**风格**：口语化、连贯、包含过渡句

**确认语**：「演讲稿完成！全套物料已生成。」

---

### 🟢 Stage 7（自动）：发送文件到微信

**自动执行**，通过 `message` 工具发送所有文件：

```
message(action="send", channel="openclaw-weixin", media="<filepath>")
```

**发送内容**：
- `[Doc_Title]_翻译稿.docx`
- `[Doc_Title]_总结.docx`
- `*.pptx`（如有）
- `speech_notes.md`

**输出**：
```
✅ 全套学术汇报物料已生成！

📄 [Doc_Title]_翻译稿.docx
📄 [Doc_Title]_总结.docx
📊 [PPT文件名].pptx（如有）
📝 speech_notes.md

文件已发送到您的微信！
```

---

## 配置管理

**配置文件**：`~/.openclaw/skills/academic-presentation/config.json`

**结构**：
```json
{
  "ppt_provider": "anygen|gamma|skip",
  "ppt_api_key_env": "ANYGEN_API_KEY|GAMMA_API_KEY",
  "user_openid": "<微信openid>"
}
```

**查看/修改配置**：
- 询问用户当前配置
- 需要修改时说"重新配置学术汇报"

---

## 文件输出目录

所有文件：`/tmp/academic-ppt/`

文件名：
- `[Doc_Title]_翻译稿.docx`
- `[Doc_Title]_总结.docx`
- `*.pptx`
- `speech_notes.md`

---

## 快速触发

- 「学术汇报」
- 「论文汇报」
- 「帮我做PPT」
- 「论文转PPT」
- 「做学术汇报」
- 「重新配置学术汇报」

---

## 发布信息

- 版本：2.0.0
- 作者：Clawhub User
- 许可：MIT
- 来源：https://clawhub.ai/academic-presentation
