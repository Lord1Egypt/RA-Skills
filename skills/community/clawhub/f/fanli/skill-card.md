## Description:

Converts shopping links or share codes into coupon-backed promotional links, compares prices across Taobao, Tmall, JD, Pinduoduo, Douyin, Vipshop, and Meituan, checks price history, and gives purchase guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping-assistant agents use Fanli to turn product or Meituan links into coupon and promotional links, compare marketplace prices, inspect historical pricing, and produce a concise buy-or-wait recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping links may contain account-specific or private parameters and are sent to a remote feima-lab/fenxianglife API for parsing.

Mitigation: Avoid submitting private shopping URLs or account-specific parameters unless the user trusts the publisher and remote API.

Risk: The server security summary flags use of an unpinned external helper with API-key access.

Mitigation: Prefer a pinned, reviewed fx-base version and provide FX_AI_API_KEY only in environments where the publisher and helper are trusted.

Risk: Generated purchase links, images, and prices come from a remote service and may be inaccurate or unsafe.

Mitigation: Verify product details, destination URLs, and final prices on the merchant site before purchase.

Risk: The server security summary flags an unsafe local script dispatch path.

Mitigation: Run the skill in a constrained agent environment and review allowed script names before enabling execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/fanli)
- [feima-lab open platform](https://platform.feima.ai/)
- [convert output template](references/convert-output.md)
- [compare-price output template](references/compare-price-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown purchase cards and recommendations, with optional JSON or table output from local Node.js commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FX_AI_API_KEY and sends submitted shopping links or share codes to the feima-lab/fenxianglife API.]

## Skill Version(s):

4.2.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
