# Python production pattern

Use `urllib` for dependency-free scripts or an explicit `httpx.Client`/`requests.Session` in applications. Set connect/read timeouts, decode as UTF-8, distinguish `HTTPError` from network timeout, and expose structured errors. Keep submission and polling functions separate so retries cannot accidentally repeat a Builder submission. Use `dataify-task-operations/scripts/dataify_client.py` as the maintained dependency-free example.
