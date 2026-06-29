"""
extract_memories.py — Unified memory extraction pipeline

Step 1 (default): session → compress → Qdrant + vault
Step 2 (--full): Qdrant concept aggregation → LLM fusion → vault
Step 3 (--full): vault clustering → LLM distillation → archive

Usage: python scripts/extract_memories.py          # Step 1 only
       python scripts/extract_memories.py --full   # Step 1+2+3
"""
import _suppress_windows

import os, sys, json, re, subprocess, tempfile, uuid
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict

if sys.stdout.encoding and sys.stdout.encoding.upper() in ("GBK", "GB2312"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.upper() in ("GBK", "GB2312"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from shared_config import (
    VAULT_DIR, MEMORY_DIR, SCRIPTS_DIR, DATA_DIR,
    LLM_BASE_URL, LLM_API_KEY, LLM_MODEL,
    LMSTUDIO_EMBED_URL as EMBED_BASE_URL, LMSTUDIO_KEY as EMBED_API_KEY, EMBED_MODEL,
    QDRANT_HOST, QDRANT_PORT, KB_COLLECTION,
)

MAX_AGE_HOURS = 48
MIN_OBSERVATIONS_FOR_CONSOLIDATION = 3
MIN_CONFIDENCE_FOR_CONCEPT = 3
CLUSTERS_FILE = DATA_DIR / "vault_clusters.json"
PROCESSED_STATE_FILE = DATA_DIR / ".extract_memories_processed.json"


# ── Step 1 functions ──

def should_use_llm(observations: list) -> bool:
    for obs in observations:
        if isinstance(obs.get("importance", 0), (int, float)) and obs["importance"] >= 8:
            return True
        if obs.get("type") in ("decision", "discovery"):
            return True
    return False


def get_recent_files():
    cutoff = datetime.now() - timedelta(hours=MAX_AGE_HOURS)
    session_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-\d{4}\.md$')
    processed = {}
    if PROCESSED_STATE_FILE.exists():
        try:
            processed = json.loads(PROCESSED_STATE_FILE.read_text(encoding='utf-8'))
        except Exception:
            processed = {}

    stale_cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
    processed = {k: v for k, v in processed.items() if v > stale_cutoff}

    candidates = []
    for f in MEMORY_DIR.glob("*.md"):
        if not session_pattern.match(f.name):
            continue
        mtime = f.stat().st_mtime
        if mtime <= cutoff.timestamp():
            continue
        fkey = f.name
        if fkey in processed and processed[fkey] >= str(mtime):
            continue
        candidates.append(f)
    return candidates


def mark_files_processed(files):
    processed = {}
    if PROCESSED_STATE_FILE.exists():
        try:
            processed = json.loads(PROCESSED_STATE_FILE.read_text(encoding='utf-8'))
        except Exception:
            processed = {}
    for f in files:
        processed[f.name] = str(f.stat().st_mtime)
    stale_cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
    processed = {k: v for k, v in processed.items() if v > stale_cutoff}
    PROCESSED_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_STATE_FILE.write_text(json.dumps(processed, ensure_ascii=False, indent=2), encoding='utf-8')


def extract_key_content(filepath):
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")
        valuable = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("---"):
                continue
            if "system-reminder" in line.lower():
                continue
            valuable.append(line)
        return "\n".join(valuable[:50])
    except Exception:
        return ""


def parse_to_observations(content: str, session_id: str = "") -> list:
    observations = []
    lines = content.split("\n")
    now_ts = datetime.now(timezone.utc).isoformat()

    user_count = sum(1 for line in lines[:50] if line.strip().startswith("user:") or line.strip().startswith("assistant:"))
    is_session_dump = user_count >= 4

    if is_session_dump:
        in_body = False
        current_role = None
        current_msg_lines = []

        def flush_pair():
            if not observations:
                return
            last = observations[-1]
            if current_role == "assistant" and current_msg_lines:
                last["toolOutput"] = " ".join(current_msg_lines)[:1000]
            elif current_role == "user" and current_msg_lines:
                last["userPrompt"] = " ".join(current_msg_lines)[:500]

        for line in lines:
            s = line.strip()
            if not s:
                if in_body and current_role:
                    current_msg_lines.append("")
                continue
            if not in_body:
                if s.startswith("user:") or s.startswith("assistant:"):
                    in_body = True
                else:
                    continue

            if s.startswith("user:"):
                flush_pair()
                current_role = "user"
                msg = s.split(":", 1)[1].strip() if ":" in s else ""
                current_msg_lines = [msg]
                observations.append({
                    "hookType": "conversation", "toolName": "", "toolInput": "",
                    "toolOutput": "", "userPrompt": msg[:500],
                    "timestamp": now_ts, "sessionId": session_id
                })
            elif s.startswith("assistant:"):
                flush_pair()
                current_role = "assistant"
                msg = s.split(":", 1)[1].strip() if ":" in s else ""
                current_msg_lines = [msg]
                if observations:
                    observations[-1]["toolOutput"] = msg[:1000]
            elif current_role and s:
                current_msg_lines.append(s)
                if current_role == "assistant" and observations:
                    observations[-1]["toolOutput"] = " ".join(current_msg_lines)[:1000]
                elif current_role == "user" and observations:
                    observations[-1]["userPrompt"] = " ".join(current_msg_lines)[:500]
        flush_pair()
    else:
        title = ""
        body_lines = []
        for line in lines:
            s = line.strip()
            if s.startswith("# ") and not title:
                title = s[2:].strip()
            elif s.startswith("> ") or s.startswith("---") or s.startswith("相关："):
                continue
            elif s:
                body_lines.append(s)
        body = "\n".join(body_lines).strip()
        if body:
            observations.append({
                "hookType": "knowledge", "toolName": "", "toolInput": "",
                "toolOutput": body[:1000], "userPrompt": title[:200],
                "timestamp": now_ts, "sessionId": session_id
            })
    return observations


def index_to_qdrant(compressed: dict, session_id: str = ""):
    import requests
    text = compressed.get("narrative","") or compressed.get("title","") or "observation"
    resp = requests.post(f"{EMBED_BASE_URL}/embeddings",
        headers={"Authorization":f"Bearer {EMBED_API_KEY}","Content-Type":"application/json"},
        json={"model":EMBED_MODEL,"input":text[:1000]}, timeout=10)
    if resp.status_code != 200: return
    try: vector = resp.json()["data"][0]["embedding"]
    except Exception: return
    point = {"id":str(uuid.uuid4()),"vector":vector,"payload":{**compressed,"pipeline":"compress","sessionId":session_id,"is_latest":True,"version":1,"indexed_at":datetime.now(timezone.utc).isoformat()}}
    requests.put(f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{KB_COLLECTION}/points",json={"points":[point]},timeout=10)


def llm_extract(content: str, source: str) -> str:
    import requests
    prompt = f"从以下对话中提取有价值的记忆（用户偏好、决策、重要发现）。\n输出格式：<memory><type>preference|knowledge|event</type><summary>一句话总结</summary><detail>详细内容</detail></memory>\n\n内容：\n{content[:1000]}"
    try:
        resp = requests.post(f"{LLM_BASE_URL}/chat/completions",
            headers={"Authorization":f"Bearer {LLM_API_KEY}"},
            json={"model":LLM_MODEL,"messages":[{"role":"user","content":prompt}],"temperature":0.1,"max_tokens":500},timeout=30)
        return resp.json()["choices"][0]["message"]["content"] if resp.status_code==200 else ""
    except Exception as e:
        print(f"  LLM extract failed: {e}")
        return ""


def _is_duplicate(target_dir, today, memory_type, text, threshold=0.5):
    prefix = f"{today}-{memory_type}-"
    snippet = text[:60].strip().lower()
    if not snippet or len(snippet) < 10:
        return False
    for f in target_dir.glob(f"{prefix}*.md"):
        try:
            existing = f.read_text(encoding="utf-8", errors="replace")
            body_lines = [l for l in existing.split("\n") if l and not l.startswith("#") and not l.startswith(">") and not l.startswith("相关")]
            existing_text = " ".join(body_lines)[:60].strip().lower()
            if not existing_text or len(existing_text) < 10:
                continue
            common = 0
            for a, b in zip(snippet, existing_text):
                if a == b: common += 1
                else: break
            if common >= 15:
                return True
        except Exception:
            continue
    return False


def save_to_vault(text, memory_type="knowledge"):
    today = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%H%M%S")
    type_match = re.search(r"<type>(\w+)</type>", text)
    if type_match:
        memory_type = type_match.group(1)
        text = re.sub(r"</?memory>","",text)
        text = re.sub(r"</?type>\w*</type>","",text)
        text = re.sub(r"</?summary>.*?</summary>","",text)
        text = re.sub(r"</?detail>","",text)
        text = text.strip()
    dir_map = {"preference":VAULT_DIR/"04-教训","knowledge":VAULT_DIR/"02-知识","event":VAULT_DIR/"01-日记"}
    target_dir = dir_map.get(memory_type, VAULT_DIR/"02-知识")
    target_dir.mkdir(parents=True, exist_ok=True)
    if _is_duplicate(target_dir, today, memory_type, text):
        print(f"  [dedup] Skipping similar content: {text[:50]}...")
        return None
    safe_name = text[:40].replace("/","-").replace("\\","-").replace(":","-").replace("\n"," ").replace("*","")
    filepath = target_dir / f"{today}-{memory_type}-{ts}-{safe_name}.md"
    header = f"# {memory_type}: {text[:60]}\n> Auto-extracted {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{text}"
    try:
        filepath.write_text(header, encoding="utf-8")
        return str(filepath.relative_to(VAULT_DIR))
    except Exception as e:
        print(f"  [vault write failed] {e}")
        return None


# ── Step 2: Concept consolidation ──

CONSOLIDATE_SYSTEM = """You are a memory distillation engine (ReMe architecture). Fuse observations on the same topic along a timeline, showing knowledge evolution.

Core principles:
- Later observations have higher weight. If contradictions exist, latest wins.
- Record evolution: initial state → trigger → current conclusion.
- If observations agree with no contradictions, initial_state = current_state, trigger = "no change".

Output strict XML:
<memory>
  <type>pattern|preference|architecture|bug|workflow|fact</type>
  <title>short title (<=60 chars)</title>
  <initial_state>earliest state or initial judgment</initial_state>
  <trigger>cause of change (or "no change")</trigger>
  <current_state>current final state or conclusion</current_state>
  <evolution>change summary like "X → Y → Z" (or "stable")</evolution>
  <confidence>1-10</confidence>
</memory>"""


def step2_fetch_qdrant_concepts(days=30):
    import requests
    points = []
    offset = None
    while True:
        payload = {"limit":500,"with_payload":True,"with_vector":False}
        if offset: payload["offset"] = offset
        resp = requests.post(f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{KB_COLLECTION}/points/scroll",json=payload,timeout=30)
        if resp.status_code != 200: break
        data = resp.json().get("result",{})
        batch = data.get("points",[])
        points.extend(batch)
        offset = data.get("next_page_offset")
        if not batch or offset is None: break

    groups = defaultdict(list)
    for pt in points:
        p = pt.get("payload",{})
        if p.get("source") == "consolidate": continue
        if p.get("is_latest") is False: continue
        if p.get("type") == "knowledge": continue
        concepts = p.get("concepts",[])
        if isinstance(concepts, list):
            for c in concepts:
                if isinstance(c,str) and len(c)>1:
                    groups[c.lower()].append(p)
    return dict(groups)


def step2_llm_fuse(concept: str, observations: list):
    import requests
    sorted_obs = sorted(observations, key=lambda o: o.get("payload",{}).get("compressedAt", ""))
    lines = []
    for i, obs in enumerate(sorted_obs):
        p = obs.get("payload",{})
        t = p.get("compressedAt", "")[:19]
        lines.append(f"[{i+1}] {t} [{p.get('type','other')}] {p.get('title','?')}\n{p.get('narrative','')}\nimportance:{p.get('importance',5)}")
    prompt = f"Concept: \"{concept}\"\n\nObservations (sorted by time, newer = higher number):\n" + "\n\n".join(lines)
    try:
        resp = requests.post(f"{LLM_BASE_URL}/chat/completions",
            headers={"Authorization":f"Bearer {LLM_API_KEY}"},
            json={"model":LLM_MODEL,"messages":[{"role":"system","content":CONSOLIDATE_SYSTEM},{"role":"user","content":prompt}],"temperature":0.1,"max_tokens":1200},
            timeout=(10,60))
        if resp.status_code != 200: return None
        response = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  Fusion LLM failed: {e}")
        return None

    try:
        import xml.parsers.expat
        tags = {}
        cur_tag, cur_text = None, ""
        def start(name, attrs): nonlocal cur_tag, cur_text; cur_tag = name; cur_text = ""
        def end(name):
            nonlocal cur_text
            if cur_text.strip(): tags[name] = cur_text.strip()
        def chars(data): nonlocal cur_text; cur_text += data
        parser = xml.parsers.expat.ParserCreate()
        parser.StartElementHandler = start
        parser.EndElementHandler = end
        parser.CharacterDataHandler = chars
        parser.Parse(response)
        if "title" in tags:
            return {
                "type": tags.get("type", "fact"),
                "title": tags["title"],
                "initial_state": tags.get("initial_state", ""),
                "trigger": tags.get("trigger", "no change"),
                "current_state": tags.get("current_state", ""),
                "evolution": tags.get("evolution", "stable"),
                "confidence": int(tags.get("confidence", 5)),
            }
    except Exception:
        pass
    return None


def step2_save_fused(result: dict, concept: str, observations: list):
    import requests
    safe_name = re.sub(r'[\\/:*?"<>|]', '-', concept)
    target_file = VAULT_DIR / "02-知识" / f"concept-{safe_name}.md"
    today = datetime.now().strftime("%Y-%m-%d")
    initial = result.get("initial_state", "")
    trigger = result.get("trigger", "no change")
    current = result.get("current_state", "")
    evolution = result.get("evolution", "stable")

    content = (
        f"# {result['title']}\n\n"
        f"**Concept:** {concept}\n**Type:** {result['type']}\n"
        f"**Confidence:** {result.get('confidence', 5)}/10\n"
        f"**Created:** {today}\n**Source observations:** {len(observations)}\n\n---\n\n"
        f"## Initial State\n{initial}\n\n## Trigger\n{trigger}\n\n"
        f"## Current Conclusion\n{current}\n\n## Evolution\n{evolution}\n\n---\n\n## Sources\n"
    )
    for obs in observations:
        p = obs.get("payload",{})
        content += f"- [{p.get('type','?')}] {p.get('title','?')} (importance:{p.get('importance','?')})\n"
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(content, encoding="utf-8")
    print(f"  Wrote: {target_file.relative_to(VAULT_DIR)}")

    text_for_embed = f"{current} {initial} {evolution}"
    resp = requests.post(f"{EMBED_BASE_URL}/embeddings",
        headers={"Authorization":f"Bearer {EMBED_API_KEY}","Content-Type":"application/json"},
        json={"model":EMBED_MODEL,"input":text_for_embed[:1000]}, timeout=10)
    if resp.status_code == 200:
        try:
            vec = resp.json()["data"][0]["embedding"]
            point = {"id":str(uuid.uuid5(uuid.NAMESPACE_DNS,str(target_file))),"vector":vec,
                     "payload":{"title":result["title"],"type":result["type"],
                                "initial_state":initial,"trigger":trigger,
                                "current_state":current,"evolution":evolution,
                                "concepts":[result.get("type","fact")],"source":"consolidate",
                                "pipeline":"consolidate","source_file":str(target_file),
                                "confidence":result.get("confidence",5),"version":1,"is_latest":True,
                                "created_at":datetime.now(timezone.utc).isoformat()}}
            requests.put(f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{KB_COLLECTION}/points",json={"points":[point]},timeout=10)
        except Exception:
            pass


def run_step2(max_fusions=5):
    print("\n=== Step 2: Concept consolidation ===")
    groups = step2_fetch_qdrant_concepts()
    candidates = [(c, obs) for c, obs in groups.items() if len(obs) >= 3]
    if not candidates:
        print("  No candidate concepts (need >=3 observations per concept)")
        return 0
    candidates.sort(key=lambda x: -len(x[1]))
    fused = 0
    for concept, obs in candidates[:max_fusions]:
        print(f"\n  Fusing: {concept} ({len(obs)} observations)")
        result = step2_llm_fuse(concept, obs[:8])
        if not result:
            print("  Fusion failed, skip")
            continue
        print(f"  Title: {result['title'][:60]}")
        step2_save_fused(result, concept, obs[:8])
        fused += 1
    return fused


# ── Step 3: Distillation pipeline ──

def run_step3(max_distills=2):
    print("\n=== Step 3: Distillation pipeline ===")
    subprocess.run(["python", str(SCRIPTS_DIR/"vault_cluster.py")], capture_output=True, timeout=30)
    if not CLUSTERS_FILE.exists():
        print("  Clusters file not found")
        return 0
    clusters = json.loads(CLUSTERS_FILE.read_text(encoding="utf-8"))
    candidates = sorted(clusters, key=lambda c: -c["file_count"])[:max_distills]
    distilled = 0
    for c in candidates:
        label = c["label"]
        n = c["file_count"]
        if n < 3:
            print(f"  {label}: {n} files, too few, skip")
            continue
        print(f"\n  Distilling: {label} ({n} files)")
        subprocess.run(["python", str(SCRIPTS_DIR/"vault_distill.py"), c["id"]], capture_output=True, timeout=30)
        subprocess.run(["python", str(SCRIPTS_DIR/"vault_distill_llm.py"), c["id"]], capture_output=True, timeout=90)
        distilled += 1
    return distilled


# ── Main ──

def main(run_full=False):
    import requests as req
    try:
        req.get(f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{KB_COLLECTION}", timeout=3)
        qdrant_ok = True
    except Exception:
        qdrant_ok = False

    if not MEMORY_DIR.exists():
        print("memory directory does not exist")
        return

    files = get_recent_files()
    zero_llm_count = llm_count = total_compressed = total_passed = total_rejected = 0
    qdrant_write_ok = qdrant_write_fail = 0
    processed_files = []

    if not files:
        print(f"No new session files in last {MAX_AGE_HOURS}h (or all processed)")
    else:
        print(f"Found {len(files)} files to process:")
        for f in files:
            print(f"  - {f.name}")
            processed_files.append(f)
            content = extract_key_content(f)
            if not content: continue
            observations = parse_to_observations(content, f.stem)
            if not observations:
                print(f"    [skip] No valid observations")
                continue

            compress_script = SCRIPTS_DIR / "compress.py"
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8', delete=False) as tf:
                    json.dump(observations, tf, ensure_ascii=False)
                    tmp_path = tf.name
                result = subprocess.run(["python", str(compress_script), "--input", tmp_path], capture_output=True, timeout=30, encoding='utf-8')
                try: os.unlink(tmp_path)
                except: pass
                if result.returncode == 0 and result.stdout.strip():
                    out = result.stdout.strip()
                    bracket = out.find("[")
                    compressed_list = json.loads(out[bracket:]) if bracket >= 0 else []
                else:
                    compressed_list = []
            except Exception as e:
                print(f"    [error] compress failed: {e}")
                compressed_list = []

            if not compressed_list:
                print(f"    [skip] compress returned empty")
                continue

            if qdrant_ok:
                from compress import quality_gate
                passed = rejected = 0
                for compressed in compressed_list:
                    total_compressed += 1
                    if not quality_gate(compressed):
                        rejected += 1; total_rejected += 1
                        continue
                    try:
                        index_to_qdrant(compressed, f.stem)
                        passed += 1; total_passed += 1; qdrant_write_ok += 1
                        importance = compressed.get("importance", 0)
                        if isinstance(importance, (int, float)) and importance >= 5:
                            narrative = compressed.get("narrative", "") or compressed.get("title", "")
                            if narrative: save_to_vault(narrative, "knowledge")
                    except Exception:
                        qdrant_write_fail += 1
                if rejected:
                    print(f"    [quality gate] Rejected {rejected} low-quality items")
                zero_llm_count += passed

            print(f"    Zero-LLM compressed: {passed if qdrant_ok else len(compressed_list)} observations")

            needs_llm = should_use_llm(compressed_list)
            if needs_llm:
                print(f"    LLM distillation needed...")
                summary = llm_extract(content, f.stem)
                if summary:
                    vault_path = save_to_vault(summary)
                    if vault_path: print(f"    [Vault] {vault_path}")
                    llm_count += 1

        print(f"\nStep 1 complete. Zero-LLM: {zero_llm_count} | LLM: {llm_count}")
        if processed_files:
            mark_files_processed(processed_files)

    if run_full:
        fused = run_step2(max_fusions=5)
        print(f"\nStep 2 complete. Fused: {fused}")
        distilled = run_step3(max_distills=2)
        print(f"\nStep 3 complete. Distilled: {distilled}")
        print("\nFull pipeline complete.")
    else:
        print("(Step 2+3 not executed. Use --full to enable)")


if __name__ == "__main__":
    full = "--full" in sys.argv
    main(run_full=full)
