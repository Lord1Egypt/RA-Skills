"""
意图分类器 — 识别用户想画什么类型的图
基于关键词匹配 + 规则推理，无需训练模型
"""
from typing import Dict, List, Optional, Tuple
import re


class IntentClassifier:
    """
    自然语言意图 → 标准意图标识

    支持的意图类别：
    - arch_floor_plan     建筑平面图
    - mech_bolt           螺栓
    - mech_gear           齿轮
    - mech_bearing        轴承
    - mech_spring         弹簧
    - elec_switch         开关
    - elec_socket         插座
    - elec_lamp           灯具
    - elec_wires          导线组
    - pipe_straight       直管段
    - pipe_elbow          弯头
    - pipe_valve          阀门
    - pipe_tee            三通/四通
    - struct_beam         梁断面配筋
    - struct_slab         楼板配筋
    - struct_footing      独立基础
    - geo_rectangle       矩形
    - geo_circle          圆
    - geo_polygon         正多边形
    """

    # ============================================================
    # 意图规则库 —— 每条规则：[权重, 意图ID, 关键词列表]
    # 权重越高越优先匹配；同一意图可有多条规则（取最高分）
    # ============================================================

    RULES = [
        # ---------- 建筑 ----------
        (100, "arch_floor_plan", [
            "平面图", "户型图", "建筑平面", "房间", "外墙",
            "开(一|两|三)扇门", "开(一|两|三)扇窗", "画.*房",
            "3600x4800", "4000x3000", "A3.*建筑", "施工图(?!(配筋|结构))",
            "墙体", "墙厚", "柱子(?![配])", "楼梯(?!配)",
        ]),

        # ---------- 机械 ----------
        (95, "mech_bolt", [
            "螺栓", "螺钉", "螺丝头", "六角头", "十字槽",
            "[Mm]\\d+.*(螺栓|螺钉)", "螺栓.*俯视",
        ]),
        (90, "mech_gear", [
            "齿轮", "齿(轮)?端面", "\\d+齿.*齿轮",
            "齿顶圆", "齿根圆", "径向齿形",
        ]),
        (88, "mech_bearing", [
            "轴承", "滚珠轴承", "滚动体", "(620[0-9]|62[0-4][0-9]).*轴承",
            "内外圈.*轴承", "轴承.*(侧面|端面|剖)",
        ]),
        (85, "mech_spring", [
            "弹簧", "压缩弹簧", "拉伸弹簧", "扭转弹簧",
            "线径.*弹簧", "外径.*圈数", "有效圈数",
            "(锯齿|波浪).*(弹|簧)", "弹簧.*侧视",
        ]),

        # ---------- 电气 ----------
        (92, "elec_switch", [
            "开关符号?", "(单极|双极|三极).*开关", "断路器符号?",
            "开关.*(垂直|水平|横放|竖放)", "触点.*开关",
        ]),
        (90, "elec_socket", [
            "插座", "电源插座", "(三孔|五孔|单相|三相).*插",
            "墙壁插座", "地插",
        ]),
        (88, "elec_lamp", [
            "灯具?符号?", "(吸顶灯|长条灯|壁灯|筒灯|射灯|轨道灯|路灯)",
            "灯.*符号", "(荧光灯|日光灯)",
        ]),
        (85, "elec_wires", [
            "导线组", "(\\d+)相导线", "(三相|两相|单相).*线",
            "平行导线", "电线组", "(火线|零线|地线).*间距",
        ]),

        # ---------- 管道 ----------
        (90, "pipe_straight", [
            "直管段", "(DN\\d+).*(直管|管道)", "双线.*管",
            "带中心线.*管", "直管道",
        ]),
        (88, "pipe_elbow", [
            "弯头", "90度.*弯", "45度.*弯",
            "R\\d+.*弯头", "弯头.*(东北|西北|东南|西南)",
        ]),
        (87, "pipe_valve", [
            "阀门", "(闸阀|截止阀|球阀|蝶阀|止回阀)",
            "(阀门|阀).*DN\\d+", "阀体.*手轮",
        ]),
        (85, "pipe_tee", [
            "三通", "四通", "(等径|异径|变径).*三通",
            "DN\\d+/DN\\d+.*三通", "主管.*支管",
        ]),
        (80, "pipe_generic", [
            "法兰", "大小头", "异径管", "管帽",
            "(法兰|大小头|管帽).*DN",
        ]),

        # ---------- 结构 ----------
        (95, "struct_beam", [
            "梁断面", "梁.*配筋", "梁截面", "配筋梁",
            "\\d+x\\d+.*梁.*(配筋|钢筋|断面|截面)",
            "箍筋.*纵筋", "混凝土.*梁",
        ]),
        (90, "struct_slab", [
            "楼板配筋", "板.*配筋", "双向配筋",
            "楼板.*厚度.*钢筋", "(底筋|面筋|负筋).*楼板",
            "\\d+厚.*板.*钢筋",
        ]),
        (88, "struct_footing", [
            "独立基础", "柱下基础", "基础详图(?!(钢))",
            "台阶式基础", "垫层.*受力筋",
            "条形基础", "基础.*配筋",
        ]),

        # ---------- 通用几何 ----------
        (70, "geo_rectangle", [
            "矩形", "画一个.*矩形", "长方形",
            "\\d+x\\d+.*(矩形|长方)", "(宽|高).*矩形",
        ]),
        (70, "geo_circle", [
            "^画.*圆$", "圆形", "同心圆",
            "圆心.*半径", "直径.*圆",
            "circle", "圆.*(半径|R\\d+)",
        ]),
        (68, "geo_polygon", [
            "正多边形", "正(三角|四|五|六|八)边",
            "正多边形.*外接圆", "正(方|六|八)(形|边形)",
        ]),
    ]

    # ============================================================
    # 评分引擎
    # ============================================================

    @classmethod
    def _score(cls, text: str, pattern: str) -> float:
        """计算单个模式对文本的匹配得分"""
        try:
            if re.search(pattern, text):
                # 更长的匹配、更具体的关键词得更高分
                match = re.search(pattern, text)
                return len(match.group()) / max(len(text), 1) * 100 + 50
        except re.error:
            pass

        # 简单包含检查
        if pattern in text:
            return 40.0

        return 0.0

    @classmethod
    def _score_rule(cls, text: str, rule: Tuple) -> float:
        """计算一条规则的总体得分"""
        weight, intent_id, patterns = rule
        scores = [cls._score(text, p) for p in patterns]
        max_score = max(scores) if scores else 0
        return max_score * (weight / 100)

    @staticmethod
    def _is_likely_architecture(text: str) -> bool:
        """快速判断是否偏向建筑工程领域"""
        arch_keywords = [
            '墙', '门', '窗', '柱', '楼梯', '阳台', '卫生间', '厨房',
            '卧室', '客厅', '平面图', '户型', '开间', '进深',
            '砖混', '框架', '剪力墙', '外墙', '内墙',
        ]
        return sum(1 for kw in arch_keywords if kw in text) >= 2

    @staticmethod
    def _is_mechanical(text: str) -> bool:
        """快速判断是否偏向机械领域"""
        mech_keywords = [
            '螺栓', '螺母', '齿轮', '轴承', '弹簧', '键槽', '销钉',
            '垫圈', '螺纹', '轴', '孔', '倒角', '公差',
            'M16', 'M20', '俯视图', '侧视图', '剖面图',
        ]
        return any(kw in text for kw in mech_keywords)

    @staticmethod
    def _is_electrical(text: str) -> bool:
        """快速判断是否偏向电气领域"""
        elec_keywords = [
            '开关', '插座', '灯具', '配电箱', '断路器',
            '导线', '线路', '回路', '相线', '零线', '接地',
            '吸顶灯', '荧光灯', '壁灯',
        ]
        return any(kw in text for kw in elec_keywords)

    @staticmethod
    def _is_piping(text: str) -> bool:
        """快速判断是否偏向管道领域"""
        pipe_keywords = [
            '弯头', '三通', '法兰', '阀门', '闸阀', '球阀',
            '直管', '管道', 'DN', '大小头', '管帽', '蝶阀',
        ]
        return any(kw in text for kw in pipe_keywords)

    @staticmethod
    def _is_structural(text: str) -> bool:
        """快速判断是否偏向结构工程"""
        struct_keywords = [
            '梁', '板', '柱', '基础', '配筋', '钢筋', '箍筋',
            '混凝土', 'C30', 'C25', '楼板', '地基', '承台',
            '独立基础', '条基', '桩', '负筋', '分布筋',
        ]
        return any(kw in text for kw in struct_keywords)

    # ============================================================
    # 主入口
    # ============================================================

    @classmethod
    def classify(cls, text: str) -> str:
        """
        分类用户自然语言输入的绘图意图

        Args:
            text: 用户输入的自然语言

        Returns:
            意图标识字符串，如 "arch_floor_plan"
        """

        # 计算每条规则的得分
        scored_rules = []
        for rule in cls.RULES:
            score = cls._score_rule(text, rule)
            if score > 0:
                scored_rules.append((rule[1], score))

        if not scored_rules:
            # 无明确匹配 — 回退到几何图形
            return cls._fallback_classify(text)

        # 按得分排序
        scored_rules.sort(key=lambda x: x[1], reverse=True)
        best_intent, best_score = scored_rules[0]

        # 如果前两名得分接近，用领域启发式打破平局
        if len(scored_rules) >= 2:
            second_intent, second_score = scored_rules[1]
            if abs(best_score - second_score) < 10:
                best_intent = cls._tiebreak(text, best_intent, second_intent)

        return best_intent

    @classmethod
    def _tiebreak(cls, text: str, intent_a: str, intent_b: str) -> str:
        """当两个意图得分接近时，用领域启发式选择"""

        domain_checkers = {
            "arch": cls._is_likely_architecture,
            "mech": cls._is_mechanical,
            "elec": cls._is_electrical,
            "pipe": cls._is_piping,
            "struct": cls._is_structural,
        }

        for domain_name, checker in domain_checkers.items():
            if checker(text):
                # 检查哪个意图属于该领域
                a_in_domain = intent_a.split('_')[0] in {
                    'arch': ['arch'],
                    'mech': ['mech'],
                    'elec': ['elec'],
                    'pipe': ['pipe'],
                    'struct': ['struct'],
                }.get(domain_name, [])
                b_in_domain = intent_b.split('_')[0] in {
                    'arch': ['arch'],
                    'mech': ['mech'],
                    'elec': ['elec'],
                    'pipe': ['pipe'],
                    'struct': ['struct'],
                }.get(domain_name, [])

                if a_in_domain and not b_in_domain:
                    return intent_a
                elif b_in_domain and not a_in_domain:
                    return intent_b

        # 无法区分，返回得分更高的
        return intent_a

    @classmethod
    def _fallback_classify(cls, text: str) -> str:
        """回退分类：无规则匹配时的兜底策略"""

        # 检查是否有尺寸描述
        has_size = bool(cls.SIZE_PATTERN.search(text))

        if has_size or '画' in text:
            # 有尺寸或"画"字，默认为矩形
            return "geo_rectangle"

        if '圆' in text:
            return "geo_circle"

        if any(w in text for w in ['三角', '四边', '五边', '六边', '八边', '多边形']):
            return "geo_polygon"

        # 完全无法分类
        return "unknown"

    SIZE_PATTERN = re.compile(r'\d+\s*[x×*]\s*\d+', re.IGNORECASE)

    # ============================================================
    # 调试工具
    # ============================================================

    @classmethod
    def debug_classify(cls, text: str) -> str:
        """调试模式：输出所有规则的评分详情"""
        lines = [f"=== 意图分类调试 ===", f"文本: {text}", f"---"]

        scored = []
        for rule in cls.RULES:
            score = cls._score_rule(text, rule)
            if score > 0:
                scored.append((rule[1], score))

        scored.sort(key=lambda x: x[1], reverse=True)

        for intent, score in scored[:5]:
            marker = " ← 最佳" if intent == scored[0][0] else ""
            lines.append(f"  {intent}: {score:.1f}{marker}")

        result = cls.classify(text)
        lines.append(f"---")
        lines.append(f"最终选择: {result}")

        # 领域检测
        lines.append(f"--- 领域检测:")
        lines.append(f"  建筑: {cls._is_likely_architecture(text)}")
        lines.append(f"  机械: {cls._is_mechanical(text)}")
        lines.append(f"  电气: {cls._is_electrical(text)}")
        lines.append(f"  管道: {cls._is_piping(text)}")
        lines.append(f"  结构: {cls._is_structural(text)}")

        return '\n'.join(lines)

    @classmethod
    def list_intents(cls) -> List[str]:
        """列出所有支持的意图类型"""
        intents = list(set(rule[1] for rule in cls.RULES))
        intents.sort()
        return intents
