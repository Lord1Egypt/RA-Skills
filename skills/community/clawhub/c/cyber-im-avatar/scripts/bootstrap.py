#!/usr/bin/env python3
"""bootstrap.py — cyber-im-avatar 首装环境自适配。

做什么：
  1. 探测本机已安装的 IM CLI（lark-cli / wecom-cli / dws）
  2. 校验各平台登录态，抓取本人 ID（防回环必需）
  3. 可选冒烟测试：对指定会话跑一轮消息拉取，验证字段适配
  4. 抓取本人近期发出的消息语料（供 agent 学习聊天风格，防穿帮）
  5. 落盘 ~/.im-standin/env.json（个人适配数据，与 Skill 目录分离）

用法:
  python3 bootstrap.py                        # 全量探测
  python3 bootstrap.py --smoke feishu oc_xxx  # 对某会话冒烟测试
  python3 bootstrap.py --alias feishu "张三私聊" oc_xxx  # 注册会话别名
  python3 bootstrap.py --note feishu "张三私聊" "对价格敏感，周五不回消息"  # 给服务对象记档案
  python3 bootstrap.py --compact feishu "张三私聊" [--dry-run]  # 画像去重/归档旧结论
  python3 bootstrap.py --learn-style feishu --chats oc_xxx [--limit 100]  # 脱敏语料
  python3 bootstrap.py --delete-data --yes                 # 删除个人数据
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

from data_guard import (atomic_write_json, atomic_write_text, ensure_private_dir,
                        redact_sensitive, secure_tree, usable_style_text)

ENV_DIR = os.environ.get("IM_STANDIN_DIR") or os.path.expanduser("~/.im-standin")
ENV_PATH = os.path.join(ENV_DIR, "env.json")
PROFILES_DIR = os.path.join(ENV_DIR, "profiles")
PROFILE_MAX_BYTES = 12 * 1024
PROFILE_SOFT_BYTES = 8 * 1024
PROFILE_MAX_HISTORY = 20
PROFILE_MAX_DATED = 8
_SAFE_RE = re.compile(r"[^0-9A-Za-z._\-\u4e00-\u9fff]+")


def _profile_rel(platform, node, alias):
    cid = _SAFE_RE.sub("_", (node.get("chat_id") or "").strip()).strip("._-")[:80]
    if cid:
        fid = cid
    else:
        base = _SAFE_RE.sub("_", (alias or "").strip()).strip("._-")[:80] or "target"
        fid = base + "-" + hashlib.sha1((alias or "").encode("utf-8")).hexdigest()[:6]
    plat = _SAFE_RE.sub("_", platform or "unknown").strip("._-") or "unknown"
    return os.path.join("profiles", plat, fid + ".md")


def _profile_template(alias, platform, chat_id):
    return (
        "# %s\n\n> %s · %s\n"
        "> 画像由值守 agent 与面板共同维护：只写下次值守还会用到的信息，不保存聊天原文。\n\n"
        "## 对方是谁\n\n## 沟通偏好\n\n## 在意与忌讳\n\n## 历史结论\n"
        % (alias or chat_id or "服务对象",
           {"feishu": "飞书", "wecom": "企业微信", "dingtalk": "钉钉"}.get(platform, platform),
           chat_id or "未绑定会话"))


def ensure_profile(platform, alias, node):
    rel = node.get("profile_file") or _profile_rel(platform, node, alias)
    path = os.path.join(ENV_DIR, rel)
    if not os.path.isfile(path):
        atomic_write_text(path, _profile_template(alias, platform, node.get("chat_id") or ""))
    node["profile_file"] = rel
    node.pop("profile", None)
    return path


def _profile_history_path(path):
    return path[:-3] + ".history.md" if path.endswith(".md") else path + ".history.md"


def _dedupe_profile_bullets(text):
    """按小节去掉完全相同的 bullet；返回 (text, 去重条数)。"""
    out, seen, section, removed = [], set(), "", 0
    for line in text.splitlines():
        if line.startswith("## "):
            section = line.strip()
        stripped = line.strip()
        if stripped.startswith("- "):
            key = (section, stripped)
            if key in seen:
                removed += 1
                continue
            seen.add(key)
        out.append(line)
    return "\n".join(out).rstrip() + "\n", removed


def _dated_bullet(line):
    return bool(re.match(r"^-\s*(\d{1,2}-\d{1,2}|\d{4}-\d{2}-\d{2})\b", line.strip()))


def _compact_profile_text(text):
    """去重 + 把「历史结论」最旧的 bullet 移到 history。

    新条目由 append_profile_note 插在最前，所以列表末尾最旧。
    返回 (新正文, 被归档的 bullet, 去重条数, 是否仍超硬上限)。
    """
    text, dedup = _dedupe_profile_bullets(text)
    head, sep, tail = text.partition("## 历史结论")
    removed = []
    if sep:
        body = tail.splitlines()
        while True:
            bullets = [i for i, line in enumerate(body) if line.strip().startswith("- ")]
            dated = [i for i in bullets if _dated_bullet(body[i])]
            candidate = head + sep + "\n".join(body)
            if not candidate.endswith("\n"):
                candidate += "\n"
            if (len(bullets) <= PROFILE_MAX_HISTORY and
                    len(dated) <= PROFILE_MAX_DATED and
                    len(candidate.encode("utf-8")) <= PROFILE_MAX_BYTES):
                break
            if not bullets:
                break
            removed.append(body.pop(bullets[-1]).strip())
        text = head + sep + "\n".join(body)
        if not text.endswith("\n"):
            text += "\n"
    too_big = len(text.encode("utf-8")) > PROFILE_MAX_BYTES
    return text, removed, dedup, too_big


def _archive_profile_bullets(path, bullets):
    if not bullets:
        return ""
    dest = _profile_history_path(path)
    ensure_private_dir(os.path.dirname(dest))
    with open(dest, "a", encoding="utf-8") as f:
        f.write("\n\n<!-- archived %s -->\n" % time.strftime("%Y-%m-%dT%H:%M:%S"))
        for bullet in bullets:
            f.write(bullet + "\n")
    os.chmod(dest, 0o600)
    return dest


def append_profile_note(platform, alias, node, note):
    path = ensure_profile(platform, alias, node)
    try:
        with open(path) as f:
            text = f.read()
    except OSError:
        text = _profile_template(alias, platform, node.get("chat_id") or "")
    if "## 历史结论" not in text:
        text = text.rstrip() + "\n\n## 历史结论\n"
    head, tail = text.split("## 历史结论", 1)
    rest = tail.lstrip("\n")
    bullet = "- " + note
    if bullet not in text:
        text = head + "## 历史结论\n\n" + bullet
        if rest.strip():
            text += "\n\n" + rest.rstrip() + "\n"
        else:
            text += "\n"
        text, removed, _dedup, too_big = _compact_profile_text(text)
        atomic_write_text(path, text)
        _archive_profile_bullets(path, removed)
        if too_big:
            print("WARN: 画像仍超过 12KB，请运行 --compact 或手动压缩", file=sys.stderr)
    return path


def compact_profile(platform, alias, dry_run=False):
    env = load_env()
    node = env.get("targets", {}).get(platform, {}).get(alias)
    if not node:
        print(f"ERROR: 别名未注册: {platform} / {alias}", file=sys.stderr)
        return 2
    path = ensure_profile(platform, alias, node)
    save_env(env)
    try:
        with open(path) as f:
            text = f.read()
    except OSError as e:
        print(f"ERROR: 读不到画像: {e}", file=sys.stderr)
        return 2
    before = len(text.encode("utf-8"))
    new_text, removed, dedup, too_big = _compact_profile_text(text)
    after = len(new_text.encode("utf-8"))
    summary = (f"{before / 1024:.1f}KB -> {after / 1024:.1f}KB，"
               f"去重 {dedup} 条，归档 {len(removed)} 条")
    if dry_run:
        print(f"[dry-run] 画像整理预演: {summary}")
        return 0
    if new_text != text:
        atomic_write_text(path, new_text)
    dest = _archive_profile_bullets(path, removed)
    print(f"[ok] 画像已整理: {summary}" + (f" -> {dest}" if dest else ""))
    if too_big:
        print("WARN: 画像仍超过 12KB，请压缩「对方是谁 / 沟通偏好 / 在意与忌讳」段",
              file=sys.stderr)
        return 2
    return 0

PLATFORMS = {
    "feishu": {
        "cli": "lark-cli",
        "cmd_whoami": ["auth", "status"],
        "f_self_id": [["identities", "user", "openId"]],
        "listen_script": "feishu_listen_cli.py",
        "id_label": "open_id (ou_xxx)",
        # ① 精准解析：按名字搜人（一次调用拿到 open_id + p2p_chat_id，最优先）
        "cmd_user_search": ["contact", "+search-user", "--as", "user",
                            "--query", "{query}"],
        "f_user_items": [["data", "users"], ["users"]],
        "f_user_id": [["open_id"]],
        "f_user_name": [["localized_name"], ["name"]],
        "f_user_chat": [["p2p_chat_id"]],
        # ② 按群名搜群（只搜可见群，不拉全量）
        "cmd_chat_search": ["im", "+chat-search", "--as", "user",
                            "--query", "{query}"],
        "f_search_items": [["data", "chats"], ["data", "items"], ["chats"]],
        # ③ 最近会话（几十条，比全量 chat-list 便宜得多）
        "cmd_recent": ["im", "+feed-shortcut-list", "--as", "user"],
        "f_recent_items": [["data", "shortcuts"], ["shortcuts"]],
        # ④ 全量列表（最后手段，必须配合页数上限）
        "cmd_chats": ["im", "+chat-list", "--as", "user", "--types=p2p,group"],
        "f_chat_items": [["data", "chats"], ["chats"], ["items"]],
        "f_chat_id": [["chat_id"]],
        "cmd_msgs": ["im", "+chat-messages-list", "--chat-id", "{chat_id}",
                     "--order", "desc", "--limit", "50", "--as", "user"],
        "f_msg_items": [["data", "messages"], ["messages"], ["items"]],
        "f_msg_sender": [["sender", "id"], ["sender", "sender_id", "open_id"]],
        "f_msg_content": [["content"], ["body", "content"]],
        "reply_user": 'lark-cli im +messages-send --chat-id {chat_id} --msg-type text '
                      '--as user --text "$(cat /tmp/reply.txt)"',
        "reply_group": 'lark-cli im +messages-send --chat-id {chat_id} --msg-type text '
                       '--as user --text "$(cat /tmp/reply.txt)"',
    },
    "wecom": {
        "cli": "wecom-cli",
        "cmd_whoami": ["auth", "show"],
        "self_id_regex": r"Bot ID:\s*(\S+)",
        "f_self_id": [["bot_id"]],
        "listen_script": "wecom_listen_cli.py",
        "id_label": "bot_id",
        # 通讯录检索（实测：contact users search --keywords）
        "cmd_user_search": ["contact", "users", "search", "--keywords", "{query}"],
        "f_user_items": [["users"], ["data", "users"]],
        "f_user_id": [["userid"], ["user_id"]],
        "f_user_name": [["name"], ["display_name"]],
        # 企微单聊 chat_id 就是对方 userid，故 f_user_chat 留空，resolve 时用 userId 兜底
        "f_user_chat": [["chat_id"], ["p2p_chat_id"]],
        # 会话列表只返回群聊，且必须带时间窗（仅最近 7 天）
        "cmd_chats": ["chat", "groups", "list",
                      "--begin-time", "{begin_time}", "--end-time", "{end_time}"],
        "f_chat_items": [["chats"], ["data", "chats"]],
        "f_chat_id": [["chat_id"]],
        "cmd_msgs": ["chat", "messages", "list", "--chat-id", "{chat_id}",
                     "--begin-time", "{begin_time}", "--end-time", "{end_time}"],
        "f_msg_items": [["messages"], ["data", "messages"]],
        "f_msg_sender": [["userid"], ["from", "userid"]],
        "f_msg_content": [["text", "content"], ["content"]],
        "supports_page_all": False,
        "reply_user": "wecom-cli message send --chat-id {chat_id} --msg-type text "
                      "--text '{{\"content\":\"...\"}}'  # chat_id 传对方 userid，text 是 JSON 对象",
        "reply_group": "wecom-cli message send --chat-id {chat_id} --msg-type text "
                       "--text '{{\"content\":\"...\"}}'  # chat_id 传群会话 ID",
    },
    "dingtalk": {
        "cli": "dws",
        "cmd_whoami": ["profile", "list"],
        "f_self_id": [["profiles", 0, "userId"], ["current", "userId"]],
        "listen_script": "dingtalk_listen_cli.py",
        "id_label": "userId",
        "cmd_user_search": ["contact", "user", "search", "--query", "{query}"],
        "f_user_items": [["result"], ["users"], ["data", "result"]],
        "f_user_id": [["userId"], ["userid"], ["openDingTalkId"]],
        "f_user_name": [["name"], ["nick"], ["displayName"]],
        "f_user_chat": [["openDingTalkId"], ["openConversationId"]],
        "cmd_chat_search": ["chat", "+chat-search", "--query", "{query}"],
        "f_search_items": [["chats"], ["conversations"], ["result"], ["items"]],
        "cmd_recent": ["chat", "+recent-conversations"],
        # 实测返回 {"ok":true,"data":{"conversations":[{conversationId,name,type}]}}
        "f_recent_items": [["data", "conversations"], ["conversations"], ["items"], ["result"], ["chats"]],
        "cmd_chats": ["chat", "+chat-list"],
        "f_chat_items": [["conversations"], ["chats"], ["items"], ["result"]],
        "f_chat_id": [["openConversationId"], ["conversationId"], ["chatId"]],
        "cmd_msgs": ["chat", "+chat-messages", "--group", "{chat_id}", "--limit", "50"],
        "f_msg_items": [["messages"], ["data", "messages"], ["result", "messages"]],
        "f_msg_sender": [["senderId"], ["sender", "userId"], ["sender"]],
        "f_msg_content": [["text", "content"], ["text"], ["content"]],
        "supports_page_all": False,
        "reply_user": 'dws chat +messages-send --as user --user {chat_id} '
                      '--text "$(cat /tmp/reply.txt)"',
        "reply_group": 'dws chat +messages-send --as user --chat-id {chat_id} '
                       '--text "$(cat /tmp/reply.txt)"',
    },
}


def dig(obj, *paths):
    """按候选路径取值，返回第一个命中的。

    兼容三种写法：
      dig(x, [["a","b"], ["c"]])   # 一条列表，元素是路径
      dig(x, ["a","b"])            # 单条路径
      dig(x, ["a","b"], ["c"])     # 多条路径
    """
    if len(paths) == 1:
        p = paths[0]
        if isinstance(p, (list, tuple)) and (not p or isinstance(p[0], (list, tuple))):
            cand = list(p)
        else:
            cand = [p]
    else:
        cand = list(paths)
    for p in cand:
        cur, ok = obj, True
        for k in (p if isinstance(p, (list, tuple)) else [p]):
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            elif isinstance(cur, list) and isinstance(k, int) and -len(cur) <= k < len(cur):
                cur = cur[k]
            else:
                ok = False
                break
        if ok:
            return cur
    return None


def load_env():
    try:
        with open(ENV_PATH) as f:
            return json.load(f)
    except Exception:
        return {"version": 1, "platforms": {}, "targets": {}, "field_overrides": {}}


def save_env(env):
    ensure_private_dir(ENV_DIR)
    env["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    atomic_write_json(ENV_PATH, env, indent=2)
    secure_tree(ENV_DIR)


def run(cli, args, timeout=20):
    try:
        p = subprocess.run([cli] + args, capture_output=True, text=True, timeout=timeout)
    except Exception as e:
        return 127, None, str(e)
    raw = (p.stdout or "").strip()
    # 部分 CLI 连续输出多个 JSON 文档，只取第一个
    try:
        obj, _end = json.JSONDecoder().raw_decode(raw.lstrip())
        return p.returncode, obj, raw
    except Exception:
        return p.returncode, None, raw


def fmt(tmpl, **kw):
    """模板展开：未提供的占位键保留原样，不会抛异常。"""
    out = []
    for a in tmpl:
        try:
            out.append(a.format(**kw))
        except (KeyError, IndexError):
            out.append(a)
    return out


def window(minutes=4320):
    """时间窗占位（默认近 3 天，企微单次最多 7 天）。"""
    end = time.time()
    begin = end - minutes * 60
    f = "%Y-%m-%d %H:%M:%S"
    return {"begin_time": time.strftime(f, time.localtime(begin)),
            "end_time": time.strftime(f, time.localtime(end)),
            "now": time.strftime(f, time.localtime(end)),
            "now_ts": int(end), "begin_ts": int(begin), "end_ts": int(end)}


def detect(env):
    found = {}
    for name, cfg in PLATFORMS.items():
        path = shutil.which(cfg["cli"])
        if not path:
            print(f"[skip] {name}: 未找到 {cfg['cli']}")
            continue
        rc, j, raw = run(cfg["cli"], cfg["cmd_whoami"])
        self_id = dig(j, cfg["f_self_id"]) if j else None
        if not self_id and cfg.get("self_id_regex") and raw:
            import re
            m = re.search(cfg["self_id_regex"], raw)
            if m:
                self_id = m.group(1)
        status = {
            "cli_path": path,
            "logged_in": bool(self_id),
            "self_id": self_id,
            "listen_script": cfg["listen_script"],
        }
        env["platforms"][name] = status
        found[name] = status
        mark = "OK" if self_id else "未登录/字段未识别"
        print(f"[{'ok' if self_id else 'warn'}] {name}: {cfg['cli']} -> {mark}"
              + (f"  本人 {cfg['id_label']}: {self_id}" if self_id else ""))
    return found


def smoke(env, platform, chat_id):
    cfg = PLATFORMS[platform]
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          cfg["listen_script"])
    # 用 --timeout 1 + 最小 interval 跑一轮：退出 3(超时) 即通路正常；2 才是故障
    p = subprocess.run([sys.executable, script, "--chat-id", chat_id,
                        "--interval", "2", "--timeout", "3"],
                       capture_output=True, text=True, timeout=30)
    if p.returncode == 3:
        print(f"[ok] {platform} 冒烟通过：拉取通路正常，无新消息命中")
        return True
    if p.returncode == 0:
        print(f"[ok] {platform} 冒烟通过：存量消息命中（--init zero 效果）")
        return True
    print(f"[fail] {platform} 冒烟失败 (rc={p.returncode}):", file=sys.stderr)
    print(p.stderr[:2000], file=sys.stderr)
    print("提示: 若是 SCHEMA_MISMATCH，对照原始输出修正 env.json 的 "
          f"field_overrides.{platform}", file=sys.stderr)
    return False


def collect_chats(env, platform, page_limit=3, extra_chats=None):
    """取候选会话，按成本从低到高降级，禁止无脑全量拉。

    顺序：① 显式 --chats ② env.json 已注册 targets
         ③ 最近会话 feed-shortcut-list（几十条）④ 全量 chat-list（限页数兜底）
    返回 [(chat_id, 标签)]
    """
    cfg = PLATFORMS[platform]
    out, seen = [], set()

    def push(cid, label=""):
        if cid and cid not in seen:
            seen.add(cid)
            out.append((cid, label))

    for cid in (extra_chats or []):
        push(cid, "explicit")
    if out:
        return out

    for alias, t in (env.get("targets", {}).get(platform, {}) or {}).items():
        push(t.get("chat_id"), alias)
    if out:
        return out

    if cfg.get("cmd_recent"):
        rc, j, raw = run(cfg["cli"], cfg["cmd_recent"])
        if rc == 0 and j is not None:
            for s in (dig(j, cfg["f_recent_items"]) or []):
                d = s.get("detail") or s
                push(dig(d, cfg["f_chat_id"]), "recent")
            if out:
                return out

    # 兜底：会话列表。平台支持自动翻页时限制页数（默认 3 页≈60 条），
    # 避免拉穿几千会话；不支持翻页的平台（企微/钉钉）直接按时间窗取一页。
    argv = fmt(cfg["cmd_chats"], **window())
    if cfg.get("supports_page_all", True):
        argv += ["--page-all", "--page-limit", str(page_limit)]
    rc, j, raw = run(cfg["cli"], argv, timeout=60)
    if rc != 0 or j is None:
        print(f"WARN: 拉会话列表失败，跳过全量兜底: {raw[:300]}", file=sys.stderr)
        return out
    for ch in (dig(j, cfg["f_chat_items"]) or []):
        push(dig(ch, cfg["f_chat_id"]), "list")
    return out


def learn_style(env, platform, limit, chats=None, retention_days=30):
    """仅从显式选择的会话提取脱敏语料，并按保留期清理旧记录。"""
    if not chats:
        print("ERROR: 学风格必须显式给 --chats id1,id2；不会默认枚举最近/全部会话",
              file=sys.stderr)
        sys.exit(2)
    cfg = PLATFORMS[platform]
    st = env.get("platforms", {}).get(platform, {})
    self_id = st.get("self_id")
    if not self_id:
        print(f"ERROR: {platform} 本人 ID 未知，先跑 bootstrap.py 探测", file=sys.stderr)
        sys.exit(2)
    ensure_private_dir(ENV_DIR)
    corpus_path = os.path.join(ENV_DIR, "self_corpus.jsonl")
    collected, seen = [], set()
    now = time.time()
    cutoff = now - retention_days * 86400 if retention_days > 0 else None
    if os.path.exists(corpus_path):
        legacy_ts = os.path.getmtime(corpus_path)
        with open(corpus_path, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    content = rec.get("content", "")
                    if not usable_style_text(content):
                        continue
                    content = redact_sensitive(content.strip())
                    collected_at = float(rec.get("collected_at") or legacy_ts)
                    if not content or content in seen:
                        continue
                    if cutoff is not None and collected_at < cutoff:
                        continue
                    rec["content"] = content
                    rec["collected_at"] = collected_at
                    seen.add(content)
                    collected.append(rec)
                except Exception:
                    pass

    candidates = collect_chats(env, platform, extra_chats=chats)
    if not candidates:
        print("ERROR: --chats 没有可用会话 ID", file=sys.stderr)
        sys.exit(2)
    print(f"[info] 语料来源会话 {len(candidates)} 个："
          + ", ".join(f"{lbl or cid}" for cid, lbl in candidates[:8])
          + (" ..." if len(candidates) > 8 else ""))
    new_count = 0
    for chat_id, _lbl in candidates:
        if new_count >= limit:
            break
        rc2, j2, _ = run(cfg["cli"],
                         fmt(cfg["cmd_msgs"], chat_id=chat_id, **window()))
        if rc2 != 0 or j2 is None:
            continue
        for m in (dig(j2, cfg["f_msg_items"]) or []):
            if new_count >= limit:
                break
            if dig(m, cfg["f_msg_sender"]) != self_id:
                continue
            content = (dig(m, cfg["f_msg_content"]) or "").strip()
            if not usable_style_text(content):
                continue
            content = redact_sensitive(content)
            if not content or content in seen:
                continue
            seen.add(content)
            collected.append({"platform": platform, "chat_id": chat_id,
                              "content": content, "collected_at": now})
            new_count += 1

    payload = "".join(json.dumps(rec, ensure_ascii=False) + "\n" for rec in collected)
    atomic_write_text(corpus_path, payload)
    retention = f"{retention_days} 天" if retention_days > 0 else "不限"
    print(f"[ok] 脱敏语料已写入 {corpus_path}（本次新增 {new_count} 条，"
          f"累计 {len(collected)} 条，保留期 {retention}）")
    print("下一步：agent 通读语料，只提炼风格写入 ~/.im-standin/persona.md，不复制事实与凭据")


def load_adapter(platform):
    """从平台入口脚本里读 ADAPTER，供 probe/selftest 复用同一份配置。"""
    import importlib.util
    cfg = PLATFORMS[platform]
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cfg["listen_script"])
    spec = importlib.util.spec_from_file_location(f"_ad_{platform}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ADAPTER


def probe(platform, chat_id="", user_id=""):
    """校准探针：把 CLI 的真实形态打出来，并生成可直接粘贴的 override 模板。

    只读操作（--help / 列消息），不发消息、不改配置。
    """
    cfg = PLATFORMS[platform]
    cli = cfg["cli"]
    print(f"== probe {platform} ({cli}) ==")
    if not shutil.which(cli):
        print(f"[fail] 未找到 {cli}，先安装并登录")
        sys.exit(2)

    rc, j, raw = run(cli, ["--help"], timeout=20)
    print(f"\n-- {cli} --help (rc={rc}) --")
    body = raw if raw else (j if isinstance(j, str) else json.dumps(j, ensure_ascii=False))
    print("\n".join((body or "").splitlines()[:45]))

    rc, j, raw = run(cli, cfg["cmd_whoami"], timeout=20)
    print(f"\n-- whoami (rc={rc}) --")
    print((raw or "")[:800])
    sid = dig(j, cfg["f_self_id"]) if j else None
    if not sid and cfg.get("self_id_regex") and raw:
        import re
        m = re.search(cfg["self_id_regex"], raw)
        sid = m.group(1) if m else None
    print(f"解析到本人 ID: {sid or '(失败)'}")

    ad = load_adapter(platform)
    plans = []  # (label, 命令模板列表, 目标值)
    if chat_id:
        plans.append(("chat", ad.get("cmd_list_chain") or [ad.get("cmd_list")], chat_id))
    if user_id:
        # 平台没有独立"按人"命令时，退化为把 userid 当 chat_id 传入（企微即如此）
        chain = [ad["cmd_list_user"]] if ad.get("cmd_list_user") else \
                (ad.get("cmd_list_chain") or [ad.get("cmd_list")])
        plans.append(("user", chain, user_id))
    if not plans:  # 没给目标：只列出候选，供人看
        for label, chain in (("chat", ad.get("cmd_list_chain") or [ad.get("cmd_list")]),
                             ("user", [ad["cmd_list_user"]] if ad.get("cmd_list_user") else [])):
            print(f"\n-- 消息命令候选（{label}，未给目标只列候选）--")
            for t in [c for c in chain if c]:
                print("   ", " ".join(t))
    for label, chain, target in plans:
        chain = [c for c in chain if c]
        if not chain:
            continue
        print(f"\n-- 消息命令候选（{label}）--")
        for t in chain:
            argv = fmt(t, chat_id=target, user_id=target, target=target, id=target,
                       **window())
            rc, j, raw = run(cli, argv, timeout=20)
            status = "OK" if rc == 0 and j is not None else f"rc={rc}"
            n, keys = "-", "-"
            if j is not None:
                items = dig(j, ad.get("f_items"))
                if isinstance(items, list):
                    n = len(items)
                    keys = ",".join(list(items[0].keys())[:8]) if items else "-"
                else:
                    keys = "顶层键: " + ",".join(list(j.keys())[:8])
            print(f"  [{'hit' if n != '-' else status}] {' '.join(argv)}")
            print(f"        items={n}  字段={keys}")

    print("\n-- 当前字段映射（写 override 时按这个键名）--")
    for k, v in ad.items():
        if k.startswith("f_"):
            print(f"  {k}: {json.dumps(v, ensure_ascii=False)}")

    print(f"""
-- 校准方法 --
1. 从上面第一条 [hit] 的命令里确认：消息数组在哪 → 改 f_items；
   消息 ID / 发送者 / 正文 / 时间字段 → 改 f_msg_id / f_sender / f_content_list / f_create_time
2. 写入 {ENV_PATH}：
   "overrides": {{"{platform}": {{"f_items": [["实际","路径"]],
                              "cmd_list": ["实际","命令","--chat-id","{{chat_id}}"]]}}}}
3. 复测：python3 scripts/bootstrap.py --selftest {platform} <会话ID>""")


def selftest(platform, chat_id):
    """跑一轮真实监听（3 秒），用退出码判断通路是否成立。"""
    cfg = PLATFORMS[platform]
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          cfg["listen_script"])
    p = subprocess.run([sys.executable, script, "--chat-id", chat_id,
                        "--interval", "2", "--timeout", "3"],
                       capture_output=True, text=True, timeout=60)
    if p.returncode == 3:
        print(f"[ok] {platform} 自检通过：拉取通路正常，3 秒内无新消息")
        return True
    if p.returncode == 0:
        print(f"[ok] {platform} 自检通过：命中存量消息（--init zero 效果）")
        print("     " + (p.stdout or "").strip()[:300])
        return True
    print(f"[fail] {platform} 自检失败 rc={p.returncode}", file=sys.stderr)
    print((p.stderr or "")[:1500], file=sys.stderr)
    print(f"提示: 先用 --probe {platform} <会话ID> 对照实际字段，再写 overrides", file=sys.stderr)
    return False


def resolve(env, platform, query, register=True):
    """按名字精准解析目标 → 用户 ID + 会话 ID，不拉全量列表。

    优先级：① 搜人（关键词检索，飞书直接回 p2p_chat_id）
           ② 搜群（按群名/成员名）
           ③ 最近/会话列表本地关键词过滤（兜底，企微/钉钉常用）
    命中唯一时自动登记到 env.json 的 targets。
    """
    cfg = PLATFORMS[platform]
    hits = []
    self_id = (env.get("platforms", {}).get(platform, {}) or {}).get("self_id")

    # ① 搜人：支持命令链（不同 CLI 版本子命令不同）
    chains = []
    if cfg.get("cmd_user_search_chain"):
        chains.append(cfg["cmd_user_search_chain"])
    if cfg.get("cmd_user_search"):
        chains.append([cfg["cmd_user_search"]])
    for chain in chains:
        got = []
        for tmpl in chain:
            rc, j, raw = run(cfg["cli"], fmt(tmpl, query=query, **window()))
            if rc != 0 or j is None:
                continue
            items = dig(j, cfg["f_user_items"])
            if items is None:
                continue
            for u in items:
                uid = dig(u, cfg["f_user_id"]) or ""
                cid = dig(u, cfg["f_user_chat"]) or ""
                # 企微/钉钉单聊的 chat_id 支持直接用 userId，缺会话 ID 时以此兜底
                if not cid:
                    cid = uid
                got.append({
                    "kind": "user",
                    "name": dig(u, cfg["f_user_name"]) or "",
                    "open_id": uid,
                    "chat_id": cid,
                    "extra": {k: u.get(k) for k in
                              ("department", "departments", "email", "position",
                               "has_chatted", "chat_recency_hint")
                              if u.get(k)},
                })
            break  # 这条链第一个可用命令就够
        if got:
            hits = got
            break

    # ② 搜群
    if not hits and cfg.get("cmd_chat_search"):
        rc, j, raw = run(cfg["cli"],
                         fmt(cfg["cmd_chat_search"], query=query, **window()))
        if rc == 0 and j is not None:
            for c in (dig(j, cfg["f_search_items"]) or []):
                hits.append({
                    "kind": "chat",
                    "name": c.get("name") or "",
                    "open_id": "",
                    "chat_id": dig(c, cfg["f_chat_id"]) or "",
                    "extra": {"chat_mode": c.get("chat_mode"),
                              "member_count": c.get("user_count")},
                })

    # ③ 兜底：最近会话/会话列表里按名字过滤（仅几十条，成本可控）
    if not hits:
        for cid, _lbl in collect_chats(env, platform, page_limit=2):
            rc, j, _raw = run(cfg["cli"],
                              fmt(cfg["cmd_msgs"], chat_id=cid, **window()))
            if rc != 0 or j is None:
                continue
            names = set()
            for m in (dig(j, cfg["f_msg_items"]) or [])[:50]:
                nm = dig(m, ["sender", "name"], ["sender_name"], ["from", "name"])
                if nm:
                    names.add(nm)
            if any(query in n for n in names):
                hits.append({"kind": "chat", "name": " / ".join(sorted(names))[:40],
                             "open_id": "", "chat_id": cid,
                             "extra": {"matched": "message-sender"}})

    if not hits:
        print(f"[none] 未解析到「{query}」（换关键词，或直接给会话/用户 ID）",
              file=sys.stderr)
        sys.exit(2)

    print(f"[hit] 「{query}」命中 {len(hits)} 个：")
    for i, h in enumerate(hits, 1):
        print(f"  {i}. [{h['kind']}] {h['name']}  chat_id={h['chat_id'] or '-'} "
              f"open_id={h['open_id'] or '-'}")
        if h["extra"]:
            print("     " + " · ".join(f"{k}={v}" for k, v in h["extra"].items()))

    if len(hits) == 1 and register:
        h = hits[0]
        alias = h["name"] or query
        targets = env.setdefault("targets", {}).setdefault(platform, {})
        t = targets.setdefault(alias, {})
        t.update({"chat_id": h["chat_id"], "open_id": h["open_id"],
                  "kind": h["kind"], "added_at": time.strftime("%Y-%m-%d")})
        ensure_profile(platform, alias, t)
        save_env(env)
        print(f"\n[ok] 已登记别名: {platform} / {alias}")
        listen = (f"python3 scripts/{cfg['listen_script']} --chat-id {h['chat_id']}"
                  if h["kind"] == "chat" or platform == "feishu" else
                  f"python3 scripts/{cfg['listen_script']} --user-id {h['chat_id']}")
        print(f"     监听: {listen}" + (f" --sender {h['open_id']}"
                                       if h["kind"] == "user" and h["open_id"] != h["chat_id"]
                                       else ""))
        reply_tpl = (cfg.get("reply_group") if h["kind"] == "chat"
                     else cfg.get("reply_user")) or cfg.get("reply_user") or ""
        if reply_tpl:
            print(f"     回复: {reply_tpl.format(chat_id=h['chat_id'])}")
    elif len(hits) > 1:
        print("\n[note] 多个候选未自动登记，用 --alias PLATFORM 别名 CHAT_ID 指定。")
    return hits


def delete_data(confirm=False):
    if not confirm:
        print("ERROR: --delete-data 会删除 env.json、画像、语料、persona 和水位；"
              "确认请追加 --yes", file=sys.stderr)
        return 2
    removed = []
    for name in ("env.json", "self_corpus.jsonl", "persona.md"):
        path = os.path.join(ENV_DIR, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
            removed.append(name)
    states = os.path.join(ENV_DIR, "states")
    if os.path.isdir(states) and not os.path.islink(states):
        shutil.rmtree(states)
        removed.append("states/")
    if os.path.isdir(PROFILES_DIR) and not os.path.islink(PROFILES_DIR):
        shutil.rmtree(PROFILES_DIR)
        removed.append("profiles/")
    print("[ok] 已删除个人数据: " + (", ".join(removed) or "无文件"))
    return 0


def main():
    ap = argparse.ArgumentParser(description="cyber-im-avatar 首装环境自适配")
    ap.add_argument("--find", nargs=2, metavar=("PLATFORM", "QUERY"),
                    help="按名字精准解析目标（人/群）→ chat_id，命中唯一自动登记别名")
    ap.add_argument("--probe", metavar="PLATFORM",
                    help="校准探针：打印 CLI 真实形态 + 生成 override 模板（只读）")
    ap.add_argument("--selftest", nargs=2, metavar=("PLATFORM", "CHAT_ID"),
                    help="自检：真跑一轮 3 秒监听，验证通路")
    ap.add_argument("--chat-id", default="", help="配合 --probe 的消息命令试跑")
    ap.add_argument("--user-id", default="", help="配合 --probe 试跑按人监听命令")
    ap.add_argument("--smoke", nargs=2, metavar=("PLATFORM", "CHAT_ID"),
                    help="对指定会话冒烟测试")
    ap.add_argument("--alias", nargs=3, metavar=("PLATFORM", "ALIAS", "CHAT_ID"),
                    help="注册会话别名，之后可用别名指代会话")
    ap.add_argument("--note", nargs=3, metavar=("PLATFORM", "ALIAS", "TEXT"),
                    help="给服务对象追加一条档案（喜好/忌讳/关系/历史结论）")
    ap.add_argument("--compact", nargs=2, metavar=("PLATFORM", "ALIAS"),
                    help="整理画像：去重 + 把最旧的历史结论归档到 .history.md")
    ap.add_argument("--dry-run", action="store_true",
                    help="配合 --compact 只打印整理结果，不写盘")
    ap.add_argument("--learn-style", metavar="PLATFORM",
                    help="从 --chats 显式选择的会话抓本人语料并脱敏")
    ap.add_argument("--chats", default="",
                    help="语料来源会话 ID（逗号分隔；学风格时必填，禁止默认枚举）")
    ap.add_argument("--retention-days", type=int, default=30,
                    help="语料保留天数，默认 30；0=不限")
    ap.add_argument("--delete-data", action="store_true",
                    help="删除 env.json、语料、persona 和水位（必须加 --yes）")
    ap.add_argument("--yes", action="store_true", help="确认 --delete-data")
    ap.add_argument("--page-limit", type=int, default=3,
                    help="全量列表兜底的最大页数（默认 3 页≈60 会话）")
    ap.add_argument("--limit", type=int, default=100, help="语料抓取条数上限")
    args = ap.parse_args()

    if args.delete_data:
        sys.exit(delete_data(args.yes))

    env = load_env()
    if args.probe:
        probe(args.probe, args.chat_id, args.user_id)
        return

    if args.selftest:
        platform, chat_id = args.selftest
        sys.exit(0 if selftest(platform, chat_id) else 2)

    if args.find:
        platform, query = args.find
        if platform not in env.get("platforms", {}):
            detect(env)
            save_env(env)
        resolve(env, platform, query)
        return

    if args.alias:
        platform, alias, chat_id = args.alias
        node = env.setdefault("targets", {}).setdefault(platform, {}).setdefault(alias, {})
        node.update({"chat_id": chat_id, "added_at": time.strftime("%Y-%m-%d")})
        ensure_profile(platform, alias, node)
        save_env(env)
        print(f"[ok] 别名已注册: {platform} / {alias} -> {chat_id}")
        return

    if args.note:
        platform, alias, text = args.note
        t = env.setdefault("targets", {}).setdefault(platform, {}).get(alias)
        if not t:
            print(f"ERROR: 别名未注册: {platform} / {alias}", file=sys.stderr)
            sys.exit(2)
        path = append_profile_note(platform, alias, t, text)
        save_env(env)
        print(f"[ok] 画像已追加: {path}")
        return

    if args.compact:
        platform, alias = args.compact
        sys.exit(compact_profile(platform, alias, args.dry_run))

    if args.learn_style:
        if args.retention_days < 0:
            print("ERROR: --retention-days 不能小于 0", file=sys.stderr)
            sys.exit(2)
        if args.learn_style not in env.get("platforms", {}):
            detect(env)
            save_env(env)
        chats = [c.strip() for c in args.chats.split(",") if c.strip()] or None
        learn_style(env, args.learn_style, args.limit, chats=chats,
                    retention_days=args.retention_days)
        return

    found = detect(env)
    save_env(env)
    if not found:
        print("\n未探测到任何可用平台 CLI。请先安装 lark-cli / wecom-cli / dws 其一。")
        sys.exit(2)
    print(f"\n环境档案已写入 {ENV_PATH}")

    if args.smoke:
        platform, chat_id = args.smoke
        if platform not in found:
            print(f"平台 {platform} 未就绪", file=sys.stderr)
            sys.exit(2)
        sys.exit(0 if smoke(env, platform, chat_id) else 2)


if __name__ == "__main__":
    main()
