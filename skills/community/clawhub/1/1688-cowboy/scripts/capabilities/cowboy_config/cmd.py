#!/usr/bin/env python3
"""牛仔配置 CLI 入口 -- 创建/更新/暂停/恢复/加载牛仔

子命令：
    create  创建牛仔（初始化卖家 AI 客服，必传 --levels）
    update  更新牛仔配置（仅更新买家等级，必传 --levels）
    pause   暂停牛仔接待
    resume  恢复牛仔接待
    load    加载牛仔配置（查询状态 + 允许接待的买家等级）
"""

COMMAND_NAME = "cowboy_config"
COMMAND_DESC = "牛仔配置（创建/更新/暂停/恢复/加载）"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from _risk_guard import emit_confirmation, get_confirmed_payload

from capabilities.cowboy_config.service import (
    create_cowboy,
    update_cowboy,
    pause_cowboy,
    resume_cowboy,
    load_cowboy_config,
)

# 需要 --levels 入参的子命令
LEVEL_REQUIRED_ACTIONS = {"create", "update"}

# 写入 / 状态变更类子命令：必须走 BashRiskCheckHook 二次确认，防止 AI 跳过 SKILL.md 软约束直接调起。
# ⚠️ 特别说明：create **不在本集合中**。原因：
#   1) Step 4「确认模拟效果」点击本身即商家显式确认，再弹一次会导致招聘体验出现重复确认；
#   2) 同商家仅能 create 一次（网关硬约束），影响面可控；
#   3) 后续任何修改都走 update，仍受二次确认保护。
WRITE_ACTIONS = {"update", "pause", "resume"}

ACTION_MAP = {
    "create": create_cowboy,
    "update": update_cowboy,
    "pause": pause_cowboy,
    "resume": resume_cowboy,
    "load": load_cowboy_config,
}

ACTION_DESC = {
    "create": "创建牛仔（初始化卖家 AI 客服）",
    "update": "更新牛仔配置（仅买家等级）",
    "pause": "暂停牛仔接待",
    "resume": "恢复牛仔接待",
    "load": "加载牛仔配置",
}


def _parse_levels(raw: str):
    """把 `L0,L1,L2` 拆成 list；service 层会再做去重 / 合法性检查。"""
    if raw is None:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="牛仔配置（创建/更新/暂停/恢复/加载）",
        allow_abbrev=False,  # 禁止前缀缩写匹配（避免 --level 被静默当成 --levels）
    )
    parser.add_argument("action", choices=ACTION_MAP.keys(),
                        help="操作类型：create | update | pause | resume | load")
    parser.add_argument("--levels", default=None,
                        help="买家等级列表，逗号分隔（例：L0,L1,L2）；create / update 必传")
    args = parser.parse_args()

    try:
        # 写入类动作：强制走 BashRiskCheckHook 二次确认。
        # Phase 1（首次调用）：校验参数 + emit_confirmation，让端侧弹窗；不调用后端 API。
        # Phase 2（商家点击确认后）：仅从 NEWTON_CONFIRM_PAYLOAD 读权威参数后照常执行。
        if args.action in WRITE_ACTIONS:
            payload = get_confirmed_payload()
            if payload is None:
                if args.action in LEVEL_REQUIRED_ACTIONS:
                    levels = _parse_levels(args.levels)
                    if not levels:
                        print_output(False,
                                     "`{}` 必须传 --levels，例：--levels L0,L1,L2".format(args.action),
                                     {})
                        return
                    msg = "即将{}（买家等级：{}），是否确认执行？".format(
                        ACTION_DESC[args.action], ",".join(levels))
                    emit_confirmation(
                        message=msg,
                        payload={"action": args.action, "levels": levels},
                        preview_markdown="待商家确认：{}".format(msg),
                    )
                else:
                    msg = "即将{}，是否确认执行？".format(ACTION_DESC[args.action])
                    emit_confirmation(
                        message=msg,
                        payload={"action": args.action},
                        preview_markdown="待商家确认：{}".format(msg),
                    )
                return

            # Phase 2：只信任 payload。严示 action 不一致（防 hook 路由错位）。
            confirmed_action = payload.get("action")
            if confirmed_action != args.action:
                print_output(False,
                             "二次确认参数不一致（payload.action={} / argv.action={}），拒绝执行".format(
                                 confirmed_action, args.action),
                             {})
                return

            fn = ACTION_MAP[args.action]
            if args.action in LEVEL_REQUIRED_ACTIONS:
                confirmed_levels = payload.get("levels") or []
                if not isinstance(confirmed_levels, list) or not confirmed_levels:
                    print_output(False,
                                 "二次确认 payload.levels 缺失或为空，拒绝执行",
                                 {})
                    return
                result = fn(confirmed_levels)
            else:
                result = fn()
            print_output(True, result["markdown"], result["data"])
            return

        # create：Step 4 商家点击「确认模拟效果」即视为显式确认，自动正式上岗，不再额外弹窗。
        if args.action == "create":
            levels = _parse_levels(args.levels)
            if not levels:
                print_output(False,
                             "`create` 必须传 --levels，例：--levels L0,L1,L2",
                             {})
                return
            result = create_cowboy(levels)
            print_output(True, result["markdown"], result["data"])
            return

        # 只读动作（load）：保持原有路径，不走二次确认。
        fn = ACTION_MAP[args.action]
        result = fn()
        print_output(True, result["markdown"], result["data"])
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
