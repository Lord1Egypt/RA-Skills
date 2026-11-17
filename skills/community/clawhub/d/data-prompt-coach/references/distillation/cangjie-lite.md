# Cangjie Lite — 4 阶段精简版蒸馏流水线

> 来源：cangjie-skill RIA-TV++ 7 阶段流水线精简
> 精简原则：保留核心方法论产出能力，去掉 cangjie 完整版的奢侈环节
> 适用于：data-prompt-coach 蒸馏入口 L0

## 与 cangjie 完整版的对比

| 维度 | cangjie 完整版 | cangjie-lite（本文件） |
|------|---------------|----------------------|
| 阶段数 | 7 | 4 |
| 整体理解 | Adler 四步拆解 → BOOK_OVERVIEW.md | Adler 精简 → 内存概览（不落文件） |
| 提取器 | 5 个并行（框架/原则/案例/反例/术语） | 5 维度并行（interview-miner-adapted.md） |
| 验证 | 三重验证 + Zettelkasten 链接 | 仅三重验证（见 three-fold-verification.md） |
| 构造 | RIA++ 六维 | RIA++ 六维（同） |
| 链接 | INDEX.md + 引用图 + 跨 skill 关系 | 仅更新 INDEX.md（追加节点） |
| 压力测试 | test-prompts.json 含诱饵 | 挂载即追加 1 条 should_trigger 测试用例 |
| 交付 | DIGEST.md + 安装到 skills 目录 | 挂载到 references/methods/M{N+1} |

**精简掉的环节及原因**：
- Zettelkasten 跨 skill 引用图：教程方法论独立性高，不需要细粒度引用
- 完整压力测试套件：1 条 should_trigger 足够验证触发
- DIGEST.md 精华长文：M{N+1} 文件已是结构化方法论，不需要二次摘要
- 安装到 skills 目录：data-prompt-coach 内部挂载即可

---

## L0.1 整体理解（Adler 精简版）

**Adler 分析阅读法**：结构 / 解释 / 批判 / 应用四步拆解

### 精简为 3 步

```
Step 1: 结构拆解（30 秒）
├─ 识别章节/段落/标题层级
├─ 判断体裁：案例教程 / 方法论教程 / 混合
└─ 提取主线：教程在讲什么 + 不讲什么

Step 2: 主题识别（30 秒）
├─ 核心主题一句话
├─ 受众画像：教程写给谁看的（小白 / 进阶 / 专家）
└─ 价值定位：教程解决什么痛点

Step 3: 适用边界（30 秒）
├─ 显式边界：教程自己说不做什么
└─ 隐式边界：从体裁推断不适用场景
```

### 产出

**内存概览**（不落文件）：
```yaml
tutorial_title: "..."
genre: "case_tutorial | methodology_tutorial | mixed"
core_topic: "..."
target_audience: "beginner | intermediate | expert"
value_proposition: "..."
explicit_boundary: "..."
implicit_boundary: "..."
```

---

## L0.2 5 维度并行提取

**详见**：[interview-miner-adapted.md](interview-miner-adapted.md)

**核心调整**：interview-insight-miner 原为"访谈转录文本挖掘"，本文件将其 5 维度适配为"教程文本挖掘"，每个维度映射到一种方法论候选类型：

| 原维度 | 原用途 | 适配后用途 | 产出类型 |
|--------|--------|----------|---------|
| 显性认知 | 提取访谈主角的观点 | 提取教程明确表述的方法论 | 方法论候选 |
| 隐性意图 | 推断访谈主角的暗示 | 提取教程暗示要避免的坑 | 陷阱候选 |
| 思维模型 | 提炼底层认知框架 | 提取作者做决策的框架 | 决策框架候选 |
| 行业信号 | 提取行业趋势判断 | 提取场景适用信号 | 触发条件候选 |
| 反常识洞察 | 提取与主流相反的观点 | 提取独特点（淘汰常识） | 独特性候选 |

---

## L0.3 三重验证

**详见**：[three-fold-verification.md](three-fold-verification.md)

**精简原则**：保留 cangjie 三重验证的核心判断逻辑，去掉跨 skill 比对环节

```
V1 跨域：原文 ≥ 2 处独立佐证（同一概念在不同章节/案例出现）
V2 预测力：能回答教程未明说的问题（举一反三）
V3 独特性：不是常识（教程作者自己也强调"很多人不知道"）
```

**通过率目标**：≥ 50%（cangjie 整书 25-50%，教程通常更高，因为教程本身就是结构化方法论）

---

## L0.4 RIA++ 挂载

### 4.1 创建 M{N+1} 文件

**文件路径**：`references/methods/M{N+1}-{slug}.md`

**文件结构**：
```markdown
# M{N+1}：{方法论名称}

> 来源：{教程标题}
> 蒸馏时间：{YYYY-MM-DD}
> 验证：V1 跨域 ✅ / V2 预测力 ✅ / V3 独特性 ✅

## R（Reading 原文引用）
{原文关键句，至少 2 处}

## I（Interpretation 重写）
{用自己的话重写方法论}

## A1（Past Application 书中案例）
{教程中的实际应用案例}

## A2（Future Trigger 触发场景）
{何时使用本方法论}

## E（Execution 可执行步骤）
{具体怎么用}

## B（Boundary 边界与盲点）
{不适用的情况 / 已知局限}
```

**slug 命名规则**：
- 全小写 + 连字符
- 不超过 4 个单词
- 反映方法论核心动作
- 示例：`golden-five-elements` / `anti-hallucination-trio`

### 4.2 更新 INDEX.md

打开 `assets/INDEX.md`，在 mermaid 引用图追加节点：
```
M{N+1}["M{N+1}: {名称}"]
```
并追加节点关系（如有）：
```
M{N+1} -.-> M{相关 ID}
```

### 4.3 更新 method-composition.md

打开 `references/routing/method-composition.md`，在路由矩阵追加场景×规模组合：
```
| {场景} | {规模} | M{N+1}+{其他} |
```

如果新方法论是通用增强（不限场景），追加到"通用方法论语"section：
```
## 通用方法论
- M{N+1} {名称}：{一句话} — 适用所有场景
```

### 4.4 追加测试用例

打开 `assets/test-prompts.json`，追加 ≥1 条测试用例：
```json
{
  "id": "test-m{N+1}-001",
  "method": "M{N+1}",
  "type": "should_trigger",
  "input": "{应该触发 M{N+1} 的真实用户说法}",
  "expected": "M{N+1} 应被选中并套用 RIA++"
}
```

可选追加 decoy / boundary 测试用例。

### 4.5 生成蒸馏报告

**产物**：直接在对话中输出（不落文件）

```markdown
# 蒸馏报告 — {教程标题}

> 蒸馏时间：{YYYY-MM-DD}
> 候选数：{N} | 通过数：{M} | 挂载数：{K}

## 挂载清单
- M{N+1}：{名称} — {一句话} — 触发：{场景}
- M{N+2}：{名称} — {一句话} — 触发：{场景}

## 淘汰清单
- 候选"{X}" 未通过 V{1/2/3}：{原因}

## 更新文件清单
- ✅ 创建：references/methods/M{N+1}-xxx.md
- ✅ 更新：assets/INDEX.md（追加 M{N+1} 节点）
- ✅ 更新：references/routing/method-composition.md（追加场景组合）
- ✅ 更新：assets/test-prompts.json（追加 test-m{N+1}-001 测试用例）
```

---

## 反模式（避免跑偏）

| 反模式 | 表现 | 修复 |
|--------|------|------|
| 蒸馏成普通摘要 | 产出是"教程讲了啥"的总结而非方法论 | 严格遵守 RIA++ 六维结构，R 必须是原文引用 |
| 跳过验证 | 所有候选都通过 | 三重验证是硬门控，通过率目标 ≥ 50% 不是 100% |
| 文件膨胀 | 一次蒸馏挂载 10+ 方法论 | 单次蒸馏挂载上限 5 个，超过的留 candidates.md |
| 重复造轮子 | 新方法论与 M1-M11 重复 | L0.4.1 创建前必查 11 原子速查表 |

---

## 与 SKILL.md 的接口

SKILL.md 双入口路由 → 触发"蒸馏教程"→ 调用本文件 L0.1 → L0.4 → 返回蒸馏报告

**入口点**：本文件 L0.1
**出口点**：本文件 L0.4.5 蒸馏报告
**依赖文件**：
- interview-miner-adapted.md（L0.2 调用）
- three-fold-verification.md（L0.3 调用）
- /references/methods/ 目录（L0.4.1 写入）
- /assets/INDEX.md（L0.4.2 更新）
- /references/routing/method-composition.md（L0.4.3 更新）
- /assets/test-prompts.json（L0.4.4 追加）
