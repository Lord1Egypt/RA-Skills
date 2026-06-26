---
name: claw-esp-expert
description: "ESP-IDF 专家型技能：环境检查、examples 导航、GPIO 规则审计与构建诊断。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "bins": ["node", "idf.py"] },
        "category": "developer-tools",
      },
  }
---

# Claw ESP Expert

Use this skill when the user needs help with ESP-IDF environment checks, example discovery, pin safety review, or build diagnostics.

## What this bundle includes

This ClawHub-facing bundle exposes nine stable MVP tools:

- `manage_env`
- `explore_demo`
- `resolve_component`
- `analyze_partitions`
- `decode_panic`
- `analyze_monitor`
- `flash_and_monitor`
- `execute_project`
- `safe_build`

These tools are implemented in the bundled runtime and are invoked through `scripts/run-tool.mjs`.

## Safety contract

- Treat this skill as a **diagnostic-first** ESP-IDF expert.
- Default to **check and explain**, not silent modification.
- Do not claim support for fully autonomous repair, deep serial-port management, or HIL automation unless the repository actually implements them.
- Do not invent additional tools beyond the ones listed in this file.
- Do not read arbitrary local config files unless the user explicitly asks; the MVP bundle does not require VS Code config scanning.
- Do not modify project files or system permissions unless the user clearly asks for that action.

## Tool contract

### `manage_env`
Purpose:
- inspect local ESP-IDF availability
- report `$IDF_PATH`, common install paths, `python/python3`, and `idf.py` availability
- when explicitly asked, return mirror-aware manual installation guidance instead of running upstream install scripts automatically

Example invocation:

```bash
printf '%s' '{"action":"check"}' | node scripts/run-tool.mjs manage_env --stdin
```

### `explore_demo`
Purpose:
- inspect local `$IDF_PATH/examples`
- find matching demos by keyword
- read the best matching `README.md` / `README_CN.md`
- summarize hardware requirements and structure

Example invocation:

```bash
printf '%s' '{"query":"gpio"}' | node scripts/run-tool.mjs explore_demo --stdin
```

### `safe_build`
Purpose:
- run GPIO safety audit before build
- reject fatal pin conflicts early
- invoke `idf.py build` only after the audit passes
- return structured build diagnostics, including partition overflow, memory overflow, missing headers, component resolution failures, config issues, and link errors

Example invocation:

```bash
printf '%s' '{"projectPath":"/path/to/project","chip":"esp32"}' | node scripts/run-tool.mjs safe_build --stdin
```

### `analyze_partitions`
Purpose:
- parse `partitions.csv` from the current ESP-IDF project
- identify the most likely app partition (`factory` / `ota_0`)
- combine partition table data with overflow logs
- return a recommended expanded partition size and an updated CSV draft
- return a structured patch-style before/after suggestion for `partitions.csv`

Example invocation:

```bash
printf '%s' '{"projectPath":"/path/to/project","rawLog":"Part '\''factory'\'' ... overflow 0x20000"}' | node scripts/run-tool.mjs analyze_partitions --stdin
```

### `decode_panic`
Purpose:
- parse ESP-IDF panic logs
- extract exception reason, registers, and backtrace addresses
- call the correct `addr2line` tool for Xtensa or RISC-V chips
- return decoded source locations from the ELF file

Example invocation:

```bash
printf '%s' '{"chip":"esp32s3","elfPath":"/path/to/app.elf","log":"Guru Meditation Error..."}' | node scripts/run-tool.mjs decode_panic --stdin
```

### `analyze_monitor`
Purpose:
- inspect raw `idf.py monitor` output
- detect panic/backtrace markers automatically
- return the recent log excerpt
- trigger panic decoding when an ELF path is available

Example invocation:

```bash
printf '%s' '{"chip":"esp32s3","elfPath":"/path/to/app.elf","log":"...monitor output..."}' | node scripts/run-tool.mjs analyze_monitor --stdin
```

### `flash_and_monitor`
Purpose:
- run `idf.py flash monitor`
- capture combined stdout/stderr
- analyze the resulting monitor log
- automatically trigger panic decoding when panic markers appear and an ELF path is available
- return stage status, stage summary, timeout info, recent log tail, and common serial/tool failure categories

Example invocation:

```bash
printf '%s' '{"projectPath":"/path/to/project","chip":"esp32s3","port":"/dev/ttyUSB0"}' | node scripts/run-tool.mjs flash_and_monitor --stdin
```

### `execute_project`
Purpose:
- run the minimum execution loop for an ESP-IDF project
- perform hardware audit first
- build the project
- then run `flash_and_monitor`
- return a single structured result for the whole flow

Example invocation:

```bash
printf '%s' '{"projectPath":"/path/to/project","chip":"esp32s3","port":"/dev/ttyUSB0"}' | node scripts/run-tool.mjs execute_project --stdin
```

### `resolve_component`
Purpose:
- query the official ESP Component Registry
- prefer `espressif/*` when an official component is a strong match
- suggest the best-matching component from official registry data
- generate a minimal `idf_component.yml` dependency snippet
- optionally merge that dependency into an existing manifest draft
- return a structured patch-style before/after suggestion for the manifest
- surface component docs, supported targets, and the matching version

Example invocation:

```bash
printf '%s' '{"query":"led_strip","target":"esp32s3"}' | node scripts/run-tool.mjs resolve_component --stdin
```

## Runtime notes

- `manage_env` can succeed even when ESP-IDF is not installed, because reporting `NOT_FOUND` is a valid diagnostic result.
- `manage_env({ action: "install" })` returns manual install guidance; it does not clone repositories or run upstream install scripts inside the skill bundle.
- `resolve_component` uses the official ESP Component Registry over the network and should be treated as an explicit online lookup step.
- `decode_panic` needs the matching ELF file and a working `addr2line` binary from the ESP-IDF toolchain.
- `analyze_monitor` is still log-driven; it does not open serial ports by itself in this MVP.
- `flash_and_monitor` does execute `idf.py flash monitor`, so the serial port, permissions, and toolchain environment must already be working.
- `safe_build` depends on a shell environment where `idf.py` is executable.
- The current hardware rules cover `esp32`, `esp32s3`, `esp32c3`, `esp32c6`, `esp32c5`, `esp32h2`, and `esp32p4`.
- Common SKU names are normalized to family rules, for example `ESP32-C6FH4 -> esp32c6` and `ESP32-S3-PICO-1-N8R2 -> esp32s3`.
- Audit results can include `file`, `line`, and `evidence` fields so the host can point back to the exact source location.
- The pin audit can resolve several common patterns beyond direct literals, including `pin_bit_mask`, common `..._io_num` fields, macro chains, simple assignment aliases, and `#define` / `const gpio_num_t` aliases.
- Pass user-controlled text through stdin JSON, not shell interpolation.

## Files

- `scripts/run-tool.mjs` — minimal stdin-driven tool runner for ClawHub-safe execution
- `dist/index.js` — bundled runtime entry
- `dist/data/soc/*.json` — current SoC rules database (`esp32`, `esp32s3`, `esp32c3`, `esp32c6`, `esp32c5`, `esp32h2`, `esp32p4`)

## Out of scope for this MVP bundle

The following ideas are roadmap items, not current bundle guarantees:

- automatic `idf_component.yml` maintenance
- automatic `partitions.csv` edits
- deep serial-port management UX
- HIL automation with `pytest-embedded`
