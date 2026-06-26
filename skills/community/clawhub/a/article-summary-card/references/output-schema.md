# Output Schema

The preferred workflow writes the final JSON in-session, then renders it. A heuristic draft helper can also write a JSON object like:

```json
{
  "title": "Article title",
  "source": "https://example.com",
  "one_sentence": "One-sentence summary.",
  "sections": [
    {
      "heading": "What happened",
      "summary": "Section summary.",
      "points": ["Point 1", "Point 2"]
    }
  ],
  "closing_takeaway": "Final takeaway.",
  "tags": ["tag1", "tag2", "tag3"]
}
```

Constraints:
- `one_sentence`: 40-80 Chinese characters when possible.
- `sections`: 2 to 4 sections.
- Each section should include a short heading, one summary line, and 2 to 3 points.
- `closing_takeaway`: one short closing conclusion tied to the article itself.
- `tags`: 3 to 8 short tags generated during the planning pass and displayed at the end of the rendered output.
