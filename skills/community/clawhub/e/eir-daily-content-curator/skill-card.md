## Description:

Daily AI news curation that learns interests from a profile, searches the web, and delivers structured summaries and daily briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyeir](https://clawhub.ai/user/heyeir)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a daily content-curation workflow that searches, selects, crawls, summarizes, and optionally posts generated Eir-format content. It supports standalone local output and an opt-in Eir mode for delivery through an Eir account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled agent runs can persist and execute recurring search, crawl, and generation work.

Mitigation: Review or remove the cron setup before deployment and run the skill in a dedicated workspace.

Risk: The skill searches the web and crawls selected URLs, which can expose the environment to untrusted content.

Mitigation: Prefer allowlisted public search and crawl endpoints and review selected sources before generation.

Risk: Search and Eir API credentials may be stored locally.

Mitigation: Restrict permissions on local config files and use dedicated API keys with limited scope where possible.

Risk: Eir mode can post generated content or shape account content.

Mitigation: Enable Eir mode only intentionally, review generated JSON before posting, and avoid personalization or interest sync unless intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/heyeir/skills/eir-daily-content-curator)
- [Eir](https://www.heyeir.com)
- [SKILL.md](artifact/SKILL.md)
- [Security and Privacy](artifact/SECURITY.md)
- [Content Spec](artifact/references/content-spec.md)
- [Candidates Spec](artifact/references/candidates-spec.md)
- [Eir Setup](artifact/references/eir-setup.md)
- [Eir API](artifact/references/eir-api.md)
- [Brave Search API](https://brave.com/search/api/)
- [Tavily](https://tavily.com/)
- [SearXNG Documentation](https://docs.searxng.org/)
- [Crawl4AI](https://github.com/unclecode/crawl4ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, task files, and generated content files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standalone mode saves local content under data/output; Eir mode can post generated JSON content to the Eir API.]

## Skill Version(s):

3.119.0 (source: server release metadata and changelog, released 2026-04-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
