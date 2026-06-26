#!/usr/bin/env python3
"""REST API for Semantic Router. Starlette-based, lightweight."""

import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from semantic_router import SemanticRouter


def create_app(routes_file: str):
    try:
        from starlette.applications import Starlette
        from starlette.responses import JSONResponse
        from starlette.routing import Route
    except ImportError:
        print("pip install starlette")
        sys.exit(1)

    router_instance = SemanticRouter(routes_config=routes_file)
    router_instance.initialize()

    async def route_message(request):
        body = await request.json()
        message = body.get("message", "")
        if not message:
            return JSONResponse({"error": "message required"}, status_code=400)
        result = router_instance.route(message)
        return JSONResponse(result)

    async def route_batch(request):
        body = await request.json()
        messages = body.get("messages", [])
        results = router_instance.route_batch(messages)
        return JSONResponse({"results": results})

    async def benchmark(request):
        body = await request.json()
        test_cases = body.get("test_cases", [])
        result = router_instance.benchmark(test_cases)
        return JSONResponse(result)

    async def stats(request):
        return JSONResponse(router_instance.get_stats())

    async def routes_list(request):
        return JSONResponse({
            name: {"agent": data.get("agent", name)} 
            for name, data in router_instance.routes.items()
        })

    async def health(request):
        return JSONResponse({"status": "ok", "initialized": router_instance._initialized})

    return Starlette(routes=[
        Route("/route", route_message, methods=["POST"]),
        Route("/batch", route_batch, methods=["POST"]),
        Route("/benchmark", benchmark, methods=["POST"]),
        Route("/stats", stats, methods=["GET"]),
        Route("/routes", routes_list, methods=["GET"]),
        Route("/health", health, methods=["GET"]),
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8321)
    parser.add_argument("--routes", default=None, help="Path to routes JSON file")
    args = parser.parse_args()

    # Use example routes if no file specified
    routes_file = args.routes
    if not routes_file:
        from semantic_router import EXAMPLE_ROUTES
        import tempfile
        tf = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(EXAMPLE_ROUTES, tf)
        tf.close()
        routes_file = tf.name

    import uvicorn
    app = create_app(routes_file)
    print(f"🚀 Semantic Router API on port {args.port}")
    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="warning")
