"""
Egatee Search Skill
调用 Web2JDE Orchestrator 搜索接口，并做本地每日调用次数限制（默认 5 次/天）。
若 api_key 经 Java 网关 `getChatHistoryByApiKey` 校验通过（HTTP 与业务态正常），则不占用该限额。

MySQL 用于 save_rfq 落库，以及可选的 jiji_ali_search.subject（中文关键词）补充检索；请配置 EGATEE_SEARCH_SKILL_DB_*（或 monorepo 回退 DB_*）。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, BinaryIO

import requests


def _import_pymysql() -> Any:
    """jiji_ali_search 补充检索与 save_rfq 落库依赖 PyMySQL（见 requirements.txt）。"""
    try:
        import pymysql

        return pymysql
    except ImportError as e:
        raise ImportError(
            "缺少 pymysql，无法访问 MySQL。请在 skill 目录执行: "
            "uv pip install -r requirements.txt 或 pip install pymysql>=1.1.0"
        ) from e


def _skill_db_host() -> str:
    v = os.getenv("EGATEE_SEARCH_SKILL_DB_HOST", "").strip()
    if v:
        return v
    v = os.getenv("DB_HOST", "localhost").strip()
    return v or "localhost"


def _skill_db_port() -> int:
    v = os.getenv("EGATEE_SEARCH_SKILL_DB_PORT", "").strip()
    if v:
        return int(v)
    return int(os.getenv("DB_PORT", "3306"))


def _skill_db_user() -> str:
    return os.getenv("EGATEE_SEARCH_SKILL_DB_USER", "").strip() or os.getenv("DB_USER", "").strip()


def _skill_db_password() -> str:
    return os.getenv("EGATEE_SEARCH_SKILL_DB_PASSWORD", "").strip() or os.getenv("DB_PASSWORD", "").strip()


def _skill_db_name() -> str:
    return (
        os.getenv("EGATEE_SEARCH_SKILL_DB_NAME", "").strip()
        or os.getenv("DB_NAME_WEBAPP", "").strip()
        or os.getenv("DB_NAME", "").strip()
    )


def _skill_api_key_cache_ttl() -> float:
    for key in ("EGATEE_SEARCH_SKILL_API_KEY_CACHE_TTL", "EGATEE_API_KEY_CACHE_TTL"):
        raw = os.getenv(key, "").strip()
        if raw:
            return float(raw)
    return 60.0


def _notify_verify_path() -> str:
    p = os.getenv(
        "EGATEE_NOTIFY_VERIFY_PATH",
        "/api/notify/im/openapi/getChatHistoryByApiKey",
    ).strip()
    if not p.startswith("/"):
        p = "/" + p
    return p


def _notify_verify_timeout() -> float:
    return float(os.getenv("EGATEE_NOTIFY_VERIFY_TIMEOUT", "15"))


def _notify_api_key_header_name() -> str:
    return os.getenv("EGATEE_NOTIFY_API_KEY_HEADER", "X-API-Key").strip() or "X-API-Key"


def _notify_verify_request_body() -> Dict[str, Any]:
    """
    与 chat-summary 等调用方一致：鉴权用 Header携带 Key，Body 为分页参数。
    可通过 EGATEE_NOTIFY_VERIFY_JSON_BODY 覆盖（整段 JSON 字符串）。
    """
    raw = os.getenv("EGATEE_NOTIFY_VERIFY_JSON_BODY", "").strip()
    if raw:
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                return dict(data)
        except json.JSONDecodeError:
            pass
    return {"day": 1, "current": 1, "size": 10}


def _notify_base_for_api_key(api_key: str) -> str:
    """
    与 SKILL.md 一致：uat_ 前缀走 UAT 网关，否则走生产；EGATEE_NOTIFY_BASE_URL 非空时覆盖二者。
    """
    override = os.getenv("EGATEE_NOTIFY_BASE_URL", "").strip().rstrip("/")
    if override:
        return override
    k = (api_key or "").strip()
    if k.lower().startswith("uat_"):
        return os.getenv("EGATEE_NOTIFY_UAT_BASE_URL", "http://api.uat.egatee.net").strip().rstrip("/")
    return os.getenv("EGATEE_NOTIFY_PROD_BASE_URL", "https://api.egatee.com").strip().rstrip("/")


def _sql_supplement_auto_threshold() -> int:
    try:
        return max(0, int(os.getenv("EGATEE_SQL_SUPPLEMENT_AUTO_THRESHOLD", "3")))
    except ValueError:
        return 3


def _sql_supplement_row_limit() -> int:
    try:
        return max(1, min(100, int(os.getenv("EGATEE_SQL_SUPPLEMENT_ROW_LIMIT", "20"))))
    except ValueError:
        return 20


def _jiji_search_table() -> str:
    t = os.getenv("EGATEE_JIJI_SEARCH_TABLE", "jiji_ali_search").strip()
    return t if re.match(r"^[A-Za-z0-9_]+$", t) else "jiji_ali_search"


def extract_chinese_keywords(text: str, max_keywords: int = 6, min_chars: int = 2) -> List[str]:
    """
    从用户查询中提取连续中文片段，用于 jiji_ali_search.subject LIKE 检索。
    min_chars: 最短片段长度（避免单字噪声）。
    """
    if not text or not isinstance(text, str):
        return []
    # 连续 CJK 统一表意文字
    pattern = r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]{" + str(max(1, min_chars)) + r",}"
    found = re.findall(pattern, text.strip())
    out: List[str] = []
    seen: set[str] = set()

    def push(w: str) -> None:
        nonlocal out
        if len(out) >= max_keywords or w in seen:
            return
        seen.add(w)
        out.append(w)

    for s in found:
        if len(out) >= max_keywords:
            break
        push(s)
        if len(s) >= 4:
            push(s[:2])
    return out


def _resolve_product_detail_url(p: Dict[str, Any]) -> str:
    """
    仅使用接口返回的 product_url / url；若无，则仅在配置了 EGATEE_PRODUCT_DETAIL_URL_TEMPLATE 时用其拼接
    （例如 https://example.com/item/{product_id}）。不再默认拼 wap.egatee.com/pd/{id}。
    """
    u = str(p.get("product_url", "") or p.get("url", "") or "").strip()
    if u:
        return u
    tpl = os.getenv("EGATEE_PRODUCT_DETAIL_URL_TEMPLATE", "").strip()
    if not tpl:
        return ""
    pid = p.get("product_id")
    if pid is None or pid == "":
        return ""
    ps = str(pid).strip()
    try:
        return tpl.format(product_id=ps)
    except (KeyError, IndexError, ValueError):
        return tpl.replace("{product_id}", ps)


def _jiji_row_to_product(row: Dict[str, Any]) -> Dict[str, Any]:
    """将 jiji_ali_search 行映射为与向量结果接近的 product dict。"""
    subject = str(row.get("subject") or "").strip()
    price = row.get("old_price")
    try:
        price_val = float(price) if price is not None else None
    except (TypeError, ValueError):
        price_val = None
    cat3 = str(row.get("category3_en") or "").strip()
    cat1 = str(row.get("category1_en") or "").strip()
    cname = str(row.get("category_name") or "").strip()
    store_bits = [x for x in (cat3, cat1, cname) if x]
    return {
        "product_id": None,
        "title": subject,
        "image_url": "",
        "category2": cat1,
        "category3": cat3,
        "price": price_val,
        "original_price": None,
        "similarity_score": None,
        "store_name": " | ".join(store_bits) if store_bits else "jiji_ali_search",
        "country": "",
        "country_code": "",
        "price_currency": "CNY",
        "source": "jiji_ali_search_sql",
    }


def _fetch_jiji_ali_search_by_subject(
    config: "SearchConfig",
    keywords: List[str],
    limit: int,
) -> List[Dict[str, Any]]:
    pymysql = _import_pymysql()

    if not keywords:
        return []
    if not (config.db_user and config.db_password and config.db_name):
        raise ValueError("未配置 MySQL（EGATEE_SEARCH_SKILL_DB_*），无法执行 jiji_ali_search 补充检索")

    table = _jiji_search_table()
    conditions: List[str] = []
    params: List[Any] = []
    for kw in keywords[:6]:
        conditions.append("subject LIKE %s")
        params.append(f"%{kw}%")
    where_kw = " OR ".join(conditions)
    params.append(limit)

    select_variants = (
        "subject, old_price, category1_en, category3_en, category_name, category_id",
        "subject, old_price, category1_en, category3_en",
        "subject, old_price",
    )

    conn = pymysql.connect(
        host=config.db_host,
        port=config.db_port,
        user=config.db_user,
        password=config.db_password,
        database=config.db_name,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        rows: List[Any] = []
        with conn.cursor() as cur:
            last_err: Optional[Exception] = None
            for cols in select_variants:
                sql = f"""
                    SELECT {cols}
                    FROM `{table}`
                    WHERE subject IS NOT NULL AND CHAR_LENGTH(TRIM(subject)) > 0
                      AND ({where_kw})
                    LIMIT %s
                """
                try:
                    cur.execute(sql, tuple(params))
                    rows = cur.fetchall()
                    last_err = None
                    break
                except Exception as e:
                    last_err = e
                    rows = []
            if last_err is not None:
                raise last_err
    finally:
        conn.close()

    return [_jiji_row_to_product(r) for r in rows if isinstance(r, dict)]


def _fetch_top_k_floor() -> int:
    """向 Orchestrator 多取若干条，便于有图优先与供 LLM 参考的候选池略大。"""
    try:
        return max(1, int(os.getenv("EGATEE_SEARCH_FETCH_TOP_K", "24")))
    except ValueError:
        return 24


def _effective_fetch_top_k(requested: int) -> int:
    return max(int(requested), _fetch_top_k_floor())


def _notify_http_response_ok(resp: requests.Response) -> bool:
    """网关返回 2xx 且 JSON 未显式失败则视为鉴权通过（不解析业务 data）。"""
    if resp.status_code < 200 or resp.status_code >= 300:
        return False
    ct = (resp.headers.get("Content-Type") or "").lower()
    if "json" not in ct:
        return True
    try:
        data = resp.json()
    except Exception:
        return True
    if not isinstance(data, dict):
        return True
    if data.get("notSuccess") is True:
        return False
    if data.get("success") is False:
        return False
    code = data.get("code")
    if isinstance(code, int) and code < 0:
        return False
    return True


@dataclass
class SearchConfig:
    base_url: str = field(
        default_factory=lambda: os.getenv(
            "EGATEE_SEARCH_BASE_URL",
            os.getenv("OPENCLAW_SEARCH_BASE_URL", "http://121.40.43.22:3004"),
        )
    )
    daily_limit: int = field(
        default_factory=lambda: int(os.getenv("EGATEE_DAILY_LIMIT", os.getenv("OPENCLAW_DAILY_LIMIT", "5")))
    )
    db_host: str = field(default_factory=_skill_db_host)
    db_port: int = field(default_factory=_skill_db_port)
    db_user: str = field(default_factory=_skill_db_user)
    db_password: str = field(default_factory=_skill_db_password)
    db_name: str = field(default_factory=_skill_db_name)
    api_key_cache_ttl: float = field(default_factory=_skill_api_key_cache_ttl)
    notify_verify_path: str = field(default_factory=_notify_verify_path)
    notify_verify_timeout: float = field(default_factory=_notify_verify_timeout)


def _default_rate_limit_state_path() -> Path:
    custom = os.getenv("EGATEE_RATE_LIMIT_STATE_PATH", "").strip()
    if custom:
        return Path(custom)
    salt = os.getenv("EGATEE_RATE_LIMIT_SALT", "").strip()
    suffix = ""
    if salt:
        suffix = "-" + hashlib.sha256(salt.encode("utf-8")).hexdigest()[:10]
    name = f"usage{suffix}.json"
    if os.name == "nt":
        base = os.getenv("LOCALAPPDATA")
        if base:
            return Path(base) / "egatee-search-skill" / name
        return Path.home() / "AppData" / "Local" / "egatee-search-skill" / name
    return Path.home() / ".cache" / "egatee-search-skill" / name


class DailyLimiter:
    def __init__(self, state_file: Path, limit: int) -> None:
        self.state_file = state_file
        self.limit = limit
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def _today(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def _read(self) -> Dict[str, Any]:
        if not self.state_file.exists():
            return {"date": self._today(), "count": 0}
        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return {"date": self._today(), "count": 0}
            return data
        except Exception:
            return {"date": self._today(), "count": 0}

    def _write(self, data: Dict[str, Any]) -> None:
        self.state_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def remaining(self) -> int:
        data = self._read()
        today = self._today()
        if data.get("date") != today:
            return self.limit
        used = int(data.get("count", 0))
        return max(0, self.limit - used)

    def consume(self) -> None:
        data = self._read()
        today = self._today()
        if data.get("date") != today:
            data = {"date": today, "count": 0}
        used = int(data.get("count", 0))
        if used >= self.limit:
            raise RuntimeError(f"Daily limit reached: {self.limit}/day")
        data["count"] = used + 1
        self._write(data)


class NotifyOpenApiKeyVerifier:
    """POST Java 网关 getChatHistoryByApiKey；响应正常即视为 api_key 有效。"""

    _cache: Dict[str, Tuple[float, bool]] = {}

    def __init__(self, config: SearchConfig) -> None:
        self.config = config

    def is_valid(self, api_key: str) -> bool:
        key = (api_key or "").strip()
        if not key:
            return False
        now = time.monotonic()
        ttl = max(0.0, self.config.api_key_cache_ttl)
        cached = self._cache.get(key)
        if cached and ttl > 0 and (now - cached[0]) < ttl:
            return cached[1]

        base = _notify_base_for_api_key(key)
        url = f"{base}{self.config.notify_verify_path}"
        header_name = _notify_api_key_header_name()
        headers = {"Content-Type": "application/json", header_name: key}
        try:
            resp = requests.post(
                url,
                json=_notify_verify_request_body(),
                headers=headers,
                timeout=self.config.notify_verify_timeout,
            )
        except requests.RequestException as e:
            raise RuntimeError(f"API Key 网关校验请求失败: {url} — {e}") from e

        ok = _notify_http_response_ok(resp)
        self._cache[key] = (now, ok)
        return ok


class EgateeSearchSkill:
    def __init__(self, config: Optional[SearchConfig] = None) -> None:
        self.config = config or SearchConfig()
        state_path = _default_rate_limit_state_path()
        self.limiter = DailyLimiter(state_path, self.config.daily_limit)
        self._verifier = NotifyOpenApiKeyVerifier(self.config)

    def remaining_today(self, api_key: Optional[str] = None) -> Optional[int]:
        """
        匿名限额剩余次数；若 api_key 经网关校验有效则返回 None（表示不限本地次数）。
        """
        resolved = self._resolve_api_key(api_key)
        if resolved and self._verified_assignment_key(resolved):
            return None
        return self.limiter.remaining()

    @staticmethod
    def _resolve_api_key(explicit: Optional[str]) -> str:
        if explicit is not None:
            return (explicit or "").strip()
        return (os.getenv("EGATEE_SEARCH_API_KEY", "") or "").strip()

    def _verified_assignment_key(self, api_key: str) -> bool:
        if not api_key:
            return False
        try:
            return self._verifier.is_valid(api_key)
        except ValueError:
            raise
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"校验 api_key 时发生错误: {e}") from e

    def _consume_quota(self, api_key: Optional[str]) -> None:
        resolved = self._resolve_api_key(api_key)
        if resolved and self._verified_assignment_key(resolved):
            return
        self.limiter.consume()

    @staticmethod
    def _safe_text(v: Any) -> str:
        s = "" if v is None else str(v)
        return (
            s.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    @staticmethod
    def _has_display_image(p: Dict[str, Any]) -> bool:
        u = str(p.get("image_url", "") or "").strip()
        if not u:
            return False
        return u.startswith("http://") or u.startswith("https://") or u.startswith("//")

    def _pick_top_products_for_display(self, products: List[Any], limit: int = 5) -> List[Dict[str, Any]]:
        """有有效主图 URL 的条目优先，其余按向量原顺序跟上（仍受 limit 约束）。"""
        with_img: List[Dict[str, Any]] = []
        without: List[Dict[str, Any]] = []
        for p in products:
            if not isinstance(p, dict):
                continue
            (with_img if self._has_display_image(p) else without).append(p)
        merged = with_img + without
        return merged[:limit]

    @staticmethod
    def _graphic_left_media_html(image_url: str, safe: Any) -> str:
        """有图用 img；无图用占位块，避免空 src 导致客户端只显示右侧文字。"""
        u = (image_url or "").strip()
        if u.startswith("http://") or u.startswith("https://") or u.startswith("//"):
            return (
                f"<img src=\"{safe(u)}\" alt=\"product\" "
                "style=\"width:92px;height:92px;object-fit:cover;border-radius:8px;background:#f5f5f5;\"/>"
            )
        return (
            "<div style=\"width:92px;height:92px;border-radius:8px;background:#f0f0f0;"
            "display:flex;align-items:center;justify-content:center;font-size:11px;color:#999;"
            "flex-shrink:0;text-align:center;padding:4px;\">无图</div>"
        )

    def _product_to_graphic_html(
        self,
        p: Dict[str, Any],
        *,
        product_url: str,
        badge: str = "",
    ) -> str:
        """左图右文 HTML；无有效 product_url 时不输出链接按钮。"""
        title = self._safe_text(p.get("title", ""))
        image_url = str(p.get("image_url", "") or "").strip()
        store_name = self._safe_text(p.get("store_name", ""))
        country = self._safe_text(p.get("country", ""))
        price = p.get("price")
        currency = self._safe_text(p.get("price_currency") or p.get("country_code") or "")
        price_text = self._safe_text(f"{currency} {price}" if price is not None else "")
        badge_html = (
            f"<div style=\"font-size:11px;color:#999;margin-bottom:4px;\">{self._safe_text(badge)}</div>"
            if badge
            else ""
        )
        left = self._graphic_left_media_html(image_url, self._safe_text)
        html = (
            "<div style=\"border:1px solid #eee;border-radius:12px;padding:10px;margin:8px 0;"
            "max-width:480px;background:#fff;\">"
            f"{badge_html}"
            f"<div style=\"display:flex;gap:10px;align-items:flex-start;\">"
            f"{left}"
            "<div style=\"flex:1;min-width:0;\">"
            f"<div style=\"font-size:14px;line-height:1.4;color:#111;font-weight:600;\">{title}</div>"
            f"<div style=\"margin-top:6px;font-size:16px;color:#e60039;font-weight:700;\">{price_text}</div>"
            f"<div style=\"margin-top:6px;font-size:12px;color:#666;\">{store_name}</div>"
            f"<div style=\"margin-top:2px;font-size:12px;color:#666;\">{country}</div>"
            "</div></div>"
        )
        if product_url:
            html += (
                f"<a href=\"{self._safe_text(product_url)}\" target=\"_blank\" "
                "style=\"display:inline-block;margin-top:10px;padding:8px 12px;border-radius:8px;"
                "background:#e60039;color:#fff;text-decoration:none;font-size:12px;\">查看商品</a>"
            )
        html += "</div>"
        return html

    def _build_product_cards(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cards: List[Dict[str, Any]] = []
        for p in products:
            pid = p.get("product_id")
            product_url = _resolve_product_detail_url(p)
            html = self._product_to_graphic_html(p, product_url=product_url, badge="")

            cards.append(
                {
                    "product_id": pid,
                    "title": p.get("title", ""),
                    "image_url": str(p.get("image_url", "") or "").strip(),
                    "price": p.get("price"),
                    "price_currency": p.get("price_currency"),
                    "store_name": p.get("store_name", ""),
                    "country": p.get("country", ""),
                    "product_url": product_url,
                    "html": html,
                }
            )
        return cards

    def _build_graphic_text_cards(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        图文卡片：明确标注来自向量检索结果，适合在聊天场景直接渲染/发送。
        """
        cards: List[Dict[str, Any]] = []
        for idx, p in enumerate(products, start=1):
            title = str(p.get("title", "") or "").strip()
            image_url = str(p.get("image_url", "") or "").strip()
            store_name = str(p.get("store_name", "") or "").strip()
            country = str(p.get("country", "") or "").strip()
            similarity_score = p.get("similarity_score")
            price = p.get("price")
            currency = str(p.get("price_currency") or p.get("country_code") or "").strip()
            price_text = f"{currency} {price}" if price is not None else ""
            pid = p.get("product_id")
            product_url = _resolve_product_detail_url(p)

            desc_parts = []
            if price_text:
                desc_parts.append(f"价格: {price_text}")
            if store_name:
                desc_parts.append(f"店铺: {store_name}")
            if country:
                desc_parts.append(f"国家: {country}")
            if similarity_score is not None:
                desc_parts.append(f"向量相似度: {similarity_score}")

            src = str(p.get("source") or "vector_search").strip() or "vector_search"
            badge = "向量检索" if src == "vector_search" else ("SQL: jiji_ali_search" if "jiji" in src else src)
            card_html = self._product_to_graphic_html(p, product_url=product_url, badge=badge)
            desc_joined = " | ".join(desc_parts)
            # 与 v1.2.2 一致：主协议仍是结构化 image_url + title + description（客户端按 URL 出图）
            # markdown 供仅支持 Markdown 的渠道；禁止 Agent 只抄 description 导致「只见字」
            md_lines: List[str] = []
            if image_url and (
                image_url.startswith("http://")
                or image_url.startswith("https://")
                or image_url.startswith("//")
            ):
                esc_title = title.replace("]", "\\]").replace("[", "\\[")
                md_lines.append(f"![{esc_title}]({image_url})")
            md_lines.append(f"**{title}**")
            if desc_joined:
                md_lines.append(desc_joined)
            if product_url:
                md_lines.append(f"[查看商品]({product_url})")
            card_markdown = "\n\n".join(md_lines)

            cards.append(
                {
                    "type": "graphic_text_card",
                    "rank": idx,
                    "source": src,
                    "product_id": pid,
                    "title": title,
                    "description": desc_joined,
                    "image_url": image_url,
                    "button_text": "查看商品" if product_url else "",
                    "button_url": product_url,
                    "markdown": card_markdown,
                    "html": card_html,
                    "raw_product": p,
                }
            )
        return cards

    def _attach_merged_graphic_html(self, result: Dict[str, Any]) -> None:
        """便于一次粘贴整段 HTML；另提供 merged markdown（多通道只放行 MD 时出图）。"""
        gt = result.get("graphic_text_cards")
        if not isinstance(gt, list):
            result["graphic_text_merged_html"] = ""
            result["graphic_text_merged_markdown"] = ""
            return
        parts = [str(c.get("html") or "") for c in gt if isinstance(c, dict) and c.get("html")]
        result["graphic_text_merged_html"] = "\n".join(parts).strip()
        md_parts = [str(c.get("markdown") or "") for c in gt if isinstance(c, dict) and c.get("markdown")]
        result["graphic_text_merged_markdown"] = "\n\n---\n\n".join(md_parts).strip()

    def _post_process_search_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        products = result.get("products")
        if not isinstance(products, list):
            return result
        result["vector_hits_returned"] = len(products)
        result["products_raw"] = [p for p in products if isinstance(p, dict)]
        top_products = self._pick_top_products_for_display(products, limit=5)
        result["products"] = top_products
        result["cards"] = self._build_product_cards(top_products)
        result["graphic_text_cards"] = self._build_graphic_text_cards(top_products)
        self._attach_merged_graphic_html(result)
        result["card_type"] = "product_cards"
        result["card_count"] = len(top_products)
        result["graphic_display_hint"] = (
            "与 v1.2.2 一致：每条 graphic_text_card 须按 image_url 出图 + title + description；"
            "或整段发送 graphic_text_merged_markdown / graphic_text_merged_html（勿只输出 description 纯文字）。"
        )
        result["display_note"] = (
            "向量检索原始命中 {} 条；已按有图优先取前 5 条写入 products/cards。"
            "最终是否向用户展示须由 LLM 按用户意图做相关性筛选（见 SKILL.md）。"
        ).format(len(products))
        result["summary"] = f"共匹配到 {len(top_products)} 个商品（仅展示前 5 个，含向量图文卡片；有图优先）"
        return result

    def _merge_vector_sql_products(
        self,
        vector_display: List[Dict[str, Any]],
        sql_products: List[Dict[str, Any]],
        supplement_forced: bool,
    ) -> List[Dict[str, Any]]:
        """合并向量 Top 与 SQL 命中；强制补充时 SQL 条目前排。"""

        def dedupe_key(p: Dict[str, Any]) -> Tuple[str, str]:
            return (str(p.get("product_id") or "").strip(), str(p.get("title") or "").strip().lower()[:240])

        seen: set[Tuple[str, str]] = set()
        out: List[Dict[str, Any]] = []

        def add_list(lst: List[Dict[str, Any]]) -> None:
            for p in lst:
                if not isinstance(p, dict):
                    continue
                k = dedupe_key(p)
                if k[1] or k[0]:
                    if k in seen:
                        continue
                    seen.add(k)
                out.append(p)

        vd = [p for p in vector_display if isinstance(p, dict)]
        sp = [p for p in sql_products if isinstance(p, dict)]
        if supplement_forced and sp:
            add_list(sp)
            add_list(vd)
        else:
            add_list(vd)
            add_list(sp)
        return out[:5]

    def _apply_sql_supplement(
        self,
        query_text: str,
        result: Dict[str, Any],
        supplement_sql: Optional[bool],
    ) -> None:
        """
        supplement_sql: True=强制跑 SQL；False=不跑；None=向量命中少于阈值时自动跑。
        依赖 EGATEE_SEARCH_SKILL_DB_*（与 save_rfq 相同库，含 jiji_ali_search）。
        """
        th = _sql_supplement_auto_threshold()
        vhits = int(result.get("vector_hits_returned") or 0)
        vtop = result.get("products") if isinstance(result.get("products"), list) else []
        auto_need = th > 0 and (vhits < th or len(vtop) < 2)

        if supplement_sql is False:
            result["sql_supplement"] = {"applied": False, "reason": "disabled_by_caller"}
            return
        if supplement_sql is None and not auto_need:
            result["sql_supplement"] = {"applied": False, "reason": "vector_sufficient"}
            return

        kw = extract_chinese_keywords(query_text)
        if not kw:
            result["sql_supplement"] = {
                "applied": False,
                "reason": "no_chinese_keywords_in_query",
                "hint": "jiji_ali_search.subject 为中文；请在搜索句或 metadata.sql_supplement_query 中提供中文关键词",
            }
            return

        lim = _sql_supplement_row_limit()
        try:
            sql_hits = _fetch_jiji_ali_search_by_subject(self.config, kw, lim)
        except Exception as e:
            result["sql_supplement"] = {"applied": False, "reason": f"sql_error: {e}", "keywords": kw}
            return

        if not sql_hits:
            result["sql_supplement"] = {
                "applied": False,
                "reason": "sql_no_rows",
                "keywords": kw,
            }
            return

        vector_display = [p for p in (result.get("products") or []) if isinstance(p, dict)]
        merged = self._merge_vector_sql_products(
            vector_display,
            sql_hits,
            supplement_forced=supplement_sql is True,
        )
        merged = self._pick_top_products_for_display(merged, limit=5)

        result["sql_supplement"] = {
            "applied": True,
            "keywords": kw,
            "row_count": len(sql_hits),
            "forced": supplement_sql is True,
            "trigger": "user_forced" if supplement_sql is True else "auto_low_vector_hits",
        }
        result["products_sql"] = sql_hits
        result["products"] = merged
        result["cards"] = self._build_product_cards(merged)
        result["graphic_text_cards"] = self._build_graphic_text_cards(merged)
        self._attach_merged_graphic_html(result)
        result["card_count"] = len(merged)
        result["graphic_display_hint"] = (
            "与 v1.2.2 一致：每条 graphic_text_card 须按 image_url 出图 + title + description；"
            "或整段发送 graphic_text_merged_markdown / graphic_text_merged_html（勿只输出 description 纯文字）。"
        )
        result["summary"] = (
            f"向量命中 {vhits} 条；SQL(jiji_ali_search.subject) 补充 {len(sql_hits)} 条；"
            f"合并展示 {len(merged)} 条（有图优先）"
        )
        note = str(result.get("display_note") or "")
        extra = "已合并 jiji_ali_search 中文 subject 检索；LLM 仍须做相关性筛选。"
        result["display_note"] = (note + " " + extra).strip() if note else extra

    def _ensure_openclaw_rfq_table(self, cursor: Any) -> None:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS openclaw_rfq (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                rfq_id VARCHAR(100) UNIQUE NOT NULL COMMENT 'OpenClaw RFQ ID',
                user_id VARCHAR(100) NULL COMMENT '用户ID',
                product_id INT NULL COMMENT '商品ID',
                quantity INT NOT NULL DEFAULT 1 COMMENT '采购数量',
                expected_price_min DECIMAL(15,2) NULL COMMENT '期望价格最小值',
                expected_price_max DECIMAL(15,2) NULL COMMENT '期望价格最大值',
                price_currency VARCHAR(10) DEFAULT 'USD' COMMENT '货币单位',
                delivery_address TEXT NULL COMMENT '收货地址',
                contact_phone VARCHAR(20) NULL COMMENT '联系电话',
                status ENUM('OPEN', 'LOCKED', 'CONFIRMED', 'PAID', 'SHIPPED', 'COMPLETED', 'CANCELLED') DEFAULT 'OPEN' COMMENT 'RFQ状态',
                notes TEXT NULL COMMENT '备注',
                is_ai_generated BOOLEAN DEFAULT TRUE COMMENT '是否AI生成',
                payment_method VARCHAR(50) NULL COMMENT '结款方式',
                delivery_method VARCHAR(50) NULL COMMENT '配送方式',
                search_image_url VARCHAR(500) NULL COMMENT '搜索图片链接',
                product_attributes JSON NULL COMMENT '商品属性',
                product_name VARCHAR(500) NULL COMMENT '产品名称',
                product_description TEXT NULL COMMENT '产品描述',
                chat_history JSON NULL COMMENT '聊天记录快照',
                selected_items JSON NULL COMMENT '用户选择快照',
                source_payload JSON NULL COMMENT '原始payload快照',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user_id (user_id),
                INDEX idx_product_id (product_id),
                INDEX idx_status (status),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='OpenClaw RFQ表（参考webapp_rfq字段）'
            """
        )

    def _extract_rfq_from_chat(self, payload: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
        params = payload.get("params") if isinstance(payload.get("params"), dict) else {}
        selected = payload.get("selected") if isinstance(payload.get("selected"), dict) else {}
        products = result.get("products") if isinstance(result.get("products"), list) else []

        def pick_str(*vals: Any) -> str:
            for v in vals:
                if isinstance(v, str) and v.strip():
                    return v.strip()
            return ""

        def pick_num(*vals: Any) -> Any:
            for v in vals:
                if v is None:
                    continue
                try:
                    return float(v)
                except Exception:
                    continue
            return None

        selected_product_id = selected.get("product_id") or payload.get("product_id")
        if selected_product_id is None and products:
            selected_product_id = products[0].get("product_id")

        product_name = pick_str(
            selected.get("product_name"),
            payload.get("product_name"),
            (products[0].get("title") if products else ""),
            self._extract_text(payload),
        )
        search_image_url = pick_str(payload.get("image_url"), self._extract_image_url(payload))
        quantity_raw = (
            selected.get("quantity")
            or payload.get("quantity")
            or metadata.get("quantity")
            or params.get("quantity")
            or 1
        )
        try:
            quantity = max(1, int(quantity_raw))
        except Exception:
            quantity = 1

        rfq = {
            "rfq_id": f"OCRFQ-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}",
            "user_id": pick_str(payload.get("user_id"), metadata.get("user_id"), payload.get("conversation_id")),
            "product_id": int(selected_product_id) if selected_product_id not in (None, "") else None,
            "quantity": quantity,
            "expected_price_min": pick_num(selected.get("expected_price_min"), payload.get("expected_price_min"), metadata.get("expected_price_min")),
            "expected_price_max": pick_num(selected.get("expected_price_max"), payload.get("expected_price_max"), metadata.get("expected_price_max")),
            "price_currency": pick_str(selected.get("price_currency"), payload.get("price_currency"), metadata.get("price_currency"), "USD"),
            "delivery_address": pick_str(selected.get("delivery_address"), payload.get("delivery_address"), metadata.get("delivery_address")),
            "contact_phone": pick_str(selected.get("contact_phone"), payload.get("contact_phone"), metadata.get("contact_phone")),
            "status": "OPEN",
            "notes": pick_str(payload.get("text"), payload.get("query"), payload.get("message"), payload.get("content")),
            "is_ai_generated": True,
            "payment_method": pick_str(selected.get("payment_method"), payload.get("payment_method"), metadata.get("payment_method")),
            "delivery_method": pick_str(selected.get("delivery_method"), payload.get("delivery_method"), metadata.get("delivery_method")),
            "search_image_url": search_image_url or None,
            "product_attributes": selected.get("product_attributes") or payload.get("product_attributes") or metadata.get("product_attributes"),
            "product_name": product_name or None,
            "product_description": pick_str(selected.get("product_description"), payload.get("product_description"), metadata.get("product_description")) or None,
            "chat_history": payload.get("chat_history") if isinstance(payload.get("chat_history"), list) else payload.get("messages"),
            "selected_items": selected or (payload.get("selected_items") if isinstance(payload.get("selected_items"), dict) else None),
            "source_payload": payload,
        }
        return rfq

    def _save_openclaw_rfq(self, rfq: Dict[str, Any]) -> Optional[int]:
        if not (self.config.db_user and self.config.db_password and self.config.db_name):
            return None
        pymysql = _import_pymysql()

        conn = pymysql.connect(
            host=self.config.db_host,
            port=self.config.db_port,
            user=self.config.db_user,
            password=self.config.db_password,
            database=self.config.db_name,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor,
        )
        try:
            with conn.cursor() as cur:
                self._ensure_openclaw_rfq_table(cur)
                sql = """
                    INSERT INTO openclaw_rfq
                    (rfq_id, user_id, product_id, quantity, expected_price_min, expected_price_max, price_currency,
                     delivery_address, contact_phone, status, notes, is_ai_generated, payment_method, delivery_method,
                     search_image_url, product_attributes, product_name, product_description, chat_history, selected_items, source_payload)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(
                    sql,
                    (
                        rfq.get("rfq_id"),
                        rfq.get("user_id"),
                        rfq.get("product_id"),
                        rfq.get("quantity"),
                        rfq.get("expected_price_min"),
                        rfq.get("expected_price_max"),
                        rfq.get("price_currency"),
                        rfq.get("delivery_address"),
                        rfq.get("contact_phone"),
                        rfq.get("status"),
                        rfq.get("notes"),
                        1 if rfq.get("is_ai_generated") else 0,
                        rfq.get("payment_method"),
                        rfq.get("delivery_method"),
                        rfq.get("search_image_url"),
                        json.dumps(rfq.get("product_attributes"), ensure_ascii=False) if rfq.get("product_attributes") is not None else None,
                        rfq.get("product_name"),
                        rfq.get("product_description"),
                        json.dumps(rfq.get("chat_history"), ensure_ascii=False) if rfq.get("chat_history") is not None else None,
                        json.dumps(rfq.get("selected_items"), ensure_ascii=False) if rfq.get("selected_items") is not None else None,
                        json.dumps(rfq.get("source_payload"), ensure_ascii=False),
                    ),
                )
                conn.commit()
                return cur.lastrowid
        finally:
            conn.close()

    def _attach_rfq_candidate(self, payload: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        rfq = self._extract_rfq_from_chat(payload, result)
        result["rfq_candidate"] = rfq
        result["rfq"] = {
            "table": "openclaw_rfq",
            "saved": False,
            "db_row_id": None,
            "rfq_id": rfq.get("rfq_id"),
            "reason": "candidate_only_waiting_for_llm_decision",
        }
        return result

    def build_rfq_candidate(self, payload: Dict[str, Any], search_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        仅抽取候选 RFQ，不落库。供 LLM 先判断信息是否足够。
        """
        if not isinstance(payload, dict):
            raise ValueError("payload must be a dict")
        if not isinstance(search_result, dict):
            raise ValueError("search_result must be a dict")
        return self._extract_rfq_from_chat(payload, search_result)

    def save_rfq(self, rfq_candidate: Dict[str, Any]) -> Dict[str, Any]:
        """
        显式落库入口：仅在 LLM 判断“信息足够形成 RFQ”后调用。
        """
        if not isinstance(rfq_candidate, dict):
            raise ValueError("rfq_candidate must be a dict")
        row_id = self._save_openclaw_rfq(rfq_candidate)
        return {
            "table": "openclaw_rfq",
            "saved": row_id is not None,
            "db_row_id": row_id,
            "rfq_id": rfq_candidate.get("rfq_id"),
        }

    def search_text(
        self,
        text: str,
        country: Optional[str] = None,
        top_k: int = 10,
        api_key: Optional[str] = None,
        supplement_sql: Optional[bool] = None,
    ) -> Dict[str, Any]:
        text = (text or "").strip()
        if not text:
            raise ValueError("text cannot be empty")

        self._consume_quota(api_key)

        fetch_k = _effective_fetch_top_k(top_k)
        payload: Dict[str, Any] = {"text": text, "top_k": fetch_k}
        if country:
            payload["country"] = country

        url = f"{self.config.base_url.rstrip('/')}/api/search/text"
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        out = self._post_process_search_result(resp.json())
        out["search_top_k_requested"] = top_k
        out["search_top_k_fetched"] = fetch_k
        self._apply_sql_supplement(text, out, supplement_sql)
        return out

    def search(self, text: str, country: Optional[str] = None, top_k: int = 10, api_key: Optional[str] = None) -> Dict[str, Any]:
        return self.search_text(text=text, country=country, top_k=top_k, api_key=api_key)

    def _search_image_fileobj(
        self,
        file_obj: BinaryIO,
        filename: str,
        country: Optional[str] = None,
        top_k: int = 10,
        api_key: Optional[str] = None,
        supplement_sql: Optional[bool] = None,
        supplement_query_text: str = "",
    ) -> Dict[str, Any]:
        self._consume_quota(api_key)

        fetch_k = _effective_fetch_top_k(top_k)
        url = f"{self.config.base_url.rstrip('/')}/api/search/image"
        data: Dict[str, Any] = {"top_k": str(fetch_k)}
        if country:
            data["country"] = country

        files = {"image": (filename, file_obj, "application/octet-stream")}
        resp = requests.post(url, data=data, files=files, timeout=60)
        resp.raise_for_status()
        out = self._post_process_search_result(resp.json())
        out["search_top_k_requested"] = top_k
        out["search_top_k_fetched"] = fetch_k
        qctx = (supplement_query_text or "").strip()
        if qctx or supplement_sql is True:
            self._apply_sql_supplement(qctx, out, supplement_sql)
        else:
            out.setdefault("sql_supplement", {"applied": False, "reason": "image_mode_no_text_for_sql"})
        return out

    def search_image(
        self,
        image_path: str,
        country: Optional[str] = None,
        top_k: int = 10,
        api_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        p = Path(image_path)
        if not p.exists() or not p.is_file():
            raise ValueError(f"image file not found: {image_path}")
        with p.open("rb") as f:
            return self._search_image_fileobj(
                file_obj=f,
                filename=p.name,
                country=country,
                top_k=top_k,
                api_key=api_key,
                supplement_sql=None,
                supplement_query_text="",
            )

    def search_image_url(
        self,
        image_url: str,
        country: Optional[str] = None,
        top_k: int = 10,
        api_key: Optional[str] = None,
        supplement_sql: Optional[bool] = None,
        supplement_query_text: str = "",
    ) -> Dict[str, Any]:
        image_url = (image_url or "").strip()
        if not image_url:
            raise ValueError("image_url cannot be empty")
        if not (image_url.startswith("http://") or image_url.startswith("https://")):
            raise ValueError("image_url must start with http:// or https://")

        download_resp = requests.get(image_url, timeout=30)
        download_resp.raise_for_status()
        content_type = download_resp.headers.get("content-type", "").lower()
        ext = ".jpg"
        if "png" in content_type:
            ext = ".png"
        elif "webp" in content_type:
            ext = ".webp"
        elif "gif" in content_type:
            ext = ".gif"

        from io import BytesIO

        image_bytes = BytesIO(download_resp.content)
        return self._search_image_fileobj(
            file_obj=image_bytes,
            filename=f"remote_image{ext}",
            country=country,
            top_k=top_k,
            api_key=api_key,
            supplement_sql=supplement_sql,
            supplement_query_text=supplement_query_text,
        )

    @staticmethod
    def _extract_top_k(payload: Dict[str, Any], default: int = 10) -> int:
        candidates: List[Any] = [
            payload.get("top_k"),
            (payload.get("metadata") or {}).get("top_k"),
            (payload.get("params") or {}).get("top_k"),
        ]
        for value in candidates:
            if value is None:
                continue
            try:
                v = int(value)
                if v > 0:
                    return v
            except Exception:
                continue
        return default

    @staticmethod
    def _extract_country(payload: Dict[str, Any]) -> Optional[str]:
        candidates: List[Any] = [
            payload.get("country"),
            (payload.get("metadata") or {}).get("country"),
            (payload.get("params") or {}).get("country"),
        ]
        for value in candidates:
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None

    @staticmethod
    def _extract_api_key(payload: Dict[str, Any]) -> str:
        candidates: List[Any] = [
            payload.get("api_key"),
            (payload.get("metadata") or {}).get("api_key"),
            (payload.get("params") or {}).get("api_key"),
        ]
        for value in candidates:
            if isinstance(value, str) and value.strip():
                return value.strip()
        auth = payload.get("authorization")
        if isinstance(auth, str) and auth.strip().lower().startswith("bearer "):
            return auth.strip()[7:].strip()
        return ""

    @staticmethod
    def _extract_text(payload: Dict[str, Any]) -> str:
        for key in ("query", "text", "message", "content"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    @staticmethod
    def _extract_image_url(payload: Dict[str, Any]) -> str:
        image_url = payload.get("image_url")
        if isinstance(image_url, str) and image_url.strip():
            return image_url.strip()

        for key in ("attachments", "files", "images"):
            items = payload.get(key)
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict):
                    continue
                url = item.get("url") or item.get("image_url")
                if not (isinstance(url, str) and url.strip()):
                    continue
                media_type = str(item.get("type", "")).lower()
                mime_type = str(item.get("mime_type", "")).lower()
                if "image" in media_type or "image/" in mime_type:
                    return url.strip()
        return ""

    @staticmethod
    def _extract_supplement_sql_flag(payload: Dict[str, Any]) -> Optional[bool]:
        meta = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
        params = payload.get("params") if isinstance(payload.get("params"), dict) else {}
        for key in ("supplement_sql_search", "sql_supplement"):
            for src in (payload, meta, params):
                if key not in src or src[key] is None:
                    continue
                v = src[key]
                if isinstance(v, bool):
                    return v
                if isinstance(v, (int, float)):
                    return bool(v)
                if isinstance(v, str):
                    s = v.strip().lower()
                    if s in ("1", "true", "yes", "on"):
                        return True
                    if s in ("0", "false", "no", "off"):
                        return False
        return None

    @staticmethod
    def _extract_sql_supplement_query(payload: Dict[str, Any]) -> str:
        meta = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
        params = payload.get("params") if isinstance(payload.get("params"), dict) else {}
        for src in (payload, meta, params):
            q = src.get("sql_supplement_query")
            if isinstance(q, str) and q.strip():
                return q.strip()
        return ""

    def run_from_chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("payload must be a dict")

        from_payload = self._extract_api_key(payload)
        api_key = from_payload if from_payload else None

        country = self._extract_country(payload)
        top_k = self._extract_top_k(payload)
        text = self._extract_text(payload)
        image_url = self._extract_image_url(payload)
        sup_sql = self._extract_supplement_sql_flag(payload)
        sql_q = self._extract_sql_supplement_query(payload)
        sql_text_ctx = text or sql_q

        mode = str(payload.get("mode", "")).strip().lower()
        if mode in ("image", "image_url") and image_url:
            result = self.search_image_url(
                image_url=image_url,
                country=country,
                top_k=top_k,
                api_key=api_key,
                supplement_sql=sup_sql,
                supplement_query_text=sql_text_ctx,
            )
            result["mode"] = "image"
            result["image_url"] = image_url
            return self._attach_rfq_candidate(payload, result)
        if mode == "text" and text:
            result = self.search_text(
                text=text,
                country=country,
                top_k=top_k,
                api_key=api_key,
                supplement_sql=sup_sql,
            )
            result["mode"] = "text"
            result["text"] = text
            return self._attach_rfq_candidate(payload, result)

        if image_url:
            result = self.search_image_url(
                image_url=image_url,
                country=country,
                top_k=top_k,
                api_key=api_key,
                supplement_sql=sup_sql,
                supplement_query_text=sql_text_ctx,
            )
            result["mode"] = "image"
            result["image_url"] = image_url
            return self._attach_rfq_candidate(payload, result)
        if text:
            result = self.search_text(
                text=text,
                country=country,
                top_k=top_k,
                api_key=api_key,
                supplement_sql=sup_sql,
            )
            result["mode"] = "text"
            result["text"] = text
            return self._attach_rfq_candidate(payload, result)

        raise ValueError(
            "No searchable input found. Provide text/query/message/content or image_url/attachments."
        )


if __name__ == "__main__":
    """
    简单命令行用法（在 egatee-search-skill 目录下）：
      文本: python egatee_search_skill.py text "power bank"
      带 API Key（环境变量 EGATEE_SEARCH_API_KEY）可跳过每日限额（库表校验通过后）
    """
    import sys

    try:
        import yaml
    except ImportError:
        yaml = None  # type: ignore[assignment]

    def _parse_chat_payload(raw: str) -> Dict[str, Any]:
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

        relaxed = re.sub(r"([{\s,])([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', raw)
        if yaml is not None:
            try:
                data = yaml.safe_load(relaxed)
                if isinstance(data, dict):
                    return data
            except Exception:
                pass
        else:
            raise ValueError(
                "Invalid chat payload (JSON parse failed). Install PyYAML for PowerShell-style payloads: pip install PyYAML"
            )

        raise ValueError("Invalid chat payload. Use JSON string or @payload.json file.")

    if len(sys.argv) < 3:
        print("Usage:")
        print("  python egatee_search_skill.py text \"keyword\"")
        print("  python egatee_search_skill.py image \"path/to/file.jpg\"")
        print("  python egatee_search_skill.py image_url \"https://xx/xx.jpg\"")
        print("  python egatee_search_skill.py chat '{\"text\":\"power bank\"}'")
        print(
            "  （可选）设置 EGATEE_SEARCH_API_KEY，经 Java 网关 getChatHistoryByApiKey 校验通过后跳过每日限额"
        )
        raise SystemExit(1)

    mode = sys.argv[1].strip().lower()
    arg = " ".join(sys.argv[2:]).strip()
    skill = EgateeSearchSkill()
    rem = skill.remaining_today()
    print(f"Remaining today: {'unlimited (verified api key)' if rem is None else rem}")
    if mode == "text":
        result = skill.search_text(arg)
    elif mode == "image":
        result = skill.search_image(arg)
    elif mode == "image_url":
        result = skill.search_image_url(arg)
    elif mode == "chat":
        if arg.startswith("@"):
            payload_text = Path(arg[1:]).read_text(encoding="utf-8")
            payload = _parse_chat_payload(payload_text)
        else:
            payload = _parse_chat_payload(arg)
        result = skill.run_from_chat(payload)
    else:
        raise SystemExit("mode must be 'text' or 'image' or 'image_url' or 'chat'")
    print(json.dumps(result, ensure_ascii=False, indent=2))
