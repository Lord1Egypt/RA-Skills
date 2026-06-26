# ContextSlim Limitations

This document honestly describes what ContextSlim **doesn't** do. Read this before deploying.

---

## What It Doesn't Do

### 1. **Exact Token Counts**
ContextSlim estimates tokens using word-based heuristics. It's accurate within 10-15% for English text, but **not exact**.

**Why:** Real tokenizers (tiktoken, transformers) are provider-specific, require heavyweight dependencies, and still vary between models. Word-based estimation is "good enough" for profiling without the baggage.

**When this matters:** Billing calculations, exact context limit checks. For those, use the provider's official tokenizer.

**Workaround:** Treat estimates as upper bounds. Add 10-15% buffer when planning.

---

### 2. **Non-English Accuracy**
Token-to-word ratios are calibrated for English. Accuracy drops significantly for:
- Languages with different word structures (Chinese, Japanese, Korean)
- Agglutinative languages (Turkish, Finnish)
- Languages with extensive diacritics

**Why:** Tokenization strategies vary wildly by language. No universal heuristic exists.

**Workaround:** Manually adjust ratios in `config.py` based on testing with your target language.

---

### 3. **Multimodal Contexts**
ContextSlim analyzes **text only**. It doesn't estimate tokens for:
- Images
- Audio
- Video
- Embedded files

**Why:** Image/audio tokenization is provider-specific and depends on resolution, duration, and encoding. No standard heuristic exists.

**Workaround:** Manually add provider's documented token costs for multimodal inputs.

---

### 4. **Code Tokenization**
Code has different token patterns than prose. Estimates may be less accurate for:
- Heavily indented code
- Code with lots of special characters
- Minified code
- Code with long identifiers

**Why:** Code tokenizers treat symbols, keywords, and structure differently than prose tokenizers.

**Workaround:** Test estimation accuracy on your specific codebase. Adjust if needed.

---

### 5. **Real-Time Monitoring**
ContextSlim is a **static analysis tool**. It doesn't:
- Hook into live AI conversations
- Monitor API usage in real-time
- Track context across sessions
- Alert you when context is getting full

**Why:** That would require integration with specific AI platforms and background processes.

**Workaround:** Run analysis manually before/after conversations. Integrate into your workflow as a pre-send check.

---

### 6. **Automatic Compression**
ContextSlim **suggests** compressions but doesn't apply them automatically.

**Why:** Context compression is lossy. What's "redundant" to a heuristic might be important to you. Human review required.

**Workaround:** Review suggestions and apply manually. Or write your own script to apply high-confidence suggestions.

---

### 7. **Custom Tokenizers**
ContextSlim doesn't support plugging in your own tokenizer.

**Why:** The whole point is to avoid tokenizer dependencies. If you have a tokenizer, you don't need ContextSlim's estimation.

**Workaround:** Use ContextSlim for profiling, then validate critical counts with your real tokenizer.

---

### 8. **Provider-Specific Features**
ContextSlim doesn't account for:
- Sliding context windows
- Cached context (Anthropic's prompt caching)
- Special token overhead (system headers, tool definitions)
- Model-specific context reservation

**Why:** These vary by provider and model. No universal standard.

**Workaround:** Manually subtract reserved tokens from the limit in `config.py`.

---

### 9. **Batch Processing UI**
No GUI, no batch file manager, no progress bars for analyzing hundreds of files.

**Why:** ContextSlim is a CLI tool. Batch processing is doable via shell scripts, but there's no built-in orchestration.

**Workaround:** Use shell loops for batch processing:
```bash
for file in prompts/*.txt; do
  python3 context_slim.py "$file" >> results.log
done
```

---

### 10. **Content Awareness**
ContextSlim treats all text equally. It doesn't know:
- Which parts of your prompt are critical vs. optional
- Whether an "example" is actually illustrative or just filler
- If shortening a phrase changes its meaning

**Why:** That requires semantic understanding, which requires... an AI model. (Ironic, right?)

**Workaround:** Human review of suggestions. You know your content best.

---

## Edge Cases

### Files Over 10 MB
Default max file size is 10 MB (configurable in `config.py`). Larger files are rejected.

**Why:** Word-splitting 100 MB text files in Python is slow and memory-intensive.

**Workaround:** Increase `MAX_FILE_SIZE` in config, or split large files before analysis.

---

### Binary Files
ContextSlim tries to read files as UTF-8 text. Binary files will error out.

**Why:** We're not building a file type detector.

**Workaround:** Only feed it text files. Check extension before processing.

---

### Deeply Nested JSON
Conversation JSON is parsed and analyzed, but deeply nested structures (10+ levels) may not be handled optimally.

**Why:** We're doing simple key lookups, not full JSON schema traversal.

**Workaround:** Flatten your conversation format before analysis.

---

## When NOT to Use ContextSlim

- **Billing validation:** Use official tokenizers for exact counts tied to costs
- **Production rate limiting:** Real-time monitoring requires integration, not static analysis
- **Non-text workflows:** Images, audio, video — out of scope
- **Legal/compliance:** "Approximately 8,000 tokens" isn't good enough for SLAs

---

## When TO Use ContextSlim

- **Prompt engineering:** Fast feedback on token usage while iterating
- **Debugging truncation:** "Why did my AI forget?" — see where the cutoff is
- **Compression opportunities:** Find low-hanging fruit for token savings
- **Team standards:** Enforce "system prompts under 5k tokens" policies
- **Offline analysis:** No internet, no API keys, just local profiling

---

## Honest Summary

ContextSlim is a **profiling tool**, not a precision instrument. It trades exactness for simplicity and zero dependencies. If you need byte-perfect token counts, use a real tokenizer. If you want fast, good-enough estimates without installing half of PyPI, this is your tool.
