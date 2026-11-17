#!/usr/bin/env python3
"""
ota_tool.py 单元测试
覆盖：CRC 标准向量、镜像头往返与防篡改、分区表计算与溢出、打包/校验往返、CLI 退出码。

运行：python tests/test_ota_tool.py     （或 python -m pytest tests/）
"""

import io
import json
import os
import struct
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ota_tool as T  # noqa: E402


class TestCrc(unittest.TestCase):
    """标准测试向量：check 值 "123456789" """

    def test_crc32_standard_vector(self):
        self.assertEqual(T.crc32(b"123456789"), 0xCBF43926)

    def test_crc16_ccitt_standard_vector(self):
        self.assertEqual(T.crc16_ccitt(b"123456789"), 0x29B1)

    def test_crc16_modbus_standard_vector(self):
        self.assertEqual(T.crc16_modbus(b"123456789"), 0x4B37)

    def test_crc32_empty(self):
        self.assertEqual(T.crc32(b""), 0x00000000)

    def test_digest_of_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.bin")
            open(p, "wb").write(b"123456789")
            info = T.digest_of(p)
            self.assertEqual(info["size"], 9)
            self.assertEqual(info["crc32"], "0xCBF43926")
            self.assertEqual(info["crc16_ccitt"], "0x29B1")
            self.assertEqual(info["md5"], "25f9e794323b453885f5181f1b624d0b")


class TestVersion(unittest.TestCase):
    def test_encode_decode_roundtrip(self):
        for text in ("1.0.0", "1.2.3", "255.255.255", "0.0.1"):
            self.assertEqual(T.decode_version(T.encode_version(text)), text)

    def test_encode_pads_short(self):
        self.assertEqual(T.encode_version("5"), 0x00050000)

    def test_encode_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            T.encode_version("1.256.0")


class TestHeader(unittest.TestCase):
    def test_header_is_64_bytes(self):
        self.assertEqual(T.HEADER_SIZE, 64)
        self.assertEqual(T.HEADER_STRUCT.size, 64)

    def test_header_field_offsets(self):
        """偏移必须与文档一致——MCU 侧按偏移解析，错了就全盘错。"""
        body = T.build_header(b"hello", 0x08008000, "1.2.3", hw_id=0x1234, timestamp=1000)
        self.assertEqual(struct.unpack_from("<I", body, 0)[0], T.MAGIC)
        self.assertEqual(struct.unpack_from("<H", body, 4)[0], T.HEADER_VER)
        self.assertEqual(struct.unpack_from("<H", body, 6)[0], 0x1234)
        self.assertEqual(struct.unpack_from("<I", body, 8)[0], T.encode_version("1.2.3"))
        self.assertEqual(struct.unpack_from("<I", body, 12)[0], 0x08008000)
        self.assertEqual(struct.unpack_from("<I", body, 16)[0], 5)
        self.assertEqual(struct.unpack_from("<I", body, 20)[0], T.crc32(b"hello"))
        self.assertEqual(struct.unpack_from("<I", body, 28)[0], 1000)

    def test_parse_roundtrip(self):
        body = T.build_header(b"payload", 0x08010000, "2.5.7", hw_id=7, timestamp=42,
                              flags=0x1)
        info = T.parse_header(body)
        self.assertTrue(info["magic_ok"])
        self.assertEqual(info["magic_str"], "FWUP")
        self.assertEqual(info["fw_version_str"], "2.5.7")
        self.assertEqual(info["load_addr"], 0x08010000)
        self.assertEqual(info["image_size"], 7)
        self.assertEqual(info["hw_id"], 7)
        self.assertTrue(info["flags_force_upgrade"])
        self.assertFalse(info["flags_allow_downgrade"])

    def test_header_crc_valid(self):
        body = T.build_header(b"data", 0x08000000)
        self.assertTrue(T.header_crc_check(body))

    def test_header_crc_detects_tamper(self):
        body = bytearray(T.build_header(b"data", 0x08000000))
        body[12] ^= 0xFF  # 改 load_addr，头 CRC 应失效
        self.assertFalse(T.header_crc_check(bytes(body)))

    def test_reserved_is_zero(self):
        body = T.build_header(b"data", 0x08000000)
        self.assertEqual(body[36:64], b"\x00" * 28)

    def test_parse_too_short_raises(self):
        with self.assertRaises(ValueError):
            T.parse_header(b"\x00" * 10)

    def test_header_to_c_contains_key_defs(self):
        info = T.parse_header(T.build_header(b"data", 0x08008000, "1.0.0"))
        text = T.header_to_c(info)
        self.assertIn("OTA_IMAGE_MAGIC", text)
        self.assertIn("0x50555746u", text)   # 小端存储即 ASCII "FWUP"
        self.assertIn("#define OTA_HEADER_SIZE      64u", text)
        self.assertIn("typedef struct {", text)
        self.assertIn("} ota_image_header_t;", text)
        self.assertIn("#endif", text)


class TestSizeParse(unittest.TestCase):
    def test_parse_size_forms(self):
        self.assertEqual(T.parse_size("256K"), 262144)
        self.assertEqual(T.parse_size("1M"), 1048576)
        self.assertEqual(T.parse_size("4096"), 4096)
        self.assertEqual(T.parse_size("0x8000"), 32768)
        self.assertEqual(T.parse_size(2048), 2048)

    def test_format_size(self):
        self.assertEqual(T.format_size(32768), "32K")
        self.assertEqual(T.format_size(1048576), "1M")
        self.assertEqual(T.format_size(2048 * 3), "6K")


class TestLayout(unittest.TestCase):
    def test_basic_layout_addresses(self):
        layout = T.build_layout(T.parse_size("256K"),
                                [("boot", T.parse_size("32K")), ("app", T.parse_size("96K"))],
                                align=0x800)
        regs = {r["name"]: r for r in layout["regions"]}
        self.assertEqual(regs["boot"]["start"], 0)
        self.assertEqual(regs["app"]["start"], 0x8000)
        self.assertEqual(regs["app"]["end"], 0x8000 + 0x18000 - 1)
        self.assertFalse(layout["overflow"])
        self.assertEqual(layout["used"], 0x8000 + 0x18000)

    def test_overflow_detected(self):
        layout = T.build_layout(T.parse_size("64K"),
                                [("boot", T.parse_size("32K")), ("app", T.parse_size("64K"))])
        self.assertTrue(layout["overflow"])
        self.assertLess(layout["free"], 0)

    def test_exact_fit_no_overflow(self):
        layout = T.build_layout(0x10000, [("a", 0x8000), ("b", 0x8000)], align=0)
        self.assertFalse(layout["overflow"])
        self.assertEqual(layout["free"], 0)

    def test_unaligned_start_shifted_with_warning(self):
        layout = T.build_layout(T.parse_size("256K"), [("a", 0x100), ("b", 0x1000)], align=0x800)
        regs = {r["name"]: r for r in layout["regions"]}
        self.assertEqual(regs["b"]["start"] % 0x800, 0)
        self.assertTrue(any("未对齐" in w for w in layout["warnings"]))

    def test_unaligned_size_warns(self):
        layout = T.build_layout(T.parse_size("256K"), [("a", 0x900)], align=0x800)
        self.assertTrue(any("非 2K 整数倍" in w for w in layout["warnings"]))

    def test_bad_region_name_raises(self):
        with self.assertRaises(ValueError):
            T.build_layout(0x10000, [("bad-name", 0x100)])

    # ---- 数字开头/特殊字符的分区名必须拦下（2026-10-21）----
    # 修因：旧校验 name.replace('_','').isalnum() 放过 '9boot'，
    # 生成 #define 9BOOT_ADDR，gcc 报 "macro names must be identifiers"。
    def test_digit_leading_name_raises(self):
        with self.assertRaises(ValueError):
            T.build_layout(0x10000, [("9boot", 0x100)])

    def test_hyphen_name_raises(self):
        with self.assertRaises(ValueError):
            T.build_layout(0x10000, [("boot-app", 0x100)])

    def test_valid_identifier_variants_pass(self):
        layout = T.build_layout(0x10000, [("_boot", 0x8000), ("app0", 0x8000)])
        self.assertEqual(len(layout["regions"]), 2)

    def test_bad_name_generated_macro_would_be_illegal_c(self):
        """固定口径：分区名即宏名前缀，非法标识符绝不能漏进生成的 .h。"""
        for bad in ("9boot", "boot-app", "boot app", "", "boot.x"):
            with self.assertRaises(ValueError, msg=f"{bad!r} 应被拒"):
                T.build_layout(0x10000, [(bad, 0x100)])

    def test_layout_to_c_has_defs_and_guard(self):
        layout = T.build_layout(T.parse_size("256K"),
                                [("boot", T.parse_size("32K")), ("app", T.parse_size("96K"))])
        text = T.layout_to_c(layout)
        self.assertIn("#define FLASH_BASE_ADDR     0x08000000u", text)
        self.assertIn("#define BOOT_ADDR     (FLASH_BASE_ADDR + 0x00000000u)", text)
        self.assertIn("#define APP_ADDR     (FLASH_BASE_ADDR + 0x00008000u)", text)
        self.assertIn("#define OTA_PARTITION_COUNT  2u", text)
        self.assertIn("ota_layout_must_fit_flash", text)
        self.assertIn("#endif", text)

    def test_layout_to_c_overflow_has_no_assert(self):
        layout = T.build_layout(T.parse_size("64K"), [("a", T.parse_size("128K"))])
        text = T.layout_to_c(layout)
        self.assertNotIn("ota_layout_must_fit_flash", text)
        self.assertIn("布局溢出", text)


class TestPackVerify(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        self.bin = os.path.join(self.d, "app.bin")
        # 造一段像样的固件：前 8 字节是初始 MSP/复位向量，避免被当空文件
        open(self.bin, "wb").write(bytes([0x00, 0x00, 0x02, 0x20, 0x01, 0x00, 0x00, 0x08])
                                   + bytes(range(256)) * 4)

    def tearDown(self):
        self.tmp.cleanup()

    def test_pack_then_verify_roundtrip(self):
        pkg = os.path.join(self.d, "app.pkg")
        T.pack_firmware(self.bin, pkg, 0x08008000, "1.2.3", hw_id=0x0001)
        self.assertTrue(os.path.isfile(pkg))
        result = T.verify_package(pkg)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["header"]["fw_version_str"], "1.2.3")
        self.assertEqual(result["header"]["load_addr"], 0x08008000)
        self.assertEqual(result["image_size_actual"], os.path.getsize(self.bin))

    def test_package_size_is_header_plus_image(self):
        pkg = os.path.join(self.d, "app.pkg")
        T.pack_firmware(self.bin, pkg, 0x08008000)
        self.assertEqual(os.path.getsize(pkg), T.HEADER_SIZE + os.path.getsize(self.bin))

    def test_verify_expect_hw_id_match_and_mismatch(self):
        pkg = os.path.join(self.d, "app.pkg")
        T.pack_firmware(self.bin, pkg, 0x08008000, hw_id=0x0001)
        self.assertTrue(T.verify_package(pkg, expect_hw_id=0x0001)["ok"])
        bad = T.verify_package(pkg, expect_hw_id=0x0002)
        self.assertFalse(bad["ok"])
        self.assertTrue(any("硬件标识不符" in e for e in bad["errors"]))

    def test_verify_expect_addr_mismatch(self):
        pkg = os.path.join(self.d, "app.pkg")
        T.pack_firmware(self.bin, pkg, 0x08008000)
        bad = T.verify_package(pkg, expect_addr=0x08010000)
        self.assertFalse(bad["ok"])
        self.assertTrue(any("加载地址不符" in e for e in bad["errors"]))

    def test_verify_detects_image_corruption(self):
        pkg = os.path.join(self.d, "app.pkg")
        T.pack_firmware(self.bin, pkg, 0x08008000)
        blob = bytearray(open(pkg, "rb").read())
        blob[-1] ^= 0xFF  # 毁掉镜像最后一个字节
        open(pkg, "wb").write(bytes(blob))
        result = T.verify_package(pkg)
        self.assertFalse(result["ok"])
        self.assertTrue(any("镜像 CRC 不符" in e for e in result["errors"]))

    def test_verify_detects_header_corruption(self):
        pkg = os.path.join(self.d, "app.pkg")
        T.pack_firmware(self.bin, pkg, 0x08008000)
        blob = bytearray(open(pkg, "rb").read())
        blob[12] ^= 0xFF  # 改头里的 load_addr
        open(pkg, "wb").write(bytes(blob))
        result = T.verify_package(pkg)
        self.assertFalse(result["ok"])
        self.assertTrue(any("头 CRC 校验失败" in e for e in result["errors"]))

    def test_verify_detects_zero_addr(self):
        pkg = os.path.join(self.d, "app.pkg")
        T.pack_firmware(self.bin, pkg, 0)  # 地址为 0
        result = T.verify_package(pkg)
        self.assertFalse(result["ok"])
        self.assertTrue(any("加载地址为 0" in e for e in result["errors"]))

    # ---- load_addr 不在 Cortex-M flash 区间给 warning（2026-10-21）----
    # 修因：--addr 0xFFFFFFFF 打包 verify 都静默通过，填错地址烧进去跑飞却无提示。
    def test_verify_warns_addr_outside_cortex_m_flash(self):
        pkg = os.path.join(self.d, "far.pkg")
        T.pack_firmware(self.bin, pkg, 0xFFFFFFFF)
        result = T.verify_package(pkg)
        self.assertTrue(result["ok"], "区间外地址是提示不是错误（工具平台无关）")
        self.assertTrue(any("0x08000000-0x081FFFFF" in w for w in result["warnings"]))

    def test_verify_no_warning_for_normal_cortex_m_addr(self):
        pkg = os.path.join(self.d, "app.pkg")
        T.pack_firmware(self.bin, pkg, 0x08008000)
        result = T.verify_package(pkg)
        self.assertTrue(result["ok"])
        self.assertFalse(any("flash 区间" in w for w in result["warnings"]))

    def test_verify_tiny_file(self):
        pkg = os.path.join(self.d, "tiny.pkg")
        open(pkg, "wb").write(b"\x01\x02")
        result = T.verify_package(pkg)
        self.assertFalse(result["ok"])
        self.assertTrue(any("不足一个头" in e for e in result["errors"]))

    def test_pack_empty_image_raises(self):
        empty = os.path.join(self.d, "empty.bin")
        open(empty, "wb").close()
        with self.assertRaises(ValueError):
            T.pack_firmware(empty, os.path.join(self.d, "e.pkg"), 0x08000000)

    def test_emit_header_file(self):
        pkg = os.path.join(self.d, "app.pkg")
        T.pack_firmware(self.bin, pkg, 0x08008000, emit_header=True)
        h = os.path.join(self.d, "app_header.h")
        self.assertTrue(os.path.isfile(h))
        text = open(h, encoding="utf-8").read()
        self.assertIn("ota_image_header_t", text)
        self.assertIn("OTA_IMAGE_MAGIC", text)


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = T.main(argv)
        return code, buf.getvalue()

    def test_no_args_prints_help_exit2(self):
        code, _ = self._run([])
        self.assertEqual(code, 2)

    def test_crc_cli(self):
        p = os.path.join(self.d, "a.bin")
        open(p, "wb").write(b"123456789")
        code, out = self._run(["crc", p])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["crc32"], "0xCBF43926")

    def test_crc_missing_file_exit2(self):
        code, _ = self._run(["crc", os.path.join(self.d, "nope.bin")])
        self.assertEqual(code, 2)

    def test_layout_cli_ok_exit0(self):
        code, out = self._run(["layout", "--flash", "256K", "--align", "2K",
                               "boot:32K", "app:96K"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertFalse(data["overflow"])
        self.assertEqual(len(data["regions"]), 2)

    def test_layout_cli_overflow_exit1(self):
        code, out = self._run(["layout", "--flash", "64K", "boot:32K", "app:64K"])
        self.assertEqual(code, 1)
        self.assertTrue(json.loads(out)["overflow"])

    def test_layout_cli_writes_h(self):
        out_h = os.path.join(self.d, "partition.h")
        code, _ = self._run(["layout", "--flash", "256K", "--out", out_h,
                             "boot:32K", "app:96K"])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.isfile(out_h))
        self.assertIn("OTA_PARTITION_TABLE", open(out_h, encoding="utf-8").read())

    def test_layout_cli_bad_part_exit2(self):
        code, _ = self._run(["layout", "--flash", "256K", "noColonSize"])
        self.assertEqual(code, 2)

    def test_pack_verify_cli_roundtrip(self):
        b = os.path.join(self.d, "f.bin")
        open(b, "wb").write(b"\x00\x00\x02\x20" + bytes(500))
        pkg = os.path.join(self.d, "f.pkg")
        code, out = self._run(["pack", b, "-o", pkg, "--addr", "0x08008000", "--ver", "3.1.4"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["fw_version"], "3.1.4")
        code, out = self._run(["verify", pkg, "--addr", "0x08008000"])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out)["ok"])

    def test_verify_cli_mismatch_exit1(self):
        b = os.path.join(self.d, "f.bin")
        open(b, "wb").write(bytes(500))
        pkg = os.path.join(self.d, "f.pkg")
        self._run(["pack", b, "-o", pkg, "--addr", "0x08008000", "--hw-id", "0x1"])
        code, _ = self._run(["verify", pkg, "--hw-id", "0x9"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
