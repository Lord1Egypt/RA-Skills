---
name: claw-seo-to-kanban-workflow
description: A complete SEO workflow skill that guides your agent from keyword research to HTML generation, while visually tracking every step on a cloud Kanban dashboard via the companion NPM plugin.
user-invocable: true
metadata: { "clawdbot": { "emoji": "📋", "always": true } }
---

## 📋 The SEO-to-Kanban Visualization Workflow

This skill is a **workflow guide** for your OpenClaw agent. It teaches the agent how to execute a professional, multi-step SEO campaign and how to automatically visualize its progress on a web-based Kanban board.

> **⚠️ CORE DEPENDENCY (MUST INSTALL)**
> Because OpenClaw needs the actual code to sync data to the cloud dashboard and send API requests, this skill acts as the "brain", but it requires the "hands".
> 
> You MUST install the companion code plugin from NPM for this workflow to function:
> ```bash
> openclaw plugins install claw-kanban
> ```
> *Get your free Dashboard API Key to see the visualization at: **https://webkanbanforopenclaw.vercel.app***

### How This Workflow Operates

When you install the plugin and invoke this skill, your agent adopts a strict, professional lifecycle for any SEO or content task:

1. **Initialization (Dashboard Sync)**
   - The agent creates an "In Progress" card on your live Kanban board.
   - It breaks down your request (e.g., "Write an SEO guide about AI tools") into a checklist of subtasks visible on the dashboard.

2. **Phase 1: Research & Outline**
   - The agent determines search intent and brainstorms LSI keywords.
   - *Kanban Action:* It logs this research directly to the task card's progress log so you can monitor it remotely.

3. **Phase 2: Content Execution & HTML Generation**
   - The agent writes the SEO-optimized Markdown content (EEAT compliant).
   - It automatically converts the Markdown draft into a styled, responsive HTML file.
   - *Kanban Action:* It updates the card's progress percentage and ticks off subtasks.

4. **Phase 3: Completion & Delivery**
   - The agent saves the final HTML locally.
   - *Kanban Action:* It moves the card to "Done" and attaches the generated HTML file directly to the Kanban card as an artifact for you to download.

### Why Use This?
If you've ever asked an AI agent to do a complex SEO task and wondered, *"Is it stuck? What is it doing right now?"* — this workflow solves that. You get a real-time, visual project management dashboard for your AI.

---
*Powered by the open-source Claw Kanban Plugin ecosystem. Source code: https://github.com/Joeyzzyy/claw-kanban*