import sys
import argparse
import os
import hashlib
import json
import warnings
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
import pyperclip

# --- SILENCE EXTERNAL NOISE ---
# Suppress all library warnings (like requests, torch, etc.)
warnings.filterwarnings("ignore")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Ensure we can find the modules if we're running locally without installation
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import Config
from src.core.rag import RAGEngine
from src.core.enhancer import PromptEnhancer
from src.ml.context_evaluator import ContextEvaluator
from src.tools.context_gatherer import gather_all
from src.tools.github_cloner import clone_github_repo
from src.utils.logger import logger
from src.utils.paths import format_path, WorkspaceManager


def _get_rag_engine(args) -> RAGEngine:
    """Centralized RAGEngine initialization to remove redundancy."""
    workspace = WorkspaceManager.get_index_dir(getattr(args, 'project', None), getattr(args, 'github', None))
    return RAGEngine(workspace)

def handle_ask(args):
    prompt_text = " ".join(args.prompt)
    console = Console()
    
    github_url = args.github
    project_name = args.project
    
    if not github_url and not project_name:
        from tools.context_gatherer import gather_git_context
        git_ctx = gather_git_context()
        if git_ctx and git_ctx.get('remote_url'):
            remote = git_ctx['remote_url']
            if "github.com" in remote:
                github_url = remote
                console.print(f"[dim]Auto-detection: GitHub Repo found ({github_url})[/dim]")

    if github_url:
        try:
            repo_path = clone_github_repo(github_url)
            console.print(f"[dim]Using GitHub-Cache for Workspace.[/dim]")
            rag = _get_rag_engine(args)
            if rag.stats()['total_documents'] == 0:
                console.print(f"🔍 [yellow]First run for this repo. Indexing...[/yellow]")
                rag.index_directory(repo_path, recursive=True)
        except Exception as e:
            console.print(f"[bold red]Aborted: Could not load GitHub repo: {e}[/bold red]")
            return
    
    rag = _get_rag_engine(args)
    
    # Auto-indexing for local project if not skipped
    if not github_url and not project_name and not getattr(args, 'no_index', False):
        console.print("[dim]Checking for code changes (Incremental Indexing)...[/dim]")
        stats = rag.index_directory(Path.cwd(), recursive=True)
        if stats['indexed'] > 0:
            console.print(f"[dim]Updated index: {stats['indexed']} files changed.[/dim]")

    enhancer = PromptEnhancer(rag)
    
    console.print("[dim]Analyzing intent and gathering context...[/dim]")
    analysis = enhancer.intent_analyzer.analyze(prompt_text)
    system_context = gather_all()
    
    console.print(f"\n[cyan]Detected Intent:[/cyan] {analysis['intent']} ({analysis['confidence']:.0%})")
    
    gaps = enhancer.refiner.analyze_gaps(prompt_text, analysis['intent'], system_context)
    
    if gaps['inferred']:
        console.print("\n[green]Automatically detected (Context Inference):[/green]")
        for key, value in gaps['inferred'].items():
            console.print(f"  {key}: [dim]{value}[/dim]")
    
    console.print(f"\n[yellow]Prompt Completeness: {gaps['completeness']:.0%}[/yellow]")
    
    answers = {}
    if gaps['missing_critical']:
        console.print("\n[bold red]Critical Gaps (Missing important info):[/bold red]\n")
        for key, question in gaps['missing_critical']:
            suggestions = enhancer.refiner._generate_suggestions(key, gaps)
            hint = f" [dim](Suggestions: {', '.join(suggestions)})[/dim]" if suggestions else ""
            answer = Prompt.ask(f"  [bold]{question}[/bold]{hint}")
            if answer.strip():
                answers[key] = answer
    
    if gaps['missing_optional']:
        if Confirm.ask("\n[dim]Would you like to provide optional details?[/dim]", default=False):
            for key, question in gaps['missing_optional']:
                answer = Prompt.ask(f"  [bold]{question}[/bold]")
                if answer.strip():
                    answers[key] = answer
    
    refined_prompt = enhancer.refiner.refine_prompt(prompt_text, analysis['intent'], answers, system_context)
    console.print(Panel(refined_prompt, title="Refined Intermediate Prompt", border_style="cyan"))
    
    if Confirm.ask("\nShould this prompt be enriched by the RAG engine?", default=True):
        console.print("[dim]Searching and evaluating code contexts...[/dim]")
        
        pipeline_result = enhancer.run_evaluation_pipeline(
            query=refined_prompt,
            analysis=analysis,
            system_context=system_context,
            max_contexts=5,
            token_budget=4000
        )
        
        console.print("\n[bold]🔍 Context Selection Checklist:[/bold]")
        for log in pipeline_result['evaluation_log']:
            icon = "[green]✓[/green]" if log['relevant'] else "[red]✗[/red]"
            console.print(f"  {icon} [cyan]{log['name'][:25]:<25}[/cyan] [dim]{log['reason']}[/dim]")
            
        if not pipeline_result['selected_contexts']:
            console.print("[yellow]No highly relevant context hits passed the selection layer. Using base prompt.[/yellow]")
        
        enhanced_prompt = pipeline_result['enhanced_prompt']
        
        output_file = WorkspaceManager.get_prompt_output_file()
        output_file.write_text(enhanced_prompt)
        
        console.print(Panel(enhanced_prompt, title="✨ Final Enhanced Prompt", border_style="green"))
        
        try:
            pyperclip.copy(enhanced_prompt)
            clipboard_msg = "[bold green]✓[/bold green] Prompt automatically copied to clipboard!"
        except Exception:
            clipboard_msg = "[yellow]! Could not copy to clipboard automatically.[/yellow]"

        console.print(f"\n{clipboard_msg}")
        console.print(f"[dim]Saved at: [cyan]{format_path(str(output_file))}[/cyan][/dim]")

def handle_index(args):
    rag = _get_rag_engine(args)
    
    if args.github:
        repo_path = clone_github_repo(args.github)
        dir_to_index = repo_path
    else:
        dir_to_index = Path(args.dir).resolve()

    if not getattr(args, 'agent_mode', False):
        print(f"Indexing directory: {format_path(str(dir_to_index))} {'(recursive)' if args.recursive else ''}")
        
    stats = rag.index_directory(dir_to_index, recursive=args.recursive)
    
    if getattr(args, 'agent_mode', False):
        print(json.dumps({"status": "success", "stats": stats}))
    else:
        print(f"\n✓ Indexing completed. Newly indexed: {stats['indexed']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")
        index_stats = rag.stats()
        print(f"Current Index Status: {index_stats['total_documents']} documents, {index_stats['index_vectors']} vectors.")

def _estimate_line_numbers(full_content: str, chunk: str) -> dict:
    """Estimates start and end line numbers for a chunk within the full content."""
    if not full_content or not chunk:
        return {"start_line": None, "end_line": None}
        
    start_idx = full_content.find(chunk)
    if start_idx == -1:
        return {"start_line": None, "end_line": None}
        
    # Count newlines up to the start index to find the starting line (1-based)
    start_line = full_content.count('\n', 0, start_idx) + 1
    # Add the number of newlines in the chunk to get the end line
    end_line = start_line + chunk.count('\n')
    
    return {"start_line": start_line, "end_line": end_line}

def handle_search(args):
    rag = _get_rag_engine(args)
    
    # Dynamic Limit Logic
    query_words = len(args.query.split())
    target_limit = args.limit
    if getattr(args, 'agent_mode', False) and query_words > 5:
        target_limit = max(target_limit, 10) 
        
    # We fetch more than target_limit to allow filtering
    results = rag.search(args.query, k=target_limit * 3)
    
    if getattr(args, 'agent_mode', False):
        # --- NEW: Advanced Selection Layer ---
        evaluator = ContextEvaluator()
        # Filter for relevance and remove Trigram redundancy
        filtered_results = evaluator.evaluate_batch(args.query, results, max_overlap=0.4)
        
        # Take the best ones after deduplication
        results = filtered_results[:target_limit]
        
        clean_results = []
        for i, r in enumerate(results):
            content = r.get('full_content', r.get('content_preview', ''))
            preview = r.get('content_preview', '')
            lines = _estimate_line_numbers(content, preview)
            
            clean_results.append({
                "path": r['path'],
                "similarity": r['similarity'],
                "relevance_score": r.get('_relevance_score', 0.0),
                "relevance_type": r.get('_relevance_type', 'general'),
                "evaluation": r.get('_evaluation_reason', ''),
                "start_line": lines["start_line"],
                "end_line": lines["end_line"],
                "content": preview
            })
        print(json.dumps({"results": clean_results}))
        return

    console = Console()
    if not results:
        console.print("[yellow]No matching contexts found.[/yellow]")
        return

    # Trim to limit for human output
    results = results[:args.limit]
    for i, res in enumerate(results):
        console.print(f"\n[bold cyan][{i+1}] {res['name']}[/bold cyan] (Sim: {res['similarity']:.2f})")
        console.print(f"[dim]{format_path(res['path'])}[/dim]")
        content = res.get('full_content', res.get('content_preview', ''))
        console.print(Panel(content[:1000] + ("..." if len(content) > 1000 else ""), border_style="dim"))

def handle_ctx(args):
    if getattr(args, 'agent_mode', False):
        from src.tools.context_gatherer import gather_all
        print(json.dumps(gather_all()))
    else:
        from tools.context_gatherer import main
        main()


def handle_harvest(args):
    rag = _get_rag_engine(args)
    
    if not args.no_index and not args.github and not args.project:
        rag.index_directory(Path.cwd(), recursive=True)
        
    enhancer = PromptEnhancer(rag)
    query = " ".join(args.keywords)
    
    if getattr(args, 'semantic', False):
        results = rag.search(query, k=args.limit)
        
        if getattr(args, 'agent_mode', False):
            print(json.dumps({"intent": "semantic_search", "results": results}))
            return
            
        print("<!-- CXM HARVEST START -->")
        print(f"<harvest_intent>semantic_search</harvest_intent>")
        if not results:
            print("<harvest_warning>No matching context found.</harvest_warning>")
        
        for doc in results:
            doc_path = format_path(doc['path'])
            print(f"\n<file_context path=\"{doc_path}\">")
            content = doc.get('content_preview', doc.get('full_content', ''))
            import re
            content = re.sub(r'\n\s*\n', '\n\n', content.strip())
            print(content)
            print("</file_context>")
        print("<!-- CXM HARVEST END -->")
        return

    intent_override = args.intent
    analysis = enhancer.intent_analyzer.analyze(query)
    if intent_override:
        analysis['intent'] = intent_override
    
    pipeline_result = enhancer.run_evaluation_pipeline(
        query=query,
        analysis=analysis,
        max_contexts=args.limit,
        token_budget=12000
    )
    
    selected = pipeline_result['selected_contexts']
            
    if getattr(args, 'agent_mode', False):
        print(json.dumps({"intent": analysis['intent'], "results": selected}))
        return

    print("<!-- CXM HARVEST START -->")
    print(f"<harvest_intent>{analysis['intent']}</harvest_intent>")
    if not selected:
        print("<harvest_warning>No matching context found.</harvest_warning>")
    
    for doc in selected:
        doc_path = format_path(doc['path'])
        print(f"\n<file_context path=\"{doc_path}\">")
        content = doc.get('content_preview', doc.get('full_content', ''))
        import re
        content = re.sub(r'\n\s*\n', '\n\n', content.strip())
        print(content)
        print("</file_context>")
    print("<!-- CXM HARVEST END -->")


def handle_watch(args):
    from core.watcher import start_watcher
    start_watcher(args.project, args.github)

def handle_map(args):
    from core.grapher import DependencyGrapher
    target = args.target if args.target else "."
    grapher = DependencyGrapher(Path.cwd())
    graph = grapher.build_graph(target)
    print(json.dumps(graph, indent=2))

def handle_ingest(args):
    rag = _get_rag_engine(args)
    dir_to_index = Path(args.dir).resolve()
    
    if not getattr(args, 'agent_mode', False):
        print(f"Ingesting non-code and config files in: {format_path(str(dir_to_index))}")
        
    stats = rag.index_directory(dir_to_index, recursive=True, force=False, is_ingest=True)
    
    if getattr(args, 'agent_mode', False):
        print(json.dumps({"status": "success", "stats": stats}))
    else:
        print(f"\n✓ Ingestion completed. Indexed: {stats['indexed']}, Skipped: {stats['skipped']}")

def main():
    parser = argparse.ArgumentParser(description="CXM (ContextMachine) CLI - Your AI Partner Orchestrator")
    parser.add_argument("-p", "--project", type=str, help="Specify project name")
    parser.add_argument("-g", "--github", type=str, help="GitHub repository URL")
    parser.add_argument("--agent-mode", action="store_true", help="Output pure JSON for Agent Skills")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # ask
    ask_parser = subparsers.add_parser("ask", help="Create an enhanced RAG prompt")
    ask_parser.add_argument("prompt", nargs="+", help="The initial prompt")
    ask_parser.add_argument("--no-index", action="store_true", help="Skip automatic incremental indexing")
    
    # index
    index_parser = subparsers.add_parser("index", help="Index a directory")
    index_parser.add_argument("dir", type=str, default=".", nargs="?", help="Directory to index")
    index_parser.add_argument("--recursive", action="store_true", default=True)
    index_parser.add_argument("-g", "--github", type=str)
    
    # search
    search_parser = subparsers.add_parser("search", help="Search the knowledge base")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--limit", type=int, default=5)
    
    # harvest
    harvest_parser = subparsers.add_parser("harvest", help="Non-interactive context harvesting for agents")
    harvest_parser.add_argument("keywords", nargs="+", help="Keywords or target files")
    harvest_parser.add_argument("--intent", type=str, help="Override intent (e.g. Feature, Bugfix)")
    harvest_parser.add_argument("--format", type=str, default="xml", help="Output format")
    harvest_parser.add_argument("--limit", type=int, default=5, help="Number of files to retrieve")
    harvest_parser.add_argument("--no-index", action="store_true", help="Skip incremental indexing")
    harvest_parser.add_argument("--semantic", action="store_true", help="Pure semantic vector search directly")

    # watch
    watch_parser = subparsers.add_parser("watch", help="Background daemon to keep RAG index updated")

    # map
    map_parser = subparsers.add_parser("map", help="Generate an AST dependency graph")
    map_parser.add_argument("target", type=str, nargs="?", help="Target file or module to map")

    # ingest
    ingest_parser = subparsers.add_parser("ingest", help="Ingest non-code files (docs, configs)")
    ingest_parser.add_argument("dir", type=str, default=".", nargs="?", help="Directory to ingest")

    # ctx
    subparsers.add_parser("ctx", help="Print current system context")
    
    args = parser.parse_args()
    
    if args.command == "ask":
        handle_ask(args)
    elif args.command == "index":
        handle_index(args)
    elif args.command == "search":
        handle_search(args)
    elif args.command == "harvest":
        handle_harvest(args)
    elif args.command == "watch":
        handle_watch(args)
    elif args.command == "map":
        handle_map(args)
    elif args.command == "ingest":
        handle_ingest(args)
    elif args.command == "ctx":
        handle_ctx(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
