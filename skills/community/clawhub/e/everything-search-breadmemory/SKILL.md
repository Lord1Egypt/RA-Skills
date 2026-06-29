---
name: everything-search-breadmemory
description: 基于 Everything/es.exe 的本地文件搜索引擎 + 面包屑知识管理系统 + 艾宾浩斯复习引擎 + 拓扑甜甜圈知识关联。
author: wUwproject
license: MIT
tags: ['search', 'filesystem', 'knowledge-management', 'ebbinghaus', 'everything']
trigger_negative: true
external_data_dir: true
sensitive_access: false
critical_write: false
permission_weight: LOW
data_dir: .standardization/everything-search-breadmemory/data/
version: 1.5.1
---
















# everything-search-breadmemory

本地文件搜索引擎（基于 Everything/es.exe），附带面包屑知识管理系统、艾宾浩斯遗忘曲线复习引擎、拓扑甜甜圈知识关联图谱。

## 适用场景

**触发条件（满足以下任意 3 条即触发）：**

- 在本地海量文件中快速搜索指定关键词/模式的文件
- 将搜索到的文件自动解析、归纳，提炼为知识条目
- 创建"面包屑小本"（breadcrumb notebook），长期积累知识碎片
- 基于艾宾浩斯遗忘曲线，每日自动轮询复习已有知识

**否定条件（以下场景不触发本技能）：**

- 需要实时联网搜索互联网（请用 web-search 等联网技能）
- 需要搜索 macOS/Linux 系统文件（本技能依赖 Everything，仅限 Windows）
- 需要语义理解搜索（本技能基于文件名关键词匹配，非语义搜索）
- 需要操作文件内容（本技能仅搜索文件路径，不读取/修改文件内容）

## 前置条件

技能首次使用时，会自动检测 Everything/es.exe 是否可用：
- **已安装**：直接使用
- **未安装**：引导下载 Everything 便携版，自动放置 es.exe 到技能目录

## 快速开始

```bash
# 1. 搜索本地文件
python {SKILL_DIR}/scripts/es_search.py search "关键词" --max 20

# 2. 添加知识条目
python {SKILL_DIR}/scripts/breadcrumb.py add --title "标题" --content "内容" --tags "标签"

# 3. 每日复习
python {SKILL_DIR}/scripts/ebbinghaus.py daily-review --count 5

# 4. 生成知识关联图谱
python {SKILL_DIR}/scripts/topology_donut.py generate
```

详情见下方各模块说明。

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

### 1. Everything 本地搜索

```bash
python {SKILL_DIR}/scripts/es_search.py search "<搜索关键词>" [--max 50] [--path "C:/限定路径"]
```

输出结构化 JSON，包含：文件路径、名称、大小、修改日期。

### 2. 面包屑小本（知识存储）

```bash
python {SKILL_DIR}/scripts/breadcrumb.py add --title "标题" --content "知识内容" --source "/path/to/file" [--tags "标签 1,标签 2"]
python {SKILL_DIR}/scripts/breadcrumb.py list [--tag "标签"] [--limit 20]
python {SKILL_DIR}/scripts/breadcrumb.py search "关键词"
python {SKILL_DIR}/scripts/breadcrumb.py delete --id <条目 ID>
python {SKILL_DIR}/scripts/breadcrumb.py show --id <条目 ID>
```

### 3. 艾宾浩斯复习引擎

```bash
python {SKILL_DIR}/scripts/ebbinghaus.py daily-review [--count 5]
python {SKILL_DIR}/scripts/ebbinghaus.py mark-reviewed --id <条目 ID>
python {SKILL_DIR}/scripts/ebbinghaus.py stats
```

**艾宾浩斯复习间隔**（天）：1, 2, 4, 7, 14, 30, 60, 120

每条知识记录自动追踪：`created_at`（首次创建）、`review_count`（已复习次数）、`last_reviewed_at`、`next_review_at`。

### 4. 拓扑甜甜圈关联引擎

自动发现面包屑间的逻辑关联，形成"甜甜圈"知识图谱。不强迫闭环，只创建有逻辑的关联。

```bash
python {SKILL_DIR}/scripts/topology_donut.py generate
python {SKILL_DIR}/scripts/topology_donut.py show-donut
python {SKILL_DIR}/scripts/topology_donut.py show-donut --id donut_001
python {SKILL_DIR}/scripts/topology_donut.py show-donut --entry-id <条目 ID>
python {SKILL_DIR}/scripts/topology_donut.py expand --id <条目 ID>
python {SKILL_DIR}/scripts/topology_donut.py stats
```

**5 种关联类型：** `tag_cluster`（标签聚类）、`content_bridge`（内容桥接）、`source_family`（同源家族）、`sequential_chain`（序贯链接）、`conceptual_hierarchy`（概念层级）

**4 种甜甜圈类型：** `closed`（闭合环路）、`nested`（嵌套结构）、`branching`（分支发散）、`chain`（线性链条）

### 5. 艾宾浩斯复习 + 拓扑扩展

```bash
python {SKILL_DIR}/scripts/ebbinghaus.py daily-review-expand [--count 5]
python {SKILL_DIR}/scripts/ebbinghaus.py daily-review --expand [--count 5]
python {SKILL_DIR}/scripts/ebbinghaus.py expand-topology --id <条目 ID>
```

## 工作流程

本技能完整执行流程见 [references/workflow.md](references/workflow.md)。

## 工作流程

完整执行流程见 [references/workflow.md](references/workflow.md)。

## 工作流程

| 主题 | 参考文件 |
|------|----------|
| 脚本详细用法 | [references/script-reference.md](references/script-reference.md) |
| Agent 行为规范 | [references/agent-behavior.md](references/agent-behavior.md) |
| 工作流程 | [references/workflow.md](references/workflow.md) |
| 数据存储结构 | [references/data-storage.md](references/data-storage.md) |
| 反模式收录 | [references/antipatterns.md](references/antipatterns.md) |
| 常见问题 | [references/faq.md](references/faq.md) |
| 权限说明 | [references/permissions.md](references/permissions.md) |

---

## 版本

当前版本：**1.5.0** — v1.5.0：skill-standardization 改造，补充否定条件、渐进式加载说明、反模式/FAQ 渐进式引用、修复写作规范、补充 permissions.md
