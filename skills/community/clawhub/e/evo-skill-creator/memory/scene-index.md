# 场景索引

> 定义不同场景下需要加载的 memory 文件，避免上下文爆炸和遗漏加载。
> 43 个知识文件不能全部加载，必须按场景按需加载。
> **规则：本文件只索引公开数据，private/ 下的文件由 private/README.md 管理。**

## 场景 1：go 命令 - 创建新角色
**触发条件**：创建新角色、帮我做一个智能体
**加载文件**：
- memory/knowledge/agent-design/skill-creation-checklist.md（创建规范检查清单）
**加载时机**：命令开始时
**不加载**：其他 42 个知识文件（创建角色不需要理论知识）

## 场景 2：go 命令 - 架构完善任务
**触发条件**：继续做P0待办、补充规范
**加载文件**：
（无公开文件需要加载，私有数据通过 private/README.md 索引）
**按需加载**：根据具体任务加载相关知识文件

## 场景 3：learn 命令
**触发条件**：学习一下、研究一下XX知识
**加载文件**：
- memory/learning-plan.md（当前学习计划）
**按需加载**：根据学习主题加载对应 knowledge/ 文件（先温故再学新）
**沉淀后**：必须更新本文件的"文件覆盖检查表"

## 场景 4：scan 命令
**触发条件**：扫描最新趋势
**加载文件**：
- memory/watchlist.md（关注清单）
- memory/learning-plan.md（识别学习方向）

## 场景 5：plan 命令
**触发条件**：制定学习计划
**加载文件**：
- memory/learning-plan.md（当前计划）

## 场景 6：review 命令 - 自省
**触发条件**：评审一下自己
**加载文件**：
- memory/scene-index.md（本文件，检查索引完整性）
- memory/learning-plan.md（学习进度）

## 场景 7：review 命令 - 评审子智能体
**触发条件**：评审XX角色、升级角色
**加载文件**：
（私有数据通过 private/README.md 索引）

## 场景 8：go 命令 - 开源准备
**触发条件**：开源、开源准备、LICENSE、CONTRIBUTING、脱敏、发布到 GitHub
**加载文件**：
- memory/knowledge/frameworks/skill-opensource-requirements-2026.md（开源全流程检查清单）
- memory/knowledge/frameworks/skill-yaml-frontmatter-discovery-2026.md（YAML frontmatter 标准）
**加载时机**：命令开始时
**说明**：开源涉及代码脱敏、标准文件补充、Skill 标准化等，需要完整的检查清单指导

## 场景 9：review 命令 - 开源准备度评审
**触发条件**：评审开源准备度、检查开源合规性
**加载文件**：
- memory/knowledge/frameworks/skill-opensource-requirements-2026.md（五阶段检查清单）
**说明**：用开源检查清单逐项评审 skill 和仓库的开源准备度

## 场景 10：suggest 命令
**触发条件**：给你提个建议、你怎么看
**加载文件**：
- memory/learning-plan.md（可能需要调整）

## 场景 11：status 命令
**触发条件**：你最近状态怎么样
**加载文件**：
- memory/learning-plan.md（学习进度）
- output/execution.log（最近活动，读最后 20 行）

## 文件覆盖检查表

> review 时必须检查：所有公开 memory 文件是否都有加载���景
> **注意：private/ 下的文件不在此表中，由 private/README.md 管理**

### 根级文件
| 文件路径 | 关联场景 | 状态 |
|---------|---------|------|
| memory/learning-plan.md | 场景3、4、5、6、10、11 | ✅ |
| memory/watchlist.md | 场景4 | ✅ |
| memory/scene-index.md | 场景6 | ✅ |

### knowledge/ 文件（43 个，按主题分组）
| 知识主题 | 文件数 | 加载场景 |
|---------|--------|---------|
| agent-design/ | 37 | 场景3（learn 按主题加载） |
| frameworks/ | 7 | 场景3（learn）、场景8/9（开源相关文件） |
| ai-models/ | 1 | 场景3（learn 按主题加载） |

#### frameworks/ 按场景索引明细
| 文件 | 关联场景 |
|------|---------|
| skill-opensource-requirements-2026.md | 场景8（开源准备）、场景9（开源评审） |
| skill-yaml-frontmatter-discovery-2026.md | 场景8（开源准备） |
| 其他 frameworks/ 文件 | 场景3（learn 按主题加载） |

**关键原则**：knowledge/ 下的文件**永远不在启动时全部加载**，只在 learn 命令中按学习主题加载对应文件。

## 沉淀时的更新规则

当通过 learn/scan/go 命令沉淀新知识文件时：
1. 创建新文件后，必须在本文件的"文件覆盖检查表"中追加一行
2. 标明该文件关联哪个场景
3. 如果是全新的知识主题，更新 knowledge/ 文件数统计
