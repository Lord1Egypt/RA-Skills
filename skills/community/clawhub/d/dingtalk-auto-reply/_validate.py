#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉自动回复技能 - 自测脚本（集成验证，不真发回复）。

两种模式：
  [默认] 集成验证：以「真实单聊未读」跑通 get_unread → get_latest_msg → gen_reply → reply --dry-run
  [--inject] 注入测试：手动指定一条假消息，验证 gen_reply 生成 + 把回复「发给自己」
            （绝不发给别人）。不依赖真实单聊未读。

【重要】测试消息只发给自己：inject 模式默认把生成结果通过
  dws chat message send --open-dingtalk-id <老板自己的openDingTalkId>
落地到老板自己的会话（文件传输/自己），不会触碰任何其他人的会话。
老板自己的 openDingTalkId 自动从通讯录探测，也可用环境变量 SELF_OPENDINGTALK_ID 指定。

用法：
  # 默认集成验证（DRY_RUN 仅影响 send_reply 是否真发；本脚本默认不真发）
  DRY_RUN=1 python ~/.workbuddy/skills/dingtalk-auto-reply/_validate.py

  # 注入测试（DRY_RUN：只生成+展示"会发给自己"，不真发）
  DRY_RUN=1 python _validate.py --inject --sender "测试同事-甲" --message "在高速，晚点回"

  # 注入测试（真发给自己：去掉 DRY_RUN，回复会真的出现在你自己的钉钉会话里）
  python _validate.py --inject --sender "测试同事-甲" --message "在高速，晚点回"

  # 高级：想测 reply(带引用) 的真实命令形态，指定一个真实会话 id（会发到该会话，慎用于真人）
  python _validate.py --inject --sender 同事甲 --message 你好 --cid "<openConversationId>"

说明：脚本随技能一起，路径用自身目录解析，可移植。
"""
import sys, os, json, time, argparse
import urllib.request, urllib.error

# 用脚本所在目录定位主模块（可移植核心，不硬编码用户名）
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
# 测试时开启 dws 实际调用追踪：run_dws 会把真实 argv/路由/返回码记进调试日志
os.environ["DEBUG_DWS_CALL"] = "1"
import dingtalk_unread_monitor as M

# DRY_RUN 来自主模块（环境变量驱动），自测脚本直接复用
DRY_RUN = getattr(M, "DRY_RUN", False)


def print_paths():
    print("=== resolved paths ===")
    print("  DWS_CMD     =", M.DWS_CMD)
    print("  CODEBUDDY_CMD=", M.CODEBUDDY_CMD)
    print("  NODE        =", M.NODE)
    print("  SEND_JS     =", M.SEND_JS)
    # 人设真源（方案 B）：codebuddy 注册 agent 优先，缺则 skill 内 dingtalk-helper-backup.md 兜底
    import reply as R
    print("  SOUL_AGENT       =", R.SOUL_AGENT)
    print("  AGENT_REGISTERED =", R._AGENT_REGISTERED)
    print("  PERSONA_BACKUP_FILE =", R.PERSONA_BACKUP_FILE)


def run_dws_check():
    """dws 实际调用比对：把『配置的路径』与『实际 invoked 的命令』对起来，
    并验证 dws 接口是否真能拉到未读。测试时必看。"""
    print("\n=== dws 实际调用比对 (DEBUG_DWS_CALL on) ===")
    e_ok = bool(M.DWS_ENTRY and os.path.exists(M.DWS_ENTRY))
    c_ok = bool(M.DWS_CMD and os.path.exists(M.DWS_CMD))
    n_ok = bool(M.NODE and os.path.exists(M.NODE))
    # DWS_EXE 是首选路由（DIRECT-exe），单独打印；缺失会回退 NODE-direct / DWS_CMD
    x_ok = bool(M.DWS_EXE and os.path.exists(M.DWS_EXE))
    print(f"  配置: DWS_EXE  = {M.DWS_EXE}")
    print(f"        exists   = {x_ok}  (首选路由 DIRECT-exe)")
    print(f"        DWS_ENTRY={M.DWS_ENTRY}")
    print(f"        exists   = {e_ok}")
    print(f"        DWS_CMD  = {M.DWS_CMD}")
    print(f"        exists   = {c_ok}")
    print(f"        NODE     = {M.NODE}")
    print(f"        exists   = {n_ok}")
    # 路由优先级（与 M.run_dws 一致）：DIRECT-exe(dws.exe) -> NODE-direct(node+dws.js)
    # -> DWS_CMD-fallback(dws.cmd)。三条路由的输出都统一走文件重定向（dws 对 PIPE
    # 异步 flush 丢失，Python 读 PIPE 恒空；文件重定向是实际主力，与控制台无关）。
    # 这是配置层预判；实际路由以调试日志 [dws-route] 行为准。
    route = ("DIRECT-exe" if x_ok
             else ("NODE-direct" if (e_ok and n_ok)
                   else ("DWS_CMD-fallback" if c_ok else "NONE!! dws 不可用")))
    print(f"  实际路由: {route}")
    print("  实际调用: run_dws(['chat','message','list-unread-conversations','--format','json'])")
    t0 = time.time()
    out = M.run_dws(["chat", "message", "list-unread-conversations", "--format", "json"])
    cost = time.time() - t0
    out_len = len(out or "")
    try:
        data = json.loads(out)
        convs = (data.get("result") or {}).get("conversations") or []
        parsed = len(convs)
    except Exception as e:
        parsed = -1
        print(f"  [warn] 解析失败: {e!r}")
    print(f"  返回: out_len={out_len} 解析会话数={parsed} 耗时={cost:.2f}s")
    print(f"  比对: 配置exists(EXE={x_ok},ENTRY={e_ok},CMD={c_ok},NODE={n_ok}) <-> 实际路由={route} <-> 接口返回len={out_len}")
    verdict = "PASS" if (route != "NONE!! dws 不可用" and out_len > 0) else ("WARN(空返回)" if route != "NONE!! dws 不可用" else "FAIL(dws 不可用)")
    print(f"  结论: {verdict}")
    print("  （详细 argv/rc 见调试日志 ~/.workbuddy/dingtalk_auto_debug.log 的 [dws-call]/[dws-route] 行；")
    print("   实际数据抓取走文件重定向，日志表现为 [dws-file] OK out_len=N）")


def run_integration():
    """默认：以真实单聊未读跑通整条链路。"""
    print("\n=== get_unread (dws list-unread-conversations) ===")
    convs, health = M.get_unread()
    print(f"  dws health: {health}  (ok=有未读 / empty=真无未读 / fail=dws 异常)")
    for c in convs:
        print("  -", c.get("title"), "single=", c.get("singleChat"), "unread=", c.get("unreadPoint"))

    target = next((c for c in convs if c.get("singleChat")), None)
    if not target:
        print("\n[skip] 当前无单聊未读，跳过集成验证（群聊不代发，符合预期）")
        print("        想完整验证生成链路可用 --inject 模式：")
        print("        python _validate.py --inject --sender 同事甲 --message 你好")
        return

    cid = target["openConversationId"]
    print("\n=== target single chat:", target.get("title"), "cid=", cid)
    msg = M.get_latest_msg(cid)
    print("  msg_id   =", M.msg_field(msg, "openMessageId", "messageId", "msgId"))
    print("  sender   =", M.msg_field(msg, "sender", "senderName", "senderNick"))
    print("  senderOpenDingTalkId =", M.extract_sender_open_id(msg))
    content = M._as_text(M.msg_field(msg, "content", "text", "body", default=""))
    print("  content  =", repr(content[:80]))

    print("\n=== gen_reply (CodeBuddy SDK, 真实生成一次, 不发送) ===")
    reply = M.gen_reply(
        M.msg_field(msg, "sender", "senderName"),
        content if content.strip() else "(图片/媒体消息)",
    )
    print("  REPLY >>>", reply)

    print("\n=== dws reply --dry-run (校验命令形态, 不真发) ===")
    args = ["chat", "message", "reply",
            "--conversation-id", cid,
            "--ref-msg-id", M.msg_field(msg, "openMessageId", "messageId", "msgId"),
            "--ref-sender", M.extract_sender_open_id(msg),
            "--text", reply or M.FALLBACK_REPLY, "--yes", "--dry-run"]
    out = M.run_dws(args)
    print(out[:600])
    print("\n=== validate done ===")


def run_inject(sender, message, cid):
    """注入测试：手动假消息跑 gen_reply，再把回复「发给自己」（绝不发给别人）。"""
    print(f"\n=== INJECT MODE（测试消息只发给自己）===")
    print(f"  sender  = {sender!r}")
    print(f"  message = {message!r}")

    print("\n=== gen_reply (CodeBuddy SDK, 真实生成, 不发送) ===")
    t0 = time.time()
    reply = M.gen_reply(sender, message)
    cost = time.time() - t0
    print(f"  returned in {cost:.1f}s")
    print("  REPLY >>>", reply)

    self_id = M.get_self_openid()
    print("\n=== 目标：老板自己 (SELF) ===")
    print("  self openDingTalkId =", self_id or "(未检测到，可用 SELF_OPENDINGTALK_ID 指定)")

    if cid:
        # 高级路径：用户显式指定真实会话，测 reply(带引用) 命令形态（会发到该会话，慎用于真人）
        print(f"\n[advanced] --cid 指定了真实会话 {cid}，做 reply --dry-run（不真发）")
        msg = M.get_latest_msg(cid)
        ref_id = M.msg_field(msg, "openMessageId", "messageId", "msgId")
        ref_sender = M.extract_sender_open_id(msg)
        if not ref_id:
            print("  [warn] 该会话取不到最新消息 ref，跳过 reply --dry-run。")
        else:
            out = M.run_dws(["chat", "message", "reply", "--conversation-id", cid,
                             "--ref-msg-id", ref_id, "--ref-sender", ref_sender,
                             "--text", reply or M.FALLBACK_REPLY, "--yes", "--dry-run"])
            print(out[:600])
        print("\n=== inject done ===")
        return

    # 默认路径：把回复发给自己（安全，绝不会打扰别人）
    if DRY_RUN:
        print("\n[DRY_RUN] 不会真发。去掉 DRY_RUN=1 后，上面的回复会直接出现在你自己的钉钉会话里。")
    else:
        if not self_id:
            print("\n[abort] 未检测到自己的 openDingTalkId，无法发给自己。")
            print("         设置环境变量 SELF_OPENDINGTALK_ID=你的openDingTalkId 后重试。")
        else:
            ok = M.send_reply_self(reply or M.FALLBACK_REPLY)
            print(f"\n[send to self] ok={ok}  -> 已把测试回复发到你自己的钉钉会话")
    print("\n=== inject done ===")


def run_guard_test(cid):
    """验证抢答防护逻辑（活跃检测 + 延迟窗口），不真发任何消息、不触碰任何人会话。"""
    print("\n=== GUARD TEST（抢答防护逻辑验证，不真发）===")
    if not cid:
        cid = M.find_single_conversation(7)
        print("  auto-detected single-chat cid =", cid or "(无)")
    if not cid:
        print("  [skip] 没有可用的单聊会话用于测试，可用 --cid 指定")
        return
    # 1) 活跃检测：老板最近是否在该会话发过消息
    print("\n[1] owner_recently_active(300s) =", M.owner_recently_active(cid, 300))
    print("    True  = 老板最近5分钟在该会话发过消息 → 会跳过代发（他在跟，会自己回）")
    print("    False = 老板不活跃 → 会进延迟窗口，等窗口结束才代发")
    # 2) 延迟窗口演示：只生成回复不真发
    print(f"\n[2] 模拟「发现未读 → 进 REPLY_DELAY_SEC 延迟窗口 → 到期代发」")
    print(f"    REPLY_DELAY_SEC = {M.REPLY_DELAY_SEC}s, ACTIVE_WINDOW_SEC = {M.ACTIVE_WINDOW_SEC}s")
    print("    DRY_RUN 下只生成回复不真发；真实运行会等延迟窗口结束才发（期间老板回了就取消）")
    reply = M.gen_reply("测试同事", "在吗？方案发你邮箱了")
    print("    若老板在窗口内未回复，将代发：", reply or "(生成失败 → 转人工通知)")
    print("\n=== guard test done ===")


def run_construct_test():
    """验证 gen_reply 修复后的 prompt 构造是否正确（不真发 SDK，monkey-patch 拦截）。
    五个场景：
      1) 延时期内对方连发多条：物理合并为一条主消息（burst-merged 模式）
      2) 单条对方消息问进度：查表 grounding 应被激活（single-main 模式）
      3) 延时期内对方连发，其中一条含'问题反馈'：table_context 保留（burst 合并后整体判 intent）
      4) 含老板历史发言：应作为背景历史喂给 AI（模仿口吻+理解上下文），
         但主回复对象仍是对方最新一条（不"回复自己"）
      5) 跨窗口的'问题反馈'是背景历史：不应被当主消息、不应触发查表
    关键修复点（2026-07-20 老板纠偏 + 2026-07-30 burst 合并）的回归验证。"""
    print("\n=== CONSTRUCT TEST（prompt 构造验证，monkey-patch 拦截 SDK，不真发）===")
    import reply as R

    async def fake_sdk_async(persona, prompt, image_paths=None, session_id=None, resume=False):
        print(f"\n{'='*78}")
        print(f"[FAKE SDK] session_id={session_id} resume={resume}")
        print(f"{'='*78}")
        print(f"【system_prompt 长度】: {len(persona)}")
        # 只在非空且较短时全打，长则截断显示前 400 字
        if persona:
            head = persona[:400]
            print(f"【system_prompt (前 400 字)】\n{head}")
            if len(persona) > 400:
                print(f"... (后 {len(persona)-400} 字省略)")
        print(f"\n【user_msg 完整内容】\n{prompt}")
        print(f"{'='*78}\n")
        return ""  # 空 → gen_reply 返回 ("", "")

    R._gen_reply_sdk_async = fake_sdk_async

    # 场景 1：延时期内对方连发多条 → 应物理合并为一条主消息（burst-merged）
    print("\n" + "#"*78)
    print("# 场景 1：延时期内对方连发多条 → burst-merged 合并为一条主消息")
    print("#"*78)
    msgs1 = [
        {"sender": "同事甲", "content": "已经忙到头昏了", "msg_id": "m7", "ts": 1700000007},
        {"sender": "同事甲", "content": "我以为让我测试呢", "msg_id": "m6", "ts": 1700000006},
        {"sender": "同事甲", "content": "目前问题反馈的进度怎么样了？呢", "msg_id": "m3", "ts": 1700000003},
        {"sender": "同事甲", "content": "不行，我让agent自己去调多维表查项目", "msg_id": "m2", "ts": 1700000002},
        {"sender": "同事甲", "content": "问题反馈表，内容跟进一下", "msg_id": "m1", "ts": 1700000001},
    ]
    R.gen_reply(sender="同事甲", content="已经忙到头昏了", return_rejected=True,
                session_id="dt_test_xxx", resume=True, messages=msgs1)

    # 场景 2：单条对方消息问进度（无历史）→ 查表 grounding 应激活（single-main 模式）
    print("\n" + "#"*78)
    print("# 场景 2：单条对方消息问进度 → single-main 模式 + 查表 grounding 激活")
    print("#"*78)
    msgs2 = [{"sender": "同事甲", "content": "目前问题反馈的进度怎么样了？呢",
              "msg_id": "m1", "ts": 1700000001}]
    R.gen_reply(sender="同事甲", content="目前问题反馈的进度怎么样了？呢",
                return_rejected=True, session_id="dt_test_yyy", resume=False, messages=msgs2)

    # 场景 3：延时期内对方连发'问题反馈'+'测试' → burst 合并后整体判 intent=feedback，
    #         table_context 应保留（旧设计"主消息=最新一条'测试' → 丢弃 context"已被 burst 替代）
    print("\n" + "#"*78)
    print("# 场景 3：延时期内对方连发'问题反馈'+'测试' → burst 合并后 table_context 应保留")
    print("#"*78)
    msgs3 = [
        {"sender": "同事甲", "content": "我以为让我测试呢", "msg_id": "m2", "ts": 1700000002},
        {"sender": "同事甲", "content": "问题反馈表，内容跟进一下", "msg_id": "m1", "ts": 1700000001},
    ]
    R.gen_reply(sender="同事甲", content="我以为让我测试呢", return_rejected=True,
                session_id="dt_test_zzz", resume=True, messages=msgs3,
                table_context="【问题反馈表·真实数据】当前老板名下共 3 条待解决：…")

    # 场景 4：含老板历史发言 → 应作为背景历史喂给 AI（模仿口吻+理解上下文），
    #         但主回复对象仍是对方连发的多条（burst 合并后含'那个 bug 修好了吗'+'结果怎么样了？'）
    print("\n" + "#"*78)
    print("# 场景 4：含老板历史发言 → burst 合并对方窗口消息 + 老板历史进背景")
    print("#"*78)
    msgs4 = [
        # 对方最新一条 = 主回复对象
        {"sender": "同事甲", "content": "结果怎么样了？", "msg_id": "m5", "ts": 1700000005, "is_self": False},
        # 老板历史发言（应进背景历史，标注"你（本人历史发言）"）
        {"sender": "本人", "content": "我下午测下给你", "msg_id": "m4", "ts": 1700000004, "is_self": True},
        # 对方更早一条（与最新一条同在延时期内，应被 burst 合并进主消息）
        {"sender": "同事甲", "content": "那个 bug 修好了吗", "msg_id": "m3", "ts": 1700000003, "is_self": False},
    ]
    R.gen_reply(sender="同事甲", content="结果怎么样了？", return_rejected=True,
                session_id="dt_test_www", resume=True, messages=msgs4)

    # 场景 5：跨窗口的'问题反馈'（时间差 > REPLY_DELAY_SEC）→ 不进 burst、应作为背景历史，
    #         也不应被 detect_table_intent 当主消息触发查表（防 2026-07-20 旧 bug 复发）
    print("\n" + "#"*78)
    print("# 场景 5：跨窗口的'问题反馈'→ 不进 burst、当背景历史、不触发查表")
    print("#"*78)
    _WIN = M.REPLY_DELAY_SEC  # 与 runtime 单一真源，不重复硬编码默认值
    _T0 = 1700000500  # 主消息锚点
    msgs5 = [
        # 对方最新一条 = 主消息（不含'问题反馈'，纯闲聊）
        {"sender": "同事甲", "content": "好的谢谢", "msg_id": "m2", "ts": _T0, "is_self": False},
        # 对方更早一条，时间差远超 REPLY_DELAY_SEC（跨窗口）→ 应进背景历史，不进 burst
        {"sender": "同事甲", "content": "问题反馈表，内容跟进一下", "msg_id": "m1",
         "ts": _T0 - _WIN - 600, "is_self": False},  # 比主消息早 WIN+600s
    ]
    R.gen_reply(sender="同事甲", content="好的谢谢", return_rejected=True,
                session_id="dt_test_vvv", resume=True, messages=msgs5)

    print("\n=== construct test done（拦截 SDK，未真发）===")
    print("判据（2026-07-30 burst 合并后）：")
    print("  场景1: mode=burst-merged, window_peer=5, main 含全部 5 条连发消息")
    print("  场景2: mode=single-main, window_peer=1, 查表 grounding 激活")
    print("  场景3: mode=burst-merged, 合并后含'问题反馈' → table_context 保留（旧'测试丢弃'已不适用）")
    print("  场景4: mode=burst-merged, window_peer=2（对方两条进主消息），老板历史进背景")
    print("  场景5: mode=single-main, 跨窗口的'问题反馈'进背景历史、不触发查表（防 07-20 旧 bug 复发）")


class _GbrainMCPClient:
    """最小 MCP Streamable-HTTP 客户端：用于验证 gbrain MCP 端点工具可用。
    不依赖 agent 子进程，零沙箱问题。gbrain serve --http 返回 SSE(text/event-stream)，
    无需 Mcp-Session-Id（无状态模式）。"""
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self._id = 0

    def _post(self, method, params=None):
        self._id += 1
        payload = json.dumps({"jsonrpc": "2.0", "id": self._id, "method": method,
                              "params": params or {}}).encode("utf-8")
        req = urllib.request.Request(self.url, data=payload, method="POST", headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": "Bearer " + self.token,
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8", "replace")
        except urllib.error.URLError as e:
            return {"error": str(e)}
        # 解析 SSE：收集所有 data: 行
        data_lines = []
        for line in body.split("\n"):
            line = line.rstrip("\r")
            if line.startswith("data:"):
                data_lines.append(line[len("data:"):].lstrip())
        if not data_lines:
            return None
        try:
            return json.loads("\n".join(data_lines))
        except Exception:
            return None

    def initialize(self):
        return self._post("initialize", {"protocolVersion": "2024-11-05",
                                         "capabilities": {},
                                         "clientInfo": {"name": "_validate", "version": "1.0"}})

    def list_tools(self):
        r = self._post("tools/list")
        return ((r or {}).get("result") or {}).get("tools") or []

    def call_tool(self, name, arguments):
        return self._post("tools/call", {"name": name, "arguments": arguments})


def run_mcp_test():
    """验证 gbrain MCP 工具链路（不跑 agent 子进程，零沙箱问题）：
      1) initialize 握手
      2) tools/list 含 search/query（SDK 侧即 mcp__gbrain__search/query）
      3) tools/call search 返回真实内容（非空、非 error）
      4) 静态验证：gen_reply 注入 agent 的 system_prompt 确实含 gbrain 调用指引
    四者全过 => MCP 工具验证 PASS，证明 agent 端「有 gbrain MCP 工具 + 知道怎么用」。"""
    print("\n=== MCP TOOL TEST（gbrain HTTP 端点，直接验证 MCP 工具）===")
    import reply as R
    import runtime
    url = getattr(runtime, "GBRAIN_MCP_URL", None) or "http://localhost:3131/mcp"
    token = getattr(runtime, "GBRAIN_MCP_TOKEN", None)
    grounding = getattr(runtime, "GBRAIN_GROUNDING", None)
    print(f"  GBRAIN_GROUNDING = {grounding}")
    print(f"  MCP URL          = {url}")
    print(f"  token            = {token[:12]}... (len={len(token)})" if token else "  token            = (空!)")
    if not token:
        print("  [FAIL] 无 gbrain token，无法连接 MCP 端点")
        return 1

    client = _GbrainMCPClient(url, token)
    # 1) initialize
    init = client.initialize()
    srv = ((init or {}).get("result") or {}).get("serverInfo")
    print(f"  [1] initialize: serverInfo={srv}")
    ok_init = bool(srv)
    # 2) tools/list
    tools = client.list_tools()
    names = sorted(t["name"] for t in tools)
    has_search = "search" in names
    has_query = "query" in names
    print(f"  [2] tools/list: 工具数={len(names)}")
    print(f"      含 'search'(→agent侧 mcp__gbrain__search): {has_search}")
    print(f"      含 'query' (→agent侧 mcp__gbrain__query) : {has_query}")
    # 3) tools/call search
    call = client.call_tool("search", {"query": "惯导 ROS2 移动底盘 产品手册", "limit": 2})
    cres = (call or {}).get("result") or {}
    ctext = ""
    for c in (cres.get("content") or []):
        if c.get("type") == "text":
            ctext += c.get("text", "")
    ok_call = bool(ctext.strip()) and not cres.get("isError")
    print(f"  [3] tools/call search: isError={cres.get('isError')} 返回文本长度={len(ctext)}")
    if ctext.strip():
        print(f"      样例: {ctext[:100].replace(chr(10), ' ')}")
    # 4) 静态验证 gen_reply system_prompt 注入 gbrain 指引
    captured = {}
    async def _fake_sdk(persona, prompt, image_paths=None, session_id=None, resume=False):
        captured["sys"] = persona
        return ""
    R._gen_reply_sdk_async = _fake_sdk
    try:
        R.gen_reply(sender="同事甲", content="H30 惯导模块串口默认波特率是多少？",
                    session_id="dt_mcp_verify", resume=False)
    except Exception as e:
        print(f"  [4] gen_reply 静态调用异常: {e!r}")
    sys_text = captured.get("sys", "") or ""
    prompt_ok = ("gbrain" in sys_text) and (
        "mcp__gbrain__search" in sys_text or "mcp__gbrain__query" in sys_text)
    print(f"  [4] 静态验证: gen_reply system_prompt 含 gbrain 指引 = {prompt_ok} (长度 {len(sys_text)})")

    allok = ok_init and has_search and has_query and ok_call and prompt_ok
    print(f"\n=== MCP TOOL TEST: {'ALL PASS' if allok else 'FAIL'} ===")
    print("  判据: initialize 握手成功 + tools/list 含 search/query")
    print("        + tools/call search 返回真实内容 + gen_reply 注入 gbrain 调用指引")
    print("  说明: MCP 服务端工具名是 search/query，SDK 客户端会自动加 mcp__gbrain__ 前缀；")
    print("        本测试直接对端点验证，与 agent 实际调用解耦，避免沙箱/行为黑盒干扰。")
    return 0 if allok else 1


def run_env_check():
    """环境预检：一键核查所有运行依赖（SDK / dws / codebuddy CLI / node / 视觉 / 人设），
    缺失项给精确修复命令。这是 SKILL.md「环境要求与安装」章节的自动化落地——
    任何模式运行前都会先跑一遍，环境异常第一时间暴露。"""
    import runtime as RT
    import reply as R
    print("\n=== ENV CHECK（环境预检）===")
    problems, warnings = [], []

    def mark(ok):
        return "OK  " if ok else "MISS"

    # 1) 解释器
    print(f"  python        : {sys.executable}  ({sys.version.split()[0]})")

    # 2) CodeBuddy Agent SDK（生成回复 + 图片识别唯一后端，关键）
    sdk_ok = RT._SDK_AVAILABLE
    print(f"  [{mark(sdk_ok)}] CodeBuddy Agent SDK (codebuddy_agent_sdk)")
    # 2b) 声明的 SDK python（.env 的 CODEBUDDY_SDK_PYTHON）
    sdk_py = RT.CODEBUDDY_SDK_PYTHON
    if sdk_py:
        py_ok = os.path.isfile(sdk_py)
        print(f"  [{mark(py_ok)}] CODEBUDDY_SDK_PYTHON = {sdk_py}")
        if not py_ok:
            problems.append(f"CODEBUDDY_SDK_PYTHON 指向不存在的 python：{sdk_py}")
            print("        修复: 跑 _setup_env.py 重新探测写入；或手动修正 .env")
    else:
        print(f"  [-- ] CODEBUDDY_SDK_PYTHON = (未配置，使用当前解释器)")
        print(f"        提示: 安装时跑 _setup_env.py 可自动写入 SDK python，实现启动自愈")
    if not sdk_ok:
        problems.append("codebuddy-agent-sdk 未安装（生成回复/图片识别均不可用）")
        home = os.path.expanduser("~")
        venv_py = os.path.join(home, ".workbuddy", "binaries", "python", "envs", "default",
                                "Scripts", "python.exe") if sys.platform.startswith("win") \
            else os.path.join(home, ".workbuddy", "binaries", "python", "envs", "default", "bin", "python3")
        print(f"        修复: {venv_py} -m pip install codebuddy-agent-sdk")
        if sdk_py and os.path.isfile(sdk_py):
            print(f"        或: 用该 SDK python 直接跑（monitor 也会自动重拉到它）：{sdk_py} _validate.py --env")
        else:
            print(f"        关键: 必须用装了 SDK 的 default venv python 跑本脚本（裸 managed python 不含 SDK）")

    # 3) dws CLI 路由
    x_ok = bool(RT.DWS_EXE and os.path.exists(RT.DWS_EXE))
    e_ok = bool(RT.DWS_ENTRY and os.path.exists(RT.DWS_ENTRY))
    c_ok = bool(RT.DWS_CMD and os.path.exists(RT.DWS_CMD))
    n_ok = bool(RT.NODE and os.path.exists(RT.NODE))
    route = ("DIRECT-exe" if x_ok else ("NODE-direct" if (e_ok and n_ok)
                                        else ("DWS_CMD-fallback" if c_ok else "NONE")))
    dws_ok = route != "NONE"
    print(f"  [{mark(dws_ok)}] dws CLI 路由 = {route}")
    if not dws_ok:
        problems.append("dws 不可用（未入 PATH / 未授权）")
        print("        修复: 跑 gen_launcher.py 自动把 dws 加入 PATH；")
        print("              dws patch chmod 授权 chat.message:list / chat.message:send / contact:search")

    # 4) codebuddy CLI（SDK 底层 prewarm server）
    cb_ok = bool(RT.CODEBUDDY_CMD and os.path.exists(RT.CODEBUDDY_CMD))
    print(f"  [{mark(cb_ok)}] codebuddy CLI (CODEBUDDY_CMD)")
    if not cb_ok:
        warnings.append("codebuddy CLI 未找到（SDK 可能走自带路径；若代复异常再查 CODEBUDDY_CMD）")

    # 5) node（dws NODE-direct 路由）
    print(f"  [{mark(n_ok)}] node (dws NODE-direct 路由)")

    # 6) 视觉后端（与文本同后端）
    print(f"  [{mark(RT.VISION_ENABLED)}] 视觉识别 = {'启用' if RT.VISION_ENABLED else '降级(仅通知不识别)'}")
    print(f"        视觉模型 VISION_MODEL = {RT.VISION_MODEL}  (文本主模型 CODEBUDDY_MODEL = {RT.CODEBUDDY_MODEL})")
    if not RT.VISION_ENABLED:
        warnings.append("视觉识别不可用（与文本同后端，SDK 缺失时两者一并降级，非视觉单独问题）")

    # 7) gbrain MCP（查表 / 知识库，可选）
    gb_ok = bool(getattr(RT, "GBRAIN_MCP_URL", ""))
    print(f"  [{mark(gb_ok)}] gbrain MCP 配置 (GBRAIN_MCP_URL)")
    if not gb_ok:
        warnings.append("gbrain MCP 未配置（查表/知识库关闭，纯人设回复仍可用）")

    # 8) 人设 agent 注册（可选，缺失用 skill 内兜底）
    ag_ok = bool(getattr(R, "_AGENT_REGISTERED", False))
    print(f"  [{mark(ag_ok)}] 人设 agent 注册 (SOUL_AGENT={getattr(R, 'SOUL_AGENT', '?')})")
    if not ag_ok:
        warnings.append("人设 agent 未注册（将用 skill 内 dingtalk-helper-backup.md 兜底）")

    # 结论
    print("\n  --- 结论 ---")
    if problems:
        print(f"  [FAIL] 阻断级缺失 {len(problems)} 项，必须先修复再运行监控：")
        for p in problems:
            print(f"    · {p}")
    if warnings:
        print(f"  [WARN] 非阻断 {len(warnings)} 项（功能降级，可运行）：")
        for w in warnings:
            print(f"    · {w}")
    if not problems and not warnings:
        print("  [PASS] 环境完整，所有依赖就位。")
    return 1 if problems else 0


def run_statemachine_test():
    """验证延迟代发状态机纯函数（不真发、不依赖 dws/SDK）。
    覆盖 PENDING/GNOTIFY 的：活跃→取消、dws未确认 defer、defer超限→放弃/直推、
    到期→代发/推送、发送失败重试、失败达上限→放弃。"""
    print("\n=== STATE MACHINE TEST（状态机纯函数验证，不真发）===")
    F = M  # 别名
    fails = 0
    def check(name, cond):
        nonlocal fails
        status = "PASS" if cond else "FAIL"
        if not cond:
            fails += 1
        print(f"  [{status}] {name}")
    now = 1000.0

    # ---- PENDING ----
    # 1) 未到期 + 老板活跃 → cancel
    j = {"deadline": now + 100, "ts": 1.0, "sender": "同事甲"}
    a, nj = F._pending_next_state(j, now, True)
    check("PENDING 未到期+活跃=cancel", a == "cancel")
    check("PENDING 纯函数不改原 job.deadline", j["deadline"] == now + 100)
    # 2) 未到期 + 不活跃 → wait
    a, _ = F._pending_next_state({"deadline": now + 100, "ts": 1.0}, now, False)
    check("PENDING 未到期+不活跃=wait", a == "wait")
    # 3) 到期 + 活跃 → cancel
    a, _ = F._pending_next_state({"deadline": now - 1, "ts": 1.0}, now, True)
    check("PENDING 到期+活跃=cancel", a == "cancel")
    # 4) 到期 + 不活跃 → send_now
    a, _ = F._pending_next_state({"deadline": now - 1, "ts": 1.0}, now, False)
    check("PENDING 到期+不活跃=send_now", a == "send_now")
    # 5) 到期 + dws未确认(连续defer<3) → defer，deadline=now+20
    j = {"deadline": now - 1, "ts": 1.0, "defers": 1}
    a, nj = F._pending_next_state(j, now, None)
    check("PENDING dws未确认+defers<3=defer", a == "defer" and nj["defers"] == 2 and nj["deadline"] == now + 20)
    # 6) 到期 + dws未确认(defers到上限) → giveup（转人工）
    j = {"deadline": now - 1, "ts": 1.0, "defers": 3, "sender": "同事甲"}
    a, nj = F._pending_next_state(j, now, None)
    check("PENDING dws未确认+defers超限=giveup", a == "giveup" and nj["defers"] == 4)
    # 7) 代发后 send成功 → done
    a, _ = F._pending_after_send({"ts": 1.0}, True, False, now)
    check("PENDING after_send send_ok=done", a == "done")
    # 8) 代发后 send失败 + notify成功 → done（已提醒老板手动回）
    a, _ = F._pending_after_send({"ts": 1.0}, False, True, now)
    check("PENDING after_send send_fail+notify_ok=done", a == "done")
    # 9) 代发后 双重失败(push_fail<5) → retry，deadline=now+45
    j = {"ts": 1.0, "push_fail": 2}
    a, nj = F._pending_after_send(j, False, False, now)
    check("PENDING after_send 双重失败<上限=retry",
          a == "retry" and nj["push_fail"] == 3 and nj["push_retry"] is True and nj["deadline"] == now + 45)
    # 10) 代发后 双重失败(push_fail到上限) → giveup
    j = {"ts": 1.0, "push_fail": 4}
    a, nj = F._pending_after_send(j, False, False, now)
    check("PENDING after_send 双重失败=上限=giveup", a == "giveup" and nj["push_fail"] == 5)

    # ---- GNOTIFY ----
    # 11) 未到期 + 非重试 + 活跃 → cancel
    a, _ = F._gnotify_next_state({"deadline": now + 100, "ts": 1.0, "push_retry": False}, now, True)
    check("GNOTIFY 未到期+非重试+活跃=cancel", a == "cancel")
    # 12) 未到期 + 重试中(即使活跃) → wait（不取消，避免老板在线却永久收不到）
    a, _ = F._gnotify_next_state({"deadline": now + 100, "ts": 1.0, "push_retry": True}, now, True)
    check("GNOTIFY 未到期+重试中=wait(不取消)", a == "wait")
    # 13) 到期 + 活跃 → cancel
    a, _ = F._gnotify_next_state({"deadline": now - 1, "ts": 1.0}, now, True)
    check("GNOTIFY 到期+活跃=cancel", a == "cancel")
    # 14) 到期 + 不活跃 → push_now
    a, _ = F._gnotify_next_state({"deadline": now - 1, "ts": 1.0}, now, False)
    check("GNOTIFY 到期+不活跃=push_now", a == "push_now")
    # 15) 到期 + dws未确认(defers<3) → defer
    j = {"deadline": now - 1, "ts": 1.0, "defers": 2}
    a, nj = F._gnotify_next_state(j, now, None)
    check("GNOTIFY dws未确认+defers<3=defer", a == "defer" and nj["defers"] == 3 and nj["deadline"] == now + 20)
    # 16) 到期 + dws未确认(defers超限) → giveup（push anyway，群不漏）
    j = {"deadline": now - 1, "ts": 1.0, "defers": 3}
    a, nj = F._gnotify_next_state(j, now, None)
    check("GNOTIFY dws未确认+defers超限=giveup(push anyway)", a == "giveup" and nj["defers"] == 4)
    # 17) 推送成功 → done
    a, _ = F._gnotify_after_push({"ts": 1.0}, True, now)
    check("GNOTIFY after_push ok=done", a == "done")
    # 18) 推送失败(push_fail<5) → retry
    j = {"ts": 1.0, "push_fail": 3}
    a, nj = F._gnotify_after_push(j, False, now)
    check("GNOTIFY after_push fail<上限=retry",
          a == "retry" and nj["push_fail"] == 4 and nj["push_retry"] is True and nj["deadline"] == now + 45)
    # 19) 推送失败(push_fail到上限) → giveup
    j = {"ts": 1.0, "push_fail": 4}
    a, nj = F._gnotify_after_push(j, False, now)
    check("GNOTIFY after_push fail=上限=giveup", a == "giveup" and nj["push_fail"] == 5)

    print(f"\n=== state machine test: {'ALL PASS' if fails == 0 else str(fails) + ' FAILED'} ===")
    return fails


def run_regex_test():
    """验证质检正则（extract_reply / _looks_like_reply）的关键用例，不真发、不耗积分。
    覆盖：<reply> 抽取、空洞收尾拒、正文+收尾抽正文、正常回复不误伤、
    角色扮演/老板/助理泄漏/凭印象答拦截、反问放行。回归 2026-08-11 空洞收尾 bug 等历史缺陷。
    （历史上这两处正则反复踩坑，此前却无自动化断言——本模式补齐。）"""
    print("\n=== REGEX TEST（质检正则验证，不真发）===")
    import reply as R
    fails = 0
    def check(name, cond, detail=""):
        nonlocal fails
        status = "PASS" if cond else "FAIL"
        if not cond:
            fails += 1
        print(f"  [{status}] {name}" + (f"  -> {detail}" if detail else ""))

    E = R.extract_reply
    check("extract <reply> 标签", E("<reply>收到，我下午发你。</reply>") == "收到，我下午发你。",
          repr(E("<reply>收到，我下午发你。</reply>")))
    check("extract <reply> 去首尾空白", E("<reply>\n  好的  \n</reply>") == "好的")
    check("extract 空串", E("") == "")
    check("extract 引用块兜底", E("分析…\n> 我确认下再回你") == "我确认下再回你")
    _got = E("这个我下午发你。\n先这样定方向，有问题随时找我。")
    check("extract 正文+空洞收尾 → 取正文", _got == "这个我下午发你。", repr(_got))
    # ⚠️ 2026-08-14 标签变体剥除回归（「回复出现代码」根因：标签变体漏剥→带标签原文代发）
    _t = "还没定呢，目前就常规筒灯+灯带那套，方案还在走，定了告诉你。"
    check("extract 带空格标签", E(f"< reply >{_t}</ reply >") == _t, repr(E(f"< reply >{_t}</ reply >")))
    check("extract 大写标签", E(f"<REPLY>{_t}</REPLY>") == _t)
    check("extract 全角标签", E(f"＜reply＞{_t}＜/reply＞") == _t)
    check("extract 无闭合标签", E(f"<reply>{_t}") == _t)
    check("extract 双重嵌套标签", E(f"<reply><reply>{_t}</reply></reply>") == _t)
    # ⚠️ 2026-08-19 工具调用标签残留回归（「回复乱码」根因：模型把 </parameter>/</tool_calls> 混进回复）
    check("extract 剥 `正文。</parameter>` 尾缀", E("哈哈行，我说咋牛头不对马嘴的。</parameter>") == "哈哈行，我说咋牛头不对马嘴的。",
          repr(E("哈哈行，我说咋牛头不对马嘴的。</parameter>")))
    check("extract 剥 `<reply>正文。</parameter>` 混合", E(f"<reply>{_t}</parameter>") == _t)
    check("extract 整条 `</tool_calls>` 剥空", E("</tool_calls>") == "")
    check("extract 整条 `</parameter>` 剥空", E("</parameter>") == "")
    # ⚠️ 2026-08-19 连续多标签结尾一次剥干净（`(?:...)+` 量词，否则残留一个靠质检兜底转人工）
    check("extract 连续多标签剥干净", E("哈哈行，我说咋牛头不对马嘴的。</parameter></tool_calls>") == "哈哈行，我说咋牛头不对马嘴的。",
          repr(E("哈哈行，我说咋牛头不对马嘴的。</parameter></tool_calls>")))
    # ⚠️ 2026-08-20 真根因回归（DSML 协议标记泄漏，三轮才定位）：真实乱码字符是
    # `</｜｜DSML｜｜parameter>`（中缀为全角竖线 U+FF5C 的 DSML 协议标记），前两轮
    # 手打用例（`</parameter>`）从未测过真实字符。以下用例必须含真实全角竖线，勿改成半角！
    _DSML_P = "</｜｜DSML｜｜parameter>"
    _DSML_T = "</｜｜DSML｜｜tool_calls>"
    _DSML_R = "</｜｜DSML｜｜reply>"
    check("真实字符自检(含全角竖线U+FF5C)", ord("｜") == 0xFF5C and "｜" in _DSML_P)
    check("extract 真实字符 `正文.</｜｜DSML｜｜parameter>`", E("哈哈行，我说咋牛头不对马嘴的。" + _DSML_P) == "哈哈行，我说咋牛头不对马嘴的。",
          repr(E("哈哈行，我说咋牛头不对马嘴的。" + _DSML_P)))
    check("extract 真实字符 整条 `</｜｜DSML｜｜tool_calls>`", E(_DSML_T) == "")
    check("extract 真实字符 `<reply>正文</｜｜DSML｜｜reply>`", E(f"<reply>{_t}" + _DSML_R) == _t)
    check("extract 半角变体 `</||DSML||parameter>`", E("哈哈行，我说咋牛头不对马嘴的。</||DSML||parameter>") == "哈哈行，我说咋牛头不对马嘴的。")

    L = R._looks_like_reply
    check("拒 标签残留", L("<reply>还没定呢</reply>") is False)
    check("拒 全角标签残留", L("＜reply＞还没定呢＜/reply＞") is False)
    check("拒 工具标签 `</tool_calls>`", L("</tool_calls>") is False)
    check("拒 工具标签 `</parameter>`", L("</parameter>") is False)
    check("拒 正文+`</parameter>` 兜底", L("哈哈行，我说咋牛头不对马嘴的。</parameter>") is False)
    check("拒 DSML 真实字符 `</｜｜DSML｜｜parameter>`", L("</｜｜DSML｜｜parameter>") is False)
    check("拒 DSML 真实字符(正文后缀)", L("哈哈行，我说咋牛头不对马嘴的。</｜｜DSML｜｜parameter>") is False)
    check("拒 孤立 ｜｜DSML｜｜ 标记", L("正文 ｜｜DSML｜｜ 继续正文") is False)
    check("放行 技术回复含 <node> 不误伤", L("launch 里 <node> 标签要写对") is True)
    check("正常回复放行", L("收到，我下午发你。") is True)
    check("信息+收尾不误伤", L("具体我下午发你。有问题随时找我。") is True)
    check("空洞收尾拒", L("先这样定方向，有问题随时找我。") is False)
    check("需发问句拒", L("需要我直接通过钉钉发出去吗？") is False)
    check("含老板拒", L("老板，这个我确认下。") is False)
    # ⚠️ 2026-08-22 误伤修复：旧规则「回复含'老板'即拒」把同事间正常提老板误杀
    # （08-21 蔡达轩"跟老板定" / 朱文杰"给老板汇报"两条正常草稿被拦转人工）。
    # 现在只有「老板+称呼标点」开头（对老板说话）才拒；指代/转述形态放行。
    check("指代老板放行(跟老板定)", L("行，你现场跟老板定就行。") is True)
    check("指代老板放行(给老板汇报)", L("我改完今晚给老板汇报。") is True)
    check("转述老板放行(老板说)", L("老板说9点在这边开会，你直接过来。") is True)
    check("角色扮演称呼拒(冒号)", L("老板：这个我没法处理。") is False)
    check("角色扮演称呼拒(叹号)", L("老板！这事我来处理") is False)
    check("角色扮演称呼拒", L("同事甲：明天的评审我看了。") is False)
    check("豁免冒号放行", L("注意：这个参数要改一下。") is True)
    check("助理泄漏拒", L("我帮您查询一下。") is False)
    check("凭印象答参数拒", L("我记得波特率是 115200。") is False)
    check("反问放行", L("要不要我帮你查下？") is True)
    check("超长跑题拒", L("测试" * 500) is False)

    print(f"\n=== regex test: {'ALL PASS' if fails == 0 else str(fails) + ' FAILED'} ===")
    return fails


def main():
    parser = argparse.ArgumentParser(description="钉钉自动回复自测（集成 / 注入 / 防护 / 构造 / 环境预检）")
    parser.add_argument("--inject", action="store_true", help="注入测试模式：手动假消息跑 gen_reply + reply --dry-run")
    parser.add_argument("--sender", default="测试同事", help="注入消息的发件人（仅用于生成上下文，不真发给此人）")
    parser.add_argument("--message", default="在吗？方案发你邮箱了", help="注入消息的内容")
    parser.add_argument("--cid", default=None, help="真实单聊会话ID，用于 reply --dry-run / --test-guard；缺省自动探测")
    parser.add_argument("--test-guard", action="store_true", help="验证抢答防护逻辑(活跃检测+延迟窗口)，不真发")
    parser.add_argument("--test-construct", action="store_true",
                        help="验证 gen_reply prompt 构造（主消息/背景历史分段+查表收紧），monkey-patch 拦截 SDK 不真发")
    parser.add_argument("--test-statemachine", action="store_true",
                        help="验证延迟代发状态机纯函数（PENDING/GNOTIFY 的取消/defer/重试/放弃分支），不真发")
    parser.add_argument("--test-mcp", action="store_true",
                        help="验证 gbrain MCP 工具链路：initialize 握手 + tools/list 含 search/query + tools/call search 返回真实内容 + gen_reply system_prompt 注入 gbrain 指引")
    parser.add_argument("--test-regex", action="store_true",
                        help="验证质检正则（extract_reply/_looks_like_reply）关键用例：<reply>抽取/空洞收尾拒/正文+收尾/正常不误伤/角色扮演/凭印象答拦截，不真发")
    parser.add_argument("--env", "--check-env", dest="env_check", action="store_true",
                        help="仅做环境预检：核查 SDK/dws/codebuddy CLI/node/视觉/人设 是否就位，打印修复命令，不跑任何生成")
    args = parser.parse_args()

    # 环境预检：--env 单独跑即退出；其它模式也先跑一遍（环境说明的自动化落地）
    if args.env_check:
        sys.exit(run_env_check())
    run_env_check()

    print_paths()
    run_dws_check()
    if args.test_guard:
        run_guard_test(args.cid)
    elif args.test_statemachine:
        run_statemachine_test()
    elif args.test_regex:
        sys.exit(run_regex_test())
    elif args.test_construct:
        run_construct_test()
    elif args.test_mcp:
        run_mcp_test()
    elif args.inject:
        run_inject(args.sender, args.message, args.cid)
    else:
        run_integration()


if __name__ == "__main__":
    main()
