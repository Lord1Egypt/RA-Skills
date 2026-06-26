---
name: arxiv-downloader
description: |
  arXiv 论文 PDF/LaTeX 源码下载工具。支持通过 arXiv ID 或 URL 下载论文。
  当用户提到下载 arXiv 论文、获取 PDF、下载 LaTeX 源码时使用。
  触发条件：(1) 用户要求下载 arXiv 论文 (2) 提供 arXiv ID 或链接 (3) 需要 PDF 或源码
---

# arXiv Downloader

从 arXiv 下载论文 PDF 或 LaTeX 源码。

## 使用方法

### 基本下载 PDF

```bash
python ~/.openclaw/workspace/skills/arxiv-downloader/scripts/download_arxiv.py <arxiv-id-or-url> [output_dir]
```

**示例：**
```bash
# 通过 ID 下载
python download_arxiv.py 2301.12345

# 通过 URL 下载
python download_arxiv.py https://arxiv.org/abs/2301.12345

# 指定输出目录
python download_arxiv.py 2301.12345 ~/Papers
```

### 下载 LaTeX 源码

```bash
python download_arxiv.py <arxiv-id> --latex
```

### 自定义文件名

```bash
python download_arxiv.py 2301.12345 --name my-paper
```

## 支持的格式

| 参数 | 说明 |
|------|------|
| 无参数 | 下载 PDF |
| `--latex` | 下载 LaTeX 源码（.tar.gz） |
| `--name` | 自定义输出文件名 |

## 常见 arXiv ID 格式

- 新格式：`2301.12345`（年份.编号）
- 带版本：`2301.12345v2`
- URL：`https://arxiv.org/abs/2301.12345`

## 实现说明

脚本使用 `urllib` 下载文件，模拟浏览器 User-Agent，支持重试机制（最多 3 次）。

PDF URL: `https://arxiv.org/pdf/{id}.pdf`
LaTeX URL: `https://arxiv.org/e-print/{id}`