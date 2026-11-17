"""CMSIS-SVD 解析（纯标准库）。

支持：
- derivedFrom：外设整体继承；寄存器继承（同名整体覆盖，不做字段合并）
- dim / dimIncrement / dimIndex：外设、簇、寄存器的数组展开，名称中的 %s 替换
- cluster：子寄存器名称前缀为簇实例名，如 CH1.CCR
- 位域三种写法：bitOffset+bitWidth、bitRange [msb:lsb]、lsb+msb
- enumeratedValues：支持 #01x 形式的任意位

结构性错误（不是 SVD、XML 语法错误）直接抛出 EtkError；局部问题（位域缺位置、
派生引用断开、派生循环）记入 Device.warnings 并跳过，保证其余内容仍可查询。
"""

from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET
from collections import OrderedDict
from dataclasses import dataclass
from dataclasses import field as dc_field

from .errors import E_SVD_NOT_FOUND, E_SVD_PARSE, EtkError
from .values import dim_indices, parse_enum_value, parse_number

_ATTR_DEFAULTS = {
    "size": 32,
    "access": "read-write",
    "reset_value": 0,
    "reset_mask": 0xFFFFFFFF,
    "modified_write_values": "",
    "read_action": "",
}
_BIT_RANGE = re.compile(r"^\[\s*(\d+)\s*:\s*(\d+)\s*\]$")
_NODE_TAGS = ("register", "cluster")


@dataclass
class EnumValue:
    name: str
    value: int
    mask: int
    description: str
    is_default: bool = False
    # enumeratedValues 的 usage：read / write / read-write（缺省按 read-write）
    usage: str = "read-write"


@dataclass
class Interrupt:
    name: str
    value: int
    description: str


@dataclass
class Field:
    name: str
    lsb: int
    width: int
    access: str
    description: str
    enums: list = dc_field(default_factory=list)
    modified_write_values: str = ""
    read_action: str = ""

    @property
    def msb(self):
        return self.lsb + self.width - 1

    @property
    def bit_text(self):
        return str(self.lsb) if self.width == 1 else "%d:%d" % (self.msb, self.lsb)

    @property
    def mask(self):
        return (1 << self.width) - 1

    @property
    def read_enums(self):
        """读视角枚举：排除 usage=write 的组；缺省 usage 视为 read-write，保持旧行为。"""
        return [e for e in self.enums if getattr(e, "usage", "read-write") != "write"]

    @property
    def write_enums(self):
        """写视角枚举：排除 usage=read 的组；缺省 usage 视为 read-write，保持旧行为。"""
        return [e for e in self.enums if getattr(e, "usage", "read-write") != "read"]


@dataclass
class Register:
    name: str
    offset: int
    size: int
    access: str
    reset_value: int
    reset_mask: int
    description: str
    fields: list = dc_field(default_factory=list)
    modified_write_values: str = ""
    read_action: str = ""

    @property
    def nbytes(self):
        return max(1, self.size // 8)

    def field(self, name):
        key = name.upper()
        for item in self.fields:
            if item.name.upper() == key:
                return item
        return None


@dataclass
class Peripheral:
    name: str
    base_address: int
    description: str
    group_name: str
    derived_from: str
    address_span: int
    registers: list = dc_field(default_factory=list)
    interrupts: list = dc_field(default_factory=list)

    def register(self, name):
        key = name.upper()
        for item in self.registers:
            if item.name.upper() == key:
                return item
        return None


@dataclass
class Device:
    name: str
    version: str
    description: str
    path: str
    peripherals: list = dc_field(default_factory=list)
    warnings: list = dc_field(default_factory=list)
    vendor: str = ""
    cpu: str = ""

    def peripheral(self, name):
        key = name.upper()
        for item in self.peripherals:
            if item.name.upper() == key:
                return item
        return None


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _kids(el, tag):
    return [c for c in el if _local(c.tag) == tag]


def _kid(el, tag):
    for c in el:
        if _local(c.tag) == tag:
            return c
    return None


def _text(el, tag):
    c = _kid(el, tag)
    if c is None or c.text is None:
        return None
    return " ".join(c.text.split()) or None


class _PeriphRec:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class _Builder:
    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.warnings = []
        self.instances = OrderedDict()
        self.built = {}
        self.defaults = self._attrs(root, "设备", dict(_ATTR_DEFAULTS))

    def build(self):
        periphs = _kid(self.root, "peripherals")
        if periphs is None:
            raise EtkError(
                E_SVD_PARSE,
                "SVD 中没有 <peripherals> 节点",
                hint="确认文件是完整的设备描述，而不是片上外设的片段。",
            )
        self._collect(periphs)
        items = []
        for key in self.instances:
            rec = self._periph(key, ())
            if rec is not None:
                items.append(Peripheral(
                    name=rec.name,
                    base_address=rec.base,
                    description=rec.description,
                    group_name=rec.group,
                    derived_from=rec.derived,
                    address_span=rec.span,
                    registers=rec.registers,
                    interrupts=rec.interrupts,
                ))
        cpu_el = _kid(self.root, "cpu")
        return Device(
            name=_text(self.root, "name") or "未命名设备",
            version=_text(self.root, "version") or "",
            description=_text(self.root, "description") or "",
            path=self.path,
            peripherals=items,
            warnings=self.warnings,
            vendor=_text(self.root, "vendor") or "",
            cpu=(_text(cpu_el, "name") if cpu_el is not None else None) or "",
        )

    def _collect(self, periphs):
        for el in _kids(periphs, "peripheral"):
            name = _text(el, "name")
            base_text = _text(el, "baseAddress")
            if not name or base_text is None:
                self.warnings.append("跳过缺少 name 或 baseAddress 的外设（%s）" % (name or "未命名"))
                continue
            try:
                base = parse_number(base_text)
            except ValueError:
                self.warnings.append("外设 %s 的 baseAddress=%r 无法解析，已跳过" % (name, base_text))
                continue
            for inst_name, addr, _ in self._instances_of(el, name, base, "外设 %s" % name):
                key = inst_name.upper()
                if key in self.instances:
                    self.warnings.append("外设名重复：%s，后者已忽略" % inst_name)
                    continue
                self.instances[key] = (inst_name, el, addr)

    def _periph(self, key, stack):
        if key in self.built:
            return self.built[key]
        if key in stack:
            self.warnings.append("外设派生循环：%s，已断开" % " -> ".join(stack + (key,)))
            return None
        inst_name, el, addr = self.instances[key]
        where = "外设 %s" % inst_name
        defaults = dict(self.defaults)
        nodes = OrderedDict()
        base = None
        base_name = el.get("derivedFrom")
        if base_name:
            base_key = base_name.upper()
            if base_key not in self.instances:
                self.warnings.append("%s 派生自未知外设 %s，已忽略继承" % (where, base_name))
            else:
                base = self._periph(base_key, stack + (key,))
                if base is not None:
                    defaults = dict(base.defaults)
                    nodes = OrderedDict(base.nodes)
        defaults = self._attrs(el, where, defaults)
        regs_el = _kid(el, "registers")
        if regs_el is not None:
            for node in regs_el:
                node_name = _text(node, "name")
                if _local(node.tag) in _NODE_TAGS and node_name:
                    nodes[node_name] = node
        registers = self._expand(list(nodes.values()), nodes, defaults, 0, "", inst_name)
        declared = []
        for el_i in _kids(el, "interrupt"):
            i_name = _text(el_i, "name")
            i_value_text = _text(el_i, "value")
            if not i_name or i_value_text is None:
                self.warnings.append("%s 有缺少 name 或 value 的 interrupt，已跳过" % where)
                continue
            try:
                i_value = parse_number(i_value_text)
            except ValueError:
                self.warnings.append("%s 的中断 %s value=%r 无法解析，已跳过" % (where, i_name, i_value_text))
                continue
            declared.append(Interrupt(
                name=i_name,
                value=i_value,
                description=_text(el_i, "description") or "",
            ))
        if declared:
            interrupts = declared
        elif base is not None:
            interrupts = list(base.interrupts)
        else:
            interrupts = []
        block = self._block_span(el, where)
        if block == 0 and base is not None:
            block = base.block
        reg_end = max((r.offset + r.nbytes for r in registers), default=0)
        rec = _PeriphRec(
            name=inst_name,
            base=addr,
            description=_text(el, "description") or (base.description if base else ""),
            group=_text(el, "groupName") or (base.group if base else ""),
            derived=base_name,
            defaults=defaults,
            nodes=nodes,
            registers=registers,
            interrupts=interrupts,
            block=block,
            span=max(block, reg_end),
        )
        self.built[key] = rec
        return rec

    def _block_span(self, el, where):
        span = 0
        for blk in _kids(el, "addressBlock"):
            try:
                off = parse_number(_text(blk, "offset") or "0")
                size = parse_number(_text(blk, "size") or "0")
            except ValueError:
                self.warnings.append("%s 的 addressBlock 无法解析，已忽略" % where)
                continue
            span = max(span, off + size)
        return span

    def _attrs(self, el, where, base):
        out = dict(base)
        size = self._num(el, "size", where)
        if size is None:
            size = self._num(el, "width", where)
        if size is not None:
            out["size"] = size
        access = _text(el, "access")
        if access:
            out["access"] = access
        reset = self._num(el, "resetValue", where)
        if reset is not None:
            out["reset_value"] = reset
        mask = self._num(el, "resetMask", where)
        if mask is not None:
            out["reset_mask"] = mask
        modified = _text(el, "modifiedWriteValues")
        if modified:
            out["modified_write_values"] = modified
        read_action = _text(el, "readAction")
        if read_action:
            out["read_action"] = read_action
        return out

    def _num(self, el, tag, where):
        text = _text(el, tag)
        if text is None:
            return None
        try:
            return parse_number(text)
        except ValueError:
            self.warnings.append("%s 的 <%s>=%r 无法解析，已忽略" % (where, tag, text))
            return None

    def _offset(self, el, where):
        text = _text(el, "addressOffset")
        if text is None:
            return 0
        try:
            return parse_number(text)
        except ValueError:
            self.warnings.append("%s 的 addressOffset=%r 无法解析，按 0 处理" % (where, text))
            return 0

    def _instances_of(self, el, name, base, where):
        """按 dim 展开为实例列表 [(实例名, 偏移或地址, 索引)]。没有 dim 时返回自身。"""
        dim_text = _text(el, "dim")
        if dim_text is None:
            return [(name, base, None)]
        try:
            count = parse_number(dim_text)
            incr = parse_number(_text(el, "dimIncrement") or "0")
        except ValueError:
            self.warnings.append("%s 的 dim/dimIncrement 无法解析，已跳过" % where)
            return []
        indices = dim_indices(count, _text(el, "dimIndex"))
        if len(indices) != count:
            self.warnings.append("%s 的 dim=%d 与 dimIndex 展开的 %d 个不一致，按 dimIndex 展开" % (where, count, len(indices)))
        return [(name.replace("%s", idx), base + i * incr, idx) for i, idx in enumerate(indices)]

    def _expand(self, nodes, scope, defaults, base_offset, prefix, periph):
        out = []
        for node in nodes:
            if not _text(node, "name"):
                continue
            if _local(node.tag) == "cluster":
                out.extend(self._expand_cluster(node, defaults, base_offset, prefix, periph))
            else:
                out.extend(self._expand_register(node, scope, defaults, base_offset, prefix, periph))
        return out

    def _expand_cluster(self, node, defaults, base_offset, prefix, periph):
        name = _text(node, "name")
        where = "外设 %s 簇 %s" % (periph, name)
        if node.get("derivedFrom"):
            self.warnings.append("%s 的 derivedFrom 暂不支持，已忽略" % where)
        own = self._offset(node, where)
        children = [c for c in node if _local(c.tag) in _NODE_TAGS]
        scope = OrderedDict((_text(c, "name"), c) for c in children if _text(c, "name"))
        out = []
        for inst_name, inst_off, _ in self._instances_of(node, name, base_offset + own, where):
            out.extend(self._expand(children, scope, defaults, inst_off, prefix + inst_name + ".", periph))
        return out

    def _expand_register(self, node, scope, defaults, base_offset, prefix, periph):
        name = _text(node, "name")
        where = "外设 %s 寄存器 %s" % (periph, name)
        tpl = self._template(node, scope, defaults, where, ())
        fields = self._fields(
            tpl["field_els"], tpl["access"], where,
            tpl["modified_write_values"], tpl["read_action"])
        offset = base_offset + self._offset(node, where)
        return [
            Register(
                name=prefix + inst,
                offset=off,
                size=tpl["size"],
                access=tpl["access"],
                reset_value=tpl["reset_value"],
                reset_mask=tpl["reset_mask"],
                description=tpl["description"],
                fields=fields,
                modified_write_values=tpl["modified_write_values"],
                read_action=tpl["read_action"],
            )
            for inst, off, _ in self._instances_of(node, name, offset, where)
        ]

    def _template(self, node, scope, defaults, where, seen):
        name = _text(node, "name")
        attrs = dict(defaults)
        description = ""
        fields = OrderedDict()
        base_name = node.get("derivedFrom")
        if base_name:
            base_el = scope.get(base_name)
            if base_el is None or base_el is node or base_name in seen:
                self.warnings.append("%s: derivedFrom=%s 找不到或形成循环，已忽略继承" % (where, base_name))
            else:
                base_tpl = self._template(base_el, scope, defaults, where, seen + (name,))
                attrs = {k: base_tpl[k] for k in _ATTR_DEFAULTS}
                description = base_tpl["description"]
                fields = OrderedDict(base_tpl["field_els"])
        attrs = self._attrs(node, where, attrs)
        fields_el = _kid(node, "fields")
        if fields_el is not None:
            for f_el in _kids(fields_el, "field"):
                f_name = _text(f_el, "name")
                if f_name:
                    fields[f_name] = f_el
                else:
                    self.warnings.append("%s 中有缺少 name 的位域，已跳过" % where)
        return dict(attrs, description=_text(node, "description") or description, field_els=fields)

    def _fields(self, field_els, access, where, modified_write_values="", read_action=""):
        out = []
        for f_name, f_el in field_els.items():
            spot = "%s 位域 %s" % (where, f_name)
            bits = self._bits(f_el, spot)
            if bits is None:
                continue
            lsb, width = bits
            out.append(Field(
                name=f_name,
                lsb=lsb,
                width=width,
                access=_text(f_el, "access") or access,
                description=_text(f_el, "description") or "",
                enums=self._enums(f_el, width, spot),
                modified_write_values=_text(f_el, "modifiedWriteValues") or modified_write_values,
                read_action=_text(f_el, "readAction") or read_action,
            ))
        return out

    def _bits(self, f_el, where):
        off = _text(f_el, "bitOffset")
        wid = _text(f_el, "bitWidth")
        rng = _text(f_el, "bitRange")
        lsb_t = _text(f_el, "lsb")
        msb_t = _text(f_el, "msb")
        try:
            if off is not None and wid is not None:
                lsb, width = parse_number(off), parse_number(wid)
            elif rng is not None and _BIT_RANGE.match(rng):
                match = _BIT_RANGE.match(rng)
                msb, lsb = int(match.group(1)), int(match.group(2))
                width = msb - lsb + 1
            elif lsb_t is not None and msb_t is not None:
                lsb, msb = parse_number(lsb_t), parse_number(msb_t)
                width = msb - lsb + 1
            else:
                self.warnings.append("%s 缺少位置信息（bitOffset/bitWidth、bitRange 或 lsb/msb），已跳过" % where)
                return None
        except ValueError:
            self.warnings.append("%s 的位置信息无法解析，已跳过" % where)
            return None
        if width <= 0:
            self.warnings.append("%s 的宽度无效（%d），已跳过" % (where, width))
            return None
        return lsb, width

    def _enums(self, f_el, width, where):
        out = []
        for group in _kids(f_el, "enumeratedValues"):
            # usage 属于 enumeratedValues 组：read / write / read-write。
            # 缺省（或无法识别的写法）按 read-write 处理，保证不丢枚举。
            usage = (_text(group, "usage") or "").strip().lower() or "read-write"
            for ev in _kids(group, "enumeratedValue"):
                text = _text(ev, "value")
                is_default = (_text(ev, "isDefault") or "").strip().lower() in ("true", "1")
                if text is None:
                    if is_default:
                        # 默认项（isDefault）：代表"其余所有取值"——mask=0 使其匹配任意值
                        out.append(EnumValue(
                            name=_text(ev, "name") or "",
                            value=0,
                            mask=0,
                            description=_text(ev, "description") or "",
                            is_default=True,
                            usage=usage,
                        ))
                    continue
                try:
                    value, mask = parse_enum_value(text, width)
                except ValueError:
                    self.warnings.append("%s 的枚举值 %r 无法解析，已忽略" % (where, text))
                    continue
                if value >> width:
                    self.warnings.append("%s 的枚举值 %r 超出位宽 %d，已忽略" % (where, text, width))
                    continue
                out.append(EnumValue(
                    name=_text(ev, "name") or "",
                    value=value,
                    mask=mask,
                    description=_text(ev, "description") or "",
                    is_default=is_default,
                    usage=usage,
                ))
        return out


_LEADING_JUNK_OK = frozenset(b" \t\r\n") | {0xEF, 0xBB, 0xBF}


def _load_root(path):
    """解析 XML 根元素，容忍 <?xml 声明前的空白或 BOM。

    部分厂商 SVD（实测 GigaDevice GD32F3x0_DFP 3.0.2）在 XML 声明前带空格，
    expat 会报 "XML or text declaration not at start of entity"。此处仅在
    首轮失败后剥离开头的纯空白/BOM 字节重试；其余内容保持原样，错误照旧上报。
    返回 (根元素, 说明或 None)。
    """
    try:
        return ET.parse(path).getroot(), None
    except ET.ParseError as original:
        with open(path, "rb") as fh:
            data = fh.read()
        idx = 0
        while idx < len(data) and data[idx] in _LEADING_JUNK_OK:
            idx += 1
        if idx == 0 or idx >= len(data) or data[idx:idx + 1] != b"<":
            raise original
        try:
            root = ET.fromstring(data[idx:])
        except ET.ParseError:
            raise original
        return root, "文件开头有 %d 字节空白或 BOM（XML 声明之前），已自动忽略" % idx


def load_device(path):
    """解析 SVD 文件，返回 Device。文件不可读或 XML 有误时抛出 EtkError。"""
    path = os.fspath(path)
    try:
        root, note = _load_root(path)
    except ET.ParseError as exc:
        line, column = exc.position
        raise EtkError(
            E_SVD_PARSE,
            "SVD 解析失败：%s（%s）" % (os.path.basename(path), exc),
            hint="检查该位置附近的标签是否配对、属性是否带引号；文件被截断时需重新获取。",
            details={"line": line, "column": column},
        ) from None
    except OSError as exc:
        raise EtkError(
            E_SVD_NOT_FOUND,
            "无法读取 SVD 文件：%s（%s）" % (path, exc.strerror or exc),
            hint="确认路径存在且有读取权限。",
        ) from None
    if _local(root.tag) != "device":
        raise EtkError(
            E_SVD_PARSE,
            "不是 CMSIS-SVD 文件：根元素是 <%s>，应为 <device>" % _local(root.tag),
            hint="确认选择的是芯片的 .svd 文件，而不是 .pdsc、.h 或其他文件。",
        )
    device = _Builder(root, path).build()
    if note:
        device.warnings.insert(0, note + "（建议向厂商反馈该 SVD 的格式问题）")
    return device


def device_name_fast(path):
    """快速读出 <device> 的第一个 <name>（用于 devices 盘点），失败时返回 None。

    用 iterparse 只读到设备名就停止，几百个文件也能秒级完成。
    """
    depth = 0
    try:
        for event, el in ET.iterparse(path, events=("start", "end")):
            if event == "start":
                depth += 1
                if depth > 3:
                    return None
                continue
            depth -= 1
            if depth == 1 and _local(el.tag) == "name":
                text = (el.text or "").strip()
                return " ".join(text.split()) or None
    except (ET.ParseError, OSError, ValueError):
        return None
    return None
