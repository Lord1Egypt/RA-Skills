## Description:

Fetches free and limited-time game deal information from Epic Games and Steam.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testmtcode](https://clawhub.ai/user/testmtcode)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to check current Epic Games and Steam free-game offers, then share formatted results or set up recurring deal checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts public Steam and Epic endpoints that may be unavailable, rate-limited, region-specific, or changed without notice.

Mitigation: Treat returned deals as leads and verify availability on the official store pages before relying on them.

Risk: Steam results may include free-to-play recommendations rather than true limited-time giveaways.

Mitigation: Label Steam results as free-to-play or recommended free games unless the store page confirms a limited-time promotion.

Risk: Optional cron setup can create recurring background checks.

Mitigation: Add the cron job only when daily checks are desired and document how to remove or disable it.

Risk: The Python scripts require the third-party requests package.

Mitigation: Install dependencies in a virtual environment and pin versions for managed deployments.

## Reference(s):

- [ClawHub Game Deals release page](https://clawhub.ai/testmtcode/skills/game-deals)
- [Epic Games Store free games promotions endpoint](https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions)
- [Steam Store search endpoint](https://store.steampowered.com/api/search)
- [Steam free-to-play store page](https://store.steampowered.com/genre/Free%20to%20Play/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Formatted text and Markdown with store links and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on public Steam and Epic endpoints, regional availability, and current store data.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
