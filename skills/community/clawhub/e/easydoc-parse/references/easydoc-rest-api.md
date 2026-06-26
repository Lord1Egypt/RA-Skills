# EasyDoc REST API Reference (CN + Global)

## Platform Matrix

| Platform | Base URL | Submit | Result | File Field | Recommended Mode |
| --- | --- | --- | --- | --- | --- |
| CN (EasyLink) | `https://api.easylink-ai.com` | `POST /v1/easydoc/parse` | `GET /v1/easydoc/parse/{task_id}` | `files` | `easydoc-parse-flash`, `easydoc-parse-premium` |
| Global (EasyDoc) | `https://api.easydoc.sh` | `POST /api/v1/parse` | `GET /api/v1/parse/{task_id}/result` | `file` | `lite` |

Max file size: `100 MB` per file for both platforms.

## Registration And API Key

CN platform:

1. Open `https://platform.easylink-ai.com`
2. Register or sign in
3. Create API key from key management page
4. Use key via header `api-key`
5. Recommended local env var: `EASYLINK_API_KEY`

Global platform:

1. Open `https://platform.easydoc.sh`
2. Register or sign in
3. Create API key from key management page
4. Use key via header `api-key`
5. Recommended local env var: `EASYDOC_API_KEY`

## CN Platform Details

Submit:

```bash
curl -X POST "https://api.easylink-ai.com/v1/easydoc/parse" \
  -H "api-key: your_apikey_here" \
  -F "files=@medical_record_001.pdf" \
  -F "mode=easydoc-parse-premium"
```

Poll:

```bash
curl -X GET "https://api.easylink-ai.com/v1/easydoc/parse/{task_id}" \
  -H "api-key: your_apikey_here"
```

Supported formats:

- `.pdf`
- `.dotm`
- `.docm`
- `.doc`
- `.dotx`
- `.docx`
- `.txt`
- `.html`
- `.dot`
- `.xltm`
- `.xlsm`
- `.xlsx`
- `.xls`
- `.xlt`
- `.potm`
- `.pptx`
- `.ppt`
- `.pot`
- `.pps`
- `.tif`
- `.png`
- `.jpg`
- `.bmp`

Typical successful submit response:

```json
{
  "success": true,
  "data": {
    "task_id": "b_parse_81d006e2-9295-4752-9033-9a37f24bc11d1748171169254",
    "status": "PROCESSING"
  }
}
```

## Global Platform Details

Submit:

```bash
curl "https://api.easydoc.sh/api/v1/parse" \
  -X POST \
  -H "api-key: your-api-key" \
  -F "file=@demo_document.pdf" \
  -F "mode=lite"
```

Poll:

```bash
curl "https://api.easydoc.sh/api/v1/parse/{task_id}/result" \
  -X GET \
  -H "api-key: your-api-key"
```

Supported formats:

- `.pdf`
- `.txt`
- `.docx`
- `.doc`
- `.pptx`
- `.ppt`

Notes:

- Start with `lite` mode for fastest processing.
- Keep API key private and avoid exposing it in repositories.

## Common Status Handling

Treat these as in-progress:

- `PENDING`
- `PROCESSING`
- `RUNNING`
- `IN_PROGRESS`
- `QUEUED`

Treat these as terminal:

- `SUCCESS`
- `ERROR`
- `FAILED`
- `COMPLETED`
- `DONE`

## Normalized Output Contract

Use this normalized structure for both platforms:

```json
{
  "task_id": "string",
  "status": "string",
  "files": [
    {
      "file_name": "string",
      "markdown": "string or null",
      "nodes": []
    }
  ],
  "raw": {}
}
```

## RAG Usage Guidance

When parsed JSON is used as a retrieval corpus, do not full-load the file by default.

Preferred workflow:

1. If the host agent provides a text-search tool such as `Grep`, `Search`, or equivalent file-content search, use that tool first against the parsed JSON file.
2. Search by query terms, aliases, dates, section headers, node ids, or `type` values such as `Title`, `Text`, `Table`, `Figure`.
3. Open only the matching lines or narrow surrounding windows.
4. Extract just the relevant nodes for chunking, summarization, or embedding.

Guidance:

- Prefer the agent's dedicated search tool over shelling out to `grep` or `rg`.
- Do not add a custom in-skill Python search script just for this retrieval path.
- Only fall back to shell-based search when the host agent does not expose an equivalent search tool.

Only load the full JSON when:

- full tree traversal is required
- global hierarchy reconstruction is required
- export or validation requires complete payload inspection

## Bundled Script Notes

`scripts/easydoc_parse.py` supports both platforms via `--platform cn|global`.

Examples:

```bash
python3 scripts/easydoc_parse.py --platform cn --api-key "$EASYLINK_API_KEY" \
  --file ./demo.pdf --mode easydoc-parse-premium --save ./cn.json

python3 scripts/easydoc_parse.py --platform global --api-key "$EASYDOC_API_KEY" \
  --file ./demo.pdf --mode lite --save ./global.json
```

Useful options:

- `--output-format normalized|raw`
- `--query-retries 3`
- `--skip-local-checks`

If `--api-key` is omitted, script resolves from env vars:

- `--platform cn`: prefer `EASYLINK_API_KEY`, fallback `EASYDOC_API_KEY`
- `--platform global`: prefer `EASYDOC_API_KEY`, fallback `EASYLINK_API_KEY`
