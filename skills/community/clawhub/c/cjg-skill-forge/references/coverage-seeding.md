# 覆盖维度播种规则 / Coverage Seeding Rules

> 锻造炉在锻造技能时，自动解析技能 `description`（frontmatter）播种 `references/coverage.md`。
> 创作者确认/修改后定稿——锻造炉不强制覆盖创作修改。

## 一、自动播种规则

锻造时解析技能 `description`（frontmatter）的自声明范围，预填 `coverage.md`：

| 检测到的 description 模式 | 预填维度 | 示例 |
|---|---|---|
| "支持 X / Y / Z 平台" / "覆盖 X、Y" | `platform` 或 `endpoint` | "支持 Slack、GitHub、Jira" → `platform: Slack, GitHub, Jira` |
| "用于 X / Y 场景" | `scenario` | "用于数据分析、文献检索" → `scenario: 数据分析, 文献检索` |
| "生成 X / Y 风格" | `genre` / `style` | "生成科幻、奇幻小说" → `genre: 科幻, 奇幻` |
| 无明确自声明 | 按技能原型给默认维度模板（见第二节） | — |

## 二、默认维度模板（按原型）

当 description 无法自动解析时，按技能原型给默认模板：

| 原型 | 默认维度 |
|---|---|
| 方法谋士 | `discipline`, `method` |
| 垂直领域工具 | `vertical`, `platform`, `doc_type`, `scenario` |
| API/平台封装 | `endpoint`, `operation`, `error_code` |
| 诊断排障 | `symptom`, `error_family` |
| 工作流/管道 | `step`, `scenario` |
| 生成创作 | `genre`, `tone`, `form`, `provider` |
| 分析研究 | `method`, `dataset`, `source` |
| 记忆状态 | `entity`, `recall_type` |
| 元技能/自指 | `skill_aspect`, `meta_concept` |
| 接口/模态适配 | `format`, `modality` |
| 多 agent 编排 | `role`, `scenario` |
| 部署/平台 | `platform`, `scenario` |
| 其他 | `task_type`, `domain`（宽松兜底） |

## 三、优雅降级

纯"通用推理 / 头脑风暴"类技能（覆盖是涌现的、无法枚举），`coverage.md` 只声明 `task_type` / `domain` 两个宽松维度。机制优雅降级：

- 缺口信号照样能记"用户问了落在外面的东西"（`in_taxonomy=false`）。
- self-audit 的"声明了但从没命中"那条**用不上**（因为没声明细粒度值），不影响主流程。

## 四、产物格式

产出的 `coverage.md` 格式：

```markdown
# 覆盖维度表 / Coverage Taxonomy

> 本技能按以下维度组织覆盖。维度值由锻造时自动播种 + 创作者补充。
> 缺口信号参照此表判断 in_taxonomy。

## dimension: {维度名}
{值1} · {值2} · {值3} · ...
```

### 示例 — 方法谋士（扫地僧）

```markdown
# 覆盖维度表 / Coverage Taxonomy

> 本技能按以下维度组织覆盖。缺口信号参照此表判断 in_taxonomy。
> 由锻造炉播种，对应 method-matrix.md 的学科轴与方法卡。

## dimension: discipline（学科）
社科/教育 · 医学/临床 · 计算机/AI · 经济 · 人文 · 工程/设计 · 艺术 · 自然/理工 · 法学实证 · 语言学 · 心理/认知 · 生态/环境

## dimension: method（方法）
实验方法 · 数据分析 · 问卷量表 · 质性方法 · 计算模拟 · 人文方法 · 设计科学 · 计量经济 · ML/AI评估 · 文献计量 · 系统综述 · 混合方法 · 法学实证 · 语言学 · 复现与预注册 · 纵向/生存 · 计算文本/网络
```

### 示例 — API 平台封装（slack-tool 为例）

```markdown
# 覆盖维度表 / Coverage Taxonomy

> 本技能按以下维度组织覆盖。维度值由锻造时自动播种 + 创作者补充。
> 缺口信号参照此表判断 in_taxonomy。

## dimension: endpoint
chat.postMessage · chat.delete · chat.update · conversations.list · users.info

## dimension: operation
send · delete · update · list · search

## dimension: error_code
rate_limited · channel_not_found · invalid_auth · missing_scope
```
