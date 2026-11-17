# Best Practices — curated-brain

## Maintaining a Healthy Catalog

### 1. Be Specific with Facts

**Bad:** "Alice said something about the deadline."
**Good:** "Alice moved Project Alpha deadline to July 15 in email on 2026-04-20."

### 2. Always Provide Source

Every entry must have a source. "I think I heard it somewhere" is not a source.

### 3. Set Realistic Confidence

Overstating confidence erodes trust. If you're not sure, say so.

### 4. Deprecate, Don't Delete

Never delete an entry. Deprecate it with a reason. This preserves history and explains why something changed.

### 5. Audit Regularly

Run `audit` weekly to catch stale or low-confidence entries before they become problems.

### 6. Keep Backup Copies

The catalog is a JSON file. Back it up like any important document. Git works well.

## Query Tips

- Use broad topics for grouping ("Q3 Goals", "Team Preferences")
- Use search for cross-topic lookups
- Combine recent + query to see what's new in a topic

## Size Limits

There is no hard limit, but performance degrades past 10,000 entries. Consider splitting into domain-specific catalogs if you approach this.
