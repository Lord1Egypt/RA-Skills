# Gamma API Reference

## Base URL
`https://public-api.gamma.app/v1.0`

## Authentication
Header: `X-API-KEY: sk-gamma-xxxxx`

## Endpoints

### POST /generations
Create a new gamma from scratch.

**Required:**
- `inputText` (string) — content/prompt (up to ~100K tokens / 400K chars)
- `textMode` (string) — `generate` | `condense` | `preserve`

**Optional:**
- `format` — `presentation` | `document` | `social` | `webpage`
- `themeId` — theme ID (get from GET /themes)
- `numCards` — 1-60 (Pro) or 1-75 (Ultra)
- `cardSplit` — `auto` (uses numCards) | `inputTextBreaks` (uses `\n---\n` in inputText)
- `additionalInstructions` — extra guidance (1-2000 chars)
- `folderIds` — array of folder IDs
- `exportAs` — `pdf` | `pptx` (download links expire)
- `textOptions.amount` — `brief` | `medium` | `detailed` | `extensive`
- `textOptions.tone` — free text (1-500 chars), e.g. "professional, inspiring"
- `textOptions.audience` — free text (1-500 chars)
- `textOptions.language` — ISO code, e.g. "en", "es", "fr"
- `imageOptions.source` — `aiGenerated` | `pictographic` | `pexels` | `giphy` | `webAllImages` | `webFreeToUse` | `webFreeToUseCommercially` | `placeholder` | `noImages`
- `imageOptions.model` — `flux-1-pro` | `imagen-4-pro` | etc.
- `imageOptions.style` — free text (1-500 chars), e.g. "photorealistic"
- `cardOptions.dimensions`:
  - presentation: `fluid` | `16x9` | `4x3`
  - document: `fluid` | `pageless` | `letter` | `a4`
  - social: `1x1` | `4x5` | `9x16`
- `cardOptions.headerFooter` — positions: topLeft/topRight/topCenter/bottomLeft/bottomRight/bottomCenter
  - type: `text` (+ value), `image` (+ source: themeLogo|custom, + src for custom, + size: sm|md|lg|xl), `cardNumber`
  - `hideFromFirstCard`, `hideFromLastCard` (boolean)
- `sharingOptions.workspaceAccess` — `noAccess` | `view` | `comment` | `edit` | `fullAccess`
- `sharingOptions.externalAccess` — `noAccess` | `view` | `comment` | `edit`
- `sharingOptions.emailOptions.recipients` — array of emails
- `sharingOptions.emailOptions.access` — `view` | `comment` | `edit` | `fullAccess`

**Response:** `{ "generationId": "xxx" }`

### POST /generations/from-template
Create a new gamma based on an existing template.

**Required:**
- `gammaId` — ID of the template gamma
- `prompt` — instructions + content (up to ~100K tokens minus template size)

**Optional:** `themeId`, `folderIds`, `exportAs`, `imageOptions`, `sharingOptions` (same as above)

**Response:** `{ "generationId": "xxx" }`

### GET /generations/{generationId}
Check status of a generation.

**Response (pending):** `{ "status": "pending", "generationId": "xxx" }`
**Response (completed):** `{ "status": "completed", "generationId": "xxx", "gammaUrl": "https://gamma.app/docs/xxx", "credits": { "deducted": 150, "remaining": 3000 } }`

### GET /themes
List available themes. Supports pagination.

**Params:** `query` (optional), `limit` (max 50), `after` (cursor)
**Response:** `{ "data": [{ "id", "name", "type": "standard|custom", "colorKeywords", "toneKeywords" }], "hasMore", "nextCursor" }`

### GET /folders
List folders. Supports pagination.

**Params:** `query` (optional), `limit` (max 50), `after` (cursor)
**Response:** `{ "data": [{ "id", "name" }], "hasMore", "nextCursor" }`

## Credits & Pricing
- Per card: 1-5 credits
- AI images: 2-125 credits/image depending on model tier (basic/advanced/premium/ultra)
- Template-based generations may cost slightly more per card
- Credits shown in GET response: `{ "credits": { "deducted": N, "remaining": N } }`

## Tips
- Insert image URLs directly into inputText where you want them
- Use `\n---\n` in inputText to control card breaks (with cardSplit: inputTextBreaks)
- Set imageOptions.source to noImages if providing your own image URLs
- Export links (PDF/PPTX) expire after a period — download promptly
- JSON-escape inputText if it contains special characters
