## Description: <br>
Search Deutsche Bahn train connections using the bahn-cli tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobiasbischoff](https://clawhub.ai/user/tobiasbischoff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find Deutsche Bahn train connections between German stations, including departure times, durations, platforms, changes, stops, and train numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run a local Node.js bahn-cli project and install its dependencies if needed. <br>
Mitigation: Install and run it only when ~/Code/bahn-cli is the intended train-search project, and review that project's package.json and dependencies before running npm install. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and summarized train-search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include departure and arrival times, platform numbers, duration, changes, intermediate stops, and train numbers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
