# Distillation Router — 蒸馏入口 L0 流程编排

> 适用于：data-prompt-coach 蒸馏入口
> 角色：编排 L0.1-L0.4 四阶段流程，作为 SKILL.md 双入口路由的下游

## 入口判定

```
用户输入
    ↓
┌─────────────────────────────────────────┐
│ 入口检测（SKILL.md 主控负责）              │
├─────────────────────────────────────────┤
│ 触发词匹配                                │
│ - "蒸馏教程" → 蒸馏入口                   │
│ - "萃取方法论" → 蒸馏入口                 │
│ - "榨干教程" → 蒸馏入口                   │
│ - "提取教程方法论" → 蒸馏入口              │
│                                          │
│ 模糊判定                                  │
│ - 用户给 URL/PDF/MD 但没说"蒸馏"          │
│   → 反问"你要做数据分析（引导）           │
│     还是蒸馏教程（萃取方法论）？"          │
└─────────────────────────────────────────┘
    ↓
进入蒸馏入口 → 本文件 L0.1
```

---

## L0 流程总览

```
L0.1 整体理解（Adler 精简版）
    ↓ 输出：内存概览（体裁/主题/受众/边界）
L0.2 5 维度并行提取（interview-miner-adapted）
    ↓ 输出：候选清单（去重+关联）
L0.3 三重验证（three-fold-verification）
    ↓ 输出：挂载/淘汰决策
L0.4 RIA++ 挂载（cangjie-lite L0.4）
    ↓ 输出：M{N+1} 文件 + 更新 4 文件 + 蒸馏报告
```

**详细方法论**：见对应文件
- L0.1 / L0.4：[cangjie-lite.md](cangjie-lite.md)
- L0.2：[interview-miner-adapted.md](interview-miner-adapted.md)
- L0.3：[three-fold-verification.md](three-fold-verification.md)

本文件只负责**编排+异常处理+文件路径解析**，不重复方法论内容。

---

## 输入接受

### 输入类型与处理

| 输入类型 | 接受方式 | 处理 |
|---------|---------|------|
| URL | 用户在对话中贴 URL | 用 WebFetch 抓取（截断警告：>3000 字可能不全，提示用户传完整文本） |
| PDF | 用户上传 PDF 文件 | 用 MinerU/markitdown 转 Markdown（用户须装对应 Skill） |
| Markdown | 用户上传 .md 文件 | 直接 Read |
| 纯文本 | 用户在对话中粘贴 | 直接处理 |
| Word | 用户上传 .docx | 用 markitdown 转 Markdown |

### 输入预检

```
输入接受
    ↓
预检：
├─ 文本长度 ≥ 500 字？ → 否 → 提示"内容太短，无法蒸馏方法论"
├─ 文本结构清晰（有章节/段落/标题）？ → 否 → 警告"结构不清晰可能影响提取质量"
└─ 文本是教程类（有方法论/步骤/案例）？ → 否 → 警告"非教程类文本，蒸馏可能无产出"
    ↓
通过预检 → L0.1
```

---

## L0.1 编排

**调用**：[cangjie-lite.md](../distillation/cangjie-lite.md) § L0.1

**主控职责**：
1. 调用 L0.1 整体理解
2. 接收"内存概览"产出
3. 判断是否继续：
   - 教程价值高（体裁=methodology_tutorial 或 mixed）→ 继续 L0.2
   - 教程价值低（体裁=纯叙事无方法论）→ 终止，输出"无可蒸馏方法论"

**主控不重复 L0.1 内容**，只做调用 + 判断 + 流转。

---

## L0.2 编排

**调用**：[interview-miner-adapted.md](../distillation/interview-miner-adapted.md) § 5 维度并行提取规则

**主控职责**：
1. 调用 L0.2 5 维度并行提取
2. 接收候选清单（含去重+关联后的清单）
3. 判断是否继续：
   - 候选数 ≥ 3 → 继续 L0.3
   - 候选数 < 3 → 警告"提取候选过少，可能教程方法论密度低"，仍继续 L0.3（但标注"低密度蒸馏"）

---

## L0.3 编排

**调用**：[three-fold-verification.md](../distillation/three-fold-verification.md) § 三重验证核心

**主控职责**：
1. 对每个候选调用三重验证
2. 接收验证结果（挂载/淘汰/捞回）
3. 汇总统计：
   - 候选总数
   - 通过数（挂载）
   - 淘汰数
   - 捞回数
4. 判断是否继续：
   - 挂载数 ≥ 1 → 继续 L0.4
   - 挂载数 = 0 → 终止，输出"教程无可挂载方法论，全部候选未通过验证"
   - 挂载数 > 5 → 警告"单次蒸馏挂载上限 5 个，超过的留 candidates.md"

**淘汰处理**：
- 完全淘汰 → 写入 `references/audit/rejected.md`
- 捞回候选 → 写入 `references/audit/candidates.md`

---

## L0.4 编排

**调用**：[cangjie-lite.md](../distillation/cangjie-lite.md) § L0.4 RIA++ 挂载

**主控职责**：

### L0.4.1 创建 M{N+1} 文件

1. 查询当前 `references/methods/` 目录，确定 N+1 编号
2. 检查 slug 是否与 M1-M11 重复
3. 检查方法论是否与已有 M1-M11 概念重复（如有，询问用户"合并还是新建？"）
4. 创建 `references/methods/M{N+1}-{slug}.md`（RIA++ 六维）

### L0.4.2 更新 INDEX.md

1. 读取 `assets/INDEX.md`
2. 在 mermaid 引用图追加节点：
   ```
   M{N+1}["M{N+1}: {名称}"]
   ```
3. 追加节点关系（如与其他方法论有关联）

### L0.4.3 更新 method-composition.md

1. 读取 `references/routing/method-composition.md`
2. 根据 L0.2 维度 4 触发条件，追加场景×规模组合
3. 如果新方法论是通用增强，追加到"通用方法论"section

### L0.4.4 追加测试用例

1. 读取 `assets/test-prompts.json`
2. 为每个新挂载的 M{N+1} 追加 ≥1 条 should_trigger 测试用例
3. 可选追加 decoy / boundary 测试用例

### L0.4.5 生成蒸馏报告

直接在对话中输出（不落文件），格式见 cangjie-lite.md § L0.4.5

---

## 文件路径解析

主控在 L0.4 阶段需要操作的文件：

| 操作 | 文件路径 | 说明 |
|------|---------|------|
| 创建 | `references/methods/M{N+1}-{slug}.md` | 新方法论文件 |
| 更新 | `assets/INDEX.md` | mermaid 引用图追加节点 |
| 更新 | `references/routing/method-composition.md` | 路由矩阵追加组合 |
| 更新 | `assets/test-prompts.json` | 追加测试用例 |
| 追加 | `references/audit/rejected.md` | 淘汰候选（如有） |
| 追加 | `references/audit/candidates.md` | 捞回候选（如有） |

**路径相对**：`data-prompt-coach/` 为根目录

---

## 异常处理

| 场景 | 处理方式 |
|------|---------|
| 输入文本 < 500 字 | 提示"内容太短，无法蒸馏方法论" + 终止 |
| 输入结构不清晰 | 警告"结构不清晰可能影响提取质量" + 继续 |
| 输入非教程类 | 警告"非教程类文本，蒸馏可能无产出" + 继续（用户确认） |
| WebFetch 截断 | 提示"URL 抓取不全（{X} 字符），建议传完整文本" + 用户选择继续或重传 |
| L0.2 候选数 < 3 | 警告"候选过少，可能教程方法论密度低" + 继续 |
| L0.3 全部淘汰 | 输出"无可挂载方法论" + 终止 |
| L0.4 挂载数 > 5 | 警告"超过单次挂载上限 5 个，超出部分留 candidates.md" + 仅挂载前 5 个 |
| 新方法论与 M1-M11 重复 | 询问"合并还是新建？" + 用户决策 |
| 文件写入失败 | 终止 + 提示"文件系统错误，请检查权限" |

---

## 与 SKILL.md 的接口

**入口点**：本文件"入口判定"段落
**出口点**：本文件 L0.4.5（蒸馏报告输出后）
**依赖文件**：
- cangjie-lite.md（L0.1 + L0.4 方法论）
- interview-miner-adapted.md（L0.2 方法论）
- three-fold-verification.md（L0.3 方法论）
- references/methods/（L0.4.1 写入）
- assets/INDEX.md（L0.4.2 更新）
- references/routing/method-composition.md（L0.4.3 更新）
- assets/test-prompts.json（L0.4.4 更新）
- references/audit/rejected.md + candidates.md（淘汰处理）
