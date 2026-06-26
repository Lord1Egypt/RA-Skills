## Description: <br>
公众号 AI 选题与标题生成助手，支持热点调研、选题策划、标题候选、摘要候选和系列排期，面向自媒体编辑与内容运营人员。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiworkskills](https://clawhub.ai/user/aiworkskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, editors, and content operations teams use this skill to research WeChat public-account article topics, generate headline and summary candidates, plan article series, and create handoff notes for drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read .aws-article configuration and product notes while preparing topics and titles. <br>
Mitigation: Install and run it only in workspaces where the agent is allowed to access those article-planning files. <br>
Risk: The workflow may write draft metadata and planning files such as topic-card.md, research.md, and article.yaml. <br>
Mitigation: Review generated article metadata and draft files before using them in a publishing workflow. <br>
Risk: The full aws-wechat-article suite may reference sibling Python helpers outside this skill artifact. <br>
Mitigation: Review referenced sibling helpers before allowing the agent to execute them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiworkskills/aws-wechat-article-topics) <br>
- [Publisher profile](https://clawhub.ai/user/aiworkskills) <br>
- [Output format reference](artifact/references/output-format.md) <br>
- [Research strategy reference](artifact/references/research-strategy.md) <br>
- [Title presets reference](artifact/references/title-presets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with topic cards, research summaries, title and digest candidates, article metadata notes, and occasional shell command suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update topic-card.md, research.md, article.yaml, and series planning files in the user's article workspace when directed by the workflow.] <br>

## Skill Version(s): <br>
1.0.23 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
