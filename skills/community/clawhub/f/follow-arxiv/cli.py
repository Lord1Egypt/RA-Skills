#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arxiv Paper Processing CLI Tool

A command-line tool that encapsulates all operations for the Arxiv paper skill.
All commands output JSON for easy parsing by agents.

Usage:
    python cli.py <command> [arguments]
"""

import sys
import json
import argparse
import os
import tempfile
import shutil
from typing import Dict, Any

# Set UTF-8 encoding for output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add src to path
sys.path.insert(0, 'src')

from utils import (
    get_config_path, get_config_dir, load_config, save_config,
    get_default_config, get_prompts_dir, load_prompt, save_prompt
)


def output_json(data: Dict[str, Any]) -> None:
    """Output data as JSON to stdout"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def output_error(message: str, error_code: int = 1) -> None:
    """Output error as JSON and exit"""
    output_json({"error": message, "success": False})
    sys.exit(error_code)


# ============================================================================
# Onboarding Commands
# ============================================================================

def check_onboarding() -> None:
    """Check if onboarding is complete"""
    config_path = get_config_path()

    if not config_path:
        output_json({
            "complete": False,
            "reason": "Config path not found"
        })
        return

    try:
        config = load_config()
        complete = config.get('onboarding_complete', False)
        output_json({
            "complete": complete,
            "config_exists": True
        })
    except Exception as e:
        output_json({
            "complete": False,
            "reason": str(e)
        })


def check_dependencies() -> None:
    """Check if required dependencies are installed"""
    missing = []

    try:
        import arxiv
    except ImportError:
        missing.append("arxiv")

    try:
        import fitz
    except ImportError:
        missing.append("pymupdf")

    try:
        import requests
    except ImportError:
        missing.append("requests")

    output_json({
        "ok": len(missing) == 0,
        "missing": missing,
        "all_installed": ["arxiv", "pymupdf", "requests"]
    })


def complete_onboarding(language: str = "zh", time_window: int = 24,
                       query: str = "AI Agent") -> None:
    """Complete onboarding and save initial config"""
    config = get_default_config()
    config.update({
        "language": language,
        "time_window_hours": time_window,
        "default_query": query,
        "onboarding_complete": True
    })

    try:
        save_config(config)
        output_json({
            "success": True,
            "config": config
        })
    except Exception as e:
        output_error(f"Failed to save config: {e}")


# ============================================================================
# Config Management Commands
# ============================================================================

def get_config() -> None:
    """Get current configuration"""
    try:
        config = load_config()
        output_json({
            "success": True,
            "config": config
        })
    except Exception as e:
        output_error(f"Failed to load config: {e}")


def set_config(key: str, value: str) -> None:
    """Set a single configuration value"""
    try:
        config = load_config()

        # Try to parse value as JSON, fallback to string
        try:
            parsed_value = json.loads(value)
        except (json.JSONDecodeError, ValueError):
            parsed_value = value

        config[key] = parsed_value
        save_config(config)

        output_json({
            "success": True,
            "key": key,
            "value": parsed_value
        })
    except Exception as e:
        output_error(f"Failed to set config: {e}")


def reset_config() -> None:
    """Reset configuration to defaults"""
    try:
        config = get_default_config()
        # Don't reset onboarding_complete if it was True
        old_config = load_config()
        if old_config.get('onboarding_complete', False):
            config['onboarding_complete'] = True

        save_config(config)

        output_json({
            "success": True,
            "config": config
        })
    except Exception as e:
        output_error(f"Failed to reset config: {e}")


# ============================================================================
# Search and Processing Commands
# ============================================================================

def search_papers(query: str = None, max_results: int = None,
                 time_window: int = None) -> None:
    """Search arxiv papers using current config"""
    try:
        from search import search_arxiv_papers

        # Load config for defaults
        config = load_config()

        papers = search_arxiv_papers(
            query=query or config.get('default_query'),
            max_results=max_results or config.get('max_results'),
            time_window_hours=time_window or config.get('time_window_hours'),
            config=config
        )

        output_json({
            "success": True,
            "papers": papers,
            "count": len(papers),
            "query_used": query or config.get('default_query')
        })
    except Exception as e:
        output_error(f"Failed to search papers: {e}")


def process_pdf(arxiv_id: str) -> None:
    """Download and process PDF for a paper"""
    try:
        from search import search_arxiv_papers
        from pdf_processor import process_pdf

        # First find the paper
        papers = search_arxiv_papers(query=f"id:{arxiv_id}", max_results=1)

        if not papers:
            output_error(f"Paper {arxiv_id} not found")

        paper = papers[0]
        result = process_pdf(paper)

        output_json({
            "success": True,
            "paper": result,
            "arxiv_id": arxiv_id
        })
    except Exception as e:
        output_error(f"Failed to process PDF: {e}")


def prepare_daily() -> None:
    """
    Prepare daily summary - combines search and prompt preparation.
    This is a single-command replacement for the multi-step process.

    Saves the JSON result to a temporary file in the project directory
    and returns the file path for stable reading by agents.
    """
    try:
        from search import search_arxiv_papers
        from analyzer import prepare_summary

        # Load config
        config = load_config()

        # Search papers
        papers = search_arxiv_papers(
            query=config.get('default_query'),
            max_results=config.get('max_results'),
            time_window_hours=config.get('time_window_hours'),
            config=config
        )

        # Prepare summary context
        result = prepare_summary(papers, config)

        # Build the data
        data = {
            "success": True,
            "papers": papers,
            "paper_count": len(papers),
            "prompt": result.get('prompt', ''),
            "instruction": result.get('instruction', ''),
            "config": {
                'language': config.get('language'),
                'time_window_hours': config.get('time_window_hours'),
                'default_query': config.get('default_query'),
                'max_results': config.get('max_results'),
                'search_categories': config.get('search_categories', [])
            }
        }

        # Create temp directory in project root
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        # Generate unique filename
        import time
        timestamp = int(time.time())
        filename = f"daily_data_{timestamp}.json"
        filepath = os.path.join(temp_dir, filename)

        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Return file path
        output_json({
            "success": True,
            "file_path": filepath,
            "paper_count": len(papers),
            "message": "Data saved to file. Use Read tool to read the file."
        })
    except Exception as e:
        output_error(f"Failed to prepare daily summary: {e}")


def prepare_analysis(arxiv_id: str = None, analysis_type: str = "deep") -> None:
    """
    Prepare paper analysis - combines PDF download and prompt preparation.
    This is a single-command replacement for the multi-step process.

    Saves the JSON result to a temporary file in the project directory
    and returns the file path for stable reading by agents.
    """
    try:
        from search import search_arxiv_papers
        from pdf_processor import process_pdf
        from analyzer import prepare_analysis

        # Load config
        config = load_config()

        # Find the paper
        papers = search_arxiv_papers(query=f"id:{arxiv_id}", max_results=1)

        if not papers:
            output_error(f"Paper {arxiv_id} not found")

        paper = papers[0]

        # Process PDF
        paper_with_content = process_pdf(paper)

        # Prepare analysis context
        result = prepare_analysis(paper_with_content, analysis_type, config)

        # Build the data
        data = {
            "success": True,
            "paper": paper_with_content,
            "prompt": result.get('prompt', ''),
            "instruction": result.get('instruction', ''),
            "config": {
                'language': config.get('language'),
                'analysis_type': analysis_type
            }
        }

        # Create temp directory in project root
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        # Generate unique filename
        import time
        timestamp = int(time.time())
        # Sanitize arxiv_id for filename
        safe_arxiv_id = arxiv_id.replace('/', '_').replace('.', '_')
        filename = f"analysis_data_{safe_arxiv_id}_{timestamp}.json"
        filepath = os.path.join(temp_dir, filename)

        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Return file path
        output_json({
            "success": True,
            "file_path": filepath,
            "arxiv_id": arxiv_id,
            "message": "Data saved to file. Use Read tool to read the file."
        })
    except Exception as e:
        output_error(f"Failed to prepare analysis: {e}")


# ============================================================================
# Prompt Management Commands
# ============================================================================

def get_prompt(name: str) -> None:
    """Get prompt template content"""
    try:
        content = load_prompt(name)
        output_json({
            "success": True,
            "name": name,
            "content": content
        })
    except FileNotFoundError:
        output_error(f"Prompt '{name}' not found")
    except Exception as e:
        output_error(f"Failed to get prompt: {e}")


def set_prompt(name: str, content: str = None) -> None:
    """Set prompt template content. If content is None, read from stdin"""
    try:
        if content is None:
            # Read from stdin
            content = sys.stdin.read()

        save_prompt(name, content)

        output_json({
            "success": True,
            "name": name,
            "length": len(content)
        })
    except Exception as e:
        output_error(f"Failed to set prompt: {e}")


def reset_prompt(name: str) -> None:
    """Reset prompt to default (delete user custom version)"""
    import os
    import glob

    try:
        user_prompts_dir = get_prompts_dir()
        user_prompt_path = os.path.join(user_prompts_dir, f"{name}.md")

        if os.path.exists(user_prompt_path):
            os.remove(user_prompt_path)

        # Verify it's gone and default exists
        default_prompt_path = os.path.join("prompts", f"{name}.md")
        if not os.path.exists(default_prompt_path):
            output_error(f"Default prompt '{name}' not found")

        output_json({
            "success": True,
            "name": name,
            "reset": True
        })
    except Exception as e:
        output_error(f"Failed to reset prompt: {e}")


def list_prompts() -> None:
    """List all available prompts"""
    import os

    try:
        default_dir = "prompts"
        user_dir = get_prompts_dir()

        available = []
        if os.path.exists(default_dir):
            for file in os.listdir(default_dir):
                if file.endswith('.md'):
                    name = file[:-3]
                    has_custom = os.path.exists(os.path.join(user_dir, file))
                    available.append({
                        "name": name,
                        "has_custom": has_custom
                    })

        output_json({
            "success": True,
            "prompts": available,
            "count": len(available)
        })
    except Exception as e:
        output_error(f"Failed to list prompts: {e}")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Arxiv Paper Processing CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Onboarding commands
    subparsers.add_parser('check-onboarding', help='Check if onboarding is complete')
    subparsers.add_parser('check-dependencies', help='Check if dependencies are installed')

    complete_parser = subparsers.add_parser('complete-onboarding', help='Complete onboarding')
    complete_parser.add_argument('--language', default='zh', help='Language preference')
    complete_parser.add_argument('--time-window', type=int, default=24, help='Time window in hours')
    complete_parser.add_argument('--query', default='AI Agent', help='Default search query')

    # Config commands
    subparsers.add_parser('get-config', help='Get current configuration')

    set_config_parser = subparsers.add_parser('set-config', help='Set a config value')
    set_config_parser.add_argument('key', help='Config key')
    set_config_parser.add_argument('value', help='Config value (JSON or string)')

    subparsers.add_parser('reset-config', help='Reset configuration to defaults')

    # Search commands
    search_parser = subparsers.add_parser('search', help='Search arxiv papers')
    search_parser.add_argument('--query', help='Search query')
    search_parser.add_argument('--max-results', type=int, help='Max results')
    search_parser.add_argument('--time-window', type=int, help='Time window in hours')

    process_pdf_parser = subparsers.add_parser('process-pdf', help='Download and process PDF')
    process_pdf_parser.add_argument('arxiv_id', help='Arxiv ID of the paper')

    subparsers.add_parser('prepare-daily', help='Prepare daily summary (search + prompt)')

    prepare_analysis_parser = subparsers.add_parser('prepare-analysis', help='Prepare paper analysis')
    prepare_analysis_parser.add_argument('arxiv_id', help='Arxiv ID of the paper')
    prepare_analysis_parser.add_argument('--type', default='deep', help='Analysis type')

    # Prompt commands
    get_prompt_parser = subparsers.add_parser('get-prompt', help='Get prompt content')
    get_prompt_parser.add_argument('name', help='Prompt name')

    set_prompt_parser = subparsers.add_parser('set-prompt', help='Set prompt content')
    set_prompt_parser.add_argument('name', help='Prompt name')
    set_prompt_parser.add_argument('--content', help='Prompt content (optional, reads from stdin if not provided)')

    reset_prompt_parser = subparsers.add_parser('reset-prompt', help='Reset prompt to default')
    reset_prompt_parser.add_argument('name', help='Prompt name')

    subparsers.add_parser('list-prompts', help='List all available prompts')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to command
    commands = {
        'check-onboarding': check_onboarding,
        'check-dependencies': check_dependencies,
        'complete-onboarding': lambda: complete_onboarding(args.language, args.time_window, args.query),
        'get-config': get_config,
        'set-config': lambda: set_config(args.key, args.value),
        'reset-config': reset_config,
        'search': lambda: search_papers(args.query, args.max_results, args.time_window),
        'process-pdf': lambda: process_pdf(args.arxiv_id),
        'prepare-daily': prepare_daily,
        'prepare-analysis': lambda: prepare_analysis(args.arxiv_id, args.type),
        'get-prompt': lambda: get_prompt(args.name),
        'set-prompt': lambda: set_prompt(args.name, getattr(args, 'content', None)),
        'reset-prompt': lambda: reset_prompt(args.name),
        'list-prompts': list_prompts,
    }

    if args.command in commands:
        commands[args.command]()
    else:
        output_error(f"Unknown command: {args.command}")


if __name__ == '__main__':
    main()
