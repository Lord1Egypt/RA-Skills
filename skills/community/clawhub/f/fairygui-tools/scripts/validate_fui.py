#!/usr/bin/env python3
"""
FairyGUI XML 合法性校验脚本
=============================
基于 FairyGUI 官方文档和 176 个示例工程 XML 提取的完整规则。
用于校验生成的 FairyGUI 工程文件是否能被编辑器正确解析。

用法:
    python validate_fui.py <目录路径>
    python validate_fui.py <单个XML文件>

返回码:
    0 = 全部通过
    1 = 存在错误
"""

import sys
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional


class ValidationError:
    """校验错误"""
    def __init__(self, file: str, line: int, level: str, msg: str):
        self.file = file
        self.line = line  # -1 表示未知行号
        self.level = level  # "ERROR" 或 "WARN"
        self.msg = msg

    def __str__(self):
        loc = f"{self.file}"
        if self.line > 0:
            loc += f":{self.line}"
        return f"[{self.level}] {loc} - {self.msg}"


class FUIValidator:
    """FairyGUI XML 校验器"""

    # ---- 合法标签/属性定义 ----

    # package.xml 资源类型
    RESOURCE_TYPES = {"image", "component", "movieclip", "font", "sound", "swf", "atlas", "misc"}

    # 资源通用属性
    RESOURCE_COMMON_ATTRS = {"id", "name", "path", "exported"}

    # 各资源类型专属属性
    RESOURCE_EXTRA_ATTRS = {
        "image": {"scale", "scale9grid", "duplicatePadding", "texture", "smoothing", "quality"},
        "component": set(),
        "movieclip": set(),
        "font": {"texture", "ttf", "fntFile"},
        "sound": set(),
        "swf": set(),
        "atlas": {"name", "index"},
        "misc": set(),
    }

    # image scale 合法值
    IMAGE_SCALE_VALUES = {"9grid", "tile", ""}

    # displayList 合法子标签
    DISPLAY_LIST_TAGS = {
        "image", "graph", "text", "richtext", "inputtext",
        "loader", "loader3d", "component", "movieclip", "jta",
        "list", "group",
    }

    # 通用元件属性
    COMMON_ELEMENT_ATTRS = {
        "id", "name", "xy", "size", "pivot", "anchor", "scale", "skew",
        "rotation", "alpha", "visible", "touchable", "grayed", "group",
        "tooltips", "customData", "blend", "filter",
    }

    # 各元件类型专属属性
    ELEMENT_EXTRA_ATTRS = {
        "image": {
            "src", "fileName", "aspect", "color", "flip",
            "fillMethod", "fillClockwise", "fillOrigin", "fillAmount",
            "locked", "forHitTest",
        },
        "graph": {
            "type", "lineSize", "lineColor", "fillColor", "corner",
            "points", "sides", "startAngle", "distances", "locked",
        },
        "text": {
            "fontSize", "font", "color", "align", "vAlign",
            "leading", "letterSpacing", "autoSize", "singleLine",
            "bold", "italic", "underline", "strikethrough",
            "strokeColor", "strokeSize", "shadowColor", "shadowOffset",
            "ubbEnabled", "ubb", "text", "input", "password", "maxLength",
            "restrict", "promptText", "prompt", "keyboardType", "var",
            "templateVars", "demoText",
        },
        "richtext": {
            "fontSize", "font", "color", "align", "vAlign",
            "leading", "letterSpacing", "autoSize", "singleLine",
            "bold", "italic", "underline", "strikethrough",
            "strokeColor", "strokeSize", "shadowColor", "shadowOffset",
            "ubbEnabled", "ubb", "text", "restrictSize",
        },
        "inputtext": {
            "fontSize", "font", "color", "align", "vAlign",
            "leading", "letterSpacing", "autoSize", "singleLine",
            "bold", "italic", "underline", "strikethrough",
            "strokeColor", "strokeSize", "shadowColor", "shadowOffset",
            "ubbEnabled", "text", "password", "maxLength",
            "restrict", "promptText", "keyboardType",
        },
        "loader": {
            "url", "fill", "align", "vAlign", "shrinkOnly", "autoSize",
            "color", "playing", "frame", "src", "fileName",
            "fillMethod", "fillClockwise", "fillOrigin", "fillAmount",
            "errorSign",
        },
        "loader3d": {
            "url", "fill", "align", "vAlign", "shrinkOnly", "autoSize",
            "color", "playing", "frame", "src", "fileName",
        },
        "component": {
            "src", "fileName", "extention", "aspect",
        },
        "movieclip": {
            "src", "fileName", "playing", "frame", "color",
        },
        "jta": {
            "src", "fileName", "playing", "frame", "color",
        },
        "list": {
            "layout", "overflow", "scroll", "scrollBar", "scrollBarFlags",
            "margin", "clipSoftness", "lineGap", "colGap",
            "defaultItem", "selectionMode", "autoResizeItem",
            "foldInvisibleItems", "lineCount", "columnCount",
            "scrollBarMargin", "selectionController", "pageController",
            "pageMode", "snapToItem", "inertiaDisabled",
            "bouncebackEffect", "scrollBarDisplay", "maskDisabled",
            "clipSoftness", "headerRes", "footerRes",
            "align", "scrollBarRes", "autoItemSize", "ptrRes",
            "treeView", "indent", "clickToExpand",
        },
        "group": {
            "advanced", "layout", "lineGap", "colGap", "excludeInvisibles",
            "autoSizeDisabled", "mainGridIndex", "mainGridMinSize",
        },
    }

    # gear 子元素
    GEAR_TAGS = {
        "gearDisplay", "gearDisplay2", "gearXY", "gearSize",
        "gearColor", "gearLook", "gearAni", "gearText",
        "gearIcon", "gearFontSize",
    }

    # gear 通用属性
    GEAR_ATTRS = {"controller", "pages", "values", "default", "tween", "easeType", "ease", "duration", "delay", "condition"}

    # 扩展元素
    EXTENSION_TAGS = {"Button", "Label", "ProgressBar", "Slider", "ScrollBar", "ComboBox"}

    # 扩展元素属性
    EXTENSION_ATTRS = {
        "Button": {
            "title", "icon", "selectedTitle", "selectedIcon",
            "checked", "controller", "page", "mode",
            "sound", "soundVolumeScale", "downEffect", "downEffectValue",
            "titleColor", "titleFontSize",
        },
        "Label": {
            "title", "icon", "titleColor", "titleFontSize",
        },
        "ProgressBar": {
            "value", "max", "titleType", "reverse",
        },
        "Slider": {
            "value", "max", "titleType", "wholeNumbers", "reverse",
        },
        "ScrollBar": {
            "fixedGripSize",
        },
        "ComboBox": {
            "titleColor", "visibleItemCount", "dropdown",
            "selectionController",
        },
    }

    # component 根属性
    COMPONENT_ROOT_ATTRS = {
        "size", "extention", "overflow", "scroll", "scrollBar",
        "scrollBarFlags", "mask", "reversedMask", "hitTest", "opaque",
        "bgColor", "bgColorEnabled", "initName", "idnum",
        "pivot", "anchor", "designImageLayer", "designImageAlpha",
        "margin", "clipSoftness", "scrollBarMargin",
        "pageMode", "snapToItem", "inertiaDisabled",
        "bouncebackEffect", "scrollBarDisplay", "maskDisabled",
        "restrictSceneScroll", "customData", "remark",
    }

    # transition item type
    TRANSITION_TYPES = {
        "XY", "Size", "Scale", "Pivot", "Alpha", "Rotation",
        "Color", "ColorFilter", "Visible", "Sound", "Transition",
        "Shake", "Animation", "Text", "Icon", "FontSize", "Skew",
    }

    # transition item 属性
    TRANSITION_ITEM_ATTRS = {
        "time", "type", "target", "tween", "startValue", "endValue",
        "value", "duration", "ease", "repeat", "yoyo", "label", "label2",
        "path", "value2",
    }

    # graph type 合法值
    GRAPH_TYPES = {"rect", "eclipse", "polygon", "regular_polygon"}

    # list layout 合法值
    LIST_LAYOUTS = {"column", "row", "flow_hz", "flow_vt", "pagination"}

    # overflow 合法值
    OVERFLOW_VALUES = {"visible", "hidden", "scroll"}

    # autoSize 合法值
    AUTO_SIZE_VALUES = {"none", "both", "height", "shrink"}

    # align 合法值
    ALIGN_VALUES = {"left", "center", "right"}

    # vAlign 合法值
    VALIGN_VALUES = {"top", "middle", "bottom"}

    # fill 合法值
    FILL_VALUES = {"none", "scale", "scaleMatchHeight", "scaleMatchWidth", "scaleFree", "scaleNoBorder"}

    # sidePair 合法前缀（不含 % 后缀）
    # 支持完整形式 "left-left" 和简写形式 "width", "height"
    SIDE_PAIR_VALUES = {
        "left-left", "left-center", "left-right",
        "center-center",
        "right-left", "right-center", "right-right",
        "leftext-left", "leftext-right",
        "rightext-left", "rightext-right",
        "width-width", "width",
        "top-top", "top-middle", "top-bottom",
        "middle-middle",
        "bottom-top", "bottom-middle", "bottom-bottom",
        "topext-top", "topext-bottom",
        "bottomext-top", "bottomext-bottom",
        "height-height", "height",
    }

    # 缓动函数
    EASE_FUNCTIONS = {
        "Linear",
        "Quad.In", "Quad.Out", "Quad.InOut",
        "Cubic.In", "Cubic.Out", "Cubic.InOut",
        "Quart.In", "Quart.Out", "Quart.InOut",
        "Quint.In", "Quint.Out", "Quint.InOut",
        "Sine.In", "Sine.Out", "Sine.InOut",
        "Bounce.In", "Bounce.Out", "Bounce.InOut",
        "Circ.In", "Circ.Out", "Circ.InOut",
        "Expo.In", "Expo.Out", "Expo.InOut",
        "Elastic.In", "Elastic.Out", "Elastic.InOut",
        "Back.In", "Back.Out", "Back.InOut",
        "Custom",
    }

    # extention 合法值
    EXTENTION_VALUES = {"Button", "Label", "ProgressBar", "Slider", "ScrollBar", "ComboBox"}

    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
        self.resource_ids: Dict[str, Set[str]] = {}  # file -> set of ids

    def _err(self, file: str, msg: str, line: int = -1):
        self.errors.append(ValidationError(file, line, "ERROR", msg))

    def _warn(self, file: str, msg: str, line: int = -1):
        self.warnings.append(ValidationError(file, line, "WARN", msg))

    # ========== 颜色校验 ==========

    def _check_color(self, file: str, attr_name: str, value: str):
        """校验颜色格式: #AARRGGBB 或 #RRGGBB"""
        if not value:
            return
        if not re.match(r'^#[0-9a-fA-F]{6}$|^#[0-9a-fA-F]{8}$', value):
            self._err(file, f"颜色格式非法 {attr_name}=\"{value}\"，应为 #RRGGBB 或 #AARRGGBB")

    # ========== 坐标校验 ==========

    def _check_xy(self, file: str, attr_name: str, value: str):
        """校验 x,y 格式"""
        if not value:
            return
        parts = value.split(",")
        if len(parts) != 2:
            self._err(file, f"{attr_name}=\"{value}\" 格式错误，应为 \"x,y\"")
            return
        for p in parts:
            p = p.strip()
            if p == "-":  # transition 中 "-" 表示不修改
                continue
            try:
                float(p)
            except ValueError:
                self._err(file, f"{attr_name}=\"{value}\" 包含非数值: \"{p}\"")

    def _check_size(self, file: str, attr_name: str, value: str):
        """校验 w,h 格式"""
        self._check_xy(file, attr_name, value)

    # ========== package.xml 校验 ==========

    def validate_package_xml(self, file: str, root: ET.Element):
        """校验 package.xml"""
        if root.tag != "packageDescription":
            self._err(file, f"根元素应为 <packageDescription>，实际为 <{root.tag}>")
            return

        if "id" not in root.attrib:
            self._err(file, "packageDescription 缺少必需属性 'id'")

        # 合法子元素
        valid_children = {"resources", "publish"}
        for child in root:
            if child.tag not in valid_children:
                self._warn(file, f"packageDescription 下出现未知元素 <{child.tag}>")

        # 校验 resources
        resources = root.find("resources")
        if resources is None:
            self._err(file, "缺少 <resources> 元素")
            return

        resource_ids = set()
        for res in resources:
            if res.tag not in self.RESOURCE_TYPES:
                self._err(file, f"resources 下出现非法资源类型 <{res.tag}>")
                continue

            # 必需属性
            res_id = res.get("id")
            if not res_id:
                self._err(file, f"<{res.tag}> 缺少必需属性 'id'")
            else:
                if res_id in resource_ids:
                    self._err(file, f"资源 ID 重复: \"{res_id}\"")
                resource_ids.add(res_id)

            if res.tag != "atlas":  # atlas 在 publish 下，格式不同
                if not res.get("name"):
                    self._err(file, f"<{res.tag} id=\"{res_id}\"> 缺少必需属性 'name'")
                if not res.get("path"):
                    self._err(file, f"<{res.tag} id=\"{res_id}\"> 缺少必需属性 'path'")

            # 属性合法性
            allowed = self.RESOURCE_COMMON_ATTRS | self.RESOURCE_EXTRA_ATTRS.get(res.tag, set())
            for attr in res.attrib:
                if attr not in allowed:
                    self._warn(file, f"<{res.tag} id=\"{res_id}\"> 出现未知属性 '{attr}'")

            # image scale 值
            if res.tag == "image" and "scale" in res.attrib:
                sv = res.get("scale")
                if sv not in self.IMAGE_SCALE_VALUES:
                    self._err(file, f"image scale 值非法: \"{sv}\"，应为 9grid/tile/空")
                if sv == "9grid" and "scale9grid" not in res.attrib:
                    self._err(file, f"image scale=\"9grid\" 但缺少 scale9grid 属性")

        self.resource_ids[file] = resource_ids

        # 校验 publish
        publish = root.find("publish")
        if publish is not None:
            if not publish.get("name"):
                self._warn(file, "<publish> 缺少 'name' 属性")

    # ========== 组件 XML 校验 ==========

    def validate_component_xml(self, file: str, root: ET.Element):
        """校验组件 XML"""
        if root.tag != "component":
            self._err(file, f"根元素应为 <component>，实际为 <{root.tag}>")
            return

        # 根属性校验
        for attr in root.attrib:
            if attr not in self.COMPONENT_ROOT_ATTRS:
                self._warn(file, f"<component> 出现未知属性 '{attr}'")

        if "size" not in root.attrib:
            self._err(file, "<component> 缺少必需属性 'size'")
        else:
            self._check_size(file, "component.size", root.get("size"))

        if "extention" in root.attrib:
            ext = root.get("extention")
            if ext not in self.EXTENTION_VALUES:
                self._err(file, f"extention 值非法: \"{ext}\"")

        # 检查节点顺序
        found_display = False
        found_controller_after_display = False
        found_transition_before_display = False
        element_names = set()

        for child in root:
            if child.tag == "controller":
                if found_display:
                    found_controller_after_display = True
                self._validate_controller(file, child)
            elif child.tag == "displayList":
                found_display = True
                self._validate_display_list(file, child, element_names)
            elif child.tag == "transition":
                if not found_display:
                    found_transition_before_display = True
                self._validate_transition(file, child)
            elif child.tag in self.EXTENSION_TAGS:
                self._validate_extension(file, child, is_root=True)
            elif child.tag == "relation":
                self._validate_relation(file, child)
            elif child.tag == "customProperty":
                pass  # 自定义属性，合法
            else:
                self._warn(file, f"<component> 下出现未知元素 <{child.tag}>")

        if not found_display:
            self._err(file, "组件缺少 <displayList> 元素")

        if found_controller_after_display:
            self._err(file, "<controller> 必须出现在 <displayList> 之前")

        if found_transition_before_display:
            self._err(file, "<transition> 必须出现在 <displayList> 之后")

    # ========== controller 校验 ==========

    def _validate_controller(self, file: str, elem: ET.Element):
        """校验 controller"""
        name = elem.get("name")
        if not name:
            self._err(file, "<controller> 缺少 'name' 属性")

        pages = elem.get("pages")
        if not pages and pages != "":
            self._err(file, f"<controller name=\"{name}\"> 缺少 'pages' 属性")
        else:
            # pages 格式: "index,name,index,name,..."
            parts = pages.split(",")
            if len(parts) % 2 != 0:
                self._err(file, f"controller \"{name}\" pages 格式错误，应为偶数个逗号分隔值")

    # ========== displayList 校验 ==========

    def _validate_display_list(self, file: str, dl: ET.Element, element_names: Set[str]):
        """校验 displayList"""
        for elem in dl:
            tag = elem.tag
            if tag not in self.DISPLAY_LIST_TAGS:
                self._err(file, f"displayList 下出现非法元素 <{tag}>")
                continue

            # 必需属性
            elem_id = elem.get("id")
            elem_name = elem.get("name")
            if not elem_id:
                self._err(file, f"<{tag}> 缺少 'id' 属性")
            if not elem_name:
                self._warn(file, f"<{tag} id=\"{elem_id}\"> 缺少 'name' 属性")

            # 属性合法性
            allowed = self.COMMON_ELEMENT_ATTRS | self.ELEMENT_EXTRA_ATTRS.get(tag, set())
            for attr in elem.attrib:
                if attr not in allowed:
                    self._warn(file, f"<{tag} id=\"{elem_id}\"> 出现未知属性 '{attr}'")

            # 类型特定校验
            if tag == "graph":
                self._validate_graph(file, elem)
            elif tag == "text" or tag == "richtext" or tag == "inputtext":
                self._validate_text(file, elem)
            elif tag == "image":
                self._validate_image_element(file, elem)
            elif tag == "loader" or tag == "loader3d":
                self._validate_loader(file, elem)
            elif tag == "component":
                self._validate_component_ref(file, elem)
            elif tag == "list":
                self._validate_list(file, elem)

            # 子元素校验（gear/relation/extension）
            for child in elem:
                if child.tag in self.GEAR_TAGS:
                    self._validate_gear(file, child, tag)
                elif child.tag == "relation":
                    self._validate_relation(file, child)
                elif child.tag in self.EXTENSION_TAGS:
                    self._validate_extension(file, child, is_root=False)
                elif child.tag == "item":
                    pass  # list/ComboBox 的 item
                else:
                    self._warn(file, f"<{tag}> 下出现未知子元素 <{child.tag}>")

            # 通用属性格式检查
            if "xy" in elem.attrib:
                self._check_xy(file, f"{tag}.xy", elem.get("xy"))
            if "size" in elem.attrib:
                self._check_size(file, f"{tag}.size", elem.get("size"))
            if "pivot" in elem.attrib:
                self._check_xy(file, f"{tag}.pivot", elem.get("pivot"))

    # ========== graph 校验 ==========

    def _validate_graph(self, file: str, elem: ET.Element):
        """校验 graph 元件"""
        graph_type = elem.get("type")
        if graph_type and graph_type not in self.GRAPH_TYPES:
            self._err(file, f"graph type 非法: \"{graph_type}\"，应为 rect/eclipse/polygon/regular_polygon")

        if "fillColor" in elem.attrib:
            self._check_color(file, "graph.fillColor", elem.get("fillColor"))
        if "lineColor" in elem.attrib:
            self._check_color(file, "graph.lineColor", elem.get("lineColor"))

        # corner 只接受单个数值（编辑器用 Single.Parse 解析）
        if "corner" in elem.attrib:
            corner_val = elem.get("corner")
            try:
                float(corner_val)
            except ValueError:
                self._err(file, f"graph corner 格式非法: \"{corner_val}\"，只接受单个数值（如 corner=\"20\"），不支持多值")

        # polygon 需要 points
        if graph_type == "polygon":
            if "points" not in elem.attrib:
                self._warn(file, "graph type=\"polygon\" 但缺少 points 属性")
            else:
                # 校验 points 格式：逗号分隔的数值序列，数量必须为偶数
                pts = elem.get("points")
                parts = pts.split(",")
                if len(parts) % 2 != 0:
                    self._err(file, f"graph points 坐标数量必须为偶数（当前 {len(parts)} 个值）")
                for i, p in enumerate(parts):
                    try:
                        float(p.strip())
                    except ValueError:
                        self._err(file, f"graph points 第 {i+1} 个值非法: \"{p.strip()}\"，应为数值")
                        break

        if graph_type == "regular_polygon" and "sides" not in elem.attrib:
            self._warn(file, "graph type=\"regular_polygon\" 但缺少 sides 属性")

        # lineSize 应为数值
        if "lineSize" in elem.attrib:
            try:
                float(elem.get("lineSize"))
            except ValueError:
                self._err(file, f"graph lineSize 格式非法: \"{elem.get('lineSize')}\"，应为数值")

    # ========== text 校验 ==========

    def _validate_text(self, file: str, elem: ET.Element):
        """校验 text/richtext/inputtext"""
        if "align" in elem.attrib:
            v = elem.get("align")
            if v not in self.ALIGN_VALUES:
                self._err(file, f"text align 非法: \"{v}\"")
        if "vAlign" in elem.attrib:
            v = elem.get("vAlign")
            if v not in self.VALIGN_VALUES:
                self._err(file, f"text vAlign 非法: \"{v}\"")
        if "autoSize" in elem.attrib:
            v = elem.get("autoSize")
            if v not in self.AUTO_SIZE_VALUES:
                self._err(file, f"text autoSize 非法: \"{v}\"")
        if "color" in elem.attrib:
            self._check_color(file, "text.color", elem.get("color"))

    # ========== image element 校验 ==========

    def _validate_image_element(self, file: str, elem: ET.Element):
        """校验 displayList 中的 image"""
        if "src" not in elem.attrib:
            self._err(file, f"<image id=\"{elem.get('id')}\"> 缺少 'src' 属性")
        if "color" in elem.attrib:
            self._check_color(file, "image.color", elem.get("color"))

    # ========== loader 校验 ==========

    def _validate_loader(self, file: str, elem: ET.Element):
        """校验 loader"""
        if "fill" in elem.attrib:
            v = elem.get("fill")
            if v not in self.FILL_VALUES:
                self._err(file, f"loader fill 非法: \"{v}\"")
        if "align" in elem.attrib:
            v = elem.get("align")
            if v not in self.ALIGN_VALUES:
                self._err(file, f"loader align 非法: \"{v}\"")
        if "vAlign" in elem.attrib:
            v = elem.get("vAlign")
            if v not in self.VALIGN_VALUES:
                self._err(file, f"loader vAlign 非法: \"{v}\"")

    # ========== component ref 校验 ==========

    def _validate_component_ref(self, file: str, elem: ET.Element):
        """校验 component 引用"""
        if "src" not in elem.attrib:
            self._err(file, f"<component id=\"{elem.get('id')}\"> 缺少 'src' 属性")

    # ========== list 校验 ==========

    def _validate_list(self, file: str, elem: ET.Element):
        """校验 list"""
        if "layout" in elem.attrib:
            v = elem.get("layout")
            if v not in self.LIST_LAYOUTS:
                self._err(file, f"list layout 非法: \"{v}\"")
        if "overflow" in elem.attrib:
            v = elem.get("overflow")
            if v not in self.OVERFLOW_VALUES:
                self._err(file, f"list overflow 非法: \"{v}\"")

        # defaultItem 格式校验：必须是 ui://包ID资源ID 或 ui://包名/资源名 格式
        if "defaultItem" in elem.attrib:
            di = elem.get("defaultItem")
            if di:
                if not di.startswith("ui://"):
                    self._err(file,
                              f"list defaultItem 格式非法: \"{di}\"，"
                              f"应为 \"ui://包ID资源ID\" 或 \"ui://包名/资源名\"，"
                              f"不能使用文件路径")

    # ========== gear 校验 ==========

    def _validate_gear(self, file: str, elem: ET.Element, parent_tag: str):
        """校验 gear 子元素"""
        if "controller" not in elem.attrib:
            self._err(file, f"<{elem.tag}> 缺少 'controller' 属性")

        # gearDisplay 和 gearDisplay2 必须有 pages
        if elem.tag in ("gearDisplay", "gearDisplay2"):
            if "pages" not in elem.attrib:
                self._warn(file, f"<{elem.tag}> 缺少 'pages' 属性")

        for attr in elem.attrib:
            if attr not in self.GEAR_ATTRS:
                self._warn(file, f"<{elem.tag}> 出现未知属性 '{attr}'")

    # ========== relation 校验 ==========

    def _validate_relation(self, file: str, elem: ET.Element):
        """校验 relation"""
        side_pair = elem.get("sidePair")
        if not side_pair:
            self._err(file, "<relation> 缺少 'sidePair' 属性")
            return

        pairs = side_pair.split(",")
        for pair in pairs:
            clean = pair.rstrip("%")
            if clean not in self.SIDE_PAIR_VALUES:
                self._err(file, f"relation sidePair 值非法: \"{pair}\"")

    # ========== extension 校验 ==========

    def _validate_extension(self, file: str, elem: ET.Element, is_root: bool):
        """校验扩展元素 (Button/Label/ProgressBar/...)"""
        tag = elem.tag
        if tag not in self.EXTENSION_TAGS:
            return

        allowed = self.EXTENSION_ATTRS.get(tag, set())
        for attr in elem.attrib:
            if attr not in allowed:
                self._warn(file, f"<{tag}> 出现未知属性 '{attr}'")

        # ComboBox 子元素 item
        if tag == "ComboBox":
            for child in elem:
                if child.tag != "item":
                    self._warn(file, f"<ComboBox> 下出现未知子元素 <{child.tag}>")

    # ========== transition 校验 ==========

    def _validate_transition(self, file: str, elem: ET.Element):
        """校验 transition"""
        name = elem.get("name")
        if not name:
            self._err(file, "<transition> 缺少 'name' 属性")

        for item in elem:
            if item.tag != "item":
                self._warn(file, f"<transition> 下出现未知元素 <{item.tag}>")
                continue

            # 必需属性
            if "time" not in item.attrib:
                self._err(file, f"transition item 缺少 'time' 属性")
            if "type" not in item.attrib:
                self._err(file, f"transition item 缺少 'type' 属性")
                continue

            item_type = item.get("type")
            if item_type not in self.TRANSITION_TYPES:
                self._err(file, f"transition item type 非法: \"{item_type}\"")

            # 属性合法性
            for attr in item.attrib:
                if attr not in self.TRANSITION_ITEM_ATTRS:
                    self._warn(file, f"transition item 出现未知属性 '{attr}'")

            # ease 值
            if "ease" in item.attrib:
                ease = item.get("ease")
                if ease not in self.EASE_FUNCTIONS:
                    self._err(file, f"transition ease 非法: \"{ease}\"")

            # tween 时应有 startValue/endValue 或 value
            is_tween = item.get("tween") == "true"
            has_value = "value" in item.attrib
            has_start_end = "startValue" in item.attrib or "endValue" in item.attrib
            if is_tween and not has_start_end:
                self._warn(file, f"transition item tween=\"true\" 但缺少 startValue/endValue")
            if not is_tween and not has_value and not has_start_end:
                # 一些类型如 Transition 嵌套可以没有 value
                if item_type not in ("Transition",):
                    self._warn(file, f"transition item type=\"{item_type}\" 缺少 value 或 startValue/endValue")

    # ========== HTML 注释检测 ==========

    def check_html_comments(self, file: str, content: str):
        """检测 XML 中的 HTML 注释"""
        if "<!--" in content:
            self._err(file, "XML 中包含 HTML 注释 <!-- -->，FairyGUI 编辑器不支持")

    # ========== 跨文件引用校验 ==========

    def validate_cross_references(self, pkg_file: str, component_files: Dict[str, ET.Element]):
        """校验包内引用完整性"""
        if pkg_file not in self.resource_ids:
            return

        pkg_ids = self.resource_ids[pkg_file]

        for comp_file, root in component_files.items():
            dl = root.find("displayList")
            if dl is None:
                continue

            for elem in dl:
                src = elem.get("src")
                if src and src not in pkg_ids:
                    self._warn(comp_file, f"元件引用的 src=\"{src}\" 在 package.xml 中未找到")

    # ========== 主入口 ==========

    def validate_file(self, filepath: str) -> bool:
        """校验单个文件"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self._err(filepath, f"无法读取文件: {e}")
            return False

        # HTML 注释检测
        self.check_html_comments(filepath, content)

        # 解析 XML
        try:
            root = ET.fromstring(content)
        except ET.ParseError as e:
            self._err(filepath, f"XML 解析失败: {e}")
            return False

        filename = os.path.basename(filepath)
        if filename == "package.xml":
            self.validate_package_xml(filepath, root)
        else:
            self.validate_component_xml(filepath, root)

        return True

    def validate_directory(self, dirpath: str):
        """校验整个目录（一个 FairyGUI 包）"""
        pkg_file = os.path.join(dirpath, "package.xml")
        component_files = {}

        # 先校验 package.xml
        if os.path.exists(pkg_file):
            self.validate_file(pkg_file)
        else:
            self._warn(dirpath, "目录中未找到 package.xml")

        # 遍历所有 XML
        for root_dir, dirs, files in os.walk(dirpath):
            for f in files:
                if f.endswith(".xml") and f != "package.xml":
                    filepath = os.path.join(root_dir, f)
                    if self.validate_file(filepath):
                        try:
                            tree = ET.parse(filepath)
                            component_files[filepath] = tree.getroot()
                        except ET.ParseError:
                            pass

        # 跨文件引用校验
        if pkg_file in self.resource_ids:
            self.validate_cross_references(pkg_file, component_files)

    def report(self) -> Tuple[int, int]:
        """输出报告，返回 (错误数, 警告数)"""
        if not self.errors and not self.warnings:
            print("[PASS] Validation passed, no issues found.")
            return 0, 0

        if self.errors:
            print(f"\n[FAIL] Found {len(self.errors)} error(s):")
            print("-" * 60)
            for e in self.errors:
                print(f"  {e}")

        if self.warnings:
            print(f"\n[WARN] Found {len(self.warnings)} warning(s):")
            print("-" * 60)
            for w in self.warnings:
                print(f"  {w}")

        print(f"\nTotal: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        return len(self.errors), len(self.warnings)


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_fui.py <目录或XML文件路径>")
        print("  目录: 校验整个 FairyGUI 包")
        print("  文件: 校验单个 XML 文件")
        sys.exit(1)

    target = sys.argv[1]
    validator = FUIValidator()

    if os.path.isdir(target):
        # 检测是否有子目录（多包）
        has_sub_packages = False
        for item in os.listdir(target):
            sub = os.path.join(target, item)
            if os.path.isdir(sub) and os.path.exists(os.path.join(sub, "package.xml")):
                has_sub_packages = True
                print(f"[PKG] Validating package: {item}")
                validator.validate_directory(sub)

        if not has_sub_packages:
            # 当前目录就是一个包
            validator.validate_directory(target)
    elif os.path.isfile(target):
        validator.validate_file(target)
    else:
        print(f"路径不存在: {target}")
        sys.exit(1)

    errors, warnings = validator.report()
    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
