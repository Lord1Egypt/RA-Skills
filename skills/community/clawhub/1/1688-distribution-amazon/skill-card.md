## Description: <br>
Creates Dianxiaobao Amazon pending-product drafts from 1688 product data through an e-commerce automation workflow that checks credentials, maps categories and attributes, processes images, builds listing payloads, and saves drafts without directly publishing to Amazon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and e-commerce operators use this skill to turn 1688 product offers into Amazon draft listings in Dianxiaobao. The skill is intended for guided draft creation; final Amazon publishing remains a separate user action in Dianxiaobao. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses Dianxiaobao user identity and gateway credentials to query stores, retrieve product data, process images, and create Amazon draft listings. <br>
Mitigation: Install only when this access is intended; keep .env files and generated /tmp session directories private. <br>
Risk: Generated session directories may contain workflow artifacts tied to stores, products, or draft creation. <br>
Mitigation: Delete old session directories when the saved workflow artifacts are no longer needed. <br>
Risk: Users may expect direct Amazon publishing even though the skill only creates Dianxiaobao pending-product drafts. <br>
Mitigation: Confirm that successful completion means a Dianxiaobao draft was saved and direct users to finish publishing from Dianxiaobao. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/1688aiinfra/1688-distribution-amazon) <br>
- [Amazon Listing Chain Reference](references/amazon-listing-chain.md) <br>
- [Amazon Listing Troubleshooting](references/troubleshooting.md) <br>
- [Dianxiaobao Amazon pending-products page](https://page.1688.com/html/isv-bridge.html?version=0.0.26&appKey=5050627&role=buyer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces session-scoped workflow artifacts under /tmp and returns draft identifiers such as localId when Dianxiaobao saves a draft successfully.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence; artifact metadata lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
