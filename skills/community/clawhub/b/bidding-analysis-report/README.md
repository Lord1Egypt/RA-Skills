# 招标数据分析报告生成技能

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

招标数据分析报告生成技能 - 支持AI项目占比分析、年度趋势分析、TOP机构排名，自动生成Word/PDF报告，嵌入高质量图表。

## ✨ 功能特性

- 📊 **AI项目占比分析** - 计算AI相关招标项目数和金额占比
- 📈 **年度趋势分析** - 分析多年度项目数和金额变化趋势
- 🏆 **TOP机构排名** - 统计招标项目数/金额排名前N的机构
- 📑 **分机构详细分析** - 每个机构的年度趋势和拓展建议
- 🎨 **图表自动生成** - 嵌套环形图、百分比柱状图
- 📄 **报告输出** - Word格式（推荐）或PDF格式

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/openclaw/bidding-analysis-report.git
cd bidding-analysis-report

# 安装依赖
pip install -r requirements.txt
```

## 🚀 快速开始

### 命令行使用

```bash
python bidding_report.py \
  --data 招标数据.xlsx \
  --title "昆明高校AI招标分析报告" \
  --output report.docx \
  --top 10 \
  --detail 5
```

### Python API

```python
from bidding_report import BiddingReport

# 创建报告实例
report = BiddingReport(
    data_path='招标数据.xlsx',
    ai_keywords=['人工智能', 'AI', '智能', '大数据'],
    output_format='word'
)

# 加载数据
report.load_data()

# 计算统计
report.calculate_stats()

# 生成报告
report.generate_word_report(
    title='昆明高校近三年AI项目分析报告',
    top_n=10,
    detail_n=5,
    output_path='report.docx'
)
```

## 📋 输入数据格式

Excel文件（.xlsx），需包含以下字段：

| 字段名 | 说明 | 必需 |
|--------|------|------|
| 项目名称 | 招标项目名称 | ✅ |
| 项目主体 | 项目分类/类型 | ✅ |
| 成交金额（元） | 中标金额 | ✅ |
| 信息采集日期 | 招标日期（时间戳或日期格式） | ✅ |
| 甲方名称 | 招标机构名称 | ✅ |

## 📊 输出报告结构

### 一、总体情况
1. AI项目数占比、金额占比（嵌套环形图）
2. 年度发展趋势分析（百分比柱状图）

### 二、TOP机构
- 项目数占比最高的N个机构列表
- 包含：机构名称、总招标数、招标总金额、AI项目数、AI金额
- 结合机构特点分析AI项目关联

### 三、分机构详细情况
每个机构包含：
1. 近3年招标项目总数及金额、AI项目数及金额（嵌套环形图）
2. 分年度AI项目趋势分析（百分比柱状图）
3. 拓展建议

## 🎨 图表配色方案

明亮科技风格配色：

| 元素 | 颜色 | 色值 |
|------|------|------|
| AI项目数 | 亮橙色 | `#FF8C42` |
| AI金额 | 青色 | `#00F5D4` |
| 其他项目 | 亮蓝色 | `#7ED4FF` |
| 其他金额 | 蓝色 | `#00D4FF` |

## ⚙️ 配置选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `data_path` | 数据文件路径 | 必填 |
| `ai_keywords` | AI项目识别关键词 | `['人工智能','AI','智能',...]` |
| `output_format` | 输出格式 | `'word'` |
| `top_n` | TOP机构数量 | 10 |
| `detail_n` | 详细分析机构数量 | 5 |
| `chart_dpi` | 图表分辨率 | 150 |
| `line_spacing` | 行距倍数 | 1.5 |

## 📝 示例输出

### 昆明高校AI招标分析报告（2023-2026）

**总体情况**：
- 总招标项目：6,786项
- AI相关项目：1,193项（占比 17.6%）
- 总招标金额：96亿元
- AI项目金额：15亿元（占比 15.6%）

**年度趋势**：
- 2023年：AI项目占比 14.8%
- 2024年：AI项目占比 16.8%
- 2025年：AI项目占比 20.7%
- 2026Q1：AI项目占比 15.7%

## 🛠 技术栈

- **Python 3.8+**
- **pandas** - 数据处理
- **matplotlib** - 图表生成
- **python-docx** - Word文档生成
- **openpyxl** - Excel文件读取

## 📌 注意事项

1. **中文字体**：优先使用微软雅黑，系统不支持时自动回退到 Droid Sans Fallback
2. **数据格式**：确保Excel文件包含必需字段，日期字段需可解析
3. **图表嵌入**：Word格式推荐，PDF格式中文字体支持有限
4. **数据填充**：使用 `.format()` 或字符串拼接，避免 f-string 编码问题

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[MIT License](LICENSE)

## 👥 作者

OpenClaw Team

---

**更新时间**: 2026-04-21  
**版本**: v1.0.0
