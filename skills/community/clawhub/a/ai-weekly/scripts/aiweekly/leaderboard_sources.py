"""单榜源解析器：每个榜站一个 fetch_*，互不影响。

从 leaderboard.py 抽出（P1#1 Phase 3）。编排、缓存、快照兜底在 `leaderboard.py`。

约定：
- 每个 `fetch_*` 失败一律返回 None（**不抛**），由编排层决定回退缓存还是标注「暂无实时数据」；
- 解析层的 `except Exception` 为**有意的 best-effort 网络容错**（P0#8 允许并已注释）；
- 解析出的每行经 `_enrich_cost` 注入成本/上下文等字段，未匹配家族一律 None（绝不编造）。
"""
import html
import json
import os
import re

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - 依赖缺失时由上层 CLI 统一提示
    BeautifulSoup = None

from aiweekly.utils import _http_get, _retry_fetch
from aiweekly.news import _is_open_source
from aiweekly.model_meta import _enrich_cost
from aiweekly.canon import _norm_model, ORG_PREFIXES, _SUFFIX_RE  # P2-1：归一原语下沉到叶子模块

# ============ 榜源地址 ============
# 综合榜：LMArena（人类偏好 Elo）+ Artificial Analysis 智能指数
# 开源榜：LLM-Stats（主）/ DataLearner（备）/ Hugging Face Open LLM Leaderboard
LM_ARENA_URL = "https://lmarena.ai/leaderboard"
AA_URL = "https://artificialanalysis.ai/"
HF_DS_API = ("https://datasets-server.huggingface.co/rows"
             "?dataset=open-llm-leaderboard/contents&config=default"
             "&split=train")
HF_LEADERBOARD_URL = "https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard"
# 开源模型榜新源（替代 HF，用户指定）：LLM-Stats（含 score/license/context/价格）、DataLearner（含 HLE/开源情况）
DATALARNER_URL = "https://www.datalearner.com/leaderboards/open-source"
LLMSTATS_URL = "https://llm-stats.com/leaderboards/open-llm-leaderboard"

# 国内可直连榜源（可直接解析站点）。注意：OpenCompass / SuperCLUE / ModelScope 官网
# 均为 JS 渲染 SPA，其数据 API 无法用简单 HTTP 稳定抓取（返回 SPA 兜底 HTML / 需鉴权），
# 故这些 live 解析器按「尽力而为」实现——连不上或拿到的不是结构化数据就返回 None，
# 由多源池优雅降级到国内快照（cn_leaderboard_snapshot.json）或缓存。
OC_LLM_URL = "https://rank.opencompass.org.cn/leaderboard-llm"
SV_GENERAL_URL = "https://www.superclueai.com/generalpage"
MS_MODELS_URL = "https://modelscope.cn/models"
# 官方开放 API（实测可用；/api/v1/models 是 404，别再用旧路径）
MS_OPENAPI_URL = "https://www.modelscope.cn/openapi/v1/models"
HF_MIRROR_API = "https://hf-mirror.com/api/models"


# ============ 国内镜像（P0-3：海外源国内不可达时自动回退）============
# 键：源站 URL 前缀；值：镜像站对应前缀。_http_get_fallback 在主源失败时
# 按此表改写前缀重试，再不行才回退快照（已有逻辑）。
# 说明（2026-09-09 实测复核，务必以实测为准，勿凭想象加镜像）：
#  - hf-mirror.com 根域与 /api/models 实测 200 + JSON → **真实可用**；
#  - hf-mirror.com/datasets-server 实测 **401**（该路径不对外）→ datasets-server 无可用镜像；
#  - lmarena.org.cn 实测 **域名不存在**（ConnectionError）→ 曾在此登记，已移除；
#  - aa-cn.mirror.xyz 实测 200 但返回的是 **mirror.xyz 博客平台**页面（与 AA 无关），
#    属「假镜像」：不仅无用，一旦解析出内容还可能污染榜单 → 已移除。
# 教训：镜像必须逐个 curl 验证「域名存在 + 返回预期内容」，只看 HTTP 200 不够。
URL_REWRITES = {
    "https://huggingface.co": "https://hf-mirror.com",
}

# 无国内镜像、且境外网络不可达时须如实告知用户的源（不伪装成「暂无数据」）
NO_CN_MIRROR_SOURCES = {
    "lm": "LMArena（lmarena.ai）无官方国内镜像，国内环境通常需代理才能访问",
    "aa": "Artificial Analysis（artificialanalysis.ai）无官方国内镜像，国内环境通常需代理才能访问",
}

# 镜像总开关：设 LEADERBOARD_USE_MIRRORS=0 可关闭（调试 / 海外环境无需镜像）
_USE_MIRRORS = os.environ.get("LEADERBOARD_USE_MIRRORS", "1") != "0"


def _http_get_fallback(url: str, timeout: int = 45, opener=None) -> str:
    """抓取 URL：主源失败自动按 URL_REWRITES 改写前缀重试镜像（P0-3）。

    返回首个成功响应的正文；全部失败则抛出最后一个异常，由上层 fetch_*
    的 best-effort 块捕获并返回 None（回退缓存 / 快照）。所有候选都不静默吞掉，
    确保「主源+镜像都挂」时仍如实降级而非假装成功。
    """
    if not _USE_MIRRORS:
        return _http_get(url, timeout=timeout, opener=opener)
    candidates = [url]
    for orig, mirror in URL_REWRITES.items():
        if url.startswith(orig):
            candidates.append(mirror + url[len(orig):])
    last_err = None
    for cand in candidates:
        try:
            return _http_get(cand, timeout=timeout, opener=opener)
        except Exception as e:  # noqa: BLE001  候选失败继续试下一个（镜像可能不存在）
            last_err = e
            continue
    raise last_err or RuntimeError(f"所有源（含镜像）均不可达：{url}")


__all__ = [
    "LM_ARENA_URL", "AA_URL", "HF_DS_API", "HF_LEADERBOARD_URL",
    "DATALARNER_URL", "LLMSTATS_URL", "OC_LLM_URL", "SV_GENERAL_URL",
    "MS_MODELS_URL", "MS_OPENAPI_URL", "HF_MIRROR_API", "NO_CN_MIRROR_SOURCES",
    "URL_REWRITES", "_USE_MIRRORS", "_http_get_fallback",
    "ORG_PREFIXES", "_clean_model_slug", "_SUFFIX_RE",
    "_norm_model", "fetch_lmarena_ranking", "OPEN_SOURCE_MODEL_KEYWORDS", "_is_open_source_model",
    "fetch_aa_ranking", "fetch_hf_open_ranking", "_parse_table_rows", "_parse_ctx",
    "_parse_money", "fetch_llmstats_ranking", "DL_ORG_SPLIT", "_split_dl_org",
    "fetch_datalearner_ranking", "fetch_opencompass_ranking", "fetch_superclue_ranking", "fetch_modelscope_ranking",
    "fetch_hf_mirror_popular",
]


def _clean_model_slug(slug: str):
    """从 LMArena 的 'Anthropicclaude-fable-5' 这类拼接 slug 切出 (org, model)。"""
    for org in ORG_PREFIXES:
        if slug.lower().startswith(org.lower()):
            model = slug[len(org):].lstrip("-_ ").replace("-", " ").strip()
            return org, model[:60].title()
    return "", slug.replace("-", " ").strip()[:60].title()


# 代理与网络 IO 已迁移到 aiweekly.utils（_PROXY_OVERRIDE / _resolved_proxy / _configure_proxy /
# _build_opener / _http_get / _probe / _detect_region）。本文件顶部已 re-export。

def fetch_lmarena_ranking(top_n: int = 15):
    """LMArena 综合排名（人类偏好 Elo）。解析排行榜页面服务端渲染的表格。"""
    try:
        html = _http_get_fallback(LM_ARENA_URL, timeout=60)
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        if not tables:
            return None
        rows = tables[0].find_all("tr")
        out = []
        for row in rows[1:]:
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cells) < 2:
                continue
            try:
                rank = int(cells[1])
            except ValueError:
                continue
            org, model = _clean_model_slug(cells[0])
            if not model:
                continue
            out.append(_enrich_cost({
                "rank": rank, "model": model, "org": org,
                "open_source": _is_open_source(org) or _is_open_source_model(model),
            }))
            if len(out) >= top_n:
                break
        return out if out else None
    except Exception as e:
        print(f"  ⚠️ LMArena 抓取失败：{e}")
        return None


# 开源模型的品牌/系列关键词（用于从模型名直接判定开源，覆盖 AA 等无机构字段的来源）
OPEN_SOURCE_MODEL_KEYWORDS = [
    "llama", "qwen", "deepseek", "mistral", "magistral", "gemma", "phi", "yi-",
    "olmo", "nemotron", "command r", "glm", "kimi", "grok", "falcon", "baichuan",
    "chatglm", "internlm", "minicpm", "vicuna", "wizardlm", "zephyr", "mixtral",
    "codellama", "cogvlm", "qwen3", "qwen2",
]


def _is_open_source_model(text: str) -> bool:
    """通过模型名/品牌关键词判定开源（与机构判定互补）。"""
    t = (text or "").lower()
    return any(k in t for k in OPEN_SOURCE_MODEL_KEYWORDS)


def fetch_aa_ranking(top_n: int = 15):
    """Artificial Analysis 智能指数（客观能力复合分）。

    数据全部来自 artificialanalysis.ai（源站本身即含成本/上下文/指数，未编造）：
      - 主页 data[] 数组：label + artificialAnalysisIntelligenceIndex + detailsUrl
      - 某模型详情页 data[] 数组（按 label 关联）：contextWindowTokens、pricing(inputPrice/outputPrice)
    """
    try:
        html = _http_get_fallback(AA_URL, timeout=45)
        # label + 智能指数 + 详情页 URL（用于二次抓取上下文/价格）
        entries = re.findall(
            r'"label":"([^"]+)","artificialAnalysisIntelligenceIndex":([\d.]+),'
            r'"detailsUrl":"([^"]+)"', html)
        if not entries:
            entries = [(m, s, "") for m, s in re.findall(
                r'"label":"([^"]+)","artificialAnalysisIntelligenceIndex":([\d.]+)', html)]
        if not entries:
            return None
        ranked = sorted(entries, key=lambda x: float(x[1]), reverse=True)

        # 上下文窗口 + 价格：从首个模型的详情页解析（按 label 关联）
        ctx_map, price_map = {}, {}
        detail_url = next((u for _, _, u in ranked if u), None)
        if detail_url:
            try:
                d = _http_get_fallback("https://artificialanalysis.ai" + detail_url, timeout=45)
                for m in re.finditer(r'"label":"([^"]+)","contextWindowTokens":(\d+)', d):
                    ctx_map[m.group(1)] = int(m.group(2))
                pre = re.compile(
                    r'"label":"([^"]+)"[^\[\]]*?"pricing":\[\s*\{"@type":"PropertyValue",'
                    r'"name":"inputPrice","value":([\d.]+)\},\s*\{"@type":"PropertyValue",'
                    r'"name":"outputPrice","value":([\d.]+)\}')
                for m in pre.finditer(d):
                    price_map[m.group(1)] = (float(m.group(2)), float(m.group(3)))
            except Exception as e:
                print(f"  ⚠️ AA 详情页（成本/上下文）抓取失败，相关字段将留空：{e}")

        out = []
        for i, (label, idx, _url) in enumerate(ranked[:top_n]):
            pin, pout = price_map.get(label, (None, None))
            row = {
                "rank": i + 1, "model": label, "score": round(float(idx), 1),
                "open_source": _is_open_source_model(label),
                "context": ctx_map.get(label),
                "price_in": pin, "price_out": pout,
            }
            out.append(_enrich_cost(row))
        return out if out else None
    except Exception as e:
        print(f"  ⚠️ Artificial Analysis 抓取失败：{e}")
        return None


def fetch_hf_open_ranking(top_n: int = 30):
    """Hugging Face Open LLM Leaderboard（开源模型榜）。

    该数据集 rows API 单次 length 上限为 100 且按字母序返回（非按分数），
    故分页拉取全部模型后再按平均分降序取 Top，避免只看到字母序靠前的弱模型。
    """
    try:
        out = []
        offset = 0
        while True:
            url = HF_DS_API + f"&offset={offset}&length=100"
            data = json.loads(_http_get_fallback(url, timeout=60))
            rows = data.get("rows", [])
            if not rows:
                break
            for r in rows:
                row = r.get("row", {})
                name = row.get("eval_name") or row.get("Model") or ""
                if not name:
                    continue
                if "_" in name:
                    org, model = name.split("_", 1)
                else:
                    org, model = "", name
                avg = row.get("Average ⬆️") or row.get("Average") or ""
                lic = row.get("Hub License") or row.get("License") or "—"
                try:
                    score = float(avg)
                except (ValueError, TypeError):
                    score = None
                model = model.replace("_", " ").strip()
                # 去掉精度/量化后缀噪声（bfloat16 / fp16 / awq ...）
                model = re.sub(r'\s+(bfloat16|float16|fp16|float32|int8|int4|'
                               r'awq|gptq|8bit|4bit)\b.*$', '', model, flags=re.I)
                out.append(_enrich_cost({
                    "model": model,
                    "org": org,
                    "score": score,
                    "license": lic,
                }))
            if len(rows) < 100:
                break
            offset += 100
            if offset > 2000:
                break
        if not out:
            return None
        scored = [o for o in out if o["score"] is not None]
        scored.sort(key=lambda x: x["score"], reverse=True)
        for i, o in enumerate(scored):
            o["rank"] = i + 1
        return scored[:top_n]
    except Exception as e:
        print(f"  ⚠️ Hugging Face 开源榜抓取失败：{e}")
        return None


def _find_col(header_map: dict, sub: str, fallback: int) -> int:
    """在表头名映射（列索引 -> 表头文本）中按子串定位列索引；找不到回退 fallback。"""
    for i, h in header_map.items():
        if sub in h.lower():
            return i
    return fallback


def _parse_table_rows(html: str):
    """从服务端渲染的 <table> 中提取所有行（每行为单元格文本列表）。"""
    tables = re.findall(r"<table[\s\S]*?</table>", html)
    if not tables:
        return []
    rows = []
    for tr in re.findall(r"<tr[\s\S]*?</tr>", tables[0]):
        cells = [re.sub(r"<[^>]+>", " ", c).strip() for c in
                 re.findall(r"<t[dh][\s\S]*?</t[dh]>", tr)]
        rows.append([c for c in cells if c != ""])
    return rows


def _parse_ctx(token: str):
    """'1.0M'->1_000_000；'128K'->128_000；'200000'->200000；否则 None。"""
    if not token:
        return None
    t = token.strip().upper().replace(",", "")
    try:
        if t.endswith("M"):
            return int(float(t[:-1]) * 1_000_000)
        if t.endswith("K"):
            return int(float(t[:-1]) * 1_000)
        return int(float(t))
    except ValueError:
        return None


def _parse_money(token: str):
    """'$3.00'->3.0；'—'/空->None。"""
    if not token:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", token)
    return float(m.group(1)) if m else None


# _parse_date_arg 已迁移到 aiweekly.utils（顶部已 re-export）。


def fetch_llmstats_ranking(top_n: int = 30):
    """LLM-Stats 开源模型榜（用户指定源）。

    实测表头（首列空占位，末列为机构；中间含众多基准列）：
        '' | Model | LLM Stats | Country | License | Context | Input $/M |
        Output $/M | Speed | ...（众多基准列）... | Organization
    含分数、机构、许可证、上下文、输入输出单价——直接注入榜单行（机构/成本/上下文/许可证）。

    修复：原先走 _parse_table_rows（逐行过滤空单元格），导致某行的空单元格被删掉、
    该行列索引与表头错位，机构列抓空。这里改用 BeautifulSoup 保留全部单元格
    （不过滤空单元格），按表头名称定位列，确保表头与数据行列索引严格对齐。
    """
    try:
        html = _http_get(LLMSTATS_URL, timeout=60)
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        if not table:
            return None
        rows = table.find_all("tr")
        if len(rows) < 2:
            return None
        # 定位表头：第一个含「Model」的行；记录数据起始行
        header_map, data_start = {}, None
        for ri, row in enumerate(rows):
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if any("model" in c.lower() for c in cells):
                for i, h in enumerate(cells):
                    header_map[i] = h
                data_start = ri + 1
                break
        if data_start is None:
            return None

        model_i = _find_col(header_map, "model", 1)
        score_i = _find_col(header_map, "llm stats", 2)
        org_i = _find_col(header_map, "organization", len(header_map) - 1)   # 机构：末列 Organization
        lic_i = _find_col(header_map, "license", 4)
        ctx_i = _find_col(header_map, "context", 5)
        in_i = _find_col(header_map, "input", 6)
        out_i = _find_col(header_map, "output", 7)
        out = []
        for row in rows[data_start:]:
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cells) <= max(model_i, score_i, lic_i, ctx_i, in_i, out_i):
                continue
            model = cells[model_i].strip()
            if not model or not re.search(r"[A-Za-z]", model):
                continue
            try:
                score = float(cells[score_i])
            except (ValueError, TypeError):
                score = None
            org = cells[org_i].strip() if len(cells) > org_i else ""
            lic = cells[lic_i].strip()
            ctx = _parse_ctx(cells[ctx_i])
            pin = _parse_money(cells[in_i])
            pout = _parse_money(cells[out_i])
            commercial = "可自部署" if ("open" in lic.lower() or "mit" in lic.lower()
                                        or "apache" in lic.lower()) else "—"
            out.append(_enrich_cost({
                "rank": len(out) + 1, "model": model, "org": org,
                "score": score, "license": lic, "context": ctx,
                "price_in": pin, "price_out": pout,
                "commercial": commercial, "open_source": True,
            }))
            if len(out) >= top_n:
                break
        return out if out else None
    except Exception as e:
        print(f"  ⚠️ LLM-Stats 开源榜抓取失败：{e}")
        return None


# DataLearner 将「模型名 + 机构名」拼接在模型列末尾（如 "Kimi K3Moonshot AI"），
# 机构总是拼在末尾，故按 endswith 切分，避免误伤模型名中的子串。
# 长词优先匹配（sorted by len desc），故「阿里巴巴」不会被「阿里」抢先截断留尾巴。
DL_ORG_SPLIT = [
    "Moonshot AI", "腾讯AI实验室", "智谱AI", "MiniMax", "DeepSeek", "阿里",
    "阿里巴巴", "百度", "字节跳动", "月之暗面", "深度求索", "StepFun", "阶跃",
    "阶跃星辰", "Mistral AI", "Meta", "OpenAI", "Anthropic",
    "Google", "xAI", "NVIDIA", "Microsoft", "Cohere", "01.AI", "Ai2",
    "Databricks", "NousResearch", "Zhipu", "Qwen", "Alibaba", "Tencent",
    "Grok", "Arcee",
]


def _split_dl_org(model: str):
    """从 DataLearner 合并的『模型名+机构名』切分机构（机构拼在末尾）。"""
    if not model:
        return "", model
    for p in sorted(DL_ORG_SPLIT, key=len, reverse=True):
        if model.endswith(p):
            m = model[: len(model) - len(p)].strip()
            if m:
                return p, m
    return "", model


def fetch_datalearner_ranking(top_n: int = 30):
    """DataLearner 开源模型榜（用户指定源，llm-stats 的备用源）。

    实测表头（共 10 列，首尾各一列空/占位）：
        '' | 排名 | 模型(含机构) | HLE | ARC-AGI-2 | FrontierMath | SWE-bench | τ²-Bench | 开源情况 | ''
    提供 HLE 综合分与「开源情况」（如 免费商用）作为分数与商用标注。

    注意：DataLearner 机构名拼在模型名末尾，且表格首尾有空列。这里用
    BeautifulSoup 保留全部单元格（不过滤空单元格），按表头名称定位列，
    避免页面结构漂移导致的错位。
    """
    try:
        html = _http_get(DATALARNER_URL, timeout=120)
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        if not table:
            return None
        rows = table.find_all("tr")
        if len(rows) < 2:
            return None
        # 定位表头：第一个含「模型」的行；同时记录数据起始行
        header_map, data_start = {}, None
        for ri, row in enumerate(rows):
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if "模型" in cells:
                for i, h in enumerate(cells):
                    header_map[i] = h
                data_start = ri + 1
                break
        if data_start is None:
            return None

        model_i = _find_col(header_map, "模型", 2)
        score_i = _find_col(header_map, "HLE", 3)
        open_i = _find_col(header_map, "开源情况", 8)
        out = []
        for row in rows[data_start:]:
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cells) <= max(model_i, score_i):
                continue
            model = cells[model_i].strip()
            if not model or not re.search(r"[A-Za-z]", model):
                continue
            try:
                score = float(cells[score_i])
            except (ValueError, TypeError):
                score = None
            org, clean_model = _split_dl_org(model)
            open_info = cells[open_i].strip() if len(cells) > open_i else "—"
            if not open_info:
                open_info = "—"
            out.append(_enrich_cost({
                "rank": len(out) + 1, "model": clean_model or model, "org": org,
                "score": score, "license": open_info, "context": None,
                "commercial": open_info, "open_source": True,
            }))
            if len(out) >= top_n:
                break
        return out if out else None
    except Exception as e:
        print(f"  ⚠️ DataLearner 开源榜抓取失败：{e}")
        return None



def fetch_opencompass_ranking(top_n: int = 15):
    """OpenCompass 司南 LLM 综合榜（国内可直连）。"""
    try:
        html = _http_get(OC_LLM_URL, timeout=40)
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        if not tables:
            return None  # SPA 未渲染出数据，降级
        rows = tables[0].find_all("tr")
        out = []
        for row in rows[1:]:
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cells) < 5:
                continue
            try:
                rank = int(cells[0])
            except ValueError:
                continue
            model = cells[1]
            if not model:
                continue
            org = cells[2] if len(cells) > 2 else ""
            open_src = "开源" in (cells[3] if len(cells) > 3 else "")
            try:
                score = float(cells[4])
            except ValueError:
                score = None
            out.append(_enrich_cost({
                "rank": rank, "model": model, "org": org,
                "open_source": open_src, "score": score,
            }))
            if len(out) >= top_n:
                break
        return out if out else None
    except Exception as e:
        print(f"  ⚠️ OpenCompass 抓取失败：{e}")
        return None


def fetch_superclue_ranking(top_n: int = 15):
    """SuperCLUE 中文通用能力总排行榜（国内可直连）。"""
    try:
        html = _http_get(SV_GENERAL_URL, timeout=40)
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        if not tables:
            return None
        rows = tables[0].find_all("tr")
        out = []
        for row in rows[1:]:
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cells) < 4:
                continue
            try:
                rank = int(cells[0])
            except ValueError:
                continue
            model = cells[1]
            if not model:
                continue
            org = cells[2] if len(cells) > 2 else ""
            open_src = "开源" in (cells[3] if len(cells) > 3 else "")
            # SuperCLUE 总分通常在第 4~5 列，取首个可解析浮点
            score = None
            for c in cells[4:7]:
                try:
                    score = float(c)
                    break
                except ValueError:
                    continue
            out.append(_enrich_cost({
                "rank": rank, "model": model, "org": org,
                "open_source": open_src, "score": score,
            }))
            if len(out) >= top_n:
                break
        return out if out else None
    except Exception as e:
        print(f"  ⚠️ SuperCLUE 抓取失败：{e}")
        return None


def fetch_modelscope_ranking(top_n: int = 15):
    """ModelScope 魔搭开源模型热度榜（国内可直连）。

    2026-09-09 重写：原先抓 `modelscope.cn/models` 页面再 BeautifulSoup 找链接，
    但该页是 SPA（服务端只回骨架），实测 **33 次调用 0 次成功** → 形同虚设。
    改用官方开放 API `openapi/v1/models`（实测 200 + JSON，含 downloads/likes/license/params），
    按下载热度排序。注意：这是**热度榜，不是能力基准**，score 存的是下载量。
    """
    url = (f"{MS_OPENAPI_URL}?PageSize={max(top_n, 20)}&PageNumber=1"
           f"&SortBy=Downloads")
    try:
        data = json.loads(_http_get(url, timeout=40))
        if not data.get("success"):
            return None
        models = (data.get("data") or {}).get("models") or []
        out = []
        for m in models:
            mid = (m.get("id") or "").strip()
            if not mid:
                continue
            org, _, tail = mid.rpartition("/")
            name = (m.get("display_name") or "").strip() or tail or mid
            out.append(_enrich_cost({
                "model": name,
                "org": org or "",
                "score": m.get("downloads"),          # 热度（下载量），非能力分
                "license": (m.get("license") or "—"),
                "open_source": True,
                "likes": m.get("likes"),
                "params": m.get("params"),
            }))
            if len(out) >= top_n:
                break
        return out if out else None
    except Exception as e:
        print(f"  ⚠️ ModelScope 抓取失败：{e}")
        return None


def fetch_hf_mirror_popular(top_n: int = 15):
    """Hugging Face 热门开源模型（走 hf-mirror.com，国内可直连）。

    背景：Open LLM Leaderboard 的 datasets-server 在国内不可达（hf-mirror 的
    datasets-server 路径实测 401），导致 hf 源国内成功率极低。
    本函数改走 hf-mirror 的 `/api/models`（实测 200 + JSON），按下载量取热门模型，
    只保留文本生成/对话类（过滤 embedding、tokenizer 等非 LLM 条目）。
    注意：这是**热度榜，不是基准评分**，score 存的是下载量。
    """
    url = f"https://hf-mirror.com/api/models?sort=downloads&limit={max(top_n * 4, 60)}"
    try:
        data = json.loads(_http_get(url, timeout=40))
        out = []
        for m in data:
            mid = (m.get("id") or "").strip()
            if not mid:
                continue
            tags = m.get("tags") or []
            # 只要文本生成/对话类，过滤 sentence-transformers / tokenizer 等
            if not any(t in ("text-generation", "conversational", "text2text-generation")
                       for t in tags):
                continue
            org, _, tail = mid.rpartition("/")
            out.append(_enrich_cost({
                "model": tail or mid,
                "org": org or "",
                "score": m.get("downloads"),          # 热度（下载量），非能力分
                "license": "—",
                "open_source": True,
                "likes": m.get("likes"),
            }))
            if len(out) >= top_n:
                break
        return out if out else None
    except Exception as e:
        print(f"  ⚠️ HF 镜像热门榜抓取失败：{e}")
        return None

