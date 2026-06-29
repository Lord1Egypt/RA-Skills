"""
setup.py — One-time setup for OpenClaw Memory System

Does:
  1. Create config.json from template (or prompt for values)
  2. Check and install Python dependencies
  3. Start Qdrant (docker-compose) if not running
  4. Initialize Qdrant collection
  5. Check embedding server
  6. Create data directories
  7. Print next-steps (hooks, cron, HEARTBEAT.md)

Usage:
  python scripts/setup.py
  python scripts/setup.py --vault-dir /path/to/vault
  python scripts/setup.py --vault-dir /path/to/vault --qdrant-url http://localhost:6333
"""
import json
import os
import sys
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS_DIR.parent
CONFIG_FILE = SCRIPTS_DIR / "config.json"
TEMPLATE_FILE = SCRIPTS_DIR / "config.template.json"
DATA_DIR = SKILL_DIR / "data"
DOCKER_COMPOSE = SKILL_DIR / "docker-compose.yml"


def check_python_deps():
    required = ["requests", "numpy"]
    optional = ["mem0ai"]
    missing_req = []
    missing_opt = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing_req.append(pkg)
    for pkg in optional:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            missing_opt.append(pkg)
    return missing_req, missing_opt


def install_deps():
    req_file = SKILL_DIR / "requirements.txt"
    if req_file.exists():
        print("  Installing dependencies...")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                          capture_output=True, text=True)
        if r.returncode == 0:
            print("  ✅ Dependencies installed")
        else:
            print(f"  ⚠️  pip install failed: {r.stderr[:200]}")
            return False
    return True


def check_qdrant(url="http://localhost:6333"):
    try:
        import urllib.request
        resp = urllib.request.urlopen(f"{url}/collections", timeout=5)
        return resp.status == 200
    except Exception:
        return False


def start_qdrant_docker():
    if not DOCKER_COMPOSE.exists():
        return False
    try:
        r = subprocess.run(["docker", "compose", "-f", str(DOCKER_COMPOSE), "up", "-d"],
                          capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            print("  ✅ Qdrant started via docker-compose")
            import time
            time.sleep(3)  # wait for startup
            return True
        else:
            print(f"  ⚠️  docker-compose failed: {r.stderr[:200]}")
    except FileNotFoundError:
        print("  ⚠️  Docker not found. Install Docker or start Qdrant manually:")
        print("     docker run -p 6333:6333 qdrant/qdrant")
    except Exception as e:
        print(f"  ⚠️  {e}")
    return False


def init_qdrant_collection(url="http://localhost:6333", collection="knowledge_base"):
    try:
        import urllib.request
        # Check if exists
        try:
            req = urllib.request.Request(f"{url}/collections/{collection}")
            resp = urllib.request.urlopen(req, timeout=5)
            if resp.status == 200:
                print(f"  ✅ Collection '{collection}' already exists")
                return True
        except Exception:
            pass

        # Create
        payload = json.dumps({"vectors": {"size": 768, "distance": "Cosine"}}).encode("utf-8")
        req = urllib.request.Request(f"{url}/collections/{collection}", data=payload, method="PUT")
        req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req, timeout=10)
        if resp.status == 200:
            print(f"  ✅ Created collection '{collection}' (768 dims, Cosine)")
            return True
    except Exception as e:
        print(f"  ⚠️  Failed: {e}")
    return False


def check_embedding_server():
    try:
        import urllib.request
        # Try reading config to get URL
        if CONFIG_FILE.exists():
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            url = cfg.get("embedder", {}).get("baseUrl", "http://localhost:1234/v1")
        else:
            url = "http://localhost:1234/v1"
        models_url = url.rstrip("/") + "/models"
        req = urllib.request.Request(models_url)
        key = None
        if CONFIG_FILE.exists():
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            key = cfg.get("embedder", {}).get("apiKey")
        if key and key != "***":
            req.add_header("Authorization", f"Bearer {key}")
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status == 200
    except Exception:
        return False


def create_config(vault_dir=None):
    if CONFIG_FILE.exists():
        print(f"  config.json already exists")
        # Check if it has placeholder values
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        if cfg.get("embedder", {}).get("apiKey") == "***":
            print(f"  ⚠️  API keys are placeholders — edit {CONFIG_FILE}")
        return True

    if not TEMPLATE_FILE.exists():
        print(f"  ERROR: Template not found at {TEMPLATE_FILE}")
        return False

    template = json.loads(TEMPLATE_FILE.read_text(encoding="utf-8"))
    if vault_dir:
        template["vault_dir"] = str(Path(vault_dir).resolve())

    CONFIG_FILE.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Created config.json from template")
    print(f"  ⚠️  Edit {CONFIG_FILE} to set your API keys and paths")
    return True


def print_cron_setup():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  CRON SETUP (choose one method)                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                             ║
║  Method A: OpenClaw Cron (recommended)                      ║
║                                                             ║
║    openclaw cron add --name heartbeat \\                     ║
║      --schedule "every 45m" \\                               ║
║      --agent routine \\                                      ║
║      --task "run python C:/path/to/scripts/maintenance_orchestrator.py --cycle light --parallel"
║                                                             ║
║    openclaw cron add --name heartbeat-heavy \\               ║
║      --schedule "every 6h" \\                                ║
║      --agent routine \\                                      ║
║      --task "run python C:/path/to/scripts/maintenance_orchestrator.py --cycle heavy --parallel"
║                                                             ║
║  Method B: HEARTBEAT.md                                     ║
║                                                             ║
║    Add to ~/.openclaw/workspace/HEARTBEAT.md:               ║
║                                                             ║
║      # === Memory System ===                                ║
║      python scripts/vault_guardian.py                       ║
║      python scripts/extract_memories.py                     ║
║      python scripts/memory_health.py                        ║
║                                                             ║
║  Method C: Windows Task Scheduler                           ║
║                                                             ║
║    schtasks /create /tn "OpenClaw-Heartbeat" \\              ║
║      /tr "python C:/path/to/scripts/maintenance_orchestrator.py --cycle light" \\
║      /sc minute /mo 45 /st 00:00                           ║
║                                                             ║
╚══════════════════════════════════════════════════════════════╝""")


def print_hooks_setup():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  HOOKS SETUP                                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                             ║
║  Enable these hooks (OpenClaw built-in):                    ║
║                                                             ║
║    openclaw hooks enable session-memory                     ║
║    openclaw hooks enable memory-compact                     ║
║    openclaw hooks enable memory-extract                     ║
║                                                             ║
║  These hooks auto-save session context to memory/ on        ║
║  /new or /reset, and extract memories before compaction.    ║
║                                                             ║
║  Verify:                                                    ║
║    openclaw hooks list                                      ║
║                                                             ║
╚══════════════════════════════════════════════════════════════╝""")


def print_vault_structure():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  EXPECTED VAULT STRUCTURE                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                             ║
║  your-vault/                                                ║
║  ├── 01-日记/          Daily logs (auto-extracted events)   ║
║  ├── 02-知识/          Technical knowledge, configs, API    ║
║  ├── 04-教训/          Lessons learned, user preferences    ║
║  ├── 06-收件箱/        Inbox (auto-categorized by agent)    ║
║  ├── 07-项目/          Project docs, architecture           ║
║  └── .obsidian/        Obsidian config (auto-skipped)       ║
║                                                             ║
║  These directories are synced to workspace/memory/ so       ║
║  they appear in memory_search. Edit sync_dirs in config     ║
║  if your vault uses different folder names.                 ║
║                                                             ║
╚══════════════════════════════════════════════════════════════╝""")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Setup OpenClaw Memory System")
    parser.add_argument("--vault-dir", help="Path to your vault directory")
    parser.add_argument("--qdrant-url", default="http://localhost:6333", help="Qdrant URL")
    parser.add_argument("--install-deps", action="store_true", help="Auto-install Python deps")
    parser.add_argument("--start-qdrant", action="store_true", help="Start Qdrant via docker-compose")
    opts = parser.parse_args()

    print("=" * 60)
    print("  OpenClaw Memory System — Setup")
    print("=" * 60)

    # 1. Config
    print("\n[1/7] Configuration...")
    create_config(opts.vault_dir)

    # 2. Python deps
    print("\n[2/7] Python dependencies...")
    missing_req, missing_opt = check_python_deps()
    if missing_req:
        print(f"  ⚠️  Missing required: {', '.join(missing_req)}")
        if opts.install_deps:
            install_deps()
            missing_req, missing_opt = check_python_deps()
        else:
            print(f"  Install: pip install {' '.join(missing_req)}")
            print(f"  Or run: python scripts/setup.py --install-deps")
    if missing_opt:
        print(f"  ℹ️  Missing optional: {', '.join(missing_opt)} (for Mem0 integration)")
    if not missing_req:
        print(f"  ✅ All required dependencies present")

    # 3. Data directory
    print("\n[3/7] Data directory...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"  ✅ {DATA_DIR}")

    # 4. Qdrant
    print("\n[4/7] Qdrant vector database...")
    qdrant_ok = check_qdrant(opts.qdrant_url)
    if not qdrant_ok and opts.start_qdrant:
        print("  Starting Qdrant via docker-compose...")
        qdrant_ok = start_qdrant_docker()
        if qdrant_ok:
            qdrant_ok = check_qdrant(opts.qdrant_url)
    if qdrant_ok:
        print(f"  ✅ Qdrant reachable at {opts.qdrant_url}")
        init_qdrant_collection(opts.qdrant_url)
    else:
        print(f"  ⚠️  Qdrant not reachable at {opts.qdrant_url}")
        print(f"  Option A: docker-compose -f {DOCKER_COMPOSE} up -d")
        print(f"  Option B: docker run -p 6333:6333 qdrant/qdrant")
        print(f"  Option C: Download from https://qdrant.tech/documentation/quick-start/")

    # 5. Embedding server
    print("\n[5/7] Embedding server...")
    if check_embedding_server():
        print(f"  ✅ Embedding server reachable")
    else:
        print(f"  ⚠️  Embedding server not reachable")
        print(f"  Options:")
        print(f"    - LM Studio: https://lmstudio.ai (load nomic-embed-text-v1.5)")
        print(f"    - Ollama: ollama pull nomic-embed-text")
        print(f"    - Any OpenAI-compatible /v1/embeddings endpoint")

    # 6. OpenClaw hooks
    print("\n[6/7] OpenClaw hooks...")
    try:
        r = subprocess.run(["openclaw", "hooks", "list"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            output = r.stdout
            for hook in ["session-memory", "memory-compact", "memory-extract"]:
                if hook in output and "ready" in output:
                    print(f"  ✅ {hook} ready")
                else:
                    print(f"  ⚠️  {hook} not ready — run: openclaw hooks enable {hook}")
        else:
            print(f"  ℹ️  Could not check hooks (openclaw not in PATH)")
    except Exception:
        print(f"  ℹ️  Could not check hooks")

    # 7. Summary
    print("\n" + "=" * 60)
    print("  Setup complete!")
    print("=" * 60)

    if CONFIG_FILE.exists():
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        needs_edit = (cfg.get("embedder", {}).get("apiKey") == "***" or
                     cfg.get("llm", {}).get("apiKey") == "***")
        if needs_edit:
            print(f"\n  ⚠️  IMPORTANT: Edit {CONFIG_FILE} with your actual API keys!")

    print_cron_setup()
    print_hooks_setup()
    print_vault_structure()

    print("\n  Verify installation:")
    print("    python scripts/shared_config.py    # check config")
    print("    python scripts/memory_health.py     # check all chains")
    print("    openclaw memory status              # check OpenClaw index")


if __name__ == "__main__":
    main()
