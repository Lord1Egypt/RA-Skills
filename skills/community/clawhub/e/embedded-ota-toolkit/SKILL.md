---
name: embedded-ota-toolkit
version: 1.2.0
display_name: 嵌入式OTA升级工具包
display_name_en: Embedded OTA / Bootloader Toolkit
description_zh: 让固件升级别变砖：15 条防砖规则审计 IAP/OTA 升级代码（跳转未设VTOR、未关中断、升级无CRC、擦写未喂狗等），每条附可直接粘贴的修复代码；另配 CRC 计算、分区规划、镜像打包与校验工具，覆盖 Cortex-M/RISC-V 与 Arduino/ESP8266，一键中文 HTML 报告。
description_en: Brick-prevention audit engine for OTA/bootloader code with 15 rules covering VTOR relocation, interrupt masking, image validation, CRC integrity, watchdog feeding, watchdog restore and erase-before-write, for bare-metal Cortex-M/RISC-V as well as the Arduino and ESP8266 frameworks, plus tooling for CRC, image headers, partition layout and package verification. Emits a shareable HTML report.
description: 嵌入式 OTA/Bootloader 升级链路检查与打包工具。审计侧静态扫描升级代码的防砖漏洞（每条附可直接粘贴的修复代码）：跳转 APP 未重定位中断向量表（VTOR）、跳转前未关中断、未校验 APP 有效性、升级数据无 CRC/哈希、flash 擦除地址未按页对齐、擦写期间未喂看门狗、分区地址硬编码、接收等待无超时、无防降级版本校验、升级状态未持久化、写入前未擦除、关闭看门狗后未恢复等；工具侧计算 CRC32/CRC16、算分区表并生成 .h、生成 64 字节镜像头、打包升级包 .pkg、校验包完整性。当用户要做 IAP/OTA 升级、bootloader 开发与跳转、固件打包、分区规划、远程或本地固件升级、升级后变砖跑飞死机排查、毕设要做固件升级/远程升级、需检查升级流程安全性时使用；原生支持裸机 Cortex-M/RISC-V 与 Arduino/ESP8266 框架写法（认 ArduinoOTA、Update、ESPhttpUpdate、ESP.wdt*、Serial.*、delay、millis）。已配套 190 项测试（145 审计 + 45 工具）。
author: fangcun
---


# Embedded OTA / Bootloader Upgrade Toolkit

Two tools, one goal: **never brick a device during firmware upgrade**.

- `ota_audit.py` — audit side: statically scans upgrade code and reports brick-vulnerable spots by severity (no compiling, no hardware)
- `ota_tool.py` — tool side: CRC, 64-byte image header generation, partition layout, `.pkg` packing, verification

**Platform coverage**: the auditor targets the **full Cortex-M family** (ST STM32 / GD32 / CH32 / APM32 / Nordic nRF5x / NXP / Renesas RA...), **RISC-V**, and the **Arduino / ESP8266 framework layer** (ESP32 built with Arduino uses vocabulary entirely different from ESP-IDF — adapted separately). Rule signals recognize ST HAL, GD32 FMC, Nordic nrfx, ESP-IDF, Zephyr, MCUboot, Arduino/ESP8266 and generic naming. The tool side (`ota_tool.py`) is **pure byte arithmetic, completely MCU-agnostic**. See "Platform Applicability" below.

## When to Use It

- **Dead on first interrupt after upgrade**: forgot `SCB->VTOR` relocation before jumping to APP — all APP interrupts land in the bootloader vector table. Rule 1.
- **Bricked by banked upgrades**: jumping with an empty/half-flashed APP partition — instant HardFault. Rule 3.
- **"Boots but misbehaves"**: received data written to flash without verification — transmission errors became firmware. Rule 4.
- **Watchdog kills upgrade mid-flash**: multi-second erase/write without feeding the dog — every failure is another brick chance. Rule 6.
- **"Upgrade succeeded but firmware is broken"**: NOR flash can only write 1-to-0; writing a page without erasing first corrupts it. Rule 14.
- **Don't know what goes in the header**: an industrially adequate 64-byte image header format + generator + verifier.

## 30-Second Demo

Feed in a realistic IAP jump + upgrade write:

```c
/* bootloader.c */
#define APP_BASE 0x08008000

void iap_load_app(void) {
    typedef void (*app_fn)(void);
    app_fn app = (app_fn)APP_BASE;
    __set_MSP(*(volatile uint32_t *)APP_BASE);
    app();
}

void ota_write_image(uint8_t *buf, uint32_t len) {
    flash_erase(0x08008100);
    flash_write(APP_BASE, buf, len);
    HAL_Delay(100);
}
```

Audit output (**score 49/100**, 4 critical, 4 major, 3 minor):

| Rule | Sev | Line | Issue |
|------|-----|------|-------|
| R1 | CRIT | L7 | Vector table not relocated before APP jump (no `SCB->VTOR` anywhere) |
| R2 | CRIT | L7 | Interrupts not disabled before jump (no `__disable_irq`) |
| R3 | CRIT | L7 | APP validity not checked before jump (no SP/vector sanity) |
| R4 | CRIT | L13 | Upgrade data has no integrity check (flash write without CRC) |
| R5 | MAJ | L12 | Erase address `0x08008100` not 1K/2K/4K aligned |
| R7 | MAJ | L12 | Hardcoded partition address (bare `0x08xxxxxx`) |
| R9 | MAJ | all | No anti-rollback version check |
| R10 | MAJ | all | Upgrade state not persisted (no resume after power loss) |
| R11 | MIN | L13 | Flash write return value unchecked |
| R12 | MIN | all | No progress output in upgrade flow |
| R13 | MIN | L14 | Hardcoded delay inside upgrade flow |

## Quick Start

**Audit**

```bash
python ota_audit.py bootloader.c                     # single file
python ota_audit.py bootloader.c high                # critical only
python ota_audit.py sketch.ino                       # Arduino sketch (.ino/.pde)
python ota_audit.py --dir ./boot                     # directory (.c/.h/.cpp/.hpp/.cc/.cxx/.ino/.pde)
python ota_audit.py --dir ./boot --html report.html  # HTML report
python ota_audit.py --dir ./boot --fail-under 80     # CI gate: score < 80 exits 1
```

Exit codes: 0 = clean, 1 = findings, 2 = usage/internal error (CI friendly; `--fail-under N` gates by score).

**Pack**

```bash
# 1) CRC
python ota_tool.py crc app.bin

# 2) Partition layout (generates .h with compile-time overflow asserts)
python ota_tool.py layout --flash 256K --align 2K boot:32K app:96K app_bak:96K cfg:8K --out partition.h

# 3) Pack (bin + 64B header), also emits MCU-side header
python ota_tool.py pack app.bin -o app.pkg --addr 0x08008000 --ver 1.2.3 --hw-id 0x0001 --emit-header

# 4) Verify (expected board/address guards against cross-flashing)
python ota_tool.py verify app.pkg --hw-id 0x0001 --addr 0x08008000
```

Exit codes: 0 = success, 1 = verification failed, 2 = usage error.

> What the tools cannot see: `references/ota-checklist.md` is the manual pre-flight checklist (power-cut / disconnect / wrong-packet fault injections), each item annotated with covering rules (`[R1]`...`[R15]`) and what must be tested on real hardware (`[HIL]`).

## End-to-End Path for New Projects

1. **Plan partitions**: `ota_tool.py layout` computes the table and generates `partition.h` (with compile-time overflow asserts); bootloader and APP both take address macros from it — stop hand-writing bare addresses.
2. **Self-audit after writing upgrade code**: `ota_audit.py bootloader.c --html report.html`; clear criticals to 0 and score >= 80 before flashing. Every finding ships paste-ready fix code.
3. **Package delivery**: `ota_tool.py pack app.bin --emit-header` produces `.pkg` + MCU-side parsing header.
4. **Last step before flashing**: `ota_tool.py verify app.pkg --hw-id 0x0001 --addr 0x08008000` confirms package integrity and board/address match; then run the power-cut/disconnect/wrong-packet injections from `ota-checklist.md` on real hardware.

## Audit Rules Quick Reference (15)

| # | Sev | Rule | One-liner |
|---|-----|------|-----------|
| 1 | CRIT | Jump without VTOR relocation | Must `SCB->VTOR = APP_ADDR` before jumping |
| 2 | CRIT | Interrupts not disabled before jump | Need `__disable_irq()` + clear NVIC pending |
| 3 | CRIT | APP validity unchecked | SP must land in SRAM, reset vector in flash |
| 4 | CRIT | No integrity check on upgrade data | Compare CRC/hash before/after flash write |
| 5 | MAJ | Erase address not page-aligned | Not a 1K/2K/4K multiple — erases the wrong page |
| 6 | MAJ | Watchdog not fed during flash | WDT enabled but not fed = guaranteed reset |
| 7 | MAJ | Hardcoded partition address | Bare `0x08xxxxxx`; use partition macros |
| 8 | MAJ | Receive wait without timeout | `while(!rx_done)` forever — disconnect = brick |
| 9 | MAJ | No anti-rollback check | Missing version compare — vulnerable firmware can be reflashed |
| 10 | MAJ | Upgrade state not persisted | State in RAM only — lost on power cut |
| 11 | MIN | Flash write return unchecked | Write failures must not be silent |
| 12 | MIN | No progress output | Field debugging becomes guesswork |
| 13 | MIN | Hardcoded delays | Magic-number delays break on other platforms |
| 14 | MAJ | No erase seen before write | NOR is 1-to-0 only; un-erased page = corrupt |
| 15 | MAJ | Watchdog not restored after disable | Disabled WDT never re-enabled = unbootable after upgrade |

**Judgment calibration** (highlights):

- Upgrade-chain rules (R4, R6, R8-R15) are gated on "OTA-context keywords or jump evidence"; ordinary business code (e.g. storing config to flash) will not be spammed by upgrade rules — deliberate false-positive governance.
- Context keywords match on "previous char is not alphanumeric" rather than ``: real code almost always uses underscore prefixes (`esp_ota_write` / `nrf_dfu_flash_store` / `gd32_ota_apply`), and `` silently kills the whole rule set; `quota` still won't match.
- Framework-layer context additionally recognizes camelCase and dotted forms: `ArduinoOTA` / `ESPhttpUpdate` / `Update.begin(` / `Updater.write(` — a separate case-sensitive regex (case-insensitive would swallow the lowercase `ota` inside `quota`). A pure `ArduinoOTA` sketch (begin in setup, handle in loop) has no standalone ota token and would score a fake 100 without this.
- "Jump evidence" must be call-shaped: `__set_MSP(`, `jump_to_app(`, `((void(*)(void))addr)()`, `asm volatile("mov pc, ...")`. A variable named `start_app` or a vector-table initializer does not count.
- **Cross-file suspicion downgrade**: when this file lacks a step but evidence exists that an external module handles it (`#include "image.h"`, `verify_*()`, custom `IV[]` table, `*_partition_state()`), report as minor tagged "verify manually — likely done externally"; without such evidence still report critical (tests cover both).
- **Framework-managed downgrades to notes (unscored)**: Arduino's erase happens inside the `Update` library — structurally invisible in a sketch, so R14 emits a note instead of a finding.
- R13 only flags magic delays replacing timeouts: `<50ms` delays treated as yield/throttle; delays already guarded by `millis()`/`deadline`/`HAL_GetTick` not flagged; delays in Arduino `loop()` are idle metronomes.
- R5 (erase misalignment) and R7 (bare flash address) are generic flash hygiene: always reported, upgrade or not.

## Platform Applicability (honest version)

| Layer | Applies to | Notes |
|---|---|---|
| Tool side `ota_tool.py` | **Any platform** | CRC32/CRC16/MD5/SHA256, 64B header, layout math, pack/verify — pure bytes |
| Audit, architecture rules R1 R2 R3 R8 R9 R12 | **All Cortex-M + RISC-V** | Standard constructs: `SCB->VTOR` / `__set_MSP` / `__disable_irq` / `CPSID i`; RISC-V recognizes `csrw mtvec` |
| Audit, peripheral rules R4 R5 R6 R7 R11 R13 R14 R15 | **Depends on platform naming** | Covers ST HAL/SPL, GD32 FMC, Nordic nrfx, ESP-IDF, Zephyr/MCUboot, Arduino/ESP8266, generic naming |
| Audit, framework layer | **Arduino / ESP8266** | Vocabulary entirely different from ESP-IDF — separately adapted |

**Known platform limits (stated plainly)**:

- R7 (bare flash address) only recognizes the `0x08xxxxxx` family (ST/GD32/CH32/APM32). nRF52 (base 0x0) and ESP32 (0x10000) will **not** trigger it — a miss, not a false positive.
- ESP32 has no `SCB->VTOR` semantics (image header + MMU boot); R1/R2/R3 don't apply and are not misreported (tested).
- Framework-managed bootloaders (mbed): no jump trio in-file; notes emitted, not findings.
- Arduino audits the sketch layer only: erase/verify live in the `Update` library, so R14 becomes a note and `Update.end(true)` serves as R4 evidence. "No R4/R14 on Arduino" means the sketch didn't miss it — not that the library is sound.
- AVR Arduino (Uno/Nano/Mega): no self-upgrade capability — classified non-OTA, score 100 means "nothing to audit", not "code is safe".
- **No "full coverage" claims**: unrecognized platform API naming means rules silently don't fire (inflated score). Check the JSON `signals` field when unsure.

Cross-platform recall was verified, not claimed: four platforms each got a deliberately broken bootloader — all caught. See the corpus section in the CN documentation (`references/CHANGELOG.md`) for the reproduction matrix: MCUboot/wolfBoot/Adafruit/ESP-IDF/Zephyr/mbed mature bootloaders score 100 (or 97-98 with "manual confirm"), ST's own IAP examples score 80 with real R1+R2 findings, and minimal bad samples on nRF52/ESP-IDF/RISC-V/GD32 all hit their expected rules. The famous lesson: `` word boundaries made the entire rule set silently fail on `esp_ota_write`-style underscore prefixes (fake 100s), and only real bad-sample cross-platform testing exposed it — then `ArduinoOTA` camelCase exposed the second variant of the same pit.

## Image Header Format (64 bytes, little-endian)

| Offset | Type | Field | Notes |
|--------|------|-------|-------|
| 0 | u32 | magic | `0x50555746` (ASCII "FWUP") |
| 4 | u16 | header_ver | format version, currently 1 |
| 6 | u16 | hw_id | hardware ID, anti cross-flash |
| 8 | u32 | fw_ver | `major<<16 \| minor<<8 \| patch` |
| 12 | u32 | load_addr | image load address |
| 16 | u32 | image_size | image bytes |
| 20 | u32 | image_crc | image CRC32 |
| 24 | u32 | header_crc | header's own CRC32 (zero this field while computing) |
| 28 | u32 | timestamp | pack UTC timestamp |
| 32 | u32 | flags | bit0=force upgrade, bit1=allow downgrade |
| 36 | u8[28] | reserved | zeros |

Note: MCU-side parsing must use `OTA_HEADER_SIZE` (64), never `sizeof(ota_image_header_t)` (struct padding varies).

## Output

Audit JSON: `summary{high,medium,low,total}` + `issues[]{rule_id,severity,line,title,description,suggestion}` + `notes[]{line,note}` (unscored) + `score` (starts 100; critical -8 / major -4 / minor -1) + `signals`. `--dir` adds `top5_files`; `--html` sets `html_report` in the JSON.

Pack JSON: `package/package_size/image/image_size/load_addr/fw_version/hw_id/image_crc32`.

## Reliability and Known Boundaries

- **190 test assertions** (145 audit + 45 tool) all passing; every rule has positive and negative cases, including "well-formed bootloaders must score 100" anti-false-positive floor tests and regressions consolidated from real open-source code (vector-table init is not a jump, HAL function definitions don't trigger R11, flash writes inside macros don't trigger R11, menu/LED feedback counts as progress, cross-file downgrade cases, recall cases for Nordic/ESP-IDF/RISC-V/GD32, 26 Arduino/ESP8266 framework cases including "bad sketch must score >=10 points below good sketch").
- **De-noising**: code inside block/line comments and string literals doesn't count as signals; jumps inside inline asm (`asm volatile("mov pc, ...")`) are separately extracted so de-noising doesn't kill them.
- **Known boundaries (deliberate)**: static text analysis only — no dataflow/controlflow. Cross-file division of labor reports minor "manual confirm" rather than asserting critical. R5 only checks constant erase addresses. R7 reports once per file. Pure-assembly jump files (.s/.asm) not scanned.
- **Gating scope**: R1-R3 only with jump evidence; R4, R6, R8-R15 gated on OTA context keywords (ota/iap/dfu/firmware/upgrade/bootloader, underscore and camel prefixes allowed) or jump evidence. R5 and R7 are generic hygiene — always reported; R7 recognizes only `0x08xxxxxx`.
- Does not replace on-target testing or HIL validation; upgrade-chain correctness is ultimately proven by power-cut/disconnect/wrong-packet injections on real hardware.

## File Structure

```
embedded-ota-toolkit/
├── SKILL.md
├── ota_audit.py            # audit engine (15 rules + notes + HTML report)
├── ota_tool.py             # toolset (crc/layout/pack/verify)
├── references/
│   ├── CHANGELOG.md
│   └── ota-checklist.md    # manual pre-flight checklist
└── tests/
    ├── test_ota_audit.py
    └── test_ota_tool.py
```
