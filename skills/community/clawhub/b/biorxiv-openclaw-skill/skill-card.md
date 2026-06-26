## Description: <br>
Access bioRxiv preprints by category and date range, list supported subject collections, and retrieve paper metadata without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aquaskyline](https://clawhub.ai/user/aquaskyline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and agents use this skill to fetch recent biology preprints from bioRxiv, filter by supported subject collection and date range, and return paper metadata for summarization or topic discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to bioRxiv and depends on Python availability in the execution environment. <br>
Mitigation: Install only where outbound requests to bioRxiv are acceptable and Python command execution is permitted. <br>
Risk: Package provenance is unavailable and the release changelog is inaccurate. <br>
Mitigation: Review the packaged artifact files and scan results before deployment rather than relying on inferred source history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aquaskyline/biorxiv-openclaw-skill) <br>
- [bioRxiv API documentation](references/api.md) <br>
- [bioRxiv API](https://api.biorxiv.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON paper metadata returned from Python command-line usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network access to the public bioRxiv API is required; no authentication is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
