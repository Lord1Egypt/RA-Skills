## Description: <br>
A comprehensive Chinese metaphysics skill that routes questions across Xiao Liu Ren, Liu Yao Na Jia, Mei Hua Yi Shu, and Da Liu Ren, then uses reference material and Python scripts to produce time-calibrated divination results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprint-yy](https://clawhub.ai/user/sprint-yy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to select and run one of four traditional Chinese divination methods, generate structured oracle outputs and readings, and include timing, method rationale, and disclaimers. It is intended for cultural, educational, and entertainment contexts rather than medical, legal, financial, or other major decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unknown city names may be sent to Open-Meteo and cached locally. <br>
Mitigation: Use an explicit longitude or a known built-in city for maximum privacy, and inspect or delete scripts/_geo_cache.json if local coordinate caching is a concern. <br>
Risk: Divination outputs can be mistaken for advice on major decisions. <br>
Mitigation: Treat outputs as cultural, educational, or entertainment reference only, include the skill's disclaimers, and do not rely on results for medical, legal, financial, or other major decisions. <br>
Risk: Broad trigger words may activate a divination workflow unexpectedly. <br>
Mitigation: Confirm that the user wants a divination flow and confirm the method before running calculation scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sprint-yy/comprehensive-divination-skill) <br>
- [README](README.md) <br>
- [Comprehensive divination skill pitfalls](references/comprehensive-divination-skill-pitfalls.md) <br>
- [Router matching matrix](references/router/matching-matrix.md) <br>
- [Xiao Liu Ren method](references/xiao-liuren/method.md) <br>
- [Liu Yao method](references/liuyao/method.md) <br>
- [Mei Hua Yi Shu method](references/meihua-yishu/method.md) <br>
- [Da Liu Ren method](references/da-liuren/method.md) <br>
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [agentskills.io standard](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown narrative with JSON blocks, inline shell commands, and optional Python script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local Python scripts for deterministic calculations; unknown city lookup may query Open-Meteo and cache resolved coordinates locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
