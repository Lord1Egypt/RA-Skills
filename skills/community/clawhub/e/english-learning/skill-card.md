## Description:

English-Learning helps agents provide primary-school, TEM-4, and TEM-8 English listening materials, including material lists and detailed listening text segments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leiwonginchaozhou-netizen](https://clawhub.ai/user/leiwonginchaozhou-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and language-learning assistants use this skill to select an English listening training category, retrieve active listening materials, and present ordered transcript segments or audio links for practice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill artifact publishes a real-looking Supabase endpoint and anon key.

Mitigation: Review before installing, use project-specific Supabase credentials where appropriate, rotate any exposed key, and verify Row Level Security limits the anon role to intended read-only listening materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leiwonginchaozhou-netizen/skills/english-learning)
- [Publisher profile](https://clawhub.ai/user/leiwonginchaozhou-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text responses with retrieved listening material lists and ordered segment details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_ANON_KEY environment variables.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
