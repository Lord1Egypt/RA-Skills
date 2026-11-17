# DRF — Serializers, ViewSets, Permissions, Pagination

Django REST Framework is a policy layer: defaults come from `REST_FRAMEWORK` in settings and are overridden per view. Most production incidents in a DRF codebase trace back to a default nobody set, or a serializer that quietly does per-row work.

## Settings Defaults That Decide Your Security

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_THROTTLE_RATES": {"anon": "60/min", "user": "1000/hour"},
}
```

- `DEFAULT_PERMISSION_CLASSES` is `AllowAny` out of the box. Every endpoint you forget to annotate is public. Set the project default to `IsAuthenticated` and open individual views deliberately.
- With no `DEFAULT_PAGINATION_CLASS`, a `ListAPIView` returns the entire table in one response. The first time that hurts is the day the table grows.
- `SessionAuthentication` enforces CSRF on unsafe methods; `TokenAuthentication` and JWT do not. A client that works with a token and 403s with a session cookie is hitting exactly this.
- Throttling is off unless rates are configured, and `AnonRateThrottle` keys on IP — behind a proxy that means one bucket for everyone unless the real client IP is resolved correctly.
- `DEFAULT_RENDERER_CLASSES` includes the browsable API by default. It is a debugging tool: keep it out of production settings, since it renders forms and executes queries for every relation.

## Serializers

- `fields` explicitly. `fields = "__all__"` publishes every future column, including the internal flag someone adds next quarter (SKILL.md Traps).
- Write protection is `read_only_fields` — a field you merely omit from validation but keep in `fields` is still writable if it is a model field.
- Ownership is set server-side: `serializer.save(user=self.request.user)` in `perform_create`. Accepting `user` from the payload is mass assignment with extra steps.
- Validation order mirrors forms: field `to_internal_value` → field validators → `validate_<field>` → `validate(self, attrs)` (cross-field) → `create`/`update`. `validate_<field>` must return the value.
- `is_valid(raise_exception=True)` produces a 400 with DRF's error shape; without it you must check the return value, and silently ignoring it writes nothing while returning 201.
- `SerializerMethodField` is the main N+1 factory: a method that touches `obj.related.all()` runs once per row. Prefetch it in `get_queryset()`, or annotate the value in the queryset and read the annotation.
- Nested writable serializers need an explicit `create()`/`update()` — the default raises. For read-nested/write-flat, use a nested serializer with `read_only=True` plus a `PrimaryKeyRelatedField(source=..., write_only=True)`.
- `PrimaryKeyRelatedField(queryset=...)` validates that the id exists, and its queryset is also the authorization boundary: unscoped, a user can attach their object to someone else's parent.
- `many=True` builds a `ListSerializer`; bulk create needs `ListSerializer.create` overridden. `to_representation` runs per object, so anything expensive there multiplies by page size.
- `depth = 1` on a `ModelSerializer` is a demo feature: it expands relations read-only, makes them unwritable, and hides the join cost.

## Views And ViewSets

| Need | Class |
|---|---|
| Full CRUD on a model | `ModelViewSet` + router |
| Read-only collection | `ReadOnlyModelViewSet` |
| One or two operations | `generics.ListCreateAPIView`, `RetrieveUpdateAPIView` |
| Non-CRUD action (send, approve, export) | `APIView`, or `@action` on a ViewSet |
| Anything shaped unlike CRUD | `APIView` — fighting the generic flow costs more than writing the handler |

- Define `get_queryset()`, not the `queryset` attribute, whenever the rows depend on the request. `queryset = Order.objects.filter(day=date.today())` binds the date at import; DRF re-evaluates with `.all()` but the filter arguments are already frozen.
- `get_queryset()` is the object-level permission layer. Scoping there protects list, retrieve, update and delete at once; `get_object()` then calls `check_object_permissions` on top.
- `perform_create/update/destroy` are where side effects belong, wrapped in `transaction.on_commit` (SKILL.md Core Rules 5).
- `@action(detail=True, methods=["post"])` adds a route to a ViewSet; it inherits the ViewSet's permissions unless you pass `permission_classes`.
- Routers generate URL names as `<basename>-list` / `<basename>-detail`; `basename` is required when the view has no `queryset` attribute.
- Setting `permission_classes` on a view **replaces** the defaults, it does not add to them. That is how an endpoint accidentally becomes public.

## Permissions And Authentication

- Two levels: `has_permission(request, view)` runs before the handler; `has_object_permission(request, view, obj)` runs only when `get_object()` is called — so a custom list endpoint that never calls it gets no object checks at all.
- `SAFE_METHODS` is the idiom for read-only-for-others permissions. Combine classes with `&`, `|`, `~`.
- Authentication answers "who"; permission answers "may they". A 401 means no credentials were recognized, a 403 means they were and it is not enough — returning the wrong one sends clients into a refresh loop.
- JWT is a dependency, not part of DRF. Its tradeoff is revocation: a stateless token stays valid until it expires, so keep access tokens short and put logout on the refresh token.
- CORS is not authentication and not part of DRF either; a browser preflight failing looks like an auth bug and is a middleware configuration.

## Pagination, Filtering, Versioning

- `PageNumberPagination` is simplest; `LimitOffsetPagination` suits clients that need arbitrary windows; `CursorPagination` is the one that stays correct and cheap on a large, changing table — it requires a stable `ordering` field.
- Every paginated response costs a `COUNT(*)` except cursor pagination. On a big table that count can exceed the page query.
- `django-filter` gives declarative query parameters; whichever mechanism you use, never pass request parameters straight into `filter(**request.query_params)` — lookup traversal lets a caller filter across relations you never meant to expose.
- Ordering from a query parameter must be validated against an allowlist, or a client sorts by a column with no index and turns a fast endpoint into a table scan.
- Versioning (`URLPathVersioning`, `AcceptHeaderVersioning`) is a settings choice; the decision of *when* to version and how to deprecate is API design (see Related Skills in SKILL.md).

## Errors And Testing

- DRF converts `ValidationError`, `PermissionDenied`, `NotFound` and friends into structured responses; anything else becomes a 500. A custom `EXCEPTION_HANDLER` is how you get one error shape across the whole API.
- Django's `ValidationError` and DRF's are different classes. Model-level validation raising Django's inside a serializer produces a 500 unless it is caught and re-raised as DRF's.
- Test with `APIClient` (`force_authenticate` skips real credentials) and assert on `response.data`, not the rendered bytes.
- Assert the query count on list endpoints (`assertNumQueries`) — it is the only regression test that catches a new `SerializerMethodField` adding N+1.
- Schema generation (`drf-spectacular` and similar) reads serializers and annotations; a view whose response is built by hand documents itself as `{}` unless annotated.
