# 知网产品目录与选型规则

## 2026-10-02 实时快照

来源：GET https://cnki.cqccjy.cn/api/paper/cnki/public/config?channel=pcnki。当前 enabled=true，pricingMode 均为 PER_ARTICLE，unit=篇，paymentChannels 返回检测卡号、微信、支付宝。

| 完整商品名 | 编码 | 快照价格 | 文件 | 提示范围 | 本地外部 ID |
|---|---|---:|---|---:|---|
| 知网本科/专科检测 | CNKI_UNDERGRADUATE | ￥18.00/篇 | doc/docx/txt/pdf | 200–80,000 | dxscnki |
| 知网硕博检测 | CNKI_GRADUATE | ￥55.00/篇 | doc/docx/txt/pdf | 200–300,000 | yjscnki |
| 知网AIGC检测 | CNKI_AIGC | ￥38.00/篇 | doc/docx/txt/pdf | 200–80,000 | cnkiaigc |
| 知网期刊检测 | CNKI_JOURNAL | ￥35.00/篇 | doc/docx/txt/pdf | 200–30,000 | 以实时映射为准 |
| 知网AIGC检测（8万字及以上） | CNKI_AIGC_OVER_80000 | ￥65.00/篇 | doc/docx/pdf | 80,000–300,000 | 以实时映射为准 |

说明：实时公共接口在 2026-10-02 返回大 AIGC 展示名为“8万字及以上”，但本地枚举和迁移目标文案是“8万字符及以上”，前端也会按 productCode 做显示规范化。稳定判断只能用 productCode 和实时限制。

## 选型决策

1. 本科、专科、大学生毕业论文：CNKI_UNDERGRADUATE。
2. 硕士、博士、研究生学位论文：CNKI_GRADUATE。
3. 期刊投稿、编辑部送审前：CNKI_JOURNAL。
4. 只查 AI 生成风险：CNKI_AIGC 或 CNKI_AIGC_OVER_80000，按实时字符提示范围。
5. 学校指定 PMLC/TMLC/AMLC/SMLC 或机构专用入口：先确认书面要求，不自动映射公共产品。

## 常见别名

| 用户说法 | 映射 |
|---|---|
| 知网本科、本科版、专科版、大学生版 | CNKI_UNDERGRADUATE |
| 知网硕士、博士、研究生版、硕博版 | CNKI_GRADUATE |
| 知网期刊、投稿版、编辑部预检 | CNKI_JOURNAL |
| 知网 AIGC、知网 AI 率、AI 检测 | 先确认字符范围，再选 AIGC 编码 |

## 价格与字符边界

- 价格是每篇，不是按每 1000 字或每个字阶梯计价；正式金额以订单页 payAmount 为准。
- hintMinCount/hintMaxCount 是页面提示范围，不等于供应商内部所有硬限制。
- 80,000 附近不要只看 Word 字数；以产品实时提示、服务端解析 wordCount 和订单结果为准。
- 同一产品的 fileType、价格、外部 ID、默认比对库和 acceptTimeRequired 都可能由后台配置更新。

## 文件与表单字段

- 题目最多 255 个字符。
- 作者 2–64 个字符，不能为纯符号。
- acceptTimeRequired=true 时提供 YYYY-MM-DD 日期。
- checkDbs 只在页面或实时产品明确提供时传入；不要凭记忆创造比对库名称。
- 服务端 DTO 允许学校/班级字段，但公共 /pzw、/zw 当前不采集，skill 不自行添加。
- 页面建议 20 MB 内，脚本硬上限 50 MiB。

## 重新读取实时目录

    python3 scripts/cnki_client.py products

正式 submit 会自动重新读取实时目录。若产品未启用、enabled=false、价格或格式与用户预期不一致，先停止并让用户确认，不用本地快照强行提交。
