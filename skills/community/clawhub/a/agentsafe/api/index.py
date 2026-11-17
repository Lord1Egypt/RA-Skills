"""Vercel Serverless Function for agentSAFE MCP server (ASGI entrypoint).

The Vercel Python runtime requires a top-level ``app`` variable that is an
ASGI callable. FastMCP's ``http_app()`` provides it, with two serverless
adaptations applied here:

1. ``stateless_http=True, json_response=True`` - no session affinity and no
   SSE streaming, both of which are serverless-hostile (cold starts kill
   sessions; function/proxy layers may buffer streams). Spec-compliant: the
   streamable-HTTP transport lets the server choose JSON responses.

2. ``_ServerlessLifespanBootstrap`` - Vercel never emits ASGI ``lifespan``
   events, but FastMCP only starts its streamable-HTTP session manager
   inside the lifespan. Without a bootstrap every ``/mcp`` request fails
   with "Task group is not initialized" -> HTTP 500 (observed in
   production).

   The bootstrap runs the real lifespan inside a dedicated holder task on
   the *current* event loop - the uvicorn model (a lifespan task separate
   from request tasks), so enter/suspend/exit happen in one task context
   and anyio task groups plus fastmcp ContextVar tokens stay consistent.

   Crucially, the holder is keyed PER EVENT LOOP: the Vercel Python runtime
   rotates event loops across function invocations of the same warm
   process. A holder bound to a previous loop leaves the session manager's
   task group on a dead loop and every subsequent ``/mcp`` request fails
   with 500 "Internal Server Error" (observed in production; landing pages
   kept working because static routes never touch the session manager).
   When the running loop differs from the holder's loop, the old holder is
   abandoned (its loop is gone; the old loop's asyncgen shutdown finalizes
   the suspended lifespan inside its own context) and a fresh holder is
   started on the current loop.

Real ASGI servers (uvicorn CLI) emit lifespan on a single loop, so the
pass-through branch keeps local behavior unchanged.

Configuration errors degrade to a plain-text 500 responder instead of
crashing the function, mirroring the FastMCP Cloud path in DEPLOYMENT.md.
"""

import asyncio
import sys
from pathlib import Path

# Add src directory to path so agentsafe package imports work.
# Vercel runs from the repo root; keep this explicit for local runs too.
_src = Path(__file__).resolve().parent.parent / "src"
_src_str = str(_src)
if _src_str not in sys.path:
    sys.path.insert(0, _src_str)


async def _send_text_error(send, message: str) -> None:
    """Emit a plain-text HTTP 500 with a safe error description."""
    body = f"agentSAFE configuration error: {message}\n".encode()
    await send(
        {
            "type": "http.response.start",
            "status": 500,
            "headers": [
                (b"content-type", b"text/plain; charset=utf-8"),
                (b"content-length", str(len(body)).encode()),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})


def _error_app(message: str):
    """Minimal ASGI app that surfaces configuration errors as HTTP 500."""

    async def _asgi(scope, receive, send):
        if scope["type"] != "http":
            return
        await _send_text_error(send, message)

    return _asgi


class _LoopLifespanState:
    """Per-event-loop lifespan holder state.

    One instance per event loop the runtime rotates through. Everything it
    holds (the asyncio lock, the holder task, the shutdown event) is bound
    to ``loop`` and must never be touched from another loop.
    """

    __slots__ = (
        "loop",
        "lock",
        "started",
        "failed",
        "error",
        "holder_task",
        "shutdown_event",
    )

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.lock = asyncio.Lock()  # created inside the running loop: bound OK
        self.started = False
        self.failed = False
        self.error = ""
        self.holder_task: asyncio.Task | None = None
        self.shutdown_event: asyncio.Event | None = None


class _ServerlessLifespanBootstrap:
    """Run the wrapped app's lifespan when the host never emits it.

    Concurrency-safe per loop: a single holder task per event loop, guarded
    by that loop's lock and flags. Startup failures are captured and
    re-served as clear 500 text instead of crashing repeatedly.
    """

    def __init__(self, asgi_app) -> None:
        self._app = asgi_app
        self._state: _LoopLifespanState | None = None
        # Set when a real ASGI server (uvicorn) emits the lifespan itself:
        # all further requests must skip bootstrapping entirely.
        self._host_lifespan_seen = False

    # ------------------------------------------------------- holder logic

    def _state_for_current_loop(self) -> _LoopLifespanState:
        """Return the state bound to the running loop, rotating on change.

        Vercel rotates event loops across invocations of the same warm
        process. When the running loop is not the holder's loop, the old
        holder is abandoned (its loop is dead - the session manager task
        group dies with it, and the old loop's asyncgen shutdown finalizes
        the suspended lifespan generator inside its own context, keeping
        ContextVar token semantics correct) and a fresh state is created.
        """
        loop = asyncio.get_running_loop()
        state = self._state
        if state is None or state.loop is not loop:
            self._state = _LoopLifespanState(loop)
            state = self._state
        return state

    async def _hold_lifespan(
        self, state: _LoopLifespanState, started: asyncio.Event, shutdown: asyncio.Event
    ) -> None:
        """Enter the lifespan and hold it until ``shutdown`` is set.

        The ``yield`` suspension point of the lifespan generator, the
        session manager's task group and every ContextVar token live inside
        this task - so a later exit (``shutdown`` or loop teardown) resets
        tokens in the very context that created them.
        """
        try:
            async with self._app.router.lifespan_context(self._app):
                state.started = True
                started.set()
                await shutdown.wait()
        except Exception as exc:  # noqa: BLE001 - fail closed with detail
            state.failed = True
            state.error = str(exc)
        finally:
            started.set()

    async def _ensure_started(self, state: _LoopLifespanState) -> None:
        if state.started or state.failed:
            return
        async with state.lock:
            if state.started or state.failed:
                return
            started = asyncio.Event()
            shutdown = asyncio.Event()
            state.shutdown_event = shutdown
            state.holder_task = state.loop.create_task(
                self._hold_lifespan(state, started, shutdown)
            )
            await started.wait()

    async def aclose(self) -> None:
        """Orderly shutdown of the CURRENT loop's holder: the holder task
        exits the lifespan inside its own context (task groups unwind,
        ContextVar tokens reset correctly). Idempotent; a no-op when the
        running loop is not the holder's loop (that holder died with its
        loop) or never started."""
        state = self._state
        if state is None or state.loop is not asyncio.get_running_loop():
            return
        task, self._state = state.holder_task, None
        if task is None or task.done():
            return
        if state.shutdown_event is not None:
            state.shutdown_event.set()
        try:
            await task
        except Exception:  # noqa: BLE001 - shutdown must never raise upstream
            pass

    # -------------------------------------------------------- ASGI entry

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            # Real ASGI server (local uvicorn): let Starlette run its own
            # lifespan, then never bootstrap on top of it.
            self._host_lifespan_seen = True
            await self._app(scope, receive, send)
            return
        if scope["type"] == "http" and not self._host_lifespan_seen:
            state = self._state_for_current_loop()
            await self._ensure_started(state)
            if state.failed:
                await _send_text_error(send, state.error)
                return
        await self._app(scope, receive, send)


def _build_app():
    """Build the serverless ASGI app, degrading to a clear 500 on failure.

    Uses validate=False (matching create_app / FastMCP Cloud) so import-time
    env-var inspection never crashes the module; the deferred lifespan
    validation still refuses to serve when configuration is incomplete.
    """
    try:
        from agentsafe.config import Settings
        from agentsafe.server import build_server

        settings = Settings()
        server = build_server(settings, validate=False)
        asgi = server.http_app(stateless_http=True, json_response=True)
        return _ServerlessLifespanBootstrap(asgi)
    except Exception as exc:  # noqa: BLE001 - entrypoint must always resolve
        return _error_app(str(exc))


# Vercel Python runtime entrypoint (ASGI).
app = _build_app()
