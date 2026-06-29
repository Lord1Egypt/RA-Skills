# 优化模式参考

本文档总结常见的 Agent 效率优化模式与案例。

---

## 模式 1：去重优化

### 问题描述

Agent 配置中存在重复或功能冗余的技能。

### 常见场景

| 重复类型 | 示例 | Token 浪费 |
|-----------|------|-------------|
| **完全重复** | `another_them` 出现 2 次 | ~500 tokens |
| **命名重复** | `another_them` + `another-them` | ~1000 tokens |
| **功能重复** | `online-search` + `multi-search-engine` | ~1500 tokens |

### 优化步骤

1. **检测重复**：
   ```python
   skills = agent.get("skills", [])
   duplicates = [s for s in skills if skills.count(s) > 1]
   ```

2. **移除重复**：保留第一个，移除后续重复项。

3. **验证功能**：确认移除后功能不受影响。

### 案例

**优化前（Stock 大作手）：**
```json
"skills": [
    "another_them",
    "another-them",  // 重复
    "online-search",
    "multi-search-engine",  // 功能重复
    ...
]
```

**优化后：**
```json
"skills": [
    "another_them",  // 只保留一个
    "online-search",    // 保留主要搜索技能
    ...
]
```

**节省：** ~1500 tokens

---

## 模式 2：去无关优化

### 问题描述

Agent 配置了与自身角色无关的技能，浪费 token。

### 常见场景

| Agent 角色 | 无关技能示例 | Token 浪费 |
|-------------|--------------|-------------|
| 股票分析 | `realestate-advisor`（房产技能） | ~800 tokens |
| 房产顾问 | `stock-analysis-team`（股票技能） | ~1000 tokens |
| 写作助手 | `wecom-weisheng-scrm`（企微 SCRM） | ~600 tokens |

### 优化步骤

1. **识别角色**：基于 `agent.name` 或 `agent.id` 判断角色。
2. **列出无关技能**：对比角色与技能描述。
3. **移除无关技能**。

### 案例

**优化前（置安居 Agent）：**
```json
"skills": [
    "realestate-advisor",  // 相关
    "stock-agent",          // 无关
    "a-share-short-term",  // 无关
    ...
]
```

**优化后：**
```json
"skills": [
    "realestate-advisor",
    "online-search",
    "weather-advisor",
    ...
]
```

**节省：** ~2000 tokens

---

## 模式 3：精简基础技能

### 问题描述

Agent 配置了过多基础配置技能（`qclaw-rules`、`qclaw-env` 等），实际只需 1-2 个。

### 常见场景

| 基础技能 | 必要性 | 建议 |
|----------|--------|------|
| `qclaw-rules` | 高 | 保留 |
| `qclaw-env` | 中 | 按需保留 |
| `qclaw-cron-skill` | 低 | 仅定时任务 Agent 保留 |
| `qclaw-text-file` | 中 | 按需保留 |

### 优化步骤

1. **评估必要性**：每个基础技能是否必须？
2. **保留核心**：只保留 1-2 个最相关的。
3. **移除其余**。

### 案例

**优化前（灵枢 Agent）：**
```json
"skills": [
    "qclaw-skill-creator",
    "qclaw-rules",
    "qclaw-env",
    "qclaw-cron-skill",
    "qclaw-text-file",  // 5 个基础技能
    ...
]
```

**优化后：**
```json
"skills": [
    "qclaw-skill-creator",
    "qclaw-rules",  // 只保留 2 个
    ...
]
```

**节省：** ~1500 tokens

---

## 模式 4：按需启用工具

### 问题描述

一次性工具（如 `qclaw-migration`）常驻技能列表，浪费 token。

### 常见场景

| 工具类型 | 示例 | 建议 |
|----------|------|------|
| **迁移工具** | `qclaw-migration` | 按需启用 |
| **测试工具** | `skill-vetter` | 开发时启用 |
| **诊断工具** | `openclaw-doctor` | 按需启用 |

### 优化步骤

1. **识别一次性工具**。
2. **从技能列表移除**。
3. **记录启用方法**：需要时通过 `config.patch` 临时添加。

### 案例

**优化前：**
```json
"skills": [
    ...,
    "qclaw-migration",  // 一次性工具
    ...
]
```

**优化后：**
```json
"skills": [
    ...,
    // 移除 qclaw-migration，需要时再添加
]
```

**节省：** ~500 tokens

---

## 模式 5：技能合并

### 问题描述

多个技能功能相似，可以合并为一个。

### 常见场景

| 当前技能 | 可合并为 | Token 节省 |
|----------|------------|-------------|
| `docx` + `pdf` + `xlsx` | `office-suite`（假设存在） | ~1000 tokens |
| `online-search` + `multi-search-engine` | `search-hub` | ~800 tokens |

### 优化步骤

1. **识别功能重叠的技能**。
2. **查找替代技能**（从 skillhub 搜索）。
3. **替换并验证**。

### 案例

（本例为假设性案例，实际需根据 skillhub 情况调整）

---

## 综合优化案例

### 案例：Stock 大作手（33 → 12 技能）

**优化前：**
- 技能数：33 个
- 预估 token：~25,000
- 效率评分：10/100

**问题与优化：**

| 问题 | 优化动作 | 节省 |
|------|----------|--------|
| 重复技能 | 移除 `another_them` / `another-them` | ~1000 |
| 无关技能 | 移除房产、写作类技能（~15 个） | ~12000 |
| 基础技能过多 | 只保留 `qclaw-text-file` | ~1000 |
| 一次性工具 | 移除 `qclaw-migration` | ~500 |

**优化后：**
- 技能数：12 个
- 预估 token：~8,000
- 效率评分：50/100
- **总节省：~68% token**

---

## 优化检查清单

执行优化时，按此清单检查：

- [ ] 移除完全重复的技能
- [ ] 移除命名重复的技能（如 `another_them` vs `another-them`）
- [ ] 移除与 Agent 角色无关的技能
- [ ] 精简基础配置技能（≤ 2 个）
- [ ] 将一次性工具改为按需启用
- [ ] 检查功能重叠的技能，考虑合并
- [ ] 验证优化后功能完整性
- [ ] 计算并确认 token 节省量

---

## 自动化建议

### 定期运行分析

```bash
# 每周一早上 9 点
0 9 * * 1 python3 scripts/analyze_agent_efficiency.py --config ~/.qclaw/openclaw.json --output metrics.json
```

### 自动推送建议

结合 `qclaw-cron-skill`，将优化建议推送到企微。

---

**最后更新：** 2026-05-29
