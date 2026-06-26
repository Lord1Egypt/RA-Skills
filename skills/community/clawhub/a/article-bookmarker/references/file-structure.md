# Article Bookmarker - File Structure

## Directory Layout

Bookmarks are stored as individual markdown files in the directory specified by the `$ARTICLE_BOOKMARK_DIR` environment variable:

```
$ARTICLE_BOOKMARK_DIR/
├── article-title-slug.md (individual articles)
├── TAG_INDEX.md (tag to article mapping)
└── README.md (directory overview)
```

## Bookmark File Format

Each bookmark file contains:

```markdown
# Article Title

**Source:** URL  
**Bookmarked:** YYYY-MM-DD HH:MM GMT+8  
**Tags:** tag1, tag2, tag3

## Summary

AI-generated concise summary of the article...

## Content

Full extracted article content...

## Original URL

[Link](URL)
```

## Tag Index Format

TAG_INDEX.md maintains bidirectional mapping:

```markdown
# Article Tag Index

## Tags

- **AI**: [article1](article1.md), [article2](article2.md)
- **Skills**: [skill-creation](skill-creation.md), [evaluation](evaluating-skill-output-quality.md)
- **Research**: [...]

## Articles by Tag Count

- 3 tags: [article1](article1.md)
- 2 tags: [article2](article2.md), [article3](article3.md)
- 1 tag: [...]
```
