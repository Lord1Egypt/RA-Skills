## Description:

Helps agents query the CDISC Library API for clinical data standards including QRS instruments, ADaM, CDASH, SDTM, and controlled terminology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whereayan](https://clawhub.ai/user/whereayan)

### License/Terms of Use:


## Use Case:

Developers, data managers, and clinical standards users can use this skill to look up CDISC products, questionnaires, domains, rules, terminology, version comparisons, and exports through the CDISC Library API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential loading can pick up an unrelated API key from a shared local TOOLS.md file and send it to the CDISC API.

Mitigation: Prefer CDISC_API_KEY through the environment or a secret manager, and avoid putting API keys in shared or committed TOOLS.md files.

Risk: The skill contacts the external CDISC API and caches responses locally.

Mitigation: Use it only in approved network environments, review whether queried data should be cached, and clear the cache when local retention is not appropriate.

Risk: Export commands write JSON or CSV files into the current working directory and may overwrite existing files with the same generated name.

Mitigation: Run exports from a directory where generated files are expected, and move or rename existing exports before repeating a query.

## Reference(s):

- [CDISC Library Browser](https://library.cdisc.org/browser)
- [CDISC API Portal](https://api.developer.library.cdisc.org)
- [CDISC API Documentation](https://api.developer.library.cdisc.org/api-details)
- [CDISC API Profile](https://api.developer.library.cdisc.org/profile)
- [CDISC Skill Quick Reference](artifact/assets/quickref.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with command examples, API query results, and optional JSON or CSV export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can contact the CDISC API, cache API responses locally for one hour, and write JSON or CSV exports to the current directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog lists 1.0 released 2026-03-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
