#!/usr/bin/env python3
"""Read a local product package; output SKU arguments or a draft JSON object.

No network, uploads, or writes. Structural checks do not establish business facts.
"""

import argparse
import hashlib
import json
import re
import sys
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, f"JSON 含重复键: {key}")
        result[key] = value
    return result


def invalid_constant(value):
    raise Invalid(f"不允许的 JSON 数值: {value}")


def resolve_inside(root, relative):
    require(isinstance(relative, str) and relative.strip(), "缺少包内相对文件路径")
    path = Path(relative)
    require(not path.is_absolute(), f"必须是商品包内相对路径: {relative}")
    target = (root / path).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        raise Invalid(f"路径越出商品包: {relative}") from None
    require(target.is_file(), f"文件不存在或不是普通文件: {relative}")
    return target


def read(root, relative):
    with resolve_inside(root, relative).open(encoding="utf-8") as stream:
        return json.load(stream, parse_float=Decimal, parse_constant=invalid_constant,
                         object_pairs_hook=pairs)


def object_file(root, name):
    data = read(root, f"text/{name}.json")
    require(isinstance(data, dict), f"{name}.json 须为 JSON 对象")
    return data


def field_file(root, name, key):
    data = object_file(root, name)
    require(set(data) == {key}, f"{name}.json 只应包含 {key}，元数据另存")
    return data[key]


def text_value(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return type(value) in (int, Decimal) and Decimal(value).is_finite()


def decimal_text(value):
    return format(Decimal(value), "f")


def dimensions(root):
    schema = object_file(root, "category-schema")
    names = schema.get("salePropNames")
    required = schema.get("requiredSalePropNames")
    for label, values in (("salePropNames", names), ("requiredSalePropNames", required)):
        require(isinstance(values, list), f"{label} 必须是实际返回的数组，缺失不等于无规格")
        require(all(text_value(n) for n in values), "规格名不能为空")
        require(len(set(values)) == len(values), "规格名不能重复")
        require(not set(values) & {"price", "stock"}, "规格名与 price/stock 冲突")
    return names + [name for name in required if name not in names]


def missing(value):
    return value is None or value == ""


def sku_rows(root, filename, names):
    rows = field_file(root, filename, "skuTable")
    required = object_file(root, "category-schema")["requiredSalePropNames"]
    require(isinstance(rows, list), f"{filename}.json 的 skuTable 必须是数组")
    require(rows or not required, "必填规格缺少对应值，请继续澄清")
    seen = set()
    for index, row in enumerate(rows, 1):
        label = f"{filename} 第 {index} 行"
        require(isinstance(row, dict), f"{label} 须为对象")
        require(set(row) <= set(names) | {"price", "stock"},
                f"{label} 含当前规格及 price、stock 以外的字段")
        for name in names:
            value = row.get(name)
            require(name not in required or text_value(value),
                    f"{label} 必填规格 {name} 缺少对应值，请继续澄清")
            require(missing(value) or (text_value(value) and "$" not in value),
                    f"{label} 的 {name} 须为非空文本且不含 $")
        identity = tuple(row.get(name) or "" for name in names)
        require(identity not in seen, f"{label} 规格组合重复")
        seen.add(identity)
        price, stock = row.get("price"), row.get("stock")
        require(missing(price) or (number(price) and price > 0), f"{label} 已填价格须为正数")
        require(missing(stock) or (type(stock) is int and stock >= 0),
                f"{label} 库存须为非负整数")
    active = [n for n in names if n in required or any(text_value(r.get(n)) for r in rows)]
    require(len(active) <= 2, "当前 SKU 工具最多表达二维采用规格，不能删必填维度绕过")
    return rows


def sku_arguments(root):
    names = dimensions(root)
    rows = sku_rows(root, "sku-input", names)
    names = [n for n in names if any(text_value(r.get(n)) for r in rows)]

    def column(key, formatter=str):
        values = ["" if missing(row.get(key)) else formatter(row[key]) for row in rows]
        return "$".join(values) if any(values) else ""

    return {
        "saleProp1": names[0] if names else "",
        "salePropValue1": column(names[0]) if names else "",
        "saleProp2": names[1] if len(names) == 2 else "",
        "salePropValue2": column(names[1]) if len(names) == 2 else "",
        "skuPrice": column("price", decimal_text),
        "skuStock": column("stock"),
    }


def url_ok(value):
    require(text_value(value) and not any(c.isspace() for c in value), "图片 URL 为空或含空白")
    parsed = urlsplit(value)
    require(parsed.scheme in ("https", "http") and parsed.hostname,
            "图片 URL 必须是完整 HTTP(S) 地址")
    require(parsed.username is None and parsed.password is None, "图片 URL 不应包含登录凭证")


class DetailImages(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = []

    def handle_starttag(self, tag, attrs):
        require(tag not in {"script", "iframe", "object", "embed"}, "详情含不支持的活动内容")
        require(not any(k.lower().startswith("on") for k, _ in attrs), "详情含事件脚本属性")
        if tag == "img":
            require(not any(k in {"srcset", "data-src"} for k, _ in attrs),
                    "详情图片请使用单一 src，避免未核验的替代地址")
            sources = [v for k, v in attrs if k == "src"]
            require(len(sources) == 1, "详情图片必须且只能包含一个 src")
            url_ok(sources[0])
            self.urls.append(sources[0])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def check_bank_files(root, used_urls):
    manifest = object_file(root, "manifest")
    assets = manifest.get("assets")
    require(isinstance(assets, list), "manifest.json 缺少 assets 列表")
    by_url = {}
    ids = set()
    for asset in assets:
        require(isinstance(asset, dict), "assets 项必须是对象")
        asset_id = asset.get("assetId")
        require(text_value(asset_id) and asset_id not in ids, "assetId 缺失或重复")
        ids.add(asset_id)
        bank = asset.get("bank")
        if bank is None:
            continue
        require(isinstance(bank, dict), f"{asset_id} 的 bank 必须是对象或 null")
        url = bank.get("url")
        url_ok(url)
        if url not in used_urls:
            continue
        require(url not in by_url, "一个图片银行 URL 被重复记为多个独立素材；先核对去重映射")
        original = resolve_inside(root, asset.get("localPath"))
        require(original.stat().st_size > 0, f"{asset_id} 原图为空")
        uploaded = resolve_inside(root, bank.get("file"))
        require(uploaded.stat().st_size > 0, f"{asset_id} 入库副本为空")
        expected = bank.get("sha256")
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
                f"{asset_id} 缺少真实 SHA-256")
        digest = hashlib.sha256()
        with uploaded.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        require(digest.hexdigest() == expected, f"{asset_id} 入库文件已改变，URL 对应待核实")
        receipt = resolve_inside(root, bank.get("receipt"))
        require(receipt.stat().st_size > 0, f"{asset_id} 入库回执为空")
        by_url[url] = asset_id
    require(used_urls <= set(by_url), "存在没有本地文件及入库回执映射的发布图片 URL")


def assemble(root):
    manifest = object_file(root, "manifest")
    require(not manifest.get("stopReason"), "当前商品存在未解除的业务终止，不能组装草稿")
    category = object_file(root, "category")
    cat_id = category.get("categoryId")
    require(type(cat_id) is int and cat_id > 0, "categoryId 必须是真实正整数")
    require(text_value(category.get("catNamePath")), "缺少实际类目路径")
    names = dimensions(root)
    sku_rows(root, "sku-input", names)  # Validate user input, not generated output.
    final_rows = field_file(root, "skuTable", "skuTable")
    require(isinstance(final_rows, list), "skuTable 必须是数组")
    require(final_rows or not object_file(root, "category-schema")["requiredSalePropNames"],
            "有必填规格时 skuTable 不能为空")
    title = field_file(root, "title", "title")
    require(text_value(title), "标题为空")
    props = field_file(root, "catProp", "catProp")
    require(isinstance(props, list) and props, "catProp 必须是非空数组")
    # Content adoption belongs to the agent; assemble accepted files without re-auditing.
    images = field_file(root, "imageList", "imageList")
    require(isinstance(images, list) and 1 <= len(images) <= 5, "主展示图数量须为 1—5")
    for url in images:
        url_ok(url)
    require(len(images) == len(set(images)), "主展示图 URL 重复")
    detail = field_file(root, "detail", "detail")
    require(text_value(detail), "详情为空")
    parser = DetailImages()
    parser.feed(detail)
    parser.close()
    check_bank_files(root, set(images) | set(parser.urls))
    return {"catId": cat_id, "scene": "aigc", "publishData": {
        "title": title, "imageList": images, "catProp": props,
        "skuTable": final_rows, "detail": detail,
    }}


def encode(value):
    """Serialize decimals without rounding them through binary floats."""
    if isinstance(value, Decimal):
        require(value.is_finite(), "不能序列化非有限数")
        return format(value, "f")
    if isinstance(value, list):
        return "[" + ",".join(encode(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + encode(v)
                               for k, v in value.items()) + "}"
    return json.dumps(value, ensure_ascii=False, allow_nan=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("sku-args", "assemble"))
    parser.add_argument("--product", required=True, help="已落地的商品目录")
    args = parser.parse_args()
    root = Path(args.product).resolve()
    try:
        require(root.is_dir(), "商品目录不存在")
        result = sku_arguments(root) if args.command == "sku-args" else assemble(root)
        print(encode(result))
    except (Invalid, OSError, ValueError, TypeError) as exc:
        print(f"未组装: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
