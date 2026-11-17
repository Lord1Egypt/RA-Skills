# Duplicate Finder — `duplicate_finder.py`

Find duplicate photos and recommend which to keep based on quality, favorite status, and file size.

```bash
python3 scripts/duplicate_finder.py [--human] [--output FILE]
```

**Detection Methods:**
1. **Apple's built-in** — Uses `ZDUPLICATEASSETVISIBILITYSTATE`
2. **Timestamp + dimensions** — Photos taken at same second with same dimensions

**Recommendation Logic:**
- Favorites get priority
- Screenshots get penalty
- Highest quality score preferred
- Largest file size as tiebreaker

**Example Output:**
```
👥 DUPLICATE FINDER RESULTS
==================================================

Found 12 duplicate groups
Total duplicates: 27
Can safely delete: 15
Total size: 156 MB
Potential savings: 89 MB

Sample groups (showing first 5):

Group 1 (apple_builtin):
  ✓ KEEP ★ IMG_1234.jpg (4.2 MB, Q:0.823)
    DELETE   IMG_1234-2.jpg (4.1 MB, Q:0.801)

Group 2 (timestamp_dimensions):
  ✓ KEEP   IMG_5678.heic (2.8 MB, Q:0.756)
    DELETE   IMG_5678-edited.jpg (3.1 MB, Q:0.654)
```

**Usage in Conversation:**

**User:** "Do I have duplicate photos?"  
**AI:** *Runs duplicate_finder.py, reports findings*

**User:** "Find duplicates and tell me which to delete"  
**AI:** *Runs duplicate_finder.py, explains recommendations*

---

[← All commands](../../SKILL.md#commands)
