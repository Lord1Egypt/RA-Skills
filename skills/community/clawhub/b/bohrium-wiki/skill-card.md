## Description: <br>
Bohrium SciencePedia helps agents browse and search encyclopedia-style scientific topics through open.bohrium.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search SciencePedia topics, browse the major/level/field/topic hierarchy, and retrieve article text for scientific concepts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Bohrium access key and sends scientific queries to Bohrium's external API. <br>
Mitigation: Store the access key in a secret or environment variable, avoid logging request headers, and avoid sending private or sensitive queries unless approved for external sharing. <br>


## Reference(s): <br>
- [Bohrium SciencePedia API](https://open.bohrium.com/openapi/v1/literature-sage/wiki_v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bohrium access key; no CLI support.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
