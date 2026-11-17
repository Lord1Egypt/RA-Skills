# 支持的写法与限制

## 写入抽取（词法层）

1. 拼接反斜杠续行（保留与原始行号的对应关系）。
2. 去注释与字符串/字符字面量（替换为空格，等长、保留换行）。
3. 跳过预处理行；收集对象宏 `#define NAME <表达式>`。
4. 按分号切分语句：圆括号内不分号；`{` / `}` 视为语句边界（函数体不会被当成一条巨语句）。
5. 在每条语句里按顺序找：CMSIS 宏调用（`SET_BIT/CLEAR_BIT/MODIFY_REG/WRITE_REG/READ_REG`）
   → 地址访问宏（TI `HWREG/HWREGB/HWREGH`、`HWREGBITW/H/B(x, bit)`；libopencm3 `MMIO8/16/32`；
   GD32 等 `REG8/16/32`；AVR `_SFR_MEM8/16/32`、`_SFR_IO8/_SFR_IO16`（I/O 空间，按 `__SFR_OFFSET`
   换算，缺定义记"未判定"不猜））：地址为**纯字面量**时按直接地址（报 E08）；
   由宏表达式组合（`HWREG(UART0_BASE + UART_O_CTL)`、`MMIO32(RCC_BASE + 0x1C)`）且可求值时按
   **具名地址**核验（与地址别名宏同口径，不报 E08）；`HWREGBIT*(&变量, n)` 这类 RAM 位带访问静默忽略
   → 直接地址（C 风格 `*(volatile uint32_t *)0xADDR`、C++ `*reinterpret_cast<...>(0xADDR)`）
   → 文件内地址别名宏（`#define REG (*(...)0xADDR)` 后的 `REG op 值`）
   → **函数宏调用作左值**（libopencm3 `GPIO_ODR(GPIOA) |= x`、GD32 `GPIO_OCTL(GPIOA) = x`）
   → `外设->寄存器 op 表达式`
   → **裸寄存器名**（AVR/MSP430/8051/PIC 风格 `PORTB = 0xFF;`、`P1OUT |= BIT0;`）：
     名字与设备 SVD 中**唯一**寄存器名精确匹配时按寄存器核验；与头文件里的地址宏重名时先按地址核验
     （见下条）；其余按普通变量赋值静默忽略、不进入统计。
   - **CMSIS union/数组成员链**：`PORT->Group[0].DIRSET.reg = v`（Microchip SAMD）、
     `SERCOM0->USART.CTRLA.reg = v`、`EIC->CONFIG[0].reg |= v`、`ADC->CTRLB.bit.RESSEL = ...`：
     `.reg/.bit` 后缀截断、`Group[N]`/`[N]` 下标（支持一层嵌套表达式）、复合寄存器名（`COUNT16.CTRLA`）
     与组/引脚后缀寄存器（`DIRSET0`、`PINCFG0_4`、`CONFIG0`）自动对上；组/引脚号为运行时表达式时
     记"未判定"（如 `PORT->Group[g_APinDescription[pin].ulPort]`）。
   - **FSP 位域视图后缀**：`R_ICU->IELSR_b[irq].IR = v`（`REG_b.FIELD` → 寄存器 `REG`）；
     层级写法（`R_PFS->PORT[x].PIN[y].PmnPFS`）无法静态映射到 SVD 寄存器名 → 记"未判定"。
   - **端口字母命名 / REG.FIELD 直写**（Silicon Labs）：`GPIO->P[3].DOUT = v`（数字端口下标
     自动补字母候选 → `PD_DOUT`；运行时端口号记"未判定"）；`GPIO->CMUROUTE.CLKOUT0ROUTE = v`
     精确匹配失败时把最后一段当字段拆出（寄存器 + 字段存在 → 正常核验；字段不存在 → 记"未判定"）。
   - **位域直写核验**：`REG.FIELD = v` / `.bit.FIELD = v` / `REG_b.FIELD = v` 解析出位域后，
     值按**位域**宽度核验（E04，字段相对，只查 `=`）、不匹配枚举报 E05（带 `isDefault` 默认项的
     位域不报）、只读位域直写报 E10；位域名在 SVD 中不存在 → 记"未判定"（可能是命名差异或拼写错误）。
   - **AVR 数据空间口径**：SVD 用"0x800000 + 数据地址"时，低地址自动做一次偏移探测
     （`*(volatile uint8_t *)0x25 = 1` → `PORTB.PORTB`，报告注明 SVD 地址）。
   - **指针表达式写入**：`*(volatile uint32_t *)(外设_BASE + 偏移) = v`——具名表达式按寄存器核验
     （不报 E08）、纯字面量表达式报 E08、运行时基址记"未判定"。
6. 目录模式收集的扩展名：`.c/.h/.cpp/.cc/.cxx/.hpp/.hh/.ino`（C/C++ 工程与 Arduino 都能核验）。
7. ESP-IDF 风格寄存器宏（`REG_WRITE/REG_SET_BIT/REG_CLR_BIT/REG_SET_FIELD/REG_CLR_FIELD/...`）：
   寄存器号来自头文件常量。用 `--headers <文件或目录>`（可多次）提供搜索根后，地址可解析 →
   按**具名寄存器**正常核验（与地址别名宏同口径，不报 E08）；未提供头文件时记"未判定"。
   - **`#include` 自动跟随**：被核验文件的 `#include "..."` 会按"相对源文件目录 → 相对搜索根 →
     文件名匹配（同名多个时按 `--headers` 给定顺序优先）"解析，**闭包优先加载**（含嵌套包含链），
     其余头文件按路径顺序补足上限——因此给项目/SDK 的 include 根即可，无需精确到 `soc` 子目录，
     也不会被大目录截断误伤；
   - **头文件里的寄存器宏按地址核验**：对象宏值为地址访问宏（`MMIO32(...)`）、指针解引用
     （`(*((volatile uint32_t *)0x400FE108))`，TI TivaWare 直寄存器风格）或函数宏调用
     （`ADC_CR1(ADC1)`）时，`宏名 op 值` 会解析出地址后核验；
   - `REG_SET_FIELD/REG_CLR_FIELD` 进一步做**字段级核验**：字段宏存在性（E03）、只读（E10）、
     值位宽与枚举（E04/E05）；
   - 地址解析支持算术表达式链、前缀解引用（`*`）、`BIT(n)`/`BIT_MASK(n)`/`_BV(n)` 位函数、
     访问宏恒等（`MMIO32(x)`→x）、以及**函数宏调用点代入**（单/多参数，
     `TIMG_RTCCALICFG_REG(0)`、`GPIO_ODR(port)`）。
   - E12：`|=`/`&=`/`^=`/`SET_BIT`/`CLEAR_BIT`/`REG_SET_FIELD` 作用于 SVD 中 `access="write-only"`
     的寄存器时，提示读改写可能不可靠（需查手册）。

## 外设名解析（别名约定）

- 精确匹配 SVD 外设名（大小写不敏感）；`GPIOA` → `GPIO` 这类家族派生只用于字段宏，不用于外设。
- **通道命名同义写法**：`P_ChannelN` ↔ `P_CHN`（各厂商 SVD 与头文件混用，如 F1 的 `DMA1_Channel1`、
  G4 SVD 描述里的 `DMA1_CH1`）；若 SVD 把通道号放在**寄存器后缀**（G4：`DMA1` 的 `CCR3`/`CNDTR3`），
  则 `DMA1_Channel3->CCR` / `DMA1_CH3->CCR` 均映射到 `DMA1.CCR3` 做正常核验。
- **Nordic 约定**：`NRF_<外设>` 视为 `<外设>` 的别名（`NRF_USBD` → `USBD`、`NRF_RADIO` → `RADIO`），
  与 `nrf.h` 的实例指针定义一致。
- **Renesas RA/FSP 约定**：`R_<外设>` 视为 `<外设>` 的别名（`R_PORT0` → `PORT0`）。
- **Silicon Labs Series 2（cmsis-svd-data）**：外设带 `_S`/`_NS` 安全别名后缀（`GPIO` → `GPIO_S`、
  `CMU` → `CMU_S`），代码里的无后缀名自动映射。
- **外设指针宏（按地址解析）**：`#define R_GPT0 ((R_GPT0_Type *) R_GPT0_BASE)` 这类厂商实例宏，
  在 `--headers` 提供设备头后按基址匹配 SVD 外设（`R_GPT0` → `GPT320`、`R_TSN_CTRL` → `TSN`）；
  **小写指针宏同样适用**（pico-sdk 的 `#define dma_hw ((dma_hw_t *)DMA_BASE)` → `dma_hw->intr` 核到
  `DMA.INTR`；`DMA_BASE` 定义里的 `_u(x) = x ## u` 拼贴宏已支持）。
- **嵌套结构体成员名**：`clocks_hw->resus.ctrl` 这类多段成员名，SVD 里是扁平名时按"下划线拼接名
  后缀唯一匹配"对应（→ `CLK_SYS_RESUS_CTRL`）；匹配不到唯一寄存器时记"多段成员名"未判定（不报 E02）。
- **`MODIFY_REG(reg, Msk, value)` 的置位值**：字段相对（≤ 掩码）与 ST 风格带位置（`VALUE << Pos`，
  位域之外为 0）两种约定都接受；位域之外置位才报 E04。
- **条件编译块口径**：目标（外设/寄存器/位域）不存在、或访问属性类问题（E10/E12/E13）出现在
  `#if/#ifdef` 块内 → 记"未判定"（厂商库跨型号/跨配置分支）；条件块**外**照常报 E01/E02/E03/E10/E12/E13。
- 其余无法匹配的名字按既有口径处理：内核外设/簇命名进"未判定"，其它像外设名的进"报"（E01，附拼写建议）。

## 字段宏映射（E03 的核心）

CMSIS 命名约定（`外设家族_寄存器_位域`），按下面顺序尝试：

1. 去掉 `_Msk/_Mask/_MSK/_MASK/_Pos/_POS/_Shift/_SHIFT` 后缀。
2. 前缀匹配家族名：外设名本身、去掉末尾数字、去掉一个末尾字母（`GPIOA`→`GPIO`）、
   `_` 前第一段（`DMA1_Channel1`→`DMA1`→`DMA`）。
3. 余下部分尝试所有切分，找"寄存器 + 位域"：
   - 寄存器精确匹配；否则前缀匹配（宏 `CCMR1` ↔ SVD `CCMR1_Output`）；
   - 寄存器名后带实例号后缀时按数字匹配（宏 `CCR` ↔ SVD `CCR1..CCR8`；多个候选时优先命中
     当前写入的寄存器，避免通道歧义）；
   - 位域名后若还剩一段，且恰好是该位域的枚举名 → 视为枚举值宏（`USART_CR1_PS_ODD`）。
4. 映射成功但属于**另一个寄存器** → E03（宏与寄存器不符）。
5. 寄存器能找到、位域找不到 → E03（给出同寄存器位域的拼写建议）。
6. 寄存器也找不到 → 未判定（列出无法映射的宏名）。
7. `REG_SET_FIELD` 系列（地址已解析、寄存器已知）另有**字段名容忍匹配**：
   前缀逐段精确匹配之外，允许"后缀词集合 ⊆ 位域名词集合"（SVD 多出/插入词的常见差异，
   如 `SENS_FORCE_XPD_SAR` ↔ SVD `SAR_FORCE_XPD_SAR`）；该级必须唯一命中，且至少 2 个词。

## 值求值（E04/E05 用）

- 支持：十进制 / `0x` / `0b` 字面量与 `U/L` 后缀；`~ - + * / % << >> & | ^` 与括号；
  `BIT(n)`/`BIT_MASK(n)`/`_BV(n)` 位函数；单参数函数宏（`#define X(i) ...`，调用点代入实参）；
  **单参数"拼贴"宏**（宏体形如 `x ## u`，如 pico-sdk 的 `_u(0x50000000)` → `0x50000000u`）；
  `#define`（文件内、`--headers` 头文件、`--define` 命令行）里的名字，递归解析（深度 ≤ 8、环检测）；
  **文件内与 `--headers` 头文件里的 C/C++ `enum` 常量**（`enum { A = 0x2, B, C = A << 2 }`，
  隐式自增按 C 语义；`#define` 优先于同名 enum 常量）。
- 不支持：`sizeof`、多参数函数宏、结构体成员、`?:`、字符字面量 → 返回"无法求值"，相应检查进未判定。
- 负数（如 `-1`）不做位宽检查（按"全 1"处理）。

## E07 时钟检查的边界

- 使能判定来源：对 RCC 中 `<外设>EN` 位域的置位（宏或可求值数值）、`__HAL_RCC_<外设>_CLK_ENABLE()`，
  或 libopencm3 的 `rcc_periph_clock_enable(RCC_<外设>)` / `rcc_enable_rtc_clock()`。
- RCC 中找不到 `<外设>EN` 字段时跳过（不报）。
- 只做**文件内**判定；库文件（时钟由调用方管理）会有已知误报，跨文件使能请用 `--no-clock-check`。

## 不支持的形态（进"未判定"或静默忽略，不报错）

| 形态 | 例子 | 处理 |
|---|---|---|
| HAL/LL 调用 | `HAL_UART_Init(&huart1);` | 不在范围内（无寄存器写入） |
| 局部变量/指针成员 | `p->tx_len = 0;`、`base->C1 = x;` | 静默忽略，**不计入统计** |
| 簇寄存器的分离命名 | `DMA1_Channel1->CCR`（SVD 中是 `DMA1` 的 `CH1.CCR`） | 进"未判定"（附说明） |
| 内核外设 | `SysTick->CTRL`、`SCB->AIRCR` | 进"未判定" |
| 无法映射的宏 | `FOO_BAR`、厂商私有宏 | 进"未判定"（列名字） |
| 运行时地址 | `*(volatile uint32_t *)base`、`ADC_CR2(adc)` | 进"未判定"（地址无法求值） |

## 补丁模式（--patch）

- 输入 unified diff / `git diff` 输出；只核验**新增行**。
- 行号按新文件编号：把新增行放回正确的行号位置，其余行留空。
- 语句跨新增/上下文行时，只有新增部分参与分析（可能进未判定）。

## 安全与性能

- 只做词法分析：不执行用户代码、不 `eval`、不网络访问（规格 0.7）。
- 目录扫描上限 200 个文件；单文件按语句处理，1000 行文件远低于 2 s 验收线。
- 不修改被检查文件；`--out` 是唯一的写出口。
