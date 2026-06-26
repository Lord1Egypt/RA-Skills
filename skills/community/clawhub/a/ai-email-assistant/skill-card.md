## Description: <br>
AI-powered email writing, review, and compliance checking. Generate templates, optimize subject lines, audit for spam triggers, and check CAN-SPAM/GDPR/CASL compliance. Powered by evolink.ai <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and marketing or operations teams use this skill to generate email templates, review drafts for spam and deliverability issues, create subject-line variants, translate emails, check CAN-SPAM/GDPR/CASL considerations, and get SPF/DKIM/DMARC setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI commands transmit selected email drafts or templates to Evolink for processing by Claude. <br>
Mitigation: Use AI commands only with content you are comfortable sending to Evolink; redact customer, regulated, legal, or confidential business information before analysis. <br>
Risk: The EVOLINK_API_KEY grants access to the external AI service. <br>
Mitigation: Store the API key securely, avoid committing it to files or logs, and rotate it if exposure is suspected. <br>
Risk: Compliance output can miss legal nuance for CAN-SPAM, GDPR, CASL, or local requirements. <br>
Mitigation: Treat compliance results as drafting assistance and have high-risk or production campaigns reviewed by qualified counsel or compliance staff. <br>
Risk: Server evidence includes unrelated crypto, wallet, and purchase capability tags. <br>
Mitigation: Do not rely on those tags to describe this release's behavior; publisher should correct the tags in ClawHub metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evolinkai/ai-email-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/evolinkai) <br>
- [Project homepage from ClawHub metadata](https://github.com/EvoLinkAI/email-skill-for-openclaw) <br>
- [EvoLink API documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=email) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, Markdown-style analysis, HTML email templates, translated email content, and DNS configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI commands send selected email content to api.evolink.ai and use EVOLINK_API_KEY; local template-listing and DNS guidance commands do not require network access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, target metadata, frontmatter, and package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
