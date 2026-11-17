# 寄存器术语速查（英 → 中）

SVD 里的描述通常是英文（厂商原文，工具原样输出）。这里收录寄存器/位域描述中高频出现的术语，
供回答时用中文解释。**术语解释是通用含义**；具体行为以 SVD 与芯片手册为准。

## 位域行为

| 术语 | 含义 |
|---|---|
| enable / disable | 使能 / 关闭 |
| set / clear | 置位（写 1）/ 清零（写 0） |
| toggle | 翻转 |
| reserved | 保留位：按复位值写，不要依赖读回值 |
| read-only / write-only | 只读 / 只写 |
| pending | 挂起（中断已触发、等处理器响应；写 1 通常清除） |
| flag | 标志位（硬件置位，软件清除） |
| ready (RDY) | 就绪（如 HSERDY：时钟稳定输出） |
| trigger | 触发（事件发生） |
| latch | 锁存（保持住某个瞬时值） |
| mask / masked | 屏蔽（禁止某事件产生影响） |
| bypass | 旁路（跳过某级电路） |
| overrun | 溢出（新数据覆盖了未读走的数据） |
| underrun | 下溢 |
| idle | 空闲（总线空闲 / 线路空闲） |
| wake-up / wakeup | 唤醒（从低功耗模式） |
| lock | 锁定（写保护，解锁前不可改） |
| one-shot | 单次触发模式 |
| prescaler (PSC) | 预分频器（把时钟频率降低 N+1 倍） |
| counter (CNT) | 计数器 |
| auto-reload (ARR) | 自动重载值（计到这里溢出/重装） |
| compare / capture | 比较 / 捕获（定时器通道功能） |
| duty cycle | 占空比 |
| baud rate | 波特率 |
| parity | 校验（偶/奇） |
| oversampling | 过采样（16 倍 / 8 倍） |
| flow control | 流控（RTS/CTS） |
| FIFO threshold | FIFO 阈值（触发水位） |
| watermark | 水位（FIFO 触发阈值） |
| sample / sampling | 采样 |
| conversion | 转换（ADC 一次测量） |
| calibration | 校准 |
| channel | 通道 |
| source / sink | 源（拉电流/来源）/ 灌（吸收电流/目标） |
| pull-up / pull-down | 上拉 / 下拉 |
| open-drain | 开漏输出 |
| push-pull | 推挽输出 |
| alternate function (AF) | 复用功能 |
| remap | 重映射（引脚/外设映射改变） |
| software / hardware | 软件 / 硬件触发来源 |
| DMA request | DMA 请求（外设要传数据给 DMA） |
| circular / normal mode | 循环模式 / 单次模式 |
| burst | 突发（一次连续传输多个数据） |
| transfer complete (TC) | 传输完成 |
| half transfer (HT) | 半传输（过半） |
| error / acknowledge (ACK) | 错误 / 应答 |

## 时钟与电源

| 术语 | 含义 |
|---|---|
| source (clock source) | 时钟源 |
| stable / settle | 稳定 / 建立时间 |
| divider | 分频器 |
| trim | 微调（内部 RC 频率校正值） |
| startup | 启动时间 |
| low-power / sleep / stop / standby | 低功耗 / 睡眠 / 停机 / 待机 |
| voltage regulator | 稳压器 |
| brown-out | 欠压 |

## 常见缩写

| 缩写 | 全称/含义 |
|---|---|
| EN | enable 使能 |
| DIS | disable 关闭 |
| IE | interrupt enable 中断使能 |
| IF | interrupt flag 中断标志 |
| ISR | interrupt status register 中断状态寄存器（ST 老命名）；在 Cortex-M 语境也指中断服务函数 |
| ICR / ICPR | interrupt clear register / clear-pending register 中断清除寄存器（写 1 清挂起） |
| ISER / ICER | interrupt set-enable / clear-enable register（NVIC 使能/关闭） |
| PR | pending register 挂起寄存器 |
| RDY | ready 就绪 |
| ERR | error 错误 |
| CFG / CFGR | configuration (register) 配置（寄存器） |
| CTL / CR | control (register) 控制（寄存器） |
| SR / STAT | status register 状态寄存器 |
| DR | data register 数据寄存器 |
| DIV | divider 分频 |
| HH / LL | high/half/low（如 ADC 高低阈值） |
| POL | polarity 极性 |
| TX / RX | 发送 / 接收 |
| RTS / CTS | request-to-send / clear-to-send 流控信号 |
| SW / SWS | switch / switch status 切换（选择）/ 当前状态 |
| W1C | write 1 to clear 写 1 清零（SVD 中对应 oneToClear） |
