## Description:

Unified entry skill for RealMarket A2A commerce workflows. Supports seller product publish and buyer product discovery through UCP market connectivity, plus end-to-end order orchestration modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill as an A2A commerce entrypoint to publish seller products, discover buyer products, and coordinate marketplace workflow contracts. It can route related identity, negotiation, staking, payment, order lifecycle, and realtime event tasks to module-level skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Networked marketplace actions may target untrusted or unintended domains.

Mitigation: Use only trusted marketplace domains and prefer explicit HTTPS URLs until domain allowlisting, endpoint validation, and HTTPS-only behavior are in place.

Risk: Seller publish mode can create product listings with supplied name, price, category, and stock details.

Mitigation: Require human confirmation of seller publish actions and review product details before execution.

Risk: Running against privileged or internal-network environments could broaden the impact of discovered endpoint calls.

Mitigation: Run with least privilege and avoid internal-network environments unless the marketplace domain and endpoint are explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/skills/a2a-supermarket)
- [Skill documentation](SKILL.md)
- [CLI entrypoint](src/cli/index.js)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json]

**Output Format:** [JSON CLI responses with concise text or markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seller mode returns seller_publish results; buyer mode returns buyer_discover product listings. The executable path performs networked marketplace requests against discovered UCP REST endpoints.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
