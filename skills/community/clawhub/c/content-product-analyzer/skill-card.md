## Description: <br>
Produces commercial teardowns of posts, creator profiles, product pages, landing pages, or app pages from URLs, screenshots, or pasted text, including audience, positioning, growth, monetization, credibility, sentiment, and competitor insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoxinling](https://clawhub.ai/user/guoxinling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, indie builders, product teams, and developers use this skill to analyze content, creator profiles, product pages, landing pages, app pages, bundles, and competitors from user-provided materials or public URLs. It separates observed facts, supported inferences, and unknowns, then returns a structured summary, detailed teardown, and concrete recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mixed-mode analysis may process current public facts and public URLs. <br>
Mitigation: Use mixed mode only for public URLs or current public facts, and cite public sources for factual claims. <br>
Risk: Sensitive or confidential user-provided materials may be exposed in the chat context. <br>
Mitigation: Do not paste secrets, private customer data, cookies, tokens, or confidential screenshots unless that content is appropriate for the chat context. <br>
Risk: Sparse inputs can lead to low-confidence commercial conclusions. <br>
Mitigation: State uncertainty clearly, separate observed facts from supported inferences and unknowns, and keep recommendations lightweight when evidence is limited. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/guoxinling/content-product-analyzer) <br>
- [README](artifact/README.md) <br>
- [Single URL example prompt](artifact/examples/prompt_single.md) <br>
- [Bundle and competitor comparison example prompt](artifact/examples/prompt_bundle_compare.md) <br>
- [Screenshot and pasted text example prompt](artifact/examples/prompt_screenshot_text.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown structured summary, long-form teardown, and optional comparison table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cited public-source findings in mixed mode and a competitor comparison matrix when two or more competitors are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
