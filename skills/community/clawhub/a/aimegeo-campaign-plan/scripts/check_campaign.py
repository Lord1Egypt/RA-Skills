#!/usr/bin/env python3
"""Validate an Agent-authored event plan; never write copy or query platforms."""

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse


STAGES = ("before", "during", "after")
CHANNELS = ("public", "moments", "dm")


def list_or_empty(value):
    return value if isinstance(value, list) else []


class Checker:
    def __init__(self):
        self.errors = []

    def error(self, code, path, message):
        self.errors.append({"code": code, "path": path, "message": message})

    def obj(self, value, path):
        if not isinstance(value, dict):
            self.error("SCHEMA", path, "须为对象")
            return {}
        return value

    def rows(self, value, path, key="id"):
        if not isinstance(value, list):
            self.error("SCHEMA", path, "须为对象列表")
            return {}
        result = {}
        for n, raw in enumerate(value):
            p = f"{path}[{n}]"
            row = self.obj(raw, p)
            identifier = row.get(key)
            if not isinstance(identifier, str) or not identifier.strip():
                self.error("SCHEMA", p + "." + key, "须为非空字符串编号")
            elif identifier in result:
                self.error("DUPLICATE_ID", p + "." + key, "编号重复")
            else:
                result[identifier] = row
        return result

    def strings(self, value, path, allowed=None):
        if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
            self.error("SCHEMA", path, "须为字符串列表")
            return []
        if len(value) != len(set(value)):
            self.error("DUPLICATE_REF", path, "列表中有重复项")
        if allowed is not None:
            for x in value:
                if x not in allowed:
                    self.error("UNKNOWN_REF", path, f"无效引用或选项：{x}")
        return value

    def text(self, row, key, path):
        value = row.get(key)
        if not isinstance(value, str) or not value.strip():
            self.error("SCHEMA", path + "." + key, "须为非空文本")
            return ""
        return value


def validate(data):
    c = Checker()
    root = c.obj(data, "$")
    if type(root.get("schema_version")) is not int or root.get("schema_version") != 1:
        c.error("SCHEMA", "schema_version", "只支持版本 1")
    c.text(root, "request", "$")
    facts = c.rows(root.get("facts"), "facts")
    confirmed = set()
    by_key = {}
    for fid, fact in facts.items():
        p = "facts." + fid
        key = c.text(fact, "key", p)
        if key in by_key:
            c.error("DUPLICATE_FACT_KEY", p, "同一事实字段不能有多个当前值")
        by_key[key] = fact
        if fact.get("status") not in ("confirmed", "missing", "unverified"):
            c.error("SCHEMA", p + ".status", "无效事实状态")
        if fact.get("status") == "confirmed":
            confirmed.add(fid)
            if fact.get("value") is None or fact.get("value") == "":
                c.error("FACT_VALUE", p, "确认事实须有值")
            source = c.obj(fact.get("source"), p + ".source")
            c.text(source, "ref", p + ".source")
            c.text(source, "excerpt", p + ".source")
        elif fact.get("status") == "missing" and fact.get("value") is not None:
            c.error("MISSING_FACT_VALUE", p, "缺失事实的值须为 null")

    def confirmed_value(key):
        fact = by_key.get(key, {})
        if fact.get("status") != "confirmed":
            c.error("REQUIRED_FACT", "facts." + key, "需要来源明确的已确认事实")
            return None
        return fact.get("value")

    event = c.obj(root.get("event"), "event")
    c.text(event, "id", "event")
    for field, key in (("brand", "brand"), ("kind", "event_kind")):
        value = c.text(event, field, "event")
        if value != confirmed_value(key):
            c.error("EVENT_FACT_MISMATCH", "event." + field, "事件字段与确认事实不一致")
    time = c.obj(event.get("time"), "event.time")
    raw_time = c.text(time, "raw", "event.time")
    if raw_time != confirmed_value("time_raw"):
        c.error("TIME_RAW_CHANGED", "event.time.raw", "须保留用户时间原话")
    dates = (time.get("start_date"), time.get("end_date"))
    if any(x is not None for x in dates):
        date_fact = by_key.get("event_dates", {})
        expected_dates = {"start_date": dates[0], "end_date": dates[1]}
        if date_fact.get("status") != "confirmed" or date_fact.get("value") != expected_dates:
            c.error("DATE_WITHOUT_EVIDENCE", "event.time", "确切展期必须有独立确认事实，不能从相对时间猜定")
        try:
            parsed = [date.fromisoformat(x) for x in dates]
            if parsed[1] < parsed[0]:
                raise ValueError()
        except (TypeError, ValueError):
            c.error("DATE_RANGE", "event.time", "日期须为有序的 ISO 日期对")
    for field in ("anchor_date", "timezone"):
        value = time.get(field)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            c.error("SCHEMA", "event.time." + field, "须为非空文本或 null")

    staff = c.rows(event.get("staff"), "event.staff")
    count = confirmed_value("staff_count")
    if type(count) is not int or count <= 0 or count != len(staff):
        c.error("STAFF_COUNT", "event.staff", "分工人数须与确认人手一致，且至少一人")
    for sid, person in staff.items():
        c.text(person, "role", "event.staff." + sid)
    scope = c.obj(root.get("scope"), "scope")
    stages = c.strings(scope.get("stages"), "scope.stages", STAGES)
    channels = c.strings(scope.get("channels"), "scope.channels", CHANNELS)
    if not stages or not channels:
        c.error("COVERAGE", "scope", "需指定非空阶段和渠道范围")
    mode = scope.get("mode")
    if mode not in ("plan", "selected", "all"):
        c.error("SCHEMA", "scope.mode", "须为 plan、selected 或 all")
    if mode in ("selected", "all"):
        c.text(scope, "authorization", "scope")

    topics = c.rows(root.get("topics"), "topics")
    shots = c.rows(root.get("shots"), "shots")
    faqs = c.rows(root.get("faqs"), "faqs")
    drafts = c.rows(root.get("drafts"), "drafts", "topic_id")
    selected = c.strings(scope.get("selected_ids"), "scope.selected_ids", topics)
    expected = set(topics) if mode == "all" else set(selected) if mode == "selected" else set()
    if mode == "selected" and not selected:
        c.error("DRAFT_SCOPE", "scope.selected_ids", "选稿模式须指定至少一条编号")
    if mode in ("plan", "all") and selected:
        c.error("DRAFT_SCOPE", "scope.selected_ids", "仅 selected 模式使用选择列表")
    if set(drafts) != expected:
        c.error("DRAFT_COVERAGE", "drafts", f"稿件缺少 {sorted(expected - set(drafts))}；超出 {sorted(set(drafts) - expected)}")

    coverage = {stage: {channel: 0 for channel in channels} for stage in stages}
    for tid, topic in topics.items():
        p = "topics." + tid
        for field in ("title", "hook", "audience", "action", "platform", "format", "time_label"):
            c.text(topic, field, p)
        if topic.get("stage") not in stages or topic.get("channel") not in channels:
            c.error("TOPIC_SCOPE", p, "选题不在要求的阶段或渠道范围")
        else:
            coverage[topic["stage"]][topic["channel"]] += 1
        if not isinstance(topic.get("owner"), str) or topic.get("owner") not in staff:
            c.error("UNKNOWN_REF", p + ".owner", "负责人不在人手表")
        c.strings(topic.get("fact_ids"), p + ".fact_ids", confirmed)
        c.strings(topic.get("faq_ids"), p + ".faq_ids", faqs)
        c.strings(topic.get("shot_ids"), p + ".shot_ids", shots)
        if not c.strings(topic.get("publish_conditions"), p + ".publish_conditions"):
            c.error("USAGE_CONDITION", p, "每条需说明使用条件")
    for stage, cells in coverage.items():
        for channel, total in cells.items():
            if not total:
                c.error("COVERAGE", f"topics.{stage}.{channel}", "缺少要求的阶段渠道选题")

    bookings = []
    minutes = 0
    for sid, shot in shots.items():
        p = "shots." + sid
        window = c.text(shot, "window", p)
        for field in ("content", "fallback"):
            c.text(shot, field, p)
        people = c.strings(shot.get("people"), p + ".people", staff)
        topic_refs = c.strings(shot.get("topic_ids"), p + ".topic_ids", topics)
        if not people or not topic_refs:
            c.error("SHOT_ASSIGNMENT", p, "镜头须分配人员和用途")
        if shot.get("priority") not in ("essential", "optional") or shot.get("status") not in ("planned", "captured", "unavailable"):
            c.error("SCHEMA", p, "无效镜头优先级或采集状态")
        start, end = shot.get("start_minute"), shot.get("end_minute")
        if type(start) is not int or type(end) is not int or start < 0 or end <= start:
            c.error("SHOT_INTERVAL", p, "窗口内分钟须为非负整数，且结束晚于开始")
        else:
            minutes += (end - start) * len(people)
            for other in bookings:
                shared = set(people) & set(other[4])
                if window == other[1] and max(start, other[2]) < min(end, other[3]) and shared:
                    c.error("SHOOT_CONFLICT", p, f"与 {other[0]} 同时占用 {','.join(sorted(shared))}")
            bookings.append((sid, window, start, end, people))
        for tid in topic_refs:
            if tid in topics and sid not in list_or_empty(topics[tid].get("shot_ids")):
                c.error("SHOT_LINK", p, f"选题 {tid} 未反向关联镜头")
    for tid, topic in topics.items():
        for sid in topic.get("shot_ids", []) if isinstance(topic.get("shot_ids"), list) else []:
            if isinstance(sid, str) and sid in shots and tid not in list_or_empty(shots[sid].get("topic_ids")):
                c.error("SHOT_LINK", "topics." + tid, f"镜头 {sid} 未反向关联选题")

    for qid, faq in faqs.items():
        p = "faqs." + qid
        c.text(faq, "question", p)
        refs = c.strings(faq.get("fact_ids"), p + ".fact_ids", confirmed)
        missing = c.strings(faq.get("missing_keys"), p + ".missing_keys")
        status = faq.get("status")
        if status not in ("supported", "partial", "missing"):
            c.error("SCHEMA", p + ".status", "无效问答状态")
        if status in ("supported", "partial"):
            c.text(faq, "answer", p)
            if not refs:
                c.error("FAQ_EVIDENCE", p, "回答需要确认事实")
        if (status == "supported" and missing) or (status in ("partial", "missing") and not missing):
            c.error("FAQ_STATUS", p, "回答状态与缺口不一致")
        if status == "missing" and faq.get("answer") is not None:
            c.error("FAQ_STATUS", p, "没有依据时不填答案")

    draft_texts = set()
    for tid, draft in drafts.items():
        p = "drafts." + tid
        text = c.text(draft, "text", p)
        normalized = "".join(text.split())
        if normalized and normalized in draft_texts:
            c.error("REPEATED_DRAFT", p, "不同选题不能使用完全相同的正文")
        draft_texts.add(normalized)
        if tid not in topics:
            c.error("UNKNOWN_REF", p, "稿件无对应选题")
        c.strings(draft.get("fact_ids"), p + ".fact_ids", confirmed)
        required = c.strings(draft.get("required_fact_ids"), p + ".required_fact_ids", facts)
        shot_refs = c.strings(draft.get("required_shot_ids"), p + ".required_shot_ids", shots)
        alternatives = draft.get("required_shot_any_of", [])
        if not isinstance(alternatives, list):
            c.error("SCHEMA", p + ".required_shot_any_of", "替代素材须为分组列表")
            alternatives = []
        shot_groups = []
        for n, group in enumerate(alternatives):
            group_path = f"{p}.required_shot_any_of[{n}]"
            refs = c.strings(group, group_path, shots)
            if not refs:
                c.error("DRAFT_SHOT_GROUP", group_path, "每个替代素材组须有至少一个有效编号")
            shot_groups.append(refs)
        if draft.get("status") not in ("ready_for_review", "awaiting_facts", "awaiting_capture"):
            c.error("SCHEMA", p + ".status", "无效稿件状态")
        if draft.get("status") == "ready_for_review":
            if any(fid not in confirmed for fid in required):
                c.error("DRAFT_FACT_GATE", p, "缺少必要事实，不能标为可审阅使用")
            if any(shots.get(sid, {}).get("status") != "captured" for sid in shot_refs):
                c.error("DRAFT_SHOT_GATE", p, "必要素材未采集，不能标为可审阅使用")
            for n, group in enumerate(shot_groups):
                if not any(shots.get(sid, {}).get("status") == "captured" for sid in group):
                    c.error("DRAFT_SHOT_GATE", p, f"替代素材组 {n + 1} 尚无已采集素材，不能标为可审阅使用")

    observations = c.rows(root.get("observations"), "observations")
    states = {x: 0 for x in ("observed", "simulated", "not_run", "query_failed")}
    mentions = citations = 0
    for oid, observation in observations.items():
        p = "observations." + oid
        status = observation.get("status")
        if not isinstance(status, str) or status not in states:
            c.error("SCHEMA", p + ".status", "无效 GEO 观测状态")
            continue
        states[status] += 1
        for field in ("question", "platform"):
            c.text(observation, field, p)
        if status != "observed":
            if observation.get("brand_mentioned") is not None or observation.get("native_citations") is not None:
                c.error("GEO_UNMEASURED", p, "模拟、未运行、失败不能填实测提及或引用值")
            if status == "query_failed":
                c.text(observation, "error", p)
            continue
        answer = c.text(observation, "answer", p)
        c.text(observation, "evidence", p)
        if observation.get("origin") not in ("provided_answer", "collected_answer"):
            c.error("GEO_EVIDENCE", p, "须标记真实输入或采集的回答来源")
        try:
            captured = datetime.fromisoformat(observation.get("captured_at", "").replace("Z", "+00:00"))
            if captured.tzinfo is None:
                raise ValueError()
        except (AttributeError, TypeError, ValueError):
            c.error("GEO_TIME", p, "观测时间须为带时区的 ISO 时间")
        mentioned = observation.get("brand_mentioned")
        if type(mentioned) is not bool:
            c.error("GEO_MENTION", p, "实测提及须为布尔值")
        elif isinstance(event.get("brand"), str) and mentioned != (event["brand"] in answer):
            c.error("GEO_MENTION", p, "提及标记与回答中的品牌原名不一致；别名和歧义需人工核实")
        else:
            mentions += int(mentioned)
        native = observation.get("native_citations")
        if not isinstance(native, list):
            c.error("SCHEMA", p + ".native_citations", "实测原生引用须为列表，确无引用时才用 []")
        else:
            seen = set()
            for n, raw in enumerate(native):
                ref = c.obj(raw, f"{p}.native_citations[{n}]")
                url = c.text(ref, "url", p)
                position = c.text(ref, "native_ref", p)
                try:
                    parsed_url = urlparse(url)
                    valid_url = parsed_url.scheme in ("http", "https") and bool(parsed_url.netloc)
                except ValueError:
                    valid_url = False
                if not valid_url or (url, position) in seen:
                    c.error("GEO_CITATION", p, "引用须有有效 URL 和不重复的原生位置")
                seen.add((url, position))
            citations += len(native)

    if c.errors:
        return {"ok": False, "errors": c.errors}
    return {"ok": True, "summary": {
        "event_id": event["id"], "time_raw": raw_time, "topics": len(topics),
        "coverage": coverage, "drafts": len(drafts), "shots": len(shots),
        "staff": len(staff), "scheduled_person_minutes": minutes,
        "pending_fact_keys": sorted(key for key, fact in by_key.items() if fact.get("status") != "confirmed"),
        "draft_statuses": {s: sum(d.get("status") == s for d in drafts.values()) for s in ("ready_for_review", "awaiting_facts", "awaiting_capture")},
        "geo": {"status": "observed" if states["observed"] else "no_observed_answers",
                "status_counts": states, "observed_answers": states["observed"],
                "brand_mentions": mentions if states["observed"] else None,
                "native_citations": citations if states["observed"] else None}
    }}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Agent-authored campaign JSON")
    args = parser.parse_args()
    try:
        # No source-reference paths or URLs are opened. Input is data only.
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [{"code": "INPUT_ERROR", "path": "input", "message": str(exc)}]}, ensure_ascii=False))
        return 2
    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
