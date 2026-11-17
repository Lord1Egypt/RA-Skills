## Description:

FOMO Smart Money helps agents query FOMO App smart-money wallets and produce token-trending summaries from public wallet activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcii](https://clawhub.ai/user/0xcii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and crypto researchers use this skill to inspect ranked FOMO smart-money wallets, check live wallet balances, open chain explorer links, and summarize recent token buying activity. The output is research support for public wallet tracking, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading summaries can be stale or misleading because wallet snapshots age and live data can change quickly.

Mitigation: Use the live balance checks and chain explorer links before relying on a wallet signal, and treat outputs as research rather than financial advice.

Risk: Public wallet and token lookups are sent to blockchain RPC providers and DexScreener.

Mitigation: Use the skill only for public addresses and tokens where these network disclosures are acceptable.

Risk: Generated FOMO links use the default AntCaveClub referral code unless changed.

Mitigation: Review shared output for referral links and override the referral value with the documented command option when appropriate.

Risk: The trending script writes a home-directory marker file to track first-run banner display.

Mitigation: Run in an environment where this marker file is acceptable, or remove the marker after use if persistent local state is not desired.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/0xcii/skills/fomo-smart-money)
- [fomo-family-frontend.md](references/fomo-family-frontend.md)
- [FOMO App referral page](https://fomo.family/r/AntCaveClub)
- [FOMO App API base](https://prod-api.fomo.family)
- [Author Dune dashboard](https://dune.com/Aturx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal text with inline links and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language outputs; token links may include a configurable FOMO referral code.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
