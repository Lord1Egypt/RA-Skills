---
name: collab-workflow-ingest
description: "协作流程：业务流程梳理 → 数字资源入库。先用 workflow-structurer 逐步澄清流程，生成结构化步骤文档；再用 demo-asset-ingest 的打包规范将成果发布到 ClawHub 资源中心。适用场景：需要将模糊需求转化为可执行流程、并把最终产物沉淀到可检索仓库的工作。"
metadata:
  clawdbot:
    emoji: "🔗"
    requires: ["clawhub"]
---

# 协作流程：流程梳理 → 资源入库

## 概述

本技能封装了两个工具的串联协作模式：

| 阶段 | 工具 | 职责 |
|------|------|------|
| 上游：流程处理 | `workflow-structurer` | 通过渐进式澄清，把模糊需求拆解为含输入/输出/风险/校验/规则的结构化步骤 |
| 下游：资源入库 | `demo-asset-ingest` | 将上游产物按 ClawHub-skill 规范打包，通过 `clawhub publish` 发布到资源中心 |

## 完整执行步骤

### Step 1: 用 workflow-structurer 梳理流程

1. 调用 workflow-structurer，依次完成 5 个阶段：
   - **Phase 1** 澄清目标（1-2 个问题）
   - **Phase 2** 提取步骤骨架
   - **Phase 3** 逐层钻取每个步骤（输入/输出/职责/风险/校验/规则）
   - **Phase 4** 汇总确认
   - **Phase 5** 生成 handoff 摘要
2. 输出物：`workflow-handoff.md`（含目标、步骤列表、关键规则、关键风险、校验总结）

### Step 2: 按 demo-asset-ingest 规范打包

1. 创建目录结构：
   ```
   collab-asset/
   ├── SKILL.md              # 技能元数据 + 操作说明
   └── references/
       └── DESCRIPTION.md    # 上游流程梳理产物（handoff 摘要）
   ```
2. 将 Step 1 产出的 handoff 摘要写入 `references/DESCRIPTION.md`
3. 验证：`ls -R collab-asset`

### Step 3: 发布到 ClawHub 资源中心

```bash
# 预览（dry-run）
clawhub publish collab-asset --slug collab-workflow-ingest --name "Collab Workflow Ingest" --tags "workflow,ingest,collab" --topics "workflow,ingest" --dry-run

# 正式发布
clawhub publish collab-asset --slug collab-workflow-ingest --name "Collab Workflow Ingest" --tags "workflow,ingest,collab" --topics "workflow,ingest"
```

### Step 4: 验证入库

```bash
clawhub search collab-workflow-ingest
```

## 输入输出关系

| 从 | 到 | 数据 |
|----|----|------|
| 用户需求 | workflow-structurer | 自然语言描述（模糊需求） |
| workflow-structurer | DESCRIPTION.md | 结构化 handoff 摘要 |
| DESCRIPTION.md | clawhub publish | skill-shaped 文件夹 |
| clawhub publish | ClawHub 资源中心 | 可检索、可安装的 skill 条目 |

## 关键注意事项

1. **不要跳步**：必须先完成流程梳理再打包，DESCRIPTION.md 内容质量决定入库价值
2. **clawhub 登录**：发布前确认 `clawhub whoami` 有有效身份
3. **slug 唯一性**：`--slug` 必须是 ClawHub 全局唯一名称
4. **dry-run 先行**：正式发布前一定先跑 `--dry-run` 验证结构和元数据
5. **审批延迟**：新发布的 skill 可能需要审核，搜索可能有短暂延迟
