## Description: <br>
Reviews Elixir code for idiomatic patterns, OTP basics, documentation, pattern matching, GenServer usage, and module documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Elixir .ex and .exs code for idiomatic style, pattern matching, OTP basics, documentation, and common Elixir security issues before reporting anchored findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local sibling review-verification-protocol skill for its mandatory verification gate, and that sibling skill was not included in the reviewed package. <br>
Mitigation: Confirm that the local sibling verification protocol is trusted before relying on the gate, and require each substantive finding to cite the protocol subsection satisfied or state why it is not applicable. <br>
Risk: Review guidance can produce misleading findings if claims are not anchored to the reviewed code and supporting artifacts. <br>
Mitigation: Require each finding to include a concrete locator and supporting evidence, and downgrade unverified claims to questions or uncertain notes. <br>


## Reference(s): <br>
- [Elixir Code Style](references/code-style.md) <br>
- [Pattern Matching](references/pattern-matching.md) <br>
- [OTP Basics](references/otp-basics.md) <br>
- [Documentation](references/documentation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review guidance and findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should include concrete locators and artifact-backed claims, with uncertain assertions downgraded to questions.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
