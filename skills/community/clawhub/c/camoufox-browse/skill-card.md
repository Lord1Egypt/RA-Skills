## Description: <br>
Stealth and anti-fingerprinting browser guidance for AI agents using Camoufox and Playwright to reach sites that block the built-in browser tool, only for authorized automated access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenaufa](https://clawhub.ai/user/zenaufa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to configure Camoufox browser automation when permitted sites block the built-in browser or require stable browser fingerprints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anti-fingerprinting browser automation can be misused for unauthorized scraping, ban evasion, impersonation, or terms-of-service violations. <br>
Mitigation: Use only where automated access is authorized by the user and permitted by the target site and applicable law; surface access or terms questions before proceeding. <br>
Risk: Automated sessions can expose real accounts, cookies, credentials, or irreversible actions such as submissions, downloads, bulk operations, or deletions. <br>
Mitigation: Use disposable profiles and least-privilege accounts, keep secrets out of scripts, and require explicit approval before irreversible or high-volume actions. <br>
Risk: The skill expects npm or pip dependencies and a browser download, increasing local execution and dependency risk. <br>
Mitigation: Install only when anti-fingerprinting browsing is needed, pin documented runtime versions, and review dependency and browser downloads in the target environment. <br>


## Reference(s): <br>
- [Camoufox documentation](https://camoufox.com) <br>
- [Camoufox Python package](https://pypi.org/project/camoufox/) <br>
- [Camoufox project repository](https://github.com/daijro/camoufox) <br>
- [camoufox-js project repository](https://github.com/apify/camoufox-js) <br>
- [Playwright Python documentation](https://playwright.dev/python/docs/intro) <br>
- [ClawHub skill page](https://clawhub.ai/zenaufa/skills/camoufox-browse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides installation, configuration, browsing workflow, troubleshooting, safety, and ethics guidance; Camoufox and browser binaries are installed separately by the user.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
