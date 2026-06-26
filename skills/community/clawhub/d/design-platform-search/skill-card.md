## Description: <br>
Runs login-free public design search flows on Dribbble, Pinterest, and Behance and normalizes result fields such as title, cover image, author, source URL, and publish time when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyyyy0430](https://clawhub.ai/user/joeyyyy0430) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and design researchers use this skill to retrieve public inspiration results from Dribbble, Pinterest, and Behance without login and return normalized records for lightweight comparison or aggregation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public design platforms can change page structure, restrict regional access, or apply anti-bot controls, which may reduce retrieval quality. <br>
Mitigation: Validate platform reachability before changing selectors, keep request volume modest, and reduce optional detail-page backfill in constrained or proxy-heavy environments. <br>
Risk: Supplying cookies, logged-in sessions, or authenticated APIs would exceed the documented public-only workflow. <br>
Mitigation: Use only public pages, avoid credentials and authenticated sessions, and leave unavailable fields nullable rather than fabricating data. <br>
Risk: English tags are the reusable default but may miss locale-specific design results. <br>
Mitigation: Override the English-tag default when the user's topic, locale, or language calls for non-English searches. <br>


## Reference(s): <br>
- [Platform Methods](references/platform-methods.md) <br>
- [Tag Guidance](references/tag-taxonomy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-shaped normalized result records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normalized public-only records keep unstable fields nullable and avoid fabricated authors, publish times, or engagement metrics.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
