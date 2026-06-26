## Description: <br>
Design Daily Insights tracks design tool updates, AI product news, design system evolution, UX research, and design inspiration, then produces a concise daily digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ellisonnnnnnn](https://clawhub.ai/user/ellisonnnnnnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, product teams, and developers use this skill to collect recent design and AI product news, deduplicate sources, and publish a bilingual digest with links to original articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated digests may be published through a public locaddr.run reverse tunnel. <br>
Mitigation: Use the tunnel only when intentional, serve a dedicated output directory, and avoid publishing private sources, internal URLs, or sensitive summaries. <br>
Risk: Recurring scheduled runs can send generated content without direct review. <br>
Mitigation: Enable cron or scheduled delivery only when needed and review the sources, channel, timeout, and alert settings before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ellisonnnnnnn/design-daily-insights) <br>
- [Source catalog](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Bilingual Markdown-style digest with article links, generated HTML page content, and optional shell or cron setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains a URL-based deduplication state, targets 10-15 items, and caps the digest to about 2000 Chinese characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
