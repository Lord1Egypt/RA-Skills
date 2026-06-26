## Description: <br>
EU AI Act risk classification, Article 12 compliance logging, and self-assessment reports — deadline August 2, 2026 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, compliance teams, and AI system operators use this skill to classify EU AI Act risk, map Article 12 logging requirements, and request self-assessment or compliance documentation from the SputnikX service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid report endpoints may send AI-system details to a third-party compliance service and can incur x402 USDC charges. <br>
Mitigation: Confirm the exact endpoint, submitted data, provider terms, and quoted charge before calling paid report endpoints; avoid submitting sensitive internal AI-system details unless the terms meet privacy and compliance needs. <br>
Risk: Compliance classifications and generated reports may be incomplete or unsuitable for a specific legal context. <br>
Mitigation: Treat outputs as compliance-support material and review them with qualified legal or governance stakeholders before relying on them for EU AI Act obligations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drivenbymyai-max/eu-ai-compliance) <br>
- [SputnikX compliance web interface](https://soulledger.sputnikx.xyz/compliance) <br>
- [SputnikX compliance API base URL](https://soul.sputnikx.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text, markdown] <br>
**Output Format:** [Markdown guidance with curl command examples and service-generated JSON or report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No local code execution or credential environment variables are required by the skill; paid endpoints disclose x402 USDC charges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
