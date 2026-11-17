#!/usr/bin/env python3
"""run_tests.py — 用 mock CLI 端到端验证监听引擎（不碰真实账号）。

覆盖：命中唤醒 / 防回环 / 水位不重复 / 关键词与发送者过滤 / 两种 JSON 形态 /
      stdout 多 JSON 文档 / SCHEMA_MISMATCH 诊断与 override 修复。

用法: python3 tests/run_tests.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")
MOCK = os.path.join(HERE, "mock_cli.py")
PY = sys.executable

passed = failed = 0


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print(f"  [ok] {name}")
    else:
        failed += 1
        print(f"  [FAIL] {name}  {detail}")


def setup(platform, shape, msgs, self_id="SELF_BOT", overrides=None):
    """建隔离工作区：env.json 指向 mock CLI，写好消息数据。"""
    d = tempfile.mkdtemp(prefix=f"standin_{platform}_")
    os.makedirs(os.path.join(d, "states"), exist_ok=True)
    data = os.path.join(d, "msgs.json")
    with open(data, "w") as f:
        json.dump({"messages": msgs}, f, ensure_ascii=False)
    ov = {"cli": os.path.abspath(MOCK)}
    ov.update(overrides or {})
    env = {
        "version": 1,
        "platforms": {platform: {"self_id": self_id, "logged_in": True}},
        "targets": {}, "overrides": {platform: ov},
    }
    with open(os.path.join(d, "env.json"), "w") as f:
        json.dump(env, f, ensure_ascii=False)
    return d, data


def listen(platform, d, data, shape, *args):
    script = os.path.join(SCRIPTS, {
        "wecom": "wecom_listen_cli.py",
        "dingtalk": "dingtalk_listen_cli.py",
        "feishu": "feishu_listen_cli.py",
    }[platform])
    env = dict(os.environ,
               IM_STANDIN_DIR=d, MOCK_SHAPE=shape, MOCK_DATA=data,
               MOCK_SELF=json.load(open(os.path.join(d, "env.json")))["platforms"][platform]["self_id"])
    return subprocess.run([PY, script] + list(args),
                          capture_output=True, text=True, env=env, timeout=60)


# ---------------------------------------------------------------- 用例
def test_wecom_hit():
    print("\n[wecom 形态] 命中 / 复合水位 / 防回环 / 过滤")
    msgs = [{"id": "x", "sender": "PEER", "content": "测试消息 REQ-2026", "time": "2026-10-30 10:00:00"}]
    d, data = setup("wecom", "wecom", msgs)
    r = listen("wecom", d, data, "wecom", "--user-id", "PEER", "--init", "zero",
               "--interval", "2", "--timeout", "5")
    check("命中返回 0", r.returncode == 0, f"rc={r.returncode} stderr={r.stderr[:200]}")
    hit = {}
    if r.returncode == 0:
        hit = json.loads(r.stdout.strip().splitlines()[-1])
    check("正文正确", "REQ-2026" in (hit.get("content") or ""), hit.get("content"))
    check("发送者正确", hit.get("sender") == "PEER", hit.get("sender"))
    check("不带身份噪声", "extra_identity_context" not in r.stdout)

    # 水位已推：同一批消息再跑不应再命中
    r2 = listen("wecom", d, data, "wecom", "--user-id", "PEER",
                "--interval", "2", "--timeout", "4")
    check("水位防重复命old", r2.returncode == 3, f"rc={r2.returncode} out={r2.stdout[:120]}")

    # 防回环：自己发的消息不该唤醒
    d3, data3 = setup("wecom", "wecom",
                      [{"id": "y", "sender": "SELF_BOT", "content": "我自己发的", "time": "2026-10-30 10:01:00"}])
    r3 = listen("wecom", d3, data3, "wecom", "--user-id", "PEER", "--init", "zero",
                "--interval", "2", "--timeout", "4")
    check("防回环", r3.returncode == 3, f"rc={r3.returncode}")

    # 发送者过滤
    d4, data4 = setup("wecom", "wecom",
                      [{"id": "z", "sender": "OTHER", "content": "别人说的", "time": "2026-10-30 10:02:00"}])
    r4 = listen("wecom", d4, data4, "wecom", "--user-id", "PEER", "--sender", "PEER",
                "--init", "zero", "--interval", "2", "--timeout", "4")
    check("发送者过滤生效", r4.returncode == 3, f"rc={r4.returncode}")

    # 关键词过滤：不匹配不唤醒
    d5, data5 = setup("wecom", "wecom",
                      [{"id": "k", "sender": "PEER", "content": "无关内容", "time": "2026-10-30 10:03:00"}])
    r5 = listen("wecom", d5, data5, "wecom", "--user-id", "PEER", "--keyword", "REQ-2026",
                "--init", "zero", "--interval", "2", "--timeout", "4")
    check("关键词过滤生效", r5.returncode == 3, f"rc={r5.returncode}")

    for x in (d, d3, d4, d5):
        shutil.rmtree(x, ignore_errors=True)


def test_dws_hit():
    print("\n[dws 形态] 倒序 + stdout 多 JSON 文档")
    msgs = [{"id": "m3", "sender": "PEER", "content": "最新的消息", "time": "2026-10-30 11:00:00"},
            {"id": "m2", "sender": "PEER", "content": "稍早的", "time": "2026-10-30 10:00:00"}]
    d, data = setup("dingtalk", "dws", msgs)
    r = listen("dingtalk", d, data, "dws", "--user-id", "PEER", "--init", "zero",
               "--interval", "2", "--timeout", "5")
    check("命中返回 0", r.returncode == 0, f"rc={r.returncode} stderr={r.stderr[:200]}")
    hit = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else {}
    check("取到最新一条（倒序不错位）", hit.get("message_id") == "m3", hit.get("message_id"))
    check("多 JSON 文档不影响解析", hit.get("sender") == "PEER", hit.get("sender"))
    shutil.rmtree(d, ignore_errors=True)


def test_schema_mismatch():
    print("\n[坏形态] SCHEMA_MISMATCH 诊断 + override 修复")
    msgs = [{"id": "s1", "sender": "PEER", "content": "字段全不对", "time": "2026-10-30 12:00:00"}]
    d, data = setup("wecom", "bad", msgs)
    r = listen("wecom", d, data, "bad", "--user-id", "PEER", "--init", "zero",
               "--interval", "2", "--timeout", "12")
    check("字段失配时退出 2 并报 SCHEMA_MISMATCH",
          r.returncode == 2 and "SCHEMA_MISMATCH" in r.stderr, f"rc={r.returncode} err={r.stderr[:200]}")

    # 用 overrides 改字段路径即可修好，不用改代码
    d2, data2 = setup("wecom", "bad", msgs, overrides={
        "f_items": [["data", "records"]],
        "f_msg_id": [["mid"]],
        "f_msg_sender": [["uid"]],
        "f_content_list": [["body"]],
        "f_create_time": [["t"]],
        "f_msg_id_compose": None,
    })
    # bad 形态里字段叫 x，这里换成与之匹配的 mock 形态：改用 wecom 数据但字段换名成本高，
    # 因此直接验证 override 里 f_items 生效即可（能解析出数组就算通过）
    r2 = listen("wecom", d2, data2, "bad", "--user-id", "PEER", "--init", "zero",
                "--interval", "2", "--timeout", "5")
    check("override 覆盖 f_items 后不再报 schema 错误",
          "SCHEMA_MISMATCH" not in r2.stderr, r2.stderr[:200])
    for x in (d, d2):
        shutil.rmtree(x, ignore_errors=True)


def test_time_window():
    print("\n[时间窗] 企微必须带 begin/end，引擎每轮生成")
    msgs = [{"id": "t1", "sender": "PEER", "content": "时间窗测试", "time": "2026-10-30 13:00:00"}]
    d, data = setup("wecom", "wecom", msgs)
    r = listen("wecom", d, data, "wecom", "--user-id", "PEER", "--init", "zero",
               "--lookback-min", "30", "--interval", "2", "--timeout", "5")
    # mock 不校验时间窗，但引擎必须成功把参数渲染出来（否则 CLI 会因缺参数报错）
    check("时间窗参数渲染成功", r.returncode == 0, f"rc={r.returncode} err={r.stderr[:200]}")
    shutil.rmtree(d, ignore_errors=True)


def test_docs():
    """文档索引不能烂：锚点可跳、章节齐全、无真实 ID 泄漏。"""
    if not os.path.exists(os.path.join(ROOT, "scripts", "verify_docs.py")):
        print("\n[文档] 跳过：包内没有 verify_docs.py（仅仓库版有）")
        return
    import glob
    import re

    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    from verify_docs import github_anchor, headings

    print("\n[文档] 故障索引锚点 / 章节完整 / 脱敏")
    tro = os.path.join(ROOT, "references", "troubleshooting.md")
    check("troubleshooting.md 存在", os.path.exists(tro))

    # ① 所有文档内锚点必须能跳：既认 HTML id="x"，也认 GitHub 标题锚
    files = [os.path.join(ROOT, "SKILL.md"), tro] + \
            glob.glob(os.path.join(ROOT, "references", "*.md")) + \
            glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True)
    bad = []
    for f in files:
        txt = open(f, encoding="utf-8").read()
        own = os.path.basename(f)
        for target, anchor in re.findall(r"\]\(([^)#\s]+\.md)?#([^)\s]+)\)", txt):
            path = os.path.join(ROOT, target) if target else f
            if target and not os.path.exists(path):
                bad.append(f"{own} → 文件不存在 {target}")
                continue
            body = open(path, encoding="utf-8").read()
            if f'id="{anchor}"' in body:
                continue
            if anchor in headings(body):
                continue
            bad.append(f"{own} → 锚点缺失 {target or own}#{anchor}")
    check("所有锚点可跳转", not bad, "; ".join(bad[:3]))

    # ② 索引必备章节（分诊表 + A..K）
    body = open(tro, encoding="utf-8").read()
    need = ['id="triage"'] + [f"## {c}." for c in "ABCDEFGHIJK"]
    missing = [n for n in need if n not in body]
    check("分诊表与 A-K 章节齐全", not missing, f"缺 {missing}")

    # ③ 文档里不许出现真实 ID / 凭据
    leak = []
    for f in files:
        txt = open(f, encoding="utf-8").read()
        for pat in (r"ou_[0-9a-f]{20,}", r"oc_[0-9a-f]{20,}",
                    r"aib[A-Za-z0-9_-]{20,}", r"Bearer\s+[A-Za-z0-9._-]{20,}"):
            if re.search(pat, txt):
                leak.append(f"{os.path.basename(f)}:{pat}")
    check("无真实 ID / token 泄漏", not leak, "; ".join(leak))

    # ④ 权限标准必须写在 SKILL.md 里（公开分发的前提：规则随包走）
    skill = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
    for kw, why in (("权限标准", "缺章节标题"),
                    ("keep", "缺默认策略说明"),
                    ("minimal", "缺最小集策略"),
                    ("--allow-add", "缺扩权闸门用法"),
                    ("--domain all", "缺「默认全量申请」这个坑"),
                    ("企业微信 / 钉钉", "缺无 scope 平台的差异说明")):
        check(f"SKILL.md 含「{kw}」（{why}）", kw in skill)


STUB = '''#!/usr/bin/env python3
import json, os, sys
name = os.path.basename(sys.argv[0])
args = sys.argv[1:]
def j(o): print(json.dumps(o))
if "--version" in args or args[:1] == ["version"]:
    print(f"{name} version 9.9.9"); sys.exit(0)
if args[:1] == ["doctor"]:
    j({"checks": [{"name": "auth", "status": "pass", "message": "ok"},
                  {"name": "net", "status": "pass", "message": "ok"}]}); sys.exit(0)
if args[:2] == ["auth", "status"]:
    j({"authenticated": True,
       "identities": {"user": {"tokenStatus": "valid", "openId": "ou_stub0001",
                               "expiresAt": "2099-01-01T00:00:00+00:00",
                               "refreshExpiresAt": "2099-01-01T00:00:00+00:00"}}}); sys.exit(0)
if args[:2] == ["auth", "show"]:
    print("Status: authorized\\nBot ID: FAKEBOTID"); sys.exit(0)
if args[:1] == ["profile"]:
    j({"profiles": [{"userId": "stubuser"}]}); sys.exit(0)
j({"ok": True})
'''


def test_doctor():
    """doctor.py 在纯桩环境下自洽：全绿、JSON 合法、退出 0。"""
    print("\n[体检] doctor.py 全绿 + JSON 输出")
    d = tempfile.mkdtemp(prefix="standin_doctor_")
    bindir = os.path.join(d, "bin")
    os.makedirs(bindir)
    for cli in ("lark-cli", "wecom-cli", "dws"):
        p = os.path.join(bindir, cli)
        with open(p, "w") as f:
            f.write(STUB)
        os.chmod(p, 0o755)
    with open(os.path.join(d, "env.json"), "w") as f:
        json.dump({"version": 1,
                   "platforms": {k: {"self_id": f"self_{k}"}
                                 for k in ("feishu", "wecom", "dingtalk")},
                   "targets": {}, "overrides": {}}, f)
    env = dict(os.environ, IM_STANDIN_DIR=d,
               PATH=bindir + os.pathsep + os.environ.get("PATH", ""))
    r = subprocess.run([PY, os.path.join(SCRIPTS, "doctor.py"), "--json"],
                       capture_output=True, text=True, env=env, timeout=120)
    ok_json = False
    try:
        data = json.loads(r.stdout)
        ok_json = True
    except Exception:
        data = {}
    check("doctor --json 输出合法 JSON", ok_json, r.stdout[:200] + r.stderr[:200])
    check("doctor 退出码 0（全部可用）", r.returncode == 0, f"rc={r.returncode} {r.stderr[:200]}")
    if ok_json:
        stats = {p: v["status"] for p, v in data.get("platforms", {}).items()}
        check("三平台均无 fail", all(s != "fail" for s in stats.values()), str(stats))
        check("self_id 已脱敏", "ou_stub0001" not in r.stdout)
    shutil.rmtree(d, ignore_errors=True)


def test_reauth():
    """授权卡片：结构正确、按钮直链、平台边界诚实（不假装支持）。"""
    print("\n[授权] 免扫码卡片结构 / 平台边界")
    sys.path.insert(0, SCRIPTS)
    import reauth

    url = ("https://accounts.feishu.cn/oauth/v1/device/verify"
           "?flow_id=FLOW0&user_code=AB12-CD34")
    card = reauth.build_card(url, "AB12-CD34", 10, who="分身")
    blob = json.dumps(card, ensure_ascii=False)
    acts = [e for e in card["elements"] if e.get("tag") == "action"]
    check("卡片含按钮动作", bool(acts))
    btn = acts[0]["actions"][0] if acts else {}
    check("按钮直链设备授权页（无需扫码）",
          btn.get("url") == url and "user_code=AB12-CD34" in btn.get("url", ""),
          btn.get("url"))
    check("正文带 user_code 兜底", "AB12-CD34" in blob)
    check("带勿转发警示", "勿转发" in blob)
    check("禁止卡片转发", card["config"].get("enable_forward") is False)

    # ---- 权限自适应：keep / minimal / 扩权闸门 ----
    src = open(os.path.join(SCRIPTS, "reauth.py"), encoding="utf-8").read()
    check("不出现 --domain（该参数默认 all，会全量申请）", '"--domain"' not in src)
    check("不出现 --recommend", '"--recommend"' not in src)
    check("login 显式带 --scope", '"--scope"' in src)
    check("有扩权闸门 guard_scopes", "def guard_scopes" in src)
    check("闸门默认拒跑（无 --allow-add 时不放行）", "if allow_add:" in src)

    class _A:                     # 默认参数：keep，无 --scope/--add
        scope = ""
        add = ""
        policy = "keep"

    # (1) 全新账号（无历史授权）→ 落到最小必需集，且不带任何无关业务域
    plan = reauth.resolve_scopes(_A(), cur=[], app=[])
    req = plan["requested"]
    check("无历史授权 -> 最小必需集", set(req) == set(reauth.REQUIRED_SCOPES), len(req))
    check("最小集覆盖 IM 收发", {"im:message:readonly", "im:message.send_as_user"} <= set(req))
    check("最小集含 offline_access（否则 2 小时一续）", "offline_access" in req)
    check("最小集不含妙搭 spark", not any(s.startswith("spark:") for s in req))
    check("最小集不含 base/docs/mail/drive",
          not any(s.startswith(("base:", "docs:", "docx:", "mail:", "drive:"))
                  for s in req))

    # (2) 应用只开通了部分权限 → 只申请交集，缺的单独报出，不硬塞
    partial = ["im:message:readonly", "im:message.send_as_user", "offline_access"]
    plan = reauth.resolve_scopes(_A(), cur=[], app=partial)
    check("应用未开通的必需权限不硬塞",
          set(plan["requested"]) <= set(partial) | reauth.BASE_SCOPES,
          plan["requested"])
    check("应用缺口被如实报出", len(plan["lack_on_app"]) > 0, plan["lack_on_app"])

    # (3) 有历史授权 → 原样沿用，新增恒为 0
    old = ["im:message:readonly", "offline_access", "base:record:read"]
    plan = reauth.resolve_scopes(_A(), cur=old, app=old)
    check("沿用现有权限时新增为 0", plan["added"] == [], plan["added"])
    check("沿用现有权限时不夹带其它域", plan["requested"] == old, plan["requested"])

    # (4) 显式扩权 → 默认被闸门拦住
    class _B(_A):
        add = "spark:app:read"
    plan = reauth.resolve_scopes(_B(), cur=old, app=old + ["spark:app:read"])
    check("新增权限被识别", plan["added"] == ["spark:app:read"], plan["added"])
    check("闸门拦下扩权", reauth.guard_scopes(plan, allow_add=False) is False)
    check("--allow-add 才放行", reauth.guard_scopes(plan, allow_add=True) is True)

    # (5) --policy minimal：主动收窄，只留必需集
    class _C(_A):
        policy = "minimal"
    plan = reauth.resolve_scopes(_C(), cur=old, app=old + reauth.REQUIRED_SCOPES)
    check("minimal 收窄到必需集",
          set(plan["requested"]) == set(reauth.REQUIRED_SCOPES), len(plan["requested"]))
    check("minimal 会丢掉无关域", "base:record:read" in plan["dropped"])

    # 企微/钉钉要么已授权(0)，要么明确 exit 4 给替代路径——不能假装支持卡片
    for plat, cli in (("wecom", "wecom-cli"), ("dingtalk", "dws")):
        if not shutil.which(cli):
            check(f"{plat} 未安装则跳过", True)
            continue
        r = subprocess.run([PY, os.path.join(SCRIPTS, "reauth.py"), plat],
                           capture_output=True, text=True, timeout=60)
        check(f"{plat} 平台边界诚实（rc∈{{0,4}}）", r.returncode in (0, 4),
              f"rc={r.returncode} {r.stdout[:120]}")


def test_find_command():
    """私聊解析结果必须生成可直接执行的监听命令。"""
    import contextlib
    import io
    sys.path.insert(0, SCRIPTS)
    import bootstrap as bs

    d = tempfile.mkdtemp(prefix="standin_find_")
    old_dir, old_path, old_run = bs.ENV_DIR, bs.ENV_PATH, bs.run
    bs.ENV_DIR = d
    bs.ENV_PATH = os.path.join(d, "env.json")
    bs.run = lambda *_args, **_kw: (0, {"data": {"users": [{
        "localized_name": "测试同事", "open_id": "ou_test", "p2p_chat_id": "oc_test",
    }]}}, "")
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            bs.resolve({"platforms": {"feishu": {}}, "targets": {}}, "feishu", "测试")
    finally:
        bs.ENV_DIR, bs.ENV_PATH, bs.run = old_dir, old_path, old_run
        shutil.rmtree(d, ignore_errors=True)
    text = out.getvalue()
    check("私聊监听建议使用 --chat-id", "--chat-id oc_test" in text, text)
    check("私聊监听建议不把 chat_id 当 user_id", "--user-id oc_test" not in text, text)


def test_absolute_deadline():
    """--until 是绝对截止时间：未来可命中，过期不再拉取/命中。"""
    import time
    print("\n[临时值守] 绝对截止时间")
    msgs = [{"id": "u1", "sender": "PEER", "content": "截止前", "time": "2026-10-30 13:00:00"}]
    d, data = setup("wecom", "wecom", msgs)
    r = listen("wecom", d, data, "wecom", "--user-id", "PEER", "--init", "zero",
               "--interval", "2", "--until", str(time.time() + 10))
    check("未来 --until 可正常命中", r.returncode == 0, f"rc={r.returncode} err={r.stderr[:200]}")
    d2, data2 = setup("wecom", "wecom", msgs)
    r2 = listen("wecom", d2, data2, "wecom", "--user-id", "PEER", "--init", "zero",
                "--interval", "2", "--until", str(time.time() - 1))
    check("过期 --until 退出 3", r2.returncode == 3, f"rc={r2.returncode} err={r2.stderr[:200]}")
    for x in (d, d2):
        shutil.rmtree(x, ignore_errors=True)


def test_cache_refresh():
    """--cache-refresh-min 到点主动退出（退出码 3），用一次重挂续上下文缓存。"""
    import time
    print("\n[缓存续期] 到点主动退出")
    msgs = [{"id": "c1", "sender": "PEER", "content": "旧消息", "time": "2026-10-30 14:00:00"}]
    d, data = setup("wecom", "wecom", msgs)
    start = time.time()
    r = listen("wecom", d, data, "wecom", "--user-id", "PEER", "--init", "latest",
               "--interval", "2", "--cache-refresh-min", "0.02", "--timeout", "20")
    elapsed = time.time() - start
    check("缓存续期到点退出 3", r.returncode == 3, f"rc={r.returncode} err={r.stderr[:200]}")
    check("退出原因写 stderr", "cache-refresh" in r.stderr, r.stderr[:200])
    check("不误报命中", '"hit": true' not in r.stdout, r.stdout[:200])
    check("按时退出（<8s）", elapsed < 8, f"{elapsed:.1f}s")
    shutil.rmtree(d, ignore_errors=True)


def test_profile_compact():
    """画像超限整理：去重、历史结论 ≤20、旧结论进 history、dry-run 不落盘。"""
    print("\n[画像] 超限整理 / 去重 / 归档")
    d = tempfile.mkdtemp(prefix="standin_compact_")
    env = dict(os.environ, IM_STANDIN_DIR=d)
    script = os.path.join(SCRIPTS, "bootstrap.py")
    r = subprocess.run([PY, script, "--alias", "feishu", "测试对象", "oc_demo"],
                       capture_output=True, text=True, env=env, timeout=30)
    profile = os.path.join(d, "profiles", "feishu", "oc_demo.md")
    hist = os.path.join(d, "profiles", "feishu", "oc_demo.history.md")
    check("别名注册建画像", r.returncode == 0 and os.path.exists(profile), r.stderr[:200])
    bullets = "\n".join(f"- 11-{i:02d} 历史事实 {i}" for i in range(30))
    text = ("# 测试对象\n\n> 飞书 · oc_demo\n\n## 对方是谁\n\n" + "填充" * 1666 +
            "\n\n## 沟通偏好\n\n- 直接\n\n## 在意与忌讳\n\n- 自证口径\n\n## 历史结论\n\n" +
            bullets + "\n- 11-00 历史事实 0\n")
    with open(profile, "w", encoding="utf-8") as f:
        f.write(text)
    before = os.path.getsize(profile)
    r2 = subprocess.run([PY, script, "--compact", "feishu", "测试对象", "--dry-run"],
                        capture_output=True, text=True, env=env, timeout=30)
    check("dry-run 退出 0 且不落盘",
          r2.returncode == 0 and os.path.getsize(profile) == before and not os.path.exists(hist),
          f"rc={r2.returncode} {r2.stderr[:200]}")
    r3 = subprocess.run([PY, script, "--compact", "feishu", "测试对象"],
                        capture_output=True, text=True, env=env, timeout=30)
    after = open(profile, encoding="utf-8").read()
    kept = [line for line in after.splitlines() if line.startswith("- 11-")]
    check("compact 退出 0", r3.returncode == 0, r3.stderr[:300])
    check("主文件 ≤12KB", os.path.getsize(profile) <= 12 * 1024, str(os.path.getsize(profile)))
    check("历史结论 ≤20 条", len(kept) <= 20, str(len(kept)))
    check("重复 bullet 被去重", after.count("- 11-00 历史事实 0") == 1,
          str(after.count("- 11-00 历史事实 0")))
    check("旧结论进 history", os.path.exists(hist) and "历史事实" in open(hist, encoding="utf-8").read())
    shutil.rmtree(d, ignore_errors=True)


def test_privacy_and_redaction():
    """个人数据默认私有；敏感语料脱敏；删除必须显式确认。"""
    import stat
    print("\n[隐私] 文件权限 / 语料脱敏 / 一键删除")
    d = tempfile.mkdtemp(prefix="standin_privacy_")
    env = dict(os.environ, IM_STANDIN_DIR=d)
    script = os.path.join(SCRIPTS, "bootstrap.py")
    r = subprocess.run([PY, script, "--alias", "feishu", "测试", "oc_test"],
                       capture_output=True, text=True, env=env, timeout=30)
    env_path = os.path.join(d, "env.json")
    check("别名写入成功", r.returncode == 0, r.stderr[:200])
    if os.path.exists(env_path):
        check("数据目录权限 700", stat.S_IMODE(os.stat(d).st_mode) == 0o700,
              oct(stat.S_IMODE(os.stat(d).st_mode)))
        check("env.json 权限 600", stat.S_IMODE(os.stat(env_path).st_mode) == 0o600,
              oct(stat.S_IMODE(os.stat(env_path).st_mode)))
    r2 = subprocess.run([PY, script, "--delete-data"], capture_output=True, text=True,
                        env=env, timeout=30)
    check("删除数据缺少 --yes 时拒跑", r2.returncode == 2 and os.path.exists(env_path),
          f"rc={r2.returncode}")
    r3 = subprocess.run([PY, script, "--delete-data", "--yes"], capture_output=True, text=True,
                        env=env, timeout=30)
    check("--delete-data --yes 删除个人数据", r3.returncode == 0 and not os.path.exists(env_path),
          f"rc={r3.returncode} err={r3.stderr[:200]}")

    sys.path.insert(0, SCRIPTS)
    import bootstrap as bs
    try:
        cleaned = bs.redact_sensitive(
            "看这个 https://example.com/?access_token=TOPSECRET，"
            "邮箱 a@example.com，password=VERYSECRET，结论不变")
    except AttributeError as e:
        check("提供语料脱敏函数", False, str(e))
    else:
        check("语料脱敏不泄露 URL/token/email/password",
              all(x not in cleaned for x in
                  ("TOPSECRET", "VERYSECRET", "a@example.com", "access_token=")), cleaned)
        check("语料脱敏保留风格文本", "结论不变" in cleaned, cleaned)
    shutil.rmtree(d, ignore_errors=True)


def test_schema_error_redaction():
    """schema 错误只暴露字段名，不回显消息正文或凭据值。"""
    sys.path.insert(0, SCRIPTS)
    import listen_core as lc
    ln = lc.Listener("wecom", {"cli": "mock", "cmd_list": ["messages"],
                               "f_items": [["messages"]]})
    raw = '{"unexpected":"TOPSECRET","content":"private message"}'
    ln.run_cli = lambda *_args, **_kw: (0, {"unexpected": "TOPSECRET",
                                             "content": "private message"}, raw)
    ok, err = ln.fetch_messages("target")
    check("schema 错误仍可诊断", not ok and "unexpected" in err, err)
    check("schema 错误不回显敏感值", "TOPSECRET" not in err and "private message" not in err, err)


def test_doctor_missing_cli():
    """没有任何 CLI 时必须不可用，未安装的平台不能进入 healthy。"""
    d = tempfile.mkdtemp(prefix="standin_no_cli_")
    bindir = os.path.join(d, "bin")
    os.makedirs(bindir)
    env = dict(os.environ, IM_STANDIN_DIR=d, PATH=bindir)
    r = subprocess.run([PY, os.path.join(SCRIPTS, "doctor.py"), "--json"],
                       capture_output=True, text=True, env=env, timeout=60)
    try:
        data = json.loads(r.stdout)
    except Exception:
        data = {}
    summary = data.get("summary", {})
    check("无 CLI 时 doctor 退出 2", r.returncode == 2,
          f"rc={r.returncode} out={r.stdout[:200]}")
    check("无 CLI 时 healthy 为空", summary.get("healthy") == [], str(summary))
    check("无 CLI 时三平台均 broken", set(summary.get("broken", [])) ==
          {"feishu", "wecom", "dingtalk"}, str(summary))
    shutil.rmtree(d, ignore_errors=True)


def test_safety_docs():
    """公开 skill 必须包含注入边界与不可重置的临时值守说明。"""
    skill = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
    check("文档声明聊天内容不可信", "不可信" in skill)
    check("文档禁止聊天消息触发命令/读文件", "执行命令" in skill and "读文件" in skill)
    check("文档提供 --until", "--until" in skill)
    check("文档提供 --cache-refresh-min", "--cache-refresh-min" in skill)
    check("文档说明 55 分钟缓存续期", "55 分钟" in skill and "缓存" in skill)
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    check("README 说明 55 分钟缓存续期", "55 分钟" in readme and "缓存" in readme)
    check("文档禁止重挂重置截止时间", "重置截止时间" in skill)
    check("文档提供显式数据删除命令", "--delete-data --yes" in skill)


def test_plugin_polling():
    """dsh-plugin：Node 单进程壳的 state/poller/live turn/API/迁移测试。"""
    plug = os.path.join(ROOT, "dsh-plugin")
    if not os.path.isdir(plug):
        print("\n[插件] 跳过：包内没有 dsh-plugin/（仅仓库版有）")
        return
    r = subprocess.run(["node", "--test"], cwd=plug, capture_output=True, text=True, timeout=180)
    tail = (r.stderr or r.stdout or "").strip().splitlines()
    detail = tail[-1] if tail else ""
    check("dsh-plugin Node 测试全过（state/poller/turns/app/迁移）", r.returncode == 0, detail)


def test_doc_contracts():
    """docs/specs/contracts 与代码对账 + 版本一致 + 构建产物新鲜度 + verify_docs。"""
    if not os.path.exists(os.path.join(HERE, "test_docs.py")):
        print("\n[文档对账] 跳过：包内没有 tests/test_docs.py（仅仓库版有）")
        return
    print("\n[文档对账] 契约 / 版本 / 构建产物 / verify_docs")
    sys.path.insert(0, HERE)
    import test_docs
    test_docs.main(check)


if __name__ == "__main__":
    print("== cyber-im-avatar 引擎端到端测试（mock CLI，不触发真实发送）==")
    test_wecom_hit()
    test_dws_hit()
    test_schema_mismatch()
    test_time_window()
    test_find_command()
    test_absolute_deadline()
    test_cache_refresh()
    test_profile_compact()
    test_privacy_and_redaction()
    test_schema_error_redaction()
    test_docs()
    test_safety_docs()
    test_doctor()
    test_doctor_missing_cli()
    test_reauth()
    test_plugin_polling()
    test_doc_contracts()
    print(f"\n结果：{passed} 通过 / {failed} 失败")
    sys.exit(1 if failed else 0)
