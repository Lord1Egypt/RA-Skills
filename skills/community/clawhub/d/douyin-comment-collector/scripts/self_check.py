# -*- coding: utf-8 -*-
"""抖音评论采集 · 一键环境自检脚本。

装完技能后先跑它，30 秒内确认环境是否就绪，并定位「跑不起来」的根因：
  - 必装层（缺了直接报错，exit!=0）：Python 版本、httpx、签名子包、SM3 已知答案、a_bogus 确定性
  - 可选层（缺了只告警，不阻断）：jieba（词频）、playwright+chromium（浏览器免登录）

用法：
  cd <skill>/scripts
  python self_check.py

退出码：0 = 必装全过（可选层可缺）；1 = 必装层有失败。
不联网：所有逻辑层检查均为离线自测，无需 cookie / 抖音可达。
"""

import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# 退出码与状态标记
EXIT_OK = 0
EXIT_FAIL = 1
OK = "✅"
WARN = "⚠️ "
FAIL = "❌"

results = []  # (level, mark, name, detail)


def record(required, mark, name, detail=""):
    """required=True 表示必装层：FAIL 会拉高 exit code。"""
    results.append((required, mark, name, detail))


def py_version_ok():
    v = sys.version_info
    ok = (v.major, v.minor) >= (3, 8)
    detail = f"{v.major}.{v.minor}.{v.micro}" + ("" if ok else "（需 >= 3.8）")
    return ok, detail


def httpx_ok():
    try:
        import httpx  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        return False, f"未安装：{exc}"
    ver = getattr(httpx, "__version__", "?")
    return True, f"httpx {ver}"


def sign_pkg_ok():
    try:
        from sign import ABogusPureSigner  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        return False, f"签名子包导入失败：{exc}"
    return True, "ABogusPureSigner 可导入"


def sm3_known_vectors():
    """离线对照 NIST 发布的 SM3 已知答案，验证国密实现正确。"""
    try:
        from sign.sm3 import sm3_hex
    except Exception as exc:  # noqa: BLE001
        return False, f"sm3 模块导入失败：{exc}"
    v1 = sm3_hex(b"abc")
    e1 = "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"
    v2 = sm3_hex(b"abcd" * 16)
    e2 = "debe9ff92275b8a138604889c18e5a4d6fdb70e5387e5765293dcba39c0c5732"
    if v1 == e1 and v2 == e2:
        return True, "SM3('abc') / SM3('abcd'*16) 均匹配 NIST 向量"
    return False, f"向量不匹配：case1={'PASS' if v1==e1 else 'FAIL'} case2={'PASS' if v2==e2 else 'FAIL'}"


def abogus_deterministic():
    """fixed=True 时签名必须确定性（同输入同输出），且长度合理。"""
    try:
        from sign import ABogusPureSigner
    except Exception as exc:  # noqa: BLE001
        return False, f"ABogusPureSigner 导入失败：{exc}"
    try:
        s = ABogusPureSigner(fixed=True, aid=2906)
        q = "aid=2906&aweme_id=7301234567890123456&cursor=0&count=20"
        a = s.sign_query(q)
        b = s.sign_query(q)
    except Exception as exc:  # noqa: BLE001
        return False, f"签名抛错：{exc}"
    if a != b:
        return False, "fixed 模式签名不确定（同输入产出不同结果）"
    if not isinstance(a, str) or len(a) < 50:
        return False, f"签名长度异常：{len(a) if isinstance(a,str) else type(a)}"
    return True, f"确定性签名 OK（长度 {len(a)}）"


def resolve_numeric_ok():
    """离线测 aweme_id 解析的数字路径（无需联网）。"""
    try:
        from fetch_comments import resolve_aweme_id
    except Exception as exc:  # noqa: BLE001
        return False, f"fetch_comments 导入失败：{exc}"
    try:
        got = resolve_aweme_id("7301234567890123456")
    except Exception as exc:  # noqa: BLE001
        return False, f"数字 id 解析抛错：{exc}"
    if got != "7301234567890123456":
        return False, f"数字 id 解析错误：{got!r}"
    return True, "纯数字 aweme_id 解析 OK（完整 URL/短链解析需联网，见下方说明）"


def jieba_ok():
    try:
        import jieba  # noqa: F401
    except Exception:  # noqa: BLE001
        return False, "未安装（--analyze 词频分析需要；pip install jieba）"
    return True, f"jieba {getattr(jieba, '__version__', '')}"


def playwright_ok():
    try:
        from playwright.sync_api import sync_playwright
    except Exception:  # noqa: BLE001
        return False, "未安装（--browser 免登录需要；pip install playwright && playwright install chromium）"
    # 仅查 chromium 二进制是否已下载，不真正启动浏览器
    try:
        with sync_playwright() as p:
            exe = p.chromium.executable_path
    except Exception as exc:  # noqa: BLE001
        return False, f"playwright 驱动启动失败：{exc}"
    if not exe or not os.path.exists(exe):
        return False, "playwright 已装，但 chromium 浏览器未下载（运行：playwright install chromium）"
    return True, f"chromium 就绪：{os.path.basename(exe)}"


def fetch_posts_ok():
    """主页作品抓取脚本：确认 fetch_posts.py 存在且（playwright 就绪时）可导入。"""
    path = os.path.join(_HERE, "fetch_posts.py")
    if not os.path.exists(path):
        return False, "fetch_posts.py 缺失（主页作品抓取不可用）"
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        import fetch_posts  # noqa: F401
        return True, "fetch_posts.py 可导入（主页作品抓取就绪）"
    except Exception:
        return False, "脚本已存在；需 playwright 才能运行（pip install playwright && playwright install chromium）"


def douyin_entry_ok():
    """统一入口 douyin.py：确认存在且可导入（仅路由，无重依赖，可安全 import）。"""
    path = os.path.join(_HERE, "douyin.py")
    if not os.path.exists(path):
        return False, "douyin.py 缺失（统一入口不可用）"
    try:
        import douyin  # noqa: F401
        return True, "douyin.py 统一入口就绪"
    except Exception as exc:  # noqa: BLE001
        return False, f"douyin.py 导入失败：{exc}"


def main() -> int:
    print("=" * 60)
    print("抖音评论采集 · 主页作品抓取 · 环境自检")
    print("=" * 60)

    # ---- 必装层 ----
    pv_ok, pv_detail = py_version_ok()
    record(True, OK if pv_ok else FAIL, "Python 版本", pv_detail)

    hx_ok, hx_detail = httpx_ok()
    record(True, OK if hx_ok else FAIL, "httpx（必装）", hx_detail)

    sg_ok, sg_detail = sign_pkg_ok()
    record(True, OK if sg_ok else FAIL, "签名子包（必装）", sg_detail)

    sm_ok, sm_detail = sm3_known_vectors()
    record(True, OK if sm_ok else FAIL, "SM3 国密实现", sm_detail)

    ab_ok, ab_detail = abogus_deterministic()
    record(True, OK if ab_ok else FAIL, "a_bogus 确定性", ab_detail)

    rn_ok, rn_detail = resolve_numeric_ok()
    record(True, OK if rn_ok else FAIL, "aweme_id 解析", rn_detail)

    # ---- 可选层 ----
    jb_ok, jb_detail = jieba_ok()
    record(False, OK if jb_ok else WARN, "jieba（词频·可选）", jb_detail)

    pw_ok, pw_detail = playwright_ok()
    record(False, OK if pw_ok else WARN, "playwright+chromium（浏览器免登录·可选）", pw_detail)

    fp_ok, fp_detail = fetch_posts_ok()
    record(False, OK if fp_ok else WARN, "fetch_posts（主页作品抓取·可选）", fp_detail)

    de_ok, de_detail = douyin_entry_ok()
    record(False, OK if de_ok else WARN, "douyin.py（统一入口·可选）", de_detail)

    # ---- 汇总 ----
    print()
    print("检查项".ljust(34), "状态", "说明")
    print("-" * 60)
    required_fail = False
    for required, mark, name, detail in results:
        print(f"{name}".ljust(34), mark, detail or "")
        if required and mark == FAIL:
            required_fail = True

    print("-" * 60)
    if required_fail:
        print(f"{FAIL} 必装层未通过：HTTP 评论抓取不可用，请先修必装项（见上方 FAIL）。")
        suggest = (
            "  修复：pip install -r <skill>/scripts/requirements.txt\n"
            "  若仍 FAIL，多半是走了错误的 python：用 `which python` 确认 pip 与运行脚本的是同一个解释器。"
        )
        print(suggest)
        code = EXIT_FAIL
    else:
        print(f"{OK} 必装层全部通过：核心 HTTP 抓取链路可用。")
        miss_opt = [n for r, m, n, _ in results if not r and m == WARN]
        if miss_opt:
            print(f"{WARN} 可选能力缺失（不影响核心）：" + "、".join(miss_opt))
            print("  浏览器免登录：pip install playwright && playwright install chromium")
            print("  词频分析：pip install jieba")
        else:
            print(f"{OK} 全部能力就绪（含浏览器免登录 + 词频分析）。")
        code = EXIT_OK

    print()
    print("下一步：")
    print("  免登录浏览器：python fetch_comments.py \"<链接>\" --browser --output c.json")
    print("  有 cookie 全量：python fetch_comments.py \"<链接>\" --cookie \"$DOUYIN_COOKIE\"")
    print("  主页作品抓取：python fetch_posts.py \"<主页链接或sec_uid>\" --since 2026-09-01 --until 2026-09-18 --analyze")
    print("  统一入口：python douyin.py comments \"<视频链接>\" / python douyin.py posts \"<主页链接>\"")
    print("  注：短链/完整 URL 的 aweme_id 解析需要联网，本自检不连网，不覆盖该项。")
    return code


if __name__ == "__main__":
    sys.exit(main())
