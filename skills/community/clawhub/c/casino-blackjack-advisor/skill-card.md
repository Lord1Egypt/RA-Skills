## Description: <br>
Returns the mathematically optimal blackjack action (HIT/STAND/DOUBLE/SPLIT/SURRENDER) for any hand using perfect basic strategy for 6-deck S17 blackjack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to get a blackjack basic-strategy action for a supplied player hand and dealer upcard. It is intended for local command-line use when the table rules match the documented 6-deck S17 assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blackjack strategy guidance may be misunderstood as a guarantee of winnings or used when casino rules differ from the documented assumptions. <br>
Mitigation: Treat outputs as strategy guidance only, verify that the table uses the documented rules before relying on an action, and do not present the result as a guaranteed financial outcome. <br>
Risk: The package declares managed automaton cron metadata even though the observed behavior is a low-impact local calculator. <br>
Mitigation: Review the automaton configuration before enabling scheduled execution and run the advisor on demand unless scheduled behavior is explicitly intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/casino-blackjack-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, JSON, shell commands] <br>
**Output Format:** [JSON from a local Python CLI, with action, explanation, hand type, total, and confidence fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys or third-party dependencies; assumes 6 decks, dealer stands on soft 17, double after split allowed, and late surrender available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
