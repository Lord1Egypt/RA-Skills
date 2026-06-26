# Full command reference

```
faces auth:login        --email  --password
faces auth:logout
faces auth:register     --email  --password  --username  [--name]  [--invite-key]
faces auth:whoami
faces auth:refresh
faces auth:connect      <provider>  [--manual]
faces auth:disconnect   <provider>
faces auth:connections

faces face:create       --name  --username  [--default-model MODEL]  [--description TEXT]  [--formula EXPR | --attr KEY=VALUE... --tool NAME...]
faces face:list
faces face:get          <face_id>
faces face:update       <face_id>  [--name]  [--default-model MODEL]  [--description TEXT]  [--formula EXPR]  [--attr KEY=VALUE]...
faces face:delete       <face_id>  [--yes]
faces face:stats
faces face:upload       <face_id>  --file PATH  [--kind document|thread]  [--perspective first-person|third-person]  [--face-speaker NAME]
faces face:diff         --face USERNAME  --face USERNAME  [--face USERNAME]...
faces face:neighbors    <face_id>  [--k N]  [--component face|beta|delta|epsilon]  [--direction nearest|furthest]

faces chat:chat         <face_username>  -m MSG  [--llm MODEL]  [--system]  [--stream]
                        [--max-tokens N]  [--temperature F]  [--file PATH]  [--responses]
faces chat:messages     <face@model | model>  -m MSG  [--system]  [--stream]  [--max-tokens N]
faces chat:responses    <face@model | model>  -m MSG  [--instructions]  [--stream]

faces compile:import       <face_id>  --url YOUTUBE_URL  [--type document|thread]  [--perspective first-person|third-person]  [--face-speaker LABEL]

faces compile:doc          <face_id>  (--content TEXT | --file PATH)  [--label]  [--perspective first-person|third-person]  [--timeout N]
faces compile:doc:create   <face_id>  [--label]  (--content TEXT | --file PATH)  [--perspective first-person|third-person]
faces compile:doc:make     <doc_id>  [--timeout N]
faces compile:doc:list     <face_id>
faces compile:doc:get      <doc_id>
faces compile:doc:edit     <doc_id>  [--label]  [--content TEXT | --file PATH]  [--perspective first-person|third-person]
faces compile:doc:delete   <doc_id>

faces compile:thread:create   <face_id>  [--label]
faces compile:thread:list     <face_id>
faces compile:thread:get      <thread_id>
faces compile:thread:edit     <thread_id>  --label TEXT
faces compile:thread:message  <thread_id>  -m MSG
faces compile:thread:make     <thread_id>  [--timeout N]
faces compile:thread:sync     <thread_id>
faces compile:thread:delete   <thread_id>  [--yes]

faces catalog:doctor   [--fix]  [--generate]
faces catalog:list

faces keys:create   --name  [--expires-days N]  [--budget F]  [--face USERNAME]...  [--model NAME]...
faces keys:list
faces keys:revoke   <key_id>  [--yes]
faces keys:update   <key_id>  [--name]  [--budget F]  [--reset-spent]

faces billing:balance
faces billing:subscription
faces billing:quota
faces billing:usage      [--group-by api_key|model|llm|date]  [--from DATE]  [--to DATE]
faces billing:topup      --amount F  [--payment-ref REF]
faces billing:checkout   [--plan connect]
faces billing:card-setup
faces billing:llm-costs  [--provider openai|anthropic|...]

faces account:state

faces config:set    <key> <value>
faces config:show
faces config:clear  [--yes]
```

## Default model (`--default-model`)

The `--default-model` flag on `face:create` and `face:update` sets the LLM used when no `--llm` override is provided to `chat:chat`. Without a default model, `chat:chat` requires `--llm` on every call.

```bash
faces face:create --name "Ada" --username ada --default-model gpt-5-nano
faces chat:chat ada -m "hello"    # uses gpt-5-nano automatically
```

## Chat auto-routing

`chat:chat` automatically routes to the correct API endpoint based on the model provider:

- `claude-*` models → Anthropic Messages API (`/v1/messages`)
- All other models → OpenAI Chat Completions API (`/v1/chat/completions`)
- `--responses` flag → OpenAI Responses API (`/v1/responses`)

`chat:messages` and `chat:responses` are still available for direct endpoint access.

## Compiling documents (`compile:doc`)

`compile:doc` is the recommended one-step command for compiling a document into a face. It handles create → compile (prepare + sync) automatically with real-time progress:

```bash
faces compile:doc alice --file essay.txt
```

Output:
```
Creating document... done (abc123)
Compiling (3 chunks):
  [1/3] ε=3 β=2 δ=1 α=5
  [2/3] ε=5 β=6 δ=2 α=12
  [3/3] ε=8 β=6 δ=5 α=26 (syncing)
Done.
```

For an already-created document, use `compile:doc:make <doc_id>` to compile it.

`--timeout` sets the polling timeout in seconds (default: 600 / 10 minutes).

## Catalog

The CLI maintains a local catalog at `~/.faces/catalog/` with a `FACE.md` file per face (YAML frontmatter + markdown notes) and a consolidated `~/.faces/catalog.json` index. The catalog is managed automatically on `face:create`, `face:update`, and `face:delete`.

- `faces catalog:doctor` — diagnose missing, stale, or orphaned catalog entries
- `faces catalog:doctor --fix` — rebuild catalog from API
- `faces catalog:doctor --generate` — fix + generate descriptions via LLM
- `faces catalog:list` — print catalog contents
- `faces config:set catalog false` — disable catalog management
- `faces config:set catalog_model gpt-5-nano` — set the model used for description generation

## Attributes (`--attr`)

The `--attr KEY=VALUE` flag on `face:create` and `face:update` sets basic demographic facts on a Face directly, without compiling a document. The flag is repeatable — pass one `--attr` per fact. These facts anchor the persona and improve compilation quality when source material is added later.

**Common attribute keys:**

| Key | Example value |
|---|---|
| `gender` | `female`, `male`, `non-binary` |
| `age` | `34` |
| `location` | `Portland, OR` |
| `occupation` | `nurse practitioner` |
| `education_level` | `master's degree` |
| `religion` | `Buddhist` |
| `ethnicity` | `Korean American` |
| `nationality` | `American` |
| `marital_status` | `married` |

These are the most common keys. Many more are accepted across categories including birth details, family, career, education, housing, and immigration. **Only keys on the accepted list work — unrecognized keys are silently ignored.** See [ATTRIBUTES.md](ATTRIBUTES.md) for the complete list of all accepted keys.

**Example — create a Face with basic facts:**
```bash
faces face:create --name "Maria Chen" --username maria \
  --attr gender=female --attr age=34 \
  --attr location="Portland, OR" \
  --attr occupation="nurse practitioner" \
  --attr education_level="master's degree" \
  --attr marital_status=married
```

**Example — add facts to an existing Face:**
```bash
faces face:update maria --attr religion=Buddhist --attr ethnicity="Korean American"
```

> Note: `--attr` cannot be combined with `--formula`. Composite faces inherit their facts from their component faces.

## Global flags

Any command accepts these flags:

```
faces [--base-url URL] [--token JWT] [--api-key KEY] [--json] COMMAND
```

## Environment variables

| Variable | Purpose |
|---|---|
| `FACES_BASE_URL` | Override API base URL (default: `api.faces.sh`) |
| `FACES_TOKEN` | JWT authentication token |
| `FACES_API_KEY` | API key authentication |
