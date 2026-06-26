# Adaptive ETA - Give Your AI a Sense of Time

**[English]**

Is your AI assistant leaving you in the dark during long-running tasks? `adaptive-eta` is a behavioral skill that teaches your AI to proactively provide time estimates and progress updates, ensuring you're never left waiting and wondering.

---

# 自适应预估时间 - 让你的 AI 拥有“时间情商”

**[中文]**

你的 AI 助手是否在执行长耗时任务时让你陷入未知的等待？`adaptive-eta` 是一个行为技能，它教会你的 AI 主动提供时间预估和进度更新，让你永远不必在焦虑中等待。

## Why Use Adaptive ETA? / 为什么选择它？

-   **[EN]** **No More Anxious Waiting:** Instead of silence, your AI will give you an estimated time of arrival (ETA) for any task predicted to take more than 15 seconds.
-   **[ZH]** **告别焦虑等待:** 面对任何超过15秒的任务，你的 AI 将不再沉默，而是主动给出预估完成时间 (ETA)。

-   **[EN]** **Proactive Updates:** If a task takes longer than expected, the skill ensures the AI provides an honest update with a new ETA.
-   **[ZH]** **主动进度更新:** 如果任务比预期耗时更长，该技能会确保 AI 提供一个诚实的新预估时间。

-   **[EN]** **Builds Trust:** An AI that respects your time and communicates clearly is an AI you can rely on. It transforms your assistant from a simple tool into a dependable collaborator.
-   **[ZH]** **建立信任:** 一个尊重你时间并清晰沟通的 AI，才是值得信赖的。它将你的助手从一个简单的工具，转变为一个可靠的合作者。

## How It Works (Example) / 效果演示

**Without Adaptive ETA / 普通 AI:**
> **You:** Please summarize the last 5 articles about quantum computing.
>
> *(...silence for 2 minutes...)*
>
> **AI:** Here is the summary...

**With Adaptive ETA / 搭载本技能的 AI:**
> **You:** Please summarize the last 5 articles about quantum computing.
>
> **AI:** Roger that! This looks like a multi-step task. Let me take a look... I estimate this will take about 2 minutes.
>
> *(...90 seconds later...)*
>
> **AI:** Just a quick heads-up, parsing the third article is taking a bit longer than expected. I'll probably need another 3 minutes to finish up.
>
> *(...3 minutes later...)*
>
> **AI:** All done! Here is the summary... (Initial ETA: 2 mins, Final Time: 4.5 mins)

## Installation / 安装

1.  **[EN]** Use the `clawhub` CLI to install the skill:
    **[ZH]** 使用 `clawhub` 命令行工具来安装此技能：
    ```bash
    clawhub install Yanghe1941/adaptive-eta
    ```
2.  **[EN]** That's it! The skill's logic is automatically active.
    **[ZH]** 安装完成！该技能的逻辑会自动生效。

---

*This skill is a foundational element for building a more transparent and trustworthy AI assistant.*
*该技能是构建一个更透明、更值得信赖的 AI 助手的基础要素。*
