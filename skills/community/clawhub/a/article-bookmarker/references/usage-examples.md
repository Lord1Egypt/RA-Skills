# Article Bookmarker - Usage Examples

## Adding Articles

### From URL

**User Input:** "帮我收藏这个文章 https://example.com/ai-research"

**Workflow:**
1. Use `web_fetch` to extract article content
2. Generate summary using current model
3. Auto-tag based on content (e.g., AI, Research, Machine Learning)
4. Create bookmark file with format:
   - Title, Source URL, Timestamp, Tags
   - AI-generated summary
   - Full extracted content
   - Original URL link
5. Save to `$ARTICLE_BOOKMARK_DIR`
6. Update TAG_INDEX.md with new entry

**Example Output:** Creates `ai-research-2024.md` with proper tagging and summary.

### From Text Content

**User Input:** "收藏这段文章内容：[粘贴的长文本内容]"

**Workflow:** Same as URL but skip web_fetch step, use provided text directly.

## Deleting Articles

### By Filename

**User Input:** "删除我收藏的 ai-research-2024.md 这篇文章"

**Confirmation Display:**
```
找到文章：ai-research-2024.md
标题：AI Research Breakthrough in 2024
路径：$ARTICLE_BOOKMARK_DIR/ai-research-2024.md
标签：AI, Research, Machine Learning
摘要：Recent advances in artificial intelligence have shown...

确认删除此文章？(yes/no)
```

### By Search Query

**User Input:** "删除我之前收藏的关于技能评估的文章"

**Search Results:**
```
找到 1 篇匹配文章：
1. evaluating-skill-output-quality.md
   标题：Evaluating skill output quality
   预览：How to test whether your skill produces good outputs using eval-driven iteration...

确认删除第 1 篇？(yes/no)
```

## Auto-Tagging Examples

### Content Analysis Patterns

**AI/Tech Articles** → Tags: `AI`, `Machine Learning`, `Research`
- Keywords: "GPT", "LLM", "neural network", "transformer"

**Programming Tutorials** → Tags: `Programming`, `Tutorial`, `Python`
- Keywords: "code example", "function", "library", "API"

**Productivity Tools** → Tags: `Productivity`, `Workflow`, `Automation`
- Keywords: "efficiency", "organize", "streamline", "process"

**OpenClaw Specific** → Tags: `OpenClaw`, `Agent`, `Skills`
- Keywords: "OpenClaw", "agent", "skill", "workflow"

## Tag Index Management

### Index Structure

TAG_INDEX.md maintains:
- **Tags section**: Tag → [article list] mapping
- **Articles by Tag Count**: Shows articles grouped by how many tags they have

### Update Triggers

Tag index updates on:
- New article addition (add to relevant tags)
- Article deletion (remove from all tags)
- Manual tag modification (if implemented)

## Error Handling

### Common Scenarios

**Duplicate Files:** Append `-1`, `-2` suffix to filename
**Network Failures:** Retry web_fetch, report error to user
**Invalid URLs:** Validate before fetching, ask for correction
**Empty Content:** Warn user, don't create bookmark
**Deletion Confirmation:** Always show path and key details before confirming

## Best Practices

1. **Descriptive Filenames**: Use sanitized titles, not random hashes
2. **Meaningful Tags**: Balance specificity vs generality
3. **Regular Index Reviews**: Clean up unused tags periodically
4. **Backup Important Articles**: Critical bookmarks might need external backup
5. **Confirm Destructive Actions**: Always double-check deletions
