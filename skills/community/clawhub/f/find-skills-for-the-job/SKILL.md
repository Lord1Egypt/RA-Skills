---
name: find-skills-for-the-job
description: >
  Find skills for the job on SkillPicker (https://skillpicker.xyz).
  Use when the user says "find skills", "find a skill for the job",
  "find skills by work", "which skill should I install", "有没有 skill",
  "推荐一个技能", or names a task, role, tool, or agent (Claude, Cursor, Codex)
  and wants a skill. Do not use it to write a new skill or to decide whether a skill is safe.
license: MIT
metadata:
  version: "1.0.0"
---

# Find skills for the job

SkillPicker (https://skillpicker.xyz) lists Agent Skills by the job: `SKILL.md` packages an agent can load. A listing means the skill text matched work people search for. It is not an endorsement, a security audit, or a promise that the skill still matches its upstream file.

Search the catalog. Do not invent a skill and present it as listed.

## Look up

1. State the job in a few words: a task, a role, a tool, an agent, or an output.
2. Read [references/topics.md](references/topics.md). It is the site's topic catalog: 109 topics, with the English name, the Chinese name, the path, and how many skills are listed. Groups are tasks, roles, tools, agents, outputs, then getting started. Inside a group, stronger search demand comes first. Pick the one path that fits. The file also names two duplicates: Students belongs at `/for/role/students/`, and Excel as an output belongs at `/for/tool/excel/`.
3. Open that topic and use its order. English: `https://skillpicker.xyz` plus the path. Chinese: `https://skillpicker.xyz/zh` plus the path. The first skills are the ones to start with. Direct matches come before possible matches. Rank on the page is fit to the job, not install count.
4. If no topic in the file fits, then search skill descriptions. Fetch `https://skillpicker.xyz/skill-index.en.json`, or `skill-index.zh.json` when the user needs Chinese descriptions. Each row is `{name, path, topicPath, source, description}`. Filter it locally. Do not download `website.json`, and do not use the homepage or the sitemap to discover topics.
5. Open a skill at `https://skillpicker.xyz` plus its `path`. Use the unprefixed `/skill/` URL. Do not fetch `/zh/skill/`, `/es/skill/`, `/ja/skill/`, or `/de/skill/`.
6. Read the GitHub `SKILL.md` linked from that page before you recommend installing. The page excerpt is a snapshot. The upstream file is the current copy.

How the index is built: `https://skillpicker.xyz/about/`. The topic file matches the published site snapshot from 2026-10-09. If that page and the file disagree, trust the page for the skill list and trust the file only for which topic to open.

## Recommend

Give a few matches, not a dump of the index. For each one, name the skill, the `source` (`owner/repo`), the topic URL, and the job it matched.

Say that a listing is a relevance match. Reported installs are a popularity signal only. Tell the user to read the skill's own instructions and requirements before installing.

If nothing in the index fits, say SkillPicker does not list one. Do not fill the gap with a skill from memory and call it a SkillPicker result.

## Install

Install only after the user asks to install. When `source` is `owner/repo`, the command is:

```bash
npx skills add owner/repo@name
```

`name` is the skill name from the index, not the topic slug.
