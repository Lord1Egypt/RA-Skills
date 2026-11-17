#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dingtalk_api.py —— 钉钉交互层。

封装所有与钉钉/ dws CLI 的交互：dws 调用路由、未读/消息拉取、单聊·群聊判定、
@我检测、图片 mediaId 提取与下载、消息发送（代复/发给自己）。

所有共享常量与运行期辅助来自 runtime.py（本模块只 import 需要的名字）。
注意：会被运行时修改的「可变配置」（DRY_RUN、SELF_OPEN_ID）一律通过
runtime.DRY_RUN / runtime.SELF_OPEN_ID 访问，避免 import 副本导致外部脚本改不动。
"""
import os, sys, json, time, datetime, re
import subprocess
import tempfile as _tempfile
import runtime
from runtime import (
    CREATE_NO_WINDOW, DWS_CMD, DWS_EXE, DWS_ENTRY, NODE, _DWS_CALL_TRACE,
    MEDIA_CACHE_DIR, DEBUG_LOG, DEBUG_LOG_MAX, log_debug,
    SELF_SENDERS, GROUP_PUSH, MENTION_NAMES,
    _MEDIA_RE, _PIC_TAG_RE, _MEDIA_EMPTY_RE, _NON_IMAGE_TAG_RE,
    _DWS_HINT_RE, _DWS_HINT_RE2,
    _RECENT_CACHE, ACTIVE_WINDOW_SEC, LAST_SELF_SENT,
)


def _run_dws_once(cmd, env, timeout):
    """执行一次 dws 子进程，返回 stdout 字符串；失败返回 None（供上层路由降级）。

    唯一定型方案：文件重定向（2026-07-15 石锤 + 重启验证）。
    dws.exe 为 Node 打包二进制，process.stdout 对匿名管道（PIPE）异步写、进程退出前未
    flush → 管道读到 0 字节；与父进程是否控制台无关（python.exe console 环境重启后仍复现）。
    故一律用临时文件承接 stdout（subprocess.run(stdout=file) → dws 同步落盘 → read），
    彻底规避 PIPE 异步丢失。不再尝试 PIPE，不再保留降级标志。"""
    if _DWS_CALL_TRACE:
        log_debug("[dws-call] argv=" + " ".join(cmd))
    fd, tmp_path = _tempfile.mkstemp(suffix=".json", prefix="dws_out_")
    os.close(fd)  # 关闭 fd，用 open() 重新打开以控制编码
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            r = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True,
                               env=env, timeout=timeout, creationflags=CREATE_NO_WINDOW)
        if r.returncode != 0:
            log_debug(f"[dws-file] rc={r.returncode} stderr={(r.stderr or '')[:300]}")
            return None
        with open(tmp_path, "r", encoding="utf-8") as f:
            out = f.read()
        if out and out.strip():
            return out
        return None
    except Exception as e:
        log_debug(f"[dws-file] error: {e}")
        return None
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def run_dws(args, timeout=30):
    env = dict(os.environ)
    env["DINGTALK_DWS_AGENTCODE"] = "workbuddy"
    out = None
    # 路由优先级（调用目标不同，输出一律走文件重定向，见 _run_dws_once 根因）：
    # 1. DIRECT-exe：直接调 dws.exe，绕过 node+dws.js 壳（快速路径）。
    # 2. NODE-direct：node + dws.js（兼容回退）。
    # 3. DWS_CMD：cmd /c dws.cmd（最后兜底）。
    # 空串（""）/None 都降级到下一路由。
    if DWS_EXE and os.path.exists(DWS_EXE):
        if _DWS_CALL_TRACE:
            log_debug(f"[dws-route] DIRECT-exe: {DWS_EXE}")
        out = _run_dws_once([DWS_EXE] + args, env, timeout)
        if out is not None and not out.strip():
            log_debug("[dws-route] DIRECT-exe returned empty stdout, falling back to NODE-direct")
    if not out and DWS_ENTRY and NODE and os.path.exists(NODE) and os.path.exists(DWS_ENTRY):
        if _DWS_CALL_TRACE:
            log_debug(f"[dws-route] NODE-direct: NODE={NODE} ENTRY={DWS_ENTRY}")
        out = _run_dws_once([NODE, DWS_ENTRY] + args, env, timeout)
        if out is not None and not out.strip():
            log_debug("[dws-route] NODE-direct returned empty stdout, falling back to DWS_CMD")
    if not out and DWS_CMD and os.path.exists(DWS_CMD):
        # ⚠️ 2026-08-13 防御（命令注入/截断）：cmd /c 会对拼接后的命令行做二次元字符解析。
        # 若 args 含 AI 生成的回复正文（send_reply 的 --text），其中的 & | < > ^ % " 会被
        # cmd.exe 当作元字符截断甚至误执行。DIRECT-exe / NODE-direct 两条路由不经 cmd、无此风险；
        # 仅落到本兜底路由时检测——含危险字符则放弃、返回失败（触发上层转人工），
        # 绝不冒险经 cmd 传递不可信文本。
        if any(ch in a for a in args for ch in '&|<>^%"'):
            log_debug("[dws-route] DWS_CMD-fallback 参数含 cmd 元字符，放弃该路由（防注入/截断）")
        else:
            dws_cmd = (["cmd", "/c", DWS_CMD] + args) if sys.platform.startswith("win") else ([DWS_CMD] + args)
            if _DWS_CALL_TRACE:
                log_debug(f"[dws-route] DWS_CMD-fallback: {DWS_CMD}")
            out = _run_dws_once(dws_cmd, env, timeout)
    if not out:
        if not (DWS_EXE and os.path.exists(DWS_EXE)) and not (DWS_ENTRY and NODE and os.path.exists(NODE) and os.path.exists(DWS_ENTRY)) and not (DWS_CMD and os.path.exists(DWS_CMD)):
            log_debug("dws error: 找不到可用的 dws 入口（DWS_EXE / DWS_ENTRY / DWS_CMD 均缺失）")
        return ""
    return out


def _dws_ok(out):
    """严格判断 dws 命令是否成功：解析 JSON 看 success/errcode，失败时返回 False。
    空输出、含 error、errcode!=0 都判失败；不再用"不含 error 即成功"的弱判据。"""
    if not out or not out.strip():
        return False
    try:
        data = json.loads(out)
        if isinstance(data, dict):
            if data.get("success") is False:
                return False
            errcode = data.get("errcode") or data.get("errCode") or data.get("code")
            if errcode not in (None, 0, "0"):
                return False
            res = data.get("result")
            if isinstance(res, dict) and res.get("success") is False:
                return False
            return True
    except Exception:
        pass
    low = out.lower()
    if "error" in low or "fail" in low:
        return False
    return ("success" in low) or ("发送成功" in out) or ("\"ok\"" in low)


def msg_field(msg, *names, default=""):
    for n in names:
        if n in msg and msg[n]:
            return msg[n]
    return default


def extract_sender_open_id(msg, default=""):
    """从钉钉消息里抽出发送者 openDingTalkId。

    跨 API 版本字段名不一：senderOpenDingTalkId / openDingTalkId / fromOpenDingTalkId。
    原先三处散落手写同一元组，曾因某处改别名另一处没改导致取到空值。
    集中于此（thin wrapper over msg_field），调用方统一用本函数，杜绝漂移。"""
    return msg_field(msg, "senderOpenDingTalkId", "openDingTalkId", "fromOpenDingTalkId", default=default)


def msg_sender_open_id(m):
    """取消息的 sender_open_id：优先取已归一化的 m['sender_open_id'] 字段
    （monitor 累积阶段写入），否则现抽原始字段。monitor._resolve_open_id 与
    累积逻辑共用，消除两处重复的 `m.get("sender_open_id") or extract_sender_open_id(m)`。"""
    return m.get("sender_open_id") or extract_sender_open_id(m)


def _norm_ts(v):
    """把时间值归一化为【秒级 epoch 浮点】（毫秒时间戳 > 1e11 除以 1000）。

    ⚠️ 2026-08-05 实锤根因（老板反馈"图片消息被误判最新、后发文字进背景"）：
    dws 的 `lastMsgCreateAt` 是【毫秒】（13 位，如 1584669332376），而消息对象里的
    createTime 常是【秒级字符串】（"2026-08-05 10:20:00"）或秒级数字——两者混用排序会
    差 1000 倍，毫秒值被误排到"最新"，burst 窗口锚点选错，连发的后续消息全部掉进背景历史，
    还导致 NOTIFIED 去重失效（job.ts 秒 vs lastMsgCreateAt 毫秒永不相等 → 重复处理）。
    统一用本函数归一化为秒，全链路（PENDING.msgs[].ts / job.ts / NOTIFIED / 排序）单位一致。
    """
    try:
        v = float(v)
    except Exception:
        return 0
    if not v:
        return 0
    if v > 1e11:  # 毫秒级（>1973 年之后所有合法时间戳都是 13 位毫秒）
        v /= 1000.0
    return v


def _msg_ts(m):
    """把消息的时间字段解析成可排序的时间戳（epoch 秒），解析失败退化为 0。
    用真实时间排序比字符串排序稳（避免时间格式变化导致排序错乱）。
    ⚠️ 数字分支必须走 _norm_ts：dws 偶发返回毫秒级 createTime（图片/媒体消息常见），
    不归一化会与秒级字符串混排差 1000 倍（见 _norm_ts 注释）。"""
    raw = msg_field(m, "createTime", "create_time", "time", default="")
    if not raw:
        return 0
    raw = str(raw)
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.datetime.strptime(raw[:26], fmt).timestamp()
        except Exception:
            pass
    return _norm_ts(raw)


_LAST_UNREAD_DIAG = 0.0  # 节流：拿到空未读/解析失败时，每 60s 最多记一条原始返回诊断


def _unread_diag(tag, out, extra=""):
    """节流记录 dws 原始返回，用于排查"后台/开机自启会话下 dws 拿不到未读"的确切原因。
    正常有未读时不记；只在空/异常时每 60s 记一次 raw 长度+头部，避免刷屏。"""
    global _LAST_UNREAD_DIAG
    now = time.time()
    if now - _LAST_UNREAD_DIAG >= 60:
        _LAST_UNREAD_DIAG = now
        log_debug(f"[dws-diag] {tag} | raw_len={len(out)} {extra} head={out[:180]!r}")


def get_unread():
    """返回 (convs, health) 元组，让主循环心跳能区分「真无消息」vs「dws 坏了」：
    - health="ok"    = dws 成功且有未读
    - health="empty" = dws 成功但无未读（健康，真无消息）
    - health="fail"   = dws 失败/超时/解析异常/显式 success!=True（不健康，读不到未读）
    旧版只返回 list，dws 挂了返回 [] 会被伪装成「unread_now=0 健康」，实际消息全漏。"""
    out = run_dws(["chat", "message", "list-unread-conversations", "--format", "json"])
    try:
        data = json.loads(out)
        convs = data.get("result", {}).get("conversations", []) or []
        success = data.get("success") if isinstance(data, dict) else None
        if success is True:
            # dws 显式成功 → 真健康
            health = "ok" if convs else "empty"
        else:
            # 解析成功但 success!=True（疑似故障）→ 视为 fail，记诊断
            _unread_diag("empty-conversations", out, f"success={success}")
            health = "fail"
        return convs, health
    except Exception as e:
        # 空串/非 JSON/超时返回——记原始返回，区分"命令失败"与"返回空"
        _unread_diag("parse-fail", out, f"err={e!r}")
        return [], "fail"


def _list_msgs_args(conv_id, n):
    """构造 `chat message list` 拉最近 n 条消息的 dws 参数（get_latest_msg / _fetch_recent 共用）。
    关键：必须带 --direction older，含义是「从给定时间往更早方向拉」；配合 --time now
    即返回「从现在往前」的最新消息、newest-first。
    时间上界推到「现在+10s」：dws list --direction older --time T 仅返回 T 之前(older)的消息；
    若 T=now(秒级截断)，落在 now 那一秒内的消息会被严格上界排除 → 偶发返回「上一条」。
    推到未来余量可保证边界消息必在窗口内，取到真正最新一条（修复「转发内容串到上一条」）。"""
    _t = datetime.datetime.now() + datetime.timedelta(seconds=10)
    tstr = _t.strftime("%Y-%m-%d %H:%M:%S")
    return ["chat", "message", "list", "--group", conv_id, "--time", tstr,
            "--direction", "older", "--limit", str(n), "--format", "json"]


def _parse_msgs(out):
    """解析 dws list 返回，得到按时间倒序的消息列表（newest-first）；失败返回 None。"""
    try:
        data = json.loads(out)
        msgs = data.get("result", {}).get("messages", []) or []
        return sorted(msgs, key=_msg_ts, reverse=True)
    except Exception:
        return None


def get_latest_msg(conv_id):
    """用 openConversationId 拉该会话最新一条消息（newest-first 取第一条）。
    加固：dws `list` 端点偶发限流会静默返回空，做一次 3s 退避重试。"""
    args = _list_msgs_args(conv_id, 5)
    for attempt in range(2):
        out = run_dws(args, timeout=40)
        msgs = _parse_msgs(out)
        if msgs:
            return msgs[0]
        if attempt == 0:
            time.sleep(3)
    return {}


def _fetch_recent(conv_id, n=10):
    """拉该会话最近 n 条消息（已按时间倒序），用于活跃检测/调试。
    返回：list（成功，可能为空）或 None（dws 失败/异常，未确认）。
    关键：失败时返回 None 且不缓存——一次抖动不应毒化整个延迟窗口的检测；
    窗口内 dws 恢复正常的那次轮询仍能抓到老板活跃。"""
    args = _list_msgs_args(conv_id, n)
    # 短时缓存（60s TTL）：仅缓存「成功」结果，省 dws 限流额度；
    # 失败结果（None）绝不缓存，留给下一轮重新尝试。
    cached = _RECENT_CACHE.get(conv_id)
    if cached and cached[0] > time.time():
        return cached[1]
    result = []
    ok = False
    for attempt in range(2):
        out = run_dws(args, timeout=40)
        if not _dws_ok(out):
            # 权限拒绝/限流/超时等：视为未确认，退避后重试
            if attempt == 0:
                time.sleep(3)
            continue
        msgs = _parse_msgs(out)
        if msgs is not None:
            result = msgs
            ok = True
            break
        if attempt == 0:
            time.sleep(3)
    if not ok:
        # 两次均未成功（权限拒绝/限流/超时/非 JSON）→ 返回 None（不缓存）
        log_debug(f"[_fetch_recent] dws failed for {conv_id}, return None")
        return None
    # 偶发限流：dws list 端点偶发限流会静默返回「成功但空列表」(_dws_ok=True,
    # messages=[])。若按旧逻辑当成功存 60s，会毒化整个 2min 延迟窗口的活跃检测——
    # 老板正回复时拉到空被缓存 → owner_recently_active 一律 False → 照发代复(07-17 事故)。
    # 修复：空结果只做极短 TTL(5s) 弱缓存，限流是瞬时的、几秒后重拉即拿到真实消息；
    # 非空结果仍用 60s 长缓存省 dws 配额。
    if not result:
        _RECENT_CACHE[conv_id] = (time.time() + 5, result)
        log_debug(f"[_fetch_recent] rate-limit-empty for {conv_id}, weak-cache 5s (no poison)")
    else:
        _RECENT_CACHE[conv_id] = (time.time() + 60, result)
    return result


def owner_recently_active(conv_id, within_sec=ACTIVE_WINDOW_SEC):
    """老板最近 within_sec 秒内是否在该会话发过消息。
    抢答防护核心信号：dws 拿不到老板在线状态，但能查会话消息归属——
    老板最近在该会话发过消息 → 大概率正拿着手机在跟，AI 不应代发。
    用 runtime.SELF_OPEN_ID 精确匹配（昵称兜底）。
    返回：True（正向证据：确凿活跃）/ None（dws 失败，未确认）/ False（确认无老板近期消息）。
    关键：失败返回 None 而非 False——绝不把「查不到」误判成「不活跃」去代发；
    同时 None 也不触发「不代发」，交给窗口内下一轮轮询重新确认（dws 抖动不应废掉功能）。"""
    try:
        msgs = _fetch_recent(conv_id, 10)
    except Exception as e:
        log_debug(f"owner_recently_active error: {e}")
        return None
    if msgs is None:
        return None  # 未确认：不置 active、不强制发
    now = time.time()
    for m in msgs:
        sender_open = extract_sender_open_id(m)
        sender = msg_field(m, "sender", "senderName", "senderNick")
        if not _is_self(sender, sender_open):
            continue
        ts = _msg_ts(m)
        if ts and (now - ts) <= within_sec:
            # 排除程序自己的代复：程序以老板身份发出，时间戳紧贴 LAST_SELF_SENT，
            # 若不加这一道，会把自身回复误判为「老板活跃」从而自锁死。
            sent = LAST_SELF_SENT.get(conv_id)
            if sent is not None and abs(ts - sent) <= 15:
                continue
            return True
    return False


def find_single_conversation(window_days=7):
    """【备用工具】不依赖未读，主动发现一个真实单聊会话 id（list-all 时间窗内首条 singleChat）。
    当前 main() 轮询未用（未读接口已天然过滤），保留给自测/调试场景按需调用；找到返回 cid，否则 None。"""
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=window_days)
    t_start = start.strftime("%Y-%m-%d 00:00:00")
    t_end = end.strftime("%Y-%m-%d %H:%M:%S")
    out = run_dws(["chat", "message", "list-all", "--start", t_start, "--end", t_end,
                   "--limit", "50", "--format", "json"], timeout=45)
    try:
        data = json.loads(out)
        clist = data.get("result", {}).get("conversationMessagesList", []) or []
        for c in clist:
            if c.get("singleChat") and c.get("openConversationId"):
                return c["openConversationId"]
    except Exception:
        pass
    return None


def _as_text(v):
    if v is None:
        return ""
    if isinstance(v, dict):
        return v.get("content") or v.get("text") or str(v)
    return str(v)


def _is_self(sender, sender_open_id=None):
    """判断最新消息是否来自老板本人（避免"回复自己"社死）。
    优先用 openid 精确匹配（运行时探测的 runtime.SELF_OPEN_ID）；拿不到 openid 时用昵称兜底。"""
    if sender_open_id and runtime.SELF_OPEN_ID and sender_open_id == runtime.SELF_OPEN_ID:
        return True
    s = (sender or "").lower()
    return any(k.lower() in s for k in SELF_SENDERS)


def group_msg_is_at_me(content):
    """群消息是否 @了老板（用于微信通知高亮「有人@你」+ 群聊 AI 草稿预览触发）。
    返回 True/False。媒体消息 content 为空 → False（无法从文本判 @）。
    ⚠️ 2026-08-05 修复：钉钉 @ 可出现在【任意位置】且可能带双 @@（复制/输入法格式）——
    原判定只认「以 @昵称 开头」导致句中 @（如「...如何处理@吉岩」）和「@@吉岩」前缀漏判，
    老板实测收不到 @提醒。改为任意位置子串匹配（宁可多提醒、不漏真 @）。"""
    if not content:
        return False
    c = content.strip()
    # @所有人 → 必然含老板
    if "@所有人" in c:
        return True
    # @all / <@all>（钉钉发送占位）→ 词边界匹配，避免 "allan"/"allstar" 等普通词误命中
    if "<@all>" in c or re.search(r"(?:^|[\s（(])@all(?:[\s）).!！?？：:；;，,]|$)", c, re.IGNORECASE):
        return True
    # 任意位置含 "@昵称"：兼容句首 / 句中 / 句末 / 多个 @ 连排 / "@@昵称" 双 @ 格式
    for name in MENTION_NAMES:
        if name and ("@" + name) in c:
            return True
    return False


def extract_media_ids(content):
    """从消息 content 提取所有图片 mediaId（钉钉内联格式，见上）。无图返回 []。
    ⚠️ 2026-08-07 修复：只提取【图片】mediaId——视频/语音/文件标签的 mediaId 先整段剔除，
    防止把视频当图片下载（download-media 会拿到视频文件，build_image_block 按 image/jpeg
    内联 → SDK 400 mime）。"""
    if not content:
        return []
    c = _NON_IMAGE_TAG_RE.sub("", content)  # 剥掉视频/语音/文件标签，只留图片/裸 mediaId
    return _MEDIA_RE.findall(c)


def clean_text_for_ai(content):
    """去掉 content 里的 [图片消息](mediaId=...) 等富媒体噪音（含 [视频]() 空括号占位），
    以及 dws 权限缺失时注入的下载提示语（「注意：如需下载使用dws chat message download-media命令下载…」），
    保留纯文字说明作为喂给 AI 的上下文（否则 AI 会看到 mediaId 垃圾或 dws 提示导致乱回）。"""
    if not content:
        return ""
    c = _PIC_TAG_RE.sub("", content)
    c = _MEDIA_EMPTY_RE.sub("", c)  # ⚠️ 2026-08-07 补：'[视频]()' 空括号占位（无 mediaId）
    c = _DWS_HINT_RE.sub("", c)
    c = _DWS_HINT_RE2.sub("", c)
    return c.strip()


def _safe_fname(s):
    return re.sub(r'[^A-Za-z0-9_\-]', '_', str(s))[:80]


def download_images(media_ids, msg_id, cid):
    """下载消息中的图片到本地缓存，返回 [(local_path, ok)]。
    路径坑：绝对路径若用 '/c/Users' 这种 Git-Bash 风格前缀，会被底层 Go 组件误解析导致落盘失败；
    必须传各平台原生分隔符路径（os.path.join 在 Windows 产反斜杠、POSIX 产正斜杠，均正确）。"""
    if not media_ids:
        return []
    try:
        os.makedirs(MEDIA_CACHE_DIR, exist_ok=True)
    except Exception:
        pass
    out = []
    for idx, mid in enumerate(media_ids[:4]):  # 单条消息最多认前 4 张，防刷屏
        fname = f"{_safe_fname(cid)}_{_safe_fname(msg_id)}_{idx}.jpg"
        local = os.path.join(MEDIA_CACHE_DIR, fname)  # 平台原生分隔符路径
        run_dws([
            "chat", "message", "download-media",
            "--type", "mediaId",
            "--resource-id", mid,
            "--message-id", msg_id,
            "--open-conversation-id", cid,
            "--output", local,
        ], timeout=60)
        ok = os.path.exists(local) and os.path.getsize(local) > 0
        out.append((local, ok))
        log_debug(f"[media] dl {mid[:18]}... -> {os.path.basename(local)} ok={ok}")
    return out


def send_reply(conv_id, msg_id, sender_open_id, text):
    if runtime.DRY_RUN:
        log_debug(f"[DRY_RUN reply] cid={conv_id} ref={msg_id} sender={sender_open_id} text={text[:80]}")
        return True
    # ⚠️ 防御：sender_open_id 空 → dws `chat message reply` 必报
    # `missing required flag(s): --ref-sender`，纯属浪费一次调用 + 误导上层。
    # 直接返回 False，让 monitor 如实通知「代复失败」而非谎称「已代复」。
    # （sender_open_id 应在 monitor 累积阶段经 _resolve_open_id 兜底拿到；
    #   若仍空，说明该会话 dws 完全取不到发送人 openId，需人工排查。）
    if not sender_open_id:
        log_debug(f"[send_reply] SKIP: sender_open_id 为空，无法 ref-reply (cid={conv_id})")
        return False
    args = [
        "chat", "message", "reply",
        "--conversation-id", conv_id,
        "--ref-msg-id", msg_id,
        "--ref-sender", sender_open_id,
        "--text", text, "--yes",
    ]
    for attempt in range(2):  # 失败退避2秒重试1次（网络抖动/限流时不丢消息）
        out = run_dws(args)
        ok = _dws_ok(out)
        if ok:
            # 记录程序自身的代复时间，供 owner_recently_active 排除「自己发的消息」，
            # 否则下轮会把程序以老板身份发出的回复误判为「老板活跃」→ 自锁死跳过真实消息。
            LAST_SELF_SENT[conv_id] = time.time()
            return True
        log_debug(f"send_reply attempt {attempt+1}/2 FAIL: {out[:200]}")
        if attempt == 0:
            time.sleep(2)
    return False


def get_self_openid():
    """获取老板本人的 openDingTalkId（用于「测试消息发给自己」）。
    优先级：环境变量 SELF_OPENDINGTALK_ID > 通讯录按 BOSS_DISPLAY_NAME 搜索。
    搜索兜底依赖 dws contact 授权；拿不到返回空字符串。"""
    env = os.environ.get("SELF_OPENDINGTALK_ID")
    if env and env.strip():
        return env.strip()
    # 隐私：源码不硬编码真实姓名，请在私密 .env 里配 BOSS_DISPLAY_NAME=你的钉钉显示名
    # （或直接配 SELF_OPENDINGTALK_ID 更精确）。都不配则跳过通讯录搜索、仅靠运行时探测。
    name = os.environ.get("BOSS_DISPLAY_NAME", "").strip()
    if not name:
        return ""
    try:
        out = run_dws(["contact", "user", "search", "--query", name, "--format", "json"], timeout=30)
        data = json.loads(out)
        res = data.get("result") or []
        if res and res[0].get("openDingTalkId"):
            return res[0]["openDingTalkId"]
    except Exception:
        pass
    return ""


def send_reply_self(text):
    """把一条回复直接发到老板自己的钉钉（自测用，绝不会发给别人）。
    用 `dws chat message send --open-dingtalk-id <自己>` 落地到「文件传输/自己」会话。"""
    self_id = get_self_openid()
    if not self_id:
        log_debug("send_reply_self: 未检测到自己的 openDingTalkId，跳过")
        return False
    if runtime.DRY_RUN:
        log_debug(f"[DRY_RUN send-self] to={self_id} text={text[:80]}")
        return True
    out = run_dws(["chat", "message", "send", "--open-dingtalk-id", self_id, "--text", text], timeout=30)
    ok = _dws_ok(out)
    if not ok:
        log_debug(f"send_reply_self FAIL: {out[:200]}")
    return ok
