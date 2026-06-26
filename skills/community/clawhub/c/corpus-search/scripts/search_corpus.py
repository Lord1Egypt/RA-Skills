#!/usr/bin/env python3
"""
Corpus Search - 语料检索工具

支持语义搜索、元数据过滤、批量搜索、缓存机制。
提供中文元数据字段的正确映射和进度条显示。

主场景元数据字段映射：
- scene_type ↔ 主场景 (scene type)
- emotion ↔ 主情绪 (primary emotion)
- pace ↔ 节奏 (pace)
- quality_score ↔ 质量分 (quality score)
- text_length ↔ 字数 (character count)
- source_file ↔ 来源文件 (source file)
"""

import json
import sys
import hashlib
import argparse
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import OrderedDict

console: Any = None
HAS_RICH = False
try:
    from rich.console import Console

    console = Console()
    HAS_RICH = True
except ImportError:
    pass

HAS_TQDM = False
try:
    from tqdm import tqdm

    HAS_TQDM = True
except ImportError:
    pass

HAS_CACHE = False

# ============== 配置区域 ==============

WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_DIR = WORKSPACE / "skills" / "corpus-search"
CONFIG_DIR = SKILL_DIR / "configs"

DEFAULT_CONFIG: Dict[str, Any] = {
    "search": {"default_limit": 10, "max_limit": 100},
    "models": {"embedding": "BAAI/bge-small-zh-v1.5"},
    "storage": {
        "persist_directory": str(
            WORKSPACE / "skills" / "corpus-builder" / "corpus" / "chroma"
        )
    },
    "cache": {
        "enabled": True,
        "directory": str(WORKSPACE / "skills" / "corpus-search" / "cache"),
        "timeout": 3600,
    },
}

# 中英文元数据字段映射
METADATA_MAPPING: Dict[str, List[str]] = OrderedDict(
    [
        ("scene_type", ["scene_type", "主场景"]),
        ("emotion", ["emotion", "主情绪"]),
        ("pace", ["pace", "节奏"]),
        ("quality_score", ["quality_score", "质量分"]),
        ("text_length", ["text_length", "字数"]),
        ("source_file", ["source_file", "来源文件"]),
    ]
)


# ============== 自定义异常 ==============


class CorpusSearchError(Exception):
    """语料搜索基础异常"""

    pass


class CollectionNotFoundError(CorpusSearchError):
    """语料库不存在错误"""

    def __init__(self, collection_name: str):
        super().__init__(f"未找到语料库：{collection_name}")
        self.collection_name = collection_name


class ModelLoadError(CorpusSearchError):
    """模型加载错误"""

    pass


class ConfigError(CorpusSearchError):
    """配置错误"""

    pass


# ============== 缓存管理器 ==============


class CacheManager:
    """缓存管理器 - 避免重复加载模型"""

    _instance: Optional["CacheManager"] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._cache: Any = None
        self._model_cache: Dict[str, Any] = {}
        self._initialized = True

    def initialize(self, cache_dir: Path, enabled: bool = True) -> None:
        """初始化缓存"""
        # diskcache 已移除，仅使用内存缓存
        pass

    def get_model(self, model_name: str) -> Optional[Any]:
        """从缓存获取模型（仅内存缓存）"""
        return self._model_cache.get(model_name)

    def set_model(self, model_name: str, model: Any) -> None:
        """将模型存入内存缓存"""
        self._model_cache[model_name] = model

    def clear(self) -> None:
        """清空缓存"""
        if self._cache is not None:
            self._cache.clear()
        self._model_cache.clear()

    def _generate_cache_key(self, model_name: str) -> str:
        """生成缓存键"""
        return f"model_{hashlib.md5(model_name.encode()).hexdigest()}"


# ============== 语料检索器 ==============


class CorpusSearcher:
    """语料检索器

    支持语义搜索、元数据过滤、批量搜索。
    使用缓存机制避免重复加载嵌入模型。
    """

    def __init__(self, config: Dict[str, Any]):
        """
        初始化语料检索器

        Args:
            config: 配置字典，包含 models、storage、cache 等配置项
        """
        self.config = config
        self._persist_dir = self._resolve_path(config["storage"]["persist_directory"])
        self._model_name = config["models"]["embedding"]
        self._embedder: Any = None
        self._client: Any = None
        self._console = console if HAS_RICH else None
        self._has_tqdm = HAS_TQDM

        # 初始化缓存
        cache_config = config.get("cache", {})
        if cache_config.get("enabled", True):
            cache_dir = Path(
                cache_config.get(
                    "directory",
                    str(WORKSPACE / "skills" / "corpus-search" / "cache"),
                )
            )
            try:
                CacheManager().initialize(
                    cache_dir, enabled=cache_config.get("enabled", True)
                )
            except ConfigError as e:
                if self._console:
                    self._console.print(f"[yellow]缓存初始化警告：{e}[/yellow]")
                else:
                    print(f"缓存初始化警告：{e}", file=sys.stderr)

    def _resolve_path(self, path: str) -> Path:
        """
        解析路径，处理 ~ 符号

        Args:
            path: 路径字符串

        Returns:
            Path 对象
        """
        if path.startswith("~"):
            return Path.home() / path[2:]
        return Path(path)

    def _print(self, message: str, style: Optional[str] = None) -> None:
        """打印消息，支持富文本样式"""
        if self._console and style:
            self._console.print(message, style=style)
        else:
            print(message)

    def _init_embedder(self) -> None:
        """初始化嵌入模型（内部方法）"""
        if self._embedder is not None:
            return

        cache = CacheManager()
        cached_model = cache.get_model(self._model_name)

        if cached_model is not None:
            self._embedder = cached_model
            self._print(
                f"[green]✅ 从缓存加载嵌入模型：{self._model_name}[/green]", "log.level"
            )
            return

        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise ModelLoadError(
                "请安装 sentence-transformers: pip3 install sentence-transformers"
            ) from e

        self._print(f"正在加载嵌入模型：{self._model_name}...", "log.level")

        try:
            self._embedder = SentenceTransformer(self._model_name)
            cache.set_model(self._model_name, self._embedder)
            self._print("[green]✅ 嵌入模型加载完成[/green]", "log.level")
        except Exception as e:
            raise ModelLoadError(f"模型加载失败：{e}") from e

    def _init_client(self) -> None:
        """初始化 ChromaDB 客户端（内部方法）"""
        if self._client is not None:
            return

        try:
            import pysqlite3.dbapi2 as sqlite3

            sys.modules["sqlite3"] = sqlite3
            self._print(
                "[green]✅ 使用 pysqlite3-binary (SQLite3 3.51.1)[/green]", "log.level"
            )
        except ImportError:
            pass

        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError as e:
            raise CorpusSearchError("请安装 chromadb: pip3 install chromadb") from e

        try:
            self._client = chromadb.PersistentClient(
                path=str(self._persist_dir),
                settings=Settings(anonymized_telemetry=False),
            )
        except Exception as e:
            raise CorpusSearchError(f"无法连接到 ChromaDB：{e}") from e

    def _build_where_filter(
        self, filters: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        构建 Where 过滤条件

        Args:
            filters: 过滤条件字典

        Returns:
            ChromaDB_where 过滤条件
        """
        if not filters:
            return None

        where_conditions: List[Dict[str, Any]] = []

        for key, value in filters.items():
            # 直接使用原始键名（数据库存储的键名）
            # 支持中英文键名
            if key in ["quality_score", "质量分"]:
                where_conditions.append({"质量分": {"$gte": int(value)}})
            elif key in ["scene_type", "主场景"]:
                where_conditions.append({"主场景": {"$eq": str(value)}})
            elif key in ["emotion", "主情绪"]:
                where_conditions.append({"主情绪": {"$eq": str(value)}})
            elif key in ["pace", "节奏"]:
                where_conditions.append({"节奏": {"$eq": str(value)}})
            elif key in ["source_file", "来源文件"]:
                where_conditions.append({"来源文件": {"$eq": str(value)}})
            else:
                where_conditions.append({key: {"$eq": value}})

        if len(where_conditions) == 1:
            return where_conditions[0]
        elif len(where_conditions) > 1:
            return {"$and": where_conditions}

        return None

    def _normalize_metadata_key(self, key: str) -> str:
        """
        规范化元数据键名，支持中英文映射

        Args:
            key: 元数据键名

        Returns:
            标准化的键名
        """
        for standard_key, aliases in METADATA_MAPPING.items():
            if key in aliases:
                return standard_key
        return key

    def _create_progress_bar(
        self, iterable: Any, total: Optional[int] = None, description: str = "处理中"
    ) -> Any:
        """
        创建进度条包装器

        Args:
            iterable: 可迭代对象
            total: 总数量
            description: 描述文本

        Returns:
            tqdm 包装后的迭代器或原迭代器
        """
        if not self._has_tqdm:
            return iterable

        return tqdm(
            iterable,
            total=total,
            desc=description,
            unit="item",
            dynamic_ncols=True,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )

    def search(
        self,
        collection_name: str,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        执行单次搜索

        Args:
            collection_name: 语料库名称
            query: 搜索查询
            filters: 元数据过滤条件
            limit: 返回数量

        Returns:
            搜索结果字典

        Raises:
            CollectionNotFoundError: 语料库不存在
            CorpusSearchError: 搜索过程出错
        """
        self._init_client()
        self._init_embedder()

        try:
            collection = self._client.get_collection(name=collection_name)
        except Exception as e:
            raise CollectionNotFoundError(collection_name) from e

        try:
            query_embedding = self._embedder.encode(
                [query], convert_to_numpy=True
            ).tolist()
        except Exception as e:
            raise CorpusSearchError(f"无法生成查询向量：{e}") from e

        where_filter = self._build_where_filter(filters)

        try:
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=limit,
                where=where_filter,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as e:
            raise CorpusSearchError(f"搜索失败：{e}") from e

        return results

    def batch_search(
        self,
        collection_name: str,
        queries: List[str],
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        批量搜索

        Args:
            collection_name: 语料库名称
            queries: 查询列表
            filters: 元数据过滤条件
            limit: 每个查询的返回数量

        Returns:
            搜索结果列表，每个元素对应一个查询的结果

        Raises:
            CollectionNotFoundError: 语料库不存在
            CorpusSearchError: 搜索过程出错
        """
        self._init_client()
        self._init_embedder()

        try:
            collection = self._client.get_collection(name=collection_name)
        except Exception as e:
            raise CollectionNotFoundError(collection_name) from e

        where_filter = self._build_where_filter(filters)
        results: List[Dict[str, Any]] = []

        try:
            query_embeddings = self._embedder.encode(
                queries, convert_to_numpy=True, show_progress_bar=self._has_tqdm
            ).tolist()
        except Exception as e:
            raise CorpusSearchError(f"无法生成查询向量：{e}") from e

        for result_idx, query_embedding in enumerate(
            self._create_progress_bar(
                query_embeddings,
                total=len(query_embeddings),
                description="批量搜索中",
            )
        ):
            try:
                result = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=limit,
                    where=where_filter,
                    include=["documents", "metadatas", "distances"],
                )
                results.append(result)
            except Exception as e:
                print(f"查询 {result_idx + 1} 失败：{e}", file=sys.stderr)
                results.append(None)

        return results

    def _normalize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        规范化元数据，统一使用标准键名

        Args:
            metadata: 原始元数据

        Returns:
            标准化后的元数据
        """
        normalized: Dict[str, Any] = {}

        for standard_key, aliases in METADATA_MAPPING.items():
            for alias in aliases:
                if alias in metadata:
                    normalized[standard_key] = metadata[alias]
                    break

        return normalized

    def _format_result(
        self, index: int, doc: str, meta: Dict[str, Any], distance: float
    ) -> Dict[str, Any]:
        """
        格式化单个搜索结果

        Args:
            index: 排名
            doc: 文档内容
            meta: 元数据
            distance: 距离值

        Returns:
            格式化后的结果字典
        """
        normalized_meta = self._normalize_metadata(meta)

        return {
            "rank": index + 1,
            "similarity": round(1 - distance, 4),
            "metadata": normalized_meta,
            "content": doc[:500] + "..." if len(doc) > 500 else doc,
            "content_length": len(doc),
        }

    def format_results(
        self,
        results: Dict[str, Any],
        query: Optional[str] = None,
        collection_name: Optional[str] = None,
        output_json: bool = False,
        batch_mode: bool = False,
    ) -> str:
        """
        格式化搜索结果

        Args:
            results: 搜索结果
            query: 查询文本
            collection_name: 语料库名称
            output_json: 是否输出 JSON 格式
            batch_mode: 是否为批量模式

        Returns:
            格式化后的字符串
        """
        if output_json:
            return self._format_json(results, query, collection_name, batch_mode)
        else:
            return self._format_console(results, query, collection_name, batch_mode)

    def _format_json(
        self,
        results: Dict[str, Any],
        query: Optional[str],
        collection_name: Optional[str],
        batch_mode: bool,
    ) -> str:
        """
        JSON 格式输出

        Args:
            results: 搜索结果
            query: 查询文本
            collection_name: 语料库名称
            batch_mode: 批量模式

        Returns:
            JSON 字符串
        """
        if batch_mode and isinstance(results, list):
            output = {"batch_mode": True, "total_queries": len(results), "results": []}

            for result_idx, result_data in enumerate(results):
                if result_data is None:
                    output["results"].append(
                        {"query_index": result_idx, "error": "No results"}
                    )
                else:
                    output["results"].append(
                        self._format_result_batch(
                            result_data=result_data, query_index=result_idx
                        )
                    )

            return json.dumps(output, ensure_ascii=False, indent=2)

        output = {
            "query": query,
            "collection": collection_name,
            "total_results": len(results["documents"][0])
            if results.get("documents")
            else 0,
            "results": [],
        }

        if results.get("documents") and results["documents"][0]:
            for i, (doc, meta, dist) in enumerate(
                zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
            ):
                output["results"].append(self._format_result(i, doc, meta, dist))

        return json.dumps(output, ensure_ascii=False, indent=2)

    def _format_result_batch(
        self, result_data: Dict[str, Any], query_index: int
    ) -> Dict[str, Any]:
        """格式化批量模式单个查询结果"""
        docs = (
            result_data.get("documents", [])[0] if result_data.get("documents") else []
        )
        metadatas = (
            result_data.get("metadatas", [])[0] if result_data.get("metadatas") else []
        )
        distances = (
            result_data.get("distances", [])[0] if result_data.get("distances") else []
        )

        batch_results = []
        for i, (doc, meta, dist) in enumerate(zip(docs, metadatas, distances)):
            batch_results.append(self._format_result(i, doc, meta, dist))

        return {
            "query_index": query_index,
            "total_results": len(batch_results),
            "results": batch_results,
        }

    def _format_console(
        self,
        results: Dict[str, Any],
        query: Optional[str],
        collection_name: Optional[str],
        batch_mode: bool,
    ) -> str:
        """
        控制台格式输出

        Args:
            results: 搜索结果
            query: 查询文本
            collection_name: 语料库名称
            batch_mode: 批量模式

        Returns:
            格式化后的字符串
        """
        lines: List[str] = []

        if batch_mode and isinstance(results, list):
            lines.append("\n" + "=" * 60)
            lines.append("批量搜索结果")
            lines.append("=" * 60)

            for result_data in self._create_progress_bar(
                results, total=len(results), description="格式化结果"
            ):
                if result_data is None:
                    lines.append(f"\n[查询 {result_data}] ❌ 无结果或出错")
                else:
                    lines.extend(self._format_single_query_console(result_data, 0))

            return "\n".join(lines)

        if query:
            lines.append(f"\n🔍 搜索结果：{query}")
        if collection_name:
            lines.append(f"   语料库：{collection_name}")

        total = len(results["documents"][0]) if results.get("documents") else 0
        lines.append(f"   返回数量：{total}")

        if total == 0:
            lines.append("\n  (无结果)")
            return "\n".join(lines)

        lines.extend(self._format_single_query_console(results, 0))

        return "\n".join(lines)

    def _format_single_query_console(
        self, results: Dict[str, Any], query_index: int = 0
    ) -> List[str]:
        """格式化单次查询的控制台输出"""
        lines: List[str] = []

        if query_index > 0:
            lines.append(f"\n{'─' * 60}")

        if query_index > 0:
            lines.append(f"\n📌 查询 {query_index + 1}")

        docs = results.get("documents", [])[0] if results.get("documents") else []
        metadatas = results.get("metadatas", [])[0] if results.get("metadatas") else []
        distances = results.get("distances", [])[0] if results.get("distances") else []

        for i, (doc, meta, dist) in enumerate(zip(docs, metadatas, distances)):
            similarity = (1 - dist) * 100

            normalized_meta = self._normalize_metadata(meta)

            scene_type = normalized_meta.get("scene_type", "N/A")
            emotion = normalized_meta.get("emotion", "N/A")
            pace = normalized_meta.get("pace", "N/A")
            quality = normalized_meta.get("quality_score", "N/A")
            source = normalized_meta.get("source_file", "N/A")
            text_len = normalized_meta.get("text_length", "N/A")

            lines.append(f"\n{i + 1}. 相似度：{similarity:.2f}%")
            lines.append(f"   场景：{scene_type}")
            lines.append(f"   情绪：{emotion}")
            lines.append(f"   节奏：{pace}")
            lines.append(f"   质量：{quality}")
            lines.append(f"   来源：{source}")
            lines.append(f"   块大小：{text_len} 字")
            lines.append("\n   内容预览:")

            preview = doc[:200] + "..." if len(doc) > 200 else doc
            for line in preview.split("\n"):
                lines.append(f"   {line}")

        return lines


# ============== 命令行Interface ==============


def parse_args() -> argparse.Namespace:
    """
    解析命令行参数

    Returns:
        argparse.Namespace 对象
    """
    parser = argparse.ArgumentParser(
        description="Corpus Search - 语料检索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 单次搜索
  python search_corpus.py -q "某场景" -c my_corpus --scene "室内" --emotion "开心"

  # 批量搜索（通过文件）
  python search_corpus.py --batch-queries queries.txt -c my_corpus --limit 5

  # JSON 输出
  python search_corpus.py -q "查询" -c my_corpus --json

  # 导出结果
  python search_corpus.py -q "查询" -c my_corpus --export results.json
        """,
    )

    # 基础选项
    parser.add_argument("--query", "-q", type=str, help="搜索查询文本")
    parser.add_argument(
        "--batch-queries",
        "-b",
        type=str,
        metavar="FILE",
        help="批量查询文件（每行一个查询）",
    )
    parser.add_argument(
        "--collection", "-c", type=str, required=True, help="语料库名称（必填）"
    )
    parser.add_argument(
        "--limit", "-l", type=int, default=10, help="每个查询的返回数量（默认 10）"
    )

    # 过滤选项
    parser.add_argument("--scene", type=str, help="场景类型过滤（支持中英文）")
    parser.add_argument("--emotion", type=str, help="情绪过滤（支持中英文）")
    parser.add_argument("--min-quality", type=int, help="最低质量分（1-10）")

    # 输出选项
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--export", type=str, metavar="FILE", help="导出结果到文件")

    return parser.parse_args()


def load_config(config_path: Path) -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    if config_path.exists():
        try:
            import yaml

            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            if HAS_RICH:
                console.print(f"[yellow]⚠ 配置文件加载警告：{e}[/yellow]")
            else:
                print(f"配置文件加载警告：{e}", file=sys.stderr)
    return DEFAULT_CONFIG


def build_filters(args: argparse.Namespace) -> Dict[str, Any]:
    """
    构建过滤条件

    Args:
        args: 命令行参数

    Returns:
        过滤条件字典
    """
    filters: Dict[str, Any] = {}

    if args.scene:
        filters["主场景"] = args.scene
    if args.emotion:
        filters["主情绪"] = args.emotion
    if args.min_quality is not None:
        filters["min_quality"] = str(args.min_quality)

    return filters


def read_queries_from_file(file_path: str) -> List[str]:
    """
    从文件读取批量查询

    Args:
        file_path: 文件路径

    Returns:
        查询列表

    Raises:
        CorpusSearchError: 文件读取失败
    """
    path = Path(file_path)
    if not path.exists():
        raise CorpusSearchError(f"文件不存在：{file_path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f if line.strip()]
            if not queries:
                raise CorpusSearchError("查询文件为空")
            return queries
    except Exception as e:
        raise CorpusSearchError(f"读取查询文件失败：{e}") from e


def main() -> None:
    """主函数"""
    args = parse_args()

    # 验证输入
    if not args.query and not args.batch_queries:
        print("错误：必须提供 --query 或 --batch-queries", file=sys.stderr)
        sys.exit(1)

    # 加载配置
    config_path = CONFIG_DIR / "default_config.yml"
    config = load_config(config_path)

    # 构建过滤条件
    filters = build_filters(args)

    # 创建检索器
    try:
        searcher = CorpusSearcher(config)
    except ConfigError as e:
        print(f"初始化失败：{e}", file=sys.stderr)
        sys.exit(1)

    try:
        # 批量搜索模式
        if args.batch_queries:
            queries = read_queries_from_file(args.batch_queries)
            results = searcher.batch_search(
                collection_name=args.collection,
                queries=queries,
                filters=filters,
                limit=args.limit,
            )
            output = searcher.format_results(
                results,
                query=f"{len(queries)} 个查询",
                collection_name=args.collection,
                output_json=args.json,
                batch_mode=True,
            )
        else:
            # 单次搜索模式
            results = searcher.search(
                collection_name=args.collection,
                query=args.query,
                filters=filters,
                limit=args.limit,
            )

            output = searcher.format_results(
                results, args.query, args.collection, output_json=args.json
            )

        # 输出结果
        print(output)

        # 导出到文件
        if args.export:
            with open(args.export, "w", encoding="utf-8") as f:
                f.write(output)
            if not args.json:
                print(f"\n✅ 结果导出到：{args.export}")

    except CollectionNotFoundError as e:
        print(f"\n❌ 错误：{e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)

    except ModelLoadError as e:
        print(f"\n❌ 模型加载错误：{e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)

    except CorpusSearchError as e:
        print(f"\n❌ 搜索错误：{e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠ 操作被用户中断", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        if args.verbose:
            import traceback

            traceback.print_exc()
        else:
            print(f"\n❌ 未预期的错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
