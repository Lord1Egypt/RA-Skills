## Description: <br>
Assistant for VCs and investors asking about the Creez project; it answers factual questions using a knowledge base and, when the user shows clear interest and provides contact details, forwards investor information for founder follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjuhua-aigc](https://clawhub.ai/user/huangjuhua-aigc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors and agents representing them use this skill to ask factual questions about Creez and, after explicitly providing contact details, request founder follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creez-hosted APIs receive investor questions submitted through the skill. <br>
Mitigation: Use the skill only when the user is comfortable sending those questions to Creez-hosted services. <br>
Risk: Email, WeChat, company, availability, and other contact details may be sent to Creez or the founder for follow-up and may be stored or forwarded internally. <br>
Mitigation: Submit only contact details the user explicitly provided and only after they are comfortable sharing them for follow-up. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangjuhua-aigc/creez-finance-bot) <br>
- [Creez knowledge search API](https://creez.lighton.video/knowledge/search) <br>
- [Creez lead capture API](https://creez.lighton.video/roundcloser/lead) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance, Configuration] <br>
**Output Format:** [Markdown or plain-text agent responses with JSON API request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send explicitly provided investor questions and contact details to Creez-hosted APIs for knowledge search and founder follow-up.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
