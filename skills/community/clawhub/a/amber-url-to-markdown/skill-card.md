## Description: <br>
Converts supported article and web page URLs into local Markdown files, with optional image downloads and an auto-fetch hook for URL messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsa03](https://clawhub.ai/user/lsa03) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to fetch shared web article URLs and preserve their content as Markdown and related image files for analysis, archiving, or follow-on agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional auto-fetch hook can execute shell commands from crafted chat URLs. <br>
Mitigation: Do not enable the hook until execution is argument-based, URL validation is added, shell metacharacters are blocked, and domain and private-network safeguards are in place. <br>
Risk: Authenticated browser state or Cookie headers may expose account-access data when fetching protected sites. <br>
Mitigation: Avoid storing Doubao cookies or pasting Cookie headers unless the operator understands the account-access risk and can remove saved profiles and output files afterward. <br>
Risk: Fetching arbitrary URLs can retrieve untrusted or sensitive network content. <br>
Mitigation: Restrict allowed domains where possible, review generated Markdown before reuse, and avoid running the skill against private-network or confidential URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lsa03/amber-url-to-markdown) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lsa03) <br>
- [Project repository listed in artifact metadata](https://github.com/OrangeViolin/amber-url-to-markdown) <br>
- [Artifact README](artifact/README.md) <br>
- [Auto-fetch hook documentation](artifact/hooks/url-auto-fetch/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with relative image references, plus console status text and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Markdown output under /root/openclaw/urltomarkdown and may create per-article image folders.] <br>

## Skill Version(s): <br>
4.0.3 (source: server release evidence and changelog, released 2026-03-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
