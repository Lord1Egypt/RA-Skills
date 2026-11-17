# Routing — Matching, Routers, and URL Surprises

Routes are matched in declaration order, first match wins. That single fact explains most "my endpoint is never called" reports.

## Order and Specificity

- `/users/me` declared after `/users/{user_id}` never runs: the parametrized route matches `me` and fails converting it to an int, returning 422 instead of your handler. Declare literal paths before parametrized ones.
- Two routes with the same path and method: the first registered wins, silently. Duplicate registration usually comes from including the same router twice with different prefixes.
- Path converters constrain the match: `/{file_path:path}` captures slashes, everything else stops at `/`. Use it for proxy-style routes, never for ids.
- Path parameter validation is a real 422 gate: `user_id: Annotated[int, Path(ge=1)]` rejects `0` and `-3` before your code runs.

## Trailing Slashes and the 307

Starlette's `redirect_slashes` (default on) answers `/items` with a 307 to `/items/` when only the slashed route exists, and vice versa.

- 307 preserves method and body, so POSTs survive — but every client pays two round trips, and some HTTP clients drop the `Authorization` header on redirect.
- Behind a proxy that terminates TLS without correct forwarded headers, the redirect `Location` comes back as `http://` and browsers block it as mixed content. Fix the proxy headers (`deployment.md`), not the route.
- Pick one convention (no trailing slash on collections is the common choice), and set `redirect_slashes=False` once the API is public so a wrong URL fails loudly instead of redirecting.

## Routers

```python
router = APIRouter(prefix="/v1/orders", tags=["orders"], dependencies=[Depends(auth)])
app.include_router(router)
```

- Prefixes must not end in `/`; FastAPI raises at startup if they do.
- `include_router` can add its own prefix, tags, dependencies, and responses on top of the router's — they compose, they do not replace.
- The same router can be included twice under different prefixes (API versioning by mount), but every route then has a duplicate `operation_id` unless you supply `generate_unique_id_function` (`openapi.md`).
- Router-level dependencies apply to every route in the router, health checks included — keep probes in their own router (`observability.md`).

## Parameters: Where Each Kind Comes From

| Declaration | Read from |
|---|---|
| Name appears in the path string | Path segment |
| Scalar type not in the path | Query string |
| Pydantic model, no annotation | JSON body |
| `Annotated[str, Header()]` | Header (underscores map to hyphens automatically) |
| `Annotated[str, Cookie()]` | Cookie |
| `Annotated[str, Form()]` | Form body (requires `python-multipart`) |
| `Annotated[UploadFile, File()]` | Multipart upload (`streaming.md`) |
| Two models in one signature | Body with one key per parameter name |

- One model plus scalars: the scalars become query parameters unless annotated `Body()`. `count: Annotated[int, Body()]` puts it in the body next to the model.
- `Annotated[list[str], Query()]` accepts repeated query parameters (`?tag=a&tag=b`); a bare `list[str]` is read as a body and fails.
- Booleans accept `true/false/1/0/on/off/yes/no` — a client sending `"False"` as a string gets `True` in some other frameworks and a correct `False` here, which is worth knowing when porting.

## Status Codes and Response Metadata

| Case | Declaration |
|---|---|
| Created a resource | `status_code=201` and a `Location` header or the resource body |
| Accepted for async processing | `status_code=202` plus a status URL (`background.md`) |
| Deleted, nothing to return | `status_code=204` and return `None` — a body with 204 is a protocol error |
| Conditional or cache-aware | Return `Response(status_code=304)` after comparing `If-None-Match` |
| Per-response header or cookie | Take `response: Response` as a parameter and mutate it; no need to build a Response object |
| Dynamic status | `Response(status_code=...)` returned directly, with `response_model=None` |

## Mounting and Sub-Applications

- `app.mount("/static", StaticFiles(directory="static"))` — mounts are matched before routes only for their prefix; a route at `/static/{name}` declared elsewhere becomes unreachable.
- Mounting a second FastAPI app gives it its own docs, exception handlers, and middleware; the parent's middleware still wraps it, the parent's exception handlers do not apply.
- Mounted apps need `root_path` awareness for correct docs URLs behind a proxy (`deployment.md`).
- A catch-all SPA route (`/{full_path:path}`) must be registered last, or it shadows the API.

## Versioning

- Path versioning (`/v1/...`) with one router per version is the low-drama default: both versions live in the same process, share dependencies, and can be deleted independently.
- Header versioning keeps URLs clean but makes caching, logs, and generated clients harder; choose it only when a gateway already routes on headers.
- Deprecate before deleting: `@router.get(..., deprecated=True)` marks it in the docs and generated clients while the route keeps working.

## Reverse URLs and Redirects

- `request.url_for("route_name", user_id=1)` builds a URL from the route's function name and honours `root_path` — hardcoded strings do not, and break the day the app moves behind a path prefix.
- `RedirectResponse(url, status_code=303)` after a form POST; 307 and 308 preserve the method, which is almost never what a browser form wants.
