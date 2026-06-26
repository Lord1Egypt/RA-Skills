# frontmatter 模板库

## concept（概念页）
```yaml
---
title: "概念名称"
type: "concept"
tags: ["领域", "子领域"]
sources: []
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
summary: "一句话描述（≤50字）"
---

# 概念名称

## 定义

## 核心特征

## 例子

## 相关概念
[[concept-xxx]] · [[concept-yyy]]

## 参考文献
```

## entity（实体页）
```yaml
---
title: "实体名称"
type: "entity"
tags: ["类型", "领域"]
sources: []
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
summary: "一句话描述"
aliases: ["别名1", "别名2"]
---

# 实体名称

## 基本信息

## 关键事件/成就

## 与我的关系

## 相关笔记
[[concept-xxx]] · [[topic-yyy]]
```

## topic（主题页）
```yaml
---
title: "主题名称"
type: "topic"
tags: ["主题", "相关领域"]
sources: []
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
summary: "主题核心问题"
status: "active"
---

# 主题名称

## 主题概述

## 关键问题

## 当前认知

## 待探索方向

## 相关笔记
[[concept-xxx]] · [[entity-yyy]]
```
