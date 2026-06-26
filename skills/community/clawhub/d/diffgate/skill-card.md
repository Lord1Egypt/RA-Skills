## Description: <br>
Compare two texts and return a unified diff with a similarity score, line-level addition and deletion counts, and individual change records for LLM output comparison, content integrity checks, and document-change tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Diffgate to run local text comparisons through an API when checking LLM output consistency, document integrity, skill-version diffs, or configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Binding the local API to a public network interface could let unintended users submit text for comparison or receive diff output. <br>
Mitigation: Keep the uvicorn server bound to localhost unless network access is intentional and controlled. <br>
Risk: Diff responses include changed input content, so sensitive text may appear in returned output. <br>
Mitigation: Avoid submitting sensitive text unless it is acceptable for that text to appear in the returned diff. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text] <br>
**Output Format:** [JSON response containing similarity, additions, deletions, and changed-line records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Input text fields are capped at 500,000 characters each.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
