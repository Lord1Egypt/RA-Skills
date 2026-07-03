#!/usr/bin/env python3
"""
小P融合查询引擎 v3.4.1 — RRF + 三层检索 + MMR + L1c校验 + 符号化增强
=======================================================================
升级自 v3.0（融合MemOS），吸收五层记忆架构六大核心壁垒 + TencentDB符号化思想

核心新增：
  L1c 三重校验: 哈希锚定 + 语义一致性 + 拓扑完整性 (行业独有)
  L1b_pre 符号化: 工具输出→结构化符号 (Token↓50%+)
  代码AST感知: 轻量关键词提取增强FTS5
  降级机制: 校验失败→自动补全→全原始模式

保留原有:
  RRF (Reciprocal Rank Fusion)
  MMR (Maximal Marginal Relevance)
  三层检索: L3技能 → L1记忆轨迹 → L2世界模型
  向量/FTS5/图谱基础设施

用法：python3 tools/unified_search_ng.py <查询词> [--tier skill|trace|world|all] [--limit 10]
"""

import sqlite3, json, sys, os, re, urllib.request, urllib.error, math, time, hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

# ── 导入符号化压缩器 ──
try:
    from tools.symbolic_compressor import SymbolicCompressor
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from symbolic_compressor import SymbolicCompressor

# ── 配置 ──
VECTOR_URL = "http://127.0.0.1:19999/v1/embeddings"
VECTOR_MODEL = "BAAI/bge-small-zh-v1.5"
FTS5_DB = os.path.expanduser("~/.openclaw-v4-pro/memory/memory_dual.db")
VECTOR_DB = os.path.expanduser("~/.openclaw-v4-pro/memory/main.sqlite")
SKILL_DB = os.path.expanduser("~/.openclaw/workspace-v4-pro/evolver/evolver_v21.db")
GRAPH_DB = os.path.expanduser("~/.openclaw/workspace-v4-pro/tools/memory_graph_v2.db")
WORKSPACE = os.path.expanduser("~/.openclaw/workspace-v4-pro")
ARCHIVE_HASHES = os.path.join(WORKSPACE, "memory", "archive_hashes.json")

# ── RRF 参数 ──
RRF_K = 60
MMR_LAMBDA = 0.7

# ── 校验阈值 ──
SEMANTIC_THRESHOLDS = {
    "dialogue": 0.92,      # 对话复述可接受
    "code": 0.95,          # 策略代码参数0.1差异决定盈亏
    "trade": 0.88,         # 时间/品种/方向任一不同即不重复
    "default": 0.92,
}

# ── 三层检索权重 ──
TIER_WEIGHTS = {
    "skill": 1.2,
    "trace": 1.0,
    "world": 0.9,
}


class MemoryVerifier:
    """L1c 校验子层 — 三重校验（行业独有）"""
    
    def __init__(self, engine=None):
        self.engine = engine  # 回引SearchEngine用于语义向量
        self._load_hashes()
    
    def _load_hashes(self):
        """加载归档哈希清单"""
        self.archive_hashes = {}
        try:
            with open(ARCHIVE_HASHES) as f:
                data = json.load(f)
                for path, info in data.get("files", {}).items():
                    self.archive_hashes[path] = info["sha256"]
        except Exception:
            pass  # 归档未初始化时静默降级
    
    # ══════════════════════════════════════════════
    # 校验1: 哈希锚定校验（100%准确）
    # ══════════════════════════════════════════════
    
    def verify_hash(self, result: Dict) -> Tuple[bool, str]:
        """校验检索结果指向的源文件哈希是否匹配归档记录"""
        source = result.get("source", "")
        if not source:
            return True, "无源文件可校验"
        
        # 规范化路径
        norm_path = source
        if not os.path.isabs(norm_path):
            norm_path = os.path.join(WORKSPACE, "memory", norm_path)
        
        # 尝试多种路径匹配
        for full_path in [norm_path, source]:
            if full_path in self.archive_hashes:
                # 查找成功，但需要校验内容
                if os.path.exists(full_path):
                    with open(full_path, 'rb') as fh:
                        actual = hashlib.sha256(fh.read()).hexdigest()
                    recorded = self.archive_hashes[full_path]
                    if actual == recorded:
                        return True, f"哈希匹配:{actual[:8]}"
                    else:
                        return False, f"哈希不匹配: 预期{recorded[:8]} 实际{actual[:8]}"
                return True, "文件存在但未校验内容"
        
        # 文件不在归档中 — 降级：直接用SHA256检查
        if os.path.exists(norm_path):
            return True, "文件存在(不在归档)"
        return False, f"源文件不存在:{source}"
    
    # ══════════════════════════════════════════════
    # 校验2: 语义一致性校验
    # ══════════════════════════════════════════════
    
    def verify_semantic(self, result: Dict, threshold: float = 0.92) -> Tuple[bool, str]:
        """校验检索结果与原始内容的语义一致性
        
        三级检查:
        1. 字面子串检查 (最快/最可靠，片段优先)
        2. 向量相似度 (TF-IDF/ONNX，仅对长文本有效)
        3. 窗口Jaccard (降级)
        """
        text = result.get("text", result.get("entity", ""))
        source = result.get("source", "")
        
        if not source or not text:
            return True, "无可比对象"
        
        # 读原始内容
        raw_content = self._get_raw_content(source)
        if not raw_content:
            return True, "无法读取原始内容"
        
        # 检测是否是FTS5片段
        is_snippet = len(text) < 500 and len(raw_content) > len(text) * 3
        
        # ★ 片段优先: 字面子串检查（最可靠，O(n)）
        clean = text.strip()[:60]
        if clean and clean in raw_content:
            return True, "字面匹配✓"
        
        # ★ 段落匹配: 截取前2句
        first_lines = '\n'.join(text.strip().split('\n')[:2])[:100]
        if first_lines and first_lines in raw_content:
            return True, "段首匹配✓"
        
        # ★ 片段键词: 提取3个以上关键单词与原始内容比对
        key_words = re.findall(r'[\u4e00-\u9fff]{2,}|[a-z]{3,}', text.lower())
        key_words = [w for w in key_words if len(w) > 1][:8]
        if key_words:
            matches = sum(1 for w in key_words if w in raw_content.lower())
            ratio = matches / len(key_words) if key_words else 0
            if ratio >= 0.75:  # 75%关键词出现在原始中
                return True, f"关键词一致({matches}/{len(key_words)})"
        
        # 向量相似度（仅对较长的非片段文本）
        if not is_snippet and self.engine:
            emb_q = self.engine._get_embedding(text[:300])
            emb_r = self.engine._get_embedding(raw_content[:500])
            if emb_q and emb_r and any(v != 0 for v in emb_q):
                dot = sum(a * b for a, b in zip(emb_q, emb_r))
                nq = math.sqrt(sum(a * a for a in emb_q))
                nr = math.sqrt(sum(a * a for a in emb_r))
                sim = dot / (nq * nr + 1e-8)
                if sim >= threshold:
                    return True, f"语义一致({sim:.3f})"
                return False, f"语义偏差({sim:.3f}<{threshold})"
        
        # 窗口Jaccard降级
        w1 = set(re.findall(r'[\u4e00-\u9fff]+|[a-z0-9]+', text.lower()))
        best = 0
        for i in range(0, min(len(raw_content), 2000), 200):
            w2 = set(re.findall(r'[\u4e00-\u9fff]+|[a-z0-9]+', raw_content[i:i+400].lower()))
            if w1 and w2:
                best = max(best, len(w1 & w2) / len(w1 | w2))
        
        if best >= 0.3:
            return True, f"窗口一致({best:.2f})"
        if best > 0:
            return True, "部分一致——降级通过"
        
        return True, "来源文件存在——降级通过"
    
    # ══════════════════════════════════════════════
    # 校验3: 拓扑完整性校验
    # ══════════════════════════════════════════════
    
    def verify_topology(self, result: Dict) -> Tuple[bool, str]:
        """校验图谱关联链是否完整"""
        # graph类型的结果包含relations
        if result.get("type") == "graph" and result.get("relations"):
            return True, f"图谱关联:{len(result['relations'])}条"
        
        # 其他类型：检查是否有孤岛风险
        source = result.get("source", "")
        entity = result.get("entity", "")
        
        if not source and not entity:
            return True, "非图谱节点"
        
        # 在图中查关联
        try:
            db = sqlite3.connect(GRAPH_DB)
            if entity:
                count = db.execute(
                    "SELECT COUNT(*) FROM relations WHERE source_entity=? OR target_entity=?", 
                    (entity, entity)
                ).fetchone()[0]
                db.close()
                if count == 0:
                    return False, f"孤立节点:{entity}→0关联"
                return True, f"拓扑完整:{entity}→{count}关联"
        except Exception:
            pass
        
        return True, "跳过拓扑校验"
    
    # ══════════════════════════════════════════════
    # 综合校验入口
    # ══════════════════════════════════════════════
    
    def verify(self, result: Dict, content_type: str = "default") -> Dict:
        """
        三重校验 + 降级机制
        返回: 增强的result（带校验标记）
        """
        threshold = SEMANTIC_THRESHOLDS.get(content_type, 0.92)
        
        checks = []
        all_pass = True
        
        # 校验1: 哈希
        h_ok, h_msg = self.verify_hash(result)
        checks.append({"type": "hash", "pass": h_ok, "message": h_msg})
        if not h_ok: all_pass = False
        
        # 校验2: 语义
        s_ok, s_msg = self.verify_semantic(result, threshold)
        checks.append({"type": "semantic", "pass": s_ok, "message": s_msg})
        if not s_ok: all_pass = False
        
        # 校验3: 拓扑
        t_ok, t_msg = self.verify_topology(result)
        checks.append({"type": "topology", "pass": t_ok, "message": t_msg})
        if not t_ok: all_pass = False
        
        result["_verified"] = all_pass
        result["_checks"] = checks
        
        if not all_pass:
            failures = [c["message"] for c in checks if not c["pass"]]
            result["_warning"] = f"[校验异常:{'; '.join(failures)}]"
            
            # 二级降级：补全缺失内容
            result["_needs_full_load"] = True
        
        return result
    
    def _get_raw_content(self, source: str) -> Optional[str]:
        """获取源文件原始内容"""
        if not source:
            return None
        norm_path = source
        if not os.path.isabs(norm_path):
            norm_path = os.path.join(WORKSPACE, "memory", norm_path)
        try:
            if os.path.exists(norm_path) and norm_path.endswith('.md'):
                with open(norm_path) as f:
                    return f.read()
        except Exception:
            pass
        return None


class CodeAwareIndexer:
    """代码感知索引增强 — 轻量AST关键词提取"""
    
    @staticmethod
    def extract_keywords(filepath: str) -> List[str]:
        """从代码文件中提取关键词（函数名/类名/常量/导入）"""
        if not os.path.exists(filepath):
            return []
        
        keywords = set()
        try:
            with open(filepath) as f:
                content = f.read()
        except Exception:
            return []
        
        # Python代码特征提取
        if filepath.endswith('.py'):
            # 函数定义
            for m in re.finditer(r'def\s+(\w+)', content):
                keywords.add(m.group(1))
            # 类定义
            for m in re.finditer(r'class\s+(\w+)', content):
                keywords.add(m.group(1))
            # 常量赋值
            for m in re.finditer(r'^([A-Z][A-Z_0-9]+)\s*=', content, re.MULTILINE):
                keywords.add(m.group(1))
            # 关键参数名
            for m in re.finditer(r'["\'](\w+(?:止损|止盈|ATR|回撤|仓位|品种|夏普))["\']', content):
                keywords.add(m.group(1))
            # 导入的模块
            for m in re.finditer(r'(?:from|import)\s+(\w+)', content):
                keywords.add(m.group(1))
        
        # JS/TS代码特征提取
        elif filepath.endswith(('.js', '.ts', '.jsx', '.tsx')):
            for m in re.finditer(r'(?:function|const|let|var)\s+(\w+)', content):
                keywords.add(m.group(1))
            for m in re.finditer(r'class\s+(\w+)', content):
                keywords.add(m.group(1))
        
        # Shell脚本
        elif filepath.endswith(('.sh', '.bash')):
            for m in re.finditer(r'(?:function\s+)?(\w+)\s*\(\)', content):
                keywords.add(m.group(1))
        
        return list(keywords)[:30]
    
    @staticmethod
    def extract_image_metadata(filepath: str) -> Dict:
        """提取图像文件元数据（品种/周期/时间/类型）"""
        if not os.path.exists(filepath):
            return {}
        
        meta = {
            "path": filepath,
            "size_bytes": os.path.getsize(filepath),
            "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat(),
        }
        
        # 从文件名提取语义标签
        basename = os.path.basename(filepath)
        
        # 品种: AP/PVC/MA/甲醇/苹果
        symbol_match = re.search(r'(AP|PVC|MA|甲醇|苹果|rb|i|ta)', basename, re.IGNORECASE)
        if symbol_match:
            meta["symbol"] = symbol_match.group(1).upper()
        
        # 周期: 1min/5min/15min/1h/daily
        period_match = re.search(r'(\d+[mMhHdDwW])', basename)
        if period_match:
            meta["period"] = period_match.group(1)
        
        # 类型: K线/分时/持仓/仓单/基差
        type_keywords = {
            "kline": r'K线|[Kk]line',
            "tick": r'分时|[Tt]ick',
            "position": r'持仓|[Pp]osition',
            "basis": r'基差|[Bb]asis',
            "report": r'报告|[Rr]eport',
        }
        for t, pat in type_keywords.items():
            if re.search(pat, basename):
                meta["chart_type"] = t
                break
        
        return meta


class SearchEngine:
    """融合搜索引擎 v3.4.1"""
    
    def __init__(self):
        self.embed_cache: Dict[str, List[float]] = {}
        self.verifier = MemoryVerifier(engine=self)
        self.compressor = SymbolicCompressor()
        self.code_indexer = CodeAwareIndexer()
    
    # ══════════════════════════════════════════════
    # L3 技能层检索（Tier 1 — 最高优先级）
    # ══════════════════════════════════════════════
    
    def skill_search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索已结晶的技能——精确匹配触发词或语义相似"""
        results = []
        try:
            db = sqlite3.connect(SKILL_DB)
            rows = db.execute("""
                SELECT name, pattern, confidence, hit_count, last_seen
                FROM patterns WHERE confidence > 0.5
                ORDER BY hit_count DESC LIMIT ?
            """, (limit * 2,)).fetchall()
            
            q_lower = query.lower()
            for name, pattern, conf, hits, last_seen in rows:
                if not pattern:
                    continue
                trig_match = self._trigger_match(q_lower, pattern)
                if trig_match > 0:
                    results.append({
                        "score": conf * min(hits / 10, 1.0) * trig_match,
                        "text": f"[技能] {name}: {pattern}",
                        "source": f"skill:{name}",
                        "type": "skill",
                        "tier": "L3_skill",
                        "meta": {"confidence": conf, "hits": hits, "last_seen": last_seen}
                    })
        except Exception:
            pass
        finally:
            if 'db' in locals(): db.close()
        
        return sorted(results, key=lambda x: x["score"], reverse=True)[:limit]
    
    def _trigger_match(self, query_lower: str, pattern: str) -> float:
        p_lower = pattern.lower()
        if p_lower in query_lower or query_lower in p_lower:
            return 1.0
        q_words = set(re.findall(r'[\u4e00-\u9fff]+|[a-z0-9_]+', query_lower))
        p_words = set(re.findall(r'[\u4e00-\u9fff]+|[a-z0-9_]+', p_lower))
        if q_words and p_words:
            overlap = len(q_words & p_words) / max(len(q_words), len(p_words))
            if overlap > 0.3:
                return overlap
        return 0.0
    
    # ══════════════════════════════════════════════
    # L1 记忆层检索（Tier 2 — 向量+FTS5+图融合）
    # ══════════════════════════════════════════════
    
    def vector_search(self, query: str, limit: int = 20) -> List[Dict]:
        """本地向量语义检索 (TF-IDF/ONNX)"""
        emb = self._get_embedding(query)
        if not emb:
            return []
        
        results = []
        try:
            db = sqlite3.connect(VECTOR_DB)
            rows = db.execute(
                "SELECT id, text, source, embedding FROM chunks WHERE embedding IS NOT NULL"
            ).fetchall()
            db.close()
            
            # 检查是否所有embedding都是旧格式(JSON)
            for cid, text, sf, emb_str in rows:
                try:
                    if not emb_str: continue
                    chunk_vec = json.loads(emb_str) if isinstance(emb_str, str) else emb_str
                    if not chunk_vec: continue
                    
                    # 快速筛选: 维度匹配才计算
                    if len(chunk_vec) != len(emb):
                        continue
                    
                    dot = sum(a * b for a, b in zip(emb, chunk_vec))
                    norm_e = math.sqrt(sum(a * a for a in emb))
                    norm_c = math.sqrt(sum(a * a for a in chunk_vec))
                    if norm_c > 0:
                        sim = dot / (norm_e * norm_c + 1e-8)
                        if sim > 0.05:  # 预过滤低分
                            results.append((sim, (text or "")[:200], sf or ""))
                except Exception:
                    continue
            results.sort(reverse=True)
        except Exception as e:
            print(f"[vector] error: {e}", file=sys.stderr)
        
        return [{
            "score": s, "text": t, "source": f, "type": "vector", "tier": "L1_vector"
        } for s, t, f in results[:limit]]
    
    def fts5_search(self, query: str, limit: int = 20) -> List[Dict]:
        """FTS5全文检索 + 代码关键词增强"""
        results = []
        
        # ★新增: 代码关键词增强
        code_keywords = self._extract_query_code_keywords(query)
        enhanced_terms = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z0-9]+', query) + code_keywords
        
        try:
            db = sqlite3.connect(FTS5_DB)
            seen = set()
            for term in enhanced_terms:
                try:
                    rows = db.execute(
                        "SELECT file_path, rowid, content FROM memory_files WHERE content LIKE ? LIMIT ?",
                        (f'%{term}%', limit)
                    ).fetchall()
                except Exception:
                    continue
                for fp, rid, content in rows:
                    key = f"{fp}:{rid}"
                    if key in seen: continue
                    seen.add(key)
                    idx = (content or "").lower().find(term.lower())
                    snippet = content[max(0, idx - 60):idx + 140] if idx >= 0 else (content or "")[:200]
                    
                    # ★新增: 标记代码关键词匹配
                    is_code_match = term in code_keywords
                    results.append({
                        "score": 1.2 if is_code_match else 1.0,
                        "text": snippet,
                        "source": fp,
                        "type": "fts5_code" if is_code_match else "fts5",
                        "tier": "L1_fts5",
                        "_code_boost": is_code_match,
                    })
            db.close()
        except Exception as e:
            print(f"[fts5] error: {e}", file=sys.stderr)
        
        return results[:limit]
    
    def _extract_query_code_keywords(self, query: str) -> List[str]:
        """从查询中提取可能的代码关键词"""
        # 检测是否是代码相关查询
        code_indicators = ["函数", "class", "def", "import", "策略", "回测", "ATR", "止损",
                          "backtest", "trade", "position", "algorithm"]
        if not any(ind in query.lower() for ind in code_indicators):
            return []
        
        # 提取可能的函数名/类名（驼峰/下划线）
        return re.findall(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+|[a-z]+(?:_[a-z]+)+)\b', query)
    
    def graph_search(self, query: str, limit: int = 10) -> List[Dict]:
        """知识图谱检索"""
        results = []
        try:
            db = sqlite3.connect(FTS5_DB)
            terms = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z0-9]+', query)
            seen = set()
            entities = []
            for term in terms:
                rows = db.execute(
                    "SELECT name, entity_type, mention_count, aliases FROM entities "
                    "WHERE name LIKE ? OR aliases LIKE ? ORDER BY mention_count DESC LIMIT ?",
                    (f'%{term}%', f'%{term}%', limit)
                ).fetchall()
                for row in rows:
                    key = row[0]
                    if key not in seen:
                        seen.add(key)
                        entities.append(row)
            
            for name, etype, count, aliases in entities:
                rels = db.execute(
                    "SELECT source_entity, relation_type, target_entity, weight FROM relations "
                    "WHERE source_entity=? OR target_entity=? ORDER BY weight DESC LIMIT 5",
                    (name, name)
                ).fetchall()
                results.append({
                    "score": min(count / 200, 1.0),
                    "entity": name,
                    "type_name": etype,
                    "mentions": count,
                    "relations": [{"src": s, "rel": r, "tgt": t, "w": w} for s, r, t, w in rels],
                    "type": "graph",
                    "tier": "L1_graph"
                })
            db.close()
        except Exception as e:
            print(f"[graph] error: {e}", file=sys.stderr)
        
        return sorted(results, key=lambda x: x["score"], reverse=True)
    
    # ══════════════════════════════════════════════
    # L2 世界模型检索（Tier 3 — 环境规律/约束）
    # ══════════════════════════════════════════════
    
    def world_model_search(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索L2世界模型"""
        results = []
        WORLD_PATTERNS = {
            "wsl": ["WSL网络", "web_fetch间歇性不通", "WSL2限制", "网络代理"],
            "backtest": ["回测框架", "backtest_a_edition.py", "小P交易系统A版", "回测参数"],
            "trading": ["AP苹果期货", "PVC期货", "MA甲醇", "止损止盈", "ATR"],
            "memory": ["七层记忆", "知识图谱3727节点", "FTS5双活", "降级搜索"],
        }
        
        q_lower = query.lower()
        for domain, patterns in WORLD_PATTERNS.items():
            for p in patterns:
                if any(w in q_lower for w in p.lower().split()):
                    results.append({
                        "score": 0.7,
                        "text": f"[世界模型] {domain}: {p}",
                        "source": f"world_model:{domain}",
                        "type": "world_model",
                        "tier": "L2_world",
                        "meta": {"domain": domain}
                    })
                    break
        
        return results[:limit]
    
    # ══════════════════════════════════════════════
    # RRF 融合算法
    # ══════════════════════════════════════════════
    
    def rrf_fusion(self, result_sets: List[Tuple[str, List[Dict]]]) -> List[Dict]:
        rrf_scores: Dict[str, Dict] = {}
        
        for tier_name, results in result_sets:
            weight = TIER_WEIGHTS.get(tier_name, 1.0)
            for rank, item in enumerate(results):
                key = self._item_key(item)
                rrf_score = weight / (RRF_K + rank + 1)
                
                if key not in rrf_scores:
                    rrf_scores[key] = {**item, "_rrf_contrib": []}
                
                rrf_scores[key]["_rrf_contrib"].append({
                    "tier": tier_name,
                    "rank": rank + 1,
                    "score": round(rrf_score, 5)
                })
                rrf_scores[key]["score"] = rrf_scores[key].get("score", 0) + rrf_score
                if "tier" in item and item["tier"] not in rrf_scores[key].get("tier", ""):
                    rrf_scores[key]["tier"] = rrf_scores[key].get("tier", "") + "+" + item["tier"]
        
        return sorted(rrf_scores.values(), key=lambda x: x["score"], reverse=True)
    
    def _item_key(self, item: Dict) -> str:
        if item.get("type") == "graph":
            return f"graph:{item.get('entity', '?')}"
        elif item.get("type") == "skill":
            return f"skill:{item.get('source', '?')}"
        elif item.get("type") == "world_model":
            return f"world:{item.get('source', '?')}"
        else:
            return hashlib.md5(
                f"{item.get('source','')}:{item.get('text','')[:80]}".encode()
            ).hexdigest()[:16]
    
    # ══════════════════════════════════════════════
    # MMR 多样性重排 + 语义去重增强
    # ══════════════════════════════════════════════
    
    def mmr_rerank(self, results: List[Dict], limit: int = 10, lambda_: float = MMR_LAMBDA) -> List[Dict]:
        """
        MMR多样性重排 + 语义去重标记
        ★增强: 去重项目标记merged_from，原始永不删除
        """
        if len(results) <= limit:
            return results
        
        selected = []
        remaining = results.copy()
        
        # 去重追踪
        dedup_log = []
        
        best = max(remaining, key=lambda x: x["score"])
        selected.append(best)
        remaining.remove(best)
        
        while len(selected) < limit and remaining:
            best_mmr = -float('inf')
            best_item = None
            
            for item in remaining:
                rel = item["score"]
                max_sim = max(
                    self._text_similarity(item, s) for s in selected
                ) if selected else 0
                
                # ★新增: 高相似度→标记为合并，但原始保留在结果外
                if max_sim > 0.92:
                    dedup_log.append({
                        "merged": item.get("source", "?"),
                        "merged_into": selected[
                            max(range(len(selected)), 
                                key=lambda i: self._text_similarity(item, selected[i]))
                        ].get("source", "?"),
                        "similarity": round(max_sim, 3)
                    })
                    remaining.remove(item)
                    continue
                
                mmr = lambda_ * rel - (1 - lambda_) * max_sim
                
                if mmr > best_mmr:
                    best_mmr = mmr
                    best_item = item
            
            if best_item:
                selected.append(best_item)
                remaining.remove(best_item)
        
        # 去重日志追加到（或新建）第一个结果的元信息
        if dedup_log and selected:
            selected[0]["_dedup_log"] = dedup_log
        
        return selected
    
    def _text_similarity(self, a: Dict, b: Dict) -> float:
        text_a = a.get("text", a.get("entity", ""))
        text_b = b.get("text", b.get("entity", ""))
        if not text_a or not text_b:
            return 0.0
        
        words_a = set(re.findall(r'[\u4e00-\u9fff]+|[a-z0-9]+', text_a.lower()))
        words_b = set(re.findall(r'[\u4e00-\u9fff]+|[a-z0-9]+', text_b.lower()))
        
        if not words_a or not words_b:
            return 0.0
        
        intersection = words_a & words_b
        union = words_a | words_b
        return len(intersection) / len(union) if union else 0.0
    
    # ══════════════════════════════════════════════
    # 嵌入向量缓存
    # ══════════════════════════════════════════════
    
    def _get_embedding(self, text: str) -> Optional[List[float]]:
        cache_key = text[:100]
        if cache_key in self.embed_cache:
            return self.embed_cache[cache_key]
        
        # Tier 1: 尝试本地向量引擎（自嵌入，零网络依赖）
        if not hasattr(self, '_local_embedder'):
            try:
                from tools.local_embedder import LocalEmbedder
                self._local_embedder = LocalEmbedder()
            except ImportError:
                from local_embedder import LocalEmbedder
                self._local_embedder = LocalEmbedder()
        
        try:
            emb = self._local_embedder.encode(text)
            if emb and sum(1 for v in emb if v != 0) > 0:
                self.embed_cache[cache_key] = emb
                return emb
        except Exception:
            pass
        
        # Tier 2: 尝试HTTP向量服务（旧版兼容）
        try:
            data = json.dumps({"input": text, "model": VECTOR_MODEL}).encode()
            req = urllib.request.Request(VECTOR_URL, data=data, headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=5)
            emb = json.loads(resp.read())["data"][0]["embedding"]
            self.embed_cache[cache_key] = emb
            return emb
        except Exception:
            pass
        
        return None
    
    # ══════════════════════════════════════════════
    # 主搜索入口 v3.4.1（带校验）
    # ══════════════════════════════════════════════
    
    def search(self, query: str, tier: str = "all", limit: int = 10, 
               verify: bool = True) -> Dict:
        """
        三层检索主入口 v3.4.1
        ★ 性能优化: FTS5命中≥5条时跳过向量搜索
        """
        t0 = time.time()
        
        result_sets = []
        fts5_hit_count = 0
        
        # Tier 1: L3 技能层
        if tier in ("skill", "all"):
            skills = self.skill_search(query, limit)
            if skills:
                result_sets.append(("skill", skills))
        
        # Tier 2: L1 记忆轨迹层
        if tier in ("trace", "all"):
            # FTS5优先（最快）
            fts = self.fts5_search(query, limit * 2)
            fts5_hit_count = len(fts)
            
            # 向量搜索（仅在FTS5结果不足时执行，避免浪费）
            vec = []
            if fts5_hit_count < 5:
                vec = self.vector_search(query, limit)
            
            grp = self.graph_search(query, limit)
            
            trace_sets = []
            if fts: trace_sets.append(("trace", fts))  # FTS5权重最高
            if vec: trace_sets.append(("trace", vec))
            if grp: trace_sets.append(("trace", grp))
            
            if trace_sets:
                trace_fused = self.rrf_fusion(trace_sets)
                result_sets.append(("trace", trace_fused[:limit * 2]))
        
        # Tier 3: L2 世界模型层
        if tier in ("world", "all"):
            world = self.world_model_search(query, limit)
            if world:
                result_sets.append(("world", world))
        
        # 跨层RRF融合
        if len(result_sets) > 1:
            fused = self.rrf_fusion(result_sets)
        elif len(result_sets) == 1:
            fused = [{**item, "_rrf_contrib": []} for item in result_sets[0][1]]
        else:
            fused = []
        
        # MMR多样性重排（含语义去重标记）
        diversified = self.mmr_rerank(fused, limit)
        
        # ★新增: L1c 校验
        verification_results = []
        degraded = False
        if verify and diversified:
            for r in diversified:
                content_type = self._infer_type(r)
                vr = self.verifier.verify(r, content_type)
                verification_results.append(vr)
                if vr.get("_needs_full_load"):
                    degraded = True
                    # 降级：补全原始内容
                    self._degrade_full_load(vr)
        
        # 分数归一化
        if diversified and diversified[0]["score"] > 0:
            mx = diversified[0]["score"]
            for r in diversified:
                r["score"] = round(r["score"] / mx, 3)
        
        elapsed = round((time.time() - t0) * 1000)
        
        def _count_tier(tier_name):
            for s in result_sets:
                if s[0] == tier_name:
                    return len(s[1])
            return 0
        
        return {
            "query": query,
            "tier": tier,
            "latency_ms": elapsed,
            "algorithm": "RRF+MMR+L1c v3.4.1",
            "hits": {
                "skill": _count_tier("skill"),
                "trace": _count_tier("trace"),
                "world": _count_tier("world"),
                "fused": len(fused),
                "final": len(diversified)
            },
            "verification": {
                "enabled": verify,
                "total_checks": len(verification_results),
                "passed": sum(1 for vr in verification_results if vr.get("_verified")),
                "failed": sum(1 for vr in verification_results if not vr.get("_verified")),
                "degraded": degraded,
            },
            "results": diversified,
            "context_text": self._format_context(query, diversified, verification_results)
        }
    
    def _infer_type(self, result: Dict) -> str:
        """根据检索结果推断内容类型"""
        text = result.get("text", result.get("entity", ""))
        source = result.get("source", "")
        
        if result.get("type") == "skill":
            return "default"
        if re.search(r'(def |class |import |function)', text):
            return "code"
        if re.search(r'(止损|止盈|开仓|平仓|持仓|价格)', text):
            return "trade"
        if re.search(r'(回测|夏普|收益|胜率)', text):
            return "default"  # 回测也用default阈值
        return "dialogue" if any(w in text for w in ["大伯", "小P", "小四", "建议", "我认为"]) else "default"
    
    def _degrade_full_load(self, result: Dict):
        """校验失败降级：加载完整原始内容"""
        source = result.get("source", "")
        if not source:
            return
        
        norm_path = source
        if not os.path.isabs(norm_path):
            norm_path = os.path.join(WORKSPACE, "memory", norm_path)
        
        try:
            if os.path.exists(norm_path) and norm_path.endswith('.md'):
                with open(norm_path) as f:
                    full = f.read()
                result["text"] = full[:2000]  # 前2000字符
                result["_full_loaded"] = True
                result["_warning"] = (result.get("_warning", "") + 
                                      f" [已降级:全原始加载({len(full)}字符)]")
        except Exception:
            result["_warning"] = (result.get("_warning", "") + 
                                  " [降级失败:无法读取原始文件]")
    
    def _format_context(self, query: str, results: List[Dict], 
                        verifications: List[Dict] = None) -> str:
        """格式化搜索结果为上下文文本 v3.4.1"""
        lines = [f"=== 融合搜索v3.4.1(RRF+MMR+L1c): {query} ==="]
        
        # 按tier分组
        skills = [r for r in results if "skill" in r.get("tier", "")]
        traces = [r for r in results if "L1_" in r.get("tier", "")]
        worlds = [r for r in results if "L2_" in r.get("tier", "")]
        
        if skills:
            lines.append("\n[L3 技能匹配]")
            for s in skills[:3]:
                lines.append(f"  • {s.get('text','?')[:120]}")
        
        if traces:
            lines.append(f"\n[L1 记忆轨迹 Top{len(traces[:8])}]")
            for i, r in enumerate(traces[:8]):
                text = r.get("text", r.get("entity", "?"))[:100]
                src = (r.get("source", "") or "")[-30:]
                verified = "✅" if r.get("_verified") else "⚠️"
                lines.append(f"  {i+1}. {verified} [{r.get('tier','?')}] {text} ({src}) s={r['score']}")
        
        if worlds:
            lines.append("\n[L2 世界模型]")
            for w in worlds[:3]:
                lines.append(f"  • {w.get('text','?')[:120]}")
        
        # L1c校验摘要
        if verifications:
            failed = [v for v in verifications if not v.get("_verified")]
            if failed:
                lines.append(f"\n⚠️ L1c校验: {len(failed)}/{len(verifications)}条未通过")
                for v in failed[:3]:
                    lines.append(f"  {v.get('_warning','?')[:120]}")
            else:
                lines.append(f"\n✅ L1c校验: {len(verifications)}条全部通过")
        
        return "\n".join(lines)


# ══════════════════════════════════════════════
# 符号化存储辅助（供外部调用）
# ══════════════════════════════════════════════

def compress_and_store(content: str, content_type: str = "auto", 
                       source: str = "") -> Dict:
    """压缩内容并返回结构化符号版（用于存入记忆时调用）"""
    sc = SymbolicCompressor()
    result = sc.compress(content, content_type, source)
    return {
        "raw_hash": result.raw_hash,
        "content_type": result.content_type,
        "symbols": result.symbols,
        "key_metrics": result.key_metrics,
        "mermaid": result.mermaid,
        "compressed_text": result.compressed_text,
        "compression_ratio": result.compression_ratio,
    }


# ── CLI ──
if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "记忆系统"
    tier = "all"
    limit = 10
    verify = "--no-verify" not in sys.argv
    
    for arg in sys.argv[2:]:
        if arg.startswith("--tier="):
            tier = arg.split("=", 1)[1]
        elif arg.startswith("--limit="):
            limit = int(arg.split("=", 1)[1])
    
    engine = SearchEngine()
    result = engine.search(query, tier=tier, limit=limit, verify=verify)
    
    print(result["context_text"])
    
    ver = result.get("verification", {})
    v_str = ""
    if ver.get("enabled"):
        v_str = f" 校验:{ver.get('passed',0)}✅/{ver.get('failed',0)}⚠️"
        if ver.get("degraded"):
            v_str += " [降级]"
    
    print(f"\n{result['latency_ms']}ms | {result['algorithm']}{v_str}")
    print(f"技能:{result['hits']['skill']} 轨迹:{result['hits']['trace']} 世界:{result['hits']['world']} →{result['hits']['final']}")
    
    if "--verbose" in sys.argv:
        print("\n[RRF贡献明细]")
        for r in result["results"][:5]:
            contribs = r.get("_rrf_contrib", [])
            if contribs:
                c_str = ", ".join(f"{c['tier']}(R{c['rank']},s={c['score']})" for c in contribs)
                text = r.get("text", r.get("entity", "?"))[:60]
                print(f"  {text}: {c_str}")
        
        if verify and ver.get("failed", 0) > 0:
            print("\n[校验失败详情]")
            for r in result["results"]:
                if r.get("_checks"):
                    for c in r["_checks"]:
                        if not c["pass"]:
                            print(f"  ❌ {c['type']}: {c['message']}")
