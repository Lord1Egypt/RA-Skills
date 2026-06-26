# Examples

Concrete usage patterns for running agent memory on top of `echo-fade-memory`.

Assumption in this file:

- commands are run from the installed skill directory
- script paths use `./scripts/...`

## 1. Store a Preference

```bash
./scripts/store.sh \
  "User prefers concise answers and dislikes nested bullets" \
  --summary "response style preference" \
  --type preference
```

## 2. Store a Project Decision

```bash
./scripts/store.sh \
  "Project decision: use chromem-go as the embedded vector store to keep setup lightweight and dependency-free" \
  --summary "vector backend decision" \
  --type project
```

If the decision really needs stronger durability or versioning, then add advanced flags such as `--importance` or `--conflict-group`.

## 3. Store a Screenshot

```bash
./scripts/store.sh \
  "/absolute/path/to/deployment-checklist.png" \
  --object-type image \
  --caption "deployment checklist screenshot" \
  --tag deployment \
  --ocr-text "Deployment Checklist"
```

## 4. Recall Before Answering

```bash
./scripts/recall.sh "vector backend decision"
./scripts/recall.sh "the screenshot containing Deployment Checklist"
```

Typical response fields to inspect:

- `mixed`
- `memories`
- `images`
- `entities`

## 5. Forget Incorrect or Obsolete State

```bash
./scripts/forget.sh "temporary deployment note"
./scripts/forget.sh "latency spike screenshot" image
```

## 6. Ground a Fuzzy Memory

```bash
curl -sS "$EFM_BASE_URL/v1/memories/<id>/ground"
```

Use this when a memory is old, fragmentary, or needs source verification before reuse.
