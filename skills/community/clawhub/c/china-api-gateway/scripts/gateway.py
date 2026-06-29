#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国AI API统一网关 - FastAPI实现
OpenAI兼容接口，聚合多个国内AI平台
依赖: pip install fastapi uvicorn httpx pyyaml
"""

import json
import time
import yaml
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="China AI API Gateway", version="1.0.0")

CONFIG = {}
PROVIDERS = {}
STATS = {"total_requests": 0, "success": 0, "failed": 0, "start_time": time.time()}

def load_config(path: str = "config.yaml"):
    global CONFIG, PROVIDERS
    try:
        with open(path, "r") as f:
            CONFIG = yaml.safe_load(f)
        for p in CONFIG.get("providers", []):
            for model in p.get("models", []):
                PROVIDERS[model] = p
    except FileNotFoundError:
        CONFIG = {"providers": [], "routing": {"strategy": "priority", "fallback": True, "timeout": 30}}

def get_provider(model: str):
    if model == "auto":
        sorted_providers = sorted(CONFIG.get("providers", []), key=lambda x: x.get("priority", 99))
        return sorted_providers[0] if sorted_providers else None
    return PROVIDERS.get(model)

async def call_provider(provider: dict, payload: dict) -> dict:
    base_url = provider["base_url"].rstrip("/")
    api_key = provider.get("api_key", "")
    timeout = CONFIG.get("routing", {}).get("timeout", 30)
    url = f"{base_url}/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()

@app.on_event("startup")
async def startup():
    load_config()

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    model = body.get("model", "auto")
    STATS["total_requests"] += 1
    provider = get_provider(model)
    if not provider:
        STATS["failed"] += 1
        raise HTTPException(status_code=404, detail=f"Model '{model}' not found")
    actual_model = provider["models"][0] if model == "auto" else model
    payload = {
        "model": actual_model,
        "messages": body.get("messages", []),
        "stream": body.get("stream", False),
        **{k: v for k, v in body.items() if k not in ("model", "messages", "stream")}
    }
    try:
        result = await call_provider(provider, payload)
        STATS["success"] += 1
        return JSONResponse(content=result)
    except httpx.HTTPStatusError as e:
        STATS["failed"] += 1
        if CONFIG.get("routing", {}).get("fallback", True):
            for p in sorted(CONFIG.get("providers", []), key=lambda x: x.get("priority", 99)):
                if p == provider:
                    continue
                try:
                    payload["model"] = p["models"][0]
                    result = await call_provider(p, payload)
                    STATS["success"] += 1
                    return JSONResponse(content=result)
                except Exception:
                    continue
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")
    except Exception as e:
        STATS["failed"] += 1
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/models")
async def list_models():
    models = []
    for p in CONFIG.get("providers", []):
        for m in p.get("models", []):
            models.append({"id": m, "object": "model", "owned_by": p["name"]})
    return {"object": "list", "data": models}

@app.get("/health")
async def health_check():
    uptime = time.time() - STATS["start_time"]
    return {
        "status": "ok",
        "uptime_seconds": round(uptime),
        "total_requests": STATS["total_requests"],
        "success_rate": f"{STATS['success']/max(STATS['total_requests'],1)*100:.1f}%",
        "providers": len(CONFIG.get("providers", [])),
        "models": len(PROVIDERS)
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=18080)
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()
    load_config(args.config)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=args.port)
