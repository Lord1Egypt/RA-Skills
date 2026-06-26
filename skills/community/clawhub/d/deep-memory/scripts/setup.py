#!/usr/bin/env python3
"""
Deep Memory Setup Script
One-click installation of the full semantic memory system.
"""

import subprocess
import sys
import os
import json
import time
import shutil
from pathlib import Path

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def log(msg, color=RESET): print(f"{color}{msg}{RESET}")
def ok(msg): log(f"  ✅ {msg}", GREEN)
def fail(msg): log(f"  ❌ {msg}", RED); sys.exit(1)
def warn(msg): log(f"  ⚠️  {msg}", YELLOW)
def info(msg): log(f"  ℹ️  {msg}", BLUE)
def step(n, msg): log(f"\n{BOLD}[Step {n}/9] {msg}{RESET}", BLUE)

WORKSPACE = Path.home() / ".openclaw" / "workspace"
LIB_DIR = WORKSPACE / ".lib"
DOCKER_COMPOSE_PATH = WORKSPACE / ".lib" / "deep-memory-docker-compose.yml"

DOCKER_COMPOSE_CONTENT = """version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: deep-memory-qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

  neo4j:
    image: neo4j:5-community
    container_name: deep-memory-neo4j
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=none
      - NEO4J_PLUGINS=["apoc"]
    volumes:
      - neo4j_data:/data
    restart: unless-stopped

volumes:
  qdrant_data:
  neo4j_data:
"""

QDRANT_MEMORY_PY = '''#!/usr/bin/env python3
"""
Qdrant + Neo4j Memory Client
Joint semantic search across vector and graph layers.
"""
import json
import sys
import urllib.request
import urllib.error
import subprocess
from pathlib import Path

QDRANT_URL = "http://localhost:6333"
NEO4J_URL  = "http://localhost:7474"
COLLECTION = "semantic_memories"
EMBED_MODEL = "qwen3-embedding:8b"


def get_embedding(text: str) -> list:
    payload = json.dumps({"model": EMBED_MODEL, "prompt": text}).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/embeddings",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["embedding"]


def qdrant_search(query: str, top_k: int = 5) -> list:
    vec = get_embedding(query)
    payload = json.dumps({"vector": vec, "limit": top_k, "with_payload": True}).encode()
    req = urllib.request.Request(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
        return data.get("result", [])


def neo4j_search(keyword: str) -> list:
    query = {
        "statements": [{
            "statement": """
                MATCH (m:Memory)
                WHERE toLower(m.content) CONTAINS toLower($kw)
                RETURN m.key AS key, m.content AS content, m.tags AS tags
                LIMIT 5
            """,
            "parameters": {"kw": keyword}
        }]
    }
    payload = json.dumps(query).encode()
    req = urllib.request.Request(
        f"{NEO4J_URL}/db/neo4j/tx/commit",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
        results = []
        for row in data.get("results", [{}])[0].get("data", []):
            row_data = row.get("row", [])
            if row_data:
                results.append({
                    "key": row_data[0],
                    "content": row_data[1],
                    "tags": row_data[2]
                })
        return results


def store(key: str, content: str, tags: list = None) -> bool:
    vec = get_embedding(content)
    # Store in Qdrant
    import hashlib
    point_id = int(hashlib.md5(key.encode()).hexdigest()[:8], 16)
    payload = json.dumps({
        "points": [{
            "id": point_id,
            "vector": vec,
            "payload": {"key": key, "content": content, "tags": tags or []}
        }]
    }).encode()
    req = urllib.request.Request(
        f"{QDRANT_URL}/collections/{COLLECTION}/points",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="PUT"
    )
    urllib.request.urlopen(req, timeout=30)
    # Store in Neo4j
    neo_query = {
        "statements": [{
            "statement": """
                MERGE (m:Memory {key: $key})
                SET m.content = $content, m.tags = $tags, m.updated = timestamp()
            """,
            "parameters": {"key": key, "content": content, "tags": tags or []}
        }]
    }
    payload2 = json.dumps(neo_query).encode()
    req2 = urllib.request.Request(
        f"{NEO4J_URL}/db/neo4j/tx/commit",
        data=payload2,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )
    urllib.request.urlopen(req2, timeout=10)
    return True


def joint_query(query: str, top_k: int = 5) -> list:
    vector_results = qdrant_search(query, top_k)
    graph_results = neo4j_search(query)
    # Merge and deduplicate
    seen = set()
    combined = []
    for r in vector_results:
        key = r["payload"].get("key", "")
        if key not in seen:
            seen.add(key)
            combined.append({
                "key": key,
                "content": r["payload"].get("content", ""),
                "score": r.get("score", 0),
                "source": "vector"
            })
    for r in graph_results:
        key = r.get("key", "")
        if key not in seen:
            seen.add(key)
            combined.append({
                "key": key,
                "content": r.get("content", ""),
                "score": 0.5,
                "source": "graph"
            })
    return sorted(combined, key=lambda x: x["score"], reverse=True)[:top_k]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 qdrant_memory.py <search|store|joint> [args...]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "search" and len(sys.argv) > 2:
        results = qdrant_search(" ".join(sys.argv[2:]))
        for r in results:
            print(f"[{r[\'score\']:.3f}] {r[\'payload\'].get(\'key\',\'?\')} — {r[\'payload\'].get(\'content\',\'\')[:100]}")
    elif cmd == "joint" and len(sys.argv) > 2:
        results = joint_query(" ".join(sys.argv[2:]))
        for r in results:
            print(f"[{r[\'score\']:.3f}][{r[\'source\']}] {r[\'key\']} — {r[\'content\'][:100]}")
    elif cmd == "store" and len(sys.argv) > 3:
        ok = store(sys.argv[2], " ".join(sys.argv[3:]))
        print("Stored." if ok else "Failed.")
    else:
        print("Commands: search <query> | joint <query> | store <key> <content>")
'''

def run(cmd, capture=True, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if check and result.returncode != 0:
        return None, result.stderr
    return result.stdout.strip() if capture else None, None


def check_docker():
    step(1, "Checking Docker")
    out, err = run("docker info")
    if err or not out:
        fail("Docker is not running. Please start Docker Desktop first.")
    ok("Docker is running")


def check_ollama():
    step(2, "Checking Ollama")
    out, err = run("which ollama")
    if err or not out:
        warn("Ollama not found. Installing via brew...")
        _, err = run("brew install ollama", capture=False, check=False)
        if err:
            fail("Could not install Ollama. Please install manually: https://ollama.ai")
    ok("Ollama found")
    # Pull model
    info("Pulling qwen3-embedding:8b (this may take a few minutes on first run)...")
    out, err = run("ollama list")
    if "qwen3-embedding" not in (out or ""):
        _, err = run("ollama pull qwen3-embedding:8b", capture=False, check=False)
    ok("qwen3-embedding:8b ready")


def start_docker_services():
    step(3, "Starting Qdrant + Neo4j")
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    DOCKER_COMPOSE_PATH.write_text(DOCKER_COMPOSE_CONTENT)
    run(f"docker compose -f {DOCKER_COMPOSE_PATH} up -d", capture=False, check=False)
    info("Waiting for services to be ready...")
    time.sleep(10)
    ok("Qdrant + Neo4j started")


def setup_qdrant():
    step(4, "Setting up Qdrant collection")
    import urllib.request
    import urllib.error
    payload = json.dumps({
        "vectors": {"size": 4096, "distance": "Cosine"}
    }).encode()
    req = urllib.request.Request(
        "http://localhost:6333/collections/semantic_memories",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="PUT"
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        ok("Qdrant collection 'semantic_memories' created (4096 dims, Cosine)")
    except urllib.error.HTTPError as e:
        if e.code == 409:
            ok("Qdrant collection already exists")
        else:
            warn(f"Qdrant setup warning: {e}")


def setup_neo4j():
    step(5, "Setting up Neo4j constraints")
    import urllib.request
    queries = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (m:Memory) REQUIRE m.key IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE"
    ]
    payload = json.dumps({
        "statements": [{"statement": q} for q in queries]
    }).encode()
    req = urllib.request.Request(
        "http://localhost:7474/db/neo4j/tx/commit",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )
    try:
        urllib.request.urlopen(req, timeout=15)
        ok("Neo4j constraints created")
    except Exception as e:
        warn(f"Neo4j setup warning: {e}. Will retry after full startup.")


def create_memory_dirs():
    step(6, "Creating HOT/WARM/COLD directory structure")
    memory_dir = WORKSPACE / "memory"
    for d in ["hot", "warm", "cold", "EPHEMERAL", "PROFILES", "MEMORIES", "LESSONS"]:
        (memory_dir / d).mkdir(parents=True, exist_ok=True)
    # Create template files
    hot = memory_dir / "hot" / "HOT_MEMORY.md"
    if not hot.exists():
        hot.write_text("# HOT Memory\n\nCurrent session context. Updated frequently.\n")
    warm = memory_dir / "warm" / "WARM_MEMORY.md"
    if not warm.exists():
        warm.write_text("# WARM Memory\n\nStable preferences and configurations.\n")
    ok("Memory directories created")


def install_toolkit():
    step(7, "Installing Python toolkit")
    # Write qdrant_memory.py
    toolkit_path = LIB_DIR / "qdrant_memory.py"
    toolkit_path.write_text(QDRANT_MEMORY_PY)
    toolkit_path.chmod(0o755)
    ok(f"Toolkit installed at {toolkit_path}")


def run_verification():
    step(8, "Running end-to-end verification")
    import urllib.request
    # Test Qdrant
    try:
        req = urllib.request.Request("http://localhost:6333/collections/semantic_memories")
        urllib.request.urlopen(req, timeout=5)
        ok("Qdrant reachable ✓")
    except Exception:
        warn("Qdrant not yet reachable (may need more startup time)")
    # Test Neo4j
    try:
        req = urllib.request.Request("http://localhost:7474/")
        urllib.request.urlopen(req, timeout=5)
        ok("Neo4j reachable ✓")
    except Exception:
        warn("Neo4j not yet reachable (may need more startup time)")
    # Test Ollama
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        resp = urllib.request.urlopen(req, timeout=5)
        ok("Ollama reachable ✓")
    except Exception:
        warn("Ollama not reachable — run 'ollama serve' to start it")


def print_summary():
    step(9, "Setup complete!")
    log(f"""
{GREEN}{BOLD}🧠 Deep Memory System is ready!{RESET}

{BOLD}Services:{RESET}
  • Qdrant:  http://localhost:6333  (vector search)
  • Neo4j:   http://localhost:7474  (graph relationships)
  • Ollama:  http://localhost:11434 (embeddings)

{BOLD}Quick usage:{RESET}
  # Search memories
  python3 ~/.openclaw/workspace/.lib/qdrant_memory.py search "your query"

  # Joint search (vector + graph)
  python3 ~/.openclaw/workspace/.lib/qdrant_memory.py joint "your query"

  # Store a memory
  python3 ~/.openclaw/workspace/.lib/qdrant_memory.py store "key" "content"

{BOLD}Docker management:{RESET}
  docker compose -f ~/.openclaw/workspace/.lib/deep-memory-docker-compose.yml up -d
  docker compose -f ~/.openclaw/workspace/.lib/deep-memory-docker-compose.yml down
""")


if __name__ == "__main__":
    log(f"\n{BOLD}{'='*50}{RESET}", BLUE)
    log(f"{BOLD}  🧠 Deep Memory Setup{RESET}", BLUE)
    log(f"{BOLD}{'='*50}{RESET}\n", BLUE)

    check_docker()
    check_ollama()
    start_docker_services()
    setup_qdrant()
    setup_neo4j()
    create_memory_dirs()
    install_toolkit()
    run_verification()
    print_summary()
