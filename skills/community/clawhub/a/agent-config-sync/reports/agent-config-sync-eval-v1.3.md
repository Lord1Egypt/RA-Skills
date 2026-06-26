# agent-config-sync v1.3.0 — 重新评估报告

**评估日期**: 2026-05-16
**评估人**: 大师 (acode)
**评估范围**: v1.3.0 package → SKILL.md + 5 references + 2 scripts + 安全评估 + 部署状态
**前次评估**: v1.1 报告 `agent-config-sync-eval-v1.1.md` (评分 2.25/5)

---

## 📊 执行摘要

| 维度 | v1.1 评分 | v1.3 评分 | 变化 |
|------|:---:|:---:|:---:|
| 通用性 | 2/5 | **4/5** | ✅ +2 |
| 可扩展性 | 2/5 | **4/5** | ✅ +2 |
| 文档质量 | 2/5 | **4/5** | ✅ +2 |
| 跨平台兼容性 | 3/5 | **3/5** | — 持平 |
| 代码健壮性 | 3/5 | **4/5** | ✅ +1 |
| 部署状态 | — | **2/5** | ⚠️ 脏 |
| 安全覆盖 | 未评估 | **4/5** | ✅ 良好 |
| **综合** | **2.25/5** | **3.6/5** | **+1.35** |

**结论**: v1.3.0 package 的代码实际为 v1.2，但 v1.2 相比 v1.1 在通用性/可扩展性/文档上有显著提升。Registry 格式已验证可用。当前部署环境处于「脏状态」——需要清理 v1.1 残留、升级 Master HEARTBEAT item 12、重建 CHANGELOG。

---

## 1. v1.3.0 改进验证

### 发现：v1.3.0 是 metadata-only 版本跳升

```
_meta.json  version: "1.3.0"    ← 包版本
SKILL.md    header:  "v1.2"     ← 代码版本
所有脚本    header:  "v1.2"     ← 代码版本
```

**实际变更内容**（v1.2 → v1.3.0）:

| 变更项 | 状态 |
|--------|------|
| `agent-registry.json` 模板修复为 `vars` + keyed agents | ✅ 已修复（本次包更新的核心） |
| SKILL.md 代码逻辑 | ❌ 无变化 |
| `scripts/init_sync.sh` | ❌ 无变化 |
| `scripts/force_sync.sh` | ❌ 无变化 |
| references 文件 | ❌ 无变化 |
| 新功能 | ❌ 无新增 |

**v1.3.0 本质上是一次 registry JSON 格式的兼容性修复版**（从错误的数组/旧格式修正为脚本期望的 `{"vars":..., "agents":{...}}` 结构）。功能代码与 v1.2 完全一致。

### v1.2 相对 v1.1 的实际改进（本次评估确认）

| v1.1 问题 | v1.2 修复 | 验证 |
|-----------|----------|:---:|
| Agent 列表硬编码在脚本参数 | 从 `agent-registry.json` 读取（单一真实来源） | ✅ |
| 脚本全中文输出 | `--lang en\|zh` 双语支持 | ✅ |
| 无 dry-run | `--dry-run` 预览模式 | ✅ |
| 无 --help | `-h` / `--help` 完整帮助 | ✅ |
| 无 demo 模式 | `--demo` 学习模式（/tmp 演示） | ✅ |
| 无 `--confirm` 安全门 | 写入操作需 `--confirm` | ✅ |
| 无 English quickstart | `references/quickstart.md` 新增 | ✅ |
| SKILL.md 无安装章节 | Installation / Configuration / Upgrading 章节完整 | ✅ |
| HEARTBEAT 模板绑定特定 agent | `references/sync-setup.md` 使用变量名 | ⚠️ 仍含硬编码中文 agent 名 |

---

## 2. Registry 格式修复验证

### 测试环境：Bash `json_val()` 函数（同 init_sync.sh 内置）

```
✅ vars.workspace_root       → ~/.openclaw
✅ vars.master_agent         → amaster
✅ vars.master_memory (raw)  → ${vars.workspace_root}/workspace-${vars.master_agent}/memory
✅ vars.master_memory (res.) → ~/.openclaw/workspace-amaster/memory
✅ agents.acode.workspace    → ~/.openclaw/workspace-acode
```

### Agent ID 提取

```
✅ read_agent_ids() → acode, ainvest, alive (3 agents)
✅ master_agent (amaster) 自动排除（不下发给自身 SYNc 文件）
```

### 变量解析验证

| 输入值 | 解析后 | 结论 |
|--------|--------|:---:|
| `${vars.workspace_root}/workspace-acode` | `~/.openclaw/workspace-acode` | ✅ |
| `${vars.workspace_root}/workspace-${vars.master_agent}/memory` | `~/.openclaw/workspace-amaster/memory` | ✅ |

**Registry 格式验证结论**: 完全可用。`json_val()` 提取 + `resolve_vars()` 变量替换 + `expand_path()` 路径扩展三层管道工作正常。

---

## 3. 实际 dry-run 验证

```
bash scripts/init_sync.sh --dry-run --lang zh
```

### 输出解析

| 检查项 | 预期 | 实际 | 结论 |
|--------|------|------|:---:|
| Master workspace 检测 | `workspace-amaster` | `/home/admin/.openclaw/workspace-amaster` | ✅ |
| Agent acode 识别 | 是 | ✅ Agent 'acode' 已配置 | ✅ |
| Agent ainvest 识别 | 是 | ✅ Agent 'ainvest' 已配置 | ✅ |
| Agent alive 识别 | 是 | ✅ Agent 'alive' 已配置 | ✅ |
| 跳过 master agent | amaster 不下发 | amaster 不在列表中 | ✅ |
| 版本文件创建 | memory/ 目录 | memory 已存在，sentinel 跳过 | ✅ (幂等) |
| SYNC.md 状态 | 已是最新 | "已是最新，跳过" × 3 | ✅ |
| BOOTSTRAP 状态 | 已有检查 | "已有同步检查" × 3 | ✅ |
| HEARTBEAT 状态 | 已有检查 | "已有同步检查" × 3 | ✅ |

**Dry-run 结论**: 全部通过。脚本逻辑正确，agent 列表从 registry 自动读取，路径解析正常。

---

## 4. 部署差距分析

### 当前环境详细状态

```
memory/.current_system_version  = v3.1  (quant system version, not sync-format)
memory/.last_sync_version       = v3.1  (same → no mismatch possible)
memory/.sync_journal.jsonl      = 0 bytes (exists but empty)
memory/CHANGELOG.md             = quant system full changelog (v0.1→v3.1)
Master HEARTBEAT item 12        = v1.1 format (pending_sync.md singular, hardcoded names)
```

### 差距清单

| # | 问题 | 严重度 | 影响 |
|---|------|:---:|------|
| G1 | **Master HEARTBEAT item 12 is v1.1** — `pending_sync.md` (单数)、硬编码"大师/元宝/牛奶"、无 journal dispatch、无 SHA256、无重试 | 🔴 高 | 即使版本 mismatch，dispatch 仍用旧机制 |
| G2 | **下游 Agent 重复条目** — BOOTSTRAP/HEARTBEAT 各含 2 份同步检查（v1.1 + v1.2），共 12 处冗余 | 🔴 高 | Agent 每次 heartbeat 执行 2 次相同同步检查 |
| G3 | **`pending_sync.md` (v1.1 单数) 仍然存在** — 下游 agent 的 BOOTSTRAP/HEARTBEAT v1.1 条目检查 `pending_sync.md` 而非 `pending_sync_*.md` | 🔴 高 | v1.2+ 产生的 `pending_sync_v3.1_xxx.md` 文件不会被 v1.1 检查发现 |
| G4 | **CHANGELOG.md 格式不兼容** — 当前为量化系统完整功能履历，不符合 sync 结构化格式（`## vX.Y (YYYY-MM-DD)` + `**Change Type**:` + `**Affected Agents**:`） | 🟡 中 | sync dispatcher 无法正确解析变更章节 |
| G5 | **`.current_system_version` = v3.1 但无对应 sync 条目** — quant 系统版本 vs sync 版本命名空间冲突 | 🟡 中 | 需要决定是否分离量化版本和 sync 版本 |
| G6 | **`agent-setup.md` 参考文件过期** — 内容为 v1.1 格式（`pending_sync.md` 单数），但 `init_sync.sh` 已生成 v1.2 内容 | 🟢 低 | 文档误导，但脚本不使用该文件 |
| G7 | **`quickstart.md` 引用 `.agent_registry` 旧文件名** — 实际文件是 `agent-registry.json` | 🟢 低 | 新用户可能困惑 |
| G8 | **`.sync_journal.jsonl` 为空** — 虽然有文件，但从未有 sync 记录 | 🟢 低 | 初始化时 touch 了空文件但从未实际使用 |
| G9 | **无 `.last_sync_version` 初始化语义** — 当前值为 v3.1（与 current 相同），但未被 init_sync.sh 正确设置 | 🟢 低 | 需要运行 `force_sync.sh` 或手动重置 |

### 下游 Agent 重复条目详情

每个下游 agent 的 **BOOTSTRAP.md**:
```
✗ 第1份 (v1.1): "检查工作目录下是否存在 `pending_sync.md`"
✓ 第2份 (v1.2): "检查工作目录下是否存在 `pending_sync_*.md` 文件"
```

每个下游 agent 的 **HEARTBEAT.md**:
```
✗ 第1份 (v1.1): "检查工作目录下是否存在 `pending_sync.md`"
✓ 第2份 (v1.2): "<!-- agent-config-sync-check v1.2 --> + pending_sync_*.md + SHA256 验证"
```

**原因**: v1.1 和 v1.2 的 `init_sync.sh` 都用了 `grep -q` 检测 "pending_sync_" 但 v1.2 使用 `agent-config-sync-check` 作为 marker。v1.1 追加时匹配了 "pending_sync_" 但 v1.2 追加时 marker 不同，所以两次都追加成功。

---

## 5. 安全评估

### SECURITY.md 覆盖分析

| 安全维度 | SECURITY.md 覆盖 | 脚本实际执行 | 评价 |
|----------|:---:|------|:---:|
| **路径校验** | ✅ `~/.openclaw/workspace-*` only | ✅ `init_sync.sh` case match, `force_sync.sh` case match | 正确 |
| **跨 agent 隔离** | ✅ 每个 agent 只读写自己的 workspace | ✅ 脚本只操作各 agent 的 BOOTSTRAP/HEARTBEAT/SYNC | 正确 |
| **用户确认** | ✅ `--confirm` required for writes | ✅ 两脚本均强制检查 `CONFIRMED` | 正确 |
| **Dry-run 预览** | ✅ `--dry-run` 始终可用 | ✅ 两脚本均支持 | 正确 |
| **备份机制** | ✅ 修改前备份 | ✅ `force_sync.sh` 创建 `.bak.timestamp` | 正确 |
| **变更日志** | ✅ stdout + journal 记录 | ⚠️ stdout 输出完整但 journal 从未实际写入 | 部分 |
| **无网络访问** | ✅ 声明不需要 | ✅ 脚本零网络调用 | 正确 |
| **无凭据访问** | ✅ 声明不需要 | ✅ 脚本不读任何凭证文件 | 正确 |
| **权限模型** | ✅ 声明 AMaster 可写所有 workspace | ⚠️ `pending_sync` 写入由 HEARTBEAT 逻辑执行，不在脚本范围内 | 文档对应 |

### 安全评分: **4/5**

**扣分项**:
- 🔸 `force_sync.sh` 只备份 sentinel 文件，不备份 CHANGELOG.md
- 🔸 无 TOCTOU 防护（检查路径和写文件之间有时间窗口）
- 🔸 无 symlink 攻击防护（`test -d` 不检测是否为 symlink）
- 🔸 journal 写入逻辑仅在伪代码中描述，脚本不实际写入 journal

**肯定项**:
- ✅ 两阶段安全门（`--dry-run` + `--confirm`）设计良好
- ✅ 路径白名单机制（`case` match `$HOME/.openclaw/workspace-*`）硬编码在脚本中
- ✅ 所有文件操作限制在已知范围内，无任意路径写入
- ✅ 声明了权限范围并清晰标注不需要的能力

---

## 6. 综合评分与修复路线

### 6.1 总体评分

| 维度 | v1.1→v1.3 | 详情 |
|------|:---:|------|
| **代码质量** | 4/5 | 脚本逻辑清晰，路径安全，错误处理基本到位 |
| **部署状态** | 2/5 | 脏环境 — v1.1+v1.2 混合，需要清理 |
| **文档完整性** | 4/5 | 中英文全，安装/配置/升级/排错章节齐全 |
| **安全模型** | 4/5 | 路径校验+用户确认+隔离声明，小缺口 |
| **v1.3 增量价值** | 1/5 | 仅 registry JSON 兼容性修复，无功能变更 |

### 6.2 修复路线图

#### Phase 1: 下游 Agent 清理（立即执行）

```
任务 P1.1: 清理 BOOTSTRAP.md 重复条目
  目标文件: workspace-acode/BOOTSTRAP.md
            workspace-ainvest/BOOTSTRAP.md
            workspace-alive/BOOTSTRAP.md
  操作: 删除 v1.1 风格的 "## 启动检查 — 配置同步" 段（含 `pending_sync.md` 单数版本）
       保留 v1.2 风格的 "## 启动检查 — 配置同步" 段（含 `pending_sync_*.md` glob）

任务 P1.2: 清理 HEARTBEAT.md 重复条目
  目标文件: workspace-acode/HEARTBEAT.md
            workspace-ainvest/HEARTBEAT.md
            workspace-alive/HEARTBEAT.md
  操作: 删除 v1.1 风格的 "## ⭐ 配置同步检查" 段（含 `pending_sync.md` 单数，无 marker）
       保留 v1.2 风格段（含 `<!-- agent-config-sync-check v1.2 -->` marker）
```

#### Phase 2: Master Agent 升级（立即可行）

```
任务 P2.1: 升级 HEARTBEAT item 12
  目标文件: workspace-amaster/HEARTBEAT.md
  操作: 将当前 v1.1 格式替换为 references/sync-setup.md 中的 v1.2+ 格式:
        - pending_sync.md → pending_sync_<VERSION>_<SHA>.md
        - 硬编码 agent 名 → 从 agent-registry.json 读取
        - 添加 journal 记录步骤 (.sync_journal.jsonl)
        - 添加 SHA256 签名
        - 添加重试逻辑

任务 P2.2: 建立 CHANGELOG.md sync 格式
  目标文件: workspace-amaster/memory/CHANGELOG.md
  决策点: 量化版本 (v0.1→v3.1) 是保留在现有 CHANGELOG 还是分离？
  建议:
    - 方案 A: 将现有 CHANGELOG 归档为 CHANGELOG_quant.md，新建 sync-format CHANGELOG.md
    - 方案 B: 在现有 CHANGELOG.md 顶部添加 sync-format 条目，底部保留量化历史

任务 P2.3: 重置版本哨兵
  操作: echo "v1.0" > .current_system_version
        echo "v1.0" > .last_sync_version
  原因: v3.1 是量化系统版本，sync 系统应从 v1.0 独立计数
  备选: 保留 v3.1 但确保后续变更使用 sync-format CHANGELOG
```

#### Phase 3: 参考文件修正（低优先级）

```
任务 P3.1: agent-setup.md
  操作: 更新为 v1.2 格式（pending_sync_*.md glob），或标记为 deprecated
  注意: 该文件不由脚本使用，仅人工参考

任务 P3.2: quickstart.md
  操作: 修正 .agent_registry → agent-registry.json
```

#### Phase 4: v1.4 建议增强（未来）

```
建议 E1: SKILL.md 版本号同步
  将 SKILL.md header 中的 "v1.2" 更新为 "v1.3.0"，或移除内嵌版本号从 package.json 读取

建议 E2: init_sync.sh 增加清理功能
  添加 --clean 模式：自动移除 v1.1 重复条目

建议 E3: 添加 TOCTOU/symlink 防护
  force_sync.sh: 在写文件时使用 mktemp + mv 替代直接 echo

建议 E4: init_sync.sh journal 初始化
  首次创建 .sync_journal.jsonl 时写入初始化记录，而非空文件

建议 E5: 版本命名空间分离
  明确 sync 版本（sync-vX.Y）与系统版本（system-vX.Y）的独立性
```

---

## 附录 A: v1.1 评估问题解决状态

| v1.1 问题 | v1.2 解决? | v1.3 状态 |
|-----------|:---:|------|
| Agent 名称硬编码遍布全库 | ✅ Registry single source of truth | 已解决 |
| init_sync.sh 无 dry-run | ✅ --dry-run | 已解决 |
| 无 --help | ✅ -h/--help | 已解决 |
| 无英文 Quickstart | ✅ quickstart.md | 已解决 |
| 脚本全中文 | ✅ --lang en\|zh | 已解决 |
| SKILL.md 场景 A/B 绑定特定 agent | ✅ 用变量和通用描述替代 | 已解决 |
| sync-journal.md 全中文 | ❌ 仍为中文 | 未解决 |
| pending-sync-template.md 中文 | ❌ 仍为中文 | 未解决 |
| 路径硬编码 | ⚠️ 通过 registry vars 可配 | 部分解决 |
| force_sync.sh 不备份 CHANGELOG | ❌ | 未解决 |
| 无 demo 模式 | ✅ --demo | 已解决 |
| 增加第5个 agent 需改多处 | ✅ 只改 registry JSON | 已解决 |

---

## 附录 B: 测试数据

### Registry 解析测试
```
$ json_val "vars.workspace_root" agent-registry.json
~/.openclaw ✓
$ json_val "vars.master_agent" agent-registry.json
amaster ✓
$ resolve_vars "${vars.workspace_root}/workspace-acode"
~/.openclaw/workspace-acode ✓
```

### init_sync.sh --dry-run 输出
```
Master 工作空间: /home/admin/.openclaw/workspace-amaster
Agent 'acode' 已配置 ✓
Agent 'ainvest' 已配置 ✓
Agent 'alive' 已配置 ✓
```

### 部署环境文件状态
```
.current_system_version → v3.1
.last_sync_version      → v3.1 
.sync_journal.jsonl     → 0 bytes
CHANGELOG.md            → quant system full changelog
```
