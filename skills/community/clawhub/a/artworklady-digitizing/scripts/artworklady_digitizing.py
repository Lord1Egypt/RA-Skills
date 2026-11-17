#!/usr/bin/env python3
"""Artwork Lady — Embroidery Digitizing intake driver (Playwright).

Art work Lady (https://www.artworklady.com) takes digitizing jobs through a
web *intake form* on its ``/placeorder`` page — there is no API. This helper
drives that form with Playwright: it logs in, opens the **Embroidery
Digitizing** tab, fills every field, attaches the files, and (only when told
to) clicks **Send** and confirms the job posted.

It is a thin *portal adapter*. It knows nothing about Odoo: give it a job
reference, the field values, and 1–3 local file paths, and it returns a
structured result. The calling routine owns polling ``digitize.demand``,
downloading the attachments to disk, and updating the record on success.

Actions
-------
  capture   Read-only diagnostic: log in, open the Embroidery tab, dump the
            live field map + a screenshot. Nothing is submitted.
  submit    Fill the Embroidery form. DRY RUN by default (fills + validates,
            stops before Send). Pass ``"confirm": true`` to actually post.

Both read one JSON object from argv[1] (or stdin) and print one JSON object,
or ``{"error": {...}}`` with a non-zero exit.

Credentials come from ``ARTWORKLADY_USERNAME`` / ``ARTWORKLADY_PASSWORD``
(never pass them in chat); they may also be given inline as ``username`` /
``password`` in the JSON. See SKILL.md for the full env-var list.

The selectors and the submit mechanism were reverse-engineered from the live
portal; see ``references/placeorder_flow_notes.md``.
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any

BASE_URL_DEFAULT = "https://www.artworklady.com"
SUBMIT_ENDPOINT_SUFFIX = "/placeorder/order_form_submit"
THANKS_SUFFIX = "/placeorder/thanks"

VALID_TURNAROUND = {"sameday", "nextday", "rushorder"}
# The file-type checkboxes unique to the Embroidery Digitizing tab.
VALID_FILE_TYPES = {"dst", "emb", "exp", "other"}
VALID_COLOR_SCHEMES = {"CMYK", "RGB"}
VALID_LOGIN_TYPES = {"employee", "company"}


class ConfigError(Exception):
    """Missing/invalid configuration — the agent's cue to fix inputs/env."""


class PortalError(Exception):
    """The portal did something we could not complete (login, submit, …)."""


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def _env(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    return v if (v is not None and v != "") else default


def _truthy(v: Any) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "on"}


def resolve_credentials(params: dict) -> tuple[str, str]:
    username = (params.get("username") or _env("ARTWORKLADY_USERNAME") or "").strip()
    password = params.get("password") or _env("ARTWORKLADY_PASSWORD") or ""
    if not username or not password:
        raise ConfigError(
            "Artwork Lady portal credentials were not provided. Set "
            "ARTWORKLADY_USERNAME and ARTWORKLADY_PASSWORD in the environment "
            "(they are the agent's bound portal login; never paste them into "
            "chat), or pass username/password inline in the JSON."
        )
    return username, password


# ---------------------------------------------------------------------------
# Browser
# ---------------------------------------------------------------------------


def _launch(pw, headless: bool):
    """Launch Chromium, wiring the agent proxy + CA pins when the environment
    provides them (both optional — a plain network needs neither)."""
    args = ["--disable-blink-features=AutomationControlled", "--no-sandbox"]
    # Only pin extra CAs when explicitly configured (e.g. a TLS-terminating
    # egress proxy). Never a blanket --ignore-certificate-errors.
    pins = _env("ARTWORKLADY_TLS_SPKI_PINS")
    if pins:
        args.append("--ignore-certificate-errors-spki-list=" + pins)

    launch_kwargs: dict[str, Any] = {"headless": headless, "args": args}
    proxy = _env("ARTWORKLADY_PROXY") or _env("HTTPS_PROXY") or _env("https_proxy")
    if proxy:
        launch_kwargs["proxy"] = {"server": proxy}
    return pw.chromium.launch(**launch_kwargs)


class Driver:
    def __init__(self, page, base_url: str, timeout_ms: int, trace: list) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.timeout_ms = timeout_ms
        self.trace = trace
        self._t0 = time.time()

    def _mark(self, step: str, **extra: Any) -> None:
        self.trace.append({"step": step, "ms": int((time.time() - self._t0) * 1000), **extra})

    # -- auth -------------------------------------------------------------

    def login(self, username: str, password: str, login_type: str) -> None:
        p = self.page
        p.goto(self.base_url + "/", wait_until="domcontentloaded", timeout=45000)
        # Home is a hydrating marketing page; wait on the concrete trigger,
        # never networkidle.
        p.wait_for_selector("button.ip2026-get-started", timeout=self.timeout_ms)
        self._mark("home-loaded", url=p.url)

        # 1) Open the Register/Login popup.
        p.click("button.ip2026-get-started")
        # 2) Switch it to the sign-in form ("already have an account").
        try:
            p.click("span[onclick=\"switchForm('login')\"]", timeout=self.timeout_ms)
        except Exception:
            p.evaluate("() => { try { switchForm('login'); } catch (e) {} }")
        p.wait_for_selector('#popupLoginForm input[name="email"]', state="visible", timeout=self.timeout_ms)
        self._mark("login-form-visible")

        # 3) Employee (default) vs Company login toggle.
        if login_type == "company":
            p.click("#popup-company-login-btn")
        else:
            # ensure the default is selected even if a prior state lingered
            p.click("#popup-employee-login-btn")
        got = p.locator("#popup_login_type").input_value()
        if got != login_type:
            # not fatal, but record it — the hidden field is what gets posted
            self._mark("login-type-mismatch", requested=login_type, actual=got)

        # 4) Credentials + submit.
        form = p.locator("#popupLoginForm")
        form.locator('input[name="email"]').fill(username)
        form.locator('input[name="password"]').fill(password)
        self._mark("credentials-filled", login_type=got)

        try:
            with p.expect_navigation(timeout=self.timeout_ms):
                form.locator('button[type="submit"]').click()
        except Exception:
            # Some flows update in place; fall through to the URL/error check.
            pass
        p.wait_for_timeout(1500)

        if not p.url.rstrip("/").endswith("/placeorder"):
            msg = ""
            try:
                msg = (p.locator("#popupLoginMessage").text_content() or "").strip()
            except Exception:
                pass
            raise PortalError(
                "Login did not reach /placeorder (landed on "
                f"{p.url!r}). Check ARTWORKLADY_USERNAME / ARTWORKLADY_PASSWORD"
                + (f" and login_type={login_type!r}." if login_type != "employee" else ".")
                + (f" Portal said: {msg!r}" if msg else "")
            )
        self._mark("logged-in", url=p.url)

    def goto_placeorder(self) -> None:
        if not self.page.url.rstrip("/").endswith("/placeorder"):
            self.page.goto(self.base_url + "/placeorder", wait_until="domcontentloaded", timeout=45000)
        self.page.wait_for_selector("#contactform", timeout=self.timeout_ms)

    # -- embroidery tab ---------------------------------------------------

    def open_embroidery(self) -> None:
        p = self.page
        p.click("button[onclick=\"change_form('embroidery')\"]")
        # change_form sets #form_type=1 and unhides the digitizing section.
        p.wait_for_function("() => document.getElementById('form_type') && document.getElementById('form_type').value === '1'", timeout=self.timeout_ms)
        p.wait_for_selector("#file1", state="visible", timeout=self.timeout_ms)
        self._mark("embroidery-tab-open")

    # -- field map (for capture) -----------------------------------------

    def field_map(self) -> dict:
        return self.page.evaluate(
            """() => {
              const vis = el => { if(!el) return false; const r=el.getBoundingClientRect(); const s=getComputedStyle(el); return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden'; };
              const cs = document.querySelector('#contactform select.color_scheme');
              return {
                form_type: (document.getElementById('form_type')||{}).value,
                jobref: !!document.getElementById('jobref'),
                turnaround: [...document.querySelectorAll('#contactform input[name=\\"radio\\"]')].map(r=>({value:r.value, checked:r.checked, visible:vis(r)})),
                file_types: [...document.querySelectorAll('#contactform input[name=\\"fileType\\"]')].filter(vis).map(c=>c.value),
                color_scheme: cs ? {id: cs.id, options:[...cs.options].map(o=>o.value)} : null,
                files: ['file1','file2','file3'].map(id=>({id, visible: vis(document.getElementById(id))})),
                message: !!document.getElementById('msg'),
                proof_template: !!document.getElementById('proof_template'),
                send: !!document.querySelector('#contactform input[name=\\"submit\\"]'),
              };
            }"""
        )

    # -- fill -------------------------------------------------------------

    def fill(self, params: dict) -> dict:
        p = self.page
        job_reference = str(params.get("job_reference") or "").strip()
        if not job_reference:
            raise ConfigError("job_reference is required (defaults to the decoration id).")

        turnaround = str(params.get("turnaround") or "").strip().lower()
        if turnaround not in VALID_TURNAROUND:
            raise ConfigError(
                "turnaround is required (the caller supplies it per demand) and "
                f"must be one of {sorted(VALID_TURNAROUND)}; got {turnaround!r}."
            )

        file_types = params.get("file_types") or ["dst"]
        if isinstance(file_types, str):
            file_types = [file_types]
        file_types = [str(x).strip().lower() for x in file_types]
        bad = [x for x in file_types if x not in VALID_FILE_TYPES]
        if bad or not file_types:
            raise ConfigError(f"file_types must be a non-empty subset of {sorted(VALID_FILE_TYPES)}; got {file_types!r}.")

        color_scheme = str(params.get("color_scheme") or "CMYK").strip().upper()
        if color_scheme not in VALID_COLOR_SCHEMES:
            raise ConfigError(f"color_scheme must be one of {sorted(VALID_COLOR_SCHEMES)}; got {color_scheme!r}.")

        files = params.get("files") or []
        if isinstance(files, str):
            files = [files]
        files = [str(f) for f in files]
        if not files:
            raise ConfigError("at least one file is required (the first fills the mandatory 'Upload File Here').")
        if len(files) > 3:
            raise ConfigError("the form accepts at most 3 files (file1/file2/file3).")
        missing = [f for f in files if not os.path.isfile(f)]
        if missing:
            raise ConfigError("file(s) not found on disk: " + ", ".join(missing))

        # Job reference
        p.fill("#jobref", job_reference)
        # Turnaround (radio)
        p.check(f'#contactform input[name="radio"][value="{turnaround}"]')
        # File types (checkboxes) — the embroidery values are unique in the form
        for ft in file_types:
            if ft == "other":
                p.check("#otherCheckbox")
                other_text = str(params.get("other_text") or "").strip()
                if other_text:
                    p.fill("#otherText", other_text)
            else:
                p.check(f'#contactform input[name="fileType"][value="{ft}"]')
        # Color scheme — target by stable class (the #colorScheme id is swapped
        # between tabs by change_form()).
        p.select_option("#contactform select.color_scheme", color_scheme)
        # Files
        p.set_input_files("#file1", files[0])
        if len(files) >= 2:
            p.set_input_files("#file2", files[1])
        if len(files) >= 3:
            p.set_input_files("#file3", files[2])
        # Proof template
        if _truthy(params.get("proof_template")):
            p.check("#proof_template")
        # Admin note (hidden) — set value directly if provided
        admin_note = str(params.get("admin_note") or "")
        if admin_note:
            p.evaluate("(v) => { const e=document.getElementById('admin_note'); if(e) e.value=v; }", admin_note)
        # Message
        message = str(params.get("message") or "")
        p.fill("#msg", message)

        self._mark("fields-filled")
        return {
            "job_reference": job_reference,
            "turnaround": turnaround,
            "file_types": file_types,
            "other_text": params.get("other_text") if "other" in file_types else None,
            "color_scheme": color_scheme,
            "files": [os.path.abspath(f) for f in files],
            "proof_template": _truthy(params.get("proof_template")),
            "message_chars": len(message),
        }

    def validate_ready(self) -> None:
        """Mirror the page's own uploadfile() preconditions before Send."""
        ok = self.page.evaluate(
            """() => {
              const jr = (document.getElementById('jobref')||{}).value || '';
              const radio = document.querySelector('#contactform input[name=\\"radio\\"]:checked');
              const anyFt = [...document.querySelectorAll('#contactform input[name=\\"fileType\\"]')].some(c=>c.checked);
              const file1 = document.getElementById('file1');
              const hasFile = file1 && file1.files && file1.files.length>0;
              return {jr: jr.trim().length>0, radio: !!radio, anyFt, hasFile};
            }"""
        )
        problems = []
        if not ok["jr"]:
            problems.append("job reference is empty")
        if not ok["radio"]:
            problems.append("no turnaround selected")
        if not ok["anyFt"]:
            problems.append("no file type checked")
        if not ok["hasFile"]:
            problems.append("no file attached to file1")
        if problems:
            raise ConfigError("form not ready to submit: " + "; ".join(problems))

    def send_and_confirm(self) -> dict:
        """Click Send and wait for the real order_form_submit XHR response.

        The page's completeHandler redirects to /placeorder/thanks on ANY
        response (it never checks status), so success is judged on the actual
        HTTP response, not the redirect.
        """
        p = self.page
        result: dict[str, Any] = {}
        try:
            with p.expect_response(
                lambda r: SUBMIT_ENDPOINT_SUFFIX in r.url and r.request.method == "POST",
                timeout=max(self.timeout_ms, 60000),
            ) as resp_info:
                p.click('#contactform input[name="submit"]')
            resp = resp_info.value
            status = resp.status
            body = ""
            try:
                body = resp.text()
            except Exception:
                pass
            result["response"] = {"status": status, "body": (body or "")[:2000], "url": resp.url}
            self._mark("submit-response", status=status)
        except Exception as exc:
            raise PortalError(f"Send clicked but no order_form_submit response arrived: {exc}") from exc

        # Give the page a beat to redirect to /thanks (informational).
        try:
            p.wait_for_url(lambda u: THANKS_SUFFIX in u, timeout=8000)
            result["thanks_url"] = p.url
        except Exception:
            result["thanks_url"] = None

        if result["response"]["status"] != 200:
            raise PortalError(
                f"Submit returned HTTP {result['response']['status']}; body: "
                f"{result['response']['body'][:300]!r}"
            )
        return result

    def screenshot(self, path: str) -> str | None:
        try:
            self.page.screenshot(path=path, full_page=True)
            return path
        except Exception:
            return None

    # -- orders / fetch finished files -----------------------------------

    def fetch_orders(self, params: dict) -> dict:
        """Download a completed order's files from /orders, by job reference.

        Scrapes THIS account's orders table, finds the row(s) for the job
        reference, and downloads the files from that row's OWN download links.
        The link is whatever the vendor actually named the file (any collision
        suffix such as ``8524_2.DST`` included), so it is authoritative — never a
        guessed URL. Returns the saved file paths and which one is the DST.

        Params: job_reference (req); order_id (opt, to disambiguate when a job
        reference repeats across our own orders); out_dir (opt); exts (opt list
        to restrict which extensions to pull); require_completed (default true).
        Returns status "fetched" | "pending" (order there, files not ready) |
        "not_found".
        """
        job = str(params.get("job_reference") or "").strip()
        if not job:
            raise ConfigError("job_reference is required (the decoration id).")
        want_order = str(params.get("order_id") or "").strip()
        out_dir = (params.get("out_dir") or params.get("artifact_dir")
                   or _env("ARTWORKLADY_ARTIFACT_DIR") or os.getcwd())
        os.makedirs(out_dir, exist_ok=True)
        require_completed = _truthy(params.get("require_completed", True))
        want_exts = params.get("exts")
        if isinstance(want_exts, str):
            want_exts = [want_exts]
        want_exts = [str(x).strip().lower().lstrip(".") for x in want_exts] if want_exts else None

        p = self.page
        p.goto(self.base_url + "/orders", wait_until="domcontentloaded", timeout=45000)
        try:
            p.wait_for_selector("table", timeout=self.timeout_ms)
        except Exception:
            pass
        p.wait_for_timeout(800)
        self._mark("orders-loaded", url=p.url)

        # Match rows and read their own download links entirely in the DOM.
        rows = p.evaluate(
            """(job) => {
              const norm = s => (s||'').replace(/\\s+/g,' ').trim();
              const out = [];
              for (const tr of document.querySelectorAll('table tr')) {
                const tds = [...tr.querySelectorAll('td')];
                if (!tds.length) continue;
                if (!tds.some(td => norm(td.textContent) === job)) continue;
                const links = [...tr.querySelectorAll('a.download-file-link, a[href*=\\"artwork_admin/upload\\"], a[href*=\\"download\\"]')]
                  .map(a => ({href: a.href, title: a.getAttribute('title') || '', text: norm(a.textContent)}))
                  .filter(a => a.href);
                out.push({
                  order_id: tds[1] ? norm(tds[1].textContent) : null,
                  completed: norm(tr.textContent).toLowerCase().includes('completed'),
                  links,
                });
              }
              return out;
            }""",
            job,
        )
        if not rows:
            return {"status": "not_found", "action": "fetch", "job_reference": job,
                    "message": "No /orders row found for job reference %s." % job,
                    "trace": self.trace}

        if want_order:
            candidates = [r for r in rows if r["order_id"] == want_order and r["links"]]
        else:
            candidates = [r for r in rows
                          if r["links"] and (r["completed"] or not require_completed)]
        if not candidates:
            return {"status": "pending", "action": "fetch", "job_reference": job,
                    "order_ids": [r["order_id"] for r in rows],
                    "message": ("order found but the digitized files are not ready yet"
                                if not any(r["completed"] for r in rows)
                                else "order completed but no download links were found in the row"),
                    "rows": rows, "trace": self.trace}

        # /orders lists newest first, so the topmost match is the most recent.
        chosen = candidates[0]
        ambiguous = (not want_order) and len(candidates) > 1

        saved, dst_path = [], None
        for link in chosen["links"]:
            href = link["href"]
            name = href.rstrip("/").split("/")[-1] or "download.bin"
            ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
            if want_exts is not None and ext not in want_exts:
                continue
            dest = os.path.join(out_dir, name)
            try:
                # page.request carries the logged-in session cookies.
                resp = p.request.get(href, timeout=max(self.timeout_ms, 60000))
                if not resp.ok:
                    saved.append({"url": href, "name": name, "error": "HTTP %s" % resp.status})
                    continue
                data = resp.body()
                with open(dest, "wb") as fh:
                    fh.write(data)
                entry = {"name": name, "path": os.path.abspath(dest), "size": len(data),
                         "ext": ext, "url": href, "title": link["title"]}
                saved.append(entry)
                if ext == "dst" and dst_path is None:
                    dst_path = entry["path"]
            except Exception as exc:  # noqa: BLE001
                saved.append({"url": href, "name": name,
                              "error": "%s: %s" % (type(exc).__name__, exc)})
        self._mark("files-downloaded", count=sum(1 for s in saved if s.get("path")))
        return {
            "status": "fetched",
            "action": "fetch",
            "job_reference": job,
            "order_id": chosen["order_id"],
            "completed": chosen["completed"],
            "ambiguous": ambiguous,
            "files": saved,
            "dst": dst_path,
            "trace": self.trace,
        }


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


def _run(action: str, params: dict) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover
        raise ConfigError(
            "playwright is required. Install with `pip install playwright` and "
            "`python -m playwright install chromium`."
        ) from exc

    base_url = (params.get("base_url") or _env("ARTWORKLADY_BASE_URL") or BASE_URL_DEFAULT).rstrip("/")
    headless = _truthy(params.get("headless", _env("ARTWORKLADY_HEADLESS", "true")))
    timeout_ms = int(params.get("timeout_ms") or _env("ARTWORKLADY_TIMEOUT_MS", "30000"))
    login_type = str(params.get("login_type") or _env("ARTWORKLADY_LOGIN_TYPE", "employee")).strip().lower()
    if login_type not in VALID_LOGIN_TYPES:
        raise ConfigError(f"login_type must be one of {sorted(VALID_LOGIN_TYPES)}; got {login_type!r}.")
    artifact_dir = params.get("artifact_dir") or _env("ARTWORKLADY_ARTIFACT_DIR") or os.getcwd()
    os.makedirs(artifact_dir, exist_ok=True)

    username, password = resolve_credentials(params)
    trace: list = []

    with sync_playwright() as pw:
        browser = _launch(pw, headless)
        state_path = params.get("state_path") or _env("ARTWORKLADY_STATE_PATH")
        ctx_kwargs: dict[str, Any] = {
            "viewport": {"width": 1440, "height": 900},
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
        }
        if state_path and os.path.isfile(state_path):
            ctx_kwargs["storage_state"] = state_path
        context = browser.new_context(**ctx_kwargs)
        context.set_default_timeout(timeout_ms)
        page = context.new_page()
        drv = Driver(page, base_url, timeout_ms, trace)

        try:
            # Reuse a saved session if it still lands us on /placeorder.
            logged_in = False
            if "storage_state" in ctx_kwargs:
                try:
                    drv.goto_placeorder()
                    logged_in = True
                    drv._mark("session-reused", url=page.url)
                except Exception:
                    logged_in = False
            if not logged_in:
                drv.login(username, password, login_type)
                drv.goto_placeorder()
                if state_path:
                    try:
                        context.storage_state(path=state_path)
                    except Exception:
                        pass

            # Fetch pulls finished files from /orders — no placeorder form needed.
            if action == "fetch":
                return drv.fetch_orders(params)

            drv.open_embroidery()

            if action == "capture":
                shot = drv.screenshot(os.path.join(artifact_dir, "artworklady_capture.png"))
                return {
                    "status": "ok",
                    "action": "capture",
                    "url": page.url,
                    "login_type": login_type,
                    "field_map": drv.field_map(),
                    "screenshot": shot,
                    "trace": trace,
                }

            # action == submit
            filled = drv.fill(params)
            drv.validate_ready()
            shot = drv.screenshot(os.path.join(artifact_dir, "artworklady_filled.png"))
            confirm = _truthy(params.get("confirm"))
            if not confirm:
                return {
                    "status": "dry_run",
                    "action": "submit",
                    "message": "DRY RUN — the Embroidery form was filled and validated but NOT sent. Re-run with \"confirm\": true to post the job.",
                    "filled": filled,
                    "screenshot": shot,
                    "trace": trace,
                }

            outcome = drv.send_and_confirm()
            drv.screenshot(os.path.join(artifact_dir, "artworklady_after_send.png"))
            return {
                "status": "submitted",
                "action": "submit",
                "filled": filled,
                "response": outcome.get("response"),
                "thanks_url": outcome.get("thanks_url"),
                "screenshot": shot,
                "trace": trace,
            }
        except (ConfigError, PortalError):
            drv.screenshot(os.path.join(artifact_dir, "artworklady_failure.png"))
            try:
                with open(os.path.join(artifact_dir, "artworklady_failure.html"), "w") as fh:
                    fh.write(page.content())
            except Exception:
                pass
            raise
        finally:
            context.close()
            browser.close()


def main(argv: list) -> int:
    if len(argv) < 2 or argv[1] not in {"capture", "submit", "fetch"}:
        print(json.dumps({"error": {"type": "usage", "message": "usage: artworklady_digitizing.py {capture|submit|fetch} '<json>'"}}))
        return 2
    action = argv[1]
    raw = argv[2] if len(argv) > 2 else sys.stdin.read()
    try:
        params = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": {"type": "bad_json", "message": str(exc)}}))
        return 2
    try:
        result = _run(action, params)
        print(json.dumps(result, indent=2))
        return 0
    except ConfigError as exc:
        print(json.dumps({"error": {"type": "config_error", "message": str(exc)}}, indent=2))
        return 3
    except PortalError as exc:
        print(json.dumps({"error": {"type": "portal_error", "message": str(exc)}}, indent=2))
        return 4
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": {"type": "unexpected", "message": f"{type(exc).__name__}: {exc}"}}, indent=2))
        return 5


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
