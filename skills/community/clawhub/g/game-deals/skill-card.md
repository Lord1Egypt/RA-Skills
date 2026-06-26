## Description: <br>
Looks up current free and limited-time game offers from Steam and Epic Games and formats the results for an agent response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[testmtcode](https://clawhub.ai/user/testmtcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to check current free-game offers and limited-time promotions from Steam and Epic Games. It is useful for generating concise game-deal summaries with claim links and offer timing. <br>

### Deployment Geography for Use: <br>
Global, with Epic Games Store results configured for the China region. <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Steam and Epic public services when invoked. <br>
Mitigation: Use explicit prompts to control activation, and only configure recurring cron checks when ongoing network access is intended. <br>
Risk: Steam results may be general free-to-play recommendations rather than limited-time promotions. <br>
Mitigation: Treat Steam output as recommendations and verify availability on Steam before presenting a deal as time-limited. <br>
Risk: Epic Games Store results are configured for the China region. <br>
Mitigation: Confirm regional availability before using Epic results for users outside that region. <br>


## Reference(s): <br>
- [ClawHub Game Deals release page](https://clawhub.ai/testmtcode/game-deals) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/testmtcode) <br>
- [Epic Games Store free games promotions endpoint](https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions) <br>
- [Steam Store search endpoint](https://store.steampowered.com/api/search) <br>
- [Steam Free to Play page](https://store.steampowered.com/genre/Free%20to%20Play/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Formatted text or Markdown with game titles, offer status, dates, and links; scripts may also be invoked from shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on public Steam and Epic services; Epic queries are configured with zh-CN locale and CN country parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
