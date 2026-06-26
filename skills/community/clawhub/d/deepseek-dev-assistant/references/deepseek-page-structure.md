# DeepSeek Share Page Structure

Last updated: 2026-05-24 (verified with real share link)

## URL patterns

| Pattern | Example |
|---------|---------|
| Share link | `https://chat.deepseek.com/share/2n4t1lmt7xn2a50rt2` |
| Direct chat | `https://chat.deepseek.com/a/chat/*` |

## Page behavior (verified)

- Content is **fully JS-rendered** — `web_fetch` returns only "DeepSeek\n" (~8 bytes of text)
- Puppeteer with `networkidle2` successfully renders all content (~1043 lines / 24KB for a single-turn chat with a large code block)
- The page includes "专家模式" badge and "该对话来自分享，由 AI 生成，请仔细甄别。" disclaimer

## Output structure (verified)

The browser returns plain text in this order:
1. Page header: "来自分享的对话", "专家模式", disclaimer
2. User messages (labeled by username or "User")
3. Assistant thinking block: "已思考（用时 XX 秒）" followed by reasoning text
4. Assistant response with code blocks and formatted content
5. Footer boilerplate: "本回答由 AI 生成，内容仅供参考，请仔细甄别。"
6. "和 DeepSeek 继续聊" link

## Cleaning the output

To extract code from the raw output:

**For complete HTML files** (common when DeepSeek outputs a full page):
```bash
sed -n '/<!DOCTYPE html>/,$p' /tmp/raw.txt | sed '/<\/html>/q' > output.html
```

**For code blocks**: look for ` ```language ... ``` ` pattern within the chat segment.

**Strip trailing boilerplate**: everything after "本回答由 AI 生成" can be discarded.

## Extraction gotchas

- Code blocks within the chat appear as plain text (no HTML tags) since `innerText` strips markup
- The thinking/reasoning block precedes the actual code — don't confuse it with the code output
- DeepSeek sometimes includes explanatory prose after code blocks (e.g. feature descriptions) — these are not part of the code
- Single-turn conversations with code output are common; the thinking block contains the design decisions
