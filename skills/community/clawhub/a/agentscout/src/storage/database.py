"""SQLite 数据库操作"""

import sqlite3
from pathlib import Path
from typing import Optional
from datetime import datetime

from src.storage.models import Project, Score, Post


class Database:
    """SQLite 数据库管理器"""

    def __init__(self, db_path: str = ""):
        if not db_path:
            from src.config import load_config
            db_path = load_config().db_path
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init(self):
        """初始化数据库表结构"""
        conn = self._connect()
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_full_name TEXT UNIQUE NOT NULL,
                    repo_url TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    language TEXT,
                    stars INTEGER DEFAULT 0,
                    forks INTEGER DEFAULT 0,
                    open_issues INTEGER DEFAULT 0,
                    last_updated TEXT,
                    created_at TEXT,
                    owner_type TEXT,
                    topics TEXT,
                    readme_excerpt TEXT,
                    discovered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    source TEXT
                );

                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    scored_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    rubric_version TEXT NOT NULL,
                    novelty REAL NOT NULL,
                    practicality REAL NOT NULL,
                    content_fit REAL NOT NULL,
                    ease_of_use REAL NOT NULL,
                    total_score REAL NOT NULL,
                    scoring_reason TEXT,
                    llm_model TEXT,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                );

                CREATE TABLE IF NOT EXISTS ranking_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_date TEXT NOT NULL,
                    rank INTEGER NOT NULL,
                    project_id INTEGER NOT NULL,
                    total_score REAL NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                );

                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    analysis_path TEXT,
                    post_path TEXT,
                    images_dir TEXT,
                    status TEXT DEFAULT 'draft',
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                );
            """)
            conn.commit()
        finally:
            conn.close()

    # ---- Projects CRUD ----

    def insert_project(self, project: Project) -> int:
        """插入项目，返回 ID。如果已存在则更新并返回已有 ID"""
        conn = self._connect()
        try:
            cursor = conn.execute(
                """INSERT INTO projects
                   (repo_full_name, repo_url, name, description, language,
                    stars, forks, open_issues, last_updated, created_at,
                    owner_type, topics, readme_excerpt, source)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(repo_full_name) DO UPDATE SET
                    stars=excluded.stars, forks=excluded.forks,
                    open_issues=excluded.open_issues,
                    last_updated=excluded.last_updated,
                    description=excluded.description,
                    readme_excerpt=excluded.readme_excerpt""",
                (project.repo_full_name, project.repo_url, project.name,
                 project.description, project.language, project.stars,
                 project.forks, project.open_issues, project.last_updated,
                 project.created_at, project.owner_type, project.topics_json,
                 project.readme_excerpt, project.source)
            )
            conn.commit()
            if cursor.lastrowid:
                return cursor.lastrowid
            # ON CONFLICT 时 lastrowid 可能为 0，需要查询
            row = conn.execute(
                "SELECT id FROM projects WHERE repo_full_name = ?",
                (project.repo_full_name,)
            ).fetchone()
            return row["id"]
        finally:
            conn.close()

    def get_project(self, project_id: int) -> Optional[Project]:
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT * FROM projects WHERE id = ?", (project_id,)
            ).fetchone()
            return Project.from_db_row(row) if row else None
        finally:
            conn.close()

    def get_project_by_name(self, repo_full_name: str) -> Optional[Project]:
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT * FROM projects WHERE repo_full_name = ?",
                (repo_full_name,)
            ).fetchone()
            return Project.from_db_row(row) if row else None
        finally:
            conn.close()

    def project_exists(self, repo_full_name: str) -> bool:
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT 1 FROM projects WHERE repo_full_name = ?",
                (repo_full_name,)
            ).fetchone()
            return row is not None
        finally:
            conn.close()

    # ---- Scores CRUD ----

    def insert_score(self, score: Score) -> int:
        conn = self._connect()
        try:
            cursor = conn.execute(
                """INSERT INTO scores
                   (project_id, rubric_version, novelty, practicality,
                    content_fit, ease_of_use, total_score, scoring_reason, llm_model)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (score.project_id, score.rubric_version, score.novelty,
                 score.practicality, score.content_fit, score.ease_of_use,
                 score.total_score, score.scoring_reason, score.llm_model)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_latest_score(self, project_id: int) -> Optional[Score]:
        conn = self._connect()
        try:
            row = conn.execute(
                """SELECT * FROM scores WHERE project_id = ?
                   ORDER BY scored_at DESC LIMIT 1""",
                (project_id,)
            ).fetchone()
            return Score.from_db_row(row) if row else None
        finally:
            conn.close()

    def get_score_history(self, project_id: int) -> list[Score]:
        conn = self._connect()
        try:
            rows = conn.execute(
                "SELECT * FROM scores WHERE project_id = ? ORDER BY scored_at",
                (project_id,)
            ).fetchall()
            return [Score.from_db_row(r) for r in rows]
        finally:
            conn.close()

    # ---- Ranking ----

    def get_top_projects(self, n: int = 20) -> list[tuple[Project, Score]]:
        """获取评分最高的 N 个项目（按最新评分排序）"""
        conn = self._connect()
        try:
            rows = conn.execute(
                """SELECT p.*, s.id as score_id, s.project_id as s_project_id,
                          s.scored_at, s.rubric_version, s.novelty,
                          s.practicality, s.content_fit, s.ease_of_use,
                          s.total_score, s.scoring_reason, s.llm_model
                   FROM projects p
                   JOIN (
                       SELECT project_id, MAX(scored_at) as max_scored
                       FROM scores GROUP BY project_id
                   ) latest ON p.id = latest.project_id
                   JOIN scores s ON s.project_id = latest.project_id
                                AND s.scored_at = latest.max_scored
                   ORDER BY s.total_score DESC
                   LIMIT ?""",
                (n,)
            ).fetchall()
            results = []
            for row in rows:
                row_dict = dict(row)
                proj_data = {k: row_dict[k] for k in [
                    "id", "repo_full_name", "repo_url", "name", "description",
                    "language", "stars", "forks", "open_issues", "last_updated",
                    "created_at", "owner_type", "topics", "readme_excerpt",
                    "discovered_at", "source"
                ]}
                project = Project.from_db_row(proj_data)
                score = Score(
                    id=row_dict["score_id"],
                    project_id=row_dict["s_project_id"],
                    scored_at=row_dict["scored_at"],
                    rubric_version=row_dict["rubric_version"],
                    novelty=row_dict["novelty"],
                    practicality=row_dict["practicality"],
                    content_fit=row_dict["content_fit"],
                    ease_of_use=row_dict["ease_of_use"],
                    total_score=row_dict["total_score"],
                    scoring_reason=row_dict["scoring_reason"],
                    llm_model=row_dict["llm_model"],
                )
                results.append((project, score))
            return results
        finally:
            conn.close()

    def save_ranking_snapshot(self, entries: list[tuple[int, int, float]]):
        """保存排行榜快照: [(rank, project_id, total_score), ...]"""
        conn = self._connect()
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            conn.executemany(
                """INSERT INTO ranking_snapshots
                   (snapshot_date, rank, project_id, total_score)
                   VALUES (?, ?, ?, ?)""",
                [(today, rank, pid, score) for rank, pid, score in entries]
            )
            conn.commit()
        finally:
            conn.close()

    # ---- Posts CRUD ----

    def insert_post(self, post: Post) -> int:
        conn = self._connect()
        try:
            cursor = conn.execute(
                """INSERT INTO posts
                   (project_id, analysis_path, post_path, images_dir, status)
                   VALUES (?, ?, ?, ?, ?)""",
                (post.project_id, post.analysis_path, post.post_path,
                 post.images_dir, post.status)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_post_status(self, post_id: int, status: str):
        conn = self._connect()
        try:
            conn.execute(
                "UPDATE posts SET status = ? WHERE id = ?",
                (status, post_id)
            )
            conn.commit()
        finally:
            conn.close()
