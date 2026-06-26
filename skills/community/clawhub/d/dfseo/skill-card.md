## Description: <br>
dfseo-cli helps agents use DataForSEO APIs from the terminal for SERP analysis, keyword research, site audits, backlink analysis, and related SEO workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricca91](https://clawhub.ai/user/ricca91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SEO practitioners, developers, and agents use this skill to run DataForSEO-backed keyword, SERP, site audit, and backlink workflows from a command-line interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DataForSEO credentials or local dfseo configuration could be exposed if handled carelessly. <br>
Mitigation: Use environment variables or interactive setup, avoid passing passwords on the command line, and protect ~/.config/dfseo/config.toml. <br>
Risk: Large target files or broad SEO jobs may submit unintended domains or incur billable API usage. <br>
Mitigation: Review --from-file inputs before execution and use --dry-run or explicit limits for large jobs. <br>
Risk: The skill depends on the external dfseo package and a DataForSEO account. <br>
Mitigation: Install only when the dfseo package source and DataForSEO account usage are trusted. <br>


## Reference(s): <br>
- [dfseo SERP Commands Reference](references/serp.md) <br>
- [dfseo Keywords Commands Reference](references/keywords.md) <br>
- [dfseo Site Audit Commands Reference](references/site.md) <br>
- [dfseo Backlinks Commands Reference](references/backlinks.md) <br>
- [ClawHub release page](https://clawhub.ai/ricca91/dfseo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline shell commands; generated dfseo commands commonly return JSON, table, or CSV output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [dfseo defaults to JSON on stdout, uses stderr for errors and progress, and supports dry-run for cost estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
