# File Downloads

## List Course Files

**API:** `GET /api/v1/courses/:course_id/files`

**Key Parameters:**
- `include[]=content_locks` - Check if files are locked
- `sort=updated_at` - Sort by last modified
- `content_types[]=application/pdf` - Filter by type

## Download Files

**Process:**
1. List files with `course.get_files()`
2. Get download URL with `file.url`
3. Download to local directory

**Script Usage:**
```python
# Download all files
python scripts/download_files.py --course 12345 --output ./materials

# Download specific folder
python scripts/download_files.py --course 12345 --folder "Lecture Notes" --output ./lectures

# Download by file type
python scripts/download_files.py --course 12345 --type pdf --output ./pdfs
```

## File Structure

Downloaded files organized as:
```
./materials/
├── Week 1/
│   ├── syllabus.pdf
│   └── lecture1_slides.pdf
├── Week 2/
│   └── reading_materials.pdf
└── Assignments/
    └── essay_template.docx
```

## Folders

**API:** `GET /api/v1/courses/:course_id/folders`

Get folder structure to preserve organization when downloading.

## Common File Types

| Type | Extension | Usage |
|------|-----------|-------|
| PDF | .pdf | Syllabus, readings, handouts |
| Word | .docx | Templates, assignment sheets |
| PowerPoint | .pptx | Lecture slides |
| Images | .png, .jpg | Diagrams, figures |
| Archives | .zip | Bulk resources |
