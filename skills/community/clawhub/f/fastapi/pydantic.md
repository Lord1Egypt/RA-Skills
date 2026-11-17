# Pydantic Models — Validation, Serialization, and the v2 Break

FastAPI's request and response layer is pydantic: a 422 is a model rejecting a payload, and a serialization surprise is a model doing exactly what it was told. Debug both by reading the model, not the endpoint.

## Reading a 422

The error body lists one object per failure. `loc` is the path that failed and it is the whole diagnosis:

| `loc` | Meaning |
|---|---|
| `["body", "email"]` | Field missing or wrong type at the top level of the body |
| `["body", "items", 0, "qty"]` | Second-level failure: index 0 of `items` |
| `["body"]` alone | The body was not valid JSON, or the content type was not `application/json` |
| `["query", "page"]` | Query parameter, not body — a client sending it in the body |
| `["path", "user_id"]` | Path segment failed conversion (`abc` into an `int`) |

- `type` names the rule: `missing`, `int_parsing`, `string_too_short`, `value_error`. Show `type` and `loc` to the client, never the raw exception (`errors.md`).
- A field the client did send but that is still `missing` almost always means an alias: the model declares `user_id`, the client sends `userId`. Fix with `Field(alias="userId")` plus `model_config = ConfigDict(populate_by_name=True)` so both spellings work.

## v1 → v2 Rename Map

| v1 | v2 |
|---|---|
| `.dict()` / `.json()` | `.model_dump()` / `.model_dump_json()` |
| `parse_obj()` / `parse_raw()` | `model_validate()` / `model_validate_json()` |
| `@validator` / `@root_validator` | `@field_validator` / `@model_validator(mode="before" \| "after")` |
| `class Config:` | `model_config = ConfigDict(...)` |
| `orm_mode = True` | `from_attributes=True` |
| `allow_population_by_field_name` | `populate_by_name` |
| `Field(regex=...)` | `Field(pattern=...)` |
| `.copy()` / `.schema()` | `.model_copy()` / `.model_json_schema()` |
| `BaseSettings` in pydantic | `pydantic-settings` package (`settings.md`) |

Behavior changes that break code silently rather than loudly:

- `Optional[str]` no longer implies a default. In v1 it was optional-with-`None`; in v2 it is required-and-nullable. Write `str | None = None` when the client may omit it.
- Coercion is stricter: `"3"` still becomes `3` for an `int` in the default lax mode, but `3.5` into `int` now fails instead of truncating, and `1`/`0` into `bool` rules changed. Round-trip your fixtures before believing the upgrade is clean.
- Validators run in a different order relative to defaults; a `@model_validator(mode="after")` sees a fully constructed model, `mode="before"` sees the raw dict.
- Pydantic's own benchmarks put v2 several times faster than v1 (a wide, model-dependent range) because validation moved to Rust — the practical consequence is that validation stops being the bottleneck and serialization or the database takes its place (`performance.md`).

## Mutable Defaults: What Is Actually True

Pydantic deep-copies mutable defaults per instance, so `items: list[str] = []` does **not** share one list across requests the way a plain function default does. `default_factory` is for values that must be *computed* per instance:

```python
id: UUID = Field(default_factory=uuid4)
created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

A shared-state bug in a FastAPI app is nearly always a module-level object or a dependency returning a singleton, not a model default.

## Request Models

- One model per operation shape. `UserCreate` (password in, no id), `UserUpdate` (every field optional), `UserRead` (id and timestamps, no password) — reusing one model for all three is how passwords end up in responses and ids become client-settable.
- Reject unknown fields where the client is your own front end: `model_config = ConfigDict(extra="forbid")` turns a typo'd field into a 422 instead of a silently ignored value. Public APIs usually want the default `ignore` for forward compatibility.
- `Annotated` carries the constraint so the type stays reusable: `Username = Annotated[str, Field(min_length=3, max_length=32, pattern=r"^[a-z0-9_]+$")]`.
- Cross-field rules go in `@model_validator(mode="after")` — `end_date > start_date` cannot be expressed on either field alone.
- Raise `ValueError` inside a validator; FastAPI converts it into a 422 with the right `loc`. Raising `HTTPException` there produces a 500 in some paths because validation runs before the handler context you expect.

## Response Models

- Declare with the return annotation (`fastapi >=0.89`) or `response_model=`. When both exist, `response_model` wins.
- The response model *filters*: fields not declared are dropped, which is the mechanism that keeps `hashed_password` out of a response even when the ORM object has it. That filtering only happens if the model is declared — returning a raw dict with `response_model=None` ships whatever you built.
- `response_model_exclude_unset=True` omits fields the object never set (not fields that happen to be `None`), which is what PATCH-style responses want. `exclude_none=True` is the blunt version and hides legitimately null values.
- `from_attributes=True` lets the model read an ORM instance's attributes. Lazy relationships still load during that read, outside your session if it already closed (`database.md`).
- `FastAPIError: Invalid args for response field` means the declared type is not something pydantic can build a schema from — an ORM class, a bare `dict` subclass, a SQLAlchemy `Row`. Wrap it in a real model.

## Serialization Details That Bite

- `datetime` serializes to ISO 8601 with the offset only if the value is timezone-aware; naive datetimes ship without a zone and clients guess wrong. Store and return aware UTC.
- `Decimal` serializes to a JSON number by default and loses exactness in JavaScript clients past 2^53; declare the field as `Decimal` and add a serializer to string for money.
- `field_serializer` and `model_serializer` customize output without a second DTO layer.
- `SecretStr` prints as `**********` in logs and tracebacks and requires `.get_secret_value()` to read — free protection for tokens carried inside models.
- `computed_field` puts a derived property into the response schema; a plain `@property` is invisible to both serialization and OpenAPI.

## Model Reuse Without Duplication

```python
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: SecretStr

class UserRead(UserBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
```

Inheritance for shared fields, separate classes for separate contracts. Generics (`Page[UserRead]`) give one pagination envelope for every resource and one OpenAPI schema per instantiation.
