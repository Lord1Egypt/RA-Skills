# Testing — Fast, Isolated, Honest

Django's test machinery is built around one trick: each test runs inside a transaction that is rolled back afterwards. Almost every confusing test behavior — data vanishing, `on_commit` never firing, a test that passes alone and fails in the suite — comes from that trick or from state that escapes it.

## Choosing The Base Class

| Class | Isolation | Cost | Use for |
|---|---|---|---|
| `SimpleTestCase` | No database access at all | Fastest | Pure functions, forms without a model, URL resolution |
| `TestCase` | Each test in a transaction, rolled back | Fast | Almost everything |
| `TransactionTestCase` | Real commits, tables truncated between tests | Slow | Code under test that commits, uses `select_for_update`, or spans threads/connections |
| `LiveServerTestCase` | A real server on a port | Slowest | Browser-driven end-to-end tests |

- `TestCase` never commits, so `transaction.on_commit` callbacks never run. Use `with self.captureOnCommitCallbacks(execute=True):` (Django >=3.2) to assert on them, or the test proves nothing about the task you queued.
- Code that tests transaction behavior itself — savepoints, `select_for_update`, a race between two connections — cannot be tested inside a transaction. That is what `TransactionTestCase` is for, and why it costs so much more.
- `TransactionTestCase` truncates tables and **resets sequences** afterwards, which is why tests that assert on primary key values pass in one class and fail in the other.

## Test Data

```python
class OrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = Customer.objects.create(name="A")   # once per class
    def setUp(self):
        self.client.force_login(self.user)                 # once per test
```

- `setUpTestData` runs once per class inside an outer transaction, so it is much cheaper than `setUp`. Django >=3.2 gives each test its own copy of those attributes, so in-place mutation no longer leaks — but mutating a *nested* object or a non-model attribute still can.
- Fixtures (`fixtures = ["orders.json"]`) reload on every test and rot silently as the schema changes. Factories (`factory_boy`) or plain helper functions are the maintainable choice; keep fixtures for reference data that genuinely never changes.
- Build only the objects the assertion needs. A test that creates fifteen rows to check one field will be rewritten by whoever changes the model next.
- `refresh_from_db()` after code under test mutates a row through a queryset `update()` — the in-memory object is stale, and the assertion is testing your local variable.

## Assertions Worth Knowing

- `assertNumQueries(n)` — the only regression test that catches an N+1 introduced by someone else's template or serializer change.
- `assertRedirects`, `assertContains(response, text, status_code=200)`, `assertTemplateUsed`, and `assertFormError(form, "field", "message")` — it takes the form object since Django >=4.1, not the response.
- `assertQuerySetEqual(qs, expected, transform=...)` compares ordered results; unordered comparisons need `ordered=False` or the test is flaky by construction.
- `assertRaisesMessage` over `assertRaises` — the type alone rarely proves the right thing failed.
- `django.core.mail.outbox` holds messages sent with the `locmem` backend, which the test runner selects automatically. Assert on `outbox[0].to` and the subject, not on the whole rendered body.
- `self.assertNumQueries` and `CaptureQueriesContext` also expose the SQL, which is how you assert that a specific index-friendly filter was actually applied.

## Settings And Isolation

- `@override_settings(...)` as a decorator or context manager; `self.settings(...)` inside a test; `modify_settings` for adding to a list such as `MIDDLEWARE`.
- It cannot reach a value your module read at import time. `from django.conf import settings` then `settings.X` inside the function is overridable; `X = settings.X` at module level is not.
- Some settings are consumed once at startup and are not overridable at all in a meaningful way: `INSTALLED_APPS` changes need `@modify_settings` plus care, and database settings need a different connection.
- Speed up hashing in tests: `@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])`. Password hashing is intentionally slow, and a suite creating hundreds of users pays for it.
- Force a synchronous, deterministic cache in tests (`LocMemCache` with a per-test `KEY_PREFIX`, or `DummyCache`) — a shared Redis makes tests order-dependent across the whole suite.
- External calls must be blocked, not merely mocked in the tests you remembered: a fixture that patches the HTTP client at the session level turns a forgotten call into a loud failure instead of a slow, flaky test.

## Speed

- `--parallel` runs test classes across processes with one database per process. It is usually the single biggest win, and it exposes tests that share state through files or an external cache.
- `--keepdb` reuses the test database between runs, skipping creation and migrations. Drop it after any schema change, or you debug a stale database.
- Running with migrations disabled (pytest-django's `--no-migrations`, or a similar hook) builds the schema directly from models: much faster, and it stops exercising the migration path — so CI must run the migration path at least once.
- `SimpleTestCase` for everything that does not need the database; `setUpTestData` over `setUp`; fewer objects per test. In that order.
- Profile the suite before optimizing it: `--durations` style output almost always shows a handful of tests owning most of the runtime.

## What To Test In A Django Project

- Do not test the framework. A test asserting that `CharField(max_length=10)` truncates is testing Django.
- Do test: the queryset methods that encode business rules, permission boundaries (an unauthorized user gets 403/404 on every route that matters), form and serializer validation including the failure messages, and the query count of the endpoints you care about.
- Do test the boundary of every side effect: that the task was queued with the right id, that the email went to the right address, that the webhook was not sent when the transaction rolled back.
- Migration tests are worth writing for data migrations with real logic: apply the previous state, run forwards, assert. The framework support is awkward enough that a rehearsal on a restored copy is often the better investment.
- Test the failure path of external calls (timeout, 500, malformed body) — that is the code that runs during an incident and the code nobody exercises manually.

## Pytest-Django

- `pytest.mark.django_db` gives a test database access, and by default wraps it in a transaction like `TestCase`; `transaction=True` gives `TransactionTestCase` semantics.
- Fixtures replace `setUpTestData`: session-scoped fixtures for reference data, function-scoped for anything mutated.
- `django_assert_num_queries` is the fixture equivalent of `assertNumQueries`.
- The choice between the two runners is a project convention, not a correctness question; whichever the codebase uses, use it consistently (`test_runner` in Configuration).
