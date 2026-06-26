## Description: <br>
Turn papers, podcasts, and case studies into publish-ready social posts, infographics, and diagrams, with topic discovery through Exa and image generation through fal.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thierrypdamiba](https://clawhub.ai/user/thierrypdamiba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and developer advocates use this skill to transform source URLs and long-form material into platform-ready posts, captions, diagrams, infographics, and local content artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches web sources and uses Playwright stealth scraping, which can conflict with site terms or expectations. <br>
Mitigation: Use it only on sources you are permitted to process, review applicable site rules, and run it in a sandboxed environment for sensitive workflows. <br>
Risk: The skill sends image prompts to fal.ai and topic-search queries to Exa. <br>
Mitigation: Use scoped, usage-limited API keys and avoid including sensitive or internal material in prompts, source URLs, or brand keywords. <br>
Risk: The Reddit drafting agent is designed to imitate ordinary human participation and could enable undisclosed promotion or fake anecdotes. <br>
Mitigation: Use Reddit outputs only as transparent drafts, remove invented personal claims, disclose promotional context where required, and review platform rules before posting. <br>
Risk: The skill stores generated artifacts locally. <br>
Mitigation: Review generated files before sharing and clean local content directories when outputs include sensitive source material. <br>


## Reference(s): <br>
- [Content Claw ClawHub page](https://clawhub.ai/thierrypdamiba/content-claw) <br>
- [Publisher profile](https://clawhub.ai/user/thierrypdamiba) <br>
- [Clawdis homepage](https://github.com/scaleintelligence/content-claw) <br>
- [Running Recipes](references/run-recipe.md) <br>
- [Create Recipe Wizard](references/create-recipe.md) <br>
- [Topic Discovery](references/topics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON specs, YAML recipes, local files, and image-generation artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local content directories and generated image files; may include hosted image URLs returned by fal.ai.] <br>

## Skill Version(s): <br>
3.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
