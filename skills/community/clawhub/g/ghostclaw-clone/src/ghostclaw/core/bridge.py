import sys
import json
import asyncio
import logging
from typing import Any, Dict, Optional, Callable, Awaitable

logger = logging.getLogger("ghostclaw.bridge")

class JSONRPCError(Exception):
    def __init__(self, code: int, message: str, data: Any = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)

class BridgeHandler:
    def __init__(self):
        self.methods: Dict[str, Callable[..., Awaitable[Any]]] = {}

    def register(self, method_name: str, handler: Callable[..., Awaitable[Any]]):
        self.methods[method_name] = handler

    async def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if "jsonrpc" not in request or request["jsonrpc"] != "2.0":
            return self._build_error(None, -32600, "Invalid Request")

        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if not method:
            return self._build_error(request_id, -32600, "Invalid Request")

        if method not in self.methods:
            return self._build_error(request_id, -32601, "Method not found")

        try:
            handler = self.methods[method]
            # If params is a dict, pass as kwargs, else as single arg if expected
            if isinstance(params, dict):
                result = await handler(**params)
            else:
                result = await handler(params)

            if request_id is not None:
                return {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id
                }
        except JSONRPCError as e:
            return self._build_error(request_id, e.code, e.message, e.data)
        except Exception as e:
            logger.exception("Internal error in JSON-RPC handler")
            return self._build_error(request_id, -32603, "Internal error", str(e))

        return None

    def _build_error(self, request_id: Any, code: int, message: str, data: Any = None) -> Dict[str, Any]:
        error = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        return {
            "jsonrpc": "2.0",
            "error": error,
            "id": request_id
        }

    def emit_event(self, method: str, params: Any):
        """Emit a JSON-RPC 2.0 notification."""
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        sys.stdout.write(json.dumps(notification) + "\n")
        sys.stdout.flush()

    async def run(self):
        """Read lines from stdin and process them as JSON-RPC requests."""
        # Fix for some environments where sys.stdin might be wrapped
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        loop = asyncio.get_running_loop()
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        while True:
            try:
                line = await reader.readline()
                if not line:
                    break

                line_str = line.decode('utf-8').strip()
                if not line_str:
                    continue

                try:
                    data = json.loads(line_str)
                except json.JSONDecodeError:
                    response = self._build_error(None, -32700, "Parse error")
                    self._send_response(response)
                    continue

                if isinstance(data, list):
                    # Batch request
                    responses = []
                    for req in data:
                        resp = await self._handle_request(req)
                        if resp:
                            responses.append(resp)
                    if responses:
                        self._send_response(responses)
                else:
                    # Single request
                    response = await self._handle_request(data)
                    if response is not None:
                        self._send_response(response)

            except Exception as e:
                logger.error(f"Bridge loop error: {e}")
                break

    def _send_response(self, response: Any):
        """Helper to write to stdout."""
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()

class GhostBridge(BridgeHandler):
    """
    Ghostclaw-specific Bridge implementation.
    Connects JSON-RPC methods to internal Ghostclaw logic.
    """
    def __init__(self, analyzer: Optional[Any] = None):
        super().__init__()
        self.analyzer = analyzer
        self.register("analyze", self.analyze)
        self.register("status", self.status)
        self.register("plugins", self.plugins)
        self.register("ping", self.ping)

    async def ping(self):
        return "pong"

    async def plugins(self):
        from ghostclaw.core.adapters.registry import registry
        registry.register_internal_plugins()
        return registry.get_plugin_metadata()

    async def get_metadata(self):
        # Keeps for internal use
        from ghostclaw.version import __version__
        return {
            "version": __version__,
            "name": "ghostclaw",
            "capabilities": ["analyze", "refactor_proposal"]
        }

    async def status(self):
        from ghostclaw.version import __version__
        return {"status": "ready", "version": __version__, "pid": sys.argv[0]}

    async def analyze(self, path: str = ".", verbose: bool = False):
        """Run a full codebase analysis via the bridge."""
        if not self.analyzer:
            from ghostclaw.core.analyzer import CodebaseAnalyzer
            self.analyzer = CodebaseAnalyzer(path)

        try:
            # We assume analyzer.analyze returns a result dict
            result = await self.analyzer.analyze()
            return result
        except Exception as e:
            raise JSONRPCError(-32000, f"Analysis failed: {str(e)}")

async def start_bridge():
    """Entry point for the ghostclaw bridge command."""
    bridge = GhostBridge()
    await bridge.run()

if __name__ == "__main__":
    asyncio.run(start_bridge())
