#!/usr/bin/env python3
"""
中国安装工程造价 - 定额关键词匹配引擎
适用标准：山东省安装工程消耗量定额（2025版，13分册）
数据源：index/quota_text_index_v4.json（从济南市价目表2026版PDF原版提取）

功能：
1. 从 index/ 目录加载 v4 索引数据
2. 按关键词检索匹配定额子目
3. 返回匹配结果（含分册号、章节号、项目名称、综合单价、工作内容）
4. 支持模糊匹配和精确匹配两种模式
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional

# ──────────────────────────────────────
# 配置
# ──────────────────────────────────────
# index/ 目录路径（相对于本脚本所在目录）
INDEX_DIR = Path(__file__).parent.parent / "index"
INDEX_FILE = INDEX_DIR / "quota_text_index_v4.json"
DATA_FILE = INDEX_DIR / "quota_data_v4.json"

# 专业分类关键词映射（2025版13分册）
CATEGORY_KEYWORDS = {
    # 第1册
    "机械设备安装": ["泵", "风机", "制冷设备", "压缩机", "离心泵", "轴流风机", "螺杆", "设备安装"],
    # 第2册
    "热力设备安装": ["锅炉", "换热器", "热力", "余热", "蒸发器", "凝汽器", "热管"],
    # 第3册
    "静置设备与金属结构": ["容器", "塔器", "储罐", "球罐", "金属平台", "钢梯", "栏杆", "静置设备"],
    # 第4册
    "电气设备安装": ["电气", "配电", "电缆", "桥架", "钢管敷设", "线槽", "母线", "灯具", "防雷", "接地", "变配电", "开关柜"],
    # 第5册
    "建筑智能化": ["综合布线", "安防", "监控", "门禁", "楼宇自控", "智能照明", "入侵报警", "DDC", "停车场"],
    # 第6册
    "自动化控制仪表": ["仪表", "温度仪表", "压力仪表", "流量计", "液位计", "传感器", "DCS", "PLC", "控制盘"],
    # 第7册
    "通风空调": ["通风", "风管", "空调", "风机", "盘管", "制冷", "暖通", "冷却塔", "消声器", "风口", "风阀"],
    # 第8册
    "工业管道": ["工业管道", "高压管道", "中压管道", "管道试压", "管道吹扫", "管道酸洗", "管道钝化", "低压管道", "碳钢管", "不锈钢管", "焊接"],
    # 第9册
    "消防工程": ["消防", "喷淋", "消火栓", "火灾报警", "气体灭火", "泡沫灭火", "防火卷帘", "消防联动", "探测器"],
    # 第10册
    "给排水采暖燃气": ["给水", "排水", "卫生器具", "雨水", "中水", "采暖", "散热器", "地暖", "燃气", "水表"],
    # 第11册
    "通信设备": ["电话", "网络", "光纤", "同轴电缆", "有线电视", "卫星电视", "通信设备", "交换机", "配线架"],
    # 第12册
    "刷油防腐绝热": ["除锈", "刷油", "防腐", "绝热", "保温", "耐火涂层", "涂料", "玻璃钢", "衬里"],
    # 第13册
    "措施项目": ["脚手架", "垂直运输", "高层增加费", "系统调试费", "安全文明施工", "措施项目"],
}

# 分册编号映射（用于输出分册名称）
VOLUME_MAP = {
    "1": "第1册 机械设备安装工程",
    "2": "第2册 热力设备安装工程",
    "3": "第3册 静置设备与工艺金属结构",
    "4": "第4册 电气设备安装工程",
    "5": "第5册 建筑智能化工程",
    "6": "第6册 自动化控制仪表安装工程",
    "7": "第7册 通风空调工程",
    "8": "第8册 工业管道工程",
    "9": "第9册 消防工程",
    "10": "第10册 给排水、采暖、燃气工程",
    "11": "第11册 通信设备与线缆安装工程",
    "12": "第12册 刷油、防腐蚀、绝热工程",
    "13": "第13册 措施项目",
}


# ──────────────────────────────────────
# 数据加载
# ──────────────────────────────────────

def load_index() -> List[Dict]:
    """
    加载 v4 索引数据。

    Returns:
        list of dict，每个元素包含 quota_no, name, spec, unit, base_price, volume, search_text
    """
    if not INDEX_FILE.exists():
        print(f"[WARN] 索引文件不存在：{INDEX_FILE}")
        return []

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    print(f"[INFO] 从 {INDEX_FILE.name} 加载 {len(index)} 条索引")
    return index


def load_full_data() -> Dict[str, Dict]:
    """
    加载完整定额数据（用于获取详细信息）。

    Returns:
        dict，key 为定额编号，value 为完整定额数据
    """
    if not DATA_FILE.exists():
        print(f"[WARN] 数据文件不存在：{DATA_FILE}")
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 建立定额编号 -> 数据的映射
    data_map = {}
    for item in data:
        quota_no = item.get("quota_no", "")
        if quota_no:
            data_map[quota_no] = item

    print(f"[INFO] 从 {DATA_FILE.name} 加载 {len(data_map)} 条定额数据")
    return data_map


# ──────────────────────────────────────
# 匹配引擎
# ──────────────────────────────────────

class QuotaMatcher:
    """
    定额匹配器（2025版13分册）。

    Usage:
        matcher = QuotaMatcher()
        results = matcher.match("低压钢管焊接")
        print(results)
    """

    def __init__(self, index_data: Optional[List[Dict]] = None):
        if index_data is None:
            self.index_data = load_index()
        else:
            self.index_data = index_data

        # 加载完整数据
        self.data_map = load_full_data()

    def match(
        self,
        query: str,
        category: Optional[str] = None,
        top_n: int = 5,
        min_score: float = 0.2,  # 降低阈值，提高召回率
    ) -> List[Dict]:
        """
        根据关键词查询匹配定额。

        Args:
            query:         工作内容关键词
            category:      专业类别（可选，用于Boost匹配分数）
            top_n:         返回最多 top_n 条结果
            min_score:     最低匹配分数阈值（0~1）

        Returns:
            list of dict，按匹配分数降序排列
        """
        query_lower = query.lower()
        # 改进的分词逻辑：同时支持中英文
        query_words = self._tokenize(query_lower)

        scored = []

        # 使用全部索引数据
        search_pool = self.index_data

        for q in search_pool:
            score = self._calc_score(query_lower, query_words, q)

            # 类别Boost：如果检测到类别，匹配类别的定额额外加分
            if category and category in CATEGORY_KEYWORDS:
                cat_keywords = CATEGORY_KEYWORDS[category]
                volume = q.get("volume", "").lower()
                name = q.get("name", "").lower()
                if any(kw in volume or kw in name for kw in cat_keywords):
                    score += 0.15  # 类别匹配额外加分

            if score >= min_score:
                q_copy = q.copy()
                # 尝试获取完整数据
                quota_no = q.get("quota_no", "")
                if quota_no in self.data_map:
                    full_data = self.data_map[quota_no].copy()
                    full_data.update(q_copy)
                    q_copy = full_data
                q_copy["match_score"] = round(score, 4)
                scored.append(q_copy)

        scored.sort(key=lambda x: x["match_score"], reverse=True)
        return scored[:top_n]

    def _tokenize(self, text: str) -> set:
        """改进的分词逻辑"""
        # 1. 先按分隔符分割
        parts = re.split(r"[\s\-_，、。,;；]+", text)
        words = set()

        # 2. 对每个部分进一步分词
        for part in parts:
            if not part:
                continue
            # 如果包含中文，按2字词语+单字分词
            if re.search(r'[\u4e00-\u9fff]', part):
                # 添加完整词
                words.add(part)
                # 2字词
                if len(part) >= 2:
                    for i in range(len(part) - 1):
                        words.add(part[i:i+2])
                # 单字
                for ch in part:
                    if ch.strip():
                        words.add(ch)
            else:
                words.add(part)

        return words

    def _calc_score(self, query: str, query_words: set, quota: Dict) -> float:
        """计算匹配分数（关键词加权）。"""
        name = quota.get("name", "").lower()
        search_text = quota.get("search_text", "").lower()
        spec = quota.get("spec", "").lower()
        volume = quota.get("volume", "").lower()

        score = 0.0

        # 精确匹配（整个查询词）
        if query in name:
            score += 0.6
        if query in search_text:
            score += 0.4
        if query in volume:
            score += 0.5  # 分册名称匹配很重要
        if query in spec:
            score += 0.3

        # 关键词分别匹配（拆分成多个词）
        matched_words = 0
        for word in query_words:
            if len(word) < 1:  # 允许单字匹配
                continue
            word_score = 0.0
            if word in name:
                word_score = 0.15
            if word in search_text:
                word_score = max(word_score, 0.1)
            if word in volume:
                word_score = max(word_score, 0.12)
            if word in spec:
                word_score = max(word_score, 0.08)
            score += word_score
            if word_score > 0:
                matched_words += 1

        # 奖励：多个关键词都匹配到
        if matched_words >= 2:
            score += 0.1 * (matched_words - 1)

        # 规格模式匹配
        spec_patterns = re.findall(r"[\w\.]+", query)
        for pat in spec_patterns:
            if len(pat) >= 3 and pat in spec:
                score += 0.1

        return min(score, 1.0)

    def match_bim_element(self, element: Dict) -> List[Dict]:
        """
        根据 BIM 元素属性匹配定额。

        Args:
            element: dict，至少含 type（类型）、material（材质）、
                     description（描述）等字段

        Returns:
            list of dict，匹配结果
        """
        elem_type = element.get("type", "")
        material = element.get("material", "")
        desc = element.get("description", "")

        query_parts = []
        if elem_type:
            query_parts.append(elem_type)
        if material:
            query_parts.append(material)
        if desc:
            query_parts.append(desc)

        query = " ".join(query_parts)
        return self.match(query, top_n=3)

    def detect_category(self, query: str) -> str:
        """
        根据查询词判断最可能的专业类别（13分册）。

        Returns:
            category name 或 "通用"
        """
        query_lower = query.lower()
        best_cat = "通用"
        best_score = 0

        for cat, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            if score > best_score:
                best_score = score
                best_cat = cat

        return best_cat if best_score > 0 else "通用"

    def get_volume_list(self) -> List[str]:
        """返回所有已加载的分册名称列表。"""
        seen = set()
        result = []
        for q in self.index_data:
            vol = q.get("volume", "")
            if vol and vol not in seen:
                seen.add(vol)
                result.append(vol)
        return result

    def get_by_quota_no(self, quota_no: str) -> Optional[Dict]:
        """根据定额编号精确查询。"""
        if quota_no in self.data_map:
            return self.data_map[quota_no].copy()
        return None


# ──────────────────────────────────────
# 交互式查询（CLI 演示）
# ──────────────────────────────────────

def interactive_query():
    """交互式定额查询（调试用）。"""
    print("\n===== 定额匹配引擎（2025版13分册）- 交互查询 =====")
    print("输入工作内容关键词查询定额，输入 'q' 退出")
    print("输入 'd 8-3-28' 查看定额详情\n")

    matcher = QuotaMatcher()
    if not matcher.index_data:
        print("[WARN] 未加载任何索引数据，请先运行重建索引脚本")
        return

    print(f"已加载 {len(matcher.index_data)} 条索引")
    print(f"已加载分册：{', '.join(matcher.get_volume_list())}\n")

    while True:
        try:
            query = input("查询 >> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if query.lower() in ("q", "quit", "exit"):
            break
        if not query:
            continue

        # 详情查询
        if query.startswith("d ") or query.startswith("D "):
            quota_no = query[2:].strip()
            detail = matcher.get_by_quota_no(quota_no)
            if detail:
                print(f"\n=== 定额详情：{quota_no} ===")
                for key, value in detail.items():
                    print(f"  {key}: {value}")
                print()
            else:
                print(f"  未找到定额：{quota_no}\n")
            continue

        # 检测类别
        cat = matcher.detect_category(query)
        results = matcher.match(query, category=cat, top_n=5)

        if not results:
            print("  未找到匹配定额，请尝试其他关键词。")
            print("  提示：可输入规格参数（如 φ57、DN50）或材料名称\n")
            continue

        print(f"\n检测专业类别：{cat}")
        print(f"找到 {len(results)} 条匹配结果：\n")
        for i, r in enumerate(results, 1):
            print(f"  [{i}] 分册：{r.get('volume', '未知')}")
            print(f"      定额编号：{r.get('quota_no', '')}")
            print(f"      项目名称：{r.get('name', '')}")
            print(f"      规格：{r.get('spec', '')}")
            print(f"      单位：{r.get('unit', '')}")
            print(f"      综合单价(含税)：{r.get('base_price', 0)} 元")
            if "labor_fee" in r:
                print(f"      人工费：{r['labor_fee']} 元")
                print(f"      材料费：{r.get('material_fee', 0)} 元")
                print(f"      机械费：{r.get('machine_fee', 0)} 元")
            print(f"      搜索文本：{r.get('search_text', '')[:50]}...")
            print(f"      匹配分：{r['match_score']:.2f}")
            print()
        print()


if __name__ == "__main__":
    interactive_query()
