## Description: <br>
Automates question submission to Amazon's Alexa/Rufus shopping assistant and collects response text, with optional keyword search context for category-specific shopping Q&A. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market researchers use this skill to ask Amazon's shopping assistant product-category questions, run serial Q&A batches, and collect the returned answers as JSON for review or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a logged-in Amazon browser session, submits user questions to Amazon's assistant, and can save returned answers locally. <br>
Mitigation: Run it only in an account and browser session intended for this work, avoid sensitive questions, and review or delete saved output files when the responses are sensitive. <br>
Risk: The security scan notes stealth multi-session automation guidance and a risk of understated interaction with a logged-in Amazon session. <br>
Mitigation: Avoid stealth multi-session use, keep batches modest, and follow Amazon's terms, rate limits, and applicable internal approval requirements. <br>
Risk: Collected shopping answers may be incomplete, time-sensitive, or shaped by Amazon's assistant and page context. <br>
Mitigation: Review the extracted JSON before relying on it and verify important product claims, prices, availability, or recommendations against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/browseract-cli/amazon-alexa-qa) <br>
- [Amazon](https://www.amazon.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON response records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an already logged-in Amazon browser session and serial browser automation; responses should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
