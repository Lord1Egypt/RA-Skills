# CHANGELOG

## 1.2.0 · 2026-10-21 · 修复建议与检测信号对账 + 工具侧加固

反向验证驱动的一轮修复：拿「工具自己的修复建议代码」和「写法规范的 bootloader」反向去撞，暴露 3 处判定与建议自相矛盾的问题，全部修掉并各配正反例测试。

### 审计侧（ota_audit.py）

- **R15（关看门狗不恢复）修复建议与信号对账**：建议写法是 `wdt_enable()` / `ESP.wdtEnable(0)`，但原判定只认 feed 类词元——照抄修复建议仍被 R15 咬。新增 `SIG_WDT_REARM`（enable/start 类），R15 恢复判定改为 feed 或 rearm 任一即豁免
- **R6 与 R15 概念分离**：R6 要的是擦写期间"定期喂"（feed/reload），`wdt_enable` 是一次性配置不算喂，R6 判定不受 rearm 信号影响（有专门测试钉死这个边界）
- **R7（裸地址）比较语境豁免**：R3 建议的跳转校验写法 `(pc & 0xFFE00001) != 0x08000001` 里的地址是校验常量不是寻址常量，照抄 R3 修复代码不该反手被 R7 咬。地址出现在 `==/!=/&/|` 比较表达式 → 豁免；作函数实参/赋值右侧 → 照报
- **R3 修复建议补芯片适配说明**：原掩码 `0x2FFE0000` 只认栈顶在 `0x2000xxxx` 的 F1/F4 系；STM32H7 的 SRAM 在 `0x24000000/0x30000000`，照抄会拒掉合法栈顶。建议代码附 H7 掩码与范围比较写法

### 工具侧（ota_tool.py）

- **layout 分区名严格校验**：旧校验 `name.replace('_','').isalnum()` 放过数字开头的 `9boot`，生成 `#define 9BOOT_ADDR`（gcc 报 macro names must be identifiers）。改为正则 `^[A-Za-z_][A-Za-z0-9_]*$`，数字开头/连字符/点号/空名全部拦截
- **verify 增加 load_addr 区间提示**：`--addr 0xFFFFFFFF` 原先静默通过。现对不在 `0x08000000-0x081FFFFF`（Cortex-M 常见 flash 映射）的地址给 warning 不拦包（工具平台无关，nRF/ESP32 地址本就不在此区间）

### 测试

- 173 → **190 项**（新增 17 项：R7 比较豁免 4 + R15 rearm 6 + 分区名 4 + verify 区间 2 + R6/R15 概念边界 1），全部通过
- mutation test：分别破坏 rearm 信号、R7 豁免、分区名校验，各引发 1/2/4 项测试变红；还原后 md5 一致、190 全绿

## 1.1.1 · 2026-10-21 · 平台重发版（下架后重新上架）

- SKILL.md version 1.1.0 → **1.1.1**（平台校验要求包内版本严格大于线上最新版本，纯跳号重发）
- 检测逻辑、规则数、测试数零改动：**15 条规则**、173 项测试（128 审计 + 45 工具）全部 PASS
- 上传包修复 README 文件名编码问题（原 zip 内中文文件名显示乱码，本次以 UTF-8 文件名重新打包）

## 1.1.0 · 2026-09-28 · 修复代码级建议 + 端到端路径（平台首版 1.0.0 后单次更新）

- **每条审计建议从"描述性文字"升级为"可直接粘贴的修复代码"**——例如 R1（跳转 APP 未重定位中断向量表）的建议现在是 `跳转前加：SCB->VTOR = APP_BASE;`（Cortex-M）或 `csrw mtvec, app_addr`（RISC-V），照抄即可修，不用再自己查怎么改
- SKILL.md 新增「**新项目端到端路径**」：毕设/新项目从分区规划（`layout`）→ 升级代码自查（`ota_audit.py` 高危清零、≥80 分）→ 打包（`pack --emit-header`）→ 上板前校验（`verify` + checklist 故障注入）的最短路径导览，命令全部来自原有「快速上手」
- frontmatter description 补口语化故障场景触发词（升级后变砖跑飞死机排查、毕设固件升级、升级流程安全性检查等），平台覆盖口径与 SKILL.md 对齐
- 检测逻辑零改动（仅建议与文档增强），**15 条规则**、173 项测试（128 审计 + 45 工具）全部 PASS
## 1.0.0 · 2026-09-15 · 首次发布

两个工具，一套方法论（沿用 embedded-code-reviewer 的误报治理思路）。

### ota_audit.py —— 升级链路静态审计

**13 条规则**（高危 4 / 中危 6 / 低危 3）：

| 规则 | 级别 | 内容 |
|---|---|---|
| R1 | 高危 | 跳转 APP 前未重定位中断向量表（缺 `SCB->VTOR`） |
| R2 | 高危 | 跳转 APP 前未关闭中断 |
| R3 | 高危 | 跳转前未校验 APP 有效性（栈顶/复位向量） |
| R4 | 高危 | 升级数据无完整性校验（写 flash 但无 CRC/哈希） |
| R5 | 中危 | flash 擦除地址未按页对齐 |
| R6 | 中危 | 擦写期间未喂看门狗 |
| R7 | 中危 | 分区地址硬编码 |
| R8 | 中危 | 接收等待无超时保护 |
| R9 | 中危 | 无防降级版本校验 |
| R10 | 中危 | 升级状态未持久化 |
| R11 | 低危 | flash 写未检查返回值 |
| R12 | 低危 | 升级流程无进度输出 |
| R13 | 低危 | 升级流程中存在硬编码延时 |

**判定架构**：文件级信号 + 行级定位。

先收集文件级信号（是否有跳转迹象、是否设了 VTOR、是否关中断、是否有 CRC…），
再在这些信号基础上判定「缺失项」——检测的是「该做的事做没做」，不是「写法对不对」。

**误报治理（刻意的取舍）**：

- 仅当出现「OTA 语境关键字（ota/iap/bootloader/firmware/upgrade…）」或「跳转迹象（`__set_MSP` / 函数指针跳转…）」时才应用升级类规则；普通业务代码（例如往 flash 存配置）不会被刷屏（`is_ota` 判定不含「有 flash 写」）
- 注释/字符串字面量内的代码不计入信号（去噪在信号收集前完成）
- R7 每文件只报一次；R11/R13 每文件只报一次；R5 每行只报一次——避免同质问题刷屏
- 设了 VTOR / 关了中断 / 有校验即不再报对应规则（不重复唠叨）

**回报**：JSON（`summary` + `issues` + `score` + `signals`）、`--dir` 目录批量（含 top5 文件）、`--html` 中文报告（内联样式、严重度分色、评分）。

**开发过程中修掉的问题**（留档备查）：

1. 规则描述里误用半角双引号（`"能跑但一进中断就死"`）导致 Python 源码语法错误 → 统一改为全角引号
2. `is_ota` 判定最初把「有 flash 写」也算 OTA 上下文，会让普通工程文件被升级类规则刷屏 → 收紧为「关键字 or 跳转迹象」
3. `\bIWDG\b` 类词边界正则匹配不到 `IWDG_Init` / `fwdgt_config`（`_` 属 word 字符，`\b` 不成立）→ 去掉 `\b` 限制
4. 同理 `\bota\b` 匹配不到 `ota_recv` → 改为 `\b(?:ota|iap|...)\w*`
5. 并行编辑同一文件时有两处 Edit 静默丢失（工具报成功但内容未变）→ 改为串行编辑并逐一复核

### ota_tool.py —— 升级包工具集

- `crc`：CRC32（zlib 兼容）/ CRC16-CCITT-FALSE / CRC16-MODBUS / MD5 / SHA256
- 镜像头：64 字节（magic/版本/地址/CRC/flags），由 `pack` 生成；`pack --emit-header` 另出 MCU 侧 `.h`
- `layout`：分区表计算器，对齐检查 + 溢出检测 + `.h` 生成（含编译期越界断言）
- `pack`：固件 bin + 镜像头 → `.pkg`
- `verify`：校验包（头 CRC → magic → 镜像 CRC → 大小自洽 → 板型/地址比对）

**镜像头**：64 字节固定长，小端；`header_crc` 为头自身 CRC32（计算时该字段置 0）；
MCU 侧解析必须用 `OTA_HEADER_SIZE` 常量而非 `sizeof(结构体)`。

**开发过程中修掉的问题**（留档备查）：

1. `header_crc_check` 把「已清零的头」拿来读存储值，等于永远拿 0 去比 → 改为先从原始头读存储值、再对清零副本算 CRC
2. magic 常量写反：`0x55504657` 小端存储是 `"WFPU"`，应为 `0x50555746` 才是 `"FWUP"` → 修正并加字节序断言测试
3. 测试里"未对齐大小"用例写成了对齐值（0x1000 是 2K 整数倍）→ 改为 0x900

### 测试

- `tests/test_ota_tool.py`：45 项（CRC 标准向量、头往返与防篡改、分区表溢出、打包/校验往返、CLI 退出码）
- `tests/test_ota_audit.py`：57 项（13 条规则正反例、去噪、非 OTA 防刷屏、评分、目录扫描、HTML、CLI）
- **合计 102 项，全部通过**

### 已知边界

- 静态文本分析，不做数据流/控制流分析：跨文件的「VTOR 在别处设的」「校验在调用方做的」会漏报
- R5 只认常量擦除地址，宏地址不判
- 不替代上板实测（断电/断连/错包三类故障注入）

## 1.0.0 · 2026-09-15 · 提交前独立复核修订

首轮 102 项测试是「自己写的测试测自己的代码」，属同源自证，不能替代独立复核。
本次用外部样本（另写的 bootloader / 普通配置代码 / 端到端打包链路）复跑，修掉 2 处误报 + 4 处文档漂移。

### 修复：误报（ota_audit.py）

1. **R12 白名单过窄**：`SIG_LOG` 原先只有 `printf/LOG_/log_/puts/trace…`，自定义进度回调（`ota_progress()`、`notify_progress()`、`report_status()`）不被认作输出 → 一份写法完全规范的 bootloader 被误报「无进度输出」（实测 99 分而非 100）。已补 `progress/notify/report/emit/_print/print_` 等，且要求带 `(` 的调用形式，避免变量名误豁免。
2. **R13 无任何门控**：R13 原先没有前置条件，凡文件出现 `HAL_Delay(500)` 就报「升级流程中存在硬编码延时」——一个 LED 闪烁任务也会中招。已加 `is_ota` 门控。

### 修正：文档与实际不符

- `SKILL.md` 测试数「57 项」→「104 项」（漏算了工具侧 45 项，原文两处）
- `SKILL.md` / `CHANGELOG.md` 把 `header` 写成 `ota_tool.py` 的子命令 → 实际 CLI 只有 `crc/layout/pack/verify` 四个，镜像头由 `pack` 产出
- `SKILL.md`「30 秒看效果」示例表格行号整体偏 1（L8/L13/L14/L15 → 实际 L7/L12/L13/L14）
- `SKILL.md` 已知边界补充「门控范围」条目，明确 R5/R7 属通用 flash 卫生检查、不受 OTA 语境门控

### 测试

- 新增 2 项回归：`test_progress_callback_ok`（进度回调不误报 R12）、`test_non_ota_delay_skipped`（非 OTA 延时不报 R13）
- 调整 1 项：`test_reported_once` 片段补 OTA 语境（R13 加门控后受影响）
- **合计 104 项，全部通过**（59 审计 + 45 工具）

### 本次复核的独立验证证据

- **复现文档示例**：`bootloader_demo.c` → 评分 49/100、4 高 4 中 3 低、共 11 条，与 SKILL.md 完全一致
- **防误报**：规范 `bootloader_clean.c` → 100 分 0 命中；普通 flash 配置代码 `normal_flash_config.c`（非 OTA）→ 100 分 0 命中
- **工具端到端**：`crc`(5 算法) → `layout`(256K/2K 对齐，用 232K 余 24K) → `pack`(8192B → 8256B = 8192+64) → `verify`(magic=FWUP、ver=1.2.3) 全通过
- **负向**：篡改 `.pkg` 第 100 字节 → `verify` 准确报「镜像 CRC 不符」并 exit 1；指定错板型 `--hw-id 0x9999` → 报「硬件标识不符」并 exit 1

## 1.0.0 · 2026-09-15 · 真实开源语料驱动的判定口径重做

上一稿用的样本仍是手写的，说服力有限。本次直接拉**真实生产级 bootloader** 语料来撞——
结论：首版在成熟工程上会误判，问题不在规则本身，而在"缺失项"的判定粒度。

### 语料（仅本地实测，未随包分发；可按下表复现）

通过 `https://ghproxy.net/https://raw.githubusercontent.com/<repo>/<branch>/<path>` 拉取：

| 类别 | 仓库 | 文件 |
|---|---|---|
| 双 Bank/swap 框架 | `mcu-tools/mcuboot` (main) | `boot/bootutil/src/loader.c`、`image_validate.c`、`bootutil_misc.c`、`swap_misc.c`、`boot/boot_serial/src/boot_serial.c` |
| 安全 bootloader | `wolfSSL/wolfBoot` (master) | `src/loader.c`、`image.c`、`libwolfboot.c`、`update_flash.c`、`boot_arm.c` |
| 商用 DFU | `adafruit/Adafruit_nRF52_Bootloader` (master) | `src/main.c`、`src/boards/boards.c` |
| 框架内置 OTA | `espressif/esp-idf`、`zephyrproject-rtos/zephyr`、`ARMmbed/mbed-bootloader` | `components/app_update/esp_ota_ops.c`、`subsys/dfu/boot/mcuboot.c`、`source/main.cpp` |
| 官方 IAP 例程 | `STMicroelectronics/STM32CubeF1/F4/F7` | `Projects/*/Applications/IAP/IAP_Main/Src/main.c` |
| 负向对照 | `littlefs`、`pellepl/spiffs`、`zephyr`、`esp-idf`、`STM32Cube HAL` | `lfs.c`、`src/spiffs_nucleus.c`、`subsys/storage/flash_map/flash_map.c`、`components/nvs_flash/src/nvs_api.cpp`、`stm32f1xx/f4xx_hal_flash.c` |

### 修复：真实语料暴露的误报（4 类）

1. **`(void (*)(void))(&END_STACK)` 被判成跳转**：中断向量表初始化里的函数指针强转，被首版的跳转正则命中（wolfBoot `boot_arm.c`）→ 强转信号改为要求"强转后立刻调用"：`((void(*)(void))addr)()`。
2. **名字里带 `start_app` 的变量被判成跳转**：Adafruit `bool const just_start_app = …`、mbed `mbed_start_application(…)` 均被命中（首版缺词边界）→ 跳转命名信号统一加 `\b` 并要求调用形态 `名字(`。
3. **R11 打到厂商 HAL 的函数定义行**：`HAL_StatusTypeDef HAL_FLASH_Program(uint32_t …)`（STM32 HAL 两个文件各 1 条）→ R11 加两条豁免（`#` 预处理/宏定义行、函数定义或声明行），并整体加 `is_ota` 门控。
4. **R11 打到 `#define` 宏里的 flash 写**：wolfBoot `#define trailer_write(…) hal_flash_write(…)` → 同上豁免覆盖。

### 修复：成熟工程被"高危误判"（跨文件存疑降级）

真实 bootloader 普遍多文件分工：`boot_arm.c` 只管跳、`image.c` 管校验、状态在 partition 模块。
首版因此在 wolfBoot `boot_arm.c` 报出 R2/R3 级别的高危断言，而实际上：

- 中断向量表由本文件自建（`IV[]` + `section(".isr_vector")`），并非"没管中断"
- 镜像校验在 `image.c`（本文件 `#include "image.h"`）
- 回滚/版本在 `security_cnt` / partition 模块

本次引入**跨文件存疑降级**：

- 检出"该步骤由外部模块承担"的迹象（`#include "image.h"|partition…`、`verify_*()/validate_*()`、`IV[]`/`.isr_vector`、`*_partition_state()`/`*_trigger()`）时，R1/R2/R3/R9/R10 改为**低危**并在描述里标注【需人工确认·疑在外部模块完成】
- **没有**这类迹象时仍按高危/中危报（新增 `TestCrossFileDeescalation.test_no_companion_evidence_stays_high` 守着，防"借降级放水"）

### 其他口径修正

5. **R3 的校验证据过宽**：首版只要全文出现 `0x2000xxxx` 字面量就认为"已校验"（漏报面大）→ 收紧为"校验词（`is_valid/validate_app…`）或明确的掩码判断（`& 0x2FFE0000) == 0x2…`）"。ST IAP 例程用的是后者，识别正确。
6. **R12 白名单再放宽**：真实工程的反馈常走菜单/显示/LED/串口（ST IAP 用 `Main_Menu()`、Adafruit 用 LED）→ 补入 `*Menu*()`、`*Display*()`、`*Led*/LED*()`、`*Serial/UART/COM*()`、`beep()`。
7. **锚点取真实跳转现场**：ST IAP 例程原先锚在 `extern pFunction JumpToApplication;`（L36 声明行），改为优先锚 `__set_MSP(`/指针调用处（L88）。
8. **内联汇编跳转纳入识别**：wolfBoot 的 `asm volatile("mov pc, %0" ::"r"(app_entry))` 因字符串去噪而不可见 → 内联汇编行的字符串单独抽取，只用于跳转/向量表/关中断判定（不污染 flash/校验类规则）。
9. **notes（不计分）**：跳转被托管给框架（`mbed_start_application()`、`bootloader_app_start()`）时输出提示条目，避免"只报缺失"造成误读；HTML 报告单独一块展示。

### 新增规则

10. **R14 升级写入前未见擦除**（中危，覆盖人工清单 B4）：NOR flash 只能 1→0，目标页不先擦就写 = 写坏。
    - 门控 `is_ota`；文件内出现 `erase` 字样（含注释，说明可能在别处或驱动内部擦）时降为低危待确认
    - 擦除识别放宽到通用形态 `\w*erase\w*()`，避免 `nor_erase()`/`erase_sector()` 漏判
    - 上语料前先量过误报面：真实语料中所有写 flash 的文件都同时有擦除动作 → 零命中，故不构成新的噪声源

### 易用性

- 新增 `--fail-under N`（CI 门禁：整体分低于 N 返回 1）；`--dir` 模式补整体 `score` 字段
- HTML 报告新增"提示（不计分）"区块；**修掉"只有提示、没有问题"的文件被整段跳过**的问题

### 测试

- 审计侧 59 → **79 项**（新增 20 项回归，含真实语料形态固化：向量表初始化不算跳转、变量名不算跳转、框架托管跳转只提示不报错、HAL 函数定义不报 R11、宏里的 flash 写不报 R11、菜单/LED 反馈算进度输出、跨文件降级正反例、内联汇编跳转、锚点在跳转现场、`--fail-under` 门禁两侧）
- 合计 **124 项**（79 审计 + 45 工具），全部通过

### 修复后语料复测

| 文件 | 评分 | 命中 |
|---|---|---|
| mcuboot `loader.c` / `image_validate.c` / `bootutil_misc.c` / `swap_misc.c` / `boot_serial.c` | 100 ×5 | — |
| wolfBoot `boot_arm.c` | 97 | R2/R3/R9（**全部低危待确认**） |
| wolfBoot `image.c` / `libwolfboot.c` / `loader.c` | 100 ×3 | — |
| wolfBoot `update_flash.c` | 98 | R10/R11（低危） |
| Adafruit `main.c` / `boards.c` | 100 ×2 | — |
| ESP-IDF `esp_ota_ops.c`、Zephyr `dfu/boot/mcuboot.c`、mbed `main.cpp` | 100 ×3 | — |
| ST `IAP_Main`（F1/F4/F7） | 80 ×3 | R1+R2 高危（真隐患）、R9 中危 |
| 负向对照 7 个文件 | 100 ×7 | — |

### 遗留（诚实标注）

- wolfBoot `boot_arm.c` 仍有 3 条低危【需人工确认】：跨文件分工下的固有噪声，人工一眼可判
- ~~wolfBoot `update_flash.c` 的 R11（`ext_flash_write()` 返回值未接）属实~~ → **后续更正为误报**：`ext_flash_write()` 在本工程里返回 `void`，没有返回值可查（详见「跨平台适用性修复」一节「修复 4」第 3 条）
- ST `IAP_Main` 的 R1/R2 是**真隐患**（`HAL_Init()` 已使能 SysTick，跳转前未设 VTOR/未关中断），不是误报
- 纯汇编（`.s`/`.asm`）里的跳转不扫；`.h` 中的宏展开不做；不做数据流/控制流分析

## 1.0.0 · 2026-09-15 · 跨平台适用性修复

起因：被问「是不是只适用 STM32」。实测下来——**当时的跨平台召回是坏的**，
只是之前从没拿非 STM32 的代码测过，所以一直没暴露。

### 定性结论（先说清楚）

| 层 | 适用范围 |
|---|---|
| `ota_tool.py`（CRC / 镜像头 / 分区表 / 打包 / 校验） | **任意平台**，纯字节运算，与架构无关 |
| 审计·架构级规则 R1 R2 R3 R8 R9 R12 | Cortex-M 全家族（ST / GD32 / CH32 / APM32 / nRF / NXP / RA…）+ RISC-V |
| 审计·外设级规则 R4 R5 R6 R7 R11 R13 R14 | 取决于平台命名覆盖；R7 只认 `0x08xxxxxx` 系（nRF52 / ESP32 上不报 = 漏报，不是误报） |

### 修复 1：`is_ota_ctx` 用 `\b` 导致整套规则静默失效（最严重）

`\b(?:…|ota|iap|…)\w*` 在真实代码里匹配不到带下划线前缀的写法：
`esp_ota_write`、`nrf_dfu_flash_store`、`gd32_ota_apply`、`my_iap_handler`——`_` 属 word 字符，
`\b` 在下划线前不成立。后果不是报错，而是**整个升级规则集不触发**，输出假的 100 分。
（早期那么多"100 分零命中"的真实文件，有相当一部分是这么来的。）

改为「前一字符非字母数字」并扩词表（补 `dfu` / `fota` / `boot_jump` / `boot_app` / …），
既认下划线前缀，又不至于把 `quota` 误判成 OTA。同时语境判定改用「去注释 + 去字符串」的文本，
避免 `#include "dfu_types.h"` 这类头文件名把纯 flash 驱动误判成 OTA 语境。

### 修复 2：跳转识别漏掉「先取向量、再赋函数指针、后调用」的写法

真实实现常见：

```c
app_fn entry = (app_fn)(*(volatile uint32_t *)(app_addr + 4));
entry();
```

当时的强转信号要求"强转后立即调用"，抓不到这种写法 → R1/R2/R3 在 Nordic / RISC-V 样本上整体漏报。
已补「从 APP 基址取栈顶 / 复位向量」的识别模式。

### 修复 3：外设信号只认 ST HAL 命名

- **flash 写**：补 `nrfx_nvmc_*write`、`nrf_fstorage_write`、`nrf_dfu_flash_store`、`sd_flash_write`、`esp_partition_write`、`esp_ota_write`、`spi_flash_write`、`flash_area_write`、`bootutil_*write`、`fmc_*program`，以及通用 `*flash*write*()` 形态
- **看门狗**：补 `nrfx_wdt_*`、`esp_task_wdt_*`、`wdt_hal` / `wdt_enable`；喂狗补 `wdt_reload*`、`esp_task_wdt_reset`、`WDT_Refresh`
- **擦除**：`RE_ERASE_CALL` 补 `fmc_*erase*`、`nrfx_nvmc_*erase*`、`esp_partition_erase*`、`FLASH_Erase*`
- **日志**：补平台日志宏 `PRINTF`（Nordic）、`NRF_LOG_*`、`ESP_LOG*`、`LOG_INF/ERR/DBG/WRN`（Zephyr）、`SEGGER_RTT_*`
- **延时**：补 `nrf_delay_*`、`esp_rom_delay_*`、`k_sleep` / `k_msleep`、`osDelay`
- **状态持久化**：补 `otadata` / `ota_select`（ESP-IDF OTA 状态分区）、`boot_write_*` / `boot_swap_info` / `BOOT_MAGIC` / `trailer`（MCUboot）
- **向量表重定位**：补 RISC-V 的 `csrw mtvec` / `csrw 0x305`

### 修复 4：新增外设信号带出的误报（4 处，逐条定性）

1. **ESP `bootloader_utility.c` 报 R10**：该文件有 96 处 `otadata`、25 处 `ota_select`（ESP 的 OTA 状态分区机制）→ 补进状态信号，误报消除（96 → 100）
2. **MCUboot `bootutil_misc.c` 报 R4 / R9**：它**就是**写 trailer / 状态的模块（`boot_write_trailer`、`BOOT_MAGIC`），校验在 `image_validate.c` → R4 补上与 R3 / R9 一致的跨文件降级（降为低危 +【需人工确认】）
3. **wolfBoot / ESP 报 R11**：`ext_flash_write()` 在 wolfBoot 里返回 `void`，根本没有返回值可查；且 `ret = esp_partition_write(...)` 明明接了却被漏豁免（原豁免正则只认大写 `Write`）→ R11 改为「只对明确返回状态码的 API 家族」判定 + 豁免改为"行首是赋值语句"
4. **wolfBoot `boot_serial.c`、ESP `bootloader_utility.c` 报 R13**：命中的是 `esp_rom_delay_us(1000); /* Allow last byte to leave FIFO */`——**复位前让串口发完**的硬件时序延时，不是"用魔数延时替代轮询" → R13 增加「附近有 reset / reboot 调用时豁免」

### 新增：平台识别

`detect_platform()` 从代码特征判断平台（`stm32` / `gd32` / `ch32` / `nordic` / `esp-idf` / `zephyr` / `rt-thread` / `riscv` / `cortex-m`），
写入 `signals.platform` 供报告与二次开发使用。**只用于标注，不参与打分**（避免平台误判改变审计结论）。

### 跨平台召回验证（自写最小坏样本，非第三方代码）

| 平台 | 用到的真实写法 | 期望命中 | 实得 |
|---|---|---|---|
| Nordic nRF52 | `nrfx_nvmc_words_write` / `nrfx_wdt_init` / 取 APP 向量跳转 | R1 R2 R3 R4 R6 R8 R12 | 全中，**51 分**；不误报 R7 |
| ESP-IDF | `esp_partition_write` / `esp_task_wdt_init` | R4 R6 R8 R14 | 全中；**不误报** R1/R2/R3 |
| RISC-V（CH32V） | `csrw mtvec` / `FLASH_Program` | R2 R3 R4 R8 R12 | 全中；`csrw mtvec` 认作重定位 → **不报 R1** |
| GD32（FMC） | `fmc_page_erase(0x08008100)` / `fmc_word_program` | R4 R5 R7 R11 | 全中 |

### 扩展语料（非 STM32 平台，9 个文件）

`adafruit/Adafruit_nRF52_Bootloader`（`src/flash_nrf5x.c`、`src/boards/boards.c`、`src/main.c`）、
`espressif/esp-idf`（`components/bootloader_support/src/bootloader_utility.c`、`components/app_update/esp_ota_ops.c`、`components/nvs_flash/src/nvs_api.cpp`）、
`zephyrproject-rtos/zephyr`（`subsys/dfu/boot/mcuboot.c`、`subsys/storage/flash_map/flash_map.c`）、
`ARM-software/CMSIS_5`（`Device/ARM/ARMCM4/Source/startup_ARMCM4.c`）

### 测试

- 审计侧 79 → **95 项**（新增 `TestCrossPlatform` 16 项：语境下划线前缀、`quota` 不误判、include 不算语境、取向量跳转识别、平台识别、四平台召回、R11 void 型不报 / 赋值豁免 / 裸调用报、R13 复位前豁免 / 轮询仍报、R10 的 otadata 与 MCUboot trailer）
- 合计 **140 项**（95 审计 + 45 工具），全部通过

### 修复后语料复测

| 文件 | 评分 | 说明 |
|---|---|---|
| 负向对照 ×7 | 100 ×7 | 零误报（含 ESP-IDF NVS、Zephyr flash_map、Nordic flash 驱动） |
| MCUboot ×5 | 100×4 + 98×1 | `bootutil_misc.c` 98：2 条低危【需人工确认】 |
| wolfBoot ×5 | 100×4 + 97×1 | `boot_arm.c` 97：3 条低危【需人工确认】 |
| Adafruit / ESP-IDF / Zephyr / mbed / CMSIS / OpenBLT | 100 ×9 | — |
| ST `IAP_Main` ×3 | 80 ×3 | R1+R2 高危真隐患 + R9 中危 |
| 非 ST 平台 9 个文件 | 100 ×9 | 含 Nordic flash 驱动、ESP bootloader、Zephyr DFU |

### 遗留（诚实标注）

- **R7 在非 `0x08xxxxxx` 平台失效**（nRF52 / ESP32）：能识别出平台但不会报警，属漏报，已写进 SKILL.md「平台适用性」
- **R11 对签名未知的写函数不判定**：宁可漏报（`hal_flash_write` 可能是 `void`）也不误报，属保守取舍
- **未覆盖的平台**：若某平台 API 命名不在信号表内，相应规则会静默不触发；拿不准请查 JSON 的 `signals` 字段

## 1.0.0 · 2026-09-15 · 框架层适配：Arduino / ESP8266

起因：被追问「Arduino 和 ESP 这些呢」。实测发现——**早先只按「架构 × 厂商」分维度，漏了「框架层」**。
同一颗 ESP32，Arduino 写法与 ESP-IDF 写法命名词汇毫无重叠，而早先的全部适配都给了 ESP-IDF。

### 实测暴露的问题（端到端跑 `review_file`，4 份样本）

| 样本 | 修复前 | 问题 |
|---|---|---|
| 坏·Arduino-ESP32 HTTP OTA | **99 分** | `Update.begin/write/end` 返回值全不查、`ESP.wdtDisable()` 关了不管、无回滚 → 只报 1 条低危 |
| 好·同场景成熟写法 | 100 分 | 与坏样本只差 1 分，**等于没有鉴别力** |
| 纯 `ArduinoOTA` 草图 | 100 分 | **`is_ota_ctx = False`，整套规则静默不触发** |
| AVR（Uno）无 OTA 草图 | 100 分 | 这一条是**正确的不适用**，不是缺陷 |

信号表逐字段探测（26 条 Arduino 惯用写法 × 12 个信号）确认零命中的有：
`ArduinoOTA.*`、`Update.*`、`ESPhttpUpdate.update`、`httpUpdate.update`、`Updater.*`、
`ESP.wdtFeed()`、`delay(N)`、`Serial.print()`。

### 根因：词边界的第二个变体（camelCase 前缀）

上一轮修的是**下划线前缀**（`esp_ota_write` 里 `_` 属 word 字符，`\b` 不成立）。
这次是**驼峰前缀**：`ArduinoOTA` 里 `OTA` 的前一字符是字母 `o`，同一套「前一字符非字母数字」判定照样拒绝。
**同一个坑，只防了一种形态。**

### 修复

1. **新增 `SIG_OTA_CTX_CAMEL`（大小写敏感、单独编译）**
   - 驼峰内嵌全大写缩写 `(?<=[a-z])(?:OTA|DFU|IAP|FOTA)(?![a-z])` → 认 `ArduinoOTA`，而 `quota`（全小写）天然不命中
   - 框架类名整体 `ArduinoOTA` / `ESPhttpUpdate` / `HTTPUpdate` / `httpUpdate`
   - 点号成员调用 `Update.begin(` / `Updater.write(` / `…rollBack(` / `…setMD5(`
   - **为什么不并进原来那条**：原正则带 `IGNORECASE`，把驼峰分支并进去会让 `quota` 里的小写 `ota` 被吃进来——正是上一轮专门避开的坑
2. **外设信号补框架命名**：`Update/Updater.write`（flash 写 + R11 状态码家族）、`Update.end(true)` / `setMD5`（库内校验证据）、`ESP.wdtDisable/Enable/Feed`、`Serial.print/println/printf/write`、裸 `delay(N)`、`millis()/micros()`、`Preferences` / `prefs.put*` / `nvs_set_*` / `EEPROM.write`
3. **新增 R15「关闭看门狗后未见恢复」**（中危）：显式关 WDT 是长 OTA 的正确做法，但关完不恢复＝刷完跑飞再也救不回来
4. **R6 增加豁免**：检出「显式关闭看门狗」时不再报"未喂狗"（在 Arduino 上那恒为误报）
5. **R11 豁免口径修正**：原来只认「行首是 `名字 =`」的赋值形态，`size_t w = Update.write(...)` 这类**带类型的声明赋值**被漏豁免 → 改为「调用点左侧存在独立赋值号」
6. **R14 在框架层改出 notes（不计分）**：Arduino 的擦除在 `Update` 库内部完成，sketch 里结构上永远看不到 `erase`，报 R14 恒为误报
7. **R13 加三重豁免**（`<50ms` 视为让出 CPU / 窗口内已有超时护栏 / Arduino `loop()` 内的空闲节拍），并明确阈值常量 `DELAY_MAGIC_MIN_MS = 50`
8. **`RE_WAIT_LOOP` 覆盖框架链路等待**：`while (client.connected())`、`while (WiFi.status() != WL_CONNECTED)`、`while (!stream.available())`——注意必须允许括号内再套一层括号，沿用 `[^)]*` 会在内层 `)` 处截断，一个都抓不到
9. **`.ino` / `.pde` 纳入 `SOURCE_EXTS`**：此前 `--dir` 会整个跳过 Arduino 草图，连报错都没有
10. **`detect_platform` 增加 `arduino`**，且**排在 `esp-idf` 之前**（ESP32 的 Arduino 代码同样含 `esp_*` 调用，不先判框架层会被误标成 ESP-IDF）

### 修复后实测

| 样本 | 修复前 | 修复后 | 说明 |
|---|---|---|---|
| 坏·Arduino HTTP OTA | 99 | **82** | 命中 R8 R9 R10 R11 R13 R15（6 条，逐条对着源码核实为真） |
| 好·同场景成熟写法 | 100 | **96** | 仅 R9，且属实（该草图确实没做防降级比较） |
| 纯 `ArduinoOTA` | 100（语境都没判出） | **99** | 已正确判为 OTA 语境；仅 R12 |
| AVR（Uno） | 100 | 100 | 正确的不适用 |

**回归**：47 个非 Arduino 文件（34 个真实开源语料含 7 个负向对照、4 个平台坏样本、其余装置文件）**评分与命中规则零变化**；
MCUboot `bootutil_misc` 98、wolfBoot `boot_arm` 97、ST IAP×3 = 80，与修复前逐条一致。

### 测试

- 审计侧 95 → **128 项**（新增 `TestArduinoFramework` 26 项、R13 阈值与护栏 5 项）
- 合计 **173 项**（128 审计 + 45 工具），全部通过
- 关键断言：**「坏草图必须比好草图低 10 分以上」**——把"没鉴别力"这个回归直接钉死
- 同时修 `TestDelayRule.test_reported_once`：样本由 `delay_ms(10)` 改为 `delay_ms(100)`（R13 引入 50ms 下限后语义变了），另补阈值边界与「`loop()` 内节拍不报」用例

### 遗留（诚实标注）

- **Arduino 只审 sketch 层，不审库内部**：R14 改出 notes、R4 以 `Update.end(true)` 作为库内校验证据。「没报 R4/R14」只代表 sketch 没漏做，**不代表 `Update` 库本身没问题**
- **AVR（Uno/Nano/Mega）天然不适用**：得 100 分是"没有可审计对象"，不是"代码安全"
- **R13 语义已收紧**：`<50ms` 的延时不再报，属刻意降噪，别当成漏报
