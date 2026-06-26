## Description: <br>
Creates, optimizes, deploys, manages, and analyzes AI-Shifu courses by converting course material into MarkdownFlow Teaching Prompts and Course Prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heshaofu2](https://clawhub.ai/user/heshaofu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Course creators, developers, and course operators use this skill to transform raw course material into AI-Shifu MarkdownFlow lessons and course prompts, deploy or manage live courses, and query learner and course analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, overwrite, delete, reorder, archive, and import live AI-Shifu course content. <br>
Mitigation: Confirm the target course ID or title before production operations, and request a preview or export before publish, import to an existing course, delete, reorder, or archive actions. <br>
Risk: Deployment and analytics commands rely on a saved AI-Shifu token. <br>
Mitigation: Keep the .env token private, exclude it from version control, and rotate or re-login if the token may have been exposed. <br>
Risk: Analytics queries can expose sensitive learner or course data if raw identifiers, codes, or learner input are presented directly. <br>
Mitigation: Use the documented CLI analytics workflow, apply the privacy and presentation rules before reporting results, and avoid exposing raw user identifiers or restricted learner fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heshaofu2/ai-shifu-course-creator) <br>
- [AI-Shifu platform](https://app.ai-shifu.cn) <br>
- [MarkdownFlow reference](references/markdownflow.md) <br>
- [Pedagogy reference](references/pedagogy.md) <br>
- [Data contracts](references/data-contracts.md) <br>
- [Course prompt reference](references/course-prompt.md) <br>
- [CLI reference](references/cli/cli-reference.md) <br>
- [Analytics overview](references/analytics/overview.md) <br>
- [Analytics privacy and presentation](references/analytics/privacy-and-presentation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas, shell commands, and generated course files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AI-Shifu course directories, MarkdownFlow lesson files, course prompts, import JSON, deployment reports, and analytics summaries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
