---
name: capacity-monitor
description: Monitors system resource utilization and reports idle capacity for workload scheduling
tags:
  - compute
  - monitoring
  - capacity
  - system
category: system-administration
version: 1.0.0
---

# 容量监控器

## 概述

读取系统资源使用情况（CPU、内存），计算当前空闲容量。供下游调度器用于决定在系统空闲时运行哪些辅助任务以提升资源利用率。

## 使用场景

- 资源优化：在系统空闲时启动辅助任务
- 容量规划：记录资源使用趋势辅助容量规划
- 负载均衡：识别低负载节点以分配更多任务

## 使用方法

1. 读取 `/proc/loadavg` 获取 CPU 负载。
2. 读取系统内存信息计算空闲内存。
3. 输出空闲容量报告 JSON。

## 输出格式

```json
{
  "monitor_timestamp": "2026-06-01T12:00:00",
  "cpu_percent_idle": 75.0,
  "memory_mb_available": 4096,
  "status": "completed"
}
```

## 实现代码

见 `scripts/monitor.py`。
