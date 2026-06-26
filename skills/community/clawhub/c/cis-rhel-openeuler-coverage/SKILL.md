---
name: cis-rhel-openeuler-coverage
description: "分析 CIS Red Hat Enterprise Linux Benchmark 中的安全规则在 OpenEuler 安全配置基线中的覆盖情况，输出完全覆盖、部分覆盖、未覆盖的规则清单。适用于：用户提供 CIS RHEL Benchmark PDF 文件路径和 OpenEuler 安全基线 MD 文件路径，要求进行规则级覆盖分析。当用户提到 'CIS覆盖分析'、'CIS对比OpenEuler'、'CIS合规差距'、'安全基线比对'、'规则覆盖检查' 时，务必使用此技能。"
---

# CIS RHEL Benchmark → OpenEuler 安全基线覆盖分析

对 CIS Red Hat Enterprise Linux Benchmark PDF 中的每一条安全规则，与 OpenEuler 安全配置基线 Markdown 文档进行逐项对比，输出覆盖分析报告。

## 使用方式

用户提供两个文件路径即可触发完整分析流程：

```
老大，分析 CIS 覆盖情况
  CIS PDF: /path/to/CIS_Red_Hat_Enterprise_Linux_9_Benchmark.pdf
  OpenEuler 基线: /path/to/openeuler-security-baseline.md
```

## 工作流

### 步骤 1：确认输入

确认用户同时提供了以下两个文件路径：
- **CIS RHEL Benchmark PDF** — CIS 官方发布的 PDF 格式 Benchmark 文档
- **OpenEuler 安全配置基线** — Markdown 格式的 OpenEuler 基线文档

### 步骤 2：解析 CIS PDF

运行 `scripts/parse_cis_pdf.py` 提取 CIS 规则清单：

```bash
python scripts/parse_cis_pdf.py "<cis-pdf-path>" -o "<output-dir>/cis_rules.json"
```

输出 JSON 结构：
```json
[
  {
    "rule_id": "1.1.1.1",
    "title": "Ensure mounting of cramfs filesystems is disabled",
    "config_path": "/etc/modprobe.d/CIS.conf",
    "config_param": "install cramfs /bin/false",
    "expected_value": "install cramfs /bin/false",
    "level": "Level 1",
    "scoring": "Scored"
  }
]
```

关键提取字段：规则编号、标题、配置项路径、参数名、期望值、级别、评分状态。

### 步骤 3：解析 OpenEuler 基线 MD

运行 `scripts/parse_openeuler_md.py` 提取基线条目：

```bash
python scripts/parse_openeuler_md.py "<openeuler-md-path>" -o "<output-dir>/openeuler_items.json"
```

输出 JSON 结构：
```json
[
  {
    "item_id": "2.1",
    "config_path": "/etc/ssh/sshd_config",
    "config_param": "MaxAuthTries",
    "expected_value": "3",
    "description": "SSH 最大认证尝试次数设置为 3"
  }
]
```

关键提取字段：条目编号、配置项路径、参数名、期望值、描述。

### 步骤 4：覆盖分析

运行 `scripts/coverage_analyzer.py` 执行匹配和判定：

```bash
python scripts/coverage_analyzer.py \
  --cis "<output-dir>/cis_rules.json" \
  --openeuler "<output-dir>/openeuler_items.json" \
  -o "<output-dir>/analysis_result.json"
```

#### 匹配策略

1. **精确匹配** — 配置项路径+参数名完全一致
2. **模糊匹配**（精确匹配失败后）— 使用 thefuzz 计算路径相似度，阈值 ≥ 85%
3. **人工标记**— 对于模糊匹配结果，标记需人工确认

#### 覆盖判定标准

| 状态 | 判定条件 |
|------|----------|
| ✅ 完全覆盖 (Fully Covered) | 路径匹配 + OpenEuler 要求值在安全严格度上 **≥ CIS 要求**（同等或更安全） |
| ⚠️ 部分覆盖 (Partially Covered) | 路径匹配但要求值无法自动判定安全严格度、或存在差异但无法确认更安全 |
| ❌ 未覆盖 (Not Covered) | 配置项在 OpenEuler 基线中不存在（精确 + 模糊均未匹配） |

#### 数值安全性比较规则

- **数字比较**：对于 "最大尝试次数"、"超时秒数" 等数值，CIS 要求 ≤ 3，OpenEuler 为 3 或更小 → 完全覆盖；若为 4 → 部分覆盖
- **布尔/状态值**：`yes`/`no`、`true`/`false`、`enabled`/`disabled` — 优先级认定一致则为覆盖
- **路径/Permissions**：权限值 `600` 比 `644` 更严格，`700` 比 `755` 更严格
- **未知模式**：无法自动判断的，归类为部分覆盖，标注"需人工确认"

### 步骤 5：生成报告

运行 `scripts/report_generator.py` 输出中英文 CSV：

```bash
python scripts/report_generator.py \
  --analysis "<output-dir>/analysis_result.json" \
  -o "<openeuler基线所在目录>"
```

生成文件：
- `<openeuler基线所在目录>/coverage_report_zh.csv` — 中文报告
- `<openeuler基线所在目录>/coverage_report_en.csv` — 英文报告

#### 报告列定义

| 中文报告 | 英文报告 | 说明 |
|----------|----------|------|
| CIS 规则编号 | CIS Rule ID | CIS 基准规则编号 |
| CIS 规则标题 | CIS Rule Title | CIS 规则标题 |
| 配置项路径 | Config Path | 受影响的配置文件或路径 |
| 配置参数 | Config Parameter | 具体的配置项 |
| CIS 期望值 | CIS Expected Value | CIS 要求的值 |
| OpenEuler 要求值 | OpenEuler Value | OpenEuler 基线定义的值 |
| 覆盖状态 | Coverage Status | 完全覆盖/部分覆盖/未覆盖 |
| 备注 | Remarks | 差异说明或人工确认提示 |

## 文件结构

```
cis-rhel-openeuler-coverage/
├── SKILL.md                       # 本文件
├── requirements.txt               # Python 依赖
└── scripts/
    ├── parse_cis_pdf.py           # CIS PDF 规则提取
    ├── parse_openeuler_md.py      # OpenEuler MD 基线解析
    ├── coverage_analyzer.py       # 匹配与覆盖分析
    └── report_generator.py        # 中英文 CSV 报告输出
```

## 依赖安装

首次使用前运行：

```bash
pip install -r "<skills-dir>/cis-rhel-openeuler-coverage/requirements.txt"
```

## 安全注意事项

- 本技能仅处理文档级分析，不修改任何系统配置
- CIS Benchmark PDF 和 OpenEuler 基线仅用于只读分析
- 生成的报告不包含凭据等敏感信息
