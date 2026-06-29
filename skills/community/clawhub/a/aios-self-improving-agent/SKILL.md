---
name: aios-self-improving-agent
description: 在 AIOS/OpenClaw 运行环境中记录当前 agent 的错误、纠正、经验、知识缺口和可复用改进。适用于命令失败、用户纠正回答、发现过时知识、外部工具/API 异常、同类问题反复出现、完成复杂任务后需要沉淀经验、或开始重要任务前需要回顾当前 agent workspace 内历史 learnings 的场景。若环境中有 QMD，优先使用 per-workspace QMD 索引检索和去重。该技能必须保持 per-agent 逻辑隔离，只在当前 agent workspace 内读写 `.learnings/`，不得默认写全局 workspace、其他 agent workspace、共享 skill 目录或管理面配置。
---

# AIOS 自改进 Agent

本技能用于把当前 agent 在任务中遇到的错误、纠正和可复用经验沉淀到当前 workspace 的 `.learnings/`。它面向 AIOS 的 per-agent 逻辑隔离模型：共享 skill 可以全局预装，但学习记录必须默认留在当前 agent 的 workspace 内。

## 边界规则

- 只在当前工作目录或当前 agent workspace 内读写 `.learnings/`。
- 不要使用 `~/.openclaw/workspace` 作为默认路径；AIOS 中 workspace 位于 `/var/aios/.openclaw/workspaces/<agentId>` 或等价运行路径。
- 不要读取、写入或汇总其他 agent 的 workspace，除非用户明确指定且当前运行环境允许。
- 不要把学习记录自动写入全局 `AGENTS.md`、`SOUL.md`、`TOOLS.md`、workspace template、`.openclaw/skills`、`openclaw.json` 或任何管理面配置。
- 不要调用 `openclaw agents add/delete`、`openclaw skills install/uninstall` 等拓扑或全局 skill 管理命令；这些变更必须走 `aios-management-web` 或人工管理流程。
- 不要记录密钥、token、私钥、完整环境变量、完整配置文件、完整源码文件或未经脱敏的命令输出。
- 只记录足够复现和预防问题的摘要、路径、错误片段和建议动作。
- 可以使用 QMD 提升 `.learnings/` 的搜索质量，但 QMD 只作为当前 workspace 的搜索缓存；不要把其他 agent workspace、全局 skill、workspace template 或管理面目录加入该技能的 QMD 索引。

## 初始化

第一次需要记录时，在当前 workspace 根目录创建 `.learnings/` 和三个日志文件。不要覆盖已有文件。

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n\n当前 agent 的纠正、洞察、知识缺口和最佳实践。\n\n**分类**: correction | insight | knowledge_gap | best_practice\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/ERRORS.md ] || printf "# Errors\n\n当前 agent 遇到的命令失败、工具异常和集成错误。\n\n---\n" > .learnings/ERRORS.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\n用户提出但当前能力或系统尚未稳定支持的能力请求。\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

如果当前目录不确定，先确认自己位于业务 agent 的 workspace 根目录。AIOS 中不要把仓库源码目录、全局 skill 目录或 `/var/aios/.openclaw` 根目录当成学习记录根目录。

## QMD 搜索优先

AIOS 环境通常内置 QMD。需要回顾、去重或查找相似经验时，优先为当前 `.learnings/` 使用独立的 per-workspace QMD index；不要使用可能混入其他 workspace 的默认 index。

初始化或刷新当前 `.learnings/` 搜索缓存：

```bash
workspace_root="$(pwd -P)"
qmd_index="aios-learnings-$(printf "%s" "$workspace_root" | sha256sum | awk '{print substr($1,1,12)}')"
if command -v qmd >/dev/null 2>&1 && [ -d .learnings ]; then
  qmd --index "$qmd_index" collection add "$workspace_root/.learnings" --name learnings --mask "**/*.md" >/dev/null 2>&1 || true
  qmd --index "$qmd_index" context add qmd://learnings "当前 agent workspace 的自改进学习记录、错误和能力请求" >/dev/null 2>&1 || true
  qmd --index "$qmd_index" update >/dev/null 2>&1 || true
fi
```

搜索选择：

- 精确找 ID、Pattern-Key、文件名或固定术语：优先 `qmd search`，必要时用 `rg` 兜底。
- 查找相似错误、相似纠正或语义相近经验：优先 `qmd query --json -n 10 --min-score 0.25 "查询词"`。
- 刚写入新条目后需要立刻搜索：先 `qmd --index "$qmd_index" update`。只有语义搜索质量明显不足且时间允许时，再运行 `qmd --index "$qmd_index" embed`。
- QMD 不可用、超时或索引不可信时，退回 `rg -n "关键词" .learnings` 或 `grep -R "关键词" .learnings`。

## 何时记录

| 场景 | 目标文件 |
| --- | --- |
| 命令、测试、构建或工具调用失败 | `.learnings/ERRORS.md` |
| 用户指出回答、假设或实现错误 | `.learnings/LEARNINGS.md`，分类 `correction` |
| 发现模型知识过时或项目事实不符合预期 | `.learnings/LEARNINGS.md`，分类 `knowledge_gap` |
| 找到可复用的更好做法 | `.learnings/LEARNINGS.md`，分类 `best_practice` |
| 用户要求当前系统没有的能力 | `.learnings/FEATURE_REQUESTS.md` |
| 同类问题再次出现 | 更新已有条目、增加关联和复现次数 |

在重大任务开始前，只搜索当前 workspace 的 `.learnings/`，不要跨 agent 汇总。优先用 QMD：

```bash
workspace_root="$(pwd -P)"
qmd_index="aios-learnings-$(printf "%s" "$workspace_root" | sha256sum | awk '{print substr($1,1,12)}')"
if command -v qmd >/dev/null 2>&1 && [ -d .learnings ]; then
  qmd --index "$qmd_index" update >/dev/null 2>&1 || true
  qmd --index "$qmd_index" search --json -n 10 "Area Tags Pattern-Key recent errors corrections"
else
  rg -n "Area|Tags|Pattern-Key|ERR-|LRN-|FEAT-" .learnings 2>/dev/null || grep -R "Area\\|Tags\\|Pattern-Key\\|ERR-\\|LRN-\\|FEAT-" .learnings 2>/dev/null || true
fi
```

## 记录格式

### 学习条目

追加到 `.learnings/LEARNINGS.md`：

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 时间
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config | ops

### Summary
一句话说明学到了什么。

### Details
说明当时的上下文、错误假设和正确做法。只写脱敏摘要。

### Suggested Action
后续如何避免或修复。

### Metadata
- Source: conversation | error | user_feedback | review
- Related Files: 相对路径或当前 workspace 内路径
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX
- Pattern-Key: 可选的稳定去重键
- Recurrence-Count: 1
- First-Seen: YYYY-MM-DD
- Last-Seen: YYYY-MM-DD

---
```

### 错误条目

追加到 `.learnings/ERRORS.md`：

````markdown
## [ERR-YYYYMMDD-XXX] command_or_tool

**Logged**: ISO-8601 时间
**Priority**: medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config | ops

### Summary
简要说明失败内容。

### Error
```text
脱敏后的关键错误片段。
```

### Context
- Command/operation: 执行了什么
- Input: 只写必要摘要
- Environment: 只写非敏感环境事实

### Suggested Fix
可行修复或下次排查顺序。

### Metadata
- Reproducible: yes | no | unknown
- Related Files: 相对路径或当前 workspace 内路径
- See Also: ERR-YYYYMMDD-XXX

---
````

### 能力请求条目

追加到 `.learnings/FEATURE_REQUESTS.md`：

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 时间
**Priority**: low | medium | high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config | ops

### Requested Capability
用户想完成什么。

### User Context
为什么需要它。

### Suggested Implementation
可以如何实现，是否需要平台管理能力。

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## ID 规则

ID 格式为 `TYPE-YYYYMMDD-XXX`：

- `LRN`：学习条目
- `ERR`：错误条目
- `FEAT`：能力请求
- `XXX`：当天递增三位编号；无法可靠计算时使用随机三位大写字母或数字

## 去重和回顾

记录前先搜索当前 workspace：

```bash
query="关键词"
workspace_root="$(pwd -P)"
qmd_index="aios-learnings-$(printf "%s" "$workspace_root" | sha256sum | awk '{print substr($1,1,12)}')"
if command -v qmd >/dev/null 2>&1 && [ -d .learnings ]; then
  qmd --index "$qmd_index" update >/dev/null 2>&1 || true
  qmd --index "$qmd_index" query --json -n 10 --min-score 0.25 "$query"
else
  rg -n "$query" .learnings 2>/dev/null || grep -R "$query" .learnings 2>/dev/null || true
fi
```

如果已有相关条目：

- 优先更新原条目的 `Last-Seen` 和 `Recurrence-Count`。
- 在新条目中添加 `See Also`。
- 反复出现且影响任务质量时，将优先级提升一级。

## Promotion 规则

将经验提升为更长期的工作指导时，必须区分“当前 agent workspace”和“平台共享内容”。

允许在当前 agent workspace 内、经用户明确同意后更新：

- `AGENTS.md`：当前 agent 的工作流、自动化规则和项目约定
- `TOOLS.md`：当前 agent 的工具使用注意事项
- `SOUL.md`：当前 agent 的行为偏好和协作风格

禁止自动更新：

- `/var/aios/workspace-templates`
- `/var/aios/.openclaw/skills`
- `/var/aios/.openclaw/openclaw.json`
- 其他 agent workspace
- 管理服务数据文件

需要跨 agent 共享的经验，应输出一段脱敏摘要，让管理员通过模板、全局 skill 或管理端流程评估后再发布。

## 状态更新

当问题已修复时，更新原条目：

```markdown
### Resolution
- **Resolved**: ISO-8601 时间
- **Commit/PR**: 提交、PR 或变更说明
- **Notes**: 做了什么，如何验证
```

状态可用值：

- `pending`
- `in_progress`
- `resolved`
- `wont_fix`
- `promoted`

## 安全检查

写入任何 `.learnings/` 文件前，检查：

- 内容是否只属于当前 agent workspace。
- 是否包含密钥、token、cookie、连接串、账号密码、私钥、完整环境变量或完整配置。
- 是否泄露其他 agent、其他用户或管理面的上下文。
- 是否把长日志压缩成了最小可用错误片段。
- 是否使用相对路径或当前 workspace 内路径，而不是无关宿主机路径。

若不确定是否敏感，先写“已脱敏摘要”，不要写原文。
