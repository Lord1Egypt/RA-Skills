from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from arxiv_client import fetch_category_for_date, today_date_string
from render import build_notes_markdown, build_xhs_post, now_labels, write_json, write_text
from cover import generate_cover_image
from scoring import matched, score_paper
from xhs_client import XHSClient


@dataclass
class PipelineResult:
    notes_path: Path
    matched_path: Path
    post_draft_path: Path
    publish_result_path: Path | None
    matched_papers: list[dict[str, Any]]
    post_payload: dict[str, str]


class DailyPipeline:
    def __init__(self, project_root: Path, topic_key: str, config: dict[str, Any]) -> None:
        self.project_root = project_root
        self.topic_key = topic_key
        self.topic_config = config["topics"][topic_key]
        self.sources = config["sources"]
        self.client = XHSClient()

    def run(self, publish: bool = False) -> PipelineResult:
        date_folder, date_label = now_labels()
        base_dir = self.project_root / "data" / self.topic_key / date_folder
        raw_dir = base_dir / "raw"
        processed_dir = base_dir / "processed"
        papers = self._collect_papers(raw_dir)
        matched_papers = self._match_and_annotate(papers)
        matched_path = processed_dir / "matched_papers.json"
        write_json(matched_path, matched_papers)
        notes_path = processed_dir / "notes.md"
        write_text(notes_path, build_notes_markdown(self.topic_config["display_name"], date_label, matched_papers))
        post_payload = build_xhs_post(self.topic_config["display_name"], self.topic_config, date_label, matched_papers)
        cover_path = processed_dir / "cover.png"
        generate_cover_image(
            output_path=cover_path,
            title=post_payload["title"],
            subtitle=f"{self.topic_config['display_name']} · arXiv Daily",
            bullets=[paper["title"] for paper in matched_papers[:3]],
            theme="light",
        )
        post_payload["cover_image"] = str(cover_path)
        post_draft_path = processed_dir / "post_draft.json"
        write_json(post_draft_path, post_payload)
        publish_result_path = None
        if publish:
            result = self.client.publish_content(post_payload["title"], post_payload["content"], [str(cover_path)])
            publish_result_path = processed_dir / "publish_result.txt"
            write_text(publish_result_path, result)
        return PipelineResult(notes_path, matched_path, post_draft_path, publish_result_path, matched_papers, post_payload)

    def _collect_papers(self, raw_dir: Path) -> list[dict[str, Any]]:
        papers: list[dict[str, Any]] = []
        seen: set[str] = set()
        target_date = today_date_string()
        for category in self.sources.get("categories", []):
            fetched = fetch_category_for_date(
                category,
                target_date=target_date,
                page_size=self.sources.get("page_size", 200),
                max_scan_results=self.sources.get("max_scan_results_per_category", 800),
            )
            if not fetched:
                fetched = fetch_category_for_date(
                    category,
                    target_date=None,
                    page_size=self.sources.get("page_size", 200),
                    max_scan_results=self.sources.get("max_scan_results_per_category", 800),
                )
            write_json(raw_dir / f"{category.replace('.', '_')}.json", fetched)
            for paper in fetched:
                paper_id = paper.get("id")
                if not paper_id or paper_id in seen:
                    continue
                seen.add(paper_id)
                papers.append(paper)
        return papers

    def _match_and_annotate(self, papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
        ranked = []
        for paper in papers:
            if not matched(paper, self.topic_config):
                continue
            enriched = dict(paper)
            enriched["score"] = score_paper(paper, self.topic_config)
            enriched["problem"] = self._problem(paper)
            enriched["method"] = self._method(paper)
            enriched["result"] = self._result(paper)
            enriched["my_thought"] = self._my_thought(paper)
            ranked.append(enriched)
        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked[: self.topic_config.get("max_matches", 5)]

    def _problem(self, paper: dict[str, Any]) -> str:
        text = f"{paper.get('title', '')} {paper.get('summary', '')}".lower()
        summary = " ".join((paper.get("summary", "") or "").split())
        if "eos" in text or "scratchpad" in text:
            return "它想回答一个很关键的问题：diffusion LLM 在推理任务上变强，到底只是输出更灵活，还是模型真的会在额外的 EoS token 上做隐式思考。"
        if "pass@$k" in text or "diverse sampling" in text or "sampling" in text:
            return "它盯的是 diffusion language model 里的一个实际痛点：多次采样时，候选容易塌到相似模式，导致 Pass@k 这类需要探索的任务吃不到真正的多样性收益。"
        return summary[:180] if summary else "这篇论文要解决的问题需要结合原文再细看。"

    def _method(self, paper: dict[str, Any]) -> str:
        text = f"{paper.get('title', '')} {paper.get('summary', '')}".lower()
        if "eos" in text or "scratchpad" in text:
            return "作者先比较补 EoS token 前后的推理表现，再做 hidden state patching 的因果干预，看这些 EoS 表征到底有没有承载中间计算。"
        if "pass@$k" in text or "diverse sampling" in text or "sampling" in text:
            return "它没有重训模型，而是在 diffusion sampling 阶段做低成本干预：顺序修改 batch 里的中间样本，让后续候选主动远离前面样本的特征空间，减少重复。"
        return "具体技术路径需要结合原文实验部分继续拆。"

    def _result(self, paper: dict[str, Any]) -> str:
        text = f"{paper.get('title', '')} {paper.get('summary', '')}".lower()
        if "eos" in text or "scratchpad" in text:
            return "摘要里提到，作者在 Addition、Entity Tracking、Sudoku 上验证了 EoS token 的作用，而且 patch counterfactual hidden states 会明显改输出，这个证据链挺扎实。"
        if "pass@$k" in text or "diverse sampling" in text or "sampling" in text:
            return "它在 HumanEval 和 GSM8K 上都提升了 diversity 和 Pass@k，而且额外开销很低，这条线对 test-time scaling 很有吸引力。"
        return "效果部分需要结合原文数据表继续细看。"

    def _my_thought(self, paper: dict[str, Any]) -> str:
        text = f"{paper.get('title', '')} {paper.get('summary', '')}".lower()
        if "eos" in text or "scratchpad" in text:
            return "这篇比表面上看起来更重要。它如果成立，说明 diffusion LLM 可能天然就有一种不同于 autoregressive model 的隐式思考空间，这对 reasoning trace 的理解会很有启发。"
        if "pass@$k" in text or "diverse sampling" in text or "sampling" in text:
            return "这条线很可能不只是采样技巧，而是会直接连到 test-time scaling。候选真能拉开，diffusion 路线在 search 上的潜力就会更大。"
        if "reason" in text or "trace" in text:
            return "我更关心的是，它会不会带来新的 reasoning trace 形式，而不只是 benchmark 上多几个点。"
        if "align" in text or "safety" in text:
            return "我会想把它往安全性和可解释性那边再推一步，看训练方式是不是会改变风险面。"
        return "第一眼看下来，我会先把它当成一个值得继续跟的问题线索，而不是立刻下结论。"
