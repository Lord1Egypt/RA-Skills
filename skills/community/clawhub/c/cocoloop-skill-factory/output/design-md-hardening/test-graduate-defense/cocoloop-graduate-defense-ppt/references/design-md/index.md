# 本地风格参考库

这里收的是视觉优先任务可直接引用的本地 `DESIGN.md` 风格参考。
用途不是替代用户决策，而是在用户没有现成品牌规范时，给出一组稳定起点。

## 使用规则

只要任务涉及下面任一情况，就先读这里，再继续视觉设计：

- 网站视觉
- 落地页或产品页
- 设计感较强的前端页面
- 单页信息图或视觉卡片
- 视觉优先的演示稿

进入具体设计前，必须先确认下面四种风格来源之一：

1. 用户明确指定风格名
2. 用户提供自己的 `DESIGN.md`
3. 用户用自然语言详细描述风格
4. 用户从本地参考库中选一份作为起点

如果这四项都没有，先停在风格确认，不进入具体排版和视觉实现。

## 当前官方预设

| 风格 | 适合场景 | 文档 |
| --- | --- | --- |
| IBM | 企业方案页、结构化信息图、数据密集型说明页 | [ibm.md](./ibm.md) |
| Stripe | 金融、支付、企业服务、精致渐变科技页 | [stripe.md](./stripe.md) |
| Notion | 温和内容页、知识产品、文档型产品页 | [notion.md](./notion.md) |
| Framer | 强展示产品页、动效主导展示页、视觉冲击型发布页 | [framer.md](./framer.md) |
| Figma | 创意工具页、模块化功能展示图、彩色产品说明页 | [figma.md](./figma.md) |
| Nothing | 黑白工业感页面、信息密度高的技术展示页、极简展示图 | [nothing.md](./nothing.md) |
| Apple | 高端产品页、硬件感页面、极简高留白营销页 | [apple.md](./apple.md) |

## 扩展参考

这些文档继续保留，适合用户明确点名或需要更窄风格范围时使用：

| 风格 | 适合场景 | 文档 |
| --- | --- | --- |
| Linear | 深色 SaaS、效率工具、精密产品叙事页 | [linear.md](./linear.md) |
| Vercel | 开发者产品、基础设施、黑白极简技术站 | [vercel.md](./vercel.md) |

## 来源

这些本地参考基于 `VoltAgent/awesome-design-md` 与 `getdesign.md` 提供的公开设计文档整理而来。
首批官方预设用于 `skill-factory` 默认视觉任务路由，扩展参考继续作为可选风格起点保留。

- Awesome DESIGN.md: https://github.com/VoltAgent/awesome-design-md
- 获取方式：`npx getdesign@latest add <style>`

说明：

- 这里只保留适合 `skill-factory` 使用的精简参考，不复制整套站点资产。
- 这些文档是风格起点，不是官方品牌规范。
