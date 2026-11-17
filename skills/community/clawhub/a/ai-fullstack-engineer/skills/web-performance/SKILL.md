---
name: web-performance
description: Web 性能优化：Core Web Vitals、bundle 分析、缓存策略、运行时性能
source:
  type: derived
  repo: skills-repo/ai-fullstack-engineer
  path: skills/web-performance/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/sickn33/antigravity-awesome-skills/web-performance-optimization
metadata:
  category: 性能
  platform: Web
  difficulty: 进阶
---

# Web 性能优化

> 系统化优化网站性能：加载速度、Core Web Vitals、bundle 大小、缓存策略、运行时性能。

## 能力

- **Core Web Vitals**：LCP（最大内容绘制）、INP（交互延迟）、CLS（布局偏移）优化
- **资源优化**：图片压缩与格式选择、字体加载策略、代码分割与懒加载
- **缓存策略**：CDN 配置、Service Worker、HTTP 缓存头、离线支持
- **Bundle 分析**：webpack/vite bundle 分析、tree-shaking、动态 import
- **运行时性能**：长任务拆分、requestAnimationFrame、Web Worker 卸载计算

## 使用方式

```
/web-performance 分析这个页面的性能瓶颈
/web-performance 优化这个 bundle，减小体积
/web-performance 帮我配置缓存策略
```

## 工作流

1. 运行 Lighthouse 获取基线指标（LCP/INP/CLS/TBT）
2. 分析 bundle 大小和网络瀑布图
3. 按优先级排序：LCP 资源 → bundle → 运行时 → 缓存
4. 逐项实施优化
5. 重新测量验证改善幅度

## 适用场景

- 页面加载速度优化
- 移动端 Web 性能提升
- 上线前性能审计
- 持续性能监控建立

## 限制

- 不涉及后端性能优化（数据库、API）
- 不涉及 CDN 服务商选择
- 不涉及 Native App 性能

## 相关参考（Playbook）

本子技能落地"Web 性能优化"，前端方法论见下列 `references/`（按需读取）：

- 前端深度 playbook（Core Web Vitals / bundle / 缓存 / 水合踩坑）：[references/frontend-playbook.md](../../references/frontend-playbook.md)