# Failure Recovery

| Failure | Recovery |
|---|---|
| Search has weak recall | Reformulate the query, change engine, or search the official domain |
| Known page is blocked | Try Web Unlocker, then an official alternate page or cached public evidence |
| Structured scraper rejects input | Validate the URL, ID, locale, and required fields before retrying |
| Async task is still running | Continue bounded polling through `dataify-task-operations`; do not resubmit |
| Async monitoring times out | Preserve the task ID and resume later; timeout is not task failure |
| Task fails | Report the API error, correct safe input errors, and retry only when duplicate cost is controlled |
| Source conflicts with another | Preserve both dates and scopes, prefer newer primary evidence, and explain uncertainty |
| Evidence remains unavailable | Mark the claim unknown and reduce confidence |

Do not repeatedly submit paid collection tasks because status is slow or uncertain. Reuse the original task ID whenever the submission may have succeeded. Never hide missing coverage behind a confident summary.
