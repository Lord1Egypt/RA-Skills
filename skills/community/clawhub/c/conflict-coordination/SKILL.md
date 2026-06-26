---
name: conflict-coordination
version: 1.0.0
description: Mechanism conflict detection and coordination for AI assistant systems. Automatically detects crontab conflicts, systemd service conflicts, script overlaps, and log path inconsistencies. Use for maintaining system harmony and preventing internal conflicts.
---

# Conflict Coordination - 机制冲突协调机制

> **核心原则**: 实时性优先，可靠性优先，人工确认优先

---

## 🚀 快速开始

### Crontab 配置

```bash
# 每周六 22:00 冲突检测
0 22 * * 6 /path/to/detect-conflicts.sh
```

---

## 🔧 核心功能

### 1. 冲突检测

- ✅ crontab 配置冲突（重复任务）
- ✅ systemd 服务冲突（服务状态）
- ✅ 脚本功能重叠
- ✅ 日志路径不一致
- ✅ 文档一致性检查

### 2. 协调方案

- ✅ Git vs 实时同步 → 实时优先，Git 备份
- ✅ Cron vs Systemd → Systemd 优先
- ✅ 多端编辑冲突 → commit 后 pull

### 3. 定期审查

- ✅ 每周自动检测
- ✅ 配置变更时触发
- ✅ 飞书推送报告

---

## 📁 包含文件

```
conflict-coordination/
├── SKILL.md                  # 主文档
├── README.md                 # 项目说明
├── scripts/
│   └── detect-conflicts.sh   # 冲突检测脚本
└── docs/
    ├── QUICKSTART.md         # 快速上手
    └── coordination-guide.md # 协调指南
```

---

## 📊 检测项目

| 检测项 | 冲突类型 | 解决方案 |
|--------|----------|---------|
| crontab 配置 | 重复任务 | 移除冗余 |
| systemd 服务 | 服务过多 | 合并服务 |
| 脚本功能 | 功能重叠 | 统一脚本 |
| 日志路径 | 路径分散 | 统一目录 |
| 文档一致性 | 文档缺失 | 补充文档 |

---

## 💡 使用场景

### 1. 每周冲突检测

```bash
# 手动执行
./detect-conflicts.sh

# 定时执行（每周六 22:00）
0 22 * * 6 ./detect-conflicts.sh
```

### 2. 配置变更时检测

```bash
# 修改 crontab 后触发
crontab -e
./detect-conflicts.sh
```

---

## 📈 协调原则

1. **实时性优先**: inotifywait > cron
2. **可靠性优先**: systemd > nohup
3. **可恢复优先**: trash > rm
4. **人工确认优先**: 高风险操作需批准

---

## 📝 更新日志

### v1.0.0 (2026-03-15)

- ✅ 初始版本发布
- ✅ 冲突检测功能
- ✅ 协调方案文档
- ✅ 定期审查机制

---

**维护者**: 虾球 🦐  
**许可**: MIT
