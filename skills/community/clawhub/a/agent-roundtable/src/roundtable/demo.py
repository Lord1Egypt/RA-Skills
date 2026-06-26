from __future__ import annotations

import logging
import os
import textwrap
from typing import Any

logger = logging.getLogger(__name__)

DEMO_TOPIC: str = "选择后端框架：FastAPI vs Go Gin vs Node Express"
DEMO_PARTICIPANTS: list[dict[str, Any]] = [
    {
        "profile": "alice",
        "role": "全栈工程师",
        "display_name": "Alice",
        "perspective": "重视开发效率和生态",
        "avatar": "👩‍💻",
        "title": "Senior Full-Stack Engineer",
        "description": (
            "10 年全栈经验，主导过多个从零到一的产品架构。擅长 Python/TypeScript 全栈，关注开发者体验和交付效率。"
        ),
    },
    {
        "profile": "bob",
        "role": "架构师",
        "display_name": "Bob",
        "perspective": "重视性能和可维护性",
        "avatar": "🏗️",
        "title": "Principal Architect",
        "description": "分布式系统架构专家，专注于高可用和水平扩展方案。擅长 Go/Rust 技术栈，推崇简洁的系统设计哲学。",
    },
    {
        "profile": "carol",
        "role": "产品经理",
        "display_name": "Carol",
        "perspective": "重视交付速度 and 团队学习成本",
        "avatar": "📊",
        "title": "Product Director",
        "description": "5 年 B 端产品经验，关注技术选型对业务交付的影响。擅长平衡技术理想与业务现实，推动敏捷迭代。",
    },
]
DEMO_SPEECHES: dict[int, dict[str, str]] = {
    1: {
        "alice": (
            "FastAPI 的类型提示和自动生成 OpenAPI 文档太香了，开发效率至少提升 30%。而且 async 原生支持，性能也不差。"
        ),
        "bob": (
            "Go Gin 编译后是原生二进制，内存占用只有 Python 的 1/10。"
            "对于我们这种高并发场景，性能优势明显。"
            "而且 Go 的 goroutine 天然适合并发。"
        ),
        "carol": (
            "从产品角度看，团队 80% 是 Python 背景。"
            "切 Go 需要 3 个月学习周期，这段时间功能迭代会停滞。"
            "FastAPI 能让我们更快交付 MVP。"
        ),
    },
    2: {
        "alice": (
            "同意 Carol 的观点。而且 FastAPI + Pydantic 的数据校验"
            "几乎是零成本的，Go 里要写大量 struct tag 和 binding 代码。"
            "维护成本 FastAPI 更低。"
        ),
        "bob": (
            "性能不能只看 hello world。FastAPI 在 CPU 密集型任务上"
            "还是有 GIL 瓶颈。不过我承认，如果用 asyncio + uvicorn，"
            "IO 密集场景差距没那么大。可以考虑 FastAPI + 分层架构。"
        ),
        "carol": (
            "Bob 说的分层架构我支持。先用 FastAPI 快速上线，"
            "性能瓶颈模块后续可以用 Go 重写微服务。"
            "这才是务实的技术选型策略。"
        ),
    },
    3: {
        "alice": (
            "最终方案：FastAPI 作为主力框架，搭配 Celery 处理异步任务。"
            "性能关键路径预留 Go 微服务接口。这样既保证了开发效率，"
            "又不堵死性能优化的路。"
        ),
        "bob": (
            "我同意这个折中方案。但需要在架构设计阶段就定义好"
            "服务边界和 API 契约，避免后面拆分时返工。"
            "建议第一周就定好领域模型。"
        ),
        "carol": (
            "完美！这样我们两周内就能出 MVP。技术风险可控，团队也不需要额外学习成本。我会把这个方案同步给管理层。"
        ),
    },
}
DEMO_FINDINGS: dict[int, list[tuple[str, str]]] = {
    1: [
        ("consensus", "团队熟悉 Python，学习成本是关键考量因素"),
        ("disagreement", "Go 性能优势 vs FastAPI 开发效率，优先级不同"),
        ("new_point", "需要评估 IO 密集 vs CPU 密集的实际占比"),
    ],
    2: [
        ("consensus", "IO 密集场景下 FastAPI 性能差距可接受"),
        ("consensus", "分层架构是合理的折中方案"),
        ("disagreement", "是否需要在第一阶段就引入 Go 微服务"),
    ],
    3: [
        ("consensus", "采用 FastAPI 主框架 + 预留 Go 微服务扩展"),
        ("consensus", "第一周完成领域模型和 API 契约设计"),
        ("consensus", "两周内交付 MVP，性能瓶颈模块后续迭代"),
    ],
}


class DemoRunner:
    """Helper to run a complete demo discussion using a RoundtableCore instance."""

    def __init__(self, core: Any) -> None:
        self.core = core

    def run(
        self,
        *,
        topic: str | None = None,
        participants: list[dict[str, Any]] | None = None,
        max_rounds: int = 3,
        verbose: bool = True,
        web: bool = False,
        web_port: int = 8199,
        stream_delay: float = 0.0,
    ) -> dict[str, Any]:
        topic = topic or DEMO_TOPIC
        participants = participants or DEMO_PARTICIPANTS
        p_map = {p["profile"]: p for p in participants}
        p_names = [p["profile"] for p in participants]

        # 设置流式延迟
        self.core._stream_delay = stream_delay

        if verbose:
            self._demo_print_header(topic, participants, max_rounds)

        # 1. Create discussion
        result = self.core.create_discussion(
            topic=topic,
            participants=participants,
            max_rounds=max_rounds,
        )
        disc_id = result["discussion_id"]

        # 1b. Optionally start web viewer
        publisher = None
        if web:
            from roundtable.web_publisher import WebPublisher

            output_dir = os.path.join("/tmp", "roundtable_web", disc_id)
            publisher = WebPublisher(output_dir, port=web_port)
            url = publisher.start(
                disc_id,
                topic=topic,
                participants=[
                    {
                        "profile": p["profile"],
                        "display_name": p.get("display_name", p["profile"]),
                        "role": p.get("role", ""),
                        "avatar": p.get("avatar", ""),
                        "title": p.get("title", ""),
                        "description": p.get("description", ""),
                    }
                    for p in participants
                ],
            )
            self.core._publishers[disc_id] = publisher
            if verbose:
                print(f"\n  🌐 Web viewer: {url}\n")

        self.core.speak(disc_id, "coordinator", f"开场：围绕「{topic}」展开圆桌讨论。")

        # 2. Run rounds
        for round_num in range(1, max_rounds + 1):
            if verbose:
                self._demo_print_round_start(round_num, max_rounds)

            # Use scripted speeches or generate simple defaults
            round_speeches = DEMO_SPEECHES.get(round_num, {})
            for name in p_names:
                content = round_speeches.get(
                    name,
                    f"Round {round_num} 发言：{name} 对本议题的看法（demo 默认内容）。",
                )
                self.core.speak(disc_id, name, content)

                if verbose:
                    p_info = p_map.get(name, {})
                    self._demo_print_speech(
                        name,
                        p_info.get("display_name", name),
                        p_info.get("role", ""),
                        content,
                    )

            # Add findings for this round
            round_findings = DEMO_FINDINGS.get(
                round_num,
                [
                    ("consensus", f"Round {round_num} 达成的共识"),
                    ("disagreement", f"Round {round_num} 存在的分歧"),
                ],
            )
            conn = self.core.db.connect()
            try:
                for ftype, content in round_findings:
                    self.core.db.add_finding(conn, disc_id, ftype, content, round_num)
                # Calculate convergence
                conv_score = self.core.db.calculate_convergence(conn, disc_id, round_num)
            finally:
                conn.close()

            if verbose:
                self._demo_print_round_end(round_findings, conv_score)

        # 3. Generate conclusion
        conclusion = (
            f"经过 {max_rounds} 轮讨论，团队达成一致："
            f"采用 FastAPI 作为主力框架，预留 Go 微服务扩展接口，"
            f"两周内交付 MVP。"
        )
        self.core.end_discussion(disc_id, conclusion=conclusion)

        # 4. Get final summary
        summary = self.core.summarize(disc_id, compact=True)

        if verbose:
            self._demo_print_conclusion(conclusion, summary)

        return {
            "ok": True,
            "discussion_id": disc_id,
            "topic": topic,
            "rounds_completed": max_rounds,
            "conclusion": conclusion,
            "convergence_score": summary.get("final_convergence_score"),
            "consensus_points": summary.get("consensus_points", []),
            "disagreement_points": summary.get("disagreement_points", []),
            "summary": summary,
            "web_url": publisher.url if publisher else None,
        }

    @staticmethod
    def _demo_print_header(topic: str, participants: list[dict[str, Any]], max_rounds: int) -> None:
        width = 58
        print()
        print("╭" + "─" * width + "╮")
        print("│" + " Roundtable Demo Discussion ".center(width) + "│")
        print("├" + "─" * width + "┤")
        topic_line = f" Topic: {topic}"
        if len(topic_line) > width - 1:
            topic_line = topic_line[: width - 2] + "…"
        print("│" + topic_line.ljust(width) + "│")
        print("│" + f" Rounds: {max_rounds}".ljust(width) + "│")
        print("│" + "".ljust(width) + "│")
        print("│" + " Participants:".ljust(width) + "│")
        for p in participants:
            icon = {"全栈工程师": "👩‍💻", "架构师": "👨‍💻", "产品经理": "👩‍💼"}.get(p.get("role", ""), "👤")
            line = f"   {icon} {p.get('display_name', p['profile'])} ({p.get('role', '')})"
            print("│" + line.ljust(width) + "│")
        print("╰" + "─" * width + "╯")
        print()

    @staticmethod
    def _demo_print_round_start(round_num: int, max_rounds: int) -> None:
        print(f"{'━' * 60}")
        print(f"  📍 Round {round_num}/{max_rounds}")
        print(f"{'━' * 60}")

    @staticmethod
    def _demo_print_speech(name: str, display_name: str, role: str, content: str) -> None:
        icon = {"全栈工程师": "👩‍💻", "架构师": "👨‍💻", "产品经理": "👩‍💼"}.get(role, "👤")
        print(f"\n  {icon} {display_name} ({role}):")
        for line in textwrap.wrap(content, width=52):
            print(f"     {line}")

    @staticmethod
    def _demo_print_round_end(findings: list[tuple[str, str]], conv_score: float | None) -> None:
        print()
        print(f"  {'─' * 52}")
        score_str = f"{conv_score:.2f}" if conv_score is not None else "N/A"
        print(f"  📊 Convergence: {score_str}")
        for ftype, content in findings:
            icon = {"consensus": "✅", "disagreement": "⚡", "new_point": "💡"}.get(ftype, "•")
            print(f"     {icon} [{ftype}] {content}")
        print()

    @staticmethod
    def _demo_print_conclusion(conclusion: str, summary: dict[str, Any]) -> None:
        width = 58
        print()
        print("╭" + "─" * width + "╮")
        print("│" + " 📋 Discussion Conclusion ".center(width) + "│")
        print("├" + "─" * width + "┤")

        for line in textwrap.wrap(conclusion, width=width - 4):
            print("│  " + line.ljust(width - 2) + "│")
        print("│" + "".ljust(width) + "│")

        final_score = summary.get("final_convergence_score")
        if final_score is not None:
            score_line = f"  🎯 Final Convergence: {final_score:.2f}"
            print("│" + score_line.ljust(width) + "│")

        consensus = summary.get("consensus_points", [])
        if consensus:
            print("│" + "  ✅ Consensus:".ljust(width) + "│")
            for pt in consensus:
                for line in textwrap.wrap(pt, width=width - 8):
                    print("│    • " + line.ljust(width - 6) + "│")

        disagreements = summary.get("disagreement_points", [])
        if disagreements:
            print("│" + "  ⚡ Disagreements:".ljust(width) + "│")
            for pt in disagreements:
                for line in textwrap.wrap(pt, width=width - 8):
                    print("│    • " + line.ljust(width - 6) + "│")

        print("╰" + "─" * width + "╯")
        print()
