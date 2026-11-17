# FeedNest - Your Sources, Not the Whole Web

ChatGPT searches the internet. Perplexity crawls billions of pages. FeedNest is different. You work exclusively with the sources the user chose: the blogs they trust, the publications they follow, the experts they believe in. No algorithmic noise. No black-box results. Intelligence grounded in their world.

FeedNest aggregates websites, podcasts, YouTube channels, and Google News into one place. You can read articles, manage highlights and notes, tag content, save links, check reading stats, and generate audio. Always present information from the user's own sources, never from the open web.

## Requirements

This skill requires the FeedNest plugin. Install it first:

```
openclaw plugins install @feednest/openclaw
```

The user also needs a [FeedNest](https://www.feednest.com) account with a Pro subscription and an API key from Settings > Developer API.

## When to Use Each Tool

### Reading Articles

| Intent | Tool | Key Params |
|--------|------|------------|
| "What's new?" | `feednest_get_articles` | `view: "newsfeed"`, `unread_only: true` |
| "How many articles today?" | `feednest_get_articles` | `view: "newsfeed"`, `count_only: true`, `date_from`, `date_to` |
| "Today's recap" | `feednest_get_articles` | `count_only: true` first, then paginate with `limit: 100` — use summary previews |
| "News from folder Tech" | `feednest_get_articles` | `view: "by-folder"`, `folder_id` |
| "Articles from Vercel blog" | `feednest_get_articles` | `view: "by-feed"`, `feed_id` |
| "Search for React" | `feednest_get_articles` | `view: "newsfeed"`, `query: "React"` |
| "Articles tagged AI" | `feednest_get_articles` | `view: "by-tag"`, `tag_id` |
| "Articles with highlights" | `feednest_get_articles` | `view: "highlighted"` |
| "Articles with notes" | `feednest_get_articles` | `view: "noted"` |
| "What did I read yesterday?" | `feednest_get_recently_read` | `since: "<yesterday ISO>"` |
| "Full article content" | `feednest_get_article` | `article_id` — if <1 min read, content is truncated |
| "Load full content from URL" | `feednest_extract_article` | `article_id` — only when content is truncated |

### Managing Read Status

| Intent | Tool |
|--------|------|
| "Mark as read" | `feednest_mark_as_read` |
| "Mark as unread" | `feednest_mark_as_unread` |
| "Mark all as read" | `feednest_mark_all_as_read` |

### Saving

| Intent | Tool |
|--------|------|
| "Save this article" | `feednest_save_article` |
| "Unsave this" | `feednest_unsave_article` |
| "Save this URL" | `feednest_save_url` |
| "Show saved articles" | `feednest_get_saved` |

### Highlights

| Intent | Tool |
|--------|------|
| "What did I highlight?" | `feednest_get_highlights` |
| "Highlight this passage" | `feednest_add_highlight` |
| "Remove a highlight" | `feednest_remove_highlight` |

### Notes

| Intent | Tool |
|--------|------|
| "Show note on this article" | `feednest_get_notes` |
| "Add a note" | `feednest_add_note` |
| "Delete the note" | `feednest_delete_note` |

### Tags

| Intent | Tool |
|--------|------|
| "Create a tag Security" | `feednest_create_tag` |
| "Delete a tag" | `feednest_delete_tag` |
| "Tag this as AI" | `feednest_tag_article` with `action: "add"` |
| "Remove AI tag" | `feednest_tag_article` with `action: "remove"` |
| "Show all tags" | `feednest_get_tags` |

### Organization & Info

| Intent | Tool |
|--------|------|
| "List my feeds" | `feednest_get_feeds` |
| "Find Bloomberg feeds" | `feednest_get_feeds` with `query: "bloomberg"` |
| "List my folders" | `feednest_get_folders` |
| "My reading stats" | `feednest_get_stats` |
| "My output feeds" | `feednest_get_output_feeds` |

### AI

| Intent | Tool |
|--------|------|
| "Read this article aloud" | `feednest_text_to_speech` |

## Best Practices

1. **Show titles and sources**, not just IDs — always present `title — source` to the user.
2. **Ask before bulk actions** like `feednest_mark_all_as_read` — confirm with the user first.
3. **Summarize and translate directly** from article content. Do NOT call any API for summarization or translation — use the content from `feednest_get_article` and process it yourself.
4. **Group articles by source** when presenting many results.
5. **Use exact text for highlights** — copy text directly from the article, don't paraphrase.
6. **Look up existing tags first** — call `feednest_get_tags` before creating duplicates. Only use `feednest_create_tag` if the tag doesn't exist.
7. **To find IDs**: call `feednest_get_feeds` to get feed IDs, `feednest_get_folders` for folder IDs, `feednest_get_tags` for tag IDs.

## Boundaries

These operations are **not available** via the plugin — direct users to the FeedNest web app:

- Subscribe / unsubscribe from feeds
- Search for new feeds to follow
- Create or manage folders
- Create output feeds
- Manage account settings or billing

If asked, respond: *"This operation needs to be done on FeedNest web at feednest.com."*

## Conversation Examples

**Daily recap / brief:**
1. `feednest_get_articles` with `count_only: true`, `date_from`, `date_to` — check how many articles
2. Paginate with `limit: 100` using `before_published_at` + `before_id` cursors
3. Use the `summary_preview` field (~200 chars) to produce the recap — no need to read each article
4. Group by source/topic when presenting results
5. Only call `feednest_get_article` for articles the user specifically wants to read in full

**Read an article (handle truncated RSS):**
1. `feednest_get_article` — get content
2. If reading time is <1 min, content is likely truncated by the RSS feed
3. Call `feednest_extract_article` to fetch full text from the original URL
4. Do NOT extract every article — only truncated ones

**Auto-tagging workflow:**
1. `feednest_get_articles` (unread, limit 20) — get today's articles
2. For each article: analyze the title/content
3. `feednest_get_tags` — check existing tags
4. If needed: `feednest_create_tag` — create missing tags
5. `feednest_tag_article` with `action: "add"` — apply tags

**Highlight key passages:**
1. `feednest_get_article` — get full content
2. Analyze and identify key passages
3. `feednest_add_highlight` for each important passage (use exact article text, not paraphrased)
