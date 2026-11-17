# business-analytics

面向多业务类型、多渠道数据的经营分析 Skill。它会先识别业务模式与数据口径，再选择指标、图表、页面结构和视觉风格，最终生成可离线打开的品牌化交互 HTML。

## 适用场景

- 餐饮、咖啡、零售和电商
- 场馆、课程、预约和会员服务
- SaaS、订阅、B2B 与项目型业务
- 美团、有赞、小程序、POS、外卖平台及多系统数据
- Excel、CSV、SQLite 等经营数据源

## 核心能力

- 根据业务类型改变分析模块、指标语言、图表组合和视觉风格
- 统一实付、退款、商家优惠、平台补贴、佣金、配送费与结算口径
- 在有效身份范围内分析新老客、频次、复购与次月留存
- 支持单月和多月选择、环比、同比与变化原因拆解
- 根据 Logo 或品牌参考图提取候选主题色
- 生成可直接通过 `file://` 打开的自包含 HTML

## 安装

将仓库复制到 Codex skills 目录：

```bash
git clone https://github.com/aijindouhua/business-analytics.git ~/.codex/skills/business-analytics
```

安装后重新载入 Codex 技能列表，即可通过 `business-analytics` 调用。

## 目录

```text
business-analytics/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── dashboard-ui.md
│   ├── input-and-channel-mapping.md
│   ├── metrics-and-periods.md
│   ├── quality-checklist.md
│   ├── routing-and-modes.md
│   └── theme-and-brand.md
└── scripts/extract_theme.py
```

## 品牌取色

```bash
python3 scripts/extract_theme.py /absolute/path/to/logo.png
```

脚本依赖 Pillow。输出的颜色是界面主题候选值，最终仍会依据文字对比度、图表辨识度和业务风格进行调整。

## 数据原则

- 不把不同平台的匿名顾客自动合并为同一人。
- 不用成交额替代结算收入，也不忽略退款、费用或补贴承担方。
- 缺少有效字段时说明分析范围，不虚构留存、毛利或转化率。
- 页面结论随筛选周期、渠道和门店动态更新。

