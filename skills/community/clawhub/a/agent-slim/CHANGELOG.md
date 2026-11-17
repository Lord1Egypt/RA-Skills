# Changelog

## 0.3.0 — 2026-11-17

通用宿主版。0.2.0 的注入测量、漂移状态机与发布闸门全部保留；本版把"只认两类内置布局"改成"任何 Agent 都能接入"，并补齐通用手法与度量口径。

### 新增

- `--layout layout.json`：声明常驻文件（`hot`）、技能根、规则根、会话根、日志根、备份根。内置分支认不出的 Agent 不必改代码即可跑 `audit / plan / apply / verify / restore`。`host` 与 `audit` 都可传，`host` 会回显声明内容。
- `schemas/layout.schema.json`：布局字段、上限与默认值。
- `references/generic-playbook.md`：六类膨胀源（规则 / 记忆 / 技能 / 工具 / 文档 / 冷数据）× 五类手法（压缩 / 外移留指针 / 去重 / 裁剪暴露面 / 归档），逐类给识别信号、动作与保体验红线，附常见反模式。
- `references/measurement.md`：三本账分开记、不依赖宿主的常驻测法、同类任务账单对比、日/月换算公式、报告模板、证明"体验没变"的四项证据。
- `references/case-workbuddy.md`：一次完整瘦身的落地记录（结构差异、七阶段、逐块数字、卡点与回滚）。定位是参照物，不是使用前提。
- `tests/test_layout.py`：布局驱动、告警替换、默认路径不变、路径逃逸、坏文件与命令回显共 7 项。

### 变化

- `SKILL.md` 重写：从"某个 Agent 的工具"改为"任何 Agent 的方法"，新增"六类源 × 五类手法"和"体验不变的底线"；发布闸门与注入测量章节保留。`description` 压到 41 字，`SKILL.md` 7,083 B，均在闸门内。
- 布局接管 `hot` 列表后，缺失文件报通用码 `HOT_FILE_MISSING`，不再误报 `AGENTS_MISSING` / `MEMORY_SUMMARY_MISSING` / `RULES_INDEX_MISSING`。
- 布局路径校验：绝对路径、`~` 开头、Windows 盘符与 `..` 段一律拒绝并返回退出码 64。判定基于原始值，先剥分隔符会把 `/tmp/x` 变成相对路径而放行。
- `manifest.json`：hosts 改为 `codex` / `workbuddy`（内置布局）+ `described`（布局文件）；entrypoints 增加通用手法、度量、案例与布局 schema。
- `docs/usage.md` 新增第 3 节布局说明（后续章节顺移），并修掉上一版遗留的重复章节号。

### 实测

- 默认路径无回归：不传 `--layout` 时 Codex 仍为 `host=codex`、hot 67 / warm 335 / cold 5 类。
- 布局生效：第二个 Agent 上 Hot 23→28 条、2,985→5,497 tok，常驻记忆与身份文件第一次被计入；3 条厂商专属误报告警归零。基线偏小会让后续百分比整体虚高。
- `python3 -m unittest discover -s tests`：44 项通过。

### 已知限制

- 本版出包环境没有 `codex` 命令，`measure_prompt.py --gate 57344` 与 `injection_state.py` 的真实 measurement 分支未能执行，按规矩记 `UNMEASURED`，不写成 PASS；`self_test.py` 中依赖 `codex` 的 6 项同样未验证，其余 3 项（看板求和、token 观测过滤、样本不足不报节省）PASS。
- 真实宿主 test-prompts 仍未提供，触发/路由回归只能是 `PARTIAL`。

## 0.2.0 — 2026-11-10

注入测量与发布闸门版。保留 0.1.x 的整体盘点、可逆执行和回滚能力，新增 Codex 固定注入的只读测量、漂移状态机和发布前瘦身闸门。

### 新增

- `scripts/measure_prompt.py`：测量七块固定注入，按 `--gate 57344` 判定文本块是否超预算；超限退出 1。
- `scripts/injection_state.py`：记录源文件指纹与当前注入块，区分 `OK / DRIFT / BODY_CHANGED / MISSING / UNMEASURED`；写状态前自动备份。
- `scripts/mcp_probe.py`：只测 MCP `tools/list` 的 schema 字节，不记录 token、请求头、请求体或提示词。
- `scripts/scan_layers.py`：四层规则去重与冲突候选，只报告，不自动合并。
- `scripts/budget_dashboard.py`：七块预算看板，明确区分文本块、MCP 占位和 App 整体 `UNMEASURED`。
- `scripts/token_experiment.py`：首请求 input 观测，固定 `billing_claim=false`，不把观测写成账单节省。
- `scripts/self_test.py`：七块对账、gate 正反例、状态机 DRIFT、看板求和和 token 过滤的自测。
- `docs/injection-measurement.md`：七块口径、状态机、发布闸门、隐私边界和已知限制。

### 图标

- `icons/icon_large.png`（512）与 `icons/icon_small.png`（128）改为 Skill 系列蓝图蓝标：深蓝底 `#0A1F3C` + 青蓝线 `#4AD3FF` + 网格底纹，图元为三层收窄的上下文块 + 量尺 + 收窄箭头。
- `scripts/make_icons.py` 重写为纯标准库渲染器（有符号距离抗锯齿），可离线复现同款图标，不再依赖 PIL。
- SkillHub 图标走平台图标上传接口，`iconUrl` 随发布 payload 提交；包内不含二进制图标。

### 发布闸门

新增或修改 Skill 发布前必须全过：

- `description` 单条 ≤45 字。
- `SKILL.md` 目标 ≤8 KB；超出外移到 `references/`，只搬不删。
- `injection_state.py --record` 后 `--check` 返回 `overall: OK`。
- `measure_prompt.py --gate 57344` 文本块 PASS。
- `self_test.py` 全部 PASS。
- `check_integration`、`check_release` 和包内测试通过。

`UNMEASURED` 和 `UNKNOWN` 不得写成 PASS。

### 修复

- 修复干净克隆后 `tests/fixtures/aging-agent/AGENTS.md` 被 `.gitignore` 排除、导致 33 项测试中 2 项失败的问题；现在 fixture 明确重新纳入版本控制。
- 发布脚本固定时间戳更新为 2026-11-10，三平台包可复现构建。
- 新增脚本和文档去除个人绝对路径与 Codex Home 字面量，统一使用 `CODEX_HOME`。
- 基线 JSON 的 `source_file` 改为通用占位，`source_mtime` 清空，保留字节与哈希口径。

### 兼容性

Python 3.9+，仅标准库。0.1.x 的 `agent_slim.py` 命令、manifest、事务和恢复脚本保持兼容；新增测量命令独立，不影响既有审计与执行路径。

## 0.1.2 — 2026-11-05

可移植性修复版。功能、安全边界和发布包内容规则不变，只修“ClawHub 安装副本跑不通随包测试”。

### 修复

- ClawHub 发布器会跳过任何含点号路径段的文件，`tests/fixtures/aging-agent` 里的 `.mcp.json`、`.app.json`、`.usage.json` 因此进不了安装副本，导致安装后 `python3 -m unittest discover -s tests` 出现 2 项失败。`tests/test_audit.py` 现在会在拷贝 fixture 后按内联内容补齐这三个隐藏文件。
- `tests/test_release.py` 的清单一致性检查允许“隐藏文件缺失”，但仍要求其余清单项与 GitHub 包完全一致，避免掩盖真实缺件。

### 验证

- 剥离全部点号路径文件模拟 ClawHub 安装副本后，`python3 -m unittest discover -s tests` 33 tests OK。
- 三个平台安装副本与源码 `scripts/agent_slim.py` 的 SHA-256 一致。

## 0.1.1 — 2026-11-05

发布后回查修复版。0.1.0 的功能与安全边界不变，仅修复“发布包内测试不能独立运行”和文档状态。

### 修复

- `tests/fixtures/aging-agent` 之前被 `.gitignore` 排除且未随包发布，导致干净安装后运行 `python3 -m unittest discover -s tests` 时 `test_audit` / `test_workflow` 共 13 项报 `FileNotFoundError`。fixture 现随仓库和 GitHub/ClawHub 包发布，SkillHub 轻量包仍不含 tests。
- `.gitignore` 不再忽略该合成 fixture；它只含生成数据，无用户、项目或公司内容。

### 文档

- README 增加 GitHub / SkillHub / ClawHub 三平台安装入口、版本和 SHA-256 核对方式。
- 更新“当前状态”：三平台已发布 v0.1.1，并保留真实宿主触发回归 `PARTIAL` 的说明。

### 验证

- 本机与公开包隔离目录均执行 `python3 -m unittest discover -s tests`：33 tests OK。
- 公开包 fixture 端到端：180 个文件 apply 后 `restore --apply` 全部复原（SHA-256、大小、mode、mtime 一致），二次恢复返回 `already-restored`。

## 0.1.0 — 2026-11-05

首次公开发布（release candidate）。

### 功能

- `host`：只读探测宿主能力，输出 `supported / unknown / unsupported` 三态；缺失 Home 时相关能力降级为 `unknown`，不猜。
- `audit`：Hot/Warm/Cold 三层盘点，Token 与磁盘分账，输出结构化证据、warning、unknown 和候选。
- `plan`：只把 allowlist 内动作放进 ready；无哈希或确认证据的项停在 pending。
- `apply`：默认 dry-run；`--apply` 事务化移动，写 manifest、`manifest.sha256`、`restore.py` 和 `restore.sh`。
- `verify`：保留文件、引用、frontmatter、可选 test-prompts 回归；缺 test-prompts 时为 `PARTIAL`。
- `restore`：幂等恢复，冲突返回 `SOURCE_CONFLICT` 并保留双方内容。
- 三种可执行动作：`quarantine-redundant-backup`、`archive-verified-old-session`、`quarantine-low-frequency-file`。

### 发布包

- GitHub 完整包：源码、测试、docs、references、schemas、agents 配置和图标。
- SkillHub 轻量文本包：运行脚本、SKILL/README、契约文档和图标，不含 tests 与构建脚本。
- ClawHub 合规包：与 GitHub 完整包功能一致，按仓库根目录布局。
- 三包共享文件逐字节一致，SHA-256 写入 `SHA256SUMS.txt`。

### 版本说明

开发期内部里程碑曾使用 0.1.0 → 0.2.x → 0.3.0 作为工作版本号。公开发布按计划统一重编号为首发版 0.1.0；此前版本从未对外发布，不存在外部用户升级问题。功能等价于内部 0.3.0（s4 完成态）。

### 已知缺口

- 真实宿主 test-prompts 未提供，触发/路由回归只能记 `PARTIAL`，不作为“能力未回退”的完整证据。
- 非 Codex 宿主只有适配器接口，未实测。
- 内容改写、插件关闭、数据库维护、系统配置修改仍属人工复核，不在自动执行范围。

### 兼容性

Python 3.9+，仅标准库；macOS、Windows、Linux。文件路径参数请加引号以避免空格问题；Windows 请使用 PowerShell 或 Git Bash 调用 `.sh` 之外的 `.py` 入口。
