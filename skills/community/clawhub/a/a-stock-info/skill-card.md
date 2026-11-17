## Description:

A Stock Info queries A-share minute-level market data through the qgdata API, with realtime quote and trade-detail commands currently represented as unfinished placeholders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[listolany](https://clawhub.ai/user/listolany)

### License/Terms of Use:


## Use Case:

External developers and quantitative analysts use this skill to run qgdata-backed A-share minute K-line queries from an agent workflow. It is appropriate for data lookup and analysis support, not unsupervised trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes a real-looking QGDATA_TOKEN and suggests storing credentials in a plaintext .env file.

Mitigation: Use a user-owned QGDATA_TOKEN, rotate any copied example token, prefer environment injection, and lock down permissions for any local credential file.

Risk: Realtime quote and trade-detail commands are advertised, but the security evidence says those capabilities appear unfinished.

Mitigation: Validate the command output before relying on it and treat minute-level K-line queries as the primary working capability.

Risk: The skill handles market data that could influence financial decisions.

Mitigation: Use the output for data retrieval and analysis support only, with human review and independent verification before trading or investment action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/listolany/skills/a-stock-info)
- [Publisher profile](https://clawhub.ai/user/listolany)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact query script](artifact/scripts/astock_query.py)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [JSON responses from a Python command-line script, with setup and usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and QGDATA_TOKEN; qgdata and pandas must be installed for the script examples to run.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
