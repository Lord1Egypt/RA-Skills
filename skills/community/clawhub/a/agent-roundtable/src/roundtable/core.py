"""Core business logic for Roundtable discussions.

Framework-agnostic: uses only RoundtableDB + models. No agent-framework
imports. All handlers return plain dicts (JSON-serializable).
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

from roundtable.db import RoundtableDB
from roundtable.demo import (
    DEMO_FINDINGS,
    DEMO_PARTICIPANTS,
    DEMO_SPEECHES,
    DEMO_TOPIC,
)
from roundtable.exceptions import (
    DiscussionNotActiveError,
    DiscussionNotFoundError,
    InvalidParticipantError,
)
from roundtable.models import ConvergenceRecord, Discussion, Participant, Speech
from roundtable.notify import Notifier

logger = logging.getLogger(__name__)


class RoundtableCore:
    """High-level discussion operations.

    Wraps RoundtableDB with validation, round progression logic,
    and result formatting. Each method returns a JSON-serializable dict.

    Args:
        db: A RoundtableDB instance (uses default if None).
        send_fn: Optional callback(platform, chat_id, message) for notifications.
    """

    def __init__(self, db: RoundtableDB | None = None, send_fn: Any = None):
        self.db = db or RoundtableDB()
        self._send_fn = send_fn
        self._publishers: dict[str, Any] = {}  # discussion_id → WebPublisher
        self._stream_delay: float = 0.0  # 每个 token chunk 之间的延迟（秒）

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_discussion(
        self,
        topic: str,
        participants: list[dict[str, Any]],
        *,
        context: str | None = None,
        max_rounds: int = 5,
        speech_order: str = "fixed",
        created_by: str = "coordinator",
        output_path: str | None = None,
        notifications: dict[str, Any] | None = None,
        web: bool = False,
        web_port: int = 8199,
    ) -> dict[str, Any]:
        """Create a new roundtable discussion.

        Returns dict with discussion_id, topic, participants, etc.
        Raises ValueError / RoundtableError on validation failure.
        """
        if not topic or not topic.strip():
            raise ValueError("topic is required")
        if not participants or not isinstance(participants, list):
            raise ValueError("participants must be a non-empty array of objects")
        if len(participants) < 2:
            raise ValueError("At least 2 participants are required for a discussion")

        try:
            max_rounds = int(max_rounds)
        except (TypeError, ValueError) as err:
            raise ValueError("max_rounds must be an integer") from err

        conn = self.db.connect()
        try:
            disc = self.db.create_discussion(
                conn,
                topic=topic.strip(),
                participants=participants,
                context=context,
                max_rounds=max_rounds,
                speech_order=speech_order,
                created_by=created_by,
                output_path=output_path,
                notifications=notifications,
            )

            # Optionally start web viewer
            web_url = None
            if web:
                from roundtable.web_publisher import WebPublisher

                output_dir = os.path.join("/tmp", "roundtable_web", disc.id)
                try:
                    publisher = WebPublisher(output_dir, port=web_port)
                    web_url = publisher.start(
                        disc.id,
                        topic=topic.strip(),
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
                except Exception as exc:
                    logger.exception("Failed to start web viewer for discussion %s", disc.id)
                    raise RuntimeError(f"Failed to start web viewer: {exc}") from exc
                self._publishers[disc.id] = publisher
                logger.info("Web viewer started for discussion %s: %s", disc.id, web_url)

            return {
                "ok": True,
                "discussion_id": disc.id,
                "topic": disc.topic,
                "participants": [p.get("profile") for p in participants],
                "max_rounds": disc.max_rounds,
                "speech_order": disc.speech_order,
                "status": disc.status,
                "web_url": web_url,
            }
        finally:
            conn.close()

    def speak(
        self,
        discussion_id: str,
        participant: str,
        content: str,
        *,
        reply_to: int | None = None,
    ) -> dict[str, Any]:
        """Record a participant's speech.

        Returns dict with speech_id, round, next_speaker, etc.
        """
        if not discussion_id:
            raise ValueError("discussion_id is required")
        if not participant:
            raise ValueError("participant is required")
        if not content or not content.strip():
            raise ValueError("content is required")

        if reply_to is not None:
            try:
                reply_to = int(reply_to)
            except (TypeError, ValueError) as err:
                raise ValueError("reply_to must be an integer") from err

        conn = self.db.connect()
        try:
            disc = self.db.get_discussion(conn, discussion_id)
            if not disc:
                raise DiscussionNotFoundError(f"Discussion {discussion_id} not found")
            if disc.status != "active":
                raise DiscussionNotActiveError(f"Discussion {discussion_id} is {disc.status}")

            active_names = self.db.get_active_participant_names(conn, discussion_id)
            is_coordinator = participant == "coordinator"
            if not is_coordinator and participant not in active_names:
                raise InvalidParticipantError(
                    f"Participant '{participant}' is not an active member of this discussion. "
                    f"Active: {', '.join(active_names)}"
                )
            if is_coordinator and disc.current_round == 0:
                existing_opening = conn.execute(
                    """SELECT id FROM speeches
                       WHERE discussion_id = ? AND round = 0 AND participant = 'coordinator'
                       LIMIT 1""",
                    (discussion_id,),
                ).fetchone()
                if existing_opening:
                    raise InvalidParticipantError("Coordinator opening statement already exists for this discussion")

            result = self.db.add_speech(
                conn,
                discussion_id=discussion_id,
                participant=participant,
                content=content.strip(),
                reply_to=reply_to,
            )
            speech = result["speech"]
            round_complete = result["round_complete"]
            discussion_complete = result["discussion_complete"]
            next_speaker = result["next_speaker"]

            # Auto-calculate convergence when a round completes
            convergence_score = None
            if round_complete and speech.round > 0:
                convergence_score = self.db.calculate_convergence(conn, discussion_id, speech.round)

            # --- Notifications ---
            notifier = self._make_notifier(disc.notifications)
            participants = self.db.get_participants(conn, discussion_id)
            p_map = {p.participant: p for p in participants}

            # --- Web publisher hook (streaming + v1 兼容) ---
            publisher = self._publishers.get(discussion_id)
            p_info = p_map.get(speech.participant)
            speech_data = {
                "id": speech.id,
                "round": speech.round,
                "participant": speech.participant,
                "display_name": p_info.display_name if p_info else speech.participant,
                "content": speech.content,
                "created_at": speech.created_at,
            }
            if publisher:
                try:
                    # 流式推送：speech_start → speech_token(s) → speech_end
                    avatar = publisher._avatar_for_participant(speech.participant)
                    display_name = p_info.display_name if p_info else speech.participant
                    role = p_info.role if p_info else ""
                    title = publisher._title_for_participant(speech.participant)
                    description = publisher._description_for_participant(speech.participant)
                    publisher.on_speech_start(
                        speech.id,
                        speech.participant,
                        avatar=avatar,
                        round_num=speech.round,
                        display_name=display_name,
                        role=role,
                        title=title if title else None,
                        description=description if description else None,
                    )
                    # 逐 token 推送（中文按 2-4 字符分块，模拟自然流式）
                    content = speech.content
                    chunk_size = 3  # 每次推送 3 个字符
                    token_seq = 0
                    import time as _time

                    for i in range(0, len(content), chunk_size):
                        token_seq += 1
                        publisher.on_speech_token(speech.id, content[i : i + chunk_size], seq=token_seq)
                        if self._stream_delay > 0:
                            _time.sleep(self._stream_delay)
                    publisher.on_speech_end(speech.id, total_tokens=token_seq)

                    # 保留 v1 兼容：也推送完整 speech 事件
                    publisher.on_speech(speech_data)
                except Exception:
                    logger.exception(f"Web publisher streaming failed for {discussion_id}")
            else:
                # Publisher not in memory (cross-process) — update discussion.json directly
                self._update_web_discussion_json(discussion_id, speech_data, disc.topic, participants)

            # Speech notification
            p_info = p_map.get(speech.participant)
            notifier.notify(
                "speech",
                discussion_id=discussion_id,
                topic=disc.topic,
                participant=speech.participant,
                display_name=p_info.display_name if p_info else speech.participant,
                role=p_info.role if p_info else "",
                round_num=speech.round,
                content=speech.content,
            )

            # Check if this is the first speech in a new round (round_start)
            if speech.round > 0 and not round_complete:
                speeches_this_round = self.db.get_speeches(conn, discussion_id, since_round=speech.round)
                # Filter to current round only
                round_speeches = [s for s in speeches_this_round if s.round == speech.round]
                if len(round_speeches) == 1:
                    # First speech in this round — fire round_start
                    notifier.notify(
                        "round_start",
                        discussion_id=discussion_id,
                        topic=disc.topic,
                        round_num=speech.round,
                    )

            # Round complete notification + streaming viewpoint event
            if round_complete and speech.round > 0:
                # Get key points from this round
                findings = self.db.get_findings(conn, discussion_id)
                round_findings = [f for f in findings if f.round == speech.round]
                key_points = [f.content for f in round_findings]
                notifier.notify(
                    "round_end",
                    discussion_id=discussion_id,
                    topic=disc.topic,
                    round_num=speech.round,
                    convergence=convergence_score,
                    key_points=key_points,
                )

                # 流式推送：轮次观点汇总
                publisher = self._publishers.get(discussion_id)
                if publisher:
                    try:
                        consensus_pts = [f.content for f in round_findings if f.type == "consensus"]
                        disagreement_pts = [f.content for f in round_findings if f.type == "disagreement"]
                        publisher.on_round_summary(
                            round_num=speech.round,
                            consensus=[{"content": p} for p in consensus_pts],
                            disagreement=[{"content": p} for p in disagreement_pts],
                        )
                    except Exception:
                        logger.exception("Web publisher on_round_summary failed for %s", discussion_id)

            # Discussion auto-concluded notification
            if discussion_complete:
                disc_after = self.db.get_discussion(conn, discussion_id)
                if disc_after:
                    self._notify_concluded(conn, disc_after, notifier)
                    if disc_after.output_path:
                        self._write_markdown_output(
                            disc_after.output_path,
                            self._build_output_markdown(conn, disc_after),
                        )

                    publisher = self._publishers.get(discussion_id)
                    if publisher:
                        try:
                            # 流式推送：最终观点总结
                            findings = self.db.get_findings(conn, discussion_id)
                            consensus_pts = [f.content for f in findings if f.type == "consensus"]
                            disagreement_pts = [f.content for f in findings if f.type == "disagreement"]
                            publisher.on_final_summary(
                                consensus=[{"content": p} for p in consensus_pts],
                                disagreement=[{"content": p} for p in disagreement_pts],
                                verdict=disc_after.conclusion or "",
                            )
                            publisher.conclude(disc_after.conclusion or "")
                        except Exception:
                            logger.exception("Web publisher conclude failed for auto-concluded %s", discussion_id)
                    else:
                        self._conclude_web_discussion(discussion_id, disc_after.conclusion or "")

            return {
                "ok": True,
                "speech_id": speech.id,
                "round": speech.round,
                "participant": speech.participant,
                "next_speaker": next_speaker,
                "round_complete": round_complete,
                "discussion_complete": discussion_complete,
                "convergence_score": convergence_score,
            }
        finally:
            conn.close()

    def read(
        self,
        discussion_id: str,
        *,
        since_round: int | None = None,
        participant: str | None = None,
    ) -> dict[str, Any]:
        """Read discussion history (speeches)."""
        if not discussion_id:
            raise ValueError("discussion_id is required")

        if since_round is not None:
            try:
                since_round = int(since_round)
            except (TypeError, ValueError) as err:
                raise ValueError("since_round must be an integer") from err

        conn = self.db.connect()
        try:
            disc = self.db.get_discussion(conn, discussion_id)
            if not disc:
                raise DiscussionNotFoundError(f"Discussion {discussion_id} not found")

            speeches = self.db.get_speeches(
                conn,
                discussion_id,
                since_round=since_round,
                participant=participant,
            )
            participants = self.db.get_participants(conn, discussion_id)
            p_map = {
                p.participant: {
                    "role": p.role,
                    "display_name": p.display_name,
                    "perspective": p.perspective,
                }
                for p in participants
            }

            return {
                "ok": True,
                "discussion_id": disc.id,
                "topic": disc.topic,
                "current_round": disc.current_round,
                "max_rounds": disc.max_rounds,
                "status": disc.status,
                "speeches": [
                    {
                        "id": s.id,
                        "round": s.round,
                        "participant": s.participant,
                        "display_name": p_map.get(s.participant, {}).get("display_name"),
                        "content": s.content,
                        "reply_to": s.reply_to,
                        "created_at": s.created_at,
                    }
                    for s in speeches
                ],
                "speech_count": len(speeches),
                "formatted_history": self._format_history(speeches, p_map),
            }
        finally:
            conn.close()

    def status(self, discussion_id: str) -> dict[str, Any]:
        """Get discussion status including convergence metrics."""
        if not discussion_id:
            raise ValueError("discussion_id is required")

        conn = self.db.connect()
        try:
            disc = self.db.get_discussion(conn, discussion_id)
            if not disc:
                raise DiscussionNotFoundError(f"Discussion {discussion_id} not found")

            participants = self.db.get_participants(conn, discussion_id)
            speech_count = self.db.get_speech_count(conn, discussion_id)
            findings = self.db.get_findings(conn, discussion_id)
            conv_history = self.db.get_convergence_history(conn, discussion_id)

            consensus_pts = [f.content for f in findings if f.type == "consensus"]
            disagreement_pts = [f.content for f in findings if f.type == "disagreement"]
            new_points = [f.content for f in findings if f.type == "new_point"]

            active_names = self.db.get_active_participant_names(conn, discussion_id)
            next_speaker = None
            if disc.status == "active" and active_names:
                speakers_current = conn.execute(
                    """SELECT DISTINCT participant FROM speeches
                       WHERE discussion_id = ? AND round = ?""",
                    (discussion_id, disc.current_round),
                ).fetchall()
                spoke = {r["participant"] for r in speakers_current}
                for name in active_names:
                    if name not in spoke:
                        next_speaker = name
                        break

            return {
                "ok": True,
                "discussion_id": disc.id,
                "topic": disc.topic,
                "status": disc.status,
                "current_round": disc.current_round,
                "max_rounds": disc.max_rounds,
                "speech_order": disc.speech_order,
                "convergence_score": disc.convergence_score,
                "consensus_points": consensus_pts,
                "disagreement_points": disagreement_pts,
                "new_points": new_points,
                "speech_count": speech_count,
                "participant_count": len(participants),
                "next_speaker": next_speaker,
                "convergence_history": [
                    {
                        "round": c.round,
                        "score": c.score,
                        "consensus": c.consensus_count,
                        "disagreement": c.disagreement_count,
                        "new_points": c.new_point_count,
                    }
                    for c in conv_history
                ],
            }
        finally:
            conn.close()

    def summarize(self, discussion_id: str, *, compact: bool = False) -> dict[str, Any]:
        """Generate summary data for a conclusion document.

        Args:
            discussion_id: The discussion to summarize.
            compact: If True, omit raw rounds data and formatted_history
                to keep output small (<5KB). Use structured_summary instead.
        """
        if not discussion_id:
            raise ValueError("discussion_id is required")

        conn = self.db.connect()
        try:
            disc = self.db.get_discussion(conn, discussion_id)
            if not disc:
                raise DiscussionNotFoundError(f"Discussion {discussion_id} not found")

            participants = self.db.get_participants(conn, discussion_id)
            speeches = self.db.get_speeches(conn, discussion_id)
            findings = self.db.get_findings(conn, discussion_id)
            conv_history = self.db.get_convergence_history(conn, discussion_id)

            p_map = {
                p.participant: {
                    "role": p.role,
                    "display_name": p.display_name,
                    "perspective": p.perspective,
                }
                for p in participants
            }

            consensus_pts = [f.content for f in findings if f.type == "consensus"]
            disagreement_pts = [f.content for f in findings if f.type == "disagreement"]
            new_points = [f.content for f in findings if f.type == "new_point"]

            rounds_dict: dict[int, list[dict[str, Any]]] = {}
            for s in speeches:
                rounds_dict.setdefault(s.round, []).append(
                    {
                        "id": s.id,
                        "participant": s.participant,
                        "display_name": p_map.get(s.participant, {}).get("display_name"),
                        "role": p_map.get(s.participant, {}).get("role"),
                        "content": s.content,
                        "reply_to": s.reply_to,
                    }
                )

            final_score = disc.convergence_score
            if not final_score and conv_history:
                final_score = conv_history[-1].score

            # Build a structured summary — compact enough for LLM context,
            # rich enough to write a conclusion without re-reading raw speeches.
            structured_summary = self._build_structured_summary(
                disc,
                participants,
                speeches,
                p_map,
                consensus_pts,
                disagreement_pts,
                new_points,
                final_score,
                conv_history,
            )

            result = {
                "ok": True,
                "discussion_id": disc.id,
                "topic": disc.topic,
                "context": disc.context,
                "status": disc.status,
                "total_rounds": disc.current_round,
                "max_rounds": disc.max_rounds,
                "final_convergence_score": final_score,
                "participants": [
                    {
                        "profile": p.participant,
                        "display_name": p.display_name,
                        "role": p.role,
                        "perspective": p.perspective,
                    }
                    for p in participants
                ],
                "consensus_points": consensus_pts,
                "disagreement_points": disagreement_pts,
                "new_points": new_points,
                "speech_count": len(speeches),
                "convergence_history": [
                    {
                        "round": c.round,
                        "score": c.score,
                        "consensus": c.consensus_count,
                        "disagreement": c.disagreement_count,
                    }
                    for c in conv_history
                ],
                "output_path": disc.output_path,
                "structured_summary": structured_summary,
            }

            if disc.output_path:
                output_result = self._write_markdown_output(disc.output_path, structured_summary)
                result.update(output_result)

            if not compact:
                # Full data — includes all raw speech content
                result["rounds"] = rounds_dict
                result["formatted_history"] = self._format_history(speeches, p_map)

            return result
        finally:
            conn.close()

    def end_discussion(
        self,
        discussion_id: str,
        *,
        force: bool = False,
        conclusion: str | None = None,
    ) -> dict[str, Any]:
        """End a discussion (conclude or cancel)."""
        if not discussion_id:
            raise ValueError("discussion_id is required")

        conn = self.db.connect()
        try:
            disc = self.db.get_discussion(conn, discussion_id)
            if not disc:
                raise DiscussionNotFoundError(f"Discussion {discussion_id} not found")
            if disc.status != "active":
                if disc.status == "concluded" and not force and conclusion is not None:
                    conn.execute(
                        "UPDATE discussions SET conclusion = ? WHERE id = ?",
                        (conclusion, discussion_id),
                    )
                    disc_after = self.db.get_discussion(conn, discussion_id)
                    conclusion_output_result: dict[str, Any] = {}
                    if disc_after and disc_after.output_path:
                        conclusion_output_result = self._write_markdown_output(
                            disc_after.output_path,
                            self._build_output_markdown(conn, disc_after, conclusion_override=conclusion),
                        )

                    publisher = self._publishers.get(discussion_id)
                    web_retained = False
                    if publisher:
                        try:
                            # 流式推送：最终观点总结
                            findings = self.db.get_findings(conn, discussion_id)
                            consensus_pts = [f.content for f in findings if f.type == "consensus"]
                            disagreement_pts = [f.content for f in findings if f.type == "disagreement"]
                            publisher.on_final_summary(
                                consensus=[{"content": p} for p in consensus_pts],
                                disagreement=[{"content": p} for p in disagreement_pts],
                                verdict=conclusion or "",
                            )
                            publisher.conclude(conclusion)
                            web_retained = True
                        except Exception:
                            logger.exception("Web publisher conclude update failed for %s", discussion_id)
                    else:
                        self._conclude_web_discussion(discussion_id, conclusion)

                    result = {
                        "ok": True,
                        "discussion_id": discussion_id,
                        "action": "concluded",
                        "success": True,
                        "web_retained": web_retained,
                    }
                    result.update(conclusion_output_result)
                    return result
                raise DiscussionNotActiveError(f"Discussion {discussion_id} is already {disc.status}")

            if force:
                ok = self.db.cancel_discussion(conn, discussion_id)
                action = "cancelled"
            else:
                ok = self.db.conclude_discussion(conn, discussion_id, conclusion=conclusion)
                action = "concluded"

            # Fire concluded notification (only on conclude, not cancel)
            disc_after = None
            if action == "concluded":
                disc_after = self.db.get_discussion(conn, discussion_id)
                if disc_after:
                    notifier = self._make_notifier(disc.notifications)
                    self._notify_concluded(conn, disc_after, notifier)

            output_result: dict[str, Any] = {}
            if action == "concluded" and disc_after and disc_after.output_path:
                output_result = self._write_markdown_output(
                    disc_after.output_path,
                    self._build_output_markdown(conn, disc_after),
                )

            # Web publisher hook. A concluded viewer remains online for post-meeting
            # review; force-cancel still stops it immediately.
            publisher = self._publishers.get(discussion_id)
            web_retained = False
            if publisher:
                try:
                    if action == "concluded" and disc_after:
                        # 流式推送：最终观点总结
                        findings = self.db.get_findings(conn, discussion_id)
                        all_points = [f.content for f in findings]
                        publisher.on_final_summary(
                            consensus=[{"content": p} for p in all_points],
                            disagreement=[],
                            verdict=disc_after.conclusion or "",
                        )
                        publisher.conclude(disc_after.conclusion or "")
                        web_retained = True
                        logger.info("Web publisher retained for concluded discussion %s", discussion_id)
                    else:
                        self._publishers.pop(discussion_id, None)
                        publisher.stop()
                        logger.info("Web publisher stopped for %s", discussion_id)
                except Exception:
                    logger.exception(f"Web publisher cleanup failed for {discussion_id}")
            elif action == "concluded" and disc_after:
                # Cross-process: update discussion.json directly
                self._conclude_web_discussion(discussion_id, disc_after.conclusion or "")

            result = {
                "ok": True,
                "discussion_id": discussion_id,
                "action": action,
                "success": ok,
                "web_retained": web_retained,
            }
            result.update(output_result)
            return result
        finally:
            conn.close()

    def list_discussions(
        self,
        *,
        status: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        """List all discussions with optional status filter."""
        try:
            limit = int(limit)
        except (TypeError, ValueError) as err:
            raise ValueError("limit must be an integer") from err

        conn = self.db.connect()
        try:
            discussions = self.db.list_discussions(conn, status=status, limit=limit)
            return {
                "ok": True,
                "discussions": [
                    {
                        "id": d.id,
                        "topic": d.topic,
                        "status": d.status,
                        "current_round": d.current_round,
                        "max_rounds": d.max_rounds,
                        "created_by": d.created_by,
                        "created_at": d.created_at,
                        "concluded_at": d.concluded_at,
                        "convergence_score": d.convergence_score,
                    }
                    for d in discussions
                ],
                "count": len(discussions),
                "filter_status": status,
            }
        finally:
            conn.close()

    def advance(self, discussion_id: str) -> dict[str, Any]:
        """Explicitly advance to the next round.

        Returns dict with new_round, max_rounds, discussion_complete.
        """
        if not discussion_id:
            raise ValueError("discussion_id is required")

        conn = self.db.connect()
        try:
            result = self.db.advance_round(conn, discussion_id)
            return {"ok": True, "discussion_id": discussion_id, **result}
        finally:
            conn.close()

    def notify(
        self,
        discussion_id: str,
        event: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Manually trigger a notification for a discussion.

        Useful for custom notification flows or re-sending missed events.
        """
        if not discussion_id:
            raise ValueError("discussion_id is required")

        conn = self.db.connect()
        try:
            disc = self.db.get_discussion(conn, discussion_id)
            if not disc:
                raise DiscussionNotFoundError(f"Discussion {discussion_id} not found")

            notifier = self._make_notifier(disc.notifications)
            notifier.notify(
                event,
                discussion_id=discussion_id,
                topic=disc.topic,
                **kwargs,
            )
            return {"ok": True, "discussion_id": discussion_id, "event": event}
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # API Aliases
    # ------------------------------------------------------------------

    def init(
        self,
        topic: str,
        participants: list[dict[str, Any]],
        *,
        context: str | None = None,
        max_rounds: int = 5,
        speech_order: str = "fixed",
        created_by: str = "coordinator",
        output_path: str | None = None,
        notifications: dict[str, Any] | None = None,
        web: bool = False,
        web_port: int = 8199,
    ) -> dict[str, Any]:
        """Create a new roundtable discussion. Alias for create_discussion."""
        return self.create_discussion(
            topic,
            participants,
            context=context,
            max_rounds=max_rounds,
            speech_order=speech_order,
            created_by=created_by,
            output_path=output_path,
            notifications=notifications,
            web=web,
            web_port=web_port,
        )

    def end(
        self,
        discussion_id: str,
        *,
        force: bool = False,
        conclusion: str | None = None,
    ) -> dict[str, Any]:
        """End a discussion (conclude or cancel). Alias for end_discussion."""
        return self.end_discussion(discussion_id, force=force, conclusion=conclusion)

    def get_status(self, discussion_id: str) -> dict[str, Any]:
        """Get discussion status including convergence metrics. Alias for status."""
        return self.status(discussion_id)

    def calculate_convergence(self, discussion_id: str, round_num: int) -> dict[str, Any]:
        """Calculate convergence score for a round from its findings.

        Score = consensus / (consensus + disagreement).
        Returns None score if no findings exist.
        """
        if not discussion_id:
            raise ValueError("discussion_id is required")

        conn = self.db.connect()
        try:
            score = self.db.calculate_convergence(conn, discussion_id, round_num)
            return {
                "ok": True,
                "discussion_id": discussion_id,
                "round": round_num,
                "convergence_score": score,
            }
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Demo mode
    # ------------------------------------------------------------------

    # Default demo scenario — topic, participants, speeches, findings
    _DEMO_TOPIC: ClassVar[str] = DEMO_TOPIC
    _DEMO_PARTICIPANTS: ClassVar[list[dict[str, Any]]] = DEMO_PARTICIPANTS
    _DEMO_SPEECHES: ClassVar[dict[int, dict[str, str]]] = DEMO_SPEECHES
    _DEMO_FINDINGS: ClassVar[dict[int, list[tuple[str, str]]]] = DEMO_FINDINGS

    def run_demo(
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
        """Run a complete demo discussion with pre-scripted content."""
        from roundtable.demo import DemoRunner

        runner = DemoRunner(self)
        return runner.run(
            topic=topic,
            participants=participants,
            max_rounds=max_rounds,
            verbose=verbose,
            web=web,
            web_port=web_port,
            stream_delay=stream_delay,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _update_web_discussion_json(
        self,
        discussion_id: str,
        speech_data: dict[str, Any],
        topic: str,
        participants: list[Any],
    ) -> None:
        """Update discussion.json directly when publisher is not in memory (cross-process)."""
        import fcntl as _fcntl

        web_dir = Path("/tmp") / "roundtable_web" / discussion_id
        json_path = web_dir / "discussion.json"
        if not json_path.exists():
            return

        try:
            # Read existing data with shared lock
            with open(json_path) as f:
                _fcntl.flock(f.fileno(), _fcntl.LOCK_SH)
                try:
                    data = json.load(f)
                finally:
                    _fcntl.flock(f.fileno(), _fcntl.LOCK_UN)

            # Append speech
            data.setdefault("speeches", []).append(speech_data)
            data["updated_at"] = int(time.time())

            # Write back with exclusive lock
            tmp = json_path.with_suffix(".json.tmp")
            with open(tmp, "w") as f:
                _fcntl.flock(f.fileno(), _fcntl.LOCK_EX)
                try:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                finally:
                    _fcntl.flock(f.fileno(), _fcntl.LOCK_UN)
            os.rename(str(tmp), str(json_path))
            logger.info("Updated web discussion.json for %s (cross-process)", discussion_id)
        except Exception:
            logger.exception("Failed to update web discussion.json for %s", discussion_id)

    def _conclude_web_discussion(self, discussion_id: str, conclusion: str) -> None:
        """Update discussion.json with conclusion when publisher is not in memory (cross-process)."""
        import fcntl as _fcntl

        web_dir = Path("/tmp") / "roundtable_web" / discussion_id
        json_path = web_dir / "discussion.json"
        if not json_path.exists():
            return

        try:
            with open(json_path) as f:
                _fcntl.flock(f.fileno(), _fcntl.LOCK_SH)
                try:
                    data = json.load(f)
                finally:
                    _fcntl.flock(f.fileno(), _fcntl.LOCK_UN)

            data["conclusion"] = conclusion
            data["status"] = "concluded"
            data["updated_at"] = int(time.time())

            tmp = json_path.with_suffix(".json.tmp")
            with open(tmp, "w") as f:
                _fcntl.flock(f.fileno(), _fcntl.LOCK_EX)
                try:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                finally:
                    _fcntl.flock(f.fileno(), _fcntl.LOCK_UN)
            os.rename(str(tmp), str(json_path))
            logger.info("Concluded web discussion.json for %s (cross-process)", discussion_id)
        except Exception:
            logger.exception("Failed to conclude web discussion.json for %s", discussion_id)

    def _make_notifier(self, config: dict[str, Any] | None) -> Notifier:
        """Create a Notifier from a discussion's notification config."""
        return Notifier(config, send_fn=self._send_fn)

    def _write_markdown_output(self, output_path: str, content: str) -> dict[str, Any]:
        """Write generated Markdown to the configured discussion output path."""
        try:
            path = Path(output_path).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content.rstrip() + "\n", encoding="utf-8")
            return {"output_written": True, "output_path": str(path)}
        except Exception as exc:
            logger.exception("Failed to write roundtable output_path: %s", output_path)
            return {"output_written": False, "output_path": output_path, "output_error": str(exc)}

    def _build_summary_markdown(self, conn: sqlite3.Connection, disc: Discussion) -> str:
        """Build the same structured Markdown used by summarize()."""
        participants = self.db.get_participants(conn, disc.id)
        speeches = self.db.get_speeches(conn, disc.id)
        findings = self.db.get_findings(conn, disc.id)
        conv_history = self.db.get_convergence_history(conn, disc.id)

        p_map = {
            p.participant: {
                "role": p.role,
                "display_name": p.display_name,
                "perspective": p.perspective,
            }
            for p in participants
        }
        consensus_pts = [f.content for f in findings if f.type == "consensus"]
        disagreement_pts = [f.content for f in findings if f.type == "disagreement"]
        new_points = [f.content for f in findings if f.type == "new_point"]
        final_score = disc.convergence_score
        if not final_score and conv_history:
            final_score = conv_history[-1].score

        return self._build_structured_summary(
            disc,
            participants,
            speeches,
            p_map,
            consensus_pts,
            disagreement_pts,
            new_points,
            final_score,
            conv_history,
        )

    def _build_output_markdown(
        self,
        conn: sqlite3.Connection,
        disc: Discussion,
        *,
        conclusion_override: str | None = None,
    ) -> str:
        """Build the Markdown written to output_path."""
        conclusion = conclusion_override if conclusion_override is not None else disc.conclusion
        summary = self._build_summary_markdown(conn, disc)
        if not conclusion:
            return summary
        return f"{summary}\n\n## 最终结论\n\n{conclusion.strip()}"

    def _notify_concluded(self, conn: sqlite3.Connection, disc: Discussion, notifier: Notifier) -> None:
        """Fire the concluded notification with summary data."""
        findings = self.db.get_findings(conn, disc.id)
        consensus = [f.content for f in findings if f.type == "consensus"]
        disagreements = [f.content for f in findings if f.type == "disagreement"]
        notifier.notify(
            "concluded",
            discussion_id=disc.id,
            topic=disc.topic,
            conclusion=disc.conclusion or "",
            convergence=disc.convergence_score,
            consensus_points=consensus,
            disagreement_points=disagreements,
        )

    def set_send_fn(self, send_fn: Callable[..., None] | None) -> None:
        """Set or replace the notification send callback."""
        self._send_fn = send_fn

    @staticmethod
    def _format_history(speeches: list[Speech], participants_map: dict[str, Any]) -> str:
        """Format speech history into a human-readable string."""
        from roundtable.formatter import format_history

        return format_history(speeches, participants_map)

    @staticmethod
    def _build_structured_summary(
        disc: Discussion,
        participants: list[Participant],
        speeches: list[Speech],
        p_map: dict[str, Any],
        consensus_pts: list[str],
        disagreement_pts: list[str],
        new_points: list[str],
        final_score: float | None,
        conv_history: list[ConvergenceRecord],
    ) -> str:
        """Build a compact structured summary for LLM consumption."""
        from roundtable.formatter import build_structured_summary

        return build_structured_summary(
            disc,
            participants,
            speeches,
            p_map,
            consensus_pts,
            disagreement_pts,
            new_points,
            final_score,
            conv_history,
        )


# Dynamic alias to avoid shadowing built-in `list` type in the class body.
RoundtableCore.list = RoundtableCore.list_discussions  # type: ignore[attr-defined]
