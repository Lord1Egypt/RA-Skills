"""SVD 查询：外设、寄存器、位域、地址反查、关键词搜索、寄存器值解码。

函数只读 Device，不做 I/O。错误用 EtkError 抛出，由调用方统一输出。
"""

from __future__ import annotations

import difflib
import hashlib
import os
import re
import time
from collections import OrderedDict

from .errors import (
    E_FIELD_NOT_FOUND,
    E_INPUT_INVALID,
    E_PERIPH_NOT_FOUND,
    E_REG_NOT_FOUND,
    E_SVD_NOT_FOUND,
    EtkError,
)
from .output import LABEL_VERIFIED, read_semantics, source_meta, write_semantics
from .values import parse_number


def hex_addr(value):
    return "0x%08X" % value


def hex_offset(value):
    return "0x%02X" % value


def hex_reset(value, size):
    return "0x%0*X" % (max(1, size // 4), value)


def hex_mask(value, size):
    return "0x%0*X" % (max(1, size // 4), value)


def split_query(text):
    raw = (text or "").strip().replace("->", ".")
    parts = [p.strip() for p in raw.split(".")]
    if not raw or any(not p for p in parts):
        raise EtkError(
            E_INPUT_INVALID,
            "查询格式不正确：%r" % text,
            hint="格式为 外设.寄存器.位域，例如 USART1.CR1.UE；也可以写 USART1->CR1。",
        )
    return parts


def suggest(name, candidates, limit=3):
    """候选名：先取前缀匹配，再取相近拼写。"""
    orig = OrderedDict()
    for cand in candidates:
        orig.setdefault(cand.upper(), cand)
    key = name.upper()
    picked = [v for k, v in orig.items() if k.startswith(key)]
    for k in difflib.get_close_matches(key, list(orig), n=limit, cutoff=0.6):
        if orig[k] not in picked:
            picked.append(orig[k])
    return picked[:limit]


def _periph_or_raise(device, name):
    periph = device.peripheral(name)
    if periph is None:
        sugg = suggest(name, [p.name for p in device.peripherals])
        hint = "检查拼写；可用 list 子命令列出全部外设。"
        if sugg:
            hint += "你可能要找：%s。" % "、".join(sugg)
        raise EtkError(
            E_PERIPH_NOT_FOUND,
            "在 %s 中找不到外设 %s" % (device.name, name),
            hint=hint,
            details={"suggestions": sugg},
        )
    return periph


def _register_missing(periph, name):
    sugg = suggest(name, [r.name for r in periph.registers])
    owners = [] if "." in name else [r for r in periph.registers if r.field(name) is not None]
    hint = "检查拼写；可用 search 子命令按关键词查找。"
    if owners:
        hint = "%s 是位域而不是寄存器，位于 %s 中，请写成 %s.%s.%s。" % (
            name, "、".join(o.name for o in owners[:3]), periph.name, owners[0].name, name)
    elif sugg:
        hint += "你可能要找：%s。" % "、".join(sugg)
    return EtkError(
        E_REG_NOT_FOUND,
        "%s 中找不到寄存器 %s" % (periph.name, name),
        hint=hint,
        details={"suggestions": sugg},
    )


def _pattern(value, mask, width):
    out = []
    for i in range(width - 1, -1, -1):
        if (mask >> i) & 1:
            out.append("1" if (value >> i) & 1 else "0")
        else:
            out.append("x")
    return "".join(out)


def _reg_dict(periph, reg):
    return {
        "name": reg.name,
        "offset": hex_offset(reg.offset),
        "address": hex_addr(periph.base_address + reg.offset),
        "size": reg.size,
        "access": reg.access,
        "reset": hex_reset(reg.reset_value, reg.size),
        "reset_mask": hex_reset(reg.reset_mask, reg.size),
        "description": reg.description,
        "modified_write_values": reg.modified_write_values,
        "write_semantics": write_semantics(reg.modified_write_values),
        "read_action": reg.read_action,
        "read_semantics": read_semantics(reg.read_action),
    }


def _field_dict(item, reg_reset, size):
    return {
        "name": item.name,
        "bits": item.bit_text,
        "lsb": item.lsb,
        "msb": item.msb,
        "width": item.width,
        "mask": hex_mask(item.mask << item.lsb, size),
        "access": item.access,
        "description": item.description,
        "reset": (reg_reset >> item.lsb) & item.mask,
        "modified_write_values": item.modified_write_values,
        "write_semantics": write_semantics(item.modified_write_values),
        "read_action": item.read_action,
        "read_semantics": read_semantics(item.read_action),
        "enums": [
            {
                "name": e.name,
                "value": e.value,
                "pattern": ("（其余值，默认）" if getattr(e, "is_default", False)
                            else _pattern(e.value, e.mask, item.width)),
                "description": e.description,
                "is_default": bool(getattr(e, "is_default", False)),
            }
            for e in item.enums
        ],
    }


def _bare_register_hits(device, name):
    """按寄存器名直接匹配（AVR/MSP430 裸寄存器名风格）：返回 [(periph, reg), ...]。"""
    key = (name or "").upper()
    index = getattr(device, "_reg_name_index", None)
    if index is None:
        index = {}
        for periph in device.peripherals:
            for reg in periph.registers:
                index.setdefault(reg.name.upper(), []).append((periph, reg))
        try:
            device._reg_name_index = index
        except AttributeError:
            pass
    return index.get(key, [])


def resolve_register(device, text):
    parts = split_query(text)
    periph = device.peripheral(parts[0])
    if periph is None:
        hits = _bare_register_hits(device, parts[0])
        if len(hits) == 1 and len(parts) == 1:
            return hits[0]
        _periph_or_raise(device, parts[0])
    if len(parts) < 2:
        raise EtkError(E_INPUT_INVALID, "需要指定寄存器，例如 RCC.CR", hint="格式为 外设.寄存器。")
    name = ".".join(parts[1:])
    reg = periph.register(name)
    if reg is None:
        if len(parts) >= 3 and periph.register(".".join(parts[1:-1])) is not None:
            raise EtkError(
                E_INPUT_INVALID,
                "此处需要寄存器，但 %s 是位域" % text,
                hint="去掉最后一段，改为 %s.%s。" % (periph.name, ".".join(parts[1:-1])),
            )
        raise _register_missing(periph, name)
    return periph, reg


def lookup(device, text):
    parts = split_query(text)
    source = source_meta(device)
    periph = device.peripheral(parts[0])
    if periph is None:
        # 裸寄存器名（AVR/MSP430/8051 风格）：UCSR0B、P1OUT、TIMSK0
        hits = _bare_register_hits(device, parts[0])
        if len(hits) == 1:
            hit_periph, hit_reg = hits[0]
            rest = parts[1:]
            if not rest:
                res = _register_result(hit_periph, hit_reg, source)
                res["resolved_by"] = "bare-name"
                return res
            fld = hit_reg.field(".".join(rest))
            if fld is None:
                sugg = suggest(rest[-1], [f.name for f in hit_reg.fields])
                hint = "可用 lookup %s.%s 查看全部位域。" % (hit_periph.name, hit_reg.name)
                if sugg:
                    hint += "你可能要找：%s。" % "、".join(sugg)
                raise EtkError(
                    E_FIELD_NOT_FOUND,
                    "%s 中没有位域 %s" % (hit_reg.name, ".".join(rest)),
                    hint=hint,
                    details={"suggestions": sugg},
                )
            res = _field_result(hit_periph, hit_reg, fld, source)
            res["resolved_by"] = "bare-name"
            return res
        if len(hits) > 1:
            options = "、".join("%s.%s" % (p.name, r.name) for p, r in hits[:6])
            raise EtkError(
                E_INPUT_INVALID,
                "%s 匹配多个寄存器：%s" % (parts[0], options),
                hint="请用 外设.寄存器 形式指定，例如 %s.%s。" % (hits[0][0].name, hits[0][1].name),
            )
        _periph_or_raise(device, parts[0])
    if len(parts) == 1:
        return _periph_result(periph, source)
    rest = parts[1:]
    full = ".".join(rest)
    reg = periph.register(full)
    if reg is not None:
        return _register_result(periph, reg, source)
    if len(rest) >= 2:
        owner = periph.register(".".join(rest[:-1]))
        if owner is not None:
            fld = owner.field(rest[-1])
            if fld is None:
                sugg = suggest(rest[-1], [f.name for f in owner.fields])
                hint = "可用 lookup %s.%s 查看全部位域。" % (periph.name, owner.name)
                if sugg:
                    hint += "你可能要找：%s。" % "、".join(sugg)
                raise EtkError(
                    E_FIELD_NOT_FOUND,
                    "%s.%s 中没有位域 %s" % (periph.name, owner.name, rest[-1]),
                    hint=hint,
                    details={"suggestions": sugg},
                )
            return _field_result(periph, owner, fld, source)
    prefix = full.upper() + "."
    members = [r for r in periph.registers if r.name.upper().startswith(prefix)]
    if members:
        return _cluster_result(periph, full, members, source)
    raise _register_missing(periph, ".".join(rest[:-1]) if len(rest) >= 2 else rest[0])


def _periph_result(periph, source):
    return {
        "kind": "peripheral",
        "peripheral": periph.name,
        "base_address": hex_addr(periph.base_address),
        "group": periph.group_name,
        "derived_from": periph.derived_from,
        "description": periph.description,
        "address_span": periph.address_span,
        "interrupts": [
            {"name": item.name, "value": item.value, "description": item.description}
            for item in periph.interrupts
        ],
        "registers": [_reg_dict(periph, r) for r in periph.registers],
        "label": LABEL_VERIFIED,
        "source": source,
    }


_SIBLING_KINDS = (("_SET", "置位"), ("_CLR", "清位"), ("_TGL", "翻转"), ("_XOR", "翻转"))


def sibling_registers(periph, reg):
    """按命名找同族的置位/清位/翻转寄存器。

    覆盖两种命名：Silabs 的 `EM4WUPOL` → `EM4WUPOL_SET/_CLR`、RP2040 的
    `GPIO_OUT` → `GPIO_OUT_SET/_CLR/_XOR`，以及 SAMD 的 `OUT0` → `OUTSET0/OUTCLR0/OUTTGL0`
    （后缀插在数字前）。无下划线的后缀（SET/CLR/TGL/XOR）要求至少两个兄弟同时存在才认定，
    避免 `RE` → `RESET` 这类误配。
    """
    names = {r.name.upper(): r.name for r in periph.registers}
    base = reg.name.upper()
    m = re.match(r"^(.*?)(\d+)$", base)
    stem, digit = (m.group(1), m.group(2)) if m else (base, "")
    out = []

    def add(cand, kind):
        if cand in names and names[cand].upper() != base:
            out.append({"name": names[cand], "kind": kind})

    for suffix, kind in _SIBLING_KINDS:
        add(base + suffix, kind)
        if digit:
            add(stem + suffix + digit, kind)
    plain = []
    for suffix, kind in (("SET", "置位"), ("CLR", "清位"), ("TGL", "翻转"), ("XOR", "翻转")):
        for cand in ([base + suffix] + ([stem + suffix + digit] if digit else [])):
            if cand in names and names[cand].upper() != base:
                plain.append((cand, kind))
    if len(plain) >= 2:
        for cand, kind in plain:
            if not any(item["name"].upper() == cand for item in out):
                out.append({"name": names[cand], "kind": kind})
    return out


def _register_result(periph, reg, source):
    note = _rmw_note(reg)
    return {
        "kind": "register",
        "peripheral": periph.name,
        "base_address": hex_addr(periph.base_address),
        "register": _reg_dict(periph, reg),
        "fields": [_field_dict(f, reg.reset_value, reg.size) for f in reg.fields],
        "siblings": sibling_registers(periph, reg),
        "notes": [note] if note else [],
        "label": LABEL_VERIFIED,
        "source": source,
    }


def _field_result(periph, reg, fld, source):
    return {
        "kind": "field",
        "peripheral": periph.name,
        "base_address": hex_addr(periph.base_address),
        "register": _reg_dict(periph, reg),
        "field": _field_dict(fld, reg.reset_value, reg.size),
        "label": LABEL_VERIFIED,
        "source": source,
    }


def _cluster_result(periph, cluster, members, source):
    return {
        "kind": "cluster",
        "peripheral": periph.name,
        "base_address": hex_addr(periph.base_address),
        "cluster": cluster,
        "registers": [_reg_dict(periph, r) for r in members],
        "label": LABEL_VERIFIED,
        "source": source,
    }


def find_address(device, address):
    source = source_meta(device)
    base = {"address": hex_addr(address), "label": LABEL_VERIFIED, "source": source}

    def _exact(addr):
        hits = []
        for periph in device.peripherals:
            for reg in periph.registers:
                if periph.base_address + reg.offset == addr:
                    hits.append({
                        "path": "%s.%s" % (periph.name, reg.name),
                        "peripheral": periph.name,
                        "register": reg.name,
                        "offset": hex_offset(reg.offset),
                        "access": reg.access,
                        "reset": hex_reset(reg.reset_value, reg.size),
                        "description": reg.description,
                    })
        return hits

    matches = _exact(address)
    if matches:
        return dict(base, kind="exact", matches=matches)
    if isinstance(address, int) and 0 < address < 0x10000:
        # AVR 等 SVD 用"0x800000 + 数据地址"的地址口径（如 PORTB = 0x800025）：做一次偏移探测
        probed = address + 0x800000
        matches = _exact(probed)
        if matches:
            return dict(base, kind="exact", matches=matches, probed_address=hex_addr(probed))
    for periph in device.peripherals:
        if periph.address_span <= 0:
            continue
        if not (periph.base_address <= address < periph.base_address + periph.address_span):
            continue
        below = [(periph.base_address + r.offset, r) for r in periph.registers
                 if periph.base_address + r.offset <= address]
        if not below:
            return dict(base, kind="gap", peripheral=periph.name, nearest=None)
        # 宽寄存器与窄别名并存时（如 W32 @0x0 4 字节 + B2 @0x2 1 字节），
        # "起始地址最大"不一定是包含者：先在所有包含者里取最具体的一个，找不到再回退最近者。
        containing = [(start, r) for start, r in below if address < start + r.nbytes]
        if containing:
            abs_addr, reg = max(containing, key=lambda item: item[0])
            delta = address - abs_addr
            kind = "inside_register"
        else:
            abs_addr, reg = max(below, key=lambda item: item[0])
            delta = address - abs_addr
            kind = "gap"
        nearest = {
            "path": "%s.%s" % (periph.name, reg.name),
            "register": reg.name,
            "address": hex_addr(abs_addr),
            "offset_in_register": delta,
            "size": reg.size,
        }
        return dict(base, kind=kind, peripheral=periph.name, nearest=nearest)
    return dict(base, kind="unmapped", peripheral=None, nearest=None)


def _rank(keyword, name, description):
    low = name.lower()
    if low == keyword:
        return 0
    if keyword in low:
        return 1
    if description and keyword in description.lower():
        return 2
    return None


def search(device, keyword, limit=50, kind=None, peripheral=None):
    kw = (keyword or "").strip().lower()
    if not kw:
        raise EtkError(E_INPUT_INVALID, "搜索关键词不能为空", hint="例如 search baud 或 search DMA。")
    periphs = [_periph_or_raise(device, peripheral)] if peripheral else device.peripherals
    hits = []
    for periph in periphs:
        rank = _rank(kw, periph.name, periph.description)
        if rank is not None and kind in (None, "peripheral"):
            hits.append((rank, periph.name, "peripheral", periph.name, periph.description))
        for reg in periph.registers:
            path = "%s.%s" % (periph.name, reg.name)
            rank = _rank(kw, reg.name, reg.description)
            if rank is not None and kind in (None, "register"):
                hits.append((rank, path, "register", path, reg.description))
            for fld in reg.fields:
                rank = _rank(kw, fld.name, fld.description)
                if rank is not None and kind in (None, "field"):
                    fpath = "%s.%s" % (path, fld.name)
                    hits.append((rank, fpath, "field", fpath, fld.description))
    hits.sort(key=lambda h: (h[0], h[1]))
    matches = [
        {"kind": kind, "path": path, "description": desc, "label": LABEL_VERIFIED}
        for _, _, kind, path, desc in hits[:limit]
    ]
    return {
        "kind": "search",
        "keyword": keyword,
        "peripheral": peripheral or None,
        "total": len(hits),
        "truncated": len(hits) > limit,
        "matches": matches,
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }


_RMW_SEMANTICS = (
    "oneToClear", "oneToSet", "oneToToggle",
    "zeroToClear", "zeroToSet", "zeroToToggle", "clear", "set", "modify",
)


def _effective_write_semantics(reg):
    if reg.modified_write_values:
        return reg.modified_write_values
    for fld in reg.fields:
        if fld.modified_write_values:
            return fld.modified_write_values
    return ""


def _rmw_note(reg):
    """读-改-写（reg |= x）陷阱提示：寄存器带 clear/set 类写语义、或读时可能被硬件修改时给出。

    读语义同时看寄存器级 readAction 与字段级 readAction：后者即使寄存器级没有声明
    （或两者并存）也要提示，避免漏掉"读后清零/置位/修改"的位域。
    """
    notes = []
    semantic = _effective_write_semantics(reg)
    if semantic == "oneToClear":
        notes.append(
            "寄存器是写 1 清零（modifiedWriteValues=oneToClear）语义：读改写（reg |= x）会把读回时"
            "已置位的标志一并写回（写 1 = 清零），可能顺带清掉没提到的标志；清标志请直写目标标志"
            "（REG = <标志>）。")
    elif semantic in _RMW_SEMANTICS:
        notes.append(
            "寄存器含 %s（modifiedWriteValues=%s）语义：用 reg |= x 改其它位可能误改状态位，"
            "建议直接写完整目标值。" % (write_semantics(semantic) or semantic, semantic))
    if reg.read_action == "modifyExternal":
        notes.append(
            "寄存器的读语义是%s（readAction=modifyExternal）：读改写（reg |= x）会把读取时的"
            "外部变化一并写回，轮询与读改写需谨慎，建议直接写目标值。"
            % (read_semantics(reg.read_action) or reg.read_action))
    elif reg.read_action:
        notes.append(
            "寄存器的读语义是%s（readAction=%s）：读取时会被硬件修改，读改写（reg |= x）会把"
            "读取时的变化一并写回，轮询与读改写需谨慎，建议直接写目标值。"
            % (read_semantics(reg.read_action) or reg.read_action, reg.read_action))
    # 字段可能继承寄存器级 readAction，已在上面提示过的不再重复
    field_actions = [fld for fld in reg.fields
                     if fld.read_action and fld.read_action != reg.read_action]
    if field_actions:
        shown = "、".join("%s（%s，readAction=%s）" % (
            fld.name, read_semantics(fld.read_action) or fld.read_action, fld.read_action)
            for fld in field_actions[:3])
        more = "等 %d 个位域" % len(field_actions) if len(field_actions) > 3 else ""
        notes.append(
            "位域 %s%s 的读语义会在读取时被硬件清零/置位/修改：读改写（reg |= x）会把读回的"
            "变化一并写回，轮询与读改写需谨慎，建议直接写目标值。" % (shown, more))
    return "".join(notes) or None


def decode(device, text, value, as_write=False):
    periph, reg = resolve_register(device, text)
    size_mask = (1 << reg.size) - 1
    if value < 0 or value > size_mask:
        raise EtkError(
            E_INPUT_INVALID,
            "值 0x%X 超出 %d 位寄存器 %s.%s 的范围" % (value, reg.size, periph.name, reg.name),
            hint="寄存器宽 %d 位，取值范围 0 到 0x%X。" % (reg.size, size_mask),
        )
    covered = 0
    rows = []
    for fld in reg.fields:
        covered |= fld.mask << fld.lsb
        fv = (value >> fld.lsb) & fld.mask
        # 写视角用 usage=write 的枚举组，读视角用 usage=read 的组；缺省 usage 仍视为两组共用
        enums = fld.write_enums if as_write else fld.read_enums
        enum = next((e for e in enums
                     if not getattr(e, "is_default", False) and (fv & e.mask) == e.value), None)
        if enum is None:
            # 没有具体枚举命中时，用"默认项"（isDefault）作为兜底说明
            enum = next((e for e in enums if getattr(e, "is_default", False)), None)
        rows.append({
            "name": fld.name,
            "bits": fld.bit_text,
            "value": fv,
            "value_hex": "0x%X" % fv,
            "enum": enum.name if enum else None,
            "enum_description": enum.description if enum else "",
            "description": fld.description,
        })
    undefined = [i for i in range(reg.size) if (value >> i) & 1 and not (covered >> i) & 1]
    write_notes = []
    if as_write:
        hazard = _rmw_note(reg)
        if hazard:
            write_notes.append(hazard)
        for fld, row in zip(reg.fields, rows):
            fv = row["value"]
            reset_fv = (reg.reset_value >> fld.lsb) & fld.mask
            if fld.access == "read-only" and fv != reset_fv:
                write_notes.append("位域 %s 的访问类型是只读（read-only），写入 0x%X 不会生效" % (fld.name, fv))
            if fld.access == "read-writeOnce":
                write_notes.append("位域 %s 只能写入一次（read-writeOnce）" % fld.name)
            if fld.modified_write_values and fv:
                write_notes.append("位域 %s 写 0x%X：%s（modifiedWriteValues=%s）" % (
                    fld.name, fv, write_semantics(fld.modified_write_values), fld.modified_write_values))
        if undefined:
            write_notes.append("有 %d 个 SVD 未定义的位被置 1（bit %s），写入行为未在 SVD 中定义" % (
                len(undefined), "、".join(str(b) for b in undefined[:8]) + ("…" if len(undefined) > 8 else "")))
    return {
        "kind": "decode",
        "peripheral": periph.name,
        "base_address": hex_addr(periph.base_address),
        "register": _reg_dict(periph, reg),
        "value": value,
        "value_hex": hex_reset(value, reg.size),
        "fields": rows,
        "undefined_bits": undefined,
        "write_notes": write_notes,
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }


def list_peripherals(device):
    return {
        "kind": "list",
        "device": device.name,
        "count": len(device.peripherals),
        "peripherals": [
            {
                "name": p.name,
                "base_address": hex_addr(p.base_address),
                "derived_from": p.derived_from,
                "group": p.group_name,
                "register_count": len(p.registers),
                "description": p.description,
            }
            for p in device.peripherals
        ],
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }


def bit_ranges(bits):
    """把位号集合压缩成 [lo, hi] 区间列表，如 [1,2,4,5,6] -> [[1,2],[4,6]]。"""
    out = []
    for bit in sorted(bits):
        if out and bit == out[-1][1] + 1:
            out[-1][1] = bit
        else:
            out.append([bit, bit])
    return out


def _covered_mask(reg):
    covered = 0
    for fld in reg.fields:
        covered |= fld.mask << fld.lsb
    return covered


def _owner(fields, bit):
    for fld in fields:
        if fld.lsb <= bit < fld.lsb + fld.width:
            return fld.name
    return None


def register_fields(device, text):
    """位域速查表：位范围、宽度、掩码、访问、复位、枚举与未定义位。"""
    periph, reg = resolve_register(device, text)
    covered = _covered_mask(reg)
    undefined = [i for i in range(reg.size) if not (covered >> i) & 1]
    return {
        "kind": "fields",
        "peripheral": periph.name,
        "base_address": hex_addr(periph.base_address),
        "register": _reg_dict(periph, reg),
        "fields": [_field_dict(f, reg.reset_value, reg.size) for f in reg.fields],
        "undefined_bits": undefined,
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }


def diagram(device, text):
    """寄存器位图：每个位域取一个符号字符，未定义位用点号。"""
    periph, reg = resolve_register(device, text)
    used = set()
    legend = []
    chars = ["." for _ in range(reg.size)]
    for fld in reg.fields:
        chosen = None
        for cand in fld.name:
            up = cand.upper()
            if up.isalnum() and up not in used:
                chosen = up
                break
        if chosen is None:
            chosen = "*"
        used.add(chosen)
        legend.append({"char": chosen, "field": fld.name, "bits": fld.bit_text})
        for bit in range(fld.lsb, min(fld.lsb + fld.width, reg.size)):
            chars[bit] = chosen
    return {
        "kind": "diagram",
        "peripheral": periph.name,
        "base_address": hex_addr(periph.base_address),
        "register": _reg_dict(periph, reg),
        "cells": [
            {"bit": i, "char": chars[i], "field": _owner(reg.fields, i)}
            for i in range(reg.size)
        ],
        "legend": legend,
        "reset_bits": [i for i in range(reg.size) if (reg.reset_value >> i) & 1],
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }


def set_fields(device, text, assignments, source_value=None):
    """按位域赋值计算寄存器写入值。source_value 为 None 时以复位值为基准。

    assignments 形如 ["CEN=1", "DIR=UP"]，值可以是数字或字段的枚举名。
    """
    periph, reg = resolve_register(device, text)
    size_mask = (1 << reg.size) - 1
    if source_value is None:
        from_label = "复位值"
        initial = reg.reset_value & size_mask
    else:
        if source_value > size_mask:
            raise EtkError(
                E_INPUT_INVALID,
                "基准值 0x%X 超出 %d 位寄存器 %s.%s 的范围" % (
                    source_value, reg.size, periph.name, reg.name),
                hint="寄存器宽 %d 位，取值范围 0 到 0x%X。" % (reg.size, size_mask),
            )
        from_label = "指定值"
        initial = source_value
    value = initial
    rows = []
    notes = []
    for item in assignments:
        name, sep, raw = item.partition("=")
        name, raw = name.strip(), raw.strip()
        if not sep or not name or not raw:
            raise EtkError(
                E_INPUT_INVALID,
                "赋值 %r 格式不正确" % item,
                hint="格式为 字段=值，例如 CEN=1 或 DIR=UP。",
            )
        fld = reg.field(name)
        if fld is None:
            sugg = suggest(name, [f.name for f in reg.fields])
            hint = "可用 lookup %s.%s 查看全部位域。" % (periph.name, reg.name)
            if sugg:
                hint += "你可能要找：%s。" % "、".join(sugg)
            raise EtkError(
                E_FIELD_NOT_FOUND,
                "%s.%s 中没有位域 %s" % (periph.name, reg.name, name),
                hint=hint,
                details={"suggestions": sugg},
            )
        # 写入只认写视角枚举（usage=write / 缺省 read-write），读枚举名不应被当成写入值
        enum = next((e for e in fld.write_enums
                     if not getattr(e, "is_default", False) and e.name.upper() == raw.upper()), None)
        if enum is not None:
            fv = enum.value
        else:
            try:
                fv = parse_number(raw)
            except ValueError:
                names = "、".join(e.name for e in fld.write_enums if e.name)
                hint = "给出数字（如 0x1）"
                if names:
                    hint += "，或字段的枚举名：" + names
                raise EtkError(
                    E_INPUT_INVALID,
                    "无法解析位域 %s 的值 %r" % (fld.name, raw),
                    hint=hint + "。",
                ) from None
        if fv > fld.mask:
            raise EtkError(
                E_INPUT_INVALID,
                "值 %s 超出位域 %s 的 %d 位宽度" % (raw, fld.name, fld.width),
                hint="该位域取值范围 0 到 %d（0x%X）。" % (fld.mask, fld.mask),
            )
        before = (value >> fld.lsb) & fld.mask
        value = (value & ~(fld.mask << fld.lsb)) | (fv << fld.lsb)
        if fld.access == "read-only":
            notes.append("位域 %s 的访问类型是 read-only，写入该值可能无效" % fld.name)
        elif fld.access == "read-writeOnce":
            notes.append("位域 %s 只能写入一次（read-writeOnce）" % fld.name)
        rows.append({
            "field": fld.name,
            "bits": fld.bit_text,
            "width": fld.width,
            "given": raw,
            "value": fv,
            "value_hex": "0x%X" % fv,
            "before": before,
            "changed": before != fv,
            "via_enum": enum.name if enum else None,
        })
    covered = _covered_mask(reg)
    undefined_set = [i for i in range(reg.size) if (value >> i) & 1 and not (covered >> i) & 1]
    hazard = _rmw_note(reg)
    if hazard:
        notes.append(hazard)
    return {
        "kind": "set",
        "peripheral": periph.name,
        "base_address": hex_addr(periph.base_address),
        "register": _reg_dict(periph, reg),
        "from": {"label": from_label, "value": initial, "value_hex": hex_reset(initial, reg.size)},
        "value": value,
        "value_hex": hex_reset(value, reg.size),
        "assignments": rows,
        "undefined_bits_set": undefined_set,
        "notes": notes,
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }


def _side_resolve(device, text, side):
    try:
        return resolve_register(device, text)
    except EtkError as exc:
        raise EtkError(
            exc.code,
            "%s 侧：%s" % (side, exc.message),
            hint=exc.hint,
            details=exc.details,
        ) from None


def _enum_diff(a_enums, b_enums):
    out = []
    by_a = {e.name.upper(): e for e in a_enums if e.name}
    by_b = {e.name.upper(): e for e in b_enums if e.name}
    removed = [by_a[k].name for k in by_a if k not in by_b]
    added = [by_b[k].name for k in by_b if k not in by_a]
    if removed:
        out.append("枚举仅 A 侧有：%s" % "、".join(removed))
    if added:
        out.append("枚举仅 B 侧有：%s" % "、".join(added))
    for key in by_a:
        if key in by_b:
            ea, eb = by_a[key], by_b[key]
            if ea.value != eb.value or ea.mask != eb.mask:
                out.append("枚举 %s 值 %d → %d" % (ea.name, ea.value, eb.value))
    return out


def _diff_register_core(periph_a, reg_a, periph_b, reg_b):
    """对比两个寄存器定义，返回 {register_differences, fields, identical}，不依赖 Device。"""
    reg_diffs = []
    if periph_a.base_address != periph_b.base_address:
        reg_diffs.append("外设基地址 %s → %s" % (
            hex_addr(periph_a.base_address), hex_addr(periph_b.base_address)))
    if reg_a.offset != reg_b.offset:
        reg_diffs.append("偏移 %s → %s" % (hex_offset(reg_a.offset), hex_offset(reg_b.offset)))
    if reg_a.size != reg_b.size:
        reg_diffs.append("宽度 %d → %d" % (reg_a.size, reg_b.size))
    if reg_a.access != reg_b.access:
        reg_diffs.append("访问 %s → %s" % (reg_a.access, reg_b.access))
    if reg_a.reset_value != reg_b.reset_value:
        reg_diffs.append("复位 %s → %s" % (
            hex_reset(reg_a.reset_value, reg_a.size), hex_reset(reg_b.reset_value, reg_b.size)))
    if reg_a.modified_write_values != reg_b.modified_write_values:
        reg_diffs.append("写语义 %s → %s" % (
            write_semantics(reg_a.modified_write_values) or "无",
            write_semantics(reg_b.modified_write_values) or "无"))
    if reg_a.read_action != reg_b.read_action:
        reg_diffs.append("读语义 %s → %s" % (
            read_semantics(reg_a.read_action) or "无",
            read_semantics(reg_b.read_action) or "无"))
    fa = {f.name.upper(): f for f in reg_a.fields}
    fb = {f.name.upper(): f for f in reg_b.fields}
    order = [f.name for f in reg_a.fields]
    order += [f.name for f in reg_b.fields if f.name.upper() not in fa]
    rows = []
    for name in order:
        key = name.upper()
        item_a, item_b = fa.get(key), fb.get(key)
        if item_a is not None and item_b is None:
            rows.append({
                "name": item_a.name, "status": "only_a",
                "a": _field_dict(item_a, reg_a.reset_value, reg_a.size),
                "b": None, "differences": [],
            })
            continue
        if item_b is not None and item_a is None:
            rows.append({
                "name": item_b.name, "status": "only_b",
                "a": None,
                "b": _field_dict(item_b, reg_b.reset_value, reg_b.size),
                "differences": [],
            })
            continue
        da = _field_dict(item_a, reg_a.reset_value, reg_a.size)
        db = _field_dict(item_b, reg_b.reset_value, reg_b.size)
        diffs = []
        if da["bits"] != db["bits"]:
            diffs.append("位 %s → %s" % (da["bits"], db["bits"]))
        if da["access"] != db["access"]:
            diffs.append("访问 %s → %s" % (da["access"], db["access"]))
        if da["reset"] != db["reset"]:
            diffs.append("复位 %d → %d" % (da["reset"], db["reset"]))
        if da["modified_write_values"] != db["modified_write_values"]:
            diffs.append("写语义 %s → %s" % (
                da["write_semantics"] or "无", db["write_semantics"] or "无"))
        if da["read_action"] != db["read_action"]:
            diffs.append("读语义 %s → %s" % (
                da["read_semantics"] or "无", db["read_semantics"] or "无"))
        diffs.extend(_enum_diff(item_a.enums, item_b.enums))
        rows.append({
            "name": da["name"],
            "status": "same" if not diffs else "diff",
            "a": da,
            "b": db,
            "differences": diffs,
        })
    identical = not reg_diffs and all(r["status"] == "same" for r in rows)
    return {"register_differences": reg_diffs, "fields": rows, "identical": identical}


def diff_registers(device_a, device_b, text):
    """对比两份 SVD 中同一路径寄存器的定义差异。"""
    periph_a, reg_a = _side_resolve(device_a, text, "A")
    periph_b, reg_b = _side_resolve(device_b, text, "B")
    core = _diff_register_core(periph_a, reg_a, periph_b, reg_b)
    return {
        "kind": "diff",
        "path": "%s.%s" % (periph_a.name, reg_a.name),
        "a": {
            "peripheral": periph_a.name,
            "base_address": hex_addr(periph_a.base_address),
            "register": _reg_dict(periph_a, reg_a),
            "source": source_meta(device_a),
        },
        "b": {
            "peripheral": periph_b.name,
            "base_address": hex_addr(periph_b.base_address),
            "register": _reg_dict(periph_b, reg_b),
            "source": source_meta(device_b),
        },
        "register_differences": core["register_differences"],
        "fields": core["fields"],
        "identical": core["identical"],
        "label": LABEL_VERIFIED,
    }


def _side_periph(device, name, side):
    try:
        return _periph_or_raise(device, name)
    except EtkError as exc:
        raise EtkError(
            exc.code,
            "%s 侧：%s" % (side, exc.message),
            hint=exc.hint,
            details=exc.details,
        ) from None


def diff_peripherals(device_a, device_b, name):
    """对比两份 SVD 中同一外设的全部寄存器（升级 Pack / 移植代码时看变了什么）。"""
    periph_a = _side_periph(device_a, name, "A")
    periph_b = _side_periph(device_b, name, "B")
    by_a = {r.name.upper(): r for r in periph_a.registers}
    by_b = {r.name.upper(): r for r in periph_b.registers}
    order = [r.name for r in periph_a.registers]
    order += [r.name for r in periph_b.registers if r.name.upper() not in by_a]
    rows = []
    counts = {"total": len(order), "same": 0, "diff": 0, "only_a": 0, "only_b": 0}
    for reg_name in order:
        key = reg_name.upper()
        reg_a, reg_b = by_a.get(key), by_b.get(key)
        row = {
            "name": reg_a.name if reg_a is not None else reg_b.name,
            "status": "",
            "register_differences": [],
            "fields_changed": [],
            "fields_same": 0,
            "fields_only_a": [],
            "fields_only_b": [],
        }
        if reg_a is not None and reg_b is None:
            row["status"] = "only_a"
        elif reg_b is not None and reg_a is None:
            row["status"] = "only_b"
        else:
            core = _diff_register_core(periph_a, reg_a, periph_b, reg_b)
            row["register_differences"] = core["register_differences"]
            row["fields_changed"] = [
                {"name": f["name"], "differences": f["differences"]}
                for f in core["fields"] if f["status"] == "diff"
            ]
            row["fields_same"] = sum(1 for f in core["fields"] if f["status"] == "same")
            row["fields_only_a"] = [f["name"] for f in core["fields"] if f["status"] == "only_a"]
            row["fields_only_b"] = [f["name"] for f in core["fields"] if f["status"] == "only_b"]
            row["status"] = "same" if core["identical"] else "diff"
        counts[row["status"]] += 1
        rows.append(row)
    base_changed = periph_a.base_address != periph_b.base_address
    identical = (not base_changed and counts["diff"] == 0
                 and counts["only_a"] == 0 and counts["only_b"] == 0)
    return {
        "kind": "diff_peripheral",
        "path": periph_a.name,
        "a": {
            "name": periph_a.name,
            "base_address": hex_addr(periph_a.base_address),
            "register_count": len(periph_a.registers),
            "source": source_meta(device_a),
        },
        "b": {
            "name": periph_b.name,
            "base_address": hex_addr(periph_b.base_address),
            "register_count": len(periph_b.registers),
            "source": source_meta(device_b),
        },
        "base_address_changed": base_changed,
        "counts": counts,
        "registers": rows,
        "identical": identical,
        "label": LABEL_VERIFIED,
    }


def find_in_range(device, start, end, limit=200):
    """列出起始地址落在 [start, end] 区间内的寄存器（按地址排序）。"""
    if start > end:
        raise EtkError(
            E_INPUT_INVALID,
            "区间起点 0x%X 大于终点 0x%X" % (start, end),
            hint="用法：range <起始地址> <结束地址>，如 range 0x40013800 0x40013FFF。",
        )
    hits = []
    for periph in device.peripherals:
        for reg in periph.registers:
            addr = periph.base_address + reg.offset
            if start <= addr <= end:
                hits.append((addr, periph, reg))
    hits.sort(key=lambda item: item[0])
    matches = [
        {
            "path": "%s.%s" % (periph.name, reg.name),
            "address": hex_addr(addr),
            "offset": hex_offset(reg.offset),
            "size": reg.size,
            "access": reg.access,
            "reset": hex_reset(reg.reset_value, reg.size),
            "description": reg.description,
        }
        for addr, periph, reg in hits[:limit]
    ]
    return {
        "kind": "range",
        "start": hex_addr(start),
        "end": hex_addr(end),
        "count": len(hits),
        "truncated": len(hits) > limit,
        "registers": matches,
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }


def device_info(device):
    """SVD 元信息与统计：厂商、CPU、各层级数量、文件哈希（可追溯出处）。"""
    registers = 0
    fields = 0
    enums = 0
    interrupts = 0
    derived = 0
    for periph in device.peripherals:
        if periph.derived_from:
            derived += 1
        interrupts += len(periph.interrupts)
        for reg in periph.registers:
            registers += 1
            fields += len(reg.fields)
            for fld in reg.fields:
                enums += len(fld.enums)
    try:
        size = os.path.getsize(device.path)
        mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(device.path)))
        digest = _sha256(device.path)
    except OSError as exc:
        raise EtkError(
            E_SVD_NOT_FOUND,
            "无法读取 SVD 文件：%s（%s）" % (device.path, exc.strerror or exc),
            hint="文件可能已被移动或删除。",
        ) from None
    return {
        "kind": "info",
        "device": device.name,
        "vendor": device.vendor,
        "cpu": device.cpu,
        "description": device.description,
        "file_size": size,
        "mtime": mtime,
        "sha256": digest,
        "counts": {
            "peripherals": len(device.peripherals),
            "derived_peripherals": derived,
            "registers": registers,
            "fields": fields,
            "enums": enums,
            "interrupts": interrupts,
            "warnings": len(device.warnings),
        },
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _comment_safe(text):
    """避免描述文本提前结束 C 注释。"""
    return (text or "").replace("*/", "* /")


def _macro_sanitize(name):
    out = []
    for ch in name:
        out.append(ch if (ch.isalnum() or ch == "_") else "_")
    return "".join(out).upper()


def _nvic_register(nvic, stem, index):
    names = ["%s%d" % (stem, index)]
    if index == 0:
        names.append(stem)  # 部分 SVD（如 GD32）不分段，只有 ISER
    for name in names:
        reg = nvic.register(name)
        if reg is not None:
            return reg
    return None


def _nvic_slot(device, value):
    """中断号的 NVIC 使能/清挂起寄存器（SVD 里有 NVIC 时），否则 None。"""
    nvic = device.peripheral("NVIC")
    if nvic is None:
        return None
    index, bit = value // 32, value % 32
    hint = {}
    enable = _nvic_register(nvic, "ISER", index)
    if enable is not None:
        hint["enable"] = {
            "register": "NVIC.%s" % enable.name,
            "bit": bit,
            "address": hex_addr(nvic.base_address + enable.offset),
        }
    clear = _nvic_register(nvic, "ICPR", index)
    if clear is not None:
        hint["clear_pending"] = {
            "register": "NVIC.%s" % clear.name,
            "bit": bit,
            "address": hex_addr(nvic.base_address + clear.offset),
        }
    # 优先级字节：每个中断占 IPR 的 1 字节（IPR 寄存器按 4 个中断一组）
    prio = _nvic_register(nvic, "IPR", value // 4)
    if prio is None:
        prio = _nvic_register(nvic, "IP", value // 4)
    if prio is not None:
        hint["priority"] = {
            "register": "NVIC.%s" % prio.name,
            "byte": value % 4,
            "bit_offset": (value % 4) * 8,
            "address": hex_addr(nvic.base_address + prio.offset),
        }
    return hint or None


def find_interrupts(device, query=None, limit=100):
    """查中断号：给数字按号精确匹配，给文字按名称/外设/描述子串匹配；不给则列出全部。"""
    entries = []
    nvic_cache = {}
    for periph in device.peripherals:
        for item in periph.interrupts:
            if item.value not in nvic_cache:
                nvic_cache[item.value] = _nvic_slot(device, item.value)
            entries.append({
                "value": item.value,
                "peripheral": periph.name,
                "name": item.name,
                "description": item.description,
                "nvic": nvic_cache[item.value],
            })
    entries.sort(key=lambda e: (e["value"], e["peripheral"], e["name"]))
    text = (query or "").strip()
    if not text:
        matched = entries
    else:
        try:
            number = parse_number(text)
        except ValueError:
            key = text.lower()
            matched = [
                e for e in entries
                if key in e["name"].lower()
                or key in e["peripheral"].lower()
                or key in (e["description"] or "").lower()
            ]
        else:
            matched = [e for e in entries if e["value"] == number]
    return {
        "kind": "irq",
        "query": text or None,
        "total": len(matched),
        "truncated": len(matched) > limit,
        "matches": matched[:limit],
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }


def macros_for(device, text, generator=None):
    """生成 CMSIS 风格的参考宏：外设/寄存器/位域均可，含出处头注释。"""
    parts = split_query(text)
    periph = _periph_or_raise(device, parts[0])
    res = lookup(device, text)
    field_sel = None
    if res["kind"] == "peripheral":
        regs = list(periph.registers)
    elif res["kind"] == "register":
        regs = [periph.register(res["register"]["name"])]
    elif res["kind"] == "field":
        regs = [periph.register(res["register"]["name"])]
        field_sel = regs[0].field(res["field"]["name"])
    else:  # cluster
        regs = [periph.register(item["name"]) for item in res["registers"]]
    src = source_meta(device)
    try:
        short_hash = _sha256(device.path)[:12]
    except OSError:
        short_hash = "?"
    lines = [
        "/* 由 %s 生成；来源：%s（设备 %s，版本 %s，sha256 前缀 %s） */" % (
            _comment_safe(generator or "embedded-register-lookup"),
            _comment_safe(src["file"]), _comment_safe(src["device"]),
            _comment_safe(src["version"]), short_hash),
        "/* 宏名含外设实例名（%s_...）；厂商头文件常用外设类型名，对照时注意命名差异。 */" % periph.name,
    ]
    entries = []
    for reg in regs:
        prefix = _macro_sanitize("%s_%s" % (periph.name, reg.name))
        addr = periph.base_address + reg.offset
        lines.append("")
        reg_desc = _comment_safe(reg.description)
        lines.append("/* %s */" % (
            ("%s: %s" % (reg.name, reg_desc)) if reg_desc and reg_desc != reg.name else reg.name))
        lines.append("#define %s_OFFSET %sUL" % (prefix, hex_offset(reg.offset)))
        lines.append("#define %s_ADDR %sUL" % (prefix, hex_addr(addr)))
        fields = []
        for fld in reg.fields:
            if field_sel is not None and fld.name != field_sel.name:
                continue
            fprefix = "%s_%s" % (prefix, _macro_sanitize(fld.name))
            fld_desc = _comment_safe(fld.description)
            lines.append("/* %s（位 %s） */" % (
                ("%s: %s" % (fld.name, fld_desc)) if fld_desc and fld_desc != fld.name else fld.name,
                fld.bit_text))
            lines.append("#define %s_Pos %dU" % (fprefix, fld.lsb))
            lines.append("#define %s_Msk (0x%XUL << %s_Pos)" % (fprefix, fld.mask, fprefix))
            enums = []
            for enum in fld.enums:
                if not enum.name:
                    continue
                if getattr(enum, "is_default", False):
                    lines.append("/* 默认项 %s：其余取值（不生成宏） */" % enum.name)
                    continue
                if enum.mask == fld.mask:
                    macro = "%s_%s" % (fprefix, _macro_sanitize(enum.name))
                    lines.append("#define %s 0x%XU" % (macro, enum.value))
                    enums.append({"name": enum.name, "value": enum.value, "macro": macro})
                else:
                    lines.append("/* 枚举 %s 含任意位（模式 %s），未生成宏 */" % (
                        enum.name, _pattern(enum.value, enum.mask, fld.width)))
            fields.append({
                "name": fld.name,
                "bits": fld.bit_text,
                "pos": fld.lsb,
                "msk": hex_mask(fld.mask << fld.lsb, reg.size),
                "macros": {"pos": "%s_Pos" % fprefix, "msk": "%s_Msk" % fprefix},
                "enums": enums,
            })
        entries.append({
            "name": reg.name,
            "offset": hex_offset(reg.offset),
            "address": hex_addr(addr),
            "macros": {"offset": "%s_OFFSET" % prefix, "address": "%s_ADDR" % prefix},
            "fields": fields,
        })
    return {
        "kind": "macros",
        "peripheral": periph.name,
        "path": text.strip(),
        "registers": entries,
        "code": "\n".join(lines),
        "label": LABEL_VERIFIED,
        "source": src,
    }


_LINT_SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


def lint(device, peripheral=None, limit=200):
    """SVD 质量检查：寄存器/位域重叠、越界、重复名，复位值超宽与中断号冲突。

    只做从 SVD 自身数据就能判定的检查，不需要任何外部信息。
    """
    if peripheral:
        periphs = [_periph_or_raise(device, peripheral)]
    else:
        periphs = device.peripherals
    findings = []

    def add(severity, code, message, periph, register=None, field=None):
        findings.append({
            "severity": severity,
            "code": code,
            "peripheral": periph.name,
            "register": register.name if register is not None else None,
            "field": field.name if field is not None else None,
            "message": message,
        })

    irq_names = {}
    for periph in periphs:
        regs = sorted(periph.registers, key=lambda r: r.offset)
        seen_reg = {}
        for reg in regs:
            key = reg.name.upper()
            if key in seen_reg:
                add("error", "duplicate_register",
                    "%s 中寄存器 %s 定义了两次（偏移 %s 与 %s）" % (
                        periph.name, reg.name, hex_offset(seen_reg[key].offset), hex_offset(reg.offset)),
                    periph, reg)
            else:
                seen_reg[key] = reg
            if reg.reset_value >> reg.size:
                add("error", "reset_out_of_range",
                    "%s.%s 的复位值 %s 超出 %d 位宽度" % (
                        periph.name, reg.name, hex_reset(reg.reset_value, reg.size), reg.size),
                    periph, reg)
            seen_field = {}
            for fld in reg.fields:
                fkey = fld.name.upper()
                if fkey in seen_field:
                    add("error", "duplicate_field",
                        "%s.%s 中位域 %s 定义了两次" % (periph.name, reg.name, fld.name),
                        periph, reg, fld)
                else:
                    seen_field[fkey] = fld
                if fld.msb >= reg.size:
                    add("error", "field_out_of_range",
                        "%s.%s.%s 位 %s（宽 %d）超出 %d 位寄存器范围" % (
                            periph.name, reg.name, fld.name, fld.bit_text, fld.width, reg.size),
                        periph, reg, fld)
            fields = sorted(reg.fields, key=lambda f: (f.lsb, -f.width))
            # 按位区间扫描：只比较"后面还想跟前面重叠"的项，宽位域覆盖多个后续项时不会漏报。
            for index, first in enumerate(fields):
                for later in fields[index + 1:]:
                    if later.lsb > first.msb:
                        break
                    if later.msb <= first.msb:
                        # 后一个位域完全落在前一个里：同一位置的多宽度视图/别名（常见厂商写法）
                        add("info", "field_alias",
                            "%s.%s 中位域 %s（位 %s）与 %s（位 %s）是同一位置的视图/别名（常见写法）" % (
                                periph.name, reg.name, first.name, first.bit_text,
                                later.name, later.bit_text),
                            periph, reg, later)
                    else:
                        add("error", "field_overlap",
                            "%s.%s 中位域 %s（位 %s）与 %s（位 %s）部分重叠" % (
                                periph.name, reg.name, first.name, first.bit_text,
                                later.name, later.bit_text),
                            periph, reg, later)
        # 寄存器按地址区间扫描：宽寄存器覆盖多个后续寄存器时逐对报告，不只比较相邻项。
        for index, first in enumerate(regs):
            for later in regs[index + 1:]:
                if later.offset >= first.offset + first.nbytes:
                    break
                if first.offset == later.offset:
                    add("info", "register_alias",
                        "%s 中 %s 与 %s 使用同一偏移 %s（同一寄存器的不同视图或别名，属常见写法；按需选用）" % (
                            periph.name, first.name, later.name, hex_offset(first.offset)),
                        periph, later)
                elif later.offset + later.nbytes <= first.offset + first.nbytes:
                    # 后一个寄存器完全落在前一个里：同一位置的多宽度视图（32/16/8 位视图等）
                    add("info", "register_view",
                        "%s 中 %s（偏移 %s，%d 字节）与 %s（偏移 %s，%d 字节）是同一位置的视图/别名（常见写法）" % (
                            periph.name, first.name, hex_offset(first.offset), first.nbytes,
                            later.name, hex_offset(later.offset), later.nbytes),
                        periph, later)
                else:
                    add("error", "register_overlap",
                        "%s 中寄存器 %s（偏移 %s，%d 字节）与 %s（偏移 %s）地址区域部分重叠（不构成包含关系）" % (
                            periph.name, first.name, hex_offset(first.offset), first.nbytes,
                            later.name, hex_offset(later.offset)),
                        periph, later)
        for item in periph.interrupts:
            key = item.name.upper()
            if key in irq_names and irq_names[key][1] != item.value:
                previous = irq_names[key]
                add("warning", "interrupt_value_conflict",
                    "中断 %s 的向量号不一致：%s 中是 %d，%s 中是 %d" % (
                        item.name, previous[0].name, previous[1], periph.name, item.value),
                    periph)
            else:
                irq_names.setdefault(key, (periph, item.value))

    findings.sort(key=lambda f: (
        _LINT_SEVERITY_ORDER.get(f["severity"], 9), f["code"],
        f["peripheral"], f["register"] or "", f["field"] or ""))
    errors = sum(1 for f in findings if f["severity"] == "error")
    warnings = sum(1 for f in findings if f["severity"] == "warning")
    infos = len(findings) - errors - warnings
    return {
        "kind": "lint",
        "device": device.name,
        "scope": peripheral or None,
        "counts": {"error": errors, "warning": warnings, "info": infos, "total": len(findings)},
        "truncated": len(findings) > limit,
        "findings": findings[:limit],
        "label": LABEL_VERIFIED,
        "source": source_meta(device),
    }
