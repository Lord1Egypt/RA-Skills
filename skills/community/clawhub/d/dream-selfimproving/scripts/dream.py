#!/usr/bin/env python3
"""
Dream — Phase 2 蒸馏脚本 v5.1

v5.1 核心改进（skill-evolver 整合）：
  - GapDetector v2.0：detect_and_generate() 同时返回缺口 + SKILL.md 草稿
  - generate_skill_draft()：11种能力模板（deep-researcher, image-generator 等）
  - E6/E8 流程重写：草稿直接写入 ~/SharedSkills/{skill_name}/SKILL.md
  - M-FLOW 倒锥知识图谱：Entity→FacetPoint→Facet→Episode 四层结构
  - Bundle Search 检索替代简单grep：锥尖广撒网→代价传播→最小路径Episode
  - 语义边：边携带描述文本，参与向量检索
  - 健康评分新增图连通性指标

v3.3: 新增 Distillation Agent（子会话）
v3.3: Phase 1+2 完整闭环，hippocampus 实时日志
"""

import os
import sys
import json
import argparse
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# M-FLOW Bundle Search（无embedding时用词袋模型）
import math as _math
import hashlib as _hl

GRAPH_SKILL_DIR = Path(__file__).parent.parent
BUNDLE_SEARCH_SCRIPT = GRAPH_SKILL_DIR / "bundle-search.py"
LONGTERM_SCRIPT = GRAPH_SKILL_DIR / "scripts" / "longterm_rag.py"

GRAPH_BUILDER_SCRIPT = GRAPH_SKILL_DIR / "graph-builder.py"

# v5.0 扩展模块
EXTENSIONS_DIR = GRAPH_SKILL_DIR / "extensions"

# v5.0: 导入扩展模块
try:
    sys.path.insert(0, str(EXTENSIONS_DIR))
    from skill_evolution import SkillScorer, DecayEngine, SkillRegistry
    from work_review import WorkAnalyzer, TomorrowPlanner
    from skill_explorer import GapDetector, SkillLearner
    from skill_developer import SkillGenerator, SkillQualityAssessor
    from reporter import DailyReporter, SkillReportGenerator
    EXTENSIONS_AVAILABLE = True
except ImportError as e:
    print(f"   [警告] 扩展模块导入失败: {e}")
    EXTENSIONS_AVAILABLE = False


def mflow_bundle_search(query: str, top_k: int = 5) -> list[dict]:
    """
    调用 bundle-search.py 执行 M-FLOW Bundle Search 检索。
    返回 top_k 个 Episode dicts（含 score、matched_facetpoints）。
    """
    import subprocess
    try:
        result = subprocess.run(
            [sys.executable, str(BUNDLE_SEARCH_SCRIPT),
             query, "--top-k", str(top_k), "--quiet", "--json"],
            capture_output=True, text=True, timeout=30,
            encoding="utf-8", errors="replace",
            cwd=str(GRAPH_SKILL_DIR)
        )
        if result.returncode == 0 and result.stdout and result.stdout.strip():
            return json.loads(result.stdout)
        return []
    except Exception as e:
        print(f"   [BundleSearch] 检索失败: {e}")
        return []


def mflow_build_graph(enrich_recall: bool = False, enrich_errors: bool = False):
    """调用 graph-builder.py 构建/更新图
    enrich_recall=True 时同时从Recall Store富化FacetPoints
    enrich_errors=True 时同时从.learnings/ERRORS.md富化FacetPoints"""
    import subprocess
    args = [sys.executable, str(GRAPH_BUILDER_SCRIPT), "--build"]
    if enrich_recall:
        args.append("--enrich-from-recall")
    if enrich_errors:
        args.append("--enrich-from-errors")
    try:
        r = subprocess.run(
            args,
            capture_output=True, text=True, timeout=120,
            encoding="utf-8", errors="replace",
            cwd=str(GRAPH_SKILL_DIR)
        )
        if r.returncode == 0:
            out = r.stdout or ""
            lines = [l for l in out.split("\n") if l.strip() and not l.startswith("   [GraphBuilder]")]
            for l in lines:
                print(f"   {l}")
            return True
        else:
            err = (r.stderr or "")[:200]
            print(f"   [GraphBuilder] 构建失败: {err}")
            return False
    except Exception as e:
        print(f"   [GraphBuilder] 调用失败: {e}")
        return False


def mflow_update_graph():
    """调用 graph-builder.py 增量更新今日日志"""
    import subprocess
    try:
        r = subprocess.run(
            [sys.executable, str(GRAPH_BUILDER_SCRIPT), "--update"],
            capture_output=True, text=True, timeout=30,
            encoding="utf-8", errors="replace",
            cwd=str(GRAPH_SKILL_DIR)
        )
        if r.returncode == 0:
            out = r.stdout or ""
            for l in out.split("\n"):
                if l.strip() and not l.startswith("   [GraphBuilder]"):
                    print(f"   {l}")
            return True
        return False
    except Exception:
        return False


def mflow_graph_status() -> dict:
    """返回M-FLOW图的简要状态（供报告用）
    自动检测workspace路径，与graph-builder.py保持一致"""
    _env = os.environ.get("OPENCLAW_WORKSPACE", "")
    if _env:
        _ws = Path(_env)
    else:
        _ws = Path(__file__).resolve().parents[2]
        if not (_ws / "memory").exists():
            _ws = Path.home() / ".openclaw" / "workspace"
    gdir = _ws / "memory" / "graph"
    entities = gdir / "entities.json"
    facetpoints = gdir / "facetpoints.json"
    episodes = gdir / "episodes.json"
    edges = gdir / "edges.json"

    def count(f):
        if not f.exists():
            return 0
        try:
            return len(json.loads(f.read_text(encoding="utf-8")))
        except:
            return 0

    return {
        "entities": count(entities),
        "facetpoints": count(facetpoints),
        "episodes": count(episodes),
        "edges": count(edges),
    }


# M-FLOW 健康权重
MFLOW_WEIGHTS = {
    "freshness": 0.20,
    "coverage": 0.20,
    "coherence": 0.20,
    "graph_connectivity": 0.20,
    "efficiency": 0.10,
    "reachability": 0.10,
}

# Windows UTF-8 fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclaw' / 'workspace'))
MEMORY_DIR = WORKSPACE / 'memory'
DREAMS_DIR = MEMORY_DIR / 'dreams'
TOPICS_DIR = MEMORY_DIR / 'topics'
TRUTH_DIR = MEMORY_DIR / '.truth'
SNAPSHOT_DIR = TRUTH_DIR / 'snapshots'
RECALL_FILE = MEMORY_DIR / '.dreams' / 'short-term-recall.json'
MEMORY_FILE = WORKSPACE / 'MEMORY.md'
INDEX_FILE = MEMORY_DIR / 'index.json'
LEARNINGS_DIR = WORKSPACE / '.learnings'

# ─── Long-Term Memory (RAG Layer) ───────────────────────────────
RAG_DIR = MEMORY_DIR / '.rag'
LONGTERM_FILE = RAG_DIR / 'longterm.jsonl'
MEMORY_K = 200
PROMOTE_AFTER_DAYS = 30

def ensure_rag_dir():
    RAG_DIR.mkdir(exist_ok=True)
    if not LONGTERM_FILE.exists():
        LONGTERM_FILE.write_text('', encoding='utf-8')

def load_longterm(k=50):
    if not LONGTERM_FILE.exists():
        return []
    entries = []
    try:
        lines = LONGTERM_FILE.read_text(encoding='utf-8').strip().split('\n')
        for line in reversed(lines):
            if line.strip():
                try:
                    entries.append(json.loads(line))
                    if len(entries) >= k:
                        break
                except:
                    continue
    except:
        pass
    return list(reversed(entries))

def query_longterm_rag(query, k=5):
    """在长记忆中搜索与 query 相关的条目（简单关键词匹配）。"""
    entries = load_longterm(k * 2)
    if not entries:
        return []
    query_words = set(query.lower().split())
    query_words = {w for w in query_words if len(w) >= 2}
    scored = []
    for entry in entries:
        content = entry.get('snippet', '') or entry.get('content', '')
        content_lower = content.lower()
        matches = sum(1 for w in query_words if w in content_lower)
        if matches > 0:
            scored.append((matches, entry))
    scored.sort(key=lambda x: -x[0])
    return [e for _, e in scored[:k]]

def promote_to_longterm_rag(recall_entries, max_promote=20):
    """将太久未被召回的条目晋升到长记忆。"""
    ensure_rag_dir()
    now = datetime.now()
    promoted = []
    to_remove = []
    for key, entry in recall_entries.items():
        last_recalled = entry.get('lastRecalledAt', '')
        recall_count = entry.get('recallCount', 0)
        if last_recalled:
            try:
                last_dt = datetime.fromisoformat(last_recalled.replace('Z', '+00:00'))
                age_days = (now - last_dt.replace(tzinfo=None)).total_seconds() / 86400
            except:
                continue
        else:
            created = entry.get('createdAt', '')
            if not created:
                continue
            try:
                created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                age_days = (now - created_dt.replace(tzinfo=None)).total_seconds() / 86400
            except:
                continue
        if age_days > PROMOTE_AFTER_DAYS and recall_count < 3:
            entry['promotedAt'] = now.isoformat()
            entry['originalKey'] = key
            promoted.append(entry)
            to_remove.append(key)
    if not promoted:
        return 0
    count = 0
    with LONGTERM_FILE.open('a', encoding='utf-8') as f:
        for entry in promoted[:max_promote]:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            count += 1
    for key in to_remove[:max_promote]:
        recall_entries.pop(key, None)
    return count

WEIGHTS = {
    'frequency': 0.24,
    'relevance': 0.30,
    'diversity': 0.15,
    'recency': 0.15,
    'consolidation': 0.10,
    'conceptual': 0.06,
}

ARCHIVE_AFTER_DAYS = 90
ARCHIVE_MIN_IMPORTANCE = 0.3

TRUTH_FILES = {
    'user_state.md':     '用户当前状态：关注项目/目标/情绪',
    'decisions.md':      '进行中的决策及上下文',
    'pending.md':        '待办事项和已承诺的待回收伏笔',
    'projects.md':      '各项目进度、关键节点',
    'preferences.md':   '用户偏好、沟通风格、禁忌',
    'constraints.md':   '约束边界（不能做的事）',
    'relations.md':     '重要关系、上下文边界、信息壁垒',
}

HIGH_WEIGHT_TAGS = {'correction', 'error', 'decision'}

# ─── 真相文件管理 ───────────────────────────────────────────────

def ensure_truth_dirs():
    TRUTH_DIR.mkdir(exist_ok=True)
    SNAPSHOT_DIR.mkdir(exist_ok=True)
    TOPICS_DIR.mkdir(exist_ok=True)
    for fname in TRUTH_FILES:
        fpath = TRUTH_DIR / fname
        if not fpath.exists():
            fpath.write_text(f"# {fname}\n\n_Last updated: never_\n\n", encoding='utf-8')


def load_truth_files():
    truths = {}
    for fname in TRUTH_FILES:
        fpath = TRUTH_DIR / fname
        truths[fname] = fpath.read_text(encoding='utf-8') if fpath.exists() else ""
    return truths


def save_truth_file(fname, content):
    (TRUTH_DIR / fname).write_text(content, encoding='utf-8')


# ─── Snapshot ───────────────────────────────────────────────────

def create_snapshot():
    ensure_truth_dirs()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    snap_dir = SNAPSHOT_DIR / timestamp
    snap_dir.mkdir(exist_ok=True)
    backed_up = []
    for fname in TRUTH_FILES:
        src = TRUTH_DIR / fname
        if src.exists():
            shutil.copy2(src, dst := snap_dir / fname)
            backed_up.append(fname)
    if INDEX_FILE.exists():
        shutil.copy2(INDEX_FILE, snap_dir / 'index.json')
        backed_up.append('index.json')
    return str(snap_dir), backed_up


def list_snapshots():
    if not SNAPSHOT_DIR.exists():
        return []
    return sorted([d.name for d in SNAPSHOT_DIR.iterdir() if d.is_dir()], reverse=True)[:10]


# ─── 数据加载 ─────────────────────────────────────────────────

def load_recall():
    if not RECALL_FILE.exists():
        return {}
    try:
        return json.loads(RECALL_FILE.read_text(encoding='utf-8')).get('entries', {})
    except (json.JSONDecodeError, IOError):
        return {}


def load_index():
    if not INDEX_FILE.exists():
        return {'entries': [], 'stats': {'totalEntries': 0}}
    try:
        return json.loads(INDEX_FILE.read_text(encoding='utf-8'))
    except:
        return {'entries': [], 'stats': {'totalEntries': 0}}


def load_learnings():
    learnings = {}
    for fname in ['LEARNINGS.md', 'ERRORS.md', 'FEATURE_REQUESTS.md']:
        path = LEARNINGS_DIR / fname
        if path.exists():
            learnings[fname] = path.read_text(encoding='utf-8')
    return learnings


def load_today_log(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    log_path = MEMORY_DIR / 'logs' / date_obj.strftime('%Y/%m') / f'{date_str}.md'
    if log_path.exists():
        return log_path.read_text(encoding='utf-8')
    return ""


def load_hippocampus_log(date_str):
    """读取 hippocampus 原始日志，返回条目列表"""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    log_path = MEMORY_DIR / 'logs' / date_obj.strftime('%Y/%m') / f'{date_str}.md'
    if not log_path.exists():
        return []
    raw = log_path.read_text(encoding='utf-8')
    entries = []
    current_time = ''
    for line in raw.split('\n'):
        line = line.strip()
        if line.startswith('## '):
            current_time = line[3:].strip()
            continue
        if not line.startswith('- ['):
            continue
        m = re.match(r'^-\s+\[(\w+)\]\s+(.+?)(?:\s+—\s+weight:\s+HIGH)?$', line, re.IGNORECASE)
        if not m:
            m2 = re.match(r'^-\s+\[(\w+)\]\s+(.+)$', line)
            if not m2:
                continue
            tag, content = m2.groups()
        else:
            tag, content = m.groups()
        content = content.strip()
        tag = tag.lower()
        if len(content) < 5:
            continue
        entries.append({
            'time': current_time,
            'type': tag,
            'content': content,
            'high': tag in HIGH_WEIGHT_TAGS,
        })
    return entries


# ─── 数据分析 ─────────────────────────────────────────────────

def compute_deep_score(entry):
    recall_count = entry.get('recallCount', 0)
    freq_score = min(1.0, recall_count / 10)
    relevance_score = entry.get('maxScore', 0.5)
    queries = entry.get('queryHashes', [])
    diversity_score = min(1.0, len(set(queries)) / 5)
    last_recalled = entry.get('lastRecalledAt', '')
    if last_recalled:
        try:
            last_dt = datetime.fromisoformat(last_recalled.replace('Z', '+00:00'))
            age_days = (datetime.now() - last_dt.replace(tzinfo=None)).total_seconds() / 86400
            recency_score = max(0.0, 1.0 - age_days / 30)
        except:
            recency_score = 0.5
    else:
        recency_score = 0.5
    recall_days = entry.get('recallDays', [])
    consolidation_score = min(1.0, len(set(recall_days)) / 7)
    tags = entry.get('conceptTags', [])
    conceptual_score = min(1.0, len(tags) / 10)
    total = (WEIGHTS['frequency'] * freq_score +
             WEIGHTS['relevance'] * relevance_score +
             WEIGHTS['diversity'] * diversity_score +
             WEIGHTS['recency'] * recency_score +
             WEIGHTS['consolidation'] * consolidation_score +
             WEIGHTS['conceptual'] * conceptual_score)
    return {'total': round(total, 4), 'frequency': round(freq_score, 3)}


def thalamus_filter(entries, date_str):
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    return {k: v for k, v in entries.items()
            if date_str in v.get('recallDays', []) or yesterday in v.get('recallDays', [])}


def analyst_scan(tagged_entries, learnings):
    error_count = defaultdict(int)
    error_examples = defaultdict(list)
    if 'ERRORS.md' in learnings:
        for line in learnings['ERRORS.md'].split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            clean = re.sub(r'[`*#\[\]]', '', line).strip()
            if len(clean) > 10:
                error_count[clean[:60]] += 1
                if len(error_examples[clean[:60]]) < 2:
                    error_examples[clean[:60]].append(clean)
    patterns = []
    for err, count in sorted(error_count.items(), key=lambda x: -x[1]):
        if count >= 3:
            patterns.append({'error': err, 'occurrences': count,
                            'examples': error_examples.get(err, []),
                            'root_cause': f'重复 {count} 次'})
    return patterns


def archive_candidates(tagged_entries, index_data):
    now = datetime.now()
    candidates = []
    for key, entry in tagged_entries.items():
        last_recalled = entry.get('lastRecalledAt', '')
        if not last_recalled:
            continue
        try:
            last_dt = datetime.fromisoformat(last_recalled.replace('Z', '+00:00'))
            age_days = (now - last_dt.replace(tzinfo=None)).total_seconds() / 86400
        except:
            continue
        if age_days > ARCHIVE_AFTER_DAYS:
            score = entry.get('_brain_score', {}).get('total', 0)
            if score < ARCHIVE_MIN_IMPORTANCE:
                candidates.append({
                    'key': key, 'path': entry.get('path', ''),
                    'last_recalled': last_recalled[:10], 'age_days': round(age_days, 1),
                    'score': score, 'snippet': entry.get('snippet', '')[:80]
                })
    return sorted(candidates, key=lambda x: x['age_days'], reverse=True)[:10]


def compute_health_metrics(tagged_entries, all_recall_entries, mflow_stats: dict = None):
    """v4.0: 新增M-FLOW图连通性指标"""
    total = len(tagged_entries)
    if total == 0:
        return {'freshness': 0, 'coverage': 0, 'coherence': 0,
                'graph_connectivity': 0, 'efficiency': 0, 'reachability': 0, 'total': 0}
    now = datetime.now()
    recent_keys = set()
    all_total = len(all_recall_entries)
    for k, v in all_recall_entries.items():
        last = v.get('lastRecalledAt', '')
        if last:
            try:
                dt = datetime.fromisoformat(last.replace('Z', '+00:00'))
                if (now - dt.replace(tzinfo=None)).total_seconds() / 86400 <= 30:
                    recent_keys.add(k)
            except:
                pass
    freshness = len(recent_keys) / max(all_total, 1)
    tagged_with_tags = sum(1 for v in tagged_entries.values() if v.get('conceptTags'))
    coverage = tagged_with_tags / max(total, 1)
    multi_day = sum(1 for v in tagged_entries.values() if len(set(v.get('recallDays', []))) > 1)
    coherence = multi_day / max(total, 1)
    efficiency = max(0, 1 - max(0, total - 50) / 100)
    reachability = 1.0

    # v4.0: M-FLOW 图连通性
    graph_episodes = mflow_stats.get("episodes", 0) if mflow_stats else 0
    graph_edges = mflow_stats.get("edges", 0) if mflow_stats else 0
    if graph_episodes > 0 and graph_edges > 0:
        # 简化估算：边/节点比例越高说明图越紧密
        edge_node_ratio = graph_edges / graph_episodes
        graph_connectivity = min(1.0, edge_node_ratio / 2.0)  # 假设 ratio=2 时连通性=1
    else:
        graph_connectivity = 0.0

    w = MFLOW_WEIGHTS
    total_score = min(100.0, (
        w["freshness"] * freshness +
        w["coverage"] * coverage +
        w["coherence"] * coherence +
        w["graph_connectivity"] * graph_connectivity +
        w["efficiency"] * efficiency +
        w["reachability"] * reachability
    ) * 100)

    return {
        'freshness': round(min(freshness, 1.0), 3),
        'coverage': round(min(coverage, 1.0), 3),
        'coherence': round(min(coherence, 1.0), 3),
        'graph_connectivity': round(graph_connectivity, 3),
        'efficiency': round(min(efficiency, 1.0), 3),
        'reachability': round(min(reachability, 1.0), 3),
        'total': round(total_score, 1),
    }


# ─── Auditor ──────────────────────────────────────────────────

def auditor_check(tagged):
    AI_FLAVOR_WORDS = ['仿佛', '忽然', '竟然', '不禁', '心头一震', '恍然大悟',
                        '不禁想到', '不由得', '只觉得', '没想到', '原来是这样']
    flavor_violations = []
    for key, entry in tagged.items():
        snippet = entry.get('snippet', '')
        for word in AI_FLAVOR_WORDS:
            if word in snippet:
                flavor_violations.append({'key': key, 'word': word, 'snippet': snippet[:80]})
    return {'passed': len(flavor_violations) == 0, 'ai_flavor_count': len(flavor_violations),
            'violations': [], 'flavor_violations': flavor_violations}


# ─── Distillation Agent（核心）───────────────────────────────

def run_distillation_agent(date_str, raw_entries, learnings_text, health, patterns, tagged_entries):
    """
    用结构化本地推理做真正的洞察提炼。
    不依赖子进程，直接分析日志内容生成洞察。
    """
    # 优先用 recall store 结构化条目，备用原始日志文件
    use_recall = bool(tagged_entries)

    if use_recall:
        # 用 recall store 的结构化条目（来自真实对话记录）
        recall_lines = []
        for k, v in list(tagged_entries.items())[-50:]:
            snippet = v.get('snippet', '')[:100]
            tag = v.get('_amygdala_tag', 'normal')
            marker = "🔴" if tag in ('error', 'correction') else "  "
            recall_lines.append(f"{marker}[{tag}] {snippet}")
        entry_text = "\n".join(recall_lines) if recall_lines else "(无recall数据)"
        source_note = "（来自recall store，真实对话记录）"
    else:
        # 用原始日志文件
        entry_lines = []
        for e in raw_entries[-50:]:
            marker = "🔴" if e['high'] else "  "
            entry_lines.append(f"{marker}[{e['type']}] {e['content']}")
        entry_text = "\n".join(entry_lines) if entry_lines else "(无原始日志)"
        source_note = "（来自hippocampus日志文件）"

    # 分析用的数据源：如果有 recall store 条目就用它，否则用原始日志
    if use_recall:
        # tagged_entries: key → {snippet, _amygdala_tag, _brain_score, ...}
        entries_for_analysis = tagged_entries
        type_counts = defaultdict(int)
        for v in entries_for_analysis.values():
            t = v.get('_amygdala_tag', 'normal')
            type_counts[t] += 1
        all_snippets = [v.get('snippet', '') for v in entries_for_analysis.values()]
        entry_count = len(entries_for_analysis)
    else:
        entries_for_analysis = raw_entries
        type_counts = defaultdict(int)
        for e in entries_for_analysis:
            type_counts[e['type']] += 1
        all_snippets = [e['content'] for e in entries_for_analysis]
        entry_count = len(entries_for_analysis)

    # 从内容中提取关键主题词（中文 + 英文，兼容乱码内容）
    important_keywords = []
    if all_snippets:
        all_text = " ".join(all_snippets)
        # 提取中文词
        cn_words = re.findall(r'[\u4e00-\U00020000]{3,}', all_text)
        # 提取英文词（至少3字符）
        en_words = re.findall(r'[a-zA-Z]{3,}', all_text)
        word_freq = defaultdict(int)
        stopwords = set(['的是', '是这样', '这个', '那个', '就是', '什么', '怎么', '为什么',
                         '没有', '一个', '可以', '用户', '今天', 'the', 'and', 'for', 'was', 'that',
                         'this', 'with', 'are', 'not', 'but', 'have', 'from', 'they',
                         'been', 'were', 'said', 'each', 'which', 'also', 'than'])
        for w in cn_words:
            if w not in stopwords:
                word_freq[w] += 1
        for w in en_words:
            if w.lower() not in stopwords:
                word_freq[w.lower()] += 1
        # 过滤乱码：只保留有意义的词（至少有2次出现，或单次但有代表性的）
        all_words = sorted(word_freq.items(), key=lambda x: -x[1])
        # 取频率最高的，如果最高频词只出现1次且全是乱码组合，则放弃关键词
        if all_words and all_words[0][1] >= 2:
            important_keywords = all_words[:10]
        elif all_words and all_words[0][1] == 1 and len(all_words) > 3:
            # 频率都偏低，用类型分布作为主要信号
            important_keywords = []

    patterns_text = "\n".join([
        f"- {p['error']} (重复{p['occurrences']}次)"
        for p in patterns[:5]
    ]) if patterns else "(无重复模式)"

    insights = []
    tomorrow_items = []
    topic_candidates = []

    # ── 推理1：连贯性低 → 记忆没有持续追踪
    if health['coherence'] < 0.5:
        insights.append(
            f"连贯性只有 {health['coherence']:.1%}，说明很多话题只聊了一次就被放下了。"
            f"明天有意识地在一件事上多聊几句，别总是新开话题。"
        )

    # ── 推理2：从类型分布判断今天的模式
    if type_counts.get('correction', 0) > 0:
        insights.append(
            f"今天有 {type_counts['correction']} 次被纠正，说明有反复踩坑的情况。"
            f"建议把这些纠正记到 .learnings/ 里，不要第二次踩同一个坑。"
        )
    elif type_counts.get('error', 0) > 0:
        insights.append(
            f"今天出现了 {type_counts['error']} 个错误，需要检查是工具问题还是方法问题。"
        )

    # ── 推理3：从高频关键词判断核心主题（仅在关键词质量好时使用）
    if important_keywords and important_keywords[0][1] >= 2:
        top_kw = important_keywords[:3]
        kw_str = "、".join([f"「{k}」" for k, _ in top_kw])
        if entry_count >= 3:
            insights.append(
                f"今天的核心主题是：{kw_str}。"
                f"共 {entry_count} 条记录，有一定活跃度。"
            )

    # ── 推理4：新鲜度高但连贯低 → 涉猎广但不深入
    if health['freshness'] >= 0.8 and health['coherence'] < 0.5:
        insights.append(
            "新鲜度高但连贯性低——涉猎很广，但每个话题都没有持续追踪。"
            "这是'收集者陷阱'，信息进来了没有消化。下一步要把一个话题聊透。"
        )

    # ── 推理5：patterns 有内容 → 重复错误
    if patterns:
        top_pattern = patterns[0]
        insights.append(
            f"最突出的重复问题是：{top_pattern['error'][:40]}。"
            f"这个问题出现了 {top_pattern['occurrences']} 次，需要建立检查清单。"
        )
        tomorrow_items.append(
            f"针对「{top_pattern['error'][:30]}」建立防复发机制"
        )

    # ── 推理6：从 entries 内容提取具体洞察（支持两种数据格式）
    if use_recall:
        # recall store 格式
        decision_keys = [k for k, v in entries_for_analysis.items() if v.get('_amygdala_tag') == 'decision']
        correction_keys = [k for k, v in entries_for_analysis.items() if v.get('_amygdala_tag') == 'correction']
        decision_snippets = [entries_for_analysis[k].get('snippet', '')[:80] for k in decision_keys[:3]]
        correction_snippets = [entries_for_analysis[k].get('snippet', '')[:80] for k in correction_keys[:3]]
        error_keys = [k for k, v in entries_for_analysis.items() if v.get('_amygdala_tag') == 'error']
    else:
        # 原始日志格式
        decision_entries = [e for e in entries_for_analysis if e.get('type') == 'decision']
        correction_entries = [e for e in entries_for_analysis if e.get('type') == 'correction']
        decision_snippets = [e.get('content', '')[:80] for e in decision_entries[:3]]
        correction_snippets = [e.get('content', '')[:80] for e in correction_entries[:3]]
        error_keys = [e for e in entries_for_analysis if e.get('type') == 'error']

    if decision_snippets:
        insights.append(
            f"今天做了 {len(decision_snippets)} 个决定：{'；'.join(decision_snippets[:2])}。"
            "这些决定的后续执行情况需要追踪。"
        )

    if correction_snippets:
        insights.append(
            f"今天有 {len(correction_snippets)} 次纠正，这些都是宝贵的学习信号。"
        )
        tomorrow_items.append(
            "把今天的纠正整理到 .learnings/，形成长期记忆"
        )

    if error_keys:
        insights.append(
            f"今天出现了 {len(error_keys)} 个错误，需要检查是工具问题还是方法问题。"
        )

    # ── 兜底：有活动但没有特殊信号
    if entry_count >= 3 and not insights:
        # 所有条目都是 normal 类型，无特殊事件
        error_cnt = type_counts.get('error', 0)
        correction_cnt = type_counts.get('correction', 0)
        decision_cnt = type_counts.get('decision', 0)
        if error_cnt == 0 and correction_cnt == 0 and decision_cnt == 0:
            insights.append(
                f"今天共 {entry_count} 条记录，全部是正常对话内容，无错误、无纠正、无决策。"
                "系统运转正常。继续保持节奏，有情况时自然会产生洞察。"
            )
        elif important_keywords:
            top_kw = important_keywords[0][0]
            insights.append(
                f"今天围绕「{top_kw}」有 {entry_count} 条记录，内容平淡无特殊事件。"
                "继续保持观察。"
            )
        else:
            insights.append(
                f"今天共 {entry_count} 条记录，类型分布：{'、'.join([k+'×'+str(v) for k,v in type_counts.items()])}。"
                "内容无法细分析，但系统运转正常。"
            )

    # ── 明日重点（如果没有从上面推出，就用通用建议）
    if not tomorrow_items:
        if insights:
            tomorrow_items.append("选择一个今天聊到的具体话题，深入聊下去")
        tomorrow_items.append("继续日常节奏，保持观察和记录")

    # ── Topic 文件候选
    if important_keywords and entry_count >= 5:
        top_topic = important_keywords[0][0]
        topic_candidates.append({
            'filename': "topic-" + re.sub(r'[^\u4e00-\u9fffa-z0-9]', '-', top_topic[:20]),
            'title': f"主题：{top_topic}",
            'desc': f"今天高频讨论的主题，涉及 {entry_count} 条记录",
            'body': f"## {top_topic}\n\n今天围绕「{top_topic}」有 {entry_count} 条相关记录。"
        })

    # 组装输出
    lines = []

    if insights:
        lines.append("## 我学到了")
        for ins in insights[:5]:
            lines.append(f"- {ins}")
        lines.append("")

    if tomorrow_items:
        lines.append("## 明日重点")
        for t in tomorrow_items[:3]:
            lines.append(f"- {t}")
        lines.append("")

    if topic_candidates:
        lines.append("## Topic 文件")
        for t in topic_candidates[:2]:
            lines.append(f"filename: {t['filename']}")
            lines.append(f"title: {t['title']}")
            lines.append(f"desc: {t['desc']}")
            lines.append(f"body: {t['body']}")
            lines.append("")

    return "\n".join(lines) if lines else None


def parse_distillation_output(output):
    """解析 Distillation Agent 输出，支持 Markdown ## 头和纯文本两种格式"""
    if not output:
        return None
    insights = []
    tomorrow = []
    topics = []
    health_note = ''

    current_section = None
    for line in output.split('\n'):
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # Section 标记检测（支持 Markdown ## 头 + 纯文本）
        if '学到了' in line_stripped or '洞察' in line_stripped:
            current_section = 'insights'
            continue
        if '明日' in line_stripped or '计划' in line_stripped:
            current_section = 'tomorrow'
            continue
        if 'Topic' in line_stripped or 'topic' in line_stripped.lower():
            current_section = 'topics'
            continue

        # 跳过空 Markdown 行
        if line_stripped.startswith('#'):
            continue

        # topics 格式
        if current_section == 'topics':
            if line.startswith('filename:'):
                topics.append({'filename': line.split(':', 1)[1].strip(), 'title': '', 'desc': '', 'body': ''})
            elif line.startswith('title:') and topics:
                topics[-1]['title'] = line.split(':', 1)[1].strip()
            elif line.startswith('desc:') and topics:
                topics[-1]['desc'] = line.split(':', 1)[1].strip()
            elif line.startswith('body:') and topics:
                topics[-1]['body'] = line.split(':', 1)[1].strip()
        # insights 收集
        elif current_section == 'insights' and line_stripped.startswith('-'):
            insights.append(line_stripped.lstrip('- '))
        # tomorrow 收集
        elif current_section == 'tomorrow' and (line_stripped.startswith('-') or line_stripped[0].isdigit()):
            tomorrow.append(line_stripped.lstrip('123456789. -'))

    return {
        'insights': insights[:5],
        'tomorrow': tomorrow[:3],
        'topics': topics[:3],
        'health_note': health_note.strip(),
    }

def write_topic_files(topics):
    """写入 topic 文件"""
    written = []
    for t in topics:
        try:
            fname = t['filename'] if t['filename'].endswith('.md') else t['filename'] + '.md'
            fpath = TOPICS_DIR / fname
            date_str = datetime.now().strftime('%Y-%m-%d')
            content = f"""---
title: {t['title']}
created: {date_str}
updated: {date_str}
---

{t.get('body', t.get('desc', ''))}

---
_由梦境蒸馏 v3.3 生成_
"""
            fpath.write_text(content, encoding='utf-8')
            written.append(fname)
        except Exception as e:
            print(f"  [警告] 写入 topic 失败 {t.get('filename')}: {e}")
    return written


def update_truth_from_insights(insights, tomorrow_items):
    """根据 Distillation Agent 的洞察更新真相文件"""
    updated = []
    date_str = datetime.now().strftime('%Y-%m-%d')

    if tomorrow_items:
        pending_path = TRUTH_DIR / 'pending.md'
        existing = pending_path.read_text(encoding='utf-8') if pending_path.exists() else ""
        lines = [f"## 明日待办 ({date_str})"]
        for item in tomorrow_items:
            lines.append(f"- [ ] {item}")
        pending_path.write_text(existing + "\n" + "\n".join(lines) + "\n", encoding='utf-8')
        updated.append('pending.md')

    if insights:
        state_path = TRUTH_DIR / 'user_state.md'
        lines = [f"## 近期洞察 ({date_str})"]
        for ins in insights[:3]:
            lines.append(f"- {ins}")
        state_path.write_text(f"# user_state.md\n\n_Last updated: {date_str}_\n\n" + "\n".join(lines) + "\n", encoding='utf-8')
        updated.append('user_state.md')

    return updated


# ─── 报告生成 ─────────────────────────────────────────────────

def generate_report_v33(date_str, tagged_count, health, auditor_result,
                        distillation_result, archive_cands, patterns,
                        truth_updated, snapshot_id, all_recall_count,
                        mflow_stats: dict = None,
                        bundle_results: list = None,
                        skill_extension_result: dict = None):  # v5.0 新增参数
    """v5.0: 新增技能扩展报告（技能评分、用进废退、技能开发、每日汇报）"""
    if bundle_results is None:
        bundle_results = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # 解析 distillation 输出
    dist = parse_distillation_output(distillation_result) if distillation_result else None
    insights = dist.get('insights', []) if dist else []
    tomorrow = dist.get('tomorrow', []) if dist else []
    topic_written = dist.get('topics', []) if dist else []
    health_note = dist.get('health_note', '') if dist else ''

    report = f"""# 🌙 梦境报告 v4.0 — {date_str}

> 触发时间：{now}
> M-FLOW Bundle Search + Distillation Agent

---

## 🧠 系统状态

| 项目 | 数值 |
|------|------|
| 原始日志条目 | {tagged_count} 条 |
| recall store 总数 | {all_recall_count} 条 |
| Auditor AI味 | {auditor_result['ai_flavor_count']} 处 |
| 蓝斑核健康 | {health['total']}/100 |

**真相文件更新：** {', '.join(truth_updated) if truth_updated else '无'}
**快照ID：** `{snapshot_id}`

"""

    # 健康评分
    coherence_low = health['coherence'] < 0.5
    freshness_low = health['freshness'] < 0.5
    gc = health.get('graph_connectivity', 0)
    report += f"""## 🫀 蓝斑核健康评分 (v4.0 M-FLOW)

| 维度 | 得分 | 状态 |
|------|------|------|
| 新鲜度 | {health['freshness']} | {"⚠️ 低" if freshness_low else "✅ 正常"} |
| 连贯性 | {health['coherence']} | {"⚠️ 低" if coherence_low else "✅ 正常"} |
| 覆盖度 | {health['coverage']} | ✅ |
| **图连通性** | {gc} | {"⚠️ 低" if gc < 0.5 else "✅ 正常"} |
| 效率 | {health['efficiency']} | ✅ |
| 可达性 | {health['reachability']} | ✅ |

"""

    # M-FLOW 图状态
    if mflow_stats:
        em = mflow_stats.get('entities', 0)
        fp = mflow_stats.get('facetpoints', 0)
        ep = mflow_stats.get('episodes', 0)
        ed = mflow_stats.get('edges', 0)
        report += f"""## 🧠 M-FLOW 知识图谱状态

| 层级 | 数量 |
|------|------|
| L4 Entity | {em} |
| L3 FacetPoint | {fp} |
| L1 Episode | {ep} |
| 语义边 | {ed} |

**倒锥结构**: 锥尖(L3)精准锚点 → 语义边传播 → 锥底(L1)Episode返回


**Bundle Search 结果**: {len(bundle_results)} 条相关Episode

"""


    if health_note:
        report += f"**健康解读：** {health_note}\n\n"
    elif coherence_low:
        report += "**⚠️ 连贯性偏低：** 很多记忆只被提到一次，没有被持续追踪。明天有意识地多聊同一个话题，别总是新开话题。\n\n"

    # 核心产出：真正的洞察
    if insights:
        report += "## 💡 我学到了\n\n"
        for ins in insights:
            report += f"- {ins}\n"
        report += "\n"
    else:
        report += "## 💡 我学到了\n\n_（Distillation Agent 未返回洞察，可能日志量不足）_\n\n"

    # 重复模式
    if patterns:
        report += f"## 🔁 重复模式（≥3次）：{len(patterns)} 个\n\n"
        for p in patterns[:5]:
            report += f"- **{p['error'][:60]}** — 重复 {p['occurrences']} 次\n"
        report += "\n"

    # 归档
    if archive_cands:
        report += f"## 🗄️ 归档候选：{len(archive_cands)} 条（90天+低权重）\n\n"
        for a in archive_cands[:3]:
            report += f"- `{a['key']}` | {a['age_days']}天前 | 评分 {a['score']:.3f}\n"
        report += "\n"

    # 明日重点
    if tomorrow:
        report += "## 🎯 明日重点\n\n"
        for t in tomorrow:
            report += f"- {t}\n"
        report += "\n"
    else:
        report += "## 🎯 明日重点\n\n_（无具体计划，保持日常节奏）_\n\n"

    # Topic 文件
    if topic_written:
        report += "## 📝 新写入的 Topic 文件\n\n"
        for t in topic_written:
            fname = t.get('filename', 'unknown')
            title = t.get('title', fname)
            desc = t.get('desc', '')
            report += f"- **{title}** (`{fname}`) — {desc}\n"
        report += "\n"

    # v5.0: 技能扩展报告
    if skill_extension_result:
        ext = skill_extension_result
        report += "## 🛠️ 技能用进废退报告 (v5.0)\n\n"
        
        # 技能评分排行
        skill_scores = ext.get('skill_scores', {})
        if skill_scores:
            report += "### 📈 技能活跃度 Top 10\n\n"
            sorted_skills = sorted(
                skill_scores.items(),
                key=lambda x: x[1].get('score', 0),
                reverse=True
            )[:10]
            for i, (name, data) in enumerate(sorted_skills, 1):
                tier = data.get('tier', '')
                score = data.get('score', 0)
                calls = data.get('calls', 0)
                report += f"{i}. {tier} **{name}** — {score}分 ({calls}次调用)\n"
            report += "\n"
        
        # 用进废退变化
        decay_report = ext.get('decay_report', {})
        if decay_report:
            changes = decay_report.get('changes', [])
            if changes:
                report += "### ⚡ 用进废退状态变化\n\n"
                for c in changes[:5]:
                    old = c.get('old_status', '')
                    new = c.get('new_status', '')
                    skill = c.get('skill', '')
                    report += f"- {skill}: {old} → {new}\n"
                report += "\n"
        
        # 技能开发
        skill_dev = ext.get('skill_development', {})
        created = skill_dev.get('created', [])
        if created:
            report += "### ✨ 新开发技能\n\n"
            for s in created:
                report += f"- **{s.get('name', '')}**: {s.get('description', '')}\n"
            report += "\n"
        
        # 每日汇报
        daily_report = ext.get('daily_report', '')
        if daily_report:
            report += "### 📊 完整每日汇报\n\n"
            report += f"_详见 `daily-report-{date_str}.md`_\n\n"
        
        report += "---\n\n"

    report += """---

*v5.0 — M-FLOW + 技能用进废退 + 全自动技能开发*
"""
    return report


# ─── v5.0 扩展模块整合 ─────────────────────────────────────────

def run_skill_extensions(date_str, raw_entries, tagged, all_recall, learnings, patterns):
    """
    v5.0: 执行技能扩展模块
    整合工作复盘、技能评分、用进废退、技能开发、汇报生成
    """
    result = {
        'work_analysis': {},
        'tomorrow_plan': {},
        'skill_scores': {},
        'skill_development': {},
        'decay_report': {},
        'learnings': [],
        'daily_report': '',
    }
    
    # 1. 工作复盘分析
    print("   [E1] 工作复盘分析...")
    analyzer = WorkAnalyzer(raw_entries)
    result['work_analysis'] = analyzer.analyze()
    print(f"       完成任务: {len(result['work_analysis'].get('completed_tasks', []))}项")
    print(f"       未完成任务: {len(result['work_analysis'].get('incomplete_tasks', []))}项")
    
    # 2. 技能评分
    print("   [E2] 技能评分（用进废退）...")
    scorer = SkillScorer()
    result['skill_scores'] = scorer.score_all_skills()
    print(f"       评分技能数: {len(result['skill_scores'])}个")
    
    # 3. 用进废退引擎
    print("   [E3] 用进废退引擎...")
    decay = DecayEngine()
    decay_changes = decay.process_all_skills_decay(result['skill_scores'])
    result['decay_report'] = decay.get_decay_report()
    if decay_changes:
        print(f"       状态变化: {len(decay_changes)}项")
    
    # 4. 技能注册表
    print("   [E4] 技能注册表更新...")
    registry = SkillRegistry()
    
    # 注册今日使用但未注册的技能
    for skill_name in result['skill_scores'].keys():
        if registry.get_skill(skill_name) is None:
            registry.add_skill(
                skill_name=skill_name,
                category='general',
                description=f'技能评分: {result["skill_scores"][skill_name].get("score", 0)}',
                auto_created=False
            )
    
    # 5. 明日计划生成
    print("   [E5] 明日计划生成...")
    planner = TomorrowPlanner(result['work_analysis'], result['skill_scores'])
    result['tomorrow_plan'] = planner.generate_plan()
    print(f"       继续任务: {len(result['tomorrow_plan'].get('continued_tasks', []))}项")
    print(f"       新任务: {len(result['tomorrow_plan'].get('new_tasks', []))}项")
    
    # 6. 技能缺口检测（含 SKILL.md 草稿生成）v2.0
    print("   [E6] 技能缺口检测（v2.0 + SKILL.md 草稿）...")
    gap_detector = GapDetector(result['work_analysis'], result['skill_scores'], registry.registry)

    # v2.0: 使用 detect_and_generate() 同时获取缺口 + 草稿
    gap_result = gap_detector.detect_and_generate()
    gaps = gap_result['gaps']
    skill_drafts = gap_result['drafts']
    outdated_skills = gap_result.get('outdated_skills', [])
    print(f"       检测到缺口: {len(gaps)}个")

    # 7. 技能学习器
    print("   [E7] 技能学习与生成...")
    learner = SkillLearner(result['skill_scores'], registry.registry)

    # 8. 技能开发（使用 v2.0 SKILL.md 草稿）v2.0
    skill_dev_result = {'created': [], 'improved': [], 'failed': [], 'reasoning': '', 'drafts': []}

    # v2.0: 先用 generate_skill_draft() 的草稿创建技能
    for draft_info in skill_drafts[:2]:  # 最多2个
        skill_name = draft_info.get('name', '')
        skill_draft = draft_info.get('draft', '')
        if not skill_name or not skill_draft:
            continue

        # 保存 SKILL.md 草稿到 SharedSkills
        SKILLS_OUTPUT = Path.home() / "SharedSkills"
        skill_path = SKILLS_OUTPUT / skill_name
        if skill_path.exists():
            print(f"       跳过（已存在）: {skill_name}")
            continue

        try:
            skill_path.mkdir(parents=True, exist_ok=True)
            (skill_path / "SKILL.md").write_text(skill_draft, encoding='utf-8')
            # 写入占位脚本
            (skill_path / "scripts").mkdir(exist_ok=True)
            (skill_path / "scripts" / "main.py").write_text(
                f"#! /usr/bin/env python3\n\"\"\"自动生成的 {skill_name} 技能\"\"\"\nprint(\"[{skill_name}] 技能占位脚本，待实现\")\n", encoding='utf-8'
            )
            skill_dev_result['created'].append({
                'name': skill_name,
                'description': draft_info.get('capability', ''),
                'quality_score': 0,
                'source': 'auto-generated-draft',
            })
            skill_dev_result['drafts'].append({
                'name': skill_name,
                'draft': skill_draft,
            })
            print(f"       ✅ 创建技能草稿: {skill_name}")
        except Exception as e:
            skill_dev_result['failed'].append({'name': skill_name, 'error': str(e)})
            print(f"       ❌ 创建失败: {skill_name} — {e}")

    result['skill_development'] = skill_dev_result
    if skill_dev_result.get('created'):
        print(f"       新开发技能（含SKILL.md）: {len(skill_dev_result['created'])}个")
    else:
        print(f"       无需开发新技能")
    
    # 9. 生成每日汇报
    print("   [E8] 生成每日汇报...")
    reporter = DailyReporter(date_str)
    
    # 从 distillaton output 提取 learnings
    dist_parsed = parse_distillation_output(None)  # 复用已有的解析
    dist_insights = []
    if dist_parsed:
        dist_insights = dist_parsed.get('insights', [])
    
    result['learnings'] = dist_insights
    
    result['daily_report'] = reporter.generate_evening_report(
        work_analysis=result['work_analysis'],
        tomorrow_plan=result['tomorrow_plan'],
        skill_scores=result['skill_scores'],
        skill_development=result['skill_development'],
        decay_report=result['decay_report'],
        learnings=result['learnings'],
        personal_thoughts='',  # 个人感想由用户提供
    )
    
    # 保存每日汇报
    report_file = DREAMS_DIR / f'daily-report-{date_str}.md'
    report_file.write_text(result['daily_report'], encoding='utf-8')
    print(f"       汇报已保存: {report_file.name}")
    
    return result


def update_index_json(health, total_entries):
    try:
        data = json.loads(INDEX_FILE.read_text(encoding='utf-8')) if INDEX_FILE.exists() else \
               {'version': '3.0', 'entries': [], 'stats': {}}
        data['stats']['healthScore'] = health['total']
        data['stats']['healthMetrics'] = health
        data['stats']['totalEntries'] = total_entries
        data['stats']['lastDream'] = datetime.now().isoformat()
        INDEX_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception as e:
        print(f"  [警告] index.json 更新失败: {e}")


# ─── 主流程 ─────────────────────────────────────────────────

def run_dream(date_str=None):
    print("🌙 Dream v4.0 — M-FLOW Bundle Search + Distillation Agent")

    DREAMS_DIR.mkdir(exist_ok=True)
    ensure_truth_dirs()

    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # [0] 快照
    print("\n[0/8] 创建状态快照...")
    snapshot_id, backed_up = create_snapshot()
    print(f"   ✅ {snapshot_id} | 已备份: {', '.join(backed_up) if backed_up else '无'}")

    # [0.5] M-FLOW 图构建（v4.0，含Recall Store富化）
    print("\n[0.5/9] M-FLOW 图构建...")
    mflow_ok = mflow_build_graph(enrich_recall=True, enrich_errors=True)
    mflow_stats = mflow_graph_status() if mflow_ok else {}
    if mflow_ok:
        print(f"   ✅ 图: {mflow_stats.get('entities',0)} ent / "
              f"{mflow_stats.get('facetpoints',0)} fp / "
              f"{mflow_stats.get('episodes',0)} ep / "
              f"{mflow_stats.get('edges',0)} edges")
    else:
        print("   ⚠️  图构建跳过（脚本未找到或失败）")

    # [1] 加载数据
    print("\n[1/9] 加载数据源...")
    all_recall = load_recall()
    index_data = load_index()
    learnings = load_learnings()
    raw_entries = load_hippocampus_log(date_str)  # 原始条目（给 Distillation Agent）
    print(f"   recall: {len(all_recall)} 条 | 原始日志: {len(raw_entries)} 条 | learnings: {len(learnings)} 个")

    # [2] 过滤
    print("\n[2/9] 丘脑过滤...")
    filtered = thalamus_filter(all_recall, date_str)
    tagged = {}
    for k, v in filtered.items():
        score = compute_deep_score(v)
        v['_brain_score'] = score
        # 只检查原始日志条目；recall snippet是AI响应，error词频≠真实错误数
        is_raw = not v.get('snippet','').startswith(('User:', 'assistant '))
        v['_amygdala_tag'] = 'error' if (is_raw and any(e in v.get('snippet','').lower() for e in ['error','fail'])) else 'normal'
        tagged[k] = v

    # [3] 评分
    tagged_count = len(tagged)
    auditor_result = auditor_check(tagged)
    patterns = analyst_scan(tagged, learnings)
    print(f"   过滤后条目: {tagged_count} | Auditor: {'✅' if auditor_result['passed'] else '❌'} | 模式: {len(patterns)} 个")

    # [4] Distillation Agent（核心步骤）
    health_metrics = compute_health_metrics(tagged, all_recall, mflow_stats)
    
    # [4.5] Long-Term Memory 查询 — 注入旧记忆到蒸馏上下文
    rag_results = []
    if tagged:
        # 从高权重条目提取关键词
        keywords = []
        for v in list(tagged.values())[:20]:
            snippet = v.get('snippet', '')[:100]
            if snippet:
                keywords.append(snippet)
        query_text = ' '.join(keywords[:5])
        rag_results = query_longterm_rag(query_text, k=5)
        if rag_results:
            rag_text = "\n".join([
                f"[LTM {i+1}] {e.get('snippet','')[:100]}"
                for i, e in enumerate(rag_results)
            ])
            learnings['LEARNINGS.md'] = (learnings.get('LEARNINGS.md') or '') + f"\n\n## Long-Term Memory (RAG)\n{rag_text}"
            print(f"   [RAG] Injected {len(rag_results)} long-term memories into distillation")
    
    
    print("\n[4/9] Distillation Agent — 推理中...")
    distillation_output = run_distillation_agent(
        date_str, raw_entries, learnings, health_metrics, patterns, tagged
    )
    if distillation_output:
        lines = distillation_output.count('\n')
        print(f"   ✅ 产出洞察 {lines} 行")
    else:
        print("   ⚠️  无洞察产出")

    # [4.6] Long-Term Memory 晋升 — 蒸馏完成后，晋升老条目到 RAG
    promoted_count = promote_to_longterm_rag(all_recall, max_promote=20)
    if promoted_count > 0:
        print(f"   [RAG] Promoted {promoted_count} old entries to long-term memory")

    # v4.0: Bundle Search — 用 distillation insights 做查询
    # Step 1: learnings error tracking
    try:
        pending_errs = load_learnings_ERR()
        if pending_errs:
            rules_cnt = learnings_update_tools(pending_errs)
            if rules_cnt > 0:
                msg = str(rules_cnt) + " fix rules appended to TOOLS.md"
                print("   [*] " + msg)
    except NameError:
        pending_errs = []
    bundle_results = []
    dist_parsed = parse_distillation_output(distillation_output) if distillation_output else None
    if dist_parsed and mflow_ok:
        insights_text = " ".join(dist_parsed.get("insights", []))[:50]
        search_queries = [
            f"{date_str} {insights_text}",
            "correction error decision user feedback",
        ]
        for q in search_queries[:1]:
            results = mflow_bundle_search(q, top_k=3)
            if results:
                bundle_results.extend(results)
                print(f"   🔍 BundleSearch '{q[:40]}...': {len(results)} 个Episode")

    # [5] 写 topic 文件
    print("\n[5/9] 写入 topic 文件...")
    dist = parse_distillation_output(distillation_output) if distillation_output else None
    topic_written = []
    if dist and dist.get('topics'):
        topic_written = write_topic_files(dist['topics'])
        print(f"   ✅ 写入: {', '.join(topic_written) if topic_written else '无'}")
    else:
        print("   ⏭️ 无新 topic")

    # [6] 更新真相文件
    print("\n[6/9] 更新真相文件...")
    truth_updated = []
    if distillation_output:
        d = parse_distillation_output(distillation_output)
        truth_updated = update_truth_from_insights(
            d.get('insights', []) if d else [],
            d.get('tomorrow', []) if d else []
        )
        for fname in truth_updated:
            print(f"   ✅ {fname}")
    if not truth_updated:
        print("   ⏭️ 无更新")

    # [7] M-FLOW 图增量更新（v4.0新增）
    print("\n[7/9] M-FLOW 图增量更新...")
    if mflow_ok:
        up_ok = mflow_update_graph()
        print(f"   {'✅ 图更新完成' if up_ok else '⚠️  图更新失败'}")
    else:
        print("   ⏭️  图构建未成功，跳过")

    # [8] 归档
    print("\n[8/9] 归档检查...")
    archive_cands = archive_candidates(tagged, index_data)
    print(f"   候选: {len(archive_cands)} 条" + (f"（已归档 {len([a for a in archive_cands if a['age_days'] > 180])} 条）" if archive_cands else ""))

    # [E] v5.0: 扩展模块 — 技能用进废退 + 工作复盘 + 技能开发 + 汇报生成
    skill_extension_result = {}
    if EXTENSIONS_AVAILABLE:
        print("\n[E/9] v5.0 扩展模块执行中...")
        skill_extension_result = run_skill_extensions(
            date_str, raw_entries, tagged, all_recall, learnings, patterns
        )
        print(f"   ✅ 扩展模块执行完成")
    else:
        print("\n[E/9] 扩展模块未安装，跳过")

    # [9] 健康评分 + 生成报告
    print("\n[9/9] 健康评分 + 生成报告...")
    print(f"   综合: {health_metrics['total']}/100")
    update_index_json(health_metrics, len(tagged))

    report = generate_report_v33(
        date_str, tagged_count, health_metrics, auditor_result,
        distillation_output, archive_cands, patterns,
        truth_updated, snapshot_id, len(all_recall),
        mflow_stats=mflow_stats,
        bundle_results=bundle_results,
        skill_extension_result=skill_extension_result  # v5.0 新增
    )

    report_file = DREAMS_DIR / f'{date_str}.md'
    report_file.write_text(report, encoding='utf-8')
    print(f"\n✅ 报告已保存: {report_file}")

    # ── [9.5] 写入 DREAMS.md（原生 Dreaming UI 集成）────────────
    _dreams_path = WORKSPACE / 'DREAMS.md'
    _marker_start = '<!-- openclaw:dreaming:diary:start -->'
    _marker_end = '<!-- openclaw:dreaming:diary:end -->'

    _dist = parse_distillation_output(distillation_output) if distillation_output else {}
    _insights = _dist.get('insights', []) or []
    _tomorrow = _dist.get('tomorrow', []) or []
    gc = health_metrics.get('graph_connectivity', 0)

    _month_map = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
    _parts = date_str.split('-')
    _month_name = _month_map.get(_parts[1], _parts[1])
    _entry_lines = []
    _entry_lines.append(f"*{_month_name} {_parts[2]} GMT+8*")
    for _ins in _insights[:3]:
        _entry_lines.append(_ins)
    if _tomorrow:
        _entry_lines.append(f"\u2192 明日: {_tomorrow[0]}")
    if gc:
        _entry_lines.append(f"\u2192 图连通性: {gc:.2f}")

    _entry_text = '\n'.join(_entry_lines)
    _new_entry = f"\n{_marker_start}\n\n{_entry_text}\n\n{_marker_end}\n"

    if _dreams_path.exists():
        _existing = _dreams_path.read_text(encoding='utf-8', errors='replace')
    else:
        _existing = "# Dream Diary\n\n"

    _date_pat = re.compile(rf'\*April {re.escape(date_str[5:])} GMT\+8\*')
    if _date_pat.search(_existing):
        _pat = re.compile(
            rf'{re.escape(_marker_start)}.*?{re.escape(_marker_end)}',
            re.DOTALL
        )
        _existing = _pat.sub('', _existing).strip()

    _dreams_path.write_text(_existing + '\n' + _new_entry, encoding='utf-8')
    print(f"   ✅ 同步写入 DREAMS.md")

    # 追加到 dream-log.md
    log_file = MEMORY_DIR / 'dream-log.md'
    existing = log_file.read_text(encoding='utf-8') if log_file.exists() else ""
    log_file.write_text(existing + "\n\n---\n\n" + report, encoding='utf-8')

    return report


def main():
    parser = argparse.ArgumentParser(description='Dream v4.0 — M-FLOW + Distillation Agent')
    parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)', default=None)
    parser.add_argument('--snapshots', action='store_true', help='列出快照')
    args = parser.parse_args()

    if args.snapshots:
        for s in list_snapshots():
            print(f"  {s}")
        return

    try:
        report = run_dream(args.date)
        print("\n" + "=" * 60)
        print(report[-3000:])  # 只打印报告末尾，避免太长
    except Exception as e:
        print(f"❌ 梦境蒸馏失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

def load_learnings_ERR():
    """Load pending entries from .learnings/ERRORS.md"""
    err_file = LEARNINGS_DIR / "ERRORS.md"
    if not err_file.exists():
        return []
    content = err_file.read_text(encoding='utf-8', errors='replace')
    entries = []
    current = {}
    for line in content.split('\n'):
        if line.startswith('## [ERR-'):
            if current:
                entries.append(current)
            parts = line.strip().split('] ', 1)
            if len(parts) == 2:
                current = {'id': parts[0].lstrip('## ['), 'title': parts[1],
                          'status': 'unknown', 'summary': ''}
        elif '**Status**:' in line:
            current['status'] = line.split('**Status**:', 1)[1].strip()
        elif '**Summary**' in line:
            txt = line.split('**Summary**', 1)[1].lstrip(' *').strip()
            current['summary'] = txt
    if current:
        entries.append(current)
    return [e for e in entries if e.get('status', '').lower() == 'pending']


def learnings_update_tools(pending_errors):
    """Generate fix rules for pending errors and append to TOOLS.md"""
    if not pending_errors:
        return 0
    import re
    tools_md = WORKSPACE / "TOOLS.md"
    content = tools_md.read_text(encoding='utf-8', errors='replace') if tools_md.exists() else ""
    content = content.rstrip()
    rules = []
    for err in pending_errors:
        err_id = err.get('id', '')
        summary = (err.get('summary') or '').strip()
        if not summary:
            summary = err.get('title', '')
        summary_text = re.sub(r'[#*`]', '', summary)[:200]
        upper = summary_text.upper()
        if 'SIGKILL' in upper or 'TIMEOUT' in upper or 'TIMEOUTEXPIRED' in upper:
            rule_text = (
                "### " + err_id + " -- SIGKILL / Timeout\n\n"
                "**Problem**: " + summary_text + "\n\n"
                "**Prevention**:\n"
                "- Add --timeout to long commands (30-60s max)\n"
                "- Use yieldMs/background=true for long tasks\n"
                "- Add timeout= to subprocess.run() calls\n"
                "- SIGKILL usually means OOM or process timeout"
            )
        elif 'EXIT' in upper or 'EXCEPTION' in upper or 'ERROR' in upper:
            rule_text = (
                "### " + err_id + " -- Exit / Exception\n\n"
                "**Problem**: " + summary_text + "\n\n"
                "**Prevention**:\n"
                "- Check exit code is 0\n"
                "- Confirm paths and args before dangerous ops\n"
                "- Add try/except around subprocess calls"
            )
        else:
            rule_text = (
                "### " + err_id + "\n\n"
                "**Problem**: " + summary_text + "\n\n"
                "**Prevention**: TBD"
            )
        rules.append(rule_text)
    rules_text = '\n\n'.join(rules)
    pit_header = '\n## Tool Pitfalls\n'
    if '## Tool Pitfalls' in content:
        pit_idx = content.find('## Tool Pitfalls')
        next_h2 = content.find('\n## ', pit_idx + 10)
        if next_h2 == -1:
            next_h2 = len(content)
        content = content[:next_h2].rstrip() + '\n\n' + rules_text + '\n' + content[next_h2:]
    else:
        content = content + pit_header + '\n\n' + rules_text + '\n'
    tools_md.write_text(content, encoding='utf-8')
    return len(rules)



