## Description: <br>
AI Daily Intelligence Digest aggregates RSS news, summarizes articles with AI, and publishes a daily digest to Feishu Wiki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, product, management, and research teams use this skill to turn multiple technology RSS feeds into a daily Feishu Wiki digest for awareness, competitor tracking, and knowledge capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically publish generated summaries to a configured Feishu Wiki destination. <br>
Mitigation: Confirm the Wiki space and parent node, run the skill manually first, and enable the daily cron only after validating the output and destination. <br>
Risk: Summaries of external RSS content may be inaccurate or include sensitive material from source articles. <br>
Mitigation: Review generated summaries for accuracy and sensitivity before relying on or broadly sharing them. <br>
Risk: Feishu credentials grant access to publish into the configured workspace. <br>
Mitigation: Use least-privilege Feishu credentials and install only when automatic posting to Feishu Wiki is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown digest, Feishu Wiki page link, article counts, and digest preview text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configured RSS feed list, article limits, summary style, Feishu Wiki destination, and optional daily cron schedule affect the produced digest.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, skill metadata, workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
