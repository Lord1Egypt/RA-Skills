## Description: <br>
Use stronger lawful workflows for sites the user is authorized to access, including local browser login, session-aware browsing, JS-heavy pages, and post-login extraction without bypassing access controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to work with websites they are authorized to access when login, client-side rendering, or post-login pages prevent ordinary fetching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may encounter authenticated page content or account-specific data while helping with post-login research. <br>
Mitigation: Use local browser login, do not share passwords, cookies, tokens, or other secrets in chat, and limit extraction to facts needed for the authorized task. <br>
Risk: Requests could drift toward bypassing paywalls, access controls, or anti-bot protections. <br>
Mitigation: Stop before bypass attempts; continue only after the user has lawful access and content is legitimately available in the local session. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1477009639zw-blip/authenticated-web-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown response summarizing public reachability, authenticated access, extracted facts, and remaining gaps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include notes identifying facts from authenticated views; no fixed token limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
