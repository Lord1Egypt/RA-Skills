# 核验规则细节（E01–E12）

每条规则给出：**判定方式、会报/不会报示例、边界与已知限制、复核方法**。所有判定只依赖 SVD 与代码
文本（词法级，不执行代码）；**不确定时进"未判定"**，不产生错误。计数口径与条件编译块口径见文末。

示例中带来源的取自真实语料（`benchmarks/verify-dogfood.md`），其余为合成用例。

## E01 外设不存在（报 / 已核验 / 高）

- 判定：`外设->寄存器` 的"外设"是形如 `USART1`/`TIM2` 的全大写标识符，但在 SVD 的外设清单里不存在。
- 会报：`TIM2->CR1 |= TIM_CR1_CEN;`（芯片 SVD 中只有 TIM1）
- 不会报：
  - `hi2c1->Init` 这类小写/驼峰局部指针（静默忽略，不计入统计）；
  - `SysTick->CTRL`（内核外设 → 未判定）；
  - `DMA1_Channel1->CCR`（疑似簇寄存器命名 → 未判定，见"通道名同义写法"）；
  - 位于 `#if/#ifdef` 块内且目标不存在（→ 未判定，见"条件编译块口径"）。
- 厂商别名自动映射（不报）：`NRF_USBD` → `USBD`、`R_PORT0` → `PORT0`、`GPIO` → `GPIO_S`（Silabs
  Series 2 安全别名）、`R_GPT0` → `GPT320`（外设指针宏按地址解析，配 `--headers`）。
- 复核：`lookup <名字>` 或 `search <关键词>`；报告里带拼写建议（编辑距离最近的 3 个外设）。

## E02 寄存器不存在（报 / 已核验 / 高）

- 判定：外设存在，但寄存器名不在该外设的寄存器清单里。
- 会报：`USART1->CR9 = 1;`（应为 CR1）
- 不会报：
  - `DMA1->CH1`（簇前缀 → 未判定）；
  - `PORT->Group[ulPort].DIRSET`（组号为运行时表达式 → 未判定"数字后缀寄存器组"）；
  - `R_PFS->PORT[x].PIN[y].PmnPFS`（层级/下标无法静态映射 → 未判定）；
  - `clocks_hw->resus.ctrl`（**嵌套结构体成员名**：SVD 里是扁平名 `CLK_SYS_RESUS_CTRL` 时按
    "下划线拼接名后缀唯一匹配"自动对应；匹配不到唯一寄存器时记"多段成员名"未判定，不报 E02）；
  - 条件编译块内的不存在写法（→ 未判定）。
- 复核：`lookup <外设>` 看寄存器清单；报告带同外设寄存器拼写建议。

## E03 字段宏不存在或与寄存器不符（报 / 已核验 / 高）

- 判定：把全大写（或 `_Msk`/`_Pos` 后缀）的标识符按 CMSIS 约定映射到"外设 → 寄存器 → 位域"：
  1. 去掉 `_MSK/_MASK/_POS/_SHIFT` 后缀；
  2. 前缀匹配外设家族名（`USART1`→`USART`、`GPIOA`→`GPIO`、`TIM1`→`TIM`、`DMA1_Channel1`→`DMA`）；
  3. 剩余部分尝试各种切分，找"寄存器名 + 位域名"（寄存器名支持前缀匹配，如宏 `CCMR1` 对应
     SVD 的 `CCMR1_Output`；寄存器名后带实例号时按数字匹配，宏 `CCR` ↔ SVD `CCR1..CCR8`）；
  4. 位域名后多出的部分是枚举名时视为枚举值宏（如 `USART_CR1_PS_ODD`）。
- 会报：
  - `USART1->CR1 |= USART_CR1_XXX;`（位域 XXX 不存在）
  - `USART1->CR1 |= USART_BRR_DIV;`（宏属于 BRR，写的是 CR1）
  - `USART1->CR1 |= USART_CR1_PS_EVEEN;`（PS 之后的 EVEEN 不是枚举名，疑似拼写错误）
- 不会报：`USART_CR1_PS_ODD`（合法枚举宏）；文件内 `#define` 能解析的数值宏（如 `UART_BAUD_VALUE`）；
  带编号的位域组（`EIC_INTENSET_EXTINT(inMask)`，编号来自运行参数 → 未判定）；
  条件编译块内（→ 未判定）。
- 复核：`lookup <外设>.<寄存器>` 看位域清单；报告带同寄存器位域拼写建议。

## E04 值超出宽度（报 / 已核验 / 高）

- 判定：右值（或 `MODIFY_REG` 的置位值）能求值，且超过目标位宽：
  - 普通寄存器写入：按**寄存器**位宽（`reg.size`）；
  - **位域直写**（`REG.FIELD = v`、`.bit.FIELD = v`、`REG_b.FIELD = v`）：按**位域**位宽（字段相对，
    只查 `=` 形态；`|=` 等掩码语义不按位宽报）；
  - **`MODIFY_REG(reg, Msk, value)`**：清位掩码映射到唯一字段时按该字段核验——`value` 支持两种
    约定：**字段相对**（≤ 掩码）与 **ST 风格带位置**（`VALUE << Pos`，位域之外的位为 0）都视为合法；
    位域之外置位才报（如 PS 在 bit 9 时 `0x400`）。
- 会报：
  - `TIM1->CR1 = 0x1FFFF;`（16 位寄存器）
  - `MODIFY_REG(CR1, PS_Msk, 0x4)`（1 位位域）
  - `PORT->Group[0].PINCFG[4].bit.PMUXEN = 3;`（PMUXEN 位宽 1）
  - `R_ICU->IELSR_b[0].IR = 2;`（FSP 位域视图，IR 位宽 1）
- 不会报：值中含变量、函数调用等无法求值时（进"未判定"）。
- 复核：`lookup <路径>` 看宽度/位域；`set`/`decode` 可算合法范围。

## E05 枚举值不合法（报 / 已核验 / 中）

- 判定：目标位域有 `enumeratedValues`、写入值可求值、且不匹配任何枚举（含 `#1xx` 这类任意位模式）：
  - `MODIFY_REG` 的清位掩码映射到唯一一个位域时，按**置位值**核验；
  - `REG_SET_FIELD` 按**字段值**核验；
  - **位域直写**（`REG.FIELD = v`、`.bit.FIELD = v`、`REG_b.FIELD = v`）按**字段值**核验（只查 `=`）。
- 会报：`MODIFY_REG(TIM1->CR2, TIM_CR2_MMS_Msk, 0x2);`（MMS 只有 RESET/ENABLE/COMPARE）；
  `TIM1->CR2.MMS = 0x2;`（位域直写）
- 不会报：值与某个枚举匹配（含掩码匹配）；位域带 **`isDefault` 默认项**（SVD 声明"其余取值"合法）时
  一律不报（如 `<enumeratedValue><name>OTHER</name><isDefault>true</isDefault>`）；
  `|=` 等掩码语义的字段写入不查枚举。
- 复核：`lookup <寄存器>.<位域>` 看枚举表（默认项显示为"（其余值，默认）"）；`set` 支持用枚举名写值。

## E06 无效清位（报 / 需查手册 / 低）

- 判定：`CLEAR_BIT(reg, FIELD)` 或 `reg &= ~FIELD`，对应位域的复位值为 0，且**本文件**中从未出现
  对该位域的置位（`|=`、`SET_BIT`、可求值的直接写等）。
- 会报：先清 `USART1->CR1.M0`，但全文件都没有置位过 M0。
- 不会报：
  - `MODIFY_REG` 的清位掩码（属于常规用法）；
  - Flag/状态类位（名字含 FLAG/SR/STATUS 等语义时降级不报——libopencm3 试跑校准）；
  - 寄存器在本文件里被整体读过（读改写语义不确定时保守跳过）。
- 注意：这是"低严重度"提示，可能是有意为之；命中时标签为"需查手册"。
- 复核：`lookup <路径>` 看复位值；对照手册确认该位是否需要先置位。

## E07 访问前未见时钟使能（报 / 需查手册 / 中）

- 判定：写入某外设（如 `USART2`）时，在 RCC/CMU 等"时钟外设"中能找到名为 `<外设>EN` 的位域
  （如 `APB1ENR.USART2EN`、CMU 的 `CLKEN0.GPIO`），但本文件里既没有对该位域的置位，也没有
  可识别的使能调用（`__HAL_RCC_USART2_CLK_ENABLE()`、libopencm3 `rcc_periph_clock_enable(RCC_USART2)`、
  `rcc_enable_rtc_clock()` 等）。
- 会报：`USART2->CR1 |= USART_CR1_UE;` 而全文件没有开 USART2 时钟。
- 不会报：先 `RCC->APB1ENR |= RCC_APB1ENR_USART2EN;`，或存在上述使能宏调用；
  RCC/CMU 里找不到 `<外设>EN` 形态的关联位时跳过该外设（如 Renesas MSTP 的 `MSTPB6` 命名无外设关联、
  ESP-IDF 走 `periph_module_enable`——均不报，不会误伤）。
- 边界：**文件级**判定。使能写在其它文件时是误报，请加 `--no-clock-check`；库文件由调用方管时钟的
  情况属于已知限制（libopencm3 语料 2 处）。
- 复核：`lookup <时钟寄存器>` 确认使能位；`--no-clock-check` 关闭本规则。

## E08 硬编码地址（报 / 已核验 / 高）

- 判定：`*(volatile uint32_t *)0x...`（含双括号 `*((...)0x...)`）、C++ `*reinterpret_cast<...>(0x...)`、
  `HWREG(0x...)`（TI 风格）、`_SFR_MEM8(0x...)`（AVR）、`*(volatile uint32_t *)(0x... + 0x..)`（**纯字面量表达式**）
  等直接地址写入；用地址反查给出对应寄存器名（若有）。
- 会报：`*(volatile uint32_t *)0x40013800 = 1;`（= USART1.CR1）
- AVR 数据空间口径：SVD 用"0x800000 + 数据地址"（如 `PORTB = 0x800025`）时，低地址（`< 0x10000`）
  自动做一次偏移探测——`*(volatile uint8_t *)0x25 = 1;`、`_SFR_MEM8(0x25) = 1;`、
  `_SFR_IO8(0x05) = 1;`（I/O 空间，+`__SFR_OFFSET`）都会核到 `PORTB.PORTB`，
  报告里注明"SVD 地址 0x00800025"。
- 不会报：
  - 文件内"地址别名宏"写法（`#define REG (*(volatile uint32_t *)0x...)` 后的 `REG = 1;`）——
    定义已经给了名字，按该地址对应的寄存器正常核验；
  - **具名表达式地址**（`HWREG(UART0_BASE + UART_O_CTL)`、`*(volatile uint32_t *)(PORT_BASE + 0x04)`）
    ——宏组合出的具名地址按具名寄存器核验，不报 E08。
- 未判定：地址表达式解析不出（依赖 SDK 头文件常量、运行时基址）时；`_SFR_IO8` 缺 `__SFR_OFFSET`
  定义时（不猜偏移，记"地址表达式无法求值"）；别名宏地址在 SVD 中不存在时。
- 复核：`addr 0x...` 反查寄存器（低地址同样做 AVR 口径探测，输出里注明）。

## E09 中断分组多处设置（报 / 需查手册 / 中）

- 判定：同一文件出现多处 `NVIC_SetPriorityGrouping`。
- 会报：两处 `NVIC_SetPriorityGrouping(3);`——互相覆盖，需确认哪一处生效。
- 复核：确认工程的统一分组策略；`lookup irq <中断>` 查中断号与 NVIC 使能位。

## E10 写只读寄存器或位域（报 / 已核验 / 高）

- 判定（四种都算）：
  1. 目标寄存器 `access` 为 `read-only`；
  2. 写入表达式中映射到的位域 `access` 为 `read-only`（含 `SET_BIT/CLEAR_BIT/MODIFY_REG` 的参数）；
  3. 数值参数命中寄存器中只读位域的位（结构体写、`SET_BIT/CLEAR_BIT/WRITE_REG` 的掩码/值、
     `MODIFY_REG` 的置位值；如 `RCC->CR = 0x400` 或 `SET_BIT(RCC->CR, 0x400)` 命中只读的 `HSIRDY`）；
  4. **位域直写**（`REG.FIELD = v`、`.bit.FIELD = v`、`REG_b.FIELD = v`）命中只读位域。
- 会报：`USART1->SR = 0x20;`（SR 只读）；`RCC->CR = 0x400;`（HSIRDY 只读）；
  `CMU->CALCNT = 100U;`（Silabs Series 2 的 CALCNT 只读）。
- 不会报/降级：
  - 位于 `#if/#ifdef` 块内的只读写入 → 未判定（访问属性随型号/配置而异，Gecko Series 1/2 分支
    里 `CALCNT` 在 Series 2 只读——真实语料校准）；
  - 位域直写时值按字段相对处理，不做寄存器级"数值命中只读位"扫描（避免错位误报）；
  - `MODIFY_REG` 清位掩码映射到唯一字段且置位值为字段相对（≤ 掩码）时，跳过只读位扫描
    （数值的位位置与寄存器位不对应，扫描会错位误报）；带位置取值照常扫描。
- 复核：`lookup <路径>` 看访问属性。

## E11 使能后写 DMA 配置寄存器（报 / 需查手册 / 中）

- 判定（文件级、文本级，不依赖外设名能否解析——簇命名 `DMA1_Channel1` 也覆盖）：
  同外设前缀下，「使能」之后又写「DMA 计数/地址寄存器」，且中间没有关闭动作。
- 使能：语句里出现 `..._EN` / `..._ENABLE` 宏（如 `DMA_CCR_EN`、`DMA_SxCR_EN`），
  且是 `=` / `|=` 或 `SET_BIT` / `WRITE_REG`；关闭：`&=` 或 `CLEAR_BIT` 同类宏。
- 数值形式：对 DMA 控制寄存器（`CCR`/`CR`/`CHCTL`/`CTL`）写入的数值 **bit0=1** 也按"使能"识别
  （`DMA1_Channel1->CCR |= 0x00000001;`）；`=` 写或 `&=`/清位掩码 bit0=0 按"关闭"识别。
- 配置寄存器：`CNDTR`、`NDTR`、`CMAR`、`CPAR`（DMA 传输数量/外设地址/内存地址）。
- 会报：`DMA1_Channel1->CCR |= DMA_CCR_EN;` 之后才 `DMA1_Channel1->CNDTR = 0x100;`；
  或 `DMA1_Channel1->CCR |= 0x00000001;` 之后再写 `CNDTR`。
- 不会报：先写 `CNDTR/CMAR/CPAR` 再置 `EN`；或先清 `EN`、改完配置再置回；
  其它外设名/寄存器名不满足上述形态的写入不参与判定。
- 说明：这是保守的启发式规则，误报请对照手册；命中时标签为"需查手册"。
- 复核：`lookup <DMA 寄存器>` 看使能位；对照手册确认"使能后能否改配置"。

## E12 只写寄存器读改写（报 / 需查手册 / 中）

- 判定：读改写形态作用于 SVD 中 `access="write-only"` 的寄存器（读回值可能为 0 或未定义）：
  - `|=` / `&=` / `^=`；
  - `SET_BIT` / `CLEAR_BIT`；
  - **`MODIFY_REG`**（先读回、改掩码位、再写回——同样是读改写）；
  - **`REG_SET_FIELD` / `REG_CLR_FIELD`**（ESP-IDF 字段宏，地址可解析时）。
- 会报：`CRC_CR |= CRC_CR_RESET;`（libopencm3 `crc_common_all.c`——真实库代码的已知限制，
  按 SVD 数据口径如实报出）；`MODIFY_REG(PORTX->BSRR, 0x1, 0x1);`（write-only 寄存器）。
- 不会报/降级：
  - `=` 直写、`WRITE_REG` / `REG_WRITE`（正确写法）；
  - 只读寄存器（走 E10）；
  - 位于 `#if/#ifdef` 块内 → 未判定（访问属性随型号/配置而异）；
  - ESP-IDF 寄存器号常量宏无法解析地址时（走未判定，不猜）。
- 复核：`lookup <寄存器>` 看访问属性；建议改用置位/清位寄存器或直接赋值。
  `lookup`/`decode --write`/`set` 也会给出读改写陷阱提示：`modifiedWriteValues`（写 1 清零等）
  以及 `readAction=modifyExternal`（读后由硬件修改）两类语义都会提示。

## E13 写 1 清零寄存器的读改写（报 / 需查手册 / 中）

- 判定：读改写形态（`|=` / `&=` / `^=` / `SET_BIT` / `CLEAR_BIT` / `MODIFY_REG` /
  `REG_SET_FIELD` / `REG_CLR_FIELD`）作用于 SVD 中带 `modifiedWriteValues="oneToClear"`
  （写 1 清零）的寄存器——寄存器级或位域级都算——**且这些写 1 清零位没有被本次写入的掩码覆盖**。
- 语义：读改写会先读回寄存器、再整体写回——写 1 即清零，所以**没被掩码提到的写 1 清零位**
  一旦当前置位，会被顺带清零（若对应其它中断源，可能丢中断）。掩码提到的位是代码本意要动的，
  不算误伤。
- 会报：`UART0->UARTICR |= 0x10;`（UARTICR 有 TXIC/RTIC 两个 W1C 位，`0x10` 只提到 TXIC，
  RTIC 未被覆盖——RP2040 真实 SVD）；`EXTI->PR |= EXTI_PR_P0;`（PR 的 P1..P15 都是 W1C，
  清 P0 会顺带清掉其它挂起线）。
- 不会报：
  - 直写（正确写法）：`UART0->UARTICR = 0x10;`（只清目标标志）；
  - **掩码覆盖了全部 W1C 位**：`UART0->UARTICR |= TXIC_Msk | RTIC_Msk;`、
    `ADSR |= ADF_Msk;`（唯一 W1C 位被提到——只清代码明确要清的标志）；
  - 只写寄存器（走 E12）；只读寄存器（走 E10）；
  - 寄存器无 `modifiedWriteValues` 数据时（不猜——很多厂商 SVD 不带该属性）；
  - 位于 `#if/#ifdef` 块内 → 未判定（写语义随型号/配置而异，与 E10/E12 同口径）。
- 未判定：读改写掩码无法静态求值（如 `REG |= flags;` 中的变量）→ 无法确认覆盖范围，
  记未判定（不猜）。
- 复核：`lookup <寄存器>` 看写语义（`modifiedWriteValues`）；`decode --write`/`set` 也会给出
  读改写陷阱提示。

## 计数口径

| 计数 | 含义 |
|---|---|
| `writes` | 计入统计的寄存器写入总数（= 报 + 未判定 + 通过） |
| `report` | 命中 E 规则（"报"桶）；`report_by_class` 给出按规则号的条数（如 `{"E04": 2, "E10": 1}`） |
| `undetermined` | 范围外/无法确定，逐条给出原因（"未判定"桶）；`undetermined_by_category` 给出原因分布 |
| `passed` | 命中写入形态、目标可映射、未触发任何规则（"通过"桶） |

文本输出的汇总行带按类计数（`报 3（E04 2、E10 1）`）与未判定原因分布
（`未判定分布：条件编译块内 9、运行时值/下标 1`），便于快速判断"系统性未判定"的来源。

**静默忽略、不计入统计**（保持 0 误报的关键口径）：

- 局部变量/指针成员访问（`p->len = 0`、`base->C1 = x`、`hi2c1.Init.X`、`p_ctrl->p_reg->DACR_b.DAOE0`）——
  运行时地址，无法静态定位；
- 与设备中**非唯一**寄存器名撞名的普通变量赋值（AVR/MSP430 裸名口径：仅唯一名核验）；
- `HWREGBIT*(&变量, n)` 这类 RAM 位带访问；
- HAL/LL 函数调用（`HAL_GPIO_WritePin`、`R_GPT_Open` 等——写入在函数内部，调用点不可见）。

## 条件编译块口径

目标（外设/寄存器/位域）**不存在**、或**访问属性类问题（E10/E12/E13）**出现在 `#if/#ifdef/#ifndef`
块内时 → 记"未判定"并注明"可能是其它型号/配置的分支"。厂商库源码常在一个文件里用 `#if` 区分芯片
家族（FSP 的 `R_GPT_ODC`、`R_ICU->INTSELR`；Gecko 的 Series 1/2 分支；Arduino 的 `#if defined(...)`）。
条件块**外**照常报 E01/E02/E03/E10/E12/E13。

## 补丁模式口径

`--patch` 只核验**新增行**：在磁盘上找到完整文件时（按当前目录与补丁所在目录查找），
置位/时钟使能等文件级上下文取自整文件——E06/E07/E11 不会因"看不到未改动的使能/置位"而误报；
找不到完整文件时按"仅新增行"核验，并在输出里明确提示（建议在仓库目录内运行或加
`--no-clock-check`）。新增行的行号按新文件对齐，与代码编辑器里的行号一致。

## 已知限制汇总

- **E07 是文件级判定**：使能写在其它文件时误报，加 `--no-clock-check` 关闭；
- **SVD 完整性**：设备 SVD 缺寄存器时（如 RA6M4 的 `INTSELR`、MG12P 的 `CMUROUTE`）报 E02——
  若该写法位于条件块内则记未判定；条件块外建议先 `lookup`/手册核对，或换更完整的 SVD；
- **内核外设**（NVIC/SysTick/SCB/CoreDebug）不在设备 SVD 中 → 未判定；
- **指针参数风格**（`base->REG`、`p_reg->REG_b.FIELD`）无法静态定位 → 静默忽略；
- **SVD 命名差异**：`REG_b` 位域视图、`_S` 安全别名、外设指针宏等已自动映射；仍无法对应时记未判定
  并注明原因，不会猜；
- **计数只统计"能看到目标"的写入**，静默忽略项不影响 `writes` 口径。

## 复核方法（与百事通闭环）

- 每条"报"带 `next`（可直接执行的 `embedded-register-lookup` 命令，已带本次 SVD 参数）；
- 加 `--explain` 时报告内联寄存器/位域定义（含**写/读语义**与**相关置位/清位寄存器建议**）；
- 复查清单（`--checklist`）分组：芯片默认（写入等于复位值）/ 已核验 / 需查手册（E06/E07/E09/E11/E12
  与未判定）/ 需实测（涉及 DMA、NVIC、SysTick 的写入）。
