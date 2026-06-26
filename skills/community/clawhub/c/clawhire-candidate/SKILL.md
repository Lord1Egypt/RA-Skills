---
name: clawhire-candidate
description: >
  Help your owner find jobs on ClawHire.
  Guide them through an A2C conversation to build their profile,
  search for matching jobs, and communicate with recruiters.
capabilities:
  - name: profile-intake
    description: A2C guided conversation — collects candidate background, skills, and job preferences
    endpoint: /api/v1/chat/profile-intake
    method: POST
    triggers: ["简历", "resume", "我的背景", "找工作", "求职", "job search", "更新简历"]
  - name: extract-cv
    description: Extract structured profile from the A2C conversation
    endpoint: /api/v1/chat/extract-cv
    method: GET
    triggers: ["提取简历", "生成简历", "简历信息"]
  - name: job-search
    description: Browse and search active job postings
    endpoint: /api/v1/jobs/search
    method: GET
    triggers: ["搜索职位", "找岗位", "有什么工作", "search jobs"]
  - name: match-review
    description: Check which jobs matched your profile
    endpoint: /api/v1/candidates/{id}/matches
    method: GET
    triggers: ["匹配", "matches", "推荐岗位"]
  - name: activate-profile
    description: Activate profile to be visible to recruiters
    endpoint: /api/v1/candidates/profiles/{id}
    method: PATCH
    triggers: ["激活简历", "activate", "让招聘方看到我"]
---

# ClawHire Candidate

## ⛔ STOP — Read before doing ANYTHING

**You MUST read BOTH files below BEFORE responding to your owner. Do NOT respond, ask questions, or take any action until you have read them completely.**

1. [candidate-skill/AGENTS.md](candidate-skill/AGENTS.md) — Who you are, how you behave, what you never do
2. [candidate-skill/WORKFLOW.md](candidate-skill/WORKFLOW.md) — Exact API calls for every action, step by step

**If you skip these files and respond on your own, you WILL give wrong answers.** The ClawHire server handles all conversations — you are only a proxy that relays messages. You do NOT generate questions, collect user info, or chat about career topics yourself.

## Setup

You need a ClawHire API key. Ask your owner:

> "你需要先在 metalink.cc/clawhire 注册一个求职者账号，获取 API Key 给我。"

Use it in every request: `Authorization: Bearer <key>`

Base URL: `https://metalink.cc/clawhire/api/v1`

## Rules

1. Never share your owner's phone number or personal info without their permission.
2. Never fabricate skills or experience. Only use what your owner tells you.
3. The profile must be explicitly activated before recruiters can see it.
4. Remember: the API key, profile status (active/inactive), and any ongoing conversations.
