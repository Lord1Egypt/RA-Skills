# clin-eval-route-picker

## English

Pick among three clinical evaluation routes (exempt catalog, same-device equivalence, clinical trial) before writing dossiers down the wrong path (zero-dependency, deterministic JSON IR).

This package is zero-dependency (Python stdlib only). See `SKILL.md` for the full bilingual procedure (English-first, Chinese-after) and `scripts/` for the CLI (`--help`).

---

## 中文

# 临床评价路径选择器 / Clinical Evaluation Route Picker

![license](https://img.shields.io/badge/license-MIT-blue) ![python](https://img.shields.io/badge/python-3.8%2B-green) ![deps](https://img.shields.io/badge/deps-zero-orange) ![LGD](https://img.shields.io/badge/LGD--Powered-三律-teal)

> `clin-eval-route-picker` v1.0.0 · Zero-dependency · Deterministic output (JSON IR) · Receipt-style errors

**三条临床评价路径，用确定的判定树选，不用凭感觉赌。**

**EN**: A deterministic decision tree for NMPA/EU clinical evaluation routes.

**关键词 / Keywords**: 临床评价 免临床目录 同品种 临床试验 NMPA 73号通告 MDCG 2020-6 WET 医疗器械注册

## Install & Try / 安装即试
```bash
mkdir -p ~/.claude/skills/clin-eval-route-picker/scripts
curl -fsSL https://raw.githubusercontent.com/zhaoxinghua09-cell/agent-skills/main/skills/clin-eval-route-picker/scripts/clin_eval_route_picker.py -o ~/.claude/skills/clin-eval-route-picker/scripts/clin_eval_route_picker.py
python ~/.claude/skills/clin-eval-route-picker/scripts/clin_eval_route_picker.py --help
```
其他 Agent：`~/.config/opencode/skills/`、`~/.agents/skills/` 等同结构放置；WorkBuddy 对话内直接装。

## Usage / 用法
```bash
# NMPA：III 类、不在免临床目录、无同品种数据
python scripts/clin_eval_route_picker.py --market nmpa --nmpa-class III --in-catalog no --eq-data no

# NMPA：列入免临床目录
python scripts/clin_eval_route_picker.py --market nmpa --nmpa-class II --in-catalog yes

# EU：IIa 类、属成熟技术（WET）
python scripts/clin_eval_route_picker.py --market eu --eu-class IIa --wet yes

# JSON 中间表示
python scripts/clin_eval_route_picker.py --market nmpa --nmpa-class II --in-catalog yes --json
```

## Sample output / 真机输出
```
$ clin_eval_route_picker.py --market nmpa --nmpa-class II --in-catalog yes
推荐路径：免临床评价路径（列入《免于临床评价医疗器械目录》）
  依据：国家药监局 2021 年第 73 号通告
  需提交：与目录条目的对比说明、与同品种器械的对比资料
  提示：对比不符项需另行评价；以官方最新版目录为准
```

## Exit codes & error receipts / 退出码与修复回执
- rc=0 ok / rc=1 findings / rc=2 usage
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| CE_E_MISSING | 缺少必需输入（如 market=nmpa 但未给 --nmpa-class） | 按提示补齐对应市场的分类与条件输入 |
| CE_E_CONFLICT | 输入组合自相矛盾（如 I 类+植入+临床数据） | 核对产品实际分类与证据现状后重新输入 |
| CE_E_VALUE | 布尔类参数取值非法 | 布尔参数仅接受 yes/no |

## FAQ
**工具给的路径能直接当注册策略吗？**

不能。输出是基于现行规则文本的确定性推荐，供立项讨论与资料准备导航；注册策略需结合产品具体属性并由注册人员/法规顾问确认。

**为什么答案总带'以官方最新为准'？**

目录、通告与指南会更新，工具按发布时规则编写；本措辞是 YMYL 内容纪律，不是免责套话。


## Links / 快链
- 仓库: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/clin-eval-route-picker
- 家族门户: https://zhaoxinghua09-cell.github.io/lgd-hub/
- Issues: https://github.com/zhaoxinghua09-cell/agent-skills/issues

## Disclaimer / 免责
clin-eval-route-picker 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

License MIT © clin-eval-route-picker authors. LGD-Powered badge: [定版真源](https://synomos.ai)

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI contributors · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
