# 样例库 · 模块 × 能力矩阵

> 本目录收纳 **11 个已通过 VERIFY 门控** 的真实可运行样例，覆盖六大输出能力与 A→G 全模块（含 E·N 院校子模块）。

> 每个样例均为单文件 HTML，可直接在浏览器/WorkBuddy 预览面板打开；文件名语义化、按能力分目录存放。

## 一、模块 × 能力 分布矩阵

| 能力 \ 模块 | A | B | C | D | E·N | F | G |
|---|---|---|---|---|---|---|---|
| **能力一·课件** | A2 概念图谱 | — | C1 对比器 | D1 沙盘 | E·N 上手 | — | G1 雷达 |
| **能力二·游戏** | — | — | — | — | — | F4 委员会<br>F1 闯关 | — |
| **能力三·备课** | — | — | — | — | — | — | — |
| **能力四·评估** | — | — | — | — | — | — | — |
| **能力五·推荐** | — | — | — | — | — | — | — |
| **能力六·协作** | — | — | — | — | — | — | — |

> 说明：能力三~六为「能力代表样例」（演示该能力的完整产出范式），不绑定特定知识模块；能力一/二额外提供跨模块课件/游戏样例。

## 二、目录结构

```
examples/
├── INDEX.md                      # 本文件（模块×能力矩阵 + 样例清单）
├── courseware/                   # 能力一·课件（+ 跨模块课件）
│   ├── c1-prompt-compare.html         # Prompt 五要素对比器
│   ├── a2-ai-concept.html             # 人工智能概念图谱
│   ├── d1-data-driven.html            # 数据驱动决策沙盘
│   ├── en-bnbu-onboard.html           # BNBU 新生 4 周 AI 上手
│   ├── g1-capability-radar.html       # AI 能力雷达图
├── game/                         # 能力二·游戏（+ 跨模块游戏）
│   ├── f4-ethics-committee.html       # 伦理委员会（沉浸式冒险）
│   ├── f1-adversarial.html            # 对抗攻击闯关
├── lesson/                       # 能力三·备课
│   ├── lesson-prep-4fmt.html          # 4 格式备课包导出
├── assessment/                   # 能力四·评估
│   ├── adaptive-quiz.html             # 自适应测评 + 薄弱点报告
├── recommend/                    # 能力五·推荐
│   ├── study-plan.html                # 零基础学习路径周计划
└── collaboration/                # 能力六·协作
    ├── collab-room.html               # 协作备课室
```

## 三、样例清单

### 能力一·课件

| 样例文件 | 覆盖模块 | 控件实测 | 门控 | 说明 | 复用参考 |
|---|---|---|---|---|---|
| `courseware/c1-prompt-compare.html` | C | 9/9 | PASS(可提交) | Prompt 五要素对比器：文本输入 + 温度滑块 + 角色/格式下拉 + 实时预览 + 重置，演示 C1 提示词工程的五要素可视化对比。 | references/p5js-courseware-guide.md §C1 |
| `courseware/a2-ai-concept.html` | A | 4/4 | PASS(可提交) | 人工智能概念图谱：卡片切换展示 A2「什么是 AI / 强弱 AI / 机器学习」核心概念，含概念翻转交互。 | references/p5js-courseware-guide.md §A2 |
| `courseware/d1-data-driven.html` | D | 4/4 | PASS(可提交) | 数据驱动决策沙盘：滑块调节样本量/噪声，实时观察 D1 数据质量对模型效果的影响。 | references/p5js-courseware-guide.md §D1 |
| `courseware/en-bnbu-onboard.html` | E·N | 10/10 | PASS(可提交) | BNBU 新生 4 周 AI 上手：E·N 院校子模块样例：为北师港浸大（BNBU）博雅智能学院（SAI）新生定制的 4 周 AI 上手路线与周任务卡。 | references/module-e-bnbu-sai.md |
| `courseware/g1-capability-radar.html` | G | 6/6 | PASS(可提交) | AI 能力雷达图：G1 最新发展可视化：输入自评生成多维度 AI 能力雷达对比。 | references/p5js-courseware-guide.md §G1 |

### 能力二·游戏

| 样例文件 | 覆盖模块 | 控件实测 | 门控 | 说明 | 复用参考 |
|---|---|---|---|---|---|
| `game/f4-ethics-committee.html` | F | 5/5 | PASS(可提交) | 伦理委员会（沉浸式冒险）：F4 安全伦理游戏化：p5 画布场景 + 选择题推进关卡 + 计分 + 生命值 + 重开。 | references/p5js-game-design-guide.md §F4 |
| `game/f1-adversarial.html` | F | 4/4 | PASS(可提交) | 对抗攻击闯关：F1 安全威胁游戏化：在画布上操作扰动滑块躲避对抗样本检测，理解对抗攻击原理。 | references/p5js-game-design-guide.md §F1 |

### 能力三·备课

| 样例文件 | 覆盖模块 | 控件实测 | 门控 | 说明 | 复用参考 |
|---|---|---|---|---|---|
| `lesson/lesson-prep-4fmt.html` | （能力代表） | 7/7 | PASS(可提交) | 4 格式备课包导出：能力三代表样例：纯前端生成 Word/PPT/Excel/PDF 四格式并用 Blob 一键打包 ZIP。 | references/interactive-lesson-builder-guide.md |

### 能力四·评估

| 样例文件 | 覆盖模块 | 控件实测 | 门控 | 说明 | 复用参考 |
|---|---|---|---|---|---|
| `assessment/adaptive-quiz.html` | （能力代表） | 12/12 | PASS(可提交) | 自适应测评 + 薄弱点报告：能力四代表样例：单选答题 + 实时评分 + IndexedDB 进度保存 + 薄弱点诊断报告。 | references/assessment-guide.md |

### 能力五·推荐

| 样例文件 | 覆盖模块 | 控件实测 | 门控 | 说明 | 复用参考 |
|---|---|---|---|---|---|
| `recommend/study-plan.html` | （能力代表） | 2/2 | PASS(可提交) | 零基础学习路径周计划：能力五代表样例：基于知识图谱推导个性化学习路径，输出可执行周计划 + 勾选打卡 + 导出。 | references/recommendation-engine.md |

### 能力六·协作

| 样例文件 | 覆盖模块 | 控件实测 | 门控 | 说明 | 复用参考 |
|---|---|---|---|---|---|
| `collaboration/collab-room.html` | （能力代表） | 5/5 | PASS(可提交) | 协作备课室：能力六代表样例：角色分配 + 版本历史 + 批注提交，演示多人协作备课闭环。 | references/collaboration-guide.md |

## 四、复测 / 校验方法

所有样例在入库前均已通过 `assets/playwright-control-test-harness.js` 控件实测（枚举全部互动控件、触发、捕获报错、输出门控结果块）。复核命令：

```bash
export NODE_PATH=$(npm root -g)
node assets/playwright-control-test-harness.js examples/courseware/c1-prompt-compare.html \
      --out /tmp/recheck --name "C1 对比器复核"
```

> 门控结论：全部样例 `PASS(可提交)`，且 `consoleErrors + pageErrors = 0`（无业务报错）。

## 五、如何使用

- **作为教学演示**：直接在浏览器或 WorkBuddy 预览面板打开对应 HTML。

- **作为生成模板**：参考 INDEX 第三列的「复用参考」指向的 `references/` 文档，按相同范式为新主题生成同类产物。

- **作为回归基线**：每次技能升级后，批量跑上述 harness 确认样例仍全部通过门控。
