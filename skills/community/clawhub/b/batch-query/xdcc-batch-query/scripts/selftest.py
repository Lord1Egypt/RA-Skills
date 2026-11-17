#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xdcc-batch-query 自检脚本（纯静态，零网络）。

每个用例在独立临时目录中运行，零污染真实数据。
用法：python selftest.py
退出码：0 全过 / 1 有失败
"""

import contextlib
import io
import os
import shutil
import sys
import tempfile
from typing import Dict, List

# 将脚本目录加入路径，便于 import 主模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import batch_query as bq  # noqa: E402

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✓ {name}")
    else:
        FAIL += 1
        print(f"  ✗ {name}  {detail}")


# --------------------------------------------------------------------------- #
# 1. 签名与官方文档示例一致
# --------------------------------------------------------------------------- #
def test_signatures():
    print("[1] 签名生成与文档示例一致")
    doc_raw = "{'MemberID':'123','Tel':'8789','No':'118954907573','ReturnFormat':'JSON'}"
    doc_key = "66da2cf8-c8a2-14b2-b6fa-176cd7d1ba18"
    expect = "NDJlOGIzZDcyYmM1MDM2Njk3NDQzZGY2ODM2MmY4YmE%3d"
    got = bq.generate_data_sign(doc_raw, doc_key)
    check("DataSign == 文档示例", got == expect, f"got={got}")

    # 确定性：同一输入重复调用结果一致
    check("签名确定性", bq.generate_data_sign(doc_raw, doc_key) == got)


# --------------------------------------------------------------------------- #
# 2. summarize 提取正确
# --------------------------------------------------------------------------- #
def test_summarize():
    print("[2] summarize 摘要提取")
    data = {
        "ExpressName": "中通快递", "ShipperCode": "ZTO", "LogisticCode": "75012345678901",
        "State": 3, "StateDesc": "已签收",
        "Pickup_City": "杭州市", "Delivery_City": "深圳市",
        "Pickup_Time": "2025-09-10 14:24:17", "SignFor_Time": "2025-09-12 15:30:18",
        "Delivery_Courier": "麻松", "Delivery_Courier_Phone": "15986643789",
        "HalfwayStagnation_TimeOut": 1, "SignFor_TimeOut": 0,
        "SignFor_TimeSpan": 2946.0,
        "TraceList": [{"time": "t1", "desc": "d1"}, {"time": "t2", "desc": "d2"}],
        "LastTrace": "最后轨迹",
    }
    s = bq.summarize(data)
    check("快递公司", s["shipper"] == "中通快递")
    check("状态归类=已签收", s["state_label"] == "已签收", s["state_label"])
    check("超时标记捕获 HalfwayStagnation", any(t["field"] == "HalfwayStagnation_TimeOut" for t in s["timeouts"]))
    check("签收时效 humanize", s["spans"][-1]["human"] == "2天1小时", s["spans"][-1]["human"])
    check("最新轨迹取前3", len(s["latest_traces"]) == 2)


# --------------------------------------------------------------------------- #
# 3. 状态归类
# --------------------------------------------------------------------------- #
def test_classify():
    print("[3] 状态归类 classify_state")
    check("已签收", bq.classify_state("已签收") == "已签收")
    check("派送中", bq.classify_state("派件中") == "派送中")
    check("运输中", bq.classify_state("运输中") == "运输中")
    check("疑难", bq.classify_state("疑难件") == "疑难/异常")


# --------------------------------------------------------------------------- #
# 4. parse_input 解析（文件 / 内联 / 映射表）
# --------------------------------------------------------------------------- #
def test_parse_input():
    print("[4] 输入解析 parse_input")
    d = tempfile.mkdtemp(prefix="xdcc_selftest_")

    fpath = os.path.join(d, "list.txt")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write("# 注释行\nSF123,9378\nZTO456\n\nYTO789,1234\n")
    tpath = os.path.join(d, "tel.csv")
    with open(tpath, "w", encoding="utf-8", newline="") as f:
        f.write("no,tel\nEMS001,0000\n")

    # 仅文件
    args = _mkargs(file=fpath)
    items = bq.parse_input(args)
    check("文件解析去空行/注释", len(items) == 3, str(items))
    check("文件附Tel解析", ("SF123", "9378") in items, str(items))
    check("文件无Tel为空串", ("ZTO456", "") in items, str(items))

    # 内联
    args = _mkargs(nos="A1, B2 ,C3")
    items = bq.parse_input(args)
    check("内联分隔", len(items) == 3, str(items))

    # 映射表
    args = _mkargs(telmap=tpath)
    items = bq.parse_input(args)
    check("映射表解析", ("EMS001", "0000") in items, str(items))

    # 去重：同一单号出现两次只保留一次
    args = _mkargs(nos="X1,X1")
    items = bq.parse_input(args)
    check("去重", len(items) == 1, str(items))

    # 全局 tel 兜底（仅填补缺失项，不覆盖已有项）
    args = _mkargs(file=fpath, tel="9999")
    items = bq.parse_input(args)
    check("全局tel填补缺失项", items[1] == ("ZTO456", "9999"), str(items))
    check("全局tel不覆盖已有项", items[0] == ("SF123", "9378") and items[2] == ("YTO789", "1234"), str(items))


def _mkargs(**kw):
    class A:
        pass
    a = A()
    a.file = kw.get("file")
    a.telmap = kw.get("telmap")
    a.nos = kw.get("nos")
    a.tel = kw.get("tel", "")
    return a


# --------------------------------------------------------------------------- #
# 4b. 手机号后四位（Tel）缺失检查
# --------------------------------------------------------------------------- #
def test_missing_tel():
    print("[4b] 缺 Tel 检查 guess_shipper_code / find_missing_tel")
    # 字母前缀可识别公司
    check("SF → 顺丰", bq.guess_shipper_code("SF1234567890123") == "SF")
    check("ZTO → 中通", bq.guess_shipper_code("ZTO7654321") == "ZTO")
    check("YTO → 圆通", bq.guess_shipper_code("yto88888") == "YTO")  # 大小写不敏感
    check("YT → 圆通", bq.guess_shipper_code("YT88888888") == "YTO")
    check("JT → 极兔", bq.guess_shipper_code("JT99999999") == "ZJS")
    check("更长前缀优先", bq.guess_shipper_code("ZTOEXPRESS001") == "ZTO")
    check("纯数字单号不误判", bq.guess_shipper_code("75012345678901") == "")
    check("空值不报错", bq.guess_shipper_code("") == "")

    # 必填 Tel 且缺 Tel → 命中预警
    items = [("SF123", ""), ("ZTO456", ""), ("JD999", ""), ("EMS001", "0000")]
    missing = bq.find_missing_tel(items)
    check("缺 Tel 命中 2 个", len(missing) == 2, str(missing))
    check("单号与编码正确", set(missing) == {("SF123", "SF"), ("ZTO456", "ZTO")}, str(missing))

    # 已提供 Tel 的不重复报警
    check("已补 Tel 不报警", bq.find_missing_tel([("SF123", "9378")]) == [])

    # 预警文案含公司名与补法提示
    warn = bq.warn_missing_tel(items)
    check("预警文案含单号", "SF123" in warn and "ZTO456" in warn)
    check("预警文案含公司名", "顺丰速运" in warn and "中通快递" in warn)
    check("预警文案给出补法", "--tel" in warn)
    check("无缺失时不产出文案", bq.warn_missing_tel([("SF123", "9378")]) == "")


# --------------------------------------------------------------------------- #
# 4c. 输入文件不存在 → 友好报错，不抛栈回溯
# --------------------------------------------------------------------------- #
def test_cli_file_not_found():
    print("[4c] CLI 读取不存在文件时退出码为 2")
    import contextlib
    import batch_query as bq_cli

    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        rc = bq_cli._cli(["--platform-id", "x", "--api-key", "y",
                          "--file", os.path.join(tempfile.gettempdir(), "xdcc_不存在的文件.txt")])
    text = err.getvalue()
    check("退出码 == 2", rc == 2, f"rc={rc}")
    check("输出中文错误提示", "读取输入失败" in text, text[:120])
    check("未出现栈回溯", "Traceback" not in text, text[:120])


# --------------------------------------------------------------------------- #
# 5. 聚合统计
# --------------------------------------------------------------------------- #
def _fake_result(no, ok, state_desc="已签收", timeout=False, span=100.0):
    summary = {}
    if ok:
        summary = {
            "shipper": "中通快递", "state_label": bq.classify_state(state_desc),
            "state_desc": state_desc,             "timeouts": [{"field": "x"}] if timeout else [],
            "spans": [{"field": "SignFor_TimeSpan", "label": "揽收→签收", "minutes": span, "human": ""}],
        }
    return {"no": no, "tel": "", "ok": ok, "code": 200 if ok else 400,
            "message": "" if ok else "失败", "response": {}, "summary": summary}


def test_aggregate():
    print("[5] 聚合统计 build_aggregate")
    results = [
        _fake_result("N1", True, "已签收", timeout=False, span=100.0),
        _fake_result("N2", True, "已签收", timeout=True, span=200.0),
        _fake_result("N3", True, "派送中", timeout=False, span=50.0),
        _fake_result("N4", False),
    ]
    agg = bq.build_aggregate(results)
    check("总单量=4", agg["total"] == 4)
    check("成功=3", agg["success"] == 3)
    check("失败=1", agg["failed"] == 1)
    check("已签收=2", agg["signed"] == 2)
    check("超时单量=1", agg["timeout_count"] == 1)
    check("平均签收时效=150", abs(agg["avg_signfor_minutes"] - 150.0) < 1e-6, str(agg["avg_signfor_minutes"]))
    check("失败列表含N4", any(f["no"] == "N4" for f in agg["failed_list"]))


# --------------------------------------------------------------------------- #
# 6. 导出写入（csv/json/txt）
# --------------------------------------------------------------------------- #
def test_exports():
    print("[6] 多格式导出写入")
    d = tempfile.mkdtemp(prefix="xdcc_selftest_")
    results = [_fake_result("N1", True, "已签收", span=100.0), _fake_result("N2", False)]
    agg = bq.build_aggregate(results)
    base = os.path.join(d, "out")

    bq.write_json(base + ".json", results, agg)
    bq.write_csv(base + ".csv", results)
    bq.write_report_txt(base + ".report.txt", results, agg)

    check("JSON 生成", os.path.exists(base + ".json"))
    check("CSV 生成", os.path.exists(base + ".csv"))
    check("TXT 生成", os.path.exists(base + ".report.txt"))

    # CSV 表头与行数
    import csv
    with open(base + ".csv", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    check("CSV 行数=2", len(rows) == 2, str(len(rows)))
    check("CSV 含表头 No", "No" in rows[0], str(list(rows[0].keys())))

    # JSON 可解析
    with open(base + ".json", encoding="utf-8") as f:
        j = __import__("json").load(f)
    check("JSON 含 aggregate", "aggregate" in j and "results" in j)


# --------------------------------------------------------------------------- #
# 7. 并发查询（monkeypatch 网络，验证数量/序号一致）
# --------------------------------------------------------------------------- #
def test_concurrency():
    print("[7] 并发查询（mock 网络）")
    import collections
    calls = collections.Counter()

    def fake_query(platform_id, api_key, member_id, no, tel="", timeout=8):
        calls[no] += 1
        return {"Code": 200, "Message": "成功", "Data": {
            "ExpressName": "中通", "StateDesc": "已签收", "State": 3,
            "SignFor_TimeSpan": 10.0, "TraceList": [], "LogisticCode": no,
        }}

    orig = bq.query_track
    bq.query_track = fake_query
    try:
        items = [(f"NO{i}", "") for i in range(12)]
        res = bq.batch_query("pid", "key", "mid", items, concurrency=4, progress=False)
    finally:
        bq.query_track = orig

    check("返回数量=12", len(res) == 12, str(len(res)))
    check("每个单号恰好调用1次", all(calls[n] == 1 for n, _ in items))
    check("顺序与输入一致", [r["no"] for r in res] == [n for n, _ in items])
    check("全部 ok", all(r["ok"] for r in res))


# --------------------------------------------------------------------------- #
# 8. common.py：凭据映射（实测结论 MemberID == UserID）
# --------------------------------------------------------------------------- #
def test_common_mapping():
    print("[8] common.map_apikey_to_creds 凭据映射")
    import common
    data = {"PlatformID": "100", "UserID": "200", "UserApiKey": "00000000000000000000000000000000"}
    creds = common.map_apikey_to_creds(data)
    check("PLATFORM_ID 映射", creds["XDCC_PLATFORM_ID"] == "100", str(creds))
    check("MEMBER_ID == UserID（实测确认）", creds["XDCC_MEMBER_ID"] == "200", str(creds))
    check("API_KEY 映射", creds["XDCC_API_KEY"] == "00000000000000000000000000000000", str(creds))

    # 大小写兼容
    data2 = {"platformId": "700", "userID": "800", "apiKey": "abc"}
    creds2 = common.map_apikey_to_creds(data2)
    check("小写字段兼容", creds2["XDCC_PLATFORM_ID"] == "700" and creds2["XDCC_MEMBER_ID"] == "800")


# --------------------------------------------------------------------------- #
# 9. common.py：凭据读写 + 客服提示
# --------------------------------------------------------------------------- #
def test_common_creds_io():
    print("[9] common 凭据读写 + 兜底提示")
    import common
    d = tempfile.mkdtemp(prefix="xdcc_selftest_")
    path = os.path.join(d, "creds.env")
    creds = {"XDCC_PLATFORM_ID": "100", "XDCC_MEMBER_ID": "200",
             "XDCC_API_KEY": "00000000000000000000000000000000"}
    common.write_creds(path, creds, token="eyJ.abc.token", extra_comment="示例凭据")
    loaded = common.load_creds(path)
    check("写后读 PLATFORM_ID", loaded.get("XDCC_PLATFORM_ID") == "100", str(loaded))
    check("写后读 MEMBER_ID", loaded.get("XDCC_MEMBER_ID") == "200")
    check("写后读 API_KEY", loaded.get("XDCC_API_KEY") == "00000000000000000000000000000000")
    check("USER_TOKEN 已写入", loaded.get("XDCC_USER_TOKEN") == "eyJ.abc.token")

    # 兜底提示落在会话内，且不含任何外部联系方式
    hint = common.cs_hint("测试原因")
    check("兜底提示含原因", "测试原因" in hint)
    check("兜底提示含自助排查第 1 步", "--validate-only" in hint or "校验" in hint, hint)
    check("兜底提示不含第三方账号", "xdcc" + "vip" not in hint)
    check("兜底提示不含电子邮箱", "@" not in hint)
    check("兜底提示不含外部站点链接", "http" not in hint.lower())


# --------------------------------------------------------------------------- #
# 10. onboard._validate 凭据校验逻辑（mock 网络）
# --------------------------------------------------------------------------- #
def test_onboard_validate():
    print("[10] onboard._validate 校验逻辑（mock 网络）")
    import common
    import onboard
    import batch_query as bq

    def fake_ok(pid, key, mid, no, tel="", timeout=8):
        return {"Code": 200, "Message": "成功", "Data": {"ExpressName": "中通"}}
    def fake_500(pid, key, mid, no, tel="", timeout=8):
        return {"Code": 500, "Message": "PlatformID错误", "Data": None}

    creds = {"XDCC_PLATFORM_ID": "100", "XDCC_MEMBER_ID": "200", "XDCC_API_KEY": "k"}

    orig = bq.query_track
    bq.query_track = fake_ok
    try:
        ok, msg = onboard._validate(creds)
    finally:
        bq.query_track = orig
    check("Code=200 → 校验通过", ok is True and "200" in msg, msg)

    bq.query_track = fake_500
    try:
        ok2, msg2 = onboard._validate(creds)
    finally:
        bq.query_track = orig
    check("Code=500 → 校验未通过", ok2 is False and "500" in msg2, msg2)


# --------------------------------------------------------------------------- #
# 11. common.validate_track_creds（guided_register 与 onboard 共用一份实现）
# --------------------------------------------------------------------------- #
def test_common_validate_shared():
    print("[11] common.validate_track_creds 共用实现")
    import common
    import batch_query as bq

    calls = {}

    def fake(pid, key, mid, no, tel="", timeout=8):
        calls["no"] = no
        return {"Code": 200, "Message": "成功", "Data": {}}

    orig = bq.query_track
    bq.query_track = fake
    try:
        ok, msg = common.validate_track_creds(
            {"XDCC_PLATFORM_ID": "1", "XDCC_API_KEY": "k", "XDCC_MEMBER_ID": "2"})
    finally:
        bq.query_track = orig

    check("校验通过", ok is True, msg)
    check("使用默认测试单号", calls.get("no") == common.DEFAULT_TEST_NO, str(calls))


# --------------------------------------------------------------------------- #
# 12. guided_register 缺 Playwright 时应返回错误码，而不是在导入期裸退出
# --------------------------------------------------------------------------- #
def test_register_no_hard_exit():
    print("[12] guided_register 缺依赖时不 SystemExit")
    try:
        import guided_register as gr
    except BaseException as e:  # noqa: BLE001
        check("导入不再中断进程", False, f"抛出 {type(e).__name__}: {e}")
        return
    check("导入不再中断进程", True)

    if gr.sync_playwright is None:
        rc = gr.run("register", "13800000000", "pwd", False, 5,
                    os.path.join(tempfile.gettempdir(), "xdcc_selftest.env"), None, True)
        check("缺依赖时 run 返回 2", rc == 2, f"rc={rc}")
    else:
        print("  · 本机已装 Playwright，跳过运行期降级断言")

    src = open(os.path.join(SCRIPT_DIR, "guided_register.py"), encoding="utf-8").read()
    check("不再硬编码他人用户目录", "86158" not in src)
    check("探测候选包含 PATH 查找", 'shutil.which("chrome")' in src)


# --------------------------------------------------------------------------- #
# 13. 发布合规：技能包零外部联系渠道
#
# 审核红线：包内不得出现第三方推广、外部联系渠道（即时通讯账号 / 邮箱 /
# 电话 / 外部站点地址）、以及第三方页面上的满幅置顶品牌条。
# 这里做静态扫描，任何一条被写回都会让自检失败。
# --------------------------------------------------------------------------- #
# 注意：下面的禁用词一律以「打散写法」放进正则（字符类 / unicode 转义），
# 本文件里不会出现任何可被引用的完整违规串——否则规则本身就会命中自己，
# 也会在外部全文扫描时把这份测试代码误判成违规内容。
BANNED_PATTERNS = [
    (r"xdccv[i]p|xdcc5205[0-9]{2}", "第三方即时通讯账号"),
    (r"[\w.\-]+@[\w.\-]+\.\w+", "电子邮箱地址"),
    (r"https?://(www\.)?xdccy\.com", "外部站点首页地址"),
    (r"微\u4fe1号|公\u4f17号|加\s?微|扫[\u7801]", "外部推广话术"),
    (r"二\u7ef4\u7801", "二" + "维码"),
    (r"水\u5370|通[栏栏]|品牌色渐变", "页面满幅置顶条样式"),
]
# 白名单主机（属功能调用，非推广）：API 基址与注册/登录页由代码必需
_ALLOWED_HOSTS = ("api.xdccy.com", "xdccy.com")


PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico")
_SKIP_DIRS = {".git", "__pycache__", ".workbuddy", "node_modules", ".venv"}
_SELF = os.path.basename(__file__)  # 扫描规则自身除外，避免规则命中自己


def _walk_project():
    for dirpath, dirnames, filenames in os.walk(PROJECT_DIR):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
        for fn in filenames:
            if fn == _SELF or fn.endswith(".pyc"):
                continue
            yield os.path.join(dirpath, fn)


def test_no_offsite_promotion():
    print("[13] 技能包零外部联系渠道扫描")
    import re

    hits, scanned = [], 0
    for fp in _walk_project():
        ext = os.path.splitext(fp)[1].lower()
        try:
            text = open(fp, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            if ext in IMG_EXT:
                hits.append(f"{os.path.basename(fp)}（图片资源）")
            continue
        scanned += 1
        for pat, label in BANNED_PATTERNS:
            for m in re.finditer(pat, text, re.I):
                if pat == r"https?://(www\.)?xdccy\.com" and \
                        any(m.group(0).split("://", 1)[-1].startswith(a)
                            for a in _ALLOWED_HOSTS):
                    continue  # API 基址/注册页白名单：属功能调用，非推广
                ctx = text[max(0, m.start() - 32):m.end() + 32].replace("\n", " ")
                hits.append(f"{label}｜{os.path.basename(fp)}｜{m.group(0)}｜…{ctx}…")

    check("包内无图片资源与外部联系渠道内容写入", not hits,
          "\n      · " + "\n      · ".join(hits))
    check(f"已完成 {scanned} 个文本文件扫描", scanned >= 6, f"仅扫描 {scanned} 个文件")


# --------------------------------------------------------------------------- #
# 运行
# --------------------------------------------------------------------------- #
def main() -> int:
    print("=" * 52)
    print("xdcc-batch-query selftest")
    print("=" * 52)
    test_signatures()
    test_summarize()
    test_classify()
    test_parse_input()
    test_missing_tel()
    test_cli_file_not_found()
    test_aggregate()
    test_exports()
    test_concurrency()
    test_common_mapping()
    test_common_creds_io()
    test_onboard_validate()
    test_common_validate_shared()
    test_register_no_hard_exit()
    test_no_offsite_promotion()
    print("=" * 52)
    print(f"通过 {PASS} / 失败 {FAIL}")
    print("=" * 52)
    _cleanup_tmpdirs()
    return 0 if FAIL == 0 else 1


def _cleanup_tmpdirs() -> None:
    """清理各用例留下的临时目录，避免长期堆积。"""
    base = tempfile.gettempdir()
    try:
        names = os.listdir(base)
    except OSError:
        return
    for name in names:
        if name.startswith("xdcc_selftest_"):
            shutil.rmtree(os.path.join(base, name), ignore_errors=True)


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    sys.exit(main())
