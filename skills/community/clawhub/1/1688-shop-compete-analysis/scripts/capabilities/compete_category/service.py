#!/usr/bin/env python3
"""竞争分析类目树查询服务"""

from _compete import compete_query
from _errors import ServiceError


def _walk(nodes: list, depth: int = 1) -> list:
    """递归展平类目树，只保留 cateId / 名称 / 层级 / 子类目数"""
    out = []
    for n in nodes or []:
        if not isinstance(n, dict):
            continue
        children = n.get("children") or []
        out.append({
            "cateId": n.get("value"),
            "cateName": n.get("内容") or n.get("text"),
            "cateLevel": n.get("类目层级") or n.get("cateLevel") or depth,
            "childCount": len(children),
            "children": _walk(children, depth + 1) if children else [],
        })
    return out


def get_compete_category(with_children: bool = False) -> dict:
    """获取当前店铺被授权的竞争分析类目树，并给出 cateId 取用建议。

    Args:
        with_children: 是否返回二/三级子类目（默认只返一级，减少输出体积）

    Returns:
        {
          "level1": [{cateId, cateName, childCount}],
          "needUserChoice": bool,   # True = 有多个一级类目，须反问用户选
          "suggested": {cateId, cateLevel} | None,
          "tree": [...]            # 仅 with_children=True 时返回完整树
        }
    """
    data = compete_query("compete/industryCategory", {})

    if not isinstance(data, list) or not data:
        raise ServiceError("未取到授权类目，请确认账号已订阅生意参谋 SVIP 且店铺有主营类目")

    tree = _walk(data)
    level1 = [{k: c[k] for k in ("cateId", "cateName", "childCount")} for c in tree]

    result = {
        "level1": level1,
        "needUserChoice": len(level1) > 1,
        "suggested": ({"cateId": level1[0]["cateId"], "cateLevel": 1}
                      if len(level1) == 1 else None),
    }
    if with_children:
        result["tree"] = tree
    return result
