---
name: frontend-performance-audit
description: 分析前端页面性能并输出结构化优化报告。适用于页面速度慢、lighthouse 指标差、core web vitals 不达标、首屏慢、交互卡顿、bundle 过大、阻塞渲染资源过多等场景。
---

# 前端性能优化

当用户提供页面地址、构建配置或前端项目文件，并希望分析性能问题、输出优化建议时，使用本技能。

## 执行流程
1. 先识别已有输入：
   - 页面 URL
   - Lighthouse 指标
   - Network 瀑布图
   - Bundle 分析
   - 技术栈信息
2. 读取 `references/metrics.md`，确定必须输出的性能指标。
3. 读取 `references/diagnosis-rules.md`，根据症状匹配原因和建议。
4. 按 `references/report-template.md` 输出正式报告。

## 规则
- 有核心 Web 指标时，优先输出核心 Web 指标。
- 明确区分“已观测证据”和“推断结论”。
- 优先给出高收益、低改动成本的建议。
- 不要轻易建议重构，除非轻量优化不足以解决问题。
- 数据不完整时，要明确说明缺失项和结论置信度。