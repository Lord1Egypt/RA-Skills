#!/usr/bin/env python3
"""
ota_audit.py 单元测试
覆盖：13 条规则正反例、文件级信号判定、注释/字符串去噪、评分、CLI、目录扫描。

运行：python tests/test_ota_audit.py
"""

import io
import json
import os
import sys
import tempfile
import unittest
import warnings
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ota_audit as A  # noqa: E402


def rule_ids(result):
    return sorted(i["rule_id"] for i in result["issues"])


class TestStripNoise(unittest.TestCase):
    def test_line_comment_removed(self):
        clean, _ = A.strip_noise('x = 1; // __set_MSP(0)', False)
        self.assertNotIn("__set_MSP", clean)

    def test_block_comment_multiline(self):
        clean, in_block = A.strip_noise("/* jump_to_app() here", False)
        self.assertTrue(in_block)
        self.assertNotIn("jump_to_app", clean)
        clean, in_block = A.strip_noise("   more   */ x = 1;", in_block)
        self.assertFalse(in_block)
        self.assertIn("x = 1;", clean)

    def test_string_literal_removed(self):
        clean, _ = A.strip_noise('printf("FLASH_Program(0)");', False)
        self.assertNotIn("FLASH_Program", clean)
        self.assertIn("printf", clean)

    def test_code_kept(self):
        clean, _ = A.strip_noise("SCB->VTOR = 0x08000000;", False)
        self.assertIn("SCB->VTOR", clean)


class TestPageAlign(unittest.TestCase):
    def test_aligned(self):
        self.assertTrue(A.is_page_aligned(0x08000000))
        self.assertTrue(A.is_page_aligned(0x08000800))
        self.assertTrue(A.is_page_aligned(0x08001000))

    def test_unaligned(self):
        self.assertFalse(A.is_page_aligned(0x08000100))
        self.assertFalse(A.is_page_aligned(0x08000A00))


class TestJumpRules(unittest.TestCase):
    """R1/R2/R3：跳转相关的三个"缺失项"检查。"""

    BAD = """
/* bootloader 跳转，三样全缺 */
void boot_jump(unsigned int addr) {
    typedef void (*fn)(void);
    fn app = (fn)addr;
    __set_MSP(*(volatile unsigned int*)addr);
    app();
}
"""

    GOOD = """
#define APP_ADDR 0x08008000
static int app_is_valid(unsigned int base) {
    unsigned int sp = *(volatile unsigned int*)base;
    return (sp >= 0x20000000 && sp < 0x20020000);
}
void boot_jump(unsigned int addr) {
    if (!app_is_valid(addr)) return;
    if (read_version() < current_version()) return;    /* 防降级 */
    __disable_irq();
    SCB->VTOR = addr;
    __DSB(); __ISB();
    __set_MSP(*(volatile unsigned int*)addr);
    ((void(*)(void))addr)();
}
"""

    def test_all_three_reported_when_missing(self):
        result = A.review_text(self.BAD, "bad_boot.c")
        ids = rule_ids(result)
        self.assertIn(1, ids)
        self.assertIn(2, ids)
        self.assertIn(3, ids)

    def test_none_reported_when_complete(self):
        result = A.review_text(self.GOOD, "good_boot.c")
        ids = rule_ids(result)
        self.assertNotIn(1, ids)
        self.assertNotIn(2, ids)
        self.assertNotIn(3, ids)

    def test_no_jump_no_report(self):
        """普通业务代码没有跳转迹象，不该被报跳转三类。"""
        result = A.review_text("int add(int a, int b) { return a + b; }", "app.c")
        ids = rule_ids(result)
        self.assertNotIn(1, ids)
        self.assertNotIn(2, ids)
        self.assertNotIn(3, ids)

    def test_jump_in_comment_not_a_signal(self):
        result = A.review_text("// jump_to_app() 参考实现\nint x = 1;", "note.c")
        self.assertEqual(result["signals"]["jump"], [])


class TestIntegrityRule(unittest.TestCase):
    """R4：写 flash 但无校验。"""

    def test_write_without_crc_reported(self):
        src = """
void ota_save(unsigned char *buf, int len) {
    flash_write(APP_ADDR, buf, len);
}
"""
        self.assertIn(4, rule_ids(A.review_text(src, "ota.c")))

    def test_write_with_crc_not_reported(self):
        src = """
void ota_save(unsigned char *buf, int len, unsigned int expect_crc) {
    if (crc32(buf, len) != expect_crc) return;
    flash_write(APP_ADDR, buf, len);
}
"""
        self.assertNotIn(4, rule_ids(A.review_text(src, "ota.c")))

    def test_no_write_no_report(self):
        self.assertNotIn(4, rule_ids(A.review_text("int f(void){return 1;}", "x.c")))


class TestEraseAlignRule(unittest.TestCase):
    """R5：擦除地址未按页对齐。"""

    def test_unaligned_erase_reported(self):
        src = "void f(void){ flash_erase(0x08000100); }"
        self.assertIn(5, rule_ids(A.review_text(src, "e.c")))

    def test_aligned_erase_ok(self):
        src = "void f(void){ flash_erase(0x08000800); }"
        self.assertNotIn(5, rule_ids(A.review_text(src, "e.c")))

    def test_macro_addr_not_checked(self):
        src = "void f(void){ flash_erase(APP_SECTOR_ADDR); }"
        self.assertNotIn(5, rule_ids(A.review_text(src, "e.c")))


class TestWatchdogRule(unittest.TestCase):
    """R6：用了看门狗 + 擦写，但不喂狗。"""

    def test_wdt_without_feed_reported(self):
        src = """
void ota(void) {
    IWDG_Init(4000);
    flash_write(APP_ADDR, buf, len);
}
"""
        self.assertIn(6, rule_ids(A.review_text(src, "ota.c")))

    def test_wdt_with_feed_ok(self):
        src = """
void ota(void) {
    IWDG_Init(4000);
    IWDG_ReloadCounter();
    flash_write(APP_ADDR, buf, len);
    IWDG_ReloadCounter();
}
"""
        self.assertNotIn(6, rule_ids(A.review_text(src, "ota.c")))

    def test_gd32_fwdgt_recognized(self):
        src = """
void ota(void) {
    fwdgt_config(4000, 64);
    flash_write(APP_ADDR, buf, len);
}
"""
        ids = rule_ids(A.review_text(src, "ota.c"))
        self.assertIn(6, ids)

    def test_no_wdt_no_report(self):
        self.assertNotIn(6, rule_ids(A.review_text(
            "void f(void){ flash_write(a,b,c); }", "x.c")))


class TestHardcodedAddrRule(unittest.TestCase):
    """R7：裸 flash 地址（#define 行豁免）。"""

    def test_bare_addr_reported(self):
        src = "void f(void){ flash_erase(0x08008000); }"
        self.assertIn(7, rule_ids(A.review_text(src, "x.c")))

    def test_define_line_exempt(self):
        src = "#define APP_ADDR 0x08008000\nvoid f(void){ x = APP_ADDR; }"
        self.assertNotIn(7, rule_ids(A.review_text(src, "x.c")))

    def test_reported_once_only(self):
        src = """
void f(void){ flash_erase(0x08008000); }
void g(void){ flash_erase(0x0800A000); }
void h(void){ flash_erase(0x0800C000); }
"""
        issues = [i for i in A.review_text(src, "x.c")["issues"] if i["rule_id"] == 7]
        self.assertEqual(len(issues), 1)

    # ---- 比较语境豁免（R3 建议代码不被 R7 反咬，2026-10-21）----
    def test_addr_in_mask_compare_exempt(self):
        """R3 建议的跳转校验写法：0x08000001 出现在 & 与 != 的比较里，是校验常量不是寻址。"""
        src = ("void iap_load_app(void){\n"
               "    uint32_t pc = *(volatile uint32_t*)(APP_BASE + 4);\n"
               "    if ((pc & 0xFFE00001) != 0x08000001) return;\n"
               "}\n")
        self.assertNotIn(7, rule_ids(A.review_text(src, "boot.c")))

    def test_addr_in_equality_only_exempt(self):
        """仅 == / != 侧出现地址也豁免（掩码在前地址在后的写法顺序）。"""
        src = "void f(void){ if (0x08000001 == (pc & 0xFFE00001)) { jump(); } }"
        self.assertNotIn(7, rule_ids(A.review_text(src, "boot.c")))

    def test_bare_addr_in_call_arg_still_reported(self):
        """反面：地址当函数实参（真寻址）照报——豁免不能把 R7 废掉。"""
        src = "void f(void){ flash_write(0x08008000, buf, n); }"
        self.assertIn(7, rule_ids(A.review_text(src, "x.c")))

    def test_bare_addr_in_assignment_still_reported(self):
        """反面：赋值右侧的裸地址（非比较语境）照报。"""
        src = "void f(void){ uint32_t a = 0x08008000; write(a); }"
        self.assertIn(7, rule_ids(A.review_text(src, "x.c")))


class TestTimeoutRule(unittest.TestCase):
    """R8：接收死等无超时。"""

    def test_wait_without_timeout_reported(self):
        src = """
void ota_recv(void) {
    while (!rx_flag) { }
}
"""
        self.assertIn(8, rule_ids(A.review_text(src, "ota.c")))

    def test_wait_with_timeout_ok(self):
        src = """
void ota_recv(void) {
    unsigned int tick = HAL_GetTick();
    while (!rx_flag) {
        if (HAL_GetTick() - tick > TIMEOUT_MS) break;
    }
}
"""
        self.assertNotIn(8, rule_ids(A.review_text(src, "ota.c")))

    def test_non_ota_context_skipped(self):
        """非 OTA 上下文的 while 等待不报（避免业务代码刷屏）。"""
        result = A.review_text("void f(void){ while(!flag){} }", "app.c")
        self.assertNotIn(8, rule_ids(result))


class TestNonOtaNoFlood(unittest.TestCase):
    """普通业务代码（写 flash 但非 bootloader）不该被升级类规则刷屏。"""

    NON_OTA = """
#include "flash_cfg.h"
/* 普通参数存储：掉电保存配置 */
void save_config(config_t *cfg) {
    flash_erase(CFG_SECTOR_ADDR);
    flash_write(CFG_ADDR, (unsigned char *)cfg, sizeof(*cfg));
}

int wait_ready(void) {
    while (!flag) { }
    return 0;
}
"""

    def test_no_ota_rules_on_plain_code(self):
        result = A.review_text(self.NON_OTA, "cfg_store.c")
        ids = rule_ids(result)
        for rid in (4, 9, 10, 11, 12, 8):
            self.assertNotIn(rid, ids, f"规则{rid}不该在非 OTA 代码上报")

    def test_ota_context_detected_by_keyword(self):
        result = A.review_text("void ota_recv(void){ flash_write(a,b,c); }", "x.c")
        self.assertTrue(result["signals"]["is_ota_ctx"])

    def test_ota_context_detected_by_jump(self):
        result = A.review_text("void boot_jump(void){ x(); }", "x.c")
        self.assertTrue(result["signals"]["jump"])


class TestVersionRule(unittest.TestCase):
    """R9：无防降级版本校验。"""

    def test_missing_version_reported(self):
        src = """
void ota_apply(void) {
    flash_write(APP_ADDR, buf, len);
}
"""
        self.assertIn(9, rule_ids(A.review_text(src, "ota.c")))

    def test_version_compare_ok(self):
        src = """
void ota_apply(void) {
    if (pkg_version < fw_version) return;
    flash_write(APP_ADDR, buf, len);
}
"""
        self.assertNotIn(9, rule_ids(A.review_text(src, "ota.c")))


class TestStateRule(unittest.TestCase):
    """R10：升级状态未持久化。"""

    def test_no_state_save_reported(self):
        src = "void ota(void){ flash_write(APP_ADDR, buf, len); }"
        self.assertIn(10, rule_ids(A.review_text(src, "ota.c")))

    def test_state_save_ok(self):
        src = """
void ota(void) {
    write_flag(OTA_UPGRADE_PENDING);
    flash_write(APP_ADDR, buf, len);
}
"""
        self.assertNotIn(10, rule_ids(A.review_text(src, "ota.c")))


class TestReturnValueRule(unittest.TestCase):
    """R11：flash 写未检查返回值。"""

    def test_unchecked_reported(self):
        src = "void ota(void){ FLASH_Program(addr, data, len); }"
        self.assertIn(11, rule_ids(A.review_text(src, "ota.c")))

    def test_checked_ok(self):
        src = """
void ota(void) {
    if (HAL_FLASH_Program(TYPEPROGRAM, addr, data) != HAL_OK) {
        error_handler();
    }
}
"""
        self.assertNotIn(11, rule_ids(A.review_text(src, "ota.c")))


class TestProgressRule(unittest.TestCase):
    """R12：无进度日志。"""

    def test_no_log_reported(self):
        src = "void ota(void){ flash_write(APP_ADDR, buf, len); }"
        self.assertIn(12, rule_ids(A.review_text(src, "ota.c")))

    def test_with_log_ok(self):
        src = """
void ota(void) {
    printf("ota start\\n");
    flash_write(APP_ADDR, buf, len);
}
"""
        self.assertNotIn(12, rule_ids(A.review_text(src, "ota.c")))

    def test_progress_callback_ok(self):
        """自定义进度回调（ota_progress 等）应视作已有进度输出。"""
        src = """
void ota(void) {
    ota_progress(50);
    flash_write(APP_ADDR, buf, len);
    ota_progress(100);
}
"""
        self.assertNotIn(12, rule_ids(A.review_text(src, "ota.c")))


class TestDelayRule(unittest.TestCase):
    """R13：硬编码延时。"""

    def test_hardcoded_delay_reported(self):
        src = "void ota(void){ HAL_Delay(500); }"
        self.assertIn(13, rule_ids(A.review_text(src, "ota.c")))

    def test_delay_with_variable_ok(self):
        src = "void ota(void){ HAL_Delay(period_ms); }"
        self.assertNotIn(13, rule_ids(A.review_text(src, "ota.c")))

    def test_reported_once(self):
        src = "void ota_a(void){ delay_ms(100); }\nvoid ota_b(void){ delay_ms(200); }"
        issues = [i for i in A.review_text(src, "x.c")["issues"] if i["rule_id"] == 13]
        self.assertEqual(len(issues), 1)

    # ---- R13 加了下限与"自带护栏"豁免（Arduino 短让出误报治理）----
    def test_short_delay_is_yield_not_magic(self):
        """<50ms 的延时是让出 CPU / 节流，不是"用固定延时替代超时机制"。"""
        for src in ("void ota(void){ delay(2); }",
                    "void ota(void){ delay(5); }",
                    "void ota(void){ delay(10); }"):
            self.assertNotIn(13, rule_ids(A.review_text(src, "sketch.ino")))

    def test_delay_threshold_boundary(self):
        """阈值边界：49 不报、50 报（DELAY_MAGIC_MIN_MS = 50）。"""
        self.assertNotIn(13, rule_ids(A.review_text("void ota(void){ delay(49); }", "s.ino")))
        self.assertIn(13, rule_ids(A.review_text("void ota(void){ delay(50); }", "s.ino")))

    def test_delay_with_inline_timeout_guard_ok(self):
        """该行自带超时护栏时，延时就只是轮询间隔，R13 的建议已经做到了。"""
        src = ("void ota(void){ while (WiFi.status() != WL_CONNECTED && millis() < deadline)"
               " { delay(100); } }")
        self.assertNotIn(13, rule_ids(A.review_text(src, "sketch.ino")))

    def test_delay_under_timeout_guard_next_line_ok(self):
        """护栏与延时分居两行（框架里最常见的缩进写法）也要豁免。"""
        src = """
void ota(void) {
    unsigned long deadline = millis() + 20000;
    while (WiFi.status() != WL_CONNECTED && millis() < deadline) {
        delay(100);
    }
}
"""
        self.assertNotIn(13, rule_ids(A.review_text(src, "sketch.ino")))

    def test_delay_without_any_guard_still_reported(self):
        """反面：没有任何超时护栏的固定延时照常报——别把 R13 豁免成摆设。"""
        src = """
void ota(void) {
    while (WiFi.status() != WL_CONNECTED) {
        delay(100);
    }
}
"""
        self.assertIn(13, rule_ids(A.review_text(src, "sketch.ino")))

    def test_delay_in_arduino_loop_is_tick_not_upgrade(self):
        """Arduino 的 loop() 是空闲主循环，其内 delay 是节拍器，不是升级等待。"""
        single = "void ota_loop(void) {}\nvoid loop() { delay(1000); }"
        multi = "void ota_tick(void) {}\nvoid loop() {\n    delay(1000);\n}\n"
        for src in (single, multi):
            self.assertNotIn(13, rule_ids(A.review_text(src, "sketch.ino")))
        # 反面：同样内容不在 loop() 里就照常报
        src = "void ota_other(void) {\n    delay(1000);\n}\n"
        self.assertIn(13, rule_ids(A.review_text(src, "sketch.ino")))

    # ---- 平台标注：Arduino 不能被标成 ESP-IDF / 通用 Cortex-M ----
    def test_detect_platform_arduino(self):
        src = ("#include <ArduinoOTA.h>\nvoid setup(){ ArduinoOTA.begin(); }\n"
               "void loop(){ ArduinoOTA.handle(); }\n")
        self.assertEqual(A.detect_platform(src)["id"], "arduino")

    def test_detect_platform_arduino_update_lib(self):
        src = "void f(void){ Update.begin(n, U_FLASH); size_t w = Update.write(b, n); }"
        self.assertEqual(A.detect_platform(src)["id"], "arduino")

    def test_detect_platform_stm32_not_arduino(self):
        """STM32 代码不能被误标成 Arduino（loop_check 这类名字要挡住）。"""
        src = "void loop_check(void);\nHAL_Init();\nHAL_FLASH_Program(t, a, d);\n"
        self.assertEqual(A.detect_platform(src)["id"], "stm32")

    def test_detect_platform_esp_idf_stays_idf(self):
        src = "void f(void){ esp_ota_write(h, b, n); esp_partition_write(p, o, b, n); }"
        self.assertEqual(A.detect_platform(src)["id"], "esp-idf")

    def test_non_ota_delay_skipped(self):
        """非 OTA 业务代码里的固定延时不该被报成「升级流程」隐患。"""
        src = "void led_task(void){ LED_Toggle(); HAL_Delay(500); }"
        self.assertNotIn(13, rule_ids(A.review_text(src, "led.c")))


class TestScoring(unittest.TestCase):
    def test_clean_file_scores_100(self):
        result = A.review_text("int add(int a,int b){return a+b;}", "app.c")
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["summary"]["total"], 0)

    def test_score_deducts_by_severity(self):
        # 3 高危 + 一堆中低危
        result = A.review_text(TestJumpRules.BAD, "bad.c")
        self.assertLess(result["score"], 100)
        weights = sum(A.SEVERITY_WEIGHT[i["severity"]] for i in result["issues"])
        self.assertEqual(result["score"], max(0, 100 - weights))

    def test_score_never_negative(self):
        src = "\n".join(["void f%d(void){ delay_ms(%d); }" % (i, i) for i in range(50)])
        result = A.review_text(src, "x.c")
        self.assertGreaterEqual(result["score"], 0)

    def test_summary_counts_match(self):
        result = A.review_text(TestJumpRules.BAD, "bad.c")
        self.assertEqual(result["summary"]["total"], len(result["issues"]))
        self.assertEqual(
            result["summary"]["high"] + result["summary"]["medium"] + result["summary"]["low"],
            result["summary"]["total"])


class TestIdealBootloaderClean(unittest.TestCase):
    """一个写得很规范的 bootloader 应当零命中——防误报的底线测试。"""

    IDEAL = """
#include "partition.h"
#define APP_ADDR   APP_OFFSET_ADDR

static int app_is_valid(unsigned int base) {
    unsigned int sp = *(volatile unsigned int *)base;
    unsigned int pc = *(volatile unsigned int *)(base + 4);
    if (sp < 0x20000000 || sp > 0x20020000) return 0;
    return pc != 0;
}

void boot_jump(void) {
    if (!app_is_valid(APP_ADDR)) { app_log("app invalid"); return; }
    if (read_fw_version(APP_ADDR) > current_version()) { return; }
    if (verify_image(APP_ADDR, image_size) != 0) { return; }
    app_log("jumping to app");
    __disable_irq();
    SCB->VTOR = APP_ADDR;
    __DSB();
    __ISB();
    __set_MSP(*(volatile unsigned int *)APP_ADDR);
    ((void (*)(void))APP_ADDR)();
}
"""

    def test_ideal_is_clean(self):
        result = A.review_text(self.IDEAL, "bootloader.c")
        self.assertEqual(result["issues"], [], f"误报：{rule_ids(result)}")


class TestDirectoryScan(unittest.TestCase):
    def test_directory_scan(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "good.c"), "w").write("int f(void){return 1;}")
            open(os.path.join(d, "bad.c"), "w").write("void f(void){ flash_erase(0x08000100); }")
            open(os.path.join(d, "note.txt"), "w").write("flash_erase(0x08000100);")  # 非源码，应忽略
            result = A.review_directory(d)
            self.assertTrue(result["success"])
            self.assertEqual(result["files_scanned"], 2)
            names = [f["file"] for f in result["files"]]
            self.assertIn("bad.c", names)
            self.assertNotIn("note.txt", names)
            self.assertGreater(result["summary"]["total"], 0)

    def test_skips_build_dirs(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "build"))
            open(os.path.join(d, "build", "gen.c"), "w").write("void f(void){ flash_erase(0x08000100); }")
            result = A.review_directory(d)
            self.assertEqual(result["files_scanned"], 0)


class TestHtmlReport(unittest.TestCase):
    def test_html_structure(self):
        result = A.review_text(TestJumpRules.BAD, "bad.c")
        html = A.to_html(result)
        for marker in ("<!DOCTYPE html>", "OTA 升级链路审计报告", "高危", "</html>"):
            self.assertIn(marker, html)

    def test_html_escapes_na(self):
        result = A.review_text("int f(void){return 0;}", "clean.c")
        html = A.to_html(result)
        self.assertIn("未发现问题", html)

    def test_directory_html(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "bad.c"), "w").write("void f(void){ flash_erase(0x08000100); }")
            html = A.to_html(A.review_directory(d))
            self.assertIn("bad.c", html)


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = A.main(argv)
        return code, buf.getvalue()

    def test_no_args_exit2(self):
        code, _ = self._run([])
        self.assertEqual(code, 2)

    def test_clean_file_exit0(self):
        p = os.path.join(self.d, "ok.c")
        open(p, "w").write("int f(void){return 1;}")
        code, out = self._run([p])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["summary"]["total"], 0)

    def test_dirty_file_exit1(self):
        p = os.path.join(self.d, "bad.c")
        open(p, "w").write("void f(void){ flash_erase(0x08000100); }")
        code, out = self._run([p])
        self.assertEqual(code, 1)
        self.assertGreater(json.loads(out)["summary"]["total"], 0)

    def test_missing_file_exit2(self):
        code, _ = self._run([os.path.join(self.d, "nope.c")])
        self.assertEqual(code, 2)

    def test_level_filter(self):
        p = os.path.join(self.d, "mix.c")
        open(p, "w").write("void ota(void){ flash_erase(0x08000100); HAL_Delay(500); }")
        code, out = self._run([p, "high"])
        data = json.loads(out)
        self.assertTrue(all(i["severity"] == "high" for i in data["issues"]))

    def test_dir_mode(self):
        open(os.path.join(self.d, "a.c"), "w").write("void f(void){ flash_erase(0x08000100); }")
        code, out = self._run(["--dir", self.d])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["files_scanned"], 1)

    def test_html_output(self):
        p = os.path.join(self.d, "bad.c")
        open(p, "w").write("void f(void){ flash_erase(0x08000100); }")
        h = os.path.join(self.d, "r.html")
        code, out = self._run([p, "all", "--html", h])
        self.assertTrue(os.path.isfile(h))
        self.assertEqual(json.loads(out)["html_report"], h)
        self.assertIn("<!DOCTYPE html>", open(h, encoding="utf-8").read())


class TestRealWorldPatterns(unittest.TestCase):
    """来自真实开源 bootloader 的写法形态（语料实测暴露的问题，此处固化为回归）。

    这些形态本身都"没问题"，属于早期的误报来源：
      1. 中断向量表初始化表里的函数指针强转被当成跳转
      2. 名字里带 start_app 的变量被当成跳转
      3. 框架托管跳转（mbed_start_application）被当成"跳转三步缺失"
      4. 厂商 HAL 里的 flash 编程函数"定义行"被要求检查返回值
      5. #define 宏里的 flash 写被要求检查返回值
      6. 用菜单/LED/串口做反馈的升级流程被判定"无进度输出"
    """

    def test_vector_table_initializer_not_a_jump(self):
        src = "void (* const IV[])(void) = { (void (*)(void))(&END_STACK), isr_reset };"
        self.assertEqual(A.review_text(src, "boot.c")["signals"]["jump"], [])

    def test_variable_named_start_app_not_a_jump(self):
        src = "bool const just_start_app = valid_app && !dfu_start && (*dbl_reset_mem) == 0x57;"
        self.assertEqual(A.review_text(src, "main.c")["signals"]["jump"], [])

    def test_framework_call_not_a_jump_but_noted(self):
        """框架托管跳转：不报 R1/R2/R3（三步在框架里），但要给出提示。"""
        src = """
void boot(void) {
    if (app_is_valid()) mbed_start_application(APP_START_ADDR);
}
"""
        result = A.review_text(src, "main.cpp")
        ids = rule_ids(result)
        for rid in (1, 2, 3):
            self.assertNotIn(rid, ids, f"规则{rid}不该在框架托管跳转上报")
        self.assertTrue(result["notes"], "应给出「跳转被托管」提示")
        self.assertIn("mbed_start_application", result["notes"][0]["note"])

    def test_hal_driver_definition_not_reported(self):
        """厂商 HAL 的 flash 编程实现（定义行）不该被要求"检查返回值"。"""
        src = """
/* ota 固件写入封装 */
HAL_StatusTypeDef HAL_FLASH_Program(uint32_t TypeProgram, uint32_t Address, uint64_t Data)
{
    return HAL_ERROR;
}

void ota_write(const void *buf, int len) {
    if (HAL_FLASH_Program(TYPEPROGRAM, ADDR, (uint64_t)buf) != HAL_OK) { ota_fail(); }
    ota_progress(100);
}
"""
        self.assertNotIn(11, rule_ids(A.review_text(src, "hal_flash.c")))

    def test_macro_flash_write_not_reported(self):
        """#define 宏里的 flash 写（写法上的复用）不该被要求检查返回值。"""
        src = """
void ota_apply(void) {
#define WRITE_TRAILER(addr, val) hal_flash_write(addr, (void *)&val, 1)
    ota_progress(1);
    WRITE_TRAILER(TRAILER_ADDR, 1);
}
"""
        ids = rule_ids(A.review_text(src, "ota.c"))
        self.assertNotIn(11, ids)

    def test_ota_unchecked_write_still_reported(self):
        """反向：升级语境里裸调用 flash 写、不接返回值，仍要报（召回不能丢）。"""
        src = """
void ota_apply(void) {
    flash_write(APP_ADDR, buf, len);
    ota_progress(100);
}
"""
        self.assertIn(11, rule_ids(A.review_text(src, "ota.c")))

    def test_menu_output_counts_as_feedback(self):
        """用菜单/显示做反馈的升级流程不该被报「无进度输出」。"""
        src = """
void iap_boot(void) {
    Main_Menu(APPLICATION_ADDRESS);
    flash_write(APP_ADDR, buf, len);
}
"""
        self.assertNotIn(12, rule_ids(A.review_text(src, "iap_main.c")))

    def test_led_feedback_counts(self):
        src = "void ota_task(void){ STM_EVAL_LEDOn(LED3); flash_write(APP_ADDR, b, n); }"
        self.assertNotIn(12, rule_ids(A.review_text(src, "ota.c")))


class TestCrossFileDeescalation(unittest.TestCase):
    """跨文件存疑降级：本文件缺某步骤、但该步骤由外部模块承担的迹象存在时，
    按低危提示输出（带【需人工确认】），而不是直接按高危断言。"""

    WOLFBOOT_STYLE = """
#include "image.h"
void (* const IV[])(void) __attribute__((section(".isr_vector"))) = { 0 };

void boot_arm(unsigned int app_entry) {
    if (verify_image_header(app_entry) != 0) { return; }
    VTOR = app_entry;
    app_log("jumping");
    asm volatile("mov pc, %0" ::"r"(app_entry));
}
"""

    def test_all_downgraded_with_confirm_flag(self):
        result = A.review_text(self.WOLFBOOT_STYLE, "boot_arm.c")
        ids = rule_ids(result)
        self.assertNotIn(1, ids, "VTOR 已在本文件设置，不该报 R1")
        for rid in (2, 3, 9):
            self.assertIn(rid, ids, f"规则{rid}应报（但降级）")
        for issue in result["issues"]:
            self.assertEqual(issue["severity"], "low", f"规则{issue['rule_id']}应降为低危")
            self.assertIn("需人工确认", issue["description"])

    def test_no_companion_evidence_stays_high(self):
        """没有任何"外部模块承担"迹象时，仍按高危判（不能借降级放水）。"""
        src = """
void boot_jump(unsigned int addr) {
    __set_MSP(*(volatile unsigned int *)addr);
    ((void (*)(void))addr)();
}
"""
        result = A.review_text(src, "jump.c")
        sev = {i["rule_id"]: i["severity"] for i in result["issues"]}
        self.assertEqual(sev.get(1), "high")
        self.assertEqual(sev.get(2), "high")
        self.assertEqual(sev.get(3), "high")

    def test_state_companion_downgrades_r10(self):
        src = """
#include "partition.h"
void ota_apply(void) {
    if (wolfBoot_get_partition_state(PART_UPDATE, &st) == 0) { }
    flash_write(APP_ADDR, buf, len);
}
"""
        issues = [i for i in A.review_text(src, "update_flash.c")["issues"] if i["rule_id"] == 10]
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["severity"], "low")
        self.assertIn("需人工确认", issues[0]["description"])


class TestInlineAsmJump(unittest.TestCase):
    """内联汇编里的跳转（asm volatile("mov pc, ...")）也要能被识别。"""

    def test_asm_jump_detected(self):
        src = """
void boot_arm(unsigned int app_entry) {
    if (read_fw_version(app_entry) < current_version()) { return; }
    if (fw_image_valid(app_entry) != 0) { return; }
    SCB->VTOR = app_entry;
    __disable_irq();
    app_log("go");
    asm volatile("mov pc, %0" ::"r"(app_entry));
}
"""
        result = A.review_text(src, "boot_arm.c")
        self.assertTrue(result["signals"]["jump"], "内联汇编跳转应被识别")
        self.assertEqual(result["issues"], [], f"误报：{rule_ids(result)}")


class TestJumpAnchor(unittest.TestCase):
    """锚点要取真实跳转现场，而不是 extern 声明行（ST 官方 IAP 例程形态）。"""

    STYLE = """
extern pFunction JumpToApplication;
void iap_jump(unsigned int APPLICATION_ADDRESS) {
    if (((*(__IO uint32_t*)APPLICATION_ADDRESS) & 0x2FFE0000 ) == 0x20000000) {
        JumpAddress = *(__IO uint32_t*) (APPLICATION_ADDRESS + 4);
        JumpToApplication = (pFunction) JumpAddress;
        __set_MSP(*(__IO uint32_t*) APPLICATION_ADDRESS);
        JumpToApplication();
    }
}
"""

    def test_anchor_is_jump_site(self):
        """高危项的定位应指向 __set_MSP 那一行（L7），不是 extern 声明（L2）。"""
        result = A.review_text(self.STYLE, "iap_main.c")
        highs = [i for i in result["issues"] if i["severity"] == "high"]
        self.assertEqual(sorted(i["rule_id"] for i in highs), [1, 2])
        for issue in highs:
            self.assertEqual(issue["line"], 7,
                             f"规则{issue['rule_id']}应锚在 __set_MSP 行，实为 L{issue['line']}")

    def test_validity_check_via_sram_mask(self):
        """ST 用 (向量表值 & 0x2FFE0000) == 0x20000000 判断合法性，应认作已校验。"""
        self.assertNotIn(3, rule_ids(A.review_text(self.STYLE, "iap_main.c")))


class TestEraseBeforeWriteRule(unittest.TestCase):
    """R14：有 flash 写但全文无擦除（NOR flash 写前必须擦）。"""

    def test_write_without_erase_reported(self):
        src = """
void ota_apply(void) {
    ota_progress(1);
    flash_write(APP_ADDR, buf, len);
}
"""
        issues = [i for i in A.review_text(src, "ota.c")["issues"] if i["rule_id"] == 14]
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["severity"], "medium")

    def test_erase_present_ok(self):
        src = """
void ota_apply(void) {
    flash_erase(SECTOR_ADDR);
    flash_write(APP_ADDR, buf, len);
    ota_progress(1);
}
"""
        self.assertNotIn(14, rule_ids(A.review_text(src, "ota.c")))

    def test_generic_erase_call_recognized(self):
        """nor_erase() / erase_sector() 这类命名也要认作擦除动作。"""
        src = "void ota(void){ nor_erase(SECTOR); flash_write(APP_ADDR,b,n); ota_progress(1); }"
        self.assertNotIn(14, rule_ids(A.review_text(src, "ota.c")))

    def test_erase_mentioned_elsewhere_downgrades(self):
        """文件里提到擦除由外部驱动负责 → 降为低危待确认，而不是中危断言。"""
        src = """
/* erase performed by the external dfu driver before this wrapper is called */
void ota_apply(void) {
    ota_progress(1);
    flash_write(APP_ADDR, buf, len);
}
"""
        issues = [i for i in A.review_text(src, "ota.c")["issues"] if i["rule_id"] == 14]
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["severity"], "low")
        self.assertIn("需人工确认", issues[0]["description"])

    def test_non_ota_not_reported(self):
        src = "void cfg_save(void){ flash_write(CFG_ADDR, cfg, sizeof(*cfg)); }"
        self.assertNotIn(14, rule_ids(A.review_text(src, "cfg.c")))


class TestCliFailUnder(unittest.TestCase):
    def test_fail_under_gate(self):
        """该样本评分 91（R5+R7 中危、R12 低危），用阈值 95 / 50 验证门禁两侧。"""
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "dirty.c")
            open(p, "w").write("void ota(void){ flash_erase(0x08000100); }")
            with redirect_stdout(io.StringIO()):
                code = A.main([p, "all", "--fail-under", "95"])
            self.assertEqual(code, 1, "91 分应低于阈值 95 → 退出码 1")
            with redirect_stdout(io.StringIO()):
                code = A.main([p, "all", "--fail-under", "50"])
            self.assertEqual(code, 0, "91 分应高于阈值 50 → 退出码 0")


class TestCrossPlatform(unittest.TestCase):
    """跨平台适用性：Nordic / ESP-IDF / RISC-V / GD32 的真实写法识别与召回。

    这些用例取自真实开源 bootloader 的写法（nrfx / ESP-IDF / CH32V / GD32 FMC），
    用来守住「不是 STM32-only 工具」这条底线——每一条都对应一次实测踩过的坑。
    """

    # ---- 语境判定：真实代码里 OTA 关键词几乎总带下划线前缀 ----
    def test_ota_ctx_underscore_prefixed_names(self):
        for src in [
            "esp_ota_write(h, buf, n);",            # ESP-IDF
            "nrf_dfu_flash_store(dst, src, len);",  # Nordic
            "void gd32_ota_apply(void){}",          # GD32
            "void my_iap_handler(void){}",          # ST 系自定义
            "void boot_jump(uint32_t a){}",         # 通用裸机
        ]:
            self.assertTrue(A.review_text(src, "x.c")["signals"]["is_ota_ctx"],
                            f"应识别为 OTA 语境: {src}")

    def test_ota_ctx_no_false_positive_on_quota(self):
        """普通业务词 quota 含 'ota' 子串，不该被判成 OTA 语境。"""
        src = "int quota = 100;\nvoid set_quota(int q){ quota = q; }"
        self.assertFalse(A.review_text(src, "billing.c")["signals"]["is_ota_ctx"])

    def test_ota_ctx_include_header_alone_not_enough(self):
        """只 include 了 dfu 头文件的纯 flash 驱动，不该被判成 OTA 语境。"""
        src = ('#include "dfu_types.h"\n'
               "void flash_nrf5x_write(unsigned a){ nrfx_nvmc_words_write(a, 0, 0); }")
        self.assertFalse(A.review_text(src, "flash_nrf5x.c")["signals"]["is_ota_ctx"])

    # ---- 跳转识别：真实实现是「取 APP 向量 → 赋函数指针 → 调用」----
    def test_jump_via_app_vector_read(self):
        src = """
typedef void (*app_fn)(void);
void nordic_boot_jump(uint32_t app_addr) {
    app_fn entry = (app_fn)(*(volatile uint32_t *)(app_addr + 4));
    entry();
}
"""
        self.assertTrue(A.review_text(src, "boot.c")["signals"]["jump"],
                        "取 APP 复位向量的写法应被识别为跳转迹象")

    # ---- 平台识别 ----
    def test_platform_detection(self):
        cases = [
            ("nrfx_nvmc_page_erase(a);", "nordic"),
            ('ESP_LOGI(TAG, "x"); esp_partition_write(p, 0, b, 1);', "esp-idf"),
            ("fmc_word_program(a, b);", "gd32"),
            ('__asm volatile("csrw mtvec, %0" :: "r"(a));', "riscv"),
            ('k_msleep(10); LOG_INF("x");', "zephyr"),
            ("HAL_FLASH_Program(0, 1, 2);", "stm32"),
        ]
        for src, want in cases:
            self.assertEqual(A.detect_platform(src)["id"], want, f"{src} 应识别为 {want}")

    # ---- 非 STM32 平台的召回（每个平台一个自写最小样本）----
    NORDIC_BAD = """
#include "nrfx_nvmc.h"
#include "nrfx_wdt.h"
#define APP_ADDR 0x00026000
typedef void (*app_fn)(void);
void nordic_boot_jump(uint32_t app_addr) {
    app_fn entry = (app_fn)(*(volatile uint32_t *)(app_addr + 4));
    entry();
}
void nordic_dfu_receive(void) {
    nrfx_wdt_init(0);
    while (!dfu_packet_ready) { }
    nrfx_nvmc_page_erase(dst & ~0xFFF);
    nrfx_nvmc_words_write(dst, (uint32_t *)src, len);
}
"""

    def test_nordic_platform_recall(self):
        ids = rule_ids(A.review_text(self.NORDIC_BAD, "bad_nordic_ota.c"))
        for rid in (1, 2, 3, 4, 6, 8, 12):  # 跳转三步缺失 / 无校验 / 未喂狗 / 死等 / 无日志
            self.assertIn(rid, ids, f"Nordic 平台的规则{rid}应命中")
        self.assertNotIn(7, ids, "nRF52 flash 基址是 0x00000000，裸地址规则不该误报")
        self.assertNotIn(11, ids, "nrfx_nvmc_words_write 返回 void，不该报未查返回值")

    ESP_BAD = """
#include "esp_ota_ops.h"
#include "esp_task_wdt.h"
esp_err_t bad_esp_ota_write(const esp_partition_t *part, const void *data, size_t len) {
    esp_task_wdt_init(5, true);
    while (!uart_rx_done) { }
    return esp_partition_write(part, 0, data, len);
}
"""

    def test_esp_platform_recall(self):
        ids = rule_ids(A.review_text(self.ESP_BAD, "bad_esp_ota.c"))
        for rid in (4, 6, 8, 14):
            self.assertIn(rid, ids, f"ESP 平台的规则{rid}应命中")
        for rid in (1, 2, 3):
            self.assertNotIn(rid, ids, "ESP32 不通过 SCB->VTOR 跳转，跳转类规则不该误报")

    GD32_BAD = """
#include "gd32f30x_fmc.h"
#define APP_BASE 0x08008000
void gd32_ota_apply(const uint8_t *fw) {
    fmc_unlock();
    fmc_page_erase(0x08008100);
    fmc_word_program(APP_BASE, *(uint32_t *)fw);
    fmc_lock();
}
"""

    def test_gd32_platform_recall(self):
        ids = rule_ids(A.review_text(self.GD32_BAD, "bad_gd32_ota.c"))
        for rid in (4, 5, 7, 11):  # 无校验 / 擦除未页对齐 / 裸地址 / 未查返回值
            self.assertIn(rid, ids, f"GD32 平台的规则{rid}应命中")

    RISCV_BAD = """
typedef void (*app_fn)(void);
void riscv_boot_jump(uint32_t app_addr) {
    __asm volatile("csrw mtvec, %0" :: "r"(app_addr));
    app_fn entry = (app_fn)(*(volatile uint32_t *)(app_addr));
    entry();
}
"""

    def test_riscv_mtvec_recognized_as_relocation(self):
        """RISC-V 用 csrw mtvec 重定位向量表，应认作已完成，不报 R1。"""
        r = A.review_text(self.RISCV_BAD, "bad_riscv_ota.c")
        self.assertTrue(r["signals"]["has_vtor"], "csrw mtvec 应被识别为向量表重定位")
        self.assertNotIn(1, rule_ids(r))

    # ---- R11：只对「有返回值语义」的写 API 判定 ----
    def test_r11_skips_void_style_driver_write(self):
        """签名未知/void 的第三方写函数（如 wolfBoot ext_flash_write）不该报 R11。"""
        src = """
void ota_apply(void) {
    boot_erase();
    ext_flash_write(dst, buf, len);
    hal_flash_write(addr, buf, len);
}
"""
        self.assertNotIn(11, rule_ids(A.review_text(src, "ota_flash.c")))

    def test_r11_exempts_assigned_return_lowercase(self):
        """ret = esp_partition_write(...) 返回值已接住，不该报 R11。"""
        src = """
int ota_flush(ota_t *it) {
    ret = esp_partition_write(it->part, it->off, it->buf, 16);
    return ret;
}
"""
        self.assertNotIn(11, rule_ids(A.review_text(src, "ota.c")))

    def test_r11_reports_bare_esp_write(self):
        src = "void ota_x(void){ esp_partition_write(p, 0, buf, n); }"
        self.assertIn(11, rule_ids(A.review_text(src, "ota.c")))

    # ---- R13：复位/重启前的硬件时序延时不算升级隐患 ----
    def test_r13_exempts_delay_before_reset(self):
        src = """
void bootloader_reset(void) {
    esp_rom_delay_us(1000); /* Allow last byte to leave FIFO */
    esp_rom_software_reset_system();
}
void ota_run(void) { bootloader_reset(); }
"""
        self.assertNotIn(13, rule_ids(A.review_text(src, "ota_boot.c")))

    def test_r13_still_reports_polling_delay(self):
        src = "void ota_wait(void){ ota_begin(); HAL_Delay(500); ota_apply(); }"
        self.assertIn(13, rule_ids(A.review_text(src, "ota.c")))

    # ---- R10：各平台的持久化状态写法应被识别 ----
    def test_r10_recognizes_esp_otadata(self):
        src = """
void ota_mark(void) {
    flash_write(otadata, &sel, sizeof(sel));
    ota_select = 1;
}
"""
        self.assertNotIn(10, rule_ids(A.review_text(src, "ota.c")))

    def test_r10_recognizes_mcuboot_trailer_write(self):
        src = """
void boot_impl(void) {
    flash_area_write(fa, off, &trailer, sizeof(trailer));
    boot_write_trailer(fa, off);
}
"""
        self.assertNotIn(10, rule_ids(A.review_text(src, "bootutil_misc.c")))


class TestArduinoFramework(unittest.TestCase):
    """Arduino / ESP8266 框架层：命名族与 ESP-IDF 完全不是一套，必须单独守。

    这一族全是实测暴露的——早先只按"架构 / 厂商"分维度，漏了"框架层"，
    结果纯 ArduinoOTA 草图（setup 里 begin、loop 里 handle）连 OTA 语境都判不出来，
    **整套升级规则静默不触发、输出假的 100 分**。根因是词边界只防了"下划线前缀"
    （esp_ota_write），没防"camelCase 前缀"（ArduinoOTA 里的 OTA 前一字符是字母 o）。
    """

    # ---- 语境判定：camelCase 与点号成员调用 ----
    def test_ota_ctx_arduinoota_camelcase(self):
        src = "#include <ArduinoOTA.h>\nvoid setup(){ ArduinoOTA.begin(); }\n"
        self.assertTrue(A.review_text(src, "sketch.ino")["signals"]["is_ota_ctx"])

    def test_ota_ctx_update_dot_member(self):
        src = "void f(void){ Update.begin(n, U_FLASH); }\n"
        self.assertTrue(A.review_text(src, "sketch.ino")["signals"]["is_ota_ctx"])

    def test_ota_ctx_httpupdate_forms(self):
        for call in ("ESPhttpUpdate.update(c, u);", "httpUpdate.update(c, u);"):
            src = "void f(void){ %s }\n" % call
            self.assertTrue(A.review_text(src, "sketch.ino")["signals"]["is_ota_ctx"])

    def test_quota_still_not_ota_ctx(self):
        """扩面不能把普通词 quota 吃进来——camelCase 分支必须大小写敏感。"""
        src = "int quota_check(int quota){ return quota * 2; }"
        self.assertFalse(A.review_text(src, "calc.c")["signals"]["is_ota_ctx"])

    def test_ota_ctx_camel_not_triggered_by_lowercase_in_word(self):
        """myOTAflag 这类"缩写后还接小写字母"的不算（保守，宁漏不误）。"""
        src = "int myOTAflag_dummy(void){ return 0; }"
        self.assertFalse(A.review_text(src, "calc.c")["signals"]["is_ota_ctx"])

    # ---- 信号识别：框架 API 要真的被认出来 ----
    def test_update_write_is_flash_write(self):
        src = "void f(void){ Update.write(buf, n); }"
        self.assertTrue(A.review_text(src, "sketch.ino")["signals"]["has_flash_write"])

    def test_updater_write_8266(self):
        src = "void f(void){ Updater.write(b, n); }"
        self.assertTrue(A.review_text(src, "sketch.ino")["signals"]["has_flash_write"])

    def test_serial_print_is_log(self):
        src = 'void f(void){ Serial.println("x"); }'
        self.assertTrue(A.review_text(src, "sketch.ino")["signals"]["has_log"])

    def test_millis_is_timeout_baseline(self):
        src = "void f(void){ if (millis() - t0 > 5000) { return; } }"
        self.assertTrue(A.review_text(src, "sketch.ino")["signals"]["has_timeout"])

    def test_esp_wdt_signals(self):
        off = A.review_text("void f(void){ ESP.wdtDisable(); }", "sketch.ino")["signals"]
        fed = A.review_text("void f(void){ ESP.wdtFeed(); }", "sketch.ino")["signals"]
        self.assertTrue(off["has_wdt_off"])
        self.assertTrue(off["has_wdt_use"])
        self.assertTrue(fed["has_wdt_feed"])

    def test_preferences_is_state_save(self):
        src = 'void f(void){ Preferences p; p.putBool("ota_ok", true); }'
        self.assertTrue(A.review_text(src, "sketch.ino")["signals"]["has_state_save"])

    def test_update_end_true_is_integrity(self):
        src = "void f(void){ Update.end(true); }"
        self.assertTrue(A.review_text(src, "sketch.ino")["signals"]["has_integrity"])

    # ---- R15：关了看门狗不恢复 ----
    def test_r15_wdt_disabled_not_restored(self):
        src = "void ota(void){ ESP.wdtDisable(); Update.write(buf, n); }"
        self.assertIn(15, rule_ids(A.review_text(src, "sketch.ino")))

    def test_r15_ok_when_wdt_resorted(self):
        src = "void ota(void){ ESP.wdtDisable(); Update.write(buf, n); ESP.wdtFeed(); }"
        self.assertNotIn(15, rule_ids(A.review_text(src, "sketch.ino")))

    # ---- R15：重新武装（enable/start）也算恢复（2026-10-21）----
    # 修因：R15 的建议写法就是 wdt_enable / ESP.wdtEnable(0)，但 SIG_WDT_FEED
    # 里没有 enable 类词元——照抄修复建议仍被 R15 咬，建议与信号表自相矛盾。
    def test_r15_ok_when_wdt_enabled_generic(self):
        src = "void ota(void){ wdt_disable(); do_update(); wdt_enable(); }"
        self.assertNotIn(15, rule_ids(A.review_text(src, "boot.c")))

    def test_r15_ok_when_wdt_started(self):
        src = "void ota(void){ wdt_disable(); do_update(); WDT_Start(1000); }"
        self.assertNotIn(15, rule_ids(A.review_text(src, "boot.c")))

    def test_r15_ok_when_wdt_enabled_nrfx(self):
        src = "void ota(void){ nrfx_wdt_disable(&wdt); do_update(); nrfx_wdt_enable(&wdt); }"
        self.assertNotIn(15, rule_ids(A.review_text(src, "boot.c")))

    def test_r15_ok_when_esp_wdt_enabled(self):
        src = "void ota(void){ ESP.wdtDisable(); Update.write(buf, n); ESP.wdtEnable(0); }"
        self.assertNotIn(15, rule_ids(A.review_text(src, "sketch.ino")))

    def test_r15_still_reported_when_never_restored(self):
        """反面：关了看门狗且全文无 feed/enable/start 任一恢复动作 → 照报。"""
        src = "void ota(void){ wdt_disable(); do_update(); ESP.restart(); }"
        self.assertIn(15, rule_ids(A.review_text(src, "boot.c")))

    def test_r15_still_reported_when_only_wdt_use_no_restore(self):
        """反面：只有 wdt_init/wdt_config（配置不算恢复）→ 照报。"""
        src = "void ota(void){ wdt_disable(); do_update(); }"
        self.assertIn(15, rule_ids(A.review_text(src, "boot.c")))

    def test_r6_unaffected_by_rearm_signal(self):
        """关键边界：R6 的"喂狗"与 R15 的"恢复"是两个概念——ESP.wdtEnable(4000)
        算 R15 恢复信号，但绝不能豁免 R6（开着狗不喂仍要报）。"""
        src = "void ota(void){ ESP.wdtEnable(4000); Update.write(buf, n); }"
        self.assertIn(6, rule_ids(A.review_text(src, "sketch.ino")))
        self.assertNotIn(15, rule_ids(A.review_text(src, "sketch.ino")))

    def test_r6_not_fired_when_wdt_explicitly_disabled(self):
        """显式关掉看门狗时"不喂狗"是设计意图，R6 不该报（否则 Arduino 上恒误报）。"""
        src = "void ota(void){ ESP.wdtDisable(); Update.write(buf, n); }"
        self.assertNotIn(6, rule_ids(A.review_text(src, "sketch.ino")))

    def test_r6_still_fired_when_wdt_on_but_unfed(self):
        """反面：看门狗开着却不喂，R6 照常报——别借新豁免把能力削掉。"""
        src = "void ota(void){ ESP.wdtEnable(4000); Update.write(buf, n); }"
        self.assertIn(6, rule_ids(A.review_text(src, "sketch.ino")))

    # ---- R11：带类型的声明赋值必须豁免 ----
    def test_r11_typed_declaration_assignment_exempt(self):
        src = "void ota(void){ size_t w = Update.write(buf, n); }"
        self.assertNotIn(11, rule_ids(A.review_text(src, "sketch.ino")))

    def test_r11_bare_call_reported(self):
        src = "void ota(void){ Update.write(buf, n); }"
        self.assertIn(11, rule_ids(A.review_text(src, "sketch.ino")))

    # ---- R14：框架代管擦除 → 不计分提示，不是问题 ----
    def test_r14_framework_erase_becomes_note(self):
        src = ("void ota(void){ Update.begin(n, U_FLASH);"
               " Update.write(buf, n); Update.end(true); }")
        res = A.review_text(src, "sketch.ino")
        self.assertNotIn(14, rule_ids(res))
        self.assertTrue(any("擦除" in n["note"] for n in res["notes"]))

    def test_r14_still_reported_for_bare_metal(self):
        """反面：非框架代码里 R14 照常报——别借框架豁免把能力削掉。"""
        src = "void ota_apply(void){ ota_progress(1); flash_write(APP_ADDR, buf, len); }"
        self.assertIn(14, rule_ids(A.review_text(src, "ota.c")))

    # ---- .ino / .pde 纳入扫描范围 ----
    def test_ino_pde_in_source_exts(self):
        self.assertIn(".ino", A.SOURCE_EXTS)
        self.assertIn(".pde", A.SOURCE_EXTS)

    def test_directory_scan_picks_ino(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "ota_sketch.ino"), "w").write(
                "void ota(void){ Update.write(buf, n); }")
            res = A.review_directory(d)
            self.assertEqual(res["files_scanned"], 1)
            self.assertIn("ota_sketch.ino", [f["file"] for f in res["files"]])

    # ---- 端到端鉴别力：坏样本必须明显低于好样本（防"全盲"回归）----
    BAD_SKETCH = """
#include <WiFi.h>
#include <Update.h>

void do_ota(void) {
    HTTPClient http;
    Update.begin(fw_size, U_FLASH);
    ESP.wdtDisable();
    while (WiFi.status() != WL_CONNECTED) { delay(100); }
    while (http.connected()) {
        size_t n = stream->readBytes(buf, sizeof(buf));
        Update.write(buf, n);
    }
    Update.end(true);
    delay(1000);
    ESP.restart();
}
"""

    GOOD_SKETCH = """
#include <WiFi.h>
#include <Update.h>
#include <Preferences.h>

static bool ota_fetch_and_flash(size_t expect) {
    Preferences prefs;
    prefs.begin("ota", false);
    uint32_t boot_count = prefs.getUInt("boot_count", 0) + 1;
    prefs.putUInt("boot_count", boot_count);

    if (!Update.begin(expect, U_FLASH)) { Update.printError(Serial); return false; }
    unsigned long deadline = millis() + 120000;
    size_t written = 0;
    while (written < expect) {
        if (millis() > deadline) { Update.abort(); return false; }
        size_t w = Update.write(buf, n);
        if (w != n) { Update.abort(); return false; }
        written += w;
        Serial.printf("ota %u\\\\n", (unsigned)written);
        delay(2);
    }
    if (!Update.end(true)) { Update.rollBack(); return false; }
    return true;
}
"""

    def test_bad_vs_good_discrimination(self):
        """核心断言：坏草图必须比好草图明显差，且各自命中该命中的。
        修复前两者是 99 / 100 —— 等于没有鉴别力。"""
        bad = A.review_text(self.BAD_SKETCH, "bad.ino")
        good = A.review_text(self.GOOD_SKETCH, "good.ino")
        self.assertTrue(bad["signals"]["is_ota_ctx"], "坏样本必须判为 OTA 语境")
        self.assertTrue(good["signals"]["is_ota_ctx"], "好样本必须判为 OTA 语境")
        self.assertLessEqual(bad["score"], good["score"] - 10,
                             "坏样本与好样本必须拉开差距（实际 %d vs %d）"
                             % (bad["score"], good["score"]))
        for rid in (8, 9, 10, 11, 12, 15):
            self.assertIn(rid, rule_ids(bad), "坏样本应命中 R%d" % rid)
        for rid in (6, 8, 10, 11, 15):
            self.assertNotIn(rid, rule_ids(good), "好样本不该命中 R%d" % rid)


if __name__ == "__main__":
    warnings.simplefilter("ignore", ResourceWarning)
    unittest.main(verbosity=2)
