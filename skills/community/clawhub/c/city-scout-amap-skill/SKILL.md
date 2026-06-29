---
name: city-scout
description: "城市踏勘官 CityScout：把城市片区、任务目标和时间预算转成可执行的踏勘路线、观察清单、风险点和汇报摘要。适用于城市更新、商业选址、文旅动线、街区活力评估等需要地图能力和现场判断结合的任务。"
---

# 城市踏勘官 CityScout

## When To Use

Use this skill when the user needs to plan a site visit, urban survey, commercial location scouting, citywalk research route, district renewal walkthrough, tourism route audit, or place-based field investigation.

Typical Chinese triggers:

- 城市踏勘
- 现场调研
- 城市更新
- 商业选址
- 文旅动线
- 街区活力
- 片区走访
- 帮我规划调研路线
- 帮我看这个地块周边

## Goal

Turn a vague location-based task into a practical fieldwork package:

- a route with ordered stops
- the reason each stop matters
- what to observe at each stop
- key POI and facility evidence
- risk and opportunity notes
- photo checklist
- short reporting summary

## Required Inputs

Ask only for missing essentials:

- city or district
- target area or anchor location
- task type
- time budget
- travel mode

If the user does not specify a task type, choose the closest one:

- urban renewal survey
- commercial site selection
- cultural tourism route planning
- night safety route audit
- community service facility scan

## Amap Capabilities To Use

Use Amap Open Platform capabilities where available:

- Geocoding API: convert the target area or anchor place into coordinates.
- Place Search / Around Search: find POIs around the target area.
- Walking / Driving / Transit Direction API: order stops into a feasible route.
- District / Administrative Boundary API: identify the district context.
- Weather API: add fieldwork weather reminders when relevant.
- Static map or JSAPI map: visualize route and stops if a demo surface is available.

If API access is unavailable, produce a transparent mock route and label it as a demo plan that should be verified with Amap data before submission or fieldwork.

## Workflow

1. Clarify the fieldwork task.
2. Define the survey radius and time budget.
3. Identify anchor points:
   - transit access
   - parking
   - major commercial nodes
   - public service facilities
   - parks, schools, hospitals, cultural landmarks
   - safety and management nodes such as police stations, convenience stores, lit streets
4. Select 5-8 stops that represent different spatial questions.
5. Arrange a route that fits the user's time budget and travel mode.
6. Produce an observation checklist for each stop.
7. Summarize:
   - opportunities
   - risks
   - missing evidence
   - next actions
8. End with a paste-ready reporting paragraph.

## Output Format

Use this structure:

```markdown
# 城市踏勘路线

## 任务判断

## 高德能力调用说明

## 推荐路线

| 顺序 | 点位 | 为什么去 | 现场观察 | 拍照建议 |
|---:|---|---|---|---|

## 风险与机会

## 现场执行清单

## 3 句汇报摘要

## 待核实数据
```

## Quality Rules

- Do not produce generic tourist recommendations.
- Every stop must serve a fieldwork question.
- Every conclusion must distinguish evidence, inference, and uncertainty.
- Prefer a route that can actually be walked or driven within the time budget.
- Include at least one route-level tradeoff, such as coverage versus depth.
- Keep the final answer practical enough for someone to leave for the site immediately.

## Example Prompt

帮我为“福州烟台山历史风貌区城市更新踏勘”规划一条 90 分钟步行路线。重点看商业活力、历史建筑利用、慢行体验、公共服务和夜间安全，输出点位、观察清单、拍照建议和 3 句汇报摘要。

## Example Output Summary

城市踏勘官会先定位烟台山片区，再围绕入口交通、核心街巷、商业节点、历史建筑、公园界面、社区服务和安全节点组织 6-8 个点位，形成一条 90 分钟步行路线。输出不只是路线，还包括每个点位该看什么、拍什么、怎么判断机会和风险，以及可以直接放进会议材料的简短汇报。
