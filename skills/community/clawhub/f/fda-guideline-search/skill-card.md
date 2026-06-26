## Description: <br>
Search FDA industry guidelines by therapeutic area or topic. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Regulatory affairs, clinical development, and agent developers can use this skill to explore FDA and ICH guidance search workflows by therapeutic area, document type, year, and keyword. Results should be treated as non-authoritative demonstration output and verified directly against FDA or ICH sources before use in regulatory work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synthetic FDA-guidance results may be presented as real regulatory search results. <br>
Mitigation: Treat outputs as non-authoritative demonstration data and verify any cited guidance directly with FDA or ICH sources before relying on it. <br>
Risk: The skill can perform network requests and write downloaded files to a local cache. <br>
Mitigation: Run it in a sandboxed workspace, review cache/output paths, and enable downloads only when needed. <br>
Risk: Regulatory or medical-development decisions could be affected by incomplete or outdated search results. <br>
Mitigation: Require qualified regulatory review and use official source documents as the decision record. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/fda-guideline-search) <br>
- [FDA Search Strategy](references/search-strategy.md) <br>
- [Therapeutic Area Mappings](references/area-mappings.json) <br>
- [FDA API Documentation Notes](references/fda-api-notes.md) <br>
- [FDA Guidance Index](https://www.fda.gov/regulatory-information/search-fda-guidance-documents) <br>
- [FDA Drug Guidance Documents](https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs) <br>
- [ICH Guidelines Database](https://database.ich.org/home) <br>
- [openFDA APIs](https://open.fda.gov/apis/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON from the Python CLI, with optional cached PDF files when download is enabled.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rate-limited external requests and local cache writes may occur; reported guidance results are non-authoritative demonstration data unless the implementation is changed to retrieve and validate actual FDA or ICH records.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
