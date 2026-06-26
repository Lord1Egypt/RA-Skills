## Description: <br>
An OpenClaw skill to manage a user's vinyl record collection on Discogs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrojas537](https://clawhub.ai/user/jrojas537) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to query and manage a Discogs vinyl collection and wantlist from a Go command-line interface. It supports collection listing, Discogs search, album art retrieval, local valuation cache workflows, and wantlist add or remove actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer path may need review before use. <br>
Mitigation: Review or fix the installer path before running the installer. <br>
Risk: The skill stores a Discogs username and personal access token in a local config file. <br>
Mitigation: Use a revocable Discogs token and protect ~/.config/discogs-cli/config.yaml. <br>
Risk: Wantlist add and remove commands mutate a user's Discogs account state. <br>
Mitigation: Confirm exact release IDs before running wantlist add or remove commands. <br>
Risk: Collection valuation data and album art are cached locally. <br>
Mitigation: Treat local cache files and album art as user collection data and remove them when no longer needed. <br>


## Reference(s): <br>
- [Discogs Cli on ClawHub](https://clawhub.ai/jrojas537/discogs-cli) <br>
- [Go installation documentation](https://go.dev/doc/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Terminal text, tabular command output, local cache files, and album art media paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Go, a Discogs username, and a Discogs personal access token stored in local configuration.] <br>

## Skill Version(s): <br>
1.3.1 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
