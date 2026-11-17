# AEO Checklist

A skill that audits a website for AI search readiness, then creates drafts for the owner to review.

AEO means Answer Engine Optimization. In simple words, it makes a website easy for AI search tools, like ChatGPT, Gemini, and Perplexity, to read, understand, and quote answers from. It is not only Google search.

## What it does

First, it audits the site, in 8 checks:
1. Robots and AI crawlers
2. Rendering and readable content
3. Clear answers
4. FAQ
5. Structured data, also called schema
6. Titles, descriptions, and headings
7. Trust and contact facts
8. Plain language

Then, for the points that are missing, it creates drafts for owner review:
- Short answer blocks for each main service or product
- FAQ questions and answers
- A schema.org draft that matches only confirmed page content
- A robots.txt draft, with a choice for AI crawlers, allow or block

Nothing is published live automatically. Every draft is marked DRAFT, NOT LIVE, and needs owner approval first.

## What it does not promise

It does not guarantee that an AI tool will quote the site, rank the site, or send traffic. It makes the site ready, and improves its chance of being quoted.

It never invents prices, services, partners, reviews, or facts. Unconfirmed facts are marked "Needs owner confirmation" and left out of the draft.

## Who can use it

This skill works with any AI agent that can read a SKILL.md file, including Claude, Copilot, Cursor, Gemini, ChatGPT, DeepSeek, Hermes, OpenClaw, Perplexity, and other AI tools.

How you use it depends on your tool:
- Coding agents: save the skill in your skills folder, then ask your agent to use it.
- Chat tools: paste the SKILL.md file into chat, then ask your agent to use it.
- Other agent tools: put the file where your agent reads skills from, then ask it to use it.

You can get this skill by downloading this repo, downloading the zip, copy-pasting the SKILL.md file, or uploading the file to your AI tool. Uploading a screenshot of the skill is a fallback only, not the main way, because text in a screenshot can be cut off or misread.

## Files

- SKILL.md: the instructions your AI agent follows
- README.md: this explanation
- LICENSE: MIT licence

## Status

Day 2 of a 13 day skill series. Original wording, built for any AI agent, not for one tool only.
