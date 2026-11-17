## Description:

Turns a consumer's photos and firsthand account into fact-based Dianping reviews or visit notes, with an optional package for manual posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT-0

## Use Case:

Individual Dianping users turn their own visit details and photos into honest Chinese-language reviews or discovery notes. On request, the skill prepares images and copy for the user to post manually; it does not publish on their behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required companion writing skill or a configured helper directory may come from an untrusted source.

Mitigation: Install hekouwang-writer-skill from a trusted source and do not point HEKOUWANG_WRITER_SKILL_DIR at untrusted folders.

Risk: Generated manual-posting packages may retain personal photos, faces, receipts, locations, and review text.

Mitigation: Review photos and copy for sensitive details, then delete generated dist packages when no longer needed.

Risk: The separately advertised Pro product may interact with a real Dianping account.

Mitigation: Assess Pro automation separately; this free release only prepares material for manual posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huiyonghkw/skills/dianping-review-skill)
- [Skill homepage](https://huiyonghkw.github.io/dianping-review-skill/)
- [Category guidance](references/category_rules.json)
- [Writing style guidance](references/style.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Images]

**Output Format:** [Chinese review or visit-note text, with optional numbered photos, cover image, and text file for manual posting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps ratings and factual details grounded in the user's account; the user posts manually. Cover-image generation requires Pillow.]

## Skill Version(s):

1.2.0 (source: ClawHub release, SKILL.md frontmatter, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
