# Adapters — 各 Lane 适配器规格

**版本**: v0.1  
**状态**: Design Draft

---

## 概述

Adapter 层负责将统一的四角色流程适配到不同对象类型：

```
┌─────────────────────────────────────────────────────────────┐
│              Auto-Improvement Orchestrator                  │
│         (Proposer → Critic → Executor → Gate)               │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Skill Adapter │   │ Macro Adapter │   │ Browser Adapter│
└───────────────┘   └───────────────┘   └───────────────┘
        ↓                     ↓                     ↓
   skill files          macro config         browser workflow
```

---

## Lane 定义

| Lane | 对象 | 典型文件 | 评估方式 |
|------|------|---------|---------|
| `generic-skill` | OpenClaw skill | SKILL.md, scripts/ | skill-evaluator |
| `skill-evaluator` | skill-evaluator 自身 | SKILL.md, tests/ | frozen benchmark |
| `macro` | macro/ainews 配置 | config.yaml, rules/ | 推送准确率 |
| `browser-workflow` | browser ops | selectors.json, flows/ | 抓取成功率 |

---

## Skill Adapter

### 目标对象
- `~/.openclaw/skills/<skill-name>/`
- `~/.openclaw/workspace/skills/<skill-name>/`

### Phase 1 minimal integration（已实现）

当前 `generic-skill` lane 的 Critic 已接入轻量级 evaluator evidence adapter：
- 引用 `skill-evaluator` 的 rubric weights / category mapping / level boundary
- 输出 `evaluator_evidence`、`score_components`、`evaluator_score`
- **未**真正执行 promptfoo / frozen benchmark / hidden tests / external regression

属于 **rubric-assisted judge**，不是 full evaluator runtime。

### Full Adapter 规格（Phase 2 规划）

详见 `references/skill-evaluator-adapter.md`，包含：
- frozen benchmark 执行规格
- hidden tests 执行规格
- external regression callback
- human spot-check interface

### 修改方式
- SKILL.md: `read/edit/write`
- scripts/: git-based patch

### 回滚方式
```bash
git checkout <commit> -- skills/<skill-name>/
```

---

## Macro Adapter

### 目标对象
- `~/.openclaw/skills/news-aggregator-skill/`
- `~/.openclaw/skills/x-hot-topics-daily/`

### 评估方法
```python
class MacroAdapter:
    def check_push_accuracy(self, config_path):
        # 对比推送内容与实际热点
        pass
    
    def check_source_health(self, config_path):
        # 检查数据源可用性
        pass
```

### 修改方式
- config.yaml: `read/edit/write`（结构化文件禁止 heredoc）
- rules/: 原子替换

### 回滚方式
```bash
git checkout <commit> -- skills/news-aggregator-skill/
```

---

## Browser Adapter

### 目标对象
- browser workflow 配置
- selector 文件
- 反爬策略配置

### 评估方法
```python
class BrowserAdapter:
    def check_selector_health(self, selector_path):
        # 测试 selector 是否仍然有效
        pass
    
    def check_success_rate(self, workflow_path):
        # 统计抓取成功率
        pass
```

### 修改方式
- selectors.json: `read/edit/write`
- flows/: 版本化更新

### 回滚方式
```bash
git checkout <commit> -- browser/
```

---

## Adapter 接口规范

所有 Adapter 必须实现以下接口：

```python
class BaseAdapter:
    def validate(self, target_path) -> bool:
        """验证目标对象是否有效"""
        pass
    
    def evaluate(self, target_path) -> dict:
        """运行评估，返回评分和报告"""
        pass
    
    def apply_change(self, target_path, change_spec) -> dict:
        """应用修改，返回结果"""
        pass
    
    def rollback(self, target_path, checkpoint) -> bool:
        """回滚到指定 checkpoint"""
        pass
```

---

## Phase 实现计划

| Phase | Lane | 状态 |
|-------|------|------|
| Phase 1 | generic-skill | ✅ first runnable + rubric-assisted critic |
| Phase 2 | skill-evaluator | 🟡 full evaluator runtime 待接 |
| Phase 2 | macro | 📝 规划 |
| Phase 3 | browser-workflow | 📝 规划 |

---

## 注意事项

1. **不要硬编码路径**：Adapter 应支持配置化路径
2. **原子操作**：修改必须原子，避免中间状态
3. **可追溯**：所有修改必须记录 diff
4. **可回滚**：必须支持 rollback
