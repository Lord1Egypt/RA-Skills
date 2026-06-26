## Description: <br>
Fleece is a credit card research and redemption CLI for rewards rates, fees, welcome bonuses, statement credits, transfer partners, wallet analysis, ROI estimates, recommendations, merchant category codes, and award travel search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyuan99](https://clawhub.ai/user/chenyuan99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and credit card rewards users use Fleece to query current US card information, compare card portfolios, analyze spending profiles, and generate JSON-friendly redemption research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fleece can store personal card inventory, spending habits, travel goals, credit limits, expiration dates, and other profile details. <br>
Mitigation: Enter only the minimum profile data needed, avoid full account details, and review or remove local profile data when it is no longer needed. <br>
Risk: Personalized research may send profile or card context to external services such as Brave Search or OpenAI. <br>
Mitigation: Avoid entering sensitive financial details, keep API keys scoped to this use case, and review prompts or command inputs before running personalized searches. <br>
Risk: Running the Streamlit app on a shared server can expose debug, history, image-fetching, or stored-profile behavior to other users. <br>
Mitigation: Prefer local execution for personal finance research and harden access controls, history handling, and image-fetching behavior before shared deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenyuan99/fleece) <br>
- [PyPI Package](https://pypi.org/project/fleece-cli/) <br>
- [Project Website](https://getfleece.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples and JSON command-output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly return JSON with ok and error fields; some workflows require BRAVE_API_KEY or OPENAI_API_KEY.] <br>

## Skill Version(s): <br>
1.6.0 (source: ClawHub release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
