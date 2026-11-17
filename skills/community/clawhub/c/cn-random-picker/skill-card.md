## Description:

Cn Random Picker helps an agent randomly select one or more entries from comma- or newline-separated input using a small bundled Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Users can ask an agent to perform a simple lottery, drawing, or random-pick task from a supplied list. The agent can run the bundled Python script and return the selected item or items as JSON-backed text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes a --count flag, weighted selection, and cryptographic randomness that the script does not implement.

Mitigation: Use the positional count argument supported by scripts/random_picker.py, treat selections as non-cryptographic, and test behavior before using it for prize, compliance-sensitive, or fairness-sensitive decisions.

Risk: The documentation is Chinese-only and includes unrelated promotional AISoBrand links.

Mitigation: Review localized instructions before deployment and treat external AISoBrand links as optional promotional material, not required setup or runtime dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-random-picker)

## Skill Output:

**Output Type(s):** [text, shell commands, code]

**Output Format:** [Markdown guidance with inline shell commands and JSON output from the picker script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script uses the Python standard library and returns a JSON object containing picked values and whether all values were returned.]

## Skill Version(s):

1.2.6 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
