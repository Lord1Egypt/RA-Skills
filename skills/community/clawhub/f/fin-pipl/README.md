# 🏦 Fin-PIPL — 金融行业个人信息保护合规检查工具

金融行业专属的 **个人信息保护法（PIPL）合规检查工具**，覆盖银行、证券/基金、保险、支付四大业务场景。

## 功能特色

- **20+ 金融场景专属检查项**：按业务类型定制，不套用通用检查
- **四大业务覆盖**：银行（开户/信贷/征信/营销）、证券（适当性/交易/智能投顾）、保险（核保/理赔/再保险）、支付（最小必要/风控/标记化）
- **交互式问答**：一问一答引导完成自查
- **多格式报告**：Markdown / JSON / HTML
- **纯本地运行**：数据不离开用户环境

## 快速使用

```bash
# 交互式检查（推荐）
python3 scripts/fin-pipl-check.py --interactive

# 指定场景
python3 scripts/fin-pipl-check.py --scenario banking
python3 scripts/fin-pipl-check.py --scenario securities
python3 scripts/fin-pipl-check.py --scenario insurance
python3 scripts/fin-pipl-check.py --scenario payment

# 输出报告
python3 scripts/fin-pipl-check.py -s banking -o report.md
python3 scripts/fin-pipl-check.py -s banking -o report.json -f json
python3 scripts/fin-pipl-check.py -s banking -o report.html -f html

# 查看版本
python3 scripts/fin-pipl-check.py --version
```

## 参考法规

- 《个人信息保护法》（PIPL）
- JR/T 0171-2020《个人金融信息保护技术规范》
- JR/T 0197-2020《金融数据安全 数据安全分级指南》
- 《征信业管理条例》
- 《金融消费者权益保护实施办法》（人民银行令〔2020〕第5号）
- 《证券期货投资者适当性管理办法》
- 《互联网信息服务算法推荐管理规定》

## 免责声明

本工具提供的合规检查结果仅供参考，不构成法律意见。金融行业合规涉及多重监管要求，请咨询专业法律顾问确认合规状态。

## 许可证

MIT © 2026 Wei Wu (wwumit)

[GitHub](https://github.com/wwumit/fin-pipl)
