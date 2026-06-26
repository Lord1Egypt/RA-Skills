# 学术汇报全自动化 (Academic Presentation Workflow)

**将论文一键转化为：翻译稿 + 总结 + PPT + 演讲稿全套物料，自动发送到微信**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-blue.svg)](https://openclaw.ai)

---

## 🎯 简介

学术汇报全自动化是一个端到端的论文处理工作流。只需提供论文（PDF 或文本），即可自动生成：

- 📄 **翻译稿**（Word .docx）— 论文全文中文翻译
- 📄 **总结稿**（Word .docx）— 核心框架结构化总结
- 📊 **PPT 演示文稿**（.pptx）— 10-15 页汇报幻灯片
- 📝 **逐字演讲稿**（Markdown）— 每页配套口语化讲解

所有文件完成后**自动发送到你的微信**。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🚀 **全自动化** | 6 个阶段自动衔接，一键启动 |
| 📱 **微信通知** | PPT 生成后自动发送到微信，无需手动下载 |
| 📝 **Word 输出** | 翻译稿和总结稿直接输出为可编辑 .docx 文件 |
| 🎨 **智能 PPT** | 调用外部 PPT 生成 API，自动设计 10-15 页专业幻灯片 |
| 🔒 **安全私密** | API Key 由用户自行配置，不嵌入任何密钥 |
| 🌍 **通用平台** | 支持 anygen、gamma.app 等多种 PPT API |

---

## 🔧 安装与配置

### 前置要求

- OpenClaw 环境（v2026.1.0+）
- 微信通道已配置（用于自动发送文件）

### 安装 Skill

```bash
# 方式 1：Clawhub 安装
clawhub install academic-presentation

# 方式 2：手动复制
cp -r academic-presentation/ ~/.openclaw/skills/
```

### 首次配置 PPT 平台

首次触发时，技能会询问选择 PPT 生成平台：

```
请选择 PPT 生成方式：
1. anygen（推荐）- 需要 ANYGEN_API_KEY
2. gamma.app - 需要 GAMMA_API_KEY  
3. 跳过 PPT - 仅生成 Word 和演讲稿
```

选择后，输入对应的 API Key 即可。

### 支持的 PPT API

| 平台 | API Key 环境变量 | 注册地址 | 特点 |
|------|------------------|----------|------|
| **anygen.io** | `ANYGEN_API_KEY` | https://www.anygen.io | 中文支持好，推荐学术使用 |
| **gamma.app** | `GAMMA_API_KEY` | https://gamma.app | 国际通用 |
| **跳过** | 无 | — | 仅生成文档和讲稿 |

---

## 📖 工作流详解

### Stage 1：接收文档

提供论文 PDF 文件路径或直接粘贴论文文本，系统自动：
- 提取论文标题
- 识别语言（中文/英文/其他）
- 设定工作变量 `[Doc_Title]`

### Stage 2：核心内容翻译（可选）

将论文核心内容（摘要、引言、方法、实验、结论）翻译为流畅的中文学术语言，输出为 **Word 文档**。

**输出**：`/tmp/academic-ppt/[论文标题]_翻译稿.docx`

### Stage 3：论文精要总结

提炼论文核心框架，输出为结构化 **Word 文档**：

1. 研究背景与痛点 (Motivation)
2. 核心贡献 (Contributions)
3. 方法与架构 (Methodology)
4. 实验结果 (Experiments)
5. 结论与局限 (Conclusion)

**输出**：`/tmp/academic-ppt/[论文标题]_总结.docx`

### Stage 4：PPT 大纲设计

根据总结自动设计 10-15 页汇报大纲，每页包含：
- 标题
- 核心要点（3-5 个）
- 过渡句设计

### Stage 5：PPT 生成

调用你选择的 PPT API 生成专业演示文稿：

**输出**：`/tmp/academic-ppt/*.pptx`

> ⚠️ PPT 生成可能需要 1-5 分钟，请耐心等待

### Stage 6：逐字演讲稿

根据 PPT 每页内容，撰写配套**口语化逐字稿**，包含：
- 开场白和过渡句
- 每页讲解内容
- 总结和致谢

**输出**：`/tmp/academic-ppt/speech_notes.md`

### Stage 7：微信自动发送（🎉亮点）

所有文件生成完成后，自动通过微信发送给你：

- 📄 翻译稿（.docx）
- 📄 总结稿（.docx）
- 📊 PPT（.pptx）
- 📝 演讲稿（.md）

**无需手动下载**，文件直接出现在微信！

---

## 🚀 快速使用

### 触发技能

发送以下任一消息即可启动：

```
学术汇报
论文汇报
帮我做PPT
论文转PPT
做学术汇报
```

### 示例对话

```
你：学术汇报
助手：🎓 您好！已为您激活学术汇报全自动化技能。
      请将您的论文 PDF 文件路径发给我，或者直接粘贴正文。
      
你：[粘贴论文内容]

助手：✅ 已收到文档："Deep Residual Learning"
      语言：英文
      
      是否需要翻译为中文？

你：翻译

助手：[Stage 2 执行中...]
      📄 翻译稿已生成
      
      [Stage 3 执行中...]
      📄 总结稿已生成
      
      [Stage 4 执行中...]
      📋 PPT 大纲已设计（12页）
      
      [Stage 5 执行中...]
      ⏳ 正在生成 PPT...
      📊 PPT 已生成
      
      [Stage 6 执行中...]
      📝 演讲稿已撰写
      
      [Stage 7]
      📱 正在发送到微信...
      
      ✅ 全套物料已发送到您的微信！
```

---

## 📁 输出文件

| 文件 | 格式 | 说明 |
|------|------|------|
| `[标题]_翻译稿.docx` | Word | 论文全文中文翻译 |
| `[标题]_总结.docx` | Word | 核心框架结构化总结 |
| `*.pptx` | PowerPoint | 10-15 页演示文稿 |
| `speech_notes.md` | Markdown | 逐字演讲稿 |

默认保存路径：`/tmp/academic-ppt/`

---

## 🔐 安全说明

- ❌ **不嵌入**任何第三方 API Key
- ✅ API Key 由用户在配置阶段自行输入
- ✅ 仅保存在用户本地配置中
- ✅ 不会上传到任何第三方服务器

---

## 🛠 故障排除

### PPT 生成失败
- 检查 API Key 是否正确配置
- 确认 API 服务是否可用
- 可以选择"跳过 PPT"仅生成文档

### 微信未收到文件
- 确认微信通道已正确配置
- 检查 OpenClaw 微信插件版本

### Word 文档打不开
- 使用 Microsoft Word 或 WPS 打开
- 推荐 Office 2016+ 或对应格式支持

---

## 📝 示例论文

推荐测试的经典论文：

- **Deep Residual Learning** (ResNet) — Kaiming He et al.
- **Attention Is All You Need** (Transformer) — Vaswani et al.
- **BERT: Pre-training of Deep Bidirectional** — Devlin et al.

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License

---

## 👨‍💻 作者

Built with ❤️ for OpenClaw

---

## 🔗 相关链接

- [OpenClaw 文档](https://docs.openclaw.ai)
- [Clawhub Skills](https://clawhub.ai)
- [Issue Tracker](https://github.com/yourname/academic-presentation/issues)
