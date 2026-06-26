# 牛马Skill (CowHorseSkill)

一个让 AI 主动询问用户输入、输出和客观需求的 workflow 构建器。

## 核心理念

> 不假设，不猜测，不确定就问。

模型不会等用户自己说全需求，而是**主动逐个提问**，结构化地明确：

- **输入规格**（7 个维度）：数据来源、文件格式、文件位置、数据结构、数据量、数据质量、输入参数
- **输出规格**（6 个维度）：产出形式、输出格式、输出位置、输出内容、排序/筛选/统计、格式要求
- **流程步骤**：每步做什么，哪些自动化
- **约束条件**：时间、技术、业务、性能

## 工作流

1. **Discovery** — 模型主动提问，逐一明确输入/输出/目标
2. **Confirmation** — 结构化总结，迭代直到用户确认
3. **Build** — 创建 skill 目录、SKILL.md、脚本、参考资料
4. **Present** — 展示结果，用户反馈，迭代修改
5. **Finalize** — 打包 skill，更新记忆

## 文件结构

```
cowhorse-skill/
├── SKILL.md                 # 技能主文件（模型执行指令）
├── scripts/
│   └── workflow_builder.py  # 辅助脚本
├── references/
│   └── workflow_guide.md    # 参考案例和决策树
└── README.md                # 本文件
```

## 使用方式

作为 Agent Skill 使用，通过触发词激活：

- "帮我做一个 workflow"
- "建一个 skill"
- "梳理流程"
- "帮我做一个工具"
- "把这个做成一个 skill"

模型会自动进入 Discovery 阶段，主动询问需求细节。

## 手动使用辅助脚本

```bash
# 需求挖掘提示
python3 scripts/workflow_builder.py --step discovery --prompt "用户描述"

# 需求确认总结
python3 scripts/workflow_builder.py --step confirm --data '{"goal":"...","input_spec":{...}}'

# 构建 skill 骨架
python3 scripts/workflow_builder.py --step build --skill-name my-skill
```

## 许可

MIT
