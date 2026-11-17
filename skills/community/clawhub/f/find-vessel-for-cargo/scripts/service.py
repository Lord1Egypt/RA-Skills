from __future__ import annotations

from html import escape
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .find_vessel import search_vessels
from .sol_tonnage import get_vessel_detail


app = FastAPI(title="ShippingClaw 租赁-货找船", version="1.0.0")


class SearchRequest(BaseModel):
    load_port: str = Field(min_length=2)
    discharge_port: str = Field(min_length=2)
    cargo_name: str = Field(min_length=1)
    cargo_tons: float = Field(gt=0)
    loading_date: str = Field(min_length=6)
    user_id: str = ""
    limit: int = Field(default=10, ge=1, le=100)
    force_refresh: bool = False


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/search")
def search(request: SearchRequest) -> dict:
    try:
        return search_vessels(**request.model_dump(), sync_demand_record=True)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/vessel/{solid}")
def detail(solid: str) -> dict:
    try:
        return get_vessel_detail(solid)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


DETAIL_FIELDS = (
    ("空船编号", "vessel_id"),
    ("船名", "vessel_name"),
    ("船型", "vessel_type"),
    ("船舶容量", "capacity"),
    ("空船港口", "open_port"),
    ("空船日期", "open_date"),
    ("船舶详细规范", "specifications"),
    ("发布日期", "published_date"),
    ("更新日期", "updated_date"),
    ("发布公司", "company_name"),
    ("联系人", "contact_name"),
    ("手机号码", "mobile"),
    ("联系电话", "telephone"),
    ("微信/QQ", "wechat_qq"),
    ("邮件", "email"),
    ("在线联系", "online_contact"),
)


def render_detail_page(vessel: dict[str, Any]) -> str:
    title = vessel.get("vessel_id") or vessel.get("vessel_name") or "空船详情"
    rows = []
    for label, field in DETAIL_FIELDS:
        raw_value = vessel.get(field)
        value = str(raw_value).strip() if raw_value is not None else ""
        rows.append(
            "<div class=\"row\">"
            f"<dt>{escape(label)}</dt>"
            f"<dd>{escape(value or '—')}</dd>"
            "</div>"
        )
    notice = (
        ""
        if vessel.get("contact_access") == "visible"
        else "<p class=\"notice\">联系方式为空、被遮罩或需要付费查看，已按规则留空。</p>"
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(str(title))}｜空船详情</title>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, "Microsoft YaHei", sans-serif; }}
    body {{ margin: 0; background: #f4f7fb; color: #172033; }}
    main {{ max-width: 820px; margin: 32px auto; padding: 0 16px; }}
    article {{ background: white; border: 1px solid #e2e8f0; border-radius: 16px;
      box-shadow: 0 8px 28px rgba(30, 50, 80, .08); overflow: hidden; }}
    header {{ padding: 24px; background: #0f766e; color: white; }}
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
        <p>ShippingClaw 站内空船详情</p>
      </header>
      <dl>{"".join(rows)}</dl>
      {notice}
    </article>
  </main>
</body>
</html>"""


@app.get("/vessel/{solid}/view", response_class=HTMLResponse)
def detail_view(solid: str) -> HTMLResponse:
    try:
        return HTMLResponse(render_detail_page(get_vessel_detail(solid)))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
