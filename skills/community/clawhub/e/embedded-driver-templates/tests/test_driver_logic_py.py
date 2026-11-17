# -*- coding: utf-8 -*-
"""
mcu-debug-mcp · 驱动纯函数逻辑的 Python 交叉验证（test_driver_logic_py.py）

为什么存在：本机沙箱阻止 gcc 子进程写盘，C 编译验证暂时无法执行。
做法：把 drivers/ 里 C 纯函数的算法用 Python 等价实现并对拍，
     期望值与 tests/test_driver_logic.c 中的 CHECK 完全一致（同源逻辑）。
验证状态：算法逻辑=本机 Python 实测通过；C 编译/运行验证=待 gcc 可用环境
     （tests/Makefile 已备好，运行：make -f Makefile.logic test）

对应 C 实现：drivers/dht11/dht11.c · drivers/hcsr04/hcsr04.c
"""

import unittest

# ---------- DHT11 decode_byte 等价实现（C: dht11_decode_byte） ----------
def dht11_decode_byte(durations):
    b = 0
    for d in durations:
        if d == 0:
            return -1
        if d <= 20:
            return -2
        if d >= 90:
            return -3
        b <<= 1
        if d > 45:
            b |= 1
    return b & 0xFF

def dht11_checksum(b5):
    return 0 if (sum(b5[:4]) & 0xFF) == b5[4] else -1

def dht11_decode_frame(d40):
    out = []
    for i in range(5):
        r = dht11_decode_byte(d40[i * 8:(i + 1) * 8])
        if r < 0:
            return r
        out.append(r)
    if dht11_checksum(out) != 0:
        return -2  # DHT11_ERR_CHECKSUM
    return out

# ---------- HC-SR04 换算等价实现（C: hcsr04_us_to_cm_x10） ----------
def hcsr04_us_to_cm_x10(us):
    MIN_US, MAX_US = 116, 23300
    if us < MIN_US or us > MAX_US:
        return -2  # HCSR04_ERR_PARAM
    return us * 1715 // 10000

class TestDht11Logic(unittest.TestCase):
    def test_byte_0(self):
        self.assertEqual(dht11_decode_byte([28] * 8), 0x00)

    def test_byte_1(self):
        self.assertEqual(dht11_decode_byte([70] * 8), 0xFF)

    def test_byte_mixed(self):
        self.assertEqual(dht11_decode_byte([70, 28, 28, 70, 28, 28, 70, 28]), 0x92)

    def test_byte_boundary_45us(self):
        self.assertEqual(dht11_decode_byte([45] * 8), 0x00)

    def test_byte_invalid(self):
        self.assertEqual(dht11_decode_byte([0, 28, 28, 28, 28, 28, 28, 28]), -1)
        self.assertEqual(dht11_decode_byte([15, 28, 28, 28, 28, 28, 28, 28]), -2)
        self.assertEqual(dht11_decode_byte([95, 28, 28, 28, 28, 28, 28, 28]), -3)

    def test_checksum(self):
        self.assertEqual(dht11_checksum([0x42, 0x00, 0x19, 0x00, 0x5B]), 0)
        self.assertEqual(dht11_checksum([0x42, 0x00, 0x19, 0x00, 0x5C]), -1)

    def test_frame_42h_25c(self):
        expect = [42, 0, 25, 0, 67]
        frame = []
        for byte in expect:
            for bit in range(7, -1, -1):
                frame.append(70 if (byte >> bit) & 1 else 28)
        self.assertEqual(dht11_decode_frame(frame), expect)

    def test_frame_corrupted(self):
        expect = [42, 0, 25, 0, 67]
        frame = []
        for byte in expect:
            for bit in range(7, -1, -1):
                frame.append(70 if (byte >> bit) & 1 else 28)
        frame[39] = 70 if frame[39] == 28 else 28
        self.assertEqual(dht11_decode_frame(frame), -2)

class TestHcsr04Logic(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(hcsr04_us_to_cm_x10(583), 99)      # ~10cm
        self.assertEqual(hcsr04_us_to_cm_x10(116), 19)      # ~2cm 下限
        self.assertEqual(hcsr04_us_to_cm_x10(23300), 3995)  # ~4m 上限

    def test_range_filter(self):
        self.assertEqual(hcsr04_us_to_cm_x10(100), -2)
        self.assertEqual(hcsr04_us_to_cm_x10(25000), -2)

# ==================== v2：新增 4 驱动交叉验证 ====================

# ---------- DS18B20（C: ds18b20_crc8 / raw_to_temp_x16 / is_reset_value） ----------
def ds18b20_crc8(data):
    crc = 0
    for b in data:
        for _ in range(8):
            mix = (crc ^ b) & 1
            crc >>= 1
            if mix:
                crc ^= 0x8C
            b >>= 1
    return crc

def ds18b20_raw_to_temp_x16(lsb, msb):
    v = (msb << 8) | lsb
    return v - 0x10000 if v >= 0x8000 else v

def ds18b20_is_reset_value(t_x16):
    return 1 if t_x16 == 850 * 16 // 10 else 0   # 1360 = 85.0°C

class TestDs18b20Logic(unittest.TestCase):
    def test_crc_single_byte(self):
        self.assertEqual(ds18b20_crc8([0x00]), 0x00)
        self.assertEqual(ds18b20_crc8([0x02]), 0xBC)

    def test_crc_zero_bytes(self):
        self.assertEqual(ds18b20_crc8([0x00] * 8), 0x00)

    def test_temp_positive(self):
        self.assertEqual(ds18b20_raw_to_temp_x16(0x91, 0x01), 401)   # 25.0625°C
        self.assertEqual(ds18b20_raw_to_temp_x16(0x00, 0x00), 0)

    def test_temp_negative_twos_complement(self):
        self.assertEqual(ds18b20_raw_to_temp_x16(0x5E, 0xFF), -162)  # -10.125°C
        self.assertEqual(ds18b20_raw_to_temp_x16(0x10, 0xFE), -496)  # -31.0°C

    def test_reset_value_85(self):
        self.assertEqual(ds18b20_is_reset_value(1360), 1)
        self.assertEqual(ds18b20_is_reset_value(400), 0)

# ---------- MPU6050（C: mpu6050_raw_to_mg / dps_centi / temp / static_check） ----------
def mpu6050_raw_to_mg(raw, fs_sel):
    return (raw * (2000 << fs_sel)) // 32768

def mpu6050_raw_to_dps_centi(raw, fs_sel):
    return (raw * (25000 << fs_sel)) // 32768

def mpu6050_temp_c_x100(raw):
    return raw * 10 // 34 + 3653

def mpu6050_static_check(ax, ay, az):
    sum2 = ax * ax + ay * ay + az * az
    g2 = 16384 * 16384
    return 1 if sum2 * 10000 >= g2 * 7225 and sum2 * 10000 <= g2 * 13225 else 0

class TestMpu6050Logic(unittest.TestCase):
    def test_accel_1g(self):
        self.assertEqual(mpu6050_raw_to_mg(16384, 0), 1000)
        self.assertEqual(mpu6050_raw_to_mg(-16384, 0), -1000)

    def test_accel_half_g(self):
        self.assertEqual(mpu6050_raw_to_mg(8192, 0), 500)

    def test_accel_scale_up(self):
        # ±4g 档：raw 16384 = 2g
        self.assertEqual(mpu6050_raw_to_mg(16384, 1), 2000)
        # ±16g 档满量程附近
        self.assertEqual(mpu6050_raw_to_mg(32767, 3), 32767 * 16000 // 32768)

    def test_gyro_1dps(self):
        self.assertEqual(mpu6050_raw_to_dps_centi(131, 0), 99)   # ≈1°/s（整数截断 99.97→99）

    def test_gyro_scale_up(self):
        self.assertEqual(mpu6050_raw_to_dps_centi(16384, 2), 16384 * 100000 // 32768)

    def test_temp_raw_zero(self):
        self.assertEqual(mpu6050_temp_c_x100(0), 3653)           # 36.53°C

    def test_temp_positive_raw(self):
        self.assertEqual(mpu6050_temp_c_x100(340), 3753)         # 37.53°C
        self.assertEqual(mpu6050_temp_c_x100(-340), 3553)        # 35.53°C

    def test_static_check(self):
        self.assertEqual(mpu6050_static_check(0, 0, 16384), 1)   # 静止 1g on z
        self.assertEqual(mpu6050_static_check(8192, 0, 14190), 1)  # 合成 ≈1g（斜放）
        self.assertEqual(mpu6050_static_check(0, 0, 0), 0)       # 全 0 不可能
        self.assertEqual(mpu6050_static_check(0, 0, 24576), 0)   # 1.5g 超容差

# ---------- ESP8266-AT（C: esp8266_classify_line / cwjap_err / ipd_parse） ----------
def esp8266_classify_line(line):
    t = line.lstrip("\r\n \t")
    if t.startswith("OK"): return "OK"
    if t.startswith("ERROR"): return "ERROR"
    if t.startswith("FAIL"): return "FAIL"
    if t.startswith("WIFI CONNECTED"): return "WIFI_CONNECTED"
    if t.startswith("WIFI GOT IP"): return "WIFI_GOT_IP"
    if t.startswith("WIFI DISCONNECT"): return "WIFI_DISCONNECT"
    if t.startswith("+IPD,"): return "IPD"
    if t.startswith("+CME ERROR"): return "CME_ERROR"
    if t.startswith("busy "): return "BUSY"
    if t.startswith(">"): return "SEND_PROMPT"
    return "OTHER"

def esp8266_cwjap_err(code):
    return {1: 1, 2: 2, 3: 3, 4: 4}.get(code, -1)

def esp8266_ipd_parse(line):
    line = line.lstrip("\r\n")
    if not line.startswith("+IPD,"):
        return -1
    p = 5
    a, has = 0, False
    while p < len(line) and line[p].isdigit():
        a = a * 10 + int(line[p]); has = True; p += 1
    if not has:
        return -1
    if p < len(line) and line[p] == ",":
        p += 1
        b, hasb = 0, False
        while p < len(line) and line[p].isdigit():
            b = b * 10 + int(line[p]); hasb = True; p += 1
        if not hasb or p >= len(line) or line[p] != ":":
            return -1
        return (a, b, p + 1)   # (ch, len, data_off)
    if p >= len(line) or line[p] != ":":
        return -1
    return (-1, a, p + 1)      # (ch=-1 单连接, len, data_off)

class TestEsp8266AtLogic(unittest.TestCase):
    def test_classify_all_types(self):
        self.assertEqual(esp8266_classify_line("OK\r\n"), "OK")
        self.assertEqual(esp8266_classify_line("ERROR\r\n"), "ERROR")
        self.assertEqual(esp8266_classify_line("WIFI CONNECTED\r\n"), "WIFI_CONNECTED")
        self.assertEqual(esp8266_classify_line("WIFI GOT IP\r\n"), "WIFI_GOT_IP")
        self.assertEqual(esp8266_classify_line("WIFI DISCONNECT\r\n"), "WIFI_DISCONNECT")
        self.assertEqual(esp8266_classify_line("+IPD,12:hello"), "IPD")
        self.assertEqual(esp8266_classify_line("+CME ERROR: 3\r\n"), "CME_ERROR")
        self.assertEqual(esp8266_classify_line("busy p...\r\n"), "BUSY")
        self.assertEqual(esp8266_classify_line(">\r\n"), "SEND_PROMPT")
        self.assertEqual(esp8266_classify_line("AT+RST\r\n"), "OTHER")

    def test_cwjap_err_map(self):
        self.assertEqual(esp8266_cwjap_err(1), 1)
        self.assertEqual(esp8266_cwjap_err(2), 2)
        self.assertEqual(esp8266_cwjap_err(5), -1)

    def test_ipd_single_conn(self):
        r = esp8266_ipd_parse("+IPD,12:hello,world!")
        self.assertEqual(r, (-1, 12, 8))   # "+IPD,12:" 共 8 字符，data 从下标 8

    def test_ipd_multi_conn(self):
        r = esp8266_ipd_parse("+IPD,0,5:hello")
        self.assertEqual(r, (0, 5, 9))     # "+IPD,0,5:" 共 9 字符

    def test_ipd_malformed(self):
        self.assertEqual(esp8266_ipd_parse("garbage"), -1)
        self.assertEqual(esp8266_ipd_parse("+IPD,abc"), -1)
        self.assertEqual(esp8266_ipd_parse("+IPD,12"), -1)   # 缺冒号

# ---------- SSD1306（C: ssd1306_coord_to_fb / fb_set_pixel / ascii_index） ----------
SSD1306_W, SSD1306_H = 128, 64

def ssd1306_coord_to_fb(x, y):
    if x >= SSD1306_W or y >= SSD1306_H:
        return -1
    return (y // 8) * SSD1306_W + x, y % 8

def ssd1306_ascii_index(c):
    if c < ' ' or c > '~':
        return 0
    return ord(c) - 32

class TestSsd1306Logic(unittest.TestCase):
    def test_coord_origin(self):
        self.assertEqual(ssd1306_coord_to_fb(0, 0), (0, 0))

    def test_coord_page_cross(self):
        # (5, 9)：第 2 页（page=1）第 5 列，位 1
        self.assertEqual(ssd1306_coord_to_fb(5, 9), (128 + 5, 1))

    def test_coord_max(self):
        self.assertEqual(ssd1306_coord_to_fb(127, 63), (1023, 7))

    def test_coord_oob(self):
        self.assertEqual(ssd1306_coord_to_fb(128, 0), -1)
        self.assertEqual(ssd1306_coord_to_fb(0, 64), -1)

    def test_ascii_index(self):
        self.assertEqual(ssd1306_ascii_index(' '), 0)
        self.assertEqual(ssd1306_ascii_index('A'), 33)
        self.assertEqual(ssd1306_ascii_index('~'), 94)
        self.assertEqual(ssd1306_ascii_index('\n'), 0)   # 非可打印映射空格

# ==================== v3：新增 3 驱动交叉验证 ====================

# ---------- SG90（C: servo_angle_to_pulse_us / servo_pulse_to_ccr） ----------
def servo_angle_to_pulse_us(angle):
    if angle < 0:
        return -1
    if angle > 180:
        return -2
    return 500 + angle * 2000 // 180

def servo_pulse_to_ccr(pulse_us, tim_clk_hz, psc, arr):
    tick_hz = tim_clk_hz // (psc + 1)
    period_us = (arr + 1) * 1000000 // tick_hz
    if period_us < 19000 or period_us > 21000:
        return -1
    ccr = pulse_us * tick_hz // 1000000
    if ccr > arr + 1:
        return -2
    return ccr

class TestServoSg90Logic(unittest.TestCase):
    def test_angle_endpoints(self):
        self.assertEqual(servo_angle_to_pulse_us(0), 500)
        self.assertEqual(servo_angle_to_pulse_us(180), 2500)

    def test_angle_middle(self):
        self.assertEqual(servo_angle_to_pulse_us(90), 1500)   # 中位
        self.assertEqual(servo_angle_to_pulse_us(45), 1000)

    def test_angle_out_of_range(self):
        self.assertEqual(servo_angle_to_pulse_us(-1), -1)
        self.assertEqual(servo_angle_to_pulse_us(181), -2)

    def test_ccr_standard_72m(self):
        # 72MHz / 72 = 1MHz tick，ARR=19999 → 20ms：经典 STM32 配置
        self.assertEqual(servo_pulse_to_ccr(1500, 72000000, 71, 19999), 1500)
        self.assertEqual(servo_pulse_to_ccr(500, 72000000, 71, 19999), 500)

    def test_ccr_wrong_period(self):
        # ARR=19999 但 PSC=35 → 2MHz tick → 周期 10ms ≠ 50Hz：直接报错
        self.assertEqual(servo_pulse_to_ccr(1500, 72000000, 35, 19999), -1)

# ---------- 28BYJ-48（C: stepper_steps_per_rev / angle_to_steps / phase / rpm） ----------
def stepper_steps_per_rev(halfstep):
    return 4076 if halfstep else 2038     # 精确减速比 63.684:1

def stepper_angle_to_steps(angle, halfstep):
    spr = stepper_steps_per_rev(halfstep)
    n = angle * spr
    if n >= 0:
        return (n + 180) // 360
    return -((-n + 180) // 360)

HALF_SEQ = [0x1, 0x3, 0x2, 0x6, 0x4, 0xC, 0x8, 0x9]
FULL_SEQ = [0x3, 0x6, 0xC, 0x9]

def stepper_phase_pattern(idx, halfstep):
    return (HALF_SEQ if halfstep else FULL_SEQ)[idx % (8 if halfstep else 4)]

def stepper_rpm_to_delay_us(rpm, halfstep):
    if rpm <= 0:
        return -1
    if rpm > 18:
        return -2
    return 60000000 // (rpm * stepper_steps_per_rev(halfstep))

class TestStepperLogic(unittest.TestCase):
    def test_steps_per_rev(self):
        self.assertEqual(stepper_steps_per_rev(1), 4076)
        self.assertEqual(stepper_steps_per_rev(0), 2038)

    def test_angle_quarter(self):
        self.assertEqual(stepper_angle_to_steps(90, 1), 1019)   # 4076/4
        self.assertEqual(stepper_angle_to_steps(90, 0), 510)    # 509.5 四舍五入

    def test_angle_full_rev(self):
        self.assertEqual(stepper_angle_to_steps(360, 1), 4076)

    def test_angle_negative(self):
        self.assertEqual(stepper_angle_to_steps(-90, 1), -1019)

    def test_phase_halfstep_cycle(self):
        self.assertEqual([stepper_phase_pattern(i, 1) for i in range(8)], HALF_SEQ)
        self.assertEqual(stepper_phase_pattern(8, 1), HALF_SEQ[0])   # 回到起点

    def test_phase_fullstep(self):
        self.assertEqual([stepper_phase_pattern(i, 0) for i in range(4)], FULL_SEQ)

    def test_rpm_delay(self):
        self.assertEqual(stepper_rpm_to_delay_us(15, 1), 981)    # 6e7/(15*4076)
        self.assertEqual(stepper_rpm_to_delay_us(0, 1), -1)
        self.assertEqual(stepper_rpm_to_delay_us(60, 1), -2)     # 超转矩

# ---------- HC-05（C: hc05_classify / hc05_error_detail / hc05_uart_cmd） ----------
HC05_BAUDS = [1200, 2400, 4800, 9600, 19200, 38400,
              57600, 115200, 230400, 460800, 921600, 1382400]

def hc05_classify(line):
    if line is None:
        return "IGNORE"
    t = line.lstrip(" \t")
    if not t:
        return "IGNORE"
    if t == "OK":
        return "OK"
    if t.startswith("ERROR"):
        return "ERROR"
    if t == "FAIL":
        return "FAIL"
    if t.startswith("+"):
        return "DATA"
    return "UNKNOWN"

def hc05_error_detail(line):
    import re
    m = re.search(r"ERROR:\((\d+)\)", line)
    if not m:
        return -1
    n = int(m.group(1))
    return n if 0 < n <= 255 else -1

def hc05_uart_cmd(baud, stop, parity):
    if baud not in HC05_BAUDS:
        return -2
    if stop not in (0, 1):
        return -3
    if parity not in (0, 1, 2):
        return -4
    return "AT+UART=%d,%d,%d\r\n" % (baud, stop, parity)

class TestHc05Logic(unittest.TestCase):
    def test_classify_all_types(self):
        self.assertEqual(hc05_classify("OK"), "OK")
        self.assertEqual(hc05_classify("ERROR"), "ERROR")
        self.assertEqual(hc05_classify("ERROR:(1)"), "ERROR")
        self.assertEqual(hc05_classify("FAIL"), "FAIL")
        self.assertEqual(hc05_classify("+NAME:HC-05"), "DATA")
        self.assertEqual(hc05_classify("+VERSION:2.0-20100653"), "DATA")
        self.assertEqual(hc05_classify(""), "IGNORE")
        self.assertEqual(hc05_classify(None), "IGNORE")
        self.assertEqual(hc05_classify("hello"), "UNKNOWN")

    def test_error_detail(self):
        self.assertEqual(hc05_error_detail("ERROR:(1)"), 1)
        self.assertEqual(hc05_error_detail("ERROR:(4)"), 4)
        self.assertEqual(hc05_error_detail("ERROR:"), -1)
        self.assertEqual(hc05_error_detail("OK"), -1)

    def test_uart_cmd_valid(self):
        self.assertEqual(hc05_uart_cmd(9600, 0, 0), "AT+UART=9600,0,0\r\n")
        self.assertEqual(hc05_uart_cmd(115200, 1, 2), "AT+UART=115200,1,2\r\n")

    def test_uart_cmd_invalid(self):
        self.assertEqual(hc05_uart_cmd(1234, 0, 0), -2)   # 不在支持列表
        self.assertEqual(hc05_uart_cmd(9600, 2, 0), -3)
        self.assertEqual(hc05_uart_cmd(9600, 0, 5), -4)

if __name__ == "__main__":
    unittest.main(verbosity=2)
