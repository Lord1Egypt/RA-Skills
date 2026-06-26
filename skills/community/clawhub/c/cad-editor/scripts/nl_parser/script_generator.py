"""
NL → 可执行脚本链生成器
核心价值：将自然语言意图 + 提取的参数，翻译成精确的 Python 绘图脚本
"""
from typing import Dict, List, Any, Optional, Tuple
import re
import json
import os


class ScriptGenerator:
    """
    自然语言 → Python 脚本生成器

    工作流程：
    1. 接收 intent (意图) + params (参数)
    2. 匹配对应的脚本模板
    3. 将参数填充到模板中
    4. 输出可执行的 Python 脚本字符串
    """

    # ============================================================
    # 脚本模板库 — 每种意图对应一段完整的绘图代码模板
    # ============================================================

    TEMPLATES = {
        # ---------- 建筑平面图 ----------
        "arch_floor_plan": '''
def draw_arch_floor_plan(doc, **kwargs):
    """建筑平面图"""
    from scripts.layer.manager import LayerManager
    from scripts.layer.linetypes import Linetypes
    from scripts.templates.architectural import ArchitecturalTemplates
    from scripts.dimension.linear import LinearDimension
    from scripts.layout.paperspace import PaperSpace

    msp = doc.modelspace()
    Linetypes.load_standard(doc)
    LayerManager(doc).setup_template('arch')

    # 外墙
    width = {width}
    depth = {depth}
    wall_thickness = {wall_thickness}
    wall_pts = [(0, 0), (width, 0), (width, depth), (0, depth)]
    ArchitecturalTemplates.wall(msp, wall_pts, thickness=wall_thickness)

    {doors_indented}

    {windows_indented}

    {columns_indented}

    # 尺寸标注 — 外部三道
    offset_base = {offset} if '{offset}' else 600
    LinearDimension.chain_horizontal(
        msp,
        [(0, -offset_base), (0, 0), (width, 0), (width, -offset_base)],
        offset=offset_base + 400
    )
    LinearDimension.chain_vertical(
        msp,
        [(-offset_base, 0), (0, 0), (0, depth), (-offset_base, depth)],
        offset=offset_base + 400
    )

    # 图框
    PaperSpace.draw_title_block(msp, (0, 0), size='{paper_size}', title='{title}')

    return doc
''',

        # ---------- 机械零件 ----------
        "mech_bolt": '''
def draw_mech_bolt(doc, **kwargs):
    """螺栓俯视图"""
    from scripts.entities.curves import Curves
    from scripts.entities.basic import BasicEntity
    from scripts.templates.mechanical import MechanicalTemplates

    msp = doc.modelspace()

    size = {size}
    cx, cy = ({center_x}, {center_y})

    MechanicalTemplates.bolt_head_top(msp, center=(cx, cy), size=size, type_='{bolt_type}')

    return doc
''',

        "mech_gear": '''
def draw_mech_gear(doc, **kwargs):
    """齿轮端面视图"""
    from scripts.templates.mechanical import MechanicalTemplates

    msp = doc.modelspace()

    teeth_count = {teeth}
    pitch_diameter = {pitch_diameter}
    bore_diameter = {bore_diameter}
    cx, cy = ({center_x}, {center_y})

    MechanicalTemplates.gear_face(
        msp, center=(cx, cy),
        teeth=teeth_count,
        pitch_diameter=pitch_diameter,
        bore=bore_diameter
    )

    return doc
''',

        "mech_bearing": '''
def draw_mech_bearing(doc, **kwargs):
    """轴承剖面/端面"""
    from scripts.templates.mechanical import MechanicalTemplates

    msp = doc.modelspace()

    bearing_type = "{bearing_model}"
    inner_d = {inner_diameter}
    outer_d = {outer_diameter}
    width = {bearing_width}
    cx, cy = ({center_x}, {center_y})

    MechanicalTemplates.bearing(
        msp, center=(cx, cy),
        model=bearing_type,
        inner_d=inner_d,
        outer_d=outer_d,
        width=width
    )

    return doc
''',

        "mech_spring": '''
def draw_mech_spring(doc, **kwargs):
    """压缩弹簧侧视图"""
    from scripts.templates.mechanical import MechanicalTemplates

    msp = doc.modelspace()

    wire_dia = {wire_diameter}
    outer_d = {spring_outer_diameter}
    active_coils = {active_coils}
    start_pt = ({start_x}, {start_y})

    MechanicalTemplates.compression_spring(
        msp, start=start_pt,
        wire_diameter=wire_dia,
        outer_diameter=outer_d,
        coils=active_coils
    )

    return doc
''',

        # ---------- 电气符号 ----------
        "elec_switch": '''
def draw_elec_switch(doc, **kwargs):
    """开关符号"""
    from scripts.templates.electrical import ElectricalTemplates

    msp = doc.modelspace()

    x, y = ({pos_x}, {pos_y})
    orientation = "{orientation}"
    poles = {poles}

    ElectricalTemplates.switch(
        msp, position=(x, y),
        orientation=orientation,
        poles=poles
    )

    return doc
''',

        "elec_socket": '''
def draw_elec_socket(doc, **kwargs):
    """插座符号"""
    from scripts.templates.electrical import ElectricalTemplates

    msp = doc.modelspace()

    x, y = ({pos_x}, {pos_y})
    socket_type = "{socket_type}"

    ElectricalTemplates.socket(
        msp, position=(x, y),
        type_=socket_type
    )

    return doc
''',

        "elec_lamp": '''
def draw_elec_lamp(doc, **kwargs):
    """灯具符号"""
    from scripts.templates.electrical import ElectricalTemplates

    msp = doc.modelspace()

    x, y = ({pos_x}, {pos_y})
    lamp_type = "{lamp_type}"

    ElectricalTemplates.lamp(
        msp, position=(x, y),
        type_=lamp_type
    )

    return doc
''',

        "elec_wires": '''
def draw_elec_wires(doc, **kwargs):
    """导线组"""
    from scripts.templates.electrical import ElectricalTemplates

    msp = doc.modelspace()

    start = ({start_x}, {start_y})
    end = ({end_x}, {end_y})
    phases = {phases}
    spacing = {spacing}

    ElectricalTemplates.wire_group(
        msp, start=start, end=end,
        phases=phases, spacing=spacing
    )

    return doc
''',

        # ---------- 管道 ----------
        "pipe_straight": '''
def draw_pipe_straight(doc, **kwargs):
    """直管段"""
    from scripts.templates.piping import PipingTemplates

    msp = doc.modelspace()

    dn = {dn}
    length = {length}
    start = ({start_x}, {start_y})
    direction = "{direction}"

    PipingTemplates.straight_pipe(
        msp, start=start, dn=dn,
        length=length, direction=direction
    )

    return doc
''',

        "pipe_elbow": '''
def draw_pipe_elbow(doc, **kwargs):
    """弯头"""
    from scripts.templates.piping import PipingTemplates

    msp = doc.modelspace()

    dn = {dn}
    radius = {radius}
    center = ({center_x}, {center_y})
    turn_direction = "{turn_direction}"

    PipingTemplates.elbow(
        msp, center=center, dn=dn,
        radius=radius, direction=turn_direction
    )

    return doc
''',

        "pipe_valve": '''
def draw_pipe_valve(doc, **kwargs):
    """阀门"""
    from scripts.templates.piping import PipingTemplates

    msp = doc.modelspace()

    valve_type = "{valve_type}"
    dn = {dn}
    position = ({pos_x}, {pos_y})
    direction = "{direction}"

    PipingTemplates.valve(
        msp, position=position,
        type_=valve_type, dn=dn, direction=direction
    )

    return doc
''',

        "pipe_tee": '''
def draw_pipe_tee(doc, **kwargs):
    """三通/四通"""
    from scripts.templates.piping import PipingTemplates

    msp = doc.modelspace()

    main_dn = {main_dn}
    branch_dn = {branch_dn}
    position = ({pos_x}, {pos_y})
    tee_type = "{tee_type}"

    PipingTemplates.tee(
        msp, position=position,
        main_dn=main_dn, branch_dn=branch_dn,
        type_=tee_type
    )

    return doc
''',

        # ---------- 结构详图 ----------
        "struct_beam": '''
def draw_struct_beam(doc, **kwargs):
    """梁断面配筋图"""
    from scripts.templates.structural import StructuralTemplates
    from scripts.hatch.patterns import HatchPatterns

    msp = doc.modelspace()

    b = {beam_width}
    h = {beam_height}
    bottom_rebar = {bottom_rebar}      # 底部钢筋数量+直径，如 "3根16"
    top_rebar = "{top_rebar}"          # 顶部钢筋
    stirrup = "{stirrup}"              # 箍筋规格，如 "8@200"
    concrete_grade = "{concrete_grade}"

    StructuralTemplates.beam_section(
        msp, width=b, height=h,
        bottom_rebar=bottom_rebar,
        top_rebar=top_rebar or None,
        stirrup=stirrup or None,
        concrete_grade=concrete_grade or 'C30'
    )

    return doc
''',

        "struct_slab": '''
def draw_struct_slab(doc, **kwargs):
    """楼板配筋图"""
    from scripts.templates.structural import StructuralTemplates

    msp = doc.modelspace()

    slab_thickness = {slab_thickness}
    bottom_x = "{bottom_x_rebar}"       # 底部X向钢筋，如 "12@150"
    bottom_y = "{bottom_y_rebar}"       # 底部Y向钢筋
    support_x = "{support_x_rebar}"     # 支座负筋X向
    support_y = "{support_y_rebar}"     # 支座负筋Y向

    StructuralTemplates.slab_reinforcement(
        msp, thickness=slab_thickness,
        bottom_x=bottom_x, bottom_y=bottom_y,
        support_x=support_x or None, support_y=support_y or None
    )

    return doc
''',

        "struct_footing": '''
def draw_struct_footing(doc, **kwargs):
    """独立基础详图"""
    from scripts.templates.structural import StructuralTemplates

    msp = doc.modelspace()

    col_size = ({col_width}, {col_height})
    base_size = ({base_width}, {base_depth})
    base_depth = {foundation_depth}
    bottom_rebar = "{footing_rebar}"

    StructuralTemplates.isolated_footing(
        msp, column_size=col_size,
        base_size=base_size,
        depth=base_depth,
        reinforcement=bottom_rebar
    )

    return doc
''',

        # ---------- 几何图形 ----------
        "geo_rectangle": '''
def draw_geo_rectangle(doc, **kwargs):
    """矩形"""
    from scripts.entities.polyline import PolylineEntity

    msp = doc.modelspace()
    w, h = {rect_width}, {rect_height}
    c = ({center_x}, {center_y}) if {has_center} else ({corner_x}, {corner_y})

    PolylineEntity.rect_centered(msp, c, w, h, layer='{layer}', color={color})
    return doc
''',

        "geo_circle": '''
def draw_geo_circle(doc, **kwargs):
    """圆"""
    from scripts.entities.curves import Curves

    msp = doc.modelspace()
    cx, cy = {center_x}, {center_y}
    r = {radius}

    Curves.circle(msp, (cx, cy), radius=r, layer='{layer}', color={color})
    return doc
''',

        "geo_polygon": '''
def draw_geo_polygon(doc, **kwargs):
    """正多边形"""
    from scripts.entities.polyline import PolylineEntity

    msp = doc.modelspace()
    sides = {sides}
    circumradius = {circumradius}
    cx, cy = {center_x}, {center_y}

    PolylineEntity.regular_polygon(msp, (cx, cy), sides=sides, circumradius=circumradius)
    return doc
''',
    }

    # ============================================================
    # 门/窗子代码生成辅助
    # ============================================================

    @staticmethod
    def _gen_door_code(doors: List[Dict]) -> str:
        """Generate door drawing code (unindented - caller handles indentation)"""
        if not doors:
            return "# No doors"
        lines = []
        for i, d in enumerate(doors):
            pos = d.get('position', (1000 * (i + 1), 0))
            width = d.get('width', 900)
            door_type = d.get('type', 'single')
            lines.append(
                f"ArchitecturalTemplates.door_{door_type}(msp, {pos}, width={width})"
            )
        return '\n'.join(lines)

    @staticmethod
    def _gen_window_code(windows: List[Dict]) -> str:
        """Generate window drawing code (unindented)"""
        if not windows:
            return "# No windows"
        lines = []
        for i, w in enumerate(windows):
            p1 = w.get('start', (800 + i * 1200, 240))
            p2 = w.get('end', (2000 + i * 1200, 240))
            lines.append(
                f"ArchitecturalTemplates.window(msp, {p1}, {p2})"
            )
        return '\n'.join(lines)

    @staticmethod
    def _gen_column_code(columns: List[Dict]) -> str:
        """Generate column drawing code (unindented)"""
        if not columns:
            return "# No columns"
        lines = []
        for i, c in enumerate(columns):
            pos = c.get('position', (i * 5000, i * 3500))
            size = c.get('size', (400, 400))
            lines.append(
                f"ArchitecturalTemplates.column(msp, {pos}, size={size})"
            )
        return '\n'.join(lines)

    # ============================================================
    # 主入口：生成完整脚本
    # ============================================================

    @classmethod
    def generate(cls, intent: str, params: Dict[str, Any],
                output_path: str = "output",
                filename: str = "drawing") -> str:
        """
        生成完整的可执行 Python 脚本

        Args:
            intent: 意图分类标识（如 "arch_floor_plan"）
            params: 提取的参数字典
            output_path: DXF/PNG 输出目录
            filename: 文件名（不含扩展名）

        Returns:
            完整的 Python 脚本字符串
        """
        template = cls.TEMPLATES.get(intent)
        if not template:
            raise ValueError(f"未知意图类型: '{intent}'，支持的类型: {list(cls.TEMPLATES.keys())}")

        # 预处理参数 —— 带默认值的安全提取
        safe_params = cls._safe_params(params, intent)

        # 对特殊意图，先生成子组件代码
        if intent == "arch_floor_plan":
            raw_doors = cls._gen_door_code(safe_params.get("doors", []))
            raw_windows = cls._gen_window_code(safe_params.get("windows", []))
            raw_columns = cls._gen_column_code(safe_params.get("columns", []))
            # Add 4-space indent for template embedding
            safe_params["doors_indented"] = '\n'.join(
                '    ' + line for line in raw_doors.split('\n')
            ) if raw_doors else "# No doors"
            safe_params["windows_indented"] = '\n'.join(
                '    ' + line for line in raw_windows.split('\n')
            ) if raw_windows else "# No windows"
            safe_params["columns_indented"] = '\n'.join(
                '    ' + line for line in raw_columns.split('\n')
            ) if raw_columns else "# No columns"

        # 填充模板
        script_body = template.format(**safe_params)

        # 组装完整脚本
        full_script = f'''# Auto-generated by cad-editor NL Parser
# Intent: {intent}
# Parameters: {json.dumps(params, ensure_ascii=False, default=str)}

import sys
import os

# 确保 cad-editor/scripts 在路径中
script_dir = os.path.dirname(os.path.abspath(__file__))
cad_editor_root = os.path.dirname(script_dir)
if cad_editor_root not in sys.path:
    sys.path.insert(0, os.path.dirname(cad_editor_root))

from scripts.core.document import CADDocument
from scripts.core.renderer import Renderer


{script_body}


if __name__ == "__main__":
    # 创建文档
    doc = CADDocument.new(version="R2010")

    # 执行绘图
    result_doc = draw_{intent}(doc)

    # 确保输出目录存在
    output_dir = r"{output_path}"
    os.makedirs(output_dir, exist_ok=True)

    # 保存 DXF
    dxf_path = os.path.join(output_dir, "{filename}.dxf")
    CADDocument.save(result_doc, dxf_path)
    print(f"DXF saved: {{dxf_path}}")

    # 渲染 PNG
    png_path = Renderer.render_quick(
        result_doc,
        output_dir=output_dir,
        name="{filename}",
        dpi=150
    )
    print(f"PNG rendered: {{png_path}}")
'''
        return full_script

    # ============================================================
    # 参数安全处理
    # ============================================================

    @staticmethod
    def _safe_params(raw: Dict, intent: str) -> Dict[str, Any]:
        """
        从原始参数中安全提取值，缺失的使用合理默认值
        返回一个所有模板占位符都有值的字典
        """
        get = lambda key, default="": raw.get(key, default)

        # 通用默认值
        safe = {
            "width": get("width", 4000),
            "depth": get("depth", 3000),
            "wall_thickness": get("wall_thickness", 240),
            "offset": get("offset", 600),
            "paper_size": get("paper_size", "A3"),
            "title": get("title", "工程图纸"),
            "center_x": get("center_x", 0),
            "center_y": get("center_y", 0),
            "color": get("color", 7),
            "layer": get("layer", "0"),
            "size": get("size", 16),
            "radius": get("radius", 50),
            "dn": get("dn", 50),
            "length": get("length", 1000),
            "direction": get("direction", "H"),
        }

        # 按意图补充特定参数
        intent_defaults = {
            "arch_floor_plan": {
                "doors": get("doors", []),
                "windows": get("windows", []),
                "columns": get("columns", []),
            },
            "mech_bolt": {
                "bolt_type": get("bolt_type", "hex"),
            },
            "mech_gear": {
                "teeth": get("teeth", 20),
                "pitch_diameter": get("pitch_diameter", 100),
                "bore_diameter": get("bore_diameter", 20),
            },
            "mech_bearing": {
                "bearing_model": get("bearing_model", "6205"),
                "inner_diameter": get("inner_diameter", 25),
                "outer_diameter": get("outer_diameter", 52),
                "bearing_width": get("bearing_width", 15),
            },
            "mech_spring": {
                "wire_diameter": get("wire_diameter", 2),
                "spring_outer_diameter": get("spring_outer_diameter", 16),
                "active_coils": get("active_coils", 6),
                "start_x": get("start_x", 0),
                "start_y": get("start_y", 0),
            },
            "elec_switch": {
                "pos_x": get("pos_x", 0),
                "pos_y": get("pos_y", 0),
                "orientation": get("orientation", "V"),
                "poles": get("poles", 1),
            },
            "elec_socket": {
                "pos_x": get("pos_x", 0),
                "pos_y": get("pos_y", 0),
                "socket_type": get("socket_type", "3pin"),
            },
            "elec_lamp": {
                "pos_x": get("pos_x", 0),
                "pos_y": get("pos_y", 0),
                "lamp_type": get("lamp_type", "ceiling"),
            },
            "elec_wires": {
                "start_x": get("start_x", 0),
                "start_y": get("start_y", 0),
                "end_x": get("end_x", 3000),
                "end_y": get("end_y", 0),
                "phases": get("phases", 3),
                "spacing": get("spacing", 30),
            },
            "pipe_straight": {
                "start_x": get("start_x", 0),
                "start_y": get("start_y", 0),
            },
            "pipe_elbow": {
                "radius": get("radius", 100),
                "turn_direction": get("turn_direction", "NE"),
            },
            "pipe_valve": {
                "valve_type": get("valve_type", "gate"),
                "pos_x": get("pos_x", 0),
                "pos_y": get("pos_y", 0),
            },
            "pipe_tee": {
                "main_dn": get("main_dn", 50),
                "branch_dn": get("branch_dn", 30),
                "pos_x": get("pos_x", 0),
                "pos_y": get("pos_y", 0),
                "tee_type": get("tee_type", "equal"),
            },
            "struct_beam": {
                "beam_width": get("beam_width", 250),
                "beam_height": get("beam_height", 500),
                "bottom_rebar": get("bottom_rebar", "3根16"),
                "top_rebar": get("top_rebar", ""),
                "stirrup": get("stirrup", "8@200"),
                "concrete_grade": get("concrete_grade", "C30"),
            },
            "struct_slab": {
                "slab_thickness": get("slab_thickness", 120),
                "bottom_x_rebar": get("bottom_x_rebar", "12@150"),
                "bottom_y_rebar": get("bottom_y_rebar", "10@200"),
                "support_x_rebar": get("support_x_rebar", ""),
                "support_y_rebar": get("support_y_rebar", ""),
            },
            "struct_footing": {
                "col_width": get("col_width", 500),
                "col_height": get("col_height", 500),
                "base_width": get("base_width", 2000),
                "base_depth": get("base_depth", 2000),
                "foundation_depth": get("foundation_depth", 600),
                "footing_rebar": get("footing_rebar", "14@150"),
            },
            "geo_rectangle": {
                "rect_width": get("rect_width", 400),
                "rect_height": get("rect_height", 300),
                "has_center": True,
                "corner_x": 0,
                "corner_y": 0,
            },
            "geo_circle": {},
            "geo_polygon": {
                "sides": get("sides", 6),
                "circumradius": get("circumradius", 100),
            },
        }

        specific = intent_defaults.get(intent, {})
        safe.update(specific)
        safe.update(raw)  # raw 参数覆盖默认值

        return safe

    # ============================================================
    # 快捷方法：一步到位（NL文本 → 脚本）
    # ============================================================

    @classmethod
    def from_natural_language(cls, text: str, output_path: str = "output",
                              filename: str = "drawing") -> Tuple[str, str]:
        """一站式：自然语言文本 → (脚本内容, 意图类型)"""
        # 延迟导入避免循环依赖
        from .intent_classifier import IntentClassifier
        from .param_extractor import ParamExtractor

        intent = IntentClassifier.classify(text)
        params = ParamExtractor.extract(text, intent)
        script = cls.generate(intent, params, output_path, filename)
        return script, intent

    # ============================================================
    # 批量生成
    # ============================================================

    @classmethod
    def generate_batch(cls, items: List[Dict[str, Any]],
                       output_path: str = "output") -> List[str]:
        """
        批量生成多个图纸的脚本

        Args:
            items: [{"text": "用户指令", "filename": "文件名"}, ...]
            output_path: 输出目录

        Returns:
            生成的脚本列表
        """
        scripts = []
        for item in items:
            text = item.get("text", "")
            fname = item.get("filename", f"drawing_{len(scripts)}")
            script, _ = cls.from_natural_language(text, output_path, fname)
            scripts.append(script)
        return scripts
