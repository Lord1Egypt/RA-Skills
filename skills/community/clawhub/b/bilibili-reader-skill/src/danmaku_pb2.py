"""B站弹幕protobuf解析 — 纯二进制解析，不依赖protobuf库"""

from dataclasses import dataclass


@dataclass
class Danmaku:
    content: str
    send_time: float  # 秒


def parse_danmaku_protobuf(data: bytes, limit: int = 50) -> list[Danmaku]:
    """解析B站弹幕protobuf二进制数据

    DmSegMobileReply 结构:
      repeated DanmakuElem elems = 1;

    DanmakuElem 结构:
      int64 id = 1;
      int32 progress = 2;  (毫秒)
      bytes content = 11;
    """
    danmakus = []
    pos = 0

    while pos < len(data) and len(danmakus) < limit:
        # 读取外层tag (field=1, wire_type=2)
        tag, pos = _read_varint(data, pos)
        if tag is None:
            break
        field_num = tag >> 3
        wire_type = tag & 0x07

        if wire_type == 0:  # varint
            _, pos = _read_varint(data, pos)
        elif wire_type == 2:  # length-delimited
            length, pos = _read_varint(data, pos)
            if length is None or pos + length > len(data):
                break
            if field_num == 1:  # elems
                elem = _parse_elem(data[pos:pos + length])
                if elem:
                    danmakus.append(elem)
            pos += length
        elif wire_type == 5:  # 32-bit
            pos += 4
        elif wire_type == 1:  # 64-bit
            pos += 8
        else:
            break

    return danmakus


def _read_varint(data: bytes, pos: int) -> tuple[int, int]:
    """读取varint，返回 (value, new_pos)"""
    value = 0
    shift = 0
    while pos < len(data):
        b = data[pos]
        pos += 1
        value |= (b & 0x7F) << shift
        shift += 7
        if not (b & 0x80):
            return value, pos
    return None, pos


def _parse_elem(data: bytes) -> Danmaku:
    """解析单个DanmakuElem"""
    content = None
    progress = 0
    pos = 0

    while pos < len(data):
        tag, pos = _read_varint(data, pos)
        if tag is None:
            break
        field_num = tag >> 3
        wire_type = tag & 0x07

        if wire_type == 0:  # varint
            value, pos = _read_varint(data, pos)
            if value is not None and field_num == 2:
                progress = value
        elif wire_type == 2:  # length-delimited
            length, pos = _read_varint(data, pos)
            if length is None:
                break
            if field_num == 11 and pos + length <= len(data):
                try:
                    content = data[pos:pos + length].decode("utf-8")
                except UnicodeDecodeError:
                    pass
            pos += length
        elif wire_type == 5:
            pos += 4
        elif wire_type == 1:
            pos += 8
        else:
            break

    if content and len(content) > 1:
        return Danmaku(content=content, send_time=progress / 1000.0)
    return None
