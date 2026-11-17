#!/usr/bin/env python3
"""Product link to ad video: paste a product page, get a 15-second ad.

create : product page URL (or product data you already have) -> ad video task
query  : resume polling a known workspace_id
"""

from __future__ import annotations

import argparse

from shared.client import (
    DEFAULT_POLL_INTERVAL,
    DEFAULT_POLL_TIMEOUT,
    AdsTurboError,
    run_cli,
    submit_and_maybe_poll,
)

CREATE = "/openapi/v1/url2video/create"
AD_TYPES = ("ugc", "product_showcase")


def _product_from_args(args) -> dict:
    """Collect the product-data flags; empty when the caller passed none."""
    fields = {
        "title": args.title,
        "description": args.description,
        "price": args.price,
        "images": args.images,
        "brand": args.brand,
    }
    return {key: value for key, value in fields.items() if value not in ("", [], None)}


def cmd_create(client, args) -> dict:
    product = _product_from_args(args)
    if bool(args.product_url) == bool(product):
        raise AdsTurboError(
            -1,
            "pass exactly one of --product-url or product data "
            "(--title / --description / --price / --images / --brand)",
        )
    if product and not args.ad_type:
        raise AdsTurboError(
            -1,
            "product data needs --ad-type: ugc (spoken ad) or product_showcase (music only, no voiceover); "
            "without it the server rejects the request with ret=60819 and charges nothing",
        )
    return submit_and_maybe_poll(client, CREATE, {
        "product_url": args.product_url,
        # an empty dict would not be dropped by the client, so send None instead
        "product": product or None,
        "ad_type": args.ad_type,
        "language": args.language,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "idempotency_key": args.idempotency_key,
    }, args)


def cmd_query(client, args) -> dict:
    return client.poll(args.workspace_id, timeout=args.timeout, interval=args.interval)


def _add_poll_flags(sub) -> None:
    sub.add_argument("--timeout", type=float, default=DEFAULT_POLL_TIMEOUT)
    sub.add_argument("--interval", type=float, default=DEFAULT_POLL_INTERVAL)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AdsTurbo product link to ad video")
    sub = parser.add_subparsers(dest="command")

    create = sub.add_parser("create", help="make a 15-second ad from a product page or product data")
    create.add_argument("--product-url", default="", help="public product page URL")
    create.add_argument("--title", default="", help="product data: use when the page cannot be fetched")
    create.add_argument("--description", default="")
    create.add_argument("--price", default="", help="number or text, e.g. 24.99")
    create.add_argument("--images", nargs="*", default=[], help="public product image URLs")
    create.add_argument("--brand", default="")
    create.add_argument("--ad-type", choices=AD_TYPES, default="",
                        help="ugc = spoken ad; product_showcase = music only. Required with product data")
    create.add_argument("--language", default="", help="voiceover language, e.g. English")
    create.add_argument("--aspect-ratio", choices=("9:16", "1:1", "16:9"), default="")
    create.add_argument("--resolution", choices=("720p", "1080p"), default="")
    create.add_argument("--idempotency-key", default="", help="1-64 chars of letters, digits, _ and -; retry-safe")
    create.add_argument("--no-wait", action="store_true", help="submit only, do not poll")
    _add_poll_flags(create)

    query = sub.add_parser("query", help="resume polling a known workspace_id")
    query.add_argument("--workspace-id", required=True)
    _add_poll_flags(query)

    return parser


HANDLERS = {
    "create": cmd_create,
    "query": cmd_query,
}

if __name__ == "__main__":
    run_cli(build_parser(), HANDLERS)
