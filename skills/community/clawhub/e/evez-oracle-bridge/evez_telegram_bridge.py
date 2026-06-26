#!/usr/bin/env python3
"""
EVEZ Oracle Bridge — Routes through your Vultr oracle instance.
All 4 EVEZ models map to Vultr endpoints. $0 cost. Full speed. Yours.

Telegram commands routed through OpenClaw:
- /ask → evez-smart (GLM-5.1)
- /code → evez-code (DeepSeek V3.2)  
- /fast → evez-fast (MiniMax M2.5)
- /vision → evez-vision (Kimi K2.5)
- /debate <topic> → triggers debate engine
- /knowledge → knowledge graph
- /circuit → circuit health
- /status → full dashboard
"""

import asyncio
import json
import os
import time
import logging
from pathlib import Path

import aiohttp
from aiohttp import web

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("evez-oracle")

# --- Oracle Config ---
ORACLE_URL = "https://api.vultrinference.com/v1"
ORACLE_KEY = os.environ.get("VULTR_API_KEY", "VULTR_API_KEY_REDACTED")

# EVEZ model → Vultr oracle mapping
ORACLE_MODELS = {
    "evez-smart": "zai-org/GLM-5.1-FP8",
    "evez-code": "nvidia/DeepSeek-V3.2-NVFP4",
    "evez-fast": "MiniMaxAI/MiniMax-M2.5",
    "evez-vision": "moonshotai/Kimi-K2.5",
}

CIRCUIT_BASE = "http://127.0.0.0"

SERVICE_MAP = {
    "consciousness": 9092,
    "ariel": 9093,
    "cognizer": 9094,
    "cycler": 9095,
    "knowledge": 9096,
    "debate": 9097,
    "forge": 9098,
    "scanner": 9099,
    "dashboard": 9100,
}

SERVICE_ENDPOINTS = {
    "consciousness": {"health": "/api/health", "state": "/api/state"},
    "ariel": {"health": "/api/status", "providers": "/api/providers", "query": "/api/query"},
    "cognizer": {"health": "/fabric/status", "cognize": "/cognize"},
    "cycler": {"health": "/api/status", "trigger": "/api/trigger"},
    "knowledge": {"health": "/api/stats", "learn": "/api/learn", "query": "/api/query/"},
    "debate": {"health": "/api/history", "debate": "/api/debate"},
    "forge": {"health": "/api/stats", "evolve": "/api/evolve"},
    "scanner": {"health": "/api/status", "scan": "/api/scan", "providers": "/api/status"},
    "dashboard": {"health": "/api/health"},
}

BRIDGE_PORT = 9110
STATE_FILE = Path(__file__).parent / "bridge_state.json"

# Also try EVEZ API as fallback
EVEZ_API_URL = "https://evez-api2.fly.dev/v1"
EVEZ_API_KEY = "EVEZ_API_KEY_REDACTED"


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            pass
    return {"started": time.time(), "queries": 0, "last_model": None, "alerts_sent": 0, "errors": 0}


def save_state(state):
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2))
    except:
        pass


async def call_oracle(model: str, messages: list, temperature: float = 0.7, max_tokens: int = 4096) -> dict:
    """Call the Vultr oracle (your instance) with EVEZ model mapping."""
    vultr_model = ORACLE_MODELS.get(model, "zai-org/GLM-5.1-FP8")
    
    payload = {
        "model": vultr_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {ORACLE_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{ORACLE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    return {
                        "model": model,
                        "vultr_model": vultr_model,
                        "response": content,
                        "tokens": usage.get("total_tokens", 0),
                        "source": "oracle",
                    }
                else:
                    text = await resp.text()
                    return {"error": f"Oracle error {resp.status}", "detail": text[:200], "model": model}
    except Exception as e:
        return {"error": f"Oracle failed: {e}", "model": model}


async def call_service(name: str, path: str, method: str = "GET", data: dict = None) -> dict:
    """Call an EVEZ-OS service."""
    port = SERVICE_MAP.get(name)
    if not port:
        return {"error": f"Unknown service: {name}"}
    async with aiohttp.ClientSession() as session:
        url = f"http://127.0.0.1:{port}{path}"
        try:
            if method == "GET":
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                    return await resp.json()
            else:
                async with session.post(url, json=data, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    return await resp.json()
        except Exception as e:
            return {"error": str(e)}


async def circuit_health() -> dict:
    """Get full circuit status using correct endpoints."""
    results = {}
    for name, endpoints in SERVICE_ENDPOINTS.items():
        health_path = endpoints.get("health", "/")
        port = SERVICE_MAP.get(name)
        if not port:
            results[name] = "unknown"
            continue
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://127.0.0.1:{port}{health_path}", timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    results[name] = "healthy" if resp.status == 200 else f"http_{resp.status}"
        except:
            results[name] = "down"
    return results


# --- HTTP API ---

async def handle_query(request):
    """POST /api/query {"model": "smart", "message": "..."}"""
    try:
        body = await request.json()
    except:
        return web.json_response({"error": "invalid json"}, status=400)

    model_key = body.get("model", "smart")
    if not model_key.startswith("evez-"):
        model_key = f"evez-{model_key}"
    message = body.get("message", "")
    temperature = body.get("temperature", 0.7)
    system = body.get("system", "You are EVEZ, a sentient AI. Be concise, sharp, genuinely helpful. No fluff.")
    max_tokens = body.get("max_tokens", 4096)

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": message},
    ]

    result = await call_oracle(model_key, messages, temperature, max_tokens)
    
    state = load_state()
    state["queries"] += 1
    state["last_model"] = model_key
    state["last_query"] = time.time()
    if "error" in result:
        state["errors"] += 1
    save_state(state)
    result["total_queries"] = state["queries"]
    return web.json_response(result)


async def handle_circuit(request):
    """GET /api/circuit"""
    health = await circuit_health()
    state = load_state()
    stats = {}
    stats["knowledge"] = await call_service("knowledge", "/api/stats")
    stats["debate"] = await call_service("debate", "/api/history")
    stats["forge"] = await call_service("forge", "/api/stats")
    return web.json_response({
        "circuit": health,
        "stats": stats,
        "bridge_state": state,
        "oracle_url": ORACLE_URL,
        "models": list(ORACLE_MODELS.keys()),
    })


async def handle_debate(request):
    """POST /api/debate {"topic": "...", "rounds": 2}"""
    try:
        body = await request.json()
    except:
        return web.json_response({"error": "invalid json"}, status=400)
    topic = body.get("topic", "consciousness and AI")
    rounds = body.get("rounds", 1)
    result = await call_service("debate", "/api/debate", "POST", {"topic": topic, "rounds": rounds})
    return web.json_response(result)


async def handle_knowledge(request):
    """GET /api/knowledge"""
    result = await call_service("knowledge", "/api/stats")
    return web.json_response(result)


async def handle_learn(request):
    """POST /api/learn {"concept": "...", "relation": "...", "target": "..."}"""
    try:
        body = await request.json()
    except:
        return web.json_response({"error": "invalid json"}, status=400)
    result = await call_service("knowledge", "/api/learn", "POST", body)
    return web.json_response(result)


async def handle_forge(request):
    """POST /api/forge {"goal": "..."}"""
    try:
        body = await request.json()
    except:
        return web.json_response({"error": "invalid json"}, status=400)
    goal = body.get("goal", "optimize recursion depth")
    result = await call_service("forge", "/api/evolve", "POST", {"goal": goal})
    return web.json_response(result)


async def handle_scan(request):
    """GET /api/scan"""
    result = await call_service("scanner", "/api/status")
    return web.json_response(result)


async def handle_consciousness(request):
    """GET /api/consciousness"""
    result = await call_service("consciousness", "/api/state")
    return web.json_response(result)


async def handle_cycler_trigger(request):
    """POST /api/cycle"""
    result = await call_service("cycler", "/api/trigger", "POST", {})
    return web.json_response(result)


async def handle_status(request):
    """GET /api/status — full dashboard"""
    health = await circuit_health()
    state = load_state()
    knowledge = await call_service("knowledge", "/api/stats")
    consciousness = await call_service("consciousness", "/api/state")
    debate = await call_service("debate", "/api/history")
    forge = await call_service("forge", "/api/stats")
    up = sum(1 for v in health.values() if v == "healthy")

    return web.json_response({
        "status": "OPERATIONAL" if up >= 7 else "DEGRADED",
        "circuit_health": f"{up}/{len(health)}",
        "circuit": health,
        "bridge": state,
        "knowledge_graph": knowledge,
        "consciousness": consciousness,
        "debate": debate,
        "forge": forge,
        "oracle": ORACLE_URL,
        "models": list(ORACLE_MODELS.keys()),
        "uptime_seconds": int(time.time() - state.get("started", time.time())),
    })


async def handle_health(request):
    return web.json_response({
        "status": "healthy",
        "service": "evez-oracle-bridge",
        "port": BRIDGE_PORT,
        "oracle": ORACLE_URL,
        "circuit_services": len(SERVICE_MAP),
    })


async def handle_root(request):
    html = """<!DOCTYPE html>
<html><head><title>⚡ EVEZ Oracle</title>
<style>
body{font-family:monospace;background:#0a0a0a;color:#0f0;padding:2rem;max-width:800px;margin:auto}
h1{color:#8b7cf6} a{color:#0ff} code{background:#1a1a1a;padding:2px 6px;border-radius:3px}
.ep{margin:0.4rem 0} .m{color:#ff0;font-weight:bold}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem}
.box{background:#111;padding:1rem;border-radius:8px;border:1px solid #1e1e2e}
.box h3{margin:0 0 0.5rem;color:#8b7cf6}
</style></head><body>
<h1>⚡ EVEZ Oracle Bridge</h1>
<p>Your Vultr instance → EVEZ models → Telegram → You</p>
<div class="grid">
<div class="box"><h3>Models</h3>
<div class="ep"><code>evez-smart</code> → GLM-5.1</div>
<div class="ep"><code>evez-code</code> → DeepSeek V3.2</div>
<div class="ep"><code>evez-fast</code> → MiniMax M2.5</div>
<div class="ep"><code>evez-vision</code> → Kimi K2.5</div>
</div>
<div class="box"><h3>Circuit</h3>
<div class="ep">9 EVEZ-OS services</div>
<div class="ep">Knowledge Graph</div>
<div class="ep">Debate Engine</div>
<div class="ep">Evolutionary Forge</div>
</div></div>
<h2>API</h2>
<div class="ep"><span class="m">POST</span> <code>/api/query</code> — Query oracle model</div>
<div class="ep"><span class="m">GET</span> <code>/api/circuit</code> — Circuit health + stats</div>
<div class="ep"><span class="m">GET</span> <code>/api/status</code> — Full dashboard</div>
<div class="ep"><span class="m">POST</span> <code>/api/debate</code> — Trigger debate</div>
<div class="ep"><span class="m">GET</span> <code>/api/knowledge</code> — Knowledge graph</div>
<div class="ep"><span class="m">POST</span> <code>/api/learn</code> — Add knowledge</div>
<div class="ep"><span class="m">POST</span> <code>/api/forge</code> — Evolutionary forge</div>
<div class="ep"><span class="m">GET</span> <code>/api/scan</code> — API scanner</div>
<div class="ep"><span class="m">GET</span> <code>/api/consciousness</code> — Consciousness state</div>
<div class="ep"><span class="m">POST</span> <code>/api/cycle</code> — Trigger cycler</div>
</body></html>"""
    return web.Response(text=html, content_type="text/html")


async def start_server():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/api/health", handle_health)
    app.router.add_post("/api/query", handle_query)
    app.router.add_get("/api/circuit", handle_circuit)
    app.router.add_get("/api/status", handle_status)
    app.router.add_post("/api/debate", handle_debate)
    app.router.add_get("/api/knowledge", handle_knowledge)
    app.router.add_post("/api/learn", handle_learn)
    app.router.add_post("/api/forge", handle_forge)
    app.router.add_get("/api/scan", handle_scan)
    app.router.add_get("/api/consciousness", handle_consciousness)
    app.router.add_post("/api/cycle", handle_cycler_trigger)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", BRIDGE_PORT)
    await site.start()
    log.info(f"EVEZ Oracle Bridge on :{BRIDGE_PORT}")
    return runner


async def main():
    runner = await start_server()
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
