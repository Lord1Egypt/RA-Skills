## Description: <br>
Use ddgr to run privacy-focused DuckDuckGo searches from the command line, including text results, site-specific searches, bangs, and JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shelehovnick1-spec](https://clawhub.ai/user/shelehovnick1-spec) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and terminal-focused users use this skill to ask an agent for ddgr installation help and command examples for web research, news lookup, documentation search, and quick facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing ddgr with sudo or from source can execute code from an untrusted package source or repository. <br>
Mitigation: Install ddgr only from a package source or repository the user trusts, and review commands before running them with elevated privileges. <br>
Risk: Search queries are sent to a web service, and bangs or automatic browser opening may contact additional sites. <br>
Mitigation: Avoid searching for passwords, tokens, private documents, or other secrets, and treat bangs and browser-opening commands as external site interactions. <br>
Risk: Unsafe search mode can return results that normal safe-search settings would filter. <br>
Mitigation: Use safe-search defaults unless the user explicitly asks to disable them and understands the content exposure tradeoff. <br>


## Reference(s): <br>
- [ddgr common usage patterns](references/usage-patterns.md) <br>
- [ddgr GitHub project](https://github.com/jarun/ddgr) <br>
- [DuckDuckGo](https://duckduckgo.com) <br>
- [DuckDuckGo Bangs](https://duckduckgo.com/bang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ddgr JSON-output command examples for scripted search workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
