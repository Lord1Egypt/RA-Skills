## Description: <br>
北京天气早安助手：获取今日北京天气并给出穿衣和饮食建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tieemo](https://clawhub.ai/user/Tieemo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users asking in Chinese for a Beijing morning briefing use this skill to get current weather, air-quality context when available, clothing suggestions, and food or drink guidance. <br>

### Deployment Geography for Use: <br>
Beijing, China <br>

## Known Risks and Mitigations: <br>
Risk: The skill may trigger on generic morning greetings when the user did not want a Beijing weather briefing. <br>
Mitigation: Use the skill when the user explicitly asks for Beijing weather, clothing, diet, or weather-based morning advice; narrow trigger wording if generic greetings should remain conversational. <br>
Risk: Weather, wind, precipitation, and air-quality data can be stale, unavailable, or inconsistent across sources. <br>
Mitigation: Prefer live weather tooling, use cautious wording such as approximate ranges, and clearly label fallback advice as not based on the day's exact weather. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tieemo/beijing-morning-weather) <br>
- [examples.md](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Chinese Markdown briefing with weather, clothing, and diet sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses current weather data when available and falls back to clearly labeled general seasonal advice when tools or network access fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
