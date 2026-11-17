from __future__ import annotations

from html import escape
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .find_cargo import search_cargo
from .sol_cargo import get_cargo_detail


app = FastAPI(
    title="ShippingClaw 租赁-船找货",
    version="1.0.0",
)


class SearchRequest(BaseModel):
    current_port: str = Field(min_length=2)
    destination_port: str = Field(min_length=2)
    capacity_tons: float = Field(gt=0)
    user_id: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=100)
    force_refresh: bool = False


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/search")
def search(request: SearchRequest) -> dict:
    try:
        return search_cargo(**request.model_dump(), sync_demand_record=True)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/cargo/{solid}")
def detail(solid: str) -> dict:
    try:
        return get_cargo_detail(solid)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


DETAIL_FIELDS = (
    ("货盘编号", "cargo_id"),
    ("货名", "cargo_name"),
    ("货量", "quantity"),
    ("装港", "load_port"),
    ("卸港", "discharge_port"),
    ("装货日期", "loading_date"),
    ("发布日期", "published_date"),
    ("更新日期", "updated_date"),
    ("发布公司", "company_name"),
    ("详细信息及其他要求", "requirements"),
    ("联系人", "contact_name"),
    ("手机号码", "mobile"),
    ("联系电话", "telephone"),
    ("微信/QQ", "wechat_qq"),
    ("邮件", "email"),
    ("在线联系", "online_contact"),
)


def render_detail_page(cargo: dict[str, Any]) -> str:
    title = cargo.get("cargo_id") or cargo.get("title") or "货盘详情"
    rows = []
    for label, field in DETAIL_FIELDS:
        raw_value = cargo.get(field)
        value = str(raw_value).strip() if raw_value is not None else ""
        display_value = value or "—"
        rows.append(
            "<div class=\"row\">"
            f"<dt>{escape(label)}</dt>"
            f"<dd>{escape(display_value)}</dd>"
            "</div>"
        )
    contact_note = (
        ""
        if cargo.get("contact_access") == "visible"
        else "<p class=\"notice\">联系方式为空、被遮罩或需要付费查看，已按规则留空。</p>"
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(str(title))}｜货盘详情</title>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, "Microsoft YaHei", sans-serif; }}
    body {{ margin: 0; background: #f4f7fb; color: #172033; }}
    main {{ max-width: 820px; margin: 32px auto; padding: 0 16px; }}
    article {{ background: white; border: 1px solid #e2e8f0; border-radius: 16px;
      box-shadow: 0 8px 28px rgba(30, 50, 80, .08); overflow: hidden; }}
    header {{ padding: 24px; background: #0c4a6e; color: white; }}
    h1 {{ margin: 0 0 6px; font-size: 24px; }}
    header p {{ margin: 0; opacity: .8; }}
    dl {{ margin: 0; }}
    .row {{ display: grid; grid-template-columns: 170px 1fr; gap: 20px;
      padding: 14px 24px; border-top: 1px solid #edf2f7; }}
    dt {{ color: #64748b; }}
    dd {{ margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; }}
    .notice {{ margin: 0; padding: 16px 24px; background: #fff8e6; color: #854d0e; }}
    @media (max-width: 560px) {{
      .row {{ grid-template-columns: 1fr; gap: 5px; }}
    }}
  </style>
</head>
<body>
  <main>
    <article>
      <header>
        <h1>{escape(str(title))}</h1>
        <p>ShippingClaw 站内货盘详情</p>
      </header>
      <dl>{"".join(rows)}</dl>
      {contact_note}
    </article>
  </main>
</body>
</html>"""


@app.get("/cargo/{solid}/view", response_class=HTMLResponse)
def detail_view(solid: str) -> HTMLResponse:
    try:
        cargo = get_cargo_detail(solid)
        return HTMLResponse(render_detail_page(cargo))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
