## Description: <br>
Acts as a used-car buying advisor that helps users clarify buying needs, search multiple Chinese used-car platforms, compare listings, and estimate loan payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trancedream](https://clawhub.ai/user/trancedream) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research used-car options, compare live listings across supported Chinese marketplaces, produce purchase recommendations, and calculate financing scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries third-party car-listing sites using browser-like scraping behavior. <br>
Mitigation: Use modest request volume, respect platform restrictions, and stop or adjust searches when a platform blocks or rate-limits access. <br>
Risk: Recent search results may be retained locally in ~/.config/car-cli/last_search.json. <br>
Mitigation: Delete the local cache file when recent searches should not remain on the machine. <br>
Risk: Debug or trace logs can expose request URLs and marketplace response details in shared environments. <br>
Mitigation: Avoid enabling debug or HTTP trace logging when logs may be shared or retained. <br>


## Reference(s): <br>
- [car-cli usage guide](scripts/README.md) <br>
- [car-cli platform adapter reference](references/adapters.md) <br>
- [ClawHub skill page](https://clawhub.ai/trancedream/car-search) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [Dongchedi used-car listings](https://www.dongchedi.com) <br>
- [Che168 used-car listings](https://www.che168.com) <br>
- [Guazi used-car listings](https://www.guazi.com) <br>
- [Youxinpai used-car listings](https://www.youxinpai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional JSON, YAML, CSV, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include vehicle listing links, comparison tables, financing estimates, and exported search data.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
