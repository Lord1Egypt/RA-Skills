# TypeScript and JavaScript

The `docspring-ts` package (TypeScript) and the `docspring` package (plain JavaScript). Everything here is TypeScript;
[JavaScript](#javascript) lists what differs. Replace `tpl_...` with the real template ID.

- [Set up](#set-up)
- [Generate the types and schema](#generate-the-types-and-schema)
- [The client module and error helper](#the-client-module-and-error-helper)
- [The job](#the-job)
- [Download](#download)
- [Webhooks](#webhooks)
- [Tests](#tests)
- [JavaScript](#javascript)

## Set up

```bash
npm install "docspring-ts@^4.2"
```

`new DocSpring.Client()` reads `DOCSPRING_TOKEN_ID`, `DOCSPRING_TOKEN_SECRET`, `DOCSPRING_REGION` and
`DOCSPRING_HOST`. Passing options overrides them: `new DocSpring.Client({ apiTokenId, apiTokenSecret, region: "EU" })`.
Optional arguments are positional: `createSubmission(templateId, body, version?, wait?)`, so pass `undefined` to skip
one (`createSubmission(templateId, body, undefined, false)`). Every model property uses the API's snake_case name.

## Generate the types and schema

`scripts/docspring-codegen.ts`, run with `npx tsx scripts/docspring-codegen.ts` (add `--check` in CI):

```ts
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import * as DocSpring from 'docspring-ts'

// Every template the app uses, at the version the app pins.
const TEMPLATES = [
  {
    name: 'invoice',
    typeName: 'InvoiceData',
    templateId: 'tpl_...',
    version: '1',
  },
]
const OUT_DIR = 'src/docspring/generated'

const client = new DocSpring.Client()
const check = process.argv.includes('--check')
let stale = false

async function update(path: string, content: string) {
  const current = await readFile(path, 'utf8').catch(() => undefined)
  if (current === content) return
  stale = true
  if (check)
    console.error(
      `${path} doesn't match the template. Run scripts/docspring-codegen.ts`
    )
  else await writeFile(path, content)
}

async function main() {
  await mkdir(OUT_DIR, { recursive: true })
  for (const t of TEMPLATES) {
    const header =
      `// Generated from DocSpring template ${t.templateId}, version ${t.version}.\n` +
      `// Don't edit it: run scripts/docspring-codegen.ts\n\n`
    const model = await client.getTemplateModelCode(
      t.templateId,
      DocSpring.ModelCodeLanguage.Typescript,
      t.version
    )
    // The root type is named after the template; the alias keeps imports working if the template is renamed.
    await update(
      `${OUT_DIR}/${t.name}.ts`,
      `${header}${model.code}\n\nexport type ${t.typeName} = ${model.root_type_name};\n`
    )
    const schema = await client.getTemplateSchema(t.templateId, t.version)
    await update(
      `${OUT_DIR}/${t.name}.schema.json`,
      `${JSON.stringify(schema, null, 2)}\n`
    )
  }
  if (check && stale) process.exit(1)
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
```

The generated file exports the interface and a `Convert` class that checks JSON at runtime. You only need the
interface: `data` takes it as it is.

## The client module and error helper

`src/docspring/client.ts`:

```ts
import * as DocSpring from 'docspring-ts'

export const docspring = new DocSpring.Client()

// The app's own setting (DocSpring doesn't read it): test PDFs unless production sets DOCSPRING_TEST_MODE=false.
export const DOCSPRING_TEST_MODE = process.env.DOCSPRING_TEST_MODE !== 'false'

// The submission that a create made when it failed without returning an ID (a network error, a 5xx, a 504 without
// one), found by your own metadata ID. Lists are newest first: this pages back to `since`, a minute early. An
// invalid_data submission made no PDF, so it doesn't count.
export async function findSubmission(
  templateId: string,
  key: string,
  value: unknown,
  since: Date
) {
  let cursor: string | undefined
  do {
    const after = new Date(since.getTime() - 60_000)
    const page = await docspring.listSubmissions(
      templateId,
      DOCSPRING_TEST_MODE,
      after,
      undefined,
      undefined,
      100,
      cursor
    )
    const found = page.data.find(
      (s) => s.metadata?.[key] === value && s.state !== 'invalid_data'
    )
    if (found) return found
    cursor = page.next_cursor ?? undefined
  } while (cursor)
  return undefined
}

export type DocSpringError = Partial<DocSpring.ErrorInfo> & {
  status: number
  retryAfterSeconds?: number
}

// The API's error from a failed call. e.body is parsed for the statuses a method documents, and a JSON string for
// the others (429, 504, 5xx).
export function docspringError(e: unknown): DocSpringError | undefined {
  if (!(e instanceof DocSpring.ApiException)) return undefined
  let body: any = e.body
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body)
    } catch {
      body = undefined
    }
  }
  const retryAfter = e.headers?.['retry-after']
    ? Number(e.headers['retry-after'])
    : NaN
  return {
    ...body?.error,
    status: e.code,
    retryAfterSeconds: Number.isFinite(retryAfter) ? retryAfter : undefined,
  }
}

// A 429 never reached the API, so it's safe to send again, even for a create.
export async function withRateLimitRetry<T>(
  call: () => Promise<T>,
  attempts = 5
): Promise<T> {
  for (let attempt = 1; ; attempt++) {
    try {
      return await call()
    } catch (e) {
      const error = docspringError(e)
      if (error?.status !== 429 || attempt >= attempts) throw e
      const seconds = error.retryAfterSeconds ?? 2 ** attempt
      await new Promise((resolve) =>
        setTimeout(resolve, seconds * 1000 + Math.random() * 1000)
      )
    }
  }
}
```

`DocSpring.ValidationError` (the client's own check of the request, before sending) isn't an `ApiException`: it's a
bug in the request, so let it fail.

## The job

`src/docspring/invoices.ts`, called from a background job. The job framework's retry is what waits for a pending or
credit-blocked submission.

```ts
import * as DocSpring from 'docspring-ts'
import {
  docspring,
  docspringError,
  findSubmission,
  DOCSPRING_TEST_MODE,
  withRateLimitRetry,
} from './client'
import type { InvoiceData } from './generated/invoice'

export const INVOICE_TEMPLATE_ID = 'tpl_...'
export const INVOICE_TEMPLATE_VERSION = '1' // the version scripts/docspring-codegen.ts uses

// Only the template's field names: an unknown key is a 422.
export function invoiceData(order: Order): InvoiceData {
  return {
    invoice_number: order.number,
    customer_name: order.customerName,
    issue_date: order.paidAt.toISOString().slice(0, 10), // YYYY-MM-DD
    total: order.totalCents / 100,
  }
}

export async function generateInvoicePdf(order: Order): Promise<void> {
  let submission: DocSpring.Submission | undefined
  if (order.invoiceSubmissionId) {
    // A retried job: never create a second submission.
    submission = await docspring.getSubmission(order.invoiceSubmissionId)
  } else if (order.invoiceRequestedAt) {
    // An earlier attempt sent the request but got no ID back, so the submission may exist.
    submission = await findSubmission(
      INVOICE_TEMPLATE_ID,
      'order_id',
      order.id,
      order.invoiceRequestedAt
    )
    if (submission) await saveInvoiceSubmissionId(order.id, submission.id)
  }

  if (!submission) {
    const body: DocSpring.CreateSubmissionRequest = {
      data: invoiceData(order),
      test: DOCSPRING_TEST_MODE,
      metadata: { order_id: order.id, pdf_filename: `invoice-${order.number}` },
    }
    await markInvoiceRequested(order.id) // sets invoiceRequestedAt to now, before the request is sent
    try {
      submission = await withRateLimitRetry(() =>
        docspring.createSubmission(
          INVOICE_TEMPLATE_ID,
          body,
          INVOICE_TEMPLATE_VERSION
        )
      )
    } catch (e) {
      const error = docspringError(e)
      // The submission exists: it waits for credits, or is still being made.
      if (
        (error?.code === 'insufficient_credits' ||
          error?.code === 'polling_timeout') &&
        error.submission_id
      ) {
        await saveInvoiceSubmissionId(order.id, error.submission_id)
      }
      if (error?.code === 'invalid_data') {
        throw new PermanentJobError(
          `Invoice data doesn't fit the template: ${error.details?.map((d) => d.pointer)}`
        )
      }
      throw e
    }
    await saveInvoiceSubmissionId(order.id, submission.id)
  }

  switch (submission.state) {
    case 'processed':
      return // submission.files.pdf is ready
    case 'pending':
    case 'insufficient_credits':
    case 'account_suspended':
      throw new Error(
        `Invoice PDF ${submission.id} is ${submission.state}: try again later`
      )
    default:
      // invalid_data, error, syntax_error, image_download_failed, image_processing_failed, or a new state
      throw new PermanentJobError(
        `Invoice PDF ${submission.id} failed: ${submission.state} ${submission.error_message ?? ''}`
      )
  }
}
```

`saveInvoiceSubmissionId`, `markInvoiceRequested` and `PermanentJobError` stand for the app's own persistence and its
job framework's "don't retry" error.

## Download

```ts
// Redirect a signed-in user to a fresh temporary link.
app.get('/orders/:id/invoice.pdf', requireUser, async (req, res) => {
  const order = await findOrderForUser(req)
  if (!order?.invoiceSubmissionId) return res.sendStatus(404)
  const submission = await docspring.getSubmission(order.invoiceSubmissionId)
  const url = submission.files.pdf?.download_url
  if (submission.state !== 'processed' || !url) return res.sendStatus(409)
  res.redirect(url)
})

// Or keep a copy in your own storage, right after it's processed.
const response = await fetch(submission.files.pdf!.download_url!)
if (!response.ok)
  throw new Error(
    `Downloading ${submission.id}'s PDF failed: ${response.status}`
  )
const pdf = Buffer.from(await response.arrayBuffer())
```

## Webhooks

Create it once, from a script the user runs (it prints the signing secret):

```ts
const webhook = await docspring.createWebhook({
  name: 'Invoice PDFs',
  url: 'https://example.com/webhooks/docspring',
  event_types: ['submission.processed', 'submission.failed'],
  template_ids: [INVOICE_TEMPLATE_ID],
  mode: 'live',
})
console.log(`Set DOCSPRING_WEBHOOK_SECRET to ${webhook.secret}`)
```

The handler (Express). `express.raw` keeps the body as the bytes DocSpring signed:

```ts
import express from 'express'
import * as DocSpring from 'docspring-ts'

// A version 4 event: data is the submission as getSubmission returns it.
type DocSpringEvent = {
  id: string
  event_type: string
  created_at: string
  data: DocSpring.Submission
}

app.post(
  '/webhooks/docspring',
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    if (
      !DocSpring.verifyWebhookSignature(
        req.body, // the Buffer from express.raw
        req.get('X-DocSpring-Signature'),
        process.env.DOCSPRING_WEBHOOK_SECRET!
      )
    ) {
      return res.sendStatus(400)
    }
    const event: DocSpringEvent = JSON.parse(req.body.toString('utf8'))
    await enqueueOnce(event.id, event) // retries resend the same id: skip ids you've seen
    res.sendStatus(200) // within 30 seconds; the job does the work
  }
)
```

Mount the route before any `express.json()` middleware, or the raw body is gone. In Next.js route handlers, read
`await request.text()` before anything parses it.

## Tests

Check what your builder makes against the committed schema (`npm install -D ajv ajv-formats`):

```ts
import Ajv from 'ajv'
import addFormats from 'ajv-formats'
import schema from '../src/docspring/generated/invoice.schema.json'
import { invoiceData } from '../src/docspring/invoices'

// DocSpring's schemas have their own x- keywords, which Ajv's strict mode rejects.
const ajv = new Ajv({ strict: false, allErrors: true })
addFormats(ajv)
const validateInvoice = ajv.compile(schema)

test("invoice data matches the DocSpring template's schema", () => {
  const valid = validateInvoice(invoiceData(sampleOrder()))
  expect(valid ? [] : validateInvoice.errors).toEqual([])
})
```

If the schema's `$schema` is draft-04, use `import Ajv from "ajv-draft-04"` instead.

The contract test, with a test API token in CI:

```ts
import { docspring } from '../src/docspring/client'
import {
  INVOICE_TEMPLATE_ID,
  INVOICE_TEMPLATE_VERSION,
  invoiceData,
} from '../src/docspring/invoices'

test('DocSpring accepts our invoice data', async () => {
  const result = await docspring.validateSubmission(
    INVOICE_TEMPLATE_ID,
    { data: invoiceData(sampleOrder()) },
    INVOICE_TEMPLATE_VERSION
  )
  expect(result.error?.details ?? []).toEqual([])
  expect(result.valid).toBe(true)
})
```

## JavaScript

- `npm install "docspring@^4.2"`, then `const DocSpring = require("docspring"); const docspring = new DocSpring.Client();`
- Optional arguments go in an options object: `createSubmission(templateId, body, { version: "1", wait: false })`,
  `getTemplateSchema(templateId, { version: "1" })`, `getTemplateModelCode(templateId, "javascript", { version: "1" })`,
  `validateSubmission(templateId, body, { version: "1" })`.
- A failed call rejects with a plain object, not an `Error`: `err.status`, `err.body` (the parsed error body) and
  `err.response.headers["retry-after"]`. The client's own request check rejects with `DocSpring.ValidationError`.
- The `javascript` model code is quicktype's runtime converters (`Convert.to<Name>(json)`), with no types. The schema
  test above does the same check, so the schema file is enough.
