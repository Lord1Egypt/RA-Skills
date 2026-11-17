---
name: embedded-driver-templates
version: 1.0.1
slug: embedded-driver-templates
displayName: 嵌入式驱动模板库
summary: 9 款预验证驱动模板（DHT11/DS18B20/MPU6050/SSD1306 等），带验证记录+接线表+坑清单，C99 平台无关移植参考。
display_name: 嵌入式驱动模板库
display_name_en: Embedded Driver Templates
description: 预验证驱动模板与外设初始化顺序查询工具——算法层纯 C99 平台无关，平台差异全部收在 port 适配层（示例给 STM32 HAL，dht11 另附 Arduino 写法，换其它平台照此自己写）。当用户要移植常用驱动——DHT11、DS18B20、HC-05、HC-SR04、MPU6050、SSD1306、SG90 舵机、28BYJ-48 步进、ESP8266-AT——或问这个驱动占哪些外设、初始化顺序有什么硬要求、接线怎么接有什么坑、换一块芯片怎么改时使用。9 款驱动全部带验证记录+接线表+坑清单，外设用法取自各驱动适配层注释原句。模板是移植参考非即拷即用；不生成新驱动代码（用 embedded-code-generator）、不做协议一致性判定与报文拆解（随嵌入式联调专家包提供）。
author: fangcun
agent_created: true
examples_zh:
- "MPU6050 接 I2C 哪些脚，移植要注意什么"
- "有没有现成的 SSD1306 OLED 驱动"
- "DHT11 读出来全是 0 是怎么回事"
examples_en:
- "Which pins does MPU6050 use on I2C and what should I watch when porting?"
- "Is there a ready-made SSD1306 OLED driver I can reuse?"
- "My DHT11 always reads zero - what am I missing?"
description_zh: 预验证驱动模板库：覆盖 DHT11、DS18B20、ESP8266-AT、HC-05、HC-SR04、MPU6050、SG90、SSD1306 与 28BYJ-48 步进电机九类毕设常用模块，每个模块含可编译源码、移植端口文件、接线说明与避坑清单，另附外设初始化顺序查询，移植驱动或排查初始化问题时直接取用。
description_en: 9 verified driver templates (DHT11 / DS18B20 / ESP8266-AT / HC-05 / HC-SR04 / MPU6050 / SG90 / SSD1306 / 28BYJ-48) with verification records, wiring guides and pitfall lists, plus the peripheral-init-order layer derived from each driver's *_port.h porting notes. Engine identical to mcu-debug-mcp v4.5.4. Reference for porting, not turnkey projects; no new driver generation (embedded-code-generator).
license: MIT
compatibility: 需要 Python 3.9+，仅使用标准库，无需联网。纯知识检索，不执行用户代码、不访问硬件。
metadata:
  author: fangcun
  version: "1.0.1"
---


# Embedded Driver Templates

Pre-verified driver templates for nine common modules (DHT11, DS18B20, ESP8266 AT, HC-05, HC-SR04, MPU6050, SG90, SSD1306, stepper). Each template ships with a build test bench and a pitfall checklist; port layers keep hardware-specific code isolated.

## How to Use

Load this skill and state your concrete inputs. The bundled references, scripts and templates carry the detailed rules and worked examples; the assistant should consult them before answering.

## Bundled Resources

- `README_____.md`
- `assets/dht11__dht11.c`
- `assets/dht11__dht11.h`
- `assets/dht11__dht11_port.h`
- `assets/dht11__meta.json`
- `assets/dht11__wiring.md`
- `assets/ds18b20__ds18b20.c`
- `assets/ds18b20__ds18b20.h`
- `assets/ds18b20__ds18b20_port.h`
- `assets/ds18b20__meta.json`
- `assets/ds18b20__wiring.md`
- `assets/esp8266at__esp8266at.c`
- `assets/esp8266at__esp8266at.h`
- `assets/esp8266at__esp8266at_port.h`
- `assets/esp8266at__meta.json`
- `assets/esp8266at__wiring.md`
- `assets/hc05__hc05.c`
- `assets/hc05__hc05.h`
- `assets/hc05__hc05_port.h`
- `assets/hc05__meta.json`
- `assets/hc05__wiring.md`
- `assets/hcsr04__hcsr04.c`
- `assets/hcsr04__hcsr04.h`
- `assets/hcsr04__hcsr04_port.h`
- `assets/hcsr04__meta.json`
- `assets/hcsr04__wiring.md`
- `assets/mpu6050__meta.json`
- `assets/mpu6050__mpu6050.c`
- `assets/mpu6050__mpu6050.h`
- `assets/mpu6050__mpu6050_port.h`
- `assets/mpu6050__wiring.md`
- `assets/servo_sg90__meta.json`
- `assets/servo_sg90__servo_sg90.c`
- `assets/servo_sg90__servo_sg90.h`
- `assets/servo_sg90__servo_sg90_port.h`
- `assets/servo_sg90__wiring.md`
- `assets/ssd1306__meta.json`
- `assets/ssd1306__ssd1306.c`
- `assets/ssd1306__ssd1306.h`
- `assets/ssd1306__ssd1306_port.h`
- `assets/ssd1306__wiring.md`
- `assets/stepper_28byj48__meta.json`
- `assets/stepper_28byj48__stepper_28byj48.c`
- `assets/stepper_28byj48__stepper_28byj48.h`
- `assets/stepper_28byj48__stepper_28byj48_port.h`
- `assets/stepper_28byj48__wiring.md`
- `scripts/driver_templates.py`
- `scripts/engine.py`
- `tests/Makefile.logic`
- `tests/run_c_tests.py`
- `tests/test_driver_logic.c`
- `tests/test_driver_logic_py.py`
- `tests/stub/dht11_port.h`
- `tests/stub/ds18b20_port.h`
- `tests/stub/hc05_port.h`
- `tests/stub/hcsr04_port.h`
- `tests/stub/mpu6050_port.h`
- `tests/stub/port_all.h`
- `tests/stub/servo_sg90_port.h`
- `tests/stub/ssd1306_port.h`
- `tests/stub/stepper_28byj48_port.h`

## Notes

This package is a static knowledge and tooling bundle. It does not call external services, does not place orders or trades, and makes no return promises. Verify any hardware-specific values against the official datasheet for your part.

Author: fangcun. License: MIT.
