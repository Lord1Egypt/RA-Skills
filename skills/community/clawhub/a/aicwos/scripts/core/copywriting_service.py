"""
文案生成辅助服务

核心优化：系列文案连续性只读摘要，不读全文。
文案正文直接写.txt文件（纯正文，用户可直接查看/编辑），DB只存元数据（摘要、hook_next）。
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from scripts.core.db_manager import DatabaseManager
from scripts.core.knowledge_service import KnowledgeService
from scripts.core.lecturer_service import LecturerService


class CopywritingService:
    """文案生成辅助"""

    def __init__(self, db: DatabaseManager, data_dir: str = None):
        self.db = db
        self.data_dir = Path(data_dir) if data_dir else None
        self.lecturer_svc = LecturerService(db)
        self.knowledge_svc = KnowledgeService(db)

    # ── 文件读写 ──────────────────────────────────────────

    def _episode_dir(self, series_id: str) -> Optional[Path]:
        """获取系列文案目录，需要data_dir和lecturer_id"""
        if not self.data_dir:
            return None
        plan = self.get_series_plan(series_id)
        if not plan:
            return None
        lid = plan["lecturer_id"]
        return self.data_dir / "讲师列表" / lid / "系列文案" / series_id

    def _write_episode_file(self, series_id: str, episode_num: int,
                            title: str, content: str):
        """将集文案写入.txt文件（纯正文，不带任何元数据头）"""
        ep_dir = self._episode_dir(series_id)
        if not ep_dir:
            return
        ep_dir.mkdir(parents=True, exist_ok=True)
        filename = f"E{episode_num:02d}_{title}.txt"
        (ep_dir / filename).write_text(content, encoding="utf-8")

    def _read_episode_file(self, series_id: str, episode_num: int) -> Optional[str]:
        """从.txt文件读取集文案正文"""
        ep_dir = self._episode_dir(series_id)
        if not ep_dir or not ep_dir.exists():
            return None
        for f in ep_dir.glob(f"E{episode_num:02d}_*.txt"):
            return f.read_text(encoding="utf-8")
        return None

    # ── 行为规则 ──────────────────────────────────────────

    def _resolve_behavior_file(self, filename: str) -> Optional[Path]:
        """
        定位行为规则文件：私有层优先 > 公共层

        知识库集/私有/公共行为/{filename}  优先
        知识库集/公共/公共行为/{filename}  其次
        """
        if not self.data_dir:
            return None
        private = self.data_dir / "知识库集" / "私有" / "公共行为" / filename
        if private.exists():
            return private
        public = self.data_dir / "知识库集" / "公共" / "公共行为" / filename
        if public.exists():
            return public
        # 兼容旧目录（无公共/私有层）
        old = self.data_dir / "知识库集" / "公共行为" / filename
        if old.exists():
            return old
        return None

    def load_behavior_rules(self) -> dict:
        """
        加载公共行为规则（允许行为 + 禁止行为）

        文件定位：私有层优先 > 公共层 > 旧目录
        冲突处理：允许 > 禁止。若禁止规则的pattern中有词与允许规则重叠，
        该条禁止规则被覆盖（从返回结果中移除，原文件不变）。

        返回 {"allowed": [...], "forbidden": [...], "overridden": [被覆盖的禁止规则]}
        文件不存在时返回空列表，不影响正常流程
        """
        result = {"allowed": [], "forbidden": [], "overridden": []}

        for key, filename in [("allowed", "允许行为.json"), ("forbidden", "禁止行为.json")]:
            fpath = self._resolve_behavior_file(filename)
            if fpath:
                try:
                    data = json.loads(fpath.read_text(encoding="utf-8"))
                    result[key] = data.get("rules", [])
                except (json.JSONDecodeError, OSError):
                    pass

        # 冲突处理：允许 > 禁止
        # 收集允许规则中所有pattern词（展开 | 分隔）
        allowed_words = set()
        for rule in result["allowed"]:
            pattern = rule.get("pattern", "")
            for word in pattern.split("|"):
                w = word.strip()
                if w:
                    allowed_words.add(w)

        # 检查禁止规则：pattern中有任何词在允许词中，则该条被覆盖
        remaining_forbidden = []
        for rule in result["forbidden"]:
            pattern = rule.get("pattern", "")
            rule_words = [w.strip() for w in pattern.split("|") if w.strip()]
            # 若有任何一个词在允许词中，整条规则被覆盖
            if any(w in allowed_words for w in rule_words):
                rule["_overridden_by"] = [w for w in rule_words if w in allowed_words]
                result["overridden"].append(rule)
            else:
                remaining_forbidden.append(rule)

        result["forbidden"] = remaining_forbidden
        return result

    def save_behavior_rules(self, rules_type: str, rules: list) -> dict:
        """
        保存行为规则到私有层文件

        用户修改行为规则时写入私有层，私有层优先级高于公共层，
        云端同步不会覆盖用户的定制。

        rules_type: "allowed" 或 "forbidden"
        rules: 规则列表，每条规则为dict
        """
        if not self.data_dir:
            return {"status": "error", "message": "未设置data_dir"}

        # 写入私有层，云端同步不会碰私有层
        behavior_dir = self.data_dir / "知识库集" / "私有" / "公共行为"
        behavior_dir.mkdir(parents=True, exist_ok=True)

        filename = "允许行为.json" if rules_type == "allowed" else "禁止行为.json"
        description = ("文案中必须遵守的用词和表述规则，生成文案时逐条执行"
                       if rules_type == "allowed"
                       else "文案中严格禁止的用词和表述，违反将导致法律风险或品牌损害")

        data = {"description": description, "rules": rules}
        fpath = behavior_dir / filename
        fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": "ok", "file": str(fpath), "count": len(rules)}

    # ── 公开接口 ──────────────────────────────────────────

    def get_generation_context(self, lecturer_id: str, topic: str,
                                knowledge_query: str = None,
                                series_id: str = None,
                                max_knowledge_tokens: int = 1000) -> dict:
        """
        获取文案生成所需的全部上下文（token优化版）

        返回：
        - profile: 轻量画像（~400 tokens）
        - reference_samples: 参考示例
        - knowledge_context: 精准知识段落（token预算内）
        - series_summaries: 当前系列摘要（若指定series_id）
        - behavior_rules: 公共行为规则（允许+禁止）
        - 不包含：quantitative（省~1500 tokens）
        """
        # 轻量画像
        profile = self.lecturer_svc.get_lite(lecturer_id)

        # 参考示例
        references = self.lecturer_svc.get_reference_samples(lecturer_id) if lecturer_id else []

        # 知识库精准检索
        knowledge = ""
        if knowledge_query:
            knowledge = self.knowledge_svc.get_relevant_context(
                knowledge_query, max_tokens=max_knowledge_tokens
            )

        # 系列摘要（连续性）
        series_summaries = None
        if series_id:
            series_summaries = self.get_episode_summaries(series_id)

        # 公共行为规则
        behavior_rules = self.load_behavior_rules()

        return {
            "profile": profile,
            "reference_samples": references,
            "knowledge_context": knowledge,
            "series_summaries": series_summaries,
            "behavior_rules": behavior_rules,
        }

    def create_series_plan(self, series_id: str, lecturer_id: str,
                           title: str, plan: dict) -> dict:
        """保存系列计划到DB"""
        now = datetime.now().isoformat(timespec="seconds")
        total = len(plan.get("episodes", []))
        self.db.execute(
            "INSERT OR REPLACE INTO series_plans "
            "(series_id, lecturer_id, title, plan_json, total_episodes, completed, "
            "created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (series_id, lecturer_id, title,
             json.dumps(plan, ensure_ascii=False), total, 0, now, now),
        )
        self.db.commit()
        return {"status": "ok", "series_id": series_id, "total_episodes": total}

    def get_series_plan(self, series_id: str) -> Optional[dict]:
        """获取系列计划"""
        row = self.db.query_one(
            "SELECT * FROM series_plans WHERE series_id=?", (series_id,)
        )
        if not row:
            return None
        return dict(row)

    def save_episode(self, series_id: str, episode_num: int, title: str,
                     content: str, summary: str = "", hook_next: str = "",
                     word_count: int = 0) -> dict:
        """
        保存一集文案
        
        正文直接写.txt文件（纯正文，用户直接看/编辑），
        DB只存元数据（摘要、hook_next、字数）供连续性查询用。
        """
        now = datetime.now().isoformat(timespec="seconds")
        # 自动计算字数
        if word_count <= 0 and content:
            word_count = sum(1 for c in content if "\u4e00" <= c <= "\u9fff" or c.isalpha())
        # DB存元数据（不含content）
        self.db.execute(
            "INSERT OR REPLACE INTO episodes "
            "(series_id, episode_num, title, summary, hook_next, word_count, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (series_id, episode_num, title, summary, hook_next, word_count, now),
        )
        # 更新计划进度（取已有最大集号，修订中间集不会把进度倒退）
        max_row = self.db.query_one(
            "SELECT MAX(episode_num) AS max_ep FROM episodes WHERE series_id=?",
            (series_id,),
        )
        max_ep = max_row["max_ep"] if max_row and max_row["max_ep"] else episode_num
        self.db.execute(
            "UPDATE series_plans SET completed=?, updated_at=? WHERE series_id=?",
            (max_ep, now, series_id),
        )
        self.db.commit()
        # 正文写.txt文件（纯正文）
        self._write_episode_file(series_id, episode_num, title, content)
        return {"status": "ok", "series_id": series_id, "episode_num": episode_num}

    def delete_episode(self, series_id: str, episode_num: int) -> dict:
        """
        删除一集文案（DB元数据 + .txt文件）

        用于修订流程：先 delete_episode 清旧数据，再 save_episode 写新数据。
        也可用于直接删除某一集。
        """
        # 删除DB元数据
        self.db.execute(
            "DELETE FROM episodes WHERE series_id=? AND episode_num=?",
            (series_id, episode_num),
        )
        # 更新计划进度（取剩余最大集号）
        max_row = self.db.query_one(
            "SELECT MAX(episode_num) AS max_ep FROM episodes WHERE series_id=?",
            (series_id,),
        )
        max_ep = max_row["max_ep"] if max_row and max_row["max_ep"] else 0
        now = datetime.now().isoformat(timespec="seconds")
        self.db.execute(
            "UPDATE series_plans SET completed=?, updated_at=? WHERE series_id=?",
            (max_ep, now, series_id),
        )
        self.db.commit()
        # 删除.txt文件
        ep_dir = self._episode_dir(series_id)
        if ep_dir.exists():
            for f in ep_dir.iterdir():
                if f.name.startswith(f"E{episode_num:02d}_") and f.suffix == ".txt":
                    f.unlink()
                    break
        return {"status": "deleted", "series_id": series_id, "episode_num": episode_num}

    def get_episode_summaries(self, series_id: str,
                               up_to: int = None) -> List[dict]:
        """
        获取系列文案摘要（连续性用）

        核心优化：只读summary+hook，不读全文
        每集约100字摘要 vs 600字全文，节省83% tokens
        """
        sql = "SELECT episode_num, title, summary, hook_prev, hook_next, word_count " \
              "FROM episodes WHERE series_id=?"
        params = [series_id]
        if up_to:
            sql += " AND episode_num <= ?"
            params.append(up_to)
        sql += " ORDER BY episode_num"

        rows = self.db.query_all(sql, tuple(params))
        return [dict(r) for r in rows]

    def get_episode_content(self, series_id: str, episode_num: int) -> Optional[str]:
        """获取单集全文：从文件读"""
        return self._read_episode_file(series_id, episode_num)

    def get_series_progress(self, series_id: str) -> Optional[dict]:
        """获取系列进度"""
        row = self.db.query_one(
            "SELECT series_id, title, total_episodes, completed, updated_at "
            "FROM series_plans WHERE series_id=?",
            (series_id,),
        )
        if not row:
            return None
        return dict(row)

    def list_series(self, lecturer_id: str = None) -> list:
        """列出系列计划"""
        if lecturer_id:
            rows = self.db.query_all(
                "SELECT series_id, title, total_episodes, completed, updated_at "
                "FROM series_plans WHERE lecturer_id=?",
                (lecturer_id,),
            )
        else:
            rows = self.db.query_all(
                "SELECT series_id, title, total_episodes, completed, updated_at "
                "FROM series_plans"
            )
        return [dict(r) for r in rows]
