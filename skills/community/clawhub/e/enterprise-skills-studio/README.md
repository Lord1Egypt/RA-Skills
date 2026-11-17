# 企业技能工程台 · Enterprise Skills Studio

> **版本：v1.1.0** ｜ 通用 · 跨平台 ｜ 遵循 agentskills.io 开放标准

一句话：把"企业技能（Enterprise Skills）"的方法论，固化成一个**通用、跨平台**的"技能工程台"——帮企业把最佳实践、业务流程、个人经验，结构化成 Agent 可调用、可治理、可复用的能力模块（即**受治理的业务工作流制品**）。

它不替你做业务，而是提供一整套从**学习 → 设计 → 治理 → 安全 → 进化 → 跨平台移植 → 门户分发**的方法论 + 可脚本化工具链。最终产出的技能遵循 agentskills.io 开放标准，可在 WorkBuddy / Codex / Claude Code / Cursor / 龙虾 / Hermes 等桌面 Agent 间移植。

**跨平台验证状态（v1.0 已实测通过）：** ✅ WorkBuddy　✅ Codex　✅ TRAE WORK　（理论兼容 Claude Code / Cursor / 龙虾 / Hermes 等一切支持 agentskills.io 的桌面 Agent）

> **关于企业样例库**：本技能附带的 `references/cases.md` 目前为方法论文献与公开基准占位。真实的企业技能样例，有待于各企业在应用本技能的过程中逐步沉淀、充实——它本身就是"边用边长"的。

---

## 企业使用须知（定位说明）

本技能定位为**企业决策与建设的辅助工具**，而非可完全依赖的自动化系统：

- **辅助决策，而非替代判断**：它提供成熟度评估、ROI 门槛、安全体检、查重等"参考结论"，但最终是否立项、是否发布、如何治理，仍由企业的人来拍板。
- **先试用，再融合**：建议企业先以小范围流程做测试，确认功能确实可用后，再把它**融合进企业自身的工作流**——例如把 `studio gate` 接进你们自己的 CI，把 `references/` 的方法论纳入内部规范。
- **可借鉴、可再造**：企业也可以不直接使用本技能，而是**借鉴其方法论与工具设计**，构建更贴合自身组织架构、合规要求与业务语境的工作流与工具链。

---

## 为什么需要它

企业里大量流程（报销、采购、HR、客服、运维）散落在文档和口口相传中。把它们做成"技能"能让 Agent 直接执行，但**做技能本身**也需要方法论与治理——否则会出现：

- 重复造轮子（多个团队做相似技能）
- 安全风险（密钥外泄、提权、`curl|sh` 投毒、prompt 注入）
- 无法移植（在某 Agent 能跑，换一个就废）
- 上线即失管（无版本、无审计、无弃用机制）

企业技能工程台就是为解决这些问题而生：**一套方法论 + 16 个可脚本化工具 + 24 个能力模式**，覆盖从"该不该做"到"安全发布、持续进化、跨平台分发"的全生命周期。

---

## 核心特点

- **厚技能 + 薄 harness**：智能封装进技能本身（脚本/模板/决策树/校验），harness 只做调度。本技能自身亦遵守。
- **零依赖、可离线、可 CI**：所有 16 个脚本均为纯 Python 标准库实现，复制即用，无需任何第三方包。
- **确定性可卡点**：安全审查是静态正则分析（非 LLM 推理），结果可复现、可嵌入 CI 自动拦截。
- **真正跨平台**：产出严格遵循 agentskills.io 标准，已在 WorkBuddy / Codex / TRAE WORK 实测可跑。
- **端到端生命周期闭环**：从规划（ROI/成熟度）→ 构建（设计/升级/查重）→ 治理（安全/生命周期）→ 进化（Evolution Log/成本计量）→ 分发（编排/评测/门户），不留治理死角。
- **可治理、可审计**：版本、弃用、审计、责任归属都有对应工具与文档支撑，符合企业对"可控 AI"的要求。
- **自包含、可移植的知识库**：技能本身即是方法论载体，新窗口、新团队拿来即用，不依赖某次对话的上下文。
- **安全语义层检测**：映射 OWASP AST10，覆盖编码绕过、敏感路径、裸 IP 外联、提权、未声明装包、声明-能力一致性、供应链投毒；并能识别"防御性提及"避免误报安全类技能。
- **自更新（检查 / 确认后升级）**：从钉置到不可变发布标签的可信仓库拉取、SHA256SUMS 校验、合并白名单、增量更新本技能自身，可备份回滚、git 仓库自动保护；企业可经 `ESS_SELF_UPDATE`/`ESS_ALLOWED_REPOS` 管控；内网可指向私有可信源。
- **技能安全审计（SkillSec 16 类）**：借鉴 NVIDIA SkillSpector 公开 16 类漏洞模式（自有开源实现），对任一技能（含本技能自身）做类 SkillSpector 式静态安全审计，输出「类别/严重度/置信度/证据/发现」报告，可作 CI 卡点。

---

## 能力全景（24 个模式）

| 阶段 | 模式 | 关键脚本 |
|---|---|---|
| 认知与规划 | 1 学习理解 · 8 体系规划 · 11 ROI 筛选 · 16 选题透镜 | `maturity_assess.py` / `roi_filter.py` |
| 设计与构建 | 2 构建设计 · 3 个人→企业升级 · 9 流程技能生成 · 13 技能发现/复用 | `upgrade_skill.py` / `dupe_check.py` / 模板 |
| 治理与安全 | 4 治理管理 · 5 安全审查 · 10 生命周期 Ops · 15 Agentic 治理 | `review_checklist.py` / `lifecycle_track.py` |
| 运营与进化 | 6/12 持续进化 · 14 培训推广 · 20 成本计量 | `evolution_log.py` / `training_pack.py` / `usage_tracker.py` |
| 编排·评测·分发·审计 | 17 编排 · 18 评测 · 7 跨平台 · 19 统一 CLI · 21 门户 · 22 发布卡点 · 23 自更新 · 24 技能安全审计 | `compose.py` / `eval_gen.py` / `cross_platform_check.py` / `portal.py` / `studio.py` / `update_skill.py` / `skillsec_audit.py` |

---

## 安全审查：7 维度静态体检

`review_checklist.py` 对一份技能做确定性体检，输出 PASS/WARN/FAIL + 评分：

1. 安全 8 项（凭据硬编码 / PII / 对抗指令 / 外泄 / Markdown 注入 / 外部输入校验 / 最小权限 / 审计）
2. CISO 5（映射 OWASP AST10）
3. 质量 5（name/description 规范 / 单一职责 / 三级加载 / 厚技能化 / 召回保守）
4. 厚技能体检
5. 事务安全四件套（幂等 / 回滚 / 审计 / 最小权限，流程技能专用）
6. 工作流可恢复性（状态机 / HITL / 降级 / 可观测）
7. 安全语义层（编码绕过 base64·ROT13·零宽字符 / 敏感路径 ssh·aws·.env·记忆文件 / 裸 IP 外联 / 提权 / 未声明装包 / 声明-能力一致性 / 供应链投毒 `curl|sh`）

另有 `skillsec_audit.py` 提供 **SkillSec 16 类安全审计**（方法论借鉴 NVIDIA SkillSpector 公开分类，自有开源实现），从「过度能动」视角补全上述 7 维度，详见下文。

---

## 发布前卡点：双体检 gate

```bash
python scripts/studio.py gate --skill <技能目录> --platform codex
```

一键同时跑 **安全体检 + 移植体检**，任一不过即整体 **BLOCK**：

- 退出码 `0` = 安全 + 移植都通过 → 放行
- 退出码 `2` = 任一不过 → 阻断（CI 据 exit code 自动卡发布/移植）

---

## 技能安全审计：SkillSec 16 类（借鉴 NVIDIA SkillSpector）

`skillsec_audit.py` 对任一技能（含本技能自身）做类 SkillSpector 式静态安全审计：

```bash
python scripts/studio.py audit ./some-skill          # 文本报告
python scripts/studio.py audit ./some-skill --json   # 给 CI 用
```

覆盖 16 类：过度能动 / 输出处理 / 叛变特工 / 触发滥用 / MCP 最低特权 / MCP 工具中毒 / 提示注入 / 数据外流 / 特权升级 / 供应链 / 系统提示漏出 / 记忆中毒 / 工具滥用 / 危险 AST / 污染追踪 / YARA 签名。输出字段含类别 / 严重度(高·中·低) / 置信度 / 证据 / 发现；退出码 `1`=存在「高」级发现（可作 CI 阻断）。

> 方法论借鉴 NVIDIA SkillSpector 公开 16 类漏洞模式；本实现为自有开源代码（纯标准库），不复制其代码或品牌。详见 `references/skill-spector-method.md`。

---

## 自更新：检查 / 确认后升级

本技能支持自我更新（模式 23）——你不用手动下载、解包、覆盖，说"检查/更新本技能"，它会先检查、确认后才应用自身的最新版本。

```bash
python scripts/update_skill.py --check            # 只检查有没有新版本（默认动作）
python scripts/update_skill.py --apply --backup   # 确认后应用，更新前先备份
python scripts/update_skill.py --apply --dry-run  # 只看将变更哪些文件，不写盘
python scripts/update_skill.py --gen-sum          # 发布侧：生成 SHA256SUMS 校验和
# 或通过统一 CLI：
python scripts/studio.py update --check
python scripts/studio.py update --apply           # 默认交互确认，明确警告将覆盖本地文件
```

- **版本真相**：技能根的 `VERSION` 文件 与 可信 GitHub 仓库（默认 `jiwei1122/enterprise-skills-studio`）的**最新发布标签（不可变）**比较，避免拉取易变分支。
- **完整性**：归档内含 `SHA256SUMS` 时逐文件校验，不匹配即中止；合并仅接受白名单路径，越界文件跳过。
- **增量合并**：只覆盖/新增远程有的文件，保留你本地额外文件；`--backup` 可更新前快照，随时回滚。
- **安全**：只解包 + 复制，绝不执行远程代码；归档做路径穿越校验，且要求根目录含 `SKILL.md` 才认可；若技能目录本身是 git 仓库则默认保护不误覆盖。
- **企业管控**：设 `ESS_SELF_UPDATE=off` 可禁用写盘更新；设 `ESS_ALLOWED_REPOS="a/b"` 限定可拉取仓库。详见 `SECURITY.md`。
- 企业内网可 fork 到内部仓库，用 `--repo` 指向私有可信源（并加入白名单），实现私有化自更新。

---

## 三种使用方式

**① 自然语言（推荐，管理者/业务人员）**
> "帮我把报销流程做成一个企业技能，要能审计、出错能回滚。"
> "发布这个技能前先给它做个体检。"
> "这个技能要装到 Cursor，帮我检查能不能直接用。"
> "检查/更新本技能，看看有没有新版本（将先预览差异并请你确认）。"

**② 直接跑脚本（工程师）**
```bash
cd <本技能目录>
python scripts/studio.py review  ./reimburse
python scripts/studio.py gate   --skill ./reimburse --platform codex
python scripts/studio.py dupe   --skills-dir ./skills
python scripts/studio.py portal --skills-dir ./skills --out PORTAL.md
```
所有子命令支持 `--json`（给程序）与 `--md`（给人看）。

**③ CI 卡点（DevOps / 安全合规）**
```yaml
# .github/workflows/skill-gate.yml
name: 技能发布体检
on: [push, pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: python scripts/studio.py gate --skill ./new-skill --platform codex
```
任何含高危问题的技能提交都会被自动拦下，无需人盯。

---

## 应用场景（10 个，非技术人员也能看懂）

| # | 谁会用 | 解决什么问题 | 直接对 Agent 说这句话就行 |
|---|---|---|---|
| 1 | 平台工程 / 流程负责人 | 把报销、请假等内部流程变成可复用的企业技能 | "帮我把公司报销流程做成一个企业技能，要能审计、出错能回滚。" |
| 2 | 安全团队 | 从网上装的技能可能偷密钥、偷数据，装前先查 | "这个从市场下载的技能，装进来之前先帮我查查有没有安全风险。" |
| 3 | 业务主管 | 不知道把某业务做成技能划不划算 | "把采购审批做成技能划算吗？帮我评估一下值不值得做。" |
| 4 | CIO / 数字化负责人 | 上了十几个技能各自为政，不知下一步怎么规划 | "我们公司现在的企业技能处在什么水平？下一步怎么规划？" |
| 5 | HR / 培训 | 技能做好了员工不会用、不知道 | "给这个报销技能生成一份给新人看的培训材料，含场景卡和常见问题。" |
| 6 | 跨团队架构 | 一份技能想在多个 Agent（如 Cursor）上都能用 | "这个技能要给 Cursor 团队用，帮我检查能不能直接搬过去。" |
| 7 | Agent 运营 | 管着好几个 Agent，权限和责任说不清 | "我们用了好几个 Agent 技能，怎么管起来？权限和责任怎么定？" |
| 8 | 技能负责人 | 业务变了，技能文档过期没人更新 | "这个报销技能最近改了审批流，帮我更新一下它的进化记录。" |
| 9 | 架构统筹 | 不同团队重复造相似技能，浪费资源 | "想新做一个客户查询技能，先帮我看看有没有已经做过的类似东西。" |
| 10 | 内审 / 合规 | 监管要证明 AI 技能安全、可控、可追溯 | "把我们所有上线的技能都做一次安全合规体检，出一份能留档的报告。" |

---

## 安装说明

本技能是一个标准 agentskills.io 技能目录，安装 = **把 `enterprise-skills-studio` 文件夹放进目标 Agent 的 `skills` 目录**。

**方式一：从 GitHub 克隆（推荐，便于更新）**
```bash
git clone <本仓库地址> /tmp/ess
# 然后按下方各平台路径复制/软链
```

**方式二：直接复制文件夹**

| 平台 | skills 目录（把本文件夹放进去） |
|---|---|
| **WorkBuddy** | `~/.workbuddy/skills/` （Windows: `C:/Users/<你>/.workbuddy/skills/`） |
| **Codex** | `~/.codex/skills/` |
| **TRAE WORK** | 该 Agent 的 skills 目录（与你验证时所用位置一致） |
| 其他（Claude Code / Cursor / 龙虾 / Hermes） | 对应 Agent 的 skills 目录，结构相同 |

> 复制后目录结构应为：`.../skills/enterprise-skills-studio/SKILL.md`（及 `scripts/`、`references/`、`assets/`）。重启或刷新 Agent 即可在对话中用自然语言触发。

**依赖**：Python 3.8+，无需任何第三方包（纯标准库）。

> **关于 Python 是否需要自己装**：普通用户用自然语言触发本技能时，运行脚本所需的 Python 由 Agent 宿主（WorkBuddy / Codex / TRAE WORK 等均自带）提供，**你无需在本机单独安装 Python**；只有当你打算在终端里手动运行这些脚本时，才需要本机具备 Python 3.8+。

---

## 目录结构

```
enterprise-skills-studio/
├── SKILL.md                 # 技能主入口（24 模式总索引）
├── README.md                # 本文件
├── VERSION                  # 版本号 1.1.0
├── assets/
│   └── SKILL.md.template    # 标准企业技能模板
├── references/              # 19 份方法论文档
└── scripts/                 # 16 个工具脚本
    ├── studio.py            # 统一 CLI（薄 harness）
    ├── review_checklist.py  # 安全审查（7 维度）
    ├── upgrade_skill.py     # 个人→企业升级
    ├── maturity_assess.py   # 成熟度评估
    ├── lifecycle_track.py   # 生命周期追踪
    ├── roi_filter.py        # ROI 筛选
    ├── evolution_log.py     # Evolution Log
    ├── dupe_check.py        # 技能查重
    ├── training_pack.py     # 培训包生成
    ├── cross_platform_check.py # 跨平台适配检查
    ├── compose.py           # 编排器生成
    ├── eval_gen.py          # 评测用例生成
    ├── usage_tracker.py     # 成本/计量追踪
    ├── portal.py            # 门户生成
    ├── update_skill.py      # 自更新（模式 23）
    └── skillsec_audit.py    # 技能安全审计 SkillSec 16 类（模式 24）
```

---

## 测试状态（v1.1.0）

已执行 L0–L5 全量发布前测试（见 v1.0 记录）：自身 `review` → 97/100 A、0 FAIL；`gate --platform codex` → PASS；5 个对抗脏样本 gate 退出码全部 2（BLOCK）；3 个真实技能正例无误报；15 子命令 + gate 冒烟全过（含 audit）；跨平台 codex/cursor 适配 PASS。v1.0.1 新增自更新（模式 23）：`update_skill.py` 检查/增量合并/备份/干跑逻辑已通过脚本冒烟（含临时旧版本目录端到端拉取归档验证）。

已执行 L0–L5 全量发布前测试：自身 `review` → 97/100 A、0 FAIL；`gate --platform codex` → PASS；5 个对抗脏样本 gate 退出码全部 2（BLOCK）；3 个真实技能正例无误报；15 子命令 + gate 冒烟全过（含 audit）；跨平台 codex/cursor 适配 PASS。v1.1.0 新增 **SkillSec 16 类审计**（模式 24）：`skillsec_audit.py` 自身 `py_compile` 通过 + 冒烟运行正常；对本技能自扫时 C03（自更新）如实命中——属设计内、受 `SECURITY.md` 七层防护治理的能力，符合预期，非漏洞。

---

## 路线图（后续可迭代）

- `gate --security-only` 模式（仅卡安全高危，放行质量类 FAIL）
- 评测闭环自动化（`eval_gen` 生成用例 → 自动执行 → 回归报告）
- 技能脚手架生成器（从业务流程文档/访谈自动起草 SKILL.md 初稿）
- 门户可视化增强（PORTAL.md 升级为带生命周期状态的 HTML 仪表盘）
- 治理集成接口（生命周期/审计事件可对接企业 SIEM 或工单系统）

---

## 许可证与贡献

内部分享 / 开源发布规则以仓库 LICENSE 为准。欢迎通过 Issue / PR 提交能力模式或检测规则。
