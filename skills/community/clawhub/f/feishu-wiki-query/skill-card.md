## Description: <br>
Feishu Wiki Query helps an agent query configured Feishu wiki knowledge bases, read text and document media, and return source-attributed answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwsong](https://clawhub.ai/user/fwsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams with Feishu access use this skill to configure one or more Feishu knowledge bases and ask an agent to retrieve document, image, whiteboard, or spreadsheet content with source attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes real-looking Feishu app credentials. <br>
Mitigation: Do not use the bundled credentials; revoke and replace them with securely managed credentials using minimal Feishu permissions. <br>
Risk: The skill includes image upload, message sending, and sheet access flows that are broader than read-only wiki querying. <br>
Mitigation: Allow those actions only after explicit user approval, with known recipients and the narrowest Feishu permissions required. <br>
Risk: The bundled configuration contains a prefilled knowledge-base entry. <br>
Mitigation: Remove or verify the prefilled configuration before use and configure only approved knowledge bases. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fwsong/feishu-wiki-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text responses with source attribution, plus JSON configuration and Feishu API command guidance when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Security review verdict: suspicious; review credentials, configured knowledge bases, Feishu recipients, and Feishu permissions before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
