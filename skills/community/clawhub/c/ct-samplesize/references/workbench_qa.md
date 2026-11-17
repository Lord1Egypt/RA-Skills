# Workbench QA Standard (Standard Inspection Process)

> Scope: the workbench page under `workbench/` — frontend `workbench.html` + backend `server.py` + contract layer `form_schema.py`.
> This is a **mandatory quality gate for the ct-samplesize skill**: any change to the workbench source must pass this suite before release.
> Chinese primary version: [workbench_qa_zh-CN.md](workbench_qa_zh-CN.md)
> Operational details of the suite: [../workbench/autotest/README.md](../workbench/autotest/README.md)

---

## 1. Purpose & Mandatory Gate

The workbench is a single-file app (`workbench.html`, ~2700 lines, inline CSS/JS) + backend `server.py` (stdlib `http.server`, REST + static) + contract layer `form_schema.py`. A drift in any one of the three surfaces as "page unclickable / wrong result / production runs a different build". Therefore this process covers **all five faces** — static contract, backend API, in-browser behavior, real user flow, layout/a11y — not just one.

**Mandatory gate (release gate) — run the full suite when ANY of these holds:**

1. Any edit to `workbench.html` / `server.py` / `form_schema.py` / `tokens.css` / `wb-list.css` / `wb-list.js`;
2. Before running `publish-kit/build_publish.py` or `install_genie.py` (i.e. before publishing the workbench bundle / going live);
3. After publishing, for the production regression pass (see §5).

**Gate criterion:** all 5 layers green (0 failed / 0 error). Any failing case = release blocked.

---

## 2. Five-Layer Architecture

| Layer | Name | Method | Independent of | Typical bugs caught |
|---|---|---|---|---|
| **L1** | Static contract | Pure-Python HTML parse (no browser/backend) | browser, backend | duplicate ids, event handlers pointing to undefined functions, missing i18n keys, hardcoded CJK, leftover `debugger`/`console`, unparseable JS, publish-bundle drift |
| **L2** | Backend API contract | spawn `server.py` subprocess + requests | browser | 5xx crashes, unguarded invalid input (should be 4xx), credential files downloadable over HTTP, session lifecycle, rate-limit bypass |
| **L3** | Frontend unit | call page JS directly inside Playwright | real interaction | zh/en dictionary mismatch, util functions throwing on malformed input, view/history state-machine errors |
| **L4** | End-to-end flow | real clicks via Playwright | — | compute broken, result rendered in wrong place, history not back-filled, missing modal validation, active view actually invisible |
| **L5** | Layout / responsive / a11y | three viewports (desktop/tablet/mobile) + computed style | — | horizontal overflow, mobile tap target <44px, button without accessible name, low contrast |

**Assertions are not shared across layers:** the same thing is tested once in the static layer and once in the browser layer (e.g. i18n coverage). Static checks "is it written in source"; browser checks "does it take effect at runtime" — each catches what the other misses.

Current size: **L1=16 · L2=43 · L3=20 · L4=18 · L5=13, total 110 cases**; full run ~70s.

---

## 3. How to Run

```bash
cd workbench/autotest

python run_all.py                # all 5 layers (~70s), emits report
python run_all.py --layer L1 L3  # only specified layers (fastest for dev iteration)
python run_all.py --keep-report  # keep this run's report directory

# single layer, with verbose traceback
python -m pytest tests/test_L2_api.py -q --tb=short
```

Outputs in `autotest/report/<timestamp>/`:

| File | Content |
|---|---|
| `summary.md` | human-readable overview (per-layer pass rate + failure list) |
| `failures.md` | full traceback of failing cases only |
| `junit_L*.xml` | machine-readable detail (CI integration) |

**Environment:** Anaconda Python (`C:\Tools\anaconda3\python.exe`, same as the rest of the skill); `pip install pytest playwright requests`; `playwright install chromium`. L2/L4 start the backend with `CTSS_COZE_MOCK=1` (validates param validation / response contract / frontend render — **does NOT validate real R numerics**; numeric correctness is owned by method-level tests like `tests/test_ct_samplesize.py`).

---

## 4. Regression Baseline (the 7 real bugs this suite guards)

These were found, fixed, and are **continuously guarded against regression**. Read before touching related code.

| # | Layer | Severity | Problem | Fix |
|---|---|---|---|---|
| 1 | L1/L3/L4 | **P0** | `#v-domain` missing a `</div>` — the "History" view and footer were nested inside the domain view; after switching to History the parent is `display:none`, so the page renders at 0×0 and is completely unusable (no error thrown, very hard to spot by eye) | add the closing tag, drop the leftover empty `<div class="sectip">` |
| 2 | L2 | **P0** | static root == skill root, so `/config/llm_key.py` and `/adapters/coze_token_embedded.py` were downloadable via any GET (obfuscation ≠ encryption; key and ciphertext in the same file) | static serving switched to "extension allowlist + directory blocklist + filename blocklist" (`_static_allowed()`) |
| 3 | L2 | **P1** | argparse on validation failure prints the full usage (~4KB) to stderr; in cloud containers stderr is often redirected to an unread pipe, buffer fills, request hangs forever, concurrency gate never releases (symptom: compute spinner never stops) | `build_namespace()` uses `redirect_stderr` into memory, returning only a one-line trimmed error |
| 4 | L2 | P1 | `survival`'s optional listed the CLI alias `hr`, but argparse's real param is `hazard_ratio`; the name is absent from params → frontend rendered an unlabeled empty control | `form_schema` filters optional against params when building catalog (same口径 as required) |
| 5 | L3 | P2 | after switching to EN, leftover CJK: domain title "全部方法" (written by JS, outside `localize()`), session dropdown "N 轮 / turn" (en dict `turn` wrongly filled with Chinese) | extract `refreshDomainTitle()` and replay in `setLang()`; `setLang()` adds `refreshSessions()`; fix en dict |
| 6 | L1 | P2 | `title="切换语言"`, `aria-label="关闭"` had no i18n coverage | add `data-i18n-title/aria` + bilingual keys |
| 7 | L5 | P2 | mobile primary CTA `#nlComputeBtn` was 40px tall (ID selector specificity beat responsive `.btn{44px}`); sidebar items 42px | add equal-specificity override inside the media query |

---

## 5. Known Limitations & Mandatory Safeguards

- **mock mode validates contract, not numerics:** L2/L4 use `CTSS_COZE_MOCK=1`. Real R numeric correctness is owned by `tests/test_ct_samplesize.py` etc.; this suite does not re-cover it.
- **🔴 Back up the appId claim marker before `build_publish.py`:** its PRUNE logic strips `publish/.wbapp_*.genie` and `publish/.workbuddy/applications.yaml`. Losing them makes a re-publish generate a suffixed new domain and you can never return to `https://ct-samplesize.app.workbuddy.host/`. (Authoritative copy lives in `publish-kit/`; restore from there and rebuild `applications.yaml`.)
- **Post-publish production regression:** after going live, walk the L4 main flow against the real `https://ct-samplesize.app.workbuddy.host/` (select method → fill params → compute → history → export) to confirm production runs exactly this build. In that environment L2's credential allowlist and rate-limit are at production thresholds; `test_rate_limit_actually_works` already validates the limiter with a `WG_STRICT` instance so the test exemption never hides a real regression.
- **Tests relax WebGuard rate-limit by default** (`WG_RELAXED`, test-process only); the limiter itself is verified via a separate `WG_STRICT` instance.
- **Backend subprocess stdout/stderr must be drained continuously:** `ServerHarness` drains to a bounded deque on a background thread, otherwise argparse's usage output blocks the request (see Bug #3).
- **Port probe must NOT use `SO_REUSEADDR`:** on Windows a listening socket with it can re-bind the same port, so the probe misjudges "occupied = free" and the new instance binds onto the old one's port — requests get eaten by the stale instance (symptom: assertions mysteriously all green). Fixed and commented in `_free_port()`.
- **Side-effect files auto-restore:** `sessions.json` / `bugreports.json` are backed up at fixture start and restored at teardown, so tests never pollute real session data.

---

## 6. Maintainer Notes

- Adding a test method: after registering it in `form_schema.py`'s catalog, L2's `param_factory` **automatically** generates valid-param cases from the schema — no manual test edit needed.
- Editing i18n: keep `zh` / `en` dictionaries in sync; L3's "dictionary key parity" case catches missing keys.
- Editing layout: after CSS changes, run L5 to confirm no horizontal overflow at 375px and primary CTA ≥44px.
- After changing the suite itself, run `run_all.py` to confirm all-green before committing; reports land in `autotest/report/`.
- This process does **not** enter the workbench publish bundle (the bundle is whitelist-built; `autotest/` is not in the whitelist). It ships only with the skill source (GitHub / ClawHub).
