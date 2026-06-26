#!/usr/bin/env python3
"""
Context Assembler — Phase 1 原型
用法: python3 assembler.py --task <type|description> [--max-tokens N] [--date YYYY-MM-DD]

输出: 优化后的 context injection block (纯文本, 直接拼到 prompt 前)
"""

import argparse
import os
import re
import sys
import yaml
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path(__file__).resolve().parents[3]))
SKILL_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"

# ============================================================
# 1. Load genome
# ============================================================

def load_genome():
    path = SKILL_DIR / "genome.yml"
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}

# ============================================================
# 2. Task Classifier
# ============================================================

def classify_task(task_desc, genome):
    """通过关键词匹配判断任务类型"""
    keywords = genome.get("task_keywords", {})
    desc_lower = task_desc.lower()
    scores = {}
    for task_type, kws in keywords.items():
        score = sum(1 for kw in kws if kw.lower() in desc_lower)
        if score > 0:
            scores[task_type] = score
    if scores:
        return max(scores, key=scores.get)
    return "chat"  # 默认

# ============================================================
# 3. Semantic Projection (Phase 1: keyword-based)
# ============================================================

def extract_memory_sections(filepath):
    """从 markdown 文件中按 ## 标题切分为 chunk，同时提取子标题内容"""
    chunks = []
    if not filepath.exists():
        return chunks
    text = filepath.read_text(encoding="utf-8", errors="ignore")
    # 按 ## 标题分块（主 section）
    sections = re.split(r'\n(?=## )', text)
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        title_match = re.match(r'^## (.+)', sec)
        title = title_match.group(1).strip() if title_match else sec[:60]
        chunks.append({
            "source": str(filepath.relative_to(WORKSPACE)),
            "title": title,
            "text": sec,
            "char_count": len(sec)
        })
        # 同时提取子标题（### ）作为独立 chunk
        subs = re.split(r'\n(?=### )', sec)
        if len(subs) > 1:
            for sub in subs[1:]:  # 跳过第一个（已在主 chunk 中）
                sub = sub.strip()
                if not sub:
                    continue
                sub_title_match = re.match(r'^### (.+)', sub)
                sub_title = sub_title_match.group(1).strip() if sub_title_match else sub[:60]
                chunks.append({
                    "source": str(filepath.relative_to(WORKSPACE)),
                    "title": f"{title} > {sub_title}",
                    "text": sub,
                    "char_count": len(sub)
                })
    return chunks

def keyword_match_score(chunk, query_terms, synonyms=None):
    """关键词匹配分数，扫描标题+正文，支持同义词展开"""
    text_lower = (chunk.get("title", "") + " " + chunk.get("text", ""))[:2000].lower()
    score = 0
    for term in query_terms:
        term_lower = term.lower()
        if len(term_lower) < 3:
            continue
        # 展开同义词
        expanded_terms = [term_lower]
        if synonyms:
            for syn_key, syn_list in synonyms.items():
                if term_lower == syn_key.lower() or term_lower in [s.lower() for s in syn_list]:
                    expanded_terms.extend([s.lower() for s in syn_list])
                    expanded_terms.append(syn_key.lower())
        # 匹配任一展开词
        matched = False
        for et in set(expanded_terms):
            if et in text_lower:
                score += 1
                matched = True
                break
        if not matched:
            # 部分匹配（2-3 字短词的子串匹配）
            if len(term_lower) >= 4:
                for et in set(expanded_terms):
                    if len(et) >= 4 and any(et[i:i+2] in text_lower for i in range(0, len(et)-1, 2)):
                        score += 0.5
                        break
    return score

def semantic_project(query, genome, task_type):
    """从 MEMORY.md + daily notes 召回相关 chunk"""
    profile = genome.get("task_profiles", {}).get(task_type, {})
    sources = profile.get("sources", ["MEMORY.md", "daily_notes"])
    recency_days = profile.get("recency_range_days", 7)
    
    results = []
    
    # 构建搜索词：从 query + task_type 关键词提取
    task_kws = genome.get("task_keywords", {}).get(task_type, [])
    query_terms = set(query.lower().split())
    query_terms.update(k.lower() for k in task_kws[:5])
    
    # 加载同义词表
    synonyms = genome.get("synonyms", {})
    
    # 搜索 MEMORY.md
    if "MEMORY.md" in sources:
        mem_file = WORKSPACE / "MEMORY.md"
        for chunk in extract_memory_sections(mem_file):
            score = keyword_match_score(chunk, query_terms, synonyms)
            if score > 0:
                # 读取文件修改时间作为新鲜度
                mtime = mem_file.stat().st_mtime if mem_file.exists() else 0
                days_old = (datetime.now().timestamp() - mtime) / 86400
                freshness = max(0.1, 1.0 - days_old / recency_days)
                results.append({
                    **chunk,
                    "score": score * freshness,
                    "relevance": "high" if score >= 3 else "medium"
                })
    
    # 搜索 daily notes (最近 N 天)
    if "daily_notes" in sources:
        cutoff = datetime.now() - timedelta(days=recency_days)
        for f in sorted(MEMORY_DIR.glob("*.md"), reverse=True):
            date_str = f.stem
            try:
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                if file_date < cutoff:
                    continue
            except ValueError:
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            # 提取 "## " 开头的行作为事件摘要
            event_lines = re.findall(r'^## (.+)$', text, re.MULTILINE)
            for line in event_lines:
                score = keyword_match_score({"text": line}, query_terms, synonyms)
                if score > 0:
                    days_old = (datetime.now() - file_date).days
                    freshness = max(0.1, 1.0 - days_old / (recency_days * 2))
                    results.append({
                        "source": f"memory/{f.name}",
                        "title": line.strip(),
                        "text": line.strip(),
                        "char_count": len(line),
                        "score": score * freshness,
                        "relevance": "medium" if score >= 2 else "low",
                        "date": date_str
                    })
    
    # 搜索 preferences.md（用户偏好）
    prefs_file = MEMORY_DIR / "improvements" / "preferences.md"
    if prefs_file.exists() and "preferences_md" in sources:
        text = prefs_file.read_text(encoding="utf-8", errors="ignore")
        score = keyword_match_score({"text": text}, query_terms, synonyms)
        if score > 0:
            results.append({
                "source": "memory/improvements/preferences.md",
                "title": "用户偏好",
                "text": text[:800],
                "char_count": min(len(text), 800),
                "score": score * 0.8,
                "relevance": "medium"
            })
    
    # 按分数排序，去重
    results.sort(key=lambda x: x["score"], reverse=True)
    seen = set()
    unique = []
    for r in results:
        key = (r["source"], r["title"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    
    return unique

# ============================================================
# 4. Timeline Collapser
# ============================================================

def collapse_timeline(genome, lookback_days=7):
    """读取 daily notes，坍缩为结构化时间线"""
    rules = genome.get("timeline", {})
    collapse_threshold = rules.get("collapse_same_failure_threshold", 2)
    high_value_patterns = rules.get("high_value_signals", [])
    noise_patterns = rules.get("noise_patterns", [])
    
    cutoff = datetime.now() - timedelta(days=lookback_days)
    events = []
    failure_counts = {}  # 追踪重复失败
    
    for f in sorted(MEMORY_DIR.glob("*.md"), reverse=True):
        try:
            file_date = datetime.strptime(f.stem, "%Y-%m-%d")
            if file_date < cutoff:
                continue
        except ValueError:
            continue
        
        text = f.read_text(encoding="utf-8", errors="ignore")
        
        # 提取 ## 和 ### 标题作为事件
        raw_sections = re.findall(r'^(#{2,3}) (.+)$', text, re.MULTILINE)
        
        for level, sec_title in raw_sections:
            title = sec_title.strip()
            date_str = f.stem
            sub_indent = "  " if level == "###" else ""
            
            # 读取该 section 的完整文本用于匹配（标题+正文）
            pattern = re.escape(f"{level} {title}")
            m = re.search(pattern + r'(.*?)(?=\n#{2,3} |\Z)', text, re.DOTALL)
            body = m.group(0) if m else title
            
            # 检查是否为噪音
            is_noise = any(re.search(p, title) for p in noise_patterns)
            
            # 检查是否为高价值（检查标题和正文）
            is_high = any(re.search(p, title + " " + body[:200]) for p in high_value_patterns)
            
            # 检查是否为失败
            is_failure = bool(re.search(r"失败|错误|timeout|超时|异常|fail|error|bug", title, re.IGNORECASE))
            
            if is_failure:
                # 追踪重复失败
                fail_key = re.sub(r'\d+', 'N', title)  # 数字归一化
                failure_counts[fail_key] = failure_counts.get(fail_key, 0) + 1
            
            events.append({
                "date": date_str,
                "title": sub_indent + title,
                "is_noise": is_noise,
                "is_high": is_high,
                "is_failure": is_failure,
                "weight": 0.3 if is_noise else (1.5 if is_high else 1.0)
            })
    
    # 构建时间线输出
    lines = []
    shown_collapsed = set()
    
    for evt in events:
        if evt["is_noise"]:
            continue
        
        prefix = ""
        if evt["is_failure"]:
            fail_key = re.sub(r'\d+', 'N', evt["title"])
            count = failure_counts.get(fail_key, 1)
            if count >= collapse_threshold and fail_key not in shown_collapsed:
                prefix = "⚠️ 重复失败 (已坍缩): "
                shown_collapsed.add(fail_key)
            elif count < collapse_threshold:
                prefix = "⚠️ "
        
        if evt["is_high"]:
            prefix = "🌟 "
        
        lines.append(f"  {evt['date']}  {prefix}{evt['title']}")
    
    # 检测断点：检查 lookback 范围内的缺失日期
    today = datetime.now()
    missing_dates = []
    for d in range(lookback_days):
        day = today - timedelta(days=d)
        date_str = day.strftime("%Y-%m-%d")
        f = MEMORY_DIR / f"{date_str}.md"
        if not f.exists():
            missing_dates.append(date_str)
    if missing_dates:
        lines.insert(0, f"  ⚠️ 缺失日志: {', '.join(sorted(missing_dates))} （无结构化记录，自检基准缺失）")
    
    return lines[:25]  # 最多 25 行

# ============================================================
# 5. Forbidden Pattern Detector
# ============================================================

def detect_forbidden_patterns(genome, lookback_days=14):
    """检测重复失败路径，生成禁止模式"""
    rules = genome.get("timeline", {})
    collapse_threshold = rules.get("collapse_same_failure_threshold", 2)
    
    cutoff = datetime.now() - timedelta(days=lookback_days)
    failure_tracker = {}
    
    for f in sorted(MEMORY_DIR.glob("*.md"), reverse=True):
        try:
            file_date = datetime.strptime(f.stem, "%Y-%m-%d")
            if file_date < cutoff:
                continue
        except ValueError:
            continue
        
        text = f.read_text(encoding="utf-8", errors="ignore")
        # 提取 ## 和 ### 标题
        sections = re.findall(r'^(#{2,3}) (.+)$', text, re.MULTILINE)
        
        for level, title in sections:
            if re.search(r'失败|错误|timeout|超时|异常|fail|error', title, re.IGNORECASE):
                # 归一化：替换数字、日期等为通配符
                normalized = re.sub(r'\d{4}-\d{2}-\d{2}', 'YYYY-MM-DD', title)
                normalized = re.sub(r'\d+', 'N', normalized)
                normalized = re.sub(r'v\d+\.\d+\.\d+', 'vX.X.X', normalized)
                key = normalized.strip()
                failure_tracker[key] = failure_tracker.get(key, 0) + 1
    
    forbidden = []
    for pattern, count in failure_tracker.items():
        if count >= collapse_threshold:
            forbidden.append(f"  - {pattern}（已失败 {count} 次，禁止重试）")
    
    return forbidden

# ============================================================
# 6. Context Packer
# ============================================================

def pack_context(task_desc, task_type, genome, memory_results, timeline, forbidden, max_tokens):
    """组装最终 context block"""
    profile = genome.get("task_profiles", {}).get(task_type, {})
    budget = profile.get("max_tokens", max_tokens or 1200)
    
    # 估算 char 到 token：~4 chars/token
    char_budget = budget * 4
    used = 0
    
    blocks = []
    
    # ── Block 1: Identity（始终注入，约 200 chars）──
    # Reads from AGENT_NAME env var, falls back to generic
    agent_name = os.environ.get("AGENT_NAME", "your personal AI agent")
    identity = f"""=== IDENTITY [永久] ===
你是 {agent_name} 的 personal AI agent。你有深度分析能力和自我进化机制。
"""
    blocks.append(identity)
    used += len(identity)
    
    # ── Block 2: Task Context ──
    date_str = datetime.now().strftime("%Y-%m-%d")
    task_block = f"""=== TASK CONTEXT ===
任务: {task_desc}
时间: {date_str} (GMT+8)
"""
    blocks.append(task_block)
    used += len(task_block)
    
    # ── Block 3: Relevant Memory（按预算截断）──
    if memory_results:
        mem_header = "=== RELEVANT MEMORY [语义投影] ===\n"
        mem_lines = [mem_header]
        remaining = char_budget - used - len(mem_header)
        
        for r in memory_results:
            line = f"[{r['relevance']}] {r['source']}: {r['title'][:120]}\n"
            if len(line) <= remaining:
                mem_lines.append(line)
                remaining -= len(line)
            else:
                break
        
        # Add context snippets for high-relevance hits (up to 3)
        high_relevance = [r for r in memory_results if r["relevance"] == "high"][:3]
        for r in high_relevance:
            snippet = r["text"][:300].replace("\n", " ")
            line = f"  摘要: {snippet}\n"
            if len(line) <= remaining:
                mem_lines.append(line)
                remaining -= len(line)
        
        mem_block = "".join(mem_lines)
        blocks.append(mem_block)
        used += len(mem_block)
    
    # ── Block 4: Timeline ──
    if timeline:
        tl_header = "=== TODAY'S EVENT TIMELINE [时间线坍缩] ===\n"
        tl_lines = [tl_header]
        remaining = char_budget - used
        
        for line in timeline:
            ln = f"{line}\n"
            if len(ln) > remaining:
                break
            tl_lines.append(ln)
            remaining -= len(ln)
        
        tl_block = "".join(tl_lines)
        blocks.append(tl_block)
        used += len(tl_block)
    
    # ── Block 5: Forbidden Patterns ──
    if forbidden:
        forb_header = "=== FORBIDDEN PATTERNS [历史失败，禁止重试] ===\n"
        forb_lines = [forb_header]
        remaining = char_budget - used
        
        for fp in forbidden[:5]:
            ln = f"{fp}\n"
            if len(ln) <= remaining:
                forb_lines.append(ln)
                remaining -= len(ln)
        
        forb_block = "".join(forb_lines)
        blocks.append(forb_block)
        used += len(forb_block)
    
    # ── Block 6: Core Rules ──
    if profile.get("require_rules_core"):
        rules = """=== CORE RULES ===
- 操作前先写方案，等确认再动手
- trash > rm（删文件优先回收站）
- 严格按事实陈述，标明信源
"""
        blocks.append(rules)
        used += len(rules)
    
    # ── Block 6b: Evolution-specific boot knowledge ──
    if task_type == "daily_evolution_check":
        evo_ctx = """=== EVOLUTION CONTEXT [自检背景] ===
旧版进化自检于 2026-05-17 被删除，原因：AI 自检 AI 本质无效，
检查不出自己的盲点。旧版问题：静态 context 注入导致输出空洞、
缺乏可对比的基准。

新版改进：
- Context Assembler 提供动态记忆注入
- 时间线坍缩避免重复失败
- 禁止模式阻止踩旧坑
- 聚焦"决策质量"而非"做了什么"
"""
        blocks.append(evo_ctx)
        used += len(evo_ctx)
    
    # ── Block 7: Task Directive ──
    blocks.append(f"\n=== TASK ===\n{task_desc}\n")
    
    return "".join(blocks)

# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Context Assembler — Phase 1")
    parser.add_argument("--task", required=True, help="任务描述或任务类型")
    parser.add_argument("--max-tokens", type=int, default=0, help="最大 token 数（0=使用 genome 默认）")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="日期")
    parser.add_argument("--debug", action="store_true", help="输出调试信息到 stderr")
    args = parser.parse_args()
    
    genome = load_genome()
    if not genome:
        print("Error: genome.yml not found", file=sys.stderr)
        sys.exit(1)
    
    # Step 1: Classify
    task_type = classify_task(args.task, genome)
    if args.debug:
        print(f"[DEBUG] Task classified as: {task_type}", file=sys.stderr)
    
    # Step 2: Semantic Projection
    memory_results = semantic_project(args.task, genome, task_type)
    if args.debug:
        print(f"[DEBUG] Memory hits: {len(memory_results)}", file=sys.stderr)
        for r in memory_results[:5]:
            print(f"  [{r['relevance']}] {r['source']}: {r['title'][:60]} (score={r['score']:.2f})", file=sys.stderr)
    
    # Step 3: Timeline Collapse
    timeline = collapse_timeline(genome)
    if args.debug:
        print(f"[DEBUG] Timeline events: {len(timeline)}", file=sys.stderr)
    
    # Step 4: Forbidden Patterns
    forbidden = detect_forbidden_patterns(genome)
    if args.debug:
        print(f"[DEBUG] Forbidden patterns: {len(forbidden)}", file=sys.stderr)
        for fp in forbidden:
            print(f"  {fp}", file=sys.stderr)
    
    # Step 5: Pack
    output = pack_context(args.task, task_type, genome, memory_results, timeline, forbidden, args.max_tokens)
    
    char_count = len(output)
    estimated_tokens = char_count // 4
    if args.debug:
        print(f"[DEBUG] Output: {char_count} chars (~{estimated_tokens} tokens)", file=sys.stderr)
    
    print(output)
    
    # 写反馈日志
    feedback_log = {
        "timestamp": datetime.now().isoformat(),
        "task": args.task,
        "task_type": task_type,
        "memory_hits": len(memory_results),
        "timeline_events": len(timeline),
        "forbidden_patterns": len(forbidden),
        "output_chars": char_count,
        "estimated_tokens": estimated_tokens
    }
    
    import json
    log_path = SKILL_DIR / "feedback" / "outcomes.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps(feedback_log, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
