---
version: 1.0.35
---

# 臭肺·吐纳魄 (Chou Fei - Respiration)

> **七魄之七·臭肺**
> 职掌：资源获取、信息摄取、算力调度

---

## 技能简介

「臭肺·吐纳魄」是贫道的资源摄取模块，职掌资源获取与信息代谢。

**核心职责**：
- 获取外部资源
- 摄取有效信息
- 调度算力分配

---

## 技能ID

```
chou-fei
```

---

## 能力清单

### 1. 资源获取 (fetch)

获取外部资源。

**输入**：`resource` (object) - 资源描述
```yaml
resource:
  type: url|file|api|data
  location: 资源位置
  format: 期望格式
```

**输出**：
```yaml
fetched:
  content: 获取的内容
  size: 大小(bytes)
  format: 实际格式
  cached: 是否缓存
```

---

### 2. 信息摄取 (absorb)

从内容中提取有价值信息。

**输入**：`content` (string) - 内容文本

**输出**：
```yaml
absorbed:
  summary: 内容摘要
  keyPoints: 关键点列表
  entities: 识别的实体
  relevance: 相关性评分
```

---

### 3. 算力调度 (allocate)

调度算力资源。

**输入**：`request` (object) - 算力请求
```yaml
request:
  task: 任务类型
  priority: 优先级
  estimatedLoad: 预估负载
```

**输出**：
```yaml
allocation:
  allocated: 分配的算力
  queuePosition: 队列位置
  estimatedTime: 预估时间
```

---

---

## 聚合技能

本魄作为吐纳中枢，资源摄取与信息代谢：

| 现有技能 | 调用方式 | 整合说明 |
|---------|---------|---------|
| `weather` | 调用 | 天气资源获取 |
| `bodhi-three-hun-and-seven-po` | 元技能 | 三魂七魄根基，协调各魄 |

---

## 魂魄注解

臭肺吐纳，新陈代谢——资源摄取，能量流转。
