# Python

The `docspring` package (Python 3.10 or later). The examples use Flask for web routes; the same code works in
Django or FastAPI with their request and response objects. Replace `tpl_...` with the real template ID.

- [Set up](#set-up)
- [Generate the models and schema](#generate-the-models-and-schema)
- [The client module and error helper](#the-client-module-and-error-helper)
- [The job](#the-job)
- [Download](#download)
- [Webhooks](#webhooks)
- [Tests](#tests)

## Set up

```bash
pip install "docspring>=4.2,<5"
```

`Client()` reads `DOCSPRING_TOKEN_ID`, `DOCSPRING_TOKEN_SECRET`, `DOCSPRING_REGION` and `DOCSPRING_HOST`. Arguments
override them: `Client(api_token_id=..., api_token_secret=..., region="EU")`. Request bodies are dicts. Optional
arguments are keywords: `client.create_submission(template_id, body, version="1", wait=False)`. Responses are
pydantic models with the API's snake_case names (`submission.files.pdf.download_url`), and enum fields such as
`submission.state` compare equal to their strings.

## Generate the models and schema

`scripts/docspring_codegen.py`, run with `python scripts/docspring_codegen.py` (add `--check` in CI):

```python
import json
import pathlib
import sys

from docspring import Client

# Every template the app uses, at the version the app pins.
TEMPLATES = [{"name": "invoice", "type_name": "InvoiceData", "template_id": "tpl_...", "version": "1"}]
OUT_DIR = pathlib.Path("app/docspring/generated")


def main() -> int:
    client = Client()
    check = "--check" in sys.argv
    stale = False
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for t in TEMPLATES:
        header = (
            f"# Generated from DocSpring template {t['template_id']}, version {t['version']}.\n"
            "# Don't edit it: run scripts/docspring_codegen.py\n\n"
        )
        model = client.get_template_model_code(t["template_id"], "python", version=t["version"])
        schema = client.get_template_schema(t["template_id"], version=t["version"])
        files = {
            # The root class is named after the template; the alias keeps imports working if it's renamed.
            OUT_DIR / f"{t['name']}.py": f"{header}{model.code}\n\n{t['type_name']} = {model.root_type_name}\n",
            OUT_DIR / f"{t['name']}.schema.json": json.dumps(schema, indent=2) + "\n",
        }
        for path, content in files.items():
            if path.exists() and path.read_text() == content:
                continue
            stale = True
            if check:
                print(f"{path} doesn't match the template. Run scripts/docspring_codegen.py", file=sys.stderr)
            else:
                path.write_text(content)
    return 1 if check and stale else 0


if __name__ == "__main__":
    sys.exit(main())
```

The generated module has a dataclass for the data, with `to_dict()` (it leaves out optional fields that are `None`)
and `from_dict()`. Pass `to_dict()`'s result as `data`.

## The client module and error helper

`app/docspring/client.py`:

```python
import datetime
import json
import os
import random
import time

from docspring import ApiException, Client

client = Client()

# The app's own setting (DocSpring doesn't read it): test PDFs unless production sets DOCSPRING_TEST_MODE=false.
DOCSPRING_TEST_MODE = os.environ.get("DOCSPRING_TEST_MODE") != "false"


def docspring_error(e: Exception) -> dict | None:
    """The API's error ({"code", "message", "details", "request_id", ...}), with "status" and "retry_after"."""
    if not isinstance(e, ApiException):
        return None
    try:
        error = json.loads(e.body or "{}").get("error") or {}
    except ValueError:
        error = {}
    retry_after = e.headers.get("Retry-After") if e.headers else None
    return {**error, "status": e.status, "retry_after": float(retry_after) if retry_after else None}


def with_rate_limit_retry(call, attempts: int = 5):
    """A 429 never reached the API, so it's safe to send again, even for a create."""
    for attempt in range(1, attempts + 1):
        try:
            return call()
        except ApiException as e:
            error = docspring_error(e)
            if error["status"] != 429 or attempt == attempts:
                raise
            time.sleep((error["retry_after"] or 2**attempt) + random.random())


def find_submission(template_id: str, key: str, value, since: datetime.datetime):
    """The submission that a create made when it failed without returning an ID (a network error, a 5xx, a 504
    without one), found by your own metadata ID. Lists are newest first: this pages back to `since` (timezone-aware),
    a minute early. An invalid_data submission made no PDF, so it doesn't count."""
    cursor = None
    while True:
        page = client.list_submissions(
            template_id=template_id,
            test=DOCSPRING_TEST_MODE,
            created_after=since - datetime.timedelta(minutes=1),
            limit=100,
            cursor=cursor,
        )
        for submission in page.data:
            if (submission.metadata or {}).get(key) == value and submission.state != "invalid_data":
                return submission
        if not page.next_cursor:
            return None
        cursor = page.next_cursor
```

`e.body` is the raw JSON string for every status; `e.data` is only parsed for some. `docspring.RequestValidationError`
(a `ValueError`, raised before sending) is a bug in the request, so let it fail.

## The job

`app/docspring/invoices.py`, called from a background job (Celery, RQ or similar). The job framework's retry is what
waits for a pending or credit-blocked submission.

```python
from docspring import ApiException

from app.docspring.client import DOCSPRING_TEST_MODE, client, docspring_error, find_submission, with_rate_limit_retry
from app.docspring.generated.invoice import InvoiceData

INVOICE_TEMPLATE_ID = "tpl_..."
INVOICE_TEMPLATE_VERSION = "1"  # the version scripts/docspring_codegen.py uses


def invoice_data(order) -> InvoiceData:
    # Only the template's field names: an unknown key is a 422.
    return InvoiceData(
        invoice_number=order.number,
        customer_name=order.customer_name,
        issue_date=order.paid_at.date().isoformat(),  # YYYY-MM-DD
        total=order.total_cents / 100,
    )


def generate_invoice_pdf(order) -> None:
    submission = None
    if order.invoice_submission_id:
        # A retried job: never create a second submission.
        submission = client.get_submission(order.invoice_submission_id)
    elif order.invoice_requested_at:
        # An earlier attempt sent the request but got no ID back, so the submission may exist.
        submission = find_submission(INVOICE_TEMPLATE_ID, "order_id", order.id, order.invoice_requested_at)
        if submission:
            save_invoice_submission_id(order, submission.id)

    if submission is None:
        body = {
            "data": invoice_data(order).to_dict(),
            "test": DOCSPRING_TEST_MODE,
            "metadata": {"order_id": order.id, "pdf_filename": f"invoice-{order.number}"},
        }
        mark_invoice_requested(order)  # sets invoice_requested_at to now (UTC), before the request is sent
        try:
            submission = with_rate_limit_retry(
                lambda: client.create_submission(INVOICE_TEMPLATE_ID, body, version=INVOICE_TEMPLATE_VERSION)
            )
        except ApiException as e:
            error = docspring_error(e)
            # The submission exists: it waits for credits, or is still being made.
            if error.get("code") in ("insufficient_credits", "polling_timeout") and error.get("submission_id"):
                save_invoice_submission_id(order, error["submission_id"])
            if error.get("code") == "invalid_data":
                pointers = [detail.get("pointer") for detail in error.get("details", [])]
                raise PermanentJobError(f"Invoice data doesn't fit the template: {pointers}") from e
            raise
        save_invoice_submission_id(order, submission.id)

    if submission.state == "processed":
        return  # submission.files.pdf is ready
    if submission.state in ("pending", "insufficient_credits", "account_suspended"):
        raise RetryLater(f"Invoice PDF {submission.id} is {submission.state}")
    # invalid_data, error, syntax_error, image_download_failed, image_processing_failed, or a new state
    raise PermanentJobError(f"Invoice PDF {submission.id} failed: {submission.state} {submission.error_message or ''}")
```

`save_invoice_submission_id`, `mark_invoice_requested`, `RetryLater` and `PermanentJobError` stand for the app's own
persistence and its job framework's retry and "don't retry" errors.

## Download

```python
from flask import abort, redirect


@app.get("/orders/<order_id>/invoice.pdf")
@login_required
def invoice_pdf(order_id):
    order = find_order_for_user(order_id)
    if order is None or not order.invoice_submission_id:
        abort(404)
    submission = client.get_submission(order.invoice_submission_id)
    pdf = submission.files.pdf
    if submission.state != "processed" or pdf is None or not pdf.download_url:
        abort(409)
    return redirect(pdf.download_url)  # a fresh temporary link
```

To keep a copy in your own storage, `GET` `submission.files.pdf.download_url` (no auth) right after it's processed.

## Webhooks

Create it once, from a script the user runs (it prints the signing secret):

```python
webhook = client.create_webhook(
    {
        "name": "Invoice PDFs",
        "url": "https://example.com/webhooks/docspring",
        "event_types": ["submission.processed", "submission.failed"],
        "template_ids": [INVOICE_TEMPLATE_ID],
        "mode": "live",
    }
)
print(f"Set DOCSPRING_WEBHOOK_SECRET to {webhook.secret}")
```

The handler. `verify_webhook_signature` takes the raw body (`str` or `bytes`) before anything parses it (Django:
`request.body`):

```python
import json
import os

from docspring import verify_webhook_signature
from flask import abort, request


@app.post("/webhooks/docspring")
def docspring_webhook():
    raw_body = request.get_data()
    header = request.headers.get("X-DocSpring-Signature", "")
    if not verify_webhook_signature(raw_body, header, os.environ["DOCSPRING_WEBHOOK_SECRET"]):
        abort(400)
    event = json.loads(raw_body)  # version 4: {"id", "event_type", "created_at", "data": <the submission>}
    enqueue_once(event["id"], event)  # retries resend the same id: skip ids you've seen
    return "", 200  # within 30 seconds; the job does the work
```

## Tests

Check what your builder makes against the committed schema (`pip install jsonschema`). `jsonschema.validate` picks
the draft from the schema's `$schema` and ignores DocSpring's own `x-` keywords:

```python
import json
import pathlib

import jsonschema

from app.docspring.invoices import invoice_data

SCHEMA = json.loads(pathlib.Path("app/docspring/generated/invoice.schema.json").read_text())


def test_invoice_data_matches_the_template_schema():
    data = invoice_data(sample_order()).to_dict()
    jsonschema.validate(data, SCHEMA, format_checker=jsonschema.FormatChecker())
```

The contract test, with a test API token in CI:

```python
from app.docspring.client import client
from app.docspring.invoices import INVOICE_TEMPLATE_ID, INVOICE_TEMPLATE_VERSION, invoice_data


def test_docspring_accepts_our_invoice_data():
    result = client.validate_submission(
        INVOICE_TEMPLATE_ID,
        {"data": invoice_data(sample_order()).to_dict()},
        version=INVOICE_TEMPLATE_VERSION,
    )
    assert result.valid, [detail.pointer for detail in result.error.details]
```
