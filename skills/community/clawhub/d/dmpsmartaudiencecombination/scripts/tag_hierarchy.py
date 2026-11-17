#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tag_hierarchy.py - 标签层级关系工具

基于tag_pool中的parentId字段，构建父子关系树，用于：
1. 检测用户选择中是否存在"父类+子类同时被选"的冗余
2. 自动在MUST层去重（保留最上层父类，子类降为OPTIONAL）
3. 判断标签之间是否存在祖先-后代包含关系
"""

import json
from typing import Dict, List, Set, Tuple


def build_parent_map(tag_pool: List[Dict]) -> Dict[int, int]:
    """构建 childId -> parentId 映射。

    仅包含 isDirectory=1 的标签（可用于组合的目录标签）。
    """
    pmap = {}
    for t in tag_pool:
        if t.get("isDirectory") != 1:
            continue
        tid = t.get("tagId")
        pid = t.get("parentId")
        if tid is not None and pid is not None:
            try:
                pmap[int(tid)] = int(pid)
            except (ValueError, TypeError):
                pass
    return pmap


def get_ancestors(tag_id: int, pmap: Dict[int, int], max_depth: int = 10) -> Set[int]:
    """获取一个标签的所有祖先ID（向上追溯parentId链）。"""
    ancestors = set()
    cur = tag_id
    for _ in range(max_depth):
        parent = pmap.get(cur)
        if parent is None or parent == cur or parent in ancestors:
            break
        ancestors.add(parent)
        cur = parent
    return ancestors


def is_descendant(child_id: int, ancestor_id: int, pmap: Dict[int, int]) -> bool:
    """判断child_id是否是ancestor_id的后代（子/孙/曾孙...）。"""
    return ancestor_id in get_ancestors(child_id, pmap)


def detect_parent_child_conflict(tag_ids: List[int], pmap: Dict[int, int]) -> List[Tuple[int, int]]:
    """检测标签列表中存在的(父类, 子类)对。

    返回列表中每个元素 (ancestor_id, descendant_id)，表示
    descendant_id 是 ancestor_id 的后代，两者同时选入MUST做AND是冗余/错误的。
    """
    conflicts = []
    id_set = set(tag_ids)
    for tid in tag_ids:
        ancestors = get_ancestors(tid, pmap)
        for aid in ancestors:
            if aid in id_set:
                conflicts.append((aid, tid))
    return conflicts


def deduplicate_must_tags(must_tags: List[int], pmap: Dict[int, int]) -> Tuple[List[int], List[int]]:
    """对MUST标签去重：移除被祖先覆盖的后代标签。

    例如：must=[女, 美妆个护, 护肤, 彩妆]，其中护肤和彩妆是美妆个护的子类，
    AND关系下选了美妆个护再选护肤/彩妆是冗余且错误的（会收窄到既是护肤又是彩妆的人）。

    返回: (deduped_must, removed_to_optional)
      - deduped_must: 去重后的MUST标签（保留祖先，移除后代）
      - removed_to_optional: 被移除的后代标签（建议放到OPTIONAL做Overlap分析）
    """
    must_set = set(must_tags)
    # 找出所有"被自己祖先也在must中"的标签
    to_remove = set()
    for tid in must_tags:
        ancestors = get_ancestors(tid, pmap)
        if ancestors & must_set:
            to_remove.add(tid)
    deduped = [t for t in must_tags if t not in to_remove]
    removed = [t for t in must_tags if t in to_remove]
    return deduped, removed


def group_tags_by_dimension(tag_ids: List[int], tag_pool: List[Dict],
                            core_interest_kws: List[str] = None) -> Dict[str, List[int]]:
    """将扁平标签列表按维度自动分组。

    基于标签的名称和category路径推断维度，用于将同维度标签放入同一OR组。
    注意：明略标签的dimension字段可能为空，需要结合category路径和名称关键词判断。

    返回: {"性别": [...], "年龄": [...], "城市级别": [...], "核心兴趣": [...], ...}
    """
    if core_interest_kws is None:
        core_interest_kws = ["美妆个护", "护肤", "彩妆", "母婴", "汽车", "3C"]
    tag_map = {int(t["tagId"]): t for t in tag_pool if t.get("isDirectory") == 1}
    groups = {}
    for tid in tag_ids:
        t = tag_map.get(int(tid))
        if not t:
            groups.setdefault("其他", []).append(int(tid))
            continue
        name = t.get("tagName", "")
        dim = t.get("dimension", "")
        category = str(t.get("category", ""))
        # 辅助函数：名称或category是否命中关键词
        def _hits(kws):
            return any(kw in name or kw in category for kw in kws)
        # 性别判断（兼容基础属性_性别_男/基本属性_性别_男等前缀格式）
        if dim == "性别" or _hits(["性别"]) or name in ("女", "男", "女性", "男性") or bool(__import__("re").search(r'_性别_[男女]$', name)):
            groups.setdefault("性别", []).append(int(tid))
        # 年龄判断：兼容明略纯数字段"20-24"和合作前缀段"基础属性_年龄_25-34"
        elif dim == "年龄" or "年龄" in category or "岁" in name or bool(__import__("re").search(r'_年龄_\d', name)) or bool(__import__("re").match(r'^\d+-\d+岁?$', name.strip())):
            groups.setdefault("年龄", []).append(int(tid))
        # 城市级别（兼容基本属性_居住城市级别/基础属性_居住城市级别）
        elif dim == "地域" or _hits(["线城市", "城市级别"]) or "居住城市级别" in name or "居住城市级别" in category:
            groups.setdefault("城市级别", []).append(int(tid))
        # 核心兴趣
        elif dim == "兴趣" or _hits(core_interest_kws):
            groups.setdefault("核心兴趣", []).append(int(tid))
        # 消费力
        elif dim == "活跃/消费力" or _hits(["消费", "轻奢", "收入"]):
            groups.setdefault("消费力", []).append(int(tid))
        # 职业
        elif _hits(["白领"]) or "职业" in category:
            groups.setdefault("职业", []).append(int(tid))
        else:
            groups.setdefault("其他", []).append(int(tid))
    return groups


def must_to_or_groups(must_tags: List[int], tag_pool: List[Dict],
                      core_interest_kws: List[str] = None) -> Tuple[List[List[int]], List[int], List[str]]:
    """将扁平MUST标签列表转换为or_groups二维列表（用于rules_helper.build_rules_http）。

    处理逻辑：
    1. 先用parentId做父子去重（祖先覆盖后代，后代移到removed_optional）
    2. 按维度自动分组（性别/年龄/城市/核心兴趣/消费/职业/其他）
    3. 同组标签放入同一个OR数组（同维度多标签是OR关系）
    4. 跨组用AND连接

    返回: (or_groups, removed_optional, warnings)
    """
    pmap = build_parent_map(tag_pool)
    warnings = []
    # Step 1: 父子去重
    deduped_must, removed = deduplicate_must_tags(must_tags, pmap)
    if removed:
        tag_map = {int(t["tagId"]): t.get("tagName", "") for t in tag_pool}
        removed_names = [f"{tag_map.get(r, r)}({r})" for r in removed]
        warnings.append(
            f"检测到父类+子类同时选中，已在MUST层移除子类标签（移至OPTIONAL）：{', '.join(removed_names)}。"
            f"原因：父类标签已包含子类人群，AND子类会导致人群过窄。"
        )
    # Step 2: 按维度分组
    dim_groups = group_tags_by_dimension(deduped_must, tag_pool, core_interest_kws)
    # Step 3: 构建or_groups
    or_groups = []
    # 固定维度顺序（保证确定性）
    dim_order = ["性别", "年龄", "城市级别", "核心兴趣", "消费力", "职业", "其他"]
    for dim in dim_order:
        if dim in dim_groups and dim_groups[dim]:
            or_groups.append(sorted(dim_groups[dim]))
    # 其他维度如果有未覆盖的，也加进去
    for dim, tags in dim_groups.items():
        if dim not in dim_order and tags:
            or_groups.append(sorted(tags))
    return or_groups, removed, warnings


if __name__ == "__main__":
    # 自检
    import os
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    pool_path = os.path.join(skill_dir, "tag_pool.json")
    if os.path.exists(pool_path):
        with open(pool_path) as f:
            pool = json.load(f)
        pmap = build_parent_map(pool)
        # 测试：美妆个护(15564) 是 护肤(15652)和彩妆(15653)的父类
        assert is_descendant(15652, 15564, pmap), "护肤应该是美妆个护的子类"
        assert is_descendant(15653, 15564, pmap), "彩妆应该是美妆个护的子类"
        assert not is_descendant(15564, 15652, pmap), "美妆个护不是护肤的子类"
        # 测试去重
        deduped, removed = deduplicate_must_tags([15705, 15564, 15652, 15653], pmap)
        assert set(deduped) == {15705, 15564}, f"去重后应为女+美妆个护，got {deduped}"
        assert set(removed) == {15652, 15653}, f"移除的应为护肤+彩妆，got {removed}"
        # 测试OR分组
        or_groups, removed2, warns = must_to_or_groups(
            [15705, 15687, 15688, 15689, 34080, 34082, 15564, 15652, 15653],
            pool, ["美妆个护", "护肤", "彩妆"]
        )
        assert len(or_groups) == 4, f"应分4组（性别/年龄/城市/核心兴趣），got {len(or_groups)}: {or_groups}"
        assert or_groups[0] == [15705], f"第一组应为性别[女]，got {or_groups[0]}"
        assert set(or_groups[1]) == {15687, 15688, 15689}, f"第二组应为年龄段OR"
        assert set(or_groups[2]) == {34080, 34082}, f"第三组应为城市OR"
        assert or_groups[3] == [15564], f"第四组核心兴趣去重后应只留美妆个护，got {or_groups[3]}"
        print("✅ tag_hierarchy 所有自检通过")
        print(f"  or_groups: {or_groups}")
        print(f"  removed_to_optional: {removed2}")
        for w in warns:
            print(f"  ⚠️ {w}")
    else:
        print("⚠️ tag_pool.json不存在，跳过自检（需要先运行query_tag_list.py）")
