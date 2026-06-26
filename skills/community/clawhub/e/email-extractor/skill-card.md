## Description: <br>
Extract and deduplicate up to 20 email addresses from webpage URLs or plain text content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loverun321](https://clawhub.ai/user/loverun321) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents can use this skill to extract email addresses from authorized webpage URLs or supplied text, deduplicate them, and return a capped result set. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unscoped URL fetching can process pages the user is not authorized to fetch or inspect. <br>
Mitigation: Use the skill only with authorized public pages or text supplied for extraction, and avoid private or internal URLs. <br>
Risk: The release evidence flags an unrelated apparent API key/payment signal and says not to rely on the payment_status output. <br>
Mitigation: Remove or rotate the exposed key, clarify payment handling before release, and verify billing or payment state outside this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loverun321/email-extractor) <br>
- [Publisher profile](https://clawhub.ai/user/loverun321) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON object containing extracted emails, a count, and status or error fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deduplicates extracted addresses and caps results at 20 unique emails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
