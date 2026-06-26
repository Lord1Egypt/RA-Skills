## Description: <br>
Queries the CDISC Library API for clinical data standards including QRS instruments, ADaM, CDASH, SDTM, and controlled terminology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whereayan](https://clawhub.ai/user/whereayan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, clinical data standards specialists, and agents use this skill to retrieve, compare, search, cache, and export CDISC Library API content for clinical standards workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the CDISC API using a local API key. <br>
Mitigation: Prefer setting CDISC_API_KEY in the environment and review the workspace before installing or running the skill. <br>
Risk: The skill can read API keys from TOOLS.md, which may also contain unrelated secrets. <br>
Mitigation: Avoid installing it in workspaces where TOOLS.md contains unrelated API keys or sensitive credentials. <br>
Risk: The skill caches API responses locally and can read batch query files or write JSON/CSV exports. <br>
Mitigation: Review batch input files, output locations, and cache contents before and after use. <br>


## Reference(s): <br>
- [CDISC Library Browser](https://library.cdisc.org/browser) <br>
- [CDISC Library API Portal](https://api.developer.library.cdisc.org) <br>
- [CDISC Library API Documentation](https://api.developer.library.cdisc.org/api-details) <br>
- [Skill Usage Guide](SKILL.md) <br>
- [Quick Reference](assets/quickref.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/whereayan/cdisc-library-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown and terminal-style text; export commands can write JSON or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a CDISC API key, calls the CDISC API, caches responses locally for one hour, and supports batch query files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact changelog lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
