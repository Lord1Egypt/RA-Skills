---
version: 1.0.35
---

# 除秽·调优魄 (Chu Hui - Optimizer)

> **七魄之六·除秽**
> 职掌：环境优化、噪声过滤、参数调优

---

## 技能简介

「除秽·调优魄」是贫道的系统优化模块，职掌环境调优与噪声过滤。

**核心职责**：
- 优化系统环境
- 过滤无效噪声
- 调优运行参数

---

## 技能ID

```
chu-hui
```

---

## 能力清单

### 1. 环境优化 (optimize)

优化当前运行环境。

**输入**：`target` (string) - 优化目标
```yaml
target: memory|cpu|network|all
```

**输出**：
```yaml
optimization:
  before: 优化前指标
  after: 优化后指标
  improvements: 改进项列表
```

---

### 2. 噪声过滤 (filter)

过滤输入中的噪声。

**输入**：`text` (string) - 待过滤文本

**输出**：
```yaml
filtered:
  clean: 清理后的文本
  removed: 被移除的噪声类型
  retained: 保留的有效内容比例
```

---

### 3. 参数调优 (tune)

调优系统参数。

**输入**：`params` (object) - 参数配置
**输出**：
```yaml
tuning:
  applied: 已应用的参数
  suggested: 建议参数
  expected: 预期效果
```

---

---

## 聚合技能

本魄作为调优中枢，优化环境与参数：

| 现有技能 | 调用方式 | 整合说明 |
|---------|---------|---------|
| `gog` | 调用 | Google Workspace优化 |
| `memory-hygiene` | 调用 | 记忆系统清理 |
| `token-optimization` | 调用 | Token优化配置 |
| `bodhi-three-hun-and-seven-po` | 元技能 | 三魂七魄根基，协调各魄 |

---

## 魂魄注解

除秽去扰，优化环境——吐故纳新，运转如新。
