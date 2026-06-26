## Description: <br>
Sell print-on-demand merchandise on Clawver. Browse Printful catalog, create product variants, track fulfillment and shipping. Use when selling physical products like posters, t-shirts, mugs, or apparel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwang783](https://clawhub.ai/user/nwang783) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and store operators use this skill to create and manage Clawver print-on-demand merchandise, including catalog browsing, variant setup, design and mockup workflows, publishing, and fulfillment tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through live Clawver store changes, including product publishing and webhook setup. <br>
Mitigation: Use a scoped or revocable API key where available and confirm prices, variants, mockups, publish status, and webhook URLs before live changes. <br>
Risk: AI design and mockup generation can spend credits after plan approval. <br>
Mitigation: Review the proposed plan before approval and require explicit confirmation before generation or publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nwang783/clawver-print-on-demand) <br>
- [Clawver](https://clawver.store) <br>
- [Print-on-Demand API Examples](references/api-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_API_KEY for live Clawver API operations.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact frontmatter lists 1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
