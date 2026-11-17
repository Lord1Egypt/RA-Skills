## Description:

This skill guides Ruby and Rails code generation, refactoring, and review in DHH's 37signals style, including REST-focused controllers, rich domain models, Current attributes, Hotwire patterns, and clarity-first Rails conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pixelxiao](https://clawhub.ai/user/pixelxiao)

### License/Terms of Use:


## Use Case:

External developers and engineers use this skill to shape Ruby and Rails application code toward 37signals-style conventions for controllers, models, views, architecture, dependencies, tests, and code review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an incomplete SSRF protection snippet that could lead generated Rails apps to unsafe outbound request handling.

Mitigation: Treat the snippet as conceptual guidance only and require a complete outbound request policy with proper IP classification, scheme and port allowlists, redirect validation, timeouts, response limits, and tests.

Risk: The artifact shows request metadata collection patterns for IP address, referrer, and user agent.

Mitigation: Define privacy limits and data minimization rules before collecting or storing request metadata in generated applications.

## Reference(s):

- [Architecture - DHH Rails Style](artifact/references/architecture.md)
- [Controllers - DHH Rails Style](artifact/references/controllers.md)
- [Frontend - DHH Rails Style](artifact/references/frontend.md)
- [Gems - DHH Rails Style](artifact/references/gems.md)
- [Models - DHH Rails Style](artifact/references/models.md)
- [Testing - DHH Rails Style](artifact/references/testing.md)
- [The Unofficial 37signals/DHH Rails Style Guide](https://github.com/marckohlbrugge/unofficial-37signals-coding-style-guide)
- [Marc Kohlbrugge](https://x.com/marckohlbrugge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Ruby, Rails, JavaScript, YAML, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; outputs recommendations and code examples for agent responses.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
