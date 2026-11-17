---
name: gdpr-export-compliance
slug: gdpr-export-compliance
display_name: GDPR出海合规实操
displayName: GDPR出海合规实操
title: GDPR出海合规实操
version: 1.0.0
category: 通用技能
platforms:
  - windows
  - macos
  - linux
  - web
author: 注册老炮
license: MIT
description: GDPR 出海合规实操手册——面向中国企业出海欧洲，覆盖 GDPR 适用范围与域外管辖判定、六项合法处理基础与健康数据特殊类别（明确同意等）、数据主体权利响应（访问/删除/可携/反对及时限）、DPIA 数据保护影响评估、跨境传输机制（充分性认定/SCC 标准合同条款/BCR 约束性公司规则/例外情形）、违规罚款与数据泄露通报（72 小时/两档罚款上限 2000 万欧或 4%）、GDPR 与中国个保法对照与落地清单，附零依赖本地工具一键判定适用范围、推荐合法基础、速查权利与罚款。面向出海企业法务、合规与数据负责人，与医械数据出海合规互补。
description_en: A practical GDPR compliance playbook for Chinese companies expanding into Europe — covering scope and extraterritorial application, six lawful bases and special-category health data (explicit consent), data subject rights responses (access/erasure/portability/objection with timelines), DPIA, cross-border transfer mechanisms (adequacy decisions/SCCs/BCRs/exceptions), fines and 72-hour breach notification (up to EUR 20M or 4%), a GDPR vs China PIPL comparison and implementation checklists. Includes a zero-dependency local toolkit for scope determination, lawful-basis recommendation and rights/penalty quick-reference. Built for legal, compliance and data leaders of export-oriented companies — complementary to medical device data export compliance.
tags:
  - GDPR
  - 数据合规
  - 出海合规
  - 欧洲数据保护
  - 跨境传输
  - SCC
  - DPIA
  - 个人信息保护
  - 数据泄露
  - Data Protection
  - EU Compliance
---

# GDPR 出海合规实操

GDPR 出海合规工作台：**判得准适不适用、选得对合法基础、答得全数据权利、传得了跨境数据、躲得开巨额罚款**。面向出海企业法务、合规与数据负责人——服务欧洲用户/客户，GDPR 就是合规底线。

## 什么时候用这个技能

- **适用判定**：「我们在中国，服务欧洲客户，受 GDPR 管吗？」
- **合法基础**：「处理欧洲用户数据用什么合法基础？同意怎么拿？」
- **数据权利**：「用户要求删除数据，多久响应？」
- **跨境传输**：「数据传到中国，用什么机制？SCC 怎么签？」
- **泄露应对**：「数据泄露了，72 小时通报怎么做？」
- **健康数据**：「处理健康数据（医疗器械场景）有什么特殊要求？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

> 「我们 App 服务欧洲用户，受 GDPR 管辖吗？」
> 「营销邮件用什么合法基础？」
> 「用户要删除数据，流程是什么？」

### 模式二：本地工具（要结构化结果）

```bash
# ① 适用范围判定：输入业务描述
python tools/gdpr_toolkit.py scope --desc "中国公司运营App，向欧洲用户提供在线服务并收集其个人数据"

# ② 合法基础推荐：输入处理场景
python tools/gdpr_toolkit.py legal --desc "向欧洲用户发送营销邮件"

# ③ 数据主体权利速查
python tools/gdpr_toolkit.py rights --right access    # access/erasure/portability/object

# ④ 跨境传输机制判定
python tools/gdpr_toolkit.py transfer --desc "将欧洲用户数据传输到中国总部处理"

# ⑤ 罚款与通报速查
python tools/gdpr_toolkit.py penalty

# 查看全部命令
python tools/gdpr_toolkit.py --help
```

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 全景与适用范围 | `references/01-GDPR全景与适用范围.md` | 原则、域外管辖、角色 |
| ② 合法基础 | `references/02-合法处理基础.md` | 六项合法基础、同意、特殊类别 |
| ③ 数据主体权利 | `references/03-数据主体权利.md` | 访问/删除/可携/反对及响应时限 |
| ④ DPIA 评估 | `references/04-DPIA评估.md` | 何时做、怎么做、报告结构 |
| ⑤ 跨境传输 | `references/05-跨境传输机制.md` | 充分性/SCC/BCR/例外 |
| ⑥ 违规与通报 | `references/06-违规罚款与泄露通报.md` | 两档罚款、72 小时通报 |
| ⑦ 与个保法对照 | `references/07-GDPR与个保法对照.md` | 中欧对照、落地清单 |
| ⑧ FAQ | `references/08-FAQ.md` | 高频疑问 |

## 快速上手（三步）

1. **判适用**：`scope` 命令输入业务描述，对照 01 模块；
2. **定基础**：`legal` 命令推荐合法基础，02 模块看细节；
3. **落机制**：`transfer` 判跨境机制，05 模块签协议；`penalty` 看红线。

## 能力边界（如实说明）

- **本技能是方法库与工具，不是法律意见**：GDPR 适用与合规判断受个案影响，重大决策请咨询执业律师/DPO；
- **法规持续演进**：EDPB 指南、欧盟判例（如 Meta 案等）持续更新，引用前复核最新状态；
- **工具不联网**：本地规则匹配，不采集数据、不调用外部服务。

## 常见问题（FAQ）

- **Q：中国公司一定受 GDPR 管吗？** 取决于是否向欧盟境内主体提供商品/服务或监控其行为（域外管辖），见 01 模块判定。
- **Q：罚款真的那么高吗？** 两档：最高 2000 万欧元或全球年营业额 4%（取高者）——EDPB 罚款指引给出计算框架。
- **Q：和个保法冲突怎么办？** 两边要求都满足（按更严执行），见 07 模块对照表。
- **Q：工具脚本要装依赖吗？** 不需要，仅 Python 标准库。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的 GDPR 合规方法论、对照整理、流程与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与监管准确性保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。
