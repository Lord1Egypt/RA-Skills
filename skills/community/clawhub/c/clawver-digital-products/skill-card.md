## Description: <br>
Create and sell digital products on Clawver by uploading files, setting pricing, publishing listings, and tracking downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwang783](https://clawhub.ai/user/nwang783) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External sellers and developers use this skill to create, upload, publish, manage, and monitor downloadable Clawver marketplace products such as art packs, ebooks, templates, software, and other digital goods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API examples can change live Clawver product listings, including prices, status, uploaded files, and archive actions. <br>
Mitigation: Review product IDs, prices, status changes, file uploads, and archive commands before execution; prefer setting a product to draft before archive actions unless the effect is intended. <br>
Risk: Use of CLAW_API_KEY authorizes marketplace management actions for the seller account. <br>
Mitigation: Use a scoped or revocable API key when available and avoid exposing the key in shared logs, prompts, or generated artifacts. <br>


## Reference(s): <br>
- [Clawver homepage](https://clawver.store) <br>
- [Digital Products API Examples](references/api-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/nwang783/clawver-digital-products) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_API_KEY and seller-side review before executing API calls that modify listings or generate download links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
