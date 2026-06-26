## Description: <br>
Multi-language, multi-currency global invoice recognition and extraction that helps agents extract invoice number, date, supplier, buyer, currency, tax amount, total amount, and line items as structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
External users, finance teams, and developers use this skill to guide an agent through ADP CLI setup, credential configuration, invoice app selection, and extraction of structured invoice data from local files, URLs, Base64 input, batches, or async tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends invoices and related business documents to Laiye ADP's cloud service, which may expose sensitive financial or business data to third-party processing. <br>
Mitigation: Use it only when ADP's API, billing, privacy, and retention terms are acceptable for the documents being processed, and avoid submitting data that is not approved for that service. <br>
Risk: The skill requires sensitive credentials for ADP service access. <br>
Mitigation: Use a scoped API key when available, store credentials through the ADP CLI configuration flow, and avoid sharing keys in prompts, logs, or exported files. <br>
Risk: The artifact includes broader document-processing and custom app-management commands beyond invoice extraction. <br>
Mitigation: Prefer the out-of-the-box invoice extraction workflow and avoid custom-app administrative commands unless the user explicitly intends to manage ADP configuration. <br>
Risk: Batch exports can write extracted invoice data to local paths. <br>
Mitigation: Choose secure local export directories and protect generated JSON files according to the sensitivity of the source invoices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/adp-invoice-recognition-and-extract) <br>
- [ADP Global portal](https://adp-global.laiye.com/) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh) <br>
- [ADP OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of the ADP CLI, API key configuration, app ID caching, local or URL-based invoice extraction, batch export paths, and async result queries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
