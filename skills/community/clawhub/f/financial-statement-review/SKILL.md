---
name: financial-statement-review
description: 专业财务报表审查 Skill，基于中国《会计法》《企业会计准则》和《税法》体系，对企业财务报表进行全面合规性审查、风险识别和分析。支持可扩展的策略库，包含税款比对分析、收入确认审查、成本操纵识别等多种专业策略。适用于年报审计、税务稽查准备、投资尽调、内部控制等场景。
---

# 财务报表审查专业工具

基于中国会计法、企业会计准则和税法体系，对企业财务报表进行全面审查和风险识别。

## 核心功能

1. **智能文件解析**：自动识别并解析主流财务软件导出的文件及通用格式
2. **报表合规性审查**：检查财务报表是否符合中国会计准则编制要求
3. **税务风险识别**：识别潜在的税务合规风险和纳税调整事项
4. **财务异常检测**：发现数据异常、勾稽关系错误、趋势异常等
5. **策略化审查引擎**：基于可扩展策略库执行专业审查
6. **生成审查报告**：输出专业的审查意见书和工作底稿

## 文件解析模块

本 Skill 内置强大的**文件解析模块**，支持自动识别和解析多种财务文件格式。

### 支持的文件格式

| 格式 | 扩展名 | 解析器 | 说明 |
|-----|--------|--------|------|
| **Excel** | .xlsx, .xls, .xlsm | excel_parser | 主流表格格式，支持多工作表 |
| **Word** | .docx | word_parser | Word文档中的表格数据 |
| **PDF** | .pdf | pdf_parser | PDF财务报告，支持表格提取 |
| **CSV** | .csv | csv_parser | 逗号分隔值文件 |

### 支持的财务软件

| 软件 | 支持版本 | 标识方式 | 解析器 |
|-----|---------|---------|--------|
| **金蝶** | KIS/K3/EAS/云星空/云星辰 | 文件名含"金蝶"/"Kingdee" | kingdee_parser |
| **用友** | U8/NC/YonSuite/畅捷通 | 文件名含"用友"/"UFIDA" | ufida_parser |
| **通用** | - | 标准格式文件 | excel_parser 等 |

### 文件解析示例

```python
from parsers import parse_file, FileParserManager

# 方式1：简单解析
result = parse_file('/path/to/金蝶_资产负债表.xlsx')

if result.success:
    data = result.data
    print(f"公司: {data.company_name}")
    print(f"营业收入: {data.income_statement.get('营业收入'):,.2f}")
    print(f"资产总计: {data.balance_sheet.get('资产总计'):,.2f}")
else:
    print(f"解析失败: {result.errors}")

# 方式2：批量解析
manager = FileParserManager()
files = ['report1.xlsx', 'report2.pdf', 'report3.csv']
results = manager.parse_files(files)

# 方式3：扫描目录
results = manager.scan_and_parse('/data/financial_reports', recursive=True)

# 合并多个文件的数据
merged_data = manager.merge_financial_data(results)
```

### 自动文件识别

系统会自动识别文件类型和财务软件来源：

```python
from parsers.file_identifier import identify_file

file_type, software_type = identify_file('金蝶_报表.xlsx')
print(f"文件类型: {file_type.name}")      # EXCEL
print(f"软件类型: {software_type.name}")  # KINGDEE
```

### 解析结果结构

解析成功后返回标准化的财务数据结构：

```python
{
    'company_name': '公司名称',
    'tax_id': '纳税人识别号',
    'report_period': '2024年度',
    'balance_sheet': {
        '货币资金': 50000000,
        '应收账款': 30000000,
        '资产总计': 200000000,
        '负债合计': 100000000,
        # ... 其他科目
    },
    'income_statement': {
        '营业收入': 150000000,
        '营业成本': 100000000,
        '净利润': 22500000,
        # ... 其他科目
    },
    'cash_flow': {
        '经营活动现金流': 25000000,
        # ... 其他项目
    },
    'source_file': '原始文件名',
    'source_software': '金蝶/用友等'
}
```

## 策略库系统

本 Skill 采用**策略化设计**，每个策略封装特定的审查逻辑，可按需组合使用。

### 内置策略列表

| 策略名称 | 策略ID | 功能描述 | 适用税种 |
|---------|--------|---------|---------|
| **税款比对分析** | `tax_reconciliation` | 比对已纳税款统计表与财务报表，识别少缴税款疑点 | 增值税、企业所得税 |
| **收入确认审查** | `revenue_recognition` | 基于 CAS 14 审查收入确认合规性，识别提前/虚构收入 | 增值税、企业所得税 |
| **成本操纵识别** | `cost_manipulation` | 识别通过成本费用调节利润的行为 | 企业所得税 |
| **税收优惠审查** | `tax_preference` | 审查税收优惠政策适用条件和计算准确性，关注政策时效性 | 企业所得税 |
| **关联交易审查** | `related_party` | 审查关联方交易税务合规性，防范资本弱化和转让定价风险 | 企业所得税、增值税 |

### 策略库架构

```
strategies/
├── __init__.py                   # 策略库入口
├── base_strategy.py              # 策略基类（所有策略需继承）
├── strategy_manager.py           # 策略管理器
├── STRATEGY_GUIDE.md             # 策略开发指南
├── tax_reconciliation.py         # 税款比对策略 [内置]
├── revenue_recognition.py        # 收入确认策略 [内置]
├── cost_manipulation.py          # 成本操纵策略 [内置]
├── tax_preference.py             # 税收优惠审查策略 [内置]
└── related_party.py              # 关联交易审查策略 [内置]

parsers/                            # ⭐ 新增：文件解析模块
├── __init__.py
├── base_parser.py                  # 解析器基类
├── parser_manager.py               # 解析器管理器
├── file_identifier.py              # 文件识别器
├── excel_parser.py                 # Excel解析器
├── csv_parser.py                   # CSV解析器
├── word_parser.py                  # Word解析器
├── pdf_parser.py                   # PDF解析器
├── kingdee_parser.py               # 金蝶专用解析器
└── ufida_parser.py                 # 用友专用解析器
```

### 使用策略库

```python
from strategies import StrategyManager

# 初始化管理器
manager = StrategyManager()

# 加载所有策略
manager.load_all_strategies()

# 查看可用策略
for info in manager.list_strategies():
    print(f"{info['name']}: {info['description']}")

# 准备审查数据
data = {
    'financial_statements': {
        'revenue': 10000000,
        'profit': 2000000,
        # ... 其他财务数据
    },
    'tax_returns': {
        'vat_revenue': 9500000,  # 增值税申报收入
        'vat_paid': 1235000,     # 已缴增值税
        'cit_taxable_income': 1800000,  # 应纳税所得额
        'cit_paid': 450000,      # 已缴企业所得税
    },
    'company_info': {
        'is_small_profit': False,  # 是否小型微利企业
    }
}

# 执行特定策略
result = manager.execute_strategy('tax_reconciliation', data)

# 或执行所有策略
all_results = manager.execute_all(data)

# 生成汇总报告
summary = manager.generate_summary_report(all_results)
print(summary)
```

### 添加自定义策略

开发者可通过继承 `BaseStrategy` 基类轻松添加新策略：

```python
from strategies import BaseStrategy, StrategyResult

class MyCustomStrategy(BaseStrategy):
    name = "my_custom_strategy"
    description = "我的自定义审查策略"
    applicable_tax_types = ["增值税"]
    required_data_fields = ["financial_statements"]
    
    def execute(self, data):
        result = StrategyResult(
            strategy_name=self.name,
            strategy_description=self.description,
            status='passed'
        )
        
        # 实现审查逻辑
        fs = data.get('financial_statements', {})
        # ... 分析代码
        
        # 发现问题时添加
        result.add_finding(
            finding_type='发现问题类型',
            description='问题描述',
            severity='high',  # high/medium/low
            tax_type='增值税',
            regulation='法规依据'
        )
        
        return result
```

将策略文件保存到 `strategies/` 目录，管理器会自动加载。

### 税款比对策略详解

**策略ID**: `tax_reconciliation`

**功能**：通过比对财务报表与纳税申报数据，自动识别少缴税款疑点

**比对维度**：
1. **收入比对**：财务收入 vs 增值税/所得税申报收入
2. **税负率分析**：实际税负率 vs 行业参考值
3. **限额扣除检查**：福利费、招待费、广宣费等超标识别
4. **理论税额测算**：基于财务数据测算理论应纳税额

**输出结果**：
- 风险发现（高/中/低风险分级）
- 预估少缴税款金额
- 法规依据引用
- 整改建议

**示例输出**：
```
[高风险] 增值税申报收入偏低
  描述：财务报表收入(10,000,000)高于增值税申报收入(9,500,000)，差异5.0%
  预估少缴税款：65,000元
  法规依据：增值税暂行条例第十九条
  建议：核实差异原因，如为未开票收入应及时申报

[中风险] 业务招待费超标
  描述：业务招待费600,000元，扣除限额360,000元，超标240,000元
  所得税影响：60,000元
  法规依据：企业所得税法实施条例第四十三条
```

### 税收优惠审查策略详解

**策略ID**: `tax_preference`

**功能**：审查企业享受的税收优惠政策是否符合条件，关注政策时效性和业务实质

**审查维度**：
1. **小型微利企业优惠**：应纳税所得额≤300万、从业人数≤300人、资产总额≤5000万
2. **高新技术企业**：研发费用占比、高新技术产品收入占比、科技人员占比、证书有效性
3. **研发费用加计扣除**：负面清单行业限制、研发费用归集准确性、委托研发比例
4. **固定资产加速折旧/一次性扣除**：500万以下设备器具、资产类型合规性
5. **区域性优惠**：西部大开发（鼓励类产业、收入占比60%）、海南自贸港
6. **政策时效性**：检查优惠政策是否已过期或即将到期

**特别关注**：
- 政策有效期提醒（如小型微利优惠延续至2027年底）
- 业务实质是否符合优惠条件
- 优惠计算准确性

**示例输出**：
```
🔴 [HIGH] 小型微利企业条件不符
  应纳税所得额3,500,000元超过300万元限额
  不应享受小型微利优惠税率，应按25%补缴税款
  法规依据：财税〔2023〕12号

🟡 [MEDIUM] 高新资质证书过期
  高新技术企业证书已于2025-12-31过期
  过期后不应继续享受15%优惠税率
  建议：及时办理重新认定，或按25%税率补缴税款

🟡 [MEDIUM] 研发费用占比不足
  研发费用占比2.5%，低于要求3%（收入2亿元以上）
  可能影响高新资质维持
  法规依据：国科发火〔2016〕32号第十一条
```

### 关联交易审查策略详解

**策略ID**: `related_party`

**功能**：审查关联方交易的税务合规性，防范资本弱化、转让定价和隐性利润分配风险

**审查维度**：
1. **资本弱化审查**：债资比2:1（一般企业）或5:1（金融企业），超标利息不得扣除
2. **关联方利息审查**：利率合理性（基准利率区间）、非金融企业借款凭证合规性
3. **关联方资金占用**：长期占用未收利息、大额资金往来异常
4. **转让定价审查**：关联方销售/采购毛利率差异、定价公允性
5. **关联方担保**：未收担保费、担保实际履行损失
6. **向关联方发放福利**：视同销售处理
7. **同期资料义务**：本地文档（关联交易2亿+）、主体文档（营收55亿+）

**特别关注**：
- 通过利息变相逃避税费（过高/过低利率）
- 股东出资不到位情况下借款利息限制
- 关联方资金回流虚增收入
- 隐性利润分配

**示例输出**：
```
🔴 [HIGH] 资本弱化-债资比超标
  关联方债资比3.5:1超过标准2:1
  关联方债务7000万元，所有者权益2000万元
  不得扣除利息支出约428,571元，补缴所得税107,143元
  法规依据：财税〔2008〕121号

🔴 [HIGH] 关联方借款利率过高
  向母公司借款利率18%超过合理区间上限15%
  超额利息300,000元不得税前扣除
  法规依据：企业所得税法第四十六条

🟡 [MEDIUM] 关联方资金占用未收利息
  关联方长期占用资金5000万元（18个月）未收取利息
  按市场利率5%估算应收利息375万元，可能涉及隐性利润分配
  法规依据：企业所得税法第四十一条

🔴 [HIGH] 关联交易定价偏低
  关联方销售毛利率15%显著低于非关联方35%
  差异20个百分点，潜在利润转移2000万元
  建议：准备同期资料或进行特别纳税调整
```

## 使用方法

### 方式一：上传文件自动审查

上传财务报表文件，Skill 将自动识别文件格式、提取数据并进行多维度审查：

```
用户：[上传 金蝶_资产负债表_2024.xlsx]

Skill：
  ✓ 识别文件格式：金蝶 Excel 格式
  ✓ 解析财务数据：
    - 资产负债表：50个科目
    - 利润表：30个科目
  ✓ 执行审查策略：
    - 税款比对分析 ✓
    - 收入确认审查 ✓
    - 关联交易审查 ✓
  ⚠ 发现 3 个高风险问题：
    1. 增值税申报收入差异
    2. 关联方债资比超标
    3. 高新资质证书过期
  📄 生成审查报告：report_20240330.md
```

**完整代码示例：**

```python
from parsers import parse_file
from strategies import StrategyManager

# 第1步：解析财务文件
file_path = '金蝶_财务报表.xlsx'
parse_result = parse_file(file_path)

if not parse_result.success:
    print(f"文件解析失败: {parse_result.errors}")
    exit()

# 第2步：提取财务数据
data = parse_result.data
review_data = {
    'financial_statements': {
        'revenue': data.income_statement.get('营业收入', 0),
        'profit': data.income_statement.get('利润总额', 0),
        'total_assets': data.balance_sheet.get('资产总计', 0),
        'owners_equity': data.balance_sheet.get('所有者权益合计', 0),
        # ... 其他字段
    },
    'company_info': {
        'name': data.company_name,
        'tax_id': data.tax_id,
    }
}

# 第3步：执行审查策略
manager = StrategyManager()
manager.load_all_strategies()
results = manager.execute_all(review_data)

# 第4步：生成报告
summary = manager.generate_summary_report(results)
print(summary)
```

### 方式二：查询特定审查要点

针对特定会计科目或业务场景获取审查指引：

```
用户：收入确认的审查要点是什么？

Skill：[输出收入确认的审查要点、常见风险、法规依据]
```

## 支持的报表类型

### 主要财务报表
- **资产负债表**：资产、负债、所有者权益的合规性和准确性审查
- **利润表**：收入、成本、费用的确认和计量审查
- **现金流量表**：经营活动、投资活动、筹资活动现金流审查
- **所有者权益变动表**：权益变动的合规性审查

### 附注和补充资料
- 会计政策披露审查
- 重要事项披露审查
- 关联交易披露审查
- 或有事项审查

## 审查维度

### 1. 合规性审查
- **准则遵循**：是否符合《企业会计准则》要求
- **格式规范**：报表格式是否符合财政部规定
- **披露完整**：附注披露是否充分、准确
- **会计政策**：会计政策选择和变更是否合理

### 2. 税务审查
- **收入确认**：增值税、企业所得税纳税义务发生时点
- **成本费用**：税前扣除凭证合规性、限额扣除项目
- **税收优惠**：优惠政策适用条件和备案要求
- **关联交易**：转让定价和同期资料准备
- **发票管理**：进项抵扣、销项开具合规性

### 3. 财务分析
- **趋势分析**：同比、环比变动异常识别
- **结构分析**：资产负债结构、收入成本结构合理性
- **比率分析**：偿债能力、盈利能力、营运能力指标
- **勾稽关系**：报表间数据一致性验证

### 4. 风险识别
- **重大错报风险**：可能导致报表重大错报的因素
- **舞弊风险**：收入舞弊、费用舞弊、资产侵占等迹象
- **持续经营风险**：流动性危机、资不抵债等风险信号
- **税务稽查风险**：高风险税务事项和稽查重点领域

## 法规依据

### 会计法规
- 《中华人民共和国会计法》
- 《企业会计准则——基本准则》
- 42项具体企业会计准则
- 《企业会计准则解释》

### 税收法规
- 《中华人民共和国企业所得税法》及实施条例
- 《中华人民共和国增值税暂行条例》及实施细则
- 《中华人民共和国个人所得税法》及实施条例
- 其他相关税收法规

### 监管规定
- 中国证监会信息披露要求
- 财政部会计监管风险提示
- 税务机关稽查重点关注领域

## 输出成果

### 1. 财务报表审查意见书
包含以下内容：
- 审查范围和依据
- 总体评价和意见类型
- 具体问题清单（按重要性分级）
- 调整分录建议
- 管理建议书

### 2. 税务风险提示报告
- 识别的税务风险点清单
- 风险等级评估（高/中/低）
- 法规依据和潜在后果
- 整改建议和时间表

### 3. 财务分析简报
- 关键财务指标分析
- 同比环比变动分析
- 行业对比（如有数据）
- 趋势预测和风险预警

## 审查深度配置

### 快速审查（30分钟）
- 报表格式合规性检查
- 主要科目异常变动识别
- 重大税务风险点识别
- 执行策略：税款比对（基础模式）
- 适用于：初步筛查、内部汇报

### 标准审查（2-4小时）
- 全科目余额变动分析
- 会计政策适用性审查
- 主要税种风险识别
- 报表间勾稽关系验证
- 执行策略：税款比对 + 收入确认审查
- 适用于：年报审计、税务自查

### 深度审查（1-3天）
- 详细凭证抽查
- 完整税务合规审查
- 内部控制评价
- 舞弊风险专项分析
- 执行策略：全部策略组合
- 适用于：投资尽调、IPO审计、税务稽查应对

### 策略配置示例

```python
# 快速审查配置
quick_review_config = {
    'tax_reconciliation': {
        'enabled': True,
        'priority': 10,
        'vat_rate': 0.13,
    }
}

# 深度审查配置
deep_review_config = {
    'tax_reconciliation': {
        'enabled': True,
        'priority': 10,
        'vat_rate': 0.13,
        'industry_type': 'manufacturing'
    },
    'revenue_recognition': {
        'enabled': True,
        'priority': 20
    },
    'cost_manipulation': {
        'enabled': True,
        'priority': 30
    }
}

# 加载配置
manager.load_all_strategies(config_map=deep_review_config)
```

## 🔧 依赖库

```bash
# 数据处理
pip install pandas>=2.0.0

# 文件解析（根据需要的格式选择性安装）
pip install openpyxl>=3.0.0      # Excel .xlsx 格式
pip install xlrd>=2.0.0          # Excel .xls 格式
pip install python-docx>=0.8.11  # Word .docx 格式
pip install pdfplumber>=0.6.0    # PDF 格式（推荐，支持表格提取）
pip install PyPDF2>=3.0.0        # PDF 格式（备选）

# 其他
pip install jieba>=0.42.1        # 中文分词
```

**依赖安装建议：**
- 基础功能：只需 `pandas`
- Excel解析：必须安装 `openpyxl`（.xlsx）或 `xlrd`（.xls）
- Word解析：必须安装 `python-docx`
- PDF解析：推荐安装 `pdfplumber`（支持表格提取效果最好）

## 数据来源

审查所需数据文件位于：
- `data/accounting_standards.csv` - 会计准则要点
- `data/tax_regulations.csv` - 税法规定汇编
- `data/review_checklists.csv` - 审查检查清单
- `data/risk_indicators.csv` - 风险识别指标

参考资料位于：
- `references/accounting_law.md` - 会计法要点
- `tax_law_summary.md` - 税法摘要
- `review_methodology.md` - 审查方法论

## 重要提示

1. **本 Skill 仅供专业参考**：审查意见基于预设规则和法规库生成，需由持证会计师或税务师复核
2. **法规时效性**：法规依据截至 Skill 版本发布日期，使用前请确认是否有最新修订
3. **专业判断**：风险识别和会计处理建议需结合具体业务实质判断
4. **保密要求**：财务数据涉及商业秘密，请确保在 secure 环境中使用

## 使用场景

### 审计师/会计师
- 年报审计准备工作
- 审计程序设计和执行
- 审计底稿编制辅助

### 企业财务/税务
- 月度/季度财务报表自查
- 税务申报前复核
- 税务稽查应对准备

### 投资人/分析师
- 投资尽调财务分析
- 财务造假识别辅助
- 行业对比分析

### 企业管理者
- 内部控制评价
- 财务风险预警
- 经营决策支持
