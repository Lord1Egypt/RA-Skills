---
name: base64-encode
description: Encode or decode text using Base64, URL percent-encoding, or HTML entities. Use when the user asks to encode, decode, base64 encode, base64 decode, URL encode, URL decode, percent-encode, HTML escape, HTML unescape, convert to base64, convert from base64, or escape special characters.
---

# Base64 / URL / HTML Encoder & Decoder

Encode or decode text using Base64, URL percent-encoding, or HTML entities. Processes text client-side with no external calls.

## Input
- The text string to encode or decode
- Encoding type: `base64` (default), `url`, or `html`
- Direction: `encode` (default) or `decode`

## Output
- The transformed string
- A brief note on the encoding type and direction applied

## Instructions

### Base64 (type: base64)

**Encode:**
1. Take the input string.
2. Convert each character to its UTF-8 byte sequence (handle non-ASCII/Unicode correctly).
3. Apply Base64 encoding using the standard alphabet (A–Z, a–z, 0–9, +, /).
4. Pad with `=` characters to make the length a multiple of 4.
5. The algorithm equivalent is: `btoa(unescape(encodeURIComponent(input)))`.

**Decode:**
1. Take the Base64-encoded input.
2. Validate it contains only valid Base64 characters (A–Z, a–z, 0–9, +, /, =).
3. Decode using: `decodeURIComponent(escape(atob(input)))`.
4. Return the original UTF-8 string.

### URL Percent-Encoding (type: url)

**Encode:**
1. Apply `encodeURIComponent` semantics: encode every character except `A–Z a–z 0–9 - _ . ! ~ * ' ( )`.
2. Spaces become `%20` (not `+`).
3. Non-ASCII characters are UTF-8 encoded then percent-escaped.

**Decode:**
1. Replace each `%XX` sequence with the corresponding byte.
2. Interpret the resulting bytes as UTF-8.
3. Equivalent to `decodeURIComponent(input)`.

### HTML Entities (type: html)

**Encode:** Replace these characters with their named HTML entities:
- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`
- `'` → `&#39;`

**Decode:** Reverse the mapping — replace each HTML entity with its literal character.

## Options
- `type`: `base64` | `url` | `html` — default: `base64`
- `direction`: `encode` | `decode` — default: `encode`

## Examples

**Base64 encode:**
Input: `Hello, World!`
Output: `SGVsbG8sIFdvcmxkIQ==`

**Base64 encode (Unicode):**
Input: `Héllo`
Output: `SMOpbGxv`

**Base64 decode:**
Input: `SGVsbG8sIFdvcmxkIQ==`
Output: `Hello, World!`

**URL encode:**
Input: `name=John Doe&city=New York`
Output: `name%3DJohn%20Doe%26city%3DNew%20York`

**URL decode:**
Input: `hello%20world%21`
Output: `hello world!`

**HTML encode:**
Input: `<script>alert("XSS")</script>`
Output: `&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;`

**HTML decode:**
Input: `&lt;h1&gt;Hello &amp; welcome&lt;/h1&gt;`
Output: `<h1>Hello & welcome</h1>`

## Error Handling
- **Invalid Base64 input for decode:** If the string contains characters outside the Base64 alphabet or has incorrect padding, report: `Error: Invalid Base64 string`. Ask the user to verify the input.
- **Invalid URL encoding for decode:** If a `%XX` sequence uses non-hex digits or the sequence is incomplete, report: `Error: Invalid URL encoded string`.
- **Empty input:** Return an empty string with a note that no input was provided.
- **Binary/non-text data:** Warn the user that Base64 encoding of binary data requires the raw bytes, which cannot be provided as plain text — suggest they use a tool that accepts file uploads.
