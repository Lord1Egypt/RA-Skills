## Description: <br>
Calculator Chat converts short user messages into numeric calculator expressions and displays them in the local system calculator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShenyfZero9211](https://clawhub.ai/user/ShenyfZero9211) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use Calculator Chat to turn brief emotional or conversational messages into calculator-number responses, usually through /calc-chat or the calc-chat CLI. The skill is intended for local calculator display rather than factual computation or decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch and control local calculator applications and may close an existing gnome-calculator process. <br>
Mitigation: Use explicit /calc-chat or calc-chat invocation and avoid running it in sensitive desktop sessions. <br>
Risk: Windows and macOS modules use desktop automation mechanisms that can send input to local applications. <br>
Mitigation: Review or remove the Windows and macOS automation modules before using the skill on those platforms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ShenyfZero9211/calculator-chat) <br>
- [Skill definition](SKILL.md) <br>
- [Calculator Chat Skill Design](docs/plans/2026-03-08-calculator-chat-skill-design.md) <br>
- [Package manifest](package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text plus local calculator display] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch, focus, automate, or close a local calculator application depending on platform support.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
