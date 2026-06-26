## Description: <br>
Opens the 1688 product image optimization page and, when a product ID is present, includes it in the page URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and 1688 shop operators use this skill to open a product image optimization workflow for main product images, optionally scoped to a detected offer ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The released package includes CLI configuration behavior for a 1688 access key, even though the advertised workflow is a simple page opener. <br>
Mitigation: Use the open_tab interaction only unless API-key configuration is intentionally needed and reviewed. <br>
Risk: Providing a 1688 access key may store it in local OpenClaw configuration or send it to a configured OpenClaw gateway. <br>
Mitigation: Review the configured gateway and local OpenClaw settings before entering credentials. <br>
Risk: CLI use may report usage metadata. <br>
Mitigation: Avoid running the bundled CLI in environments where usage telemetry is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-item-image-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [Interaction component specification](references/interaction-specs.md) <br>
- [1688 image optimization page](https://air.1688.com/app/CSBC-modules/csbc-ai-component-loader/picture-optimize.html) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance] <br>
**Output Format:** [JSON open_tab interaction payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include an offerId query parameter when a product ID is available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
