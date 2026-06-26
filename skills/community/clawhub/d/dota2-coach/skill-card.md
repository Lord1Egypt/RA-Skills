## Description: <br>
Dota 2 出装与打法攻略 helps agents answer Chinese Dota 2 hero, item build, win-rate, lane, skill, talent, and gameplay questions using local game data with optional manual refresh scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangjian1412](https://clawhub.ai/user/yangjian1412) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and Dota 2 content builders use this skill to generate Chinese hero guidance, including win-rate context, common and recommended item builds, lane notes, skill and talent details, and practical gameplay advice. Agents normally answer from bundled local JSON data and only refresh public game data when explicitly asked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Dota-related trigger words may activate the skill during general Dota conversations. <br>
Mitigation: Use it when the user wants Dota 2 coaching, builds, matchups, or data-backed game guidance; otherwise ask a clarifying question before applying the skill. <br>
Risk: Optional update scripts make outbound requests and rewrite bundled JSON data files. <br>
Mitigation: Run update scripts only when intentionally refreshing local game data, then review the resulting data changes before publishing or relying on them. <br>
Risk: Dota 2 balance patches can make stored build and gameplay guidance stale. <br>
Mitigation: Check the skill version and update notes against the current Dota 2 patch before relying on recommendations for recent gameplay. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangjian1412/dota2-coach) <br>
- [OpenDota heroStats API](https://api.opendota.com/api/heroStats) <br>
- [OpenDota item popularity API](https://api.opendota.com/api/heroes/{hero_id}/itemPopularity) <br>
- [dotabase ability data](https://raw.githubusercontent.com/mdiller/dotabase/master/json/abilities.json) <br>
- [dotabase talent data](https://raw.githubusercontent.com/mdiller/dotabase/master/json/talents.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese-language Markdown with tables and optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled local Dota 2 JSON data by default; optional refresh scripts can update that data from public sources.] <br>

## Skill Version(s): <br>
1.1.8 (source: evidence.release.version; changelog notes Dota 2 7.41d item, neutral item, hero, and bug-fix data updates) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
