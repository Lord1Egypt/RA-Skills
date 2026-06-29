# amap-family-halfday-planner

ClawHub / OpenClaw Skill package for the Amap contest project "亲子半日游规划师".

This folder is the uploadable Skill package. It intentionally contains only text files because ClawHub publishing accepts `SKILL.md` plus text supporting files.

## Local Test

```bash
export AMAP_API_KEY=your_amap_webservice_key
node scripts/family-halfday-plan.mjs --origin "杭州西湖文化广场" --city "杭州市" --age "4-6岁"
```

Windows PowerShell:

```powershell
$env:AMAP_API_KEY="your_amap_webservice_key"
node scripts/family-halfday-plan.mjs --origin "杭州西湖文化广场" --city "杭州市" --age "4-6岁"
```

## Publish Fields

- Slug: `amap-family-halfday-planner`
- Display name: `亲子半日游规划师`
- Version: `1.0.0`
- Tags: `latest`, `amap`, `family-travel`, `route-planning`
- Changelog: `Initial release: generates child-friendly half-day route stories using Amap geocoding, nearby POI search, and walking route estimation.`
