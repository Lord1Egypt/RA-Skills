"""Load user-supplied chat exports into a normalized schema."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


SYSTEM_PATTERNS = [
    re.compile(r"^\[系统"),
    re.compile(r"通过 .+ 加入了群聊"),
    re.compile(r"修改群名"),
    re.compile(r"成为新群主"),
    re.compile(r"群聊 AI 功能"),
]


@dataclass
class Message:
    conversation_id: str
    sender_id: str
    sender_name: str
    content: str
    ts: Optional[int] = None
    msg_type: Any = 0
    is_system: bool = False
    is_share_like: bool = False
    raw_id: str = ""


@dataclass
class Conversation:
    conversation_id: str
    name: str
    conv_type: str  # group | dm | unknown
    platform: str = ""
    source_path: str = ""
    members: Dict[str, str] = field(default_factory=dict)  # id -> name
    messages: List[Message] = field(default_factory=list)

    def to_public_dict(self) -> dict:
        return {
            "conversation_id": self.conversation_id,
            "name": self.name,
            "type": self.conv_type,
            "platform": self.platform,
            "source_path": self.source_path,
            "member_count": len(self.members),
            "message_count": len(self.messages),
        }



def _looks_like_chatlab(sample: str) -> bool:
    head = (sample or "").lstrip()
    if not head.startswith("{"):
        return False
    # ChatLab JSONL: header row or ndjson message rows
    if '"_type"' in head[:500] or '"chatlab"' in head[:500]:
        return True
    # multi-line objects
    if "\n" in sample and head.startswith("{"):
        first = sample.splitlines()[0].strip()
        try:
            json.loads(first)
            return True
        except Exception:
            return False
    return False

def _display_name(path: Path) -> str:
    try:
        return path.name or str(path)
    except Exception:
        return "input"


def load_input(path: Path) -> List[Conversation]:
    path = Path(path).expanduser()
    try:
        path = path.resolve()
    except OSError:
        pass
    if not path.exists():
        raise FileNotFoundError(f"输入路径不存在: {_display_name(path)}")
    if path.is_dir():
        convs: List[Conversation] = []
        files = sorted(
            set(
                list(path.glob("*.jsonl"))
                + list(path.glob("*.ndjson"))
                + list(path.glob("*.json"))
                + list(path.glob("*.txt"))
                + list(path.glob("*.md"))
                + list(path.glob("*.chatlab.txt"))
                + list(path.glob("*.jsonl.txt"))
            )
        )
        if not files:
            raise ValueError(
                f"目录内没有可识别的导出文件（需要 .jsonl/.json/.txt/.md/.ndjson）: {_display_name(path)}"
            )
        for f in files:
            convs.extend(load_input(f))
        return _dedupe_merge(convs)
    try:
        suffix = path.suffix.lower()
        name_l = path.name.lower()
        sample = path.read_text(encoding="utf-8", errors="replace")[:4000]
        # ClawHub may strip bare .jsonl — also accept *.chatlab.txt / *.jsonl.txt / *.ndjson
        if suffix == ".jsonl" or suffix == ".ndjson" or name_l.endswith(".jsonl.txt") or name_l.endswith(".chatlab.txt"):
            return load_chatlab_jsonl(path)
        if suffix == ".json":
            return load_json_file(path)
        if suffix in {".txt", ".md", ".log"}:
            if _looks_like_chatlab(sample):
                return load_chatlab_jsonl(path)
            return [load_plaintext(path)]
        # try jsonl by content for unknown extensions
        if _looks_like_chatlab(sample):
            try:
                return load_chatlab_jsonl(path)
            except Exception:
                pass
        raise ValueError(
            f"无法识别的导出格式: {_display_name(path)}。"
            "支持 ChatLab JSONL / JSON 数组 / 纯文本「昵称: 内容」"
        )
    except PermissionError as e:
        raise PermissionError(f"没有权限读取: {_display_name(path)}") from e


def load_chatlab_jsonl(path: Path) -> List[Conversation]:
    conv = Conversation(
        conversation_id=path.stem,
        name=path.stem,
        conv_type="unknown",
        source_path=str(path),
    )
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"{Path(path).name}:{line_no} JSON 无效: {e}") from e
            t = obj.get("_type")
            if t == "header":
                meta = obj.get("meta") or {}
                name = meta.get("name") or conv.name
                conv.name = str(name)
                # ChatLab sometimes marks group exports as private; member count later fixes
                raw_type = str(meta.get("type") or "unknown").lower()
                conv.conv_type = "dm" if raw_type in {"private", "dm", "c2c"} else (
                    "group" if raw_type in {"group", "chatroom"} else raw_type
                )
                conv.platform = str(meta.get("platform") or "")
                cid = meta.get("conversationId") or meta.get("id") or meta.get("ownerId")
                if cid:
                    conv.conversation_id = str(cid)
            elif t == "member":
                pid = str(obj.get("platformId") or obj.get("id") or "")
                name = str(obj.get("accountName") or obj.get("name") or pid)
                if pid:
                    conv.members[pid] = name
            elif t == "message":
                content = _extract_content(obj)
                sender_id = str(obj.get("sender") or obj.get("senderId") or "")
                sender_name = str(
                    obj.get("accountName")
                    or conv.members.get(sender_id)
                    or obj.get("senderName")
                    or sender_id
                    or "unknown"
                )
                ts = obj.get("timestamp") or obj.get("ts") or obj.get("time")
                try:
                    ts_i = int(ts) if ts is not None else None
                except Exception:
                    ts_i = None
                msg = Message(
                    conversation_id=conv.conversation_id,
                    sender_id=sender_id,
                    sender_name=sender_name,
                    content=content,
                    ts=ts_i,
                    msg_type=obj.get("type", 0),
                    is_system=_is_system(content, obj),
                    is_share_like=_is_share_like(content, obj),
                    raw_id=str(obj.get("platformMessageId") or obj.get("id") or ""),
                )
                conv.messages.append(msg)
            else:
                # tolerate unknown rows
                continue
    if len(conv.members) >= 3 and conv.conv_type == "dm":
        conv.conv_type = "group"
    # header-only empty exports are allowed; inventory gate will fail them cleanly
    if not conv.messages and not conv.members and not conv.name:
        raise ValueError(f"ChatLab JSONL 未解析到有效会话: {Path(path).name}")
    return [conv]


def load_json_file(path: Path) -> List[Conversation]:
    data = json.loads(path.read_text(encoding="utf-8"))
    # clean_msgs style: {name, messages:[{sender, content, ts}]}
    if isinstance(data, dict) and "messages" in data:
        name = str(data.get("name") or path.stem)
        conv = Conversation(
            conversation_id=str(data.get("id") or path.stem),
            name=name,
            conv_type=str(data.get("type") or "unknown"),
            platform=str(data.get("platform") or ""),
            source_path=str(path),
        )
        for m in data.get("messages") or []:
            content = str(m.get("content") or "")
            sid = str(m.get("sender_id") or m.get("senderId") or m.get("sender") or "")
            sname = str(m.get("sender") or m.get("accountName") or sid)
            if sid and sid not in conv.members:
                conv.members[sid] = sname
            ts = m.get("ts") or m.get("timestamp")
            try:
                ts_i = int(ts) if ts is not None else None
            except Exception:
                ts_i = None
            conv.messages.append(
                Message(
                    conversation_id=conv.conversation_id,
                    sender_id=sid,
                    sender_name=sname,
                    content=content,
                    ts=ts_i,
                    msg_type=m.get("type", 0),
                    is_system=_is_system(content, m),
                    is_share_like=_is_share_like(content, m),
                    raw_id=str(m.get("id") or ""),
                )
            )
        if len(conv.members) >= 3 and conv.conv_type in {"unknown", "dm", "private"}:
            conv.conv_type = "group"
        return [conv]
    if isinstance(data, list):
        conv = Conversation(
            conversation_id=path.stem,
            name=path.stem,
            conv_type="unknown",
            source_path=str(path),
        )
        for m in data:
            if not isinstance(m, dict):
                continue
            content = str(m.get("content") or m.get("text") or "")
            sname = str(m.get("sender") or m.get("accountName") or m.get("user") or "unknown")
            sid = str(m.get("sender_id") or m.get("senderId") or sname)
            conv.members[sid] = sname
            ts = m.get("ts") or m.get("timestamp")
            try:
                ts_i = int(ts) if ts is not None else None
            except Exception:
                ts_i = None
            conv.messages.append(
                Message(
                    conversation_id=conv.conversation_id,
                    sender_id=sid,
                    sender_name=sname,
                    content=content,
                    ts=ts_i,
                    is_system=_is_system(content, m),
                    is_share_like=_is_share_like(content, m),
                )
            )
        return [conv]
    raise ValueError(f"不支持的 JSON 结构: {path}")



def _parse_loose_ts(s: str):
    """Best-effort parse for plaintext [time] prefixes → unix seconds or None."""
    from datetime import datetime
    s = (s or "").strip()
    if not s:
        return None
    if s.isdigit() and len(s) >= 10:
        return int(s[:10])
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M", "%m-%d %H:%M", "%H:%M:%S", "%H:%M"):
        try:
            dt = datetime.strptime(s, fmt)
            if dt.year == 1900:
                dt = dt.replace(year=datetime.now().year)
            return int(dt.timestamp())
        except Exception:
            continue
    return None


def load_plaintext(path: Path) -> Conversation:
    conv = Conversation(
        conversation_id=path.stem,
        name=path.stem,
        conv_type="unknown",
        source_path=str(path),
    )
    # patterns: "张三: 你好" or "[12:01] 张三: 你好"
    line_re = re.compile(
        r"^(?:\[(?P<ts>[^\]]+)\]\s*)?(?P<sender>[^:：]{1,40})[:：]\s*(?P<content>.+)$"
    )
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        m = line_re.match(line)
        if not m:
            # orphan line belongs to previous? keep as system-ish
            sender = "unknown"
            content = line
        else:
            sender = m.group("sender").strip()
            content = m.group("content").strip()
        sid = sender
        conv.members[sid] = sender
        ts_val = None
        if m and m.groupdict().get("ts"):
            ts_val = _parse_loose_ts(m.group("ts"))
        conv.messages.append(
            Message(
                conversation_id=conv.conversation_id,
                sender_id=sid,
                sender_name=sender,
                content=content,
                ts=ts_val,
                is_system=_is_system(content, {}),
                is_share_like=_is_share_like(content, {}),
            )
        )
    return conv


def _extract_content(obj: dict) -> str:
    c = obj.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, dict):
        for k in ("text", "title", "desc", "description", "url"):
            if c.get(k):
                return str(c.get(k))
        return json.dumps(c, ensure_ascii=False)[:500]
    if c is None:
        # some exporters put text elsewhere
        for k in ("text", "body", "msg"):
            if obj.get(k):
                return str(obj.get(k))
        return ""
    return str(c)


def _is_system(content: str, obj: dict) -> bool:
    if obj.get("is_system") is True:
        return True
    c = content or ""
    if c.strip() in {"[系统消息]", "[系统]"}:
        return True
    for pat in SYSTEM_PATTERNS:
        if pat.search(c):
            return True
    return False


def _is_share_like(content: str, obj: dict) -> bool:
    t = obj.get("type")
    # douyin export: type 1 often image/link; 5/24 cards — treat URL-heavy as share-like for ranking
    c = content or ""
    if "douyinpic.com" in c or "iesdouyin.com" in c or "v.douyin.com" in c:
        return True
    if c.startswith("http://") or c.startswith("https://"):
        return True
    if t in {1, 5, 24, "share", "card", "video"}:
        # only if little prose
        if len(re.sub(r"https?://\S+", "", c).strip()) < 8:
            return True
    return False


def _dedupe_merge(convs: List[Conversation]) -> List[Conversation]:
    # keep separate files as separate conversations even if names collide
    out = []
    seen = set()
    for i, c in enumerate(convs):
        key = (c.source_path, c.conversation_id, c.name)
        if key in seen:
            c.conversation_id = f"{c.conversation_id}#{i}"
        seen.add((c.source_path, c.conversation_id, c.name))
        out.append(c)
    return out


def filter_messages(
    messages: Iterable[Message],
    *,
    drop_system: bool = True,
    person: Optional[str] = None,
) -> List[Message]:
    out = []
    person_l = person.lower().strip() if person else None
    for m in messages:
        if drop_system and m.is_system:
            continue
        if person_l:
            if person_l not in (m.sender_name or "").lower() and person_l not in (m.sender_id or "").lower():
                continue
        out.append(m)
    return out
