# HTML Responses — Jinja2, HTMX, Forms, and Static Files

FastAPI is a fine server-rendered stack: same routing, same dependencies, HTML instead of JSON. The differences that matter are escaping, form handling, and the fact that a browser is not a generated client.

## Rendering

```python
templates = Jinja2Templates(directory="templates")

@router.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, user: CurrentUser, db: DbSession):
    orders = await service.list_orders(db, user.id)
    return templates.TemplateResponse(request, "orders.html", {"orders": orders})
```

- `jinja2` must be installed; the `request` argument is required because the template context needs it for `url_for`.
- Newer FastAPI takes `request` as the first positional argument; the older signature (`"orders.html", {"request": request, ...}`) still works and is deprecated. Pick one form across the codebase.
- `response_class=HTMLResponse` in the decorator keeps the OpenAPI schema honest — otherwise the route documents a JSON response it never returns.
- Rendering a large template is CPU work on the event loop: templates rendering in single-digit milliseconds are fine, a 5,000-row table is not (`async.md`).
- Enable Jinja's bytecode cache or accept compile-on-first-use per worker; template compilation is per process, so the first request after every deploy pays for it.

## Escaping and XSS

- `Jinja2Templates` enables autoescaping for `.html` files. That protection ends the moment you write `{{ content | safe }}` or build markup with string concatenation.
- User-supplied HTML that must render (comments, rich text) gets sanitized with an allowlist library before it reaches the template — never with a regex.
- Escaping is context-sensitive: autoescape covers HTML text and attributes, not JavaScript. Passing data into a script tag needs `{{ data | tojson }}` inside the script, or a `data-` attribute the script reads.
- URLs from users in `href` still allow `javascript:`; validate the scheme.
- Pair this with a Content-Security-Policy so an escaping mistake is not automatically code execution (`security.md`).

## Forms

```python
@router.post("/login")
async def login(username: Annotated[str, Form()], password: Annotated[SecretStr, Form()]):
```

- Form parsing needs `python-multipart` installed, the same as uploads (`streaming.md`).
- Browsers send `application/x-www-form-urlencoded`, so a JSON-only endpoint cannot accept a plain HTML form; declare `Form()` fields or post with JavaScript.
- Validation failures return the framework's 422 JSON, which is useless to a browser. Catch `RequestValidationError` and re-render the form with errors for HTML routes, keyed on the route or an `Accept` header (`errors.md`).
- POST-redirect-GET after a successful form: `RedirectResponse(url, status_code=303)`. 307 and 308 preserve the method and make the browser re-POST on refresh.
- Cookie-based sessions plus forms means CSRF is live: `SameSite=Lax` covers most of it, and any cross-site or `SameSite=None` flow needs a real token (`auth.md`).

## HTMX and Partials

- Return HTML fragments, not JSON, from HTMX endpoints; one template per fragment, and full pages composed from the same fragments so both paths render identically.
- Branch on the `HX-Request` header to serve a fragment to HTMX and a full page to a direct navigation or a refresh: the same URL then works with and without JavaScript.
- Response headers drive the client: `HX-Redirect`, `HX-Trigger`, `HX-Retarget`. Setting them beats returning a JSON envelope the front end has to interpret.
- Errors need the same treatment: a 422 with a JSON body swaps nothing useful into the page — return the re-rendered fragment with error markup and a 200, or an error partial with the right status and `HX-Retarget`.
- Server-pushed updates for these apps are usually SSE, not WebSockets: it is plain HTTP, reconnects automatically, and fits the fragment model (`streaming.md`).

## Static Files

```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

- A mount claims its whole prefix: any route under `/static/...` declared elsewhere becomes unreachable (`routing.md`).
- In production a proxy or CDN should serve these; `StaticFiles` spends worker time on bytes and has no cache tuning worth the name (`performance.md`).
- Cache-bust with a content hash in the filename and a long `Cache-Control`; a query string works but some intermediaries ignore it.
- `html=True` turns the mount into an SPA-style server (serving `index.html` for unknown paths) — convenient, and it will swallow API 404s if mounted at `/`.

## Deciding Between HTML and JSON

| Situation | Serve |
|---|---|
| Internal tool, few developers, no mobile client | HTML with HTMX: no build step, no duplicate models |
| A mobile app or third-party integration exists or is planned | JSON API, HTML as a separate consumer |
| Both, from one codebase | Separate routers with separate response classes; share the service layer, never the template (`structure.md`) |
| Public marketing pages | A static site or CDN, not this process |
