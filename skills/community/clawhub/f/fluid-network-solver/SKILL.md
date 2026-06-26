---
name: fluid-network-solver
description: >
  流体网络求解与分析工具。输入TOML格式的网络描述，计算压力流量分布，分析负载状态和连通性。
  Use when: 需要分析液压、环控、化工等流体网络系统的工况。
  NOT for: 瞬态流动分析、可压缩流体。
---

# Fluid Network Solver

## When to Run
- 用户需要分析流体网络
- 需要计算管路流量和压力分布
- 需要判断负载是否满足工作条件

## Workflow
1. 接收 TOML 格式的网络描述
2. 解析网络拓扑和节点属性
3. 根据指定工况求解线性流阻模型
4. 计算各节点压力和管路流量
5. 分析负载状态（压力/流量阈值）和连通性
6. 返回 JSON 格式结果

## Input Format
接受 JSON 格式输入：
```json
{
  "toml": "TOML格式的网络描述字符串",
  "scenario": "工况名称（可选）"
}