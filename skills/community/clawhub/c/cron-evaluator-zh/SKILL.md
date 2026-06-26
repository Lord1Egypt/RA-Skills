---
name: cron-evaluator-zh
description: |
  Cron 评估器 — 分析和评分 cron 任务，用于健康检查、资源使用、冲突检测和弹性改进。
  使用场景：(1) 审计 cron 任务，(2) 检测时间冲突，(3) 优化 cron 性能，(4) 规划 systemd 迁移。
triggers:
  - "cron 评估"
  - "cron 健康检查"
  - "时间冲突检测"
  - "cron 优化"
  - "systemd 迁移"
author: "Axioma Cluster"
date: "2026-05-17"
version: 1.0.0
tags:
  - cron
  - 评估
  - 系统管理
  - 性能
  - systemd
  - 调度
status: "active"
---

# Cron 评估器

从 4 个维度评估 cron 任务的健康状况：时间、资源、弹性、相关性。

## 4 个维度

| 维度 | 检查项 | 分数范围 |
|------|--------|----------|
| **时间** | 午夜冲突、频率、抖动 | 0-1 |
| **资源** | 重型命令 (torch, docker, ollama) | 0-1 |
| **弹性** | 日志、flock、超时、错误处理 | 0-1 |
| **相关性** | Cron vs systemd timer 推荐 | 0-1 |

## 使用方法

```bash
# 扫描所有 cron 任务
python3 cron_evaluator_v3.py --scan

# 健康检查
python3 cron_evaluator_v3.py --health

# 改进建议
python3 cron_evaluator_v3.py --suggest
```

## 健康阈值

| 分数 | 状态 |
|------|------|
| >80% | 🟢 健康 |
| 60-80% | 🟡 需要改进 |
| <60% | 🔴 危险 |

## 主要功能

### 时间冲突检测
```python
# 两个 cron 都在 00:00 → 建议添加抖动
if cron1['time'] == '0 0 * * *' and cron2['time'] == '0 0 * * *':
    suggest("添加抖动: sleep $((RANDOM % 60))")
```

### 资源签名
```python
重型命令 = ['torch', 'tensorflow', 'ollama', 'docker']
if any(h in command for h in 重型命令):
    score -= 0.3  # 资源消耗大
```

### 弹性验证
```python
检查项 = {
    '日志': '>> /var/log/...' in command or '2>' in command,
    'flock': 'flock' in command,
    '超时': 'timeout' in command,
    '错误处理': '||' in command
}
```

## 抖动实现

```bash
# 之前（冲突风险）
0 2 * * * /path/to/script.sh

# 之后（带抖动）
0 2 * * * sleep $((RANDOM % 60)) && /path/to/script.sh
```

## 文件结构

```
cron-evaluator/
├── SKILL.md              # 本文件
├── scripts/
│   ├── cron_evaluator.py      # v1 (基础)
│   ├── cron_evaluator_v2.py    # v2 (增强)
│   ├── cron_evaluator_v3.py    # v3 (带 KAN)
│   └── train_cron_kan.py       # KAN 训练脚本
├── data/
│   └── cron_training.json       # 训练数据集
└── models/
    └── cron_kan.pt             # 训练好的 KAN 模型
```

## KAN 模型

Cron KAN (16→32→16→8→4→3) 从调度和命令模式中提取 16 个特征来预测 cron 任务质量。