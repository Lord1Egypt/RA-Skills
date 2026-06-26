## Description: <br>
Checks novel chapters for consistency issues in character names, traits, timelines, locations, and relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors, editors, and developers use this skill to check novel projects before release for inconsistent names, character details, timelines, locations, and relationships. It supports local rule-based checking and an optional LLM helper for deeper consistency review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional LLM helper can send selected manuscript and character content to DashScope. <br>
Mitigation: Use the documented local checker for private manuscripts unless external processing is intended and approved; set DASHSCOPE_API_KEY only when using the LLM helper deliberately. <br>
Risk: The LLM helper has an under-documented external service dependency and requires the missing requests dependency. <br>
Mitigation: Pin dependencies and add the requests dependency before relying on the LLM helper in a repeatable workflow. <br>
Risk: Keyword-based local checks may miss nuanced timeline or narrative consistency issues. <br>
Mitigation: Treat reports as review aids and keep human editorial review in the release process. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown consistency report or JSON issue list, with CLI commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local checker reads a novel project directory; the optional LLM helper requires DASHSCOPE_API_KEY and may process selected chapter and character content.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
