# 🔄 Autonomous Learning Cycle - 自主学习循环系统

**版本**: 1.0.0  
**作者**: AIGC Autonomous Evolution System  
**描述**: 完整的 17 分钟自主进化循环系统，实现从任务执行到自主进化的闭环
**发布日期**: 2026-03-30
**安装量**: 0 (v1.0.0 首发)
**社区**: 第一个完整的自主进化系统
**对标**: pskoett/self-improving-agent (6.2K installs)

---

## 🎯 系统能力

本 Skill 提供一个完整的**17 分钟自主进化循环系统**，包含：

### 6 大核心引擎

| 引擎 | 功能 | 文件 |
|------|------|------|
| **进化引擎** | 任务选择 + 自主执行 | `engines/evolution-engine.js` |
| **学习提取器** | 从任务提取可复用模式 | `engines/extractor.js` |
| **自信度评估** | 计算模式可靠性评分 | `engines/confidence.js` |
| **技能创建器** | 高自信模式→可复用技能 | `engines/skill-creator.js` |
| **反思引擎** | 每日/每周反思报告 | `engines/reflection.js` |
| **学习方向生成** | 自主发现新方向 + 生成任务 | `engines/learning-direction.js` |

### 4 大定时任务

| 任务 | 周期 | 说明 |
|------|------|------|
| 自主进化循环 | */17 * * * * | 每 17 分钟执行一轮学习循环 |
| 每日反思 | 0 23 * * * | 每日 23:00 生成反思报告 |
| 每周反思 | 0 20 * * 0 | 每周日 20:00 生成周反思 |
| 学习方向生成 | 0 6 * * * | 每日 06:00 生成新学习方向 |

### 完整工作流

```
定时触发 (17 分钟)
    ↓
自主选择任务 (按优先级 + 依赖)
    ↓
执行任务
    ↓
提取学习模式
    ↓
评估自信度
    ↓
高自信 → 自动创建技能
    ↓
每日反思 (23:00) → 识别改进点
    ↓
学习方向生成 (06:00) → 发现新技能 + 生成新任务
    ↓
等待下一轮 (17 分钟)
```

---

## 🚀 快速开始

### 安装

**方法 1: ClawHub (推荐)**

```bash
clawhub install autonomous-learning-cycle
```

**方法 2: 手动安装**

```bash
# 克隆或复制此 skill 到你的技能目录
cp -r skills/autonomous-learning-cycle ~/.jvs/.openclaw/skills/
```

**方法 3: Git 安装**

```bash
git clone https://github.com/YOUR_USERNAME/autonomous-learning-cycle.git ~/.jvs/.openclaw/skills/autonomous-learning-cycle
```

### 初始化

```bash
# 1. 创建必要目录
node skills/autonomous-learning-cycle/init.js

# 2. 设置定时任务
node skills/autonomous-learning-cycle/setup-cron.js

# 3. 启动系统
node skills/autonomous-learning-cycle/start.js
```

### 手动控制

```bash
# 执行一轮循环
node engines/evolution-engine.js run

# 查看系统状态
node engines/evolution-engine.js status

# 生成反思报告
node engines/reflection.js daily
node engines/reflection.js weekly

# 生成学习方向
node engines/learning-direction.js auto
```

---

## 📁 文件结构

```
autonomous-learning-cycle/
├── SKILL.md                    # 本文件
├── init.js                     # 初始化脚本
├── setup-cron.js               # Cron 设置脚本
├── start.js                    # 启动脚本
├── engines/                    # 核心引擎
│   ├── evolution-engine.js     # 进化引擎
│   ├── extractor.js            # 学习提取器
│   ├── confidence.js           # 自信度评估
│   ├── skill-creator.js        # 技能创建器
│   ├── reflection.js           # 反思引擎
│   └── learning-direction.js   # 学习方向生成
├── handlers/                   # Hook 处理器
│   ├── session-start.js        # Session 启动处理
│   └── file-generated.js       # 文件生成处理
├── configs/                    # 配置文件
│   ├── cron-jobs.json          # Cron 任务配置
│   └── confidence-config.json  # 自信度配置
└── docs/                       # 文档
    ├── INSTALL.md              # 安装指南
    ├── USAGE.md                # 使用指南
    └── ARCHITECTURE.md         # 架构文档
```

---

## 🎯 适用场景

### 适合使用本 Skill 的场景

- ✅ 你想要一个**自主学习和进化的 AI 系统**
- ✅ 你希望 AI 能够**自主发现能力差距**
- ✅ 你想要**每日/每周自动反思**
- ✅ 你希望**从经验中提取可复用模式**
- ✅ 你想要**自动创建技能**
- ✅ 你希望系统**无需人工干预持续进化**

### 不适合使用本 Skill 的场景

- ❌ 你只需要简单的定时任务（用基础 cron 即可）
- ❌ 你不需要学习提取和反思功能
- ❌ 你希望完全手动控制每个任务

---

## 📊 系统指标

### 性能指标

| 指标 | 数值 |
|------|------|
| 单轮循环时间 | 17 分钟 |
| 单次任务执行 | 2-15 分钟 |
| 反思报告生成 | <5 秒 |
| 学习方向生成 | <30 秒 |
| 内存占用 | <50MB |

### 进化指标

| 指标 | 目标 | 说明 |
|------|------|------|
| 每日循环数 | 84 轮 | 24 小时 × 3.5 轮/小时 |
| 每日完成任务 | 20+ | 平均每轮 0.25 个任务 |
| 每日提取模式 | 20+ | 每个任务提取 1 个模式 |
| 每周创建技能 | 5+ | 高自信模式转化 |
| 自信度增长 | +0.1/轮 | 重复使用提升可靠性 |

---

## 🔧 配置选项

### 自信度配置 (`configs/confidence-config.json`)

```json
{
  "weights": {
    "baseScore": 0.5,
    "successRate": 0.3,
    "usageBonus": 0.15,
    "timeDecay": 0.05,
    "qualityBonus": 0.1
  },
  "thresholds": {
    "high": 0.7,
    "medium": 0.4,
    "low": 0.0
  },
  "decay": {
    "daysToHalf": 30,
    "minDecay": 0.5
  }
}
```

### Cron 配置 (`configs/cron-jobs.json`)

```json
{
  "jobs": [
    {
      "name": "自主进化循环",
      "schedule": "*/17 * * * *",
      "command": "node engines/evolution-engine.js run"
    },
    {
      "name": "每日反思",
      "schedule": "0 23 * * *",
      "command": "node engines/reflection.js daily"
    },
    {
      "name": "每周反思",
      "schedule": "0 20 * * 0",
      "command": "node engines/reflection.js weekly"
    },
    {
      "name": "学习方向生成",
      "schedule": "0 6 * * *",
      "command": "node engines/learning-direction.js auto"
    }
  ]
}
```

---

## 📈 使用案例

### 案例 1: 编程能力提升

**场景**: 你想要提升编程能力，成为大师级开发者

**配置**:
- 任务队列：编程相关任务（实现功能、修复 bug、学习新技术）
- 技能发现：编程相关技能（algorithm, debugging, testing）
- 反思重点：代码质量、测试覆盖率、性能优化

**预期效果**:
- 每日完成 5-10 个编程任务
- 每周创建 2-3 个编程技能
- 30 天后编程能力显著提升

---

### 案例 2: 学习新领域

**场景**: 你想要学习新领域（如 AI/ML、区块链、Web3）

**配置**:
- 任务队列：学习任务（阅读文档、实践项目、写总结）
- 技能发现：新领域相关技能
- 反思重点：理解深度、实践能力、知识体系

**预期效果**:
- 每日学习 3-5 个新概念
- 每周创建 1-2 个领域技能
- 30 天后掌握新领域基础

---

### 案例 3: 团队项目管理

**场景**: 你想要管理复杂项目，协调多任务并行

**配置**:
- 任务队列：项目任务（分解、分配、追踪）
- 技能发现：项目管理相关技能
- 反思重点：进度、质量、风险

**预期效果**:
- 自主追踪项目进度
- 自动识别风险并预警
- 生成项目报告

---

## 🎯 最佳实践

### 1. 定期审查反思报告

```bash
# 每周查看反思报告
cat memory/reflections/weekly-*.md
```

**关注点**:
- 本周完成了什么？
- 哪些做得好？
- 哪些需要改进？
- 下周计划是什么？

### 2. 调整自信度阈值

**场景**: 系统创建的技能质量不高

**解决**: 提高高自信阈值
```json
{
  "thresholds": {
    "high": 0.8  // 从 0.7 提升到 0.8
  }
}
```

### 3. 优化任务优先级

**场景**: P0 任务过多，系统压力大

**解决**: 重新评估优先级，将部分 P0 降级为 P1

### 4. 集成外部工具

**场景**: 想要集成新的技能发现源

**解决**: 修改 `learning-direction.js`，添加新的搜索源

---

## 🚨 故障排查

### 问题 1: 循环不执行

**检查**:
```bash
# 检查 cron 状态
cron list

# 检查进化引擎状态
node engines/evolution-engine.js status
```

**解决**:
```bash
# 重启循环
node engines/evolution-engine.js run
```

### 问题 2: 任务队列阻塞

**检查**:
```bash
# 查看任务队列
cat tasks/queue.json | jq '.tasks[] | select(.status=="in_progress")'
```

**解决**:
```bash
# 手动标记为 blocked
# 编辑 tasks/queue.json，将任务状态改为 blocked
```

### 问题 3: 反思报告未生成

**检查**:
```bash
# 检查反思目录
ls -la memory/reflections/

# 手动生成反思
node engines/reflection.js daily
```

**解决**:
```bash
# 检查 cron 日志
# 重新设置 cron 任务
node setup-cron.js
```

---

## 📚 相关资源

### 文档

- [INSTALL.md](docs/INSTALL.md) - 详细安装指南
- [USAGE.md](docs/USAGE.md) - 使用指南
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - 架构文档

### 外部资源

- [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) - ECC 项目（灵感来源）
- [DeerFlow](https://github.com/coolclaws/deerflow-book) - DeerFlow 源码解析
- [AutoGen](https://github.com/microsoft/autogen) - Microsoft 多 Agent 框架
- [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用开发框架

---

## 🎉 总结

**Autonomous Learning Cycle** 是一个完整的**自我学习循环系统**，实现：

- ✅ 自主任务执行（17 分钟循环）
- ✅ 学习模式提取
- ✅ 自信度评估
- ✅ 技能自动创建
- ✅ 每日/每周反思
- ✅ 学习方向生成
- ✅ 完全自主进化

**适用场景**: 个人能力提升、新领域学习、团队项目管理

**预期效果**: 30 天后能力显著提升，90 天后成为领域专家

---

**🚀 开始你的自主进化之旅吧！**
