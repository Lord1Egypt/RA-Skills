# Feishu File Delivery 飞书文件交付

[![GitHub](https://img.shields.io/badge/GitHub-openclaw--feishu--file--delivery-blue)](https://github.com/wd041216-bit/openclaw-feishu-file-delivery)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

Deliver locally generated office files back into Feishu chats as real attachments.
将本地生成的办公文件自动作为真实附件上传到飞书会话。

## ✨ Features 功能特点

- 📎 **Auto-upload attachments** — Feishu adapter detects absolute paths and uploads files automatically
  自动上传附件 — 飞书适配器检测绝对路径并自动上传文件

- 📄 **Multiple formats** — Supports `.pptx`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.zip`, `.txt`, `.md`
  多种格式支持

- 🚀 **Streaming mode** — Real-time progress updates for long-running tasks
  流式模式 — 长任务实时进度更新

- 🔗 **Zero-config integration** — Works seamlessly with other OpenClaw skills
  零配置集成 — 与其他 OpenClaw 技能无缝协作

## 🚀 Quick Start 快速开始

### Basic Usage 基本用法

1. Generate your file locally (本地生成文件)
2. In your Feishu reply, include the absolute path on its own line (在飞书回复中，将绝对路径放在单独的行上)

```text
报告已生成：
/Users/dawei/Documents/weekly-report.pdf
/Users/dawei/Documents/weekly-report.pptx
```

The Feishu adapter will automatically attach these files!
飞书适配器会自动附加这些文件！

### With Streaming Mode 启用流式模式

For long-running tasks (file generation, conversion, etc.):
对于长任务（文件生成、转换等）：

```text
[0%] 开始生成文件...
[33%] 正在处理数据...
[66%] 正在生成图表...
[100%] 完成！

文件已就绪：
/Users/dawei/Documents/output.pptx
```

## 📦 Installation 安装

### Via ClawHub 通过 ClawHub

```bash
clawhub install feishu-file-delivery
```

### Manual Install 手动安装

```bash
git clone https://github.com/wd041216-bit/openclaw-feishu-file-delivery.git
cd openclaw-feishu-file-delivery
# Skills are auto-loaded from ~/.openclaw/workspace/skills/
```

## 📁 File Structure 文件结构

```
feishu-file-delivery/
├── SKILL.md          # Skill definition & usage guide 技能定义与使用指南
├── README.md         # This documentation 本文档
├── skill.json        # Metadata for discovery 发现元数据
├── _meta.json        # Publish metadata 发布元数据
└── agents/           # Optional agent configurations 可选代理配置
    └── delivery.agent.md
```

## 🔌 Integrations 集成

This skill integrates with:
本技能与以下技能集成：

| Skill | Description |
|-------|-------------|
| `pptx-design-director` | Professional PPT design 专业 PPT 设计 |
| `pdf-generator` | PDF document generation PDF 文档生成 |
| `word-docx` | Word document operations Word 文档操作 |
| `powerpoint-pptx` | PowerPoint manipulation PowerPoint 操作 |
| `openclaw-slides` | HTML slide generation HTML 幻灯片生成 |
| `feishu-doc` | Feishu cloud docs 飞书云文档 |
| `feishu-sheets` | Feishu spreadsheets 飞书表格 |

## 📝 Examples 示例

### Example 1: PPTX Delivery PPTX 交付

```text
演示文稿已完成，包含 15 页内容：
/Users/dawei/.openclaw/workspace-council/output/quarterly-review.pptx
```

### Example 2: Multiple Files 多个文件

```text
已生成所有文件：
/Users/dawei/Documents/report.pdf
/Users/dawei/Documents/report.docx
/Users/dawei/Documents/data.csv
```

### Example 3: With Progress Streaming 带进度流式传输

```text
[启动] 开始生成文件
[进度 50%] 正在处理...
[完成] 文件就绪

/Users/dawei/Documents/final-output.xlsx
```

## ⚙️ Configuration 配置

### Streaming Response 流式回复

Enable streaming in Feishu channels by using progress markers:
在飞书通道中通过使用进度标记启用流式回复：

- `[0%]` — Task started 任务开始
- `[X%]` — Progress update 进度更新
- `[100%]` — Complete 完成

### Path Format 路径格式

✅ **Correct 正确:**
```
/Users/dawei/Documents/file.pdf
```

❌ **Incorrect 错误:**
```
- /Users/dawei/Documents/file.pdf  (bullet 项目符号)
- [file](/Users/dawei/Documents/file.pdf)  (markdown link Markdown 链接)
- ~/Documents/file.pdf  (tilde expansion 波浪号扩展)
```

## 🛠️ Troubleshooting 故障排除

### Files Not Uploading 文件未上传

1. **Check file exists** 检查文件是否存在
   ```bash
   ls -la /path/to/your/file.pdf
   ```

2. **Verify absolute path** 验证绝对路径
   - Use full path, not relative (使用完整路径，非相对路径)
   - No `~` expansion (无波浪号扩展)

3. **Check formatting** 检查格式
   - One path per line (每行一个路径)
   - No bullets or markdown (无项目符号或 Markdown)

4. **Check adapter logs** 检查适配器日志
   ```bash
   openclaw gateway logs
   ```

### Streaming Not Working 流式传输不工作

1. Ensure you're in a Feishu channel (确保在飞书通道中)
2. Use progress markers (使用进度标记)
3. Check `feishu-progress-heartbeat` skill is available (检查技能可用)

## 🤝 Contributing 贡献

Contributions welcome! Please:
欢迎贡献！请：

1. Fork the repository
2. Create a feature branch (创建功能分支)
3. Make your changes (进行更改)
4. Submit a PR (提交 PR)

## 📄 License 许可证

MIT License — see [LICENSE](LICENSE) for details.

## 🔗 Links 链接

- [GitHub Repository](https://github.com/wd041216-bit/openclaw-feishu-file-delivery)
- [OpenClaw Documentation](https://openclaw.ai)
- [Feishu/OpenLark](https://www.feishu.cn)

---

**Author:** Dawei
**Version:** 2.0.0 (Optimized with streaming mode)
**Last Updated:** 2026-03-14
