#!/usr/bin/env python3
"""
1688-shop-health-check —— 店铺健康分析工具集 CLI 统一入口

Usage:
    python3 cli.py <command> [options]

Commands（命令自动发现，更多参数见项目根目录 SKILL.md 与 references/cli-commands.md）:
    get_bindlist                       获取多店铺绑定关系列表
    alibaba.1688.seller.trade.code.index            店铺交易核心指标（总盘）
    alibaba.1688.seller.import.abnormal.offer       异常商品（风险定位）
    alibaba.1688.seller.top.offer                   优秀商品榜单（多榜单）
    alibaba.1688.seller.activity.registered.info    近 30 天活动参与及效果
    alibaba.1688.seller.customer.business.province  客户地域分布
    alibaba.1688.seller.customer.detail             头部老客户明细
    alibaba.1688.get.traffic.trend                  逐日流量趋势数据
    alibaba.1688.get.traffic.overview               全店流量概览（PV/UV/UVCTR + 多期对比）
    alibaba.1688.get.channel.traffic                各渠道流量及多期对比
    alibaba.1688.get.search.channel.detail          搜索渠道深度下钻
    alibaba.1688.get.recommend.channel.detail       推荐渠道深度下钻
    alibaba.1688.get.ad.channel.detail              广告渠道深度下钻
    alibaba.1688.get.core.metrics                   店铺核心指标同行对比及趋势
    alibaba.1688.get.product.status                商品状态检查（搜索降权/下架等）
    alibaba.1688.get.industry.benchmark             行业大盘对比
    shop_health_check                  店铺健康检查（订单履约/合规扣分/买家评价）
    configure                          配置 AK

输出 JSON：{"success": bool, "markdown": str, "data": {...}}
"""

import json
import os
import sys
import importlib

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPTS_DIR)

def _discover_capabilities() -> dict:
    """扫描 capabilities/*/cmd.py，自动注册命令"""
    commands = {}
    caps_dir = os.path.join(SCRIPTS_DIR, "capabilities")

    if not os.path.isdir(caps_dir):
        return commands

    for name in sorted(os.listdir(caps_dir)):
        cmd_path = os.path.join(caps_dir, name, "cmd.py")
        if not os.path.isfile(cmd_path):
            continue
        module_path = f"capabilities.{name}.cmd"
        try:
            mod = importlib.import_module(module_path)
            cmd_name = getattr(mod, 'COMMAND_NAME', name)
            commands[cmd_name] = module_path
        except Exception:
            pass

    return commands

def _usage(commands: dict):
    lines = ["**1688-shop-health-check 用法**\n", "```"]
    for name in sorted(commands):
        try:
            mod = importlib.import_module(commands[name])
            desc = getattr(mod, 'COMMAND_DESC', '')
            lines.append(f"python3 cli.py {name:<36} {desc}")
        except Exception:
            lines.append(f"python3 cli.py {name}")
    lines.append("```")

    print(json.dumps({
        "success": False,
        "data": {},
        "markdown": "\n".join(lines),
    }, ensure_ascii=False, indent=2))

def main():
    commands = _discover_capabilities()

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        _usage(commands)
        sys.exit(1)

    cmd = sys.argv[1]
    module_path = commands[cmd]

    sys.argv = [f"cli.py {cmd}"] + sys.argv[2:]

    module = importlib.import_module(module_path)
    module.main()

    # 每次命令执行后上报埋点，失败不影响主流程
    try:
        from _tracker import report_skill_usage
        report_skill_usage()
    except Exception:
        pass

if __name__ == "__main__":
    main()
