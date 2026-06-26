---
name: deslop
category: knowledge
description: |
  当文章/文档/分享稿读起来像 AI 写的、充满套话、缺具体细节时使用。中英文反 AI 味两次 pass 重写。
  不适用于代码注释和 commit message 的去 AI 味（用 slopbuster --mode code）。参见 doc-gen (用于生成文档)、human-writing (用于项目级中文写作参考)。
license: MIT
triggers:
  - AI.*味
  - 人味
  - 去.*AI
  - 像.*AI.*写
  - 重写.*文章
  - 文章.*风格
  - human.*writing
  - deslop
  - slopbuster
  - humanizer
  - 写作.*优化
---

# Deslop — 反 AI 味写作

蒸馏自 `@human-writing`、slopbuster、humanizer 三个 skill 的核心规则。

去 AI 味只是一半。去完之后的文字如果无菌、无观点、无节奏，同样一眼就能看出是 AI 改过的。目标是替换，不是删除。

## When to Use

- 文章/文档/博客写完后读起来像 AI 生成的
- ATA 分享稿、对外文档需要去 AI 味
- 用户明确要求"去 AI 味"、"写得更像人"
- 审查已有文档的 AI 痕迹并修复

## When NOT to Use

- 代码注释和 commit message 的去 AI 味（用 slopbuster `--mode code`）
- 学术论文的去 AI 味（用 slopbuster `--mode academic`）
- 纯文档生成（用 `@doc-gen`）
- 内容本身需要重写而不只是去 AI 味

<example>
正确用法：对一篇 ATA 技术分享稿做两次 pass 去 AI 味重写
输入: 一篇 2000 字的技术文章，包含"革命性"、"赋能开发者"、"无缝集成"等 AI 痕迹
Pass 1: 去掉 12 个 AI 词汇、5 个意义膨胀、3 个 copula 回避
Pass 2: 发现残留痕迹（均匀句长、无观点），注入节奏变化和具体感受
结果: 评分从 3.2/10 提升到 8.1/10
</example>

<anti-example>
错误用法：只做 Pass 1 不做 Pass 2
Pass 1 去掉 AI 模式后，文字变得干净但无菌——均匀句长、中立陈述、完美结构
这种"无菌文"和 AI slop 一样容易被识别，只是被不同的检测器识别
MUST 做两次 pass，NEVER 只做一次
</anti-example>

## Usage

```
/deslop <file>              # 标准深度，自动检测语言
/deslop <file> --score-only # 只评分，不重写
```

## Workflow

MUST 按以下 4 步执行，NEVER 跳过 Pass 2（跳过 = 产出无菌文，同样一眼能看出 AI 改过）。如果不确定某个改动是否合适，保留原文并标注，让用户确认。

```
Step 1. 诊断  — 读全文，按模式清单标注所有 AI 痕迹，给原始评分
Step 2. Pass 1 — 去模式：逐条消除标注的 AI 模式，保留事实和论证
Step 3. Pass 2 — 注灵魂：问"这还像 AI 写的吗？"，列出残留痕迹，再改一遍
Step 4. 评分  — 给最终版评分，输出变更日志
```

Pass 2 是关键。Pass 1 去掉 AI 模式后，文字往往变得干净但无聊——均匀的句长、中立的陈述、完美的结构。这种"无菌文"和 AI slop 一样容易被识别，只是被不同的检测器识别。

Do not add new content that doesn't exist in the original. Do not inject opinions the author didn't express. Avoid over-correcting formal technical writing into casual blog tone.

## 核心模式（Tier 1 — 最强 AI 信号）

每个命中扣 3 分。在中文技术写作中最常见的：

| # | 模式 | 典型表现 | 修复 |
|---|------|---------|------|
| 1 | AI 词汇 | delve, tapestry, landscape(抽象), interplay, foster, garner, pivotal, showcase, underscore | 换成普通词。"showcase" → 去掉，句子本身就在展示 |
| 2 | 意义膨胀 | "marks a pivotal moment", "is a testament to", "setting the stage for" | 说具体发生了什么。不加评价 |
| 3 | Copula 回避 | "serves as", "stands as", "functions as", "operates as" | 用 "is"。信任简单动词 |
| 4 | 负面并行 | "It's not just X, it's Y", "Not merely A, but B", "goes beyond X to Y" | 直接说 Y。跳过 "not X" 的铺垫 |
| 5 | -ing 伪分析 | "highlighting...", "showcasing...", "ensuring...", "reflecting..." | 砍掉。如果解释有价值，写成独立句子并加来源 |
| 6 | 推广语言 | "vibrant", "groundbreaking", "nestled", "breathtaking", "stunning" | 换成具体描述。什么让它 "groundbreaking"？说那个 |
| 7 | 聊天残留 | "I hope this helps!", "Let me know if...", "Great question!" | 删除 |

## 核心模式（Tier 2 — 中等 AI 信号）

每个命中扣 2 分：

| # | 模式 | 修复 |
|---|------|------|
| 8 | 模糊归因 | "experts argue", "studies show", "industry reports suggest" → 点名，否则删掉 |
| 9 | 三的规则 | 强制凑三个 → 有几个写几个 |
| 10 | 同义轮换 | 同一个事物换 3 种叫法 → 选一个用到底 |
| 11 | 虚假范围 | "from X to Y" 但 X、Y 不在同一刻度上 → 列出实际内容 |
| 12 | 公式化挑战 | "Despite X... continues to thrive" → 说具体挑战和具体应对 |
| 13 | 过度 hedging | "could potentially possibly" → 说 "may" 或直说 |
| 14 | 通用结尾 | "the future looks bright", "exciting times ahead" → 给具体下一步 |
| 15 | em dash 过度 | 一段 3+ 个 em dash → 用句号或逗号 |
| 16 | 粗体过度 | 机械地加粗关键词 → 只在真正需要强调时用 |
| 17 | 竖列表带粗体标题 | `- **X:** description` 格式 → 写成段落，或用简单列表 |
| 18 | 权威伪装 | "the real question is", "at its core", "what really matters" → 直接说 |
| 19 | 路标预告 | "let's dive in", "let's explore", "here's what you need to know" → 删，直接开始 |
| 20 | 断裂标题 | 标题后跟一句话重述标题 → 删重述，直接进入内容 |

## 结构性 AI 模式（Tier 3 — 需要全文视角才能发现）

单独看每段都没问题，放在一起就暴露了。每个命中扣 1.5 分：

| # | 模式 | 表现 | 修复 |
|---|------|------|------|
| 21 | 重复定位语 | 同一个卖点（"不是框架"、"只管执行层"）出现 3+ 次 | 第一次说清楚，后面用短指代（"harness"、"这套东西"） |
| 22 | 平行段落结构 | 连续 3+ 段使用完全相同的展开模式（每段都是"场景→根因→方案"） | 至少一段打破模式——有的只说问题不给方案，有的从方案倒推问题 |
| 23 | 自问自答过密 | 连续 3+ 个"X？Y。"句式（"代价是什么？文件 I/O 慢。"） | 每 500 字最多 1 个自问自答，其余改成陈述 |
| 24 | 段末格式化引用 | 每段末尾都是 "→ Pattern X.Y Name" 或 "详见 §3.2" | 有些自然过渡到方案，有些就停在问题上 |
| 25 | 情感平坦 | 全文零个人感受、零犹豫、零意外 | 至少 2-3 处注入真实反应（"第一次遇到时很恼火"、"解法朴素到有点丢人"） |
| 26 | 解说员语气 | 每个概念都按"是什么→为什么→代价"三段展开 | 有些只说结论不解释，有些深入展开，节奏不均匀 |

这些模式是 Pass 1 无法检测的——需要在 Pass 2 用全文视角扫描。单段去 AI 味之后如果全文结构仍然对称，整篇文章照样一眼 AI。

## 中文特有 AI 模式

| 模式 | 典型 | 修复 |
|------|------|------|
| 四字堆砌 | "高效协同、智能赋能、敏捷迭代" | 每个四字词展开成具体的事 |
| 被动过多 | "已被成功实施"、"已被采纳" | "我们把 X 降到了 Y"、"团队选了方案 B" |
| 无意义总分总 | "下面从三个方面...综上所述..." | 直接说最重要的，其他自然带出 |
| 过度谦虚 | "一些微小的尝试"、"抛砖引玉" | 实事求是。做了什么就说什么 |
| 过度热情开头 | "我们很高兴地宣布..."、"我们激动地分享..." | 直接说做了什么，因为什么 |
| 企业套话 | "赋能开发者"、"最佳实践"、"无缝集成" | 说具体做法 |

## 灵魂注入（Pass 2 的核心）

去完模式后做两层检查：

**句级（逐段）：**
- **节奏变化了吗？** 连续 3 句同样长度 → 打断。短句、长句交替。有些段落只有一句话
- **有观点吗？** 纯中立陈述 → 加一句反应。"这个数据让我们放弃了方案 A"
- **有具体感受吗？** "this is concerning" → "有个事一直困扰我们：指标在涨，但没人能说清为什么"

**篇级（全文鸟瞰）：** 这层是 Pass 2 最容易漏的
- **段落结构对称吗？** 连续 3+ 段用同一种展开方式 → 至少一段打破模式
- **同一个定位语说了几遍？** 3+ 次 → 第二次之后换简短指代
- **自问自答数了吗？** 全文超过 5 个 → 砍到 3 个以内
- **情绪有波动吗？** 全文零个人感受 → 注入 2-3 处真实反应
- **结尾在总结吗？** → 删总结。换成新角度、具体行动、或未解决的问题

### 语气校准

| 场景 | 定位 | 证据优先级 |
|------|------|-----------|
| 技术分享 | 懂行的同行 | 代码示例 > 性能数据 > 真实案例 |
| 愿景方案 | 有实践支撑的建设者 | 前后对比 > 真实案例 > 回应质疑 |
| 教程 | 犯过错的过来人 | 可运行示例 > 预期输出 > 常见坑 |

技术文章的灵魂是技术本身——代码、数据、架构图、失败案例。不是语气和情绪。

### Voice Calibration（可选）

如果用户提供了自己的写作样本，先分析：
- 句长模式（短而有力？长而流畅？混合？）
- 用词层级（口语？学术？中间？）
- 段落开头习惯
- 标点偏好（em dash 多？括号多？分号？）
- 过渡方式（显式连接词？直接进下一个点？）

然后用样本的模式替换 AI 模式，而不是用通用的"人味"替换。

## 禁用词表

| 禁用 | 替代 |
|------|------|
| 革命性/颠覆性 | 说具体改变了什么 |
| 赋能/empowering | 说具体让谁能做什么 |
| 无缝/seamless | 说具体集成步骤 |
| 前沿/cutting-edge | 说具体用了什么技术 |
| 最佳实践 | 说具体做法 |
| 驱动创新 | 说具体创新了什么 |
| 释放潜力/unlock | 说具体获得了什么能力 |
| 范式/paradigm | 说具体方法 |
| 协同/synergy | 说具体怎么配合 |

## 评分（0-10）

| 分段 | 含义 |
|------|------|
| 0-3 | 明显 AI（多个 Tier 1 命中，机械结构） |
| 4-5 | AI 痕迹重（有人味但需要大改） |
| 6-7 | 混合（可能 AI 可能人，缺强烈声音） |
| 8-9 | 像人写的（自然声音，极少模式残留） |
| 10 | 和熟练写手无法区分 |

## 输出格式

```
原始评分: X/10
模式: text | 深度: standard

--- PASS 1 重写 ---
[去模式版本]

--- 残留 AI 痕迹 ---
- [简要列出]

--- PASS 2 最终版 ---
[注入灵魂版本]

最终评分: Y/10

变更日志:
- 删除了 N 个 hedging 短语
- 替换了 N 个 AI 词汇
- 修复了 N 个结构模式
- 加入了 N 个具体示例
```

## 自检清单

发布前逐条过：

1. **人会这么说话吗？** 不会就重写
2. **每个声明有证据吗？** 没有就加数据或删掉
3. **这句话放到任何公司的博客都成立吗？** 是就太通用了
4. **开头是热情还是信息？** 用信息开头
5. **结尾在总结还是在延伸？** 删总结，换延伸
6. **这个过渡可以删吗？** 可以就删

## Related

`@doc-gen` 文档生成 | `@deep-research` 调研报告 | `@human-writing` 中文写作参考

## References

- 完整模式目录（29+ 模式详解和示例）: `references/full-pattern-catalog.md`
- 中文 AI vs 人味写作对比示例: `references/writing-patterns-zh.md`
- 场景语气指南和快速修复清单: `references/tone-guide.md`
