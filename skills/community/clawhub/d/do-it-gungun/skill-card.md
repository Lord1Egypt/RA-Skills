## Description: <br>
帮助地球人做人生选择的 AI 判断技能 - 你只管 do it，判断交给滚滚 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alsoforever](https://clawhub.ai/user/alsoforever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to structure difficult life decisions such as career moves, relationships, investments, and housing choices. The agent returns a recommendation with reasoning, an execution plan, risk notes, and supportive follow-up language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may enter sensitive financial, relationship, employment, or family details while seeking a decision recommendation. <br>
Mitigation: Use anonymized or minimal details, review where the web/API version sends and stores data, and avoid submitting highly sensitive personal information. <br>
Risk: The web demo stores decision history in browser local storage and the API logs submitted problem titles. <br>
Mitigation: Clear browser history storage after use, avoid real names or identifying facts, and review local server logs before sharing the environment. <br>
Risk: Recommendations can appear decisive even though the bundled datasets and heuristics are not verified live professional advice. <br>
Mitigation: Treat results as informal brainstorming, validate important facts independently, and consult qualified professionals for legal, medical, financial, or high-impact personal decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alsoforever/do-it-gungun) <br>
- [Gungun Family 2.0 multi-agent workflow](GUNGUN-FAMILY-2.0.md) <br>
- [Usage Guide](USAGE-GUIDE.md) <br>
- [Database schema](references/database-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, analysis, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with optional JSON or HTML from the local API/web demo] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informal decision-support recommendations and may include action plans, risk warnings, and follow-up prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
