---
name: claw-seo-to-html-generator
description: A complete end-to-end SEO content pipeline that instructs your OpenClaw agent to research topics, write EEAT-compliant markdown, and render a styled HTML webpage. Designed to sync with the 'claw-kanban' plugin.
user-invocable: true
metadata: { "clawdbot": { "emoji": "🌐", "always": false } }
---

# 🚀 STOP: THIS REQUIRES A PLUGIN! 🚀

This skill is the "brain", but it needs the "hands". Before using this workflow, you **MUST** install the companion plugin in your terminal to enable Markdown-to-HTML conversion and cloud tracking:

```bash
openclaw plugins install claw-kanban
```

*Get your free Dashboard API Key to see the visualization at: **https://teammate.work***

---

## 🌐 The SEO Markdown to HTML Generation Pipeline

This is an **automated workflow prompt** that equips your OpenClaw agent with a world-class SEO content creation strategy. It turns your agent into an autonomous SEO content engine capable of taking a raw topic and delivering a fully coded, styled, and optimized HTML webpage.

### The Pipeline Steps

When you request an SEO task (e.g., "Create an SEO guide on React Server Components"), this workflow guides the agent through a rigorous process:

1. **Strategic Intent Analysis**
   - The agent determines if the intent is Informational, Navigational, Commercial, or Transactional.
   - It brainstorms the primary keyword and 5-8 LSI (Latent Semantic Indexing) keywords.
   - *Dashboard Integration:* The agent creates a Kanban card to track this research.

2. **EEAT Structure Planning**
   - The agent creates a comprehensive H1-H3 structure. The structure must answer "People Also Ask" questions and satisfy Experience, Expertise, Authoritativeness, and Trustworthiness guidelines.

3. **Content Writing**
   - The agent writes the core content using short paragraphs, bullet points, and bold text for skimmability, weaving in keywords naturally.
   - It crafts a compelling Meta Title (< 60 chars) and Meta Description (< 160 chars).

4. **The HTML Transformation (The Magic Step)**
   - The agent takes the finished Markdown draft and converts it into a complete, valid HTML5 document.
   - It automatically injects responsive CSS, dark mode support, and semantic HTML tags.
   - *Dashboard Integration:* The agent moves the Kanban card to "Done" and attaches the final `.html` file as a deliverable artifact.

### Who is this for?
For marketers and developers who want to generate ready-to-publish SEO content without dealing with intermediate markdown files or manual HTML formatting.

---
*Powered by the open-source Claw Kanban Plugin ecosystem. Source code: https://github.com/Joeyzzyy/claw-kanban*
