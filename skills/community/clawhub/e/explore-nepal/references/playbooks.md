# Scenario Playbooks

## PB-1: Recommended Route

**Trigger:** "nepal flight", "尼泊尔航班"

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
```

## PB-2: Cheapest Option

**Trigger:** "cheap", "budget", "最便宜", "省钱"

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 3
```

## PB-3: Fastest Route

**Trigger:** "fast", "quick", "最快", "省时"

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 4
```

## PB-4: Direct Flight

**Trigger:** "direct", "nonstop", "直飞", "不经停"

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --journey-type 1 --sort-type 2
```

## PB-5: Price + Date Range

**Trigger:** "flexible dates", "date range", "灵活日期"

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date-start {{start}} --dep-date-end {{end}} --sort-type 3
```

## PB-6: Broad Search (fallback)

**Trigger:** 0 results from above playbooks

```bash
flyai search-flight --origin "{{o}}" --destination "{{d}}" --dep-date {{date}} --sort-type 2
flyai keyword-search --query "{{origin}} to {{destination}} flight"
```
