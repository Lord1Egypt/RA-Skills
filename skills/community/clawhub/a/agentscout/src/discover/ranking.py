"""TopK 排行榜管理"""

from rich.console import Console
from rich.table import Table

from src.storage.models import Project, Score, RankingEntry
from src.storage.database import Database


class RankingManager:
    """排行榜管理器"""

    def __init__(self, db: Database, topk_size: int = 20):
        self.db = db
        self.topk_size = topk_size

    def get_top_n(self, n: int = 3) -> list[RankingEntry]:
        """获取当前排行榜前 N 名"""
        top_projects = self.db.get_top_projects(n)
        entries = []
        for rank, (project, score) in enumerate(top_projects, 1):
            entries.append(RankingEntry(rank=rank, project=project, score=score))
        return entries

    def save_snapshot(self):
        """保存当天排行榜快照"""
        top_projects = self.db.get_top_projects(self.topk_size)
        entries = [
            (rank, project.id, score.total_score)
            for rank, (project, score) in enumerate(top_projects, 1)
        ]
        if entries:
            self.db.save_ranking_snapshot(entries)

    def present_top_n(self, n: int = 3) -> list[RankingEntry]:
        """展示 Top N 项目并返回列表"""
        entries = self.get_top_n(n)
        if not entries:
            print("\n📭 暂无评分项目，请先运行搜索和评分。\n")
            return entries

        console = Console()
        table = Table(
            title="🏆 AgentScout Top 项目",
            show_lines=True,
            title_style="bold cyan",
        )
        table.add_column("#", style="bold", width=3)
        table.add_column("项目", style="cyan", width=30)
        table.add_column("描述", width=40)
        table.add_column("⭐", justify="right", width=6)
        table.add_column("总分", justify="right", style="bold green", width=6)
        table.add_column("评价", width=30)

        for entry in entries:
            p = entry.project
            s = entry.score
            table.add_row(
                str(entry.rank),
                f"[link={p.repo_url}]{p.repo_full_name}[/link]",
                (p.description[:37] + "...") if len(p.description) > 40 else p.description,
                str(p.stars),
                f"{s.total_score:.1f}",
                s.scoring_reason,
            )

        console.print(table)
        console.print()

        # 详细评分
        for entry in entries:
            s = entry.score
            console.print(
                f"  [{entry.rank}] {entry.project.name}: "
                f"新颖={s.novelty:.0f} 实用={s.practicality:.0f} "
                f"适配={s.content_fit:.0f} 易用={s.ease_of_use:.0f}"
            )
        console.print()

        return entries

    def select_project(self, entries: list[RankingEntry]) -> RankingEntry:
        """让用户从 Top N 中选择一个项目"""
        if len(entries) == 1:
            print(f"只有一个项目，自动选择: {entries[0].project.name}")
            return entries[0]

        while True:
            try:
                choice = input(f"请选择项目编号 (1-{len(entries)}): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(entries):
                    selected = entries[idx]
                    print(f"\n✅ 已选择: {selected.project.repo_full_name}\n")
                    return selected
                print(f"请输入 1 到 {len(entries)} 之间的数字")
            except (ValueError, EOFError):
                print("输入无效，请重试")
