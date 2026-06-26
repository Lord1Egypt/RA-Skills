## Description: <br>
Fetches historical K-line data for A-share stocks and major Chinese indexes, using AKShare first and Sina Finance as a fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mc82465](https://clawhub.ai/user/mc82465) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve A-share stock and index K-line data, calculate price changes, and build simple market-data workflows in Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised today quote path can return stale March 2026 data. <br>
Mitigation: Validate the returned quote date or fix the hard-coded AKShare date window before using it for real-time financial decisions. <br>
Risk: The skill makes outbound requests to AKShare and Sina Finance market-data endpoints. <br>
Mitigation: Use it only in environments where third-party market-data access is allowed, and treat upstream availability as a dependency. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mc82465/get-stock-line) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and Python snippets describing structured dictionaries and lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return market-data dictionaries or lists from external AKShare and Sina Finance requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
