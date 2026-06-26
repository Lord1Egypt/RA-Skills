## Description: <br>
Curate and post AI trend tweets from X (Twitter) with quote suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yusaku-0426](https://clawhub.ai/user/yusaku-0426) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Social media and community operators use this skill to find AI-related posts on X, curate balanced Japanese and English selections, draft quote suggestions, format them for Slack, and mark posted URLs to reduce duplicates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post agent-curated content to Slack where others may see it. <br>
Mitigation: Use a preview-and-approve step before posting and configure the Slack destination to a known channel. <br>
Risk: The package references scripts/ai_trends.js, but that helper script is not included in the reviewed artifact. <br>
Mitigation: Install only after verifying the helper script from a trusted source and reviewing what commands it runs. <br>
Risk: Slack posting may use credentials or identities with broad visibility. <br>
Mitigation: Use the least-privilege Slack identity needed for the intended channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yusaku-0426/ai-trend-curation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-shaped tweet data for Slack Block Kit formatting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires xurl and a trusted scripts/ai_trends.js helper to search, format, check duplicates, and mark posts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
