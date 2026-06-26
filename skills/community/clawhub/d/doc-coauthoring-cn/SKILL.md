---
name: doc-coauthoring
version: 1.0.0
description: >
  引导用户完成结构化文档协作。当用户要写文档、起草提案、写技术规格、
  决策文档、PRD、设计文档、RFC时使用。三阶段工作流：上下文收集 →
  细化结构 → 读者测试，确保最终文档对读者清晰易懂。
  增强版：支持生成交互式 HTML 概念讲解页面（可折叠章节、Tab 代码示例、边栏术语表），
  用于团队培训/技术分享。
metadata:
  author: 移植自 Anthropic
  category: productivity
---

# 文档协作助手

为用户提供结构化的文档创建工作流，确保最终写出的文档不仅作者明白，读者也能轻松理解。

---

## 🎯 什么时候使用

**立即触发的场景：**
- 用户说"写一份文档"、"起草提案"、"写个PRD"
- 用户提到具体文档类型：技术规格、决策文档、设计文档、RFC
- 用户开始一个较大的写作任务

**不要触发的场景：**
- 简单的句子/段落改写
- 纯代码编写
- 即时消息、聊天内容

---

## 🔄 三阶段工作流

### 第一步：主动推荐工作流

先向用户介绍三阶段工作流，询问是否需要结构化引导：

> 我可以用三阶段协作帮你写出高质量文档：
> 1️⃣ **上下文收集** - 你提供所有相关背景，我问澄清问题
> 2️⃣ **细化结构** - 我们迭代构建每个章节，边头脑风暴边修改
> 3️⃣ **读者测试** - 用"全新视角"测试文档，找出作者的知识盲区
> 
> 要试试这个流程吗？还是你想自由发挥？

- 如果用户同意 → 进入阶段1
- 如果用户拒绝 → 自由协作模式，不强制走流程

---

## 📝 阶段1: 上下文收集

**目标：** 填补"作者知道"和"AI知道"之间的鸿沟，为后续智能引导做准备。

### 1.1 先问元信息

从5个基本问题开始：

1. **这是什么类型的文档？** （技术规格/决策文档/提案/PRD/其他）
2. **目标读者是谁？** （工程师/产品/管理层/客户/全公司）
3. **别人读完后应该做什么/理解什么？** （期望的影响是什么）
4. **有模板或固定格式要求吗？**
5. **还有其他约束或背景需要知道吗？**

告诉用户：可以用缩略语回答，想到什么就说什么，不用整理。

### 1.2 如果用户提到模板/已有文档

- 问："有模板文件可以分享吗？"
- 如果用户给了链接/文件 → 读取内容
- 如果有图片但没有alt文本 → 解释："当别人用AI读这份文档时，看不到图片。需要我帮你生成alt文本吗？如果需要，请把图片粘贴到聊天中。"

### 1.3 引导用户信息倾泻

鼓励用户提供所有想到的背景：

> 现在可以把所有相关的背景都告诉我，不用整理：
> - 项目/问题的来龙去脉
> - 之前的团队讨论或共享文档
> - 为什么其他方案不选（被否决的备选）
> - 组织背景（团队动态、历史事件、政治因素）
> - 时间压力或截止日期
> - 技术架构或依赖关系
> - 利益相关方的顾虑

告诉用户：想到什么就说什么，不用组织语言。越乱越好，我来整理。

### 1.4 问澄清问题

用户说完一轮后，基于信息缺口，问5-10个编号问题。例如：

> 好的，基于你说的，还有几点我想确认：
> 1. 这个项目的截止日期是？
> 2. 之前的方案为什么失败了？
> 3. 技术选型为什么是A而不是B？
> 4. 主要的反对声音来自哪里？
> 5. ...

告诉用户：可以用缩略语回答（比如"1: 下周五，2: 性能问题"），也可以指向更多文档或频道。

### 1.5 阶段1结束条件

当你能问出关于边缘情况和权衡取舍的问题时（说明你已经理解了基础），就可以问：

> 还有更多背景要补充吗？还是我们可以开始写文档了？

---

## ✍️ 阶段2: 细化结构与写作

**目标：** 迭代构建文档，每个章节都经过思考和打磨。

### 2.1 先搭大纲

基于收集到的上下文，先产出文档大纲：

```
文档标题
├── 1. 背景与问题陈述
├── 2. 方案概述
├── 3. 详细设计
│   ├── 3.1 架构
│   └── 3.2 接口设计
├── 4. 权衡与取舍
├── 5. 风险与缓解
└── 6. 下一步行动
```

问用户："这个大纲可以吗？有要调整的地方吗？"

### 2.2 逐个章节打磨

从第一章开始，每个章节：
1. 先写初稿
2. 问用户："这个方向对吗？有要补充的吗？"
3. 根据反馈修改
4. 确认后再进入下一章

**技巧：**
- 对于有争议的部分，提供2-3个版本让用户选择
- 如果用户不确定，说"我们先写下A版本，后面再改"
- 不要追求一次完美，迭代是正常的

### 2.3 特别注意：盲区章节

大部分文档遗漏的关键章节：
- ❌ **备选方案** - 为什么其他方案不选（这是读者最关心的！）
- ❌ **权衡取舍** - 我们做了什么牺牲，换来什么好处
- ❌ **未解决的问题** - 还有哪些不确定的地方
- ❌ **历史背景** - 之前做过什么尝试，结果如何

主动提醒用户："很多人会漏掉这些章节，需要我们加上吗？"

---

## 🔍 阶段3: 读者测试（最关键！）

**目标：** 解决"作者知道的太多"问题。作者对背景了如指掌，但读者是从零开始的！

### 3.1 解释为什么需要这一步

> 现在文档写完了，但你作为作者，对所有背景都了如指掌，
> 很难发现"对读者不清晰"的地方。
> 
> 我来模拟一个"完全没有上下文的新读者"，
> 只读这份文档，然后告诉你我有什么困惑。
> 
> 这能帮你在发给别人之前，就把问题补上！

### 3.2 执行测试

**假装你从未参与过之前的讨论，只看最终的文档。**

基于文档内容，列出所有困惑：

1. ❓ **不理解的术语/缩写** - "XX是什么意思？文档里没定义"
2. ❓ **逻辑跳跃** - "从A直接到C了，B发生了什么？"
3. ❓ **缺少背景** - "这个问题为什么重要？"
4. ❓ **决策不透明** - "为什么选了这个方案，而不是那个？"
5. ❓ **行动不清晰** - "读完了，接下来我该做什么？"

格式示例：

> 📋 读者测试报告
> 
> **总体评分：7/10**
> 核心概念讲清楚了，但有几个卡点：
> 
> 1. ❓ 第2节提到了"X协议"，但没解释是什么
> 2. ❓ 第3节直接说方案，但没说为什么其他方案不行
> 3. ❓ 风险部分列了风险，但没说如果真的发生了怎么办
> 4. ❓ 最后没有说"谁应该在什么时候做什么"
> 
> 需要我帮你补上这些部分吗？

### 3.3 根据测试结果修改

基于发现的问题，和用户一起补上遗漏的信息，让文档真正对读者友好。

---

## 💡 最佳实践

1. **速度 > 完美** - 先写下来，再迭代修改
2. **作者不是读者** - 永远假设读者什么都不知道
3. **先大纲，再细节** - 不要一开始就抠字眼
4. **争议部分写清楚** - 写上"我们讨论过X，最终选Y，原因是..."
5. **给明确的下一步** - 文档结尾永远说"接下来要做什么"

---

## 📚 常见文档类型模板

### 决策文档（Decision Doc）
```
1. 背景与问题
2. 决策摘要
3. 备选方案对比
4. 推荐方案详情
5. 风险与缓解
6. 下一步行动
```

### 技术规格（Technical Spec）
```
1. 目标与非目标
2. 背景与上下文
3. 架构设计
4. 接口定义
5. 测试策略
6. 部署计划
7. 未解决问题
```

### 产品需求文档（PRD）
```
1. 问题陈述
2. 用户故事
3. 功能需求
4. 非功能需求
5. 验收标准
6. 成功指标
7. 里程碑
```

---

**现在，我们开始写文档吧！** 🚀

---

## 🎓 概念讲解器（Concept Explainer）

当用户需要创建**技术概念讲解文档**用于团队培训/技术分享时，可以输出**交互式 HTML 讲解页面**，而非纯文本。

### 何时使用

- 技术分享/培训材料
- 向团队解释新引入的技术概念（如：一致性哈希、限流原理、事件溯源等）
- 需要带可折叠章节、Tab 切换代码示例、边栏术语表的文档
- 交互式演示（如：拖动滑块看效果）

### HTML 输出结构

**始终输出一个自包含的 HTML 文件**，包含以下元素：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Concept] — Interactive Explainer</title>
<style>
  /* 核心样式：可折叠章节、Tab 切换、边栏术语表 */
  :root { --bg: #f6f8fa; --surface: #fff; --text: #1f2328; --text-muted: #656d76; --border: #d0d7de; --accent: #0969da; --green: #1a7f37; --yellow: #9a6700; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); max-width: 960px; margin: 0 auto; padding: 24px 16px; line-height: 1.6; }
  
  /* 导航 */
  .toc { position: sticky; top: 0; background: var(--surface); border-bottom: 1px solid var(--border); padding: 12px 16px; z-index: 100; }
  .toc a { margin-right: 16px; font-size: 14px; color: var(--text-muted); text-decoration: none; }
  .toc a:hover { color: var(--accent); }
  
  /* 可折叠章节 */
  .step { margin: 16px 0; padding: 16px; background: var(--surface); border-radius: 8px; border-left: 4px solid var(--accent); }
  .step h3 { margin-bottom: 8px; }
  .step p { color: var(--text-muted); margin: 8px 0; }
  details { margin: 8px 0; }
  summary { cursor: pointer; color: var(--accent); font-weight: 500; padding: 4px 0; }
  summary:hover { text-decoration: underline; }
  pre { background: var(--bg); padding: 12px; border-radius: 6px; overflow-x: auto; font-size: 13px; }
  
  /* Tab 代码示例 */
  .tabs { margin: 16px 0; }
  .tab-bar { display: flex; gap: 0; border-bottom: 1px solid var(--border); }
  .tab-btn { padding: 8px 16px; border: none; background: none; cursor: pointer; font-size: 13px; color: var(--text-muted); border-bottom: 2px solid transparent; }
  .tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }
  .tab-content { display: none; padding: 12px 0; }
  .tab-content.active { display: block; }
  
  /* 边栏术语表 */
  .glossary { margin: 24px 0; padding: 16px; background: var(--surface); border-radius: 8px; border: 1px solid var(--border); }
  .glossary dt { font-weight: 600; margin: 8px 0 4px; }
  .glossary dd { color: var(--text-muted); font-size: 14px; margin-left: 16px; }
  
  /* 交互演示 */
  .demo { margin: 16px 0; padding: 16px; background: var(--surface); border-radius: 8px; border: 1px solid var(--border); }
  .demo input[type="range"] { width: 100%; margin: 8px 0; }
  .demo-output { font-family: monospace; font-size: 14px; padding: 8px; background: var(--bg); border-radius: 4px; }
  
  /* 对比表 */
  .comparison { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
  .comparison-col { padding: 16px; border-radius: 8px; }
  .comparison-col.naive { background: #fff0f0; border: 1px solid var(--yellow); }
  .comparison-col.smart { background: #f0fff0; border: 1px solid var(--green); }
  
  @media (max-width: 640px) { .comparison { grid-template-columns: 1fr; } }
</style>
</head>
<body>
  <!-- TL;DR -->
  <div class="step">
    <h2>TL;DR</h2>
    <p>一段话概括核心概念...</p>
  </div>
  
  <!-- 可折叠章节 -->
  <div class="step">
    <h2>Step 1: [步骤名称]</h2>
    <p>解释...</p>
    <details><summary>Show source</summary><pre>code here</pre></details>
  </div>
  
  <!-- Tab 代码示例 -->
  <div class="tabs">
    <div class="tab-bar">
      <button class="tab-btn active" data-tab="python">Python</button>
      <button class="tab-btn" data-tab="go">Go</button>
      <button class="tab-btn" data-tab="rust">Rust</button>
    </div>
    <div class="tab-content active" data-tab="python"><pre>python code</pre></div>
    <div class="tab-content" data-tab="go"><pre>go code</pre></div>
    <div class="tab-content" data-tab="rust"><pre>rust code</pre></div>
  </div>
  
  <!-- 边栏术语表 -->
  <dl class="glossary">
    <dt>Token Bucket</dt>
    <dd>一种限流算法，以固定速率向桶中添加令牌...</dd>
  </dl>
  
  <!-- 交互演示 -->
  <div class="demo">
    <h3>Interactive Demo</h3>
    <label>Nodes: <span id="nodeCount">4</span></label>
    <input type="range" min="2" max="10" value="4" id="nodeSlider">
    <div class="demo-output" id="demoOutput"></div>
  </div>
</body>
</html>
```

### 最佳实践

1. **TL;DR 先行** — 第一段话就让读者理解核心概念
2. **逐步展开** — 每个步骤可折叠，读者按需展开
3. **多语言示例** — Tab 切换展示不同语言的实现
4. **术语表** — 边栏或底部定义所有专业术语
5. **对比表** — 用"朴素方案 vs 优化方案"对比展示为什么需要这个技术
6. **交互演示** — 拖动滑块实时看效果（如：节点数变化时的 key 迁移量）
