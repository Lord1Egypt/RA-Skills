# ChatLift — Limitations

**Last updated:** 2026-02-21

---

## What This Does NOT Do

### 1. Real-Time Sync

**Limitation:** ChatLift does NOT automatically sync with AI platforms.

**Why:** Platforms don't provide APIs for conversation export (only manual exports).

**Workaround:**
- Export manually from each platform
- Re-import periodically to update archive
- Use duplicate handling to avoid re-processing

---

### 2. Semantic Search

**Limitation:** Search is text-based (substring/regex matching), not semantic.

**Example:**
- Searching "ML" won't find "machine learning"
- Searching "code" won't find "programming"

**Why:** Semantic search requires embeddings and vector database (heavy dependencies).

**Workaround:**
- Use regex patterns: `machine.learning|ML|m\.l\.`
- Search multiple terms separately
- Use synonyms in search queries

---

### 3. Export Format Variations

**Limitation:** Export formats vary by platform version. ChatLift may not parse all variations.

**Example:**
- ChatGPT changed export format in 2023
- Claude export structure varies
- Gemini exports may differ by region

**Why:** Platforms update export formats without documentation.

**Workaround:**
- Check `conversations` successfully imported
- Report format issues (can add parser support)
- Manually edit JSON if needed

---

### 4. Large Archive Performance

**Limitation:** Search and archive generation slow with 10,000+ conversations.

**Why:** ChatLift loads all conversations into memory for search.

**Workaround:**
- Split archives by year or platform
- Use grep/ripgrep for very large archives
- Generate HTML archive for smaller subsets

---

### 5. No Attachment Support

**Limitation:** ChatLift only extracts text. Images, files, and attachments are ignored.

**Why:** Attachments are often separate downloads or embedded binary data.

**Workaround:**
- Download attachments separately from platform
- Reference attachment files in conversation metadata
- Future enhancement: attachment extraction

---

### 6. Limited Markdown Conversion

**Limitation:** Markdown conversion is basic. Complex formatting may be lost.

**Example:**
- Tables → plain text
- LaTeX math → raw LaTeX
- Nested lists may not render perfectly

**Why:** Full markdown parsing requires external libraries.

**Workaround:**
- Use HTML export for better formatting
- Use JSON export to preserve raw structure
- Manually clean up markdown if needed

---

### 7. No Multi-Turn Context Preservation

**Limitation:** Multi-part assistant responses may appear as separate messages.

**Why:** Export formats sometimes split long responses into chunks.

**Workaround:**
- Review JSON export for structure
- Manually merge messages if needed
- Future enhancement: context reconstruction

---

### 8. Timestamp Accuracy

**Limitation:** Timestamps may be missing or inconsistent across platforms.

**Why:** Not all platforms include timestamps in exports.

**Workaround:**
- Use conversation create_time as fallback
- Search ignores missing timestamps
- HTML archive shows timestamps when available

---

### 9. No Conversation Editing

**Limitation:** ChatLift doesn't support editing imported conversations.

**Why:** Designed as import/export tool, not conversation manager.

**Workaround:**
- Edit JSON files directly
- Re-import to update archive
- Use external editor for markdown files

---

### 10. Platform-Specific Features Lost

**Limitation:** Platform-specific features (plugins, code execution, image generation) are not preserved.

**Example:**
- ChatGPT plugin calls → plain text description
- Claude code execution → output only
- Gemini multimodal → text only

**Why:** Exports don't include execution metadata.

**Workaround:**
- Accept text-only export
- Save screenshots separately for important visual content

---

### 11. No Deduplication Across Platforms

**Limitation:** Same conversation exported from multiple platforms appears as duplicates.

**Why:** Different platforms use different IDs for same conversation.

**Workaround:**
- Manual review and deletion
- Use search to find similar conversations
- Future enhancement: fuzzy deduplication

---

### 12. HTML Archive Requires Browser

**Limitation:** HTML archive requires modern web browser with JavaScript.

**Why:** Search functionality uses JavaScript.

**Workaround:**
- Use markdown files for plain text access
- Use JSON files for programmatic access
- HTML works in any browser (Chrome, Firefox, Safari)

---

## Design Philosophy

**ChatLift is a converter, not a platform.**

✅ **Does well:**
- Import major AI platform exports
- Convert to portable formats
- Search text content
- Generate static archive

❌ **Doesn't do:**
- Real-time sync
- Semantic search
- Conversation editing
- Attachment management

**Recommended workflow:**

```
1. Export from AI platforms (manual, monthly)
2. Import to ChatLift
3. Search when needed
4. Archive remains offline/portable
```

ChatLift gives you ownership and searchability. It's not a replacement for the AI platforms themselves.

---

## Export Format Support

**Tested:**
- ChatGPT exports (2023-2024 format)
- Claude exports (Anthropic)
- Gemini exports (Google)

**Not tested:**
- Other AI chat platforms
- Custom chatbot exports
- Very old export formats

If your export doesn't work, check:
1. Is it valid JSON?
2. Does it have conversation structure?
3. File an issue with sample (redact sensitive data)

---

## Python Version Compatibility

**Requires:** Python 3.7+

**Why:** Uses `pathlib`, type hints, f-strings, `datetime.fromisoformat()`.

**Not tested on:** Python 2.x (will not work).

---

## Platform Support

**Tested on:**
- Linux (Ubuntu, Debian, Arch)
- macOS 10.15+
- Windows 10+ (WSL recommended)

**Known issues:**
- Windows path handling (use `Path` for cross-platform)
- Unicode handling (use UTF-8 encoding)

---

## When NOT to Use ChatLift

**Don't use ChatLift if:**

- You need real-time conversation sync → Use platform's native app
- You need semantic/AI-powered search → Use vector database tools
- You want to edit conversations → Use conversation management app
- You have 100,000+ conversations → Consider database solution

**Use ChatLift when:**

- You want to own your conversation history
- You need offline access to chats
- You want searchable archive
- You want portable formats (Markdown/HTML/JSON)

---

## Future Enhancements (Maybe)

**Possible additions:**
- Attachment extraction
- Semantic search via embeddings
- Fuzzy deduplication
- More platform support (Poe, Perplexity, etc.)

**Not planned:**
- Real-time sync (platform limitation)
- Conversation editing UI
- Cloud hosting/sync

ChatLift stays focused on import, search, and archive generation.

---

## Questions?

If something doesn't work as expected, check:
1. Is your export format supported?
2. Is the export file valid JSON?
3. Is it in this limitations doc?

Still stuck? Check the export file structure and compare to working examples.
