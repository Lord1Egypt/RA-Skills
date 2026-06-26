#!/usr/bin/env python3
"""
Corpus Builder - 语料库构建工具

支持智能分块、AI 标注、向量化存储。使用 ChromaDB 进行向量检索，
支持 YAML/JSON 混合存储，完全离线运行。

Author: OpenClaw
Version: 1.0.0
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import psutil
import yaml
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn

# 支持两种运行方式：作为脚本直接运行 or 作为模块导入
if __name__ == "__main__" and __package__ is None:
    # 作为脚本运行时，添加父目录到 sys.path
    parent_dir = Path(__file__).resolve().parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    # 使用绝对导入
    from scripts.annotator import AIAnnotator, FeatureExtractor
    from scripts.chunker import Chunk, TextChunker
    from scripts.embedder import EmbeddingGenerator
    from scripts.store import VectorStore
    from scripts.utils import load_config, setup_sqlite3
else:
    # 作为模块运行时，使用相对导入
    from .annotator import AIAnnotator, FeatureExtractor
    from .chunker import Chunk, TextChunker
    from .embedder import EmbeddingGenerator
    from .store import VectorStore
    from .utils import load_config, setup_sqlite3

# 修复 SQLite3 版本问题：优先使用 pysqlite3-binary (需要 sqlite3 >= 3.35.0)
setup_sqlite3()

console = Console()


def build_corpus(
    args: argparse.Namespace,
    config: Dict,
    chunker: TextChunker,
    extractor: FeatureExtractor,
    annotator: AIAnnotator,
    embedder: EmbeddingGenerator,
    store: VectorStore,
):
    """构建语料库"""
    console.print(f"\n📚 开始构建语料库：[bold]{args.name}[/bold]")
    console.print(f"📁 源目录：{args.source}")
    console.print(f"📝 题材：{args.genre or '未指定'}")

    # 检查内存
    memory = psutil.virtual_memory()
    if memory.percent > 90:
        console.print(f"\n❌ 错误：内存使用过高 ({memory.percent:.1f}%)")
        sys.exit(1)

    # 查找所有 TXT 文件
    source_path = Path(args.source)
    txt_files = list(source_path.glob("*.txt"))

    if not txt_files:
        console.print(f"\n❌ 错误：未找到 TXT 文件：{args.source}")
        sys.exit(1)

    console.print(f"✅ 找到 {len(txt_files)} 个 TXT 文件")

    # 创建集合
    collection = store.create_collection(
        name=args.name, metadata={"genre": args.genre} if args.genre else None
    )

    # 处理文件
    all_chunks: List[Chunk] = []
    processed_files = []
    checkpoint_file = (
        args.checkpoint
        or f"{config['storage']['checkpoint_dir']}/{args.name}_checkpoint.json"
    )

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("处理文件...", total=len(txt_files))

        for txt_file in txt_files:
            try:
                # 读取文件
                text = txt_file.read_text(encoding="utf-8")

                # 分块
                chunks = chunker.chunk_by_scene(text, txt_file.name)

                # 特征提取
                for chunk in chunks:
                    chunk.features = extractor.extract_features(chunk.text)
                    chunk.annotation = {
                        "source_file": chunk.source_file,
                        **extractor.predict_preliminary_tags(chunk.features),
                    }

                all_chunks.extend(chunks)
                processed_files.append(txt_file.name)

                progress.update(task, advance=1)

                # 检查内存
                if len(processed_files) % 10 == 0:
                    memory = psutil.virtual_memory()
                    if memory.percent > 85:
                        console.print(
                            f"\n⚠️  警告：内存使用过高 ({memory.percent:.1f}%)"
                        )

            except Exception as e:
                console.print(f"\n❌ 处理文件失败：{txt_file.name}: {str(e)}")
                continue

    console.print(f"\n✅ 分块完成：{len(all_chunks)} 个语料块")

    # 特征提取
    if args.verbose:
        console.print("\n📝 提取特征...")

    chunks_no_features = [c for c in all_chunks if c.features is None]
    if chunks_no_features:
        for i in range(0, len(chunks_no_features), 100):
            batch = chunks_no_features[i : i + 100]
            for chunk in batch:
                chunk.features = extractor.extract_features(chunk.text)

    # AI 标注
    if args.verbose:
        console.print("\n🤖 AI 标注...")

    chunks_no_annotation = [
        c for c in all_chunks if not c.annotation or c.annotation.get("fallback")
    ]

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("标注中...", total=len(chunks_no_annotation))

        for i in range(0, len(chunks_no_annotation), args.batch_size):
            batch = chunks_no_annotation[i : i + args.batch_size]

            for chunk in batch:
                if not chunk.annotation:
                    chunk.annotation = {"source_file": chunk.source_file}
                chunk.annotation.update(
                    {
                        "source_file": chunk.source_file,
                        **extractor.predict_preliminary_tags(chunk.features),
                    }
                )
                chunk.annotation = annotator.annotate(chunk.text, chunk.annotation)

            progress.update(task, advance=min(args.batch_size, len(batch)))

    console.print("\n✅ AI 标注完成")

    # 向量化
    if args.verbose:
        console.print("\n🚀 向量化...")

    texts = [c.text for c in all_chunks]

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("向量化中...", total=len(texts))

        embeddings = embedder.batch_generate_with_resume(
            texts, checkpoint_file, config["processing"]["embedding_batch_size"]
        )

        # 更新 chunk.embedding
        for i, chunk in enumerate(all_chunks):
            chunk.embedding = embeddings[i]
            progress.update(task, advance=len(texts[i : i + 1]))

    console.print("\n✅ 向量化完成")

    # 存储到 ChromaDB
    if args.verbose:
        console.print("\n💾 存储到 ChromaDB...")

    store.add_annotated_chunks(collection, all_chunks)

    console.print("\n✅ 存储完成")

    # 保存标注到 JSON 文件
    output_dir = Path(config["storage"]["persist_directory"]) / "annotations"
    output_dir.mkdir(parents=True, exist_ok=True)

    annotations_path = output_dir / f"{args.name}_annotations.json"
    export_data = []
    for chunk in all_chunks:
        export_data.append(
            {
                "id": f"chunk_{len(export_data):06d}",
                **chunk.annotation,
                "original_text": chunk.text,
                "source_file": chunk.source_file,
                "embedding": chunk.embedding,
            }
        )

    with open(annotations_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    console.print(f"✅ 标注保存到：{annotations_path}")

    # 保存处理记录
    checkpoint_data = {
        "processed_files": processed_files,
        "processed_chunks": len(all_chunks),
        "last_updated": datetime.now().isoformat(),
    }

    Path(checkpoint_file).parent.mkdir(parents=True, exist_ok=True)
    with open(checkpoint_file, "w", encoding="utf-8") as f:
        json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)

    console.print(f"✅ 断点保存到：{checkpoint_file}")

    # 统计信息
    scene_dist = {}
    emotion_dist = {}
    for chunk in all_chunks:
        for s in chunk.annotation.get("scene_type", []):
            scene_dist[s] = scene_dist.get(s, 0) + 1
        for e in chunk.annotation.get("emotion", []):
            emotion_dist[e] = emotion_dist.get(e, 0) + 1

    avg_quality = sum(c.annotation.get("quality_score", 5) for c in all_chunks) / max(
        len(all_chunks), 1
    )

    stats = {
        "collection_name": args.name,
        "genre": args.genre,
        "total_chunks": len(all_chunks),
        "total_files": len(processed_files),
        "avg_chunk_size": sum(len(c.text) for c in all_chunks)
        / max(len(all_chunks), 1),
        "scene_type_dist": scene_dist,
        "emotion_dist": emotion_dist,
        "avg_quality_score": round(avg_quality, 2),
        "processed_time": datetime.now().isoformat(),
    }

    stats_path = output_dir / f"{args.name}_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    console.print("\n📊 统计信息:")
    console.print(f"  总块数：{stats['total_chunks']}")
    console.print(f"  文件数：{stats['total_files']}")
    console.print(f"  平均块大小：{stats['avg_chunk_size']:.0f} 字")
    console.print(f"  平均质量分：{stats['avg_quality_score']}")
    console.print(f"  场景分布：{list(scene_dist.items())[:5]}")
    console.print(f"  情绪分布：{list(emotion_dist.items())[:5]}")
    console.print(f"\n✅ 统计信息保存到：{stats_path}")

    console.print(f"\n🎉 语料库构建完成：{args.name}")


def show_stats(args: argparse.Namespace, config: Dict):
    """显示统计信息"""
    persist_dir = Path(config["storage"]["persist_directory"])
    stats_path = persist_dir / "annotations" / f"{args.name}_stats.json"

    if not stats_path.exists():
        console.print(f"\n❌ 错误：未找到统计文件：{stats_path}")
        console.print(
            "   请先构建语料库：python3 build_corpus.py --source ... --name ..."
        )
        sys.exit(1)

    with open(stats_path, encoding="utf-8") as f:
        stats = json.load(f)

    console.print(f"\n📊 语料库统计：{stats['collection_name']}")
    console.print(f"  生成时间：{stats['processed_time']}")
    console.print(f"  总块数：{stats['total_chunks']}")
    console.print(f"  文件数：{stats['total_files']}")
    console.print(f"  题材：{stats.get('genre', '未指定')}")
    console.print(f"  平均块大小：{stats['avg_chunk_size']:.0f} 字")
    console.print(f"  平均质量分：{stats['avg_quality_score']}")

    # 绘制场景分布
    if stats.get("scene_type_dist"):
        console.print("\n  场景分布:")
        for scene, count in sorted(
            stats["scene_type_dist"].items(), key=lambda x: -x[1]
        )[:10]:
            console.print(f"    {scene}: {count}")

    # 绘制情绪分布
    if stats.get("emotion_dist"):
        console.print("\n  情绪分布:")
        for emotion, count in sorted(
            stats["emotion_dist"].items(), key=lambda x: -x[1]
        )[:10]:
            console.print(f"    {emotion}: {count}")

    # 检查 ChromaDB 集合
    store = VectorStore(config["storage"]["persist_directory"])
    try:
        collection = store.client.get_collection(name=args.name)
        console.print("\n  ChromaDB 集合：[bold green]✅ 存在[/bold green]")
        # 尝试获取向量维度（兼容不同 ChromaDB 版本）
        try:
            dim = getattr(collection._embedding_function, "dimension", None)
            if dim:
                console.print(f"    向量维度：{dim}")
        except AttributeError:
            pass
        console.print(f"    文档数：{collection.count()}")
    except Exception:
        console.print("\n  ChromaDB 集合：[bold red]❌ 不存在[/bold red]")


def export_annotations(args: argparse.Namespace, config: Dict, store: VectorStore):
    """导出标注"""
    try:
        collection = store.client.get_collection(name=args.name)
    except Exception:
        console.print(f"\n❌ 错误：未找到集合：{args.name}")
        sys.exit(1)

    # 获取所有数据
    all_data = collection.get(include=["metadatas", "documents"])

    export_data = []
    for doc, meta in zip(all_data["documents"], all_data["metadatas"]):
        # 解析 metadata（扁平化转回嵌套）
        annotation = {}

        list_fields = ["scene_type", "emotion", "techniques", "key_elements", "usage"]
        for fld in list_fields:
            if fld in meta and meta[fld]:
                annotation[fld] = meta[fld].split(",") if meta[fld] else []

        scalar_fields = [
            "pace",
            "pov",
            "character_count",
            "power_level",
            "quality_score",
        ]
        for fld in scalar_fields:
            if fld in meta:
                annotation[fld] = meta[fld]

        # 转换质量分
        if "quality_score" in annotation:
            try:
                annotation["quality_score"] = int(annotation["quality_score"])
            except Exception:
                annotation["quality_score"] = 5

        export_data.append(
            {
                "original_text": doc,
                **annotation,
            }
        )

    # 选择输出格式
    if args.export == "json":
        output_path = args.output or f"annotations_{args.name}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

    elif args.export == "yaml":
        output_path = args.output or f"annotations_{args.name}.yaml"
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(
                export_data, f, ensure_ascii=False, indent=2, default_flow_style=False
            )

    console.print(f"\n✅ 标注导出到：{output_path}")
    console.print(f"   记录数：{len(export_data)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Corpus Builder - 语料库构建工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 构建语料库
  python3 scripts/build_corpus.py --source ./novels --name test --genre fantasy

  # 查看统计
  python3 scripts/build_corpus.py --stats --collection test

  # 导出标注
  python3 scripts/build_corpus.py --export json --collection test --output results.json
        """,
    )

    parser.add_argument("--source", "-s", type=str, help="源目录（包含 TXT 文件）")
    parser.add_argument("--name", "-n", type=str, help="语料库名称")
    parser.add_argument(
        "--collection",
        "-c",
        type=str,
        help="语料库名称（--name 的别名，用于 stats/export）",
    )
    parser.add_argument("--genre", "-g", type=str, help="题材类型")
    parser.add_argument(
        "--max-chunk-size", type=int, default=2000, help="最大块大小（默认 2000）"
    )
    parser.add_argument(
        "--min-chunk-size", type=int, default=100, help="最小块大小（默认 100）"
    )
    parser.add_argument("--overlap", type=int, default=200, help="块重叠（默认 200）")
    parser.add_argument(
        "--batch-size", type=int, default=5, help="AI 标注批量大小（默认 5）"
    )
    parser.add_argument("--stats", action="store_true", help="查看统计信息")
    parser.add_argument(
        "--export", type=str, choices=["json", "yaml"], help="导出标注格式"
    )
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--no-cache", action="store_true", help="禁用缓存")
    parser.add_argument("--checkpoint", type=str, help="断点文件路径")
    parser.add_argument(
        "--memory-limit", type=int, default=2500, help="内存限制（默认 2500 MB）"
    )
    parser.add_argument("--config", type=str, help="配置文件路径")

    args = parser.parse_args()

    # --collection 作为 --name 的别名
    if args.collection and not args.name:
        args.name = args.collection

    # 加载配置
    config = load_config(args.config)

    # 设置全局参数
    if args.name:
        config["storage"]["collection_name"] = args.name
    if args.genre:
        config["storage"]["genre"] = args.genre
    if args.memory_limit:
        config["memory"]["limit_mb"] = args.memory_limit

    # 验证必要参数
    if not args.source and not args.stats and not args.export:
        parser.print_help()
        console.print("\n❌ 错误：请指定 --source（构建）、--stats（统计）或 --export（导出）")
        sys.exit(1)

    # 初始化组件
    chunker = TextChunker(
        max_chunk_size=args.max_chunk_size,
        min_chunk_size=args.min_chunk_size,
        overlap=args.overlap,
    )
    extractor = FeatureExtractor()
    annotator = AIAnnotator()
    embedder = EmbeddingGenerator(config["models"]["embedding"])
    store = VectorStore(config["storage"]["persist_directory"])

    if args.source:
        # 构建语料库
        build_corpus(args, config, chunker, extractor, annotator, embedder, store)

    elif args.stats:
        # 查看统计
        show_stats(args, config)

    elif args.export:
        # 导出标注
        export_annotations(args, config, store)


if __name__ == "__main__":
    main()
