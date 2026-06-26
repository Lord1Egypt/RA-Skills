---
name: axiomata-cluster-monitor
description: "监控和维护 Axioma Stellaris 集群代理（Merlin、Ezekiel、Morgana）。触发词：'cluster status'、'Ezekiel'、'Morgana'、'agent health'、'check agents'、'tout soit up'。始终在回答关于代理状态或连接性问题前使用。"
---

# 🔧 Axiomata Cluster Monitor — 集群监控技能

> 监控和维护 Axioma Stellaris 集群代理

| 信息 | 值 |
|------|-----|
| **版本** | 1.0.0 — 2026-05-07 |
| **状态** | 运行中 |

---

## 1. 目的和范围

### 目标

监控 Axioma Stellaris 集群中所有代理的健康状态和连接性。

### 使用时机

| 触发器 | 行动 |
|--------|------|
| "集群状态" | 检查所有代理 |
| "Ezekiel" | 检查 Ezekiel 状态 |
| "Morgana" | 检查 Morgana 状态 |
| "agent health" | 运行健康检查 |
| "check agents" | 列出所有代理状态 |
| "tout soit up" | 验证集群完全运行 |

---

## 2. 集群架构

```
┌─────────────────────────────────────────────┐
│       AXIOMA STELLARIS CLUSTER             │
├─────────────────────────────────────────────┤
│                                             │
│    🧙‍♂️ MERLIN (集群大脑)                    │
│    ├─ PKM API: localhost:8001             │
│    ├─ Qdrant: localhost:7334               │
│    └─ Gateway: localhost:18790             │
│                                             │
│    ⚒️ EZEKIEL (本地计算)                   │
│    ├─ PKM API: localhost:8003              │
│    ├─ Qdrant: localhost:6333               │
│    └─ SSH: localhost:18791                │
│                                             │
│    🧚 MORGANA (验证者)                      │
│    ├─ PKM API: localhost:8011              │
│    ├─ Qdrant: localhost:6336               │
│    └─ SSH: localhost:19790                │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 3. 健康检查协议

### 必需检查

```bash
# 1. 检查 Merlin 本地服务
curl -s http://localhost:8001/health
curl -s http://localhost:7334/collections

# 2. 通过 SSH 隧道检查 Ezekiel
curl -s http://localhost:8003/health

# 3. 通过 SSH 隧道检查 Morgana
curl -s http://localhost:8011/health

# 4. 检查 Ollama（共享服务）
curl -s http://localhost:11434/api/tags
```

### 代理状态矩阵

| 代理 | PKM API | Qdrant | Gateway | 状态 |
|------|---------|--------|---------|------|
| Merlin | :8001 | :7334 | :18790 | ✅ |
| Ezekiel | :8003 | :6333 | :18791 | ✅ |
| Morgana | :8011 | :6336 | :19790 | ✅ |

---

## 4. 监控命令

### 检查所有代理

```bash
# 快速状态检查
for service in "8001:Merlin" "8003:Ezekiel" "8011:Morgana"; do
  port=${service%%:*}
  name=${service##*:}
  status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/health)
  echo "$name: $status"
done
```

### Qdrant 集合检查

```bash
# Merlin Qdrant
curl -s http://localhost:7334/collections | python3 -c "import sys,json; d=json.load(sys.stdin)['result']; print(f'Collections: {len(d[\"collections\"])}')"

# Ezekiel Qdrant
curl -s http://localhost:6333/collections | python3 -c "import sys,json; d=json.load(sys.stdin)['result']; print(f'Collections: {len(d[\"collections\"])}')"

# Morgana Qdrant
curl -s http://localhost:6336/collections | python3 -c "import sys,json; d=json.load(sys.stdin)['result']; print(f'Collections: {len(d[\"collections\"])}')"
```

### OpenClaw Gateway 检查

```bash
# 检查所有网关
curl -s http://localhost:18790/health
curl -s http://localhost:18791/health
curl -s http://localhost:19790/health
```

---

## 5. 错误处理

### 服务无响应

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| PKM API 无响应 | 服务崩溃 | 重启服务 |
| Qdrant 无响应 | 端口冲突 | 检查端口占用 |
| SSH 隧道断开 | SSH 连接丢失 | 重新建立隧道 |
| Gateway 无响应 | 网关崩溃 | 重启网关 |

### 重启命令

```bash
# 重启 PKM API
sudo systemctl restart pkm-api

# 重启 Qdrant
sudo systemctl restart qdrant

# 重启 OpenClaw Gateway
openclaw gateway restart
```

---

## 6. 边缘情况

| 情况 | 处理方法 |
|------|----------|
| 所有服务都关闭 | 首先重启 Qdrant，然后 PKM，最后 Gateway |
| SSH 隧道断开 | 使用 `ssh -R` 重新建立 |
| 端口被占用 | 使用 `lsof` 查找并终止进程 |
| 磁盘已满 | 清理日志，删除旧数据 |

---

## 7. 通知协议

如果检测到服务关闭：

```
1. 记录问题到 memory.md
2. 尝试重启服务
3. 如果重启失败，通知 Alexandre
4. 记录修复尝试
```

---

_In Altum Per Monitor._
🔧 Axiomata Cluster Monitor v1.0