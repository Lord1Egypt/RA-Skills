"""FastMCP server - the agentSAFE MCP entry point.

Tools:
  audit_contract(address)        -> dispatch GitHub Actions audit, return task_id
  check_audit_status(task_id)   -> recoverable status + report when ready
  get_contract_info(address)    -> on-chain + verification snapshot

Modes:
  stdio  : local development / single-client (default)
  http   : remote deployment (run behind an authenticating proxy)

Payments: fail-closed x402 gate (Phase 12). PAYMENTS_ENABLED=false runs free
in dev mode; true requires the pinned official x402 SDK (see
payment/x402_adapter.py) and gates audit_contract with verify-before-execution
/ settle-after-execution. Report retrieval is bound to the verified payment.
"""

from __future__ import annotations

import base64
import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.tools import ToolResult
from starlette.requests import Request
from starlette.responses import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    Response,
)

from agentsafe import __version__
from agentsafe.config import Settings, validate_runtime_settings
from agentsafe.explorer import ContractNotVerifiedError, EtherscanClient, ExplorerError
from agentsafe.github_client import (
    ArtifactExpiredError,
    GitHubActionsClient,
    GitHubClientError,
    RunAssociationError,
)
from agentsafe.payment.x402_adapter import (
    StarletteRequestAdapter,
    VerifiedPayment,
    X402PaymentAdapter,
)
from agentsafe.pricing import (
    CUSTOM_PRICING_CONTACT_URL,
    ContractTooLargeError,
    audit_price_for_lines,
    count_source_lines,
    pricing_summary,
)
from agentsafe.rpc import EthRpcClient
from agentsafe.schemas import AuditReport, TaskState, normalize_address
from agentsafe.task_store import open_task_store
from agentsafe.web import INDEX_HTML, LegalDocumentMissingError, legal_html

logger = logging.getLogger("agentSAFE.server")

# -------------------------------------------------------------- x402 REST API
# Machine-readable discovery (openapi.json, indexed by x402scan & co) plus a
# real x402-gated REST dispatch endpoint mirroring the MCP audit_contract
# flow. This is NOT part of the MCP protocol surface; it exists so that
# x402 indexers and plain-HTTP x402 clients can discover and pay for audits.
REST_AUDIT_PATH = "/api/audit"
# The REST endpoint's flat fee (X402_REST_PRICE) only covers contracts up to
# this many source lines. Larger contracts must use the MCP endpoint's tiered
# pricing (audit_contract) or the enterprise channel; this cap prevents the
# flat REST fee from undercutting the higher MCP tiers.
REST_AUDIT_MAX_LINES = 500
_OPENAPI_FILE = Path(__file__).resolve().parents[2] / "openapi.json"
_FAVICON_FILE = Path(__file__).resolve().parents[2] / "favicon.ico"
_LOGO_FILE = Path(__file__).resolve().parents[2] / "logo.png"

mcp: FastMCP | None = None


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    # httpx logs full request URLs at INFO; Etherscan URLs embed the API key
    # as a query parameter, so those lines must never be emitted.
    logging.getLogger("httpx").setLevel(logging.WARNING)


def build_server(settings: Settings, *, validate: bool = True) -> FastMCP:
    """Construct the FastMCP instance. Fails fast on bad config.

    validate=False defers configuration validation to server startup via a
    lifespan hook. Used for cloud deployments (FastMCP Cloud / Horizon)
    where build-time inspection runs without environment variables; a
    misconfigured deployment still refuses to serve at runtime.
    """
    if validate:
        validate_runtime_settings(settings)  # raises SettingsError with ALL problems

    # Task store: explicit TASK_STORE wins; otherwise auto-selected from the
    # environment - 'redis' when a Redis/Upstash URL is detectable (serverless
    # safe, survives cold starts), else 'sqlite' for durable local state.
    store_mode = settings.resolved_task_store
    task_store = open_task_store(
        store_mode,
        Path(settings.TASK_DB_PATH),
        redis_url=settings.effective_redis_url if store_mode == "redis" else "",
        retention_days=settings.ARTIFACT_RETENTION_DAYS,
    )

    # Payments gate (fail-closed; disabled = dev no-op)
    payment = X402PaymentAdapter(
        enabled=settings.PAYMENTS_ENABLED,
        sdk_version=settings.X402_SDK_VERSION,
        network=settings.X402_NETWORK,
        pay_to=settings.X402_PAY_TO,
        facilitator_url=settings.X402_FACILITATOR_URL,
        price=settings.X402_PRICE,
        asset=settings.X402_ASSET,
        max_timeout_seconds=settings.X402_MAX_TIMEOUT_SECONDS,
    )
    # Re-arm replay protection: payloads already consumed before a restart
    # must stay rejected (bounded by the task-store retention window).
    if payment.enabled:
        payment.seed_replay_ledger(task_store.payment_refs())

    gh = GitHubActionsClient(
        token=settings.GITHUB_TOKEN,
        repo=settings.GITHUB_REPO,
        workflow_file=settings.GITHUB_WORKFLOW_FILE,
        ref=settings.GITHUB_REF,
        timeout_seconds=settings.GITHUB_API_TIMEOUT_SECONDS,
        poll_interval_seconds=settings.GITHUB_POLL_INTERVAL_SECONDS,
        strict=validate,
    )

    rpc = EthRpcClient(settings.INFURA_ETH_ENDPOINT)
    explorer = EtherscanClient(
        settings.ETHERSCAN_API_KEY,
        base_url=settings.ETHERSCAN_BASE_URL,
        strict=validate,
    )

    # Official x402 HTTP flow for the REST endpoint (payments-enabled only).
    # Built once per process and shares the adapter's already-initialized
    # x402ResourceServer (facilitator /supported cached at adapter startup),
    # so no extra startup round-trips. Indexers like x402scan hit
    # POST /api/audit without payment and receive the official 402 wire
    # format (PAYMENT-REQUIRED header + body quoting X402_REST_PRICE).
    x402_http = None
    if payment.enabled:
        from x402.http import PaymentOption, RouteConfig

        x402_http = payment.http_resource_server(
            {
                f"POST {REST_AUDIT_PATH}": RouteConfig(
                    accepts=PaymentOption(
                        scheme="exact",
                        pay_to=payment.pay_to,
                        price=settings.X402_REST_PRICE,
                        network=payment.network,
                        max_timeout_seconds=settings.X402_MAX_TIMEOUT_SECONDS,
                        extra={"asset": settings.X402_ASSET} if settings.X402_ASSET else None,
                    ),
                    description="AI smart-contract risk audit dispatch (x402-paid)",
                    mime_type="application/json",
                    service_name="agentSAFE",
                    tags=["smart-contract-audit", "ai-audit", "base"],
                )
            }
        )

    @asynccontextmanager
    async def _startup_validation(server: FastMCP) -> AsyncIterator[None]:
        if not validate:
            # Cloud mode: env vars only exist at runtime, so fail fast HERE.
            validate_runtime_settings(Settings())
        yield None

    app = FastMCP(
        "agentSAFE",
        instructions=(
            "EVM smart-contract audit MCP (Ethereum Mainnet). AI-assisted risk "
            "screening, NOT a formal security audit. Findings require human "
            "verification before any action."
        ),
        lifespan=_startup_validation,
        # Production safety: clients never receive internal stack traces or
        # environment-derived error details from a crashing tool; full
        # details stay in the service logs.
        mask_error_details=True,
    )

    @app.tool
    async def health() -> dict[str, Any]:
        """Liveness/config probe. Safe, non-paid, and never returns secrets.

        Use this to verify a deployment (public endpoint reachability,
        tool discovery) without triggering an audit or a payment.
        """
        return {
            "ok": True,
            "service": "agentSAFE",
            "version": __version__,
            "chain": "ethereum-mainnet",
            "payments": {
                "enabled": payment.enabled,
                "network": settings.X402_NETWORK if payment.enabled else None,
                "pricing": pricing_summary(),
            },
            "task_store": getattr(settings, "TASK_STORE", "sqlite"),
            "audit_workflow": settings.GITHUB_WORKFLOW_FILE,
            "terms_of_service": "https://github.com/luka1968/agentsafe/blob/main/TERMS_OF_SERVICE.md",
            "web_pages": {
                "/": "landing",
                "/terms": "Terms of Service",
                "/privacy": "Privacy Policy",
                "/refund": "Refund Policy",
                "/openapi.json": "OpenAPI discovery document (x402scan indexing)",
                "/api/audit": "x402 REST audit dispatch (paid, see /openapi.json)",
            },
        }

    # ------------------------------------------------------- public web pages
    # Served by the HTTP transport (http_app): the legal Markdown files are
    # the same single source of truth linked from the health tool.

    @app.custom_route("/", methods=["GET"])
    async def _index(request: Request) -> HTMLResponse:
        return HTMLResponse(INDEX_HTML)

    @app.custom_route("/terms", methods=["GET"])
    async def _terms(request: Request) -> HTMLResponse:
        try:
            return HTMLResponse(legal_html("terms"))
        except LegalDocumentMissingError as exc:
            return PlainTextResponse(str(exc), status_code=500)

    @app.custom_route("/privacy", methods=["GET"])
    async def _privacy(request: Request) -> HTMLResponse:
        try:
            return HTMLResponse(legal_html("privacy"))
        except LegalDocumentMissingError as exc:
            return PlainTextResponse(str(exc), status_code=500)

    @app.custom_route("/refund", methods=["GET"])
    async def _refund(request: Request) -> HTMLResponse:
        try:
            return HTMLResponse(legal_html("refund"))
        except LegalDocumentMissingError as exc:
            return PlainTextResponse(str(exc), status_code=500)

    # ------------------------------------------------ x402 REST API (x402scan)

    @app.custom_route("/openapi.json", methods=["GET"])
    async def _openapi(request: Request) -> Response:
        """Machine-readable discovery document for x402 indexers."""
        try:
            spec = json.loads(_OPENAPI_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.error("openapi.json unavailable at %s: %s", _OPENAPI_FILE, exc)
            return PlainTextResponse(
                "openapi discovery document unavailable", status_code=500
            )
        return JSONResponse(spec)

    @app.custom_route("/.well-known/openapi.json", methods=["GET"])
    async def _openapi_wellknown(request: Request) -> Response:
        """Alias used by x402scan & discovery crawlers that probe the well-known
        path instead of the root OpenAPI file."""
        try:
            spec = json.loads(_OPENAPI_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.error("openapi.json unavailable at %s: %s", _OPENAPI_FILE, exc)
            return PlainTextResponse(
                "openapi discovery document unavailable", status_code=500
            )
        return JSONResponse(spec)

    @app.custom_route("/logo.png", methods=["GET"])
    async def _logo(request: Request) -> Response:
        """512x512 brand logotype for directory listings (x402scan
        'Logotype URL' field and similar) that prefer PNG over ICO."""
        try:
            data = _LOGO_FILE.read_bytes()
        except OSError as exc:
            logger.error("logo.png unavailable at %s: %s", _LOGO_FILE, exc)
            return PlainTextResponse("logo unavailable", status_code=404)
        return Response(
            content=data,
            media_type="image/png",
            headers={"cache-control": "public, max-age=3600"},
        )

    @app.custom_route("/favicon.ico", methods=["GET"])
    async def _favicon(request: Request) -> Response:
        """API-root icon surfaced by x402scan listings and browser tabs."""
        try:
            data = _FAVICON_FILE.read_bytes()
        except OSError as exc:
            logger.error("favicon.ico unavailable at %s: %s", _FAVICON_FILE, exc)
            return PlainTextResponse("favicon unavailable", status_code=404)
        return Response(
            content=data,
            media_type="image/x-icon",
            # Short TTL: lets icon updates propagate within an hour across
            # browser + CDN caches (x402scan hotlinks this URL directly).
            headers={"cache-control": "public, max-age=3600"},
        )

    @app.custom_route(REST_AUDIT_PATH, methods=["POST"])
    async def _api_audit(request: Request) -> Response:
        """x402-gated REST audit dispatch (documented in openapi.json).

        Fail-closed mirror of the MCP audit_contract flow:
          no payment     -> official x402 402 (PAYMENT-REQUIRED header + body)
          replay         -> 402, payload never accepted twice
          verified       -> source-size guard BEFORE settlement (flat-fee cap),
                            task dispatch, settlement AFTER successful dispatch
          dispatch fail  -> settlement NOT attempted (no funds ever move)
        """
        if x402_http is None:
            # Dev mode (payments disabled): free dispatch, mirrors free MCP tools.
            body_bytes = await request.body()
            try:
                parsed_body = json.loads(body_bytes) if body_bytes else None
            except json.JSONDecodeError:
                parsed_body = None
            return await _dispatch_audit_rest(request, None, parsed_body, None)
        try:
            from x402.http import HTTPRequestContext

            body_bytes = await request.body()
            try:
                parsed_body = json.loads(body_bytes) if body_bytes else None
            except json.JSONDecodeError:
                parsed_body = None
            ctx = HTTPRequestContext(
                adapter=StarletteRequestAdapter(request, parsed_body=parsed_body),
                path=REST_AUDIT_PATH,
                method="POST",
            )
            result = await x402_http.process_http_request(ctx)
            if result.type == "payment-error":
                instr = result.response
                assert instr is not None  # SDK contract: error carries instructions
                headers = {
                    k: v for k, v in (instr.headers or {}).items() if k.lower() != "content-type"
                }
                # Official x402 v2 wire format carries the machine-readable
                # requirements in the base64 PAYMENT-REQUIRED header with an
                # empty body. Mirror the decoded JSON into the body as well:
                # the body is free-form per spec, and human/indexer fallback
                # parsers (x402scan variants) get the terms without having to
                # decode the header.
                body = instr.body if isinstance(instr.body, dict) and instr.body else None
                if body is None:
                    required_header = headers.get("PAYMENT-REQUIRED") or headers.get(
                        "payment-required"
                    )
                    body = {"error": "Payment Required"}
                    if required_header:
                        try:
                            body = json.loads(base64.b64decode(required_header).decode("utf-8"))
                        except Exception:  # noqa: BLE001 - fall back to minimal body
                            logger.warning("could not decode PAYMENT-REQUIRED header for body mirror")
                return JSONResponse(body, status_code=instr.status, headers=headers)
            if result.type != "payment-verified" or result.payment_payload is None:
                return JSONResponse(
                    {
                        "ok": False,
                        "error_code": "payment_required",
                        "error": "Payment Required",
                    },
                    status_code=402,
                )
            ref = X402PaymentAdapter.payment_ref(result.payment_payload)
            if payment.replay_seen(ref):
                logger.info("REST payment replay rejected ref=%s", ref[:16])
                return JSONResponse(
                    {
                        "ok": False,
                        "error_code": "payment_replay",
                        "error": "Payment already used (replay rejected)",
                    },
                    status_code=402,
                )
            payment.record_replay(ref)
            verified = VerifiedPayment(
                payload=result.payment_payload,
                requirements=result.payment_requirements,
                ref=ref,
            )
            return await _dispatch_audit_rest(request, verified, parsed_body, ctx)
        except Exception:  # noqa: BLE001 - never leak internals to HTTP clients
            logger.exception("REST audit endpoint failed")
            return JSONResponse(
                {"ok": False, "error_code": "internal_error", "error": "internal error"},
                status_code=500,
            )

    async def _dispatch_audit_rest(
        request: Request,
        verified: VerifiedPayment | None,
        parsed_body: Any,
        ctx: Any = None,
    ) -> Response:
        """Shared dispatch pipeline for POST /api/audit (x402-paid or free in
        dev mode). The source-size guard runs BEFORE any settlement, so a
        paid request that cannot be served at the flat fee never moves funds."""
        if not isinstance(parsed_body, dict):
            return JSONResponse(
                {
                    "ok": False,
                    "error_code": "invalid_json",
                    "error": "request body must be a JSON object with an 'address' field",
                },
                status_code=400,
            )
        try:
            addr = normalize_address(str(parsed_body.get("address", "")))
        except ValueError as exc:
            return JSONResponse(
                {"ok": False, "error_code": "invalid_address", "error": str(exc)},
                status_code=400,
            )
        try:
            bundle = await explorer.get_verified_source(addr)
        except ContractNotVerifiedError:
            return JSONResponse(
                {
                    "ok": False,
                    "error_code": "source_not_verified",
                    "error": "audit requires verified source; no price can be quoted",
                },
                status_code=422,
            )
        except ExplorerError as exc:
            return JSONResponse(
                {
                    "ok": False,
                    "error_code": "pricing_failed",
                    "error": f"could not retrieve source for validation: {exc}",
                },
                status_code=422,
            )
        lines = count_source_lines(bundle)
        if lines > REST_AUDIT_MAX_LINES:
            logger.info("REST dispatch rejected: lines=%d exceeds flat-fee cap", lines)
            return JSONResponse(
                {
                    "ok": False,
                    "error_code": "REST_FLAT_FEE_LINE_LIMIT",
                    "error": (
                        f"{lines} source lines exceed the {REST_AUDIT_MAX_LINES}-line flat fee; "
                        "use the MCP endpoint (audit_contract) for tiered pricing"
                    ),
                },
                status_code=422,
            )

        task = task_store.create_task(addr)
        if verified is not None:
            task_store.mark_paid(task.task_id, verified.ref)
        task_store.set_state(task.task_id, TaskState.QUEUED)
        logger.info(
            "REST audit dispatch address=%s task_id=%s paid=%s",
            addr,
            task.task_id,
            verified is not None,
        )
        try:
            dispatched_at = await gh.trigger_workflow(addr, task.task_id)
            run_id = await gh.resolve_run_id(task.task_id, dispatched_after=dispatched_at)
            task_store.link_run(task.task_id, run_id)
            task_store.set_state(task.task_id, TaskState.RUNNING)
        except GitHubClientError as exc:
            # Dispatch failed: settlement is NOT attempted (verify-only so
            # far; the on-chain transfer never executes -> no funds move).
            task_store.set_state(task.task_id, TaskState.FAILED, error_code="dispatch_failed")
            return JSONResponse(
                {
                    "ok": False,
                    "task_id": task.task_id,
                    "error_code": "dispatch_failed",
                    "error": str(exc),
                },
                status_code=502,
            )

        headers: dict[str, str] = {}
        settlement_error: str | None = None
        if verified is not None and x402_http is not None and ctx is not None:
            settle = await x402_http.process_settlement(
                verified.payload,
                verified.requirements,
                context=ctx,
                phase="after-handler",
            )
            headers = {
                k: v for k, v in (settle.headers or {}).items() if k.lower() != "content-type"
            }
            if not settle.success:
                # Settlement failure does not stop the dispatched audit; it
                # is surfaced to the payer (mirrors the MCP after-handler flow).
                logger.error(
                    "REST settlement failed ref=%s reason=%s",
                    verified.ref[:16],
                    settle.error_reason,
                )
                settlement_error = (
                    f"payment settlement failed: {settle.error_reason or 'unknown failure'}"
                )
        body: dict[str, Any] = {
            "ok": True,
            "task_id": task.task_id,
            "address": addr,
            "state": "running",
            "run_id": run_id,
            "note": "report retrieval via the agentSAFE MCP tool check_audit_status",
        }
        if settlement_error:
            body["settlement_error"] = settlement_error
        return JSONResponse(body, status_code=202, headers=headers)

    @app.tool
    async def audit_contract(address: str, ctx: Context) -> dict[str, Any] | ToolResult:
        """Start an audit for a Mainnet contract address. Returns a task_id.

        The audit runs on a GitHub Actions worker; poll check_audit_status.

        When payments are enabled, this tool is x402-gated: an unpaid call
        returns the official 402 payment-required body and never dispatches.
        """
        try:
            addr = normalize_address(address)
        except ValueError as exc:
            return {"ok": False, "error_code": "invalid_address", "error": str(exc)}

        verified: VerifiedPayment | None = None
        if payment.enabled:
            # Tiered pricing: quote from the verified source size BEFORE any
            # payment challenge, so the advertised amount always matches the
            # real audit cost. The client cannot influence the quoted tier.
            try:
                bundle = await explorer.get_verified_source(addr)
            except ContractNotVerifiedError:
                return {
                    "ok": False,
                    "error_code": "source_not_verified",
                    "error": "audit requires verified source; no price can be quoted",
                }
            except ExplorerError as exc:
                return {
                    "ok": False,
                    "error_code": "pricing_failed",
                    "error": f"could not retrieve source for pricing: {exc}",
                }
            lines = count_source_lines(bundle)
            try:
                price = audit_price_for_lines(lines)
            except ContractTooLargeError:
                # Enterprise interception: reject BEFORE any payment is
                # initiated or expensive processing starts. Never truncate
                # the input or split it into billable requests.
                return {
                    "ok": False,
                    "error_code": "ENTERPRISE_INQUIRY_REQUIRED",
                    "error": "ENTERPRISE_INQUIRY_REQUIRED",
                    "message": (
                        "Your project exceeds the standard 5,000-line limit. "
                        "Please contact us to discuss enterprise processing."
                    ),
                    "inquiryUrl": CUSTOM_PRICING_CONTACT_URL,
                }
            tier_requirements = payment.requirements_for_price(price)
            # Official SDK flow: verify BEFORE execution. Unverified requests
            # receive the payment-required result quoting the tier price and
            # no dispatch happens.
            verified, deny = await payment.verify(
                ctx, "audit_contract", requirements=tier_requirements
            )
            if deny is not None:
                return deny
            logger.info("audit_contract quoted tier price=%s lines=%d", price, lines)

        task = task_store.create_task(addr)
        if verified is not None:
            # Bind the verified payment to this task; report retrieval for
            # this task is released only when this flag is set.
            task_store.mark_paid(task.task_id, verified.ref)
        task_store.set_state(task.task_id, TaskState.QUEUED)
        logger.info("audit_contract address=%s task_id=%s", addr, task.task_id)
        try:
            dispatched_at = await gh.trigger_workflow(addr, task.task_id)
            run_id = await gh.resolve_run_id(task.task_id, dispatched_after=dispatched_at)
            task_store.link_run(task.task_id, run_id)
            task_store.set_state(task.task_id, TaskState.RUNNING)
        except RunAssociationError as exc:
            settled = await _settle_payment(verified, "audit_contract")
            if settled is not None:
                return settled
            return {
                "ok": True,
                "task_id": task.task_id,
                "address": addr,
                "note": (
                    "workflow dispatched but run not yet visible; retry check_audit_status shortly"
                ),
                "detail": str(exc),
            }
        except GitHubClientError as exc:
            # Dispatch failed: settlement is NOT attempted (verify-only so far,
            # the on-chain transfer never executes -> no funds collected).
            # No refund is owed or promised.
            task_store.set_state(task.task_id, TaskState.FAILED, error_code="dispatch_failed")
            return {
                "ok": False,
                "task_id": task.task_id,
                "error_code": "dispatch_failed",
                "error": str(exc),
            }
        settled = await _settle_payment(verified, "audit_contract")
        if settled is not None:
            return settled
        return {
            "ok": True,
            "task_id": task.task_id,
            "address": addr,
            "run_id": run_id,
            "state": "running",
        }

    async def _settle_payment(
        verified: VerifiedPayment | None, tool_name: str
    ) -> ToolResult | None:
        """Settle AFTER successful execution (official after-handler phase).

        Returns the settlement-failed error result on failure, else None.
        A settlement failure does not stop the dispatched audit; it is
        surfaced to the payer. No automatic refunds exist in the exact-EVM
        scheme.
        """
        if verified is None:
            return None
        try:
            settle_result = await payment.settle(verified)
        except Exception as exc:
            logger.error("settlement failed tool=%s ref=%s: %s", tool_name, verified.ref, exc)
            return await payment.settlement_failed_result(
                tool_name, str(exc), requirements=[verified.requirements]
            )
        if not settle_result.success:
            logger.error(
                "settlement rejected tool=%s ref=%s reason=%s",
                tool_name,
                verified.ref,
                settle_result.error_reason,
            )
            return await payment.settlement_failed_result(
                tool_name,
                settle_result.error_reason or "unknown settlement failure",
                requirements=[verified.requirements],
            )
        logger.info(
            "payment settled tool=%s ref=%s tx=%s",
            tool_name,
            verified.ref[:16],
            settle_result.transaction,
        )
        return None

    @app.tool
    async def check_audit_status(task_id: str) -> dict[str, Any]:
        """Check audit progress; returns the report once the run completes."""
        if not task_id or len(task_id) > 64:
            return {
                "ok": False,
                "error_code": "invalid_task_id",
                "error": "task_id must be 1..64 chars",
            }
        task = task_store.get(task_id)
        if task is None:
            return {
                "ok": False,
                "error_code": "unknown_task",
                "error": "no such task (it may have expired or never existed)",
            }

        if task.run_id is None:
            return {
                "ok": True,
                "task_id": task_id,
                "state": task.state.value,
                "detail": "workflow dispatch pending or run not yet associated",
            }

        try:
            run = await gh.get_run(task.run_id)
        except GitHubClientError as exc:
            return {
                "ok": True,
                "task_id": task_id,
                "state": task.state.value,
                "error": f"status lookup failed: {exc}",
            }

        mapped = gh.map_run_status(run)
        task_store.set_state(task_id, TaskState(mapped))

        if mapped == "completed":
            if payment.enabled and not task.paid:
                # Payment binding: a task that never passed payment
                # verification must not release a paid report.
                return {
                    "ok": False,
                    "task_id": task_id,
                    "state": mapped,
                    "error_code": "payment_required",
                    "error": "report withheld: no verified payment is bound to this task",
                }
            try:
                report = await gh.fetch_report(task.run_id, task_id)
            except ArtifactExpiredError:
                task_store.set_state(task_id, TaskState.EXPIRED, error_code="artifact_expired")
                return {
                    "ok": True,
                    "task_id": task_id,
                    "state": "expired",
                    "error": "report artifact expired; re-run the audit",
                }
            except GitHubClientError as exc:
                return {
                    "ok": True,
                    "task_id": task_id,
                    "state": mapped,
                    "error": f"report unavailable: {exc}",
                }
            task_store.set_state(task_id, TaskState.COMPLETED)
            return {
                "ok": True,
                "task_id": task_id,
                "state": "completed",
                "report": _clip_report(report),
            }
        if mapped == "failed":
            task_store.set_state(
                task_id, TaskState.FAILED, error_code=f"run_conclusion:{run.get('conclusion')}"
            )
        return {
            "ok": True,
            "task_id": task_id,
            "state": mapped,
            "run_conclusion": run.get("conclusion"),
        }

    @app.tool
    async def get_contract_info(address: str) -> dict[str, Any]:
        """On-chain snapshot: is contract, bytecode size, verified source?"""
        try:
            addr = normalize_address(address)
        except ValueError as exc:
            return {"ok": False, "error_code": "invalid_address", "error": str(exc)}
        info: dict[str, Any] = {"address": addr}
        try:
            code = await rpc.get_code(addr)
            info["is_contract"] = len(code) > 2
            info["bytecode_size_bytes"] = (len(code) - 2) // 2
        except Exception as exc:
            info["rpc_error"] = str(exc)
        try:
            await explorer.get_verified_source(addr)
            info["verified_source"] = True
        except ContractNotVerifiedError:
            info["verified_source"] = False
        except Exception as exc:
            info["etherscan_error"] = str(exc)
        return {"ok": True, **info}

    return app


def _clip_report(report: dict[str, Any]) -> dict[str, Any]:
    """Sanity-clip the report payload returned through MCP."""
    if not isinstance(report, dict):
        return {"raw": str(report)[:1000]}
    findings = report.get("findings")
    if isinstance(findings, list) and len(findings) > 100:
        report = dict(report)
        report["findings"] = findings[:100]
        report["findings_truncated"] = True
    try:
        AuditReport.model_validate(report)  # validate shape when possible
    except Exception:
        return {"raw": str(report)[:4000]}
    return report


def create_app() -> FastMCP:
    """Zero-arg factory for FastMCP Cloud / Prefect Horizon deployments.

    Entrypoint: agentsafe.server:create_app (env vars supply all settings).
    Cloud builds inspect the server WITHOUT env vars, so validation is
    deferred to runtime startup (see build_server validate=False).
    """
    return build_server(Settings(), validate=False)


def main() -> None:
    """Entry point: python -m agentsafe.server [--transport stdio|http]"""
    import argparse

    parser = argparse.ArgumentParser(description="agentSAFE MCP server")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    settings = Settings()
    _setup_logging(settings.LOG_LEVEL)
    global mcp
    mcp = build_server(settings)
    logger.info(
        "agentSAFE MCP v%s starting (transport=%s, payments=%s)",
        __version__,
        args.transport,
        settings.PAYMENTS_ENABLED,
    )
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        # HTTP transport: serve the app with the access-log middleware
        # (visitor IP + time, 30-day retention - see PRIVACY_POLICY.md).
        import uvicorn
        from starlette.middleware import Middleware as StarletteMiddleware

        from agentsafe.web import AccessLogMiddleware, AccessLogStore

        store = AccessLogStore(settings.ACCESS_LOG_DB_PATH)
        purged = store.purge()
        logger.info(
            "access log db=%s purged=%d (retention 30 days)",
            settings.ACCESS_LOG_DB_PATH,
            purged,
        )
        app = mcp.http_app(middleware=[StarletteMiddleware(AccessLogMiddleware, store=store)])
        uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
