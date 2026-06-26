## Description: <br>
Lightweight Dividend tracker. Add entries, view stats, search history, and export in multiple formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Dividend to keep local notes about dividends, balances, forecasts, alerts, tax notes, history, and related personal-finance activity, then review statistics, search entries, and export records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dividend stores finance notes, balances, alerts, tax notes, searches, and exports in plaintext files under ~/.local/share/dividend. <br>
Mitigation: Avoid entering passwords, account credentials, API keys, or highly sensitive financial details, and delete or protect that directory when the data should no longer be retained. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bytesagain3/dividend) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain3) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Dividend command script](artifact/scripts/script.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Terminal text with local JSON, CSV, and plain text exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-entered records and exports as local plaintext files under ~/.local/share/dividend.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
