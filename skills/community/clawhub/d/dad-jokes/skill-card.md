## Description:

Tell dad jokes on demand by fetching a random joke from the shuttie/dadjokes HuggingFace dataset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathandeamer](https://clawhub.ai/user/jonathandeamer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer casual requests for a dad joke or light humor by fetching and formatting one joke.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes an external network request to HuggingFace when responding to humor requests.

Mitigation: Run it only in environments where outbound access to the public HuggingFace dataset endpoint is allowed, and use the documented fallback when the request fails.

## Reference(s):

- [Dad Jokes dataset by Roman Grebennikov](https://huggingface.co/datasets/shuttie/dadjokes)
- [Original Reddit Dad Jokes dataset by Oktay Ozturk](https://www.kaggle.com/datasets/oktayozturk010/reddit-dad-jokes)
- [ClawHub skill page](https://clawhub.ai/jonathandeamer/skills/dad-jokes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown text with a setup and punchline, backed by an inline Python shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches one public dataset row when network access succeeds; falls back to a joke from memory on fetch failure.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
