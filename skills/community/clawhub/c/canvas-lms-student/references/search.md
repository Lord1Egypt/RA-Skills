# Search Techniques

## Canvas Native Search

Canvas API has limited native search. This skill implements:

1. **Local content fetching** - Download and index content
2. **Pattern matching** - Search titles, descriptions, filenames
3. **Cross-course aggregation** - Search all enrolled courses

## Search Scope

```python
python scripts/search_canvas.py --query "midterm essay requirements"
```

Searches across:
- Assignment names and descriptions
- File names
- Announcement titles and messages
- Page titles (if available)

## Advanced Search

```python
# Search specific course only
python scripts/search_canvas.py --query "final project" --course 12345

# Search files only
python scripts/search_canvas.py --query "syllabus" --type file

# Search assignments only
python scripts/search_canvas.py --query "group project" --type assignment

# Case-sensitive search
python scripts/search_canvas.py --query "Python" --case-sensitive

# Output full content (not just titles)
python scripts/search_canvas.py --query "requirements" --full-content
```

## Use Cases for AI Writing

### Find Assignment Requirements
```python
python scripts/search_canvas.py --query "essay 2 requirements" --full-content
```

### Find Related Materials
```python
python scripts/search_canvas.py --query "citation guidelines" --type file
```

### Check Previous Announcements
```python
python scripts/search_canvas.py --query "deadline extension" --type announcement
```

## Output Format

```json
[
  {
    "course": "English Composition",
    "course_id": 12345,
    "type": "assignment",
    "title": "Essay 2: Argumentative Essay",
    "url": "https://...",
    "match_context": "...essay requirements include..."
  }
]
```

## Limitations

- Cannot search inside file contents (PDFs, Word docs)
- Cannot search discussion posts (requires additional permissions)
- Searches cached/downloaded content only
