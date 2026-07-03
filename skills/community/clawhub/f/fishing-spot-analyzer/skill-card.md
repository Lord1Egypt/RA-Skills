## Description: <br>
智能钓鱼选点分析助手。上传钓点照片后，自动尝试提取 EXIF GPS 定位，失败则提示用户手动输入位置，结合天气、地形、鱼情输出完整钓鱼报告和装备推荐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhanchao883](https://clawhub.ai/user/wangzhanchao883) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze an uploaded fishing spot photo, location, weather, and visible terrain features before choosing whether and how to fish there. It returns a fishing spot score, likely species, gear and bait suggestions, preferred time windows, and safety reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded photos may contain precise EXIF GPS coordinates, and the skill may use those coordinates for weather lookup without clear user-facing consent. <br>
Mitigation: Review before installing if precise photo locations are sensitive; prefer city or district-level location and remove GPS EXIF data from photos when sharing private fishing spots. <br>
Risk: Weather lookup can send coordinates to an external weather API. <br>
Mitigation: Use approximate locations when exact coordinates are unnecessary, and inform users when external weather data is being requested. <br>
Risk: Fishing guidance may be inappropriate for restricted, unsafe, or locally regulated waters. <br>
Mitigation: Check local rules and visible warning signs before fishing, avoid prohibited areas, and follow the skill's water-safety and bad-weather cautions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzhanchao883/fishing-spot-analyzer) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m,precipitation&timezone=auto&forecast_days=1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with tables, scored analysis, recommendations, and safety notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request a fishing spot photo and a city, district, or location; may use EXIF GPS coordinates and Open-Meteo weather data when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
