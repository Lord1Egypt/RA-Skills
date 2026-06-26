## Description: <br>
Tell dad jokes on demand by fetching a random joke from the shuttie/dadjokes HuggingFace dataset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathandeamer](https://clawhub.ai/user/jonathandeamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent for a dad joke or casual humor, and the skill fetches a random setup and punchline for the agent to present naturally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on running a small Python command and making an outbound HuggingFace request, so it may fail in environments without python3 or network access. <br>
Mitigation: Install only in environments where that execution and outbound request are acceptable, and rely on the documented fallback when the fetch fails. <br>


## Reference(s): <br>
- [Dad Jokes skill page](https://clawhub.ai/jonathandeamer/dad-jokes) <br>
- [shuttie/dadjokes dataset](https://huggingface.co/datasets/shuttie/dadjokes) <br>
- [Original Reddit Dad Jokes dataset](https://www.kaggle.com/datasets/oktayozturk010/reddit-dad-jokes) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with a short joke setup and punchline] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fall back to a joke from memory if the outbound dataset request fails.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
