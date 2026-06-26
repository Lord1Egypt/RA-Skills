# Cohere Command A Translate — Complete Research & Usage Manual

> Researched: 2026-05-16 | 50+ empirical tests across 11 dimensions
> Model: `command-a-translate-08-2025` | 111B params | 8K in / 8K out | 23 languages

---

## 1. MODEL IDENTITY: What It Actually Is

**This is NOT a pure translation engine like Google Translate API.** It's a 111B-parameter LLM (based on Command A) finetuned via DPO with difficulty filtering for translation. It retains full LLM capabilities:

| Capability | Evidence |
|---|---|
| Translation | ✅ Core strength |
| Q&A | ✅ "What is the capital of France?" → full Paris description |
| Chat | ✅ "Tell me about yourself" → detailed Cohere model description |
| Math | ✅ "123 × 456" → step-by-step calculation → 56088 |
| Code generation | ✅ "Write a Python sort function" → full implementation with docs |
| Summarization | ✅ "Summarize this" → correct summary |
| Reasoning | ✅ Multi-step math explanation |

**Critical implication**: Without an explicit "translate" instruction, the model will answer questions/chat normally. You MUST include a translation directive in every request.

---

## 2. API USAGE

### Basic Request (curl)
```bash
curl -X POST https://api.cohere.ai/v2/chat \
  -H "Authorization: bearer $COHERE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "command-a-translate-08-2025",
    "messages": [
      {"role": "user", "content": "Translate everything that follows into Japanese:\n\nHello world"}
    ]
  }'
```

### Response Format
```json
{
  "id": "...",
  "message": {
    "role": "assistant",
    "content": [{"type": "text", "text": "こんにちは世界"}]
  },
  "finish_reason": "COMPLETE",
  "usage": {
    "billed_units": {"input_tokens": 16, "output_tokens": 5},
    "tokens": {"input_tokens": 511, "output_tokens": 7}
  }
}
```

**NOTES on token counting**: `billed_units` ≠ `tokens`. Billed tokens are what you pay for. The model adds internal tokens you don't pay for. Input tokens are ~30x higher than billed for short texts (template overhead).

### Python SDK
```python
from cohere import ClientV2
co = ClientV2(api_key="...")

response = co.chat(
    model="command-a-translate-08-2025",
    messages=[{"role": "user", "content": f"Translate everything that follows into Japanese:\n\n{text}"}],
    temperature=0.3,          # optional, recommended
    max_tokens=4000,          # optional, defaults to 8K
    safety_mode="CONTEXTUAL", # default
)
print(response.message.content[0].text)
```

### Available Parameters
| Parameter | Type | Default | Effect |
|---|---|---|---|
| `model` | string | required | `"command-a-translate-08-2025"` |
| `messages` | array | required | Chat messages (system + user) |
| `temperature` | float | model default | 0.1=deterministic, 1.0=creative |
| `max_tokens` | int | 8000 | Cap output length |
| `safety_mode` | string | `"CONTEXTUAL"` | `"CONTEXTUAL"` / `"STRICT"` / `"NONE"` |
| `stop_sequences` | array | none | Stop generation on matching string |
| `stream` | boolean | false | Enable SSE streaming |

---

## 3. PARAMETER DEEP DIVE

### 3.1 Temperature

Test: Same input (EN→JA), temperatures 0.1 to 1.0

| Temp | Result | Notes |
|---|---|---|
| 0.1 | 素早い茶色のキツネが怠け者の犬を飛び越えた。近所は美しい日だった。 | Identical to 0.3 |
| 0.3 | (same as above) | **RECOMMENDED for translation** |
| 0.5 | (same as above) | Still consistent |
| 0.7 | 素早い茶色の**狐**が...近所は**とても良い天気**だった。 | Kanji variant + nuance shift |
| 1.0 | 素早い茶色のキツネ**は**...近所は**とてもいい日**だった。 | More variation |

**Recommendation**: Use `temperature=0.3` for translation. It produces consistent, accurate output without the artificial "flatness" of 0.1. Higher temperatures (>0.5) introduce unnecessary variation that harms translation reliability.

### 3.2 max_tokens

| max_tokens | Effect |
|---|---|
| 5 | Cuts off mid-sentence: `カスタマーサービスの担当者は非常に親切で、` (incomplete, finish_reason=MAX_TOKENS) |
| 50 | Complete translation: `カスタマーサービスの担当者は非常に親切で、数分以内に問題を解決してくれました。` |
| (default) | 8000 — sufficient for any practical translation |

**Warning**: If `max_tokens` is too low and cuts off mid-translation, `finish_reason` will be `"MAX_TOKENS"` — always check this field.

### 3.3 safety_mode

Test: "The competitor's product is terrible and their CEO is incompetent."

| Mode | Result |
|---|---|
| CONTEXTUAL | Normal translation produced |
| STRICT | Normal translation produced |
| NONE | Normal translation produced |

**Finding**: safety_mode has no observable effect on standard translation tasks. The model translates content faithfully regardless of setting. This parameter is about safety refusal, not translation filtering.

### 3.4 stop_sequences

Test: "Translate ...\n\nFirst sentence.\nSecond sentence.\nThird sentence." with stop at `\n`

- Stops generation at first newline in output
- Useful for extracting only the first line of translation
- Up to 5 stop strings supported

### 3.5 stream

Streaming via SSE available but not tested in this research. Standard for real-time UI display.

---

## 4. SYSTEM MESSAGE: Does It Work?

### 4.1 Influence on Translation Tone

Test: Same EN→JA text with various system messages:

| System Message | Result | Effective? |
|---|---|---|
| None | 明日はランチを食べに行くべきだと思うんだけど、どう思う？ | — |
| "Use formal keigo" | **IDENTICAL** | ❌ No effect |
| "Use casual friendly" | **IDENTICAL** | ❌ No effect |
| "Translate literally" | **ERROR (API crash)** | ❌ Broke |

**Critical finding**: System messages have **minimal to zero observable effect** on translation output for this model. The model's translation behavior appears to be hard-coded through its DPO training. Changing formality/tone via system prompt does NOT work reliably.

**What DOES work**: The system message works for operational constraints:
- "Output ONLY the translation" → respected
- "Keep numbers/URLs as-is" → respected  
- Glossary instructions → respected (though model may already do it)

### 4.2 Verified System Prompt Capabilities

✅ **Works**: Operational constraints (output format, preservation rules)
❌ **Doesn't work reliably**: Tone/formality control, translation style

---

## 5. PROMPT FORMAT: What's Optimal?

Test: 4 prompt formats × 3 text types (casual, business, technical)

| Format | Example | Quality | Input tokens |
|---|---|---|---|
| BARE | `"Translate to Japanese: {text}"` | ✅ Good | Lowest |
| RECOMMENDED | `"Translate everything that follows into Japanese:\n\n{text}"` | ✅ Good | +5 tokens |
| INSTRUCTION | `"Please translate the following text to Japanese accurately and naturally.\n\n{text}"` | ✅ Good | +9 tokens |
| NATURAL | `"Translate this into Japanese: \"{text}\""` | ⚠️ Adds quotes to output | +2 tokens |

**Recommendation**: Use the RECOMMENDED format. It's what Cohere designed the model for and provides clear separation between instruction and content.

The model also understands:
- `"日本語に翻訳してください"` (Japanese instruction)
- `"Translate to ja"` (language code)
- `"次の文章を翻訳してください"` (implicit target)

Target language can be specified as name ("Japanese"), code ("ja"), or implied by prompt language.

---

## 6. TRANSLATION QUALITY BY DOMAIN

### 6.1 EN→JA

| Domain | Test Input | Quality | Notes |
|---|---|---|---|
| Casual | "Hey, what's up? Wanna grab some coffee?" | ⭐⭐⭐⭐⭐ | Natural Japanese: `やあ、調子はどう？後でコーヒーでも飲まない？` |
| Business | "cordially invite you to our annual shareholders meeting" | ⭐⭐⭐⭐⭐ | Proper formal: `ご案内申し上げます` |
| Technical | "token bucket algorithm with refill rate" | ⭐⭐⭐⭐⭐ | Accurate: `トークンバケットアルゴリズム...リフィルレート` |
| Legal | "Lessee shall indemnify and hold harmless" | ⭐⭐⭐⭐ | Good but some legal nuance may be simplified |
| Medical | "acute abdominal pain... suggestive of appendicitis" | ⭐⭐⭐⭐⭐ | Accurate medical terminology |
| Literary | "autumn leaves danced... world set ablaze" | ⭐⭐⭐⭐ | Poetic but slightly literal |
| Marketing | "Unlock your potential! 50% off! 🔥" | ⭐⭐⭐⭐⭐ | Natural, preserves emoji and energy |
| Gaming | "Press R1 to dodge roll, hold L2 to aim" | ⭐⭐⭐⭐ | Good, preserves game terminology |

### 6.2 JA→EN

| Type | Test Input | Quality | Notes |
|---|---|---|---|
| Casual | `お疲れ様です。資料を送っていただけますか？` | ⭐⭐⭐⭐ | Good but "otsukaresama" nuance lost |
| Keigo | `格別のご高配を賜り、厚く御礼申し上げます` | ⭐⭐⭐⭐⭐ | Excellent: "sincere gratitude for your continued support" |
| Onomatopoeia | `ザーザー降っていて、ビュービュー吹いて` | ⭐⭐⭐⭐ | Good: "raining heavily... wind was howling" |
| Complex | Long government-style sentence | ⭐⭐⭐⭐ | Correct but slightly unnatural flow |
| Culture | `お盆には先祖の霊が帰ってくる` | ⭐⭐⭐⭐⭐ | "Obon" preserved with context: "spirits of ancestors return during Obon" |
| Slang | `それな。まじ卍。草生えるwww` | ❌ API ERROR | **Slang/abbreviated Japanese causes errors** |

### 6.3 Other Language Pairs

| Pair | Quality | Notes |
|---|---|---|
| Korean ↔ EN | ⭐⭐⭐⭐ | Good |
| Chinese ↔ EN | ⭐⭐⭐⭐ | Good |
| French ↔ EN | ⭐⭐⭐⭐⭐ | Excellent |
| Spanish ↔ EN | ⭐⭐⭐⭐⭐ | Excellent |

---

## 7. STRENGTHS

### 7.1 What It Excels At

1. **Business/formal translation**: Handles keigo, polite forms, business correspondence naturally
2. **Technical accuracy**: Preserves technical terms correctly
3. **Number/date handling**: `$1,234.56` → preserved correctly
4. **URL/code preservation**: Markdown, code blocks, URLs kept intact
5. **Cultural adaptation**: "Obon" explained, not just transliterated
6. **Consistent output**: Low temperature produces identical results across runs
7. **Multi-language understanding**: Accepts instructions in Japanese, English, codes
8. **Long text**: Correct translation even at 600+ input tokens
9. **Emoji preservation**: `🔥` preserved in translated output
10. **Name handling**: `Tanaka-san from Suzuki Corporation` correctly preserved

### 7.2 Edge Cases Handled Well

- Mixed Japanese/English text → natural integration
- Roman numerals → correct (`Chapter IV` → proper)
- Very short text (single words) → handled
- Repeated words → handled
- Complex negation → accurate Japanese rendering

---

## 8. WEAKNESSES & LIMITATIONS

### 8.1 Critical Limitations

1. **Japanese slang/abbreviated forms cause API errors**: `それな。まじ卍。草生えるwww` crashed the API call. Internet slang, 2ch-style abbreviations, and heavily abbreviated casual Japanese are problematic.

2. **System messages can't control translation tone**: Unlike general-purpose LLMs, this model's translation style is largely hardwired. You cannot reliably switch between formal/casual via system prompt.

3. **8K input limit**: The model's 8K token input window is small compared to modern LLMs (GPT-5 has 1M+). Long documents need chunking.

4. **Not a pure translator**: It will happily answer questions, write code, or do math if not given an explicit translation instruction. This is both a strength and a risk — always include "Translate" in the prompt.

5. **Input token overhead**: Short texts incur ~30x overhead in total tokens vs billed. A 16-token billed input consumed 511 actual tokens (system prompt template + Cohere internal additions). For many small translations, this overhead dominates.

6. **Nested conditionals**: Very complex grammatical structures (triple-nested conditionals) may be restructured incorrectly. The model can lose track of which clause modifies what.

### 8.2 Quality Issues Observed

- JA→EN long sentences: Grammatically correct but sometimes unnatural flow
- Literary text: Slightly too literal, loses some poetic nuance
- Keigo-to-English: `お疲れ様です` becomes generic "Could you..." — the uniquely Japanese greeting nuance is lost (inherent limitation of any translation)
- Repetition with repeated input: If input text is repetitive (e.g., same sentence 30 times), output will also be repetitive (not a bug — expected behavior)

### 8.3 Not Suitable For

- Real-time chat translation (too slow, API round-trip)
- Translating internet slang / 2ch-style Japanese
- Documents >8K tokens without chunking strategy
- Tasks requiring precise tone control (formal/casual switching)

---

## 9. CONSISTENCY TEST

Same input × 3 runs (temperature default):

| Run | Output |
|---|---|
| 1 | 四半期決算報告は市場予想を12%上回り、アジア太平洋地域の好調な業績が主な要因でした。 |
| 2 | (identical) |
| 3 | (identical) |

✅ Perfect consistency at default temperature. This is crucial for production use — you get the same translation every time.

---

## 10. PRACTICAL GUIDELINES

### 10.1 Optimal Request Template
```python
def translate(text, target_language="Japanese", source_language=None):
    """Optimal translation call for command-a-translate-08-2025."""
    return co.chat(
        model="command-a-translate-08-2025",
        messages=[{
            "role": "user",
            "content": f"Translate everything that follows into {target_language}:\n\n{text}"
        }],
        temperature=0.3,
    ).message.content[0].text
```

### 10.2 When to Chunk
- Text >~6000 characters → chunk at natural boundaries
- Use the Cohere-recommended `chunk_split()` with threshold=0.8
- Split at `\n`, `.`, `)` — sentence boundaries
- 15 words per chunk maximum for best quality

### 10.3 Error Handling
```python
def safe_translate(text, target_lang="Japanese"):
    try:
        resp = call(...)
        if resp.get("finish_reason") == "MAX_TOKENS":
            # Translation truncated — need longer max_tokens or chunking
            return None, "truncated"
        return resp["message"]["content"][0]["text"], None
    except Exception as e:
        # May fail on: slang, encoding issues, rate limits
        return None, str(e)
```

### 10.4 Cost Optimization
- Short texts: Group multiple small translations into one request
- Overhead: Each call has ~500 token overhead — batch when possible
- Trial key: 1,000 calls/month, 20 req/min

### 10.5 Language Detection
The model does NOT auto-detect source language. You must specify the target. The source language is inferred from the text itself.

---

## 11. COMPARISON: WHEN TO USE THIS vs DASHSCOPE QWEN-MT

| Factor | Cohere Command A Translate | DashScope qwen-mt |
|---|---|---|
| Quality (EN↔JA) | SOTA (per benchmarks) | Good |
| System prompt control | ❌ Does NOT control tone | ❌ Not supported at all |
| Non-translation tasks | ✅ Full LLM capability | ❌ Translation only |
| Free tier | 1,000 calls/month (trial) | DashScope free quota |
| Input token overhead | ~30x (511 tokens for 16 billed) | Lower |
| Slang handling | ❌ Crashes on JA slang | Unknown |
| API simplicity | Standard chat API | OpenAI-compatible |

---

## 12. QUICK REFERENCE CARD

```
MODEL:        command-a-translate-08-2025
ENDPOINT:     POST https://api.cohere.ai/v2/chat
AUTH:         Bearer $COHERE_API_KEY
TEMP:         0.3 (optimal for translation)
MAX_TOKENS:   4000 (safe default, model max 8000)
PROMPT:       "Translate everything that follows into {target}:\n\n{text}"
LANGUAGES:    23 (EN, JA, KO, ZH, FR, ES, DE, IT, PT, AR, RU, PL, TR, VI, NL, CS, ID, UK, RO, EL, HI, HE, FA)
RATE LIMIT:   20 req/min (trial), 1000 calls/month
PRICE:        Free (trial key)
CONTEXT:      8K input / 8K output
SYSTEM MSG:   Works for constraints, NOT for tone control
STREAMING:    Supported (SSE)
```
