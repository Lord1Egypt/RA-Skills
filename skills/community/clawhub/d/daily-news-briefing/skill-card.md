## Description:

Produces polished daily news briefings, market snapshots, executive digests, and founder updates with verified sourcing, clear prioritization, and premium Markdown or HTML formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmouseboy](https://clawhub.ai/user/fmouseboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, CEOs, investors, and operators use this skill to create current, source-linked daily briefings, morning newsletters, market notes, and executive digests tailored to a specific audience and scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated briefings may include stale, weakly sourced, contested, or unsupported news claims.

Mitigation: Verify time-sensitive stories with current sources, cite every major story near the relevant item, and clearly label contested claims or editorial inferences.

Risk: Generated HTML metadata can include user-supplied title, audience, date, or scope values.

Mitigation: Review or escape those fields before publishing generated HTML on a trusted site, especially when values came from untrusted parties.

Risk: The local package generator writes Markdown, optional HTML, and a JSON manifest into a user-specified output directory.

Mitigation: Choose an intended local output path and review generated files before reuse or publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fmouseboy/skills/daily-news-briefing)
- [Editorial Standards](references/editorial-standards.md)
- [Output Blueprints](references/output-blueprints.md)
- [Markdown Briefing Template](assets/briefing-template.md)
- [HTML Briefing Template](assets/briefing-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing content by default, with optional HTML briefing files, local package manifests, and shell command examples for template generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should use exact dates, current source links near each story, concise executive summaries, top stories, watchlists, and a closing take.]

## Skill Version(s):

1.0.0 (source: evidence release and artifact changelog, released 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
