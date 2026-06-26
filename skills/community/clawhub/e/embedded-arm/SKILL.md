# 嵌入式 ARM 全栈开发 (Embedded ARM)

ARM Cortex-M / RISC-V 嵌入式系统专业级开发指南，聚焦 Rust embedded + FreeRTOS 双栈。

---

## 1. MCU 架构

### 概述

ARM Cortex-M 系列是嵌入式主流架构，覆盖从低功耗传感器到高性能工业控制。RISC-V 正在部分领域替代。

### ARM Cortex-M 架构对比

| 特性 | M0/M0+ | M3 | M4 | M7 | M23 | M33 | M55 |
|------|--------|----|----|-----|------|------|------|
| **流水线** | 3级 | 3级 | 3级 | 6级(双发射) | 3级 | 3级 | 8级 |
| **FPU** | ✗ | ✗ | 单精度可选 | 双+单精度 | ✗ | 单精度可选 | 单+双精度 |
| **DSP** | ✗ | 部分SIMD | 可选 | ✗ | ✗ | 可选 | Helium MVE |
| **MPU** | 8区 | 8区 | 8区 | 16区 | ✗ | 可选 | 可选 |
| **TrustZone** | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| **中断数** | 16-32 | 240 | 240 | 240 | 16-32 | 240 | 480 |
| **典型主频** | 48MHz | 72MHz | 180MHz | 480MHz+ | 48MHz | 100MHz | 400MHz |
| **DMIPS/MHz** | 0.84 | 1.25 | 1.25 | 2.14 | 0.83 | 1.5 | 3.3 |
| **能效(DMIPS/mW)** | ★★★★★ | ★★★ | ★★★ | ★★ | ★★★★★ | ★★★ | ★★ |
| **典型芯片** | STM32F0/G0, nRF51 | STM32F1 | STM32F4/L4, nRF52 | STM32H7, i.MX RT | STM32L0/G0 | STM32L5/U5, nRF53 | CORTEX-M55 |

### RISC-V (RV32IMAC) 对比

| 特性 | ARM Cortex-M | RISC-V RV32IMAC |
|------|-------------|-----------------|
| **指令集** | 固定16/32位 | 可扩展模块化 |
| **特权级** | Handler/Thread | M/S/U 三级 |
| **中断架构** | NVIC(向量+尾链) | CLIC/PLIC(平台定义) |
| **调试** | CoreSight(标准) | Debug Spec 1.0(JTAG) |
| **生态成熟度** | ★★★★★ | ★★★ |
| **授权成本** | 芯片厂商付费 | 开源免费 |
| **典型芯片** | STM32全系列 | CH32V, GD32VF103, ESP32-C3 |

### 中断架构 (NVIC)

```
中断优先级分组（ARMv7-M+）:
  AIRCR[10:8] = PRIGROUP
  0b000 = 16个抢占优先级, 0个子优先级
  0b101 = 8个抢占优先级, 2个子优先级  (常用)
  0b111 = 4个抢占优先级, 4个子优先级

中断进入延迟:
  M3/M4: 12周期 (尾链优化至 6周期)
  M7:   12-16周期
  M0/M0+: 16周期

关键寄存器:
  NVIC_ISER  - 中断使能
  NVIC_ICER  - 中断清除使能
  NVIC_ISPR  - 中断挂起
  NVIC_IPR   - 优先级 (4bit/中断)
  SCB->AIRCR - 优先级分组
  SCB->SHCSR - 系统异常控制
```

### MPU 配置

```c
// STM32F4 MPU 配置示例: 保护 SRAM 区域
void MPU_Config(void) {
    MPU_Region_InitTypeDef MPU_InitStruct = {0};
    HAL_MPU_Disable();

    // 区域0: 保护堆栈 (不可执行, 只读数据区)
    MPU_InitStruct.Enable           = MPU_REGION_ENABLE;
    MPU_InitStruct.Number           = MPU_REGION_NUMBER0;
    MPU_InitStruct.BaseAddress      = 0x20000000;
    MPU_InitStruct.Size             = MPU_REGION_SIZE_256KB;
    MPU_InitStruct.SubRegionDisable = 0x00;
    MPU_InitStruct.TypeExtField     = MPU_TEX_LEVEL0;
    MPU_InitStruct.AccessPermission = MPU_REGION_FULL_ACCESS;
    MPU_InitStruct.DisableExec      = MPU_INSTRUCTION_ACCESS_DISABLE;  // XN=1
    MPU_InitStruct.IsShareable      = MPU_ACCESS_SHAREABLE;
    MPU_InitStruct.IsCacheable      = MPU_ACCESS_CACHEABLE;
    MPU_InitStruct.IsBufferable     = MPU_ACCESS_BUFFERABLE;
    HAL_MPU_ConfigRegion(&MPU_InitStruct);

    HAL_MPU_Enable(MPU_PRIVILEGED_DEFAULT);
}
```

### 存储器映射 (Cortex-M 典型)

```
0xFFFFFFFF ──────────── System
0xE0100000 ──────────── Private Peripherals (NVIC, SysTick, SCB, MPU)
0xA0000000 ──────────── External Device
0x60000000 ──────────── External RAM
0x40000000 ──────────── Peripheral (APB/AHB 外设寄存器)
0x20000000 ──────────── SRAM
0x00000000 ──────────── Code (Flash/ROM, 别名到 0x08000000)
```

### 最佳实践

- **M0/M0+ 选型**: 电池供电传感器、简单控制（成本敏感）
- **M4 选型**: 需要 DSP/FPU 的音频、电机控制、传感器融合
- **M7 选型**: 图形UI、复杂算法、实时Linux副核
- **M33 选型**: 安全敏感（TrustZone隔离固件+ bootloader）
- **MPU 必开**: 生产环境防止缓冲区溢出、保护关键数据
- **中断优先级**: DMA > 外设 > 通信 > 应用逻辑

---

## 2. Rust Embedded 生态

### 概述

Rust 在嵌入式领域提供零成本抽象 + 内存安全 + 强类型，通过 `embedded-hal` trait 实现硬件无关的驱动开发。

### 核心工具链

```toml
# .cargo/config.toml
[target.thumbv6m-none-eabi]
runner = "probe-rs run --chip STM32G030K6Tx"
rustflags = [
    "-C", "link-arg=-Tlink.x",        # cortex-m-rt 提供的默认链接脚本
    "-C", "link-arg=-Tdefmt.x",        # defmt 需要的符号表
]

[target.thumbv7em-none-eabihf]
runner = "probe-rs run --chip STM32F401CCUx"
rustflags = [
    "-C", "link-arg=-Tlink.x",
    "-C", "link-arg=-Tdefmt.x",
]

[build]
target = "thumbv6m-none-eabi"
```

```toml
# Cargo.toml
[dependencies]
cortex-m = { version = "0.7", features = ["critical-section-single-core"] }
cortex-m-rt = "0.7"
cortex-m-semihosting = "0.5"
embedded-hal = "1.0"
defmt = "0.3"
defmt-rtt = "0.4"
panic-probe = { version = "0.3", features = ["print-defmt"] }
# flip-link = "0.1"  # 作为 cargo-binutils 子命令或独立使用

[profile.release]
opt-level = "z"     # 优化代码大小
lto = true          # 链接时优化
strip = true        # 去除符号
codegen-units = 1   # 更好的优化
```

### memory.x 链接脚本

```
MEMORY
{
    FLASH : ORIGIN = 0x08000000, LENGTH = 64K
    RAM   : ORIGIN = 0x20000000, LENGTH = 8K
}

/* cortex-m-rt 预定义区域 */
_stack_start = ORIGIN(RAM) + LENGTH(RAM);
```

### embedded-hal trait 体系 (v1.0)

```rust
use embedded_hal::{
    digital::{OutputPin, InputPin, StatefulOutputPin},
    spi::{SpiBus, SpiDevice},
    i2c::I2c,
    serial::{Write, Read},
    adc::Adc,
    pwm::SetDutyCycle,
    delay::DelayNs,
    rng::Read,
};
```

| trait | 用途 | 关键方法 |
|-------|------|---------|
| `OutputPin` | GPIO输出 | `set_low()`, `set_high()` |
| `InputPin` | GPIO输入 | `is_high()`, `is_low()` |
| `SpiBus` | SPI总线 | `read()`, `write()`, `transfer()` |
| `SpiDevice` | SPI从机(带CS) | `transaction()` |
| `I2c` | I2C通信 | `read()`, `write()`, `transaction()` |
| `Write`/`Read` | 串口 | `write()`, `read()` |
| `Adc` | ADC采样 | `read()` |
| `SetDutyCycle` | PWM | `set_duty_cycle()` |
| `DelayNs` | 延时 | `delay_ns()` |
| `Read` (rng) | 随机数 | `read()` |

### embedded-hal-async

```rust
use embedded_hal_async::{
    spi::SpiBus as SpiBusAsync,
    i2c::I2c as I2cAsync,
    delay::DelayNs as DelayNsAsync,
};

// 异步 SPI 读取
async fn read_sensor<SPI: SpiBusAsync>(spi: &mut SPI, cs: &mut impl OutputPin) -> Result<[u8; 6], SPI::Error> {
    let mut buf = [0u8; 6];
    cs.set_low().ok();
    spi.read(&mut buf).await?;
    cs.set_high().ok();
    Ok(buf)
}
```

### defmt 日志

```rust
use defmt::{info, warn, error, debug, trace};

#[entry]
fn main() -> ! {
    info!("系统启动, 时钟: {} MHz", 48);
    
    loop {
        let sensor_val = read_temperature();
        debug!("温度: {}°C", sensor_val);
        
        if sensor_val > 85.0 {
            warn!("温度过高! 当前: {}°C", sensor_val);
        }
    }
}
```

### panic 处理

```toml
# 开发阶段: 通过 probe-rs RTT 输出 panic 信息
panic-probe = { version = "0.3", features = ["print-defmt"] }

# 生产阶段: 持久化 panic 到 Flash，复位后可读
# panic-persist = "1"
```

### Embassy 异步框架

```rust
#![no_std]
#![no_main]

use embassy_executor::main;
use embassy_time::{Timer, Duration};
use embassy_stm32::{gpio::Output, Config};
use {defmt_rtt as _, panic_probe as _};

#[main]
async fn main(spawner: embassy_executor::Spawner) {
    let p = embassy_stm32::init(Config::default());
    let mut led = Output::new(p.PA5, embassy_stm32::gpio::Level::High);

    loop {
        led.set_low();  // LED on
        Timer::after(Duration::from_millis(500)).await;
        led.set_high(); // LED off
        Timer::after(Duration::from_millis(500)).await;
    }
}
```

### RTIC 零开销 RTOS

```rust
#![no_std]
#![no_main]

use rtic::app;
use rtic_monotonics::systick::Systick;

#[app(device = stm32f4::stm32f401, dispatchers = [SPI2])]
mod app {
    use super::*;

    #[shared]
    struct Shared {
        led: bool,
    }

    #[local]
    struct Local {}

    #[init]
    fn init(cx: init::Context) -> (Shared, Local, init::Monotonics) {
        Systick::start(cx.device.SYST, 16_000_000);
        defmt::info!("RTIC init");
        (Shared { led: false }, Local {}, Systick::monotonic())
    }

    // 硬件任务：优先级1
    #[task(priority = 1, shared = [led])]
    async fn blink(mut cx: blink::Context) {
        loop {
            cx.shared.lock(|led| *led = !*led);
            Systick::delay(500.millis()).await;
        }
    }
}
```

### probe-rs 工具

```bash
# 烧录
probe-rs run --chip STM32F401CCUx --target thumbv7em-none-eabihf

# 调试 (GDB)
probe-rs gdb --chip STM32F401CCUx

# RTT 日志
probe-rs attach --chip STM32F401CCUx --log-format Defmt

# 擦除 & 烧录 bin
probe-rs download --chip STM32F401CCUx target/thumbv7em-none-eabihf/release/app.bin

# 二进制大小分析
probe-rs info --chip STM32F401CCUx
cargo size --release -- -A
```

### 最佳实践

- **优先用 Embassy**: 异步编程模型，代码更清晰，资源利用更高
- **RTIC 适用场景**: 硬实时约束、需要严格优先级调度的系统
- **defmt > println**: defmt 零开销，生产环境可完全关闭
- **flip-link**: 堆栈溢出时覆盖链接脚本防止 RAM 破坏
- **`.cargo/config.toml` 放仓库根目录**: 团队共享编译配置
- **内存布局检查**: `cargo size --release` 关注 text/data/bss

---

## 3. RTOS

### 概述

RTOS 提供确定性任务调度和 IPC 机制。选择依据：实时性要求、代码复杂度、生态支持。

### FreeRTOS

```c
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"

// === 任务管理 ===
void vSensorTask(void *pvParam) {
    TickType_t xLastWake = xTaskGetTickCount();
    while (1) {
        float temp = read_sensor();
        xQueueSend(sensorQueue, &temp, pdMS_TO_TICKS(100));
        vTaskDelayUntil(&xLastWake, pdMS_TO_TICKS(100));  // 周期100ms
    }
}

// 创建任务 (静态分配, 推荐)
static StackType_t sensorStack[256];
static StaticTask_t sensorTCB;
void create_tasks(void) {
    xTaskCreateStatic(vSensorTask, "Sensor", 256, NULL, 2, sensorStack, &sensorTCB);
    // 优先级: Idle(0) < App(1-3) < ISR通知(4+)
}

// === 队列 ===
QueueHandle_t sensorQueue;  // xQueueCreateStatic(10, sizeof(float), buf, &qstruct)

// === 二值信号量 (ISR同步) ===
SemaphoreHandle_t xDataReadySem;
// ISR中: BaseType_t xHigherPriorityTaskWoken = pdFALSE;
//        xSemaphoreGiveFromISR(xDataReadySem, &xHigherPriorityTaskWoken);
//        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
// 任务中: xSemaphoreTake(xDataReadySem, portMAX_DELAY);

// === 互斥量 (优先级继承) ===
SemaphoreHandle_t xI2cMutex;
// 保护共享I2C总线
xSemaphoreTake(xI2cMutex, pdMS_TO_TICKS(100));
i2c_write(I2C1, addr, data, len);
xSemaphoreGive(xI2cMutex);

// === 任务通知 (零RAM开销的轻量IPC) ===
// 发送: xTaskNotifyGive(xReceiverTask);
//       vTaskNotifyGiveFromISR(xReceiverTask, &xHigherPriorityTaskWoken);
// 接收: ulTaskNotifyTake(pdTRUE, portMAX_DELAY);

// === 事件组 ===
EventGroupHandle_t xInitEvent;
// 设置: xEventGroupSetBits(xInitEvent, BIT_WIFI_READY);
// 等待: xEventGroupWaitBits(xInitEvent, BIT_WIFI_READY | BIT_SENSOR_READY,
//          pdTRUE, pdTRUE, portMAX_DELAY);  // AllSet, AutoClear

// === 软件定时器 ===
// xTimerCreate("Blink", pdMS_TO_TICKS(500), pdTRUE, NULL, vBlinkCallback);
// xTimerStart(xBlinkTimer, 0);

// === Tickless Idle (低功耗) ===
// configUSE_TICKLESS_IDLE = 2  // 在 FreeRTOSConfig.h 中启用
// 需实现: vApplicationSleep()
```

### FreeRTOS Rust 绑定

```rust
use freertos_rust::*;

fn sensor_task() {
    // 优先级继承互斥量
    let mutex = Mutex::new().unwrap();
    
    loop {
        let _guard = mutex.lock(Duration::infinite());
        // 临界区: 自动释放
        read_i2c_sensor();
    }
}

fn main() {
    // 创建任务
    Task::new()
        .name("sensor")
        .stack_size(512)
        .priority(TaskPriority(2))
        .spawn(sensor_task)
        .unwrap();
    
    // 队列
    let queue: Queue<f32, 16> = Queue::new(16).unwrap();
    queue.send(25.5, Duration::infinite()).unwrap();
    
    // 二值信号量
    let sem = BinarySemaphore::new(BinarySemaphore::empty()).unwrap();
    
    // 任务通知
    let task_handle = current().task_handle();
    task_handle.notify(TaskNotification::no_bits());
    
    FreeRtos::start_scheduler();
}
```

### Zephyr RTOS

```c
// Kconfig 配置
CONFIG_BT=y
CONFIG_GPIO=y
CONFIG_I2C=y

// 设备树 (overlay.dts)
/ {
    my_sensor: bme280@76 {
        compatible = "bosch,bme280";
        reg = <0x76>;
        int-gpios = <&gpioa 0 GPIO_ACTIVE_LOW>;
    };
};

// 线程
void sensor_thread(void *p1, void *p2, void *p3) {
    const struct device *i2c = DEVICE_DT_GET(DT_NODELABEL(i2c1));
    while (1) {
        uint8_t data[8];
        i2c_write_read(i2c, 0x76, &reg, 1, data, 8);
        k_sleep(K_MSEC(1000));
    }
}
K_THREAD_DEFINE(sensor_tid, 1024, sensor_thread, NULL, NULL, NULL, 7, 0, 0);

// 工作队列 (延迟工作)
static struct k_work_delayable sensor_work;
void sensor_work_handler(struct k_work *work) { /* ... */ }
k_work_queue_start(&my_workq, stack, 1024, 5, NULL);
k_work_init_delayable(&sensor_work, sensor_work_handler);
k_work_reschedule(&sensor_work, K_MSEC(100));
```

### 裸机调度模式

```c
// 超级循环 + 状态机 (最简单)
typedef enum { STATE_IDLE, STATE_MEASURE, STATE_TRANSMIT } State_t;

int main(void) {
    State_t state = STATE_IDLE;
    uint32_t last_tick = get_tick();
    
    while (1) {
        uint32_t now = get_tick();
        
        switch (state) {
            case STATE_IDLE:
                if (now - last_tick >= 1000) {
                    state = STATE_MEASURE;
                    last_tick = now;
                }
                break;
            case STATE_MEASURE:
                sensor_data = read_sensor();
                state = STATE_TRANSMIT;
                break;
            case STATE_TRANSMIT:
                uart_send(&sensor_data, sizeof(sensor_data));
                state = STATE_IDLE;
                break;
        }
        
        // 低功耗: 无事可做时进入 sleep
        __WFI();
    }
}
```

### 最佳实践

- **FreeRTOS 选型**: 工业控制、多任务协作、成熟生态
- **Embassy 选型**: Rust项目、异步IO密集、低RAM设备
- **Zephyr 选型**: Linux基金会支持、丰富设备驱动、多架构
- **裸机选型**: 简单产品、极低RAM(<4KB)、无多任务需求
- **优先用静态分配**: 避免堆碎片，`configSUPPORT_STATIC_ALLOCATION=1`
- **任务通知 > 队列**: 单值通知零RAM开销
- **Tickless idle**: 必开，显著降低空闲功耗

---

## 4. 外设驱动开发

### 概述

外设驱动是嵌入式核心技能。每个外设需掌握：寄存器配置、时序要求、中断/DMA模式、错误处理。

### GPIO

```rust
// 输出 + 中断输入 (Embassy STM32)
use embassy_stm32::gpio::{Input, Output, Pull, Level, Speed};

#[main]
async fn main(_spawner: Spawner) {
    let p = embassy_stm32::init(Config::default());
    let mut led = Output::new(p.PA5, Level::High, Speed::Low);
    let mut button = Input::new(p.PA0, Pull::Up);
    
    // 去抖动处理
    let mut last_state = button.is_high();
    loop {
        let current = button.is_high();
        if current != last_state {
            Timer::after(Duration::from_millis(20)).await;  // 去抖
            if button.is_high() != current { continue; }      // 确认
            last_state = current;
            if current { led.set_high(); } else { led.set_low(); }
        }
        Timer::after(Duration::from_millis(5)).await;
    }
}
```

### UART (中断 + DMA)

```c
// STM32 HAL UART DMA 接收
#define RX_BUF_SIZE 256
uint8_t rx_buf[RX_BUF_SIZE];
volatile uint16_t rx_len = 0;

// 空闲中断 + DMA: 接收不定长数据
void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t size) {
    if (huart->Instance == USART1) {
        rx_len = size;
        // 处理接收到的数据...
        process_data(rx_buf, rx_len);
        // 重新启动接收
        HAL_UARTEx_ReceiveToIdle_DMA(huart, rx_buf, RX_BUF_SIZE);
        __HAL_DMA_DISABLE_IT(huart->hdmarx, DMA_IT_HT);  // 禁用半传输中断
    }
}

void uart_init(void) {
    HAL_UARTEx_ReceiveToIdle_DMA(&huart1, rx_buf, RX_BUF_SIZE);
    __HAL_DMA_DISABLE_IT(huart1.hdmarx, DMA_IT_HT);
}
```

### SPI (DMA 双缓冲)

```c
// SPI DMA 发送 + 双缓冲
uint8_t tx_buf1[256], tx_buf2[256];
volatile uint8_t active_buf = 0;

void HAL_SPI_TxCpltCallback(SPI_HandleTypeDef *hspi) {
    active_buf ^= 1;  // 切换缓冲区
    // 填充下一个缓冲区...
    HAL_SPI_Transmit_DMA(&hspi1, (active_buf ? tx_buf2 : tx_buf1), 256);
}
```

### I2C (多从机 + 错误处理)

```c
// I2C 扫描总线
void i2c_scan(I2C_HandleTypeDef *hi2c) {
    printf("I2C Bus Scan:\n");
    for (uint8_t addr = 0x08; addr < 0x78; addr++) {
        if (HAL_I2C_IsDeviceReady(hi2c, addr << 1, 1, 10) == HAL_OK) {
            printf("  0x%02X found\n", addr);
        }
    }
}

// 带重试的 I2C 写入
HAL_StatusTypeDef i2c_write_safe(I2C_HandleTypeDef *hi2c, uint8_t dev_addr,
                                  uint8_t reg, uint8_t *data, uint16_t len) {
    HAL_StatusTypeDef ret;
    uint8_t retry = 3;
    do {
        ret = HAL_I2C_Master_Transmit(hi2c, dev_addr << 1, &reg, 1, 100);
        if (ret == HAL_OK) ret = HAL_I2C_Master_Transmit(hi2c, dev_addr << 1, data, len, 100);
        if (ret == HAL_OK) break;
        HAL_I2C_DeInit(hi2c);
        HAL_I2C_Init(hi2c);  // 总线恢复
    } while (retry-- > 0);
    return ret;
}
```

### ADC (DMA 连续扫描)

```c
// 多通道 ADC DMA 扫描
#define ADC_CH_COUNT 4
uint16_t adc_raw[ADC_CH_COUNT];
uint32_t adc_dma_buf[ADC_CH_COUNT];  // DMA 需要对齐

void adc_start(void) {
    ADC_ChannelConfTypeDef sConfig = {0};
    // 配置多个通道...
    hadc1.Init.DMAContinuousRequests = ENABLE;
    hadc1.Init.ContinuousConvMode     = ENABLE;
    hadc1.Init.ScanConvMode          = ENABLE;
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_raw, ADC_CH_COUNT);
}

// 校准
void adc_calibrate(void) {
    HAL_ADCEx_Calibration_Start(&hadc1, ADC_SINGLE_ENDED);
}
```

### DMA 双缓冲

```c
// DMA 双缓冲接收 (循环缓冲区)
#define DMA_BUF_SIZE 512
uint8_t dma_buf[DMA_BUF_SIZE * 2];  // 两个半缓冲区

// 在 DMA 半传输中断中处理前半部分
void HAL_UART_RxHalfCpltCallback(UART_HandleTypeDef *huart) {
    process_uart_data(dma_buf, DMA_BUF_SIZE / 2);
}

// 在 DMA 完成中断中处理后半部分
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    process_uart_data(dma_buf + DMA_BUF_SIZE / 2, DMA_BUF_SIZE / 2);
}
```

### Flash (页擦写)

```c
// STM32 内部 Flash 页擦写 (掉电安全)
HAL_StatusTypeDef flash_write(uint32_t addr, uint8_t *data, uint16_t len) {
    HAL_StatusTypeDef status;
    uint32_t page_addr = addr & ~(FLASH_PAGE_SIZE - 1);
    
    HAL_FLASH_Unlock();
    FLASH_EraseInitTypeDef erase;
    erase.TypeErase    = FLASH_TYPEERASE_PAGES;
    erase.PageAddress  = page_addr;
    erase.NbPages      = 1;
    uint32_t error;
    
    status = HAL_FLASHEx_Erase(&erase, &error);
    if (status != HAL_OK) { HAL_FLASH_Lock(); return status; }
    
    for (uint16_t i = 0; i < len; i += 2) {
        uint16_t half_word = *(uint16_t*)(data + i);
        status = HAL_FLASH_Program(FLASH_TYPEPROGRAM_HALFWORD, addr + i, half_word);
        if (status != HAL_OK) break;
    }
    HAL_FLASH_Lock();
    return status;
}

// 磨损均衡: 简单轮换方案
// 将存储区域分为 N 个 slot，每次写入下一个 slot，用计数器或标记位确定活跃 slot
```

### 最佳实践

- **GPIO 去抖**: 硬件 RC 滤波 + 软件 20ms 延迟双重保护
- **UART**: 优先用 DMA + 空闲中断处理不定长数据
- **I2C 总线恢复**: 检测 SCL/SDA 卡死后，发 9 个时钟脉冲恢复
- **SPI 时钟上限**: 查从机数据手册，通常 <10MHz，注意 CPOL/CPHA 匹配
- **ADC 采样**: 硬件上在 ADC 输入加 RC 低通滤波，软件上做滑动平均
- **DMA 对齐**: DMA 缓冲区必须对齐到 4 字节边界
- **Flash 寿命**: 典型 10K~100K 擦写次数，必须做磨损均衡

---

## 5. 低功耗设计

### 概述

低功耗是电池供电产品的核心指标。需从硬件选型、时钟配置、外设管理、软件策略全链路优化。

### 睡眠模式对比 (STM32)

| 模式 | CPU | Flash | SRAM | 时钟 | 唤醒时间 | 典型电流 |
|------|-----|-------|------|------|---------|---------|
| **Run** | ON | ON | ON | 全开 | - | 5-50mA |
| **Sleep** | OFF | ON | ON | AHB开 | <1μs | 1-5mA |
| **LowPower Run** | ON | ON | ON | 降频 | - | 0.5-2mA |
| **LowPower Sleep** | OFF | ON | ON | 降频 | <1μs | 0.5-1mA |
| **Stop 0** | OFF | ON | 保持 | OFF | 5μs | 5-50μA |
| **Stop 1** | OFF | OFF | 保持 | OFF | 5μs | 2-20μA |
| **Standby** | OFF | OFF | OFF | OFF | 50μs | 0.5-3μA |
| **Shutdown** | OFF | OFF | OFF | OFF | 500μs | 0.01-0.3μA |

### 时钟树配置策略

```c
// 低功耗时钟配置
void system_clock_lp_init(void) {
    // 1. 使用 HSI (内部RC) 代替 HSE (外部晶振) → Standby时省电
    // 2. 关闭 PLL → 降频运行
    // 3. 预分频最大化 → 降低总线频率
    
    RCC_OscInitTypeDef osc = {0};
    osc.OscillatorType  = RCC_OSCILLATORTYPE_LSE | RCC_OSCILLATORTYPE_LSI;
    osc.LSEState        = RCC_LSE_ON;     // RTC 用外部 32.768kHz
    osc.LSIState        = RCC_LSI_ON;     // IWDG 用内部低速
    
    // 外设时钟门控
    __HAL_RCC_GPIOA_CLK_ENABLE();  // 只开需要的
    __HAL_RCC_USART1_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_DISABLE(); // 关闭不用的
    __HAL_RCC_SPI1_CLK_DISABLE();
    
    // 动态门控: 进入 Stop 前关闭
    void enter_stop(void) {
        HAL_SuspendTick();
        __HAL_RCC_PWR_CLK_ENABLE();
        HAL_PWREx_EnableUltraLowPower();   // ULP 模式
        HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);  // Stop2: SRAM保持, 更低功耗
        SystemClock_Config();  // 唤醒后恢复时钟
        HAL_ResumeTick();
    }
}
```

### 唤醒源配置

```c
// RTC 闹钟唤醒
void rtc_wakeup_configure(uint32_t seconds) {
    RTC_TimeTypeDef time = { .Hours = 0, .Minutes = 0, .Seconds = seconds, .SubSeconds = 0 };
    HAL_RTC_SetTime(&hrtc, &time, RTC_FORMAT_BIN);
    HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, seconds, RTC_WAKEUPCLOCK_CK_SPRE_16BITS);
}

// GPIO 外部中断唤醒
void exti_wakeup_configure(void) {
    // Stop 模式下 EXTI 仍可用
    // Standby 模式需要 Wakeup Pin (不是普通 EXTI)
    HAL_PWREx_EnableWakeUpPin(PWR_WAKEUP_PIN1_HIGH);  // PA0
}

// LPUART 唤醒 (DeepSleep/Stop 下接收数据唤醒)
void lpuart_wakeup_configure(void) {
    // LPUART 可在 Stop 模式下通过 32.768kHz 时钟接收
    // 波特率受限于 LSE: 最大 9600 @ LSE=32.768kHz
    LL_LPUART_EnableInStopMode(LPUART1);
}
```

### 电池寿命计算

```
电池容量: C (mAh)
日均电流: I_avg (mA)
电池寿命: T = C / I_avg (天)

I_avg = (I_run × T_run + I_sleep × T_sleep) / (T_run + T_sleep)

示例:
  电池: CR2032 = 220mAh
  运行: 10mA × 100ms/次 × 60次/时 = 10mA × 1.67% ≈ 167μA
  睡眠: 2μA × 98.33%
  I_avg ≈ 167 + 2 = 169μA
  寿命 ≈ 220 / 0.169 ≈ 1302 天 ≈ 3.6 年

  考虑自放电 (~1%/年):
  实际寿命 ≈ 1200 天
```

### Brown-out 检测

```c
// BOR (Brown-Out Reset) 配置
// 在选项字节中设置, 不是运行时配置
// BOR Level 2: 2.1V → 电池电压低于 2.1V 时自动复位
// BOR Level 3: 2.4V
// BOR Level 4: 2.7V

// 运行时检测电压
void check_battery(void) {
    // 启用内部电压参考
    ADC1->CR |= ADC_CR_ADVREGEN;
    ADC1_COMMON->CCR |= ADC_CCR_VREFEN;
    
    // 采样内部 VREFINT
    uint16_t vref = read_vrefint();  // 约 1.2V
    float vdd = 1.2 * 4095.0 / vref;
    
    if (vdd < 2.5) {
        // 低电量警告: 关闭非必要外设, 延长采样间隔
        enter_low_power_mode();
    }
}
```

### 最佳实践

- **选型优先**: 选原生低功耗 MCU (STM32L/U/G0 系列)
- **时钟策略**: 运行用 HSI, Standby 关 HSE, RTC 用 LSE
- **外设门控**: 用完立即关, `__HAL_RCC_xxx_CLK_DISABLE()`
- **唤醒间隔**: 传感器产品 1-60s 采样一次，中间全睡
- **LPUART**: 蓝牙/WiFi 休眠时保持串口通信的唯一选择
- **测量验证**: 用高精度万用表或功耗分析仪实测, 不要只算理论值

---

## 6. 硬件调试

### 概述

硬件调试是嵌入式开发必备技能。从简单的串口打印到专业的逻辑分析仪分析。

### 调试器对比

| 调试器 | 速度 | 特性 | 价格 | 适用 |
|--------|------|------|------|------|
| **J-Link** | ★★★★★ | RTT, SWO, Flash BP, ETM | ¥500-3000 | 专业开发 |
| **ST-Link V3** | ★★★★ | SWV, TRACESWO | ¥150 | STM32 |
| **DAP-Link** | ★★★ | CMSIS-DAP开源 | ¥30-100 | 入门/学习 |
| **CMSIS-DAP** | ★★★ | 标准协议 | 开源 | 跨平台 |

### GDB 调试

```bash
# 启动 GDB Server
JLinkGDBServer -device STM32F401CC -if SWD -speed 4000

# GDB 调试
arm-none-eabi-gdb target/thumbv7em-none-eabihf/debug/app
(gdb) target remote :2331
(gdb) load                      # 烧录
(gdb) break main                # 断点
(gdb) break sensor.c:42         # 行断点
(gdb) watch sensor_value        # 数据观察点
(gdb) continue
(gdb) step                     # 单步入函数
(gdb) next                     # 单步过函数
(gdb) print/x *0x40021000      # 查看外设寄存器
(gdb) info registers            # 查看寄存器
(gdb) set {int}0x20000000 = 0x1234  # 写内存
```

### probe-rs 调试

```bash
# RTT 实时日志
probe-rs attach --chip STM32F401CCUx --log-format Defmt

# 查看变量
probe-rs dap server
# 然后用 openocd + gdb 或 VSCode Cortex-Debug 连接

# dump 内存
probe-rs info --chip STM32F401CCUx
```

### SWO/ITM 实时日志

```c
// ITM 日志输出 (不占用 UART, 零额外硬件)
#include "core_cm4.h"

void itm_log(const char *str) {
    while (*str) {
        // 等待 TX 缓冲区就绪
        while (ITM->PORT[0].u32 == 0);
        ITM->PORT[0].u8 = *str++;
    }
}

// J-Link Settings: SWO Clock = HCLK/1 (最大 2MHz)
// 波特率 > 1MHz 时用 J-Link RTT 代替
```

### 逻辑分析仪协议解码

```
常用逻辑分析仪: Saleae Logic, Sigrok/PulseView

关键协议解码:
  - UART: 查看 start/stop bit, 波特率验证
  - I2C: START → Address → ACK/NACK → Data → STOP
  - SPI: CS → CLK → MOSI/MISO 数据对齐
  - 1-Wire: 复位脉冲, 存在检测, 时隙

常见问题定位:
  - I2C NACK → 地址错误或从机未响应
  - UART 帧错误 → 波特率不匹配
  - SPI 相位错误 → CPOL/CPHA 配置错
```

### 电流测量

```
高边采样 (推荐):
  电流表串联在 VDD 和 MCU 之间
  精度: μA 级
  设备: Keithley DMM7510, Nordic PPK2

低边采样:
  电流表串联在 MCU GND 和电源 GND 之间
  注意: 地电位偏移影响 ADC 等模拟电路

积分法 (平均电流):
  示波器串联 1Ω 采样电阻
  测量电压降 → V/R = I
  用平均功能或积分算功耗
```

### 最佳实践

- **J-Link RTT > SWO > UART**: 速度和便利性递减
- **先串口, 再调试器**: 简单问题 printf 即可定位
- **逻辑分析仪必备**: I2C/SPI 时序问题只能用它看
- **功耗分析**: Nordic PPK2 是性价比最高的 μA 级电流测量工具
- **崩溃定位**: 硬件 Fault Handler 记录寄存器, 复位后读回

---

## 7. 软件工程

### 概述

嵌入式软件工程关注：代码结构、内存约束、测试策略、启动流程。

### 代码分层架构

```
应用层 (App/)           ← 业务逻辑, 状态机, 协议
  ├── app_main.c
  ├── sensor_manager.c
  └── comm_manager.c

驱动层 (Drivers/)       ← 芯片外设抽象
  ├── bme280.c          ← 传感器驱动
  └── w25qxx.c          ← 外部 Flash

HAL层 (HAL/)            ← MCU 外设薄封装 (或用 vendor HAL)
  ├── hal_gpio.c
  ├── hal_uart.c
  └── hal_spi.c

平台层 (Platform/)      ← MCU 启动, 时钟, 中断向量
  ├── startup_stm32f401.s
  ├── system_stm32f4xx.c
  └── stm32f401xx.h
```

### 启动流程

```
复位向量 → Reset_Handler:
  1. 设置 SP (Stack Pointer) = _stack_start (RAM 顶部)
  2. 复制 .data 段从 Flash 到 SRAM
  3. 清零 .bss 段
  4. 调用 SystemInit() → 配置时钟, PLL
  5. 调用 __libc_init_array → C++ 构造函数
  6. 调用 main()
  7. main 返回后进入无限循环 (或 fault)

// Rust (cortex-m-rt) 等效:
  1. 设置 SP
  2. 复制 .data (rust_main_data)
  3. 清零 .bss (rust_main_bss)
  4. 调用 main() (#[entry] 宏标记)
```

### MISRA C:2012 关键规则

```c
// 规则 1.3: 不使用未定义行为
// 规则 11.4: 整数到指针转换用 uintptr_t
volatile uint32_t *reg = (volatile uint32_t *)(uintptr_t)0x40021000;

// 规则 14.4: 条件语句用 bool
if (is_initialized == true) { ... }

// 规则 17.7: 返回值不能被忽略 (除强转 void)
(void)HAL_I2C_Master_Transmit(...);  // 显式忽略

// 规则 21.3: malloc/free 禁止 (嵌入式推荐静态分配)
// 替代方案: 静态内存池, 预分配缓冲区
static uint8_t uart_tx_buf[256];
```

### Rust 嵌入式单元测试

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    // Mock HAL trait
    struct MockSpi;
    impl SpiBus for MockSpi {
        type Error = ();
        fn read(&mut self, words: &mut [u8]) -> Result<(), Self::Error> { Ok(()) }
        fn write(&mut self, words: &[u8]) -> Result<(), Self::Error> { Ok(()) }
        fn transfer(&mut self, read: &mut [u8], write: &[u8]) -> Result<(), Self::Error> { Ok(()) }
    }
    
    #[test]
    fn test_sensor_read() {
        let mut spi = MockSpi;
        let val = read_sensor_value(&mut spi).unwrap();
        assert!(val > 0.0 && val < 100.0);
    }
}
```

### CI/CD

```yaml
# .github/workflows/embedded-ci.yml
name: Embedded CI
on: [push, pull_request]
jobs:
  build-check:
    strategy:
      matrix:
        target: [thumbv6m-none-eabi, thumbv7em-none-eabihf, thumbv7m-none-eabi]
        chip: [STM32G030K6Tx, STM32F401CCUx, STM32F103C8Tx]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.target }}
      - run: cargo build --release --target ${{ matrix.target }}
      - name: Binary size gate
        run: |
          SIZE=$(cargo size --release --target ${{ matrix.target }} -- -A | tail -1 | awk '{print $1}')
          echo "Binary size: $SIZE bytes"
          # Flash 限制门控
          [ $SIZE -lt 65536 ] || (echo "ERROR: Binary exceeds 64KB" && exit 1)
      - run: cargo clippy --target ${{ matrix.target }} -- -D warnings
      - run: cargo test  # Host tests (mock)
```

### Flash/RAM 优化

```toml
# Cargo.toml 优化配置
[profile.release]
opt-level = "z"       # 或 "s" (平衡速度/大小)
lto = true            # 链接时优化, 通常减少 10-20%
strip = true          # 去符号表
codegen-units = 1     # 单编译单元, 更好的 LTO
panic = "abort"       # 不展开 panic, 省空间
```

```c
// C 优化
// 1. 编译器标志: -Os (优化大小) 或 -O2
// 2. LTO: -flto
// 3. 去除未用函数: -ffunction-sections -fdata-sections + --gc-sections
// 4. 查看大小分布
//    arm-none-eabi-nm --size-sort -S build/app.elf | tail -20
//    arm-none-eabi-size build/app.elf
```

### 最佳实践

- **分层清晰**: HAL 只做寄存器操作, Driver 做协议逻辑, App 做业务
- **静态分配优先**: 嵌入式禁用动态内存, 预分配所有缓冲区
- **MISRA 合规**: 至少遵循 Rule 1-10 (安全关键系统需全部合规)
- **测试策略**: 单元测试用 mock, 集成测试用 HIL (Hardware-in-Loop)
- **二进制大小门控**: CI 中设置 Flash/RAM 上限, 防止膨胀
- **版本管理**: 固件版本号嵌入二进制, `git describe --dirty` 在编译时注入

---

## 8. 常见 MCU 平台

### 概述

不同 MCU 平台各有特点，选型需综合考虑：性能、功耗、外设、成本、供货、生态。

### STM32 系列

| 系列 | 内核 | 主频 | Flash | RAM | 特点 | 典型应用 |
|------|------|------|-------|-----|------|---------|
| **F0** | M0 | 48MHz | 16-256K | 4-32K | 入门, 便宜 | 简单控制 |
| **G0** | M0+ | 64MHz | 16-512K | 6-144K | F0替代, 更强 | 家电, 工控 |
| **L0** | M0+ | 48MHz | 16-192K | 2-20K | 超低功耗 | 传感器, 电池 |
| **F1** | M3 | 72MHz | 16-1024K | 4-96K | 经典, 生态好 | 通用, 教学 |
| **L4** | M4F | 80MHz | 128-1024K | 32-320K | 低功耗+FPU | 便携设备 |
| **F4** | M4F | 180MHz | 256-2048K | 64-512K | 性能均衡 | 工控, 通信 |
| **H7** | M7 | 480MHz | 512-2048K | 256-1024K | 高性能 | 图形, AI |
| **U5** | M33 | 160MHz | 256-4096K | 256-4096K | 安全+低功耗 | IoT, 支付 |

### 国产 MCU

| 厂商 | 系列 | 兼容 | 特点 | 适用 |
|------|------|------|------|------|
| **兆易创新** | GD32F1/F3/F4 | STM32F1/F3/F4 | 性能略高, 更便宜 | 消费电子 |
| **航顺** | HK32F030/F103 | STM32F030/F103 | Pin兼容, 低价 | 小家电 |
| **极海** | APM32F0/F1/F4 | STM32F0/F1/F4 | 工业级 | 工控 |
| **华大半导体** | HC32F003/F005/F031/F033 | 独立架构 | ARM M0+, 超低功耗 | 传感器 |
| **中微半导** | CMS32 | 独立 | 电表专用 | 能源计量 |
| **芯海** | CS32 | 独立 | 模拟+MCU | 消费 |

### Nordic nRF52/53

| 芯片 | 内核 | 特点 |
|------|------|------|
| **nRF52832** | M4F 64MHz | BLE 5.0, 512K Flash, 低功耗标杆 |
| **nRF52840** | M4F 64MHz | BLE 5 + USB, 1M Flash |
| **nRF5340** | M33双核 | BLE 5.3, 应用核+网络核分离 |
| **nRF54H20** | M33+RISC-V | 多核, WiFi+BLE+802.15.4 |

```toml
# Embassy nRF52832
[dependencies]
embassy-nrf = { version = "0.2", features = ["nrf52832", "time-driver-rtc1", "gpiote", "unstable-pac"] }
```

### NXP i.MX RT

| 芯片 | 内核 | 主频 | 特点 |
|------|------|------|------|
| **i.MX RT1062** | M7 | 600MHz | 交叉型 (MCU封装+应用处理器性能) |
| **i.MX RT1064** | M7 | 600MHz | 内置 4MB Flash |
| **i.MX RT1170** | M7+M4 | 1GHz+400MHz | 双核, 千兆ETH |

```toml
# Embassy i.MX RT
[dependencies]
embassy-imxrt = { version = "0.1", features = ["imxrt1062"] }
```

### ESP32 (RISC-V)

| 芯片 | 内核 | 特点 |
|------|------|------|
| **ESP32-C3** | RV32IMAC 160MHz | WiFi+BLE5, 入门级 |
| **ESP32-C6** | RV32IMAC 160MHz | WiFi6+BLE5, 低功耗 |
| **ESP32-S3** | Xtensa LX7 240MHz | WiFi+BLE, 摄像头, USB |
| **ESP32-P4** | RV32IMAFC 400MHz | 双核, H264, MIPI |

```toml
# ESP32-C3 Rust (esp-hal)
[dependencies]
esp-hal = { version = "0.21", features = ["esp32c3"] }
esp-hal-embassy = { version = "0.4", features = ["esp32c3"] }
```

### 最佳实践

- **选型决策树**: 低功耗 → L系列/G0; 性能 → F4/H7; BLE → nRF52; WiFi → ESP32
- **国产替代**: 优先选 Pin-compatible 的 (GD32/航顺), 移植成本最低
- **供货风险**: 工业产品避免单源, 至少准备一个 Pin-compatible 备选
- **开发板先行**: 先用 Nucleo/Discovery 板验证功能, 再投 PCB
- **Rust 生态**: STM32 > nRF52 > ESP32, 国产 MCU 生态较弱需自行写 PAC

---

## 9. 快速参考

### 交叉编译目标

```
thumbv6m-none-eabi     → Cortex-M0/M0+
thumbv7m-none-eabi     → Cortex-M3
thumbv7em-none-eabi    → Cortex-M4/M7 (无FPU)
thumbv7em-none-eabihf  → Cortex-M4/M7 (单精度FPU)
thumbv8m.base-none-eabi    → Cortex-M23
thumbv8m.main-none-eabi    → Cortex-M33 (无FPU)
thumbv8m.main-none-eabihf  → Cortex-M33 (单精度FPU)
riscv32imac-unknown-none-elf → RISC-V RV32IMAC
```

### 常用工具命令

```bash
# 编译 & 烧录
cargo build --release --target thumbv7em-none-eabihf
probe-rs run --chip STM32F401CCUx

# 大小分析
cargo size --release --target thumbv7em-none-eabihf
arm-none-eabi-objdump -h target/.../app

# 反汇编
cargo objdump --release -- -d | less
arm-none-eabi-objdump -d -S app.elf

# bin 生成 (OTA 用)
arm-none-eabi-objcopy -O binary app.elf app.bin
```

### 故障排查速查

| 症状 | 可能原因 | 排查方法 |
|------|---------|---------|
| HardFault | 空指针/栈溢出/除零 | 检查 CFSR, BFAR, HFSR |
| 卡死 | 死锁/中断风暴/死循环 | JTAG attach 看停在何处 |
| UART 乱码 | 波特率错/时钟错 | 示波器测实际波特率 |
| I2C NACK | 地址错/总线卡死 | 逻辑分析仪看 SDA/SCL |
| Flash 写失败 | 未解锁/页未擦除 | 检查 FLASH_SR 寄存器 |
| 电流过大 | 外设未关/引脚浮空 | 逐个关闭外设排查 |
| 唤醒失败 | 唤醒源未配置/时钟未恢复 | 检查 PWR_CSR, RCC 寄存器 |
