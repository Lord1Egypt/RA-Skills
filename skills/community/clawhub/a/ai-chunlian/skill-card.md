## Description: <br>
AI春联生成专家，根据用户提供的场景、氛围或关键词，生成富有意境的春联。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liulian822](https://clawhub.ai/user/liulian822) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this paid ClawHub skill to generate Chinese Spring Festival couplets from a scene, mood, or keyword after completing the configured payment flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags mismatched service identity in payment records and instructions. <br>
Mitigation: Review the order details before payment and ask the publisher to fix the service-identity mismatch before normal use. <br>
Risk: Payment configuration can change the actual payee and amount. <br>
Mitigation: Confirm the payee, amount, and active configuration file before installing or paying. <br>
Risk: The skill stores order and payment workflow data locally and the security review says that storage is under-disclosed. <br>
Mitigation: Avoid entering sensitive text as the couplet prompt and review local storage behavior before use. <br>
Risk: The skill depends on a separate payment skill and payment credential flow. <br>
Mitigation: Verify the separate clawtip payment skill and ensure payment credentials are handled only through the expected flow. <br>
Risk: The security review flags a mismatch between the documented generation command and the artifact behavior. <br>
Mitigation: Confirm the required command arguments before execution and ask the publisher to fix the command mismatch before normal use. <br>
Risk: The artifact includes a thought-process instruction in the user-facing skill text. <br>
Mitigation: Ask the publisher to remove the thought-process instruction before normal use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liulian822/ai-chunlian) <br>
- [Publisher profile](https://clawhub.ai/user/liulian822) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Chinese text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces payment status plus a horizontal scroll title, upper line, and lower line when payment verification succeeds.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
