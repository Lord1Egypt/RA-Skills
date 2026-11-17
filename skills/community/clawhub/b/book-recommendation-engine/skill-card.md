## Description:

書籍推薦引擎：支援協同過濾 / 內容相似度 / 熱門暢銷 / 標籤擴展四種演算法；內建 8 大主題書單；Open Library API 即時搜書；想讀書單追蹤含價格監控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to ask an agent for book recommendations, themed reading lists, Open Library lookups, and wishlist tracking with price checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Book queries, topics, ISBNs, and web-search terms may be sent to external book or search sites.

Mitigation: Use queries appropriate for external services and avoid entering sensitive reading interests when external lookup features are enabled.

Risk: Reading preferences, ratings, wishlist entries, and cached lookup data are stored locally under ~/.bookshelf-plus/recommendations.

Mitigation: Review and remove local data when it should not persist on the machine.

Risk: Generated booklists and wishlist exports can write to user-selected output paths.

Mitigation: Choose output paths carefully and review existing files before exporting or generating Markdown.

Risk: Open Library descriptions and web snippets may be incomplete, inaccurate, or untrusted.

Mitigation: Review generated recommendations and summaries before relying on them for purchasing, education, or business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuan905/skills/book-recommendation-engine)
- [Open Library](https://openlibrary.org)
- [Open Library Covers API](https://covers.openlibrary.org/b)
- [DuckDuckGo HTML Search](https://duckduckgo.com/html/)
- [Books.com.tw](https://www.books.com.tw)
- [TAAZE](https://www.taaze.tw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or terminal text with optional generated Markdown files and local JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local files under ~/.bookshelf-plus/recommendations and user-selected export paths.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
