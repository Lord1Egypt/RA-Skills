## Description: <br>
Discover your supporter personality and find AI tools you'll love. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bloomprotocol](https://clawhub.ai/user/bloomprotocol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, indie developers, AI builders, and consumer AI enthusiasts use this skill to analyze recent conversation history, produce a supporter identity card, and receive tool recommendations that match how they work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically downloads and runs external code and npm dependencies. <br>
Mitigation: Install only if the Bloom publisher and dependency chain are trusted, and review the installed code before use in sensitive environments. <br>
Risk: The skill reads conversation sessions and sends analysis results to Bloom services. <br>
Mitigation: Avoid running it on sensitive conversations and review what data is sent to Bloom services before sharing an identity card. <br>
Risk: The skill creates local configuration that can include a default JWT secret. <br>
Mitigation: Replace the default JWT secret before any dashboard use. <br>
Risk: The skill sets up wallet and network behavior for future tipping features. <br>
Mitigation: Do not deposit funds into the generated wallet until custody, withdrawal, and cleanup behavior are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bloomprotocol/bloom) <br>
- [Bloom Protocol publisher profile](https://clawhub.ai/user/bloomprotocol) <br>
- [Bloom Protocol](https://bloomprotocol.ai) <br>
- [Bloom API endpoint](https://api.bloomprotocol.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text with dashboard URLs, identity-card details, recommendations, and setup or error guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration, install npm dependencies, read conversation session files, call Bloom services, and generate a wallet address for future tipping features.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
