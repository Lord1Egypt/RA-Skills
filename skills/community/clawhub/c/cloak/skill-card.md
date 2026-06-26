## Description: <br>
Share one-time secrets between humans and agents via encrypted self-destructing links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saba-ch](https://clawhub.ai/user/saba-ch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use Cloak to create, retrieve, and delete one-time links for API keys, passwords, tokens, and other secrets without exposing the secret value in conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret values are sent to the Cloak service, so users must trust cloak.opsy.sh with passwords, API keys, or tokens. <br>
Mitigation: Confirm before uploading secrets, prefer short-lived or least-privilege credentials, and avoid sharing material that should not leave the local environment. <br>
Risk: Retrieved secrets are destroyed after one read, so accidental retrieval can make a shared link unusable. <br>
Mitigation: Route retrieved values directly into the intended environment variable, file, or command, and verify the destination before reading the link. <br>
Risk: Secrets can leak if displayed in chat, logs, shell history, or committed files. <br>
Mitigation: Do not echo retrieved values, avoid committing files such as .env.local, and pipe values directly to the target destination. <br>


## Reference(s): <br>
- [Cloak service homepage](https://cloak.opsy.sh) <br>
- [ClawHub skill page](https://clawhub.ai/saba-ch/cloak) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require curl and jq; retrieved secrets should be piped directly to their destination.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
