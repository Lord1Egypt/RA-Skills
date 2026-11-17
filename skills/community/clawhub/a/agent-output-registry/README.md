# AI 产出有籍登记器（LGD-I 有籍）· agent-output-registry

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> LGD-I 有籍 · 凡造必登。给每条 AI 产出发一张「籍」（户口），可溯源、可证完整性、可查归属。

## 用法

```bash
# 登记（--out 传文件路径或文本）
python scripts/output_registry.py add --out 报告.txt --model qwen3.5 --version 9b \
  --prompt "写合规总结" --issuer SynomosAI --license MIT
# → 返回籍号 LGD-REG-xxxxxxxx

python scripts/output_registry.py verify --id LGD-REG-xxxxxxxx --out 报告.txt   # 证完整性
python scripts/output_registry.py lookup --id LGD-REG-xxxxxxxx                  # 查归属
python scripts/output_registry.py report                                        # 列全部
```

台账落 `registry/`（md + csv + jsonl），纯离线零依赖。

## 解决痛点

AI 产出说不清来源、被改了认不出、权属扯不清 → 指纹 + 模型/版本/提示哈希 + 权属人 = 可举证户口。

© SynomosAI · MIT · LGD-Powered

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI · China. All rights reserved.
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