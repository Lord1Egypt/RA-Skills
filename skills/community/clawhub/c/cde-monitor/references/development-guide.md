# Development Guide

## Project snapshot

This repository queries live public drug-review data from the CDE website through Selenium-driven browser automation. It is intentionally split into a thin CLI layer, a single runtime client that knows the site behavior, and small normalization/result-model helpers.

Current supported command families:

- `breakthrough-announcements`
- `breakthrough-included-by-company`
- `breakthrough-included-by-drug`
- `priority-announcements`
- `priority-included-by-company`
- `priority-included-by-drug`
- `in-review-by-company`
- `in-review-by-drug`
- `review-status-by-acceptance-no`

Current public constraints:

- The implementation depends on the live CDE page structure and current network payload shape.
- `in-review-*` year selection is limited to `2016` through `2026`.
- `review-status-by-acceptance-no` also depends on the inferred year falling within `2016` through `2026`.
- Company and drug matching on the CDE page is strict; fuzzy matching is not implemented.

## Repository layout

### `scripts/cde_query.py`

CLI entrypoint.

Responsibilities:

- Defines the command surface with `argparse`.
- Performs lightweight input validation such as year bounds.
- Dispatches each command into `CDEClient`.
- Prints either raw JSON or the compact `--pretty` output.

When adding a new feature, this file is usually the first place to update if the feature needs a new CLI subcommand or arguments.

### `scripts/cde_client.py`

Core runtime implementation.

Responsibilities:

- Starts the Chrome driver.
- Navigates CDE menus and tabs.
- Applies text and select filters.
- Submits searches and captures JSON payloads from performance logs.
- Scrapes DOM tables when a page does not expose a stable JSON result path.
- Normalizes records and returns structured result objects.

This is the main extension point for new CDE capabilities.

### `scripts/models.py`

Result model definitions.

Current result types:

- `QueryTarget`: static definition of a generic page flow.
- `PageCapture`: wrapper around one captured JSON payload.
- `QueryRunResult`: standard list-result shape for most commands.
- `AcceptanceReviewResult`: specialized result shape for the two-step acceptance-number lookup.

If a new feature returns a materially different payload shape, add or extend a dedicated result model here.

### `scripts/normalizers.py`

Field normalization and deduplication.

Responsibilities:

- Maps raw CDE keys into a stable `normalized` object.
- Infers the year from the record date when needed.
- Generates dedupe fingerprints across merged pages and years.

Any new raw field that should be exposed consistently to the skill or CLI should be added here first.

### `tests/`

Unit tests use the standard library `unittest` framework.

Current testing split:

- `tests/test_cli.py`: parser and argument validation.
- `tests/test_cde_client.py`: query orchestration, pagination, acceptance-number lookup behavior.
- `tests/test_normalizers.py`: normalization and dedupe behavior.

### `SKILL.md`

Operator-facing skill contract.

Keep it aligned with the actual command surface, supported flows, failure handling, and response interpretation. When a feature is added or behavior changes, this file should be updated in the same change.

## Two implementation patterns

The codebase currently has two stable patterns for feature work.

### Pattern 1: Generic list-style query

Used by:

- breakthrough announcements and included lists
- priority announcements and included lists
- in-review lookups by company or drug

Flow:

1. Define a `QueryTarget` constant in `scripts/cde_client.py`.
2. Add a public `query_*` method on `CDEClient`.
3. Route the method through `_query_target()` or `_query_in_review()`.
4. Add a CLI subcommand in `scripts/cde_query.py`.
5. Extend tests and docs.

`_query_target()` already handles most of the repeated mechanics:

- open page
- click left and right tabs
- apply text and select filters
- submit search
- read JSON payloads from the browser network log
- paginate until exhausted or repeated
- normalize and dedupe records

If the new CDE page behaves like a list page with a stable payload, prefer this pattern.

### Pattern 2: Specialized orchestrated flow

Used by:

- `review-status-by-acceptance-no`

Flow:

1. Resolve prerequisite information first.
2. Build one or more search plans.
3. Run page-specific logic that may mix filters, DOM scraping, and pagination.
4. Return a dedicated result model instead of forcing the data into `records`.

This pattern is appropriate when the CDE workflow is multi-step or the result page is not served through the same network-payload pattern as the other list pages.

## Current interface inventory

### Public `CDEClient` methods

- `query_breakthrough_announcements()`
- `query_breakthrough_included_by_company(company)`
- `query_breakthrough_included_by_drug(drug)`
- `query_priority_announcements()`
- `query_priority_included_by_company(company)`
- `query_priority_included_by_drug(drug)`
- `query_in_review_by_company(company, years)`
- `query_in_review_by_drug(drug, years)`
- `query_review_status_by_acceptance_no(acceptance_no)`

These methods are the runtime API that the CLI consumes. If another integration layer is added later, it should usually call these methods rather than reimplementing page logic.

### Internal reusable helpers in `CDEClient`

Generic helpers:

- `_query_target()`
- `_build_driver()`
- `_open_listing_page()`
- `_click_left_tab()`
- `_click_right_tab()`
- `_fill_text_filter()`
- `_select_filter()`
- `_submit_search()`
- `_wait_for_payload()`
- `_extract_capture_from_log()`
- `_detect_total_pages()`
- `_go_to_page()`

Acceptance-number helpers:

- `infer_acceptance_year()`
- `_query_acceptance_basic_info()`
- `_query_review_status_for_basic_info()`
- `_build_review_search_plans()`
- `_run_review_status_attempt()`
- `_scrape_review_task_page()`
- `_normalize_review_task_row()`

When implementing a new feature, reuse these helpers before adding new site-specific code.

## How the current commands are implemented

### Breakthrough and priority commands

These are the simplest commands. They differ mainly by:

- left tab
- right tab
- whether a company or drug filter is applied

They all return `QueryRunResult` and use normalized list records.

### In-review by company or drug

These are still list-style queries, but they are special because they merge results across multiple years. The public methods delegate into `_query_in_review()`, which calls `_query_target()` once per year, then deduplicates the merged records.

This pattern is a good reference if you need to add another feature that must sweep multiple parameter values and merge the output.

### Review status by acceptance number

This is the current most complex feature.

Implementation summary:

1. Normalize the acceptance number.
2. Infer the year from digits 5 and 6.
3. Validate that the inferred year is currently queryable on the CDE page.
4. Query `受理品种信息 -> 在审品种目录浏览` to fetch the basic application record.
5. Derive review-task filters from `drug_type`, `application_type`, and the acceptance-number prefix.
6. Query `审评任务公示 -> 新报任务公示`.
7. If the page returns a warning for the strict acceptance-number filter, retry without that filter and scan the paginated table for the exact row.
8. Convert lamp icons into stable stage labels.

This flow is the reference implementation for any future feature that requires multiple dependent CDE pages.

## Site-specific assumptions worth preserving

- Left navigation is most reliable through `.etcd_nav_ul li`.
- Generic text and select filters are located through label text plus a set of preferred element ids.
- Generic list pages are consumed primarily through captured network payloads.
- The review-task page is consumed through DOM scraping because the UI behavior is different enough that direct payload reuse is less reliable.
- Review-task lamp icon mapping is part of the business output and should be treated as a maintained contract.

If a future feature breaks, verify whether the underlying issue is:

- a changed selector
- a changed network payload shape
- a changed tab layout
- a changed filter id or label

## Recommended workflow for adding a new feature

1. Confirm whether the target CDE page fits the generic list-query pattern or needs a specialized flow.
2. Inspect the live page with `--show-browser` and verify tabs, filter labels, ids, and result behavior.
3. Implement the runtime logic in `scripts/cde_client.py` first.
4. Add or update normalized fields in `scripts/normalizers.py` if new data needs to be exposed.
5. Add or update result models in `scripts/models.py` if the output shape is new.
6. Expose the command in `scripts/cde_query.py`.
7. Add unit tests in `tests/`.
8. Update `SKILL.md` and any relevant files in `references/`.
9. Run unit tests and at least one live smoke test for the new command.

## Testing and release notes

Primary verification command:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Typical release checks:

- `python scripts/cde_query.py --help`
- unit test suite
- one live query per supported query family
- rebuild `dist/package` and `dist/runtime-package`

Preferred packaging command:

```bash
python ./scripts/build_dist.py
```

This script clears Python cache artifacts before copying files into `dist` and excludes those artifacts from the generated zip files.

Current packaging convention:

- full package includes `SKILL.md`, `.clawhubignore`, `scripts`, `references`, and `tests`
- runtime package includes `SKILL.md`, `scripts`, and `references`

## Good starting points for the next feature

Choose the starting point by feature type:

- New list page with standard filters: copy the breakthrough or priority pattern.
- New multi-year list page: copy the `in-review` pattern.
- New dependent multi-step lookup: copy the acceptance-number review-status pattern.
- New output field on existing commands: start in `scripts/normalizers.py`, then adjust the caller and tests.
- New user-facing command only: start in `scripts/cde_query.py`, but only after the runtime method exists.

If the next feature is still inside the CDE public site, `scripts/cde_client.py` should remain the single place that knows the browser and page details.