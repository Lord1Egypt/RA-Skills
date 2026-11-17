#!/usr/bin/env python3
"""Offline manuscript packaging and append-only publication receipt ledger.

No browser, network, credential discovery, shell execution or publishing code.
"""

import argparse
import copy
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile
from urllib.parse import urlsplit
import uuid


LEDGER = "发布交接包.json"
ACCEPTED = {"submitted", "under_review", "public"}
STATUSES = {"ready", "pre_filled", "unknown", "failed"} | ACCEPTED
MODES = {"observed", "user_report", "simulated", "not_run", "query_failed"}
LABELS = {"ready": "待发布", "pre_filled": "已预填", "submitted": "已提交",
          "under_review": "审核中", "public": "已公开", "unknown": "结果未知", "failed": "失败"}
MODE_LABELS = {"observed": "回读记录", "user_report": "用户提供，未独立核验",
               "simulated": "模拟", "not_run": "未运行", "query_failed": "查询失败"}


class HandoffError(Exception):
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(detail)


def require(condition, code, detail):
    if not condition:
        raise HandoffError(code, detail)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def timestamp(value):
    require(isinstance(value, str), "INVALID_TIME", "时间须为带时区的 ISO 8601 字符串")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise HandoffError("INVALID_TIME", "时间须为带时区的 ISO 8601 字符串")
    require(parsed.tzinfo is not None, "INVALID_TIME", "时间缺少时区")
    return parsed


def normalized_history(receipts):
    require(isinstance(receipts, list), "INVALID_FIELD", "existing_receipts 须为列表")
    timed = []
    for receipt in receipts:
        require(isinstance(receipt, dict), "INVALID_FIELD", "receipt 须为对象")
        timed.append((timestamp(receipt.get("observed_at")), receipt))
    # Stable sorting preserves explicit input order for exactly equal instants;
    # neither receipt IDs nor status ranks may invent a recovery sequence.
    return [receipt for _, receipt in sorted(timed, key=lambda item: item[0])]


def string(value, label):
    require(isinstance(value, str) and bool(value.strip()), "INVALID_FIELD", label + "不能为空")
    return value


def keys(obj, allowed, label):
    require(isinstance(obj, dict), "INVALID_FIELD", label + "须为对象")
    require(not (set(obj) - set(allowed)), "UNKNOWN_FIELD", label + "含未支持字段")


def read_json(path):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            require(k not in result, "DUPLICATE_JSON_KEY", "JSON 字段重复: " + k)
            result[k] = v
        return result
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique)


def local_file(root, relative):
    require(isinstance(relative, str) and "\\" not in relative, "UNSAFE_PATH", "路径须为包内相对路径")
    part = PurePosixPath(relative)
    require(relative and not part.is_absolute() and ".." not in part.parts,
            "UNSAFE_PATH", "路径不得越出输入目录或交接包")
    root = Path(root).resolve()
    path = root.joinpath(*part.parts).resolve()
    require(path.is_relative_to(root), "UNSAFE_PATH", "符号链接越出目录")
    require(path.is_file(), "MISSING_FILE", "找不到所需文件: " + relative)
    return path


def http_url(value):
    require(isinstance(value, str), "INVALID_URL", "链接须为 HTTP(S) URL")
    try:
        u = urlsplit(value)
        good = u.scheme in {"http", "https"} and u.hostname and not u.username and not u.password
        good = good and not any(c.isspace() for c in value)
    except ValueError:
        good = False
    require(good, "INVALID_URL", "链接须为不含凭据的 HTTP(S) URL")


def target_id(platform, account_id, body_sha256):
    # Deliberately independent of title, batch id, version label and asset names.
    return digest(canonical([platform, account_id, body_sha256]).encode())[:20]


def authorization(value, target, body_sha256):
    keys(value, {"action", "platform", "account_id", "draft_sha256", "reference", "valid_until"}, "authorization")
    require(value.get("action") in {"prepare", "submit"}, "INVALID_AUTHORIZATION", "动作须为 prepare 或 submit")
    string(value.get("reference"), "授权来源说明")
    require((value.get("platform"), value.get("account_id"), value.get("draft_sha256")) ==
            (target["platform"], target["account_id"], body_sha256),
            "AUTHORIZATION_SCOPE", "授权必须匹配平台、账号和正文哈希")
    if "valid_until" in value:
        timestamp(value["valid_until"])
    return copy.deepcopy(value)


def accepted_before(target):
    return any(e.get("mode") in {"observed", "user_report"} and e.get("status") in ACCEPTED
               for e in target["receipts"])


def unresolved_attempts(target):
    """Rebuild independent obligations for each intent and unscoped legacy facts."""
    events = [(timestamp(intent["created_at"]), 0, "intent", intent)
              for intent in target["intents"]]
    events += [(timestamp(receipt["observed_at"]), 1, "receipt", receipt)
               for receipt in target["receipts"] if receipt.get("mode") in {"observed", "user_report"}]
    pending, created, latest_intent = set(), set(), None
    # An intent precedes its readback at the same instant; equal-time receipts
    # retain explicit input/append order, without status-priority tie breakers.
    for _, _, kind, event in sorted(events, key=lambda item: (item[0], item[1])):
        if kind == "intent":
            latest_intent = event["id"]
            created.add(latest_intent)
            pending.add(latest_intent)
        elif event.get("status") in {"unknown", "failed"}:
            zero_submission = (event.get("status") == "failed" and event["mode"] == "observed"
                               and event.get("submission_absent") is True)
            if zero_submission:
                scope = event.get("intent_id")
                # A proof cannot close another intent, or an intent not yet created.
                # An unbound proof can only close the separate legacy obligation.
                if scope is None or scope in created:
                    pending.discard(scope)
            else:
                pending.add(event.get("intent_id", latest_intent))
    return pending


def unresolved_submission(target):
    return bool(unresolved_attempts(target))


def earlier_intents_have_zero_proof(target, next_intent):
    """Archive order is evidence of past serial attempts, not a new action grant.

    A late observation can reopen an older attempt after a later one was created.
    Preserve both facts; their independent unresolved obligations still block new actions.
    """
    return all(any(r.get("mode") == "observed" and r.get("status") == "failed"
                   and r.get("submission_absent") is True and r.get("intent_id") == prior["id"]
                   and timestamp(prior["created_at"]) <= timestamp(r["observed_at"]) < timestamp(next_intent["created_at"])
                   for r in target["receipts"]) for prior in target["intents"])


def next_action(target):
    state = target["state"]
    if accepted_before(target):
        return "只读回查；同账号同稿不再投稿"
    if unresolved_submission(target):
        return "历史中仍有未解除的未知提交或失败；先回读原任务，禁止再次投稿"
    if state == "unknown":
        return "先回读原任务；禁止再次投稿"
    if state == "failed":
        r = target.get("current_receipt") or {}
        if r.get("mode") == "observed" and r.get("submission_absent") is True:
            return "已记录零提交证据；修复后重新预填并核对授权"
        return "先回读确认是否受理；禁止直接重投"
    if state == "pre_filled":
        return "沿有效授权保存提交意图；无提交授权则交人工"
    return "按平台稿件与素材清单手动发布，或授权执行器预填"


def atomic_json(path, obj):
    path = Path(path)
    fd, temp = tempfile.mkstemp(prefix=".ledger-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


@contextmanager
def lock(pack):
    p = Path(pack) / ".handoff.lock"
    try:
        fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise HandoffError("PACK_BUSY", "交接包正在写入；先核对原进程，勿并发执行或直接重投")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(str(os.getpid()))
        yield
    finally:
        p.unlink()


def verify(pack, ledger):
    require(ledger.get("schema_version") == 1, "SCHEMA_VERSION", "不支持的交接包版本")
    expected = {"source/body.md": ledger["draft"]["sha256"]}
    for a in ledger["assets"]:
        expected["source/" + a["file"]] = a["sha256"]
    for t in ledger["targets"]:
        prefix = "targets/" + t["id"] + "/"
        expected[prefix + "body.md"] = ledger["draft"]["sha256"]
        expected[prefix + "metadata.json"] = t["metadata_sha256"]
        for a in ledger["assets"]:
            expected[prefix + a["file"]] = a["sha256"]
    for name, sha in expected.items():
        require(digest(local_file(pack, name).read_bytes()) == sha,
                "CONTENT_CHANGED", "文件已变化，停止沿用旧版本或授权: " + name)


def select_target(ledger, tid):
    selected = [t for t in ledger["targets"] if t["id"] == tid]
    require(len(selected) == 1, "UNKNOWN_TARGET", "目标不在当前交接包")
    return selected[0]


def normalized_intents(ledger, intents):
    require(isinstance(intents, list), "INVALID_FIELD", "existing_intents 须为列表")
    timed, seen = [], {}
    for entry in intents:
        keys(entry, {"id", "created_at", "draft_sha256", "authorization"}, "existing_intent")
        iid = string(entry.get("id"), "existing_intent.id")
        when = timestamp(entry.get("created_at"))
        require(entry.get("draft_sha256") == ledger["draft"]["sha256"],
                "VERSION_MISMATCH", "历史意图正文哈希不匹配")
        auth = entry.get("authorization")
        require(isinstance(auth, dict), "INVALID_FIELD", "历史意图 authorization 须为对象")
        for field in ("platform", "account_id"):
            string(auth.get(field), "existing_intent.authorization." + field)
        target = select_target(ledger, target_id(auth["platform"], auth["account_id"], entry["draft_sha256"]))
        checked = authorization(auth, target, ledger["draft"]["sha256"])
        require(checked["action"] == "submit", "SUBMIT_NOT_AUTHORIZED", "历史意图须保留原 submit 授权")
        if "valid_until" in checked:
            require(when <= timestamp(checked["valid_until"]), "AUTHORIZATION_EXPIRED", "历史意图创建时授权已过期")
        if iid in seen:
            require(seen[iid] == entry, "INTENT_CONFLICT", "同历史意图 ID 内容冲突")
            continue
        seen[iid] = copy.deepcopy(entry)
        timed.append((when, entry))
    return [entry for _, entry in sorted(timed, key=lambda item: item[0])]


def apply_receipt(ledger, receipt, imported_intents=None, history_replay=False):
    keys(receipt, {"receipt_id", "platform", "account_id", "draft_sha256", "mode", "status",
                   "observed_at", "source", "evidence", "native_id", "public_url", "public_verified",
                   "submission_absent", "checks", "intent_id"}, "receipt")
    string(receipt.get("receipt_id"), "receipt_id")
    for field in ("platform", "account_id", "draft_sha256", "source", "evidence"):
        string(receipt.get(field), field)
    when = timestamp(receipt.get("observed_at"))
    require(receipt["draft_sha256"] == ledger["draft"]["sha256"], "VERSION_MISMATCH", "回执正文哈希不匹配")
    target = select_target(ledger, target_id(receipt["platform"], receipt["account_id"], receipt["draft_sha256"]))
    mode = receipt.get("mode")
    require(mode in MODES, "INVALID_MODE", "未知观测类型")
    if receipt.get("native_id") is not None:
        string(receipt["native_id"], "平台原生作品/任务 ID")
    if "public_url" in receipt and receipt["public_url"] is not None:
        http_url(receipt["public_url"])
    for name in ("public_verified", "submission_absent"):
        if name in receipt:
            require(type(receipt[name]) is bool, "INVALID_FIELD", name + "须为布尔值")
    for t in ledger["targets"]:
        for old in t["receipts"]:
            if old["receipt_id"] == receipt["receipt_id"]:
                require(old == receipt, "RECEIPT_CONFLICT", "同 receipt_id 内容冲突，原回执不覆盖")
                return {"target": target["id"], "applied": False, "duplicate": True, "state": target["state"]}
    state = receipt.get("status")
    if mode in {"not_run", "query_failed"}:
        require(state is None, "INVALID_RECEIPT", "未运行或查询失败不能附成功/零引用等业务状态")
    else:
        require(state in STATUSES - {"ready"}, "INVALID_STATUS", "不支持的回执状态")
    if mode in {"observed", "user_report"} and state in ACCEPTED:
        string(receipt.get("native_id"), "平台原生作品/任务 ID")
    if mode == "observed" and state == "public":
        http_url(receipt.get("public_url"))
        require(receipt.get("public_verified") is True, "PUBLIC_NOT_VERIFIED", "已公开须有实际公开页核验记录")
    if mode == "observed" and state == "pre_filled":
        checks = receipt.get("checks")
        require(isinstance(checks, dict) and set(checks) == {"account", "title", "body", "assets"}
                and all(v is True for v in checks.values()),
                "PREFILL_NOT_VERIFIED", "预填回读须核对账号、标题、正文及素材")
    if "intent_id" in receipt:
        # A late-recorded observation may predate the intent it names. During
        # import, validate that reference against the complete scoped archive;
        # replay still introduces each intent only at its real creation time.
        references = target["intents"] if imported_intents is None else imported_intents.get(target["id"], [])
        require(any(i["id"] == receipt["intent_id"] for i in references),
                "INTENT_MISMATCH", "回执 intent_id 不属于此目标")
    effective = mode in {"observed", "user_report"}
    newer = not target["state_at"] or when >= timestamp(target["state_at"])
    # Import reconstructs existing facts, rather than requesting a new action.
    # Its complete history still drives unresolved_submission/accepted_before;
    # normal record and intent commands retain every action-transition guard.
    if effective and newer and not history_replay:
        if target["intents"] and state == "failed" and receipt.get("submission_absent") is True:
            require(receipt.get("intent_id") == target["intents"][-1]["id"]
                    or receipt.get("intent_id") in unresolved_attempts(target),
                    "INTENT_MISMATCH", "零提交证据须绑定当前意图或尚未解除的旧意图；无关联证明不能解除其他提交")
        # Never reset an unresolved attempt or an accepted manuscript to a refillable state.
        if state == "pre_filled":
            require(not unresolved_submission(target), "READBACK_REQUIRED", "历史未知提交尚无有效零提交证据，不能重新预填")
            require(target["state"] in {"ready", "pre_filled", "failed"} and not accepted_before(target),
                    "READBACK_REQUIRED", "未知或已受理状态不能回退为预填")
            if target["state"] == "failed":
                previous = target.get("current_receipt") or {}
                require(previous.get("mode") == "observed" and previous.get("submission_absent") is True,
                        "READBACK_REQUIRED", "失败后须先有未受理的原生证据")
        if state == "failed" and receipt.get("submission_absent") is True:
            require(mode == "observed" and not accepted_before(target),
                    "ACCEPTED_PROTECTED", "已受理稿件或用户口述不能解除同稿保护")
        # A later low-confidence user message must not overwrite an observed public result.
        require(not (target["state"] == "public" and state != "public"),
                "PUBLIC_PROTECTED", "已公开记录不能降级；请保留独立异常说明")
    target["receipts"].append(copy.deepcopy(receipt))
    current = target.get("current_receipt") or {}
    preserve_verified_public = (target["state"] == "public" and current.get("mode") == "observed"
                                and ((mode == "user_report" and state == "public")
                                     or (history_replay and state != "public")))
    applied = effective and newer and not preserve_verified_public
    if applied:
        target["state"], target["state_at"] = state, receipt["observed_at"]
        target["current_receipt"] = copy.deepcopy(receipt)
    return {"target": target["id"], "applied": applied, "duplicate": False, "state": target["state"]}


def markdown(value):
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def write_reports(pack, ledger):
    pack = Path(pack)
    lines = ["# 回执状态表", "", "仅汇总输入的回执；脚本不查询平台。正文版本：" + ledger["draft"]["version"],
             "", "| 平台 / 账号 | target_id | 当前状态 | 原生 ID / 公开链接 | 下一步 |",
             "| --- | --- | --- | --- | --- |"]
    listing = ["# 平台稿件及素材清单", "", "正文 SHA256：`" + ledger["draft"]["sha256"] + "`",
               "", "正文按字节保留，标题及栏目等字段单独交接。所有路径相对于本交接包。", ""]
    for t in ledger["targets"]:
        r = t.get("current_receipt") or {}
        label = LABELS[t["state"]] + ("（" + MODE_LABELS[r["mode"]] + "）" if r else "")
        link = r.get("public_url") or "未取得公开链接"
        lines.append("| " + " | ".join(map(markdown, [t["platform_name"] + " / " + t["account_name"],
                     t["id"], label, (r.get("native_id") or "无原生 ID") + " / " + link, next_action(t)])) + " |")
        prefix = "targets/" + t["id"] + "/"
        listing.extend(["## " + markdown(t["platform_name"] + " / " + t["account_name"]), "",
                        "- 稳定账号 ID：`" + markdown(t["account_id"]) + "`",
                        "- 标题：" + markdown(t["title"]),
                        "- 正文：[body.md](" + prefix + "body.md)",
                        "- 平台字段：[metadata.json](" + prefix + "metadata.json)",
                        "- 当前授权：" + t["authorization"]["action"] + "；" + markdown(t["authorization"]["reference"]),
                        "- 接续：" + next_action(t)])
        for a in ledger["assets"]:
            listing.append("- 素材（" + markdown(a["role"]) + "）：[" + markdown(a["description"]) + "](" +
                           prefix + a["file"] + ")；SHA256 `" + a["sha256"] + "`")
        if not ledger["assets"]:
            listing.append("- 素材：本稿未提供独立素材；发布界面如必填封面，先补齐再提交。")
        listing.append("")
    lines.extend(["", "## 观测与失败历史", "",
                  "模拟、未运行和查询失败仅进入历史，不改变当前发布状态；不统计 AI 收录或引用数。", ""])
    for t in ledger["targets"]:
        for e in t["receipts"]:
            lines.append("- " + "；".join(map(markdown, [t["id"], e["observed_at"], MODE_LABELS[e["mode"]],
                         LABELS.get(e.get("status"), "未取得业务状态"), e["receipt_id"], e["source"], e["evidence"]])))
        for intent in t["intents"]:
            lines.append("- 提交意图：" + t["id"] + "；" + intent["id"] + "；" + intent["created_at"] +
                         "；只代表预留一次提交，须由执行器回读结果。")
    (pack / "回执状态表.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (pack / "平台稿件及素材清单.md").write_text("\n".join(listing) + "\n", encoding="utf-8")


def prepare(input_path, output):
    input_path, output = Path(input_path).resolve(), Path(output).resolve()
    plan = read_json(input_path)
    keys(plan, {"schema_version", "batch_id", "draft", "assets", "targets", "existing_receipts", "existing_intents"}, "plan")
    require(plan.get("schema_version") == 1, "SCHEMA_VERSION", "plan.schema_version 须为 1")
    string(plan.get("batch_id"), "batch_id")
    draft = plan.get("draft")
    keys(draft, {"id", "version", "title", "body_file", "content_type"}, "draft")
    for key in ("id", "version", "title", "body_file"):
        string(draft.get(key), "draft." + key)
    require(draft.get("content_type") == "article", "CONTENT_TYPE", "此工具处理已完成的 UTF-8 图文稿")
    body_path = local_file(input_path.parent, draft["body_file"])
    body = body_path.read_bytes()
    require(bool(body.decode("utf-8").strip()), "EMPTY_BODY", "正文不能为空")
    body_sha = digest(body)
    assets, files = [], {"body.md": body}
    raw_assets = plan.get("assets", [])
    require(isinstance(raw_assets, list), "INVALID_FIELD", "assets 须为列表")
    for a in raw_assets:
        keys(a, {"file", "role", "description"}, "asset")
        path = string(a.get("file"), "asset.file")
        require(re.fullmatch(r"assets/[A-Za-z0-9_./-]+", path) is not None and ".." not in PurePosixPath(path).parts,
                "UNSAFE_PATH", "素材须位于 assets/，使用字母、数字、下划线、连字符及目录")
        require(path not in files, "DUPLICATE_ASSET", "素材路径重复")
        for key in ("role", "description"):
            string(a.get(key), "asset." + key)
        data = local_file(input_path.parent, path).read_bytes()
        files[path] = data
        assets.append({**a, "sha256": digest(data), "bytes": len(data)})
    raw_targets = plan.get("targets")
    require(isinstance(raw_targets, list) and bool(raw_targets), "EMPTY_TARGETS", "至少需要一个平台账号目标")
    targets, seen = [], {}
    for raw in raw_targets:
        keys(raw, {"platform", "platform_name", "account_id", "account_name", "title", "fields", "authorization"}, "target")
        t = copy.deepcopy(raw)
        for field in ("platform", "platform_name", "account_id", "account_name"):
            string(t.get(field), field)
        require(re.fullmatch(r"[a-z][a-z0-9_-]*", t["platform"]) is not None,
                "INVALID_PLATFORM", "平台 key 使用小写字母、数字、下划线或连字符")
        require(t["account_id"] == t["account_id"].strip(), "INVALID_ACCOUNT", "账号 ID 不能含首尾空白")
        t.setdefault("title", draft["title"])
        string(t["title"], "平台标题")
        t.setdefault("fields", {})
        require(isinstance(t["fields"], dict), "INVALID_FIELD", "fields 须为对象")
        t["authorization"] = authorization(t.get("authorization"), t, body_sha)
        tid = target_id(t["platform"], t["account_id"], body_sha)
        if tid in seen:
            require(t == seen[tid], "DUPLICATE_TARGET_CONFLICT", "同账号同稿的平台字段或授权冲突，需明确一个版本")
            continue
        seen[tid] = copy.deepcopy(t)
        metadata = {k: v for k, v in t.items() if k != "authorization"}
        metadata.update({"draft_sha256": body_sha, "body_file": "body.md", "assets": assets})
        meta_bytes = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode()
        t.update({"id": tid, "metadata_sha256": digest(meta_bytes), "state": "ready", "state_at": None,
                  "current_receipt": None, "intents": [], "receipts": [],
                  "authorization_history": [copy.deepcopy(t["authorization"])]})
        targets.append(t)
        files["metadata/" + tid] = meta_bytes
    existing = normalized_history(plan.get("existing_receipts", []))
    ledger = {"schema_version": 1, "skill": "aimegeo-publish-handoff", "batch_id": plan["batch_id"],
              "draft": {k: draft[k] for k in ("id", "version", "title", "content_type")},
              "assets": assets, "targets": targets}
    ledger["draft"].update({"sha256": body_sha, "body_file": "source/body.md", "bytes": len(body)})
    imported = normalized_intents(ledger, plan.get("existing_intents", []))
    normalized_plan = {**plan, "existing_receipts": existing}
    # Omitted empty intent history retains fingerprints of existing version-1 plans.
    if "existing_intents" in plan:
        normalized_plan["existing_intents"] = imported
    fingerprint = digest(canonical({"plan": normalized_plan, "body": body_sha, "assets": assets}).encode())
    ledger["plan_fingerprint"] = fingerprint
    imported_by_target = {}
    for entry in imported:
        auth = entry["authorization"]
        tid = target_id(auth["platform"], auth["account_id"], entry["draft_sha256"])
        imported_by_target.setdefault(tid, []).append(entry)
    events = [(timestamp(entry["created_at"]), 0, entry) for entry in imported]
    events += [(timestamp(receipt["observed_at"]), 1, receipt) for receipt in existing]
    for _, kind, entry in sorted(events, key=lambda item: (item[0], item[1])):
        if kind == 1:
            apply_receipt(ledger, entry, imported_by_target, history_replay=True)
            continue
        auth = entry["authorization"]
        target = select_target(ledger, target_id(auth["platform"], auth["account_id"], entry["draft_sha256"]))
        require(earlier_intents_have_zero_proof(target, entry),
                "OVERLAPPING_INTENTS", "引入历史意图 " + entry["id"] + " 前，上一意图尚无更早且有效的零提交证明；同账号同稿不支持重叠意图")
        target["intents"].append(copy.deepcopy(entry))
        if auth not in target["authorization_history"]:
            target["authorization_history"].append(copy.deepcopy(auth))
        # Import preserves historical facts, including late observations. It
        # grants no click; an accepted manuscript keeps its permanent result.
        if not accepted_before(target):
            target["state"], target["state_at"], target["current_receipt"] = "unknown", entry["created_at"], None
    if output.exists():
        require((output / LEDGER).is_file(), "OUTPUT_EXISTS", "输出目录已有内容；选择新目录")
        with lock(output):
            old = read_json(output / LEDGER)
            verify(output, old)
            require(old["plan_fingerprint"] == fingerprint, "PLAN_CHANGED", "现有交接包不可替换；新增回执用 record，改稿另存版本并先核对历史")
            write_reports(output, old)
        return {"command": "prepare", "reused": True, "targets": len(old["targets"])}
    require(not input_path.parent.is_relative_to(output), "OUTPUT_SCOPE", "输出目录不能覆盖输入目录")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".handoff-build-", dir=output.parent))
    try:
        for prefix in ["source"] + ["targets/" + t["id"] for t in targets]:
            for path, data in files.items():
                if path.startswith("metadata/"):
                    continue
                dest = stage / prefix / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
        for t in targets:
            (stage / "targets" / t["id"] / "metadata.json").write_bytes(files["metadata/" + t["id"]])
        atomic_json(stage / LEDGER, ledger)
        write_reports(stage, ledger)
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return {"command": "prepare", "reused": False, "targets": len(targets), "draft_sha256": body_sha}


def record(pack, receipt_path):
    pack = Path(pack)
    with lock(pack):
        ledger = read_json(pack / LEDGER)
        verify(pack, ledger)
        result = apply_receipt(ledger, read_json(receipt_path))
        atomic_json(pack / LEDGER, ledger)
        write_reports(pack, ledger)
    return {"command": "record", **result}


def intent(pack, tid, authorization_path=None):
    pack = Path(pack)
    with lock(pack):
        ledger = read_json(pack / LEDGER)
        verify(pack, ledger)
        t = select_target(ledger, tid)
        require(not accepted_before(t), "ALREADY_ACCEPTED", "此账号此稿已有受理记录，只能回读")
        require(not unresolved_submission(t), "READBACK_REQUIRED", "历史未知提交尚未解除；先回读原任务，禁止新建提交意图")
        require(t["state"] == "pre_filled" and (t.get("current_receipt") or {}).get("mode") == "observed",
                "READBACK_REQUIRED", "须先完成原生预填回读；未知、审核中或失败不能直接投稿")
        auth = t["authorization"] if authorization_path is None else authorization(read_json(authorization_path), t, ledger["draft"]["sha256"])
        require(auth["action"] == "submit", "SUBMIT_NOT_AUTHORIZED", "当前范围仅准备交接包，未获得提交授权")
        if "valid_until" in auth:
            require(timestamp(auth["valid_until"]) >= timestamp(now()), "AUTHORIZATION_EXPIRED", "提交授权已过期")
        if auth != t["authorization"]:
            t["authorization_history"].append(copy.deepcopy(auth))
            t["authorization"] = copy.deepcopy(auth)
        created = now()
        entry = {"id": "intent-" + uuid.uuid4().hex, "created_at": created,
                 "draft_sha256": ledger["draft"]["sha256"], "authorization": copy.deepcopy(auth)}
        t["intents"].append(entry)
        # Commit unknown BEFORE an executor is permitted to click. A crash stays protected.
        t["state"], t["state_at"], t["current_receipt"] = "unknown", created, None
        atomic_json(pack / LEDGER, ledger)
        write_reports(pack, ledger)
    return {"command": "intent", "target": tid, "intent_id": entry["id"], "state": "unknown",
            "next_action": "仅本次新意图可交当前授权执行器点击一次；中断或报错先回读，不重投"}


def report(pack):
    pack = Path(pack)
    with lock(pack):
        ledger = read_json(pack / LEDGER)
        verify(pack, ledger)
        write_reports(pack, ledger)
    return {"command": "report", "targets": [{"id": t["id"], "platform": t["platform"],
            "account_id": t["account_id"], "state": t["state"], "next_action": next_action(t)} for t in ledger["targets"]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="校验输入并生成可手动使用的离线交接包")
    p.add_argument("--input", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("record", help="追加用户提供或实际回读的回执")
    p.add_argument("--pack", required=True)
    p.add_argument("--receipt", required=True)
    p = sub.add_parser("intent", help="预填核验后，持久化一次提交意图；不执行投稿")
    p.add_argument("--pack", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--authorization")
    p = sub.add_parser("report", help="校验副本并重建状态表和素材清单")
    p.add_argument("--pack", required=True)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            result = prepare(args.input, args.out)
        elif args.command == "record":
            result = record(args.pack, args.receipt)
        elif args.command == "intent":
            result = intent(args.pack, args.target, args.authorization)
        else:
            result = report(args.pack)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except HandoffError as e:
        error = {"error": e.code, "detail": e.detail}
    except (OSError, ValueError, KeyError, TypeError) as e:
        error = {"error": "INVALID_INPUT_OR_IO", "detail": str(e)}
    print(json.dumps(error, ensure_ascii=False), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
