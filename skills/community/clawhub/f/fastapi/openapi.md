# OpenAPI — Docs That Are A Contract, Not A Byproduct

The schema is generated from your annotations, so schema problems are annotation problems. It is also the artifact other teams build against: treat a change to it like a change to the API, because it is one.

## What Produces What

| In code | In the schema |
|---|---|
| Return annotation or `response_model` | The 200 response body schema |
| Request model | The request body schema, with `$ref` to a component |
| `Annotated[int, Query(ge=1, le=100, description=...)]` | Parameter with constraints and description |
| Route docstring | Operation description (first line becomes the summary if `summary=` is absent) |
| `tags=["orders"]` | Grouping in the docs and, usually, the generated client's class name |
| `status_code=201` | The documented success status |
| `responses={404: {"model": ErrorBody}}` | Additional documented responses |
| `Security(...)` / security dependencies | Security requirements per operation |
| `deprecated=True` | Strike-through in the docs, deprecation in generated clients |
| `include_in_schema=False` | Nothing — route works, stays undocumented |

Anything not annotated is invisible: a route returning a bare `dict` documents an empty object, and clients generated from it get no types.

## Making Generated Clients Usable

- Operation ids are the client's method names. FastAPI's default is derived from function name, path, and method — long and ugly (`read_users_users__user_id__get`). Set `operation_id="get_user"` per route, or supply one `generate_unique_id_function` for the whole app and get consistent names everywhere.
- Duplicate operation ids (the same router included twice) make most generators emit broken or colliding methods, with only a startup warning.
- Name response models after the resource and role (`UserRead`, `OrderPage`), not after the endpoint: those names become the client's types.
- Enums in models become enums in clients; a bare `str` field with documented magic values does not.
- Pin the generator's input: commit the generated `openapi.json` and diff it in CI. That diff is the review surface for accidental breaking changes.

## Examples And Descriptions

```python
class OrderCreate(BaseModel):
    sku: str = Field(examples=["SKU-123"], description="Catalog identifier")
    qty: int = Field(default=1, ge=1, le=100)
    model_config = ConfigDict(json_schema_extra={
        "examples": [{"sku": "SKU-123", "qty": 2}]})
```

- Field-level `examples` populate the try-it form; a model-level example shows a whole realistic body, which is what a human reading the docs actually needs.
- `Body(openapi_examples={...})` gives several named examples per endpoint (success, edge case, failure) with descriptions — the highest-value documentation per line in the whole schema.
- Descriptions belong on the fields, not in a wall of docstring: they travel into the client's docstrings and the docs UI.

## App-Level Metadata

```python
app = FastAPI(
    title="Orders API", version="2.3.0",
    summary="Order capture and fulfilment",
    openapi_tags=[{"name": "orders", "description": "Create and track orders"}],
    servers=[{"url": "https://api.example.com", "description": "prod"}],
)
```

- `version` is your API's version, not FastAPI's; generated clients and changelogs read it.
- `servers` matters behind a path prefix; combined with `root_path` it produces URLs clients can actually call (`deployment.md`).
- Custom schema post-processing (adding a global security scheme, stripping internal tags) goes in an `app.openapi()` override that caches its result in `app.openapi_schema` — without the cache it regenerates on every docs request.

## Exposure

- Internal API: `FastAPI(openapi_url=None)` disables the schema and both docs UIs in one setting; make it conditional on `environment` (`settings.md`).
- Keep docs but require auth: serve `/docs` behind an authenticated route that renders `get_swagger_ui_html`, with `openapi_url` pointing at an equally protected schema route.
- The schema leaks your internal model names, field constraints, and every route including admin ones. That is fine for a public API and a gift to an attacker on an internal one.
- The docs UIs load their JavaScript from a CDN by default; air-gapped deployments must self-host those assets or the docs page renders blank.

## Schema Drift And Compatibility

- Breaking, for a generated client: removing a field, tightening a type, making an optional request field required, changing a status code, renaming an operation id, changing an enum's members.
- Non-breaking: adding an optional request field, adding a response field (clients ignore unknown fields), adding a route, adding a documented error response.
- Deprecate for one release with `deprecated=True` and a sunset date in the description before removing anything.
- CI gate: generate the schema, diff against the committed copy, fail on unexpected differences. It catches the accidental removal of a response model far earlier than a consumer's bug report.
