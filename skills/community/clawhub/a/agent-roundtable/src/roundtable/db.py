"""SQLite database layer for Roundtable.

Framework-agnostic: uses only stdlib sqlite3 + dataclasses from models.
DB path resolution: ROUNDTABLE_DB env var > ~/.roundtable/roundtable.db
"""

from __future__ import annotations

import json
import os
import secrets
import sqlite3
import time
from pathlib import Path
from typing import Any

from roundtable.exceptions import (
    DiscussionNotActiveError,
    DiscussionNotFoundError,
    InvalidFindingTypeError,
    InvalidParticipantError,
    InvalidReplyToError,
    InvalidSpeechOrderError,
)
from roundtable.models import (
    ConvergenceRecord,
    Discussion,
    Finding,
    Participant,
    Speech,
)
from roundtable.schema import (
    SCHEMA_SQL,
    VALID_FINDING_TYPES,
    VALID_SPEECH_ORDERS,
    migrate_db,
)

# Constants and SCHEMA_SQL are imported from roundtable.schema


# ---------------------------------------------------------------------------
# RoundtableDB — the database access layer
# ---------------------------------------------------------------------------


class RoundtableDB:
    """SQLite-backed storage for roundtable discussions.

    Args:
        db_path: Explicit path to the SQLite file.
            Falls back to ``ROUNDTABLE_DB`` env var,
            then ``~/.roundtable/roundtable.db``.
    """

    def __init__(self, db_path: str | Path | None = None):
        if db_path:
            self._path = Path(db_path)
        else:
            env = os.environ.get("ROUNDTABLE_DB")
            if env:
                self._path = Path(env)
            else:
                self._path = Path.home() / ".roundtable" / "roundtable.db"
        self._initialized = False

    @property
    def db_path(self) -> Path:
        return self._path

    def connect(self) -> sqlite3.Connection:
        """Open (and initialize if needed) the roundtable DB.

        WAL mode + foreign keys on every connection.
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self._path), isolation_level=None, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA foreign_keys=ON")
        if not self._initialized:
            conn.executescript(SCHEMA_SQL)
            self._migrate(conn)
            self._initialized = True
        return conn

    def _migrate(self, conn: sqlite3.Connection) -> None:
        """Apply schema migrations for existing databases."""
        migrate_db(conn)

    # ------------------------------------------------------------------
    # Discussion CRUD
    # ------------------------------------------------------------------

    def create_discussion(
        self,
        conn: sqlite3.Connection,
        topic: str,
        participants: list[dict[str, Any]],
        *,
        context: str | None = None,
        max_rounds: int = 5,
        speech_order: str = "fixed",
        created_by: str = "unknown",
        output_path: str | None = None,
        notifications: dict[str, Any] | None = None,
    ) -> Discussion:
        if speech_order not in VALID_SPEECH_ORDERS:
            raise InvalidSpeechOrderError(f"Invalid speech_order: {speech_order}")
        if max_rounds < 1:
            raise ValueError("max_rounds must be >= 1")
        if not participants:
            raise ValueError("At least one participant is required")
        seen_profiles: set[str] = set()
        for p in participants:
            profile = p.get("profile", "").strip()
            if not profile:
                raise ValueError("Each participant must have a 'profile' field")
            if profile in seen_profiles:
                raise ValueError(f"Duplicate participant profile: {profile}")
            seen_profiles.add(profile)

        disc_id = f"rt_{secrets.token_hex(4)}"
        now = int(time.time())
        notif_json = json.dumps(notifications) if notifications else None

        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute(
                """INSERT INTO discussions
                   (id, topic, context, status, max_rounds, current_round,
                    speech_order, created_by, created_at, output_path, notifications)
                   VALUES (?, ?, ?, 'active', ?, 0, ?, ?, ?, ?, ?)""",
                (disc_id, topic, context, max_rounds, speech_order, created_by, now, output_path, notif_json),
            )
            for p in participants:
                profile = p.get("profile", "").strip()
                conn.execute(
                    """INSERT INTO participants
                       (discussion_id, participant, role, perspective,
                        display_name, joined_at, is_active)
                       VALUES (?, ?, ?, ?, ?, ?, 1)""",
                    (disc_id, profile, p.get("role"), p.get("perspective"), p.get("display_name"), now),
                )
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

        return Discussion(
            id=disc_id,
            topic=topic,
            context=context,
            status="active",
            max_rounds=max_rounds,
            current_round=0,
            speech_order=speech_order,
            created_by=created_by,
            created_at=now,
            concluded_at=None,
            conclusion=None,
            convergence_score=None,
            output_path=output_path,
            notifications=notifications,
        )

    def get_discussion(self, conn: sqlite3.Connection, discussion_id: str) -> Discussion | None:
        row = conn.execute("SELECT * FROM discussions WHERE id = ?", (discussion_id,)).fetchone()
        if not row:
            return None
        return self._row_to_discussion(row)

    def list_discussions(
        self,
        conn: sqlite3.Connection,
        *,
        status: str | None = None,
        limit: int = 50,
    ) -> list[Discussion]:
        if status:
            rows = conn.execute(
                "SELECT * FROM discussions WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                (status, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM discussions ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._row_to_discussion(r) for r in rows]

    def conclude_discussion(
        self,
        conn: sqlite3.Connection,
        discussion_id: str,
        *,
        conclusion: str | None = None,
        convergence_score: float | None = None,
    ) -> bool:
        now = int(time.time())
        cur = conn.execute(
            """UPDATE discussions
               SET status = 'concluded', concluded_at = ?,
                   conclusion = COALESCE(?, conclusion),
                   convergence_score = COALESCE(?, convergence_score)
               WHERE id = ? AND status = 'active'""",
            (now, conclusion, convergence_score, discussion_id),
        )
        return cur.rowcount > 0

    def cancel_discussion(self, conn: sqlite3.Connection, discussion_id: str) -> bool:
        now = int(time.time())
        cur = conn.execute(
            """UPDATE discussions
               SET status = 'cancelled', concluded_at = ?
               WHERE id = ? AND status = 'active'""",
            (now, discussion_id),
        )
        return cur.rowcount > 0

    # ------------------------------------------------------------------
    # Participants
    # ------------------------------------------------------------------

    def get_participants(self, conn: sqlite3.Connection, discussion_id: str) -> list[Participant]:
        rows = conn.execute(
            "SELECT * FROM participants WHERE discussion_id = ? ORDER BY joined_at",
            (discussion_id,),
        ).fetchall()
        return [
            Participant(
                discussion_id=r["discussion_id"],
                participant=r["participant"],
                role=r["role"],
                perspective=r["perspective"],
                display_name=r["display_name"],
                joined_at=r["joined_at"],
                is_active=bool(r["is_active"]),
            )
            for r in rows
        ]

    def get_active_participant_names(self, conn: sqlite3.Connection, discussion_id: str) -> list[str]:
        rows = conn.execute(
            """SELECT participant FROM participants
               WHERE discussion_id = ? AND is_active = 1
               ORDER BY joined_at""",
            (discussion_id,),
        ).fetchall()
        return [r["participant"] for r in rows]

    # ------------------------------------------------------------------
    # Speeches
    # ------------------------------------------------------------------

    def add_speech(
        self,
        conn: sqlite3.Connection,
        discussion_id: str,
        participant: str,
        content: str,
        *,
        reply_to: int | None = None,
    ) -> dict[str, Any]:
        """Add a speech and return result with speech + round metadata.

        Round 0 is reserved for the coordinator opening statement. Once that
        opening is recorded, participant discussion starts at round 1.

        Returns dict with: speech (Speech), round_complete (bool),
        discussion_complete (bool), next_speaker (str|None).
        """
        disc = self.get_discussion(conn, discussion_id)
        if not disc:
            raise DiscussionNotFoundError(f"Discussion {discussion_id} not found")
        if disc.status != "active":
            raise DiscussionNotActiveError(f"Discussion {discussion_id} is {disc.status}")

        now = int(time.time())
        current_round = disc.current_round
        speech_round = current_round

        if current_round == 0 and participant != "coordinator":
            raise InvalidParticipantError("Round 0 is reserved for the coordinator opening statement")

        if reply_to is not None:
            ref = conn.execute(
                "SELECT id FROM speeches WHERE id = ? AND discussion_id = ?",
                (reply_to, discussion_id),
            ).fetchone()
            if not ref:
                raise InvalidReplyToError(f"reply_to speech {reply_to} not found in discussion {discussion_id}")

        conn.execute("BEGIN IMMEDIATE")
        try:
            cur = conn.execute(
                """INSERT INTO speeches
                   (discussion_id, round, participant, content, reply_to, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (discussion_id, speech_round, participant, content, reply_to, now),
            )
            speech_id = cur.lastrowid

            active_names = self.get_active_participant_names(conn, discussion_id)
            round_complete = False
            discussion_complete = False

            if participant == "coordinator" and current_round == 0:
                round_complete = True
            else:
                # Check if all active participants have spoken in this round.
                speakers_this_round = conn.execute(
                    """SELECT DISTINCT participant FROM speeches
                       WHERE discussion_id = ? AND round = ?""",
                    (discussion_id, current_round),
                ).fetchall()
                spoke_names = {r["participant"] for r in speakers_this_round}
                round_complete = all(name in spoke_names for name in active_names)

            if round_complete:
                new_round = current_round + 1
                conn.execute(
                    "UPDATE discussions SET current_round = ? WHERE id = ?",
                    (new_round, discussion_id),
                )
                if new_round > disc.max_rounds:
                    conn.execute(
                        """UPDATE discussions
                           SET status = 'concluded', concluded_at = ?
                           WHERE id = ? AND status = 'active'""",
                        (now, discussion_id),
                    )
                    discussion_complete = True

            # Determine next speaker based on the CURRENT round (post-advance)
            disc_after = self.get_discussion(conn, discussion_id)
            target_round = disc_after.current_round if disc_after else current_round
            next_speaker = None
            if not discussion_complete and active_names and disc.speech_order == "fixed":
                speakers_next = conn.execute(
                    """SELECT DISTINCT participant FROM speeches
                       WHERE discussion_id = ? AND round = ?""",
                    (discussion_id, target_round),
                ).fetchall()
                spoke_next = {r["participant"] for r in speakers_next}
                for name in active_names:
                    if name not in spoke_next:
                        next_speaker = name
                        break

            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

        speech = Speech(
            id=speech_id or 0,
            discussion_id=discussion_id,
            round=speech_round,
            participant=participant,
            content=content,
            reply_to=reply_to,
            created_at=now,
        )
        return {
            "speech": speech,
            "round_complete": round_complete,
            "discussion_complete": discussion_complete,
            "next_speaker": next_speaker,
        }

    def get_speeches(
        self,
        conn: sqlite3.Connection,
        discussion_id: str,
        *,
        since_round: int | None = None,
        participant: str | None = None,
    ) -> list[Speech]:
        query = "SELECT * FROM speeches WHERE discussion_id = ?"
        params: list[Any] = [discussion_id]
        if since_round is not None:
            query += " AND round >= ?"
            params.append(since_round)
        if participant:
            query += " AND participant = ?"
            params.append(participant)
        query += " ORDER BY id ASC"
        rows = conn.execute(query, params).fetchall()
        return [
            Speech(
                id=r["id"],
                discussion_id=r["discussion_id"],
                round=r["round"],
                participant=r["participant"],
                content=r["content"],
                reply_to=r["reply_to"],
                created_at=r["created_at"],
            )
            for r in rows
        ]

    def get_speech_count(self, conn: sqlite3.Connection, discussion_id: str) -> int:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM speeches WHERE discussion_id = ?",
            (discussion_id,),
        ).fetchone()
        return row["cnt"] if row else 0

    # ------------------------------------------------------------------
    # Findings
    # ------------------------------------------------------------------

    def add_finding(
        self,
        conn: sqlite3.Connection,
        discussion_id: str,
        finding_type: str,
        content: str,
        round_num: int,
        related_speeches: list[int] | None = None,
    ) -> int:
        if finding_type not in VALID_FINDING_TYPES:
            raise InvalidFindingTypeError(f"Invalid finding type: {finding_type}")
        rs_json = json.dumps(related_speeches) if related_speeches else None
        cur = conn.execute(
            """INSERT INTO findings
               (discussion_id, type, content, round, related_speeches)
               VALUES (?, ?, ?, ?, ?)""",
            (discussion_id, finding_type, content, round_num, rs_json),
        )
        return cur.lastrowid or 0

    def get_findings(
        self,
        conn: sqlite3.Connection,
        discussion_id: str,
        *,
        finding_type: str | None = None,
    ) -> list[Finding]:
        if finding_type:
            rows = conn.execute(
                """SELECT * FROM findings
                   WHERE discussion_id = ? AND type = ?
                   ORDER BY id ASC""",
                (discussion_id, finding_type),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM findings WHERE discussion_id = ? ORDER BY id ASC",
                (discussion_id,),
            ).fetchall()
        return [
            Finding(
                id=r["id"],
                discussion_id=r["discussion_id"],
                type=r["type"],
                content=r["content"],
                round=r["round"],
                related_speeches=json.loads(r["related_speeches"]) if r["related_speeches"] else None,
            )
            for r in rows
        ]

    # ------------------------------------------------------------------
    # Convergence
    # ------------------------------------------------------------------

    def record_convergence(
        self,
        conn: sqlite3.Connection,
        discussion_id: str,
        round_num: int,
        score: float,
        consensus_count: int,
        disagreement_count: int,
        new_point_count: int,
    ) -> None:
        conn.execute(
            """INSERT OR REPLACE INTO convergence_history
               (discussion_id, round, score, consensus_count,
                disagreement_count, new_point_count)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (discussion_id, round_num, score, consensus_count, disagreement_count, new_point_count),
        )

    def get_convergence_history(self, conn: sqlite3.Connection, discussion_id: str) -> list[ConvergenceRecord]:
        rows = conn.execute(
            """SELECT * FROM convergence_history
               WHERE discussion_id = ? ORDER BY round ASC""",
            (discussion_id,),
        ).fetchall()
        return [
            ConvergenceRecord(
                discussion_id=r["discussion_id"],
                round=r["round"],
                score=r["score"],
                consensus_count=r["consensus_count"],
                disagreement_count=r["disagreement_count"],
                new_point_count=r["new_point_count"],
            )
            for r in rows
        ]

    def advance_round(self, conn: sqlite3.Connection, discussion_id: str) -> dict[str, Any]:
        """Explicitly advance to the next round.

        Returns dict with new_round, discussion_complete, max_rounds.
        Raises DiscussionNotFoundError / DiscussionNotActiveError.
        """
        disc = self.get_discussion(conn, discussion_id)
        if not disc:
            raise DiscussionNotFoundError(f"Discussion {discussion_id} not found")
        if disc.status != "active":
            raise DiscussionNotActiveError(f"Discussion {discussion_id} is {disc.status}")

        now = int(time.time())
        new_round = disc.current_round + 1
        discussion_complete = False

        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute(
                "UPDATE discussions SET current_round = ? WHERE id = ?",
                (new_round, discussion_id),
            )
            if new_round > disc.max_rounds:
                conn.execute(
                    """UPDATE discussions
                       SET status = 'concluded', concluded_at = ?
                       WHERE id = ? AND status = 'active'""",
                    (now, discussion_id),
                )
                discussion_complete = True
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise

        return {
            "new_round": new_round,
            "max_rounds": disc.max_rounds,
            "discussion_complete": discussion_complete,
        }

    def calculate_convergence(self, conn: sqlite3.Connection, discussion_id: str, round_num: int) -> float | None:
        """Calculate convergence score for a given round from its findings.

        Score = consensus_count / (consensus_count + disagreement_count).
        Returns None if no findings exist for the round.
        """
        rows = conn.execute(
            """SELECT type, COUNT(*) as cnt FROM findings
               WHERE discussion_id = ? AND round = ?
               GROUP BY type""",
            (discussion_id, round_num),
        ).fetchall()
        counts = {r["type"]: r["cnt"] for r in rows}
        consensus = int(counts.get("consensus", 0))
        disagreement = int(counts.get("disagreement", 0))
        new_points = counts.get("new_point", 0)

        total = consensus + disagreement
        if total == 0:
            return None

        score = consensus / total

        # Record in convergence_history
        self.record_convergence(
            conn,
            discussion_id,
            round_num,
            score,
            consensus,
            disagreement,
            new_points,
        )

        # Update the discussion's overall convergence_score (latest round)
        conn.execute(
            "UPDATE discussions SET convergence_score = ? WHERE id = ?",
            (score, discussion_id),
        )

        return score

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_discussion(row: sqlite3.Row) -> Discussion:
        notif_raw = row["notifications"]
        try:
            notif = json.loads(notif_raw) if notif_raw else None
        except json.JSONDecodeError:
            notif = None
        return Discussion(
            id=row["id"],
            topic=row["topic"],
            context=row["context"],
            status=row["status"],
            max_rounds=row["max_rounds"],
            current_round=row["current_round"],
            speech_order=row["speech_order"],
            created_by=row["created_by"],
            created_at=row["created_at"],
            concluded_at=row["concluded_at"],
            conclusion=row["conclusion"],
            convergence_score=row["convergence_score"],
            output_path=row["output_path"],
            notifications=notif,
        )
