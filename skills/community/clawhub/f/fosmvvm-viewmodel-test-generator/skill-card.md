## Description:

Generate ViewModel tests with codable round-trip, versioning stability, and multi-locale translation verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foscomputerservices](https://clawhub.ai/user/foscomputerservices)

### License/Terms of Use:


## Use Case:

Developers use this skill to generate Swift tests and optional YAML localization files for FOSMVVM ViewModels. It helps verify codable round-trip behavior, versioning stability, locale coverage, embedded ViewModels, and localized substitutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tests or YAML may target the wrong ViewModel, resource directory, target module, or locale set when project context is incomplete.

Mitigation: Confirm the FOSMVVM project target, resource accessor, supported locales, and generated diffs before committing.

Risk: Localization strings and substitution assertions can be syntactically valid while still using incorrect wording or expected values.

Mitigation: Review generated translations and substitution expectations with project context, then run the relevant Swift test filter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foscomputerservices/skills/fosmvvm-viewmodel-test-generator)
- [FOSUtilities project homepage](https://github.com/foscomputerservices/FOSUtilities)
- [reference.md](reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Swift and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Swift test suite patterns and YAML localization templates for use by an agent.]

## Skill Version(s):

2.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
