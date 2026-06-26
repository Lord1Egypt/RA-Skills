## Description: <br>
A ClawHub skill release that presents BitoPro spot-market tools and credential prompts, while server security evidence classifies it as a disclosed security-research proof of concept rather than a legitimate BitoPro integration. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[mahetagaurang22](https://clawhub.ai/user/mahetagaurang22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security reviewers and developers can examine this release as a supply-chain risk example showing how a BitoPro-looking ClawHub skill can request exchange credentials without implementing a trusted integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release registers as a BitoPro trading skill and asks for real exchange API credentials without implementing a legitimate integration. <br>
Mitigation: Do not install it as a working BitoPro integration and do not provide real BitoPro credentials. <br>
Risk: Users may confuse the claimed BitoPro functionality with a trusted exchange integration. <br>
Mitigation: Confirm the publisher handle and use a trusted, legitimate exchange skill that clearly implements the advertised API behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mahetagaurang22/bitopro-spot) <br>
- [Publisher profile](https://clawhub.ai/user/mahetagaurang22) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-like API response text, depending on the agent action.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requests BitoPro credential environment variables for private account and trading actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
