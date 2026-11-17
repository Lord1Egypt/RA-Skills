---
name: embedded-code-generator
show_name: 嵌入式代码生成器
description: 嵌入式C代码生成器，提供15类量产级C代码模板（PI控制器/RS485收发切换/低通滤波/CRC校验/环形缓冲区/SVPWM/软件I2C主机/SPI主机/ADC均值滤波/有限状态机框架/DMA环形接收缓冲/软件定时器/命令行shell/轻量断言框架/按键扫描消抖），含Doxygen注释、错误处理和使用示例，全部模板经自家审查器闭环扫描与18个gcc测试套件（518项断言）验证。当用户需要生成、编写、查找嵌入式常用模块代码、不想重复造轮子要现成标准写法、PI控制器代码、RS485方向控制、低通滤波器、CRC校验、环形缓冲区ring buffer、SVPWM空间矢量PWM、FOC电机控制代码、软件I2C模拟IIC、SPI主机、ADC采样均值滤波、状态机FSM、DMA循环模式接收、软件定时器、串口命令解析shell、断言与故障记录、按键扫描、按键消抖、长按短按、连按自动重复等嵌入式C模块时使用。
show_description: 生成15类量产级嵌入式C代码：PI控制器、RS485收发切换、低通滤波、CRC校验、环形缓冲区、SVPWM、软件I2C主机、SPI主机、ADC均值滤波、有限状态机框架、DMA环形接收缓冲、软件定时器、命令行shell、轻量断言框架、按键扫描消抖
display_name: 嵌入式代码生成器
display_name_en: Embedded Code Generator
description_zh: 说「给我一个256字节串口环形缓冲」，直接得到可编译的量产级.h+.c：15类嵌入式C模块（PI控制器、RS485、CRC、环形缓冲、SVPWM、软件I2C/SPI、FSM、DMA接收、shell、按键消抖等），含Doxygen注释与错误处理，518项gcc断言验证，未指定的参数按推荐默认值直接产出。
description_en: 15 production-grade embedded C templates covering PI controller, RS485, CRC, ring buffer, SVPWM, soft I2C/SPI, FSM, DMA, debounced key scanning and more. Doxygen-documented with error handling, verified by 518 gcc test assertions.
version: 1.1.0
author: fangcun
---


# Embedded C Code Generator

> **Current version: 1.1.0** | **All 15 template families free to use, no gating**

Never let an AI hand-write concurrency- or timing-sensitive modules on the fly — hand-rolled ring buffers leak edge cases, hand-rolled CRC gets polynomials wrong, hand-rolled PI hits integral windup, hand-rolled key debouncing misses bounce and wraparound. This skill ships **test-verified, production-grade templates**: 15 common module families as `.h` + `.c` file pairs, each with complete Doxygen comments, parameter validation, error handling and usage examples — all closed-loop scanned by the companion reviewer (0 critical, 0 major) and verified by gcc test suites (18 tests, 518 assertions).

## When to Use It

- **Need a ring buffer / PI controller / CRC**: don't reinvent the wheel — especially not an untested one. Take the template, configure per the parameter table.
- **AI-generated code you dare not ship**: every template here carries a 518-assertion test endorsement; algorithmic correctness is documented.
- **High quality bar**: ISR safety (lock-free SPSC), C99 with no dynamic allocation, C++ compatible, fixed-point support, overflow protection — these pits are already walked through in the templates.

## Workflow

1. **Identify the module**: match user need to a module in the table below.
2. **Read template files**: load the corresponding `.h` and `.c` from `templates/`.
3. **Collect config parameters**: confirm configurable items per the parameter table (Kp/Ki, pin assignments, buffer sizes). **For unspecified items, use the recommended defaults below directly — do not stall with follow-up questions.** Only for platform-specific items (pin numbers, USART instances) output placeholder macros and note them in the usage notes.
4. **Fill and output**: populate config macros and init code per user parameters; output complete compilable `.h` and `.c` contents. If the user gave an MCU platform (STM32F4, GD32E230), add platform adaptation notes in comments.
5. **Usage notes**: briefly explain key cautions (ISR safety, timing requirements).

## Module Catalog

| # | Module | Files | Key parameters | Trigger words |
|---|--------|-------|----------------|---------------|
| 1 | PI controller | `pi_controller.h/c` | Kp, Ki, Ts, out_min/max, i_min/max | PI, PID, anti-windup |
| 2 | RS485 TX/RX switch | `rs485_tc.h/c` | DE/RE pins, USART instance | RS485, half-duplex, DE/RE, TC flag |
| 3 | First-order low-pass | `lowpass_filter.h/c` | fc, Ts or alpha | low-pass, LPF, IIR, smoothing |
| 4 | CRC | `crc_utils.h/c` | buffer, length; optional CRC_USE_TABLE | CRC8, CRC16, Modbus, CCITT |
| 5 | Ring buffer | `ring_buffer.h/c` | size, element type, full policy | ring buffer, FIFO, lock-free, ISR queue |
| 6 | SVPWM | `svpwm.h/c` | Vdc, pwm_period | SVPWM, space vector, FOC, PMSM, BLDC |
| 7 | Software I2C master | `soft_i2c.h/c` | SCL/SDA macros, bit_delay, clock stretch | I2C, bit-bang, open-drain, WriteThenRead |
| 8 | SPI master | `spi_master.h/c` | mode 0-3, msb_first, cs_active_low | SPI, CS, CPOL, CPHA, full duplex |
| 9 | ADC mean filter | `adc_avg_filter.h/c` | ReadFn pointer, N, trimmed-mean switch | ADC, averaging, outlier rejection |
| 10 | FSM framework | `fsm_framework.h/c` | transition table, guards, actions, on_entry/exit | state machine, table-driven, guard |
| 11 | DMA ring RX buffer | `dma_ring.h/c` | buffer (DMA circular target), write-position recovery | DMA, circular, UART RX, idle interrupt, no packet loss |
| 12 | Software timers | `soft_timer.h/c` | now tick, period, one-shot/periodic, callback | soft timer, polling, wraparound-safe |
| 13 | Mini shell | `mini_shell.h/c` | command table, MAX_ARGS | shell, command parser, argv, serial CLI |
| 14 | Lightweight assert | `lite_assert.h/c` | LA_MODE, MAX_RECORDS, reset hook | assert, fault log, production, no-halt |
| 15 | Key scan debounce | `key_scan.h/c` | max keys, debounce/long-press/repeat ticks, active level | key scan, debounce, long press, auto-repeat |

## Recommended Defaults (apply directly when user gives none)

Produce code with these defaults without asking; list actually-used defaults in the usage notes.

| # | Module | Defaults |
|---|--------|----------|
| 1 | PI | Ts=0.001s (1 kHz), out/i limits ±1.0 (normalized duty); Kp=0.5, Ki=10.0 placeholders pending tuning |
| 2 | RS485 | DE/RE tied to one GPIO (placeholder `RS485_DE_Pin`), USART1; wait TC flag before dropping DE |
| 3 | Low-pass | Ts=0.001s, fc=50 Hz (general speed-feedback smoothing) |
| 4 | CRC | CRC16/MODBUS (init 0xFFFF), table-driven `CRC_USE_TABLE=1` |
| 5 | Ring buffer | UART stream/log: 256 B, uint8_t, OVERWRITE on full; command parse: 128 B, REJECT |
| 6 | SVPWM | Vdc=24 V, pwm_period=0.0001 s (10 kHz) |
| 7 | Soft I2C | 100 kHz standard mode (half-bit 5 us); pins are platform placeholders |
| 8 | SPI | mode 0, MSB first, CS active-low |
| 9 | ADC filter | N=8, trimmed mean on (needs N>=3) |
| 10 | FSM | guards/actions NULL when unspecified |
| 11 | DMA ring | 256 B, uint8_t (sufficient for UART <=115200) |
| 12 | Soft timer | 1 ms tick (SysTick), period per user |
| 13 | Shell | MAX_ARGS=8, 128 B line buffer, case-sensitive |
| 14 | Assert | LA_MODE=record (no production halt), MAX_RECORDS=8, reset hook `NVIC_SystemReset` |
| 15 | Key scan | debounce 20 ms @1 ms scan, long-press 1 s, repeat 200 ms, 8 keys, active-low |

## Code Quality Standards

- **C99**: no external libraries, no dynamic allocation (no malloc/free)
- **Doxygen**: every file, function and struct field documented (`@brief`/`@param`/`@return`)
- **C++ compatible**: all headers carry `#ifdef __cplusplus extern "C"` guards
- **Parameter validation**: public functions check NULL and invalid args, return error codes
- **ISR safe**: ring buffer is lock-free SPSC with volatile and memory barriers
- **Fixed-point**: PI and low-pass provide Q16.16 variants (conditional compile)
- **Overflow protection**: 64-bit intermediates for fixed-point multiply; checked adds
- **Configurable**: macros trim features (table CRC, fixed-point, asserts) to flash/RAM budget
- **MISRA-C aware**: no implicit conversions, meaningful return codes, no VLAs

## Reading Templates

Read the matching `.h`/`.c` under `scripts/templates/`. Each file is complete and compilable: header comment (purpose, algorithm, usage, cautions), config macro section, type definitions, function declarations/implementation, usage examples in `@code`/`@endcode` blocks.

After reading, adjust per user parameters: config macro defaults (`RB_STRATEGY`, `CRC_USE_TABLE`), struct init values, platform-specific types and low-level access functions.

## Self-Test Suite

`tests/` carries 18 self-test programs, 518 assertions total, covering algorithm correctness of all 15 families. Run from the package root:

```
make test
```

- **Environment**: gcc with C99; PI/low-pass/SVPWM tests link libm; no other dependencies.
- **Coverage**: CRC-8/MAXIM + CRC-16/MODBUS + CRC-16/CCITT-FALSE (bitwise and table variants), Modbus RTU frames; ring buffer FIFO order, REJECT/OVERWRITE policies, boundary and validation; soft I2C bit-level slave simulator (START/address/read-write/ACK/NACK/WriteThenRead/clock stretch/bus release); SPI master edge-accurate slave (modes 0-3, MSB/LSB, full duplex, transactional CS); ADC mean (replay and fixed-level, trimmed mean, 255x65535 no-overflow); FSM table transitions, guard chains, entry/exit ordering, self-loops, illegal events; PI backward-Euler hand-checked response, anti-windup clamping, reset/re-tune; low-pass bilinear alpha, hand-computed steps, steady-state; RS485 DE timing via mock platform layer, BUSY re-entry guard; SVPWM zero-vector symmetry, per-sector mapping, overmodulation clamp; DMA ring wraparound, segmented read, overrun resync, drain mode; soft timers one-shot/periodic, wraparound (0xFFFFFF9C+100), multi-instance; shell argc/argv, CRLF, unknown commands; lite assert record/saturate/overwrite-oldest/reset hooks; key scan double-edge debounce, long press, repeat, wraparound, two-key independence, both polarities.
- **Expected**: all 518 assertions `[PASS]`, final line `=== ALL TESTS PASSED ===`, zero compile warnings; any failure makes `make` return non-zero.

## Output Format

Output as Markdown code blocks labeled with `.h` / `.c` filenames.

## Cautions

- Platform abstraction layers (RS485 GPIO/USART access, soft I2C/SPI pin hooks) use weak functions — override per your MCU.
- PI controller must run at a fixed period Ts; sampling jitter degrades control. Prefer a hardware timer.
- SVPWM outputs normalized duty (0.0-1.0); convert to compare-register values per your timer ARR.
- On 8-bit MCUs (AVR), define `RB_ENTER_CRITICAL`/`RB_EXIT_CRITICAL` to guard 16-bit index access.
- Soft I2C speed is set by `SI2C_DelayHalfBit`; slave clock stretching relies on `SI2C_WAIT_SCL` — do not remove.
- SPI mode is set once via `SPI_Config_t.mode` (CPOL=bit1, CPHA=bit0); CS polarity handled in the user CS hook.
- ADC mean accumulator is uint32_t; full-scale 16-bit samples are safe for N<=255. Trimmed mean needs N>=3, else degrades to plain mean.
- FSM guard chains: first passing guard wins in table order; all-fail keeps state. Self-loop transitions still fire on_exit/on_entry — count side effects in actions, not entry hooks.
