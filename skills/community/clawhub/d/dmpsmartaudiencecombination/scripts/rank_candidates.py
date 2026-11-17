#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rank_candidates.py

候选标签分组推荐脚本（确定性版·零依赖）。
核心理念：按用户需求维度分组展示，不混排；组内排序完全确定性，同分按tagId稳定tie-break。

在 tag_profile_enrich.py 补全画像后执行：
1) 硬门槛过滤（剔除无关标签）
2) 按用户需求维度分组（性别/年龄/城市/核心兴趣/消费/职业/活跃 等）
3) 每组内确定性排序：语义分桶→有画像优先→大类优先→工程分→tagId兜底
4) 核心维度缺口提示（性别/年龄/城市级别/核心兴趣为空时输出警告）
5) 中文表头统一输出

输入：
- enriched.json：tag_profile_enrich.py 输出
- --core-interest：核心兴趣关键词（逗号分隔），用于分组和大类优先判定
- --required-dims：必须有候选的维度（逗号分隔），为空时输出缺口提示

输出：
- grouped.json：按维度分组的候选标签（字段名中文：标签ID/标签名称/来源/相似度/工程分…）
"""

import argparse
import json
import re

# 表格输出格式：默认Markdown表格；如需框线表格可切换
# - markdown: 使用 |---| 形式，便于在支持Markdown的渠道直接展示

from pathlib import Path
from typing import Any, Tuple, List, Dict


def _load_json_file(path: str) -> Any:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _dedup_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        x = str(x).strip()
        if not x or x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def _infer_seed_kws(core_interest_arg: str, schema_path: str, coverage_path: str, queries_path: str, max_kws: int = 8) -> Tuple[List[str], Dict[str, Any]]:
    """方案B：核心兴趣=种子词(seed_kws)；AUTO时从schema/coverage/queries确定性推导。

    返回：(seed_kws, meta)
    meta用于解释来源与过滤情况。
    """
    meta: Dict[str, Any] = {"mode": "manual", "sources": [], "filtered": []}

    if core_interest_arg and core_interest_arg != "AUTO":
        kws = [k.strip() for k in core_interest_arg.split(",") if k.strip()]
        kws = _dedup_keep_order(kws)[:max_kws]
        return kws, meta

    meta["mode"] = "auto"

    schema = _load_json_file(schema_path) or {}
    cov = _load_json_file(coverage_path) or {}
    qobj = _load_json_file(queries_path) or {}

    ambiguous = set()
    try:
        ambiguous_list = (((qobj.get("meta") or {}).get("ambiguous_short")) or [])
        ambiguous = set([str(x).strip() for x in ambiguous_list if str(x).strip()])
    except Exception:
        ambiguous = set()

    # 1) schema里显式兴趣字段优先
    candidates: List[str] = []
    for key in ("interests", "interest", "兴趣", "核心兴趣"):
        v = schema.get(key)
        if isinstance(v, list):
            candidates.extend([str(x).strip() for x in v])
        elif isinstance(v, str):
            candidates.append(v.strip())
    if candidates:
        meta["sources"].append("schema.interest")

    # 2) coverage_matrix里兴趣相关维度
    matrix = (cov.get("coverage_matrix") if isinstance(cov, dict) else {}) or {}
    if isinstance(matrix, dict):
        for dim_key in ("interest", "category", "industry", "兴趣", "品类", "行业"):
            vals = matrix.get(dim_key)
            if isinstance(vals, list):
                candidates.extend([str(x).strip() for x in vals])
                meta["sources"].append(f"coverage.{dim_key}")

    # 3) queries.boost_words兜底（较长锚点词）
    boost_words = qobj.get("boost_words") if isinstance(qobj, dict) else None
    if isinstance(boost_words, list):
        candidates.extend([str(x).strip() for x in boost_words])
        meta["sources"].append("queries.boost_words")

    # 过滤：长度<2、歧义短词
    cleaned = []
    for w in candidates:
        ww = str(w).strip()
        if not ww:
            continue
        if len(ww) < 2:
            meta["filtered"].append({"kw": ww, "reason": "too_short"})
            continue
        if ww in ambiguous:
            meta["filtered"].append({"kw": ww, "reason": "ambiguous_short"})
            continue
        cleaned.append(ww)

    cleaned = _dedup_keep_order(cleaned)

    # 最终门禁：最多N个
    seed_kws = cleaned[:max_kws]
    return seed_kws, meta


def _hits_seed(t: Dict, seed_kws: List[str]) -> Tuple[bool, str]:
    """命中判断：tagName/category/profile_match_name 任一包含种子词即命中。
    返回：(is_hit, hit_field)
    """
    if not seed_kws:
        return False, ""
    name = str(t.get("tagName", ""))
    category = str(t.get("category", ""))
    pmn = str(t.get("profile_match_name", ""))
    for kw in seed_kws:
        if kw and (kw in name):
            return True, "tagName"
        if kw and (kw in category):
            return True, "category"
        if kw and (kw in pmn):
            return True, "profile_match_name"
    return False, ""

# - box: Unicode框线表格（┌─┬─┐），用于Markdown渲染不稳定的渠道
DEFAULT_TABLE_FORMAT = "markdown"


from typing import List, Dict


# 默认排除关键词（通用无关项）：排除和目标用户明确相反的标签 + 消费偏好类非消费水平标签
DEFAULT_EXCLUDE = [
    "三线城市", "四线及以下",
    "低消费", "低-消费水平", "低收入", "中低收入", "中低",
    "女性护理价格", "手机价格",
    "自驾圈层", "滑雪圈层", "运动健身", "户外", "极限", "3C圈层", "汽车圈层",
    "短剧圈层", "0-20-",
    "居住地_省", "居住地_市",
    "油车", "新能源车",
    "非精准到访",  # WiFi非精准到访排除，只留精准到访
    "纹身", "纹绣", "产后", "瘦身",
    "其他年龄",
    # 明略兴趣标签中的消费偏好类（非消费水平，属于兴趣方向，和"消费力"无关）
    "运动消费", "汽车消费", "房产消费", "医疗消费", "3C消费",
    # 纯父级目录节点（isDirectory=1但无实际覆盖率的分类目录）
    "消费状态", "消费倾向", "消费水平",
]

# 全局最低相似度阈值：低于此阈值的非核心维度标签直接过滤（防止弱相关噪声）
MIN_SIMILARITY_THRESHOLD = 0.20

# 真正属于"消费力"组的关键词（消费水平类，非消费偏好类）
CONSUMPTION_LEVEL_KWS = [
    "高消费", "低消费", "中等消费", "中消费", "超高消费",
    "高-消费", "中-消费", "低-消费", "轻奢",
    "高收入", "中高收入", "中收入", "低收入", "富人",
]

# 核心维度（拉新/美妆场景默认必须有候选，否则输出缺口提示）
# 使用中文名，与 make_group_key/_dim_hint 归一化后的分组key一致
DEFAULT_REQUIRED_DIMS = ["性别", "年龄", "城市级别", "核心兴趣"]

# _dim_hint 可能出现的别名 → 标准中文分组名映射
# 注意："地域"是一个大维度，里面包含"城市级别"子组，不应直接映射到"地域-其他"
_DIM_ALIAS_MAP = {
    "gender": "性别", "sex": "性别", "男女性别": "性别",
    "age": "年龄", "年龄段": "年龄",
    "city": "城市级别", "city_level": "城市级别", "city_tier": "城市级别", "城市": "城市级别",
    "城市级别": "城市级别",
    "region": "地域", "地域": "地域",
    "core_interest": "核心兴趣", "core": "核心兴趣", "核心": "核心兴趣",
    "interest": "其他兴趣", "兴趣": "其他兴趣",
    "sub_interest": "兴趣细分", "兴趣细分": "兴趣细分",
    "consumption": "消费力", "消费": "消费力", "消费力": "消费力",
    "occupation": "职业", "职业": "职业",
    "activity": "活跃度", "活跃": "活跃度", "活跃度": "活跃度",
    "crowd": "八大人群/圈层", "八大人群": "八大人群/圈层", "圈层": "八大人群/圈层",
    "related": "关联兴趣", "关联兴趣": "关联兴趣",
    "其他": "其他",
}

# 地域维度的子组：当required_dims传"地域"时，只要有任一子组存在就不算缺口
_REGION_SUBGROUPS = ["城市级别", "地域-其他"]


def _is_consumption_level(name: str) -> bool:
    """判断是否为真正的消费水平标签（而非消费偏好兴趣标签）"""
    return any(kw in name for kw in CONSUMPTION_LEVEL_KWS)


def _is_consumption_preference(name: str, category: str) -> bool:
    """判断是否为消费偏好类兴趣标签（如运动消费/汽车消费/房产消费/医疗消费），这些属于兴趣不是消费力"""
    # 明略标签中category路径含"兴趣爱好"且名中带"消费"且不是消费水平词
    if "兴趣爱好" in category:
        if name.endswith("消费") and not _is_consumption_level(name):
            return True
    return False


def _is_parenting_stage_tag(name: str) -> bool:
    """判断是否为育儿阶段标签（如0-1岁父母、1-3岁小孩父母、备孕、孕期等），这些属于母婴兴趣不是年龄"""
    parenting_kws = ["岁父母", "岁小孩父母", "备孕", "孕期", "孕妈妈", "准妈妈",
                     "孕妈", "孕婴", "新妈", "老妈", "母婴", "亲子", "育儿",
                     "小学生家长", "中学生家长", "二胎家长", "妈妈"]
    return any(kw in name for kw in parenting_kws)


def hard_filter(tags: List[Dict], exclude_keywords: List[str]) -> List[Dict]:
    """硬门槛过滤"""
    kept = []
    # 有效的维度名（来自expand_by_dimension的九维度）
    _VALID_DIMS = {"性别", "年龄", "城市级别", "八大人群/圈层", "核心兴趣",
                   "兴趣细分", "消费力", "职业", "关联兴趣", "活跃度"}
    for t in tags:
        name = t.get("tagName", "")
        sim = t.get("similarity", 0) or 0
        category = str(t.get("category", ""))

        # 1. isDirectory=0 的纯目录节点直接排除
        if t.get("isDirectory") != 1:
            continue

        # 2. 明确排除关键词
        if any(kw in name for kw in exclude_keywords):
            continue

        # 3. 消费偏好类兴趣标签（运动消费/汽车消费/3C消费等）直接排除——属于弱相关兴趣方向，不是消费力
        if _is_consumption_preference(name, category):
            continue

        # 4. 全局相似度阈值：非核心维度兜底标签低于阈值直接过滤
        recall_source = t.get("recall_source", "semantic")
        is_fallback = (recall_source == "fallback_dict")
        is_core_dim = t.get("_dim_hint") in _VALID_DIMS
        # 核心维度标签（性别/年龄/城市等）只要存在就保留，不被相似度阈值过滤
        is_gender_dim = bool(re.match(r'^(?:基础属性|基本属性)?_?性别_[男女]$', name)) or name in {"女", "男", "女性", "男性"}
        is_age_dim = bool(re.match(r'^\d{1,2}-\d{1,2}岁?$', name.strip())) or "年龄_" in name
        is_city_dim = ("线城市" in name and "居住城市级别" in name)
        is_core_dim = is_core_dim or is_fallback or is_gender_dim or is_age_dim or is_city_dim
        if not is_fallback and not is_core_dim and sim < MIN_SIMILARITY_THRESHOLD:
            continue

        # 5. 无覆盖率的父级目录节点过滤（覆盖率None且相似度低于0.55的分类中间节点）
        cov = t.get("coverage_rate")
        if cov is None and sim < 0.55 and not is_fallback:
            continue

        # 6. MISSING标签处理
        if t.get("profile_status") == "MISSING":
            dim_hint = t.get("_dim_hint", "")
            if dim_hint in _VALID_DIMS:
                kept.append(t)
                continue
            # 其他MISSING标签：名字命中核心关键词才保留
            keep_kws = ["女", "男", "性别", "岁", "年龄", "线城市", "城市级别",
                        "护肤", "彩妆", "美妆", "轻奢", "白领",
                        "新锐白领", "高活", "活跃", "圈层", "精致", "高消费",
                        "奢侈品", "珠宝", "服装", "医美", "海淘", "潮流",
                        "大学生", "主播", "明星", "自拍", "拍摄", "丽人",
                        "美甲", "美发", "皮肤管理", "化妆品", "香水", "口腔",
                        "身体护理", "高端", "大众", "欧美", "日韩", "中国",
                        "面霜", "面膜", "精华", "口红", "洁面", "眼膜",
                        "高收入", "中高收入", "富人", "高-",
                        "运动", "健身", "体育", "跑步", "球类",
                        "母婴", "育儿", "孕", "亲子", "新妈", "老妈",
                        "汽车", "3C", "数码", "房产", "教育", "游戏",
                        "金融", "理财", "旅游", "美食", "医疗", "健康",
                        "妈妈", "爸爸", "学生", "小镇青年"]
            if not any(kw in name for kw in keep_kws):
                continue

        kept.append(t)

    # 7. 按tagId去重（防止同标签重复出现）
    dedup = {}
    for t in kept:
        tid = t.get("tagId")
        if tid is not None:
            dedup[tid] = t
        else:
            # fallback：用名称+来源去重
            key = (t.get("tagName",""), t.get("tagType",""))
            dedup[str(key)] = t

    return list(dedup.values())


def _is_age_range(name: str) -> bool:
    """判断是否为纯年龄段格式（如25-29、25-29岁），年龄段中的'-'不算细分标志"""
    return bool(re.match(r'^\d+-\d+岁?$', name.strip()))


def is_subdivision_tag(name: str) -> bool:
    """判断是否为细分标签（子类/品牌/价格段/功效/高兴趣度后缀）"""
    if not name:
        return False
    # 年龄段不算细分
    if _is_age_range(name):
        return False
    # 含"-"且不是年龄段（如"彩妆-欧美"、"中高端-护肤"、"护肤彩妆-高"）
    if "-" in name:
        # 合作标签格式"基础属性_年龄_18-24"中的年龄段部分
        if re.search(r'[_-]\d+-\d+$', name):
            return True  # 合作标签年龄段作为合并段，标细分备选
        if not any(c in name for c in "岁线城市级别"):
            return True
    if "价格" in name:
        return True
    sub_cats = ["口红", "唇膏", "面部", "面霜", "水乳", "精华", "面膜", "眼膜", "眼霜",
                "洁面", "卸妆", "补水", "美白", "提拉", "抗痘", "控油", "紧致",
                "抗衰", "抗氧化", "淡斑", "保湿", "成分", "功效", "香水", "口腔",
                "身体护理", "洗发护发", "珠宝", "海淘", "社交电商", "潮流", "图片分享",
                "拍摄", "丽人图像", "服装服饰"]
    if any(sc in name for sc in sub_cats):
        return True
    if name.endswith("-高"):
        return True
    # 合作标签前缀格式（基础属性_xxx_yyy 中yyy部分视为细分）
    if "_" in name and name.count("_") >= 2:
        # 如"兴趣偏好_购物_护肤彩妆"不算细分，但"-高"后缀已在上面处理
        # "基本属性_居住城市级别_一线城市"中的城市名算细分选项
        prefix = name.rsplit("_", 1)[-1]
        if prefix in ["一线城市", "二线城市", "三线城市", "四线", "高消费人群",
                      "中等消费人群", "低消费人群", "富人"]:
            return True
    return False


def make_group_key(t: Dict, seed_kws: List[str]) -> str:
    """根据标签dimension和名称，映射到用户可理解的需求维度分组名"""
    dim = t.get("dimension", "")
    name = t.get("tagName", "")
    category = str(t.get("category", ""))  # category路径，如"兴趣爱好-美妆个护-护肤"

    # 辅助：名称或category路径中是否命中核心兴趣关键词
    def hits_core() -> bool:
        hit, _field = _hits_seed(t, seed_kws)
        return hit

    if dim == "性别":
        return "性别"
    if dim == "年龄":
        # 育儿阶段标签不归入年龄组
        if _is_parenting_stage_tag(name):
            return "核心兴趣" if hits_core() else "其他兴趣"
        return "年龄"
    if dim == "地域":
        if "城市级别" in name or "线城市" in name:
            return "城市级别"
        return "地域-其他"
    if dim == "活跃/消费力":
        if "白领" in name or "职业" in name:
            return "职业"
        if _is_consumption_level(name):
            return "消费力"
        if _is_consumption_preference(name, category):
            return "其他兴趣" if not hits_core() else "核心兴趣"
        if "高活" in name or "活跃" in name or "圈层" in name:
            return "活跃度"
        return "消费力"
    if dim == "兴趣":
        # 消费偏好类标签归兴趣不归消费力
        if _is_consumption_preference(name, category):
            return "其他兴趣"
        if hits_core():
            return "核心兴趣"
        return "其他兴趣"

    # MISSING标签按名称推断（方案A：性别组只收“真·性别标签”，禁止用“包含女性/女字”粗暴归类）
    # 允许进入“性别”组的MISSING标签：
    # - 纯性别词：女 / 男 / 女性 / 男性
    # - 明确性别字段：基础属性_性别_女 / 基础属性_性别_男 / 性别_女 / 性别_男
    # 其余即便包含“女性”字样（如“女性健康管理”）也不得归入性别组。
    # 性别组：用正则兼容所有标签前缀（基础属性/基本属性/性别_），不依赖硬编码白名单
    if re.match(r'^(?:基础属性|基本属性)?_?性别_[男女]$', name) or name in {"女", "男", "女性", "男性"}:
        return "性别"
    # 育儿阶段标签（"X岁父母""X岁小孩父母""备孕""孕期"等）归入核心兴趣/母婴，不归年龄组
    if _is_parenting_stage_tag(name):
        return "核心兴趣" if hits_core() else "其他兴趣"
    if ("岁" in name or "年龄" in name) and "父母" not in name and "小孩" not in name:
        return "年龄"
    # 明略纯年龄段名（如"25-29""30-34"，纯数字-数字格式）也归年龄组
    if re.match(r'^\d{2}-\d{2}岁?$', name.strip()) and not _is_parenting_stage_tag(name):
        return "年龄"
    if any(kw in name for kw in ["一线", "二线", "城市级别"]):
        return "城市级别"
    if any(kw in name for kw in ["护肤", "彩妆", "美妆", "女性护理"]) or hits_core():
        return "核心兴趣"
    if _is_consumption_level(name):
        return "消费力"
    if _is_consumption_preference(name, category):
        return "其他兴趣"
    if "白领" in name:
        return "职业"
    if "高活" in name or "活跃" in name:
        return "活跃度"
    return "其他"


def make_group_sort_key(t: Dict):
    """【确定性排序·方案2：工程分优先，相似度做桶保护】
    组内排序key（元组字典序，完全确定性无随机）：
    1. similarity_bucket 降序：±0.05一桶，语义差0.05以上的不会因工程分高反超（避免无关标签因数据量大头名）
    2. profile_status：OK=0排前，MISSING=1排后（无画像数据的标签降权）
    3. is_subdivision：大类=0排前，细分↳=1排后（大类标签优先展示）
    4. eng_score 降序：【主排序】工程分高的在前
    5. similarity 精确降序：工程分相同时，语义更相关的在前
    6. tagId 升序：【最终兜底】所有分数都相同时按tagId升序，保证完全稳定

    浮点统一round后再比较，避免浮点尾差导致跨运行不一致：
    - similarity round(6)
    - eng_score  round(4)
    """
    sim = round(t.get("similarity", 0) or 0, 6)
    eng = round(t.get("eng_score"), 4) if t.get("eng_score") is not None else 0.0
    has_profile = 0 if t.get("profile_status") == "OK" else 1
    is_sub = 1 if is_subdivision_tag(t.get("tagName", "")) else 0
    bucket = int(sim / 0.05)  # 相似度±0.05一桶
    tag_id = int(t.get("tagId", 0) or 0)
    return (-bucket, has_profile, is_sub, -eng, -sim, tag_id)


def _fmt_pct(v):
    """格式化百分比（仅用于coverage_rate等0~1的小数比例）"""
    if v is None:
        return "-"
    return f"{v*100:.1f}%"


def _fmt_size(v):
    """格式化量级（人数）。注意：量级是人数，不是百分比。"""
    if v is None:
        return "-"
    try:
        return f"{int(float(v)):,}"
    except Exception:
        return str(v)


def _fmt_eng(v):
    """格式化工程分"""
    if v is None:
        return " -"
    return f"{v:.2f}"


def _src_label(tag_type):
    return "明略" if tag_type == 1 else "合作"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enriched", required=True, help="enriched.json (tag_profile_enrich.py输出)")
    ap.add_argument(
        "--table-format",
        default=DEFAULT_TABLE_FORMAT,
        choices=["markdown", "box", "card"],
        help="Step6分组推荐表格输出格式：markdown=默认；box=框线表格；card=Octo卡片友好JSON（精简列+短来源名，供AI构建Display Card）",
    )
    ap.add_argument("--core-interest", default="AUTO",
                    help="核心兴趣种子词(逗号分隔)。AUTO表示从schema/coverage/queries自动推导；命中(tagName/category/画像匹配名)的候选标签进入核心兴趣组")
    ap.add_argument("--schema", default="", help="schema.json路径（用于AUTO推导核心兴趣种子词）")
    ap.add_argument("--coverage", default="", help="coverage_matrix.json路径（用于AUTO推导核心兴趣种子词）")
    ap.add_argument("--queries", default="", help="queries.json路径（用于AUTO推导核心兴趣种子词/歧义词过滤）")
    ap.add_argument("--core-group-name", default="核心兴趣",
                    help="核心兴趣组显示名称，默认'核心兴趣'")
    ap.add_argument("--exclude", default="", help="额外排除关键词(逗号分隔)")
    ap.add_argument("--required-dims", default=",".join(DEFAULT_REQUIRED_DIMS),
                    help="必须有候选的维度(逗号分隔)，缺失时输出缺口提示")
    ap.add_argument("--top-per-group", type=int, default=12, help="每组最多展示数量，默认12")
    ap.add_argument("--out", required=True, help="输出JSON路径")
    args = ap.parse_args()

    with open(args.enriched, "r", encoding="utf-8") as f:
        tags = json.load(f)

    seed_kws, seed_meta = _infer_seed_kws(args.core_interest, args.schema, args.coverage, args.queries)
    required_dims = [d.strip() for d in args.required_dims.split(",") if d.strip()]
    core_group_name = args.core_group_name

    exclude = list(DEFAULT_EXCLUDE)
    if args.exclude:
        exclude.extend([kw.strip() for kw in args.exclude.split(",") if kw.strip()])

    # 1) 硬过滤
    filtered = hard_filter(tags, exclude)

    # 2) 按需求维度分组（核心：优先使用expand_by_dimension写入的_dim_hint字段）
    groups: Dict[str, List[Dict]] = {}
    for t in filtered:
        # 优先使用_dim_hint（expand_by_dimension.py已按九维度分好组）
        gk = t.get("_dim_hint")
        # 归一化_dim_hint别名到标准中文分组名
        if gk and gk in _DIM_ALIAS_MAP:
            gk = _DIM_ALIAS_MAP[gk]
        if not gk or gk == "其他":
            # 兜底：按dimension+名称推断
            gk = make_group_key(t, seed_kws)
        if gk == "核心兴趣":
            gk = core_group_name
        t["_group"] = gk
        groups.setdefault(gk, []).append(t)

    # 3) 每组内确定性排序
    for gk in groups:
        groups[gk].sort(key=make_group_sort_key)
        groups[gk] = groups[gk][:args.top_per_group]

    # 3.5) 仅按tagId去重（同标签ID重复出现时保留一份），不做跨来源合并
    # 明略标签和合作伙伴标签是不同的tagId，即使语义相同（如明略"女"vs合作"基础属性_性别_女"）
    # 也应都保留展示给用户，让用户自己选择用哪个来源的标签
    for gk in groups:
        seen_ids = set()
        unique = []
        for t in groups[gk]:
            tid = t.get("tagId")
            if tid not in seen_ids:
                seen_ids.add(tid)
                unique.append(t)
        groups[gk] = unique

    # 4) 按展示顺序排列组（固定九维度+其他兴趣，隐藏空组和"其他"组）
    base_order = ["性别", "年龄", "城市级别", "八大人群/圈层", core_group_name,
                  "兴趣细分", "消费力", "职业", "关联兴趣",
                  "活跃度", "其他兴趣", "地域-其他"]
    ordered_groups = {}
    for gk in base_order:
        if gk in groups and len(groups[gk]) > 0:
            ordered_groups[gk] = groups[gk]
    for gk, items in groups.items():
        if gk not in ordered_groups and len(items) > 0 and gk != "其他":
            ordered_groups[gk] = items

    # 5) 核心维度缺口检测（先归一化required_dims中的别名）
    gaps = []
    for dim in required_dims:
        # 归一化别名
        dim_name = _DIM_ALIAS_MAP.get(dim, dim)
        if dim_name == "核心兴趣":
            dim_name = core_group_name
        # 地域大维度：只要城市级别或地域-其他任一子组存在就不算缺口
        if dim_name == "地域":
            has_region = any(ordered_groups.get(sg) for sg in _REGION_SUBGROUPS)
            if not has_region:
                gaps.append("城市级别")
            continue
        if dim_name not in ordered_groups or len(ordered_groups[dim_name]) == 0:
            gaps.append(dim_name)

    # 6) 输出JSON（中文字段名，所有浮点统一round保证确定性）
    out_json = {}
    for gk, items in ordered_groups.items():
        out_json[gk] = []
        for t in items:
            fr = t.get("audience_size")
            cr = t.get("coverage_rate")
            out_json[gk].append({
                "标签ID": t.get("tagId"),
                "标签名称": t.get("tagName"),
                "来源": _src_label(t.get("tagType")),
                "来源简写": "明" if t.get("tagType") == 1 else "合",
                "维度": t.get("dimension", ""),
                "相似度": round(t.get("similarity", 0), 6),
                "工程分": round(t.get("eng_score", 0), 4) if t.get("eng_score") is not None else None,
                "标签量级": int(fr) if fr is not None else None,
                "覆盖率": round(cr, 4) if cr is not None else None,
                "画像状态": t.get("profile_status", ""),
                "召回来源": t.get("recall_source", "semantic"),
                "细分标签": is_subdivision_tag(t.get("tagName", "")),
            })

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    total = sum(len(v) for v in ordered_groups.values())
    summary = {
        "ok": True,
        "in": len(tags),
        "after_filter": len(filtered),
        "groups": len(ordered_groups),
        "total_tags": total,
        "required_gaps": gaps,
        "out": args.out,
    }
    print(json.dumps(summary, ensure_ascii=False))

    # 7) 打印分组表格（默认Markdown；可选框线表格）
    def _pad(s, width, align="left"):
        """中文对齐填充（按显示宽度计算，中文算2字符）"""
        s = str(s)
        disp_w = sum(2 if ord(c) > 127 else 1 for c in s)
        pad = width - disp_w
        if pad < 0:
            pad = 0
        if align == "right":
            return " " * pad + s
        return s + " " * pad

    def _print_markdown_table(group_name: str, rows: list):
        """打印Markdown表格（不做宽度对齐，交给渲染层）。"""
        print(f"\n### {group_name}（{len(rows)}个标签）")
        headers = ["标签ID", "来源", "相似度", "工程分", "标签量级", "覆盖率", "标签名称"]
        print("| " + " | ".join(headers) + " |")
        print("|" + "|".join(["---"] * len(headers)) + "|")
        for tid, src, sim, eng, fr, cr, name in rows:
            print(f"| {tid} | {src} | {sim} | {eng} | {fr} | {cr} | {name} |")

    for gk, items in ordered_groups.items():
        # 预计算每行数据
        rows = []
        for t in items:
            fr = _fmt_size(t.get("audience_size"))
            cr = _fmt_pct(t.get("coverage_rate"))
            eng = _fmt_eng(t.get("eng_score")).strip()
            sim = f"{t.get('similarity',0):.3f}"
            warn = "⚠️" if t.get("profile_status") == "MISSING" else ""
            sub = "↳" if is_subdivision_tag(t.get("tagName", "")) else ""
            tt = _src_label(t.get("tagType"))
            tid = str(t.get("tagId", ""))
            name = f"{warn}{sub}{t.get('tagName','')}"
            rows.append((tid, tt, sim, eng, fr, cr, name))

        # 按输出格式打印（markdown 直接输出并跳过框线渲染）
        if args.table_format == "markdown":
            _print_markdown_table(gk, rows)
            continue

        # 否则输出框线表格
        print(f"\n📂 {gk}（{len(items)}个标签）")

        # 列定义：(表头, 宽度, 对齐)
        cols = [
            ("标签ID", 8, "right"),
            ("来源", 6, "left"),
            ("相似度", 7, "right"),
            ("工程分", 7, "right"),
            ("标签量级", 7, "right"),
            ("覆盖率", 7, "right"),
            ("标签名称", 0, "left"),  # 自适应宽度
        ]
        # 自适应最后一列宽度
        max_name_w = max(
            sum(2 if ord(c) > 127 else 1 for c in r[6]) for r in rows
        ) if rows else 10
        cols[6] = ("标签名称", max(max_name_w + 2, 12), "left")

        # 构建框线
        def _make_border(left, mid, right, fill="─"):
            parts = [fill * w for _, w, _ in cols]
            return left + mid.join(parts) + right

        top_border = _make_border("┌", "┬", "┐")
        mid_border = _make_border("├", "┼", "┤")
        bot_border = _make_border("└", "┴", "┘")

        # 表头
        header_cells = [_pad(h, w, "center" if a in ("center",) else "left") for h, w, a in cols]
        # center not used but safe
        header_line = "│" + "│".join(header_cells) + "│"

        print(top_border)
        print(header_line)
        print(mid_border)
        for row in rows:
            cells = [_pad(row[i], cols[i][1], cols[i][2]) for i in range(len(cols))]
            print("│" + "│".join(cells) + "│")
        print(bot_border)

    # card格式：输出适合Octo Display Card消费的JSON，按维度分卡片，精简列
    if args.table_format == "card":
        card_data = {
            "groups": [],
            "gaps": gaps,
            "total_tags": total,
        }
        for gk, items in ordered_groups.items():
            rows = []
            for t in items:
                fr = t.get("audience_size")
                cr = t.get("coverage_rate")
                sub_prefix = "↳" if is_subdivision_tag(t.get("tagName", "")) else ""
                # 精简名称：合作标签前缀简化
                name = t.get("tagName", "")
                short_name = name
                # 已知前缀规则映射到简洁名（"基础属性_"和"基本属性_"两种都可能出现）
                prefix_rules = [
                    ("基础属性_居住城市级别_", ""),
                    ("基础属性_消费水平_", ""),
                    ("基础属性_年龄_", ""),
                    ("基础属性_职业_", ""),
                    ("基础属性_", ""),
                    ("基本属性_居住城市级别_", ""),
                    ("基本属性_消费水平_", ""),
                    ("基本属性_年龄_", ""),
                    ("基本属性_职业_", ""),
                    ("基本属性_", ""),
                    ("兴趣偏好_", ""),
                    ("线下场景_LBS__", ""),
                ]
                is_basic_dim = False
                for prefix, replace in prefix_rules:
                    if name.startswith(prefix):
                        short_name = name[len(prefix):]
                        is_basic_dim = True
                        break
                # 基础属性维度标签（性别/年龄/城市/消费/职业）不应该加↳，
                # 它们是同一维度下的不同选项，不是父子类关系
                if is_basic_dim:
                    sub_prefix = ""
                # 兴趣偏好子类也不加↳（除非本身有-后缀，那已经被is_subdivision_tag识别）
                if name.startswith(("兴趣偏好_", "基础属性_", "基本属性_")) and "-" not in short_name:
                    sub_prefix = ""
                rows.append({
                    "id": t.get("tagId"),
                    "name": sub_prefix + short_name,
                    "src": "明" if t.get("tagType") == 1 else "合",
                    "sim": round(t.get("similarity", 0), 3),
                    "fill": _fmt_size(fr),
                    "cov": _fmt_pct(cr),
                })
            card_data["groups"].append({
                "name": gk,
                "count": len(items),
                "rows": rows,
            })
        print("\n===CARD_DATA===")
        print(json.dumps(card_data, ensure_ascii=False))
        print("===END_CARD===")

    if gaps:
        print(f"\n⚠️ 缺口提示：以下核心维度没有找到可用标签 → {gaps}")
        print("   可能原因：标签池缺失该维度标签，或画像表未覆盖，或阈值过高。")

    # ⛔ 强制交互提示（AI必读）：Step 6完成后必须严格按以下顺序交互
    print("\n===STEP6_INTERACTIVE_PROMPT===")
    print(f"✅ 候选标签召回完成：过滤后{total}个可用，覆盖{len(ordered_groups)}个维度。")
    if gaps:
        print(f"⚠️ 缺口维度：{gaps}——需要告知用户缺口原因并处理")
    print("\n【AI必须执行的交互流程——禁止跳步】：")
    print("1. 先用一句话简要告知用户召回结果（标签数量、覆盖维度数、是否有缺口）")
    print("2. 检查是否有三方标签匹配（Step 6.5），如有则提示可展开查看")
    print("3. 询问用户：是否需要查看候选标签详情？")
    print("   - 回复\"展开\"：展示按维度分组的候选标签表（含相似度/覆盖率等画像指标）")
    print("   - 回复\"确认\"或\"跳过\"：进入Step 7推荐组合")
    print("4. 禁止直接跳到Step 7推荐组合，必须先完成以上询问")
    print("===END_STEP6_PROMPT===")


if __name__ == "__main__":
    main()