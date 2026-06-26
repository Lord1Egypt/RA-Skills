## Description: <br>
Content Creator Pro helps agents draft and queue platform-native social posts, threads, newsletters, articles, and short-form video scripts using brand voice, hook frameworks, scheduling, and performance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to create human-facing content for Twitter/X, LinkedIn, Reddit, Substack, and short-form video workflows. It is intended to prepare and queue public-facing drafts while tracking hooks, calendar slots, and performance data for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate and queue ready-to-publish public content on a schedule. <br>
Mitigation: Review every generated post, thread, newsletter, article, or script before publication and keep publishing integrations gated by human approval. <br>
Risk: The skill persists brand voice, calendar, hook, performance, learning, error, queue, library, and audit records in local workspace files. <br>
Mitigation: Keep secrets, customer data, and unverifiable personal claims out of these files, and review stored records before sharing or publishing content derived from them. <br>
Risk: The bundled Python tracker updates performance files, hook records, audit logs, and error logs. <br>
Mitigation: Run the tracker only after explicit opt-in, inspect its target paths, and avoid enabling cron or other unattended execution until the local workflow has been reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/georges91560/content-creator-pro) <br>
- [README](artifact/README.md) <br>
- [Human writing guide](artifact/human_writing.md) <br>
- [Hooks library](artifact/hooks.md) <br>
- [Content tracker script](artifact/content_tracker.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-backed content files with optional Python CLI status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces public-facing drafts and local tracking records under /workspace/content and /workspace/.learnings paths; release metadata reports no direct network requests.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
