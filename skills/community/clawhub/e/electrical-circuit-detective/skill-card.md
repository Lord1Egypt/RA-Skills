## Description:

Use when a breaker keeps tripping, an outlet went dead, or you wonder if a circuit can take one more appliance. Computes real circuit load with the 80% continuous rule, routes dead outlets (GFCI cascade, backstab failure), separates overload vs short vs ground-fault trip patterns, and names the exact point to call an electrician.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Homeowners and renters use this skill to estimate household circuit loads, triage common breaker trips and dead outlets, and decide when to stop troubleshooting and contact a qualified electrician.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Load calculations and appliance matches are preliminary estimates and may not reflect actual appliance input watts.

Mitigation: Verify appliance input watts and matched names before relying on a calculation.

Risk: Optional circuit mapping stores household details in plaintext at ~/.circuit_map.json, and reusing a label replaces its entry.

Mitigation: Avoid sensitive notes and remember that reusing a label replaces its saved entry.

Risk: Electrical wiring repairs can be hazardous.

Mitigation: Have a qualified electrician handle wiring repairs.

## Reference(s):

- [Circuit Guide](artifact/references/circuit-guide.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/electrical-circuit-detective)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Configuration]

**Output Format:** [Plain text and Markdown guidance, command-line output, and a JSON circuit map]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preliminary load estimates and interactive troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
