#!/usr/bin/env python3
"""
deal-closer CRM 知识图谱模块

构建客户关系网络图谱，支持实体管理、关系查询、组织架构映射、
影响力链路追踪和 Mermaid 可视化。
基于 ontology 理念，将CRM数据结构化为知识图谱。
"""

import json
import os
import sys
from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from utils import (
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    today_str,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    write_json_file,
)


# ============================================================
# 常量与配置
# ============================================================

GRAPH_FILE = "crm_graph.json"
DEALS_FILE = "deals.json"

# 实体类型
ENTITY_TYPES = ["Person", "Company", "Deal", "Meeting", "Email"]

# 关系类型及其描述
RELATION_TYPES = {
    "works_at": "就职于",
    "reports_to": "汇报给",
    "knows": "认识",
    "decision_maker_for": "是决策人",
    "competitor_of": "竞争对手",
    "partner_of": "合作伙伴",
    "referred_by": "由...推荐",
    "participated_in": "参与了",
    "related_to": "关联于",
    "contact_of": "是联系人",
}

# 默认图谱数据结构
_DEFAULT_GRAPH = {
    "entities": [],
    "relations": [],
    "version": "1.0.0",
    "last_updated": "",
}


# ============================================================
# 数据操作
# ============================================================

def _get_graph() -> Dict[str, Any]:
    """读取图谱数据。"""
    filepath = get_data_file(GRAPH_FILE)
    if not os.path.exists(filepath):
        return dict(_DEFAULT_GRAPH)
    data = read_json_file(filepath)
    if isinstance(data, list):
        return dict(_DEFAULT_GRAPH)
    return data


def _save_graph(graph: Dict[str, Any]) -> None:
    """保存图谱数据。"""
    graph["last_updated"] = now_iso()
    write_json_file(get_data_file(GRAPH_FILE), graph)


def _get_deals() -> List[Dict[str, Any]]:
    """读取所有商机数据。"""
    return read_json_file(get_data_file(DEALS_FILE))


def _find_entity(entities: List[Dict], entity_id: str) -> Optional[Dict]:
    """根据ID查找实体。"""
    for e in entities:
        if e.get("id") == entity_id:
            return e
    return None


def _find_entity_by_name(entities: List[Dict], name: str,
                          entity_type: str = "") -> Optional[Dict]:
    """根据名称查找实体。"""
    name_lower = name.lower().strip()
    for e in entities:
        if e.get("name", "").lower().strip() == name_lower:
            if not entity_type or e.get("type") == entity_type:
                return e
    return None


def _get_entity_relations(relations: List[Dict],
                           entity_id: str) -> List[Dict]:
    """获取与实体相关的所有关系。"""
    result = []
    for r in relations:
        if r.get("from_id") == entity_id or r.get("to_id") == entity_id:
            result.append(r)
    return result


# ============================================================
# 自动填充
# ============================================================

def _auto_populate_from_deals(graph: Dict[str, Any]) -> int:
    """从商机数据自动填充图谱实体和关系。

    Args:
        graph: 图谱数据。

    Returns:
        新增实体和关系的总数。
    """
    deals = _get_deals()
    entities = graph.get("entities", [])
    relations = graph.get("relations", [])
    added = 0

    # 已有实体名称索引
    existing_names = {
        (e.get("name", "").lower(), e.get("type", ""))
        for e in entities
    }

    for deal in deals:
        deal_id = deal.get("id", "")
        deal_name = deal.get("name", "")

        # 添加商机实体
        if (deal_name.lower(), "Deal") not in existing_names and deal_name:
            entity = {
                "id": f"GE_{deal_id}",
                "type": "Deal",
                "name": deal_name,
                "properties": {
                    "deal_id": deal_id,
                    "amount": deal.get("amount", 0),
                    "stage": deal.get("stage", ""),
                },
                "created_at": now_iso(),
            }
            entities.append(entity)
            existing_names.add((deal_name.lower(), "Deal"))
            added += 1

        # 添加联系人实体
        contact_name = deal.get("contact_name", "")
        contact_entity_id = None
        if contact_name and (contact_name.lower(), "Person") not in existing_names:
            contact_entity_id = generate_id("GE")
            entity = {
                "id": contact_entity_id,
                "type": "Person",
                "name": contact_name,
                "properties": {
                    "email": deal.get("contact_email", ""),
                    "phone": deal.get("contact_phone", ""),
                },
                "created_at": now_iso(),
            }
            entities.append(entity)
            existing_names.add((contact_name.lower(), "Person"))
            added += 1
        elif contact_name:
            # 查找已有实体
            existing = _find_entity_by_name(entities, contact_name, "Person")
            if existing:
                contact_entity_id = existing.get("id")

        # 添加公司实体
        company = deal.get("company", "")
        company_entity_id = None
        if company and (company.lower(), "Company") not in existing_names:
            company_entity_id = generate_id("GE")
            entity = {
                "id": company_entity_id,
                "type": "Company",
                "name": company,
                "properties": {},
                "created_at": now_iso(),
            }
            entities.append(entity)
            existing_names.add((company.lower(), "Company"))
            added += 1
        elif company:
            existing = _find_entity_by_name(entities, company, "Company")
            if existing:
                company_entity_id = existing.get("id")

        # 建立关系
        deal_entity = _find_entity_by_name(entities, deal_name, "Deal")
        deal_entity_id = deal_entity.get("id") if deal_entity else None

        # 联系人 -> 商机 关系
        if contact_entity_id and deal_entity_id:
            rel_key = (contact_entity_id, deal_entity_id, "contact_of")
            existing_rels = {
                (r.get("from_id"), r.get("to_id"), r.get("relation"))
                for r in relations
            }
            if rel_key not in existing_rels:
                relations.append({
                    "id": generate_id("GR"),
                    "from_id": contact_entity_id,
                    "to_id": deal_entity_id,
                    "relation": "contact_of",
                    "properties": {},
                    "created_at": now_iso(),
                })
                added += 1

        # 联系人 -> 公司 关系
        if contact_entity_id and company_entity_id:
            rel_key = (contact_entity_id, company_entity_id, "works_at")
            existing_rels = {
                (r.get("from_id"), r.get("to_id"), r.get("relation"))
                for r in relations
            }
            if rel_key not in existing_rels:
                relations.append({
                    "id": generate_id("GR"),
                    "from_id": contact_entity_id,
                    "to_id": company_entity_id,
                    "relation": "works_at",
                    "properties": {},
                    "created_at": now_iso(),
                })
                added += 1

    graph["entities"] = entities
    graph["relations"] = relations
    return added


# ============================================================
# BFS 查询
# ============================================================

def _bfs_query(graph: Dict[str, Any], start_id: str,
               max_depth: int = 3) -> Dict[str, Any]:
    """广度优先搜索查询相关实体。

    Args:
        graph: 图谱数据。
        start_id: 起始实体ID。
        max_depth: 最大搜索深度。

    Returns:
        搜索结果，包含实体和关系。
    """
    entities = graph.get("entities", [])
    relations = graph.get("relations", [])

    # 构建邻接表
    adjacency: Dict[str, List[Tuple[str, Dict]]] = {}
    for r in relations:
        from_id = r.get("from_id", "")
        to_id = r.get("to_id", "")
        if from_id not in adjacency:
            adjacency[from_id] = []
        if to_id not in adjacency:
            adjacency[to_id] = []
        adjacency[from_id].append((to_id, r))
        adjacency[to_id].append((from_id, r))

    visited: Set[str] = set()
    result_entities = []
    result_relations = []

    queue: deque = deque()
    queue.append((start_id, 0))
    visited.add(start_id)

    while queue:
        current_id, depth = queue.popleft()

        # 添加当前实体
        entity = _find_entity(entities, current_id)
        if entity:
            result_entities.append({
                **entity,
                "depth": depth,
            })

        if depth >= max_depth:
            continue

        # 遍历邻居
        for neighbor_id, relation in adjacency.get(current_id, []):
            if relation not in result_relations:
                result_relations.append(relation)

            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, depth + 1))

    return {
        "entities": result_entities,
        "relations": result_relations,
    }


# ============================================================
# 操作函数
# ============================================================

def add_entity(data: Dict[str, Any]) -> None:
    """添加实体到知识图谱。

    必填字段: type, name
    可选字段: properties

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("advanced_analytics", "CRM知识图谱"):
        return

    entity_type = data.get("type", "")
    name = data.get("name", "")

    if not entity_type:
        output_error("实体类型（type）为必填字段", code="VALIDATION_ERROR")
        return

    if entity_type not in ENTITY_TYPES:
        output_error(
            f"无效实体类型: {entity_type}，有效类型: {', '.join(ENTITY_TYPES)}",
            code="VALIDATION_ERROR",
        )
        return

    if not name:
        output_error("实体名称（name）为必填字段", code="VALIDATION_ERROR")
        return

    graph = _get_graph()
    entities = graph.get("entities", [])

    # 检查重复
    existing = _find_entity_by_name(entities, name, entity_type)
    if existing:
        output_error(
            f"已存在同名{entity_type}实体：{name}（ID: {existing.get('id')}）",
            code="DUPLICATE",
        )
        return

    entity = {
        "id": generate_id("GE"),
        "type": entity_type,
        "name": name,
        "properties": data.get("properties", {}),
        "created_at": now_iso(),
    }

    entities.append(entity)
    graph["entities"] = entities
    _save_graph(graph)

    output_success({
        "message": f"已添加{entity_type}实体「{name}」",
        "entity": entity,
    })


def add_relation(data: Dict[str, Any]) -> None:
    """添加关系到知识图谱。

    必填字段: from_id（或 from_name）, to_id（或 to_name）, relation
    可选字段: properties

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("advanced_analytics", "CRM知识图谱"):
        return

    relation_type = data.get("relation", "")
    if not relation_type:
        output_error("关系类型（relation）为必填字段", code="VALIDATION_ERROR")
        return

    if relation_type not in RELATION_TYPES:
        valid = ", ".join(f"{k}({v})" for k, v in RELATION_TYPES.items())
        output_error(
            f"无效关系类型: {relation_type}，有效类型: {valid}",
            code="VALIDATION_ERROR",
        )
        return

    graph = _get_graph()
    entities = graph.get("entities", [])
    relations = graph.get("relations", [])

    # 解析来源实体
    from_id = data.get("from_id", "")
    if not from_id and data.get("from_name"):
        entity = _find_entity_by_name(entities, data["from_name"])
        if entity:
            from_id = entity.get("id", "")

    # 解析目标实体
    to_id = data.get("to_id", "")
    if not to_id and data.get("to_name"):
        entity = _find_entity_by_name(entities, data["to_name"])
        if entity:
            to_id = entity.get("id", "")

    if not from_id:
        output_error("来源实体（from_id 或 from_name）未找到", code="NOT_FOUND")
        return

    if not to_id:
        output_error("目标实体（to_id 或 to_name）未找到", code="NOT_FOUND")
        return

    # 验证实体存在
    from_entity = _find_entity(entities, from_id)
    to_entity = _find_entity(entities, to_id)

    if not from_entity:
        output_error(f"未找到ID为 {from_id} 的实体", code="NOT_FOUND")
        return

    if not to_entity:
        output_error(f"未找到ID为 {to_id} 的实体", code="NOT_FOUND")
        return

    # 检查重复关系
    for r in relations:
        if (r.get("from_id") == from_id
                and r.get("to_id") == to_id
                and r.get("relation") == relation_type):
            output_error("该关系已存在", code="DUPLICATE")
            return

    relation = {
        "id": generate_id("GR"),
        "from_id": from_id,
        "to_id": to_id,
        "relation": relation_type,
        "relation_display": RELATION_TYPES.get(relation_type, relation_type),
        "properties": data.get("properties", {}),
        "created_at": now_iso(),
    }

    relations.append(relation)
    graph["relations"] = relations
    _save_graph(graph)

    output_success({
        "message": (
            f"已添加关系：{from_entity.get('name')} "
            f"--[{RELATION_TYPES.get(relation_type, relation_type)}]--> "
            f"{to_entity.get('name')}"
        ),
        "relation": relation,
    })


def query(data: Dict[str, Any]) -> None:
    """查询实体及其关联。

    必填字段: entity_id 或 name
    可选字段: max_depth（默认 3）

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("advanced_analytics", "CRM知识图谱查询"):
        return

    graph = _get_graph()
    entities = graph.get("entities", [])

    # 自动填充
    _auto_populate_from_deals(graph)
    _save_graph(graph)

    entity_id = data.get("entity_id", "")
    if not entity_id and data.get("name"):
        entity = _find_entity_by_name(entities, data["name"])
        if entity:
            entity_id = entity.get("id", "")

    if not entity_id:
        output_error("请提供 entity_id 或 name", code="VALIDATION_ERROR")
        return

    start_entity = _find_entity(entities, entity_id)
    if not start_entity:
        output_error(f"未找到ID为 {entity_id} 的实体", code="NOT_FOUND")
        return

    max_depth = int(data.get("max_depth", 3))
    result = _bfs_query(graph, entity_id, max_depth)

    output_success({
        "start_entity": start_entity,
        "related_entities": result["entities"],
        "relations": result["relations"],
        "entity_count": len(result["entities"]),
        "relation_count": len(result["relations"]),
    })


def company_map(data: Dict[str, Any]) -> None:
    """生成公司组织架构图。

    必填字段: company（公司名称）或 company_id

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("advanced_analytics", "CRM组织架构图"):
        return

    graph = _get_graph()

    # 自动填充
    _auto_populate_from_deals(graph)
    _save_graph(graph)

    entities = graph.get("entities", [])
    relations = graph.get("relations", [])

    # 查找公司实体
    company_name = data.get("company", "")
    company_id = data.get("company_id", "")

    company_entity = None
    if company_id:
        company_entity = _find_entity(entities, company_id)
    elif company_name:
        company_entity = _find_entity_by_name(entities, company_name, "Company")

    if not company_entity:
        output_error("未找到指定公司", code="NOT_FOUND")
        return

    comp_id = company_entity.get("id", "")

    # 找到所有与公司相关的人
    contacts = []
    for r in relations:
        if r.get("to_id") == comp_id and r.get("relation") in ("works_at",):
            person = _find_entity(entities, r.get("from_id", ""))
            if person:
                contacts.append({
                    "person": person,
                    "relation": r.get("relation", ""),
                })
        elif r.get("from_id") == comp_id and r.get("relation") in ("works_at",):
            person = _find_entity(entities, r.get("to_id", ""))
            if person:
                contacts.append({
                    "person": person,
                    "relation": r.get("relation", ""),
                })

    # 找出决策人
    decision_makers = []
    influencers = []
    for r in relations:
        if r.get("relation") == "decision_maker_for":
            person = _find_entity(entities, r.get("from_id", ""))
            if person:
                decision_makers.append(person.get("name", ""))

    # 找出汇报关系
    reporting = []
    person_ids = {c["person"].get("id") for c in contacts}
    for r in relations:
        if r.get("relation") == "reports_to":
            if r.get("from_id") in person_ids or r.get("to_id") in person_ids:
                from_name = ""
                to_name = ""
                from_e = _find_entity(entities, r.get("from_id", ""))
                to_e = _find_entity(entities, r.get("to_id", ""))
                if from_e:
                    from_name = from_e.get("name", "")
                if to_e:
                    to_name = to_e.get("name", "")
                reporting.append({
                    "from": from_name,
                    "to": to_name,
                })

    # 关联的商机
    related_deals = []
    for r in relations:
        if r.get("relation") == "contact_of":
            if r.get("from_id") in person_ids:
                deal_entity = _find_entity(entities, r.get("to_id", ""))
                if deal_entity and deal_entity.get("type") == "Deal":
                    related_deals.append({
                        "name": deal_entity.get("name", ""),
                        "properties": deal_entity.get("properties", {}),
                    })

    output_success({
        "company": company_entity.get("name", ""),
        "company_id": comp_id,
        "contacts": [
            {
                "name": c["person"].get("name", ""),
                "id": c["person"].get("id", ""),
                "properties": c["person"].get("properties", {}),
                "is_decision_maker": c["person"].get("name", "") in decision_makers,
            }
            for c in contacts
        ],
        "decision_makers": decision_makers,
        "reporting_lines": reporting,
        "related_deals": related_deals,
        "total_contacts": len(contacts),
    })


def influence_chain(data: Dict[str, Any]) -> None:
    """追踪推荐/影响力链路。

    必填字段: person_name 或 person_id

    Args:
        data: 参数字典。
    """
    if not require_paid_feature("advanced_analytics", "影响力链路"):
        return

    graph = _get_graph()
    entities = graph.get("entities", [])
    relations = graph.get("relations", [])

    # 查找起始人物
    person_name = data.get("person_name", "")
    person_id = data.get("person_id", "")

    start = None
    if person_id:
        start = _find_entity(entities, person_id)
    elif person_name:
        start = _find_entity_by_name(entities, person_name, "Person")

    if not start:
        output_error("未找到指定人物", code="NOT_FOUND")
        return

    # 追踪 referred_by 和 knows 链路
    chain = []
    visited: Set[str] = set()
    current_id = start.get("id", "")

    # 向上追踪（谁推荐了当前人物）
    upstream = []
    _trace_chain(entities, relations, current_id, "referred_by",
                 visited, upstream, direction="upstream")

    # 向下追踪（当前人物推荐了谁）
    visited_down: Set[str] = set()
    downstream = []
    _trace_chain(entities, relations, current_id, "referred_by",
                 visited_down, downstream, direction="downstream")

    # knows 网络
    knows_network = []
    for r in relations:
        if r.get("relation") == "knows":
            if r.get("from_id") == current_id:
                target = _find_entity(entities, r.get("to_id", ""))
                if target:
                    knows_network.append(target.get("name", ""))
            elif r.get("to_id") == current_id:
                target = _find_entity(entities, r.get("from_id", ""))
                if target:
                    knows_network.append(target.get("name", ""))

    output_success({
        "person": start.get("name", ""),
        "person_id": start.get("id", ""),
        "upstream_referrals": upstream,
        "downstream_referrals": downstream,
        "knows_network": knows_network,
        "total_connections": len(upstream) + len(downstream) + len(knows_network),
    })


def _trace_chain(entities: List[Dict], relations: List[Dict],
                 current_id: str, relation_type: str,
                 visited: Set[str], chain: List[Dict],
                 direction: str = "upstream", max_depth: int = 10) -> None:
    """递归追踪关系链路。

    Args:
        entities: 实体列表。
        relations: 关系列表。
        current_id: 当前实体ID。
        relation_type: 关系类型。
        visited: 已访问集合。
        chain: 结果链路列表。
        direction: 追踪方向（upstream/downstream）。
        max_depth: 最大深度。
    """
    if current_id in visited or len(chain) >= max_depth:
        return

    visited.add(current_id)

    for r in relations:
        if r.get("relation") != relation_type:
            continue

        if direction == "upstream" and r.get("from_id") == current_id:
            # 当前被 to_id 推荐
            target_id = r.get("to_id", "")
            target = _find_entity(entities, target_id)
            if target and target_id not in visited:
                chain.append({
                    "name": target.get("name", ""),
                    "id": target_id,
                    "type": target.get("type", ""),
                })
                _trace_chain(entities, relations, target_id,
                            relation_type, visited, chain, direction, max_depth)

        elif direction == "downstream" and r.get("to_id") == current_id:
            # 当前推荐了 from_id
            target_id = r.get("from_id", "")
            target = _find_entity(entities, target_id)
            if target and target_id not in visited:
                chain.append({
                    "name": target.get("name", ""),
                    "id": target_id,
                    "type": target.get("type", ""),
                })
                _trace_chain(entities, relations, target_id,
                            relation_type, visited, chain, direction, max_depth)


def visualize(data: Optional[Dict[str, Any]] = None) -> None:
    """生成 Mermaid 可视化图谱（付费功能）。

    可选字段: company（按公司过滤）、entity_id（以某实体为中心）

    Args:
        data: 可选参数。
    """
    if not require_paid_feature("mermaid_chart", "CRM图谱可视化"):
        return

    graph = _get_graph()

    # 自动填充
    _auto_populate_from_deals(graph)
    _save_graph(graph)

    entities = graph.get("entities", [])
    relations = graph.get("relations", [])

    data = data or {}

    # 过滤范围
    target_entity_ids: Optional[Set[str]] = None

    if data.get("entity_id"):
        result = _bfs_query(graph, data["entity_id"], max_depth=2)
        target_entity_ids = {e.get("id") for e in result["entities"]}
    elif data.get("company"):
        company_entity = _find_entity_by_name(entities, data["company"], "Company")
        if company_entity:
            result = _bfs_query(graph, company_entity["id"], max_depth=2)
            target_entity_ids = {e.get("id") for e in result["entities"]}

    # 生成 Mermaid 代码
    lines = ["```mermaid", "graph LR"]

    # 类型样式映射
    type_shapes = {
        "Person": ("([", "])" ),
        "Company": ("[[", "]]"),
        "Deal": ("{{", "}}"),
        "Meeting": ("(", ")"),
        "Email": ("(", ")"),
    }

    # 添加节点
    entity_ids_in_graph: Set[str] = set()
    for e in entities:
        eid = e.get("id", "")
        if target_entity_ids is not None and eid not in target_entity_ids:
            continue

        name = e.get("name", "").replace('"', "'")
        etype = e.get("type", "")
        shape = type_shapes.get(etype, ("(", ")"))

        # 使用安全的节点ID
        safe_id = eid.replace("-", "_")
        lines.append(f"    {safe_id}{shape[0]}\"{etype}: {name}\"{shape[1]}")
        entity_ids_in_graph.add(eid)

    # 添加边
    for r in relations:
        from_id = r.get("from_id", "")
        to_id = r.get("to_id", "")
        if from_id in entity_ids_in_graph and to_id in entity_ids_in_graph:
            relation_name = RELATION_TYPES.get(
                r.get("relation", ""), r.get("relation", "")
            )
            safe_from = from_id.replace("-", "_")
            safe_to = to_id.replace("-", "_")
            lines.append(f"    {safe_from} -->|{relation_name}| {safe_to}")

    lines.append("```")
    mermaid_code = "\n".join(lines)

    output_success({
        "mermaid": mermaid_code,
        "entity_count": len(entity_ids_in_graph),
        "relation_count": sum(
            1 for r in relations
            if r.get("from_id") in entity_ids_in_graph
            and r.get("to_id") in entity_ids_in_graph
        ),
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("deal-closer CRM知识图谱")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "add-entity": lambda: add_entity(data or {}),
        "add-relation": lambda: add_relation(data or {}),
        "query": lambda: query(data or {}),
        "company-map": lambda: company_map(data or {}),
        "influence-chain": lambda: influence_chain(data or {}),
        "visualize": lambda: visualize(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
