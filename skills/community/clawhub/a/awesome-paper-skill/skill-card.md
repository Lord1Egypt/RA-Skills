## Description: <br>
End-to-end pipeline for topic-driven literature research: collect papers from multiple sources, generate an Awesome-style README, and update/push to user GitHub repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YoujunZhao](https://clawhub.ai/user/YoujunZhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to scout papers for a topic, organize them into an Awesome-style README, and publish or update that README in a GitHub repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or change GitHub repositories using the user's account without a clear final confirmation step. <br>
Mitigation: Use an explicit repository owner, repository name, and visibility; verify the active GitHub CLI account; inspect the generated README; and require manual confirmation before repository creation, pushes, or visibility changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YoujunZhao/awesome-paper-skill) <br>
- [Awesome list format reference](https://github.com/sindresorhus/awesome) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown README, JSON paper list, shell commands, and brief text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses topic, repository owner/name, visibility, and source result limits; may create or update a GitHub repository.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact _meta.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
