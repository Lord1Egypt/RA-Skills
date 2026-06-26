## Description: <br>
Answers Chinese bill-finance product questions by retrieving from the bundled bill_knowledge Markdown knowledge base and citing source files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krillingone](https://clawhub.ai/user/krillingone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users and support agents use this skill to answer questions about bill products, discounting, financing, signing, quotas, quotes, contracts, invoices, letters of credit, disclosure, channels, coupons, and related platform workflows from local knowledge-base documents. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Financial and banking workflow guidance may be mistaken for authoritative transaction approval. <br>
Mitigation: Use answers as informational support only, and independently confirm transaction, account, disclosure, rate, and contract details through verified official banking or platform channels before acting. <br>
Risk: Users may expose passwords, SMS codes, ID images, bank account details, tax credentials, or facial-verification material while asking for help. <br>
Mitigation: Do not paste sensitive credentials or identity materials into chat; complete authentication, tax authorization, identity checks, and banking actions only through verified official channels. <br>
Risk: Product steps, pricing, timelines, and platform screens may become stale or may not cover the user's exact case. <br>
Mitigation: Cite the local source files used for each answer and direct users to the official platform or relevant bank contact for current terms and case-specific confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krillingone/bill-product-knowledge) <br>
- [富票融平台](https://p.fbank.com/home/ticket) <br>
- [票交所信披平台](http://disclosure.shcpe.com.cn/) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown answers with cited source filenames and an official platform link when applicable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only retrieval over local Markdown files; no code execution or API calls.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
