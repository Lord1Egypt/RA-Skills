## Description: <br>
Use this skill when working with the `bwm` CLI, including Bing Webmaster API key setup, CLI authentication, site listing, traffic stats, URL index checks with explanation, URL submission, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NmadeleiDev](https://clawhub.ai/user/NmadeleiDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to install, authenticate, operate, and troubleshoot the Bing Webmaster `bwm` CLI for site listings, traffic statistics, URL index checks, and URL submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bing Webmaster API keys are sensitive and may be exposed through shell history, process listings, or shared local credential files. <br>
Mitigation: Prefer environment variables or the interactive prompt when practical, avoid passing keys inline on shared systems, avoid storing credentials on shared machines, and run `bwm auth clear` when finished. <br>
Risk: URL batch submission can send unintended URLs for indexing if the input file or site target is wrong. <br>
Mitigation: Review URL batch files and selected site values before submitting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NmadeleiDev/bing-webmaster-cli) <br>
- [Bing Webmaster Tools](https://www.bing.com/webmasters/) <br>
- [Bing Webmaster API access documentation](https://learn.microsoft.com/en-us/bingwebmaster/getting-access) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON, CSV, or table output mode guidance for `bwm` commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
