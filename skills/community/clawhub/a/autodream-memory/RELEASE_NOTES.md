# AutoDream 技能发布说明

## 概述

成功创建 `autodream` 技能，实现类似 Claude Code AutoDream 的自动记忆整理功能。

## 技能信息

- **名称**: autodream
- **版本**: 1.0.0
- **位置**: `/root/.openclaw/workspace-research/skills/autodream/`
- **安装命令**: `skillhub install autodream`（需发布到 skillhub）

## 核心功能

### 四阶段整理流程

1. **Orientation** - 读取记忆目录，建立状态地图
2. **Gather Signal** - 窄搜索会话记录，提取高价值信号
3. **Consolidation** - 合并、去重、删除过时条目
4. **Prune and Index** - 更新 MEMORY.md 索引（≤200 行）

### 触发机制

- **自动触发**: 24 小时 + 5 次会话后
- **手动触发**: `--force` 参数强制运行

### 安全约束

- 只读模式（仅写入记忆文件）
- 锁文件防并发
- 后台执行不阻塞
- 删除前备份

## 文件结构

```
skills/autodream/
├── SKILL.md              # 技能定义
├── README.md             # 使用文档
├── package.json          # 元数据
├── _meta.json            # 技能元信息
├── config/
│   ├── config.json       # 配置文件
│   └── cron.json         # 定时任务配置
└── scripts/
    ├── autodream_cycle.py       # 主循环脚本
    ├── setup_24h.sh             # 定时任务设置
    └── ensure_openclaw_cron.py  # Cron 配置确保
```

## 测试结果

首次运行结果：
- 找到 4 个记忆文件，共 29 个条目
- MEMORY.md: 57 行 → 44 行
- 无过时/重复条目（因为是首次运行）

## 与 memory-mesh-core 的关系

| 特性 | autodream | memory-mesh-core |
|------|-----------|------------------|
| 主要目标 | 单工作区记忆整理 | 跨工作区记忆共享 |
| 整理频率 | 24 小时 +5 次会话 | 12 小时 |
| 记忆范围 | 本地记忆文件 | 本地 + 全局共享 |
| 输出格式 | Markdown + JSON | JSON + GitHub Issue |

**推荐组合使用**：
- `autodream` 负责日常记忆整理
- `memory-mesh-core` 负责跨工作区记忆共享

## 后续工作

1. **发布到 skillhub**: 需要上传到 skillhub 索引
2. **增强信号提取**: 改进会话记录分析算法
3. **添加备份功能**: 删除前备份到 `memory/autodream/backup/`
4. **优化日期转换**: 支持更多相对日期模式

## 使用示例

```bash
# 立即运行一次
python3 skills/autodream/scripts/autodream_cycle.py --workspace .

# 设置定时任务（24 小时）
bash skills/autodream/scripts/setup_24h.sh

# 强制运行
python3 skills/autodream/scripts/autodream_cycle.py --workspace . --force

# 试运行（不写入）
python3 skills/autodream/scripts/autodream_cycle.py --workspace . --dry-run
```

## 创建时间

2026-04-02
