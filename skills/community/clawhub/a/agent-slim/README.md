# Agent Slim（Agent 整体瘦身师）

给使用一段时间后的 Agent 做一次“体检 + 可逆减负”：先找出真正占用每轮上下文的常驻内容（规则、记忆、技能清单、工具 schema），再把低频资料移到按需加载区，最后用回归测试证明关键能力还在。

不绑定特定 Agent：内置布局自动识别，其他 Agent 写一份 `layout.json` 描述目录即可，不用改代码。

## 安装（三平台）

三个平台使用同一 slug `agent-slim`，当前版本 `0.3.0`。

| 平台 | 安装方式 | 适用 |
| --- | --- | --- |
| GitHub | 下载 [agent-slim-github-v0.3.0.zip](https://github.com/lisong2003-lgtm/agent-slim/releases/tag/v0.3.0)，解压后运行 `python3 scripts/agent_slim.py --version` | 完整包，含测试与构建脚本 |
| SkillHub | `skillhub install agent-slim --namespace user_43faedd6 --dir "${CODEX_HOME:-$HOME/.codex}/skills"` | Codex 用户，轻量文本包 |
| ClawHub | `clawhub --dir "${CODEX_HOME:-$HOME/.codex}/skills" install agent-slim` | ClawHub / OpenClaw 用户 |
| 任意 Agent | 下载 GitHub 包，放到该 Agent 的 skills 目录；必要时加 `--layout layout.json` 指路 | 其他 Agent |

GitHub 包的 SHA-256 以 Release 附件 `SHA256SUMS.txt` 为准；下载后执行 `shasum -a 256 -c SHA256SUMS.txt` 核对。安装后先跑只读命令：

```sh
python3 "${CODEX_HOME:-$HOME/.codex}/skills/agent-slim/scripts/agent_slim.py" audit --help
```

## 5 分钟快速使用

1. **圈定范围**：说明要瘦身哪个 Agent、哪些项目或 Skill、哪些内容不能动。
2. **只读体检**：运行 `python3 scripts/agent_slim.py audit --json`；CODEX_HOME 可自动探测，也可用 `--home` 指定。此时不修改任何用户文件。
3. **生成计划**：运行 `plan --audit audit.json`；没有哈希或人工确认证据的项只进待确认，不进入执行。
4. **可逆执行**：`apply` 默认 dry-run；显式 `--apply` 才把 allowlist 文件移入 Home 外事务区，并先写 manifest、SHA-256 和恢复脚本。
5. **验证与恢复**：`verify` 检查保留文件、引用、解析和可选 test-prompts；`restore --apply` 幂等恢复，冲突时停止。

可直接对 Agent 说：

```text
用 agent-slim 审计当前 Agent，先 dry-run。
分别报告 Hot、Warm、Cold 三层、Token 与磁盘收益、风险等级和回滚方式。
不要修改任何文件，等我确认计划。
```

## 发布前瘦身闸门

0.2.0 起，任何 Skill 新增或修改，发布前都要过同一道闸门：

```sh
python3 scripts/injection_state.py --record
python3 scripts/injection_state.py --check      # 必须 overall: OK
python3 scripts/measure_prompt.py --gate 57344  # 文本七块必须 PASS
python3 scripts/self_test.py                    # 必须 ALL PASS
```

硬指标：`description` ≤45 字、`SKILL.md` 目标 ≤8 KB、文本块 ≤57,344 B、`check_integration` 与 `check_release` 全过。`UNMEASURED` 不是 PASS，`UNKNOWN` 不是已支持。

## 安全执行流程

```sh
python3 scripts/agent_slim.py host --home <codex-home> --output host.json
python3 scripts/agent_slim.py audit --json --output audit.json
python3 scripts/agent_slim.py plan --audit audit.json --output plan.json
python3 scripts/agent_slim.py apply --plan plan.json            # dry-run
python3 scripts/agent_slim.py apply --plan plan.json --apply
python3 scripts/agent_slim.py verify --plan plan.json --test-prompts prompts.json
python3 scripts/agent_slim.py restore --manifest <transaction>/manifest.json --apply
```

报告包含 Hot/Warm/Cold、体积、近似 Token、证据、风险、可逆性、warning 和待确认项。Token 是 `ceil(chars × 0.6)` 近似值，不是账单实测；Cold 只记磁盘。详见 [执行契约](docs/execution-contract.md) 和 [审计契约](docs/audit-json-contract.md)。

## 六类源，五类手法

每轮被吃掉的内容通常来自六类：常驻规则、记忆/画像、技能清单与正文、工具 schema、固定注入的文档、以及只占磁盘的冷数据。对应五类手法：**压缩、外移留指针、去重、裁剪暴露面、归档**。前四类才可能省 Token，归档只省磁盘。

逐类的识别信号与红线见 [通用瘦身手记](references/generic-playbook.md)；怎么量、怎么给用户看省了多少见 [度量与报告](references/measurement.md)。

## 三层收益怎么看

- **Hot**：每轮都进入上下文的规则、描述和工具说明；缩小它通常能直接减少每轮 Token。
- **Warm**：只有触发时才加载的 Skill 正文、参考文档和脚本说明；只有实际避免加载时才减少 Token。
- **Cold**：只占磁盘的归档、备份、旧会话；清理它只省空间，不算 Token 收益。

## 当前状态

- s1 已冻结产品边界、通用架构、安全 allowlist 和验收门槛。
- s2 只读审计引擎已实现：纯标准库、只读元数据、跨 fixture 测试、稳定 JSON 契约。
- s3 安全执行已实现：plan/apply/verify/restore、允许清单、事务 manifest、SHA-256、恢复脚本、冲突保护和 fixture 端到端恢复。
- s4 已完成职责适配与合成老化环境端到端：能力三态、30 个用户 Skill、100 个会话、三类可执行动作和全量恢复证据。
- s5 已完成 Ponytail 与技能架构师审查、发布元数据和三平台发布包；包内共享文件逐字节一致。
- 真实宿主 test-prompts 仍未提供，触发/路由回归只能记 `PARTIAL`；不得把 fixture 结果写成真实宿主 PASS。
- v0.2.0 为三平台公开版本，新增注入测量、漂移状态机与发布闸门；发布回查记录见 `outputs/s5-release-ready.md`。
- v0.3.0 把宿主假设降为可配置项：新增 `layout.json` 接入任意 Agent、通用手法手册、度量报告模板与实测案例；注入测量与发布闸门保留。
- 发布包内测试可离线运行：`python3 -m unittest discover -s tests`（fixture 随包提供，不再依赖本机生成物）。

## 文档入口

- [技能入口](SKILL.md)
- [使用说明](docs/usage.md)
- [架构](docs/architecture.md)
- [安全边界](docs/safety.md)
- [执行契约](docs/execution-contract.md)
- [验收标准](docs/acceptance.md)
- [固定注入测量与发布闸门](docs/injection-measurement.md)
- [审计 JSON 契约](docs/audit-json-contract.md)
- [通用瘦身手记](references/generic-playbook.md)
- [度量与报告](references/measurement.md)
- [实测案例](references/case-workbuddy.md)
- [布局描述 schema](schemas/layout.schema.json)
- [适配器契约](references/adapter-contract.md)
- [职责路由与调用契约](references/integration-routing.md)

## 设计原则

默认只读、证据优先、最小改动、可逆执行、能力优先于数字。无法证明的收益不写成收益；无法实测的宿主能力不写成已支持。
