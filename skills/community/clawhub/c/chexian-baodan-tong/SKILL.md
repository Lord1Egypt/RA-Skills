---
name: chexian-baodan-tong
description: 车险保单通 — 一站搞定重命名和归档。消除低效环节，让代理人和保险公司工作人员一站搞定识别、整理、重命名、归档保险保单，让保险保单归档更直接、更便捷。支持识别多家保险公司保单 PDF，自动提取车牌号、投保人、保单号，追加车牌号重命名文件，本地模式（pdfminer）与 API 模式（AI 解析）双轨并行，整理完毕后自动打包为 ZIP 文件。
---

# 车险保单通
> 一站搞定重命名和归档 · V1.0.1
> 作者：WuWenBin-BeiJing-ST

**车险保单通**消除低效环节，让代理人和保险公司工作人员一站搞定识别、整理、重命名、归档保险保单，让保险保单归档更直接、更便捷。

## 核心脚本

`scripts/extract_and_rename.py` — 唯一入口脚本，包含全部逻辑。

## 功能特性

| 功能 | 说明 |
|------|------|
| 📄 PDF 识别 | 自动扫描指定文件夹下所有 PDF 保单文件 |
| 🔍 信息提取 | 提取**车牌号**、**投保人**、**保单号** |
| ✏️ 自动重命名 | `{原名}_{车牌号}.pdf`，如 `Policy_xxx_晋MX0923.pdf` |
| 🤖 双模式 | **本地模式**（pdfminer，正则匹配，无需联网）<br>**API 模式**（AI 解析，更精准，需配置 API Key） |
| 📦 ZIP 打包 | 自动打包为 `保险单整理_YYYYMMDD.zip` |

## 工作流程

```
用户指定文件夹
    │
    ▼
┌──────────────────────┐
│   选择解析模式        │
├──────────────────────┤
│ 本地模式（默认）       │  ← 使用 pdfminer.six + 正则匹配
│ API 模式（--api）      │  ← 调用外部 AI API 解析
└──────────────────────┘
    │
    ▼
提取：车牌号 / 投保人 / 保单号
    │
    ▼
重命名文件：{原名}_{车牌号}.pdf
    │
    ▼
打包 ZIP：保险单整理_YYYYMMDD.zip
```

## 使用方式

### 命令行参数

| 参数 | 说明 |
|------|------|
| `folder` | PDF 文件所在文件夹（默认当前目录） |
| `--no-rename` | 跳过文件重命名（预览模式） |
| `--no-pack` | 跳过 ZIP 打包 |
| `--api` | 使用 API 模式（需设置环境变量） |
| `--zip-name` | 自定义 ZIP 文件名 |

### 典型用法

```bash
# 本地模式（默认，无需联网）
python3 ~/.qclaw/skills/chexian-baodan-tong/scripts/extract_and_rename.py ~/Downloads

# API 模式（需设置 INSURANCE_API_KEY）
python3 ~/.qclaw/skills/chexian-baodan-tong/scripts/extract_and_rename.py ~/Downloads --api

# 预览模式（不重命名、不打包）
python3 ~/.qclaw/skills/chexian-baodan-tong/scripts/extract_and_rename.py ~/Downloads --no-rename --no-pack
```

### 环境变量（API 模式）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `INSURANCE_API_KEY` | API 密钥（必需） | - |
| `INSURANCE_API_ENDPOINT` | API 端点 | OpenAI 兼容接口 |
| `INSURANCE_API_MODEL` | 模型名称 | `gpt-4o` |

## 解析模式选择建议

**本地模式**：速度快、无需联网，对标准格式保险单识别率高。**首选方案。**

**API 模式**：识别率更高，能处理复杂/非标准格式或扫描图片类 PDF（无文字层）。需要配置 `INSURANCE_API_KEY`。

推荐工作流：
1. 先用本地模式尝试
2. 如返回"未识别"，切换到 API 模式重试

## 提取字段说明

| 字段 | 提取逻辑 | 备注 |
|------|---------|------|
| 车牌号 | 在"车牌号"标签后跨行匹配省级简称+字母+数字 | 支持晋/京/沪等全部省份格式 |
| 投保人 | 在"投保人"/"被保险人"标签后查找公司名或姓名 | 优先返回公司名称 |
| 保单号 | 在"保单号码"标签后查找大写字母数字组合 | 通常 15-22 位 |

## 重命名规则

- **有车牌号**：`{原文件名}_{车牌号}.pdf`
  - 例如：`Policy_abc.pdf` → `Policy_abc_晋MX0923.pdf`
- **无车牌号但有保单号**：`{原文件名}_{保单号}.pdf`
- **都未识别**：跳过重命名，标记"未识别"

## ZIP 打包规则

- 文件名格式：`保险单整理_YYYYMMDD.zip`
- 打包范围：目标文件夹下所有文件
- 同一日期多次运行会覆盖前一次 ZIP

## 依赖安装

本地模式依赖 `pdfminer.six`：

```bash
pip install pdfminer.six
```

## 注意事项

- 脚本直接修改原文件，完成后 PDF 已被重命名，建议先做备份或使用 `--no-rename` 预览
- 本地模式对纯扫描图片类 PDF（无文字层）识别率极低，建议切换到 API 模式
