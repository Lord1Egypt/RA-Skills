#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉未读消息监控 → AI 自动回复（单聊，支持图片识别）+ 微信提醒（含图片内容识别，未配视觉API时降级）

完整、可直接移植的技能脚本（与 SKILL.md 配套）。
所有外部二进制路径均走「环境变量覆盖 → 自动探测（~/.workbuddy 下）」，
不再硬编码任何具体用户名，可在任意装了 WorkBuddy 的机器上运行。

流程：
  1. 轮询 `dws chat message list-unread-conversations`（天然只返回有未读的会话）
  2. 单聊未读 → 用 openConversationId 拉最新一条消息，
     用 CodeBuddy Agent SDK（codebuddy-agent-sdk）生成回复：以 system_prompt 注入老板人设，
     编程式调用、独立会话、上下文干净，比命令行 subprocess 更快更稳（无管道挂死、无编码坑）。
  3. `dws chat message reply` 带引用回复（单聊）
  4. 微信推送：单聊 → 「收到谁:内容 + 已代复:回复」合并一条；
     群聊 → 按 GROUP_PUSH 策略（默认 atme：仅 @我/@all 才推，其余群消息静默跳过）
     （依赖 weixinclaw-proactive-push skill；未安装时自动降级为仅日志，不报错）

设计要点：
  - 仅单聊自动回复；群聊只通知不代发（防社死）
  - 群聊微信推送默认只在 @我/@all 时触发（GROUP_PUSH=atme），避免群刷屏打扰
  - 若会话最新一条来自老板本人（SELF_SENDERS），不代复，避免"回复自己"
  - SKIP_SENDERS：可配置不自动回复的名单（如家人/上级），默认空
  - DRY_RUN=1 时只生成+打印，不真发回复、不推微信，用于验证
  - 启动瞬间先把当前未读时间戳记进去重表（静默 seed），只对启动后新到的消息回复，
    不会 retro 回复历史未读
  - 去重按 (会话ID -> 最新消息 openMessageId/lastMsgCreateAt)，同一条不会重复回
  - 生成失败/媒体无文本 → 不代发，仅推微信「需手动处理」转人工（绝不发兜底话术误导对方以为老板看到了）

=== 模块拆分（2026-07-17）===
原单文件（1642 行）已按职责拆分为 4 个模块 + 本入口，便于维护：
  - runtime.py       基础/配置层：.env 加载、SDK 可用探测、路径探测、全部共享常量、日志/锁/缓存/审计/鉴权
  - dingtalk_api.py  钉钉交互层：dws 调用、未读/消息拉取、单聊·群@判定、图片下载、发送
  - vision.py        多模态层：图片识别（deepseek-v4-flash 内置 / 外部 OpenAI 兼容 API）
  - reply.py         回复生成层：persona / 查表 grounding / SDK 生成 / 微信推送
  - dingtalk_unread_monitor.py（本文件）入口：仅保留 docstring + main() + 统一 re-export
本文件把上面各模块的名字 re-export 到自身命名空间，因此 `import dingtalk_unread_monitor as M`
的旧调用方（_validate.py / recover_missed.py）无需改动。
"""
import os, sys, time, json, re, datetime
import runtime  # 用于运行时修改 runtime.SELF_OPEN_ID 等可变配置
# 注：以下 import 里含「兼容 re-export」——_validate.py / recover_missed.py 经
# `import dingtalk_unread_monitor as M` 访问这些名字（M.DWS_CMD / M.gen_reply 等）。
# 删名字前请先确认这两个外部脚本没有用 M.<name>。
from runtime import (
    VISION_ENABLED, TEST_MODE, ONCE,
    AUTO_REPLY_IMAGE, REPLY_DELAY_SEC, ACTIVE_WINDOW_SEC, DRY_RUN,
    POLL_INTERVAL, check_codebuddy_auth, print_auth_banner, log_debug, _acquire_lock,
    _release_lock, _SKILL_DIR, NOTIFIED, PENDING, LAST_SELF_SENT, AUDIT_LOG, AUDIT_LOG_MAX,
    GROUP_PUSH, SKIP_SENDERS, FALLBACK_REPLY, _RECENT_CACHE,
    GROUP_REPLY_PREVIEW,
    log_audit, _clean_media_cache, DWS_CMD, CODEBUDDY_CMD, NODE, SEND_JS, GNOTIFY,
    DWS_ENTRY, DWS_EXE, CHINA_EDITION, CODEBUDDY_API_KEY,
)
from dingtalk_api import (
    run_dws, msg_field, extract_sender_open_id, msg_sender_open_id, _msg_ts, _norm_ts,
    get_unread, get_latest_msg, _fetch_recent,
    find_single_conversation, owner_recently_active, _as_text, _is_self, group_msg_is_at_me,
    extract_media_ids, clean_text_for_ai, download_images, send_reply, get_self_openid,
    send_reply_self,
)
from vision import describe_images
from reply import (
    gen_reply, push_weixin, _seed_notify, SESSION_RESUMED,
)


def _resolve_open_id(msgs):
    """从累积/最近消息里取【发送人】的 openDingTalkId 兜底。

    背景（图片消息 openId 缺失 bug）：图片消息在 dws `chat message list`
    返回结构里偶发不含 `senderOpenDingTalkId` 扁平字段 → 只取最新一条会拿到空 →
    send_reply 调 dws 报 `missing required flag(s): --ref-sender` → 代复失败（钉钉没发出）。
    改为扫描窗口内所有消息，取第一条「非空 且 非老板本人」的 openId：
    同一单聊里同事的 openId 稳定，兜底可靠；不取老板本人（避免「回复自己」）。"""
    # ⚠️ 必须用 runtime.SELF_OPEN_ID（模块属性）而非顶部 SELF_OPEN_ID 副本：
    # 后者在 import 时为空串（runtime.py:365 默认 ""），main() 启动期第 147 行才填充
    # runtime.SELF_OPEN_ID = get_self_openid()——改的是模块属性，不会反向同步到 import 副本。
    # 若用副本，本函数永远拿到空串 → 第一个非空 openId 会被返回（无论是不是老板本人）→
    # 极端情况下兜底误取老板本人 openId → "回复自己"风险。
    _self = runtime.SELF_OPEN_ID or ""
    for m in msgs:  # msgs 已 newest-first
        soid = msg_sender_open_id(m)
        if soid and soid != _self:
            return soid
    # 极端兜底：上面没命中（全是老板本人消息）→ 任取一个非空
    for m in msgs:
        soid = msg_sender_open_id(m)
        if soid:
            return soid
    return ""


def _download_imgs(media_ids, msg_id, cid, need_image):
    """need_image 且（有图 + 视觉可用 + 非 DRY_RUN）时下载图片到缓存，
    返回 [(local_path, ok)]；否则返回 []。单聊/群聊共用（消除两处重复的下载条件判断）。"""
    if not (need_image and media_ids and VISION_ENABLED and not runtime.DRY_RUN):
        return []
    return [p for p, ok in download_images(media_ids, msg_id, cid) if ok]


def _desc_paths(img_paths):
    """识别已下载图片，返回中文描述（无图 / DRY_RUN 时返回空串）。"""
    if not img_paths or runtime.DRY_RUN:
        return ""
    return describe_images([(p, True) for p in img_paths])


# ---------- 延迟代发状态机（纯函数，可单测；单测见 _validate.py --test-statemachine） ----------
# 把 PENDING（单聊延迟代发）/ GNOTIFY（群通知延迟）的「窗口/取消/defer/重试」嵌套逻辑抽成纯函数：
# 只计算下一步动作(action) + 更新 job 内部状态(deadline/defers/push_retry/push_fail)，不调用任何副作用
# （gen_reply/send_reply/push_weixin 仍在 main 循环里按 action 分发）。dict(job) 复制确保可单测、
# 且绝不修改调用方传入的原 job。owner_active 由 main 传入（owner_recently_active 的 True/False/None），
# 便于单测时直接注入，不依赖 dws/SDK。
PENDING_DEFER_SEC = 20        # dws 未确认时单次推迟窗口
PENDING_RETRY_SEC = 45        # 发送/通知失败后重试窗口
PENDING_MAX_DEFERS = 3        # defer 上限（>3 判定 dws 持续异常 → 不再无限推迟）
PENDING_MAX_PUSH_FAIL = 5     # 推送/发送失败上限（>=5 放弃，避免日志刷屏/耗 dws 配额）


def _pending_next_state(job, now, owner_active):
    """单聊延迟代发 PENDING job 的下一步动作（纯函数）。返回 (action, new_job)。
    action:
      'wait'     未到期且老板不活跃 → 继续等
      'cancel'   老板活跃 → 取消代发（他在跟，会自己回）
      'defer'    dws 未确认(owner_active is None) → 推迟 PENDING_DEFER_SEC 重确认（defers<=上限）
      'giveup'   dws 持续未确认（defers 超限）→ 转人工放弃
      'send_now' 窗口结束老板无动作 → 真正代发
    """
    job = dict(job)
    if now < job.get("deadline", 0):
        if owner_active is True:
            return "cancel", job
        return "wait", job
    if owner_active is True:
        return "cancel", job
    if owner_active is None:
        job["defers"] = job.get("defers", 0) + 1
        if job["defers"] <= PENDING_MAX_DEFERS:
            job["deadline"] = now + PENDING_DEFER_SEC
            return "defer", job
        return "giveup", job
    return "send_now", job


def _pending_after_send(job, send_ok, notify_ok, now):
    """代发(SDK+send_reply)后按发送/通知结果决定重试或放弃（纯函数）。返回 (action, new_job)。
    action:
      'done'   已通知（send 成功，或 send 失败但 notify 成功提醒老板手动回）→ 结束 job
      'retry'  双重失败 → 保留 PENDING_RETRY_SEC 后重试（push_fail<上限）
      'giveup' 双重失败已达上限 → 放弃
    """
    job = dict(job)
    if send_ok or notify_ok:
        return "done", job
    job["push_fail"] = job.get("push_fail", 0) + 1
    if job["push_fail"] >= PENDING_MAX_PUSH_FAIL:
        return "giveup", job
    job["push_retry"] = True
    job["deadline"] = now + PENDING_RETRY_SEC
    return "retry", job


def _gnotify_next_state(job, now, owner_active):
    """群通知延迟 GNOTIFY job 的下一步动作（纯函数）。返回 (action, new_job)。
    action:
      'wait'     未到期（非重试中）且老板不活跃 → 继续等
      'cancel'   老板活跃 → 取消通知
      'defer'    dws 未确认 → 推迟 PENDING_DEFER_SEC 重确认（defers<=上限）
      'giveup'   dws 持续未确认 → 不再 defer，直接推（群消息不漏）
      'push_now' 窗口结束老板无动作 → 推送微信
    注：retrying(push_retry) 期间不取消、不 defer，避免「老板在线却永久收不到」。
    """
    job = dict(job)
    if now < job.get("deadline", 0):
        if not job.get("push_retry") and owner_active is True:
            return "cancel", job
        return "wait", job
    _act = owner_active if not job.get("push_retry") else False
    if _act is True:
        return "cancel", job
    if _act is None:
        job["defers"] = job.get("defers", 0) + 1
        if job["defers"] <= PENDING_MAX_DEFERS:
            job["deadline"] = now + PENDING_DEFER_SEC
            return "defer", job
        return "giveup", job
    return "push_now", job


def _gnotify_after_push(job, push_ok, now):
    """群通知推送后按微信结果决定重试或放弃（纯函数）。返回 (action, new_job)。
    action:
      'done'   推送成功 → 结束 job
      'retry'  推送失败 → 保留 PENDING_RETRY_SEC 后重试（push_fail<上限）
      'giveup' 推送失败已达上限 → 放弃
    """
    job = dict(job)
    if push_ok:
        return "done", job
    job["push_fail"] = job.get("push_fail", 0) + 1
    if job["push_fail"] >= PENDING_MAX_PUSH_FAIL:
        return "giveup", job
    job["push_retry"] = True
    job["deadline"] = now + PENDING_RETRY_SEC
    return "retry", job


# ---------- 活跃判定（已读信号·单路·零内容拉取）----------
# 唯一权威依据 = list-unread-conversations 返回的未读会话集合：
#   老板一旦读过（打开/回复会话），该会话即离开未读列表。
#   → 会话「不在」未读列表 = 已读 = 活跃(取消代发)
#   → 会话「仍在」未读列表 = 未读 = 不活跃(到点代发)
# 全程不拉聊天内容，故不受 list_conversation_message_v2 权限被拒影响。
# 仅当本轮回拉可靠(ok/empty)才采信结果；dws glitch 空列表(16:24 实测)返回 None，避免误杀待发任务。
# 注：内存二次确认 owner_recently_active_from_msgs 已于 2026-07-28 作为死代码移除，
# 活跃判定仅走未读信号单路。
def _owner_active_now(cid, seen_unread, unread_reliable):
    """返回老板活跃状态：
      True  = 已读/活跃 → 取消代发
      False = 未读/不活跃 → 到点代发
      None  = 本轮回拉不可信(dws glitch) → 保守 defer，不盲发
    """
    if not unread_reliable:
        return None
    return cid not in seen_unread   # 不在未读列表 ⇒ 已读(True)


def main():
    # —— 启动期 CodeBuddy 认证健康检查（老板核心要求：未登录要明确提醒）——
    auth = check_codebuddy_auth()
    if not auth:
        print_auth_banner()
        log_debug("=== CodeBuddy 未认证，退出（请登录/填 Key 后重启）===")
        sys.exit(2)   # 非0退出，常驻启动器可感知并停止重试
    # 单实例锁：已有实例在跑则退出，避免双发/双处理（最糟=同条消息回两次）
    if not _acquire_lock():
        log_debug("=== 已有另一个监控实例在运行，本进程退出 ===")
        sys.exit(0)
    # 首次运行自检：确保 Startup 启动器存在。
    # .vbs 不随 skill 分发（见 .gitignore），需本机生成；有 gen_launcher.py 则
    # 自动落地到 %APPDATA%\...\Startup，换机/移植后首次运行即可自愈，无需手动复制。
    try:
        if _SKILL_DIR not in sys.path:
            sys.path.insert(0, _SKILL_DIR)
        from gen_launcher import ensure_launcher
        _lp, _created = ensure_launcher()
        if _created:
            log_debug(f"    [launcher] 自动生成 Startup 启动器: {_lp}")
    except Exception as _e:
        log_debug(f"    [launcher] 自动生成启动器失败（可手动跑 gen_launcher.py）: {_e}")
    import atexit
    atexit.register(_release_lock)
    # 优雅退出：SIGTERM/SIGINT 时释放单实例锁再退出
    import signal as _signal
    def _graceful_exit(signum, frame):
        log_debug(f"=== received signal {signum}, exiting ===")
        _release_lock()
        sys.exit(0)
    _signal.signal(_signal.SIGTERM, _graceful_exit)
    _signal.signal(_signal.SIGINT, _graceful_exit)
    log_debug(f"=== auto-reply monitor started (DRY_RUN={runtime.DRY_RUN}) ===")
    log_debug(f"    [auth] {auth[0]} :: {auth[1]}")
    log_debug(f"    [china] CHINA_EDITION={CHINA_EDITION}  API_KEY={'set' if CODEBUDDY_API_KEY else 'unset'}")
    log_debug(f"    DWS_CMD={DWS_CMD}")
    log_debug(f"    DWS_EXE={DWS_EXE}")
    log_debug(f"    CODEBUDDY_CMD={CODEBUDDY_CMD}")
    # 启动时比对「配置入口」与「实际会用的路由」，一眼看出 dws 是否可用/走哪条路
    _dws_route = ("DIRECT-exe" if (DWS_EXE and os.path.exists(DWS_EXE))
                   else ("NODE-direct" if (DWS_ENTRY and NODE and os.path.exists(NODE) and os.path.exists(DWS_ENTRY))
                   else ("DWS_CMD-fallback" if (DWS_CMD and os.path.exists(DWS_CMD)) else "NONE!! dws 不可用")))
    log_debug(f"    DWS_ROUTE={_dws_route}  DWS_EXE={DWS_EXE}")
    log_debug(f"    DWS_ENTRY={DWS_ENTRY}  NODE={NODE}  SEND_JS={SEND_JS}")
    # 启动时探测一次自己的 openid，后续 _is_self 用它精确匹配（昵称改了也不失效）
    runtime.SELF_OPEN_ID = get_self_openid()
    log_debug(f"    SELF_OPEN_ID={runtime.SELF_OPEN_ID or '(未探测到，回退昵称匹配)'}")
    seeded = False
    consecutive_errors = 0
    last_heartbeat = 0.0
    _last_unread_fp = None  # 未读集合指纹：仅在未读(会话+未读数)变化时打印 raw unread，消除无新消息刷屏
    _consecutive_dws_fail = 0  # 连续 dws 失败计数（health="fail"），用于触发微信异常提醒
    _last_dws_fail_notify = 0.0  # 上次推「dws 异常」微信的时间戳（节流，避免反复推）
    while True:
        try:
            # 持久外层错误（如 dws 服务挂掉）→ 退避，避免热循环狂刷日志
            if consecutive_errors:
                time.sleep(min(consecutive_errors * 10, 120))
            convs, unread_health = get_unread()
            consecutive_errors = 0
            # —— 已读信号集（抢答防护权威依据·零内容拉取）——
            # list-unread-conversations 本就每轮拉取；老板一旦读过（打开/回复）会话即离开未读列表，
            # 不在本集合即判"已读→活跃"。仅 dws 本轮真实返回（ok/empty）才采信，glitch 空列表不误杀待发。
            _unread_reliable = unread_health in ("ok", "empty")
            _seen_unread = {c.get("openConversationId") or c.get("conversationId") or c.get("id") or "" for c in convs}
            _seen_unread.discard("")
            # —— dws 健康追踪：连续失败 N 次（约 12 分钟）推一次微信提醒，节流 30 分钟 ——
            # 避免 dws 挂了但心跳伪装「unread_now=0 健康」，老板长期不知道消息全漏。
            if unread_health == "fail":
                _consecutive_dws_fail += 1
            else:
                _consecutive_dws_fail = 0
            if _consecutive_dws_fail >= 6 and time.time() - _last_dws_fail_notify >= 1800:
                _mins = _consecutive_dws_fail * POLL_INTERVAL // 60
                push_weixin(
                    f"⚠️ 钉钉监控异常：dws 接口连续 {_consecutive_dws_fail} 次拉取失败（约 {_mins} 分钟），"
                    f"心跳看着健康但实际读不到未读。请检查 dws 是否在 PATH / 授权是否过期 / "
                    f"钉钉客户端是否在跑 / 会话是否被占用。"
                )
                _last_dws_fail_notify = time.time()
            if convs:
                _fp = tuple(sorted(((c.get("openConversationId"), c.get("unreadPoint")) for c in convs),
                                   key=lambda x: str(x[0])))
                if _fp != _last_unread_fp:
                    log_debug("raw unread: " + json.dumps(convs, ensure_ascii=False)[:2000])
                    _last_unread_fp = _fp
            # 心跳：即使无未读也每 ~120s 打一行，证明进程活着。
            # 否则“dws 超时→空→无日志”会伪装成假死，难诊断（真凶曾在此）。
            # 【2026-07-22】加 health 标记：区分「真无消息」(empty) vs 「dws 坏了」(fail)，
            # 一眼看出 dws 是否健康，避免被「unread_now=0」伪装的健康骗到。
            now = time.time()
            if now - last_heartbeat >= 120:
                _health_tag = ""
                if unread_health == "empty":
                    _health_tag = " (empty: 真无未读)"
                elif unread_health == "fail":
                    _health_tag = f" (dws_unhealthy! fail×{_consecutive_dws_fail})"
                log_debug(f"[heartbeat] alive, unread_now={len(convs)}{_health_tag}, ts={datetime.datetime.now().strftime('%H:%M:%S')}")
                last_heartbeat = now
            # —— 抢答防护：处理到期的延迟代发任务 ——
            now = time.time()
            for cid, job in list(PENDING.items()):
                # 活跃判定（已读信号·单路·零内容拉取）：会话离开未读列表 = 老板已读 → 取消代发。
                # owner_active 语义：True=已读(取消) / False=未读(到点代发) / None=本轮回拉不可信(defer)。
                # 会话一旦被读过即离开未读列表，故「在/不在未读列表」即活跃与否的权威依据；
                # 仅 dws 本轮可靠(ok/empty)才采信，glitch 空列表不误杀待发任务。
                # （内存二次确认已于 2026-07-28 作为死代码移除，活跃判定仅走未读信号单路。）
                _act = _owner_active_now(cid, _seen_unread, _unread_reliable)
                action, job = _pending_next_state(job, now, _act)
                if action == "wait":
                    continue
                if action == "cancel":
                    del PENDING[cid]; NOTIFIED[cid] = job["ts"]
                    log_debug(f"[pending-cancel] owner read (unread-list): {cid}")
                    continue
                if action == "defer":
                    PENDING[cid] = job
                    log_debug(f"[pending-defer] dws unconfirmed #{job['defers']}: {cid}")
                    continue
                if action == "giveup":
                    log_debug(f"[pending-giveup] dws unconfirmed after {job['defers']} defers, skip: {cid}")
                    del PENDING[cid]; NOTIFIED[cid] = job["ts"]
                    push_weixin(f"🔔 钉钉（{job['sender']}）因 dws 持续异常无法确认您是否在线，已转人工，请自行回复")
                    continue
                # action == "send_now" → 窗口结束老板无动作 → 真正代发
                # 查表事实 grounding + 按会话记忆（同一对话多次消息续上下文）
                # ⚠️ detect_table_intent / fetch_table_context 移到 reply.py 内部，
                # 用 msgs[0]（最新一条）判意图；老版本用 job["content"]（已 join 多条历史）
                # 会被最旧那条误触发"问题反馈"意图，注入查表数据污染当前回复。
                sid = "dt_" + re.sub(r"[^A-Za-z0-9_]", "_", str(cid))[:48]
                resume = SESSION_RESUMED.get(sid, False)
                # return_rejected=True：即便质检拦下也回传草稿，保证单聊「生成过就推微信」。
                reply, rejected = gen_reply(job["sender"], job["content"], image_paths=job.get("image_paths"),
                                            return_rejected=True, session_id=sid, resume=resume,
                                            messages=job.get("msgs"))
                SESSION_RESUMED[sid] = True
                if reply:
                    if job.get("preview_only"):
                        # 🆕 群聊 AI 草稿预览（2026-08-05）：生成后【绝不发钉钉群】（红线：不在群聊替老板发言），
                        # 只推微信给老板预览验证；老板确认后如需代发另行处理。
                        _title_disp = f"群：{job.get('title','')}\n"
                        notify_ok = push_weixin(
                            f"🔔 钉钉群聊·AI 草稿（未发送）\n{_title_disp}@我的人：{job['sender']}\n"
                            f"内容：{str(job['content'])[:200]}\n\n"
                            f"🤖 草稿：{reply[:300]}\n\n（验证期只预览不发送，确认后告诉我，我再帮你发到群里）")
                        log_audit("group_preview", cid=cid, title=job.get("title",""), sender=job["sender"],
                                  content=str(job["content"])[:200], reply=reply[:200], sent_to_weixin=notify_ok, delayed=True)
                        log_debug(f"[group-preview] 草稿已推微信(未发钉钉) sender={job['sender']} -> {reply[:60]}")
                        # 复用 _pending_after_send 的微信推送重试/放弃语义（ok_send 传 True：未发钉钉是设计而非失败）
                        act2, job = _pending_after_send(job, True, notify_ok, now)
                    elif TEST_MODE:
                        # 测试模式：生成的回复只发给老板自己（钉钉自己会话 + 微信），绝不发给原发送人
                        send_reply_self(reply)
                        push_weixin(f"🧪【TEST·本应代复给 {job['sender']}】\n{reply}")
                        log_audit("auto_reply_test", cid=cid, sender=job["sender"],
                                  content=str(job["content"])[:200], reply=reply[:200], sent_to_self=True, delayed=True)
                        log_debug(f"[TEST single-delayed] 已发给自己(未发{job['sender']}) -> {reply[:60]}")
                        act2, job = "done", job
                    else:
                        # ⚠️ 发送前最后一波兜底：累积阶段仍未拿到 sender_open_id
                        # （图片消息在 dws list 偶发缺该字段）→ 实时拉最近消息扫描同事 openId，
                        # 否则 send_reply 必败（missing --ref-sender）。图片消息 openId 缺失修复。
                        if not job.get("sender_open_id"):
                            _rec = _fetch_recent(cid, 10)
                            if _rec:
                                job["sender_open_id"] = _resolve_open_id(_rec)
                                if job["sender_open_id"]:
                                    log_debug(f"[sender-open-id] recovered via _fetch_recent: {job['sender_open_id'][:12]}…")
                        ok_send = send_reply(cid, job["msg_id"], job["sender_open_id"], reply)
                        log_audit("auto_reply", cid=cid, sender=job["sender"],
                                  content=str(job["content"])[:200], reply=reply[:200], sent=ok_send, delayed=True)
                        log_debug(f"[single-delayed] reply ok={ok_send} sender={job['sender']} -> {reply[:60]}")
                        if ok_send:
                            # ✅ 仅在钉钉真实发出后才宣称「已代复」，杜绝「微信说已代复、钉钉却空空」的误导
                            # 代复已发 → 同事已收到 → 业务闭环。微信通知失败静默接受（同事已收到回复，
                            # 老板下次看微信时知道），不再重试（重试只会刷日志，无业务价值）。
                            notify_ok = push_weixin(f"🔔 钉钉新消息（单聊·已代复）\n来自：{job['sender']}\n内容：{str(job['content'])[:200]}\n\n🤖 已代复：{reply[:200]}")
                        else:
                            # 代复发送失败（dws 拒绝/ref-sender 缺失/接口异常）→ 如实告知，绝不谎称已代复
                            log_debug(f"[single-delayed] send FAILED (sender_open_id={job.get('sender_open_id')!r}) -> 通知老板手动回")
                            notify_ok = push_weixin(f"🔔 钉钉新消息（单聊·代复发送失败）\n来自：{job['sender']}\n内容：{str(job['content'])[:200]}\n\n⚠️ 代复发送被钉钉拒绝（ref-sender 缺失/接口异常），未真正发出。\n🤖 应发草稿：{reply[:200]}\n请老板手动回复，或我修复后补发。")
                        act2, job = _pending_after_send(job, ok_send, notify_ok, now)
                    if act2 == "done":
                        del PENDING[cid]; NOTIFIED[cid] = job["ts"]
                    elif act2 == "retry":
                        PENDING[cid] = job
                    elif act2 == "giveup":
                        log_debug(f"[single-delayed] send+notify FAILED {job['push_fail']} times, GIVE UP: {job['sender']}")
                        log_audit("single_giveup", cid=cid, sender=job["sender"], push_fail=job["push_fail"])
                        del PENDING[cid]; NOTIFIED[cid] = job["ts"]
                else:
                    # 单聊：只要生成过（含被质检拦下的草稿）就带到微信，方便老板判断/手动处理；
                    # 草稿 NOT 代发到钉钉（废话不发），但原文同步给老板。
                    reason = "AI 生成失败/质量不达标"
                    log_audit("skip_reply", cid=cid, sender=job["sender"], content=str(job["content"])[:200], reason=reason, delayed=True)
                    log_debug(f"[single-delayed-skip] sender={job['sender']} reason={reason} rejected_len={len(rejected) if rejected else 0} rejected_preview={(rejected[:800] if rejected else '')!r}")
                    draft_line = f"\n\n🤖 生成的内容（未代发到钉钉）：{rejected[:500]}" if rejected else ""
                    if job.get("preview_only"):
                        # 群聊预览生成失败 → 转人工（老板自己在群里回）
                        _title_disp = f"群：{job.get('title','')}\n"
                        push_weixin(f"🔔 钉钉群聊 @你（AI 草稿生成失败）\n{_title_disp}@我的人：{job['sender']}\n内容：{str(job['content'])[:200]}\n\n⚠️ {reason}，请老板在群里手动回复{draft_line}")
                    elif TEST_MODE:
                        push_weixin(f"🧪【TEST·需手动处理·原发送人 {job['sender']}】\n内容：{str(job['content'])[:200]}\n\n⚠️ {reason}，未代复{draft_line}")
                    else:
                        push_weixin(f"🔔 钉钉新消息（单聊·需手动处理）\n来自：{job['sender']}\n内容：{str(job['content'])[:200]}\n\n⚠️ {reason}，未代复，请老板手动回复{draft_line}")
                    del PENDING[cid]; NOTIFIED[cid] = job["ts"]

            # —— 抢答防护（群通知延迟）：处理到期的延迟群通知 ——
            now = time.time()
            for cid, job in list(GNOTIFY.items()):
                # 活跃判定（与单聊一致，已读信号单路·零内容拉取）。
                _act = _owner_active_now(cid, _seen_unread, _unread_reliable)
                action, job = _gnotify_next_state(job, now, _act)
                if action == "wait":
                    continue
                if action == "cancel":
                    del GNOTIFY[cid]; NOTIFIED[cid] = job["ts"]
                    log_debug(f"[gnotify-cancel] owner active: {cid}")
                    continue
                if action == "defer":
                    GNOTIFY[cid] = job
                    log_debug(f"[gnotify-defer] dws unconfirmed #{job['defers']} (group): {cid}")
                    continue
                if action == "giveup":
                    # dws 持续未确认 → 不再 defer，直接推（群消息不漏）
                    log_debug(f"[gnotify-giveup] dws unconfirmed after {job['defers']} defers, push anyway (group): {cid}")
                # action in ("giveup"(push anyway), "push_now") → 推送微信（多条@已合并到 msgs）
                msgs = job.get("msgs", [])
                title_disp = f"群：{job['title']}\n"
                pic_line = f"📷 图片内容：{job['img_desc']}\n" if job.get("img_desc") else ""
                if len(msgs) > 1:
                    lines = [f"· {x['sender']}：{x['content'][:200]}" for x in msgs]
                    content_disp = "\n".join(lines)
                    header = "群聊·有人@你（合并 %d 条@）" % len(msgs)
                else:
                    content_disp = (job.get("body") or "")[:200]
                    header = "群聊·有人@你" if job.get("at_me") else "群聊"
                ok = push_weixin(f"🔔 钉钉新消息（{header}）\n{title_disp}{pic_line}内容：{content_disp}\n")
                act2, job = _gnotify_after_push(job, ok, now)
                if act2 == "done":
                    log_audit("notify_only", cid=cid, title=job["title"], is_single=False,
                              at_me=job.get("at_me"), content=content_disp[:200],
                              delayed=True, merged=len(msgs) > 1)
                    log_debug(f"[group-delayed] pushed notify merged={len(msgs)} title={job['title']}")
                    del GNOTIFY[cid]; NOTIFIED[cid] = job["ts"]
                elif act2 == "retry":
                    GNOTIFY[cid] = job
                elif act2 == "giveup":
                    log_debug(f"[group-delayed] weixin push FAILED {job['push_fail']} times, GIVE UP: {job['title']}")
                    log_audit("weixin_push_giveup", cid=cid, title=job["title"],
                              push_fail=job["push_fail"], merged=len(msgs) > 1)
                    del GNOTIFY[cid]; NOTIFIED[cid] = job["ts"]

            seen = set()
            for conv in convs:
                cid = conv.get("openConversationId") or conv.get("conversationId") or conv.get("id") or ""
                if not cid:
                    continue
                seen.add(cid)
                title = conv.get("title") or "(未知会话)"
                unread = conv.get("unreadPoint") or 0
                is_single = conv.get("singleChat", False)
                # 去重键用未读对象里始终存在的 lastMsgCreateAt（msg_id 可能为空的媒体消息，不能作为去重依据）
                # ⚠️ 2026-08-05 修复：必须 _norm_ts 归一化为秒——lastMsgCreateAt 是毫秒（13 位），
                # 不归一化会与 _msg_ts 解析的秒级 ts 混排差 1000 倍（图片消息误判最新、连发文字掉进背景历史、去重失效）。
                last_ts = _norm_ts(conv.get("lastMsgCreateAt") or 0)

                # 启动静默 seed：记录当前未读时间戳，避免启动时回 backlog（不代复）。
                # 但对「近期(24h 内)到达」的单聊未读，发一次被动通知让老板知情——
                # 否则 downtime 期间到达的消息会在重启时被静默吞掉，造成「毫无反应」（此前 bug）。
                # 放在 get_latest_msg 之前：对注定 seed 跳过的会话不白调 dws。
                if not seeded:
                    NOTIFIED[cid] = last_ts
                    try:
                        _seed_notify(cid, title, is_single)
                    except Exception:
                        pass
                    continue

                # 去重：该会话最新消息时间戳已处理过 → 跳过（防重复轰炸）
                if NOTIFIED.get(cid) == last_ts:
                    continue

                msg = get_latest_msg(cid)
                msg_id = msg_field(msg, "openMessageId", "messageId", "msgId")
                sender = msg_field(msg, "sender", "senderName", "senderNick")
                content = _as_text(msg_field(msg, "content", "text", "body", default=""))
                sender_open_id = extract_sender_open_id(msg)

                # —— 富媒体：提取图片 mediaId、清洗文本（去掉 mediaId 噪音，避免 AI 看到垃圾）——
                media_ids = extract_media_ids(content)
                clean = clean_text_for_ai(content)
                has_text = bool(clean)
                body = (clean[:600] if clean else "(图片/媒体消息)").strip() or "(图片/媒体消息)"

                # 群聊 @我/@all 判定（提前算：群聊 AI 草稿预览分支需要；单聊恒 False）
                at_me = (not is_single) and group_msg_is_at_me(content or body)

                # 老板本人发的最后一条 → 不代复（他在自己聊，或已回复），跳过免得"回复自己"
                if is_single and _is_self(sender, sender_open_id):
                    NOTIFIED[cid] = last_ts
                    log_debug(f"[self] latest msg from self ({sender}), skip auto-reply")
                    continue

                # 🆕 2026-08-05 群聊 AI 草稿预览：@我 且有文本 → 复用单聊 PENDING 机制
                # （2min 延迟 + 背景历史 + AI 生成），生成后只推微信预览、绝不发钉钉群。
                _grp_preview = (not is_single) and GROUP_REPLY_PREVIEW and at_me and has_text
                if (is_single or _grp_preview) and not any(k in (sender or "") for k in SKIP_SENDERS) and msg_id:
                    if cid in PENDING:
                        # 已在延迟窗口等待：把窗口内新到的消息累积进 job，
                        # 等待期结束时统一作为「一条连贯回复」回应（而非逐条零散代复）。
                        # ⚠️ 关键约束：msgs 顺序必须 = 时间【倒序】（newest 在前），
                        # 否则 gen_reply 会把最旧那条当主回复对象，复述历史话题。
                        # _fetch_recent 本身是 newest-first，append 进去就保持倒序；
                        # 这里再 sorted 一次兜底（防御未来 _fetch_recent 顺序被改）。
                        try:
                            _recent = _fetch_recent(cid, 10) or []
                            _have = {m.get("msg_id") for m in PENDING[cid].get("msgs", [])}
                            for _m in _recent:
                                _mid = msg_field(_m, "openMessageId", "messageId", "msgId")
                                _s = msg_field(_m, "sender", "senderName", "senderNick")
                                _soid = extract_sender_open_id(_m)
                                # ⚠️ 2026-07-21 老板要求：拉历史对话记录包括老板自己的
                                # （让 AI 模仿老板口吻 + 理解上下文连续性）。
                                # 不再 _is_self → continue 过滤；改为加 is_self 字段标记，
                                # gen_reply 里区分对待（老板消息 = 背景历史，不是主回复对象）。
                                if _mid in _have:
                                    continue
                                _ct = _as_text(msg_field(_m, "content", "text", "body", default=""))
                                _cl = clean_text_for_ai(_ct)
                                if not _cl:
                                    continue
                                PENDING[cid]["msgs"].append({
                                    "sender": _s, "content": _cl,
                                    "msg_id": _mid, "ts": _msg_ts(_m),
                                    "is_self": _is_self(_s, _soid),   # 标记老板本人消息（供 gen_reply 区分对待）
                                    "sender_open_id": extract_sender_open_id(_m),
                                })
                                _have.add(_mid)
                            _ms = PENDING[cid].get("msgs", [])
                            if _ms:
                                # ⚠️ 顺序兜底：按 ts 倒序重排，newest 必须在第一位。
                                # 防御：dws 偶发 ts 异常/同 ts 时序抖动时顺序仍对。
                                _ms.sort(key=lambda x: x.get("ts") or 0, reverse=True)
                                PENDING[cid]["msgs"] = _ms
                                # ✅ content/sender/msg_id 取【对方最新一条】（过滤 is_self=True 后取最新）。
                                # 主回复对象必须是对方，不能是老板自己（否则"回复自己"+引用错对象）。
                                _peer_msgs = [m for m in _ms if not m.get("is_self")]
                                _main = _peer_msgs[0] if _peer_msgs else _ms[0]
                                PENDING[cid]["content"] = _main["content"]
                                PENDING[cid]["sender"] = _main["sender"]
                                PENDING[cid]["msg_id"] = _main["msg_id"]
                                # sender_open_id 扫描兜底（不再只取最新一条）：
                                # 图片消息在 dws list 偶发缺 senderOpenDingTalkId 扁平字段，
                                # 只取最新一条会拿到空 → dws reply 报 missing --ref-sender → 代复失败。
                                # 改扫描窗口内所有累积消息，取第一条非空且非老板本人的 openId
                                # （同一会话同事的 openId 稳定，兜底可靠）。图片消息 openId 缺失修复。
                                PENDING[cid]["sender_open_id"] = _resolve_open_id(_ms)
                                # ⚠️ 同步更新 job["ts"] = 最新累积消息 ts（_ms[0] 已按 ts 倒序，[0] 是 newest）：
                                # 双重失败放弃时设的 NOTIFIED[cid] = job["ts"] 必须是最新 ts，
                                # 否则下轮 get_unread 返回的 last_ts（最新累积消息的）不等于 NOTIFIED 里设的旧 ts
                                # → 去重不命中 → 重复加载已处理未读 → 无限循环刷日志。
                                PENDING[cid]["ts"] = _ms[0].get("ts") or PENDING[cid].get("ts", 0)
                                _n_self = len(_ms) - len(_peer_msgs)
                                log_debug(f"[pending] cid={cid} accumulated msgs={len(_ms)} (peer={len(_peer_msgs)} self_history={_n_self}, newest-first, latest_ts={_ms[0].get('ts')})")
                        except Exception as _e:
                            log_debug(f"[pending] accumulate error: {_e}")
                        continue
                    # 单聊图片：下载（每条新消息只做一次）；是否识别取决于场景
                    img_paths = _download_imgs(media_ids, msg_id, cid, True)
                    # img_paths 非空 ⇒ 已有图且视觉可用，无需再重复判 media_ids/VISION_ENABLED
                    want_auto_image = bool(AUTO_REPLY_IMAGE and img_paths)
                    # 纯空（无文字、无图）或图片代复关闭 → 转人工
                    if not has_text and not want_auto_image:
                        # 不代复场景：仍让老板知道图里是什么 → 识别一次（仅通知，省去代复的二次调用）
                        img_desc = _desc_paths(img_paths)
                        pic_line = f"\n📷 图片内容：{img_desc}\n" if img_desc else ""
                        reason = ("图片消息（已识别内容，但单聊图片自动代复已关闭）"
                                  if (media_ids and VISION_ENABLED)
                                  else "媒体消息无文本，AI 无法生成回复")
                        log_audit("skip_reply", cid=cid, sender=sender, content=body[:200], reason=reason, has_image=bool(img_paths))
                        log_debug(f"[single-skip] sender={sender} reason={reason}")
                        push_weixin(
                            f"🔔 钉钉新消息（单聊·需手动处理）\n来自：{sender}\n{pic_line}内容：{body[:200]}\n\n"
                            f"⚠️ {reason}，未代复，请老板手动回复"
                        )
                        NOTIFIED[cid] = last_ts
                    else:
                        # 进延迟窗口；代复上下文 = 纯文字 + （代复图片则直接传图路径，gen_reply 内联，省一次 describe）
                        # msgs：窗口内累积的对方消息列表，等待期结束时统一连贯回复（不再逐条零散代复）。
                        PENDING[cid] = {
                            "deadline": time.time() + REPLY_DELAY_SEC,
                            "ts": last_ts, "sender": sender, "msg_id": msg_id,
                            "sender_open_id": sender_open_id,
                            "content": (clean if clean else "(图片消息)"),
                            "image_paths": img_paths if want_auto_image else [],
                            "msgs": [{"sender": sender, "content": (clean if clean else "(图片消息)"),
                                      "msg_id": msg_id, "ts": last_ts}],
                            "defers": 0,
                            # 🆕 群聊 AI 草稿预览标记（2026-08-05）：True=群聊@我 预览（只推微信不发钉钉）；
                            # 单聊代发为 False/缺省。分发处据此决定 send_reply vs push_weixin。
                            "preview_only": bool(_grp_preview),
                            "title": title if _grp_preview else "",
                            "at_me": bool(at_me) if _grp_preview else False,
                        }
                        _tag = "group-preview" if _grp_preview else "single"
                        log_debug(f"[pending] cid={cid} sender={sender} delay={REPLY_DELAY_SEC}s auto_img={want_auto_image} mode={_tag}")
                else:
                    # 群聊 / skip 名单 / 缺 msg_id：仅通知，不代发
                    at_me = (not is_single) and group_msg_is_at_me(content or body)
                    # 群聊图片：仅在 @我 时下载+识别（避免群刷图烧视觉额度），仅通知用
                    img_paths = _download_imgs(media_ids, msg_id, cid, at_me)
                    img_desc = _desc_paths(img_paths)

                    if is_single:
                        # 单聊（skip 名单 / 缺 msg_id）：照常通知老板
                        who_disp = f"来自：{sender}\n"
                        unread_disp = f"(共 {unread} 条未读)\n" if unread and unread > 1 else ""
                        chat_label = "单聊"
                        pic_line = f"📷 图片内容：{img_desc}\n" if img_desc else ""
                        push_weixin(f"🔔 钉钉新消息（{chat_label}）\n{who_disp}{pic_line}内容：{body[:200]}\n{unread_disp}")
                        log_audit("notify_only", cid=cid, sender=sender, title=title,
                                  is_single=is_single, at_me=at_me, content=body[:200], has_image=bool(media_ids))
                        log_debug(f"[single-skip] notify only sender={sender} at_me={at_me} img={bool(media_ids)}")
                        NOTIFIED[cid] = last_ts
                    else:
                        # 群聊：按 GROUP_PUSH 策略决定是否通知；可通知的消息进延迟窗口
                        # （类单聊 PENDING）—— 等待期内老板若在群里活跃则取消、多条@合并一条，
                        # 避免即时打扰/刷屏。
                        if GROUP_PUSH == "off":
                            log_debug(f"[group] push disabled (GROUP_PUSH=off): title={title} sender={sender}")
                            NOTIFIED[cid] = last_ts
                        elif GROUP_PUSH == "all" or at_me:
                            if cid in GNOTIFY:
                                # 窗口内再 @我 → 累积（去重 by msg_id），保留首条 img_desc，不重复烧视觉额度
                                _have = {m.get("msg_id") for m in GNOTIFY[cid].get("msgs", [])}
                                if msg_id and msg_id not in _have:
                                    GNOTIFY[cid]["msgs"].append({
                                        "sender": sender,
                                        "content": (body if body else "(图片/媒体消息)"),
                                        "msg_id": msg_id, "ts": last_ts,
                                    })
                                    GNOTIFY[cid]["at_me"] = GNOTIFY[cid].get("at_me") or at_me
                                    # ⚠️ 同步更新 job["ts"] = 最新累积消息 ts：
                                    # 放弃时设的 NOTIFIED[cid] = job["ts"] 必须是最新 ts，
                                    # 否则下轮 get_unread 返回的 last_ts（最新累积消息的）不等于 NOTIFIED 里设的旧 ts
                                    # → 去重不命中 → 重复加载已处理未读 → 又触发 5 次失败 → 无限循环刷日志。
                                    GNOTIFY[cid]["ts"] = last_ts
                                    log_debug(f"[gnotify] cid={cid} accumulated msgs={len(GNOTIFY[cid]['msgs'])} (waiting)")
                                continue
                            # 首条 @我/群消息：建延迟窗口（复用 REPLY_DELAY_SEC，与单聊一致）
                            GNOTIFY[cid] = {
                                "deadline": time.time() + REPLY_DELAY_SEC,
                                "ts": last_ts, "title": title, "sender": sender,
                                "body": (body if body else "(图片/媒体消息)"),
                                "img_desc": img_desc, "at_me": at_me,
                                "msgs": [{"sender": sender,
                                           "content": (body if body else "(图片/媒体消息)"),
                                           "msg_id": msg_id, "ts": last_ts}],
                                "defers": 0,
                            }
                            log_debug(f"[gnotify] cid={cid} title={title} sender={sender} delay={REPLY_DELAY_SEC}s at_me={at_me}")
                            # 注意：此处【不】立即设 NOTIFIED，留待窗口到期推送后再标记，
                            # 以便窗口内后续 @我能累积进同一通知（与单聊 PENDING 行为一致）。
                            continue
                        else:
                            # 群聊非 @我/@all → 静默跳过，不推微信（GROUP_PUSH=atme 默认）
                            log_debug(f"[group] skipped (not @me, GROUP_PUSH=atme): title={title} sender={sender}")
                            NOTIFIED[cid] = last_ts
            seeded = True
            # 会话已读（不在未读列表）→ 清除标记
            for cid in list(NOTIFIED.keys()):
                if cid and cid not in seen:
                    del NOTIFIED[cid]
            # 每 200 轮清理一次图片缓存（防常驻下缓存无限增长）
            main._poll = getattr(main, "_poll", 0) + 1
            if main._poll % 200 == 0:
                _clean_media_cache(7)
                # 清理 _RECENT_CACHE 过期项（防长跑下 dict 无限增长）
                now_t = time.time()
                for k in list(_RECENT_CACHE.keys()):
                    if _RECENT_CACHE[k][0] <= now_t:
                        del _RECENT_CACHE[k]
                # ⚠️ 2026-08-13 清理 LAST_SELF_SENT 过期项：仅 owner_recently_active 的
                # 15s 自锁判定会用到，超过 24h 的条目已无意义，清理防长跑下缓慢增长。
                for k in list(LAST_SELF_SENT.keys()):
                    if now_t - LAST_SELF_SENT[k] > 86400:
                        del LAST_SELF_SENT[k]
        except Exception as e:
            consecutive_errors += 1
            log_debug(f"loop error ({consecutive_errors}): {e}")
        if ONCE:
            log_debug("=== ONCE 模式：单次轮询完成，退出 ===")
            break
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    # SDK 自拉起：若本进程用的 python 没装 codebuddy-agent-sdk，但 .env 里
    # CODEBUDDY_SDK_PYTHON 指向另一个装了 SDK 的 python，则用 os.execv 重拉到它
    # （保留 os.environ，子进程重启时会再次读 .env）。这样无论监控被哪个 python 拉起，
    # 都能自愈到正确的 SDK 环境，无需外部保证启动解释器。
    _reexec = runtime.sdk_reexec_target()
    if _reexec:
        try:
            import sys as _sys
            os.execv(_reexec, [_reexec, os.path.abspath(__file__)] + _sys.argv[1:])
        except Exception as _e:
            # 重拉失败不致命：继续用当前解释器跑（SDK 不可用会走不代发降级逻辑）
            print(f"[warn] 重拉到 SDK python 失败：{_reexec}（{_e}）；继续用当前解释器")
    main()
