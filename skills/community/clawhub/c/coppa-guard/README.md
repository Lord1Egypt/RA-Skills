# 🛡️ COPPA 美国儿童隐私护栏 (coppa-guard) v1.0.0

面向**出海美国、触及儿童用户**的产品（儿童 App / 游戏 / 电商 / 教育产品）的
**事前合规护栏**。在文案、隐私政策、应用商店描述**发布前**，实时检测触发 COPPA
适用的表述与儿童隐私违规用语，按风险分级输出命中与整改建议。

## 为什么需要

COPPA（Children's Online Privacy Protection Act）由美国 FTC 执法：任何面向 13 岁以下
儿童、或明知收集 13 岁以下儿童个人信息的运营者，必须先取得"可验证家长同意"
(Verifiable Parental Consent, VPC)，并提供家长审查/撤回/删除通道、最小化收集。
违规可由 FTC 处以巨额罚款。本护栏帮你在发布前拦住高频红线。

## 快速开始

```bash
python3 scripts/guard.py --text "Our kids app collects children's data without parental consent"
echo "preschool game for toddlers" | python3 scripts/guard.py --stdin
python3 scripts/guard.py --text "..." --format json
python3 scripts/guard.py --list-categories
```

## 检测范围（6 类）

| 类别 | 风险 |
|------|------|
| 面向儿童(触发适用) | medium |
| 收集儿童个人信息 | high |
| 儿童行为定向广告 | high |
| 缺少可验证家长同意 | high |
| 第三方披露儿童数据 | medium |
| 儿童持久标识符追踪 | medium |

## 特性

- 纯本地、零网络、零动态执行（仅 Python 标准库）
- 风险分级 + 逐条整改建议 + 结构化 JSON
- 内核与规则分离，追加词即可扩展

## 法律声明

本工具仅作辅助检测，**不构成法律建议**。重大合规决策请咨询具备美国法执业资格的法律顾问。
详见 `SKILL.md` 的「法律声明」与「Skill 自身合规声明」章节。
