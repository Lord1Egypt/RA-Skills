# RTOS 实战（FreeRTOS / RT-Thread）

## 核心概念速查

| 概念 | 作用 | 典型使用 |
|------|------|---------|
| 任务 (Task) | 独立执行单元 | 传感器采集，通信处理 |
| 队列 (Queue) | 任务间传递数据 | ISR→任务，任务→任务 |
| 信号量 (Semaphore) | 资源计数/同步 | 保护共享资源 |
| 互斥量 (Mutex) | 防止优先级反转 | 总线访问 |
| 软件定时器 | 软定时器回调 | LED闪烁，心跳 |
| 事件组 (Event) | 多事件同步 | 多个条件组合触发 |

## FreeRTOS 任务创建

```c
#include "FreeRTOS.h"
#include "task.h"

// 任务函数（必须永不返回）
void Sensor_Task(void *arg) {
    TickType_t last_wake = xTaskGetTickCount();
    while (1) {
        float value = Read_Sensor();
        DataPacket pkt = {.val = value, .ts = last_wake};
        xQueueSend(data_queue, &pkt, 0);
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(100)); // 固定周期
    }
}

void Motor_Ctrl_Task(void *arg) {
    DataPacket pkt;
    while (1) {
        if (xQueueReceive(data_queue, &pkt, portMAX_DELAY) == pdTRUE) {
            Motor_SetPoint(pkt.val);
        }
    }
}

// 创建任务
StackType_t sensor_stack[256];
StaticTask_t sensor_tcb;
TaskHandle_t sensor_handle = xTaskCreateStatic(
    Sensor_Task, "Sensor", 256, NULL, 3,
    sensor_stack, &sensor_tcb
);

// 动态创建（需 heap_4/5）
xTaskCreate(Sensor_Task, "Sensor", 256, NULL, 3, NULL);
```

## 队列（数据传递）

```c
QueueHandle_t data_queue;

// 创建队列
data_queue = xQueueCreate(10, sizeof(DataPacket));

// 中断中发送（FromISR版本）
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
DataPacket pkt = { .val = 123 };
xQueueSendFromISR(data_queue, &pkt, &xHigherPriorityTaskWoken);
portYIELD_FROM_ISR(xHigherPriorityTaskWoken);

// 任务中接收
DataPacket pkt;
if (xQueueReceive(data_queue, &pkt, pdMS_TO_TICKS(500)) == pdTRUE) {
    // 处理数据
}
```

## 信号量

```c
// 二值信号量（Binary Semaphore）- ISR同步
SemaphoreHandle_t data_sem;

// 创建
data_sem = xSemaphoreCreateBinary();

// 中断中释放
xSemaphoreGiveFromISR(data_sem, &xHigherPriorityTaskWoken);

// 任务中获取
xSemaphoreTake(data_sem, portMAX_DELAY);

// 计数信号量 - 资源计数
SemaphoreHandle_t uart_sem = xSemaphoreCreateCounting(3, 3);
xSemaphoreTake(uart_sem, portMAX_DELAY);  // 获取
xSemaphoreGive(uart_sem);                  // 释放

// 互斥量（优先级继承，防止优先级反转）
MutexHandle_t i2c_mutex = xSemaphoreCreateMutex();
xSemaphoreTake(i2c_mutex, portMAX_DELAY);
I2C_Transfer();
xSemaphoreGive(i2c_mutex);
```

## 软件定时器

```c
TimerHandle_t led_timer;
bool led_state = false;

void LED_Timer_Callback(TimerHandle_t xTimer) {
    led_state = !led_state;
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13,
        led_state ? GPIO_PIN_SET : GPIO_PIN_RESET);
}

led_timer = xTimerCreate("LED", pdMS_TO_TICKS(500),
    pdTRUE, NULL, LED_Timer_Callback);  // 自动重载
xTimerStart(led_timer, 0);
```

## 内存管理

```c
// FreeRTOS Heap 配置
// heap_1.c: 最简单，不能释放（无 free，推荐小型系统）
// heap_2.c: 最佳匹配，可释放但不改归（推荐大多数场景）
// heap_4.c: 首次适应，支持合并（推荐复杂系统）
// heap_5.c: heap_4 + 非连续内存区域

// pvPortMalloc / vPortFree
uint8_t *buf = pvPortMalloc(256);
if (buf) {
    // 使用 buf
    vPortFree(buf);
}

// 静态分配（无内存碎片，推荐安全关键系统）
static uint8_t stack_buf[512];
StaticTask_t tcb_buf;
xTaskCreateStatic(..., stack_buf, &tcb_buf);
```

## RT-Thread 风格（Finsh/MSH）

```c
#include <rtthread.h>

// 定义组件
#define THREAD_PRIORITY      25
#define THREAD_STACK_SIZE    512
#define THREAD_TIMESLICE     10

ALIGN(RT_ALIGN_SIZE)
static char thread_stack[THREAD_STACK_SIZE];
static struct rt_thread thread;

void thread_entry(void *param) {
    while (rt_thread_mq_recv(&mq, &msg, RT_WAITING_FOREVER) == RT_EOK) {
        // 处理消息
    }
}

int thread_init(void) {
    rt_err_t err = rt_thread_init(&thread, "sensor",
        thread_entry, RT_NULL,
        thread_stack, THREAD_STACK_SIZE,
        THREAD_PRIORITY, THREAD_TIMESLICE);
    if (err == RT_EOK) {
        rt_thread_startup(&thread);
    }
    return 0;
}
MSH_CMD_EXPORT(thread_init, initialize sensor thread);
```

## 优先级反转与解决方案

```
低优先级任务 L 持有互斥锁
    ↓
高优先级任务 H 尝试获取该锁，阻塞
    ↓
中优先级任务 M（不需要该锁）运行，L 无法运行
    ↓
H 被 M 间接抢占，导致系统响应变差

解决：优先级继承（Mutex 天然支持）
FreeRTOS: configUSE_MUTEXES = 1 即可启用
```

## 常见错误

```c
// 错误1：栈溢出
void Bad_Task(void *arg) {
    float buf[512];  // 2KB 栈！256字节能否承受？
}
// 解决：用静态分配 + 栈水位监测

// 错误2：临界区内调用阻塞API
void HardFault_Handler(void) {
    vTaskDelay(100);  // 死锁！临界区不能睡眠
}

// 错误3：任务内 malloc 在中断中 free
// 解决：内存池（Memory Pool）

// 错误4：优先级设置错误
// 通信任务应高于数据处理任务
// sensor(高) → queue → motor_ctrl(中) → display(低)
```
