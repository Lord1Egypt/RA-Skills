# 外设驱动开发手册

## GPIO

### 工作模式

| 模式 | 用途 | 配置要点 |
|------|------|---------|
| Input-Floating | 按钮检测 | PUPD=00，外设关闭 |
| Input-PullUp | 按钮接GND | PUPD=01，上拉 |
| Input-PullDown | 按钮接VCC | PUPD=10，下拉 |
| Output-PP | 推挽输出 | 驱动LED，小电流负载 |
| Output-OD | 开漏输出 | I2C总线，OC门，多点控制 |
| AF-PP | 复用推挽 | UART/TIM PWM/SPI MOSI |
| AF-OD | 复用开漏 | I2C复用引脚 |

### 寄存器配置（STM32F1 直写）

```c
// 使能 GPIOB 时钟 (RCC_APB2ENR)
RCC->APB2ENR |= RCC_APB2ENR_IOPBEN;

// 配置 PB0 为 50MHz 推挽输出
GPIOB->CRL &= ~((0xF) << (0 * 4));        // 清除原配置
GPIOB->CRL |= (0x3 << (0 * 4));           // MODE=11(50MHz)
GPIOB->CRL |= (0x0 << (2 * 4));           // CNF=00(PP)

// 读取 PA1（输入模式，保持原样）
uint32_t state = (GPIOA->IDR & (1 << 1));
```

---

## UART

### 异步模式配置步骤

1. 使能 USART1 + GPIOA 时钟
2. 配置 PA9(TX) 复用推挽，PA10(RX) 输入
3. 写 BRR（115200 @ 72MHz: 72000000/115200 = 0x270）
4. 配置 CR1：TE=1（发送）, RE=1（接收）, RXNEIE=1（中断）
5. 使能 USART：UE=1

```c
// STM32F1 115200 8N1
USART1->BRR = 72000000 / 115200;  // 0x270
USART1->CR1 = USART_CR1_TE | USART_CR1_RE | USART_CR1_RXNEIE;
USART1->CR1 |= USART_CR1_UE;

// 发送字节
void UART_SendByte(USART_TypeDef *u, uint8_t ch) {
    while (!(u->SR & USART_SR_TXE));
    u->DR = ch;
}

// DMA 发送（高效率）
void UART_DMA_Init(void) {
    RCC->AHBENR |= RCC_AHBENR_DMA1EN;
    DMA1_Channel4->CPAR = (uint32_t)&USART1->DR;
    DMA1_Channel4->CMAR = (uint32_t)tx_buf;
    DMA1_Channel4->CNDTR = len;
    DMA1_Channel4->CCR = DMA_CCR1_DIR | DMA_CCR1_MINC | DMA_CCR1_TCIE;
}
```

---

## I2C

### 关键时序参数

| 参数 | 典型值（100kHz标准） | 快速模式400kHz |
|------|---------------------|---------------|
| SCL 频率 | 100kHz | 400kHz |
| SCL 高电平 | ≥4.0µs | ≥0.6µs |
| SCL 低电平 | ≥4.7µs | ≥1.3µs |
| 起始条件 setup | ≥4.7µs | ≥0.6µs |
| 停止条件 setup | ≥4.0µs | ≥0.6µs |

### I2C 引脚配置（开漏+上拉）

```c
// STM32F1 I2C1: PB6=SCL, PB7=SDA
GPIOB->CRL = (0x3<<24) | (0x3<<28)  // 开漏输出
GPIOB->ODR |= (1<<6) | (1<<7);      // 外设模式下拉无效，内部上拉

// 软件I2C（精确时序控制，推荐新手）
void I2C_Soft_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_6 | GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    I2C_SCL_H; I2C_SDA_H;  // 总线空闲
}

void I2C_Start(void) {
    I2C_SDA_H; I2C_SCL_H; delay_us(5);
    I2C_SDA_L; delay_us(5);
    I2C_SCL_L;
}
```

---

## SPI

### 四种模式（CPOL/CPHA）

| 模式 | CPOL | CPHA | 空闲SCLK | 采样沿 |
|------|------|------|---------|-------|
| 0 | 0 | 0 | 低电平 | 第一个边沿 |
| 1 | 0 | 1 | 低电平 | 第二个边沿 |
| 2 | 1 | 0 | 高电平 | 第一个边沿 |
| 3 | 1 | 1 | 高电平 | 第二个边沿 |

常用：**模式0**（CPOL=0, CPHA=0）

```c
// SPI 基本发送（STM32 HAL）
uint8_t SPI_SendRecvByte(SPI_HandleTypeDef *hspi, uint8_t data) {
    uint8_t ret;
    HAL_SPI_TransmitReceive(hspi, &data, &ret, 1, 100);
    return ret;
}

// 软件SPI（对时序要求严格时，如Flash读取）
void SPI_SW_SendByte(uint8_t byte) {
    for (int i = 7; i >= 0; i--) {
        (byte & (1 << i)) ? SPI_SDA_H : SPI_SDA_L;
        SPI_SCL_H;
        __NOP(); __NOP();  // 至少60ns
        SPI_SCL_L;
    }
}
```

---

## ADC

### 关键参数

- **分辨率**：12位（4096级），3.3V/4096 ≈ 0.8mV/级
- **采样时间**：越大越精确（电容充电时间），建议≥55 Cycles
- **参考电压**：内部1.2V bandgap 或外部 VREF+
- **DMA**：高采样率必备，避免CPU中断开销

```c
// ADC DMA 多通道采集（STM32F1）
void ADC_DMA_Init(void) {
    RCC->APB2ENR |= RCC_APB2ENR_ADC1EN;
    // ADC时钟预分频：PCLK2/6 = 12MHz（ADCCLK ≤ 14MHz）
    RCC->CFGR |= (2 << 14);  // PCLK2/6

    ADC1->SMPR2 |= (7 << 0) | (7 << 3) | (7 << 6); // CH0,1,2 采样周期239.5cycles
    
    ADC1->CR1 |= ADC_CR1_SCAN;  // 扫描模式
    ADC1->CR2 |= ADC_CR2_DMA | ADC_CR2_CONT;  // DMA + 连续转换
    ADC1->JSQR |= (2 << 20) | (1 << 15) | (0 << 10); // 3通道序列
    
    DMA1_Channel1->CPAR = (uint32_t)&ADC1->DR;
    DMA1_Channel1->CMAR = (uint32_t)adc_buf;
    DMA1_Channel1->CNDTR = 3;
    DMA1_Channel1->CCR = DMA_CCR1_MINC | DMA_CCR1_PSIZE_16BIT | DMA_CCR1_MSIZE_16BIT | DMA_CCR1_CIRC;
    DMA1_Channel1->CCR |= DMA_CCR1_EN;
    
    ADC1->CR2 |= ADC_CR2_ADON | ADC_CR2_SWSTART;
}
```

---

## Timer & PWM

### 定时器分类

| 类型 | 代表 | 用途 |
|------|------|------|
| 基本定时器 | TIM6/7 | 定时中断， DAC触发 |
| 通用定时器 | TIM2/3/4 | PWM，输入捕获，编码器 |
| 高级定时器 | TIM1/8 | 三相PWM，刹车，死区 |

### PWM 初始化（以 TIM3 CH2 为例，PB5）

```c
void PWM_Init(uint16_t period, uint16_t pulse) {
    // 1. GPIO复用配置
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;      // 复用推挽
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    // 2. 定时器时钟使能
    __HAL_RCC_TIM3_CLK_ENABLE();

    // 3. 时基配置
    TIM_HandleTypeDef htim = {0};
    htim.Instance = TIM3;
    htim.Init.Prescaler = 72 - 1;    // 1MHz
    htim.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim.Init.Period = period - 1;   // 周期
    htim.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_PWM_Init(&htim);

    // 4. PWM通道配置
    TIM_OC_InitTypeDef sConfig = {0};
    sConfig.OCMode = TIM_OCMODE_PWM1;
    sConfig.Pulse = pulse;             // 占空比
    sConfig.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfig.OCFastMode = TIM_OCFAST_DISABLE;
    HAL_TIM_PWM_ConfigChannel(&htim, &sConfig, TIM_CHANNEL_2);

    // 5. 启动
    HAL_TIM_PWM_Start(&htim, TIM_CHANNEL_2);
}

// 使用：PWM_Init(20000, 1500) => 50Hz, 7.5%占空比（舵机）
// 使用：PWM_Init(1000, 500)  => 1kHz, 50%占空比（电机）
```

---

## CRC

```c
// 使用STM32硬件CRC计算校验
uint32_t CRC_Calc(uint8_t *data, uint32_t len) {
    CRC->CR = CRC_CR_RESET;  // 复位
    for (uint32_t i = 0; i < len; i++) {
        CRC->DR = data[i];
    }
    return CRC->DR;
}
```
