# 通信协议对比与实现

## 协议选型

| 协议 | 距离 | 速率 | 拓扑 | 抗干扰 |
|------|------|------|------|--------|
| UART | <1m | <5Mbps | 点对点 | 弱 |
| RS485 | <1200m | <10Mbps | 总线 | 强 |
| I2C | <1m | <3.4Mbps | 总线 | 中 |
| SPI | <1m | <几十Mbps | 总线+片选 | 弱 |
| CAN | <1000m | <1Mbps | 总线 | 极强 |
| LoRa | <10km | <几十kbps | 星形 | 极强 |
| BLE | <10m | <2Mbps | 星形 | 中 |

## RS485 + Modbus RTU

```c
// MAX485 收发控制
#define RS485_DE_HIGH()  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_12, GPIO_PIN_SET)
#define RS485_DE_LOW()   HAL_GPIO_WritePin(GPIOB, GPIO_PIN_12, GPIO_PIN_RESET)

void RS485_Send(uint8_t *data, uint8_t len) {
    RS485_DE_HIGH(); HAL_Delay(1);
    HAL_UART_Transmit(&huart1, data, len, 100);
    while (!__HAL_UART_GET_FLAG(&huart1, UART_FLAG_TC));
    HAL_Delay(1); RS485_DE_LOW();
}

// CRC16 (Modbus 标准)
uint16_t modbus_crc16(uint8_t *buf, uint8_t len) {
    uint16_t crc = 0xFFFF;
    for (int i = 0; i < len; i++) {
        crc ^= buf[i];
        for (int j = 0; j < 8; j++)
            crc = (crc & 1) ? ((crc >> 1) ^ 0xA001) : (crc >> 1);
    }
    return crc;
}
```

## CAN 总线

```c
// STM32 CAN 发送
CAN_TxHeaderTypeDef tx_header = {
    .StdId = 0x100, .IDE = CAN_ID_STD,
    .RTR = CAN_RTR_DATA, .DLC = 8
};
uint32_t mailbox;
uint8_t data[8] = {1, 2, 3, 4, 5, 6, 7, 8};
HAL_CAN_AddTxMessage(&hcan, &tx_header, data, &mailbox);
```

## 帧解析状态机

```c
typedef enum { FRAME_IDLE, FRAME_HEAD, FRAME_LEN, FRAME_DATA, FRAME_CRC } ParseState;

uint8_t protocol_parse(uint8_t ch) {
    static ParseState state = FRAME_IDLE;
    static uint8_t frame_len = 0, idx = 0;
    static uint8_t buf[128];

    switch (state) {
    case FRAME_IDLE:
        if (ch == 0xAA) state = FRAME_HEAD; break;
    case FRAME_HEAD:
        state = (ch == 0x55) ? FRAME_LEN : FRAME_IDLE; break;
    case FRAME_LEN:
        frame_len = ch; idx = 0; state = FRAME_DATA; break;
    case FRAME_DATA:
        buf[idx++] = ch;
        if (idx >= frame_len) state = FRAME_CRC; break;
    case FRAME_CRC:
        if (ch == calc_crc16(buf, idx))
            process_frame(buf, frame_len);
        state = FRAME_IDLE; break;
    }
}
```

## LoRa 发送

```c
// SX1278 发送模式
void LoRa_Transmit(uint8_t *data, uint8_t len) {
    HAL_GPIO_WritePin(RFSW_CTRL_GPIO_Port, RFSW_CTRL_Pin, GPIO_PIN_SET); // TX
    SX1278->RegOpMode = 0x08 | 0x01; // Sleep + LORA
    SX1278->RegFiFoAddrPtr = 0x80;
    for (int i = 0; i < len; i++) SX1278->RegFifo = data[i];
    SX1278->RegPayloadLength = len;
    SX1278->RegOpMode = 0x08 | 0x03; // TX
    while (!(SX1278->RegIrqFlags & 0x08)); // TxDone
    SX1278->RegIrqFlags = 0x08;
    HAL_GPIO_WritePin(RFSW_CTRL_GPIO_Port, RFSW_CTRL_Pin, GPIO_PIN_RESET); // RX
}
```
