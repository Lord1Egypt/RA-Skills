# Communication Protocols - 通信协议完整知识体系

> 覆盖物理层到应用层所有主流通信协议，每个协议统一结构：概述→帧格式→关键机制→开发要点→工具。

---

## 目录

1. [物理层/数据链路层](#1-物理层数据链路层)
2. [无线通信协议](#2-无线通信协议)
3. [网络层/传输层](#3-网络层传输层)
4. [应用层协议](#4-应用层协议)
5. [物联网协议](#5-物联网协议)
6. [安全](#6-安全)

---

## 1. 物理层/数据链路层

### 1.1 UART/RS-232/RS-485/RS-422

#### 概述

UART 是异步串行通信基础接口。RS-232/RS-485/RS-422 是基于 UART 的电气标准。

| 标准 | 拓扑 | 最大距离 | 最大速率 | 信号电平 | 收发 |
|------|------|----------|----------|----------|------|
| TTL UART | 点对点 | ~1m | ~5Mbps | 0/3.3V或0/5V | 1:1全双工 |
| RS-232 | 点对点 | 15m | 20kbps(标准) | ±5~±15V | 1:1全双工 |
| RS-422 | 1发10收 | 1200m | 10Mbps(12m内) | 差分±2~±6V | 全双工 |
| RS-485 | 多点 | 1200m | 10Mbps(12m内) | 差分±1.5~±5V | 半双工32节点 |

#### 帧格式

```
空闲(高) → 起始位(低,1bit) → 数据位(5/6/7/8bit, LSB first) → 校验位(可选:无/奇/偶) → 停止位(1/1.5/2bit, 高)
通信参数写作: 115200,8,N,1 (波特率,数据位,校验,停止位)
```

#### 关键机制

- **RS-232**: 全双工，DTE-DCE连接（TX↔RX, RTS↔CTS, DTR↔DSR, DCD, RI），D-sub 9/25针
- **RS-485**: 半双工差分传输，需方向控制（DE/RE引脚或自动方向切换），总线两端各120Ω终端匹配
- **RS-422**: 全双工差分传输，4线（TX+/TX-/RX+/RX-），1驱动10接收
- **多机通信**: 9-bit模式，第9位标识地址帧/数据帧
- **波特率容差**: <3%（推荐<2%）

#### 开发要点

- RS-485首尾各一个120Ω终端电阻，长总线中间无需
- 发送完成后需延迟再切接收（等最后一个字节完全发出）
- 长距离通信降低波特率（距离↑ → 速率↓）
- 工业现场用光耦/磁耦隔离（ADM2587E, ISO3082）
- 差分信号抗干扰强，适合工业噪声环境
- 常用波特率: 9600, 19200, 38400, 57600, 115200

#### 工具

- `minicom`/`picocom`/`screen` — Linux串口终端
- `pyserial` — Python串口库（跨平台）
- 逻辑分析仪 (Saleae, sigrok/pulseview) — 时序调试
- CH340/CP2102/FT232 — USB转串口芯片

---

### 1.2 SPI/I2S

#### 概述

SPI (Serial Peripheral Interface) 是同步全双工串行总线。I2S (Inter-IC Sound) 是 SPI 的音频扩展。

#### SPI 帧格式

```
CS# (低有效) → SCLK → MOSI(主出从入) / MISO(主入从出), MSB first
4种时钟模式: CPOL/CPHA = 00(空闲低,上升沿采样), 01(空闲低,下降沿), 10(空闲高,下降沿), 11(空闲高,上升沿)
```

#### I2S 格式

```
SCLK(位时钟) → WS(字选择,左右声道) → SD(串行数据)
采样率: 44.1/48/96/192kHz, 数据: 16/24/32bit
变体: TDM(多声道时分复用)
```

#### 关键机制

- **多从机**: 独立CS#线或菊花链(daisy-chain)
- **QSPI**: 4条数据线，吞吐×4，常用于Flash
- 时钟速率: 通常1~50MHz，高速可达100MHz+

#### 开发要点

- CS#传输前拉低、完成后拉高
- SPI无流控，从机需跟上主机时钟
- DMA用于高速场景（ADC、屏幕刷新）

#### 工具

- `spidev` — Linux SPI (`/dev/spidev0.0`), 逻辑分析仪

---

### 1.3 I2C

#### 概述

半双工同步串行总线，2线（SCL+SDA），多主多从。

#### 帧格式

```
起始(SCL高SDA↓) → 7位地址+R/W# → ACK → 数据(8bit×N) → ACK → 停止(SCL高SDA↑)
10位地址: 11110 + 高2位 + R/W# → ACK → 低8位 → ACK
```

#### 关键机制

- **时钟同步**: 线与(wired-AND)
- **仲裁**: SDA首个发低者赢
- **时钟拉伸**: 从机拉低SCL强制等待
- **速率**: 100k/400k/1M/3.4M bps
- **SMBus**: I2C子集，超时+PEC校验

#### 开发要点

- 上拉电阻: 4.7kΩ(典型)
- 总线电容≤400pF
- 地址冲突: PCA954x多路复用器
- 死锁恢复: 9个SCL脉冲
- 常见地址: 0x50(EEPROM), 0x68(RTC), 0x76(BME280)

#### 工具

- `i2cdetect`/`i2cget`/`i2cset`, Arduino `Wire`, 逻辑分析仪

---

### 1.4 CAN/CAN-FD

#### 概述

多主差分串行总线，汽车/工业标准。CAN-FD 支持可变数据长度和更高数据段波特率。

#### 帧格式

**CAN 2.0 标准帧**:
```
| SOF | 11位ID | RTR | IDE | r0 | DLC(4) | 数据(0-8B) | CRC(15) | ACK | EOF |
```

**CAN-FD**: EDL(=1)标识FD, BRS切换数据段速率, DLC支持0-64B, CRC增强(17/21位)
CAN-FD DLC: 0-8直接, 9→12B, 10→16B, 11→20B, 12→24B, 13→32B, 14→48B, 15→64B

#### 关键机制

- **位仲裁**: 显性(0)覆盖隐性(1)，ID越小优先级越高
- **位填充**: 5个同极性后插反极性位
- **错误状态**: Active → Passive(TEC/REC≥128) → Bus Off(TEC≥256)

#### 开发要点

- 两端各120Ω终端; 波特率+时间段需匹配; 过滤器: 屏蔽码+过滤码
- 常用波特率: 125/250/500/1000kbps

#### 工具

- `candump`/`cansend`/`cangen` (SocketCAN), `BUSMASTER`, Vector CANoe

---

### 1.5 1-Wire

#### 概述

Maxim(ADI)单总线协议，一根数据线通信+供电(寄生模式)。

#### 帧格式

```
复位(480μs低) → 存在脉冲(60~240μs低) → ROM命令(0x33读/0x55匹配/0xF0搜索) → 功能命令 → 数据
时间槽: 写0(60~120μs低), 写1(<15μs低), 读(<15μs低后15μs内采样)
```

#### 关键机制

- **寄生供电**: 高电平充电; **64位ROM ID**: CRC+序列号+家族码; **搜索ROM**: 二叉树

#### 开发要点

- 严格时序(关中断); 上拉2.2~4.7kΩ; 设备: DS18B20, DS2401

#### 工具

- `owfs` — Linux 1-Wire文件系统, DS9490R USB适配器

---

### 1.6 USB

#### 概述

通用串行总线，热插拔即插即用，树形拓扑。

#### 传输类型

| 类型 | 可靠性 | 用途 |
|------|--------|------|
| Control | 保证 | 枚举/配置 |
| Bulk | 保证 | 大数据(存储) |
| Interrupt | 保证 | 键鼠 |
| Isochronous | 不保证 | 音视频 |

#### 描述符层级

```
设备(VID/PID) → 配置 → 接口(Class/SubClass) → 端点(Address,Type,MaxPacketSize)
```

#### 枚举流程

```
插入→复位(地址0)→获取设备描述符(前8B)→分配地址→完整描述符→配置描述符→选择配置→就绪
```

#### 关键机制

- USB 2.0: 480Mbps, NRZI; USB 3.x: 5/10/20Gbps, 128b/132b
- 供电: PD 3.1 EPR最高240W(48V/5A)
- Type-C: CC引脚/PD/替代模式

#### 开发要点

- VID/PID向USB-IF购买; CDC-ACM虚拟串口; HID免驱
- 调试: `lsusb -v`, `usbmon`, Wireshark

#### 工具

- `lsusb -v`, `libusb`, Wireshark+usbmon

---

### 1.7 以太网

#### 概述

IEEE 802.3，从10Mbps演进到400Gbps+。

#### 802.3 MAC 帧

```
| 前导(7B) | SFD(1B) | 目的MAC(6B) | 源MAC(6B) | EtherType(2B) | Payload(46-1500B) | FCS(4B) |
最小64B, 标准1518B, Jumbo 9018B
VLAN(802.1Q): TPID(0x8100)+PCP+VID
EtherType: 0x0800(IPv4), 0x86DD(IPv6), 0x0806(ARP)
```

#### 关键机制

- **Auto-Negotiation**: FLP交换能力; **PAUSE帧**: 流量控制; **PTP(1588)**: 时间同步
- 物理层: 100BASE-TX(100M), 1000BASE-T(1G), 10GBASE-T(10G), 10GBASE-SR/LR(光纤)

#### 开发要点

- MAC-PHY: MII/RMII/RGMII; MDIO/MDC配置PHY; WoL: Magic Packet

#### 工具

- `tcpdump`/`Wireshark`, `ethtool`, `iperf3`, `nmap`

---

### 1.8 PPP/HDLC/LAPB

#### 概述

HDLC: ISO基础链路层; PPP: LCP+NCP扩展; LAPB: X.25数据链路层。

#### 帧格式

**HDLC**: `| 标志(0x7E) | 地址 | 控制(I/S/U帧) | 信息 | FCS | 标志(0x7E) |` (0比特填充)
**PPP**: `| 标志(0x7E) | 0xFF | 0x03 | 协议(2B) | 信息 | FCS | 标志(0x7E) |`
协议: 0x0021(IP), 0x8021(IPCP), 0xC021(LCP), 0xC023(PAP), 0xC223(CHAP)

#### 关键机制

- **LCP**: 链路建立/配置/终止; **NCP**: IPCP分配IP/DNS
- **PAP**: 明文2次握手; **CHAP**: MD5 3次握手; **MP**: 多链路捆绑

#### 工具

- `pppd`, `chat`, `minicom`

---

## 2. 无线通信协议

### 2.1 LoRa/LoRaWAN

#### 概述

LoRa: Semtech CSS物理层调制。LoRaWAN: 基于LoRa的MAC层(LoRa联盟)。

#### LoRa 物理层参数

| 参数 | 说明 | 可选值 |
|------|------|--------|
| SF | 扩频因子 | 5~12(标准7~12) |
| BW | 信号带宽 | 125/250/500kHz |
| CR | 纠错编码率 | 4/5, 4/6, 4/7, 4/8 |

链路预算: SF12+BW125 ≈ 157dB (15km+); SF7@125k≈5.5kbps, SF12@125k≈250bps

#### LoRaWAN MAC 层

| Class | 下行模式 | 场景 |
|-------|---------|------|
| A | 发送后两接收窗口 | 传感器(最低功耗) |
| B | Ping Slot接收 | 下行调度 |
| C | 持续接收 | 市电供电 |

**消息格式**: `PHYPayload = MHDR(1B) | MACPayload | MIC(4B)`
MACPayload = FHDR(DevAddr 4B + FCtrl + FCnt 2B + FOpts) | FPort | FRMPayload

**Join (OTAA)**: 设备发Join Request(AppEUI+DevEUI+DevNonce) → NS回Join Accept(AppNonce+NetID+DevAddr, AES加密) → 派生NwkSKey/AppSKey
**ABP**: 预配置DevAddr+NwkSKey+AppSKey

**ADR**: 根据SNR/RSSI自动调整SF/BW/TxPower

#### CN470 频段(中国)

- 上行: 470.3~489.3MHz, 96通道(200kHz); 下行: 500.3~509.7MHz
- 发射功率: ≤17dBm, 需SRRC认证

#### 开发要点

- 1%占空比限制; Rx Delay 1/2(1s/2s); Frame Counter需持久化
- 芯片: SX1276/78, SX1261/62

#### 工具

- `ChirpStack`(开源NS), `TTN`(公共网络), `RadioHead`(Arduino)

---

### 2.2 NB-IoT

#### 概述

3GPP R13蜂窝物联网，180kHz带宽，覆盖增强20dB，PSM/eDRX低功耗。

#### 部署模式

| 模式 | 说明 |
|------|------|
| In-band | LTE载波内替换一个PRB |
| Guard-band | LTE保护带 |
| Stand-alone | 独立频谱(GSM refarming) |

#### 版本演进

- R13: 基础(CE 0-3, PSM, eDRX)
- R14: 多载波, 定位(OTDOA), multicast
- R17: NTN(卫星)支持

#### 关键机制

- **CE Level 0-3**: 最多2048次重复
- **PSM**: T3324活跃定时器 + T3412周期TAU, 深度睡眠数天
- **eDRX**: 寻呼周期最长2.56h
- **NPRACH**: 3.75kHz单音 → NPDCCH → NPDSCH

#### 开发要点

- 模组: BC26/BC35-G(移远), Hi2115; AT: `AT+CEREG`, `AT+CGATT`, `AT+NPSMR`
- 运营商APN: CMIoT/CTNET/UNIM2M; 功耗优化: PSM+eDRX

#### 工具

- `QNavigator`, 运营商IoT平台, `minicom`

---

### 2.3 LTE Cat.1

#### 概述

3GPP R8 UE Cat.1, 下行10Mbps/上行5Mbps, 中速物联网，LTE广覆盖优势。

#### 协议栈

```
用户面: 应用 → PDCP → RLC → MAC → PHY
控制面: RRC → NAS(EMM/ESM) → EPC(MME/S-GW/P-GW/HSS)
```

#### 附着流程

```
PLMN选择 → 小区选择 → SIB → RRC建立(PRACH→Request→Setup→Complete)
→ NAS Attach Request → EPC认证(MME↔HSS AKA) → 承载建立 → Attach Accept
```

#### EPS 承载

- 默认承载: Attach自动建立, Best Effort (QCI 5-9)
- 专用承载: 按需, QoS保障(QCI 1-4 GBR)

#### AT 指令

```
AT+CFUN=1; AT+CGREG?; AT+CGDCONT=1,"IP","cmnet"; AT+CGATT=1; AT+CGACT=1,1
AT+CIPSTART="TCP","server",port; AT+MQTTCONN/PUB/SUB(移远扩展)
```

#### 开发要点

- Cat.1 bis: 单天线(R15); 模组: EC20/EC200T, ML302, L610
- 支持 VoLTE; 功耗: 空闲~3mA(DRX)

#### 工具

- `minicom`, `usb_modeswitch`, `wvdial`/`pppd`, `qmi-utils`

---

### 2.4 5G NR

#### 概述

5G New Radio: eMBB/URLLC/mMTC。

#### 频段

- FR1(Sub-6G): 410MHz~7.125GHz, 覆盖好
- FR2(mmWave): 24.25~52.6GHz, 大带宽高速率
- 中国: n78(3300~3800MHz), n41(2496~2690MHz), n79(4400~5000MHz)

#### 关键物理信道

- **SSB**: PSS+SSS+PBCH, 同步/小区搜索
- **PRACH**: 随机接入前导码(Format 0~3 FR1, A/B FR2)
- **PDCCH**: DCI调度PDSCH/PUSCH
- **numerology**: SCS 15/30/60/120/240kHz (μ=0~4)
- **BWP**: 带宽部分, UE可配置

#### 关键技术

- Massive MIMO (64T64R+), 波束管理(SSB扫描,CSI-RS,SRS)
- 网络切片, SBA 5GC核心网
- RedCap (R17): 简化5G用于IoT

#### 工具

- `srsRAN`(开源RAN), `UERANSIM`(5G模拟)

---

### 2.5 BLE 5.x

#### 概述

Bluetooth Low Energy, 低功耗蓝牙。BLE 5.0: 2M PHY+长距离+广播扩展。BLE 5.2: LE Isochronous。

#### GAP 设备角色

Central(主机) / Peripheral(从机) / Broadcaster(广播者) / Observer(观察者)

**广播**: 通道37/38/39 → AdvData(31B Legacy / 255B Extended) → 扫描请求/响应(可选) → 连接

#### GATT 层级

```
Profile → Service(UUID 16/128bit) → Characteristic(值+CCCD 0x2902) → Descriptor
CCCD: 使能Notification(无确认)或Indication(有确认)
```

#### 关键参数

- **MTU**: 默认23B(有效20B), 可协商至517B (iOS默认185B)
- **连接间隔**: 7.5ms~4s(默认30ms)
- **DLE**: 单包27B→251B (BLE 4.2+)
- **2M PHY**: 速率翻倍; **Coded PHY(125kbps)**: 长距离

#### 开发要点

- 服务发现UUID+缓存; Notify快/Indicate可靠
- 安全: SMP配对, AES-CCM加密
- 芯片: nRF52832/40, ESP32-C3, CH582

#### 工具

- `nRF Connect`(手机), `nRF sniffer`, `bleno`/`noble`(Node.js)

---

### 2.6 ZigBee 3.0

#### 概述

基于IEEE 802.15.4的Mesh网络。ZigBee PRO 2017/3.0统一配置文件。

#### 网络拓扑

| 拓扑 | 说明 |
|------|------|
| 星形 | 1协调器+N终端 |
| 树形 | 协调器→路由器→终端 |
| Mesh | 多路由冗余路径 |

设备角色: 协调器(1个网络1个), 路由器, 终端(低功耗)

#### ZCL (ZigBee Cluster Library)

```
端点(1~240) → 簇(Cluster, 16bit) → 属性(Attribute)
操作: Read/Write/Report/Configure Reporting
```

#### 关键机制

- 128位AES加密; 16位短地址+64位MAC地址
- AODV路由; 绑定表实现跨设备通信; OTA升级

#### 开发要点

- 协议栈: Z-Stack(TI), EmberZNet(Silicon Labs)
- 信道: 11~26(2.4GHz); PAN ID: 16位标识网络

#### 工具

- `Zigbee2MQTT`, XCTU(Digi)

---

### 2.7 Wi-Fi 6/7

#### 概述

- Wi-Fi 6 (802.11ax): OFDMA, MU-MIMO上下行, BSS Coloring
- Wi-Fi 7 (802.11be): 320MHz, 4096-QAM, MLO(多链路), MRU

| 特性 | Wi-Fi 6 | Wi-Fi 7 |
|------|---------|---------|
| 峰值速率 | 9.6Gbps | 46Gbps |
| 频段 | 2.4/5/6GHz | 2.4/5/6GHz |
| 最大带宽 | 160MHz | 320MHz |
| 调制 | 1024-QAM | 4096-QAM |
| OFDMA | RU: 26~2×996 | MRU更灵活 |
| MU-MIMO | 8×8 | 16×16 |
| BSS Coloring | 6bit | 增强 |

#### 关键机制

- **OFDMA**: 信道分多个RU并行传输, 提升多用户效率
- **MU-MIMO**: 空间复用, 上下行多用户
- **BSS Coloring**: 6bit标识, 同频干扰判断
- **TWT (Target Wake Time)**: 调度设备唤醒, 降低功耗
- **MLO (Multi-Link Operation)**: Wi-Fi 7同时用多条链路, 降低延迟

#### 开发要点

- 芯片: ESP32-C6/C5(Wi-Fi 6), IPQ6018, MT7916
- WPA3: SAE认证, OWE(机会性加密)
- 6GHz: DFS不需, 更多连续信道

#### 工具

- `iwconfig`/`iw`, `Wireshark`, `iperf3`

---

### 2.8 Thread/Matter

#### 概述

- **Thread**: 基于6LoWPAN/IPv6 over 802.15.4的Mesh网络, 无单点故障
- **Matter**: CSA(原CSA/Connectivity Standards Alliance)统一智能家居协议, 运行在Thread/Wi-Fi/Ethernet上

#### Thread 关键机制

- IPv6 over 802.15.4 (2.4GHz, 6LoWPAN适配)
- Mesh路由: MPL(Multicast), 地址分配(SLAAC)
- 设备角色: Leader, Router,