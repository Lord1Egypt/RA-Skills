# Lifecycle Automation

## Principle
Archive first, then consider cleanup later. Do not auto-delete by default.

## Lifecycle stages
1. **daily-active**
   - raw / synthesized / boss remain in primary daily-review tree
2. **archive-ready**
   - weekly + monthly summaries exist
   - retention window exceeded
   - archive candidate listed by planner
3. **archived**
   - daily-layer files copied into archive tree
   - index marks the related daily records as archived
4. **cleanup-candidate**
   - archive has been retained long enough
   - user/system policy explicitly allows deletion
5. **deleted**
   - only after a stricter policy gate; not default

## Recommended automation chain
- Daily 03:00: generate raw + synthesized + index
- Daily 03:20: push boss summary
- Weekly Sunday 03:40: generate weekly summary and update index
- Monthly day 1 03:50: generate monthly summary and update index
- Monthly day 2 04:00: run retention planner + readiness check + archive eligible daily layer

## Safety rule
Deletion should remain a separate, stricter step and should not be enabled by default in the public skill.
