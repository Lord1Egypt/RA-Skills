## Description:

Turn an Amazon product link into an evidence-based short-form video script by extracting listing selling points, mining real buyer language from embedded reviews, and producing a shot-by-shot script after the user chooses a content direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyu-xixihaha](https://clawhub.ai/user/chengyu-xixihaha)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, sellers, and content teams use this skill to turn a single Amazon product page into an evidence-backed UGC, ad, or short-form social video script. The workflow is intended to reduce copywriting guesswork by grounding scripts in listing claims and buyer language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may encounter Amazon login-gated review pages or authentication prompts while collecting reviews.

Mitigation: Use only the embedded reviews available on the product page and do not provide or request Amazon credentials.

Risk: Amazon page access can return incomplete, geolocated, or anti-bot affected listing data.

Mitigation: Use browser automation instead of bare HTTP requests, flag non-US pricing when detected, and avoid presenting thin review coverage as comprehensive.

Risk: The generated script may overstate product claims if unsupported copy is added during scriptwriting.

Mitigation: Keep each script line traceable to a listing detail or authentic buyer quote gathered earlier in the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chengyu-xixihaha/skills/amazon-product-analysis)
- [Publisher Profile](https://clawhub.ai/user/chengyu-xixihaha)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown brief and shot-by-shot script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local insights.md and script.md files for the selected Amazon product; does not generate video.]

## Skill Version(s):

1.0.0 (source: release evidence and config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
