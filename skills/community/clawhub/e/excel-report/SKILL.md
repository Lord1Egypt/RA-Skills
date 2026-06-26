# Excel可视化报表生成器 (excel-report)

---

## 简介

一键生成大厂生产级 Excel 可视化报表的 OpenClaw Skill。

**核心功能（v4.0 PRO）：**
- ✅ Excel 公式替代硬编码（数据更新自动刷新）
- ✅ 专业财务配色体系（深蓝表头 + 斑马纹）
- ✅ 专业边框 + 数字格式
- ✅ KPI 仪表盘自动计算
- ✅ 多工作表报表输出
- ✅ 批量生成 + 邮件发送
- ✅ 智能列名映射（中英文）
- ✅ 数据验证

---

## 支持的行业模板

| 行业 | 模板ID | 说明 |
|------|--------|------|
| **制造业** | production_daily | 生产产能日报表 |
| 制造业 | quality_monthly | 生产质量月度报表 |
| **零售业** | store_daily | 门店销售日报表 |
| 零售业 | sales_monthly | 月度销售业绩分析报表 |
| **金融业** | bank_revenue | 银行月度营收报表 |
| 金融业 | securities_asset | 证券客户资产月度报表 |
| **互联网** | app_dau | APP日活与留存报表 |
| 互联网 | ecommerce_order | 电商平台订单月度报表 |
| **医疗** | clinic_monthly | 医院门诊月度报表 |
| 医疗 | equipment_ops | 医疗设备运维报表 |
| **通用** | kpi_monthly | 月度KPI考核报表 |
| 通用 | data_summary | 月度数据汇总报表 |

---

## 安装方法

```bash
# 安装依赖
pip install openpyxl pandas

# 安装 Skill（复制到 skills 目录）
~/.qclaw/skills/excel-report/
```

---

## 使用方法

### 1. 列出模板

```bash
python scripts/generate_report.py --list
```

### 2. 生成报表

```bash
# 基本用法
python scripts/generate_report.py -t <模板ID> -d <数据文件>

# 示例
python scripts/generate_report.py -t store_daily -d sales.xlsx -o report.xlsx
python scripts/generate_report.py -t production_daily -d production.xlsx
```

### 3. 批量生成

```bash
python scripts/generate_report.py --batch --data-dir ./sample_data
```

### 4. 邮件发送

```bash
# 配置环境变量
export SMTP_HOST=smtp.gmail.com
export SMTP_USER=your@email.com
export SMTP_PASSWORD=xxx

python scripts/generate_report.py -t store_daily -d sales.xlsx --email --to user@email.com
```

---

## 专业标准（参考 xlsx skill）

### Excel 公式替代硬编码

**KPI 使用 Excel 公式，数据更新后自动刷新：**

```excel
=SUM('原始数据'!C2:C1000)           -- 总和
=AVG('原始数据'!E2:E1000)           -- 平均
=IFERROR(SUM(D2:D100)/SUM(C2:C100),"-")  -- 比率（含错误保护）
```

### 专业配色体系

| 元素 | 颜色 | 说明 |
|------|------|------|
| 表头背景 | #1F3864 | 深蓝色 |
| 表头文字 | #FFFFFF | 白色粗体 |
| KPI背景 | #DEEAF1 | 浅蓝色 |
| KPI数值 | #1F3864 | 深蓝色大字 |
| 数据奇数行 | #FFFFFF | 白色 |
| 数据偶数行 | #F2F2F2 | 浅灰（斑马纹） |

### 专业边框

| 位置 | 样式 |
|------|------|
| 表头底部 | 双线边框 |
| 数据区域 | 细线边框 |
| KPI卡片 | 粗外框 |

### 数字格式

| 类型 | 格式 | 示例 |
|------|------|------|
| 货币 | `¥#,##0.00` | ¥1,234.56 |
| 百分比 | `0.0%` | 95.5% |
| 整数 | `#,##0` | 1,234 |
| 负数 | `(#,##0)` | (1,234) |

### 功能保障

- **冻结窗格**：数据表冻结首行
- **自动筛选**：数据表开启筛选
- **IFERROR**：所有除法公式加错误保护
- **列宽自适应**：根据内容调整

---

## 数据文件格式

### 支持格式
- **xlsx** - Excel 2007+（推荐）
- **csv** - 自动识别 UTF-8/GBK 编码
- **json** - JSON 数组

### 列名智能映射

无需严格匹配，系统自动识别：
- 日期 / Date / 统计日期
- 销售额 / Sales / 销售金额

---

## 输出报表结构

```
Sheet1: 原始数据
  - 专业表头（深蓝+白色粗体）
  - 斑马纹数据行
  - 冻结首行 + 自动筛选
  - 数字格式（货币/百分比）

Sheet2: 分析看板
  - 大标题
  - KPI 卡片（Excel 公式）
  - 可视化图表

Sheet3: 明细数据
  - 专业样式明细表
```

---

## KPI 公式语法

```javascript
SUM(field)              // 求和
AVG(field)              // 平均值
COUNT(field)            // 计数
SUM(a)/SUM(b)           // 比率（自动加 IFERROR）
COUNT_DISTINCT(field)   // 去重计数
```

---

## 文件结构

```
excel-report/
├── SKILL.md                    # 本文件
├── scripts/
│   └── generate_report.py     # 主入口 (v4.0 PRO)
├── templates/                  # 12个行业模板
│   ├── manufacturing/ (2)
│   ├── retail/ (2)
│   ├── finance/ (2)
│   ├── internet/ (2)
│   ├── medical/ (2)
│   └── general/ (2)
├── styles/
│   └── themes.json            # 配色主题
├── sample_data/               # 示例数据
└── output/                    # 输出目录
```

---

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--list` | 列出所有模板 |
| `-t <ID>` | 指定模板 |
| `-d <file>` | 数据文件 |
| `-o <file>` | 输出路径 |
| `--batch` | 批量生成 |
| `--email --to <addr>` | 发送邮件 |

---

## 更新日志

- **2026-03-31 v4.0 PRO**
  - Excel 公式替代硬编码
  - 专业财务配色体系
  - 斑马纹 + 专业边框
  - 数字格式标准化
  - 冻结窗格 + 自动筛选
  - IFERROR 零错误保障

- **2026-03-31 v3.0**
  - 批量生成模式
  - 邮件发送支持
  - 数据匹配优化

- **2026-03-30 v2.0**
  - 12个行业模板
  - 32个图表
