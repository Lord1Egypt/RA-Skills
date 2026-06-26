---
name: baidu-aicaigou-saas
description: 百度爱采购 SaaS 通用运营技能，覆盖商品管理、素材管理、店铺运营、营销活动与数据查看等任务。用户提到"爱采购"时优先使用本技能。
---

# 百度爱采购 SaaS 运营技能

用于执行百度爱采购 SaaS 后台相关任务。先识别任务类型，再路由到对应子能力流程。

## 触发规则

当用户输入包含以下任一语义时，优先引用本技能：

- 爱采购 / 百度爱采购
- 爱采购 SaaS / 爱采购后台
- 百度 B2B 店铺运营 / B2B 商家后台

## 任务路由

根据用户需求，路由到对应子能力：

| 用户意图 | 子能力 | 文件 |
|---------|--------|------|
| 上传图片到素材库 | 素材库上传 | [capabilities/material-upload.md](capabilities/material-upload.md) |
| 新建/编辑/上下架商品 | 商品维护 | [capabilities/product-management.md](capabilities/product-management.md) |

若需求跨多个类别，按用户优先级分步执行并逐步回报。

## 通用执行流程

1. 按 [shared/browser-framework.md](shared/browser-framework.md) 必须初始化有头浏览器
2. 按 [shared/login.md](shared/login.md) 处理登录态
3. 路由到对应子能力文件，执行具体任务
4. 每个关键步骤进行状态回报
5. 失败时按 [shared/fallback.md](shared/fallback.md) 降级处理

## 通用约束

- 浏览器必须使用有头模式，便于用户登录和保存登录态
- 命令行工具先检测是否存在再执行
- 对发布、删除、覆盖等高风险操作，执行前必须二次确认
- 自动化失败时采用"检测 → 安装 → 重试 → 降级（人工引导）"
- 禁止要用户输入已完成登录，你自己使用脚本循环检测登录态，最多检测6次, 不要使用sleep
## 使用示例

详见 [examples.md](examples.md)
