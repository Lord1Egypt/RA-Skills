from __future__ import annotations

import logging

from .dns import install_feishu_dns_fallback

install_feishu_dns_fallback()

import lark_oapi as lark
from lark_oapi.api.docx.v1.resource.document_block_children import DocumentBlockChildren

from .config import get_settings


def create_client(*, enable_set_token: bool = False) -> lark.Client:
    settings = get_settings()

    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))

    builder = (
        lark.Client.builder()
        .app_id(settings.app_id)
        .app_secret(settings.app_secret)
    )

    if enable_set_token:
        builder = builder.enable_set_token(True)

    if settings.base_url and settings.base_url != "https://open.feishu.cn":
        builder = builder.domain(settings.base_url)

    client = builder.build()

    if not hasattr(client.docx.v1.document_block, "children"):
        client.docx.v1.document_block.children = DocumentBlockChildren(client.docx.v1.document_block.config)

    return client
