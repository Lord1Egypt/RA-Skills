## Description: <br>
Retrieves Google Search Console analytics for akku-alle.de, including clicks, impressions, CTR, rankings, and top keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akkualle](https://clawhub.ai/user/akkualle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Site owners and SEO analysts use this skill to ask an agent for Search Console performance metrics, keyword rankings, and search query summaries for akku-alle.de. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Google credentials and can expose Search Console analytics for akku-alle.de. <br>
Mitigation: Use a least-privilege Google credential scoped to the intended Search Console property and enable the skill only for authorized users. <br>
Risk: The release instructs the agent to run a local executable that is not included in the artifact. <br>
Mitigation: Inspect and trust /root/.openclaw/skills/gsc-search/gsc-search before installing or invoking the skill. <br>
Risk: Broad always-on routing may invoke the skill for general SEO questions. <br>
Mitigation: Limit invocation to explicit Search Console analytics requests from users who are allowed to view the property data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown summaries with metric bullets and tables, plus shell command invocations for execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_APPLICATION_CREDENTIALS and access to the local gsc-search executable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
