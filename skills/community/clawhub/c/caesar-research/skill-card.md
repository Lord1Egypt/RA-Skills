## Description: <br>
Deep research using the Caesar API - run queries, follow up with chat, brainstorm, and manage collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexrudloff](https://clawhub.ai/user/alexrudloff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and researchers use this skill to run Caesar research jobs, ask follow-up questions, brainstorm clarifying questions, and organize collection context from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires CAESAR_API_KEY for access to Caesar's remote service. <br>
Mitigation: Store the API key securely, avoid committing it to source control, and rotate it if it may have been exposed. <br>
Risk: Research prompts, chat messages, and collection context may be sent to Caesar's remote service. <br>
Mitigation: Do not submit secrets, regulated data, or confidential documents unless organizational policy and Caesar's terms permit it. <br>
Risk: A compromised or untrusted Caesar CLI installation could affect command behavior. <br>
Mitigation: Install the Caesar CLI only from a trusted source and review the command output before using it in downstream workflows. <br>


## Reference(s): <br>
- [Caesar](https://www.caesar.org/) <br>
- [Caesar API endpoint](https://api.caesar.xyz) <br>
- [Deep Research with Caesar.org on ClawHub](https://clawhub.ai/alexrudloff/caesar-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include synthesized research answers, citations, source lists, job status JSON, brainstorm questions, chat responses, and collection metadata.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
