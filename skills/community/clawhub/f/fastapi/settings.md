# Settings and Secrets — One Typed Object, Loaded Once

Configuration read with `os.getenv` scattered through handlers fails at request time, in production, on the one code path nobody tested. A settings model fails at startup, in every environment, before traffic arrives.

Reference patterns only: every variable name below (`APP_DATABASE_URL`, `jwt_secret`) is a placeholder for the reader's own configuration; the skill reads no credentials of its own.

## The Pattern

```python
from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", env_nested_delimiter="__", extra="ignore"
    )
    environment: str = "local"
    database_url: str
    jwt_secret: SecretStr
    http_timeout_s: float = 5.0
    cors_origins: list[str] = Field(default_factory=list)

@lru_cache
def get_settings() -> Settings: return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]
```

- `BaseSettings` lives in the separate `pydantic-settings` package (pydantic >=2.0); importing it from `pydantic` is the first error of a v2 migration.
- `@lru_cache` makes it a per-process singleton that tests can reset with `get_settings.cache_clear()`.
- Injecting settings as a dependency instead of importing the instance keeps every module overridable in tests and free of import-time configuration.

## Precedence and Naming

Highest to lowest: init arguments → environment variables → `.env` file → secrets directory → field default. A value present in the process environment always beats `.env`, which is why a stale exported variable in a shell explains "the .env change did nothing".

- `env_prefix="APP_"` means the field `database_url` reads `APP_DATABASE_URL`. Field names are matched case-insensitively.
- Nested models read `APP_REDIS__HOST` with `env_nested_delimiter="__"`; without the delimiter the nested field is invisible and falls back to its default silently.
- `list` and `dict` fields parse the environment value as JSON: `APP_CORS_ORIGINS='["https://a.com","https://b.com"]'`. A comma-separated string fails validation unless you add a `field_validator(mode="before")` that splits it.
- `extra="ignore"` prevents unrelated environment variables from breaking startup; `extra="forbid"` catches typos in your own variables but breaks the moment the platform injects its own.

## Secrets

- Type every secret as `SecretStr`. Its repr is masked, so it stays out of tracebacks, log lines, and `/debug` style dumps; `.get_secret_value()` is the deliberate unwrap.
- Never a default for a secret: a `jwt_secret: SecretStr = SecretStr("dev")` ships to production the first time an environment variable is misspelled. Required-with-no-default turns that into a startup crash.
- Docker and Kubernetes secret files: `SettingsConfigDict(secrets_dir="/run/secrets")` reads one file per field name — no environment variable, so `docker inspect` and `/proc/<pid>/environ` stay clean.
- Rotation: read the secret through the settings object, never capture it in a module-level constant; then a rolling restart is the whole rotation procedure.
- Cloud secret managers belong in lifespan, not in the model: fetch once at startup, build the Settings instance with the fetched values, fail fast if the fetch fails.

## Per-Environment Configuration

- One class, values from the environment. Subclasses per environment (`ProdSettings`) drift and get imported in the wrong place; an `environment: Literal["local","ci","staging","prod"]` field plus conditionals in the few places that differ is enough.
- Validate combinations that must not coexist:

```python
@model_validator(mode="after")
def prod_is_locked_down(self):
    if self.environment == "prod" and (self.debug or "*" in self.cors_origins):
        raise ValueError("debug or wildcard CORS in prod")
    return self
```

This turns the worst production misconfiguration into a container that refuses to start — visible in the deploy, not in a breach report.

- Docs exposure is configuration too: `FastAPI(openapi_url=None)` when the environment is prod and the API is internal (`openapi.md`).

## Validation at Startup

- Startup should fail on: missing required settings, an unreachable database when the app cannot function without it, and a JWT key that does not parse. Everything else (optional cache, metrics exporter) degrades with a warning.
- A missing required variable raises a pydantic `ValidationError` listing every missing field at once — far better than discovering them one deploy at a time.
- Print the effective non-secret configuration once at startup (`settings.model_dump(exclude={"jwt_secret"})`). Half of production incidents are answered by that one log line.

## Twelve-Factor Edges Worth Keeping

- Configuration comes from the environment; the image is identical across environments. An image that bakes `staging` cannot be promoted.
- The connection string carries the driver: `postgresql+asyncpg://` for async SQLAlchemy, `postgresql+psycopg://` for sync. A URL copied from a dashboard is usually the sync form and produces a driver mismatch at first query (`database.md`).
- Feature flags with more than three consumers belong in a flag service, not in settings — settings changes require a restart, flags should not.
