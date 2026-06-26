"""脑补陷阱共享 helper（v1.7.2 引入）。

设计意图
========
把「脚本名拼错」从 OS-level `No such file or directory`（非结构化、模型读不懂）
**升级为带 `intended_script` 的结构化 JSON 错误**，模型读到 `next_action`
后立即就能改正脚本名重试，不必再去翻 SKILL.md。

为什么用 stub 文件而不是 wrapper 入口
======================================
- wrapper 方案（如 `m.py order_modify`）会改变速抄表的命令形式，模型可能照样脑补
- stub 方案：直接为最常被脑补的 13 个错名各放一个 3 行的"陷阱脚本"
  跑了立刻吐结构化指引，**不依赖模型读 SKILL.md**，治本

为什么不 import _client
=======================
保持极轻量启动（< 50ms）。`_client.py` 顶层 import urllib3 / fsopenapi 这些重模块，
trap 触发时不需要这些依赖。
"""
import json
import sys


def wrong_name(intended: str, action_zh: str) -> None:
    """脚本名拼错时的统一出口：输出结构化 JSON 并退出码 2。

    Args:
        intended: 真实应该用的脚本名（含 `.py`，如 `"order_modify.py"`）。
        action_zh: 用户原话对应的中文动作（如 `"改单"`），用于 message 友好化。
    """
    wrong = sys.argv[0].rsplit("/", 1)[-1]
    payload = {
        "ok": False,
        "error_code": "WRONG_SCRIPT_NAME",
        "message": (
            f"脚本名拼错了：本 skill 没有 `{wrong}` 这个脚本，"
            f"{action_zh}的正确脚本是 `{intended}`。"
        ),
        "hint": (
            "本 skill 18 个业务脚本统一命名规则是 `<domain>_<action>.py`"
            "（如 `order_modify.py` / `order_cancel.py` / `order_create.py`），"
            "唯一历史例外是 `sync_accounts.py`。"
            "模型常见的英语动宾倒置（modify_order / cancel_order 等）以及简写（modify / buy 等）"
            "都被 `code/` 目录下的 trap stub 接住，避免落到 OS-level 的 `No such file` 错误。"
        ),
        "next_action": (
            f"把命令里的 `{wrong}` 改成 `{intended}` 重试；其它参数（含 `--confirm`）保持不变。"
            "完整脚本名清单见 SKILL.md「合法脚本清单」。**禁止再猜其它脚本名**——正确答案就是 "
            f"`{intended}`。"
        ),
        "intended_script": intended,
        "wrong_script": wrong,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(2)
