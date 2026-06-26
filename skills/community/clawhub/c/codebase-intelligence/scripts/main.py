#!/usr/bin/env python3
"""
Codebase Intelligence - Main Entry Point

Enhanced version with caching and smart Q&A.
Usage: python3 main.py <command> [options]
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent


def run_analyze(args):
    """Run the analyze command using indexer"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from indexer import Indexer
    
    indexer = Indexer(args.path, args.cache_dir)
    
    if args.stats:
        # Build index and show stats
        indexer.build_index(max_files=args.max_files)
        stats = indexer.get_stats()
        
        print(f"\n📊 Codebase Analysis Report")
        print(f"{'='*50}")
        print(f"Root Directory: {stats['root']}")
        print(f"Generated: {__import__('datetime').datetime.now().isoformat()}")
        print(f"\n## Overview")
        print(f"- **Total Files**: {stats['total_files']}")
        print(f"- **Total Lines**: {stats['total_lines']:,}")
        print(f"- **Total Modules**: {stats['total_modules']}")
        print(f"- **Total Functions**: {stats['total_functions']}")
        print(f"- **Total Classes**: {stats['total_classes']}")
        
        print(f"\n## Languages")
        print("")
        print("| Language | Files | Lines |")
        print("|----------|-------|-------|")
        
        for lang, data in sorted(stats['languages'].items(), 
                                 key=lambda x: x[1]['lines'], reverse=True):
            print(f"| {lang} | {data['files']} | {data['lines']:,} |")
        print("")
        
        # Show module structure
        index = indexer.get_index()
        if index:
            print("## Module Structure")
            print("```")
            for module in sorted(index.modules.keys()):
                file_count = len(index.modules[module])
                print(f"📁 {module}/ ({file_count} files)")
            print("```")
    
    elif args.search:
        # Search for files
        indexer.build_index(max_files=args.max_files)
        results = indexer.search(args.search, limit=args.limit or 20)
        
        print(f"\n🔍 Search results for '{args.search}':")
        print(f"{'='*50}")
        for file_path, score in results:
            print(f"  {score:6.1f}  {file_path}")
    
    elif args.symbol:
        # Find symbol
        indexer.build_index(max_files=args.max_files)
        results = indexer.find_symbol(args.symbol, args.symbol_type)
        
        print(f"\n🔍 Symbol '{args.symbol}' found in:")
        print(f"{'='*50}")
        for file_path in results:
            print(f"  • {file_path}")
    
    else:
        # Default: show stats
        indexer.build_index(max_files=args.max_files)
        stats = indexer.get_stats()
        
        print(f"\n✅ Codebase indexed successfully!")
        print(f"   Files: {stats['total_files']}")
        print(f"   Lines: {stats['total_lines']:,}")
        print(f"   Functions: {stats['total_functions']}")
        print(f"   Classes: {stats['total_classes']}")
        print(f"\n   Use --stats for detailed report")
        print(f"   Use --search <query> to find files")
        print(f"   Use --symbol <name> to find symbols")


def run_deps(args):
    """Run the deps command"""
    cmd = [sys.executable, str(SCRIPT_DIR / 'deps.py'), args.target]
    if args.root:
        cmd.extend(['--root', args.root])
    if args.reverse:
        cmd.append('--reverse')
    if args.depth:
        cmd.extend(['--depth', str(args.depth)])
    if args.format:
        cmd.extend(['--format', args.format])
    if args.output:
        cmd.extend(['--output', args.output])
    subprocess.run(cmd)


def run_ask(args):
    """Run the enhanced ask command"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from ask_v2 import SmartQuestionAnswering
    
    question = ' '.join(args.question)
    qa = SmartQuestionAnswering(args.root)
    result = qa.answer(question, use_llm=not args.no_llm, context_files=args.context)
    
    print(qa.format_answer(result, args.format))


def run_diagram(args):
    """Run the diagram command"""
    cmd = [sys.executable, str(SCRIPT_DIR / 'diagram.py')]
    if args.root:
        cmd.extend(['--root', args.root])
    if args.format:
        cmd.extend(['--format', args.format])
    if args.output:
        cmd.extend(['--output', args.output])
    if args.max_nodes:
        cmd.extend(['--max-nodes', str(args.max_nodes)])
    if args.entry_points:
        cmd.extend(['--entry-points'] + args.entry_points)
    subprocess.run(cmd)


def run_index(args):
    """Build or update the codebase index"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from indexer import Indexer
    
    indexer = Indexer(args.path, args.cache_dir)
    
    if args.watch:
        print("👀 Watch mode not yet implemented")
        print("   For now, re-run this command to update the index")
        return
    
    index = indexer.build_index(max_files=args.max_files)
    
    if args.export:
        # Export index to JSON
        import json
        export_path = Path(args.export)
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(index.to_dict(), f, indent=2, default=str)
        print(f"\n💾 Index exported to: {export_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Codebase Intelligence - Analyze and understand your codebase',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py analyze                          # Index and show stats
  python3 main.py analyze --stats                  # Detailed report
  python3 main.py analyze --search "auth"          # Search for files
  python3 main.py analyze --symbol "User"          # Find symbol definition
  
  python3 main.py ask "How does auth work?"        # Smart Q&A
  python3 main.py ask "Where is the database code?"
  
  python3 main.py deps src/main.py                 # Show dependencies
  python3 main.py deps src/utils.py --reverse      # Reverse dependencies
  
  python3 main.py diagram                          # Generate diagram
  python3 main.py diagram --format mermaid-flow
  
  python3 main.py index                            # Build/update index
  python3 main.py index --export index.json        # Export to JSON
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # analyze command (enhanced with indexer)
    analyze_parser = subparsers.add_parser('analyze', help='Analyze codebase structure')
    analyze_parser.add_argument('path', nargs='?', default='.', help='Path to analyze')
    analyze_parser.add_argument('--stats', '-s', action='store_true',
                                help='Show detailed statistics')
    analyze_parser.add_argument('--search', help='Search for files matching query')
    analyze_parser.add_argument('--symbol', help='Find symbol definition')
    analyze_parser.add_argument('--symbol-type', choices=['func', 'class'],
                               help='Symbol type filter')
    analyze_parser.add_argument('--limit', '-l', type=int, default=20,
                               help='Limit search results')
    analyze_parser.add_argument('--max-files', type=int, default=5000,
                                help='Maximum files to analyze')
    analyze_parser.add_argument('--cache-dir', help='Cache directory')
    analyze_parser.add_argument('--format', '-f', choices=['md', 'json'], default='md',
                                help='Output format')
    analyze_parser.set_defaults(func=run_analyze)
    
    # deps command
    deps_parser = subparsers.add_parser('deps', help='Analyze dependencies')
    deps_parser.add_argument('target', help='File or module to analyze')
    deps_parser.add_argument('--root', '-r', default='.', help='Project root')
    deps_parser.add_argument('--reverse', '-R', action='store_true',
                            help='Show reverse dependencies')
    deps_parser.add_argument('--depth', '-d', type=int, default=2,
                            help='Dependency depth')
    deps_parser.add_argument('--format', '-f', choices=['md', 'json', 'mermaid'],
                            default='md', help='Output format')
    deps_parser.add_argument('--output', '-o', help='Output file')
    deps_parser.set_defaults(func=run_deps)
    
    # ask command (enhanced)
    ask_parser = subparsers.add_parser('ask', help='Ask questions about codebase')
    ask_parser.add_argument('question', nargs='+', help='Question to ask')
    ask_parser.add_argument('--root', '-r', default='.', help='Project root')
    ask_parser.add_argument('--context', '-c', type=int, default=10,
                           help='Number of context files')
    ask_parser.add_argument('--format', '-f', choices=['md', 'json'], default='md',
                           help='Output format')
    ask_parser.add_argument('--no-llm', action='store_true',
                           help='Use local search only (no LLM)')
    ask_parser.set_defaults(func=run_ask)
    
    # diagram command
    diagram_parser = subparsers.add_parser('diagram', help='Generate architecture diagrams')
    diagram_parser.add_argument('--root', '-r', default='.', help='Project root')
    diagram_parser.add_argument('--format', '-f',
                                choices=['mermaid', 'mermaid-flow', 'mermaid-component', 'dot'],
                                default='mermaid', help='Diagram format')
    diagram_parser.add_argument('--output', '-o', help='Output file')
    diagram_parser.add_argument('--max-nodes', '-n', type=int, default=30,
                               help='Maximum nodes')
    diagram_parser.add_argument('--entry-points', '-e', nargs='+',
                               help='Entry points for flow diagram')
    diagram_parser.set_defaults(func=run_diagram)
    
    # index command
    index_parser = subparsers.add_parser('index', help='Build or update codebase index')
    index_parser.add_argument('path', nargs='?', default='.', help='Path to index')
    index_parser.add_argument('--cache-dir', help='Cache directory')
    index_parser.add_argument('--max-files', type=int, default=5000,
                             help='Maximum files to index')
    index_parser.add_argument('--watch', '-w', action='store_true',
                             help='Watch for changes (not implemented)')
    index_parser.add_argument('--export', '-e', help='Export index to JSON file')
    index_parser.set_defaults(func=run_index)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
