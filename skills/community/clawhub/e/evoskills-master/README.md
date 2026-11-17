# OpenClaw EvoSkills

一个永久性的元技能，用于通过迭代的生成器-验证器循环来路由、创建、审计和自我进化技能。

## 概述

OpenClaw EvoSkills 被设计为 OpenClaw 工作区中始终运行的元技能。它监督其他技能，自动将重复的工作流捕获为新技能，并通过短期的、验证器驱动的迭代来进化现有技能，而不是一次性重写。

## 功能特性

- **技能进化**：通过 基准 → 补丁 → 验证 循环迭代改进现有技能
- **自动技能捕获**：检测重复工作流并自动创建可复用的技能
- **元技能架构**：作为最高优先级的技能，路由和管理其他技能
- **代理验证**：静态检查 + 使用真实提示词进行前向测试
- **自我修复**：自动修复常见技能问题（断链、内容薄弱、格式错误的元数据）

## 快速开始

### 安装

1. 克隆此仓库到你的 OpenClaw 工作区：
   ```bash
   git clone https://github.com/majiabin2020/openclaw-evoskills.git
   ```

2. 激活为元技能：
   ```bash
   python scripts/activate_meta_skill.py --workspace <openclaw-workspace> --json
   ```

### 基本用法

**进化现有技能：**
```bash
python scripts/evolve_skill.py <target-skill-dir> --goal "期望的改进" --rounds 3 --json
```

**从重复工作中创建新技能：**
```bash
python scripts/scaffold_skill.py <skills-root> --goal "重复工作流目标" --evidence "示例1" --evidence "示例2" --rounds 2 --json
```

**自动发现技能候选：**
```bash
python scripts/observe_repetition.py --workspace <openclaw-workspace> --json
```

## 脚本说明

| 脚本 | 描述 |
|------|------|
| `activate_meta_skill.py` | 安装并激活为工作区级元技能 |
| `evolve_skill.py` | 运行完整进化循环（审计 → 修复 → 验证 → 报告） |
| `scaffold_skill.py` | 从重复工作流证据创建新技能 |
| `observe_repetition.py` | 扫描内存/会话轨迹寻找技能候选 |
| `skill_audit.py` | 静态结构和元数据验证 |
| `repair_skill.py` | 自动修复常见技能问题 |
| `surrogate_verify.py` | 生成并运行提示词验证矩阵 |

## 进化工作流

1. **基准测试**：读取目标技能，捕获当前状态和失败点
2. **定义评估集**：创建 3-7 个真实提示词，覆盖触发匹配、核心工作流、失败恢复
3. **补丁修复**：修复最高价值的瓶颈（结构 → 触发器 → 工作流 → 资源 → 验证）
4. **验证**：运行静态检查 + 使用真实提示词进行前向测试
5. **升级验证器**：如果技能通过检查但在真实任务中失败，加强评估矩阵
6. **重复**：继续直到收敛或达到轮次上限

## 项目结构

```
openclaw-evoskills/
├── SKILL.md                 # 主技能定义
├── agents/
│   └── openai.yaml          # Agent 接口配置
├── references/
│   ├── evolution-loop.md    # 协同进化循环文档
│   ├── hermes-alignment.md  # Hermes 风格技能模式
│   └── meta-skill-policy.md # 元技能集成策略
└── scripts/
    ├── activate_meta_skill.py
    ├── evolve_skill.py
    ├── observe_repetition.py
    ├── repair_skill.py
    ├── scaffold_skill.py
    ├── skill_audit.py
    └── surrogate_verify.py
```

## 元技能契约

当安装为元技能时：

- 在其他技能路由之前加载
- 决定是否调用、进化、合并、拆分或创建任务技能
- 自动捕获重复工作流
- 在工作区技能层次结构中保持最高优先级

## 文档

- [进化循环](references/evolution-loop.md) - 核心进化方法论
- [元技能策略](references/meta-skill-policy.md) - 与 OpenClaw 工作区集成
- [Hermes 对齐](references/hermes-alignment.md) - 渐进式披露模式

## 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m '添加新功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件。

## 作者

- **majiabin2020** - [GitHub 主页](https://github.com/majiabin2020)

## 致谢

- 为 OpenClaw 生态系统构建
- 受 EvoSkills 迭代改进方法论启发
