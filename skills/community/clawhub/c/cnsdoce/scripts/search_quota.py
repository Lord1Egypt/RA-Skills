# -*- coding: utf-8 -*-
"""
cnsdoce 定额语义搜索脚本（v6 - SQLite优先版）
改进点：
  v6:
  1. SQLite + FTS5 全文搜索优先（毫秒级查询）
  2. 精确查询、模糊查询、FTS5全文三级检索
  3. 材料库也使用SQLite查询
  4. 向后兼容：SQLite不可用时降级到旧方式（FAISS/JSON）
  v5:
  1. 分册精确过滤：search() 支持 volume 参数，先过滤分册再做语义/文本搜索
  2. 纯Python向量索引优先：优先加载 faiss-cpu 索引，ChromaDB 降级为次选
  3. 支持 quota_text_index_v4.json（倒排索引）和 quota_data_v4.json（主数据）
用法：python search_quota.py "DN200焊接钢管" [top_k] [volume]
  eg: python search_quota.py "低压钢管焊接" 5 "第8册"
"""

import json
import re
import sqlite3
import sys
from pathlib import Path


# ==================== 配置 ====================
SKILL_DIR = Path(__file__).parent.parent
INDEX_DIR  = SKILL_DIR / "index"
REFS_DIR   = SKILL_DIR / "references"

# SQLite 数据库（v6 新增，优先使用）
DB_PATH = INDEX_DIR / "quota.db"

# 旧版JSON文件（降级使用）
DATA_FILE  = INDEX_DIR / "quota_data_v4.json"
TEXT_INDEX_FILE = INDEX_DIR / "quota_text_index_v4.json"

# FAISS 索引
FAISS_INDEX_FILE = INDEX_DIR / "quota_index.faiss"
FAISS_META_FILE  = INDEX_DIR / "quota_metadata.json"

# ChromaDB 目录
CHROMA_DIR = INDEX_DIR / "chroma_db"


# ==================== 工具函数 ====================
def quota_no_to_volume(quota_no: str) -> str:
    """从定额编号提取分册号，如 'AZ-8-3-28' → '第8册'"""
    # 去掉专业前缀
    no = quota_no.split("-", 1)[-1] if "-" in quota_no else quota_no
    m = re.match(r'(\d+)', no)
    return f"第{m.group(1)}册" if m else ""


def parse_volume_arg(volume: str) -> str:
    """将用户输入的分册参数统一化为 '第X册' 格式"""
    if not volume:
        return ""
    m = re.search(r'(\d+)', str(volume))
    return f"第{m.group(1)}册" if m else volume.strip()


def volume_to_prefix(volume: str) -> str:
    """将分册参数转为定额编号前缀，如 '第8册' → 'AZ-8-'"""
    if not volume:
        return ""
    m = re.search(r'(\d+)', str(volume))
    if not m:
        return ""
    return f"AZ-{m.group(1)}-"


def _row_to_dict(cursor, row):
    """将SQLite Row转为dict"""
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row))


# ==================== SQLite 搜索器（v6 新增）====================
class SQLiteQuotaSearcher:
    """SQLite + FTS5 定额搜索器（毫秒级查询）"""

    def __init__(self, db_path: Path = None):
        self.db_path = db_path or DB_PATH
        self.conn = None
        self.has_fts5 = False
        self._connect()

    def _connect(self):
        """连接SQLite数据库"""
        if not self.db_path.exists():
            raise FileNotFoundError(f"SQLite数据库不存在：{self.db_path}")

        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA cache_size=-64000")  # 64MB缓存
        self.conn.execute("PRAGMA temp_store=MEMORY")

        # 检测FTS5
        try:
            cursor = self.conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='quotas_fts'"
            )
            self.has_fts5 = cursor.fetchone() is not None
        except Exception:
            self.has_fts5 = False

    def close(self):
        if self.conn:
            self.conn.close()

    # ---------- 定额查询 ----------

    def search(self, query: str, top_k: int = 5, volume: str = None) -> list:
        """
        搜索定额（三级检索策略，针对中文优化）
        策略1: LIKE模糊查询（中文首选，1-3ms，完美支持中文）
        策略2: 多关键词拆分LIKE（支持"DN200 阀门"等复合查询）
        策略3: 精确编号匹配
        """
        vol_prefix = volume_to_prefix(volume) if volume else ""

        # 策略1: 整词LIKE模糊查询
        results = self._search_like(query, top_k, vol_prefix)
        if results:
            return results

        # 策略2: 拆分多关键词（空格/逗号分隔）
        keywords = re.split(r'[\s,，、]+', query.strip())
        if len(keywords) > 1:
            results = self._search_multi_keyword(keywords, top_k, vol_prefix)
            if results:
                return results

        # 策略3: 精确编号匹配
        return self._search_by_quota_no(query, vol_prefix)

    def _search_fts5(self, query: str, top_k: int, vol_prefix: str) -> list:
        """FTS5 全文搜索（英文/数字查询用，中文效果差）"""
        # FTS5默认分词器(unicode61)对中文按单字分词，短语匹配不可靠
        # 仅在英文/数字查询时使用
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', query))
        if has_chinese:
            return []

        sql = """
            SELECT q.quota_no, q.name, q.unit, q.base_price, q.price_tax,
                   q.labor_fee, q.material_fee, q.machine_fee,
                   q.chapter, q.category, q.work_content, q.source,
                   q.category_prefix, q.original_quota_no,
                   f.rank as score
            FROM quotas_fts f
            JOIN quotas q ON q.id = f.rowid
            WHERE quotas_fts MATCH ?
        """
        params = [query]

        if vol_prefix:
            sql += " AND q.quota_no LIKE ?"
            params.append(f"{vol_prefix}%")

        sql += " ORDER BY f.rank LIMIT ?"
        params.append(top_k)

        try:
            cursor = self.conn.execute(sql, params)
            return self._format_results(cursor)
        except Exception:
            return []

    def _search_like(self, query: str, top_k: int, vol_prefix: str) -> list:
        """LIKE 模糊查询（中文首选，1-3ms），同时搜索name和chapter字段"""
        sql = """
            SELECT quota_no, name, unit, base_price, price_tax,
                   labor_fee, material_fee, machine_fee,
                   chapter, category, work_content, source,
                   category_prefix, original_quota_no
            FROM quotas
            WHERE (name LIKE ? OR chapter LIKE ?)
        """
        params = [f"%{query}%", f"%{query}%"]

        if vol_prefix:
            sql += " AND quota_no LIKE ?"
            params.append(f"{vol_prefix}%")

        sql += " LIMIT ?"
        params.append(top_k)

        cursor = self.conn.execute(sql, params)
        return self._format_results(cursor)

    def _search_multi_keyword(self, keywords: list, top_k: int, vol_prefix: str) -> list:
        """多关键词AND搜索（如"DN200 阀门"→同时匹配DN200和阀门），搜索name+chapter"""
        # 每个关键词需在 name 或 chapter 中出现
        conditions = []
        params = []
        for kw in keywords:
            conditions.append("(name LIKE ? OR chapter LIKE ?)")
            params.extend([f"%{kw}%", f"%{kw}%"])

        sql = f"""
            SELECT quota_no, name, unit, base_price, price_tax,
                   labor_fee, material_fee, machine_fee,
                   chapter, category, work_content, source,
                   category_prefix, original_quota_no
            FROM quotas
            WHERE {' AND '.join(conditions)}
        """

        if vol_prefix:
            sql += " AND quota_no LIKE ?"
            params.append(f"{vol_prefix}%")

        sql += " LIMIT ?"
        params.append(top_k)

        cursor = self.conn.execute(sql, params)
        return self._format_results(cursor)

    def _search_by_quota_no(self, query: str, vol_prefix: str) -> list:
        """按定额编号精确/前缀查询"""
        # 尝试带专业前缀精确查询
        sql = """
            SELECT quota_no, name, unit, base_price, price_tax,
                   labor_fee, material_fee, machine_fee,
                   chapter, category, work_content, source,
                   category_prefix, original_quota_no
            FROM quotas WHERE quota_no = ?
        """
        cursor = self.conn.execute(sql, [query])
        results = self._format_results(cursor)
        if results:
            return results

        # 尝试不带前缀
        sql = "SELECT * FROM quotas WHERE original_quota_no = ?"
        cursor = self.conn.execute(sql, [query])
        return self._format_results(cursor)

    def search_by_quota_no(self, quota_no: str) -> list:
        """按定额编号精确查询"""
        # 先尝试带前缀
        sql = """
            SELECT quota_no, name, unit, base_price, price_tax,
                   labor_fee, material_fee, machine_fee,
                   chapter, category, work_content, source,
                   category_prefix, original_quota_no
            FROM quotas WHERE quota_no = ?
        """
        cursor = self.conn.execute(sql, [quota_no])
        results = self._format_results(cursor)
        if results:
            return results

        # 再尝试不带前缀
        sql2 = sql + " OR original_quota_no = ?"
        cursor = self.conn.execute(sql2, [quota_no, quota_no])
        return self._format_results(cursor)

    def search_by_volume(self, volume: str, limit: int = 20) -> list:
        """列出某分册的定额（前N条）"""
        vol_prefix = volume_to_prefix(volume)
        if not vol_prefix:
            return []

        sql = """
            SELECT quota_no, name, unit, base_price, price_tax,
                   labor_fee, material_fee, machine_fee,
                   chapter, category, work_content, source,
                   category_prefix, original_quota_no
            FROM quotas WHERE quota_no LIKE ?
            LIMIT ?
        """
        cursor = self.conn.execute(sql, [f"{vol_prefix}%", limit])
        return self._format_results(cursor)

    # ---------- 材料查询 ----------

    def search_material(self, keyword: str, top_k: int = 10, source: str = None) -> list:
        """
        搜索材料价格
        :param keyword: 搜索关键词（名称/规格）
        :param top_k: 返回条数
        :param source: 数据来源过滤（如 '价格取定表(2026)'）
        """
        sql = """
            SELECT orig_id, 编码, 名称, 规格型号, 单位,
                   含税单价, 除税单价, 增值税率,
                   含税单价_202602, 含税单价_202603, 取定价,
                   数据来源, 备注, 适用专业
            FROM materials
            WHERE 名称 LIKE ?
        """
        params = [f"%{keyword}%"]

        if source:
            sql += " AND 数据来源 = ?"
            params.append(source)

        sql += " LIMIT ?"
        params.append(top_k)

        cursor = self.conn.execute(sql, params)
        columns = [desc[0] for desc in cursor.description]
        results = []
        for row in cursor.fetchall():
            item = dict(zip(columns, row))
            results.append(item)
        return results

    def search_material_by_dn(self, target_dn: int, keyword: str = "", top_k: int = 10) -> list:
        """
        按DN口径搜索材料（DN/管外径/φ多格式匹配）
        :param target_dn: 目标DN口径（如 200）
        :param keyword: 额外关键词（如 "阀门"、"钢管"）
        """
        # DN→管外径映射
        dn_map = {
            15:18, 20:25, 25:32, 32:38, 40:45, 50:57, 65:76, 80:89,
            100:108, 125:133, 150:159, 200:219, 250:273, 300:325,
            350:377, 400:426, 450:480, 500:530, 600:630, 700:720, 800:820
        }
        outer_d = dn_map.get(target_dn, 0)

        # 构建搜索条件
        conditions = ["名称 LIKE ?"]
        params = [f"%DN{target_dn}%"]

        if outer_d:
            conditions.append("名称 LIKE ?")
            params.append(f"%D{outer_d}%")
            conditions.append("名称 LIKE ?")
            params.append(f"%φ{outer_d}%")
            conditions.append("名称 LIKE ?")
            params.append(f"%Φ{outer_d}%")

        if keyword:
            conditions.append("名称 LIKE ?")
            params.append(f"%{keyword}%")

        where_clause = " OR ".join(conditions)

        sql = f"""
            SELECT orig_id, 编码, 名称, 规格型号, 单位,
                   含税单价, 除税单价, 增值税率,
                   含税单价_202602, 含税单价_202603, 取定价,
                   数据来源, 备注, 适用专业
            FROM materials
            WHERE ({where_clause})
            LIMIT ?
        """
        params.append(top_k)

        cursor = self.conn.execute(sql, params)
        columns = [desc[0] for desc in cursor.description]
        results = []
        for row in cursor.fetchall():
            item = dict(zip(columns, row))
            # 计算匹配分数
            name = item.get("名称", "")
            score = 0
            if f"DN{target_dn}" in name:
                score += 10
            if outer_d and f"D{outer_d}" in name:
                score += 9
            if outer_d and (f"φ{outer_d}" in name or f"Φ{outer_d}" in name):
                score += 8
            if keyword and keyword in name:
                score += 3
            item["match_score"] = score
            results.append(item)

        # 按分数排序
        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        return results

    # ---------- 内部方法 ----------

    def _format_results(self, cursor) -> list:
        """格式化查询结果为统一dict格式"""
        columns = [desc[0] for desc in cursor.description]
        results = []
        for row in cursor.fetchall():
            item = dict(zip(columns, row))
            # 添加 volume 字段
            item["volume"] = quota_no_to_volume(item.get("quota_no", ""))
            results.append(item)
        return results

    def get_stats(self) -> dict:
        """获取数据库统计信息"""
        stats = {}
        stats["quota_count"] = self.conn.execute("SELECT COUNT(*) FROM quotas").fetchone()[0]
        stats["material_count"] = self.conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
        stats["has_fts5"] = self.has_fts5

        # 各专业统计
        cursor = self.conn.execute("""
            SELECT category_prefix, COUNT(*) as cnt
            FROM quotas GROUP BY category_prefix ORDER BY cnt DESC
        """)
        stats["by_category"] = dict(cursor.fetchall())

        return stats


# ==================== 兼容旧版：JSON/FAISS/ChromaDB 搜索器 ====================
class LegacyQuotaSearcher:
    """旧版搜索器（JSON遍历/FAISS/ChromaDB），作为降级备选"""

    def __init__(self, index_dir: Path = None):
        self.index_dir = index_dir or INDEX_DIR
        self.items = []
        self.text_index = {}
        self.faiss_index = None
        self.faiss_meta  = []
        self.chroma_collection = None
        self.search_type = "none"
        self._load_index()

    def _load_index(self):
        """按优先级加载索引：FAISS > ChromaDB > 文本倒排"""
        self._load_main_data()

        if FAISS_INDEX_FILE.exists() and FAISS_META_FILE.exists():
            try:
                self._load_faiss()
                return
            except Exception as e:
                print(f"⚠ FAISS 加载失败，降级: {e}")

        if CHROMA_DIR.exists():
            try:
                self._load_chromadb()
                return
            except Exception as e:
                print(f"⚠ ChromaDB 加载失败，降级: {e}")

        if TEXT_INDEX_FILE.exists():
            self._load_text_index()
            return

    def _load_main_data(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.items = json.load(f)

    def _load_faiss(self):
        import faiss
        self.faiss_index = faiss.read_index(str(FAISS_INDEX_FILE))
        with open(FAISS_META_FILE, 'r', encoding='utf-8') as f:
            self.faiss_meta = json.load(f)
        self.search_type = "faiss"

    def _load_chromadb(self):
        import chromadb
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.chroma_collection = client.get_collection("quota_index")
        self.search_type = "chroma"

    def _load_text_index(self):
        with open(TEXT_INDEX_FILE, 'r', encoding='utf-8') as f:
            self.text_index = json.load(f)
        self.search_type = "text"

    def search(self, query: str, top_k: int = 5, volume: str = None) -> list:
        vol = parse_volume_arg(volume) if volume else ""
        if self.search_type == "faiss":
            return self._search_faiss(query, top_k, vol)
        elif self.search_type == "chroma":
            return self._search_chroma(query, top_k, vol)
        else:
            return self._search_text(query, top_k, vol)

    def _search_faiss(self, query, top_k, volume):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            return self._search_text(query, top_k, volume)

        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        import numpy as np
        query_emb = model.encode([query]).astype('float32')
        import faiss
        faiss.normalize_L2(query_emb)

        search_k = max(top_k * 3, 50)
        distances, indices = self.faiss_index.search(query_emb, search_k)

        results = []
        seen = set()
        vol_prefix = volume.replace("第", "").replace("册", "").strip() + "-" if volume else ""
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.faiss_meta):
                continue
            meta = self.faiss_meta[idx]
            if vol_prefix and not meta.get("quota_no", "").startswith(vol_prefix):
                continue
            key = meta.get("quota_no", "") + meta.get("name", "")
            if key in seen:
                continue
            seen.add(key)
            item = meta.copy()
            item["similarity_score"] = float(distances[0][i])
            item["volume"] = quota_no_to_volume(meta.get("quota_no", ""))
            results.append(item)
            if len(results) >= top_k:
                break
        return results

    def _search_chroma(self, query, top_k, volume):
        where_clause = None
        if volume:
            vol_num = re.search(r'(\d+)', volume)
            if vol_num:
                where_clause = {"volume": quota_no_to_volume(vol_num.group(1))}
        results = self.chroma_collection.query(
            query_texts=[query], n_results=top_k, where=where_clause
        )
        metadatas = results.get('metadatas', [[]])[0]
        for m in metadatas:
            if "volume" not in m:
                m["volume"] = quota_no_to_volume(m.get("quota_no", ""))
        return metadatas

    def _search_text(self, query, top_k, volume):
        if not self.text_index:
            return []
        tokens = set()
        for ch in query:
            if ch.strip():
                tokens.add(ch)
        for i in range(len(query) - 1):
            tokens.add(query[i:i+2])

        score_map = {}
        for token in tokens:
            if token in self.text_index:
                for idx in self.text_index[token]:
                    score_map[idx] = score_map.get(idx, 0) + 1

        sorted_indices = sorted(score_map.items(), key=lambda x: -x[1])
        results = []
        seen = set()
        vol_prefix = volume.replace("第", "").replace("册", "").strip() + "-" if volume else ""
        for idx, score in sorted_indices:
            if idx < 0 or idx >= len(self.items):
                continue
            item = self.items[idx].copy()
            if vol_prefix and not item.get("quota_no", "").startswith(vol_prefix):
                continue
            key = item.get("quota_no", "") + item.get("name", "")
            if key in seen:
                continue
            seen.add(key)
            item["score"] = score
            item["volume"] = quota_no_to_volume(item.get("quota_no", ""))
            results.append(item)
            if len(results) >= top_k:
                break
        return results

    def search_by_quota_no(self, quota_no: str) -> list:
        results = []
        for item in self.items:
            if item.get("quota_no") == quota_no:
                item["volume"] = quota_no_to_volume(item.get("quota_no", ""))
                results.append(item)
        return results

    def search_by_volume(self, volume: str, limit: int = 20) -> list:
        vol = parse_volume_arg(volume)
        if not vol:
            return []
        prefix = vol.replace("第", "").replace("册", "").strip() + "-"
        results = []
        for item in self.items:
            if item.get("quota_no", "").startswith(prefix):
                item["volume"] = vol
                results.append(item)
            if len(results) >= limit:
                break
        return results


# ==================== 统一搜索器（自动选择最优后端）====================
class QuotaSearcher:
    """定额搜索器（v6：SQLite优先，降级到旧版）"""

    def __init__(self, index_dir: Path = None):
        self.index_dir = index_dir or INDEX_DIR
        self.searcher = None
        self.search_type = "none"
        self._init_searcher()

    def _init_searcher(self):
        """按优先级初始化搜索后端：SQLite > FAISS > ChromaDB > 文本倒排"""
        # 优先使用SQLite
        db_path = self.index_dir / "quota.db"
        if db_path.exists():
            try:
                self.searcher = SQLiteQuotaSearcher(db_path)
                self.search_type = "sqlite"
                stats = self.searcher.get_stats()
                print(f"✓ SQLite 搜索器已初始化（定额{stats['quota_count']}条，材料{stats['material_count']}条，FTS5={'✓' if stats['has_fts5'] else '✗'}）")
                return
            except Exception as e:
                print(f"⚠ SQLite 初始化失败，降级: {e}")

        # 降级到旧版
        try:
            self.searcher = LegacyQuotaSearcher(self.index_dir)
            self.search_type = self.searcher.search_type
            print(f"✓ 旧版搜索器已初始化（类型：{self.search_type}）")
        except Exception as e:
            print(f"❌ 搜索器初始化失败: {e}")

    def search(self, query: str, top_k: int = 5, volume: str = None) -> list:
        """搜索定额"""
        if self.searcher:
            return self.searcher.search(query, top_k, volume)
        return []

    def search_by_quota_no(self, quota_no: str) -> list:
        """按定额编号精确查询"""
        if self.searcher:
            return self.searcher.search_by_quota_no(quota_no)
        return []

    def search_by_volume(self, volume: str, limit: int = 20) -> list:
        """列出某分册的定额"""
        if self.searcher:
            return self.searcher.search_by_volume(volume, limit)
        return []

    def search_material(self, keyword: str, top_k: int = 10, source: str = None) -> list:
        """搜索材料价格（仅SQLite模式支持）"""
        if isinstance(self.searcher, SQLiteQuotaSearcher):
            return self.searcher.search_material(keyword, top_k, source)
        return []

    def search_material_by_dn(self, target_dn: int, keyword: str = "", top_k: int = 10) -> list:
        """按DN口径搜索材料（仅SQLite模式支持）"""
        if isinstance(self.searcher, SQLiteQuotaSearcher):
            return self.searcher.search_material_by_dn(target_dn, keyword, top_k)
        return []

    def get_stats(self) -> dict:
        """获取统计信息"""
        if isinstance(self.searcher, SQLiteQuotaSearcher):
            return self.searcher.get_stats()
        return {"search_type": self.search_type}


# ==================== 主程序 ====================
def main():
    if len(sys.argv) < 2:
        print("cnsdoce 定额语义搜索 v6（SQLite优先版）")
        print()
        print("用法: python search_quota.py <搜索关键词> [top_k] [volume]")
        print("示例:")
        print('  python search_quota.py "DN200焊接钢管"')
        print('  python search_quota.py "低压钢管焊接" 5')
        print('  python search_quota.py "低压钢管焊接" 5 "第8册"')
        print('  python search_quota.py "调节阀" 5 "第8册"')
        print()
        print("特殊查询:")
        print('  python search_quota.py --quota-no AZ-8-3-27     # 精确编号查询')
        print('  python search_quota.py --volume 第8册           # 列出分册定额')
        print('  python search_quota.py --material 法兰阀门       # 材料价格查询')
        print('  python search_quota.py --material-dn 200 阀门    # 按DN口径查材料')
        print('  python search_quota.py --stats                   # 数据库统计')
        sys.exit(1)

    args = sys.argv[1:]

    # 特殊查询模式
    if args[0] == "--quota-no" and len(args) > 1:
        searcher = QuotaSearcher()
        results = searcher.search_by_quota_no(args[1])
        _print_results(results, "定额编号查询")
        return

    if args[0] == "--volume" and len(args) > 1:
        searcher = QuotaSearcher()
        results = searcher.search_by_volume(args[1], 20)
        _print_results(results, f"分册查询 {args[1]}")
        return

    if args[0] == "--material" and len(args) > 1:
        searcher = QuotaSearcher()
        results = searcher.search_material(args[1])
        _print_material_results(results)
        return

    if args[0] == "--material-dn" and len(args) > 1:
        searcher = QuotaSearcher()
        dn = int(args[1])
        keyword = args[2] if len(args) > 2 else ""
        results = searcher.search_material_by_dn(dn, keyword)
        _print_material_results(results)
        return

    if args[0] == "--stats":
        searcher = QuotaSearcher()
        stats = searcher.get_stats()
        print("\n📊 数据库统计")
        print("=" * 40)
        for k, v in stats.items():
            print(f"  {k}: {v}")
        return

    # 常规搜索
    query  = args[0]
    top_k  = int(args[1]) if len(args) > 1 else 5
    volume = args[2] if len(args) > 2 else None

    print("=" * 60)
    vol_hint = f"（分册过滤：{volume}）" if volume else ""
    print(f"搜索: {query} {vol_hint}")
    print("=" * 60)

    searcher = QuotaSearcher()
    if searcher.search_type == "none":
        print("❌ 无可用搜索后端")
        sys.exit(1)

    results = searcher.search(query, top_k, volume)

    if not results:
        print("\n未找到匹配结果，请尝试其他关键词")
        return

    print(f"\n找到 {len(results)} 条匹配结果（搜索类型：{searcher.search_type}）:\n")
    _print_results(results, "定额搜索")


def _print_results(results, title):
    """打印定额查询结果"""
    for i, item in enumerate(results, 1):
        print(f"--- 结果 {i} ---")
        print(f"  定额编号: {item.get('quota_no', 'N/A')}")
        print(f"  子目名称: {item.get('name', 'N/A')}")
        print(f"  单位:     {item.get('unit', 'N/A')}")
        print(f"  分册:     {item.get('volume', 'N/A')}")
        print(f"  章节:     {item.get('chapter', 'N/A')}")
        print(f"  基价:     {item.get('base_price', 'N/A')} 元")
        print(f"  人工费:   {item.get('labor_fee', 'N/A')} 元")
        print(f"  材料费:   {item.get('material_fee', 'N/A')} 元")
        print(f"  机械费:   {item.get('machine_fee', 'N/A')} 元")
        if 'score' in item:
            print(f"  匹配分:   {item['score']}")
        if 'similarity_score' in item:
            print(f"  相似度:   {item['similarity_score']:.4f}")
        print()


def _print_material_results(results):
    """打印材料查询结果"""
    if not results:
        print("未找到匹配材料")
        return

    print(f"\n找到 {len(results)} 条材料:\n")
    for i, item in enumerate(results, 1):
        print(f"--- 材料 {i} ---")
        print(f"  编码: {item.get('编码', 'N/A')}")
        print(f"  名称: {item.get('名称', 'N/A')}")
        print(f"  规格: {item.get('规格型号', '-')}")
        print(f"  单位: {item.get('单位', 'N/A')}")

        # 根据数据来源显示正确价格
        source = item.get('数据来源', '')
        if source == '济南造价信息2026年03期':
            print(f"  03期市场价: {item.get('含税单价_202603', 'N/A')} 元")
            print(f"  02期市场价: {item.get('含税单价_202602', 'N/A')} 元")
            print(f"  取定价:     {item.get('取定价', 'N/A')} 元")
        else:
            print(f"  含税单价: {item.get('含税单价', 'N/A')} 元")
            print(f"  除税单价: {item.get('除税单价', 'N/A')} 元")

        print(f"  数据来源: {source}")
        if 'match_score' in item:
            print(f"  匹配分:   {item['match_score']}")
        print()


if __name__ == "__main__":
    main()
