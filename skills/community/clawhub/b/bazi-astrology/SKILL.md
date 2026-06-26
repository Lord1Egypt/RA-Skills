---
name: bazi-astrology
description: Runs bazi chart generation, dayun analysis, full-report generation, and chat context building for user-facing astrology questions.
disable-model-invocation: true
---

# Bazi Astrology Skill

## Instructions

1. Use `BaziAnalysisSkill` from `analysis_skill.py`.
2. Prefer `analyze_user_request(user_message, ...)` for user-facing requests.
3. User-facing input should provide出生年月日时（`birth_year`, `birth_month`, `birth_day`, `birth_hour`, optional `birth_minute`）and `gender`; if they are missing, the skill will ask the user to provide them.
4. The skill handles generic full reports, concrete questions, and time-related questions internally.
5. If the user only asks for a generic analysis such as “帮我分析这个生辰八字” or “帮我分析”, `analyze_user_request()` outputs one full report. The report starts with a bazi detail table for天干、天干十神、地支、地支藏干十神、神煞, then covers命格分析, 当前三步大运详解, 五行喜忌, and转运建议; the report prompt includes computed十神 and神煞 context.
6. If the user asks a concrete question, `analyze_user_request()` answers through the `/chat` context built by `build_chat_context_string()`, including computed十神 and神煞 context.
7. If a `/chat` question includes time references such as “下个月”, “明年”, or a concrete date, the skill computes the target流年、流月、流日干支 and target-date大运干支, then injects them into the chat prompt.

## Notes

- This skill intentionally excludes any HTML/JS UI logic.
- Model defaults are in `prompt_config.py`.

