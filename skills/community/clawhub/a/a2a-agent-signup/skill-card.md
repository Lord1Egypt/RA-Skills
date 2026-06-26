## Description: <br>
Interactive CLI wizard for registering an agent on A2A Marketplace, collecting wallet and profile details, handling a $0.01 USDC Polygon registration fee, and saving local credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcus20232023](https://clawhub.ai/user/marcus20232023) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and marketplace participants use this skill to create an A2A Marketplace agent profile, optionally list a first service, complete the required registration payment, and save credentials for later marketplace use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs npm dependencies, creates a shell command symlink, may append ~/bin to ~/.bashrc, and then starts the signup wizard. <br>
Mitigation: Review setup.sh before running it, run it only in a trusted shell environment, and confirm any PATH changes are acceptable. <br>
Risk: The skill handles wallet addresses, registration payment flow details, auth tokens, .env data, and ~/.a2a-agent-config credentials. <br>
Mitigation: Protect the generated .env and ~/.a2a-agent-config files as secrets, avoid reusing generated test wallets for real funds, and keep wallet private keys outside this workflow. <br>
Risk: The marketplace API URL can be configured, so a malicious or mistaken endpoint could receive registration and wallet metadata. <br>
Mitigation: Use only a trusted A2A_API_URL and verify the endpoint before submitting registration or payment information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcus20232023/a2a-agent-signup) <br>
- [A2A Marketplace](https://a2a.ex8.ca) <br>
- [A2A Marketplace JSON-RPC endpoint](https://a2a.ex8.ca/a2a/jsonrpc) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Interactive terminal prompts, status text, JSON snippets, shell commands, and local configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes .env in the current directory and ~/.a2a-agent-config with restrictive file permissions; setup may create a ~/bin symlink and update ~/.bashrc.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
