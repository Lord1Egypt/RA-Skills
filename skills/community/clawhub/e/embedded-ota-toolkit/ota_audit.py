#!/usr/bin/env python3
r"""
嵌入式 OTA / Bootloader 升级链路静态审计引擎

配套 ota_tool.py：tool 负责"把固件做成可升级的包"，本引擎负责
"检查升级代码有没有防砖漏洞"——不用编译、不接硬件，静态扫。

设计原则（与 embedded-code-reviewer 同一套方法论）：
  - 误报优先治理：宁可漏报也不刷屏，每条规则都有明确豁免口径
  - 文件级信号 + 行级定位：先判断"这是不是 bootloader/OTA 代码"，
    再在文件级信号基础上判定缺失项（缺 VTOR、缺校验…），
    避免逐行正则把普通工程也报一遍
  - 检测的是"缺失"而非"写法"：问的是"跳转前该做的做了吗"，
    不是"代码长得对不对"

规则集（15 条）：
  高危：R1 跳转未重定位 VTOR / R2 跳转前未关中断 / R3 跳转前未校验 APP
        / R4 升级数据无完整性校验
  中危：R5 擦除地址未按页对齐 / R6 擦写期间未喂看门狗 / R7 分区地址硬编码
        / R8 接收等待无超时 / R9 无防降级版本校验 / R10 升级状态未持久化
        / R14 升级写入前未见擦除 / R15 关闭看门狗后未见恢复
  低危：R11 flash 写未检查返回值 / R12 无进度日志 / R13 硬编码延时

平台覆盖：
  - 工具侧（ota_tool.py）纯字节运算，与芯片平台无关
  - 架构级规则（R1-R3、R8、R9、R12）跨 Cortex-M 全家族（ST/GD32/CH32/
    APM32/nRF/NXP/RA…）与 RISC-V（认 csrw mtvec）
  - 外设级规则（R4-R7、R11、R13、R14、R15）信号覆盖 ST HAL/SPL、GD32 FMC、
    Nordic nrfx、ESP-IDF、Zephyr/MCUboot、RT-Thread 与通用命名（flash_write 等）
  - 框架层：Arduino / ESP8266 —— 认 ArduinoOTA、ESPhttpUpdate、
    httpUpdate、Updater.*、Update.*，以及 Serial.*（日志）、delay(N)（延时）、
    millis()（超时）、ESP.wdtDisable/Enable/Feed（看门狗）；.ino/.pde 纳入扫描
  - 已知限制（如实标注边界，不宣称"已支持"）：
      · R7 只认 0x08xxxxxx 系（nRF52/ESP32 上不报＝漏报，不是误报）
      · Arduino 的擦除/校验封装在 Update 库内部，sketch 里看不见 →
        R4/R14 对该框架降级为低危【需人工确认】，属"看不到就不报"的边界
      · AVR Arduino（Uno/Nano/Mega）无自升级代码（bootloader 走串口 STK500），
        本引擎对其天然不适用，得 100 分属"没有可审计对象"而非"代码安全"
      · 平台 API 命名未覆盖时规则静默不触发，请查 signals 字段确认

判定口径修正（依据真实开源 bootloader 语料实测，详见 CHANGELOG）：
  - 跳转信号要求"调用形态"：`\b名字\s*\(`，不再把 `just_start_app`（变量）、
    `mbed_start_application`（框架函数）、`(void (*)(void))(&END_STACK)`
    （中断向量表初始化）当成跳转迹象
  - R1/R2/R3/R9 引入"跨文件存疑降级"：本文件缺某步骤、但存在"该步骤由
    外部模块/框架承担"的迹象时，按低危提示输出并标注【需人工确认】，
    不再直接按高危断言（真实生产 bootloader 大量采用多文件分工）
  - R11 仅在下判为升级链路语境时生效，且豁免 `#define` 宏与函数定义/声明行
  - R12 日志白名单补入菜单/显示/LED/串口类反馈调用
  - 新增 R14「升级写入前未见擦除」（覆盖人工清单 B4 项；真实语料上零误报）
  - 擦除识别放宽到通用 `\w*erase\w*()` 形态，避免 `nor_erase()` / `erase_sector()` 漏判
  - 跳转锚点优先取真实跳转现场（__set_MSP / mov pc / 指针调用），
    不再锚在 `extern pFunction JumpToApplication;` 这类声明行
  - 内联汇编里的跳转/向量表操作（asm volatile("mov pc, ...")）纳入识别
  - 新增 notes（不计分）：提示"跳转已被外部/框架函数托管"，避免只报缺失

跨平台修复（依据四平台坏样本实测）：
  - 语境判定弃用 `\b`：真实代码里 OTA 关键词几乎总带下划线前缀
    （esp_ota_write / nrf_dfu_ / gd32_ota_apply），用 `\b` 会让整套升级规则
    静默失效（得出假的 100 分）；改为「前一字符非字母数字」并扩词表
  - 跳转识别补「先取 APP 向量、再赋函数指针、后调用」的常见写法
  - 外设信号补 Nordic nrfx / ESP-IDF / Zephyr / MCUboot 的 API 命名
  - R4 补跨文件降级（与 R3/R9 一致）；R11 只对明确返回状态码的 API 判定；
    R13 豁免复位前延时；R10 认 otadata / boot_write_* 等状态写法
  - 新增 detect_platform()：识别目标平台写入 signals.platform（不参与打分）

退出码：0=无问题、1=有问题、2=用法/内部错误
"""

import argparse
import json
import os
import re
import sys

SEVERITY_WEIGHT = {"high": 8, "medium": 4, "low": 1}
SOURCE_EXTS = (".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh",
               ".ino", ".pde")   # .ino/.pde：Arduino 草图

# --------------------------------------------------------------------------
# 规则元信息
# --------------------------------------------------------------------------
RULES = {
    1:  ("high",   "跳转 APP 前未重定位中断向量表",
         "从 bootloader 跳转到 APP 前必须把中断向量表指到 APP 区，否则 APP 里所有中断都会跳到 bootloader 的向量表（或未初始化区）——现象是「能跑但一进中断就死」。",
         "跳转前加：SCB->VTOR = APP_BASE;  // Cortex-M 把向量表指到 APP 区；RISC-V 写 csrw mtvec, app_addr"),
    2:  ("high",   "跳转 APP 前未关闭中断",
         "跳转前必须 __disable_irq() 关总中断，否则跳转瞬间来一个中断，会在 MSP 已切换、向量表未就绪的窗口里跑飞。",
         "跳转前加：__disable_irq();  // 并清已挂起中断：for(int i=0;i<8;i++) NVIC->ICPR[i]=0xFFFFFFFF;"),
    3:  ("high",   "跳转前未校验 APP 有效性",
         "APP 可能没烧、烧了一半、或被擦坏。跳转前必须校验 APP 起始的栈顶指针落在 SRAM 范围内、复位向量落在 flash 范围内，通过才跳。不校验等于「分区是空的也照跳」，直接 hardfault 死循环。",
         "跳转前加：uint32_t sp=*(volatile uint32_t*)APP_BASE, pc=*(volatile uint32_t*)(APP_BASE+4);\n// 栈顶须 8 字节对齐且落在 SRAM、复位向量须落在 flash 且 bit0=1（Thumb）：\nif ((sp & 0x2FFE0000) != 0x20000000 || (pc & 0xFFE00001) != 0x08000001) return;\n// 注意掩码按芯片 SRAM 映射调整：F1/F4 栈顶在 0x2000xxxx 用上式；H7 的 SRAM 在 0x24000000/0x30000000，改为 (sp & 0x3FFE0000) != 0x24000000 或 0x30000000 二选一；GCC 下也可用 __builtin_frame_address 之外直接范围比较 sp>=SRAM_BASE && sp<SRAM_BASE+SRAM_SIZE"),
    4:  ("high",   "升级数据无完整性校验",
         "收到升级数据后直接写 flash，没有任何 CRC/哈希比对。传输误码、flash 写入失败、断包都会变成「能启动但逻辑错乱」的固件，且无法回滚。",
         "收满整包先校验再写：uint32_t crc = crc32(buf, len); if (crc != hdr.image_crc) { /* 拒包重传 */ }；写完 flash 后回读再比对一次"),
    5:  ("medium", "flash 擦除地址未按页对齐",
         "Cortex-M 的 flash 擦除粒度是页（常见 1K/2K，GD32/CH32 部分型号 4K）。擦除地址不是页大小整数倍时，多数 HAL 会返回错误、部分厂商库会静默擦掉相邻页——把 bootloader 自己擦了就是砖。",
         "擦除前把地址按页取整：addr &= ~(FLASH_PAGE_SIZE - 1);  // 1K/2K/4K 页按型号，地址全部走分区表宏"),
    6:  ("medium", "擦写期间未喂看门狗",
         "flash 擦除一页通常几十毫秒，整包升级累计可达数秒。若开了看门狗却在擦写循环里不喂狗，升级必然被 WDT 复位打断——每失败一次就多一次变砖机会。",
         "擦写循环内每页喂一次狗：HAL_IWDG_Refresh(&hiwdg);  // 或 WDT_Feed() / ESP.wdtFeed() / nrfx_wdt_feed()"),
    7:  ("medium", "分区地址硬编码",
         "裸写 0x08008000 这类地址，改分区布局时必然漏改某处，导致「擦 A 区写 B 区」。",
         "地址集中在分区表头文件：#define APP_BASE 0x08008000  // 全文引用宏，与链接脚本的 .ld 对齐，禁用裸 0x08xxxxxx"),
    8:  ("medium", "接收等待无超时保护",
         "while(!rx_done) 这种死等，一旦对端掉线/断连，bootloader 会永远卡在这里——看门狗在喂就永远不复位，产品变成砖。",
         "所有等待带超时退出：uint32_t t0=HAL_GetTick(); while(!rx_done){ if(HAL_GetTick()-t0>5000) goto ota_recover; }"),
    9:  ("medium", "无防降级版本校验",
         "不做版本比较，攻击者/误操作可以把设备刷回有已知漏洞的旧固件。至少要拒绝旧版本（除非显式置允许降级标志）。",
         "写 flash 前比较版本：if (new_ver < cur_ver && !(hdr.flags & FLAG_ALLOW_DOWNGRADE)) return OTA_REJECT_OLDER;  // ver = major<<16|minor<<8|patch"),
    10: ("medium", "升级状态未持久化",
         "升级标志/进度只放 RAM，中途掉电就丢失，设备既没升级完也回不到正常启动——只能返厂。",
         "状态写入 flash 备份区（先写标志后写数据）：flash_write(STATE_ADDR, &ota_state, sizeof(ota_state));  // 启动时读标志决定：续传/回滚/正常启动"),
    11: ("low",    "flash 写未检查返回值",
         "flash 编程失败（写保护、电压不足、对齐错误）必须检查返回值并回退，否则校验和会悄悄对不上，问题在下次启动才暴露。",
         "接住返回值：if (HAL_FLASH_Program(TYPEWORD, addr, data) != HAL_OK) { ota_abort(err_line); }  // 失败立即中止升级，别静默"),
    12: ("low",    "升级流程无进度输出",
         "升级过程没有任何日志/进度输出，现场排障只能靠猜。",
         "阶段切换处加日志：printf(\"[OTA] erase %u/%u\\n\", page, total);  // 至少输出：开始/擦除/写入/校验/完成/失败原因"),
    13: ("low",    "升级流程中存在硬编码延时",
         "固定魔数延时（如 delay_ms(500)）依赖主频与编译器优化，换平台就失准。",
         "魔数延时改状态轮询+超时：while(!ready){ if(HAL_GetTick()-t0>TMO) break; }  // 替换 delay_ms(N)"),
    14: ("medium", "升级写入前未见擦除",
         "NOR flash 只能把 1 写成 0：目标页必须先擦成全 1 才能写入。直接写未擦除的页，多数 HAL 会返回错误、部分厂商库会静默失败，结果是「升级看起来成功、固件其实是坏的」。",
         "每个目标页写前先擦：flash_erase(page_addr);  // 同文件内应能同时看到 erase 与 write，且擦除地址与写入地址同页"),
    15: ("medium", "关闭看门狗后未见恢复",
         "升级流程里显式关闭看门狗（ESP.wdtDisable / wdt_disable 等）本身是对的——长擦写不该被 WDT 打断。但关掉之后若不恢复，新固件一旦跑飞就再也没有兜底复位，只能人工救砖。",
         "升级结束/重启前重新武装看门狗：wdt_enable();  // 或 ESP.wdtEnable(0) / WDT_Start() / nrfx_wdt_enable()，重新使能即视为恢复，确保新固件有兜底复位"),
}

# --------------------------------------------------------------------------
# 信号正则
# --------------------------------------------------------------------------
RE_BLOCK_OPEN = re.compile(r"/\*")
RE_BLOCK_CLOSE = re.compile(r"\*/")

SIG_JUMP_STRONG = re.compile(
    r"__set_MSP\s*\("
    r"|MSR\s+MSP"
    r"|\bmov\s+pc\s*,"
    r"|\bjalr\b|\bmret\b"
    # 函数指针强转后立即调用：  ((void (*)(void))addr)()   —— 必须跟"实参)("
    r"|\(\s*void\s*\(\s*\*\s*\)\s*\(\s*void\s*\)\s*\)\s*\(\s*[\w\s.\->\[\]&*]*\)\s*\("
    # 从 APP 基址取栈顶/复位向量的"跳转准备"——真实实现常写成
    #   app_fn entry = (app_fn)(*(volatile uint32_t *)(app_addr + 4));  ... entry();
    # 这种"先取向量、再赋函数指针、后调用"的写法，上面那条"立即调用"模式抓不到。
    r"|\*\s*\(\s*(?:volatile\s+)?uint32_t\s*\*\s*\)\s*\(\s*\w*(?:app|APP|entry|ENTRY|firmware|FW|user|USER)\w*\s*[+)]"
)
SIG_JUMP_NAMED = re.compile(
    r"\b(?:jump_to_app|JumpToApp|jump_app|JumpApp|boot_jump|BootJump|iap_jump|iapjump|"
    r"run_app|RunApp|start_app|StartApp|app_entry|APP_ENTRY)\s*\("
)
SIG_JUMP = re.compile("(?:" + SIG_JUMP_STRONG.pattern + ")|(?:" + SIG_JUMP_NAMED.pattern + ")")

# 跳转被托管给外部/框架函数（本文件不含跳转三步，属于"跨文件存疑"）
SIG_JUMP_DELEGATED = re.compile(
    r"\b\w*(?:mbed_start_application|bootloader_app_start|nrf_bootloader_app_start|"
    r"start_application|jump_to_application|jump_to_app_if_valid)\s*\(")

SIG_VTOR = re.compile(
    r"SCB\s*->\s*VTOR\s*=|SCB_VTOR|NVIC_SetVectorTable|NVIC_VectTab|set_vtor|VTOR\s*="
    r"|VECT_TAB_OFFSET|VTOR_S|E000ED08"
    # RISC-V：mtvec 重定位（csrw mtvec / 0x305 是 mtvec 的 CSR 号）
    r"|\bmtvec\s*=|csrw\s+mtvec|csrw\s+0x305|mtvec_bits")
SIG_DISABLE_IRQ = re.compile(
    r"__disable_irq\s*\(|__set_PRIMASK\s*\(\s*1|CPSID\s+i|portDISABLE_INTERRUPTS"
    r"|rt_hw_interrupt_disable|DISABLE_INT|irq_disable|disable_irq\s*\("
    # FreeRTOS 临界区 / Zephyr irq_lock / ESP-IDF / RISC-V 内建
    r"|taskENTER_CRITICAL|portENTER_CRITICAL|irq_lock\s*\(|esp_intr_disable"
    r"|GLOBAL_INT_DISABLE|riscv_disable_irq|csrclr\s+[Mm][Ii][Ee]"
)
# APP 有效性校验：要求出现"判断性"证据，而不是任意收尾的 0x2000xxxx 字面量
SIG_VALID_CHECK = re.compile(
    r"is_valid|check_valid|valid_app|verify_app|check_app|app_is_valid"
    r"|is_app_valid|validate_app|image_valid|boot_valid|check_application"
    r"|SRAM_BASE|RAM_BASE|SRAM_START|RAM_START"
    r"|0x2[Ff][Ff][Ee]0000"
    r"|&\s*0x2[0-9A-Fa-f]{7}\s*\)*\s*==\s*0x2"
    # 各平台自带的镜像/应用头校验 API（ESP-IDF / MCUboot / Zephyr / nRF）
    r"|esp_image_verify\w*|esp_ota_get_app_description|esp_app_desc"
    r"|bootutil_img_verify|flash_area_verify|image_validate|nrf_dfu_validation"
    r"|img_validate|image_check")
SIG_FLASH_WRITE = re.compile(
    # ST HAL / 标准外设库
    r"HAL_FLASH_Program|FLASH_Program|FLASH_ProgramWord|FLASH_ProgramHalfWord"
    # 通用命名
    r"|flash_write|flash_program|program_flash|WriteFlash|write_flash"
    r"|fmc_write|fmc_program|fmc_word_program|fmc_halfword_program"
    r"|nvm_write|nvm_program"
    # Nordic nRF5 SDK / nrfx：nrfx_nvmc_words_write / nrf_nvmc_write_bytes / sd_flash_write
    r"|nrfx?_nvmc_\w*write|nrf_fstorage_write|nrf_dfu_flash_store|sd_flash_write"
    # Espressif ESP-IDF：esp_partition_write / esp_ota_write / spi_flash_write
    r"|esp_partition_write\w*|esp_ota_write\w*|esp_flash_write\w*|spi_flash_write\w*"
    # MCUboot / Zephyr / 通用 flash 抽象层：flash_area_write
    r"|flash_area_write\w*|bootutil_\w*write"
    # 外部 NOR/NAND 驱动常见命名
    r"|nor_write|nand_write|\bw25q\w*write|\bat25\w*write|\bmx25\w*write"
    # 通用动词形态：spi_flash_write_bytes() / flash_write_page() / write_flash_region()
    r"|\b\w*[Ff]lash\w*[Ww]rite\w*\s*\(|\b\w*[Ww]rite\w*[Ff]lash\w*\s*\("
    # Arduino / ESP8266 框架：Update.write() / Updater.write()（封装了擦+写）
    r"|(?<![A-Za-z0-9])(?:Update|Updater)\s*\.\s*write\s*\("
)
SIG_FLASH_ERASE = re.compile(
    r"HAL_FLASHEx_Erase|FLASH_Erase|flash_erase|fmc_erase|nvm_erase"
    r"|EraseFlash|erase_flash|PageErase|page_erase"
    # 通用"擦除调用"形态：nor_erase() / erase_sector() / nrfx_nvmc_page_erase()
    r"|\b\w*[Ee]rase\w*\s*\("
    # 外部 NOR/NAND 驱动的"块/扇区"清除命名
    r"|\b\w*[Bb]lock[Ee]rase\w*\s*\(|\b\w*[Ss]ector[Ee]rase\w*\s*\("
)
SIG_INTEGRITY = re.compile(
    r"\bcrc|CRC|checksum|CheckSum|check_sum|sha256|SHA256|sha1|md5|MD5"
    r"|verify_image|verify_fw|verify_pkg|verify_package|verify_update|integrity"
    # 各平台签名/摘要校验 API
    r"|esp_image_verify|esp_ota_get_app_description|bootutil_img_verify"
    r"|image_validate|img_validate|_signature|signature_verify|verify_signature"
    # Arduino / ESP8266 框架：Update.end(true) = 写入完成并比对校验值；
    # Update.setMD5() = 指定期望摘要。二者都是"库内已完成校验"的证据。
    r"|(?<![A-Za-z0-9])(?:Update|Updater)\s*\.\s*(?:end\s*\(\s*true|setMD5|setMD5Sum)"
)
# R11 专用：确认「有返回状态码语义」的 flash 写 API。
# 静态分析看不到函数签名，对签名未知的第三方写函数（如 wolfBoot 的 ext_flash_write
# 返回 void）报"未检查返回值"纯属噪音，故 R11 只认这批明确返回状态码的家族。
SIG_FLASH_WRITE_STATUS = re.compile(
    r"HAL_FLASH_Program|FLASH_Program\w*|\bflash_write\w*|flash_area_write|"
    r"esp_partition_write|esp_ota_write|esp_flash_write|spi_flash_write|"
    r"fmc_\w*program|nrf_fstorage_write"
    # Arduino / ESP8266：Update.write() 返回已写入字节数（size_t），
    # 返回 0 或小于请求长度就是写失败，必须判断——归入"有状态码语义"一族
    r"|(?<![A-Za-z0-9])(?:Update|Updater)\s*\.\s*write"
)
SIG_WDT_USE = re.compile(
    r"IWDG|WWDG|HAL_IWDG|HAL_WWDG|wdt_init|WDT_Init|wdt_config"
    r"|watchdog|WatchDog|fwdgt|FWDGT|WDOG|Wdog"
    # Nordic nrfx / ESP-IDF / 通用看门狗
    r"|nrfx?_wdt|wdt_hal|wdt_enable|WDT_Enable|esp_task_wdt|wdt_start"
    # Arduino ESP8266：ESP.wdtDisable() / ESP.wdtEnable()（camelCase + 点号，
    # 上面那套下划线命名一条都盖不到）
    r"|ESP\s*\.\s*wdt(?:Disable|Enable)\s*\("
)
SIG_WDT_FEED = re.compile(
    r"IWDG_ReloadCounter|HAL_IWDG_Refresh|WWDG_SetCounter|HAL_WWDG_Refresh"
    r"|wdt_feed|feed_dog|kick_dog|watchdog_feed|fwdgt_counter_reload|clear_wdt"
    # Nordic nrfx / ESP-IDF / 通用重载命名
    r"|nrfx?_wdt_\w*(?:feed|reload)|wdt_reload\w*|esp_task_wdt_reset"
    r"|WDT_Refresh|WDOG_Refresh|refresh_wdt|reload_wdt|wdt_kick"
    # Arduino ESP8266：ESP.wdtFeed()（喂狗同时会重新使能看门狗）
    r"|ESP\s*\.\s*wdtFeed\s*\("
)
# 「重新武装看门狗」——R15 专用，与 R6 的"喂狗"是两个概念：
#   R6 要的是擦写期间"定期喂"（feed/reload），wdt_enable 是一次性配置不算喂；
#   R15 要的是 disable 之后"有没有恢复"，wdt_enable/WDT_Start 就是恢复。
# 修因（2026-10-21 探针实测）：R15 的建议写法是 wdt_enable / ESP.wdtEnable(0)，
# 但原判定只认 feed——照抄修复建议仍被 R15 咬，建议与信号表自相矛盾。
SIG_WDT_REARM = re.compile(
    r"wdt_enable|WDT_Enable|wdt_start|enable_wdt|WDT_Start|start_wdt"
    r"|watchdog_enable|watchdog_start|nrfx?_wdt_enable"
    # ESP.wdtEnable 重新使能（注意 ESP.wdtEnable 喂狗语义弱于 wdtFeed，只算恢复）
    r"|ESP\s*\.\s*wdtEnable\s*\("
)
# 「显式关闭看门狗」——用于把 R6（未喂狗）与 R15（关了不恢复）区分开：
# Arduino 长 OTA 的惯用做法就是先 ESP.wdtDisable() 关掉看门狗，此时"没喂狗"
# 是设计意图而不是缺陷，报 R6 属误报；真正的风险变成"升级完没恢复看门狗"。
SIG_WDT_OFF = re.compile(
    r"ESP\s*\.\s*wdtDisable\s*\(|wdt_disable\s*\(|WDT_Disable|disable_wdt"
    r"|iwdg_disable|IWDG_Disable|nrfx?_wdt\w*_stop|wdt_stop",
    re.IGNORECASE)
SIG_TIMEOUT = re.compile(
    r"timeout|TIMEOUT|_tick|Tick|elapsed|deadline|HAL_GetTick|GetTick|expire"
    # Arduino：millis()/micros() 是该框架下超时护栏的唯一时间基准
    # （Arduino 没有 HAL_GetTick，超时只能写成 millis() - t0 > N）
    r"|millis\s*\(\s*\)|micros\s*\(\s*\)")
SIG_VERSION = re.compile(r"version|Version|fw_ver|FW_VER|\b_ver\b|\bver\b|VERSION")
SIG_STATE_SAVE = re.compile(
    r"update_flag|ota_flag|upgrade_flag|boot_flag|bootloader_flag|save_state|store_state"
    r"|write_flag|progress|upgrade_status|ota_status|magic_num|update_pending|flag_write"
    # 各平台持久化状态：ESP-IDF otadata / MCUboot boot_record / nRF dfu state
    r"|otadata|ota_select|ota_data|boot_record|boot_record_status"
    r"|nrf_dfu\w*_state|esp_ota_get_boot_partition|boot_count"
    # MCUboot 系：写 trailer / swap 状态 / boot magic —— 真实的状态持久化写法
    r"|boot_write_\w+|boot_read_\w+|boot_swap_info|swap_status|BOOT_MAGIC|BOOT_FLAG|trailer"
    # Arduino/ESP8266 的持久化载体：Preferences(NVS) / EEPROM
    # （Arduino 没有裸 flash 状态分区，升级标志只能落在这两处）
    r"|\bPreferences\b|prefs\s*\.\s*(?:put|get)\w*|nvs_set_\w+|nvs_commit"
    r"|EEPROM\s*\.\s*(?:write|put|commit|read)"
)
# 日志/反馈：printf 家族 + 各平台日志宏 + 进度回调 + 现场常见的菜单/显示/LED/串口反馈
SIG_LOG = re.compile(
    r"printf|LOG_|log_|LOGI|LOGD|LOGE|DEBUG_|puts|uart_print|app_log|trace"
    r"|(?:progress|Progress|notify|Notify|report|Report|emit|_print|print_)\w*\s*\("
    r"|\w*[Mm]enu\w*\s*\(|\w*[Dd]isplay\w*\s*\(|\w*(?:Led|LED)\w*\s*\("
    r"|\w*(?:Serial|UART|Uart|COM_)\w*\s*\(|beep\s*\(|Beep\s*\("
    # 各平台日志宏：Nordic PRINTF/NRF_LOG / ESP-IDF ESP_LOGx / Zephyr LOG_xxx / RTT
    r"|\bPRINTF\b|nrf_log\w*|NRF_LOG_\w+|esp_log\w*|ESP_LOG\w+|ESP_LOGI|ESP_LOGE"
    r"|\bLOG_INF\b|\bLOG_ERR\b|\bLOG_DBG\b|\bLOG_WRN\b|SEGGER_RTT_\w+|rtt_printf"
    # Arduino：Serial.print/println/printf(...) —— 点号成员调用。
    # 上面那条 \w*(?:Serial)\w*\s*\( 被中间那个 '.' 挡死了，永远匹配不到。
    r"|(?<![A-Za-z0-9])(?:Serial\d?|USBSerial|SerialUSB)"
    r"\s*\.\s*(?:print|println|printf|write)\s*\("
)
SIG_DELAY = re.compile(
    r"\b(?:HAL_Delay|delay_ms|delay_us|delay_s|vTaskDelay|rt_thread_mdelay|mdelay"
    r"|osDelay|nrf_delay_\w+|esp_rom_delay_\w+|k_msleep|k_sleep|taskDelay"
    # Arduino：裸 delay(N)。\b 前缀本身已排除 _delay( 这类下划线写法
    # （下划线是 word 字符，前面不构成词边界），故不会误吃 rt_thread_mdelay
    r"|delay)\s*\(\s*\d+")
# R13 的判定下限（毫秒）：小于该值视为"让出 CPU / 节流"（Arduino 的 delay(2)、
# delay(10) 是给协议栈喘气），不属于"用固定延时替代超时机制"，不报。
DELAY_MAGIC_MIN_MS = 50
SIG_BARE_ADDR = re.compile(r"(?<![0-9A-Fa-fx])0x08[0-9A-Fa-f]{6}(?![0-9A-Fa-f])")

# --------------------------------------------------------------------------
# OTA 语境判定（决定整套升级规则是否启用）
# 坑：不能用 \b —— 真实代码里这些词几乎总带下划线前缀（esp_ota_write /
# nrf_dfu_ / gd32_ota_apply / my_iap_handler），\b 在下划线前不成立，
# 会导致「整个规则集不触发」的灾难性漏报；也不能完全不设边界，否则 quota
# 这类普通词会被误判成 OTA。故用「前一字符不是字母/数字」（允许下划线）。
# --------------------------------------------------------------------------
SIG_OTA_CTX = re.compile(
    r"(?<![A-Za-z0-9])(?:"
    r"bootloader|boot_load|boot_(?:jump|app|entry|loader|image|flag|mode|update|upgrade|request)"
    r"|iap|ota|dfu|fota|firmware|fw_update|upgrade|update_fw|app_update|img_update|self_update"
    r")\w*",
    re.IGNORECASE)

# 框架层（Arduino / ESP8266）的 OTA 语境证据。
# 为什么必须单独编译、且大小写敏感：驼峰分支 (?<=[a-z])(?:OTA|DFU|IAP|FOTA) 若带上
# IGNORECASE，小写词 quota 里嵌的 "ota"（前一字符 u 是小写字母）也会命中——这是
# 早先用 (?<![A-Za-z0-9]) 专门避开的坑，不能在扩面时又踩回去。
# 大小写敏感下 quota 全小写、根本不含 "OTA"，天然安全。
# 场景：纯 ArduinoOTA 草图（setup 里 begin、loop 里 handle）不含独立的 ota 词元，
# 上面那套 (?<![A-Za-z0-9]) 边界判定不到，会让整套升级规则静默不触发。
SIG_OTA_CTX_CAMEL = re.compile(
    # 驼峰内嵌全大写缩写：ArduinoOTA / EspDFU / MyIAP（后接小写字母的不算，如 myOTAflag）
    r"(?<=[a-z])(?:OTA|DFU|IAP|FOTA)(?![a-z])"
    # 框架类名/全局对象整体出现
    r"|(?<![A-Za-z0-9])(?:ArduinoOTA|ESPhttpUpdate|HTTPUpdate|httpUpdate)"
    # 点号成员调用：Update.begin(...) / Updater.write(...)
    r"|(?<![A-Za-z0-9])(?:Update|Updater)\s*\.\s*"
    r"(?:begin|write|end|abort|rollBack|printError|hasError|setMD5)",
)

# "flash 擦除由框架库代管"的迹象：Arduino 的 Update 库在 begin/write 内部自己
# 擦除目标扇区，sketch 里根本看不到 erase 调用。用于 R14 降级，避免把框架代管
# 误判成"漏做擦除"。
SIG_FRAMEWORK_FLASH = re.compile(
    r"(?<![A-Za-z0-9])(?:Update|Updater)\s*\.\s*(?:begin|write)\s*\(")

# "该步骤可能由外部模块承担"的迹象（用于跨文件存疑降级）
SIG_VERIFY_COMPANION = re.compile(
    r"\b\w*(?:verify|validate|authenticat|check_integrity|security_cnt|rollback|counter)\w*\s*\("
    r"|#\s*include\s*[\"<](?:image|bootutil|verify|security|image_header|boot_)"
    r"|image_header|img_hdr|security_counter|anti_rollback")
SIG_IRQ_POLICY = re.compile(
    r"isr_vector|\.isr_vector|\bIV\s*\[\s*\]|__enable_irq|NVIC_EnableIRQ|HAL_NVIC_EnableIRQ"
    r"|SysTick_Config|HAL_InitTick|__attribute__\s*\(\s*\(\s*section")
# "升级状态由外部模块持久化"的迹象（分区状态 API / 触发标志 API / 分区头文件）
SIG_STATE_COMPANION = re.compile(
    r"\b\w*(?:partition_state|part_state|update_trigger|boot_trigger|update_pending|"
    r"update_state|bank_state|swap_status|img_state|mark_updated|set_update|"
    r"get_partition_state)\w*\s*\("
    r"|#\s*include\s*[\"<](?:partition|loader|image|bootutil|boot)\w*[\">]")

# 擦除调用里提取常量地址
RE_ERASE_CALL = re.compile(
    r"(?:HAL_FLASHEx_Erase|FLASH_Erase\w*|flash_erase\w*|fmc_\w*erase\w*|nvm_erase\w*"
    r"|nrfx?_nvmc_\w*erase\w*|esp_partition_erase\w*|EraseFlash|erase_flash\w*"
    r"|PageErase|page_erase\w*|nor_erase\w*|erase_sector\w*|erase_page\w*)"
    r"\s*\([^)]*?(0x[0-9A-Fa-f]+|\b\d{4,}\b)"
)
# while 死等（接收/握手等待）
# 允许"括号内再套一层括号"：框架写法普遍是 while (obj.method() != X)，
# 若沿用 [^)]* 会在内层 ')' 处截断，WL_CONNECTED / connected() 一个都抓不到。
RE_WAIT_LOOP = re.compile(
    # 标志位死等：while(!rx_flag) / while(x == 0) / while(x != 1)
    r"while\s*\([^)]*(?:!\s*\w*(?:flag|done|ready|ok|recv|rx)|==\s*0\s*\)|!=\s*1\s*\))"
    # 框架层链路等待：while(client.connected()) / while(WiFi.status()!=WL_CONNECTED)
    # / while(!stream.available()) —— 对端一掉线就是永久卡死，正是 R8 要抓的场景
    r"|while\s*\((?:[^()]|\([^()]*\))*\b"
    r"(?:connected|available|isConnected|WL_CONNECTED|waitForData|linkUp)\b"
)
# 函数定义/声明形态（用于豁免"这不是调用点"）
RE_DEF_LIKE = re.compile(
    r"^\s*(?:static\s+|inline\s+|extern\s+|__weak\s+|WEAK\s+|const\s+)*"
    r"[A-Za-z_]\w*(?:\s*[*&]\s*|\s+)+[A-Za-z_]\w*\s*\(")
RE_STRING = re.compile(r'"((?:[^"\\]|\\.)*)"')
# 内联汇编行（跳转/向量表常写在 asm volatile("...") 字符串里）
RE_ASM_LINE = re.compile(r"\b(?:asm|__asm)\b")

# --------------------------------------------------------------------------
# 平台识别：从代码特征判断目标平台，用于报告标注与"规则适用性"提示。
# 只用于显示、不参与加减分（避免平台误判改变审计结论）。
# 顺序敏感：先判特征更特异的平台，最后才落到泛化的 STM32 / 通用 Cortex-M。
# --------------------------------------------------------------------------
_PLATFORM_LABELS = {
    "arduino": "Arduino / ESP8266 框架",
    "nordic": "Nordic nRF5x",
    "esp-idf": "Espressif ESP32 (ESP-IDF)",
    "zephyr": "Zephyr RTOS",
    "rt-thread": "RT-Thread",
    "gd32": "GD32（国产 Cortex-M）",
    "ch32": "CH32 / WCH（沁恒）",
    "stm32": "STM32（ST HAL/SPL）",
    "riscv": "RISC-V 通用",
    "cortex-m": "通用 Cortex-M / 裸机",
}
_PLATFORM_HINTS = (
    # Arduino 放最前：ESP32 的 Arduino 代码同样含 esp_* 调用，若不先判框架层
    # 会被误标成 ESP-IDF（两者命名词汇完全不同，标注错了会误导读者）。
    ("arduino",   re.compile(r"ArduinoOTA|ESPhttpUpdate|httpUpdate|"
                             r"(?:Update|Updater)\s*\.\s*(?:begin|write)\s*\(|"
                             r"ESP\s*\.\s*wdt(?:Disable|Enable|Feed)\s*\(|"
                             r"\bvoid\s+setup\s*\(\s*\)|\bvoid\s+loop\s*\(\s*\)")),
    ("nordic",    re.compile(r"nrfx?_\w+|NRF_LOG|\bnrf5\d{3}\b|sd_flash_write|\bsdk_config\.h")),
    ("esp-idf",   re.compile(r"\besp_[a-z]\w+\(|ESP_LOG\w+|esp_system\.h|esp-idf")),
    ("zephyr",    re.compile(r"\bk_\w+\(|LOG_INF|\bZephyr\b|devicetree|zephyrproject")),
    ("rt-thread", re.compile(r"\brt_\w+\(|rtthread|RT_USING")),
    ("gd32",      re.compile(r"\bfmc_\w+\(|\bGD32\w*|__GD32")),
    ("ch32",      re.compile(r"\bCH32\w*|\bWCH\w+_|__CH32")),
    ("stm32",     re.compile(r"\bHAL_\w+\(|STM32Cube|__STM32|stm32\w*xx_hal")),
    ("riscv",     re.compile(r"\bmtvec\b|\briscv\w*|__riscv|RISC-V")),
)


def detect_platform(text: str) -> dict:
    """识别目标平台，返回 {id, label}（仅用于报告标注，不参与评分）。"""
    for pid, rx in _PLATFORM_HINTS:
        if rx.search(text):
            return {"id": pid, "label": _PLATFORM_LABELS[pid]}
    return {"id": "cortex-m", "label": _PLATFORM_LABELS["cortex-m"]}


def strip_noise(line: str, in_block: bool, keep_strings: bool = False):
    """去掉块注释 / 行注释 / 字符串字面量，避免注释里的示例代码被当成真代码。

    keep_strings=True 时保留字符串内容（用于识别 `#include "image.h"`、
    `section(".isr_vector")` 这类"外部模块承担"的证据——它们本身就在字符串里）。
    """
    out, i, n = [], 0, len(line)
    while i < n:
        if in_block:
            end = line.find("*/", i)
            if end == -1:
                return "".join(out), True
            i, in_block = end + 2, False
            continue
        ch = line[i]
        if ch == "/" and i + 1 < n:
            two = line[i:i + 2]
            if two == "//":
                break
            if two == "/*":
                in_block, i = True, i + 2
                continue
        if ch in "\"'" and not keep_strings:
            quote, i = ch, i + 1
            while i < n:
                if line[i] == "\\":
                    i += 2
                    continue
                if line[i] == quote:
                    i += 1
                    break
                i += 1
            out.append(" ")  # 字符串替换成空格，保留列语义
            continue
        out.append(ch)
        i += 1
    return "".join(out), in_block


def is_page_aligned(addr: int) -> bool:
    """按常见 Cortex-M 页大小判定对齐：1K/2K/4K 任一整数倍即视为对齐。"""
    return any(addr % page == 0 for page in (0x400, 0x800, 0x1000))


def pick_jump_anchor(clean_lines, jump_hits) -> int:
    """锚点优先取"真实跳转现场"，而不是 extern 声明或变量出现处。

    ST 官方 IAP 例程里 `extern pFunction JumpToApplication;`（声明，L36）会先于
    `__set_MSP(...)`（真跳转，L88）被匹配；报 L36 会让用户看不懂在对哪行说话。
    """
    for pattern in (SIG_JUMP_STRONG, SIG_JUMP_NAMED):
        for i, line in enumerate(clean_lines):
            if pattern.search(line):
                return i + 1
    return jump_hits[0] if jump_hits else 1


def review_text(text: str, filename: str = "<stdin>") -> dict:
    """审计一份源码文本，返回 {issues, summary, score, signals}。"""
    raw_lines = text.splitlines()
    clean_lines, in_block = [], False
    for line in raw_lines:
        clean, in_block = strip_noise(line, in_block)
        clean_lines.append(clean)

    joined = "\n".join(clean_lines)

    # 保留字符串、仅去注释的一版文本：用于识别"该步骤由外部模块承担"的证据
    # （如 #include "image.h"、section(".isr_vector")）——这些内容在字符串里，
    # 用去噪版 joined 会把证据一起删掉，导致降级判定失效。
    rawish_lines, in_block_raw = [], False
    for line in raw_lines:
        clean_raw, in_block_raw = strip_noise(line, in_block_raw, keep_strings=True)
        rawish_lines.append(clean_raw)
    rawish_joined = "\n".join(rawish_lines)
    raw_joined = "\n".join(raw_lines)

    # ---- 内联汇编：跳转/向量表常写在 asm volatile("...") 字符串里，单独抽取 ----
    asm_by_line, asm_chunks = {}, []
    for idx, raw in enumerate(raw_lines):
        if not RE_ASM_LINE.search(raw):
            continue
        for m in RE_STRING.finditer(raw):
            asm_by_line.setdefault(idx + 1, []).append(m.group(1))
            asm_chunks.append(m.group(1))
    asm_text = "\n".join(asm_chunks)
    asm_jump_lines = sorted(ln for ln, chunks in asm_by_line.items()
                            if SIG_JUMP.search(" ".join(chunks)))
    joined_all = joined + "\n" + asm_text if asm_text else joined

    # ---- 文件级信号 ----
    jump_hits = sorted(set([i + 1 for i, l in enumerate(clean_lines) if SIG_JUMP.search(l)]
                           + asm_jump_lines))
    sig = {
        # 语境判定用「去注释 + 去字符串字面量」的版本：避免 #include "dfu_types.h"
        # 这类头文件名（在字符串里）把一个纯 flash 驱动误判成 OTA 语境。
        "is_ota_ctx": bool(SIG_OTA_CTX.search(joined) or SIG_OTA_CTX_CAMEL.search(joined)),
        "jump": jump_hits,
        "platform": detect_platform(joined_all),
        "has_vtor": bool(SIG_VTOR.search(joined_all)),
        "has_disable_irq": bool(SIG_DISABLE_IRQ.search(joined_all)),
        "has_valid_check": bool(SIG_VALID_CHECK.search(joined)),
        "has_flash_write": bool(SIG_FLASH_WRITE.search(joined)),
        "has_flash_erase": bool(SIG_FLASH_ERASE.search(joined)),
        "has_integrity": bool(SIG_INTEGRITY.search(joined)),
        "has_wdt_use": bool(SIG_WDT_USE.search(joined)),
        "has_wdt_feed": bool(SIG_WDT_FEED.search(joined)),
        "has_wdt_rearm": bool(SIG_WDT_REARM.search(joined)),
        "has_wdt_off": bool(SIG_WDT_OFF.search(joined)),
        "has_timeout": bool(SIG_TIMEOUT.search(joined)),
        "has_version": bool(SIG_VERSION.search(joined)),
        "has_state_save": bool(SIG_STATE_SAVE.search(joined)),
        "has_log": bool(SIG_LOG.search(joined)),
    }
    # 只有"明确 OTA 语境"或"存在跳转迹象"才按升级链路规则审查；
    # 仅凭"有 flash 写"不足以判定为 bootloader（普通参数存储也写 flash），
    # 否则普通工程文件会被升级类规则刷屏。
    is_ota = sig["is_ota_ctx"] or bool(jump_hits)

    # ---- "该步骤可能由外部模块承担"的迹象（用于跨文件存疑降级）----
    verify_companion = bool(SIG_VERIFY_COMPANION.search(rawish_joined))
    irq_policy = bool(SIG_IRQ_POLICY.search(rawish_joined + "\n" + asm_text))
    delegated = bool(SIG_JUMP_DELEGATED.search(joined))
    CONFIRM = "【需人工确认·疑在外部模块完成】"

    issues, notes = [], []

    def add(rule_id, line, extra=None, severity=None, prefix=None):
        base_sev, title, desc_base, fix = RULES[rule_id]
        sev = severity or base_sev
        desc = desc_base if extra is None else f"{desc_base}｜{extra}"
        if prefix:
            desc = prefix + desc
        issues.append({
            "rule_id": rule_id,
            "severity": sev,
            "line": line,
            "title": title,
            "description": desc,
            "suggestion": fix,
        })

    # ---- R1/R2/R3：跳转相关（仅在检测到跳转迹象时判定）----
    if jump_hits:
        anchor = pick_jump_anchor(clean_lines, jump_hits)
        # 真实生产 bootloader 常多文件分工：本文件缺某步骤、但该步骤由框架或
        # 校验模块承担的迹象存在时，按低危提示输出并标注"需人工确认"，
        # 不直接按高危断言（避免对成熟工程误判）。
        if not sig["has_vtor"]:
            add(1, anchor, f"在 L{anchor} 检测到跳转现场，全文未见 SCB->VTOR / mtvec 赋值",
                severity="low" if delegated else "high",
                prefix=CONFIRM if delegated else None)
        if not sig["has_disable_irq"]:
            esc = delegated or irq_policy
            add(2, anchor, "全文未见 __disable_irq / CPSID / portDISABLE_INTERRUPTS"
                           + ("（本文件自行管理中断向量/使能）" if irq_policy else ""),
                severity="low" if esc else "high",
                prefix=CONFIRM if esc else None)
        if not sig["has_valid_check"]:
            esc = delegated or verify_companion
            add(3, anchor, "全文未见栈顶/向量表合法性检查"
                           + ("（检测到镜像校验模块迹象）" if verify_companion else ""),
                severity="low" if esc else "high",
                prefix=CONFIRM if esc else None)

    # ---- notes（不计分）：跳转被托管时避免"只报缺失"造成误读 ----
    for i, line in enumerate(clean_lines):
        m = SIG_JUMP_DELEGATED.search(line)
        if m:
            notes.append({
                "line": i + 1,
                "note": f"检测到 {m.group(0).rstrip('(').strip()}() —— 跳转由外部/框架实现，"
                        f"本文件不含跳转三步；请核对该实现是否设置向量表、关中断、校验 APP",
            })
            break

    # ---- R4：升级写 flash 但无完整性校验 ----
    if is_ota and sig["has_flash_write"] and not sig["has_integrity"]:
        first_write = next((i + 1 for i, l in enumerate(clean_lines) if SIG_FLASH_WRITE.search(l)), 1)
        # 跨文件分工：真实 bootloader 的整包校验常独立成模块（image_validate.c 等），
        # 本文件只负责搬运。检出校验模块迹象时降为低危并标注，交人工确认；
        # 无证据仍按高危报（配正反例测试，防借降级放水）。
        esc = verify_companion
        add(4, first_write,
            "检测到 flash 编程调用，但全文无 crc/checksum/sha 等校验"
            + ("（检测到镜像校验模块迹象）" if esc else ""),
            severity="low" if esc else "high",
            prefix=CONFIRM if esc else None)

    # ---- R5：擦除地址未按页对齐（逐行）----
    for i, line in enumerate(clean_lines):
        for match in RE_ERASE_CALL.finditer(line):
            token = match.group(1)
            try:
                addr = int(token, 0)
            except ValueError:
                continue
            if addr >= 0x1000 and not is_page_aligned(addr):
                add(5, i + 1, f"擦除地址 {token} 非 1K/2K/4K 整数倍")
                break

    # ---- R6：用了看门狗 + 有擦写，但没喂狗 ----
    # 豁免"显式关闭看门狗"：Arduino 长 OTA 的惯用做法就是先 ESP.wdtDisable()
    # 把 WDT 关掉，此时"没喂狗"是设计意图而非缺陷，报 R6 属误报。
    # 真正的风险（关了之后不恢复）改由 R15 判定。
    if sig["has_wdt_use"] and (sig["has_flash_write"] or sig["has_flash_erase"]) \
            and not sig["has_wdt_feed"] and not sig["has_wdt_off"]:
        add(6, 0, "检测到看门狗配置但全文无喂狗调用（擦写期间会被复位）")

    # ---- R7：分区地址硬编码（逐行，跳过 #define）----
    # 豁免「比较/掩码语境」：R3 建议的跳转校验写法 (pc & 0xFFE00001) != 0x08000001
    # 里的 0x08000001 是"校验常量"而非"寻址常量"——照抄 R3 修复代码不该反手
    # 被 R7 咬（建议与规则自相矛盾，2026-10-21 探针实测）。判定口径：
    # 地址出现在 ==/!=/& 的比较表达式里 → 豁免；地址作为函数实参/赋值右侧 → 照报。
    RE_ADDR_IN_COMPARE = re.compile(
        r"(?:[=!]=|&|\|)\s*0x08[0-9A-Fa-f]{6}"
        r"|0x08[0-9A-Fa-f]{6}\s*(?:[=!]=|&|\|)")
    for i, line in enumerate(clean_lines):
        stripped = line.strip()
        if stripped.startswith("#define"):
            continue
        if SIG_BARE_ADDR.search(line) and not RE_ADDR_IN_COMPARE.search(line):
            add(7, i + 1, "裸 flash 地址，建议改用分区表宏")
            break  # 同一文件只报一次，避免刷屏

    # ---- R8：接收死等无超时 ----
    if is_ota and not sig["has_timeout"]:
        for i, line in enumerate(clean_lines):
            if RE_WAIT_LOOP.search(line):
                add(8, i + 1, "while 等待外无超时机制（全文未见 timeout/tick 类变量）")
                break

    # ---- R9：无防降级版本校验 ----
    if is_ota and (sig["has_flash_write"] or jump_hits) and not sig["has_version"]:
        add(9, 0, "未见任何版本号比较逻辑"
                  + ("（检测到校验/回滚计数模块迹象）" if verify_companion else ""),
            severity="low" if verify_companion else "medium",
            prefix=CONFIRM if verify_companion else None)

    # ---- R10：升级状态未持久化 ----
    if is_ota and sig["has_flash_write"] and not sig["has_state_save"]:
        esc = bool(SIG_STATE_COMPANION.search(rawish_joined))
        add(10, 0, "本文件未见写 flash 的升级标志/进度存储"
                   + ("（检测到分区状态/触发标志模块迹象）" if esc else ""),
            severity="low" if esc else "medium",
            prefix=CONFIRM if esc else None)

    # ---- R11：flash 写未检查返回值（仅升级语境；逐行）----
    if is_ota:
        for i, line in enumerate(clean_lines):
            if not SIG_FLASH_WRITE.search(line):
                continue
            stripped = line.strip()
            # 豁免三类"不是调用点"的行：预处理/宏定义行、函数定义或声明行
            if stripped.startswith("#"):
                continue
            if RE_DEF_LIKE.match(line) and ";" not in line:
                continue
            # 返回值已被接住的形式豁免：
            #   a) 调用点左侧存在独立赋值号（覆盖 `ret = write(...)`，
            #      也覆盖 `size_t w = Update.write(...)` 这类"带类型的声明赋值"——
            #      旧版只认行首是 `名字 =` 的形态，带类型的那种会被漏豁免而误报）
            #   b) if (...) 判断
            #   c) return 带回
            mw = SIG_FLASH_WRITE.search(stripped)
            lhs = stripped[:mw.start()] if mw else ""
            if re.search(r"(?<![=!<>+\-*/%&|^])=(?!=)", lhs) or \
               re.match(r"^\s*[\w.\[\]\->*]+\s*[|&+\-*/]?=(?!=)", stripped) or \
               re.search(r"\bif\s*\(", stripped) or stripped.startswith("return"):
                continue
            # 只对「有返回状态码语义」的写 API 判 R11；签名未知的第三方写函数
            # （可能是 void，如 wolfBoot ext_flash_write）不纳入，避免纯噪音。
            if SIG_FLASH_WRITE_STATUS.search(stripped):
                add(11, i + 1, "建议接住并判断返回值 / 状态码")
                break

    # ---- R12：无进度日志 ----
    if is_ota and not sig["has_log"]:
        add(12, 0, "全文未见任何日志输出调用")

    # ---- R13：硬编码延时（仅 OTA 语境；普通业务代码的 delay 不算升级隐患）----
    if is_ota:
        for i, line in enumerate(clean_lines):
            md = SIG_DELAY.search(line)
            if not md:
                continue
            # 豁免一：短延时当"让出 CPU / 节流"用，不算魔数延时
            # （Arduino 的 delay(2)/delay(10)、ESP 的 delay(5) 都是给协议栈喘气）
            mnum = re.search(r"(\d+)$", md.group(0))
            if not mnum or int(mnum.group(1)) < DELAY_MAGIC_MIN_MS:
                continue
            # 豁免二：系统复位/重启前的短延时（等串口 FIFO 发完、电源稳定），
            # 属于必要的硬件时序，不是"用魔数延时替代状态轮询"。
            window = "\n".join(clean_lines[i:i + 4] + clean_lines[max(0, i - 3):i])
            if re.search(r"\b\w*(?:reset|reboot|restart|atexit)\w*\s*\(", window, re.IGNORECASE):
                continue
            # 豁免三：延时外面套着"带超时的轮询"，此时延时就只是轮询间隔，
            # R13 建议的"状态轮询+超时"已经做到了。框架写法里两者常分居两行：
            #   while (WiFi.status() != WL_CONNECTED && millis() < deadline) {
            #       delay(100);          ← 只判本行会漏掉上一行的 millis()
            #   }
            # 故查前后 3 行窗口，而不是只看本行。
            if re.search(r"millis\s*\(\s*\)|micros\s*\(\s*\)|deadline|timeout|"
                         r"HAL_GetTick|esp_timer_get_time|elapsed|expire",
                         window, re.IGNORECASE):
                continue
            # 豁免四：Arduino 的 loop() 是框架的空闲主循环（等价 while(1)），
            # 它里面的 delay 是节拍器，跟升级流程无关——报"升级流程中的硬编码延时"
            # 属于事实错误。向上找回最近的函数头，若落在 loop() 体内则跳过。
            in_loop = False
            for j in range(i, max(-1, i - 12), -1):
                if re.search(r"\bvoid\s+loop\s*\(\s*\)", clean_lines[j]):
                    in_loop = True
                    break
                if j != i and clean_lines[j].strip().startswith("}"):
                    break
            if in_loop:
                continue
            add(13, i + 1, "延时魔数依赖主频，建议改状态轮询+超时")
            break

    # ---- R14：有 flash 写但全文无擦除（NOR flash 写前必须擦）----
    if is_ota and sig["has_flash_write"] and not sig["has_flash_erase"]:
        first_write = next((i + 1 for i, l in enumerate(clean_lines)
                            if SIG_FLASH_WRITE.search(l)), 1)
        if SIG_FRAMEWORK_FLASH.search(joined):
            # Arduino 的 Update/Updater 在库内部完成擦除，sketch 里结构上不可能
            # 看到 erase 调用——在框架层报 R14 恒为误报，降成不计分的提示。
            notes.append({
                "line": first_write,
                "note": "检测到 Arduino Update/Updater 框架写 flash：擦除由该库内部"
                        "完成，本文件看不到 erase 属正常；请核对该库版本的行为",
            })
        else:
            # 降级证据允许来自注释/声明（只降不升，方向保守）
            esc = bool(re.search(r"\berase\b", raw_joined, re.IGNORECASE))
            add(14, first_write, "全文未见 flash 擦除调用"
                      + ("（文件内出现 erase 字样，疑由其它模块或驱动内部擦除）" if esc else ""),
                severity="low" if esc else "medium",
                prefix=CONFIRM if esc else None)

    # ---- R15：显式关闭看门狗后未见恢复（框架层特有砖因）----
    # 恢复 = feed 或 rearm（enable/start）任一；只看 feed 会咬掉"照建议代码
    # 用 wdt_enable 恢复"的规范写法（2026-10-21 修复）。
    if is_ota and sig["has_wdt_off"] \
            and not (sig["has_wdt_feed"] or sig["has_wdt_rearm"]):
        off_line = next((i + 1 for i, l in enumerate(clean_lines)
                         if SIG_WDT_OFF.search(l)), 0)
        add(15, off_line, "检测到关闭看门狗，但全文未见 wdtEnable / wdtFeed 恢复调用")

    issues.sort(key=lambda x: ({"high": 0, "medium": 1, "low": 2}[x["severity"]], x["line"]))
    summary = {
        "high": sum(1 for x in issues if x["severity"] == "high"),
        "medium": sum(1 for x in issues if x["severity"] == "medium"),
        "low": sum(1 for x in issues if x["severity"] == "low"),
    }
    summary["total"] = len(issues)
    score = max(0, 100 - sum(SEVERITY_WEIGHT[x["severity"]] for x in issues))
    return {"file": filename, "success": True, "issues": issues, "notes": notes,
            "summary": summary, "score": score, "signals": sig}


def review_file(path: str) -> dict:
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        return {"file": path, "success": False, "error": str(exc), "issues": [], "notes": [],
                "summary": {"high": 0, "medium": 0, "low": 0, "total": 0}, "score": 100}
    result = review_text(text, os.path.basename(path))
    result["path"] = path
    return result


def review_directory(root: str) -> dict:
    files, skipped = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in ("__pycache__", ".git", "build", "output", "Debug", "Release")]
        for name in sorted(filenames):
            if not name.endswith(SOURCE_EXTS):
                continue
            full = os.path.join(dirpath, name)
            res = review_file(full)
            res["file"] = os.path.relpath(full, root).replace(os.sep, "/")
            files.append(res)
            if not res.get("success"):
                skipped.append(res["file"])
    totals = {"high": 0, "medium": 0, "low": 0, "total": 0}
    for res in files:
        for key in ("high", "medium", "low", "total"):
            totals[key] += res["summary"][key]
    ranked = sorted([f for f in files if f["summary"]["total"] > 0],
                    key=lambda f: -f["summary"]["total"])[:5]
    return {
        "root": root,
        "success": True,
        "files_scanned": len(files),
        "files": files,
        "summary": totals,
        "top5_files": [{"file": f["file"], "total": f["summary"]["total"],
                        "high": f["summary"]["high"], "score": f["score"]} for f in ranked],
        "skipped": skipped,
    }


# --------------------------------------------------------------------------
# HTML 报告
# --------------------------------------------------------------------------
SEV_COLOR = {"high": "#d93026", "medium": "#e8a33d", "low": "#8a94a6"}
SEV_LABEL = {"high": "高危", "medium": "中危", "low": "低危"}


def overall_score(result: dict) -> int:
    """单文件取自身评分；目录取"扣分总和"折算的整体分（0~100）。"""
    if "files" in result:
        return max(0, 100 - sum(SEVERITY_WEIGHT[i["severity"]]
                                for f in result["files"] for i in f["issues"]))
    return result["score"]


def to_html(result: dict, title: str = "OTA 升级链路审计报告") -> str:
    is_dir = "files" in result
    summary = result["summary"]
    score = overall_score(result)
    rows = []
    bar = []
    for sev in ("high", "medium", "low"):
        count = summary[sev]
        bar.append(f'<span class="bar-seg" style="background:{SEV_COLOR[sev]};flex:{max(count,0.001)}"></span>')
        rows.append(f'<span class="pill" style="background:{SEV_COLOR[sev]}">{SEV_LABEL[sev]} {count}</span>')

    detail = []
    targets = result["files"] if is_dir else [result]
    for res in targets:
        if not res["issues"] and not res.get("notes"):
            continue
        rows_html = []
        for issue in res["issues"]:
            rows_html.append(
                f'<tr><td class="sev" style="color:{SEV_COLOR[issue["severity"]]}">'
                f'{SEV_LABEL[issue["severity"]]}</td>'
                f'<td class="rid">R{issue["rule_id"]}</td>'
                f'<td>{"L%d" % issue["line"] if issue["line"] else "全文"}</td>'
                f'<td class="ttl">{issue["title"]}</td>'
                f'<td class="desc">{issue["description"]}</td></tr>')
        notes_html = "".join(
            f'<li>L{n["line"]}：{n["note"]}</li>' for n in res.get("notes", []))
        notes_block = (f'<div class="notes"><b>提示（不计分，供人工核对）</b>'
                       f'<ul>{notes_html}</ul></div>') if notes_html else ''
        table_block = (f'<table><thead><tr><th>级别</th><th>规则</th><th>位置</th><th>问题</th>'
                       f'<th>说明 / 修复建议</th></tr></thead>'
                       f'<tbody>{"".join(rows_html)}</tbody></table>') if rows_html else ''
        detail.append(
            f'<section><h3>{res["file"]} <small>评分 {res["score"]}/100 · '
            f'{res["summary"]["total"]} 个问题</small></h3>'
            f'{table_block}{notes_block}</section>')

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
 *{{box-sizing:border-box}}
 body{{margin:0;padding:32px;background:#f5f6f8;color:#1f2430;
   font:14px/1.65 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif}}
 .wrap{{max-width:1080px;margin:0 auto}}
 h1{{font-size:22px;margin:0 0 4px}}
 .sub{{color:#6b7280;margin-bottom:24px}}
 .card{{background:#fff;border-radius:10px;padding:20px 22px;margin-bottom:18px;
   box-shadow:0 1px 3px rgba(16,24,40,.08)}}
 .score{{font-size:40px;font-weight:700;line-height:1}}
 .bar{{display:flex;height:10px;border-radius:5px;overflow:hidden;margin:14px 0 10px;background:#eceff3}}
 .bar-seg{{display:block;height:100%}}
 .pill{{display:inline-block;color:#fff;border-radius:12px;padding:2px 10px;margin-right:8px;font-size:12px}}
 section{{background:#fff;border-radius:10px;padding:18px 20px;margin-bottom:16px;
   box-shadow:0 1px 3px rgba(16,24,40,.08)}}
 h3{{font-size:15px;margin:0 0 12px;word-break:break-all}}
 h3 small{{color:#6b7280;font-weight:400;font-size:12px;margin-left:6px}}
 table{{width:100%;border-collapse:collapse;font-size:13px}}
 th{{text-align:left;color:#6b7280;font-weight:600;border-bottom:1px solid #e5e7eb;padding:8px 6px}}
 td{{border-bottom:1px solid #f0f2f5;padding:9px 6px;vertical-align:top}}
 .sev{{white-space:nowrap;font-weight:600}}
 .rid{{color:#6b7280;white-space:nowrap}}
 .ttl{{font-weight:600}}
 .desc{{color:#4b5563}}
 .notes{{margin-top:12px;padding:10px 12px;background:#f3f6fb;border-left:3px solid #7c93b8;
   border-radius:0 6px 6px 0;color:#40506b;font-size:12.5px}}
 .notes ul{{margin:6px 0 0;padding-left:18px}}
 footer{{color:#9aa3b2;font-size:12px;text-align:center;margin-top:24px}}
</style></head><body><div class="wrap">
<h1>{title}</h1>
<div class="sub">目标：{result.get("root") or result.get("path") or result.get("file")}
 {'· 扫描文件 %d 个' % result["files_scanned"] if is_dir else ''}</div>
<div class="card">
  <div class="score" style="color:{SEV_COLOR['high'] if summary['high'] else (SEV_COLOR['medium'] if summary['medium'] else '#2f9e5f')}">{score}<span style="font-size:14px;color:#6b7280">/100</span></div>
  <div class="bar">{''.join(bar)}</div>
  <div>{''.join(rows)}<span style="color:#6b7280">共 {summary['total']} 个问题</span></div>
</div>
{''.join(detail) if detail else '<section><h3>未发现问题</h3><p>没有命中任何防砖规则。仍建议人工复核升级流程的中断/向量表切换时序。</p></section>'}
<footer>由 embedded-ota-toolkit / ota_audit.py 生成 · 静态分析结果，不替代上板实测与硬件在环验证</footer>
</div></body></html>"""


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="ota_audit.py",
        description="嵌入式 OTA/Bootloader 升级链路静态审计 1.0.0（15 条防砖规则）",
        epilog="""示例：
  python ota_audit.py bootloader.c
  python ota_audit.py bootloader.c high
  python ota_audit.py sketch.ino
  python ota_audit.py --dir ./boot --html ota_report.html
""")
    parser.add_argument("file", nargs="?", help="待审计源码文件")
    parser.add_argument("level", nargs="?", default="all",
                        choices=["all", "high", "medium", "low"], help="只输出该级别及以下")
    parser.add_argument("--dir", help="批量扫描目录（.c/.h/.cpp/.hpp/.ino/.pde）")
    parser.add_argument("--html", help="生成 HTML 报告到指定路径")
    parser.add_argument("--json", action="store_true", help="强制输出 JSON（默认即 JSON）")
    parser.add_argument("--fail-under", type=int, metavar="N", dest="fail_under",
                        help="评分低于 N 时返回退出码 1（CI 门禁用；缺省按是否存在问题判定）")
    args = parser.parse_args(argv)

    if not args.file and not args.dir:
        parser.print_help()
        return 2

    if args.dir:
        if not os.path.isdir(args.dir):
            print(f"目录不存在：{args.dir}", file=sys.stderr)
            return 2
        result = review_directory(args.dir)
    else:
        if not os.path.isfile(args.file):
            print(f"文件不存在：{args.file}", file=sys.stderr)
            return 2
        result = review_file(args.file)

    if args.level != "all":
        keep = {"high": ("high",), "medium": ("high", "medium"),
                "low": ("high", "medium", "low")}[args.level]
        targets = result["files"] if "files" in result else [result]
        for res in targets:
            res["issues"] = [i for i in res["issues"] if i["severity"] in keep]

    if args.html:
        with open(args.html, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(to_html(result))
        result["html_report"] = args.html

    if "files" in result:
        result["score"] = overall_score(result)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.fail_under is not None:
        return 0 if result["score"] >= args.fail_under else 1
    return 1 if result["summary"]["total"] else 0


if __name__ == "__main__":
    sys.exit(main())
