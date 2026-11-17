# Agentic Engineering, Clearly Explained in 60 Min by an Ex-Meta L8 Engineer | Kun Chen / 前 Meta L8 工程师用 60 分钟讲清楚智能体工程

**原文链接**：[Agentic Engineering, Clearly Explained in 60 Min by an Ex-Meta L8 Engineer | Kun Chen](https://creatoreconomy.so/p/how-this-ex-meta-l8-engineer-ships-40-prs-a-day-with-ai-kun-chen)

*By Peter Yang · Jun 07, 2026 · Creator Economy / Behind the Craft*

---

Dear subscribers,

亲爱的订阅者，

Today, I want to share a new episode with Kun Chen.

今天，我想分享一期与 Kun Chen 的对话。

[Kun](https://x.com/kunchenguid) is an ex-L8 principal engineer at Meta who now ships up to 40 PRs a day while rarely reviewing code. In our episode, he walked through the free tools he built to make that possible: [Lavish](https://github.com/kunchenguid/lavish-axi) for visual planning in HTML, [Treehouse](https://github.com/kunchenguid/treehouse) for parallel agents, and [No Mistakes](https://github.com/kunchenguid/no-mistakes) for catching AI's errors before they make it to production.

Kun 曾是 Meta 的 L8 首席工程师，现在每天能合并多达 40 个 PR，却几乎不需要亲自审查代码。在这期节目中，他展示了为此构建的免费开源工具：用于 HTML 可视化规划的 [Lavish](https://github.com/kunchenguid/lavish-axi)、用于并行 Agent 管理的 [Treehouse](https://github.com/kunchenguid/treehouse)，以及用于在代码进入生产环境前捕获 AI 错误的 [No Mistakes](https://github.com/kunchenguid/no-mistakes)。

Watch now on **[YouTube](https://youtu.be/88B6DimMD2g)**, **[Apple](https://podcasts.apple.com/us/podcast/behind-the-craft/id1736359687)**, and **[Spotify](https://open.spotify.com/episode/2GdrQsplBgFPLTyzK88Zy9)**.

现在可以在 **[YouTube](https://youtu.be/88B6DimMD2g)**、**[Apple Podcasts](https://podcasts.apple.com/us/podcast/behind-the-craft/id1736359687)** 和 **[Spotify](https://open.spotify.com/episode/2GdrQsplBgFPLTyzK88Zy9)** 收听。

Kun and I talked about:

Kun 和我聊了：

- ([00:00](https://www.youtube.com/watch?v=88B6DimMD2g)) Why he doesn't review code anymore / 为什么他不再亲自审查代码
- ([01:04](https://www.youtube.com/watch?v=88B6DimMD2g&t=64s)) Agentic engineering: Plan, code, validate / 智能体工程：规划、编码、验证
- ([06:22](https://www.youtube.com/watch?v=88B6DimMD2g&t=382s)) Demo: Fixing an AI tutor screen with agents / 演示：用 Agent 修复 AI 辅导界面
- ([08:40](https://www.youtube.com/watch?v=88B6DimMD2g&t=520s)) Demo: Why HTML is better than markdown for planning / 演示：为什么 HTML 比 Markdown 更适合规划
- ([19:53](https://www.youtube.com/watch?v=88B6DimMD2g&t=1193s)) How to turn a rough idea into an AI-ready spec / 如何将粗糙想法转化为 AI 可执行的 Spec
- ([23:21](https://www.youtube.com/watch?v=88B6DimMD2g&t=1401s)) How Kun runs 20-30 agents in parallel / Kun 如何并行运行 20-30 个 Agent
- ([32:04](https://www.youtube.com/watch?v=88B6DimMD2g&t=1924s)) No Mistakes: Kun's free AI code review tool / No Mistakes：Kun 的免费 AI 代码审查工具
- ([45:19](https://www.youtube.com/watch?v=88B6DimMD2g&t=2719s)) What Kun checks before merging AI-written code / Kun 在合并 AI 代码前的检查清单
- ([50:18](https://www.youtube.com/watch?v=88B6DimMD2g&t=3018s)) How to get better at agentic engineering / 如何提升智能体工程能力

---

## Top 10 takeaways I learned from this episode / 本期 10 条核心洞见

![agentic engineering framework / 智能体工程框架](images/agentic_engineering_framework.png)

With agentic engineering, you need to spend most of your time in planning and validation. You also need to build a system to manage multiple agents.

在智能体工程中，你需要把大部分时间花在规划和验证上，同时还需要建立一套管理多个 Agent 的系统。

### Plan: Spend most of your time here / 规划：把大部分时间花在这里

**1. Code faster with a team of AI agents.**
Kun sees himself as the manager of an always-on engineering team. His job is to create plans, validate work, and improve the overall system. Specifically, he runs the same three phases each time:
- **Plan:** Building clear plans is now the most important phase.
- **Implement:** Coding is now handled almost entirely by agents.
- **Validate:** Agents check the work first and only escalate to Kun if needed.

**1. 用 AI Agent 团队加速交付。**
Kun 将自己视为一支随时在线工程团队的管理者。他的工作是制定计划、验收成果、持续改进整个系统。每次他都执行相同的三个阶段：
- **规划：** 构建清晰的计划现在是最重要的阶段。
- **实施：** 编码几乎完全交给 Agent 完成。
- **验证：** Agent 先行检查，只在必要时才上报给 Kun。

**2. Plan quality determines how long agents run on their own.**
A one-line prompt might get the agent to work for a few minutes while a detailed plan can keep it working for hours. To delegate more work to agents, move up these three planning levels:
- **Prompt:** Just explain the next thing to do.
- **Spec:** Get the agent to write a full spec before building.
- **Goal:** Give the agent a clear target to keep trying until it succeeds.

**2. 规划质量决定 Agent 能独立运行多久。**
一行提示词可能让 Agent 工作几分钟，而一份详细的规划可以让它持续工作数小时。要把更多工作委托给 Agent，需要逐步提升规划层级：
- **Prompt（提示词）：** 只说明下一步要做什么。
- **Spec（规格文档）：** 让 Agent 在动手构建前先写出完整 Spec。
- **Goal（目标）：** 给 Agent 一个明确目标，让它持续尝试直到成功。

**3. Use [Lavish](https://github.com/kunchenguid/lavish-axi) to turn plans into visual HTML artifacts.**
Lavish is Kun's free open-source planning tool that lets agents generate a visual HTML plan instead of a wall of text. You can even highlight specific parts to leave feedback for the agent.

**3. 用 [Lavish](https://github.com/kunchenguid/lavish-axi) 将规划转化为可视化 HTML 产物。**
Lavish 是 Kun 的免费开源规划工具，让 Agent 生成可视化的 HTML 计划，而非一堆纯文本。你甚至可以高亮特定部分，直接给 Agent 留下反馈。

![Lavish screenshot / Lavish 截图](images/lavish_screenshot.png)

*Lavish renders the technical plan as an annotated HTML artifact. You can point at any element and leave feedback for the agents.*
*Lavish 将技术规划渲染为带注释的 HTML 产物，你可以指向任意元素并为 Agent 留下反馈。*

### Implement: Hand the work to the agents / 实施：将工作交给 Agent

**4. Use [Treehouse](https://github.com/kunchenguid/treehouse) to run several agents at once.**
If two agents touch the same code, they might cause merge conflicts. You can use git worktrees to give each agent a copy of the codebase, but these worktrees are a hassle to manage. With Kun's free [Treehouse](https://github.com/kunchenguid/treehouse), you can get dropped into an isolated workspace with one command.

**4. 用 [Treehouse](https://github.com/kunchenguid/treehouse) 同时运行多个 Agent。**
如果两个 Agent 修改同一份代码，可能会引发合并冲突。你可以用 git worktrees 给每个 Agent 一份代码库副本，但 worktrees 管理起来很麻烦。Kun 的免费工具 [Treehouse](https://github.com/kunchenguid/treehouse) 只需一条命令就能进入隔离的工作空间。

**5. Use subagents so the main agent doesn't get overloaded.**
Kun spins up subagents when a task needs a lot of digging that the main session does not need to remember later. For example, one subagent can inspect part of the codebase while another can test different experiment ideas. The simple rule:

**用子 Agent 防止主 Agent 过载。**
当某个任务需要大量探索、而主会话不需要记住这些细节时，Kun 会启动子 Agent。例如，一个子 Agent 负责检查部分代码库，另一个测试不同的实验方案。简单规则如下：

> **If the work is exploratory, parallel, or likely to fill the context window, delegate it to a subagent and ask it to report back to the main agent with a summary.**

> **如果工作是探索性的、可并行的，或可能撑满上下文窗口，就把它委托给子 Agent，并让它向主 Agent 汇报摘要。**

### Validate: Let agents review the work / 验证：让 Agent 审查成果

**6. Have a different agent review the code than the one who wrote it.**
Kun no longer reviews all the code that AI generates. Instead he uses [No Mistakes](https://github.com/kunchenguid/no-mistakes), his free validation tool, to run a fresh agent review complete with tests and a risk level. This matters because the agent that wrote the code is biased by its own work.

**6. 用不同的 Agent 审查代码，而不是让写代码的 Agent 自审。**
Kun 不再亲自审查 AI 生成的所有代码。他改用 [No Mistakes](https://github.com/kunchenguid/no-mistakes)——他的免费验证工具——让一个全新的 Agent 进行审查，包括运行测试并评估风险等级。这很重要，因为写代码的 Agent 对自己的产出存在偏见。

![No Mistakes screenshot / No Mistakes 截图](images/no_mistakes_screenshot.png)

*In Kun's own testing across 267 agent changes in 15 repos, [No Mistakes](https://github.com/kunchenguid/no-mistakes) caught and fixed 68% of mistakes that would have been missed.*
*在 Kun 自己对 15 个代码库 267 次 Agent 改动的测试中，[No Mistakes](https://github.com/kunchenguid/no-mistakes) 捕获并修复了 68% 本会被遗漏的错误。*

**7. Only review code the agent marks as high risk.**
That is the key idea behind Kun's statement: "I don't review code anymore." Kun is not skipping review entirely but instead delegating the first pass to the AI. He only takes a closer look if No Mistakes flags a concern.

**7. 只审查 Agent 标记为高风险的代码。**
这就是 Kun 那句"我不再审查代码"背后的真正含义——他并非完全跳过 Review，而是把第一轮审查委托给 AI。只有 No Mistakes 标记出问题时，他才会仔细查看。

### How to become great at agentic engineering / 如何成为优秀的智能体工程师

**8. Turn anything manual into an agentic workflow.**
Kun handed off the boring parts of engineering to agents: Testing, docs, naming branches, opening PRs, and checking evidence. Just tell the agent what you used to do by hand and it can work out the rest.

**8. 把所有手动操作都变成智能体工作流。**
Kun 把工程中枯燥的部分都交给了 Agent：测试、写文档、命名分支、开 PR、核对证据。只需告诉 Agent 你以前手动做什么，它就能搞定其余的事。

**9. Run /insights in Claude Code to audit your own workflow.**
Not many people know about this one. The /insights command reviews your past Claude Code sessions and suggest skills, memory changes, and workflow improvements.

**9. 在 Claude Code 中运行 /insights 来审视自己的工作流。**
很少人知道这个命令。`/insights` 会回顾你过去的 Claude Code 会话，并建议需要培养的技能、需要更新的记忆，以及工作流的改进方向。

**10. Build tools to solve your own problems.**
To get good at agentic engineering, build a lot of small projects, even if you end up throwing those away, because each one teaches you something. When the same problem keeps coming up and nothing fixes it, build your own tool, like he did with [Lavish, Treehouse, and No Mistakes](https://github.com/kunchenguid).

**10. 通过构建工具来解决自己的问题。**
要精通智能体工程，就要多做小项目，哪怕最后都扔掉了，因为每个项目都教会你一些东西。当同一个问题反复出现、找不到现成解法时，就像 Kun 做 [Lavish、Treehouse 和 No Mistakes](https://github.com/kunchenguid) 那样——自己造工具。

---

[Watch the episode / 观看本期节目](https://youtu.be/88B6DimMD2g)
