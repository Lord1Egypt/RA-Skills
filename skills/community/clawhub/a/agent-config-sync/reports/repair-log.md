# agent-config-sync 本地部署修复日志

**修复日期**: 2026-05-16 10:30 CST
**执行人**: acode (大师)
**参考报告**: agent-config-sync-eval-v1.3.md §6.2 修复路线图
**量化系统版本**: v3.2
**同步系统版本**: v1.5 (v1.4 冲突管理 + v1.5 使用向导)

---

## 历次变更摘要

### v1.5 — 使用向导 + 开包即用 + GitHub 发布准备 (2026-05-16 13:00 CST)

#### 新增文件

| 文件 | 描述 | 状态 |
|:-----|:-----|:--:|
| `scripts/wizard.sh` | 交互式安装向导（纯 bash, 中英双语, --auto 模式） | ✅ |
| `README.md` | GitHub 项目 README（完整英文文档） | ✅ |

#### 修改文件

| 文件 | 变更 | 状态 |
|:-----|:-----|:--:|
| `_meta.json` | 版本 1.4.0 → 1.5.0 | ✅ |
| `scripts/init_sync.sh` | 新增 `--auto` 模式 + 自动检测 workspace 并生成 registry | ✅ |
| `scripts/init_sync.sh` | SYNC.md 模板增强（新手上路指南 + 常用操作速查表） | ✅ |
| `SKILL.md` | 顶部新增 Quick Start 章节，安装章节新增 Option A/B（wizard/auto） | ✅ |
| `SKILL.md` | Files 表格新增 wizard.sh 条目 | ✅ |
| `references/agent-registry.json` | 版本 1.4.0 → 1.5.0（quote 改双引号） | — |

#### wizard.sh 功能详情

| Step | 功能 | 实现方式 |
|:-----|:-----|:-----|
| Step 1 | 检测环境 | 检查 openclaw 命令 + 扫描 ~/.openclaw/workspace-* + 读取 IDENTITY.md |
| Step 2 | 配置注册表 | 自动生成 agent-registry.json，供用户确认/编辑 |
| Step 3 | 运行初始化 | 自动调用 init_sync.sh --confirm |
| Step 4 | HEARTBEAT 集成 | 自动追加 item 12 到 master HEARTBEAT.md |
| Step 5 | 完成报告 | 显示哨兵状态 + Agent 就绪状态 + 下一步指南 |

#### 特性

- `wizard.sh --auto`: 全自动检测，无需交互，2 分钟内完成安装
- `wizard.sh --lang en|zh`: 完整中英双语支持
- `wizard.sh --skip 1,4`: 可选跳过任意步骤
- `init_sync.sh --auto`: 一键初始化（自动检测 workspace，生成 registry，跳过确认）
- SYNC.md 新增「新手上路指南」和「常用操作速查表」
- 所有改动增量式，完全兼容 v1.4

#### 集成验证结果

```
$ bash scripts/wizard.sh --auto --lang en
== agent-config-sync v1.5 — Auto Setup ==
── Step 1/5: Detect Environment ✅
── Step 2/5: Configure Agent Registry ✅ (5 agents)
── Step 3/5: Initialize Sync Infrastructure ✅
── Step 4/5: Integrate HEARTBEAT ✅
── Step 5/5: Completion Report ✅

$ bash scripts/init_sync.sh --auto --dry-run --lang en  
=== Agent Config Sync v1.5 — Initialization ===
🤖 AUTO MODE — all good
```

---

### v1.4 — 版本冲突管理全量优化 (2026-05-16 11:30 CST)

**设计依据**: `/home/admin/.openclaw/workspace-amaster/skills/agent-config-sync/reports/version-conflict-management-design.md`

#### Phase 1: 基础增强 ✅

| ID | 任务 | 文件 | 状态 |
|:---|:-----|:-----|:--:|
| P1.1 | pending_sync 模板增加 TTL/过期时间/前置字段 | `references/pending-sync-template.md` | ✅ |
| P1.2 | 每个 agent 增加 `.agent_sync_version` 文件 | `scripts/init_sync.sh` | ✅ |
| P1.3 | 原子写入 `_atomic_write()` | `scripts/force_sync.sh`, `scripts/init_sync.sh` | ✅ |
| P1.4 | SECURITY.md 新增 Version Conflict Scenarios | `SECURITY.md` | ✅ |
| P1.5 | SKILL.md 新增 Version Conflict Management 章节 | `SKILL.md` | ✅ |

#### Phase 2: 核心冲突处理 ✅

| ID | 任务 | 文件 | 状态 |
|:---|:-----|:-----|:--:|
| P2.1 | CHANGELOG 新增 depends_on / 协同依赖 可选字段 | `references/sync-setup.md` | ✅ |
| P2.2 | Agent 端版本折叠逻辑 (Agent-side Version Collapse) | `SKILL.md` | ✅ |
| P2.3 | Master 端分发锁 (dispatch lock + timeout logic) | `references/sync-setup.md` | ✅ |
| P2.4 | 离线追赶包 (offline catch-up) | `references/sync-setup.md`, `SKILL.md` | ✅ |
| P2.5 | 循环检测 (loop detection) | `references/sync-setup.md`, `references/sync-journal.md` | ✅ |
| P2.6 | HEARTBEAT item 12 伪代码重写 (v1.4 增强版) | `references/sync-setup.md` | ✅ |

#### Phase 3: 高级场景处理 ✅

| ID | 任务 | 文件 | 状态 |
|:---|:-----|:-----|:--:|
| P3.1 | 自身升级隔离 (self_protect + isolated_sync) | `references/agent-registry.json`, `SKILL.md`, `SECURITY.md` | ✅ |
| P3.2 | 批量合入 (batch mode + batch_window_sec) | `references/agent-registry.json`, `SKILL.md`, `references/sync-setup.md` | ✅ |
| P3.3 | 回滚机制 (snapshots + revert manifest) | `references/sync-setup.md`, `SKILL.md`, `SECURITY.md` | ✅ |
| P3.4 | HEARTBEAT item 12 v1.4 完整文本 | `references/sync-setup.md` | ✅ (含 P2.6) |
| P3.5 | 集成验证 (`init_sync.sh --dry-run`) | 全部通过 | ✅ |

#### 版本与元数据

| 文件 | 旧值 | 新值 |
|:-----|:-----|:-----|
| `_meta.json` → version | `1.3.0` | `1.4.0` |
| `agent-registry.json` → version | `1.2.1` | `1.4.0` |
| `init_sync.sh` → title | v1.2 | v1.4 |
| `force_sync.sh` → title | v1.2 | v1.4 |
| `SKILL.md` → header | v1.2 | v1.4 |
| `pending-sync-template.md` → header | v1.1 | v1.4 |
| `.sync_own_version` | (不存在) | v1.4 |
| HEARTBEAT marker | v1.2 | v1.4 |
| BOOTSTRAP check | v1.2 (basic) | v1.4 (TTL + catch-up + isolated) |

#### 新建文件

| 文件 | 内容 |
|:-----|:-----|
| `skills/agent-config-sync/.sync_own_version` | `v1.4` |
| `workspace-{agent}/memory/.agent_sync_version` (×4) | `v1.1` |
| `workspace-{agent}/memory/.sync_snapshots/` (×4) | 空目录 |

#### 集成验证结果

```
$ bash scripts/init_sync.sh --dry-run --lang zh
=== Agent Config Sync v1.4 — 初始化 ===
Master 工作空间: /home/admin/.openclaw/workspace-amaster
ℹ️  版本文件已存在，跳过创建
ℹ️  all agents up-to-date
✅ 所有 agent 已配置
=== 初始化完成 ===

✅ .agent_sync_version 存在于所有 agent + master
✅ .sync_snapshots 目录存在于所有 agent + master
✅ .sync_own_version = v1.4
✅ _meta.json version = 1.4.0
✅ force_sync.sh --dry-run 正常（原子写入预览）
```

---

### v1.2 → v1.1: 初始部署 (2026-05-16 10:30 CST)

### Phase 1: 下游 Agent 重复条目清理 ✅

#### P1.1 — BOOTSTRAP.md 去重
| 文件 | 删除内容 | 保留内容 | 状态 |
|------|----------|----------|:--:|
| `workspace-acode/BOOTSTRAP.md` | v1.1 段 (`pending_sync.md` 单数 + 量化版本确认) | v1.2 段 (`pending_sync_*.md` glob) | ✅ |
| `workspace-ainvest/BOOTSTRAP.md` | 同上 | 同上 | ✅ |
| `workspace-alive/BOOTSTRAP.md` | 同上 | 同上 | ✅ |

**识别特征**: v1.1 段含 `pending_sync.md`（单数，无通配符）+ "使用量化系统/比价系统前先确认版本"

#### P1.2 — HEARTBEAT.md 去重
| 文件 | 删除内容 | 保留内容 | 状态 |
|------|----------|----------|:--:|
| `workspace-acode/HEARTBEAT.md` | v1.1 段 (`pending_sync.md` 单数，无 marker) | v1.2 段 (`<!-- agent-config-sync-check v1.2 -->` marker) | ✅ |
| `workspace-ainvest/HEARTBEAT.md` | 同上 | 同上 | ✅ |
| `workspace-alive/HEARTBEAT.md` | 同上 | 同上 | ✅ |

**识别特征**: v1.1 段无 `agent-config-sync-check` marker 且检查 `pending_sync.md` 单数

---

### Phase 2: Master Agent 升级 ✅

#### P2.1 — 升级 HEARTBEAT item 12
| 文件 | 变更 |
|------|------|
| `workspace-amaster/HEARTBEAT.md` | item 12 从 v1.1 升级到 v1.2 |

**具体变更**:
- `pending_sync.md` (单数) → `pending_sync_<VERSION>_<SHA>.md` (复用模式)
- 硬编码 agent 名 "大师/元宝/牛奶" → `agent-registry.json` 动态读取
- 新增: SHA256 签名生成步骤
- 新增: `.sync_journal.jsonl` 记录（含 timestamp/version/agent dispatch 状态）
- 新增: 重试逻辑（检查 `status=prepared` 记录）
- 日志目标: `MEMORY.md` → `.sync_journal.jsonl`
- 变更章节读取: "全量 CHANGELOG" → "最新版本变更章节（非全量）"

#### P2.2 — CHANGELOG 分离
| 操作 | 文件 |
|------|------|
| 重命名 | `CHANGELOG.md` → `CHANGELOG_quant.md` |
| 新建 | `CHANGELOG.md` (sync 标准结构化格式) |

**新 CHANGELOG.md 格式**: 按 `sync-setup.md` 规范，含 `**变更类型**` / `**影响范围**` / `**变更人**` / `**紧急程度**` 字段

#### P2.3 — 初始化 sync 哨兵
| 文件 | 值 | 说明 |
|------|:--:|------|
| `.current_system_version` | v1.0 | sync 系统版本（独立于量化系统 v3.2） |
| `.last_sync_version` | v1.0 | 与 current 一致（初始状态） |

---

### Phase 3: 参考文件修正 ✅

#### P3.1 — quickstart.md 文件引用修正
| 文件 | 变更 |
|------|------|
| `skills/agent-config-sync/references/quickstart.md` | `.agent_registry` → `agent-registry.json` (3处) |

#### P3.2 — Master HEARTBEAT pending_sync.md 缓存修复
| 文件 | 说明 |
|------|------|
| `workspace-amaster/HEARTBEAT.md` | 已在 P2.1 中一并修正，不再使用 `pending_sync.md` 单数格式 |

---

## 验证结果

### init_sync.sh --dry-run --lang zh
```
🔍 预览模式 — 不会执行任何修改
=== Agent Config Sync v1.2 — 初始化 ===
Master 工作空间: /home/admin/.openclaw/workspace-amaster
ℹ️  版本文件已存在，跳过创建
ℹ️  acode/SYNC.md 已是最新，跳过
ℹ️  acode/BOOTSTRAP.md 已有同步检查
ℹ️  acode/HEARTBEAT.md 已有同步检查
✅ Agent 'acode' 已配置
ℹ️  ainvest/SYNC.md 已是最新，跳过
ℹ️  ainvest/BOOTSTRAP.md 已有同步检查
ℹ️  ainvest/HEARTBEAT.md 已有同步检查
✅ Agent 'ainvest' 已配置
ℹ️  alive/SYNC.md 已是最新，跳过
ℹ️  alive/BOOTSTRAP.md 已有同步检查
ℹ️  alive/HEARTBEAT.md 已有同步检查
✅ Agent 'alive' 已配置
=== 初始化完成 ===
```

✅ 全部通过，无错误。

### 下游文件验证（grep 确认）
| 文件 | pending_sync 引用数 | 仅 v1.2 格式 |
|------|:---:|:--:|
| acode/BOOTSTRAP.md | 1 | ✅ |
| ainvest/BOOTSTRAP.md | 1 | ✅ |
| alive/BOOTSTRAP.md | 1 | ✅ |
| acode/HEARTBEAT.md | 1 (含 marker) | ✅ |
| ainvest/HEARTBEAT.md | 1 (含 marker) | ✅ |
| alive/HEARTBEAT.md | 1 (含 marker) | ✅ |

---

## 未完成项 & 需确认

### 需 Leon 确认
1. **版本命名空间独立**: 量化系统 v3.2 与 sync 系统 v1.0 分开计数。当前 `.current_system_version` 和 `.last_sync_version` 都设为 `v1.0`。如果希望保留跨系统统一版本号，请告知。
2. **CHANGELOG_quant.md**: 原始量化系统完整履历已归档到此文件，新 `CHANGELOG.md` 为 sync 格式。确认此分离方式 OK？
3. **HEARTBEAT item 12 语义**: 新格式增加了 SHA256 签名、journal 记录、重试逻辑。AMaster 下次 heartbeat 时将按新格式执行。确认无误？

### 评估报告 G6 (agent-setup.md 过期)
- 该文件仍为 v1.1 格式内容，但 `init_sync.sh` 不实际使用它（仅人工参考）。
- 如需修复留待 Phase 4 处理。

### 评估报告建议 E1-E5 (v1.4)
- 未执行，留待后续迭代。
