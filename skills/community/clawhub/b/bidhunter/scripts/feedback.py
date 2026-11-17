#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BidHunter 零成本反馈模块
=========================

设计约束（硬性，不可违反）
--------------------------
1. 零云成本：不发起任何网络请求，不连自建后端，不需要域名/服务器。
2. 只做三件事：本地格式化反馈 -> 尝试写剪贴板 -> 打开平台评论页。
3. 全部依赖 Python 标准库。剪贴板失败静默降级，绝不抛异常中断。

用法
----
    python3 feedback.py                     # 交互式收集
    python3 feedback.py --platform clawhub  # 指定打开哪个平台
    python3 feedback.py --no-open           # 只生成文本，不开浏览器
    python3 feedback.py --type 2 --detail "规则看不懂"   # 非交互，直接给内容
    python3 feedback.py --selftest          # 内置自检（无需 pytest）

退出码
------
    0  成功
    1  浏览器未能自动打开（文本仍已生成，可手动复制）
"""

import os
import sys
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# 平台地址
# 说明：以下两个 URL 均于 2026-09-08 实测 HTTP 200。
#       不要改成 clawhub.io —— 该域名不通（实测 curl 返回 000）。
# --------------------------------------------------------------------------
PLATFORM_URLS = {
    "skillhub": "https://skillhub.cn/skills/user_7a89592b/bidhunter",
    "clawhub": "https://clawhub.ai/419597334-sudo/bidhunter",
}

FEEDBACK_TYPES = {
    "1": "匹配不准（该中的没中 / 不该中的中了）",
    "2": "规则配置困难（E002）",
    "3": "推送失败",
    "4": "报告问题（看不懂 / 缺信息）",
    "5": "想要新功能",
    "0": "其他",
}

FEEDBACK_TEMPLATE = """【BidHunter 反馈】版本 {version}

1. 反馈类型：{feedback_type}
2. 使用场景：{scenario}
3. 具体问题/建议：
{detail}

---
系统：{platform} / Python {python_version}
生成时间：{timestamp}
"""


# --------------------------------------------------------------------------
# 版本探测：动态读 SKILL.md frontmatter，避免每版手改硬编码
# --------------------------------------------------------------------------
def detect_version(default="unknown"):
    try:
        skill_md = Path(SCRIPT_DIR).parent / "SKILL.md"
        with open(skill_md, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.lower().startswith("version:"):
                    return line.split(":", 1)[1].strip().strip('"').strip("'")
                if line == "---" and "version" not in line:
                    continue
    except Exception:
        pass
    return default


# --------------------------------------------------------------------------
# 反馈收集
# --------------------------------------------------------------------------
class FeedbackSession:
    """交互式反馈收集；非交互环境自动降级为模板，不报错退出。"""

    def __init__(self, version=None, interactive=None):
        self.version = version or detect_version()
        self.interactive = interactive if interactive is not None else sys.stdin.isatty()
        self._inputs = {
            "type": FEEDBACK_TYPES["0"],
            "scenario": "未填写",
            "detail": "未填写",
        }

    def collect(self):
        if self.interactive:
            self._collect_interactive()
        else:
            self._inputs["scenario"] = "未填写（非交互环境）"
        return self._render()

    def _collect_interactive(self):
        print("BidHunter 快速反馈（直接回车跳过该项）\n")

        print("反馈类型：")
        for k in ["1", "2", "3", "4", "5", "0"]:
            mark = "  ← 最常见" if k == "2" else ""
            print(f"  [{k}] {FEEDBACK_TYPES[k]}{mark}")

        choice = self._ask("\n选数字", default="0").strip()
        self._inputs["type"] = FEEDBACK_TYPES.get(choice, FEEDBACK_TYPES["0"])

        self._inputs["scenario"] = self._ask(
            "\n你在做什么时遇到的？（如：跑第一个标 / 改规则 / 看报告）",
            default="未填写",
        )

        self._inputs["detail"] = self._ask_multiline() or "未填写"

    def _collect_argv(self, type_key=None, scenario=None, detail=None):
        """命令行直填模式（供自动化/脚本调用）"""
        if type_key:
            self._inputs["type"] = FEEDBACK_TYPES.get(str(type_key), FEEDBACK_TYPES["0"])
        if scenario:
            self._inputs["scenario"] = scenario
        if detail:
            self._inputs["detail"] = detail

    def _ask(self, prompt, default=""):
        try:
            v = input(f"{prompt} [默认: {default}]: ").strip()
            return v if v else default
        except (EOFError, KeyboardInterrupt):
            print()
            return default

    def _ask_multiline(self):
        print("\n具体描述（可多行，空行结束）:")
        lines = []
        try:
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
        except (EOFError, KeyboardInterrupt):
            print()
        return "\n".join(lines).strip()

    def _render(self):
        return FEEDBACK_TEMPLATE.format(
            version=self.version,
            feedback_type=self._inputs["type"],
            scenario=self._inputs["scenario"],
            detail=self._inputs["detail"],
            platform=sys.platform,
            python_version="{}.{}.{}".format(*sys.version_info[:3]),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )


# --------------------------------------------------------------------------
# 剪贴板：跨平台，失败静默
# --------------------------------------------------------------------------
def copy_to_clipboard(text):
    """尝试写入系统剪贴板，成功返回 True，任何失败静默返回 False。"""
    try:
        data = text.encode("utf-8")
        if sys.platform == "darwin":
            r = subprocess.run(["pbcopy"], input=data, timeout=5)
            return r.returncode == 0

        if sys.platform == "win32":
            try:
                r = subprocess.run(["clip"], input=text.encode("utf-16-le"), timeout=5)
                if r.returncode == 0:
                    return True
            except Exception:
                pass
            r = subprocess.run(
                ["clip"], input=text.encode("gbk", errors="replace"), timeout=5
            )
            return r.returncode == 0

        if sys.platform.startswith("linux"):
            if os.environ.get("TERMUX_VERSION"):
                r = subprocess.run(["termux-clipboard-set"], input=data, timeout=5)
                return r.returncode == 0
            for cmd in (
                ["wl-copy"],
                ["xclip", "-selection", "clipboard"],
                ["xsel", "--clipboard", "--input"],
            ):
                try:
                    r = subprocess.run(cmd, input=data, timeout=5)
                    if r.returncode == 0:
                        return True
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    continue
    except Exception:
        pass
    return False


def open_feedback_page(platform="skillhub"):
    """打开平台主页（评论区所在页），返回是否成功。"""
    url = PLATFORM_URLS.get(platform, PLATFORM_URLS["skillhub"])
    try:
        return bool(webbrowser.open(url, new=2))
    except Exception:
        return False


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------
def run_feedback(version=None, platform="skillhub", open_browser=True,
                 type_key=None, scenario=None, detail=None, quiet=False):
    session = FeedbackSession(version=version)
    if type_key or scenario or detail:
        session._collect_argv(type_key, scenario, detail)
        report = session._render()
    else:
        report = session.collect()

    if not quiet:
        print("\n" + "=" * 52)
        print("反馈内容已生成", end="")
        print("，已复制到剪贴板" if copy_to_clipboard(report) else "（请手动选中复制）")
        print("=" * 52)
        print(report)
        print("=" * 52)
    else:
        copy_to_clipboard(report)

    if not open_browser:
        print("\n（--no-open：未打开浏览器）")
        for name, url in PLATFORM_URLS.items():
            print(f"  • {name}: {url}")
        return 0

    print(f"\n正在打开 {platform} 页面...")
    if open_feedback_page(platform):
        print("✓ 浏览器已打开，粘贴提交即可。感谢！")
        return 0

    print("⚠ 未能自动打开浏览器（无图形界面环境常见）")
    for name, url in PLATFORM_URLS.items():
        print(f"  • {name}: {url}")
    return 1


# --------------------------------------------------------------------------
# 内置自检（不依赖 pytest，任何环境都能跑）
# --------------------------------------------------------------------------
def selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  {'✓' if cond else '✗'} {name}")
        if not cond:
            ok = False

    print("feedback.py 自检")

    # 1. 模板占位符完整
    try:
        FEEDBACK_TEMPLATE.format(
            version="t", feedback_type="t", scenario="t", detail="t",
            platform="t", python_version="t", timestamp="t",
        )
        check("模板字段完整", True)
    except KeyError as e:
        check(f"模板字段完整（缺 {e}）", False)

    # 2. 非交互降级不崩溃且含版本
    s = FeedbackSession(version="9.9.9", interactive=False)
    out = s.collect()
    check("非交互降级输出含版本", "9.9.9" in out)
    check("非交互降级输出含类型", "反馈类型" in out)

    # 3. 命令行直填模式
    s2 = FeedbackSession(version="1.0.0", interactive=False)
    s2._collect_argv("2", "跑第一个标", "规则看不懂")
    out2 = s2._render()
    check("直填模式 type 生效", "E002" in out2)
    check("直填模式 scenario 生效", "跑第一个标" in out2)
    check("直填模式 detail 生效", "规则看不懂" in out2)

    # 4. 非法类型键回退到「其他」
    s3 = FeedbackSession(version="1.0.0", interactive=False)
    s3._collect_argv("99")
    check("非法类型键回退", "其他" in s3._render())

    # 5. 剪贴板永不崩溃
    check("剪贴板调用不崩溃", isinstance(copy_to_clipboard("测试"), bool))
    check("剪贴板空串不崩溃", isinstance(copy_to_clipboard(""), bool))

    # 6. 平台 URL 正确性（防回归：clawhub 必须是 .ai）
    check("clawhub 域名为 .ai", PLATFORM_URLS["clawhub"].startswith("https://clawhub.ai/"))
    check("skillhub URL 存在", "skillhub.cn" in PLATFORM_URLS["skillhub"])

    # 7. 版本探测
    v = detect_version()
    check(f"版本探测可用（读到 {v}）", v != "unknown")

    print("\n" + ("自检全部通过 ✓" if ok else "存在失败项 ✗"))
    return 0 if ok else 1


def main():
    import argparse
    ap = argparse.ArgumentParser(
        prog="feedback.py",
        description="BidHunter 零成本反馈：本地格式化 + 剪贴板 + 打开平台评论页",
    )
    ap.add_argument("--platform", choices=list(PLATFORM_URLS.keys()),
                    default="skillhub", help="打开哪个平台的反馈页（默认 skillhub）")
    ap.add_argument("--no-open", action="store_true", help="只生成文本，不打开浏览器")
    ap.add_argument("--type", dest="type_key", help="反馈类型编号 0-5（非交互直填）")
    ap.add_argument("--scenario", help="使用场景（非交互直填）")
    ap.add_argument("--detail", help="具体描述（非交互直填）")
    ap.add_argument("--quiet", action="store_true", help="只写剪贴板，不在终端打印")
    ap.add_argument("--selftest", action="store_true", help="运行内置自检后退出")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    return run_feedback(
        platform=args.platform,
        open_browser=not args.no_open,
        type_key=args.type_key,
        scenario=args.scenario,
        detail=args.detail,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    sys.exit(main())
