# Assignment Handling

## List Assignments

**API:** `GET /api/v1/courses/:course_id/assignments`

**Key Parameters:**
- `include[]=submission` - Include user's submission status
- `include[]=rubric_assessment` - Include rubric details
- `bucket=future` - Only upcoming assignments
- `bucket=overdue` - Overdue assignments
- `order_by=due_at` - Sort by due date

**Script Usage:**
```python
python scripts/get_assignments.py --course 12345 --upcoming
```

## Get Assignment Details

**API:** `GET /api/v1/courses/:course_id/assignments/:id`

**Returns:**
- Assignment name and description
- Due date
- Points possible
- Submission types allowed
- Rubric criteria (for AI writing guidance)
- Attachments

**Script Usage:**
```python
python scripts/get_assignment_detail.py --course 12345 --assignment 67890
```

## For AI-Assisted Writing

Key fields for essay/assignment completion:

1. **description** - Full assignment prompt and requirements
2. **rubric** - Grading criteria (what to aim for)
3. **submission_types** - How to submit (online_upload, online_text_entry, etc.)
4. **allowed_extensions** - File type restrictions
5. **points_possible** - Target scope/depth

## Submission Status

Check if assignment is submitted:
```python
assignment.get_submission(user_id)
```

Returns:
- `workflow_state`: submitted, unsubmitted, graded
- `score`: Grade received
- `submitted_at`: Submission timestamp
- `late`: Whether submission was late
