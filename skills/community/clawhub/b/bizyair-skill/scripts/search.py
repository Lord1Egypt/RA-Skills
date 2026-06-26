"""search.py — 远端候选搜索 + 评分 + JSON/Markdown 候选回包。

被 app.py --pick-image-candidates / --pick-video-candidates 调起。

主要逻辑：
  - 接受用户的"几个短词"作为查询（通常 LLM 把用户原话拆出来再喂进来）
  - 调远端 bizy_models/community 列表 API，按短词逐个搜索（顺序而非并发，速率友好）
  - 对每个候选打分：query 命中度 + 路由匹配 + 输入需求 + freshness（新发布加权）
  - 按格式回包：reply_format='markdown' 给用户看、'json' 给 LLM 选

挑选逻辑里有大量启发式（classify_route_match / candidate_freshness_hint 等），
跟具体业务模型强相关，谨慎修改。
"""
from __future__ import annotations
import json, re
from typing import Any

import api
import contract
import common
from common import SEARCH_MAX_ROUNDS, SEARCH_MIN_ROUNDS

def summarize_remote_candidate(item: dict[str, Any]) -> dict[str, Any]:
    versions = item.get('versions') or []
    first_version = versions[0] if versions else {}
    used_count = (item.get('counter') or {}).get('used_count')
    cover_urls = first_version.get('cover_urls') or []
    preview_image = None
    preview_video = None
    for url in cover_urls:
        low = str(url).lower()
        if preview_image is None and any((low.endswith(ext) or ext in low for ext in ['.webp', '.jpg', '.jpeg', '.png', '.gif'])):
            preview_image = url
        if preview_video is None and any((low.endswith(ext) or ext in low for ext in ['.mp4', '.mov', '.webm'])):
            preview_video = url
    return {'id': item.get('id'), 'name': item.get('name'), 'type': item.get('type'), 'base_model': first_version.get('base_model'), 'version_id': first_version.get('id'), 'sign': first_version.get('sign'), 'draft_id': first_version.get('draft_id'), 'used_count': used_count, 'available': first_version.get('available'), 'cover_urls': cover_urls, 'preview_image': preview_image, 'preview_video': preview_video, 'cover_image_url': preview_image, 'cover_video_url': preview_video, 'official_url': f"https://bizyair.cn/community/app/{item.get('id')}" if item.get('type') == 'Application' else None, 'stability': 'remote-only-analysis', 'layer': 'platform-result'}

def number_badge(index: int) -> str:
    return f'{index}.'

def candidate_cover_markdown(item: dict[str, Any]) -> str | None:
    image_url = item.get('preview_image') or item.get('cover_image_url')
    if not image_url:
        return None
    title = str(item.get('name') or 'BizyAir 候选')
    return f'![{title}]({image_url})'

def candidate_link(item: dict[str, Any]) -> str:
    if item.get('official_url'):
        return str(item.get('official_url'))
    if item.get('id'):
        return f"https://bizyair.cn/community/app/{item.get('id')}"
    return ''

def candidate_execution_hint(item: dict[str, Any]) -> str:
    kind = common.normalized_text(item.get('type'))
    if kind == 'workflow':
        return '⚠️ 命中的是 workflow，是否支持直接开跑还要继续确认'
    if item.get('available') is False:
        return '⚠️ 当前先继续看信息和参数'
    return '✅ 支持直接开跑'

def candidate_fit_summary(item: dict[str, Any], modality: str | None) -> str:
    reasons = item.get('remote_rank_reason') or []
    for raw in reasons:
        reason = str(raw or '').strip()
        if reason.startswith('match:'):
            term = reason.split(':', 1)[1].strip()
            if term:
                return f'和你这轮要找的“{term}”更贴近。'
        if reason == 'route:image-edit':
            return '更偏图片编辑、换背景、局部重绘这类路线。'
        if reason == 'route:commercial':
            return '更偏商品图、电商图、商业视觉这类路线。'
        if reason == 'route:lip-sync':
            return '更偏对口型、音频驱动和数字人口播这类路线。'
        if reason == 'route:first-last-frame':
            return '更偏首尾帧、过渡镜头这类路线。'
        if reason == 'pack:illustration':
            return '更偏插画、动漫、二次元这类画面。'
    base_model = str(item.get('base_model') or '').strip()
    if base_model:
        return f'底层路线更偏 {base_model}，适合作为这轮候选继续往下看。'
    if common.normalized_text(modality) == 'video':
        return '更适合你这轮这个视频方向，可以先从它开始看。'
    return '更适合你这轮这个图片方向，可以先从它开始看。'

def build_candidate_reply_markdown(candidates: list[dict[str, Any]], *, modality: str | None=None) -> str:
    if not candidates:
        return f'📭 **没找到合适的 BizyAir 对象**\n当前关键词没匹配到结果。\n\n可以换个更具体的说法再试一次。'
    heading = '🎯 **找到几个 BizyAir 对象**'
    intro = '候选如下（按 BizyAir 上 Most Used 排序，模态由你根据用户需求自行判断）：'
    lines = [heading, '', intro, '']
    for (idx, item) in enumerate(candidates, start=1):
        title = item.get('name') or item.get('title') or f"BizyAir 对象 {item.get('id')}"
        lines.append(f'{number_badge(idx)} **{title}**')
        lines.append('')
        lines.append(f'- **最适合做什么**：{candidate_fit_summary(item, modality)}')
        cover_md = candidate_cover_markdown(item)
        if cover_md:
            lines.append(f'- **封面图**：{cover_md}')
        lines.append(f'- **能否直接执行**：{candidate_execution_hint(item)}')
        link = candidate_link(item)
        if link:
            lines.append(f'- **链接**：{link}')
        if item.get('id'):
            lines.append(f"- **ID**：`{item.get('id')}`")
        lines.append('')
    lines.append('你看中哪个？直接告诉我编号或者 ID，我就接着往下帮你跑。')
    return '\n'.join(lines).strip()

def emit_candidate_reply(payload: dict[str, Any], *, reply_format: str='json') -> None:
    if common.normalized_text(reply_format) == 'markdown':
        print(payload.get('reply_markdown') or '')
        return
    print(json.dumps(payload, ensure_ascii=False, indent=2))

def deduplicate_app_workflow_pairs(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """识别同一个底层 app 的 (App, Workflow 壳) 重复对，每对只保留 Application。

    BizyAir 上经常有 workflow 壳页面包装一个真实 app（壳的 input_nodes=0，跑会失败），
    搜索结果里两者一起出现会占掉宝贵的候选位。

    去重信号优先级：
      ① 强信号：workflow.versions[0].ref_bizy_model_id 指向同结果集里的 app（铁证）
      ② 启发式：三条件叠加才生效（避免单 ID 距离条件的误杀）
                 - 完全同名（normalized_text 相等）
                 - ID 数值相邻 (|id_a - id_b| <= 2)
                 - 一个 Application、一个 Workflow

    保留谁：保留 Application 丢 Workflow（app 通常是真实执行体，壳页面更可能跑失败）。
    """
    by_id: dict[str, dict[str, Any]] = {}
    for it in items:
        item_id = str(it.get('id') or '').strip()
        if item_id:
            by_id[item_id] = it
    drop: set[str] = set()

    # ① 强信号：ref_bizy_model_id 直接指向同结果集里的某个 app
    for it in items:
        if str(it.get('type') or '').lower() != 'workflow':
            continue
        first_version = (it.get('versions') or [{}])[0] if it.get('versions') else {}
        ref_id = first_version.get('ref_bizy_model_id')
        if ref_id is None:
            continue
        ref_str = str(ref_id).strip()
        if ref_str and ref_str in by_id and ref_str != str(it.get('id') or ''):
            drop.add(str(it.get('id') or ''))

    # ② 启发式：同名 + ID 数值相邻 + 一 app 一 workflow（三条件叠加才生效）
    items_with_int_id: list[tuple[int, dict[str, Any]]] = []
    for it in items:
        raw_id = str(it.get('id') or '').strip()
        if raw_id.isdigit():
            items_with_int_id.append((int(raw_id), it))
    for i, (id_a, item_a) in enumerate(items_with_int_id):
        if str(id_a) in drop:
            continue
        for (id_b, item_b) in items_with_int_id[i + 1:]:
            if str(id_b) in drop or abs(id_b - id_a) > 2:
                continue
            type_a = str(item_a.get('type') or '').lower()
            type_b = str(item_b.get('type') or '').lower()
            if {type_a, type_b} != {'application', 'workflow'}:
                continue
            name_a = common.normalized_text(item_a.get('name'))
            name_b = common.normalized_text(item_b.get('name'))
            if not name_a or name_a != name_b:
                continue
            # 三条件全满足，丢 workflow 留 app
            drop.add(str(id_a) if type_a == 'workflow' else str(id_b))

    if not drop:
        return items
    return [it for it in items if str(it.get('id') or '') not in drop]


def format_remote_candidates(items: list[dict[str, Any]], semantic_plan: dict[str, Any], modality: str | None, limit: int | None=None) -> list[dict[str, Any]]:
    """取前 N 条并格式化输出。排序依赖 API 原始顺序（sort=Most Used）。"""
    selected = items[:limit] if limit is not None else items
    return [summarize_remote_candidate(item) for item in selected]

def clean_search_term(value: str) -> str:
    text = str(value or '').strip()
    text = re.sub('^[\\-\\*\\d\\.\\)\\(]+\\s*', '', text)
    text = text.strip('`\'"“”‘’[](){}')
    text = re.sub('\\s+', ' ', text).strip()
    return text[:48]

def derive_subword_variants(term: str) -> list[str]:
    """从一个多 token 复合词派生短子词，用作长词命中失败时的兜底关键词。

    场景：BizyAir 服务端 keyword 搜索基本走 app 名字 fuzzy 匹配，
    传 'Flux Kontext Max' 这种长词如果库里没有 app 同时含 'flux' 和 'kontext' 和 'max'，
    就会 0 命中。通过把它拆成 ['Flux', 'Kontext', 'Max'] 这种短子词追加到搜索列表，
    可以让长词不命中时仍然有机会捞到 name 只含 'Kontext' 的应用。

    规则：按空白拆 token，丢掉过短（< 2 字符）和纯标点的，去重，保持原顺序。
    """
    text = str(term or '').strip()
    if not text or not re.search('\\s', text):
        return []
    raw_tokens = re.split('\\s+', text)
    seen: set[str] = set()
    variants: list[str] = []
    for tok in raw_tokens:
        cleaned = clean_search_term(tok)
        if not cleaned or cleaned == text:
            continue
        if len(cleaned) < 2:
            continue
        if not re.search('[\\w\\u4e00-\\u9fff]', cleaned):
            continue
        low = cleaned.lower()
        if low in seen:
            continue
        seen.add(low)
        variants.append(cleaned)
    return variants

def build_candidate_search_terms(query: str, modality: str | None=None) -> list[str]:
    raw = str(query or '').strip()
    if not raw:
        return ['图生视频' if common.normalized_text(modality) == 'video' else '通用出图']
    normalized = raw
    for sep in ['\n', '\r', '，', ',', '、', '|', '；', ';', '/']:
        normalized = normalized.replace(sep, '\n')
    terms: list[str] = []
    if normalized != raw:
        for part in normalized.splitlines():
            cleaned = clean_search_term(part)
            if cleaned:
                common.add_unique_key(terms, cleaned)
    else:
        cleaned = clean_search_term(raw)
        if cleaned:
            common.add_unique_key(terms, cleaned)
    if not terms:
        common.add_unique_key(terms, '图生视频' if common.normalized_text(modality) == 'video' else '通用出图')
    # 兜底 fan-out：当原始词数没用满 SEARCH_MAX_ROUNDS 时，把每个多 token 复合词
    # 的子词也补进去（追加在原词后面，先搜全名再退到子词）。LLM 没主动拆短词时也能补救。
    if len(terms) < SEARCH_MAX_ROUNDS:
        for original in list(terms):
            for variant in derive_subword_variants(original):
                if len(terms) >= SEARCH_MAX_ROUNDS:
                    break
                common.add_unique_key(terms, variant)
            if len(terms) >= SEARCH_MAX_ROUNDS:
                break
    return terms[:SEARCH_MAX_ROUNDS]

def infer_high_confidence_route_from_terms(terms: list[str], modality: str | None, *, has_image: bool=False, has_audio: bool=False) -> str:
    joined = ' '.join((common.normalized_text(term) for term in terms if term))
    if common.normalized_text(modality) == 'video':
        if has_audio or any((x in joined for x in ['对口型', '口播', '嘴型', '音频驱动', 'lip sync', 'lip-sync', '图片加音频'])):
            return 'lip-sync-or-audio-video'
        if any((x in joined for x in ['首尾帧', '首帧', '尾帧', '帧间过渡', '转场'])):
            return 'first-last-frame-video'
        if has_image or any((x in joined for x in ['图生视频', '照片动起来', '图片动起来', 'image to video'])):
            return 'image-to-video'
        return 'video-search'
    if has_image or any((x in joined for x in ['改图', '重绘', '局部重绘', '换背景', '图生图', '修图', '抠图', '扩图', '参考图', 'inpaint', 'image edit'])):
        return 'image-edit-or-reference-search'
    if any((x in joined for x in ['商品图', '产品图', '电商', '主图', '详情页', '白底', '模特上身', 'product image', 'ecommerce'])):
        return 'commercial-image-search'
    if any((x in joined for x in ['字体', '中文排版', '文字海报', 'logo字', 'text layout', 'font design'])):
        return 'text-capable-image-search'
    return 'image-search'

def build_semantic_plan(query: str, modality: str | None, *, has_image: bool=False, has_audio: bool=False) -> dict[str, Any]:
    search_terms = build_candidate_search_terms(query, modality)
    recommended_route = infer_high_confidence_route_from_terms(search_terms, modality, has_image=has_image, has_audio=has_audio)
    required_input_kind = None
    primary_intent = recommended_route if recommended_route not in {'image-search', 'video-search'} else 'generic-video' if common.normalized_text(modality) == 'video' else 'generic-image'
    reasoning_summary = f"搜索词={', '.join(search_terms[:SEARCH_MAX_ROUNDS])}"
    if recommended_route not in {'image-search', 'video-search'}:
        reasoning_summary += f'，高确定性路由={recommended_route}'
    return {'query': str(query or '').strip(), 'modality': common.normalized_text(modality) or None, 'has_image': has_image, 'has_audio': has_audio, 'primary_intent': primary_intent, 'secondary_intents': [], 'matched_packs': [], 'search_queries': search_terms, 'negative_queries': [], 'local_hints': [], 'recommended_route': recommended_route, 'required_input_kind': required_input_kind, 'reasoning_summary': reasoning_summary}

def is_remote_candidate_object(item: dict[str, Any]) -> bool:
    return str(item.get('type') or '') in {'Application', 'Workflow'}


def _cmd_pick_remote_candidates(query: str, modality: str, *, api_key_arg: str | None=None, remote_source: str='community', page: int=1, page_size: int=24, sort: str | None=None, base_models: str | None=None, limit: int=10, reply_format: str='json') -> None:
    """统一的 AI 应用候选搜索（图片 / 视频共用）。

    设计变化（vs 旧版 cmd_pick_image_candidates / cmd_pick_video_candidates）：
    - 删除客户端 modality 启发式过滤（is_remote_image_candidate / is_remote_video_candidate）。
      AI 应用没有权威 modality 字段，启发式靠 4 个散乱关键词列表猜，准确率低且常误杀。
      抽样验证：用户搜「kling」想要图片 → 服务端只有 kling 视频版 → 旧版直接 0 条卡死，
      新版让 LLM 看到 base_model=Kling 自己判断要不要再帮用户搜 Flux/Seedream。
    - 0 命中拆词兜底：服务端 keyword 不支持空格分词（如「Seedream 文生图」直接 0 条），
      命中 0 条时自动用 derive_subword_variants 拆词分别试。
    - modality 参数只影响 build_semantic_plan 的 search_queries 生成，不影响过滤。
    """
    api_key = api.require_api_key(api_key_arg)
    semantic_plan = build_semantic_plan(query, modality)
    resolved_sort = sort or ('Auto' if common.normalized_text(remote_source) == 'official' else 'Most Used')
    search_terms = list(semantic_plan.get('search_queries', [])) or build_candidate_search_terms(query, modality)
    collected: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    attempts: list[dict[str, Any]] = []
    internal_cap = max(limit * 4, 30)
    max_pages_per_term = 2
    terms_to_search = list(search_terms[:SEARCH_MAX_ROUNDS])

    def run_term(term: str) -> int:
        """跑一个 keyword，返回这一轮新增的候选数。"""
        term_added = 0
        for current_page in range(page, page + max_pages_per_term):
            resp = api.fetch_remote_models(api_key, remote_source=remote_source, page=current_page, page_size=page_size, keyword=term, sort=resolved_sort, model_types=None, base_models=base_models)
            resp_data = api.extract_result_data(resp) if isinstance(resp, dict) else {}
            items = resp_data.get('list', [])
            attempt = {'keyword': term, 'raw_total': resp_data.get('total'), 'page': resp_data.get('current'), 'raw_page_count': len(items), 'accepted_count': 0}
            attempts.append(attempt)
            if not items:
                break
            for item in items:
                item_id = str(item.get('id'))
                if not item_id or item_id in seen_ids:
                    continue
                if not is_remote_candidate_object(item):
                    continue
                seen_ids.add(item_id)
                collected.append(item)
                attempt['accepted_count'] += 1
                term_added += 1
            if len(collected) >= internal_cap:
                break
        return term_added

    for (term_index, term) in enumerate(terms_to_search, start=1):
        run_term(term)
        if term_index < SEARCH_MIN_ROUNDS:
            continue
        if len(collected) >= internal_cap:
            break

    # 兜底：所有原始 search_terms 都 0 命中 → 拆词重试一轮
    if not collected:
        fallback_terms: list[str] = []
        for original in terms_to_search:
            for variant in derive_subword_variants(original):
                if variant not in terms_to_search and variant not in fallback_terms:
                    fallback_terms.append(variant)
                if len(fallback_terms) >= SEARCH_MAX_ROUNDS:
                    break
            if len(fallback_terms) >= SEARCH_MAX_ROUNDS:
                break
        for term in fallback_terms:
            run_term(term)
            if collected:
                break

    collected = deduplicate_app_workflow_pairs(collected)
    platform_results = format_remote_candidates(collected, semantic_plan, modality, limit=limit)
    source_tag = 'remote-pick-video' if common.normalized_text(modality) == 'video' else 'remote-pick'
    payload = {'source': source_tag, 'remote_source': remote_source, 'query': query, 'semantic_plan': semantic_plan, 'expanded_keywords': search_terms, 'attempts': attempts, 'limit': limit, 'platform_results': platform_results, 'candidates': platform_results, 'raw_total': sum((a.get('raw_total') or 0 for a in attempts)), 'reply_markdown': build_candidate_reply_markdown(platform_results, modality=modality)}
    emit_candidate_reply(payload, reply_format=reply_format)


def cmd_pick_image_candidates(query: str, *, api_key_arg: str | None=None, remote_source: str='community', page: int=1, page_size: int=24, sort: str | None=None, base_models: str | None=None, limit: int=10, reply_format: str='json'):
    _cmd_pick_remote_candidates(query, 'image', api_key_arg=api_key_arg, remote_source=remote_source, page=page, page_size=page_size, sort=sort, base_models=base_models, limit=limit, reply_format=reply_format)


def cmd_pick_video_candidates(query: str, *, api_key_arg: str | None=None, remote_source: str='community', page: int=1, page_size: int=24, sort: str | None=None, base_models: str | None=None, limit: int=10, reply_format: str='json'):
    _cmd_pick_remote_candidates(query, 'video', api_key_arg=api_key_arg, remote_source=remote_source, page=page, page_size=page_size, sort=sort, base_models=base_models, limit=limit, reply_format=reply_format)
