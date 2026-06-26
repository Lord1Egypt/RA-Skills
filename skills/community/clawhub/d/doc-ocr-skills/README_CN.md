# Document OCR Skill (docr)

[![Go Version](https://img.shields.io/badge/Go-1.21+-00ADD8?style=flat&logo=go)](https://golang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[English Version](./README.md)

一个强大、单二进制文件的命令行工具，用于对扫描的 PDF 和图像进行光学字符识别 (OCR)。支持多种引擎，包括 **Gemini 2.5 Flash**、**PaddleOCR** 和 **RapidOCR**。

## ✨ 功能特性

- **多引擎支持**：可选云端 (Gemini) 或本地 (PaddleOCR, RapidOCR) 引擎。
- **单二进制文件**：使用 Go 编译，方便分发和安装。
- **批量处理**：支持单条命令处理整个目录的文档。
- **跨平台**：支持 macOS (Darwin)、Linux 和 Windows。
- **自定义提示词**：使用 Gemini 时，可以通过自定义提示词增强识别效果。

## 🚀 快速开始

### 一键安装

```bash
npx skills add scottkiss/doc-ocr-skills
```

### 手动安装 (二进制)

使用我们的安装脚本下载适用于您系统的最新预编译二进制文件：

```bash
curl -sSL https://raw.githubusercontent.com/scottkiss/doc-ocr-skills/main/scripts/install.sh | bash
```

*注意：脚本会将 `docr` 二进制文件安装到运行目录下的 `docr` 文件夹中。建议将其添加到 PATH 以便全局访问。*

### 源码编译

如果您安装了 Go 1.21+：

```bash
git clone https://github.com/scottkiss/doc-ocr-skills.git
cd doc-ocr-skills/scripts/docr
go build -o docr .
```

## 🛠 前置条件

### 本地引擎 (可选)
如果您打算使用本地 OCR 引擎，请确保已安装相应的 Python 包：

- **RapidOCR** (默认): `pip install rapidocr_onnxruntime`
- **PaddleOCR**: `pip install paddleocr paddlepaddle`

### API 配置 (针对 Gemini)
要使用 Gemini 引擎，请在 `~/.ocr/config` 创建配置文件：

```bash
mkdir -p ~/.ocr
cat > ~/.ocr/config << EOF
# Google Gemini API Key
gemini_api_key=您的_gemini_密钥
EOF
```

## 📖 使用方法

### 基础识别
使用默认引擎 (RapidOCR) 识别文本：
```bash
docr document.pdf
docr image.png
```

### 指定引擎
```bash
# 使用 Google Gemini (需要 API Key)
docr -engine gemini document.pdf

# 使用 PaddleOCR (本地)
docr -engine paddle document.pdf
```

### 批量处理
处理目录下所有受支持的文件，并将结果保存到输出文件夹：
```bash
docr -batch ./input_docs/ -o ./output_results/
```

### 命令行选项

| 选项 (Flag) | 描述 |
|------|-------------|
| `-engine`, `-e` | 使用的 OCR 引擎：`rapid` (默认), `gemini`, 或 `paddle`。 |
| `-o`, `-output` | 输出文件或目录的路径（用于批量模式）。 |
| `-batch` | 开启目录批量处理模式。 |
| `-prompt` | 自定义识别提示词（仅适用于 Gemini）。 |

## ❗ 故障排除

| 问题 | 解决方案 |
|-------|----------|
| `config file not found` | 确保 `~/.ocr/config` 文件存在。 |
| `gemini_api_key not found` | 检查配置文件中是否已正确设置密钥。 |
| `pip: command not found` | 确保已安装 Python 和 pip 以使用本地引擎。 |
| Permission Denied | 对二进制文件运行 `chmod +x docr`。 |

## 📄 开源协议

本项目采用 MIT 协议开源。
