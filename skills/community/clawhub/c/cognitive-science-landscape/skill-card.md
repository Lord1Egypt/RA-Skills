## Description: <br>
Maps cognitive failures across eight interconnected domains, identifies the primary bottleneck and upstream dependencies, and guides selection of a targeted intervention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to diagnose broad thinking, learning, decision-making, communication, or cognitive-performance problems by identifying the cognitive domain bottleneck and upstream dependencies before recommending an intervention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad activation language may select this skill when a more specific cognitive-domain skill is already appropriate. <br>
Mitigation: Confirm the user's concrete case and switch to a more specific skill when the cognitive domain or problem type is already clear. <br>
Risk: Users may treat reflective cognitive coaching as medical or mental-health advice. <br>
Mitigation: Frame outputs as coaching guidance only, avoid diagnosis or treatment claims, and direct clinical or mental-health concerns to qualified professionals. <br>
Risk: An unsupported domain assignment can lead to ineffective or misleading interventions. <br>
Mitigation: Require observable behavioral evidence and map upstream dependencies before recommending domain-specific tools. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deciqai/skills/cognitive-science-landscape) <br>
- [Sources - Cognitive Science Landscape](references/sources.md) <br>
- [Method in Action: The 1956 MIT Symposium and the Birth of Cognitive Science](examples/the-1956-mit-symposium-and-the-birth-of-cognitive-science-1956.md) <br>
- [Neisser, Cognitive Psychology](https://archive.org/details/cognitivepsychol00neis) <br>
- [Baddeley and Hitch, Working Memory](https://doi.org/10.1016/S0079-7421(08)60452-1) <br>
- [Miller, The Magical Number Seven, Plus or Minus Two](https://doi.org/10.1037/h0043158) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown coaching response with a cognitive domain map] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause for user responses in coach mode; requires user-specific behavioral evidence before domain assignment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
