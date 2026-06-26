#!/usr/bin/env python3
"""
张飞搬家铺货助手 ISV Provider（采购方向）。

整合自 fx-procurement-9018264 ISV Skill，对接中台 SkillController 接口。
支持淘宝和抖音双平台，能力包括：自动下单、售后、关联货源。

业务逻辑由同目录下的 cli.py + scripts/procurement.py 实现，
本文件负责 Provider 注册和 CLI 封装调用。
"""

import os
import sys

_PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
sys.path.insert(0, _PROJECT_ROOT)

from scripts.isv.base import ISVApiClient, ISVProvider, register_provider


class ZhangfeiProcurementProvider(ISVProvider):
    """张飞搬家铺货助手 ISV Provider（采购方向）。"""

    name = "zhangfei"
    app_keys = ["9018264"]
    display_name = "张飞搬家铺货助手"
    api_base = "https://spmiddle.1tsoft.com/skill/skill"
    platform_credentials = {
        "douyin": {
            "client_id": "ytdyzfbj",
            "client_secret": "yxb6aU3dXip1J3WgmtQezrPVP0FyIGrPYSqHwK5N3eU=",
        },
        "taobao": {
            "client_id": "yttbzfbj",
            "client_secret": "Y9Ng8rau+XXJXeKB1QQXQZylYg4ThEQ78DjjBMKSyAc=",
        },
    }

    # ---- 淘宝能力 ----

    def list_shops(self, client: ISVApiClient, **kwargs):
        return self.run_cli("list-shops", token=client.token)

    def list_distributors(self, client: ISVApiClient, **kwargs):
        shop_id = kwargs.get("shop_id", "")
        return self.run_cli("list-distributors", token=client.token, extra_args=["--shop-id", str(shop_id)])

    def list_products(self, client: ISVApiClient, **kwargs):
        shop_nick = kwargs.get("shop_nick", "")
        return self.run_cli("list-products", token=client.token, extra_args=["--shop-nick", str(shop_nick)])

    def enable_link_type(self, client: ISVApiClient, **kwargs):
        item_ids = kwargs.get("item_ids", "")
        shop = kwargs.get("shop", "")
        purchasing_accounts = kwargs.get("purchasing_accounts", "")
        return self.run_cli("enable-link-type", token=client.token, extra_args=[
            "--item-ids", str(item_ids),
            "--shop", str(shop),
            "--purchasing-accounts", str(purchasing_accounts),
        ])

    def enable_auto_order(self, client: ISVApiClient, **kwargs):
        shop_name = kwargs.get("shop_name", "")
        purchase_account = kwargs.get("purchase_account", "")
        return self.run_cli("enable-auto-order", token=client.token, extra_args=[
            "--shop-name", str(shop_name),
            "--purchase-account", str(purchase_account),
        ])

    def list_after_sale_accounts(self, client: ISVApiClient, **kwargs):
        shop_id = kwargs.get("shop_id", "")
        return self.run_cli("list-after-sale-accounts", token=client.token, extra_args=["--shop-id", str(shop_id)])

    def enable_auto_after_sale(self, client: ISVApiClient, **kwargs):
        shop_id = kwargs.get("shop_id", "")
        purchase_account = kwargs.get("purchase_account", "")
        shop_names = kwargs.get("shop_names", "")
        extra_args = [
            "--shop-id", str(shop_id),
            "--purchase-account", str(purchase_account),
            "--shop-names", str(shop_names),
        ]
        body_file = kwargs.get("body_file")
        if body_file:
            extra_args.extend(["--body-file", str(body_file)])
        return self.run_cli("enable-auto-after-sale", token=client.token, extra_args=extra_args)

    def link_preview(self, client: ISVApiClient, **kwargs):
        return self.run_cli("link-preview", token=client.token, extra_args=[
            "--shop-id", str(kwargs.get("shop_id", "")),
            "--shop-nick", str(kwargs.get("shop_nick", "")),
            "--local-item-id", str(kwargs.get("local_item_id", "")),
            "--source-offer-url", str(kwargs.get("source_offer_url", "")),
            "--purchase-account", str(kwargs.get("purchase_account", "")),
        ])

    def confirm_link(self, client: ISVApiClient, **kwargs):
        extra_args = [
            "--shop-id", str(kwargs.get("shop_id", "")),
            "--shop-nick", str(kwargs.get("shop_nick", "")),
            "--local-item-id", str(kwargs.get("local_item_id", "")),
            "--source-offer-url", str(kwargs.get("source_offer_url", "")),
            "--purchase-account", str(kwargs.get("purchase_account", "")),
        ]
        limit_rows = kwargs.get("limit_rows")
        if limit_rows is not None:
            extra_args.extend(["--limit-rows", str(limit_rows)])
        return self.run_cli("confirm-link", token=client.token, extra_args=extra_args)

    def link_source(self, client: ISVApiClient, **kwargs):
        return self.run_cli("link-source", token=client.token, extra_args=[
            "--downstream-item-id", str(kwargs.get("downstream_item_id", "")),
            "--shop", str(kwargs.get("shop", "")),
            "--purchasing-accounts", str(kwargs.get("purchasing_accounts", "")),
        ])

    def query_settings(self, client: ISVApiClient, **kwargs):
        extra_args = []
        shop_id = kwargs.get("shop_id")
        if shop_id:
            extra_args.extend(["--shop-id", str(shop_id)])
        return self.run_cli("settings", token=client.token, extra_args=extra_args)

    # ---- 抖音能力 ----

    def douyin_list_shops(self, client: ISVApiClient, **kwargs):
        return self.run_cli("douyin-list-shops", token=client.token)

    def douyin_list_distributors(self, client: ISVApiClient, **kwargs):
        shop_id = kwargs.get("shop_id", "")
        return self.run_cli("douyin-list-distributors", token=client.token, extra_args=["--shop-id", str(shop_id)])

    def douyin_list_products(self, client: ISVApiClient, **kwargs):
        shop_nick = kwargs.get("shop_nick", "")
        return self.run_cli("douyin-list-products", token=client.token, extra_args=["--shop-nick", str(shop_nick)])

    def douyin_enable_link_type(self, client: ISVApiClient, **kwargs):
        return self.run_cli("douyin-enable-link-type", token=client.token, extra_args=[
            "--item-ids", str(kwargs.get("item_ids", "")),
            "--shop", str(kwargs.get("shop", "")),
            "--purchasing-accounts", str(kwargs.get("purchasing_accounts", "")),
        ])

    def douyin_enable_auto_order(self, client: ISVApiClient, **kwargs):
        return self.run_cli("douyin-enable-auto-order", token=client.token, extra_args=[
            "--shop-name", str(kwargs.get("shop_name", "")),
            "--purchase-account", str(kwargs.get("purchase_account", "")),
        ])

    def douyin_list_after_sale_accounts(self, client: ISVApiClient, **kwargs):
        shop_id = kwargs.get("shop_id", "")
        return self.run_cli("douyin-list-after-sale-accounts", token=client.token, extra_args=["--shop-id", str(shop_id)])

    def douyin_enable_auto_after_sale(self, client: ISVApiClient, **kwargs):
        shop_id = kwargs.get("shop_id", "")
        purchase_account = kwargs.get("purchase_account", "")
        shop_names = kwargs.get("shop_names", "")
        extra_args = [
            "--shop-id", str(shop_id),
            "--purchase-account", str(purchase_account),
            "--shop-names", str(shop_names),
        ]
        body_file = kwargs.get("body_file")
        if body_file:
            extra_args.extend(["--body-file", str(body_file)])
        return self.run_cli("douyin-enable-auto-after-sale", token=client.token, extra_args=extra_args)

    def douyin_link_preview(self, client: ISVApiClient, **kwargs):
        return self.run_cli("douyin-link-preview", token=client.token, extra_args=[
            "--shop-id", str(kwargs.get("shop_id", "")),
            "--shop-nick", str(kwargs.get("shop_nick", "")),
            "--local-item-id", str(kwargs.get("local_item_id", "")),
            "--source-offer-url", str(kwargs.get("source_offer_url", "")),
            "--purchase-account", str(kwargs.get("purchase_account", "")),
        ])

    def douyin_confirm_link(self, client: ISVApiClient, **kwargs):
        extra_args = [
            "--shop-id", str(kwargs.get("shop_id", "")),
            "--shop-nick", str(kwargs.get("shop_nick", "")),
            "--local-item-id", str(kwargs.get("local_item_id", "")),
            "--source-offer-url", str(kwargs.get("source_offer_url", "")),
            "--purchase-account", str(kwargs.get("purchase_account", "")),
        ]
        limit_rows = kwargs.get("limit_rows")
        if limit_rows is not None:
            extra_args.extend(["--limit-rows", str(limit_rows)])
        return self.run_cli("douyin-confirm-link", token=client.token, extra_args=extra_args)

    def douyin_link_source(self, client: ISVApiClient, **kwargs):
        extra_args = [
            "--downstream-item-id", str(kwargs.get("downstream_item_id", "")),
            "--shop", str(kwargs.get("shop", "")),
            "--purchasing-accounts", str(kwargs.get("purchasing_accounts", "")),
        ]
        source_offer_id = kwargs.get("source_offer_id")
        if source_offer_id:
            extra_args.extend(["--source-offer-id", str(source_offer_id)])
        return self.run_cli("douyin-link-source", token=client.token, extra_args=extra_args)

    def douyin_query_settings(self, client: ISVApiClient, **kwargs):
        extra_args = []
        shop_id = kwargs.get("shop_id")
        if shop_id:
            extra_args.extend(["--shop-id", str(shop_id)])
        return self.run_cli("douyin-settings", token=client.token, extra_args=extra_args)


# ---------------------------------------------------------------------------
# 注册 Provider
# ---------------------------------------------------------------------------

register_provider(ZhangfeiProcurementProvider())
