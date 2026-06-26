---
name: cost-report-generator
description: 从项目费用 Excel 文件（如 EVP 项目费用.xlsx）自动生成按客户分类的成本分析报告。支持帝国、BAT、MT、ITMS 等客户分类，包含 2025 年和 2026 年成本分析，自动计算年度汇总、月度明细、月均数据。使用场景：用户发送类似"EVP 项目费用.xlsx"的文件并要求生成成本分析报告，或提到"按客户提炼成本"、"生成成本分析报告"、"整理项目费用"等。
---

# 成本分析报告生成器

从项目费用 Excel 文件自动生成按客户分类的成本分析报告。

## 触发条件

当用户：
- 上传类似 `EVP 项目费用.xlsx` 的文件并要求生成成本分析报告
- 提到"按客户分类生成成本报告"、"提炼成本分析"、"整理项目费用"
- 发送包含客户费用数据的 Excel 文件

## 核心功能

1. **自动识别客户分类**：帝国、BAT、MT、ITMS 等
2. **费用分类汇总**：
   - HR 费用（人工费用）
   - 试产/打样费用（打样 + 制造 + 物料耗用）
   - 测试费用（测试 + 外发认证）
   - 开发投资（开模 + 改模）
   - 其他费用（IDC、品烟、其它、手板）
3. **时间维度**：2025 年（12 个月）、2026 年（1-2 月）
4. **数据指标**：年度汇总、月均、月度明细
5. **格式化输出**：千分符、两位小数、美化样式

## 使用方法

### 方式 1：直接运行脚本

```bash
python3 ~/.openclaw/workspace/skills/cost-report-generator/scripts/generate_cost_report.py <源文件路径> [输出目录]
```

示例：
```bash
python3 ~/.openclaw/workspace/skills/cost-report-generator/scripts/generate_cost_report.py ~/Desktop/EVP_项目费用.xlsx
```

### 方式 2：通过 Python 调用

```python
from scripts.generate_cost_report import generate_cost_report

output_file = generate_cost_report(
    source_file="/path/to/EVP_项目费用.xlsx",
    output_dir="/path/to/output"  # 可选，默认为源文件所在目录
)
```

## 输入文件格式

### 必需列

- **客户大类**：客户分类（帝国、BAT、MT、ITMS 等）
- **项目大类**：项目名称/类别
- **内部订单号**：订单编号

### 费用列（按年份和月份）

支持的费用类型：
- 人工费用
- 打样费用
- 制造费用
- 物料耗用
- 测试费用
- 外发认证费用
- 开模费用
- 改模费用
- IDC 费用
- 品烟费用
- 其它费用
- 手板费用

列名格式：`{年份} 年{月份} 月{费用类型}`，如：
- `25 年 1 月人工费用`
- `25 年打样费用`（年度汇总）
- `26 年 1-2 月人工费用`

### 表头位置

脚本默认使用**第 4 行**（索引 3）作为表头。如果源文件格式不同，需要调整 `header` 参数。

## 输出报告结构

### 工作表

1. **2025 年成本分析**：按客户分类展示 2025 年 1-12 月数据
2. **2026 年成本分析**：按客户分类展示 2026 年 1-2 月数据

### 列结构（每个客户分类）

| 列范围 | 内容 |
|--------|------|
| A-C | 基本信息（客户大类、项目大类、内部订单号） |
| D-E | HR 费用（汇总、月均） |
| F-R | HR 费用月度明细（1-12 月） |
| S-T | 试产/打样费用（汇总、月均） |
| U-AG | 试产/打样费用月度明细 |
| ... | 其他费用类别同理 |
| 最后两列 | 总计（汇总、月度合计） |

### 样式特点（必须严格遵守）

- **表头**：深蓝色背景 (#2E74B5) + 白色文字，微软雅黑字体
- **子标题**：浅蓝色背景 (#D6EAF8) + 深色文字
- **数据行**：交替使用白色/浅灰色背景 (#F8F9FA)，便于阅读
- **总计列**：黄色高亮 (#FFEB9C) + 粗体，突出显示
- **月度合计**：绿色高亮 (#C6EFCE) + 粗体
- **数字格式**：`#,##0.00`（千分符 + 两位小数），所有数值统一
- **对齐方式**：文本左对齐，数字右对齐
- **列宽**：基本信息列加宽（14-20），月度列统一（10），总计列加宽（14）
- **边框**：细边框 + 浅灰色 (#CCCCCC)

## 月均计算逻辑

- **2025 年**：年度汇总 ÷ 12
- **2026 年**：年度汇总 ÷ 2（因为只有 1-2 月数据）

脚本会自动统计实际有数据的月份数，并按以下规则计算：
```python
max_months = 2 if year == 2026 else 12
divisor = min(actual_months_count, max_months)
monthly_avg = monthly_sum / divisor
```

## 注意事项

1. **表头位置**：确保源文件的表头在第 4 行（索引 3），否则需要调整 `header` 参数
2. **客户分类**：只处理"帝国"、"BAT"、"MT"、"ITMS"四类，其他会被忽略
3. **数据完整性**：如果某些月份数据缺失，月均计算会自动调整除数
4. **输出位置**：默认保存到源文件所在目录，可通过 `output_dir` 参数指定

## 故障排除

### 问题：读取数据为空

**原因**：表头位置不正确

**解决**：检查源文件的表头位置，修改脚本中的 `header` 参数：
```python
df = pd.read_excel(source_file, sheet_name='Sheet1', header=3)  # 调整为正确的行号
```

### 问题：费用数据为 0

**原因**：列名格式不匹配

**解决**：检查源文件的列名格式，确保包含"年"、"月"等关键字，如`25 年 1 月人工费用`

### 问题：客户分类缺失

**原因**：客户大类列的值与预期不符

**解决**：检查"客户大类"列的实际值，必要时在脚本的 `valid_customers` 列表中添加新的客户类型

## 相关文件

- **脚本**：`scripts/generate_cost_report.py` - 核心生成脚本

## 分享与发布

### 本地使用（当前用户）

技能已安装在 `~/.openclaw/workspace/skills/cost-report-generator/`，当前 OpenClaw 会话可直接使用。

### 分享给其他飞书用户

**方式 1：通过 ClawHub 发布（推荐）**

```bash
# 1. 登录 ClawHub
clawhub login

# 2. 发布技能
clawhub publish ~/.openclaw/workspace/skills/cost-report-generator \
  --slug cost-report-generator \
  --name "成本分析报告生成器" \
  --version 1.0.0 \
  --changelog "初始版本：支持 EVP 项目费用文件自动生成成本分析报告"
```

其他用户安装：
```bash
clawhub install cost-report-generator
```

**方式 2：直接共享技能文件夹**

将 `~/.openclaw/workspace/skills/cost-report-generator/` 打包发送给其他用户，让他们放到自己的 `~/.openclaw/workspace/skills/` 目录下。

**方式 3：通过 OpenClaw 团队空间**

如果多个用户共享同一个 OpenClaw workspace，技能会自动对所有用户可见。

### 技能元数据（发布用）

```yaml
name: cost-report-generator
version: 1.0.0
description: 从项目费用 Excel 自动生成按客户分类的成本分析报告
author: Richard 张
tags: [成本分析，财务报告，Excel, 飞书]
```
