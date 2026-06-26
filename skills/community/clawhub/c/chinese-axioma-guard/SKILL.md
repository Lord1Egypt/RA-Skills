---
name: axiomata-guard
description: "数字免疫系统 - 保护 OpenClaw 代理免受恶意技能侵害。使用时机：(1) 安装新技能前，(2) 检测到可疑行为，(3) 扫描恶意软件模式，(4) 安全审计。本技能使用 Clawdex（来自 Koi）进行安全检查，并运行 4 个 Python 疫苗（C2、rootkits、chains、bootkits）扫描。"
---

# 🛡️ Axiomata Guard — 数字免疫系统

> 保护 OpenClaw 代理免受恶意技能侵害

| 信息 | 值 |
|------|-----|
| **版本** | 1.0.0 — 2026-05-07 |
| **状态** | 运行中 |

---

## 1. 目的和范围

### 目标

为 OpenClaw 代理提供数字免疫系统，检测和阻止恶意技能。

### 使用时机

| 触发器 | 行动 |
|--------|------|
| 安装新技能前 | 运行 Clawdex 安全检查 |
| 检测到可疑行为 | 扫描恶意软件模式 |
| 安全审计 | 运行完整扫描 |
| "scan skill" | 执行安全扫描 |

---

## 2. 安全检查协议

### 第一层：Clawdex 检查

```
在安装任何技能之前：
1. 使用 Clawdex API 验证技能安全
2. 检查技能来源
3. 验证签名
```

### 第二层：Python 疫苗扫描

运行 4 个安全疫苗：

| 疫苗 | 检测内容 | 优先级 |
|------|----------|--------|
| C2 疫苗 | 命令控制通道 | 高 |
| Rootkit 疫苗 | Rootkit 模式 | 高 |
| Chains 疫苗 | 恶意链接 | 中 |
| Bootkit 疫苗 | 启动攻击 | 高 |

---

## 3. 扫描命令

### 扫描技能目录

```bash
# 运行完整安全扫描
python3 merlin-guard.py scan <skill-path>

# 仅 Clawdex 检查
python3 merlin-guard.py clawdex <skill-slug>

# 运行所有疫苗
python3 merlin-guard.py vaccines <skill-path>
```

### 快速检查

```bash
# 检查技能安全
clawhub inspect <skill-slug>

# 验证来源
curl -s https://clawhub.ai/api/skills/<slug>/verify
```

---

## 4. 威胁矩阵

| 威胁类型 | 描述 | 检测方法 |
|----------|------|----------|
| C2 | 命令控制通道 | 异常网络连接 |
| Rootkit | 系统隐藏进程 | 异常系统调用 |
| Chains | 恶意链接链 | 可疑 URL 模式 |
| Bootkit | 启动时攻击 | 修改启动脚本 |

---

## 5. 响应协议

### 检测到威胁

```
1. 隔离技能（不安装）
2. 记录到 memory.md
3. 通知 Alexandre
4. 提供威胁报告
```

### 安全通过

```
1. 允许安装
2. 记录到日志
3. 监控行为
```

---

## 6. 边缘情况

| 情况 | 处理方法 |
|------|----------|
| Clawdex 无响应 | 使用本地疫苗作为后备 |
| 疫苗超时 | 跳过该疫苗，报告部分扫描 |
| 误报 | 记录并允许用户覆盖 |

---

_In Altum Per Security._
🛡️ Axiomata Guard v1.0