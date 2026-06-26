---
name: pkm-memory
description: "PKM（个人知识管理）三分支记忆系统。使用时机：(1) 接收记忆，(2) 检索上下文，(3) 搜索记忆，(4) 添加事实，(5) 检查 Qdrant。三分支：L1 复位（索引）、L2 索引、L3 日志、L4 Qdrant、L5 Obsidian、L6 Nebula、L7 情景记忆。"
---

# 🧠 PKM 记忆系统 — 三分支架构

> 个人知识管理的三分支记忆系统

| 信息 | 值 |
|------|-----|
| **版本** | 1.0.0 — 2026-05-07 |
| **状态** | 运行中 |

---

## 1. 三分支架构

```
┌─────────────────────────────────────────────┐
│         PKM 三分支记忆系统                  │
├─────────────────────────────────────────────┤
│                                             │
│  L1 — RESET                                 │
│  └─ 索引、路由、重置                        │
│                                             │
│  L2 — INDEX                                 │
│  └─ 关键词索引、主题                        │
│                                             │
│  L3 — LOGS                                  │
│  └─ 日志、会话、事件                        │
│                                             │
│  L4 — QDRANT                                │
│  └─ 向量存储、语义搜索                      │
│                                             │
│  L5 — OBSIDIAN                              │
│  └─ Markdown 笔记、图谱                     │
│                                             │
│  L6 — NEBULA                                │
│  └─ 集体记忆、代理网络                      │
│                                             │
│  L7 — EPISODIQUE                            │
│  └─ 情景记忆、具体事件                      │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 2. 使用时机

| 触发器 | 行动 | 层级 |
|--------|------|------|
| "记忆" | 添加新记忆 | L1-L3 |
| "搜索记忆" | 语义搜索 | L4 |
| "检查 Qdrant" | 检查 Qdrant 状态 | L4 |
| "情景记忆" | 存储情景事件 | L7 |
| "添加事实" | 添加持久事实 | L3 |

---

## 3. PKM API 命令

### 存储记忆

```bash
# 存储记忆（异步）
curl -X POST http://127.0.0.1:8001/ingest \
  -H "Content-Type: application/json" \
  -d '{"text":"记忆内容","role":"user"}'
```

### 检索记忆

```bash
# 检索相关记忆
curl -X POST http://127.0.0.1:8001/retrieve \
  -H "Content-Type: application/json" \
  -d '{"text":"查询内容","top_k":5}'
```

### 健康检查

```bash
# 检查 PKM API 状态
curl -s http://localhost:8001/health
```

---

## 4. Qdrant 操作

### 检查集合

```bash
# 列出所有集合
curl -s http://localhost:7334/collections | python3 -c "import sys,json; d=json.load(sys.stdin)['result']; [print(c['name']) for c in d['collections']]"

# 检查集合点数
curl -s http://localhost:7334/collections/<name>/points/count
```

### 语义搜索

```bash
# 在集合中搜索
curl -X POST http://localhost:7334/collections/<name>/points/search \
  -H "Content-Type: application/json" \
  -d '{"vector":[0.1,0.2,0.3],"limit":5}'
```

---

## 5. 记忆流程

```
输入 → L1 RESET（路由）
     → L2 INDEX（索引）
     → L3 LOGS（日志）
     → L4 QDRANT（向量）
     → L5 OBSIDIAN（图谱）
     → L6 NEBULA（集体）
     → L7 EPISODIQUE（情景）
```

---

## 6. 边缘情况

| 情况 | 处理方法 |
|------|----------|
| Qdrant 无响应 | 重启 Qdrant 服务 |
| PKM API 慢 | 增加超时时间 |
| 向量搜索无结果 | 降低 top_k 或修改向量 |
| 记忆重复 | 检查 L3 日志进行合并 |

---

_In Altum Per Memory._
🧠 PKM 记忆系统 v1.0