# Output Templates

Templates for formatting news digests.

## Markdown Digest Template

```markdown
# 📰 News Digest

*Generated: {timestamp}*

## {category}

{articles}

---

### {title}
**Source:** {source} | **Time:** {published}

{summary}

[Read more]({link})

---

*Powered by Newsman*
```

## Slack Message Template

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "📰 News Digest - {category}",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*{title}*\n{summary}\n\n<{link}|Read more> · {source}"
      }
    },
    {
      "type": "divider"
    }
  ]
}
```

## Plain Text Template

```
📰 News Digest - {category}
Generated: {timestamp}

━━━━━━━━━━━━━━━━━━━━

{title}
Source: {source} | {published}

{summary}

Link: {link}

━━━━━━━━━━━━━━━━━━━━

Powered by Newsman
```

## JSON Output Format

```json
{
  "digest": {
    "generated_at": "{timestamp}",
    "category": "{category}",
    "total_items": {count},
    "articles": [
      {
        "title": "{title}",
        "summary": "{summary}",
        "source": "{source}",
        "published": "{published}",
        "link": "{link}",
        "category": "{category}"
      }
    ]
  }
}
```

## Customization

Edit the templates above to match your preferred output format.
Available placeholders:
- `{timestamp}` - Generation time
- `{category}` - News category
- `{title}` - Article title
- `{summary}` - Article summary
- `{source}` - Source name
- `{published}` - Publication time
- `{link}` - Article URL
- `{count}` - Total article count
