## Description: <br>
Helps travelers narrow hotel choices to three options by comparing hotel search results, nearby points of interest, price, ratings, and fit with stated preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect trip constraints, search hotels and destination POIs with FlyAI commands, compare the best three hotel options, and present a concise recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install the FlyAI CLI globally with an unpinned @latest package. <br>
Mitigation: Review the package before installation, prefer a pinned or local install, and avoid sudo-based installation through an agent. <br>
Risk: The skill suggests disabling TLS certificate verification for travel searches. <br>
Mitigation: Use normal TLS verification for routine searches and treat certificate failures as a setup issue to fix rather than bypass. <br>
Risk: The skill can read and store travel preferences, budget, companions, and special needs in memory or a local profile file. <br>
Mitigation: Ask for user consent before saving preferences and avoid storing sensitive details beyond what is needed for travel recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-hotel-picker) <br>
- [search-hotel reference](reference/search-hotel.md) <br>
- [search-poi reference](reference/search-poi.md) <br>
- [search-marriott-hotel reference](reference/search-marriott-hotel.md) <br>
- [user-profile-storage reference](reference/user-profile-storage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown travel recommendation with comparison sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hotel names, prices, ratings, location analysis, recommendation rationale, and links returned by FlyAI search commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
