## Description: <br>
Coordinates publishAt embargo timing across blog index visibility and social post scheduling so posts are indexed only after social posts are queued. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to coordinate blog publishAt frontmatter, pull request timing, and Buffer scheduling for synchronized blog and social launches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect dates, time zones, or target Buffer channels could publish or schedule public content at the wrong time. <br>
Mitigation: Review publishAt values, time zones, Buffer queue conflicts, and target channels before applying the workflow. <br>
Risk: A merged post may be directly reachable before it appears in the blog index. <br>
Mitigation: Schedule Buffer posts after confirming the merge and account for the direct URL being live while index visibility is still gated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/blog-embargo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No automatic execution; users must review publishAt values, time zones, pull request timing, and Buffer channels.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
