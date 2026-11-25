"""Read-only authoring feedback over the canonical graph, not a business verifier.

Suggestions expose already-declared links which a selected handoff would omit.
They never add dependencies, infer a join, confirm knowledge or execute SQL.
"""
from collections import Counter
import copy

from workbench.semantic_package import PackageError, asset_dependencies, count_grain_review


def evidence_origin(asset, sources):
    if asset.get("properties", {}).get("assertion_basis") == "model_inferred":
        return "model_inferred"
    origins = set()
    for item in asset.get("evidence", []):
        if item.get("type") == "manual":
            origins.add("operator_statement")
        elif item.get("source_id") in sources:
            fmt = sources[item["source_id"]]
            origins.add(fmt if fmt in {"ddl", "metadata"} else "document")
    return next(iter(origins)) if len(origins) == 1 else "mixed" if origins else "unattributed"


def modeling_guidance(stage, assets, knowledge, event, result):
    """Bound the feedback to this operation; never present a candidate as an applied edit."""
    changes = set((event or {}).get("changed_asset_ids", []))
    changed = [a for a in assets if a["id"] in changes]
    sources = knowledge["sources"]
    formats = {s["id"]: s["format"] for s in sources}
    group_ids = set(result.get("group_ids", []) or result.get("scan", {}).get("group_ids", []))
    groups = [g for g in knowledge["groups"] if g["id"] in group_ids and g["status"] == "pending" and not result.get("seeded")]
    candidates = [c["asset"] for g in groups for c in g["candidates"] if c.get("asset")]
    active = [a for a in changed if a["status"] != "retired"]
    focus = next((a for a in active if a.get("properties", {}).get("conflict_resolutions")), None)
    focus = focus or next((a for a in active if a["kind"] == "relation" and a.get("relation_type") != "physical_fk"), None)
    focus = focus or next((a for a in active if a["kind"] in {"metric", "rule", "mapping"}), None)
    focus = focus or next((a for a in changed if a["kind"] not in {"field", "dataset"} and a["status"] != "retired"), None)
    focus = focus or next((a for a in changed if a["status"] != "retired"), None)
    issue = None
    for key, code in (("unresolved_conflicts", "conflicting_sources"), ("knowledge_gaps", "missing_evidence")):
        for a in changed or candidates:
            value = a.get("properties", {}).get(key)
            if value and a["status"] != "retired":
                detail = value[0] if isinstance(value, list) else value
                if isinstance(detail, dict):
                    claims = detail.get("claims", [])
                    detail = " / ".join(str(c.get("claim") or c.get("quote") or "") for c in claims if isinstance(c, dict)) if isinstance(claims, list) else ""
                issue = {"kind": code, "asset_id": a["id"], "asset_name": a["name"],
                         "detail": str(detail)[:300]}
                focus = a
                break
        if issue:
            break
    if not issue:
        for a in changed or candidates:
            if a["status"] == "needs_review" or (a["status"] == "draft" and evidence_origin(a, formats) == "model_inferred"):
                issue = {"kind": "source_changed" if a["status"] == "needs_review" else "confirm_inference",
                         "asset_id": a["id"], "asset_name": a["name"]}
                focus = a
                break
    if stage == "edit" and not issue:
        root = next((a for a in changed if a["kind"] in {"metric", "mapping", "rule"} and a.get("refs") and a["status"] != "retired"), None)
        if root:
            for problem in inspect_model(assets, sources, asset_ids=[root["id"]])["issues"]:
                if problem["code"] in {"MULTI_DATASET_RELATION_REVIEW", "UNRESOLVED_JOIN_KEY", "JOIN_KEYS_OUTSIDE_CONTEXT"}:
                    issue = {"kind": "review_relationship", "asset_id": root["id"], "detail": problem["message"],
                             "related_ids": problem["asset_ids"][:5]}
                    focus = root
                    break
    if result.get("seeded") and not issue:
        # A schema import has no operator-selected subject. Open the table overview.
        focus = None
    action = ("repair_material" if result.get("parsed", {}).get("status") in {"failed", "needs_conversion"}
              else "review_candidates" if groups else "review_evidence" if issue else "choose_business_question_or_export" if result.get("seeded")
              else "interpret_material" if stage == "import" and result.get("batch_id") else "inspect_change" if changed else "none")
    return {"stage": stage, "changed_count": len(changes), "by_kind": dict(Counter(a["kind"] for a in changed)),
            "evidence_origins": dict(Counter(evidence_origin(a, formats) for a in changed)),
            "candidate_count": sum(len(g["candidates"]) for g in groups),
            "next_action": action, "attention": issue, "focus_id": focus["id"] if focus and focus["id"] in changes else None}


def inspect_model(assets, sources, *, asset_ids=None):
    if not isinstance(assets, list) or any(not isinstance(a, dict) or not isinstance(a.get('id'), str) for a in assets):
        raise PackageError('INVALID_MODEL', 'Inspect requires canonical asset objects / 检查需要有效资产列表')
    index = {a['id']: a for a in assets}
    if len(index) != len(assets):
        raise PackageError('INVALID_MODEL', 'Duplicate asset IDs / 资产身份重复')
    roots = list(dict.fromkeys(asset_ids if asset_ids is not None else
                               [a['id'] for a in assets if a.get('status') != 'retired']))
    if any(not isinstance(aid, str) or aid not in index for aid in roots):
        raise PackageError('UNKNOWN_ASSET', 'Choose actual asset IDs from state --summary / 请使用摘要中的实际资产 ID')
    required, missing, queue = set(), [], list(roots)
    while queue:
        aid = queue.pop()
        if aid in required:
            continue
        if aid not in index:
            missing.append(aid)
            continue
        required.add(aid)
        queue.extend(asset_dependencies(index[aid]))
    issues = []

    def issue(code, ids, message, *, severity='advisory', **extra):
        issues.append(dict(code=code, asset_ids=sorted(set(ids)), severity=severity,
                           message=message, **extra))

    if missing:
        issue('MISSING_DEPENDENCY', missing, 'Referenced assets are absent / 已声明的依赖不存在', severity='blocker')
    unconfirmed = sorted(aid for aid in required if index[aid].get('status') != 'confirmed')
    if unconfirmed:
        issue('UNCONFIRMED_ASSETS', unconfirmed,
              'Review supported definitions as a group under existing authorization; unknown meaning stays draft / '
              '按已有授权成组核对有据定义；业务含义未知的部分保留草稿', severity='blocker')
    for aid in sorted(required):
        properties = index[aid].get("properties", {})
        if properties.get("unresolved_conflicts"):
            issue("UNRESOLVED_CONFLICT", [aid], "Compare cited sources and record the applicable scope / 对照各方原文并记录适用范围", severity="blocker")
        if properties.get("knowledge_gaps"):
            issue("DECLARED_KNOWLEDGE_GAP", [aid], "Review the declared gaps for this question / 核对当前问题依赖的已知缺口",
                  questions=properties["knowledge_gaps"])

    from workbench.semantic_package import _source_index, physical_fk_issues
    for problem in physical_fk_issues(index, {}, _source_index([s for s in sources if s.get("format") in {"ddl", "metadata"}]), selected=required):
        details = dict(problem)
        code, aid, message = (details.pop(key) for key in ("code", "asset_id", "message"))
        issue(code, [aid], message, severity=details.pop("severity", "blocker"), **details)

    # Dataset membership comes only from explicit field references, never names.
    field_tables = {aid: {ref for ref in a.get('refs', []) if ref in index and index[ref]['kind'] == 'dataset'}
                    for aid, a in index.items() if a['kind'] == 'field'}
    touched = set().union(*(field_tables.get(aid, set()) for aid in required)) if required else set()
    mapping_candidates = [a['id'] for a in assets if a['kind'] == 'mapping' and a.get('status') != 'retired'
                          and a['id'] not in required and a.get('from') in required and a.get('to') in required]
    if mapping_candidates:
        issue('MAPPINGS_OUTSIDE_CONTEXT', mapping_candidates,
              'Existing mappings between selected definitions and fields are not required dependencies; '
              'include relevant mappings in the root refs / 当前定义和字段之间已有映射未进入上下文；将相关映射加入根资产 refs')
    relation_candidates = []
    adjacency = {key: set() for key in touched}
    for a in assets:
        if a['kind'] != 'relation' or a.get('status') == 'retired':
            continue
        left, right = a.get('from'), a.get('to')
        both_selected = left in required and right in required
        connects_tables = left in touched and right in touched
        if a['id'] not in required and (both_selected or connects_tables):
            relation_candidates.append(a['id'])
        if a['id'] in required and connects_tables:
            adjacency[left].add(right)
            adjacency[right].add(left)
        if a['id'] in required and a.get('relation_type') == 'physical_fk':
            needed = []
            for endpoint, field_key in [('from', 'from_fields'), ('to', 'to_fields')]:
                table_id = a.get(endpoint)
                columns = a.get('properties', {}).get(field_key)
                for column in columns if isinstance(columns, list) else []:
                    matches = [fid for fid, tables in field_tables.items() if table_id in tables
                               and index[fid].get("status") != "retired"
                               and index[fid].get("properties", {}).get("column") == column]
                    needed += [fid for fid in matches if fid not in required]
            if needed:
                issue('JOIN_KEYS_OUTSIDE_CONTEXT', needed,
                      'Some key fields are outside the explicitly selected graph; scoped export includes them / '
                      '部分连接字段位于显式选择范围外；按范围导出时会自动纳入', relation_id=a['id'])
    if relation_candidates:
        issue('RELATIONS_OUTSIDE_CONTEXT', relation_candidates,
              'Existing links between selected endpoints are omitted. Review their purpose before adding refs; '
              'a physical FK is not a business relationship / 所选端点之间已有关系未交付；核对用途后引用，物理外键不等于业务含义')
    if len(touched) > 1:
        visited, queue = set(), [min(touched)]
        while queue:
            key = queue.pop()
            if key not in visited:
                visited.add(key)
                queue.extend(adjacency.get(key, set()) - visited)
        if visited != touched:
            issue('MULTI_DATASET_RELATION_REVIEW', touched,
                  'Fields span datasets without a connected declared table path. Check identity, join keys, '
                  'cardinality, time alignment and fanout; independent aggregates may legitimately stay separate / '
                  '字段跨表但已声明表关系未连通；核对身份、连接键、基数、时间和重复累计，独立汇总可保持分离')

    sql_assets = [aid for aid in required if any(key.casefold() == 'sql' or key.casefold().endswith('_sql')
                  for key in index[aid].get('properties', {}))]
    if sql_assets:
        issue('UNTRACKED_SQL_TEXT', sql_assets,
              'Free-form SQL text is not parsed or executed and does not declare dependencies. Bind the used '
              'fields, mappings and relations through refs / SQL 文本不被解析或执行，也不自动声明依赖；请通过 refs 绑定实际字段、映射和关系')
    for aid in sorted(required):
        asset = index[aid]
        if asset['kind'] == 'metric':
            review = count_grain_review(asset)
            if review:
                issue(review['code'], [aid], review['message'], grain_ids=review['grain_ids'], aggregation=review['aggregation'])
            values = [asset.get('properties', {}).get(key) for key in ('inclusions', 'exclusions', 'time_scope')]
            if all(isinstance(v, str) and v.strip() for v in values) and len({v.strip() for v in values}) == 1:
                issue('UNDISTINGUISHED_METRIC_PROPERTIES', [aid],
                      'Inclusions, exclusions and time scope repeat the same text. Extract their distinct '
                      'supported meanings or record what is unknown / 包含项、排除项和时间范围重复同一段文字；'
                      '请分别提取有据含义，未明确的部分标为未知')
    sources_by_id = {s['id']: s for s in sources}
    material_texts = {}
    for source in sources:
        revision = next((r for r in source.get('revisions', []) if r['revision'] == source.get('current_revision')), {})
        texts = [f.get('text', '') for f in revision.get('parsed', {}).get('fragments', [])]
        for text in texts + ['\n'.join(texts)]:
            normalized = ' '.join(text.split())
            if len(normalized) >= 30:
                material_texts.setdefault(normalized, set()).add(source['id'])
    changed_evidence = []
    for aid in sorted(required):
        for ev in index[aid].get('evidence', []):
            if ev.get('type') == 'manual':
                matching = material_texts.get(' '.join(ev.get('quote', '').split()))
                if matching:
                    issue('IMPORTED_TEXT_AS_MANUAL', [aid],
                          'Manual assertion repeats imported text without its revision link. If that material '
                          'supports the assertion, attach its actual source evidence for change tracking / '
                          '手工声明重复已导入文字但未绑定修订；若依据该材料，请关联真实来源以跟踪变更',
                          candidate_source_ids=sorted(matching), equivalence_verified=False)
            source = sources_by_id.get(ev.get('source_id'))
            if not source or not isinstance(ev.get('revision'), int) or source.get('current_revision', 0) <= ev['revision']:
                continue
            current = next((r for r in source.get('revisions', []) if r['revision'] == source['current_revision']), {})
            quote = ev.get('quote', '')
            locations = [copy.deepcopy(f.get('location')) for f in current.get('parsed', {}).get('fragments', [])
                         if quote and quote in f.get('text', '')]
            changed_evidence.append({'asset_id': aid, 'source_id': source['id'], 'source_name': source.get('name'),
                                     'cited_revision': ev['revision'], 'current_revision': source['current_revision'],
                                     'quote': quote, 'quote_still_present': bool(locations),
                                     'current_quote_locations': locations,
                                     'meaning_unchanged': 'not_established'})
    if changed_evidence:
        issue('NEWER_SOURCE_REVIEW', [r['asset_id'] for r in changed_evidence],
              'Compare the cited assertion and its current scope/exceptions; an unchanged quotation does not '
              'prove unchanged meaning / 核对断言及新上下文中的范围和例外；引文保留不等于含义未变')
    blockers = sum(i['severity'] == 'blocker' for i in issues)
    return {'status': 'empty' if not roots else 'needs_review' if issues else 'ready_for_review', 'read_only': True,
            'business_coverage': 'not_verified', 'roots': roots, 'required_asset_ids': sorted(required),
            'counts': dict(Counter(index[aid]['kind'] for aid in required)),
            'blockers': blockers, 'issues': issues, 'changed_evidence': changed_evidence,
            'next_step': 'Review relevant issues, batch edit authorized assets, then export selected roots / '
                         '核对相关提示，成组维护已授权资产，再按根资产导出',
            'boundary': 'Checks only declared assets and links. No inferred facts, automatic confirmation, '
                        'question-coverage proof or execution / 仅检查已声明资产和关系；不推断事实、不自动确认、不证明问题覆盖、不执行'}
