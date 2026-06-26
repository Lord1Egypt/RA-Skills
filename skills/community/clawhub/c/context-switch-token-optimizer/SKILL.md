---
name: context-switch-token-optimizer
description: >-
  智能对话上下文切换与 Token 优化。分析对话主题连续性以管理上下文、在话题间切换并节省 Token。
  适用于多任务对话、项目工作流、学习研究等需管理上下文与 Token 使用的场景。
---

# Context Switch Token Optimizer

## 技能描述

通过关键词相似度、弱关联子串与时间衰减判断「连续 / 渐变漂移压缩 / 硬切换」，并可监控 Token、触发压缩与清理。实现见 `context_manager.py`、`token_optimizer.py`；详细算法见 [docs/TOPIC_AND_CONTINUITY.md](docs/TOPIC_AND_CONTINUITY.md)。

## 上下文动作（与代码一致）

| 动作 | 条件 | 行为 |
|------|------|------|
| `load_memory` | 无当前主题且无历史 | 建主题、可选加载 `memory/topic` 下记忆 |
| `continuous` | 与上一轮相似度 ≥ `similarity_threshold` | 追加历史，不压缩 |
| `drift_compress` | 相似度 ∈ [`continuity_threshold`, `similarity_threshold`) | 对话仍连续；压缩与当前弱相关的历史轮（`is_compressed`，保留短摘要） |
| `switch_context` | 相似度 < `continuity_threshold` | 硬切换，换记忆、增 `switch_count` |

相似度计算：`calculate_topic_similarity()`（关键词 Jaccard 式重叠 × 时间衰减 + 2 字子串/首字弱关联 + `continuity_bonus_for_partial`，弱关联封顶 `drift_similarity_cap`）。

## 持久化状态格式（`memory/context_switch_state.json`）

与 `ContextState` / `TopicSummary` 一致，主题历史项包含：

- `topic`, `keywords`, `timestamp`, `tokens_used`, `content_snippet`, **`is_compressed`**
- 顶层另有：`current_topic`, `memory_context`, `last_switch_time`, `switch_count`, `total_tokens`

## 配置文件（`config.json`）

所有键名与 `load_skill_config()` 默认值一致；用户 JSON 按**顶层块**与默认**合并**（同一块内键覆盖，未写的子键保留默认）。

### `context_switch`

| 键名 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `similarity_threshold` | number | 0.7 | ≥ 此值判为 `continuous` |
| `continuity_threshold` | number | 0.35 | < 此值判为硬切换 `switch_context` |
| `compress_relevance_threshold` | number | 0.3 | `drift_compress` 时，历史轮与当前相似度低于此则压缩该轮 |
| `continuity_bonus_for_partial` | number | 0.3 | 存在弱关联时的相似度加成 |
| `drift_similarity_cap` | number | 0.65 | 弱关联时相似度上限，便于进入 `drift_compress` |
| `time_decay_factor` | number | 0.95 | 按小时衰减的底数 |
| `max_topic_history` | int | 10 | 主题历史条数上限 |
| `memory_relevance_threshold` | number | 0.5 | 记忆文件匹配阈值 |
| `log_level` | string | （不设） | 可由环境变量 `CONTEXT_SWITCH_LOG_LEVEL` 写入 |

### `token_optimization`

| 键名 | 类型 | 默认 | 说明 |
|------|------|------|------|
| **`enabled`** | bool | true | 为 false 时不自动触发优化（对应环境变量 `TOKEN_OPTIMIZER_ENABLED`） |
| `token_limit` | int | 80000 | Token 预算 |
| `compression_threshold` | int | 56000 | 压缩参考阈值 |
| `context_cleanup_threshold` | number | 0.8 | 上下文清理参考 |
| `memory_load_limit` | int | 2000 | 记忆加载参考 |
| `optimization_interval` | int | 300 | 优化间隔（秒，预留） |
| `max_history_size` | int | 100 | Token 使用记录条数上限 |

### `memory_search`

| 键名 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `max_search_results` | int | 5 | 最多返回记忆条数 |
| `keyword_limit` | int | 5 | 每轮提取关键词数 |
| **`search_depth`** | int | 2 | 可由环境变量 `MEMORY_SEARCH_DEPTH` 覆盖（1–3） |
| `file_types` | string[] | `["*.md"]` | 记忆目录 glob |

### `optimization_settings`

| 键名 | 说明 |
|------|------|
| `auto_optimization` | 是否自动优化（策略预留） |
| `health_score_threshold` | 健康分阈值 |
| `suggestions_check_interval` | 建议检查间隔（秒） |

## 环境变量（与 `apply_environment_overrides()` 一致）

| 环境变量 | 映射配置键 | 取值与行为 |
|----------|------------|------------|
| **`CONTEXT_HISTORY_SIZE`** | `context_switch.max_topic_history` | 正整数，限制在 **1–100** |
| **`MEMORY_SEARCH_DEPTH`** | `memory_search.search_depth` | 正整数，限制在 **1–3** |
| **`TOKEN_OPTIMIZER_ENABLED`** | `token_optimization.enabled` | `true`/`1`/`yes`/`on` 为启用；`false`/`0`/`no`/`off` 为禁用（禁用后使用率 >70% 也不触发 `trigger_optimization`） |
| **`CONTEXT_SWITCH_LOG_LEVEL`** | `context_switch.log_level` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL`；设置根 logger 级别 |

未设置上述环境变量时，行为完全由 `config.json` 与代码默认决定。

## CLI 与入口

- 主入口：`python3 context-switch-token-optimizer.py [--config path] --process|--status|--reset|--test`
- 子模块：`context_manager.py`、`token_optimizer.py`（参数见 `--help`）

---

**维护**: Hermosa  
**版本**: v1.1  
**最后更新**: 2026-03-17
