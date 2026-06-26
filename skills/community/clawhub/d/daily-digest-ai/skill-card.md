## Description: <br>
Fetches curated technology RSS feeds, uses an external AI provider to score and summarize articles, and generates a structured daily Markdown digest with translated titles, categories, trend highlights, and visual statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richball876](https://clawhub.ai/user/richball876) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technology readers use this skill to generate a daily RSS digest of recent technical articles, including AI-assisted scoring, summaries, category grouping, trends, and charts. It is intended for technology blog and RSS sources rather than real-time news APIs or non-technical topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends RSS article metadata and generated prompts to the configured external AI provider. <br>
Mitigation: Use a provider and API key approved for the intended environment, and avoid using it for private or sensitive source material. <br>
Risk: The skill can persist an API key and preferences in a local config file for convenience. <br>
Mitigation: Use a dedicated low-limit API key and review or delete ~/.hn-daily-digest/config.json when the digest workflow is no longer needed. <br>
Risk: Generated summaries and trend assessments may be incomplete, stale, or misleading. <br>
Mitigation: Treat the digest as an AI-written triage aid and verify important claims against the original linked articles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richball876/daily-digest-ai) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Digest script](artifact/scripts/digest.ts) <br>
- [Hacker News Popularity Contest 2025](https://refactoringenglish.com/tools/hn-popularity/) <br>
- [Bun runtime](https://bun.sh) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest file with tables, Mermaid charts, ASCII charts, article summaries, plus command and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and an OpenAI-compatible or Gemini API key; can save configuration under ~/.hn-daily-digest/config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
