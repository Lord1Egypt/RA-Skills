## Description: <br>
去AI味助手面向中文营销、运营、内容创作和产品场景，帮助用户基于文本、文件或公开链接生成 AI 写作痕迹诊断、自然化改写稿和问题片段说明。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to rewrite Chinese drafts so they read more naturally for channels such as general Chinese content, WeChat articles, Xiaohongshu notes, official blogs, marketing pages, course scripts, and knowledge-base documents. Users provide text, a file, or a public URL plus optional goals, audience, tone, and brand constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service processes user-provided text, files, or URLs through a third-party AI Skills API and requires an API key. <br>
Mitigation: Install only when external processing is approved, prefer explicit invocation, and avoid confidential or regulated content unless policy allows it. <br>
Risk: The skill can disguise AI-written or academic text, and the security verdict is suspicious because implicit invocation is broad for that behavior. <br>
Mitigation: Do not use the skill to bypass academic, workplace, platform, or disclosure rules about AI-generated writing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/ai-humanizer-zh) <br>
- [AI Skills service](https://ai-skills.ai) <br>
- [Form schema](references/form-schema.json) <br>
- [Skill metadata](references/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON response envelope containing user-facing text and structured result content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected outputs include AI writing-trace diagnosis, a naturalized rewrite, notes on problematic passages, and next-step suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
