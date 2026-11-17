#!/usr/bin/env python3
"""
嵌入式 OTA / Bootloader 升级工具集 - 镜像头 · CRC · 分区表 · 打包校验

与 ota_audit.py（链路静态审计）配套：audit 负责"查代码有没有雷"，
本工具负责"把固件做成可升级的包"。

设计取向：面向 Cortex-M 裸机 + 国产 MCU（GD32/CH32/APM32 等），
不依赖 Zephyr / MCUboot / imgtool 那套成熟生态——那些场景用户直接用它即可。

功能：
  - crc       : 计算 CRC32（zlib 兼容）/ CRC16-CCITT / MD5 / SHA256
  - header    : 生成 64 字节 OTA 镜像头（二进制 + 配套 .h）
  - layout    : 分区表计算器，校验溢出并生成 .h
  - pack      : 固件 bin + 镜像头 → 升级包 .pkg
  - verify    : 校验升级包（解头、验头 CRC、验镜像 CRC、验大小/地址合法性）

镜像头格式（小端，固定 64 字节）：
  偏移  类型     字段          说明
  0     uint32   magic         0x50555746（小端存储即 ASCII "FWUP"）
  4     uint16   header_ver    头格式版本（当前 1）
  6     uint16   hw_id         硬件标识（防串板）
  8     uint32   fw_ver        固件版本 (major<<16 | minor<<8 | patch)
  12    uint32   load_addr     镜像加载地址（flash 内绝对地址）
  16    uint32   image_size    镜像字节数
  20    uint32   image_crc     镜像 CRC32
  24    uint32   header_crc    本头 CRC32（计算时本字段置 0）
  28    uint32   timestamp     打包 UTC 时间戳
  32    uint32   flags         位0=强制升级 位1=允许降级（默认都不置）
  36    uint8[28] reserved     保留，全 0
  合计 64 字节

退出码：0=成功、1=校验不通过、2=用法/内部错误
"""

import argparse
import binascii
import hashlib
import json
import os
import re
import struct
import sys
import time
import zlib

MAGIC = 0x50555746  # 小端存储字节即 46 57 55 50 = ASCII "FWUP"
HEADER_VER = 1
HEADER_SIZE = 64
HEADER_STRUCT = struct.Struct("<IHHIIIIIII28s")  # 8+4*8+28 = 64
HEADER_FIELDS = (
    "magic", "header_ver", "hw_id", "fw_ver", "load_addr",
    "image_size", "image_crc", "header_crc", "timestamp", "flags", "reserved",
)


# --------------------------------------------------------------------------
# CRC / 摘要
# --------------------------------------------------------------------------

def crc32(data: bytes) -> int:
    """标准 CRC32（IEEE 802.3，zlib 兼容），嵌入式常用初值 0xFFFFFFFF + 异或输出。"""
    return zlib.crc32(data) & 0xFFFFFFFF


def crc16_ccitt(data: bytes, init: int = 0xFFFF) -> int:
    """CRC16-CCITT-FALSE（poly 0x1021，初值 0xFFFF，不反转）。"""
    crc = init
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if (crc & 0x8000) else (crc << 1) & 0xFFFF
    return crc


def crc16_modbus(data: bytes, init: int = 0xFFFF) -> int:
    """CRC16-MODBUS（poly 0x8005 反射，用于 RS485 场景）。"""
    crc = init
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if (crc & 1) else crc >> 1
    return crc & 0xFFFF


def digest_of(path: str) -> dict:
    data = open(path, "rb").read()
    return {
        "file": os.path.basename(path),
        "size": len(data),
        "crc32": f"0x{crc32(data):08X}",
        "crc16_ccitt": f"0x{crc16_ccitt(data):04X}",
        "crc16_modbus": f"0x{crc16_modbus(data):04X}",
        "md5": hashlib.md5(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


# --------------------------------------------------------------------------
# 镜像头
# --------------------------------------------------------------------------

def encode_version(text: str) -> int:
    """'1.2.3' → 0x00010203；兼容单段 '5' → 0x00000500。"""
    parts = [int(p) for p in str(text).split(".")]
    while len(parts) < 3:
        parts.append(0)
    major, minor, patch = parts[0], parts[1], parts[2]
    for name, value in (("major", major), ("minor", minor), ("patch", patch)):
        if not 0 <= value <= 255:
            raise ValueError(f"版本段 {name}={value} 超出 0-255")
    return (major << 16) | (minor << 8) | patch


def decode_version(value: int) -> str:
    return f"{(value >> 16) & 0xFF}.{(value >> 8) & 0xFF}.{value & 0xFF}"


def build_header(image: bytes, load_addr: int, fw_version: str = "1.0.0",
                 hw_id: int = 0, flags: int = 0, timestamp: int = None) -> bytes:
    """构造 64 字节镜像头。header_crc 为头自身 CRC32（计算时该字段置 0）。"""
    ts = int(time.time()) if timestamp is None else int(timestamp)
    body = HEADER_STRUCT.pack(
        MAGIC, HEADER_VER, hw_id & 0xFFFF, encode_version(fw_version),
        load_addr & 0xFFFFFFFF, len(image), crc32(image),
        0, ts, flags & 0xFFFFFFFF, b"\x00" * 28,
    )
    header_crc = crc32(body)
    return HEADER_STRUCT.pack(
        MAGIC, HEADER_VER, hw_id & 0xFFFF, encode_version(fw_version),
        load_addr & 0xFFFFFFFF, len(image), crc32(image),
        header_crc, ts, flags & 0xFFFFFFFF, b"\x00" * 28,
    )


def parse_header(blob: bytes) -> dict:
    """解析镜像头，返回字段字典（含版本字符串与 magic 合法性）。"""
    if len(blob) < HEADER_SIZE:
        raise ValueError(f"数据不足一个镜像头：{len(blob)} < {HEADER_SIZE}")
    values = HEADER_STRUCT.unpack(blob[:HEADER_SIZE])
    info = dict(zip(HEADER_FIELDS, values))
    info["magic_ok"] = info["magic"] == MAGIC
    info["magic_str"] = struct.pack("<I", info["magic"]).decode("ascii", "replace")
    info["fw_version_str"] = decode_version(info["fw_ver"])
    info["flags_force_upgrade"] = bool(info["flags"] & 0x1)
    info["flags_allow_downgrade"] = bool(info["flags"] & 0x2)
    info.pop("reserved")
    return info


def header_crc_check(blob: bytes) -> bool:
    """重算头 CRC（header_crc 字段清零）并与存储值比对。"""
    stored = HEADER_STRUCT.unpack(blob[:HEADER_SIZE])[7]
    zeroed = bytearray(blob[:HEADER_SIZE])
    zeroed[24:28] = b"\x00\x00\x00\x00"
    return crc32(bytes(zeroed)) == stored


def header_to_c(info: dict, guard: str = "OTA_IMAGE_HEADER_H") -> str:
    """生成 MCU 侧可用的 .h（结构体 + 字段偏移宏 + magic）。"""
    force = 1 if info.get("flags_force_upgrade") else 0
    allow_down = 1 if info.get("flags_allow_downgrade") else 0
    return f"""/* 自动生成 by ota_tool.py —— 勿手改
 * OTA 镜像头定义，固定 {HEADER_SIZE} 字节，小端。
 * 解析侧务必用 OTA_HEADER_SIZE 做长度校验，不要 sizeof(结构体)（对齐会变）。 */
#ifndef {guard}
#define {guard}

#include <stdint.h>

#define OTA_IMAGE_MAGIC      0x{MAGIC:08X}u  /* "{struct.pack('<I', MAGIC).decode()}" */
#define OTA_HEADER_VERSION   {HEADER_VER}u
#define OTA_HEADER_SIZE      {HEADER_SIZE}u

/* 示例包信息（本次打包时的取值，仅供对照，不要写死到业务代码） */
#define OTA_SAMPLE_HW_ID     {info['hw_id']}u
#define OTA_SAMPLE_FW_VER    0x{info['fw_ver']:08X}u   /* {info['fw_version_str']} */
#define OTA_SAMPLE_LOAD_ADDR 0x{info['load_addr']:08X}u
#define OTA_SAMPLE_IMAGE_SIZE {info['image_size']}u
#define OTA_SAMPLE_IMAGE_CRC  0x{info['image_crc']:08X}u
#define OTA_SAMPLE_FLAGS     {info['flags']}u   /* force={force} allow_downgrade={allow_down} */

typedef struct {{
    uint32_t magic;        /*!< OTA_IMAGE_MAGIC */
    uint16_t header_ver;   /*!< 头格式版本 */
    uint16_t hw_id;        /*!< 硬件标识，防串板 */
    uint32_t fw_ver;       /*!< major<<16 | minor<<8 | patch */
    uint32_t load_addr;    /*!< 镜像应写入的 flash 地址 */
    uint32_t image_size;   /*!< 镜像字节数（不含头） */
    uint32_t image_crc;    /*!< 镜像 CRC32 */
    uint32_t header_crc;   /*!< 本头 CRC32（计算时该字段置 0） */
    uint32_t timestamp;    /*!< 打包 UTC 时间戳 */
    uint32_t flags;        /*!< bit0=强制升级 bit1=允许降级 */
    uint8_t  reserved[28]; /*!< 保留，全 0 */
}} ota_image_header_t;

#endif /* {guard} */
"""


# --------------------------------------------------------------------------
# 分区表
# --------------------------------------------------------------------------

def parse_size(text) -> int:
    """'256K' / '1M' / '4096' / '0x8000' → 字节数。"""
    if isinstance(text, int):
        return text
    s = str(text).strip().upper().replace(" ", "")
    mult = 1
    if s.endswith("K"):
        mult, s = 1024, s[:-1]
    elif s.endswith("M"):
        mult, s = 1024 * 1024, s[:-1]
    return int(s or "0", 0) * mult


def format_size(value: int) -> str:
    if value and value % (1024 * 1024) == 0:
        return f"{value // (1024 * 1024)}M"
    if value and value % 1024 == 0:
        return f"{value // 1024}K"
    return str(value)


RE_C_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def build_layout(flash_size: int, parts: list, align: int = 0x800) -> dict:
    """按顺序排布分区，返回 {regions, overflow, warnings}。
    parts: [(name, size), ...]，名字需为合法 C 标识符（数字开头、连字符等
    会在生成的 .h 里产生非法宏名，gcc 直接编译不过，必须在这里拦下）。"""
    regions, offset, warnings = [], 0, []
    for name, size in parts:
        if not RE_C_IDENTIFIER.match(name):
            raise ValueError(f"分区名不合法：{name}（需 C 标识符：字母/下划线开头，仅含字母数字下划线）")
        if align > 1:
            if offset % align:
                pad = align - (offset % align)
                warnings.append(f"分区 {name} 起始 0x{offset:X} 未对齐 {format_size(align)}，已前移 {pad} 字节")
                offset += pad
            if size % align:
                warnings.append(f"分区 {name} 大小 {format_size(size)} 非 {format_size(align)} 整数倍，"
                                f"擦写页边界可能跨区（建议向上取整到 {format_size(align)}）")
        regions.append({"name": name, "start": offset, "size": size, "end": offset + size - 1})
        offset += size
    return {
        "flash_size": flash_size,
        "align": align,
        "regions": regions,
        "used": offset,
        "free": flash_size - offset,
        "overflow": offset > flash_size,
        "warnings": warnings,
    }


def layout_to_c(layout: dict, guard: str = "OTA_PARTITION_H") -> str:
    """生成分区表 .h（地址宏 + 结构体表 + 编译期越界断言）。"""
    lines = [
        "/* 自动生成 by ota_tool.py —— 勿手改",
        " * flash 分区表。修改布局请改脚本参数重生成，不要手改本文件。 */",
        f"#ifndef {guard}",
        f"#define {guard}",
        "",
        "#include <stdint.h>",
        "",
        f"#define FLASH_BASE_ADDR     0x08000000u",
        f"#define FLASH_TOTAL_SIZE    {format_size(layout['flash_size'])}u   /* {layout['flash_size']} bytes */",
        "",
    ]
    for r in layout["regions"]:
        up = r["name"].upper()
        lines.append(f"/* {r['name']}: 0x{r['start']:08X} - 0x{r['end']:08X} ({format_size(r['size'])}) */")
        lines.append(f"#define {up}_ADDR     (FLASH_BASE_ADDR + 0x{r['start']:08X}u)")
        lines.append(f"#define {up}_OFFSET   0x{r['start']:08X}u")
        lines.append(f"#define {up}_SIZE     {format_size(r['size'])}u")
        lines.append("")
    lines += [
        "typedef struct {",
        "    const char *name;",
        "    uint32_t    offset;  /*!< 相对 FLASH_BASE_ADDR */",
        "    uint32_t    size;",
        "} ota_region_t;",
        "",
        "static const ota_region_t OTA_PARTITION_TABLE[] = {",
    ]
    for r in layout["regions"]:
        lines.append(f'    {{ "{r["name"]}", 0x{r["start"]:08X}u, {format_size(r["size"])}u }},')
    lines += [
        "};",
        f"#define OTA_PARTITION_COUNT  {len(layout['regions'])}u",
        "",
    ]
    if layout["overflow"]:
        lines.append(f'/* 警告：布局溢出 flash {layout["free"]} 字节，本文件不可用！ */')
    else:
        lines += [
            "/* 编译期总占用校验：使用本表的代码会在此处报错说明布局超了 flash */",
            "typedef char ota_layout_must_fit_flash[",
            f"    ({layout['used']}u <= {layout['flash_size']}u) ? 1 : -1];",
            "",
        ]
    lines.append(f"#endif /* {guard} */")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# 打包 / 校验
# --------------------------------------------------------------------------

def pack_firmware(bin_path: str, out_path: str, load_addr: int,
                  fw_version: str = "1.0.0", hw_id: int = 0,
                  flags: int = 0, emit_header: bool = False) -> dict:
    """bin + 头 → .pkg。返回结果字典（含校验信息）。"""
    image = open(bin_path, "rb").read()
    if not image:
        raise ValueError(f"固件为空：{bin_path}")
    header = build_header(image, load_addr, fw_version, hw_id, flags)
    pkg = header + image
    with open(out_path, "wb") as fp:
        fp.write(pkg)
    result = {
        "package": os.path.basename(out_path),
        "package_size": len(pkg),
        "image": os.path.basename(bin_path),
        "image_size": len(image),
        "load_addr": f"0x{load_addr:08X}",
        "fw_version": fw_version,
        "hw_id": hw_id,
        "image_crc32": f"0x{crc32(image):08X}",
    }
    if emit_header:
        h_path = os.path.splitext(out_path)[0] + "_header.h"
        info = parse_header(header)
        with open(h_path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(header_to_c(info))
        result["header_h"] = os.path.basename(h_path)
    return result


def verify_package(pkg_path: str, expect_hw_id: int = None,
                   expect_addr: int = None) -> dict:
    """校验升级包：头 CRC → magic → 镜像 CRC → 大小自洽 → 可选板型/地址比对。"""
    blob = open(pkg_path, "rb").read()
    errors, warnings = [], []
    if len(blob) < HEADER_SIZE:
        return {"ok": False, "errors": [f"文件不足一个头（{len(blob)} < {HEADER_SIZE}）"], "warnings": []}

    header_blob, image = blob[:HEADER_SIZE], blob[HEADER_SIZE:]
    if not header_crc_check(header_blob):
        errors.append("镜像头 CRC 校验失败（头被改坏，或写入时未按 64 字节对齐）")
    try:
        info = parse_header(header_blob)
    except ValueError as exc:
        return {"ok": False, "errors": errors + [str(exc)], "warnings": []}

    if not info["magic_ok"]:
        errors.append(f"magic 错误：0x{info['magic']:08X}（期望 0x{MAGIC:08X}）")
    if info["header_ver"] != HEADER_VER:
        warnings.append(f"头格式版本 {info['header_ver']} 非当前工具版本 {HEADER_VER}，解析侧需兼容")
    if info["image_size"] != len(image):
        errors.append(f"镜像大小不符：头声明 {info['image_size']}，实际 {len(image)}")
    if crc32(image) != info["image_crc"]:
        errors.append(f"镜像 CRC 不符：头声明 0x{info['image_crc']:08X}，实算 0x{crc32(image):08X}")
    if info["load_addr"] == 0:
        errors.append("加载地址为 0——未填 load_addr，烧进去必然跑飞")
    elif not (0x08000000 <= info["load_addr"] <= 0x081FFFFF):
        # Cortex-M 系 flash 常见映射 0x08000000-0x081FFFFF（STM32 最大 2MB）。
        # ESP32/nRF 地址不在此区间，属提示不拦包（工具侧平台无关）。
        warnings.append(f"加载地址 0x{info['load_addr']:08X} 不在 Cortex-M 常见 flash 区间 "
                        f"0x08000000-0x081FFFFF——若目标平台是 nRF/ESP32 等请忽略，"
                        f"若是 STM32/GD32 系则大概率填错，烧进去必然跑飞")
    if expect_hw_id is not None and info["hw_id"] != expect_hw_id:
        errors.append(f"硬件标识不符：包 hw_id={info['hw_id']}，期望 {expect_hw_id}（防串板校验）")
    if expect_addr is not None and info["load_addr"] != expect_addr:
        errors.append(f"加载地址不符：包 0x{info['load_addr']:08X}，期望 0x{expect_addr:08X}")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "header": info,
        "image_size_actual": len(image),
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _print_json(obj: dict) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="ota_tool.py",
        description="嵌入式 OTA/Bootloader 升级工具集 1.0.0——镜像头、CRC、分区表、打包校验",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例：
  python ota_tool.py crc firmware.bin
  python ota_tool.py layout --flash 256K --align 2K boot:32K app:96K app_bak:96K cfg:8K
  python ota_tool.py pack app.bin -o app.pkg --addr 0x08008000 --ver 1.2.3 --hw-id 0x0001
  python ota_tool.py verify app.pkg --hw-id 0x0001 --addr 0x08008000
""",
    )
    sub = parser.add_subparsers(dest="cmd")

    p_crc = sub.add_parser("crc", help="计算 CRC32/CRC16/MD5/SHA256")
    p_crc.add_argument("file")

    p_layout = sub.add_parser("layout", help="计算分区表并生成 .h")
    p_layout.add_argument("--flash", required=True, help="flash 总大小，如 256K / 1M")
    p_layout.add_argument("--align", default="2K", help="分区起始/大小对齐，默认 2K（多数 Cortex-M 擦写页）")
    p_layout.add_argument("--out", help="输出 .h 路径（不给则只打印结果）")
    p_layout.add_argument("parts", nargs="+", help="分区定义 name:size，按顺序排列")

    p_pack = sub.add_parser("pack", help="bin + 镜像头 → 升级包")
    p_pack.add_argument("bin")
    p_pack.add_argument("-o", "--out", help="输出 .pkg（默认同名 .pkg）")
    p_pack.add_argument("--addr", required=True, help="镜像加载地址，如 0x08008000")
    p_pack.add_argument("--ver", default="1.0.0")
    p_pack.add_argument("--hw-id", type=lambda v: int(v, 0), default=0)
    p_pack.add_argument("--force", action="store_true", help="置强制升级标志")
    p_pack.add_argument("--allow-downgrade", action="store_true", help="置允许降级标志")
    p_pack.add_argument("--emit-header", action="store_true", help="同时生成 MCU 侧 .h")

    p_verify = sub.add_parser("verify", help="校验升级包")
    p_verify.add_argument("pkg")
    p_verify.add_argument("--hw-id", type=lambda v: int(v, 0), default=None)
    p_verify.add_argument("--addr", type=lambda v: int(v, 0), default=None)

    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 2

    try:
        if args.cmd == "crc":
            if not os.path.isfile(args.file):
                print(f"文件不存在：{args.file}", file=sys.stderr)
                return 2
            _print_json(digest_of(args.file))
            return 0

        if args.cmd == "layout":
            parts = []
            for item in args.parts:
                if ":" not in item:
                    raise ValueError(f"分区定义需为 name:size 形式：{item}")
                name, size = item.split(":", 1)
                parts.append((name.strip(), parse_size(size.strip())))
            layout = build_layout(parse_size(args.flash), parts, parse_size(args.align))
            out = {
                "flash_size": layout["flash_size"],
                "align": format_size(layout["align"]),
                "regions": [
                    {"name": r["name"], "start": f"0x{r['start']:08X}",
                     "addr": f"0x{0x08000000 + r['start']:08X}",
                     "size": format_size(r["size"]), "bytes": r["size"]}
                    for r in layout["regions"]
                ],
                "used": format_size(layout["used"]),
                "free": format_size(layout["free"]),
                "overflow": layout["overflow"],
                "warnings": layout["warnings"],
            }
            if args.out:
                with open(args.out, "w", encoding="utf-8", newline="\n") as fp:
                    fp.write(layout_to_c(layout))
                out["out"] = args.out
            _print_json(out)
            return 1 if layout["overflow"] else 0

        if args.cmd == "pack":
            if not os.path.isfile(args.bin):
                print(f"文件不存在：{args.bin}", file=sys.stderr)
                return 2
            out_path = args.out or os.path.splitext(args.bin)[0] + ".pkg"
            flags = (0x1 if args.force else 0) | (0x2 if args.allow_downgrade else 0)
            _print_json(pack_firmware(args.bin, out_path, int(args.addr, 0), args.ver,
                                      args.hw_id, flags, args.emit_header))
            return 0

        if args.cmd == "verify":
            if not os.path.isfile(args.pkg):
                print(f"文件不存在：{args.pkg}", file=sys.stderr)
                return 2
            result = verify_package(args.pkg, args.hw_id, args.addr)
            _print_json(result)
            return 0 if result["ok"] else 1
    except ValueError as exc:
        print(f"参数错误：{exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # 内部错误
        print(f"内部错误：{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
