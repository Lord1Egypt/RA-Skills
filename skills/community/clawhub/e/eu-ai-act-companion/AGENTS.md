# AGENTS.md — AI 技能说明书

本文件面向使用或扩展本技能的 AI 编码代理（以及接手的人类维护者）。人类读者请优先读 `README.md`。

技能：`eu-ai-act-companion`
一句话定位：当用户问『我的AI产品要过EU AI Act吗』『高风险还是有限风险』『provider还是deployer义务』『合规要做什么』『截止日期』，或要把 AI 系统投放欧盟市场/在欧部署时使用。把 EU AI Act 从法规文本落成导航：风险四级分类（不可接受/高/有限/最小）、按角色的义务清单（provider/deployer/importer）、关键时间节点（2024-08 生效、2025-02 禁止类、2026-08 高危义务、2027-08 全量）、文档与合格评定路径。附可运行分类器，输入用例即输出风险级+义务+节点。泛化自 eu-ai-act-check。触发词：EU AI Act、欧盟人工智能法、AI合规、高风险AI、合格评定、provider义务、deployer义务、AI法案截止、CE标志、AI监管、 conformity assessment。

---

## 一、用途（Purpose）

本技能是 LGD/UIBC 治理理论技能体系的一员。调用入口为 `SKILL.md`：AI 代理应先读 `SKILL.md`，按其 frontmatter 的 `name`/`description` 判断是否适用，再按正文步骤执行。

## 二、文件约定（Directory conventions）

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 主说明书：frontmatter + 触发条件 + 执行步骤（AI 调用入口） |
| `AGENTS.md` | 本文件：面向 AI 代理的说明书 |
| `README.md` | 面向人类的总览（如存在） |
| `llms.txt` | 面向 AI 的轻量索引（如存在） |
| `scripts/`、`assets/` 等 | 技能执行所需资源（按需） |

## 三、可改 / 不可改边界（Editable / non-editable boundary）

### 可以改
- 本技能自身的文档、脚本与配置；按主题新增资产并同步更新 `SKILL.md` 说明。

### 不可改（改动即视为合规偏差）
- **许可与署名声明**：LICENSE / 许可口径（保留所有权利）不得删除或弱化。
- **任何"文件即证据"类声明**：版本号、日期、权属、DOI、徽章来源。

> 代理若判断某项改动触及上述边界，默认停下来并在变更记录里显式提问。

## 四、给代理的行为准则（Agent rules of engagement）

- **先读后写**：改任何文件前先读原文件，理解既有约定。
- **最小改动**：只做被要求的改动，不顺手重构。
- **不做远端写操作**：不执行 `git push`、不调用远端发布接口；远端写入是人工步骤。
- **如实报告**：无法确认的事项标为 TODO，不要编造。

<!-- 生成：2026-10-15 · 技能骨架批量升级（本地执行） -->
