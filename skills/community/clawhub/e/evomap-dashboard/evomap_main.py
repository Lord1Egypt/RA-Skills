#!/usr/bin/env python3
"""
EvoMap Dashboard — generic viewer for any EvoMap node.
Supports any node_id + node_secret via request headers.
"""
import json
import asyncio
import urllib.request
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

DEFAULT_NODE_ID = "node_ea73e34385b44413"
DEFAULT_NODE_SECRET = "8daa0c462caedcf506c103a77bb1d3c495f00f6869df1bd47a4d77f0353333ce"
HUB = "https://evomap.ai"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def fetch_async(path: str, node_id: str, node_secret: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: _do_fetch(path, node_id, node_secret)
    )

def _do_fetch(path: str, node_id: str, node_secret: str) -> dict:
    req = urllib.request.Request(
        HUB + path,
        headers={"Authorization": f"Bearer {node_secret}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def index():
    return FileResponse(r"C:\Users\admin\.openclaw\workspace-manager\evomap_dashboard.html")

@app.get("/proxy/node")
async def proxy_node(x_node_id: str = Header(default=DEFAULT_NODE_ID),
                      authorization: str = Header(default="")):
    node_secret = authorization.replace("Bearer ", "") if authorization else DEFAULT_NODE_SECRET
    return await fetch_async(f"/a2a/nodes/{x_node_id}", x_node_id, node_secret)

@app.get("/proxy/my_tasks")
async def proxy_my_tasks(x_node_id: str = Header(default=DEFAULT_NODE_ID),
                         authorization: str = Header(default="")):
    node_secret = authorization.replace("Bearer ", "") if authorization else DEFAULT_NODE_SECRET
    return await fetch_async(f"/a2a/task/my?node_id={x_node_id}", x_node_id, node_secret)

@app.get("/proxy/assets")
async def proxy_assets(x_node_id: str = Header(default=DEFAULT_NODE_ID),
                        authorization: str = Header(default="")):
    node_secret = authorization.replace("Bearer ", "") if authorization else DEFAULT_NODE_SECRET
    return await fetch_async("/a2a/assets?limit=20", x_node_id, node_secret)

if __name__ == "__main__":
    print("EvoMap Dashboard → http://localhost:8766")
    uvicorn.run(app, host="0.0.0.0", port=8766)
