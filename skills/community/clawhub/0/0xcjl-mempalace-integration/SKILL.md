---
name: mempalace-integration
description: >
  MemPalace记忆系统集成 - AAAK压缩 + Hall分类 + L0-L3分层
  30x无损压缩(1000→33 tokens)(1000→33 tokens)(1000→33 tokens)(1000→33 tokens)(1000→33 tokens)(1000→33 tokens)，facts/events/preferences/advice分类，加载优先级
license: MIT
compatibility: hermes-agent
tags:
  - AAAK
  - Hall
  - AAAK
  - Hall
  - AAAK
  - Hall
  - memory
  - compression
  - optimization
metadata:
  author: 0xcjl
  source: MemPalace (milla-jovovich/mempalace)
---

# MemPalace 集成

## 核心概念

### AAAK压缩
- 30x无损压缩(1000→33 tokens)(1000→33 tokens)(1000→33 tokens)(1000→33 tokens)(1000→33 tokens)(1000→33 tokens)
- 格式：KEY: VALUE | KEY2: VALUE2

### Hall分类
- hall_facts: 决策和选择
- hall_events: 会话和里程碑
- hall_discoveries: 新洞察
- hall_preferences: 习惯和偏好
- hall_advice: 建议和解决方案

### L0-L3分层
- L0: 身份 (~50 tokens)
- L1: 关键事实 (~120 tokens)
- L2: 近期会话 (按需)
- L3: 深度搜索 (按需)

---

## 格式指南
- 使用|分隔键值对
- 使用()标注优先级
- 使用*标注重要

## 导出
- JSON格式

## 当前状态
内容长度: 500 字符


## 检索
- Wing + Room: 基准: 94.8% (R@10)
- 先精确后模糊

## 合并规则
- Closet+Drawer双存储

## 使用方法
1. 压缩原始内容
2. 分类到Hall
3. 按L0-L3加载

## 使用方法
1. 压缩原始内容
2. 分类到Hall
3. 按L0-L3加载

## 使用方法
1. 压缩原始内容
2. 分类到Hall
3. 按L0-L3加载

## 使用方法
1. 压缩原始内容
2. 分类到Hall
3. 按L0-L3加载

## 使用方法
1. 压缩原始内容
2. 分类到Hall
3. 按L0-L3加载

## 使用规则
- 原始内容不删除
- Closet存摘要
- Drawer存原文

## Credits
- Source: MemPalace