# Views — URLs, View Classes, Middleware, Requests and Responses

A request passes through: URL resolution → middleware (in `MIDDLEWARE` order) → view → middleware again (reverse order) → response. Most "impossible" view bugs are a misread of that pipeline or of where class-based view attributes come from.

## URLs

- Path converters validate before the view runs: `<int:pk>` rejects `abc` with a 404 the view never sees. Custom converters (`register_converter`) move validation out of the view entirely.
- `re_path` still exists for patterns `path()` cannot express. Anchor them: an unanchored regex matches more URLs than you think.
- `app_name` in the app's `urls.py` plus `namespace` in `include()` gives `{% url "shop:order-detail" pk=1 %}`. `NoReverseMatch` is nearly always a missing namespace or an argument-count mismatch — the exception message lists the patterns it tried.
- `reverse_lazy` for module-level use (`success_url`, class attributes); `reverse` at call time. `reverse` at import time raises because the URLConf is not loaded yet.
- `APPEND_SLASH` (on by default with `CommonMiddleware`) answers a slash-less URL with a 301 when the slashed version resolves. Browsers drop the body on that redirect, so a POST silently becomes a GET with no data. Post to the exact URL.
- URL order matters: the first match wins, so a catch-all `<slug:slug>` above a literal `/new/` swallows it.

## Function Views vs Class-Based Views

- Function views: obvious control flow, no MRO to reason about, best when the logic is not one of the standard shapes.
- Generic CBVs (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`, `FormView`) pay off when your view *is* that shape. When you start overriding four hooks to fight the flow, a function view is shorter and clearer.
- Override points, in the order they run: `setup()` → `dispatch()` → `get()`/`post()` → `get_queryset()` → `get_object()` → `get_context_data()` → `form_valid()`/`form_invalid()` → `get_success_url()`.
- `self.request` exists from `setup()` onward — never in `__init__`, because Django instantiates the view per request through `as_view()`.
- Mutable class attributes are shared across requests. `queryset = Order.objects.filter(day=date.today())` freezes the date at import; `get_queryset()` re-evaluates per request. Any mutable default on a CBV is a cross-request leak.
- Mixin order is MRO order: the mixin that must run first goes leftmost (`class OrderView(LoginRequiredMixin, DetailView)`). Reversed, the access check never runs.
- `@login_required` on a class decorates the class object, not the handler. Use `LoginRequiredMixin`, or `@method_decorator(login_required, name="dispatch")`.

## The Request Object

- `request.POST` is populated only for `application/x-www-form-urlencoded` and `multipart/form-data`. A JSON body arrives in `request.body` — `json.loads(request.body)` — and `request.POST` will be an empty dict, not an error.
- `request.body` is consumed once. Reading it after accessing `request.POST` (or vice versa) raises `RawPostDataException` in some paths and returns `b""` in others. Read once, store the value.
- `request.FILES` is empty unless the form declares `enctype="multipart/form-data"`. Check the enctype before anything else when a file the user selected never arrives: nothing raises, the dict is simply empty.
- `request.GET`/`request.POST` are `QueryDict`s: immutable, and `d["k"]` returns the *last* value while `d.getlist("k")` returns all of them. Checkbox groups and multi-selects need `getlist`.
- `request.get_host()` honors `ALLOWED_HOSTS` and, if enabled, `X-Forwarded-Host`; `request.META["HTTP_HOST"]` does not — never trust the raw header for URL building or emails.
- `request.user` exists only with `AuthenticationMiddleware` installed and ordered after `SessionMiddleware`. Without it, `request.user` raises `AttributeError`, not "anonymous".

## Responses

- `HttpResponse` (body in memory), `JsonResponse` (`safe=False` to serialize a list), `StreamingHttpResponse` (an iterator; the response starts before the work finishes), `FileResponse` (streaming with the right headers, and it closes the file).
- `redirect()` returns 302; `redirect(..., permanent=True)` returns 301. Permanent redirects are cached by browsers essentially forever — never use one while a URL scheme is still in flux.
- Never redirect to a raw `next` parameter. Validate with `url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()})` or you have shipped an open redirect.
- `StreamingHttpResponse` bypasses middleware that needs a full body (`GZipMiddleware`, conditional GET) and does not play well with `ATOMIC_REQUESTS`: the transaction commits before the generator finishes producing rows.
- Large downloads should be served by the web server or object storage with a signed URL, not streamed through a worker that is then unavailable for other requests.
- Set caching explicitly with `@cache_control(...)` / `patch_cache_control`. A response with no cache headers is a decision made by a proxy you do not control.

## Middleware

```python
class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response          # called once at startup
    def __call__(self, request):
        # before the view, in MIDDLEWARE order
        response = self.get_response(request)
        # after the view, in REVERSE order
        return response
```

- Request phase runs top to bottom; response phase runs bottom to top. Anything that must see the final response (compression, security headers) goes near the top of the list, so it wraps everything below.
- Order dependencies that actually bite: `SessionMiddleware` before `AuthenticationMiddleware` before anything reading `request.user`; `CommonMiddleware` before your redirect logic; `GZipMiddleware` above the view but below security headers.
- Returning a response from the request phase short-circuits the rest of the chain *and* the view — the remaining middlewares' response phases still run.
- `process_exception` only fires for exceptions raised by the *view*, not by another middleware's request phase.
- Middleware runs on every single request, including static files in development and health checks. A database query there is a query on every request forever.
- A middleware that is not async-aware forces a thread hop around every async view.

## Errors

- `get_object_or_404(qs_or_model, **kwargs)` raises `Http404`, which the handler turns into a 404 page — catching `DoesNotExist` around it does nothing. `get_list_or_404` is the list form.
- Custom handlers are module-level names in the root URLConf: `handler404`, `handler500`, `handler403`, `handler400`. They only run with `DEBUG=False`, and `handler500` receives no context processors — keep that template trivial or it fails while reporting a failure.
- `raise PermissionDenied` → 403, `raise SuspiciousOperation` → 400, `raise Http404` → 404. Use them instead of returning bare `HttpResponse(status=...)`, so the project's handlers and logging apply uniformly.
- Unhandled exceptions with `DEBUG=False` go to the `django.request` logger. With no logging configured, that means an email to `ADMINS` and nothing else.

## Pagination

- `Paginator` runs a `COUNT(*)` for every page. On a large table that count can cost more than the page — cache it, or use keyset pagination (`filter(created_at__lt=cursor)`) when the data is append-mostly.
- `Paginator` over an unordered queryset warns and gives inconsistent pages; always `order_by` on a unique-enough key (add `pk` as a tiebreaker).
- Deep `OFFSET` degrades linearly: the database reads and discards every skipped row. Page 500 of a 50-per-page list reads 25 000 rows to return 50.

## Context Processors

- Every context processor runs on every rendered template response. A query inside one is a query on every page of the site — cache it, or move it into the views that need it.
- They only apply to templates rendered with a `RequestContext` (`render()`, `TemplateResponse`). A template rendered manually with `Template.render(Context(...))` gets none of them, which is why "the variable is missing in this one place".
