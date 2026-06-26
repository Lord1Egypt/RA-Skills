# DrugFlow Common APIs Call Flow

## 0) Base URL and Session
1. Domain-only input is allowed; default to `https://<domain>`.
2. Use the same cookie session for all endpoints after sign in.

## 1) Sign In
1. Endpoint: `POST /signin`
2. Form fields:
- `email`
- `password`
- `phone` (some deployments enforce this as required; send placeholder like `0` if email login)
3. Success response: `{"detail":"ok"}`.

## 2) Sign Up
1. Endpoint: `POST /signup`
2. Form fields:
- `email`
- `name`
- `organization`
- `password1`
- `password2`
3. Success response usually `{"detail":"ok"}` with `201`.
4. Existing account usually returns `400` with validation errors.

## 3) Workspace APIs
1. List workspaces: `GET /api/workspace/list?page=1&page_size=20`
2. Create workspace: `POST /api/workspace/create`
- JSON body: `{"ws_name":"<name>","is_default":true}`
3. Reuse policy:
- if caller passed `ws_id`, use it directly.
- else choose default workspace (`status=1`) if exists.
- else choose first workspace.
- else create one.

## 4) Balance API
1. Endpoint: `GET /api/token/balance?account=person|team`
2. Parse `tokens` as available balance.

## 5) Jobs List API
1. Endpoint: `GET /api/jobs?ws_id=<ws_id>&page=1&page_size=20`
2. `ws_id` is mandatory.
3. Compatibility note:
- some deployments accept `ws_id` (workspace short id string).
- some deployments require workspace numeric `id`; map from `/api/workspace/list` and retry.

## 6) Script Entry Points
1. Shared client: `scripts/common/drugflow_api.py`
2. Smoke test: `scripts/common/test_common_apis.py`
3. VS flow (using shared client): `scripts/virtual-screening/run_vs_flow.py`
4. Docking flow (using shared client): `scripts/docking/run_docking_flow.py`
