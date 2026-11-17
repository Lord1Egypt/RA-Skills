from __future__ import annotations

from html import escape
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .find_buyer import search_buyers
from .sol_purchases import get_purchase_detail


app = FastAPI(title="ShippingClaw 租赁-卖家找买家", version="1.0.0")


class SearchRequest(BaseModel):
    vessel_type: str = Field(min_length=1)
    capacity: str = Field(min_length=1)
    age: str = Field(min_length=1)
    flag: str = ""
    trade_scope: str = ""
    user_id: str = ""
    limit: int = Field(default=10, ge=1, le=100)
    force_refresh: bool = False


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/search")
def search(request: SearchRequest) -> dict:
    try:
        return search_buyers(**request.model_dump(), sync_demand_record=True)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/purchase/{solid}")
def detail(solid: str) -> dict:
    try:
        return get_purchase_detail(solid)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


DETAIL_FIELDS = (
    ("信息编号", "purchase_id"),
    ("求购船型", "vessel_type"),
    ("需求载重/容量", "capacity"),
    ("船龄要求", "age_range"),
    ("船旗要求", "flag"),
    ("有效期限", "valid_until"),
    ("发布日期", "published_date"),
    ("备注", "remarks"),
    ("买家公司", "company_name"),
    ("联系人", "contact_name"),
    ("电话", "telephone"),
    ("手机", "mobile"),
    ("微信/QQ", "wechat_qq"),
    ("邮件", "email"),
)


def render_detail_page(purchase: dict[str, Any]) -> str:
    title = purchase.get("purchase_id") or "求购船舶详情"
    rows = []
    for label, field in DETAIL_FIELDS:
        raw = purchase.get(field)
        value = str(raw).strip() if raw is not None else ""
        rows.append(
            '<div class="row">'
            f"<dt>{escape(label)}</dt><dd>{escape(value or '—')}</dd>"
            "</div>"
        )
    notice = "" if purchase.get("contact_access") == "visible" else '<p class="notice">联系方式为空、被遮罩或需要付费查看，已按规则留空。</p>'
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(str(title))}｜求购船舶详情</title>
<style>
:root{{font-family:system-ui,"Microsoft YaHei",sans-serif;color-scheme:light}}
body{{margin:0;background:#f4f7fb;color:#172033}}main{{max-width:860px;margin:32px auto;padding:0 16px}}
article{{background:#fff;border:1px solid #e2e8f0;border-radius:16px;box-shadow:0 8px 28px rgba(30,50,80,.08);overflow:hidden}}
header{{padding:24px;background:#0f766e;color:#fff}}h1{{margin:0 0 6px;font-size:24px}}header p{{margin:0;opacity:.8}}dl{{margin:0}}
.row{{display:grid;grid-template-columns:170px 1fr;gap:20px;padding:14px 24px;border-top:1px solid #edf2f7}}dt{{color:#64748b}}dd{{margin:0;white-space:pre-wrap;overflow-wrap:anywhere}}
.notice{{margin:0;padding:16px 24px;background:#fff8e6;color:#854d0e}}@media(max-width:560px){{.row{{grid-template-columns:1fr;gap:5px}}}}
</style></head><body><main><article><header><h1>{escape(str(title))}</h1><p>ShippingClaw 站内买家需求详情</p></header><dl>{''.join(rows)}</dl>{notice}</article></main></body></html>"""


@app.get("/purchase/{solid}/view", response_class=HTMLResponse)
def detail_view(solid: str) -> HTMLResponse:
    try:
        return HTMLResponse(render_detail_page(get_purchase_detail(solid)))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
