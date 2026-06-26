## Description: <br>
Search for relevant sponsored content, deals, and AI-powered ad results from AttentionMarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AminAmbike](https://clawhub.ai/user/AminAmbike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search AttentionMarket for sponsored deals, promotions, product recommendations, restaurant offers, and other commercial-intent results, then present them transparently as sponsored links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow asks the agent to handle an AttentionMarket account password. <br>
Mitigation: Review scripts/setup.sh before entering credentials, use a dedicated credential rather than a reused password, and install only if the publisher is trusted. <br>
Risk: The setup flow saves AM_API_KEY in plaintext under ~/.clawdbot/.env. <br>
Mitigation: Protect or remove the environment file after setup as appropriate, avoid exposing the key in logs or chat transcripts, and rotate the key if it is disclosed. <br>
Risk: The skill returns sponsored content for commercial recommendation requests. <br>
Mitigation: Label results as Sponsored and include click URLs transparently so users can distinguish advertising from organic recommendations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AminAmbike/attentionmarket) <br>
- [AttentionMarket Dashboard](https://dashboard.attentionmarket.ai) <br>
- [AttentionMarket Decide Endpoint](https://peruwnbrqkvmrldhpoom.supabase.co/functions/v1/decide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sponsored results should include title, body, call to action, click URL, relevance, and sponsored labeling when results are filled.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
