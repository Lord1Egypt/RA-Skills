## Description: <br>
Generates product mockups by compositing a user-provided decoration onto a blank product image, then reviewing and tuning placement before returning the rendered mockup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmtucker](https://clawhub.ai/user/zmtucker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to preview how logos or graphics look on apparel and product blanks, including placement edits, background removal, and saved placement-rule tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local mockup outputs and can persist edited placement defaults. <br>
Mitigation: Use the default MOCKUP_DATA_DIR where possible and confirm before saving tuned placement changes as future defaults. <br>
Risk: Untrusted --rules or --output paths could direct reads or writes to unintended locations. <br>
Mitigation: Avoid passing untrusted paths to --rules or --output and verify input and output paths before running the scripts. <br>
Risk: First-run background removal and garment detection depend on a cached rembg model; blocked downloads can degrade detection or stop background removal. <br>
Mitigation: Install dependencies in advance and verify the first-run model cache before relying on automated background removal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/drivethru-graphic-artist) <br>
- [Decoration spec](references/decoration_spec.md) <br>
- [Self-review loop](references/self_review.md) <br>
- [Iterative feedback](references/iterative_feedback.md) <br>
- [Placement rules schema](references/placement_rules_schema.json) <br>
- [rembg](https://github.com/danielgatis/rembg) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [PNG mockup files with JSON receipts and concise Markdown or text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes mockup outputs locally and may persist edited placement defaults in the configured MOCKUP_DATA_DIR.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
