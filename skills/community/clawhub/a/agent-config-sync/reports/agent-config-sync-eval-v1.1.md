# agent-config-sync v1.1 — 功能评估报告

**评估日期**: 2026-05-16
**评估人**: 大师 (acode)
**评估范围**: SKILL.md + references/ (5 files) + scripts/ (2 files)

---

## 1. 通用性评分: 2/5

### 问题清单

| 位置 | Hardcode 内容 | 影响 |
|------|-------------|------|
| `SKILL.md` description | `acode/ainvest/alive` | 新用户 Agent ID 不同，description 误导 |
| `SKILL.md` 场景 A/B | 大师/元宝/牛奶 | 中文名称 + 特定 agent，英文用户无法理解 |
| `.agent_registry` | `acode/ainvest/alive` + 大师/元宝/牛奶 | 注册表有定义但无说明如何修改 |
| `references/sync-setup.md` | 推送消息给大师/元宝/牛奶 | HEARTBEAT 模板硬编码中文 Agent 名 |
| `references/sync-setup.md` 伪代码 | `agent_ids` 不明确来源 | 未说明从哪读取 agent 列表 |
| `references/sync-setup.md` pending paths | `workspace-acode/ainvest/alive` | 路径写死 |
| `references/sync-journal.md` | 全部中文注释和描述 | 英文用户完全无法理解 |
| `references/pending-sync-template.md` | 混合中文 | 模板内容中文，非中文用户难用 |
| `scripts/init_sync.sh` | 中文输出 + 中文文件内容 | 脚本 echo 和生成文件全是中文 |
| `scripts/force_sync.sh` | 中文输出 | 错误消息全部中文 |

### 结论
新用户安装后需要修改 **至少 8 处** 才能适配自己的 Agent 体系。非中文用户完全无法使用（脚本输出、模板、journal 文档全部中文）。

---

## 2. 可扩展性评分: 2/5

### 增加第 5 个 Agent 需要改几处？

| 文件 | 修改内容 | 估计工作量 |
|------|---------|----------|
| `.agent_registry` | 添加新条目 | 1 行 |
| `SKILL.md` description | 追加 agent ID | 1 行 |
| `references/sync-setup.md` HEARTBEAT 模板 | "大师/元宝/牛奶" → "大师/元宝/牛奶/新Agent" | 1 行 |
| `references/sync-setup.md` pending paths | 追加路径 | 1 行 |
| `references/sync-setup.md` 伪代码 | 无改动（如果 agent_ids 是数组） | 0 行 |
| `SKILL.md` 场景 A/B | 追加新 Agent 名称 | 2 处 |
| `scripts/init_sync.sh` | 命令行参数多传一个 | 调用处 |
| **总计** | | **6-7 处修改** |

### 去掉牛奶需要改几处？

| 文件 | 修改内容 | 估计工作量 |
|------|---------|----------|
| `.agent_registry` | 删除 alive 条目 | 1 行 |
| `SKILL.md` description | 删除 alive | 1 行 |
| `references/sync-setup.md` HEARTBEAT 模板 | 去掉"牛奶" | 1 行 |
| `references/sync-setup.md` pending paths | 删除 alive 路径 | 1 行 |
| `SKILL.md` 场景 | 去掉牛奶引用 | 2-3 处 |
| **总计** | | **5-6 处修改** |

### 根本问题
Agent 列表**没有单一真实来源**——`.agent_registry` 存在但脚本和文档都不从中读取。每次增删 Agent 需要在 JSON + 多个 Markdown + Shell 脚本中同步修改。

---

## 3. 文档质量评分: 2/5

### 按文件评估

| 文件 | 语言 | 自包含性 | 问题 |
|------|------|---------|------|
| `SKILL.md` | 中英混合 | 部分自包含 | description 英文但正文场景全中文；无安装步骤；无变量自定义说明 |
| `references/sync-setup.md` | 全中文 | 需要理解整个体系 | 无英文；HEARTBEAT 模板绑定特定 Agent；伪代码不完整 |
| `references/pending-sync-template.md` | 中英混合 | 需要理解上下文 | 模板内容中文；无独立使用说明 |
| `references/sync-journal.md` | 全中文 | 需要理解两步提交 | 全中文；无英文版本 |
| `references/.agent_registry` | 英文 JSON | 部分自包含 | JSON 格式清晰但无注释说明字段含义 |

### 关键缺失
- ❌ 无英文 Quickstart
- ❌ 无「如何适配你的 Agent」指南
- ❌ 安装步骤散落在 SKILL.md 和 sync-setup.md 之间
- ❌ 无可配置变量表格（用户不知道改哪）

---

## 4. 跨平台兼容性: 3/5

### Shell 脚本分析

| 特性 | `init_sync.sh` | `force_sync.sh` | POSIX? |
|------|:---:|:---:|:---:|
| Shebang `#!/bin/bash` | ✅ | ✅ | ❌ Bash 非 POSIX |
| `shift` | ✅ | ❌ | ✅ POSIX |
| `[[ ... ]]` | ❌ 使用 `[ ]` | ❌ 使用 `[ ]` | ✅ POSIX |
| `${1:-default}` | ✅ | ✅ | ✅ POSIX |
| `$@` / `$*` | ✅ | ✅ | ✅ POSIX |
| `<< 'CHG'` heredoc | ✅ | ❌ | ✅ POSIX |
| `grep -qE` | ✅ | ✅ | ✅ POSIX |
| `sed` extended regex | ❌ 未使用 -E | ❌ 未使用 -E | ⚠️ 基础 sed 安全 |
| `$(date ...)` | ✅ | ✅ | ✅ POSIX |

### 路径问题
- `~/.openclaw/` 在所有文件中硬编码
- 无 `OPENCLAW_ROOT` 环境变量支持
- `basename "$agent_ws" | sed 's/workspace-//'` 假设 workspace 命名规则，不灵活

### 结论
脚本在 Bash 下可正常运行于 Linux/macOS。基础语法接近 POSIX，但 Shebang 是 bash。路径不可配置是最主要的可移植性问题。

---

## 5. 风险点

### 🔴 高优先级

1. **Agent 名称硬编码遍布全库**
   - 在任何地方增删 Agent 需要修改 5+ 个文件
   - 容易遗漏，导致部分 Agent 收到同步、部分收不到
   - `.agent_registry` 已定义但没人用——增加了维护负担

2. **init_sync.sh 会直接修改 Agent 的 BOOTSTRAP.md / HEARTBEAT.md**
   - Agent 可能有自定义内容，脚本无备份直接追加
   - 无 dry-run 模式预览副作用
   - 追加的中文内容对非中文 Agent 无意义

3. **版本哨兵文件依赖特定路径 `memory/`**
   - 没有配置入口
   - 如果 AMaster 的 memory 在别处，整个机制失效

### 🟡 中优先级

4. **sync-journal.md 全中文**：日志格式清晰但操作文档不可读
5. **force_sync.sh 覆盖 .current_system_version 后备份不完整**：只备份了 sentinel 文件，没备份 CHANGELOG
6. **无回滚机制**：force_sync 可以创建 mismatch 但无法撤销

### 🟢 低优先级

7. **init_sync.sh SYNC.md 模板比较逻辑**：用 `sed` 剥离空白比较，跨平台可能有 `sed` 行为差异
8. **无 `--help` 参数**：两个脚本都没有 `-h`/`--help`

---

## 总体评分

| 维度 | 评分 | 加权 | 备注 |
|------|:---:|:---:|------|
| 通用性 | 2/5 | 30% | 绑定特定 Agent 体系，中文用户限定 |
| 可扩展性 | 2/5 | 25% | 增删 Agent 需改多处，无单一真实来源 |
| 文档质量 | 2/5 | 20% | 无英文快速入门，安装步骤分散 |
| 跨平台兼容性 | 3/5 | 15% | Bash 可运行但路径硬编码 |
| 代码健壮性 | 3/5 | 10% | 基本错误处理，无 dry-run，无回滚 |
| **综合** | **2.25/5** | | 功能可用但通用性严重不足 |

---

## 优化建议摘要

1. 将 `.agent_registry` 设为单一真实来源，所有脚本和模板从它读取
2. SKILL.md 增加变量配置表，用户只需改一处
3. 新建 `references/quickstart.md`（全英文）作为新用户入口
4. 脚本双语化：支持 `--lang en`，默认中文
5. `init_sync.sh` 增加 `--dry-run` 和 `--demo` 模式
6. SKILL.md 补全 Installation / Configuration / Daily Operations / Troubleshooting / Upgrading 章节
