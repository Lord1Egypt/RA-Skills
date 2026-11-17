# Reading records

## Choose the read

- One known object or published read, such as
  `candor transactions get TRANSACTION_ID --reason "Read the transaction in question"`, `candor recurring list --reason "Read the recurring bills and income"`,
  `candor goals list --reason "Read the saved goals"`, `candor budget status --period YYYY-MM --reason "Read this month's budget"`.
- Rows from a dataset with filters: `candor data query DATASET --reason "Read the rows the question needs"` with its
  filters. Check fields and filters first with `candor data schema DATASET --reason "Check the dataset's fields and filters"`.
- Several datasets together for local analysis:
  `candor data snapshot --datasets transactions,accounts --output snapshot.sqlite --reason "Build a local snapshot for analysis"`.
- Period comparisons: `candor changes list --reason "Compare this month with last month"`, which states both ranges and
  withholds totals when history is incomplete.
- An unfamiliar call: `candor catalog describe OPERATION_ID` returns its exact
  arguments.

## Pages and totals

- Every bounded read returns its rows, calculations, and pagination together
  under `data.page`. The calculations cover exactly the rows on that page.
- Continue only through the call in `next_actions`; replay it exactly. A
  cursor is bound to the filters that issued it.
- Before you state a total for a period, follow every continuation for it, or
  say the total covers only what you read.
- Keep raw pages out of your reply. As pages arrive, carry forward only
  counts, totals, and the few records you need next. If you can run code,
  save the pages and analyze them there.

## Coverage

- `financial_position.coverage` on the opening, and `candor coverage get --reason "Check which accounts and dates the records cover"`,
  say which accounts report, from when, and how fresh. Observed first and last
  transactions are not the coverage boundary.
- A missing record is uncertainty, not hidden spending, income, or a
  preference.
- When a connected bank's sync is old for the question, `candor sync refresh --reason "Refresh balances that are too old for the question"` asks for new
  data; connecting new ones happens on the web. An account kept by hand has
  nothing to refresh: it is current through its `records_through` date, and
  newer records come from the person's next statement or export.
- A partial result carries a warning and its scope. Keep that limit in the
  answer instead of treating omitted records as zero.

## Visuals

`candor visual overview --reason "Show the overview"`, `candor visual goals --reason "Show the person their goals"`,
`candor visual budget-status --period YYYY-MM --reason "Show this month's budget"`, `candor visual recurring --reason "Show upcoming bills"`,
`candor visual cashflow --reason "Show cash flow"`, `candor visual holdings --reason "Show investment holdings"`, and
`candor visual investments --reason "Show investments over time"` return a panel
as text context, structured data, and a View in Candor link. Hosts with MCP
Apps also draw it. Read the panel text before discussing it, pass the link
through, and never recalculate its values.

## Links

Use the `view_url` values Candor returns. A response URL opens the related
view; a record URL selects that record. Never build URLs from ids.
