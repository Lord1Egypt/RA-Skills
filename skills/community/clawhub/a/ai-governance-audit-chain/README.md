# AI 留痕与门禁（ai-governance-audit-chain）

> 「凡自治之物 —— 有籍 · 有证 · 有门禁。」

给任何 AI 系统或智能体装上三件套：**L1 立籍**（谁在干、干什么、依据什么）、**L2 留证**（改了什么、证据在哪、怎么复算）、**L3 设门**（高危动作前必须过闸）。

## 它解决什么

| 你的问题 | 它给的动作 |
|---|---|
| AI 改完文件就说完了，事后说不清谁改了什么 | 生成可复算的证据链（指纹 + 变更台账 + 双时间戳） |
| AI 自动发邮件/发帖/删文件，怕它乱来 | 高危动作登记 → 未确认出不了"可举证"结论 |
| 出了问题追不到人，也不知当时依据什么 | 每任务一条籍：谁发起、干什么、依据哪份材料、谁批的 |

## 一分钟上手

```bash
python scripts/audit_chain.py init --root . --task "要做什么" --actor "谁在干"
# …干活…
python scripts/audit_chain.py seal --root . --note "本轮做了什么"
python scripts/audit_chain.py verify --root . --report EVIDENCE_REPORT.md
```

`verify` 三种判定，正好对应三件事：

- `[L2 PASS]` 指纹与基线一致 → 没有未记录改动
- `[L2 FAIL]` 有文件变了但没记录 → 这就是「说不清谁改了什么」
- `[L3 WAIT]` 有高危动作未确认 → 这就是「闸门没拦」

## 四个子命令

| 命令 | 作用 | 产物 |
|---|---|---|
| `init` | L1 建籍 + 基线快照 | `.governance/registry.jsonl` |
| `seal` | L2 追加指纹快照（记录 delta） | `.governance/evidence.jsonl` |
| `gate` | L3 登记高危动作，待人工确认 | `.governance/gates.jsonl` |
| `verify` | 复算并出举证报告 | `EVIDENCE_REPORT.md` |

零依赖，只用 Python 标准库；产物只增不改。

## 目录

```
SKILL.md                        技能主文件（触发 / 工作流 / 反例 / 边界）
scripts/audit_chain.py          证据链引擎（init / seal / gate / verify）
references/01-证据链模板.md      一条证据必须包含的 7 个字段
references/02-门禁清单.md        A/B/C 三级动作与三种闸门实现
references/03-反例与边界.md      七种错法 + 五件不做的事 + 红线
references/04-项目治理骨架.md    可直接复制的目录结构与字段说明
LICENSE.md                      分层许可（代码 MIT / 理论文本保留所有权利）
ATTESTATION.md                  权属证据（时间戳 + 内容指纹）
```

## 边界

- 不出具法律意见、不做合规结论认定
- 不替代第三方认证（ISO/IEC 42001 / NIST AI RMF / GB/Z 185 等）
- 不承诺不可篡改（需要时另接可信时间戳服务）
- 不追补安装前的历史动作
- 不把密钥与个人隐私写进台账

## 与 LGD 的关系

本技能是 LGD（Lifecycle Governance Doctrine / 全程治理论）的实现层落地件，提供 **How**，不主张优先于任何既有标准或前人工作。

## 署名

诺衡(Krites)@SynomosAI ｜ © 2026 赵兴华 / Steven Zhao·China
