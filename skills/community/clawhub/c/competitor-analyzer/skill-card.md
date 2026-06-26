## Description: <br>
Generate a detailed competitive analysis report for a company, including overview, pricing, social presence, recent news, and SWOT-lite insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and business users can use this skill to generate a concise competitive intelligence report from a public company name or URL. It supports quick market research by collecting public web results and organizing them into overview, pricing, social, news, and assessment sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe input handling in the shell script can allow a crafted company name to run local Python commands. <br>
Mitigation: Review and fix the shell script before installation, replacing interpolated query encoding with safe argument passing. <br>
Risk: Using confidential company names, internal URLs, or private targets can expose sensitive research intent through web queries. <br>
Mitigation: Use only public company names or URLs and avoid confidential targets when running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claudiodrusus/competitor-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands] <br>
**Output Format:** [Markdown report printed to stdout and saved as a .md file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, Python 3, and internet access; report quality depends on public web search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
