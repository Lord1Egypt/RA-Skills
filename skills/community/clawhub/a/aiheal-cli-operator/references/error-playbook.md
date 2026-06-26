# Error Playbook

## Response Envelope

Every command emits JSON:

- Success: `{"ok": true, "data": ...}`
- Failure: `{"ok": false, "error": {...}}`

Primary fields:

- `error.code`: `AUTH_ERROR`, `API_ERROR`, `VALIDATION_ERROR`, `RUNTIME_ERROR`, `UNKNOWN_ERROR`
- `error.status`: HTTP status when available (`0` for network failure)
- `error.message`: first human-readable diagnosis

## Typical Failures

### AUTH_ERROR (401)

Symptoms:

- `error.code = AUTH_ERROR`
- message like `Missing auth token` or auth rejection

Actions:

1. Run login command (`auth login` or phone variants)
2. Check token with `config get` and `whoami`
3. Ensure region and token slot match (`--region zh|en`)

### API_ERROR with status 0

Symptoms:

- `error.code = API_ERROR`
- `error.status = 0`
- message like `fetch failed`

Actions:

1. Verify `apiBaseUrl` in `config get`
2. Test network reachability outside CLI
3. Retry with explicit `--api-base https://aihealing.me/api`

### Validation/400 Errors

Symptoms:

- service returns field validation messages

Actions:

1. Compare payload keys and enum values with endpoint constraints
2. Prefer `--payload-file` to avoid shell escaping issues
3. Remove unexpected fields and retry

### CLI VALIDATION_ERROR (local preflight)

Symptoms:

- `error.code = VALIDATION_ERROR`
- `error.issues[]` contains field-level diagnostics before request is sent

Actions:

1. Fix each issue by `field` and `message`
2. Follow `expected` and `suggestion` when present
3. For `single-job create`, omit `requestId` to let CLI auto-generate
4. For `plan-stage-job create`, keep required fields (`planId`, `stageIndex`, `planPath`, `day`) and note that `requestId` is optional without auto-generation

### Async Job Timeout

Symptoms:

- `single-job wait` or `plan-stage-job wait` timed out

Actions:

1. Fetch direct status (`single-job get/by-request`, `plan-stage-job get`)
2. Inspect `status`, `progress`, and `errorMessage`
3. Increase `--timeout-ms` only if status is still progressing

### npm/npx EPERM cache issue

Symptoms:

- `npm error code EPERM`
- errors around npm cache ownership

Actions:

1. Prefer global install: `npm install -g aihealingmecli`
2. Use temp cache for one-shot runs:

```bash
NPM_CONFIG_CACHE=/tmp/aiheal-npm-cache npx -y -p aihealingmecli aiheal --help
```

## Runtime Notes

- Prefer installed package execution (`aiheal ...`)
- Use `npx -y -p aihealingmecli aiheal ...` when global binary is unavailable
- Keep API target on public endpoint unless user explicitly asks otherwise
