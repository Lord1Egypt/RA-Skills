# Course Operations

## List Courses

**API:** `GET /api/v1/courses`

**Key Parameters:**
- `enrollment_state=active` - Only currently enrolled courses
- `include[]=total_scores` - Include current grades
- `per_page=100` - Max items per page

**Script Usage:**
```python
python scripts/list_courses.py --active-only
```

**Returns:**
- Course ID
- Course name
- Course code
- Current grade (if available)
- Enrollment state

## Get Course Details

**API:** `GET /api/v1/courses/:id`

**Script Usage:**
```python
python scripts/get_course_detail.py --course 12345
```

**Returns:**
- Full course information
- Syllabus body (if available)
- Term dates
- Course settings

## Filter by Enrollment Type

Courses can be filtered by:
- `student` - Courses where user is a student
- `teacher` - Courses where user is a teacher (TAs)
- `ta` - TA enrollments
- `observer` - Observer enrollments

## Common Use Cases

1. **Get current semester courses**: Use `--active-only` flag
2. **Check grades**: Use `--with-grades` to include current scores
3. **Find course ID**: Run `list_courses.py` to get IDs for other scripts
