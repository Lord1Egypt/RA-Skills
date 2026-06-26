# 火山引擎 Skillhub 上架信息 — 报表自动生成

## 基本信息

| 字段 | 内容 |
|------|------|
| **Skill 名称** | 报表自动生成 |
| **副标题** | 上传数据，AI自动生成专业报表（图表+分析） |
| **分类** | 办公效率 > 数据分析 > 报表生成 |
| **语言** | 中文（默认）、English |

---

## 功能详细描述

### 核心能力

**报表自动生成** 是一款 AI 驱动的数据报表生成工具。用户只需上传 CSV 或 Excel 数据文件，系统将自动完成：

1. **数据解析**：自动识别 CSV/Excel 格式，解析行列结构
2. **AI 数据分析**：调用大语言模型，自动发现数据模式、趋势和异常
3. **图表生成**：根据数据特征自动选择最佳图表类型（折线/柱状/饼图/散点/面积/热力图）
4. **报表构建**：生成专业 Excel 报表（多 Sheet 含格式），附带 AI 文字分析
5. **多模板支持**：月报、财务、销售、对比、自定义等多种报表模板

### 适用场景

- 📊 **月报生成**：财务、运营、市场等周期性报表自动生成
- 💰 **财务分析**：P&L、收入分析、成本汇总等财务报表
- 📈 **销售分析**：销售业绩追踪、区域对比、趋势预测
- 🔍 **数据对比**：多时期/多维度数据对比分析报告
- 📋 **自定义报表**：灵活配置模板满足特定业务需求

### 技术特性

- 支持 CSV、Excel (.xlsx/.xls) 格式
- 最大支持 50MB 文件
- 支持多图表类型（折线图、柱状图、饼图、散点图、面积图、热力图）
- AI 文字分析自动生成关键洞察
- Excel 多 Sheet 导出，含格式化标题、数据表、图表
- 内置额度管理系统，免费用户 5 次

---

## 套餐说明

| 套餐 | 价格 | 月额度 | 图表数 | PDF导出 | 自定义模板 |
|------|------|--------|--------|---------|-----------|
| **FREE** | ¥0 | 5次（终身） | 每报表1个 | ❌ | ❌ |
| **STD** | ¥9.9/月 | 50次/月 | 每报表3个 | ❌ | ❌ |
| **PRO** | ¥29.9/月 | 200次/月 | 不限 | ✅ | ❌ |
| **MAX** | ¥99/月 | 不限次 | 不限 | ✅ | ✅ |

### Token 前缀

| 套餐 | Token前缀 |
|------|-----------|
| FREE | `REPORT-FREE` |
| STD | `REPORT-STD` |
| PRO | `REPORT-PRO` |
| MAX | `REPORT-MAX` |

---

## 技术要求

### 运行环境

- **Python 版本**：Python 3.8 及以上
- **操作系统**：Linux / macOS / Windows

### Python 依赖

```
pandas>=1.3.0
openpyxl>=3.0.0
xlsxwriter>=3.0.0
matplotlib>=3.4.0
Pillow>=8.0.0
requests>=2.25.0
numpy>=1.20.0
```

### AI API 要求

- OpenAI API Key（环境变量 `OPENAI_API_KEY`）
- 或 DeepSeek API Key（环境变量 `DEEPSEEK_API_KEY`）

---

## 安装步骤

```bash
# 1. 进入技能目录
cd auto-report-generator

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
export OPENAI_API_KEY="sk-your-key-here"

# 4. 运行
python scripts/generator.py --file data.csv --template monthly --output report.xlsx
```

---

## 使用示例

### 命令行使用

```bash
# 基础用法
python scripts/generator.py --file 销售数据.csv --template 销售 --output 月报.xlsx

# 指定 AI 提供商
python scripts/generator.py \
    --file 数据.xlsx \
    --template 月报 \
    --ai-provider deepseek \
    --ai-model deepseek-chat \
    --tier STD \
    --output 报表.xlsx
```

### Python API 使用

```python
from scripts.generator import ReportGenerator

generator = ReportGenerator(
    ai_provider="openai",
    ai_model="gpt-4",
    tier="PRO"
)

result = generator.generate(
    file="sales_data.csv",
    template="monthly",
    output="monthly_report.xlsx"
)
```

---

## 上架前清理命令

在发布前，请务必执行以下清理命令，删除打包残留的空目录：

```bash
# 删除 scripts、templates、core 空目录（打包残留）
rm -rf /home/gem/workspace/agent/workspace/skills/auto-report-generator/scripts
rm -rf /home/gem/workspace/agent/workspace/skills/auto-report-generator/templates
rm -rf /home/gem/workspace/agent/workspace/skills/auto-report-generator/core

# 如果创建了错误的字面量目录，也一并删除
rm -rf '/home/gem/workspace/agent/workspace/skills/auto-report-generator/{scripts,templates,core}'
```

---

## 打包前最终检查

打包发布前，确认目录结构如下（无空目录）：

```
auto-report-generator/
├── SKILL.md
├── README.md
├── CLAWHUB.md
├── SKILLHUB.md
└── requirements.txt
```

执行以下命令验证：

```bash
# 检查是否有空目录
find /home/gem/workspace/agent/workspace/skills/auto-report-generator -type d -empty

# 应无输出，表示无空目录

# 查看最终文件列表
ls -la /home/gem/workspace/agent/workspace/skills/auto-report-generator/
```

---

## 注意事项

1. **数据隐私**：数据在本地处理，仅 AI 请求会发送到外部 API
2. **免费额度**：FREE 套餐限制 5 次（终身），非每月重置
3. **文件格式**：建议使用 .xlsx 格式以获得最佳兼容性
4. **列标题**：数据文件第一行必须包含列标题
5. **数值列**：至少需要一列数值数据才能生成图表
6. **API Key**：使用 AI 功能前请确保已配置有效的 API Key
