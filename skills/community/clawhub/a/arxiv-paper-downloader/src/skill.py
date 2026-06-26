#!/usr/bin/env python3
"""
arXiv Paper Downloader Skill

Download papers from arXiv by category or custom arXiv IDs.
Supports batch downloading with metadata export.
"""

import requests
import json
from pathlib import Path
import time
from typing import List, Dict, Optional


class ArxivDownloader:
    """arXiv paper downloader with batch support."""

    # Pre-curated paper lists by category
    PAPER_COLLECTIONS = {
        "agent_testing": [
            ("2310.06129", "SWE-agent: Agent-Computer Interfaces for Automated SE"),
            ("2402.01031", "SWE-bench: Can LMs Resolve Real-world GitHub Issues?"),
            ("2406.12615", "SWE-agent 2.0: Improving SE with Agents"),
            ("2305.00443", "Generating Unit Tests with LLMs"),
            ("2307.04325", "Test Case Generation using LLMs"),
            ("2401.03325", "Unit Test Generation using Code LLMs"),
            ("2310.08572", "Automatic Test Generation with LLMs"),
            ("2404.00166", "Test Gen with LLMs: A Survey"),
            ("2403.16210", "Autonomous Agents for Software Testing"),
            ("2311.13720", "Multi-Agent Code Testing with LLMs"),
            ("2405.07989", "Agent Testing in the Wild"),
            ("2304.14106", "Evaluating LLMs in Testing Scenarios"),
            ("2402.13216", "LLM-based Test Oracle Generation"),
            ("2312.14151", "Benchmarking LLMs for Code Testing"),
            ("2308.02554", "Bug Detection and Repair with LLMs"),
            ("2312.04726", "Automated Bug Fixing using Code LMs"),
            ("2401.10043", "LLM-based Bug Detection: A Survey"),
            ("2308.11444", "Code Understanding for Test Generation"),
            ("2403.09218", "Neuro-Symbolic Testing with LLMs"),
        ],
        "agents": [
            ("2308.08155", "Generative Agents: Interactive Simulacra"),
            ("2309.07864", "LLMs are Superpositions of All Agents"),
            ("2402.04891", "Survey on LLM-based Autonomous Agents"),
            ("2309.10833", "Multi-Agent Collaboration: A Survey"),
            ("2312.05282", "ChatEval: Multi-Agent Collaborative Text Eval"),
            ("2401.08086", "CoLLM: Collaborative Multi-Agent LLMs"),
            ("2310.10158", "AgentBench: Evaluating LLMs as Agents"),
            ("2402.07456", "AgentBoard: An Analytical Evaluation Board"),
            ("2401.16142", "Tool Learning with Foundation Models"),
            ("2305.10601", "Plan-and-Solve Prompting for LLMs"),
            ("2309.06122", "Reflexion: Language Agents with Verbal RL"),
            ("2312.11166", "Chain of Thought Hindsight for Planning"),
        ],
        "llm": [
            ("1706.03762", "Attention Is All You Need (Transformer)"),
            ("1810.04805", "BERT: Pre-training of Deep Bidirectional"),
            ("2005.14165", "GPT-3: Language Models are Few-Shot"),
            ("2107.03374", "Evaluating LLMs Trained on Code"),
            ("2112.11446", "Training LMs to Follow Instructions"),
            ("2303.08774", "GPT-4 Technical Report"),
            ("2302.13971", "LLaMA: Open and Efficient Foundation LMs"),
            ("2307.09288", "Llama 2: Open Foundation and Chat Models"),
            ("2401.02954", "LLM Survey: A Comprehensive Review"),
            ("2112.04426", "CodeT5: Identifier-aware Pre-trained ED"),
            ("2304.12244", "WizardLM: Empowering LLMs to Follow"),
            ("2401.11817", "Code Llama: Open Foundation Models for Code"),
            ("2305.14314", "LoRA: Low-Rank Adaptation of LLMs"),
            ("2310.05914", "QLoRA: Efficient Finetuning of Quantized"),
            ("2404.02060", "Long Context Processing: A Survey"),
        ],
    }

    def __init__(self, output_dir: str = "./papers", delay: float = 1.5):
        """
        Initialize the downloader.

        Args:
            output_dir: Directory to save downloaded papers
            delay: Delay between downloads in seconds
        """
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; arxiv-downloader/1.0)"
        })

    def download_pdf(self, arxiv_id: str, title: str = "") -> Dict:
        """
        Download a single paper PDF.

        Args:
            arxiv_id: arXiv ID (e.g., "2310.06129")
            title: Paper title for filename

        Returns:
            dict with status, path, size
        """
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in (title[:40] or arxiv_id))
        filename = f"{arxiv_id}_{safe_title}.pdf"
        filepath = self.output_dir / filename

        if filepath.exists():
            return {"status": "skipped", "path": str(filepath), "size": 0}

        try:
            resp = self.session.get(pdf_url, timeout=120)
            if resp.status_code == 200:
                self.output_dir.mkdir(parents=True, exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                return {
                    "status": "downloaded",
                    "path": str(filepath),
                    "size": len(resp.content)
                }
            else:
                return {"status": "failed", "error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def download_batch(self, category: str, delay: Optional[float] = None) -> Dict:
        """
        Download all papers in a category.

        Args:
            category: Category name (agent_testing, agents, llm)
            delay: Optional delay override

        Returns:
            dict with downloaded, skipped, failed counts and metadata path
        """
        if category not in self.PAPER_COLLECTIONS:
            return {"error": f"Unknown category: {category}"}

        papers = self.PAPER_COLLECTIONS[category]
        cat_dir = self.output_dir / category
        results = {"downloaded": 0, "skipped": 0, "failed": 0, "papers": []}

        for arxiv_id, title in papers:
            result = self.download_pdf(arxiv_id, title)
            result["arxiv_id"] = arxiv_id
            result["title"] = title
            results["papers"].append(result)

            if result["status"] == "downloaded":
                results["downloaded"] += 1
                print(f"✓ {arxiv_id} - {title[:50]}...")
            elif result["status"] == "skipped":
                results["skipped"] += 1
            else:
                results["failed"] += 1

            time.sleep(delay or self.delay)

        # Save metadata
        metadata = {
            "category": category,
            "total": len(papers),
            "results": results
        }
        meta_file = cat_dir / "download_metadata.json"
        cat_dir.mkdir(parents=True, exist_ok=True)
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        results["metadata_path"] = str(meta_file)

        return results

    def download_by_ids(self, arxiv_ids: List[str]) -> Dict:
        """
        Download papers by arXiv IDs.

        Args:
            arxiv_ids: List of arXiv IDs

        Returns:
            dict with results
        """
        results = {"downloaded": 0, "skipped": 0, "failed": 0, "papers": []}

        for arxiv_id in arxiv_ids:
            result = self.download_pdf(arxiv_id, arxiv_id)
            result["arxiv_id"] = arxiv_id
            results["papers"].append(result)

            if result["status"] == "downloaded":
                results["downloaded"] += 1
            elif result["status"] == "skipped":
                results["skipped"] += 1
            else:
                results["failed"] += 1

            time.sleep(self.delay)

        return results

    def get_available_categories(self) -> List[str]:
        """Return list of available paper categories."""
        return list(self.PAPER_COLLECTIONS.keys())

    def get_category_info(self, category: str) -> Dict:
        """
        Get information about a paper category.

        Args:
            category: Category name

        Returns:
            dict with category info
        """
        if category not in self.PAPER_COLLECTIONS:
            return {"error": f"Unknown category: {category}"}

        papers = self.PAPER_COLLECTIONS[category]
        return {
            "name": category,
            "paper_count": len(papers),
            "papers": [{"arxiv_id": id, "title": title} for id, title in papers]
        }


# Skill entry points
def download_papers(category: str = "agent_testing", output_dir: str = "./papers", delay: float = 1.5) -> Dict:
    """
    Download papers from arXiv by category.

    Args:
        category: Paper category (agent_testing, agents, llm, or all)
        output_dir: Directory to save papers
        delay: Delay between downloads in seconds

    Returns:
        dict with download statistics

    Examples:
        >>> download_papers("agent_testing")
        >>> download_papers("all", output_dir="./my_papers")
        >>> download_papers("llm", delay=2.0)
    """
    downloader = ArxivDownloader(output_dir, delay)

    if category == "all":
        all_results = {"categories": {}}
        for cat in downloader.get_available_categories():
            print(f"\nDownloading {cat}...")
            all_results["categories"][cat] = downloader.download_batch(cat)
        return all_results
    else:
        return downloader.download_batch(category)


def download_by_arxiv_ids(arxiv_ids: List[str], output_dir: str = "./papers", delay: float = 1.5) -> Dict:
    """
    Download papers by arXiv IDs.

    Args:
        arxiv_ids: List of arXiv IDs to download
        output_dir: Directory to save papers
        delay: Delay between downloads

    Returns:
        dict with download results

    Examples:
        >>> download_by_arxiv_ids(["2310.06129", "2402.01031"])
        >>> download_by_arxiv_ids(["1706.03762"], output_dir="./transformer")
    """
    downloader = ArxivDownloader(output_dir, delay)
    return downloader.download_by_ids(arxiv_ids)


def list_categories() -> List[str]:
    """
    List available paper categories.

    Returns:
        List of category names

    Examples:
        >>> list_categories()
        ['agent_testing', 'agents', 'llm']
    """
    downloader = ArxivDownloader()
    return downloader.get_available_categories()


def get_category_info(category: str) -> Dict:
    """
    Get information about a paper category.

    Args:
        category: Category name

    Returns:
        dict with category info

    Examples:
        >>> get_category_info("agent_testing")
        {'name': 'agent_testing', 'paper_count': 19, 'papers': [...]}
    """
    downloader = ArxivDownloader()
    return downloader.get_category_info(category)


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="arXiv Paper Downloader Skill")
    parser.add_argument("--category", choices=["testing", "agents", "llm", "all"],
                       default="testing", help="Paper category")
    parser.add_argument("--output", default="./papers", help="Output directory")
    parser.add_argument("--delay", type=float, default=1.5, help="Download delay")
    parser.add_argument("--ids", nargs="+", help="Specific arXiv IDs to download")
    args = parser.parse_args()

    if args.ids:
        result = download_by_arxiv_ids(args.ids, args.output, args.delay)
    else:
        result = download_papers(args.category, args.output, args.delay)

    print(f"\nDownload complete: {result}")
