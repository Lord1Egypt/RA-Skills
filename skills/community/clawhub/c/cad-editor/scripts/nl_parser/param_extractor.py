"""
参数提取器 — 从自然语言中提取精确的绘图参数
支持：尺寸、数量、位置、方向、材料、规格等参数的智能识别
"""
from typing import Dict, List, Any, Optional, Tuple
import re
import json


class ParamExtractor:
    """
    从用户自然语言输入中提取结构化参数

    核心策略：
    1. 正则匹配数值+单位
    2. 关键词语义识别（门/窗/螺栓/钢筋...）
    3. 上下文推理（"4000x3000房间" → width=4000, depth=3000）
    4. 行业默认值填充
    """

    # ============================================================
    # 正则模式库
    # ============================================================

    # 尺寸模式：4000x3000 / 4000×3000 / 4000*3000 / 4000 3000
    SIZE_PATTERN = re.compile(
        r'(\d+(?:\.\d+)?)\s*[x×x*\s]\s*(\d+(?:\.\d+)?)',
        re.IGNORECASE
    )

    # 单个数值带单位：M16 / DN50 / 1200mm / R100
    SINGLE_VALUE_PATTERNS = {
        'metric_mm': re.compile(r'(\d+(?:\.\d+)?)\s*(?:mm|毫米)', re.IGNORECASE),
        'metric_m': re.compile(r'(\d+(?:\.\d+)?)\s*(?:m|米)', re.IGNORECASE),
        'bolt_size': re.compile(r'[Mm](\d+(?:\.\d+)?)'),           # M16 → 16
        'dn': re.compile(r'[Dd][Nn](\d+(?:\.\d+)?)'),              # DN50 → 50
        'radius': re.compile(r'[Rr](\d+(?:\.\d+)?)'),              # R100 → 100
        'bearing_model': re.compile(r'(\d{4})[型式]?\s*(?:轴承)?'), # 6205轴承
        'diameter_d': re.compile(r'[Dd](\d{2,4})'),                # D100 → 100
        'bare_number': re.compile(r'(?<![a-zA-Z])(\d{2,4})(?![\d.])'),
    }

    # 钢筋规格：3根16 / 14@150 / 12@150/10@200
    REBAR_PATTERN = re.compile(
        r'(\d+)\s*根\s*(\d+)\s*'      # "3根16"
        r'|'
        r'(\d+)\s*@\s*(\d+)'          # "14@150"
    )
    REBAR_DUAL = re.compile(
        r'(\d+)@(\d+)/(\d+)@(\d+)'     # "12@150/10@200" 双向配筋
    )

    # 数量词
    COUNT_PATTERN = re.compile(r'(\d+)\s*(扇|根|个|只|步|齿|圈|层|相)')

    # 方向/方位
    DIRECTION_MAP = {
        '水平': 'H', '垂直': 'V', '竖直': 'V', '纵向': 'V',
        '东北': 'NE', '西北': 'NW', '东南': 'SE', '西南': 'SW',
        '东': 'E', '西': 'W', '南': 'S', '北': 'N',
        '上': 'N', '下': 'S', '左': 'W', '右': 'E',
    }

    # 图纸规格
    PAPER_SIZES = {
        'A0': (1189, 841), 'A1': (841, 594), 'A2': (594, 420),
        'A3': (420, 297), 'A4': (297, 210),
    }

    # ============================================================
    # 门/窗识别
    # ============================================================

    @staticmethod
    def _extract_doors(text: str) -> List[Dict]:
        """从文本中识别门的数量和规格"""
        doors = []

        # "一扇900宽的门" / "开一扇900宽的门"
        door_matches = re.findall(
            r'(?:一扇|单扇)?(\d*)\s*(?:宽的?)?门(?:单扇|双扇)?',
            text
        )
        widths = re.findall(r'(\d+)\s*宽\s*的门', text)

        if '双开' in text or '双扇' in text or '双开门' in text:
            door_type = 'double'
            w = int(widths[0]) if widths else 1500
        elif '子母' in text:
            door_type = 'mother_son'
            w = int(widths[0]) if widths else 1200
        else:
            door_type = 'single'
            w = int(widths[0]) if widths else 900

        count_match = ParamExtractor.COUNT_PATTERN.search(text)
        count = int(count_match.group(1)) if count_match else 1

        for i in range(count):
            doors.append({
                'position': (1000 + i * 2000, 0),  # 默认均匀分布在底边
                'width': w,
                'type': door_type,
            })

        return doors

    @staticmethod
    def _extract_windows(text: str) -> List[Dict]:
        """从文本中识别窗的数量和规格"""
        windows = []

        # "两扇1200x1500的窗" / "两扇1200的窗"
        window_sizes = ParamExtractor.SIZE_PATTERN.findall(text)
        win_widths = re.findall(r'(\d+)\s*(?:宽|x|×|\*)\s*(\d+)?\s*的?窗', text)

        count_match = re.search(r'(\d+)\s*扇\s*(?:的?)?窗', text)
        count = int(count_match.group(1)) if count_match else (
            2 if '两扇' in text else ('两' in text and 2 or 1)
        )

        default_w = 1200
        default_h = 1500

        if window_sizes:
            default_w = int(float(window_sizes[0][0]))
            default_h = int(float(window_sizes[0][1])) if window_sizes[0][1] else default_h
        elif win_widths:
            default_w = int(win_widths[0][0])
            default_h = int(win_widths[0][1]) if win_widths[0][1] else default_h

        spacing = max(default_w + 200, 1500)
        for i in range(count):
            windows.append({
                'start': (800 + i * spacing, 240),
                'end': (800 + i * spacing + default_w, 240),
                'width': default_w,
                'height': default_h,
            })

        return windows

    # ============================================================
    # 机械零件参数
    # ============================================================

    @staticmethod
    def _extract_mech_params(text: str) -> Dict[str, Any]:
        """机械零件参数提取"""
        params = {}

        # 螺栓规格
        bolt_m = re.search(r'[Mm](\d+(?:\.\d+)?)', text)
        if bolt_m:
            params['size'] = float(bolt_m.group(1))

        bolt_types = {'六角': 'hex', '十字': 'phillips', '一字': 'flat', '内六角': 'socket'}
        for keyword, btype in bolt_types.items():
            if keyword in text:
                params['bolt_type'] = btype
                break

        # 齿轮参数
        teeth_m = re.search(r'(\d+)\s*齿', text)
        if teeth_m:
            params['teeth'] = int(teeth_m.group(1))

        d_m = ParamExtractor.SINGLE_VALUE_PATTERNS['diameter_d'].search(text)
        if d_m:
            params['pitch_diameter'] = float(d_m.group(1))

        bore_m = re.search(r'(?:轴孔|孔径|孔)[Dd]?(\d+)', text)
        if bore_m:
            params['bore_diameter'] = float(bore_m.group(1))

        # 轴承
        bearing_m = re.search(r'(\d{4})', text)
        if bearing_m and ('轴承' in text):
            params['bearing_model'] = bearing_m.group(1)

        # 弹簧
        wire_m = re.search(r'(?:线径|丝径|钢丝直径)[Dd]?(\d+(?:\.\d+)?)', text)
        if wire_m:
            params['wire_diameter'] = float(wire_m.group(1))

        outer_m = re.search(r'(?:外径|外圈)[Dd]?(\d+(?:\.\d+)?)', text)
        if outer_m:
            params['spring_outer_diameter'] = float(outer_m.group(1))

        coil_m = re.search(r'(\d+)\s*(?:圈|有效圈)', text)
        if coil_m:
            params['active_coils'] = int(coil_m.group(1))

        # 视图方向
        if '俯视' in text or '俯视图' in text or '顶视' in text:
            params['view'] = 'top'
        elif '侧视' in text or '侧面' in text or '侧视图' in text:
            params['view'] = 'side'
        elif '端面' in text or '端视图' in text:
            params['view'] = 'face'

        return params

    # ============================================================
    # 管道参数
    # ============================================================

    @staticmethod
    def _extract_pipe_params(text: str) -> Dict[str, Any]:
        """管道系统参数提取"""
        params = {}

        # DN 规格
        dn_m = ParamExtractor.SINGLE_VALUE_PATTERNS['dn'].search(text)
        if dn_m:
            params['dn'] = float(dn_m.group(1))

        # 弯头半径
        r_m = ParamExtractor.SINGLE_VALUE_PATTERNS['radius'].search(text)
        if r_m:
            params['radius'] = float(r_m.group(1))

        # 方向
        for direction, code in ParamExtractor.DIRECTION_MAP.items():
            if direction in text:
                if direction in ['东北', '西北', '东南', '西南']:
                    params['turn_direction'] = code
                elif direction in ['水平', '垂直']:
                    params['direction'] = code
                break

        # 阀门类型
        valve_types = {
            '闸阀': 'gate', '截止阀': 'globe', '球阀': 'ball',
            '蝶阀': 'butterfly', '止回阀': 'check', '截止': 'globe',
        }
        for vname, vcode in valve_types.items():
            if vname in text:
                params['valve_type'] = vcode
                break

        # 三通类型
        if '三通' in text:
            params['tee_type'] = 'tee'
        elif '四通' in text:
            params['tee_type'] = 'cross'

        # 异径管
        size_m = re.search(r'DN(\d+)\s*/\s*DN(\d+)', text, re.IGNORECASE)
        if size_m:
            params['main_dn'] = float(size_m.group(1))
            params['branch_dn'] = float(size_m.group(2))
        elif '大小头' in text or '异径' in text:
            params['main_dn'] = params.get('dn', 50)
            params['branch_dn'] = params.get('main_dn', 50) * 0.8

        # 管长
        length_m = re.search(r'(?:长度|长|L)(\d+)', text)
        if length_m:
            params['length'] = float(length_m.group(1))

        return params

    # ============================================================
    # 结构参数
    # ============================================================

    @staticmethod
    def _extract_struct_params(text: str) -> Dict[str, Any]:
        """结构详图参数提取"""
        params = {}

        # 梁断面：250x500梁 / 梁250x500
        beam_m = re.search(r'(\d+)\s*[x×]\s*(\d+)\s*(?:的?)?(?:梁)', text)
        if beam_m:
            params['beam_width'] = int(beam_m.group(1))
            params['beam_height'] = int(beam_m.group(2))

        # 配筋
        rebar_m = re.search(r'配?(\d+)根(\d+)\s*(?:底部|底筋|纵筋)?', text)
        if rebar_m:
            params['bottom_rebar'] = f"{rebar_m.group(1)}根{rebar_m.group(2)}"

        top_m = re.search(r'(?:顶部|面筋|负筋)(\d+)根(\d+)', text)
        if top_m:
            params['top_rebar'] = f"{top_m.group(1)}根{top_m.group(2)}"

        stirrup_m = re.search(r'(?:箍筋|箍)(\d+)@(\d+)', text)
        if stirrup_m:
            params['stirrup'] = f"{stirrup_m.group(1)}@{stirrup_m.group(2)}"
        elif '箍筋' in text:
            params['stirrup'] = "8@200"

        # 混凝土等级
        concrete_m = re.search(r'(C\d+[a-zA-Z]?)', text, re.IGNORECASE)
        if concrete_m:
            params['concrete_grade'] = concrete_m.group(1).upper()

        # 板厚
        slab_m = re.search(r'(\d+)\s*(?:厚|mm厚的?板|楼板)', text)
        if slab_m:
            params['slab_thickness'] = int(slab_m.group(1))

        # 双向配筋
        dual_m = ParamExtractor.REBAR_DUAL.search(text)
        if dual_m:
            params['bottom_x_rebar'] = f"{dual_m.group(1)}@{dual_m.group(2)}"
            params['bottom_y_rebar'] = f"{dual_m.group(3)}@{dual_m.group(4)}"

        # 基础
        footing_m = re.search(
            r'(\d+)\s*[x×]\s*(\d+)\s*(?:柱|柱下)?.*?独立基础.*?(\d+)\s*[x×]\s*(\d+).*?深(\d+)',
            text
        )
        if footing_m:
            params['col_width'] = int(footing_m.group(1))
            params['col_height'] = int(footing_m.group(2))
            params['base_width'] = int(footing_m.group(3))
            params['base_depth'] = int(footing_m.group(4))
            params['foundation_depth'] = int(footing_m.group(5))

        # 基础钢筋
        footing_rebar = re.search(r'(?:基础|垫层).*(\d+)@(\d+)', text)
        if footing_rebar:
            params['footing_rebar'] = f"{footing_rebar.group(1)}@{footing_rebar.group(2)}"

        return params

    # ============================================================
    # 电气参数
    # ============================================================

    @staticmethod
    def _extract_elec_params(text: str) -> Dict[str, Any]:
        """电气符号参数提取"""
        params = {}

        # 开关极数
        pole_map = {
            '单极': 1, '一开': 1, '1开': 1,
            '双极': 2, '二开': 2, '2开': 2,
            '三极': 3, '三开': 3, '3开': 3,
        }
        for keyword, poles in pole_map.items():
            if keyword in text:
                params['poles'] = poles
                break

        # 方向
        orientation = 'V'  # 默认垂直
        if any(kw in text for kw in ['水平', '横放', '横向']):
            orientation = 'H'
        params['orientation'] = orientation

        # 插座类型
        socket_map = {
            '三孔': '3pin', '五孔': '5pin', '单相': '1phase',
            '三相': '3phase', '地插': 'floor', '壁装': 'wall',
        }
        for skw, stype in socket_map.items():
            if skw in text:
                params['socket_type'] = stype
                break

        # 灯具类型
        lamp_map = {
            '吸顶灯': 'ceiling', '吸顶': 'ceiling',
            '长条灯': 'linear', '荧光灯': 'linear', '日光灯': 'linear',
            '壁灯': 'wall', '筒灯': 'downlight', '射灯': 'spot',
            '轨道灯': 'track', '路灯': 'street',
        }
        for lkw, ltype in lamp_map.items():
            if lkw in text:
                params['lamp_type'] = ltype
                break

        # 导线相数和间距
        phase_m = re.search(r'(\d)\s*相', text)
        if phase_m:
            params['phases'] = int(phase_m.group(1))

        spacing_m = re.search(r'间距\s*(\d+)', text)
        if spacing_m:
            params['spacing'] = int(spacing_m.group(1))

        return params

    # ============================================================
    # 建筑平面图参数
    # ============================================================

    @staticmethod
    def _extract_arch_params(text: str) -> Dict[str, Any]:
        """建筑平面图参数提取"""
        params = {}

        # 主尺寸：4000x3000 / 3600x4800
        size_m = ParamExtractor.SIZE_PATTERN.search(text)
        if size_m:
            params['width'] = int(float(size_m.group(1)))
            params['depth'] = int(float(size_m.group(2)))

        # 图纸规格
        for ps_name in ParamExtractor.PAPER_SIZES:
            if ps_name in text.upper():
                params['paper_size'] = ps_name
                break

        # 墙厚（常见值）
        wall_map = {240: ['240'], 200: ['200'], 180: ['180'], 120: ['120']}
        for thickness, keywords in wall_map.items():
            if any(kw in text for kw in keywords):
                params['wall_thickness'] = thickness
                break

        # 楼梯
        stair_steps_m = re.search(r'(\d+)\s*步', text)
        if stair_steps_m:
            params['stair_steps'] = int(stair_steps_m.group(1))

        stair_width_m = re.search(r'(?:宽度|宽)(\d+)', text)
        if stair_width_m:
            params['stair_width'] = int(stair_width_m.group(1))

        # 提取门窗
        params['doors'] = ParamExtractor._extract_doors(text)
        params['windows'] = ParamExtractor._extract_windows(text)

        # Title
        title_m = re.search(r'(?:title|named?|called?)\s*["\']?([^"\'\uff0c\uff1b]+)', text, re.IGNORECASE)
        if title_m:
            params['title'] = title_m.group(1)

        return params

    # ============================================================
    # 几何图形参数
    # ============================================================

    @staticmethod
    def _extract_geo_params(text: str) -> Dict[str, Any]:
        """通用几何图形参数提取"""
        params = {}

        # 矩形尺寸
        rect_m = ParamExtractor.SIZE_PATTERN.search(text)
        if rect_m:
            params['rect_width'] = int(float(rect_m.group(1)))
            params['rect_height'] = int(float(rect_m.group(2)))

        # 圆半径
        radius_m = re.search(r'(?:半径|r|R)(\d+(?:\.\d+)?)', text)
        if radius_m:
            params['radius'] = float(radius_m.group(1))

        # 圆心坐标
        center_m = re.search(r'(?:圆心|中心)[(（](\d+)\s*[,\s，]\s*(\d+)[)）]', text)
        if center_m:
            params['center_x'] = float(center_m.group(1))
            params['center_y'] = float(center_m.group(2))

        # 多边形边数
        poly_map = {
            '三角': 3, '三角形': 3,
            '正方': 4, '方形': 4, '矩形': 4,
            '五边': 5, '五边形': 5,
            '六边': 6, '六边形': 6,
            '八边': 8, '八边形': 8,
            '正多边形': 6,  # 默认六边形
        }
        for pword, sides in poly_map.items():
            if pword in text:
                params['sides'] = sides
                break

        # 外接圆/内切圆半径
        circum_m = re.search(r'(?:外接圆|外圆)[半径rR]?(\d+)', text)
        if circum_m:
            params['circumradius'] = int(circum_m.group(1))

        # 同心圆组
        concentric = re.findall(r'(?:直径|D)(\d+)', text)
        if len(concentric) >= 2:
            params['concentric_diameters'] = [int(d) for d in concentric]

        # 图层/颜色
        layer_m = re.search(r'(?:layer|layer)[\"\']?\s*(\w+)', text, re.IGNORECASE)
        if layer_m:
            params['layer'] = layer_m.group(1)

        # Color
        color_m = re.search(r'(?:color|#)([0-9a-fA-F]{6}|\d+)', text)
        if color_m:
            try:
                params['color'] = int(color_m.group(1), 16) if color_m.group(1).startswith(('0x', '')) and len(color_m.group(1)) > 2 else int(color_m.group(1))
            except ValueError:
                pass

        return params

    # ============================================================
    # 主入口
    # ============================================================

    @staticmethod
    def extract(text: str, intent: str) -> Dict[str, Any]:
        """
        从自然语言中提取参数

        Args:
            text: 用户输入的自然语言文本
            intent: 已分类的意图标识

        Returns:
            结构化参数字典
        """
        extractors = {
            "arch_floor_plan": ParamExtractor._extract_arch_params,
            "mech_bolt": ParamExtractor._extract_mech_params,
            "mech_gear": ParamExtractor._extract_mech_params,
            "mech_bearing": ParamExtractor._extract_mech_params,
            "mech_spring": ParamExtractor._extract_mech_params,
            "elec_switch": ParamExtractor._extract_elec_params,
            "elec_socket": ParamExtractor._extract_elec_params,
            "elec_lamp": ParamExtractor._extract_elec_params,
            "elec_wires": ParamExtractor._extract_elec_params,
            "pipe_straight": ParamExtractor._extract_pipe_params,
            "pipe_elbow": ParamExtractor._extract_pipe_params,
            "pipe_valve": ParamExtractor._extract_pipe_params,
            "pipe_tee": ParamExtractor._extract_pipe_params,
            "struct_beam": ParamExtractor._extract_struct_params,
            "struct_slab": ParamExtractor._extract_struct_params,
            "struct_footing": ParamExtractor._extract_struct_params,
            "geo_rectangle": ParamExtractor._extract_geo_params,
            "geo_circle": ParamExtractor._extract_geo_params,
            "geo_polygon": ParamExtractor._extract_geo_params,
        }

        extractor = extractors.get(intent, ParamExtractor._extract_geo_params)

        try:
            result = extractor(text)
        except Exception as e:
            print(f"[ParamExtractor] 警告: 参数提取异常 ({intent}): {e}")
            result = {}

        # 存储原始文本供调试
        result['_raw_text'] = text
        result['_intent'] = intent

        return result

    # ============================================================
    # 调试工具
    # ============================================================

    @staticmethod
    def debug_extract(text: str, intent: str = None) -> str:
        """调试模式：输出详细的参数提取过程"""
        # 延迟导入避免循环依赖
        if intent is None:
            from .intent_classifier import IntentClassifier
            intent = IntentClassifier.classify(text)

        params = ParamExtractor.extract(text, intent)

        report = [
            f"=== NL 参数提取报告 ===",
            f"原始文本: {text}",
            f"意图分类: {intent}",
            f"---",
            f"提取参数:",
        ]
        for k, v in params.items():
            if k.startswith('_'):
                continue
            report.append(f"  {k}: {v} ({type(v).__name__})")

        return '\n'.join(report)
