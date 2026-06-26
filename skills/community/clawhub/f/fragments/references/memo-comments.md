# Memo Comments

## Overview

Memos support threaded comments for discussion and collaboration.
Comments inherit the visibility of their parent memo.

**Key points:**
- Comments are attached to a specific memo
- Comment visibility follows parent memo (PRIVATE/PROTECTED/PUBLIC)
- Deleting a memo also deletes all its comments

## MCP Tools

| Operation | Tool | Description |
|-----------|------|-------------|
| List comments | `memos_list_memo_comments` | Retrieve all comments on a memo |
| Add comment | `memos_create_memo_comment` | Create a new comment |

## List Comments Workflow

### Trigger

User wants to see discussion on a memo.
Keywords: "show comments", "list comments", "评论", "查看评论".

### Steps

1. **Locate the memo:**
   - If memo name provided: proceed directly
   - If content described: `memos_search_memos(query=...)`

2. **Retrieve comments:**
   ```python
   memos_list_memo_comments(
       name="memos/{uid}",
       page_size=20,      # optional, default is reasonable
       page_token=...,    # optional, for pagination
       order_by="display_time desc"  # optional
   )
   ```

3. **Present results:**
   - Show comment count
   - List each comment with:
     - Author (creator field)
     - Timestamp (displayTime)
     - Content snippet

4. **Pagination:**
   - If `nextPageToken` exists, offer to load more
   - Keep `page_size` small (10-20) for token efficiency

### Example Output

```
📋 Comments on memos/abc123 "API Design Guidelines" (3 total)

1. @users/456 · 2024-01-15 10:30
   "Great point about REST conventions. Should we add GraphQL examples?"

2. @users/789 · 2024-01-15 14:22
   "I can add the GraphQL section next week."

3. @users/456 · 2024-01-16 09:05
   "Thanks! Looking forward to it."
```

## Add Comment Workflow

### Trigger

User wants to add a comment to a memo.
Keywords: "add comment", "comment on", "回复", "添加评论".

### Steps

1. **Locate the target memo:**
   - Same as list comments workflow

2. **Gather comment content:**
   - User provides the comment text
   - Markdown is supported

3. **User confirmation:**
   - Show memo title and comment content
   - Ask for explicit approval

4. **Execute:**
   ```python
   memos_create_memo_comment(
       name="memos/{uid}",
       content="Comment text in markdown..."
   )
   ```

5. **Report result:**
   - Confirm comment was added
   - Optionally show updated comment count

### Example

```
User: "Add a comment to my API design memo saying I'll review the auth section"

1. Search: memos_search_memos(query="API design")
2. Found: memos/abc123 "API Design Guidelines"
3. Confirm: "Add comment to memos/abc123:
   'I'll review the auth section'
   Proceed?"
4. User confirms
5. Call memos_create_memo_comment(...)
6. Confirm: "Comment added to memos/abc123"
```

## Use Cases

### 1. Collaborative Discussion

Multiple users can discuss a memo's content through comments:
- Clarify points
- Ask questions
- Provide updates
- Share related resources

### 2. Progress Tracking

Comments can record progress on tasks documented in memos:
- "Status update: 50% complete"
- "Blocked: waiting for API key"
- "Resolved: issue fixed in commit abc123"

### 3. Context Preservation

Comments preserve context that might not fit in the memo itself:
- Links to related resources
- Historical decisions
- Meeting notes
- Review feedback

## Safety Notes

- Comments require the parent memo to exist
- Comment creation requires authentication (PAT token)
- Comments are deleted when their parent memo is deleted
- There is no "update comment" API — edit by deleting and recreating (if supported by Memos server)

## Token Efficiency

When listing comments:
- Use `page_size` to limit results
- Show truncated snippets first, expand on request
- Avoid loading all comments for very active discussions unless needed
