# deepaistudy-prep Skill

深智智智能学习系统预习课件生成 Skill。通过 AI 分析教材 PDF 或图片，生成互动预习课件（SVG幻灯片 + 小测验）。

## 工作原理

```
用户图片/PDF → [Qwen VL Max OCR] → 课文原文 → [Gemini SVG生成] → 互动幻灯片 + 小测
```

## 前置要求

1. **服务器运行中**：本地开发服务器（`cd ~/study_ai && ./start_dev.sh`）或远程 www.deepaistudy.com
2. **用户已登录**：浏览器中已登录深智智网站
3. **AI 余额充足**：余额不足会导致生成失败

## 使用方式

### 方式 1：AI 分析 PDF（推荐）

分析 PDF 并自动识别目录、学科、年级：

```bash
deepaistudy-prep analyze /path/to/textbook.pdf --ai
```

### 方式 2：上传图片生成预习

```bash
deepaistudy-prep upload /path/to/images/*.jpg \
  --subject 数学 \
  --grade "小学三年级" \
  --topic "第一章 加减法" \
  --difficulty medium
```

### 方式 3：批量从 PDF 生成（整本书）

```bash
deepaistudy-prep batch /path/to/textbook.pdf \
  --subject 数学 \
  --grade "小学三年级" \
  --auto-split
```

## 配置

首次使用需要设置服务器地址和认证：

```bash
deepaistudy-prep config set server https://www.deepaistudy.com
deepaistudy-prep config set username your_email@domain.com
deepaistudy-prep config set password your_password
```

查看当前配置：

```bash
deepaistudy-prep config list
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `analyze <file> --ai` | AI 自动分析 PDF |
| `upload <path> --subject X --grade Y` | 上传图片生成预习 |
| `batch <file> --auto-split` | 批量从 PDF 生成 |
| `list` | 查看预习列表 |
| `status <prep_id>` | 查看生成状态 |
| `result <prep_id>` | 获取生成结果 |
| `config set <key> <value>` | 设置配置项 |
| `config list` | 查看当前配置 |

## 返回内容

生成完成后返回：

- `ocr_text`：课文原文（OCR 识别）
- `animation_svg`：SVG 格式互动幻灯片
- `slide_images`：渲染后的 PNG 图片
- `interactive_preview.quiz`：预习小测验题目
- `knowledge_points`：知识点列表

## 状态说明

| 状态 | 说明 |
|------|------|
| `queued` | 排队中 |
| `processing` | 生成中 |
| `completed` | 完成 |
| `failed` | 失败 |

## 注意事项

- 生成大约需要 1-3 分钟（OCR + AI 生成）
- 图片会缩放到最大 2048px
- 支持学科：语文、数学、英语、物理、化学等
- 小测答对才算预习完成
