# Mail Translation Contracts

## Files to prepare in your own project

Create or maintain equivalent contract docs for:
- mail translation prompt contract
- mail assistant product/result contract
- postprocess boundary contract
- implementation closeout or architecture notes

## What matters

### Prompt layer owns
- subject formatting
- date formatting
- bilingual body formatting
- recipient truncation
- history summarization
- duplicate suppression
- signature formatting

### Program layer owns
- raw mail extraction
- prompt assembly
- lightweight worker / LLM runtime invocation
- output extraction
- failure fallback

### Product direction
- Keep bilingual output when language-learning support or source transparency matters
- Preserve channel-specific indentation only if the downstream channel renderer requires it
- If translation equals original, keep only the original
- If recipients exceed 3, show first 3 and end with `...`
- If quoted history exists, summarize it below the main body using a clear label such as `历史邮件摘要：`
- Postprocess should remain pass-through for formatting
