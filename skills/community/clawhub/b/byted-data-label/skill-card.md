## Description: <br>
Byted Data Label helps agents use Seederive to run LLM-based batch analysis and labeling for text, audio, and image data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to preview, create, manage, and optimize Seederive data-labeling tasks for sentiment analysis, tag classification, opinion extraction, translation, content scoring, and related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user data to Seederive cloud services for labeling and analysis. <br>
Mitigation: Install only when cloud-based Seederive processing is intended, verify the API endpoint, and require explicit confirmation before uploads. <br>
Risk: The skill uses cloud credentials for live API calls. <br>
Mitigation: Use least-privileged Volcengine credentials and avoid exposing access keys in prompts, logs, or shared files. <br>
Risk: The helper script may install Python dependencies at runtime. <br>
Mitigation: Preinstall dependencies in a controlled environment instead of allowing runtime package installation. <br>
Risk: The skill can update, delete, backfill, optimize, and change models for remote Seederive resources. <br>
Mitigation: Require explicit user confirmation before uploads, model changes, backfills, optimizations, updates, or deletions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-data-label) <br>
- [Seederive task management guide](references/task.md) <br>
- [Seederive tag-base management guide](references/tag-base.md) <br>
- [Seederive optimization guide](references/optimize.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and optional JSON or CSV result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY for live Seederive API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
