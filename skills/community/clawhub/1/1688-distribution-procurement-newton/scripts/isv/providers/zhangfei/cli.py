#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分销铺货 CLI：透传中台 yzg Skill；`--token`；stdout JSON。详见 SKILL.md。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import procurement  # noqa: E402


def _configure_utf8_stdio() -> None:
    """强制标准输出为 UTF-8，避免 Windows 终端中文乱码。"""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def _print_json(obj: dict) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _auth_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--token",
        "--jwt-token",
        default=None,
        dest="token",
        metavar="TOKEN",
        help="ISV Token（由 Skill 自动注入）",
    )


def _validate_cli_auth(args: argparse.Namespace) -> dict | None:
    t = (getattr(args, "token", None) or "").strip()
    if t:
        return None
    # SKILL.md §3.1「鉴权失败」锁定句；不向用户暴露 Token / 参数细节
    return {
        "success": False,
        "markdown": "需要先登录一下再试。",
        "data": {},
        "error": "missing_token",
    }


def main() -> None:
    _configure_utf8_stdio()
    parser = argparse.ArgumentParser(
        description=(
            "fx-procurement-9018264 分销铺货 / 采购 CLI。统一入口：python3 cli.py <command> [options]\n"
            "鉴权：所有命令通过 --token 传入 ISV Token。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    """  ------------淘宝开始----------- """
    p_ls = sub.add_parser("list-shops", help="查询当前用户绑定的分销店铺列表")
    _auth_args(p_ls)

    p_ld = sub.add_parser("list-distributors", help="查询某店铺的分销账号列表")
    _auth_args(p_ld)
    p_ld.add_argument("--shop-id", required=True, help="店铺 ID")

    p_lp = sub.add_parser("list-products", help="查询店铺在售商品（itemlink/syn）")
    _auth_args(p_lp)
    p_lp.add_argument(
        "--shop-nick",
        required=True,
        help="店铺 nick 或 ID（仅支持直接传值）",
    )

    p_elt = sub.add_parser("enable-link-type", help="开启分销宝贝开关（可多个宝贝 ID，逗号分隔）")
    _auth_args(p_elt)
    p_elt.add_argument("--item-ids", required=True, help="商品 ID，多个英文逗号隔开")
    p_elt.add_argument("--shop", required=True, help="店铺名称（与下游 shop 一致）")
    p_elt.add_argument("--purchasing-accounts", required=True, help="采购账号列表，多个英文逗号隔开")

    p_eao = sub.add_parser("enable-auto-order", help="保存自动下单配置（透传 POST …/automationOrder）")
    _auth_args(p_eao)
    p_eao.add_argument("--shop-name", required=True, help="店铺名称")
    p_eao.add_argument("--purchase-account", required=True, help="采购账号")

    p_lasa = sub.add_parser("list-after-sale-accounts", help="售后采购账号列表")
    _auth_args(p_lasa)
    p_lasa.add_argument("--shop-id", required=True, help="店铺 ID（仅用于中台解析 sid，与下游 query 无关）")

    p_eaas = sub.add_parser(
        "enable-auto-after-sale",
        help="保存售后规则（POST …/afterSale/setting；可选 --body-file 覆盖默认体）",
    )
    _auth_args(p_eaas)
    p_eaas.add_argument("--shop-id", required=True, help="店铺 ID（用于中台解析 sid）")
    p_eaas.add_argument(
        "--body-file",
        default=None,
        help="可选：JSON 对象文件（UTF-8），与代码内默认售后请求体合并后提交（键覆盖默认值；勿含 loginName）",
    )
    p_eaas.add_argument(
        "--purchase-account",
        required=True,
        help="采购账号，多个英文逗号分隔（与用户对话确认后传入，覆盖 body 内 purchaseAccount）",
    )
    p_eaas.add_argument(
        "--shop-names",
        required=True,
        help="店铺范围，如「全部」或所选店铺名，多个英文逗号分隔（覆盖 body 内 shopNames）",
    )

    p_set = sub.add_parser("settings", help="聚合：绑定店铺 + 可选按 shop-id 查分销账号")
    _auth_args(p_set)
    p_set.add_argument("--shop-id", default=None, help="若提供则额外查询该店的分销账号")

    p_lk = sub.add_parser("link-source", help="分销关系关联（复用 enable-link-type 逻辑）")
    _auth_args(p_lk)
    p_lk.add_argument(
        "--downstream-item-id",
        required=True,
        help="下游商品 ID，多个英文逗号分隔则批量",
    )
    p_lk.add_argument("--source-offer-id", default=None, help="1688 货源 offer（可选，记入 data）")
    p_lk.add_argument("--shop", required=True, help="店铺 nick / 与下游 shop 一致")
    p_lk.add_argument("--purchasing-accounts", required=True, help="采购账号，多个英文逗号分隔")

    p_lprev = sub.add_parser("link-preview", help="SKU 匹配预览")
    _auth_args(p_lprev)
    p_lprev.add_argument("--shop-id", required=True, help="店铺 ID（与 list-shops 的 id 一致）")
    p_lprev.add_argument("--shop-nick", required=True, help="店铺名称 / shopNick")
    p_lprev.add_argument("--local-item-id", required=True, help="本店宝贝 ID")
    p_lprev.add_argument("--source-offer-url", required=True, help="1688 货源页 URL（detail.1688.com/offer/…）")
    p_lprev.add_argument("--purchase-account", required=True, help="采购账号（与 list-distributors 中 name 一致）")

    p_cf = sub.add_parser("confirm-link", help="确认并保存 SKU 映射")
    _auth_args(p_cf)
    p_cf.add_argument("--shop-id", required=True, help="店铺 ID")
    p_cf.add_argument("--shop-nick", required=True, help="店铺名称 / shopNick")
    p_cf.add_argument("--local-item-id", required=True, help="本店宝贝 ID")
    p_cf.add_argument("--source-offer-url", required=True, help="1688 货源页 URL")
    p_cf.add_argument("--purchase-account", required=True, help="采购账号")
    p_cf.add_argument(
        "--limit-rows",
        type=int,
        default=None,
        metavar="N",
        help="仅提交预览匹配结果前 N 条 SKU 映射（可选；不传则提交全部）",
    )
    """  ------------淘宝结束----------- """

    """  ------------抖音开始----------- """
    p_dy_ls = sub.add_parser("douyin-list-shops", help="抖音：查询当前用户绑定的分销店铺列表")
    _auth_args(p_dy_ls)

    p_dy_ld = sub.add_parser("douyin-list-distributors", help="抖音：查询某店铺的分销账号列表")
    _auth_args(p_dy_ld)
    p_dy_ld.add_argument("--shop-id", required=True, help="店铺 ID")

    p_dy_lp = sub.add_parser("douyin-list-products", help="抖音：查询店铺在售商品（itemlink/syn）")
    _auth_args(p_dy_lp)
    p_dy_lp.add_argument(
        "--shop-nick",
        required=True,
        help="店铺 nick 或 ID（仅支持直接传值）",
    )

    p_dy_elt = sub.add_parser("douyin-enable-link-type", help="抖音：开启分销商品开关（可多个商品 ID，逗号分隔）")
    _auth_args(p_dy_elt)
    p_dy_elt.add_argument("--item-ids", required=True, help="商品 ID，多个英文逗号隔开")
    p_dy_elt.add_argument("--shop", required=True, help="店铺名称（与下游 shop 一致）")
    p_dy_elt.add_argument("--purchasing-accounts", required=True, help="采购账号列表，多个英文逗号隔开")

    p_dy_eao = sub.add_parser("douyin-enable-auto-order", help="抖音：保存自动下单配置（透传 POST …/automationOrder）")
    _auth_args(p_dy_eao)
    p_dy_eao.add_argument("--shop-name", required=True, help="店铺名称")
    p_dy_eao.add_argument("--purchase-account", required=True, help="采购账号")

    p_dy_lasa = sub.add_parser("douyin-list-after-sale-accounts", help="抖音：售后采购账号列表")
    _auth_args(p_dy_lasa)
    p_dy_lasa.add_argument("--shop-id", required=True, help="店铺 ID（仅用于中台解析 sid，与下游 query 无关）")

    p_dy_eaas = sub.add_parser(
        "douyin-enable-auto-after-sale",
        help="抖音：保存售后规则（POST …/afterSale/setting；可选 --body-file 覆盖默认体）",
    )
    _auth_args(p_dy_eaas)
    p_dy_eaas.add_argument("--shop-id", required=True, help="店铺 ID（用于中台解析 sid）")
    p_dy_eaas.add_argument(
        "--body-file",
        default=None,
        help="可选：JSON 对象文件（UTF-8），与代码内默认售后请求体合并后提交（键覆盖默认值；勿含 loginName）",
    )
    p_dy_eaas.add_argument(
        "--purchase-account",
        required=True,
        help="采购账号，多个英文逗号分隔（与用户对话确认后传入，覆盖 body 内 purchaseAccount）",
    )
    p_dy_eaas.add_argument(
        "--shop-names",
        required=True,
        help="店铺范围，如「全部」或所选店铺名，多个英文逗号分隔（覆盖 body 内 shopNames）",
    )

    p_dy_set = sub.add_parser("douyin-settings", help="抖音：聚合绑定店铺 + 可选按 shop-id 查分销账号")
    _auth_args(p_dy_set)
    p_dy_set.add_argument("--shop-id", default=None, help="若提供则额外查询该店的分销账号")

    p_dy_lk = sub.add_parser("douyin-link-source", help="抖音：分销关系关联（复用 enable-link-type 逻辑）")
    _auth_args(p_dy_lk)
    p_dy_lk.add_argument(
        "--downstream-item-id",
        required=True,
        help="下游商品 ID，多个英文逗号分隔则批量",
    )
    p_dy_lk.add_argument("--source-offer-id", default=None, help="1688 货源 offer（可选，记入 data）")
    p_dy_lk.add_argument("--shop", required=True, help="店铺 nick / 与下游 shop 一致")
    p_dy_lk.add_argument("--purchasing-accounts", required=True, help="采购账号，多个英文逗号分隔")

    p_dy_lprev = sub.add_parser("douyin-link-preview", help="抖音：SKU 匹配预览")
    _auth_args(p_dy_lprev)
    p_dy_lprev.add_argument("--shop-id", required=True, help="店铺 ID（与 douyin-list-shops 的 id 一致）")
    p_dy_lprev.add_argument("--shop-nick", required=True, help="店铺名称 / shopNick")
    p_dy_lprev.add_argument("--local-item-id", required=True, help="本店商品 ID")
    p_dy_lprev.add_argument("--source-offer-url", required=True, help="1688 货源页 URL（detail.1688.com/offer/…）")
    p_dy_lprev.add_argument("--purchase-account", required=True, help="采购账号（与 douyin-list-distributors 中 name 一致）")

    p_dy_cf = sub.add_parser("douyin-confirm-link", help="抖音：确认并保存 SKU 映射")
    _auth_args(p_dy_cf)
    p_dy_cf.add_argument("--shop-id", required=True, help="店铺 ID")
    p_dy_cf.add_argument("--shop-nick", required=True, help="店铺名称 / shopNick")
    p_dy_cf.add_argument("--local-item-id", required=True, help="本店商品 ID")
    p_dy_cf.add_argument("--source-offer-url", required=True, help="1688 货源页 URL")
    p_dy_cf.add_argument("--purchase-account", required=True, help="采购账号")
    p_dy_cf.add_argument(
        "--limit-rows",
        type=int,
        default=None,
        metavar="N",
        help="仅提交预览匹配结果前 N 条 SKU 映射（可选；不传则提交全部）",
    )
    """  ------------抖音结束----------- """

    args = parser.parse_args()

    auth_err = _validate_cli_auth(args)
    if auth_err is not None:
        _print_json(auth_err)
        sys.exit(1)

    token = getattr(args, "token", None)

    if args.command == "list-shops":
        result = procurement.list_shops(token=token)
    elif args.command == "list-distributors":
        result = procurement.list_distributors(token=token, shop_id=args.shop_id)
    elif args.command == "list-products":
        result = procurement.list_shop_products(token=token, shop_nick=args.shop_nick)
    elif args.command == "enable-link-type":
        result = procurement.enable_link_type(
            token=token,
            item_ids=args.item_ids,
            shop=args.shop,
            purchasing_accounts=args.purchasing_accounts,
        )
    elif args.command == "enable-auto-order":
        result = procurement.save_automation_order(
            token=token,
            shop_name=args.shop_name,
            purchase_account=args.purchase_account,
        )
    elif args.command == "list-after-sale-accounts":
        result = procurement.list_purchase_accounts_after_sale(token=token, shop_id=args.shop_id)
    elif args.command == "enable-auto-after-sale":
        body_overrides: dict | None = None
        if args.body_file:
            try:
                with open(args.body_file, encoding="utf-8") as bf:
                    loaded = json.load(bf)
            except OSError as exc:
                _print_json(
                    {
                        "success": False,
                        "markdown": f"## 售后处理\n\n无法读取 body-file：{exc}",
                        "data": {"saved": False},
                        "error": str(exc),
                    }
                )
                sys.exit(1)
            except json.JSONDecodeError as exc:
                _print_json(
                    {
                        "success": False,
                        "markdown": f"## 售后处理\n\nbody-file 不是合法 JSON：{exc}",
                        "data": {"saved": False},
                        "error": str(exc),
                    }
                )
                sys.exit(1)
            if not isinstance(loaded, dict):
                _print_json(
                    {
                        "success": False,
                        "markdown": "## 售后处理\n\nbody-file 根节点须为 JSON 对象。",
                        "data": {"saved": False},
                        "error": "invalid_body_root",
                    }
                )
                sys.exit(1)
            loaded.pop("loginName", None)
            body_overrides = loaded
        result = procurement.save_auto_after_sale(
            token=token,
            shop_id=args.shop_id,
            purchase_account=(args.purchase_account or "").strip(),
            shop_names=(args.shop_names or "").strip(),
            body_overrides=body_overrides,
        )
    elif args.command == "settings":
        result = procurement.query_procurement_settings(token=token, shop_id=args.shop_id)
    elif args.command == "link-preview":
        result = procurement.run_link_preview(
            token=token,
            shop_id=args.shop_id,
            shop_nick=args.shop_nick,
            local_item_id=args.local_item_id,
            source_offer_url=args.source_offer_url,
            purchase_account=args.purchase_account,
        )
    elif args.command == "confirm-link":
        result = procurement.run_confirm_link(
            token=token,
            shop_id=args.shop_id,
            shop_nick=args.shop_nick,
            local_item_id=args.local_item_id,
            source_offer_url=args.source_offer_url,
            purchase_account=args.purchase_account,
            limit_rows=getattr(args, "limit_rows", None),
        )
    elif args.command == "link-source":
        result = procurement.link_source(
            token=token,
            downstream_item_id=args.downstream_item_id,
            source_offer_id=args.source_offer_id,
            shop=args.shop,
            purchasing_accounts=args.purchasing_accounts,
        )

    elif args.command == "douyin-list-shops":
        result = procurement.douyin_list_shops(token=token)
    elif args.command == "douyin-list-distributors":
        result = procurement.douyin_list_distributors(token=token, shop_id=args.shop_id)
    elif args.command == "douyin-list-products":
        result = procurement.douyin_list_shop_products(token=token, shop_nick=args.shop_nick)
    elif args.command == "douyin-enable-link-type":
        result = procurement.douyin_enable_link_type(
            token=token,
            item_ids=args.item_ids,
            shop=args.shop,
            purchasing_accounts=args.purchasing_accounts,
        )
    elif args.command == "douyin-enable-auto-order":
        result = procurement.douyin_save_automation_order(
            token=token,
            shop_name=args.shop_name,
            purchase_account=args.purchase_account,
        )
    elif args.command == "douyin-list-after-sale-accounts":
        result = procurement.douyin_list_purchase_accounts_after_sale(token=token, shop_id=args.shop_id)
    elif args.command == "douyin-enable-auto-after-sale":
        body_overrides: dict | None = None
        if args.body_file:
            try:
                with open(args.body_file, encoding="utf-8") as bf:
                    loaded = json.load(bf)
            except OSError as exc:
                _print_json(
                    {
                        "success": False,
                        "markdown": f"## 售后处理\n\n无法读取 body-file：{exc}",
                        "data": {"saved": False},
                        "error": str(exc),
                    }
                )
                sys.exit(1)
            except json.JSONDecodeError as exc:
                _print_json(
                    {
                        "success": False,
                        "markdown": f"## 售后处理\n\nbody-file 不是合法 JSON：{exc}",
                        "data": {"saved": False},
                        "error": str(exc),
                    }
                )
                sys.exit(1)
            if not isinstance(loaded, dict):
                _print_json(
                    {
                        "success": False,
                        "markdown": "## 售后处理\n\nbody-file 根节点须为 JSON 对象。",
                        "data": {"saved": False},
                        "error": "invalid_body_root",
                    }
                )
                sys.exit(1)
            loaded.pop("loginName", None)
            body_overrides = loaded
        result = procurement.douyin_save_auto_after_sale(
            token=token,
            shop_id=args.shop_id,
            purchase_account=(args.purchase_account or "").strip(),
            shop_names=(args.shop_names or "").strip(),
            body_overrides=body_overrides,
        )
    elif args.command == "douyin-settings":
        result = procurement.douyin_query_procurement_settings(token=token, shop_id=args.shop_id)
    elif args.command == "douyin-link-preview":
        result = procurement.douyin_run_link_preview(
            token=token,
            shop_id=args.shop_id,
            shop_nick=args.shop_nick,
            local_item_id=args.local_item_id,
            source_offer_url=args.source_offer_url,
            purchase_account=args.purchase_account,
        )
    elif args.command == "douyin-confirm-link":
        result = procurement.douyin_run_confirm_link(
            token=token,
            shop_id=args.shop_id,
            shop_nick=args.shop_nick,
            local_item_id=args.local_item_id,
            source_offer_url=args.source_offer_url,
            purchase_account=args.purchase_account,
            limit_rows=getattr(args, "limit_rows", None),
        )
    elif args.command == "douyin-link-source":
        result = procurement.douyin_link_source(
            token=token,
            downstream_item_id=args.downstream_item_id,
            source_offer_id=args.source_offer_id,
            shop=args.shop,
            purchasing_accounts=args.purchasing_accounts,
        )
    else:
        parser.error("未知子命令")

    _print_json(result)
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
