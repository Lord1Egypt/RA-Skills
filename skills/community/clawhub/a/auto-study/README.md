[English](README.md) | [简体中文](README.zh-CN.md)

# Auto-Study

[![Skill](https://img.shields.io/badge/Type-Agent%20Skill-0f766e)](auto-study/SKILL.md) [![Runtime](https://img.shields.io/badge/Runtime-Windows%20%7C%20WSL%20%7C%20macOS-2563eb)](#default-configuration) [![Browser](https://img.shields.io/badge/Browser-Google%20Chrome-4285F4?logo=googlechrome&logoColor=white)](https://www.google.com/chrome/) [![License](https://img.shields.io/github/license/AmiracleTa/Auto-Study-Skill)](LICENSE)

The Auto-Study skill is an agent skill for **web-based learning platforms** such as **Yuketang**, **Xuexitong**, **pintia**, and other **question-answering scenarios**.

It teaches the agent to use learning platforms in a browser, read text or images, return answers, choose options, fill in blanks, and carry out similar actions. It uses a separate browser profile to preserve login state, reduce potential security risks, and support background execution.

It currently supports **Windows**, **WSL**, and **macOS**. Browser support is limited to **Google Chrome**. When used from **WSL**, it should drive **Google Chrome on Windows**.

## Preview

**Yuketang**

`user: Finish these 50 OOP-6 questions, but don't submit them yet`

[Preview](https://github.com/user-attachments/assets/43711b7f-937f-4b95-a277-0847b9b8d996)

**Xuexitong**

`user: Open Xuexitong`

`user: Finish the chapter quizzes for 10.1-10.5 and submit them directly`

> *wait for some time...*

`agent:`

```text
The chapter quizzes for 10.1 - 10.5 are all completed and submitted.
- 10.1: 100
- 10.2: 100
- 10.3: 100
- 10.4: 100
- 10.5: 100

I also saved the screenshots and answer records for each section:
- workspace/auto-study/xuexitong/10.1-以法治为重器：法治的价值定位/record.md
- workspace/auto-study/xuexitong/10.2-以系统为谋划：法治的推进战略/record.md
- workspace/auto-study/xuexitong/10.3-以世界为方法：法治的世界结构（上）/record.md
- workspace/auto-study/xuexitong/10.4-以世界为方法：法治的世界结构（下）/record.md
- workspace/auto-study/xuexitong/10.5-以中国为目的：法治的中国语境/record.md
```

> Auto-generated markdown with captured questions, answer analysis, and recorded scores.

<img width="800" alt="Image" src="https://github.com/user-attachments/assets/ea38471f-27d3-40d6-8d06-c9f82a31aea1" />

**Other usage examples**

`user: Give me the answers for the 4.1 chapter quiz`

`user: Briefly analyze each question`

## Install the Skill

### Let your agent handle it

Just tell your agent: `Help me install this skill, https://github.com/AmiracleTa/Auto-Study-Skill`

---

### Manual Installation

#### Copy the repository

Copy the `auto-study` folder from this repository into your agent's `skills` folder.

**OpenClaw:** `~/.openclaw/workspace/skills`

**Codex:** `~/.codex/skills`

#### Install dependencies

- Google Chrome (Windows or macOS)
- [Agent Browser CLI](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill](https://clawhub.ai/MaTriXy/agent-browser-clawdbot)

## Behavior

- By default, it returns answers directly without extra explanation.
- Unless explicitly requested, it does not submit automatically after finishing.

For detailed strategy, see [auto-study/SKILL.md](auto-study/SKILL.md).

## Default Configuration

- CDP port: `9344`
- Profile root directory on Windows: `%LOCALAPPDATA%\AutoStudy\browser`
- Profile root directory on macOS: `~/Library/Application Support/AutoStudy/browser`

## Workflow

1. Start or connect to Chrome using a dedicated CDP port
2. Read the browser page and current state
3. Perform the requested actions according to the user's instructions

## Detailed Strategy

- [auto-study/SKILL.md](auto-study/SKILL.md) Core strategy
- [auto-study/references/xuexitong.md](auto-study/references/xuexitong.md) Xuexitong-specific strategy
- [auto-study/references/zhihuishu.md](auto-study/references/zhihuishu.md) Zhihuishu-specific strategy
- [auto-study/references/yuketang.md](auto-study/references/yuketang.md) Yuketang-specific strategy
- [auto-study/references/pintia.md](auto-study/references/pintia.md) pintia-specific strategy
- [auto-study/references/runtime-windows.md](auto-study/references/runtime-windows.md) Windows runtime instructions
- [auto-study/references/runtime-wsl.md](auto-study/references/runtime-wsl.md) WSL runtime instructions
- [auto-study/references/runtime-macos.md](auto-study/references/runtime-macos.md) macOS runtime instructions

## Acceptable Use

When using this skill, you are responsible for ensuring compliance with applicable laws and regulations, school or institutional rules, and platform terms of service.

This skill is designed for: **learning, ordinary quizzes, and browser-based answering assistance**

Do not use it for **formal exams, bypassing technical restrictions, or any other disallowed automation**.

---

***AI is not a human. Use auto-submit with caution.***
