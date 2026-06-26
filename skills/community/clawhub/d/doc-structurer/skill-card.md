## Description: <br>
Analyzes parsed document text, classifies document types, and converts key information into structured JSON for downstream document pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators working with parsed document batches use this skill to classify business documents and extract titles, dates, parties, priorities, financial fields, related documents, and action-oriented metadata into a JSON structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Structured output may contain sensitive information from contracts, invoices, personal records, or confidential business documents. <br>
Mitigation: Review structured_results.json before passing it to Notion, Apple Calendar, or any other sync skill. <br>
Risk: Document classification and extracted fields may be incomplete or low confidence for ambiguous inputs. <br>
Mitigation: Check the processing summary and review records with low classification confidence or missing fields before downstream use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkbeomjun-gkgkgk/doc-structurer) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands] <br>
**Output Format:** [JSON file plus brief text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads parsed_results.json and writes structured_results.json by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
