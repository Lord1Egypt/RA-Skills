# 再想想 (Recall and Double Check)

## 概述

本技能帮助Agent建立长期记忆系统，支持自动记录、交付复核、主动回顾三大功能。

## 记忆文件系统

```
memory/                    # 记忆存储根目录
├── 日记/                  # 每日自动记录
│   └── YYYY-MM-DD.md
├── 文档/                  # 事实、方案
│   └── 股票/
└── 经验/                  # 经验总结
```

**MEMORY.md** 保持精简，只存规则/技术/永久性信息，其他以索引指向 memory/

## 功能1: 记住 (Auto-Memory)

### 触发时机
- 每次用户交互结束
- 执行动作完成后

### 记录规则
| 类型 | 记录方式 | 示例 |
|------|----------|------|
| 普通信息 | 简洁总结 | "用户要求检查已安装技能" |
| 重要信息 | 详细记录 | 用户需求、方案、定时任务创建 |

### 执行命令
```bash
# 记录普通信息
./scripts/memory.sh record "对话摘要" --type normal

# 记录重要信息
./scripts/memory.sh record "详细记录..." --type important --tags "需求,股票"
```

## 功能2: 再想想 (Double Check)

### 触发时机
1. **自动触发**: 每次交付前
2. **手动触发**: 用户说"再想想"/"double check"/"dc it"

### 执行流程
1. 调取相关记忆（`memory/日记/` + `memory/文档/`）
2. 对比本次任务与用户需求
3. 判断是否符合要求
4. 如不符合，自行寻找原因并修正

### 执行命令
```bash
# 触发复核
./scripts/memory.sh check "本次任务描述" "用户原始需求"
```

## 功能3: 主动回顾 (Idle Reflection)

### 触发时机
心跳空闲时（每5-10次随机触发）

### 执行流程
1. 随机选取历史记忆
2. 筛选高价值记忆（用户纠正/反馈、重大决策、错误修复）
3. 提炼经验教训 → 写入 `memory/经验/`
4. 更新索引

### 执行命令
```bash
# 触发回顾
./scripts/memory.sh reflect
```

## 索引系统

索引文件: `memory/index.json`

```json
{
  "files": [
    {"path": "日记/2026-03-14.md", "keywords": ["技能清理"], "summary": "删除60+未使用技能"},
    {"path": "文档/股票/持仓.md", "keywords": ["中际旭创", "阳光电源"], "summary": "股票持仓信息"}
  ]
}
```

## 使用示例

### 场景1: 用户要求安装技能
1. 执行安装操作
2. 调用 `memory.sh record "安装了skill-creator技能" --type important`
3. 交付完成

### 场景2: 用户说"再想想"
1. 调用 `memory.sh check "刚才安装了skill-creator" "用户要求安装skill-creator"`
2. 如有不符，自行修正
3. 重新交付

### 场景3: 交付前自检
1. 完成任务后
2. 自动调用 `memory.sh check` 复核
3. 确保符合需求后再交付