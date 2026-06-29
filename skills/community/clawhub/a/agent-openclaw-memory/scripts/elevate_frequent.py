"""
elevate_frequent.py — vault 高频内容自动升格为 self-improving 规则

Phase 1: Scoring        — Qdrant scroll + filesystem heuristics (0 token)
Phase 2: Candidate      — 阈值过滤 (0 token)
Phase 3: Distill        — LLM 蒸馏 via Gateway (仅候选文件)
Phase 4: Write          — 写入 self-improving/
Phase 5: De-escalate    — 清理过期规则 (0 token)

用法:
    python scripts/elevate_frequent.py              # 全流程
    python scripts/elevate_frequent.py --dry-run    # 只评分不写入
    python scripts/elevate_frequent.py --force <relative-path>  # 手动升格
    python scripts/elevate_frequent.py --de-escalate-only       # 只降级
    python scripts/elevate_frequent.py --threshold 8.0          # 覆盖阈值
"""

import json
import os
import re
import sys
import time
import shutil
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict

# ── Paths ──────────────────────────────────────────────────────────
from shared_config import VAULT_DIR as VAULT
SELF_IMPROVING = Path.home() / "self-improving"
SCRIPTS_DIR    = Path(__file__).parent
RULE_STATE_FILE = SELF_IMPROVING / ".rule_state.json"
CANDIDATES_DIR  = SELF_IMPROVING / ".candidates"
MEMORY_FILE     = SELF_IMPROVING / "memory.md"
CORRECTIONS_FILE = SELF_IMPROVING / "corrections.md"

# ── Qdrant ─────────────────────────────────────────────────────────
QDRANT_URL  = "http://127.0.0.1:6333"
KB_COLLECTION = "knowledge_base"

# ── Gateway (LLM proxy) ────────────────────────────────────────────
GATEWAY_URL   = "http://127.0.0.1:18789"  # kept for reference, use gateway_client for actual calls
from shared_config import MIMO_MODEL
LLM_MODEL_HEADER = MIMO_MODEL

# ── Thresholds ─────────────────────────────────────────────────────
DEFAULT_THRESHOLD   = 3.5   # 进入候选的最低分
AUTO_ELEVATE_SCORE  = 5.5   # 自动升格（不等人审）
MAX_DISTILL_PER_RUN = 3     # 每次最多蒸馏条数
COOLDOWN_DAYS       = 7     # 同一文件冷却期
DECAY_HALF_LIFE_DAYS = 30   # recency 指数衰减半衰期
DEESCALATE_DAYS     = 30    # N 天无引用 → 降级
DENSITY_MIN         = 0.15  # 最低结构化密度

# ── Config file ────────────────────────────────────────────────────
CONFIG_FILE = SCRIPTS_DIR / "elevate_frequent_config.json"


def _load_config():
    """Load config, falling back to defaults."""
    cfg = _load_json(CONFIG_FILE, {})
    if not cfg:
        cfg = {}
    return cfg


# ── Scoring weights (overridable via config) ────────────────────────
def _get_weights():
    cfg = _load_config()
    w = cfg.get("weights", {})
    return (
        w.get("recency", 0.30),
        w.get("qdrant", 0.25),
        w.get("xrefs", 0.15),
        w.get("mentions", 0.20),
        w.get("manual", 0.10),
    )

# ── Vault dir → target mapping ─────────────────────────────────────
ROUTE_MAP = {
    "02-知识": ("domains", "knowledge"),
    "04-教训": ("memory",   "behavior"),
    "07-项目": ("projects", "project"),
}


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  UTILITIES                                                        ║
# ╚═════════════════════════════════════════════════════════════════════╝

def _load_json(path: Path, default=None):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    return default if default is not None else {}


def _save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _read_text(path: Path) -> str:
    """安全读取文本，自动处理编码"""
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="gbk")
        except Exception:
            return ""


def _relpath(abs_path: str) -> str:
    """将绝对路径转为相对 vault 的路径"""
    try:
        return str(Path(abs_path).relative_to(VAULT))
    except ValueError:
        return abs_path


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  PHASE 1: SCORING  (0 token)                                      ║
# ╚═════════════════════════════════════════════════════════════════════╝

def _scroll_vault_points(max_points=3000):
    """
    从 Qdrant 滚动获取所有 is_latest=true 且 deleted=false 的点。
    返回 [(payload,), ...] 列表。
    """
    import requests
    points = []
    offset = None
    while len(points) < max_points:
        payload = {
            "limit": min(500, max_points - len(points)),
            "with_payload": True,
            "with_vector": False,
            "filter": {
                "must": [
                    {"key": "is_latest", "match": {"value": True}},
                    {"key": "deleted",  "match": {"value": False}},
                ]
            },
        }
        if offset:
            payload["offset"] = offset
        try:
            resp = requests.post(
                f"{QDRANT_URL}/collections/{KB_COLLECTION}/points/scroll",
                json=payload, timeout=30,
            )
            if resp.status_code != 200:
                break
            data = resp.json().get("result", {})
            batch = data.get("points", [])
            points.extend(batch)
            offset = data.get("next_page_offset")
            if not batch or offset is None:
                break
        except Exception:
            break
    return points


def _score_recency(file_path: str) -> float:
    """文件 mtime → 指数衰减分 [0,10]"""
    try:
        mtime = os.path.getmtime(file_path)
    except OSError:
        return 0.0
    age_days = (time.time() - mtime) / 86400
    # 指数衰减: 半衰期 DECAY_HALF_LIFE_DAYS 天
    raw = 10.0 * (0.5 ** (age_days / DECAY_HALF_LIFE_DAYS))
    return round(raw, 2)


def _score_qdrant_chunks(source_path: str, chunk_counts: dict) -> float:
    """
    Qdrant chunk 数 → 归一化分 [0,10]。
    假设 30+ chunks = 满分，< 3 chunks = 基础分。
    """
    count = chunk_counts.get(source_path, 0)
    if count <= 0:
        return 0.0
    # log-scale: 3 chunks=3.0, 10 chunks=7.0, 30 chunks=10.0
    import math
    if count <= 1:
        return 1.0
    raw = min(10.0, 3.0 * math.log(count + 1, 3))
    return round(raw, 2)


def _score_cross_references(rel_path: str, vault_index: dict = None) -> float:
    """
    扫描 vault 文件是否被其他文件内链引用 [[...]]。
    返回 [0,10]，5+ 次引用 = 满分。
    """
    if vault_index is None:
        vault_index = _build_vault_index()
    count = vault_index.get("refs", {}).get(rel_path, 0)
    return round(min(10.0, count * 2.0), 2)


def _score_correction_mentions(rel_path: str, mentions_cache: dict = None) -> float:
    """
    检查 corrections.md / memory.md 是否提及该文件。
    每次提及 = 5 分，2 次 = 满分。
    """
    if mentions_cache is None:
        mentions_cache = _build_mentions_cache()
    count = mentions_cache.get(rel_path, 0)
    return round(min(10.0, count * 5.0), 2)


def _score_manual_boost(frontmatter: dict) -> float:
    """从 frontmatter elevation_boost 取手动分 [0,10]"""
    boost = frontmatter.get("elevation_boost", 0)
    try:
        return round(min(10.0, float(boost)), 2)
    except (TypeError, ValueError):
        return 0.0


def _compute_density(content: str) -> float:
    """
    结构化密度 = (标题行数 + 列表行数) / 总非空行数。
    纯日记/叙事 < 0.15 → 跳过。
    """
    lines = [l.strip() for l in content.split("\n") if l.strip()]
    if not lines:
        return 0.0
    structured = sum(
        1 for l in lines
        if l.startswith("#") or l.startswith("- ") or l.startswith("* ")
        or l.startswith("1. ") or l.startswith("> ") or l.startswith("|")
    )
    return structured / len(lines)


def _parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter（简单实现，处理 --- 区块）"""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end < 0:
        return {}
    fm = {}
    for line in content[3:end].strip().split("\n"):
        line = line.strip()
        if ":" in line:
            k, _, v = line.partition(":")
            k, v = k.strip(), v.strip()
            # 尝试解析数字
            try:
                fm[k] = int(v)
            except ValueError:
                try:
                    fm[k] = float(v)
                except ValueError:
                    fm[k] = v.strip('"').strip("'")
    return fm


def _build_vault_index() -> dict:
    """
    扫描 vault 内所有 .md 的 [[link]] 引用，构建被引次数索引。
    缓存到内存，单次心跳只跑一次。
    """
    refs = defaultdict(int)
    files = defaultdict(int)  # file → total links
    try:
        for root, dirs, files_in_dir in os.walk(VAULT):
            if ".obsidian" in root:
                continue
            for fname in files_in_dir:
                if not fname.endswith(".md"):
                    continue
                fpath = Path(root) / fname
                try:
                    content = _read_text(fpath)
                except Exception:
                    continue
                links = re.findall(r'\[\[([^\]|#]+)', content)
                for link in links:
                    link = link.strip()
                    refs[link] += 1
    except Exception:
        pass
    return {"refs": dict(refs)}


def _build_mentions_cache() -> dict:
    """
    扫描 corrections.md 和 memory.md，统计 vault 文件名被提及次数。
    """
    mentions = defaultdict(int)
    for mentions_file in [CORRECTIONS_FILE, MEMORY_FILE]:
        content = _read_text(mentions_file)
        if not content:
            continue
        # 匹配 "02-知识/blah.md" 或 "vault/02-知识/blah" 模式
        for match in re.finditer(
            r'(?:vault[/\\])?((?:0[1247]-[^\s\]]+\.md))', content
        ):
            mentions[match.group(1)] += 1
        # 也匹配 "E:\\yx\\KL\\vault\\..." 绝对路径
        for match in re.finditer(
            r'(?:E:\\yx\\KL\\vault\\)([^\s]+\.md)', content
        ):
            mentions[match.group(1)] += 1
    return dict(mentions)


def score_all_files(dry_run=False) -> list:
    """
    Phase 1: 对所有 vault 文件评分。
    返回 [{"file": rel_path, "scores": {...}, "composite": float}, ...]
    """
    print("[Phase 1] Scoring vault files...")

    # 1a. Qdrant chunk counts (一次 scroll)
    chunk_counts = defaultdict(int)
    try:
        points = _scroll_vault_points()
        for pt in points:
            p = pt.get("payload", {})
            src = p.get("source", "")
            if src:
                chunk_counts[src] += 1
        print(f"  Qdrant: {len(points)} points, "
              f"{len(chunk_counts)} unique source files")
    except Exception as e:
        print(f"  Qdrant scroll failed: {e}")

    # 1b. Cross-reference index (一次全 vault 扫描)
    print("  Building cross-reference index...")
    vault_index = _build_vault_index()
    print(f"  Indexed {len(vault_index.get('refs', {}))} referenced targets")

    # 1c. Mentions cache
    mentions_cache = _build_mentions_cache()

    # 1d. Walk vault
    results = []
    skipped_density = 0
    skipped_dir = 0
    for root, dirs, files_in_dir in os.walk(VAULT):
        if ".obsidian" in root:
            continue
        for fname in files_in_dir:
            if not fname.endswith(".md"):
                continue
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, VAULT)

            # 路由检查：01-日记不参与
            top_dir = rel_path.split(os.sep)[0]
            if top_dir not in ROUTE_MAP:
                skipped_dir += 1
                continue

            # 读取内容
            content = _read_text(Path(full_path))
            if not content:
                continue

            # Density 过滤器
            density = _compute_density(content)
            if density < DENSITY_MIN:
                skipped_density += 1
                continue

            # 解析 frontmatter
            fm = _parse_frontmatter(content)

            # 检测是否废弃
            if fm.get("deprecated"):
                continue

            # 各维度评分
            s_recency   = _score_recency(full_path)
            s_qdrant    = _score_qdrant_chunks(full_path, chunk_counts)
            s_xrefs     = _score_cross_references(rel_path, vault_index)
            s_mentions  = _score_correction_mentions(rel_path, mentions_cache)
            s_manual    = _score_manual_boost(fm)

            w_r, w_q, w_x, w_m, w_b = _get_weights()
            composite = (
                w_r * s_recency
                + w_q * s_qdrant
                + w_x * s_xrefs
                + w_m * s_mentions
                + w_b * s_manual
            )

            results.append({
                "file": rel_path,
                "absolute": full_path,
                "top_dir": top_dir,
                "density": round(density, 3),
                "scores": {
                    "recency":  s_recency,
                    "qdrant":   s_qdrant,
                    "xrefs":    s_xrefs,
                    "mentions": s_mentions,
                    "manual":   s_manual,
                },
                "composite": round(composite, 2),
            })

    # 排序
    results.sort(key=lambda x: x["composite"], reverse=True)

    if dry_run:
        print(f"\n  Files scored: {len(results)}")
        print(f"  Skipped (wrong dir): {skipped_dir}")
        print(f"  Skipped (density < {DENSITY_MIN}): {skipped_density}")
        if results:
            print(f"\n  Top 10 by composite score:")
            print(f"  {'File':50s} {'Score':>6s}  {'R':>5s} {'Q':>5s} {'X':>5s} {'M':>5s} {'B':>5s}")
            print(f"  {'-'*50} {'-'*6}  {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*5}")
            for r in results[:10]:
                s = r["scores"]
                print(f"  {r['file'][:48]:50s} {r['composite']:6.2f}  "
                      f"{s['recency']:5.1f} {s['qdrant']:5.1f} "
                      f"{s['xrefs']:5.1f} {s['mentions']:5.1f} {s['manual']:5.1f}")

    return results


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  PHASE 2: CANDIDATE FILTERING  (0 token)                          ║
# ╚═════════════════════════════════════════════════════════════════════╝

def filter_candidates(scored: list, threshold: float,
                      state: dict) -> tuple:
    """
    过滤出候选文件。
    返回 (auto_elevate_list, candidate_list)
    - auto_elevate: score >= AUTO_ELEVATE_SCORE
    - candidate: threshold <= score < AUTO_ELEVATE_SCORE
    同时检查冷却期。
    """
    auto_list = []
    candidate_list = []
    now = datetime.now(timezone.utc)
    elevated = state.get("elevated", {})

    for item in scored:
        score = item["composite"]

        if score < threshold:
            continue

        # 冷却期检查：同一文件 7 天内不重复蒸馏
        file_key = item["file"]
        if file_key in elevated:
            last_ts = elevated[file_key].get("elevated_at", "")
            if last_ts:
                try:
                    last_dt = datetime.fromisoformat(last_ts)
                    if (now - last_dt).days < COOLDOWN_DAYS:
                        continue
                except ValueError:
                    pass

        if score >= AUTO_ELEVATE_SCORE:
            auto_list.append(item)
        else:
            candidate_list.append(item)

    cfg = _load_config()
    max_per_run = cfg.get("max_distill_per_run", MAX_DISTILL_PER_RUN)
    # 限制每次蒸馏数量
    auto_list = auto_list[:max_per_run]
    candidate_list = candidate_list[:max_per_run - len(auto_list)]

    return auto_list, candidate_list


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  PHASE 3: LLM DISTILLATION                                        ║
# ╚═════════════════════════════════════════════════════════════════════╝

def _get_distill_prompts():
    """Load prompts from config, with built-in ASCII fallbacks."""
    cfg = _load_config()
    prompts = cfg.get("distill_prompts", {})
    if prompts:
        return prompts
    # Hard fallback (ASCII-only, avoids encoding issues in Python source)
    return {
        "knowledge": (
            'You are a rule distillation engine. '
            'Extract ONE reusable rule from the vault file below.\n\n'
            'The rule must be actionable: "When X, do Y". '
            'Not a factual statement.\n'
            'Output STRICT JSON, no markdown blocks, nothing else:\n\n'
            '{"title": "Rule title (<=20 char)", '
            '"rule": "One-line rule", '
            '"why": "Reason", '
            '"when": "When to apply", '
            '"confidence": 7}\n\n'
            'Source file content:\n{content}'
        ),
        "behavior": (
            'You are a behavior rule distillation engine. '
            'Extract ONE Agent behavior rule from the vault file below.\n\n'
            'The rule must be: "The AI should do/not do X".\n'
            'Output STRICT JSON, no markdown blocks, nothing else:\n\n'
            '{"title": "Rule title", '
            '"rule": "One-line rule with action verb", '
            '"why": "Why this matters", '
            '"when": "When to apply", '
            '"confidence": 7}\n\n'
            'Source file content:\n{content}'
        ),
        "project": (
            'You are a project decision distillation engine. '
            'Extract ONE design/architecture decision from the file below.\n\n'
            'Focus on "why A over B" decisions.\n'
            'Output STRICT JSON, no markdown blocks, nothing else:\n\n'
            '{"title": "Decision title", '
            '"rule": "Decision content", '
            '"why": "Trade-off reason", '
            '"when": "Project phase", '
            '"confidence": 7}\n\n'
            'Source file content:\n{content}'
        ),
    }


def _llm_distill(content: str, distill_type: str) -> dict | None:
    """
    调 Gateway /v1/chat/completions 蒸馏 (via gateway_client)。
    返回 {"title","rule","why","when","confidence"} 或 None。
    """
    from gateway_client import chat

    prompts = _get_distill_prompts()
    prompt_template = prompts.get(distill_type, prompts.get("knowledge", ""))
    prompt = prompt_template.replace("{content}", content[:3000])

    try:
        result = chat(
            messages=prompt,
            model=LLM_MODEL_HEADER,
            temperature=0.1,
            max_tokens=400,
            timeout=30,
        )
        if not result:
            return None

        raw = result["content"].strip()

        # 清理可能的 markdown 代码块包裹
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)

        parsed = json.loads(raw)

        # 自评：confidence < 5 丢弃
        confidence = int(parsed.get("confidence", 5))
        if confidence < 5:
            print(f"    Confidence too low ({confidence}), discarding")
            return None

        return {
            "title": str(parsed.get("title", ""))[:40],
            "rule": str(parsed.get("rule", "")),
            "why": str(parsed.get("why", "")),
            "when": str(parsed.get("when", "")),
            "confidence": confidence,
        }

    except json.JSONDecodeError as e:
        print(f"    JSON parse failed: {e}")
        return None
    except Exception as e:
        print(f"    LLM distillation failed: {e}")
        return None


def distill_files(file_list: list, dry_run=False) -> list:
    """
    Phase 3: 对候选文件列表 LLM 蒸馏（批量，1 次 API 调用）。
    返回 [{"file":..., "result":{...}}, ...]
    """
    if not file_list:
        print("[Phase 3] No candidates to distill.")
        return []

    print(f"[Phase 3] Distilling {len(file_list)} candidate(s)...")

    if dry_run:
        results = []
        for item in file_list:
            rel_path = item["file"]
            top_dir = item["top_dir"]
            _, distill_type = ROUTE_MAP.get(top_dir, ("domains", "knowledge"))
            print(f"  [DRY] Would distill: {rel_path} (type={distill_type})")
            results.append({"file": rel_path, "result": None, "dry": True})
        return results

    # 批量：收集所有文件内容和类型，1 次 API 调用
    from gateway_client import chat
    from pathlib import Path as _Path

    items = []
    prompts_list = _get_distill_prompts()
    for item in file_list:
        rel_path = item["file"]
        top_dir = item["top_dir"]
        _, distill_type = ROUTE_MAP.get(top_dir, ("domains", "knowledge"))
        content = _read_text(_Path(item["absolute"]))
        if not content:
            continue
        prompt_template = prompts_list.get(distill_type, prompts_list.get("knowledge", ""))
        items.append((rel_path, top_dir, distill_type, content, prompt_template))

    if not items:
        return []

    print(f"  → Batch distilling {len(items)} files in 1 API call...")

    parts = []
    for i, (rel_path, top_dir, distill_type, content, prompt_template) in enumerate(items):
        prompt = prompt_template.replace("{content}", content[:3000])
        parts.append(f"### File {i}: {rel_path} (type={distill_type})\n{prompt}")

    combined = (
        "Process each file below independently. "
        "Output exactly one JSON object per file, separated by a blank line. "
        "No markdown fences, no extra commentary.\n\n"
        + "\n\n".join(parts)
        + f"\n\nOutput {len(items)} JSON objects, one per line, in file order:"
    )

    try:
        result = chat(
            messages=combined,
            model=LLM_MODEL_HEADER,
            temperature=0.1,
            max_tokens=500 * len(items),
            timeout=30 + 30 * len(items),
        )
    except Exception as e:
        print(f"    Batch distillation failed: {e}")
        return []

    if not result:
        return []

    text = result["content"].strip()
    if text.startswith("```"):
        text = __import__("re").sub(
            r"^```(?:json)?\s*|\s*```$", "", text, flags=__import__("re").MULTILINE
        )

    # Parse one JSON object per non-empty line
    parsed = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            parsed.append(obj)
        except json.JSONDecodeError:
            parsed.append(None)

    results = []
    for i, (rel_path, top_dir, distill_type, _, _) in enumerate(items):
        if i < len(parsed) and parsed[i]:
            r = parsed[i]
            r["type"] = distill_type
            r["top_dir"] = top_dir
            results.append({"file": rel_path, "result": r})
            print(f"    → \"{r['title']}\" (confidence: {r['confidence']})")
        else:
            print(f"    → FAILED: {rel_path}")

    return results


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  PHASE 4: WRITE TO SELF-IMPROVING                                 ║
# ╚═════════════════════════════════════════════════════════════════════╝

def _write_domains_rule(result: dict, source_file: str) -> Path:
    """
    将知识规则写入 domains/ 目录。
    自动按 title 生成文件名。
    """
    topic = re.sub(r'[\\/:*?"<>|]', '-', result["title"])
    out_file = SELF_IMPROVING / "domains" / f"{topic}.md"

    content = (
        f"## {result['title']}\n"
        f"- {result['rule']}\n"
        f"- 适用场景: {result['when']}\n"
        f"- 原因: {result['why']}\n"
        f"- 来源: [[{source_file}]]\n"
        f"- 置信度: {result['confidence']}/10\n"
        f"- 升格于: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    )
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(content, encoding="utf-8")
    return out_file


def _write_memory_rule(result: dict, source_file: str) -> Path:
    """
    将行为规则追加到 memory.md 的 Rules 区域。
    写入前备份 memory.md → memory.md.bak。
    """
    # 备份
    if MEMORY_FILE.exists():
        shutil.copy2(MEMORY_FILE, MEMORY_FILE.with_suffix(".md.bak"))

    existing = _read_text(MEMORY_FILE)
    if not existing:
        existing = "# Memory (HOT Tier)\n\n## Rules\n"

    rule_block = (
        f"\n## {result['title']}\n"
        f"**规则：** {result['rule']}\n"
        f"**Why：** {result['why']}\n"
        f"**How to apply：** {result['when']}\n"
        f"（来源: {source_file} | 置信度: {result['confidence']}/10 | "
        f"升格于: {datetime.now().strftime('%Y-%m-%d %H:%M')}）\n"
    )

    # 追加到 Rules 区域（找到第一个 ## Rules 后的合适位置）
    rules_idx = existing.find("## Rules")
    if rules_idx >= 0:
        # 找到 ## Rules 后下一个 ## 的位置
        next_section = existing.find("\n## ", rules_idx + 8)
        if next_section < 0:
            next_section = len(existing)
        new_content = (
            existing[:next_section] + rule_block + existing[next_section:]
        )
    else:
        new_content = existing + "\n## Rules\n" + rule_block

    MEMORY_FILE.write_text(new_content, encoding="utf-8")
    return MEMORY_FILE


def _write_project_rule(result: dict, source_file: str) -> Path:
    """
    将项目决策写入 projects/ 目录。
    """
    project = re.sub(r'[\\/:*?"<>|]', '-', result["when"] or result["title"])
    out_file = SELF_IMPROVING / "projects" / f"{project[:60]}.md"

    today = datetime.now().strftime("%Y-%m-%d")
    content = (
        f"## {today}\n"
        f"- **决策: {result['title']}**\n"
        f"- 内容: {result['rule']}\n"
        f"- 原因: {result['why']}\n"
        f"- 来源: [[{source_file}]]\n"
        f"- 置信度: {result['confidence']}/10\n"
        f"- 升格于: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    )
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(content, encoding="utf-8")
    return out_file


WRITE_HANDLERS = {
    "domains":  _write_domains_rule,
    "memory":   _write_memory_rule,
    "projects": _write_project_rule,
}


def write_rules(distilled: list, state: dict, dry_run=False) -> dict:
    """
    Phase 4: 将蒸馏结果写入 self-improving/。
    返回更新后的 state。
    """
    if not distilled:
        print("[Phase 4] Nothing to write.")
        return state

    print(f"[Phase 4] Writing {len(distilled)} rule(s)...")
    now_iso = datetime.now(timezone.utc).isoformat()
    elevated = state.setdefault("elevated", {})

    for entry in distilled:
        if entry.get("dry"):
            continue

        result = entry["result"]
        if not result:
            continue

        source_file = entry["file"]
        top_dir = result.get("top_dir", "02-知识")
        target, _ = ROUTE_MAP.get(top_dir, ("domains", "knowledge"))
        handler = WRITE_HANDLERS.get(target, _write_domains_rule)

        if dry_run:
            print(f"  [DRY] Would write to {target}/: {result['title']}")
            continue

        try:
            out_path = handler(result, source_file)
            print(f"  ✓ {target}/: {result['title']} → {out_path.name}")

            # 更新状态
            elevated[source_file] = {
                "target": target,
                "title": result["title"],
                "elevated_at": now_iso,
                "confidence": result["confidence"],
            }
        except Exception as e:
            print(f"  ✗ Write failed for {result['title']}: {e}")

    state["elevated"] = elevated
    state["last_elevation"] = now_iso
    _save_json(RULE_STATE_FILE, state)
    return state


def write_candidates(candidates: list, dry_run=False):
    """
    将未达自动升格阈值的候选写入 .candidates/ 供人工审核。
    """
    if not candidates:
        return

    CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    out_file = CANDIDATES_DIR / f"candidates-{today}.json"

    existing = _load_json(out_file, [])
    existing.extend(candidates)
    _save_json(out_file, existing)

    if dry_run:
        print(f"  [DRY] Would write {len(candidates)} to candidates file")
    else:
        print(f"  Candidates saved: {out_file} ({len(candidates)} entries)")


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  PHASE 5: DE-ESCALATION                                           ║
# ╚═════════════════════════════════════════════════════════════════════╝

def de_escalate(state: dict, dry_run=False) -> dict:
    """
    Phase 5: 检查已升格规则是否过期。
    - 30 天未被引用 + 源文件未更新 → 移入 archive/
    - frontmatter deprecated: true → 立即降级
    """
    print("[Phase 5] Checking for stale rules...")
    elevated = state.get("elevated", {})
    if not elevated:
        print("  No elevated rules to check.")
        return state

    now = datetime.now(timezone.utc)
    mentions_cache = _build_mentions_cache()
    archive_dir = SELF_IMPROVING / "archive"
    removed = 0

    for file_key in list(elevated.keys()):
        entry = elevated[file_key]

        # 检查是否有 deprecated 标记
        full_path = VAULT / file_key
        content = _read_text(full_path)
        fm = _parse_frontmatter(content) if content else {}

        should_remove = False
        reason = ""

        if fm.get("deprecated"):
            should_remove = True
            reason = "frontmatter deprecated"
        else:
            # 检查引用
            refs = mentions_cache.get(file_key, 0)
            # 检查源文件 mtime
            try:
                mtime = os.path.getmtime(str(full_path))
                age_days = (now.timestamp() - mtime) / 86400
            except OSError:
                age_days = 999

            elevated_at = entry.get("elevated_at", "")
            try:
                elevated_dt = datetime.fromisoformat(elevated_at)
                elevated_days = (now - elevated_dt).days
            except ValueError:
                elevated_days = 999

            if refs == 0 and age_days > DEESCALATE_DAYS and elevated_days > DEESCALATE_DAYS:
                should_remove = True
                reason = f"no refs in {elevated_days}d, source age {age_days:.0f}d"

        if should_remove:
            if dry_run:
                print(f"  [DRY] Would de-escalate: {file_key} ({reason})")
            else:
                # 移动规则文件到 archive
                target = entry.get("target", "domains")
                title = entry.get("title", file_key)
                safe_name = re.sub(r'[\\/:*?"<>|]', '-', title)
                # 查找并移动
                for ext_dir in ["domains", "projects"]:
                    candidate = SELF_IMPROVING / ext_dir / f"{safe_name}.md"
                    if candidate.exists():
                        archive_dir.mkdir(parents=True, exist_ok=True)
                        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest = archive_dir / f"{ts}_{safe_name}.md"
                        shutil.move(str(candidate), str(dest))
                        print(f"  ↓ Archived: {candidate.name} → archive/ ({reason})")
                        break

            del elevated[file_key]
            removed += 1

    print(f"  De-escalated: {removed} rule(s)")
    state["elevated"] = elevated
    _save_json(RULE_STATE_FILE, state)
    return state


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  FORCE ELEVATION: 手动升格指定文件                                  ║
# ╚═════════════════════════════════════════════════════════════════════╝

def force_elevate(rel_path: str, state: dict, dry_run=False) -> dict:
    """
    手动升格指定文件（--force）。
    跳过评分，直接用 LLM 蒸馏并写入。
    """
    full_path = VAULT / rel_path
    if not full_path.exists():
        print(f"ERROR: File not found: {full_path}")
        return state

    top_dir = rel_path.split(os.sep)[0]
    if top_dir not in ROUTE_MAP:
        print(f"ERROR: {top_dir} not in elevation scope")
        return state

    target, distill_type = ROUTE_MAP[top_dir]
    content = _read_text(full_path)
    if not content:
        print(f"ERROR: Cannot read {full_path}")
        return state

    print(f"[Force] Elevating: {rel_path} ({distill_type} → {target})")

    if dry_run:
        print("  [DRY] Would distill and write")
        return state

    result = _llm_distill(content, distill_type)
    if not result:
        print("  Distillation FAILED")
        return state

    result["type"] = distill_type
    result["top_dir"] = top_dir

    print(f"  Distilled: \"{result['title']}\" (confidence: {result['confidence']})")

    # 写入
    handler = WRITE_HANDLERS.get(target, _write_domains_rule)
    out_path = handler(result, rel_path)
    print(f"  Written: {out_path}")

    # 更新状态
    now_iso = datetime.now(timezone.utc).isoformat()
    state.setdefault("elevated", {})[rel_path] = {
        "target": target,
        "title": result["title"],
        "elevated_at": now_iso,
        "confidence": result["confidence"],
    }
    state["last_elevation"] = now_iso
    _save_json(RULE_STATE_FILE, state)
    return state


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  MAIN                                                             ║
# ╚═════════════════════════════════════════════════════════════════════╝

def main():
    parser = argparse.ArgumentParser(
        description="elevate_frequent.py — vault 高频内容自动升格"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="只评分/预览，不写入")
    parser.add_argument("--force", type=str, metavar="REL_PATH",
                        help="手动升格指定 vault 文件（相对路径）")
    parser.add_argument("--de-escalate-only", action="store_true",
                        help="只执行降级清理")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"候选阈值（默认 {DEFAULT_THRESHOLD}）")
    parser.add_argument("--score-only", action="store_true",
                        help="只评分，不蒸馏不写入不降级")
    opts = parser.parse_args()

    # 加载状态
    state = _load_json(RULE_STATE_FILE, {"elevated": {}, "last_elevation": ""})

    # ── 只降级模式 ──
    if opts.de_escalate_only:
        de_escalate(state, dry_run=opts.dry_run)
        return

    # ── 手动升格模式 ──
    if opts.force:
        force_elevate(opts.force, state, dry_run=opts.dry_run)
        return

    # ── 标准流程 ──
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
          f"elevate_frequent.py (threshold={opts.threshold})")

    # Phase 1 & 2: Scoring + Candidate
    scored = score_all_files(dry_run=opts.dry_run)

    if opts.score_only:
        print("\n[OK] Score-only mode. Done.")
        return

    auto_list, candidate_list = filter_candidates(scored, opts.threshold, state)

    print(f"\n[Phase 2] Candidates: {len(auto_list)} auto, "
          f"{len(candidate_list)} review")

    # Phase 3: Distill (auto + candidates 都蒸馏，但 auto 直接写入)
    all_to_distill = auto_list + candidate_list
    distilled = distill_files(all_to_distill, dry_run=opts.dry_run)

    # 区分 auto 和 candidate 的蒸馏结果
    auto_files = {a["file"] for a in auto_list}
    auto_distilled = [d for d in distilled if d["file"] in auto_files]
    review_distilled = [d for d in distilled if d["file"] not in auto_files]

    # Phase 4: Write
    if auto_distilled:
        print(f"\n[Phase 4] Auto-elevating {len(auto_distilled)} rule(s)...")
        state = write_rules(auto_distilled, state, dry_run=opts.dry_run)
    else:
        print("\n[Phase 4] No auto-elevation candidates.")

    # 未达 auto 的蒸馏结果写入 candidates 目录
    if review_distilled:
        candidate_results = []
        for d in review_distilled:
            if d.get("result"):
                candidate_results.append({
                    "file": d["file"],
                    "title": d["result"]["title"],
                    "rule": d["result"]["rule"],
                    "why": d["result"]["why"],
                    "when": d["result"]["when"],
                    "confidence": d["result"]["confidence"],
                    "composite": next(
                        (s["composite"] for s in scored if s["file"] == d["file"]), 0
                    ),
                })
        if candidate_results:
            write_candidates(candidate_results, dry_run=opts.dry_run)

    # Phase 5: De-escalate
    state = de_escalate(state, dry_run=opts.dry_run)

    print(f"\n[OK] elevate_frequent.py complete.")
    print(f"  Auto-elevated: {len(auto_distilled)}")
    print(f"  Review candidates: {len(review_distilled)}")


if __name__ == "__main__":
    main()
