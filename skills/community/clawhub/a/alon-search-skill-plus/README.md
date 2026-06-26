[简体中文](./README.zh.md)

# Alon Search Skill Plus

Search agent skills across trusted directories, ClawHub, and GitHub adaptation candidates with explicit source ranking and security filtering.

## Quick Install

```bash
npx skills add alondotsh/alon-skills --skill alon-search-skill-plus
```

## When to Use

Use this skill when a user wants to find an existing skill before building one from scratch.

Typical prompts:

- `Find me a skill for frontend design`
- `Is there a skill that can generate changelogs?`
- `Search for browser automation skills`
- `Find a skill for publishing Markdown to WeChat`

## What It Does

- searches trusted skill directories first
- expands into ClawHub and GitHub only when needed
- distinguishes ready-to-use skills from adaptable GitHub repositories
- applies minimum quality and safety filters before recommending results
- explains when coverage is limited instead of pretending confidence

## Safety and Limits

- does not treat the open web as a general search target
- treats ClawHub and low-trust aggregators as cautionary sources
- does not present ordinary GitHub code as a ready-to-install skill unless it includes standard skill packaging
- recommends code review before installing lower-trust skills

## Output

The result is a ranked shortlist with:

- search keywords used
- source labels
- star counts and recency where relevant
- safety notes for lower-trust sources
- separate sections for adaptable GitHub repositories

## About Alon

These public skills come from Alon's real daily workflows.

Alon is actively exploring the future of agent skills and is open to connecting with people who want to build useful skills.

- GitHub: https://github.com/alondotsh
- ClawHub: https://clawhub.ai/u/alondotsh
- X: https://x.com/alondotsh
- WeChat Official Account: alondotsh

## License

MIT
