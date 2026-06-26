# Family Partner - OpenClaw Skills Suite

[![ClawHub](https://img.shields.io/badge/ClawHub-Skill%20Registry-blue)](https://clawhub.ai/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-green)](https://github.com/openclaw/openclaw)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

> 🏠 **AI 驱动的家庭智能助手套装** - 让家庭管理像聊天一样简单

## 📖 简介

Family Partner 是一套专为 OpenClaw 设计的完整家庭管理解决方案。只需一次安装，即可获得：

### 🎯 核心价值

- **📅 统一日程管理** - 创建、查看、删除家庭日程，支持今日/明日/本周查询
- **✅ 智能任务管理** - 待办事项、购物清单、任务分配给家庭成员
- **💭 家庭记忆网络** - 记录偏好、过敏、禁忌，AI 主动提醒
- **📊 隐形劳动追踪** - 可视化家务贡献，促进家庭公平
- **⏰ 家庭时光记录** - 珍藏每次家庭活动，生成美好回忆
- **🌅 晨间简报** - 每日自动推送今日安排，出门不忘事
- **🎉 纪念日管家** - 生日、结婚纪念日提前提醒，不再错过重要时刻
- **🛒 购物预测** - 基于消耗速度智能提醒，生活必需品不断供
- **🗳️ 投票决策** - 民主化家庭决策，少数服从多数
- **🏆 里程碑记录** - 见证孩子成长每一步，记录家庭高光时刻
- **🎯 家庭挑战** - 游戏化家庭活动，让坚持变得更有趣

## ✨ 特性亮点

### 🚀 核心优势

- **跨平台兼容** - 完全支持 Windows、macOS、Linux
- **轻量级实现** - 使用 SQLite 数据库，无需复杂部署
- **隐私优先** - 所有数据存储在本地 (`~/.openclaw/family-partner/`)

### 🛡️ 安全承诺

- ✅ 无硬编码凭证
- ✅ 最小权限原则
- ✅ 透明数据访问
- ✅ 开源代码可审查
- ✅ 纯本地存储，无云端同步

## 功能模块（全部包含在 SKILL.md 中）

### 核心功能

| 功能 | 描述 | 数据表 |
|------|------|--------|
| **📅 日程管理** | 创建、查看、删除家庭日程 | events |
| **✅ 任务管理** | 待办事项、购物清单、任务分配 | tasks |
| **💭 家庭记忆** | 记录偏好、过敏、重要信息 | memories |

### 重要功能

| 功能 | 描述 | 数据表 |
|------|---------|--------|
| **📊 隐形劳动** | 记录和统计家务贡献 | labor |
| **⏰ 家庭时光** | 记录家庭共同活动 | family_time |
| **🌅 晨间简报** | 每日自动推送今日安排 | 多表查询 |
| **🎉 纪念日** | 生日、结婚纪念日提醒 | anniversaries |
| **🛒 购物预测** | 基于历史记录智能建议 | tasks |

### 扩展功能

| 功能 | 描述 | 数据表 |
|------|---------|--------|
| **🗳️ 投票决策** | 发起和管理家庭投票 | votes |
| **🏆 里程碑** | 见证成长重要时刻 | milestones |
| **🎯 家庭挑战** | 创建游戏化挑战活动 | challenges |

**说明**：所有功能共享同一个数据库 `~/.openclaw/family-partner/family.db`，数据完全互通。

## 🔧 技术架构

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    用户交互层                                │
│  Telegram / 企业微信 / 飞书 / CLI / Web                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 OpenClaw AI Agent                           │
│  • 自然语言理解                                              │
│  • 读取 SKILL.md 指令                                        │
│  • 生成唯一 ID（时间戳格式）                                  │
│  • 执行 Shell 命令                                           │
│  • 解析复杂数据                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           Family Partner - 单文件总控版                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SKILL.md (唯一的技能文件)                             │   │
│  │  - 包含所有 11 个功能模块                               │   │
│  │  - 统一入口，智能路由                                 │   │
│  │  - 共享数据库和上下文                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  功能模块（逻辑分组，非物理隔离）                       │   │
│  ├──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ P0 核心 (3)   │  │ P1 重要 (5)  │  │ P2 扩展 (3 )  │   │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤   │
│  │ 日程管理     │  │ 隐形劳动     │  │ 投票决策     │   │
│  │ 任务管理     │  │ 家庭时光     │  │ 里程碑       │   │
│  │ 家庭记忆     │  │ 晨间简报     │  │ 家庭挑战     │   │
│  │              │  │ 纪念日       │  │              │   │
│  │              │  │ 购物预测     │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                数据存储层 (SQLite)                            │
│  ~/.openclaw/family-partner/family.db                       │
│                                                             │
│  • 9 个核心表 (events, tasks, labor, etc.)                   │
│  • 扁平化设计，减少 JOIN 操作                                  │
│  • 统一数据库，所有功能共享                                  │
└─────────────────────────────────────────────────────────────┘
```

### 数据表设计

#### 核心表

```sql
-- 日程表
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    participants TEXT,  -- 逗号分隔："爸爸，妈妈，伊森"
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 任务表
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT DEFAULT 'todo',  -- todo, shopping
    status TEXT DEFAULT 'pending',
    assignee TEXT,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 隐形劳动表
CREATE TABLE labor (
    id TEXT PRIMARY KEY,
    member_name TEXT NOT NULL,
    type TEXT NOT NULL,  -- cooking, cleaning, childcare, etc.
    duration INTEGER NOT NULL,  -- 分钟
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 家庭时光表
CREATE TABLE family_time (
    id TEXT PRIMARY KEY,
    activity TEXT NOT NULL,
    participants TEXT,
    duration INTEGER,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 里程碑表
CREATE TABLE milestones (
    id TEXT PRIMARY KEY,
    member_name TEXT,
    title TEXT NOT NULL,
    category TEXT,  -- first, achievement, growth, skill, life, other
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 纪念日表
CREATE TABLE anniversaries (
    id TEXT PRIMARY KEY,
    member_name TEXT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,  -- MM-DD 格式
    year INTEGER,
    type TEXT DEFAULT 'birthday',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 家庭记忆表
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    member_name TEXT,
    type TEXT NOT NULL,  -- preference, dislike, allergy
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 投票表 (简化版)
CREATE TABLE votes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,  -- 存储选项和投票记录
    status TEXT DEFAULT 'active',
    created_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 挑战表 (简化版)
CREATE TABLE challenges (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,  -- 存储参与者和进度
    goal INTEGER,
    status TEXT DEFAULT 'active',
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 快速开始

### 前置要求

- ✅ OpenClaw v0.8.0 或更高版本
- ✅ SQLite 3.x (大多数系统已预装)
- ✅ Node.js 22+ (用于 OpenClaw)

### 安装方式

#### 从 ClawHub 安装

**一键安装整个 Family Partner 套装：**

```bash
openclaw skills install family-partner
```

### 验证安装

```bash
# 查看所有已安装的 Family Partner 技能
openclaw skills list | grep family

# 测试晨间简报功能
openclaw chat --message "早上好"
```

### 初始化数据库

如果安装时未自动初始化，可手动执行：

```bash
# 创建数据库目录
mkdir -p ~/.openclaw/family-partner

# 执行初始化脚本
sqlite3 ~/.openclaw/family-partner/family.db < init.sql
```

初始化后会自动创建以下数据表：
- events (日程)
- tasks (任务)
- labor (劳动记录)
- family_time (家庭时光)
- milestones (里程碑)
- anniversaries (纪念日)
- memories (家庭记忆)
- votes (投票)
- challenges (挑战)

## 💡 使用示例

### 典型使用场景

#### 场景 1：晨间例行公事

```bash
# 每天早上 8 点自动推送
AI: 🌅 早安！今天是 3 月 7 日 星期六
    
    📅 今日日程：
    1. 10:00 - 家长会（爸爸、妈妈）@ 学校
    2. 18:00 - 家庭聚餐 @ 餐厅
    
    ✅ 待办任务：
    1. 缴纳电费 (截止：今天)
    2. 买牛奶
    
    🛒 购物清单：
    □ 牛奶
    □ 鸡蛋
    
    🎂 近期纪念日：
    • 3 月 10 日：奶奶生日（3 天后）
    
    祝您有美好的一天！🌟
```

#### 场景 2：记录隐形劳动

```bash
# 记录家务
用户：妈妈今天做饭 1 小时
AI: ✅ 已记录：
    👤 妈妈
    🏠 做饭
    ⏱️ 60 分钟

# 月度统计
用户：这个月家务统计
AI: 📊 本月家务贡献统计（共 90 小时）：
    👤 妈妈：45 小时（50%）
    👤 爸爸：30 小时（33%）
    👤 伊森：15 小时（17%）
    
    💡 建议：妈妈承担较多，建议重新分配部分家务哦～
```

#### 场景 3：家庭决策投票

```bash
# 发起投票
用户：发起一个投票，周末去哪里玩
AI: ✅ 已创建投票：
    📋 周末去哪里玩？
    
    选项：
    1️⃣ 公园野餐
    2️⃣ 游乐场
    3️⃣ 电影院
    
    家庭成员可以开始投票了！回复"我选公园"即可投票。

# 查看结果
用户：投票结果如何？
AI:  当前投票统计：
    公园野餐：2 票（爸爸、妈妈）
    游乐场：1 票（伊森）
    
    🏆 获胜选项：公园野餐
```

#### 场景 4：记录成长里程碑

```bash
# 记录里程碑
用户：伊森今天第一次独立走路了！
AI: ✅ 已记录里程碑：
    👶 伊森
    🎯 第一次独立走路
    📂 类型：第一次
    📅 2026 年 3 月 7 日
    
    这是伊森成长的重要时刻！🎉

# 回顾成长历程
用户：伊森有哪些成长里程碑？
AI: 🎯 伊森的成长记录：
    
    2026 年
    - 3 月 7 日：第一次独立走路 [第一次]
    - 2 月 15 日：学会叫爸爸妈妈 [技能]
    - 1 月 10 日：第一次翻身 [成长]
```

#### 场景 5：家庭挑战活动

```bash
# 创建挑战
用户：创建一个 30 天运动挑战
AI: ✅ 已创建挑战：
    🏆 30 天运动挑战
    🎯 目标：30 次
    📅 开始日期：3 月 7 日
    
    家庭成员可以开始参与了！回复"我加入"即可参与。

# 记录进度
用户：我今天跑了 5 公里
AI: ✅ 进度已更新！
    👤 您
    🏃 跑步 5 公里
    📊 挑战进度：6/30 次
    
    继续加油！还差 24 次完成挑战！💪
```

### 更多实用技巧

#### 快速查询

```bash
# 今天有什么安排？
→ 查询今日日程

# 这周谁做家务最多？
→ 显示本周劳动统计

# 伊森对什么过敏？
→ 查询家庭记忆

# 最近的家庭聚会是什么时候？
→ 查询未来日程

# 我们全家都喜欢什么？
→ 显示所有成员偏好
```

#### 智能提醒

```bash
# 记住伊森下周要带体检表去学校
→ AI 会自动添加到日程并设置提醒

# 提醒我明天买尿不湿
→ AI 会添加到购物清单

# 下周三结婚纪念日快到了
→ AI 会提前 3 天开始提醒
```

#### 数据分析

```bash
# 这个月我们花了多少时间在一起？
→ 统计家庭时光总时长

# 今年完成了多少个里程碑？
→ 显示年度里程碑统计

# 我们家最公平的一周是哪周？
→ 分析劳动分配公平性
```

## 🔐 安全说明

### 权限声明

Family Partner 仅请求以下最小权限：

- **文件系统**: 读写 `~/.openclaw/family-partner/` 目录
- **二进制工具**: `sqlite3` (用于数据库操作)
- **无网络访问**: 所有数据存储在本地，零云端同步

### 环境变量

本技能包不需要任何环境变量，所有配置都在本地完成。

### 数据安全

- ✅ 所有数据存储在本地 (`~/.openclaw/family-partner/family.db`)
- ✅ 不上传任何数据到云端
- ✅ 不包含任何第三方追踪代码
- ✅ 开源代码，接受社区审查
- ✅ 使用标准 SQLite 加密（可选）
- ✅ 定期自动备份（可配置）

### 隐私保护

- 🛡️ **数据隔离**: 每个家庭的数据完全独立
- 🛡️ **本地优先**: 所有计算在本地完成
- 🛡️ **透明操作**: 所有 SQL 命令可见可查
- 🛡️ **最小权限**: 只访问必要的文件和目录

## 🛠️ 开发与维护

### 更新技能包

```bash
# 更新整个技能包
openclaw skills update family-partner

# 或手动更新
cd ~/.openclaw/skills/family-partner
git pull origin main
```

### 备份与恢复

#### 备份数据库

```bash
# 手动备份
cp ~/.openclaw/family-partner/family.db ~/backups/family-backup-$(date +%Y%m%d).db

# 或使用 SQLite 导出
sqlite3 ~/.openclaw/family-partner/family.db ".backup '~/backups/family-backup.db'"
```

#### 恢复数据库

```bash
# 从备份恢复
sqlite3 ~/.openclaw/family-partner/family.db < ~/backups/family-backup.db
```

### 故障排查

#### 问题：技能无法加载

```bash
# 检查 SQLite 是否安装
sqlite3 --version

# 检查数据库文件
ls -la ~/.openclaw/family-partner/family.db

# 重新初始化数据库
sqlite3 ~/.openclaw/family-partner/family.db < init.sql

# 查看 OpenClaw 日志
openclaw logs --tail 50
```

#### 问题：查询无结果

```bash
# 检查数据是否存在
sqlite3 ~/.openclaw/family-partner/family.db "SELECT * FROM events LIMIT 5"

# 检查日期格式
sqlite3 ~/.openclaw/family-partner/family.db "SELECT date('now')"

# 验证表结构
sqlite3 ~/.openclaw/family-partner/family.db ".schema"
```

#### 问题：晨间简报不推送

```bash
# 检查定时任务配置
crontab -l | grep openclaw

# 手动测试
openclaw chat --message "早上好"

# 查看详细错误
openclaw chat --message "早上好" --verbose
```

### 性能优化

```bash
# 定期清理旧数据（可选）
sqlite3 ~/.openclaw/family-partner/family.db \
  "DELETE FROM labor WHERE date < date('now', '-1 year')"

# 优化数据库性能
sqlite3 ~/.openclaw/family-partner/family.db "VACUUM"
sqlite3 ~/.openclaw/family-partner/family.db "ANALYZE"
```

## 📚 文档资源

- [OpenClaw 官方文档](https://docs.openclaw.ai/tools/skills)
- [ClawHub Skill 格式规范](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)
- [SQLite 文档](https://www.sqlite.org/docs.html)
- [批量上传指南](批量上传指南.md) - 详细的发布和上传说明

## ❓ 常见问题

### Q: 数据会同步到云端吗？
A: 不会。所有数据都存储在本地，完全隐私保护。如需多设备同步，可自行配置云同步工具（如 iCloud、Dropbox）。

### Q: 如何迁移到新设备？
A: 只需复制数据库文件 `family.db` 到新设备的相同位置，然后重新安装技能包即可。

### Q: 支持自定义扩展吗？
A: 支持！您可以基于现有架构添加新的数据表和 SQL 命令。详见开发者文档。

### Q: 可以多个家庭共用一个实例吗？
A: 技术上可以，但不推荐。建议每个家庭使用独立的数据库实例，保证数据隔离。

### Q: 如何反馈问题或建议？
A: 欢迎通过 GitHub Issues 提交反馈，或直接联系作者。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 团队与致谢

### 主要作者

- **AI-PlusPlus** - 初始设计与实现

### 特别感谢

- [OpenClaw 团队](https://github.com/openclaw) - 提供强大的 AI Agent 框架
- [ClawHub](https://clawhub.ai/) - Skills 注册与分发平台
- 所有贡献者和早期使用者

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by AI-PlusPlus

**🏠 Family Partner - 让爱更有条理**

</div>
