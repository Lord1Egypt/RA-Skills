## Description:

Daily Gushiwen fetches daily classical Chinese literature content from the Gushiwen homepage and formats poems, painting-caption quotations, and selected famous lines for delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enchograph](https://clawhub.ai/user/enchograph)

### License/Terms of Use:


## Use Case:

External users or agents use this skill to respond to daily classical Chinese literature prompts by fetching the current Gushiwen homepage and preparing a concise digest of poems, painting-caption quotations, and famous lines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese poetry trigger wording may activate the skill when the user wanted general poetry help rather than a daily Gushiwen digest.

Mitigation: Confirm the user wants the daily Gushiwen digest before fetching and sending formatted daily content when intent is ambiguous.

Risk: The skill fetches public content from gushiwen.cn and an associated image host, which creates network access and media delivery considerations.

Mitigation: Allow only the documented public content sources and avoid sending sensitive user data, credentials, or private context in fetch requests.

Risk: Daily website content and parsed image URLs can change, so output may become stale or incorrectly structured if the source page changes.

Mitigation: Review fetched content before delivery and fall back to text-only output when image extraction or media sending is unreliable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enchograph/skills/daily-gushiwen)
- [Gushiwen homepage](https://www.gushiwen.cn/)
- [Parsing guide](artifact/references/parsing-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style Chinese daily digest with section separators and optional public image media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is fetched from public web pages at request time and should stay concise, without added analysis.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
