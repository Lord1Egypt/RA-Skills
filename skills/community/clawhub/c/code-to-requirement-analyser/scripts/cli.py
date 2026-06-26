#!/usr/bin/env python3
"""
交易代码分析器 CLI v2.1
统一命令行入口 - 支持缓存和错误恢复
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入解析器（支持可选导入）
from parser.vue_parser import VueParser
from parser.base import CacheManager

try:
    from parser.react_parser import ReactParser
except ImportError as e:
    print(f"⚠️  ReactParser 导入警告: {e}", file=sys.stderr)
    ReactParser = None

try:
    from parser.angular_parser import AngularParser
except ImportError as e:
    print(f"⚠️  AngularParser 导入警告: {e}", file=sys.stderr)
    AngularParser = None

from analyzer.business_analyzer import TradeBusinessAnalyzer
from knowledge.builder import KnowledgeGraphBuilder


def main():
    parser = argparse.ArgumentParser(
        description="交易代码分析器 v2.1 - 智能分析交易维度前端代码",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 解析 Vue 文件
  python3 scripts/cli.py parse ./src/views/Order.vue
  
  # 解析 React 文件（跳过缓存）
  python3 scripts/cli.py parse ./src/views/Order.tsx --no-cache
  
  # 完整分析并保存到知识库
  python3 scripts/cli.py full ./src/views/Order.vue --save-knowledge
  
  # 搜索知识库
  python3 scripts/cli.py knowledge --search "基金"
  
  # 管理缓存
  python3 scripts/cli.py cache --stats
  python3 scripts/cli.py cache --clear
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 解析命令
    parse_parser = subparsers.add_parser("parse", help="解析代码文件")
    parse_parser.add_argument("file", help="代码文件路径")
    parse_parser.add_argument(
        "--type", 
        choices=["vue", "react", "angular"], 
        help="强制指定类型（默认自动检测）"
    )
    parse_parser.add_argument(
        "-o", "--output", 
        help="输出JSON文件路径（默认输出到控制台）"
    )
    parse_parser.add_argument(
        "--no-cache",
        action="store_true",
        help="禁用缓存（强制重新解析）"
    )
    
    # 分析命令
    analyze_parser = subparsers.add_parser("analyze", help="分析业务需求")
    analyze_parser.add_argument("parsed_file", help="解析结果JSON文件路径")
    analyze_parser.add_argument(
        "-o", "--output", 
        help="输出分析结果JSON路径"
    )
    
    # 知识库命令
    kb_parser = subparsers.add_parser("knowledge", help="知识库操作")
    kb_parser.add_argument("--add", help="添加分析结果到知识库（指定JSON文件）")
    kb_parser.add_argument("--search", help="按标签搜索知识库")
    kb_parser.add_argument("--related", help="查找关联知识（指定知识ID）")
    kb_parser.add_argument(
        "--base-path", 
        default="~/.openclaw/knowledge/trade/",
        help="知识库根目录"
    )
    
    # 缓存管理命令
    cache_parser = subparsers.add_parser("cache", help="缓存管理")
    cache_parser.add_argument(
        "--stats",
        action="store_true",
        help="显示缓存统计信息"
    )
    cache_parser.add_argument(
        "--clear",
        action="store_true",
        help="清除所有缓存"
    )
    cache_parser.add_argument(
        "--dir",
        default="~/.openclaw/cache/trade-analyzer/",
        help="缓存目录"
    )
    
    # 完整流程命令
    full_parser = subparsers.add_parser("full", help="执行完整分析流程（推荐）")
    full_parser.add_argument("file", help="代码文件路径")
    full_parser.add_argument(
        "--save-knowledge", 
        action="store_true",
        help="保存分析结果到知识库"
    )
    full_parser.add_argument(
        "--generate-report", 
        help="生成Markdown报告的文件路径"
    )
    full_parser.add_argument(
        "--output-dir",
        default="~/trade-analysis-reports/",
        help="报告输出目录"
    )
    full_parser.add_argument(
        "--no-cache",
        action="store_true",
        help="禁用缓存"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "parse":
            result = cmd_parse(args)
        elif args.command == "analyze":
            result = cmd_analyze(args)
        elif args.command == "knowledge":
            result = cmd_knowledge(args)
        elif args.command == "cache":
            result = cmd_cache(args)
        elif args.command == "full":
            result = cmd_full(args)
        else:
            parser.print_help()
            sys.exit(1)
        
        # 美化输出
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def cmd_parse(args):
    """解析命令（带缓存支持）"""
    file_path = Path(args.file).expanduser().resolve()
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 自动检测类型
    ext = file_path.suffix.lower()
    file_type = args.type
    
    if not file_type:
        if ext == '.vue':
            file_type = 'vue'
        elif ext in ['.jsx', '.tsx', '.js', '.ts']:
            file_type = 'react'
        elif ext in ['.component.html', '.component.ts']:
            file_type = 'angular'
        else:
            raise ValueError(f"无法自动识别文件类型: {ext}，请使用 --type 指定")
    
    # 选择解析器
    use_cache = not args.no_cache
    if file_type == 'vue':
        parser = VueParser(str(file_path), use_cache=use_cache)
        result = parser.parse_with_cache() if use_cache else parser.parse()
    elif file_type == 'react':
        if ReactParser is None:
            raise NotImplementedError("React 解析器未正确导入")
        parser = ReactParser(str(file_path), use_cache=use_cache)
        result = parser.parse_with_cache() if use_cache else parser.parse()
    elif file_type == 'angular':
        if AngularParser is None:
            raise NotImplementedError("Angular 解析器未正确导入")
        parser = AngularParser(str(file_path), use_cache=use_cache)
        result = parser.parse_with_cache() if use_cache else parser.parse()
    else:
        raise ValueError(f"不支持的类型: {file_type}")
    
    # 添加解析元数据
    result["_parse_metadata"] = {
        "timestamp": datetime.now().isoformat(),
        "parser_type": file_type,
        "cache_used": result.get("_from_cache", False),
        "cache_hit": result.get("_cache_hit", False)
    }
    
    # 移除内部缓存标记
    result.pop("_from_cache", None)
    result.pop("_cache_hit", None)
    
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✓ 解析结果已保存: {output_path}", file=sys.stderr)
    
    return result


def cmd_analyze(args):
    """分析命令"""
    parsed_file = Path(args.parsed_file).expanduser()
    
    if not parsed_file.exists():
        raise FileNotFoundError(f"文件不存在: {parsed_file}")
    
    with open(parsed_file, 'r', encoding='utf-8') as f:
        parsed_data = json.load(f)
    
    analyzer = TradeBusinessAnalyzer()
    result = analyzer.analyze(parsed_data)
    
    # 添加分析元数据
    result["_analysis_metadata"] = {
        "timestamp": datetime.now().isoformat(),
        "source_file": str(parsed_file),
        "analyzer_version": "2.1.0"
    }
    
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✓ 分析结果已保存: {output_path}", file=sys.stderr)
    
    return result


def cmd_knowledge(args):
    """知识库命令"""
    base_path = Path(args.base_path).expanduser()
    builder = KnowledgeGraphBuilder(str(base_path))
    
    if args.add:
        add_file = Path(args.add).expanduser()
        if not add_file.exists():
            raise FileNotFoundError(f"文件不存在: {add_file}")
        
        with open(add_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        
        node, edges = builder.add_knowledge(analysis, str(add_file))
        return {
            "success": True,
            "knowledge_id": node.id,
            "title": node.title,
            "relationships_created": len(edges),
            "tags": node.tags
        }
    
    elif args.search:
        results = builder.search({"tags": [args.search]})
        return {
            "query": args.search,
            "results_count": len(results),
            "results": [
                {
                    "id": r.get("id"),
                    "title": r.get("title"),
                    "dimension": r.get("trade_dimension", {})
                }
                for r in results[:10]
            ]
        }
    
    elif args.related:
        related = builder.get_related_knowledge(args.related)
        return {
            "source_id": args.related,
            "related_count": len(related),
            "related_knowledge": [
                {
                    "id": r.get("id"),
                    "title": r.get("title"),
                    "relation_type": r.get("relation", {}).get("relation_type"),
                    "strength": r.get("relation", {}).get("strength")
                }
                for r in related
            ]
        }
    
    else:
        # 返回索引概览
        return {
            "knowledge_base_path": str(base_path),
            "total_entries": len(builder.index.get("nodes", {})),
            "last_updated": builder.index.get("last_updated"),
            "tags": list(builder.index.get("tags", {}).keys())[:20]
        }


def cmd_cache(args):
    """缓存管理命令"""
    cache_manager = CacheManager(args.dir)
    
    if args.clear:
        success = cache_manager.clear_cache()
        return {
            "action": "clear_cache",
            "success": success,
            "cache_dir": str(cache_manager.cache_dir)
        }
    
    elif args.stats:
        stats = cache_manager.get_cache_stats()
        return {
            "action": "cache_stats",
            **stats
        }
    
    else:
        # 默认显示统计
        stats = cache_manager.get_cache_stats()
        return {
            "action": "cache_info",
            **stats,
            "help": "使用 --stats 查看详情，--clear 清除缓存"
        }


def cmd_full(args):
    """完整流程命令（带缓存支持）"""
    file_path = Path(args.file).expanduser().resolve()
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    use_cache = not args.no_cache
    print(f"🔍 开始分析: {file_path.name}", file=sys.stderr)
    print(f"   缓存模式: {'启用' if use_cache else '禁用'}", file=sys.stderr)
    
    # 1. 解析
    print("  1/4 解析代码结构...", file=sys.stderr)
    ext = file_path.suffix.lower()
    
    try:
        if ext == '.vue':
            parser = VueParser(str(file_path), use_cache=use_cache)
            parsed = parser.parse_with_cache() if use_cache else parser.parse()
        elif ext in ['.jsx', '.tsx']:
            if ReactParser is None:
                raise NotImplementedError("React 解析器未正确导入")
            parser = ReactParser(str(file_path), use_cache=use_cache)
            parsed = parser.parse_with_cache() if use_cache else parser.parse()
        elif ext in ['.component.ts', '.component.html']:
            if AngularParser is None:
                raise NotImplementedError("Angular 解析器未正确导入")
            parser = AngularParser(str(file_path), use_cache=use_cache)
            parsed = parser.parse_with_cache() if use_cache else parser.parse()
        else:
            raise ValueError(f"暂不支持: {ext}")
        
        # 检查是否来自缓存
        from_cache = parsed.get("_from_cache", False)
        if from_cache:
            print(f"     ⚡ 命中缓存，跳过解析", file=sys.stderr)
        
        comp_count = len(parsed.get('components', []))
        api_count = len(parsed.get('apis', []))
        print(f"     ✓ 识别组件: {comp_count} 个", file=sys.stderr)
        print(f"     ✓ 识别 API: {api_count} 个", file=sys.stderr)
        
    except Exception as e:
        print(f"     ❌ 解析失败: {e}", file=sys.stderr)
        raise
    
    # 2. 分析
    print("  2/4 推导业务需求...", file=sys.stderr)
    try:
        analyzer = TradeBusinessAnalyzer()
        analyzed = analyzer.analyze(parsed)
        dimension = analyzed.get("trade_dimension", {})
        trade_types = dimension.get("trade_type", ['未知'])
        lifecycles = dimension.get("lifecycle", ['未知'])
        req_count = len(analyzed.get("functional_requirements", []))
        print(f"     ✓ 交易类型: {', '.join(trade_types)}", file=sys.stderr)
        print(f"     ✓ 生命周期: {', '.join(lifecycles)}", file=sys.stderr)
        print(f"     ✓ 功能需求: {req_count} 项", file=sys.stderr)
    except Exception as e:
        print(f"     ❌ 分析失败: {e}", file=sys.stderr)
        raise
    
    # 3. 保存到知识库（可选）
    knowledge_id = None
    if args.save_knowledge:
        print("  3/4 沉淀到知识库...", file=sys.stderr)
        try:
            base_path = Path(args.output_dir).expanduser().parent / "knowledge" / "trade"
            base_path.mkdir(parents=True, exist_ok=True)
            
            builder = KnowledgeGraphBuilder(str(base_path))
            node, edges = builder.add_knowledge(analyzed, str(file_path))
            knowledge_id = node.id
            edge_count = len(edges)
            print(f"     ✓ 知识ID: {knowledge_id}", file=sys.stderr)
            print(f"     ✓ 关联知识: {edge_count} 条", file=sys.stderr)
        except Exception as e:
            print(f"     ⚠️ 知识库保存失败: {e}", file=sys.stderr)
    else:
        print("  3/4 跳过知识库保存（使用 --save-knowledge 启用）", file=sys.stderr)
    
    # 4. 生成报告（可选）
    if args.generate_report:
        print("  4/4 生成分析报告...", file=sys.stderr)
        try:
            report_path = Path(args.generate_report).expanduser()
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            report = generate_markdown_report(analyzed, str(file_path))
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"     ✓ 报告已保存: {report_path}", file=sys.stderr)
        except Exception as e:
            print(f"     ⚠️ 报告生成失败: {e}", file=sys.stderr)
    else:
        print("  4/4 跳过报告生成（使用 --generate-report 启用）", file=sys.stderr)
    
    # 返回摘要
    confidence = analyzed.get("analysis_confidence", {}).get("overall", 0)
    return {
        "success": True,
        "file": str(file_path),
        "analysis_summary": {
            "trade_type": trade_types[0] if trade_types else "未知",
            "lifecycle": lifecycles,
            "requirements_count": req_count,
            "rules_count": len(analyzed.get("business_rules", [])),
            "confidence": confidence
        },
        "cache_info": {
            "used": use_cache,
            "hit": from_cache if use_cache else False
        },
        "knowledge_id": knowledge_id,
        "suggestions": analyzed.get("suggestions", [])[:3]
    }


def generate_markdown_report(analysis, source_file):
    """生成 Markdown 分析报告"""
    lines = [
        f"# {analysis.get('trade_dimension', {}).get('trade_type', ['交易'])[0]}业务需求分析报告",
        "",
        "## 📊 分析概览",
        f"- **源文件**: `{source_file}`",
        f"- **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **整体置信度**: {analysis.get('analysis_confidence', {}).get('overall', 0):.1%}",
        "",
        "## 🎯 交易维度识别",
    ]
    
    dim = analysis.get("trade_dimension", {})
    lines.extend([
        f"- **交易类型**: {', '.join(dim.get('trade_type', ['未识别']))}",
        f"- **生命周期**: {', '.join(dim.get('lifecycle', ['未识别']))}",
        f"- **产品类型**: {', '.join(dim.get('product_type', ['未指定']))}",
        f"- **交易渠道**: {', '.join(dim.get('channel', ['未指定']))}",
        f"- **参与方**: {', '.join(dim.get('parties', ['客户']))}",
        "",
        "## 📋 功能需求清单",
        "",
        "| ID | 功能名称 | 优先级 | 业务场景 |",
        "|----|---------|--------|---------|"
    ])
    
    for req in analysis.get("functional_requirements", []):
        scenario = req.get('scenario', '')
        if len(scenario) > 25:
            scenario = scenario[:25] + '...'
        lines.append(f"| {req.get('id', '-')} | {req.get('name', '-')} | {req.get('priority', '-')} | {scenario} |")
    
    lines.extend([
        "",
        "## ⚖️ 业务规则",
        ""
    ])
    
    rules = analysis.get("business_rules", [])
    for rule in rules[:10]:
        lines.extend([
            f"### {rule.get('id', 'BR-xxx')}: {rule.get('name', '未命名规则')}",
            f"- **类型**: `{rule.get('rule_type', 'unknown')}`",
            f"- **级别**: {rule.get('severity', 'info')}",
            f"- **描述**: {rule.get('description', '暂无描述')}",
            ""
        ])
    
    if len(rules) > 10:
        remaining = len(rules) - 10
        lines.append(f"*... 还有 {remaining} 条规则未显示*")
        lines.append("")
    
    lines.extend([
        "## 💡 优化建议",
        ""
    ])
    
    suggestions = analysis.get("suggestions", [])
    if suggestions:
        for suggestion in suggestions:
            lines.append(f"- {suggestion}")
    else:
        lines.append("- 暂无优化建议")
    
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
