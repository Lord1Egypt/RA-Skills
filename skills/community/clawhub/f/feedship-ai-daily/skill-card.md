## Description: <br>
Generate a daily AI news digest from Feedship subscriptions by extracting articles, filtering AI and technology content, producing LLM-based strategic analysis, and replacing citation placeholders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanpeipan](https://clawhub.ai/user/yanpeipan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create on-demand or scheduled AI news briefings from Feedship subscriptions. It is intended for daily summaries, periodic recaps, and Chinese-language AI trend analysis with citation links injected from source article data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subscription-derived article titles may be processed by the configured LLM. <br>
Mitigation: Use the skill only with Feedship data you are comfortable sending to that LLM, and review privacy expectations before enabling scheduled runs. <br>
Risk: The workflow writes intermediate article and report files under /tmp, which may be unsuitable on shared machines. <br>
Mitigation: Review and adapt the temporary file behavior for the target environment before deployment. <br>
Risk: The documented commands include a hard-coded Feedship path, Beijing-time cron settings, and user-supplied delivery channel fields. <br>
Mitigation: Update the local Feedship path, timezone, destination channel, and recipient before enabling the cron command. <br>
Risk: The LLM can emit invalid citation placeholders that do not map to source articles. <br>
Mitigation: Run the bundled replacement script and review warnings for invalid references before sharing the final report. <br>


## Reference(s): <br>
- [Prompt Template](references/prompt.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yanpeipan/feedship-ai-daily) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with injected article links and supporting shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses numbered citation placeholders that are post-processed into article links.] <br>

## Skill Version(s): <br>
1.21.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
