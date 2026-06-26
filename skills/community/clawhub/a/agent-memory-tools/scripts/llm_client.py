#!/usr/bin/env python3
"""
Unified LLM + Embedding client for agent-memory-tools.
Reads config.json, supports LM Studio, Ollama, and OpenAI-compatible APIs.
"""
from __future__ import annotations
import json, os, platform, subprocess, sys, re
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"
IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"

def load_config(preset: str | None = None, script: str | None = None) -> dict:
    """Load config.json, optionally applying a preset overlay."""
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    
    # Auto-detect workspace: env var > config > skill parent dir
    ws = cfg.get("paths", {}).get("workspace", "")
    if not ws or not os.path.isdir(ws):
        ws = os.environ.get(
            "MEMORY_WORKSPACE",
            str(Path(__file__).resolve().parents[2])  # skill parent
        )
    cfg.setdefault("paths", {})["workspace"] = ws
    
    # Apply preset if requested
    if preset and preset in cfg.get("presets", {}):
        p = cfg["presets"][preset]
        if "llm" in p:
            cfg["llm"].update(p["llm"])
        if "embeddings" in p:
            cfg["embeddings"].update(p["embeddings"])
    
    # Apply script-specific overrides
    if script and script in cfg.get("scriptOverrides", {}):
        overrides = cfg["scriptOverrides"][script]
        if "llm" in overrides:
            cfg["llm"].update(overrides["llm"])
        if "embeddings" in overrides:
            cfg["embeddings"].update(overrides["embeddings"])
    
    return cfg


def call_llm(prompt: str, cfg: dict | None = None, debug: bool = False) -> str | None:
    """Call LLM via OpenAI-compatible or Ollama API. Returns raw text."""
    if cfg is None:
        cfg = load_config()
    
    llm = cfg["llm"]
    api_format = llm.get("apiFormat", "openai")
    base_url = llm["baseUrl"].rstrip("/")
    
    if api_format == "ollama":
        url = f"{base_url}/api/generate"
        payload = {
            "model": llm["model"],
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": llm.get("temperature", 0.1), "num_predict": llm.get("maxTokens", 2048)}
        }
    else:
        url = f"{base_url}/chat/completions"
        payload = {
            "model": llm["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": llm.get("temperature", 0.1),
            "max_tokens": llm.get("maxTokens", 2048),

        }
    
    timeout = llm.get("timeoutSeconds", 120)
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", str(timeout), url,
             "-H", "Content-Type: application/json", "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=timeout + 10
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        
        if "error" in data:
            if debug:
                print(f"  LLM error: {data['error']}", file=sys.stderr)
            return None
        
        if api_format == "ollama":
            text = data.get("response", "")
            # Qwen 3.x puts content in "thinking" field via Ollama
            if not text and data.get("thinking"):
                text = data["thinking"]
        else:
            msg = data.get("choices", [{}])[0].get("message", {})
            text = msg.get("content", "")
            # Fallback: reasoning models (GPT-OSS, Qwen) put content elsewhere
            if not text:
                text = msg.get("reasoning", "") or msg.get("reasoning_content", "")
        
        # Strip thinking tags (Qwen, DeepSeek)
        if "<think>" in text:
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
        
        # Strip "Thinking Process:" preamble (Qwen 3.x via Ollama — no <think> tags)
        if text.startswith("Thinking Process:") or text.startswith("Thinking process:"):
            text = text.strip()
        
        if debug:
            print(f"  LLM ({llm['model']}): {text[:200]}", file=sys.stderr)
        return text
    except Exception as e:
        if debug:
            print(f"  LLM exception: {e}", file=sys.stderr)
        return None


def _extract_json(text: str) -> dict | None:
    """Extract JSON object or array from text (handles code blocks, tags, etc)."""
    # Strip model-specific channel/tool tags (GPT-OSS)
    text = re.sub(r'<\|[^|]+\|>[^\n{]*', '', text)
    
    # Extract from markdown code blocks
    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if json_match:
        text = json_match.group(1)
    
    # Try to find JSON object/array
    for pattern in [r'\{.*\}', r'\[.*\]']:
        m = re.search(pattern, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                continue
    return None


def call_llm_json(prompt: str, cfg: dict | None = None, debug: bool = False, retries: int = 1) -> dict | None:
    """Call LLM and parse JSON from response. Retries on parse failure."""
    if cfg is None:
        cfg = load_config()
    
    for attempt in range(1 + retries):
        text = call_llm(prompt, cfg, debug)
        if not text:
            continue
        
        result = _extract_json(text)
        if result is not None:
            return result
        
        if debug and attempt < retries:
            print(f"  JSON parse failed (attempt {attempt+1}), retrying...", file=sys.stderr)
    
    return None


def embed(texts: list[str], cfg: dict | None = None, debug: bool = False) -> list[list[float]]:
    """Embed texts via OpenAI-compatible or Ollama API."""
    if cfg is None:
        cfg = load_config()
    
    emb = cfg["embeddings"]
    api_format = emb.get("apiFormat", "openai")
    base_url = emb["baseUrl"].rstrip("/")
    
    if api_format == "ollama":
        url = f"{base_url}/api/embed"
        payload = {"model": emb["model"], "input": texts}
    else:
        url = f"{base_url}/embeddings"
        payload = {"model": emb["model"], "input": texts}
    
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "120", url,
             "-H", "Content-Type: application/json", "-d", json.dumps(payload)],
            capture_output=True, text=True, timeout=130
        )
        data = json.loads(result.stdout)
        
        # OpenAI format
        if "data" in data:
            return [d["embedding"] for d in data["data"]]
        # Ollama format
        if "embeddings" in data:
            return data["embeddings"]
        
        if debug:
            print(f"  Embed unexpected response: {str(data)[:200]}", file=sys.stderr)
        return []
    except Exception as e:
        if debug:
            print(f"  Embed exception: {e}", file=sys.stderr)
        return []


def cosine_sim(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def check_server(cfg: dict | None = None) -> dict:
    """Check if LLM and embedding servers are reachable."""
    if cfg is None:
        cfg = load_config()
    
    status = {"llm": False, "embeddings": False, "llm_models": [], "embed_models": []}
    
    for key, section in [("llm", cfg["llm"]), ("embeddings", cfg["embeddings"])]:
        base_url = section["baseUrl"].rstrip("/")
        api_format = section.get("apiFormat", "openai")
        
        if api_format == "ollama":
            url = f"{base_url}/api/tags"
        else:
            url = f"{base_url}/models"
        
        try:
            result = subprocess.run(
                ["curl", "-s", "--max-time", "5", url],
                capture_output=True, text=True, timeout=10
            )
            data = json.loads(result.stdout)
            status[key] = True
            if "data" in data:
                status[f"{key}_models"] = [m.get("id", "") for m in data["data"]]
            elif "models" in data:
                status[f"{key}_models"] = [m.get("name", "") for m in data["models"]]
        except Exception:
            pass
    
    return status


if __name__ == "__main__":
    """Quick self-test."""
    cfg = load_config()
    print(f"Config loaded. LLM: {cfg['llm']['model']} @ {cfg['llm']['baseUrl']}")
    print(f"Embed: {cfg['embeddings']['model']} @ {cfg['embeddings']['baseUrl']}")
    
    status = check_server(cfg)
    print(f"\nServer status: LLM={'OK' if status['llm'] else 'DOWN'}, Embed={'OK' if status['embeddings'] else 'DOWN'}")
    if status['llm_models']:
        print(f"LLM models: {', '.join(status['llm_models'][:5])}")
    
    # Quick embed test
    vecs = embed(["test"], cfg)
    if vecs:
        print(f"Embed OK: dims={len(vecs[0])}")
    else:
        print("Embed FAILED")
    
    # Quick LLM test
    resp = call_llm("Reply with exactly: OK", cfg)
    print(f"LLM test: {resp[:50] if resp else 'FAILED'}")
