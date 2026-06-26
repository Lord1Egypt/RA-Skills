## Description: <br>
Bracket Oracle helps agents generate NCAA March Madness bracket recommendations using Torvik or optional KenPom ratings, Monte Carlo tournament simulation, and pool-aware strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lastandy](https://clawhub.ai/user/lastandy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch basketball ratings, simulate NCAA tournament outcomes, analyze public-pick value, and produce bracket strategies for pools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes sports-data web requests and stores local JSON caches. <br>
Mitigation: Use a virtual environment, inspect requested network access, and keep cached data in the local workspace. <br>
Risk: Optional KenPom access uses user-provided subscription credentials. <br>
Mitigation: Only provide credentials through environment variables when the dependency and publisher are trusted. <br>
Risk: Bracket submissions or ESPN pool actions could affect public competitions. <br>
Mitigation: Require explicit human approval before submitting GitHub pull requests or taking ESPN pool actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lastandy/bracket-oracle) <br>
- [Agent Bracket League 2026](https://github.com/lastandy/bracket-league-2026) <br>
- [ESPN Tournament Challenge group](https://fantasy.espn.com/games/tournament-challenge-bracket-2026/group?id=83062dd9-bc6e-4867-896e-d57926480488) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated bracket data is represented as Python dictionaries or JSON-serializable structures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch sports ratings and public-pick data over HTTP and cache JSON files locally.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
