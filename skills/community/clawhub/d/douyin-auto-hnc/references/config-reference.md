# 编排器配置参数详解

## 配置位置

编排器常量定义在 `douyin_full_orchestrator.py` 顶部。所有路径通过 CONFIG.md 管理。

## 关键常量

```python
# 路径（从 CONFIG.md 读取，或硬编码覆盖）
AGENT_DB_PATH     = "{chatgroup_db}"
CREATOR_TOOLS_DIR = "{creator_tools}"
CREATOR_OUTPUT    = "{comments_output}"
UPLOADS_DIR       = "{uploads_dir}"

# 发布频率（见 references/publishing.md）
MIN_SCORE = 0
MAX_ITEMS = 1
MIN_PUBLISH_INTERVAL_H = 1
MAX_DAILY_PUBLISH = 3

# AI 优化（从 CONFIG.md 读取）
OPENCLAW_GATEWAY = "{openclaw_gateway}"
OPENCLAW_TOKEN   = "<从 openclaw.json 获取>"
OPENCLAW_MODEL   = "{openclaw_model}"
AI_OPTIMIZE_TIMEOUT = 30  # 秒

# 小红书（已禁用）
XHS_ENABLED = False
```

## 路径解析

编排器启动时从 CONFIG.md 解析路径。如果没有 CONFIG.md，会回退到脚本中的硬编码默认值。

推荐的修改方式：**在编排器顶部添加覆盖变量**，不直接改硬编码常量。

```python
# === 用户配置覆盖区 ===
# MAX_DAILY_PUBLISH = 5
# XHS_ENABLED = True
# AI_OPTIMIZE_ENABLED = False
```

## 状态字段

monitor_items 表中与发布相关的字段：

| 字段 | 含义 |
|------|------|
| `article_published` | 是否已发文章（0/1） |
| `imagetext_published` | 是否已发长图文（0/1） |
| `publish_status` | published / failed:xxx / NULL |
| `publish_time` | 发布时间（ISO 格式） |
| `transcript_status` | pending / processing / full |
| `rank_score` | 内容质量评分 |
