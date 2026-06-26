## Description: <br>
POI 详情页问题排查编排器，自动执行查代码 sourceId、查日志、复现请求、解析返回、阅读代码和定位问题的 POI 详情页排查流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hnyyghk](https://clawhub.ai/user/hnyyghk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal developers and support engineers use this skill to investigate Gaode/Amap POI detail page issues from a gsid, traceId, POI ID, or module name. It coordinates log lookup, request replay, response-field inspection, source mapping, and a concise root-cause report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use GSIDs, trace IDs, log output, full replay URLs, and saved JSON reports that may contain sensitive production or business data. <br>
Mitigation: Use it only in an authorized internal debugging environment, redact sensitive values before sharing, and delete or secure generated files under /tmp after each investigation. <br>
Risk: Request replay can query internal gray or online services using captured URLs. <br>
Mitigation: Review the script before use and avoid online replay unless the investigation owner has explicitly approved it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hnyyghk/gaode-c3-us-shop) <br>
- [README](README.md) <br>
- [Field reference](references/fields.md) <br>
- [Source ID map](references/source_id_map.md) <br>
- [FAQ](references/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with shell command examples and JSON-derived findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local JSON reports under /tmp/poi-debug-results and response files under /tmp.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json; artifact SKILL.md lists 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
