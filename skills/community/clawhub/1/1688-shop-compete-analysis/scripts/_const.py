#!/usr/bin/env python3
"""
1688-shop-compete-analysis 全局常量
"""

# Skill 版本
SKILL_VERSION = "0.1.0"

# ── MCP 工具名（经 accio-mcp-cli 调用，替代旧的网关 REST 路径）──────────────
# 工具名为 MCP 实际注册名，无统一前缀规则，必须按实际注册名写死，不可凭约定推断。
# 鉴权与商家身份由本地网关登录态注入，调用时无需 AK / userId。

# 商家经营数据取数（对应旧 /api/1688_query_shop_data/1.0.0）
# 入参：{"dataSource": <SYCM|ITEM|...>, "apiPath": <接口路径>, "params": {...}}
# 竞争域接口均为 dataSource=SYCM（compete/*），买家流失为 dataSource=ITEM（/item/customerLoss）
TOOL_QUERY_SHOP_DATA = "1688_query_shop_data"
