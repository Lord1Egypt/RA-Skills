# Common Workflows

Multi-command recipes. Each command's flags are in [commands/](commands/).

### Workflow 1: Quick Cleanup Assessment

```bash
# Get overview
python3 scripts/library_analysis.py --human

# Find junk
python3 scripts/junk_finder.py --human

# Review and manually clean up in Photos.app
```

### Workflow 2: Free Up Storage

```bash
# Analyze storage
python3 scripts/storage_analyzer.py --human

# Find duplicates
python3 scripts/duplicate_finder.py --human

# Find junk with aggressive settings
python3 scripts/junk_finder.py --screenshot-age 14 --quality-threshold 0.4 --human

# Use findings to guide cleanup
```

### Workflow 3: Year-End Photo Recap

```bash
# Generate timeline for the year
python3 scripts/timeline_recap.py --start-date 2024-01-01 --end-date 2024-12-31 --narrative

# Get storage stats by year
python3 scripts/storage_analyzer.py | jq '.by_year'

# Get top people for the year
python3 scripts/library_analysis.py | jq '.top_people'

# Photo habits for the year
python3 scripts/photo_habits.py --year 2024 --human

# Best photos of the year
python3 scripts/best_photos.py --year 2024 --top 20 --human
```

### Workflow 4: Export Organized Archive

```bash
# Plan export
python3 scripts/smart_export.py --output-dir ~/Desktop/Photos-Export --favorites --start-date 2024-01-01 --plan-only

# Review the plan, then run the same command without --plan-only to export
python3 scripts/smart_export.py --output-dir ~/Desktop/Photos-Export --favorites --start-date 2024-01-01
```

### Workflow 5: Deep Cleanup

```bash
# Find all junk
python3 scripts/junk_finder.py --human

# Preview old screenshots
python3 scripts/cleanup_executor.py --category old_screenshots --human

# After the user approves: run the preview's next_command (ends in --execute --confirm <token>)

# Check album health
python3 scripts/album_auditor.py --human
```

### Workflow 6: Daily Memory Check

```bash
# See what happened on this day in past years
python3 scripts/on_this_day.py --human

# With a wider window
python3 scripts/on_this_day.py --window 2 --human
```

### Workflow 7: Location & Travel Review

```bash
# See all your locations
python3 scripts/location_mapper.py --human

# Focus on trips from a specific year
python3 scripts/location_mapper.py --year 2025 --human

# What content you shot at those places
python3 scripts/scene_search.py --human
```

### Workflow 8: People Deep Dive

```bash
# Who's in your photos
python3 scripts/people_analyzer.py --human

# Find hidden gems of specific people
python3 scripts/best_photos.py --hidden-gems --human

# Best and worst portraits per person
python3 scripts/face_quality.py --human
```

### Workflow 9: Live Photo & Storage Optimization

```bash
# Analyze Live Photos vs stills
python3 scripts/live_photo_analyzer.py --human

# Find similar photos (potential duplicates)
python3 scripts/similarity_finder.py --threshold 0.95 --human

# Check iCloud sync status
python3 scripts/icloud_status.py --human
```

### Workflow 10: Seasonal Year in Review

```bash
# Get seasonal highlights
python3 scripts/seasonal_highlights.py --year 2024 --human

# Location review with place names
python3 scripts/location_mapper.py --year 2024 --human

# Photo habits for the year
python3 scripts/photo_habits.py --year 2024 --human
```

### Workflow 11: Shared Library Audit

```bash
# Check shared library status
python3 scripts/shared_library.py --human

# See who contributed what and storage impact
python3 scripts/shared_library.py --output shared_report.json
```

---

[← SKILL.md](../SKILL.md)
