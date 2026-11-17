"""URL 构建逻辑 + 参数校验

根据 type / offerId / imgUrl / imgUrlList 构建 1688 图片工具页面 URL，
输出透传对象供 LLM 原样转发触发 open_tab 交互。
"""

import os
from urllib.parse import quote
from _errors import ParamError

# 基础 URL（含固定参数，动态参数通过 & 拼接）
BASE_URL = (
    "https://air.1688.com/app/CSBC-modules/csbc-ai-component-loader"
    "/picture-optimize.html"
)

# type 入参 → (URL type 值, 图片参数名, 中文标题)
# 单图工具用 imgUrl，多图工具用 imgUrlList
TYPE_MAP = {
    "main":                  ("oneOptimization",       "imgUrl",     "主图优化"),
    "carousel":              ("carouselImage",         "imgUrlList", "轮播图制作"),
    "detail":                ("detailImage",           "imgUrlList", "详情图制作"),
    "matting":               ("matting",               "imgUrl",     "白底图"),
    "replaceSubject":        ("replaceSubject",        "imgUrl",     "背景替换"),
    "outpainting":           ("outpainting",           "imgUrl",     "一键扩图"),
    "digitalModel":          ("digitalModel",          "imgUrl",     "数字模特"),
}


def _fail(markdown: str) -> dict:
    return {"success": False, "markdown": markdown, "data": {}}


def _succeed(markdown: str, url: str, title: str) -> dict:
    return {
        "success": True,
        "markdown": markdown,
        "data": {
            "open_tab": {
                "type": "open_tab",
                "url": url,
                "title": title,
            }
        },
    }


def build_tool_url(
    type_: str,
    offer_id: str = None,
    img_url: str = None,
    img_url_list: str = None,
) -> dict:
    """构建图片工具页面 URL 并返回透传对象。

    Args:
        type_: main / carousel / detail
        offer_id: 商品 ID（可选）
        img_url: 单张图片路径/URL（可选，有则带入工具页）
        img_url_list: 多张图片路径/URL，逗号分隔（可选，有则带入工具页）

    Returns:
        标准输出 dict: {success, markdown, data}
    """
    # V1: type 校验
    if type_ not in TYPE_MAP:
        return _fail(f"❌ 不支持的图片类型：{type_}，可选值：" + " / ".join(TYPE_MAP.keys()))

    url_type, img_param, title = TYPE_MAP[type_]

    # V2: 空字符串校验（传了空字符串视为错误；None/未传则正常跳过）
    if img_url is not None and img_url.strip() == "":
        return _fail("❌ 图片路径无效，请检查后重试")
    if img_url_list is not None and img_url_list.strip() == "":
        return _fail("❌ 图片路径无效，请检查后重试")

    # V3: 图片参数与工具类型错配校验（报错而非静默忽略，让上游 LLM 自纠）。
    # 经 V2 后，此处非 None 的 img_url / img_url_list 必为非空。
    if img_param == "imgUrl" and img_url_list is not None:
        return _fail(f"❌ {title}是单图工具，请用 --img-url 传入图片")
    if img_param == "imgUrlList" and img_url is not None:
        return _fail(f"❌ {title}是多图工具，请用 --img-url-list 传入图片（多张逗号分隔）")

    # 构建 URL 参数
    params = [f"type={url_type}"]

    # 注入 sessionid（从环境变量 NEWTON_SESSION_ID 读取，缺失则跳过）
    session_id = os.environ.get("NEWTON_SESSION_ID")
    if session_id:
        params.append(f"sessionId={quote(session_id, safe='')}")

    if offer_id:
        params.append(f"offerId={offer_id}")

    # 图片参数：按 img_param 决定 imgUrl / imgUrlList，有则带入，无则跳过（工具页自带上传入口）
    if img_param == "imgUrl" and img_url:
        params.append(f"imgUrl={quote(img_url, safe='')}")
    elif img_param == "imgUrlList" and img_url_list:
        encoded_urls = ",".join(quote(u.strip(), safe="") for u in img_url_list.split(",") if u.strip())
        params.append(f"imgUrlList={encoded_urls}")

    url = BASE_URL + "?" + "&".join(params)

    return _succeed(f"正在为你打开{title}工具...", url, title)
