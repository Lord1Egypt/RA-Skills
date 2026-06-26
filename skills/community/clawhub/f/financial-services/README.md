# Financial Services for OpenClaw

面向金融专业人士的 AI 分析技能集合。覆盖投行、商业银行、资管、保险四大场景，内置源归因机制和标准化输出格式。

## 安装

### 方式一：ClawHub 安装
```bash
clawhub install financial-services
```

### 方式二：手动安装
将整个 `financial-services/` 目录复制到 `~/.openclaw/skills/`：

```bash
cp -r financial-services ~/.openclaw/skills/
```

重启 OpenClaw Gateway 后生效。

## 技能列表

### 核心分析技能
| 技能 | 说明 | 典型场景 |
|------|------|----------|
| `investment-banking` | 投行分析方法论 | Pitch book, CIM, Comps, DCF, 并购估值 |
| `commercial-banking` | 商业银行分析方法论 | Credit memo, 贷款承销, 合约测试, 现金流分析 |
| `asset-management` | 资管分析方法论 | 组合报告, Brinson归因, IC memo, 业绩Deck |
| `insurance` | 保险分析方法论 | 准备金审查, 精算分析, 承保, 监管报告 |

### 基础技能
| 技能 | 说明 |
|------|------|
| `source-attribution` | 每个数字必须追溯到源文档。金融声明验证清单。 |
| `excel-powerpoint-output` | Excel 工作簿和 PowerPoint Deck 的标准化格式规范 |

## 工作流

```
用户请求（如"帮我做pitch book"）
         ↓
investment-banking（投行分析流程）
         ↓
source-attribution（源归因验证）
         ↓
excel-powerpoint-output（标准化输出）
         ↓
交付：Excel 模型 + PowerPoint Deck
```

## 四大场景示例

### 投行：构建估值摘要 Slide
```
用附件CIM和可比公司财务数据，构建Meridian收购的估值摘要。
包含：EV/Revenue和EV/EBITDA中位数和Meridian倍数、
可比公司隐含估值范围、10-12% WACC的DCF、先例交易。
格式化为标准pitch book模板的PowerPoint。
```

### 商业银行：贷款承销分析
```
从借款人资料包中提取Atlas Manufacturing近四年财务数据，
映射到合约条款。包含利润表、资产负债表、关键信用比率、
现金流及同比变化。高亮FY2026E中任何合约违约或接近违约项。
输出为内部信用委员会审查格式的Excel工作簿。
```

### 资管：组合业绩报告
```
用持仓数据和基准收益率生成Pinnacle Growth Equity Fund
Q1 2026业绩摘要。使用Brinson-Fachler行业归因。
包含：主动收益和信息比率、行业贡献（bps）、
风险指标：Sharpe、Beta、最大回撤、主动份额。
格式化为面向机构投资者的PowerPoint slide。
```

### 保险：准备金充足性审查
```
用附件精算工作簿和监管报告审查Sentinel Casualty
一般责任险准备金充足性。显示：总选择终极赔付、
已提准备金vs指示准备金及冗余、2019-2025事故年
平均终极趋势。构建链比率热力图。
格式化为董事会精算委员会的PowerPoint slide。
```

## 数据源集成

本技能集合定义分析方法论。数据接入通过 MCP connectors 配置：

| 数据源 | 用途 |
|--------|------|
| FactSet | 股票价格、财务数据、一致预期 |
| S&P Global / Capital IQ | 财务数据、财报电话会纪要 |
| Morningstar | 估值数据、研究分析 |
| PitchBook | 私募市场数据 |
| Databricks / Snowflake | 企业内部数据平台 |
| Box | 安全文档管理和数据室分析 |
| Daloopa | 公开披露的基础数据和KPI |

配置 MCP server 后，技能会自动利用可用数据源。

## 兼容性

- 平台：OpenClaw
- 格式：SKILL.md（YAML frontmatter + Markdown）
- 无需额外依赖

## 许可

MIT-0

## 致谢

灵感来自 Anthropic 的 [Claude for Financial Services](https://claude.com/solutions/financial-services)。
