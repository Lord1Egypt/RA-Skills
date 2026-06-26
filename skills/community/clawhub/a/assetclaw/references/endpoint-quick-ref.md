# AssetHub API 端点速查

> ⚠️ **动态文档**：此文件由 `bash scripts/assethub_api.sh module <模块名>` 动态生成。
> 如发现端点信息与实际不符，请运行 `bash scripts/assethub_api.sh modules` 查看最新模块列表。

## 资产模块 /assets

### 资产模块 `/assets`
资产的全生命周期管理，包括资产的增删改查、统计、导入导出等功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `assets` | 获取资产列表 |
| `GET` | `assets/:id` | 获取资产详情 (必填: id) |
| `POST` | `assets` | 创建资产 |
| `PUT` | `assets/:id` | 更新资产 |
| `DELETE` | `assets/:id` | 删除资产 |
| `GET` | `assets/statistics/overview` | 获取资产统计概览 |
| `GET` | `assets/statistics/by-department` | 获取部门资产分布 |
| `GET` | `assets/export` | 导出资产 |
| `GET` | `assets/import-template` | 下载导入模板 |
| `POST` | `assets/import` | 批量导入资产 |
| `GET` | `assets/categories/list` | 获取资产分类列表 |
| `POST` | `assets/categories` | 创建资产分类 |
| `PUT` | `assets/categories/:id` | 更新资产分类 |
| `DELETE` | `assets/categories/:id` | 删除资产分类 |
| `GET` | `assets/departments/list` | 获取部门列表 |

### 维修模块 `/maintenance`
资产维修记录管理，包括报修、维修进度跟踪、维修记录查询等功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `maintenance` | 获取维修列表 |
| `POST` | `maintenance` | 创建维修记录 |
| `GET` | `maintenance/:id` | 获取维修详情 |
| `PUT` | `maintenance/:id` | 更新维修记录 |
| `DELETE` | `maintenance/:id` | 删除维修记录 |

### AI维修助手 `/maintenance/ai`
基于AI的智能维修助手，支持自然语言交互创建维修记录

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `maintenance/ai/init` | 初始化对话 |
| `POST` | `maintenance/ai/message` | 发送消息 |
| `POST` | `maintenance/ai/submit-request` | 提交报修申请 |
| `POST` | `maintenance/ai/audio` | 语音输入 |
| `POST` | `maintenance/ai/extract` | 提取维修信息 |

### 库存盘点模块 `/inventory`
资产盘点管理，支持盘点计划制定、盘点执行、差异处理等功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `inventory` | 获取盘点列表 |
| `POST` | `inventory` | 创建盘点任务 |
| `GET` | `inventory/:id` | 获取盘点详情 |
| `PUT` | `inventory/:id` | 更新盘点 |
| `POST` | `inventory/:id/records` | 提交盘点结果 |

### 资产调配模块 `/transfer`
资产调配申请管理，包括调配申请、审批流程、调配记录等功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `transfer` | 获取调配列表 |
| `POST` | `transfer` | 创建调配申请 |
| `GET` | `transfer/:id` | 获取调配详情 |
| `PUT` | `transfer/:id` | 更新调配申请 |
| `POST` | `transfer/:id/approve` | 审批调配 |
| `POST` | `transfer/:id/reject` | 拒绝调配 |

### 闲置资产模块 `/idle`
闲置资产管理和再利用

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `idle` | 获取闲置资产列表 |
| `POST` | `idle` | 标记为闲置 |
| `POST` | `idle/:id/reuse` | 重新利用闲置资产 |

### 报废管理模块 `/scrapping`
资产报废申请和审批管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `scrapping` | 获取报废申请列表 |
| `POST` | `scrapping` | 创建报废申请 |
| `GET` | `scrapping/:id` | 获取报废详情 |
| `POST` | `scrapping/:id/appraise` | 评估报废资产 |
| `POST` | `scrapping/:id/approve` | 审批报废 |
| `POST` | `scrapping/:id/dispose` | 处置报废资产 |

### 验收管理模块 `/acceptance`
资产验收管理，包括验收申请、验收记录等功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `acceptance` | 获取验收列表 |
| `POST` | `acceptance` | 创建验收 |
| `GET` | `acceptance/:id` | 获取验收详情 |
| `PUT` | `acceptance/:id` | 更新验收 |

### 技术资料模块 `/technical-documents`
资产技术资料管理，支持资料上传、分类管理、版本控制等功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `technical-documents` | 获取资料列表 |
| `POST` | `technical-documents` | 上传资料 |
| `GET` | `technical-documents/:id` | 获取资料详情 |
| `DELETE` | `technical-documents/:id` | 删除资料 |
| `GET` | `technical-documents/download/:id` | 下载资料 |

### AI文档分析模块 `/technical-documents/ai`
基于AI的技术资料智能分析功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `technical-documents/ai/analyze` | 分析文档 |
| `POST` | `technical-documents/ai/search` | 智能搜索 |
| `POST` | `technical-documents/ai/summary` | 生成摘要 |

### 资产定位模块 `/asset-location`
资产位置追踪和管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `asset-location` | 获取位置列表 |
| `POST` | `asset-location` | 更新位置 |
| `GET` | `asset-location/history/:assetId` | 获取位置历史 |

### IoT设备模块 `/iot-devices`
IoT设备管理，用于资产监控和追踪

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `iot-devices` | 获取设备列表 |
| `POST` | `iot-devices` | 注册设备 |
| `GET` | `iot-devices/:id` | 获取设备详情 |
| `PUT` | `iot-devices/:id` | 更新设备 |
| `DELETE` | `iot-devices/:id` | 删除设备 |
| `GET` | `iot-devices/:id/data` | 获取设备数据 |

### 用户管理模块 `/users`
系统用户管理，包括用户信息、角色权限等功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `users/profile` | 获取当前用户信息 |
| `PUT` | `users/profile` | 更新当前用户信息 |
| `PUT` | `users/password` | 修改密码 |
| `POST` | `users/login` | 用户登录 |
| `POST` | `users/logout` | 用户登出 |

### 角色权限模块 `/roles-permissions`
角色和权限管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `roles-permissions/roles` | 获取角色列表 |
| `POST` | `roles-permissions/roles` | 创建角色 |
| `GET` | `roles-permissions/permissions` | 获取权限列表 |
| `POST` | `roles-permissions/roles/:roleId/permissions` | 分配权限 |

### 部门管理模块 `/departments`
组织架构管理，包括部门创建、层级管理等功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `departments` | 获取部门列表 |
| `POST` | `departments` | 创建部门 |
| `GET` | `departments/:id` | 获取部门详情 |
| `PUT` | `departments/:id` | 更新部门 |
| `DELETE` | `departments/:id` | 删除部门 |

### 资产标签模块 `/asset-labels`
资产标签生成和管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `asset-labels/generate` | 生成标签 |
| `POST` | `asset-labels/print` | 打印标签 |

### 资产图片模块 `/asset-images`
资产图片管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `asset-images` | 获取图片列表 |
| `POST` | `asset-images` | 上传图片 |
| `DELETE` | `asset-images/:id` | 删除图片 |

### 临时资产模块 `/temp-assets`
临时资产登记和管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `temp-assets` | 获取临时资产列表 |
| `POST` | `temp-assets` | 创建临时资产 |
| `PUT` | `temp-assets/:id` | 更新临时资产 |
| `DELETE` | `temp-assets/:id` | 删除临时资产 |
| `POST` | `temp-assets/:id/convert` | 转为正式资产 |

### 位置编码模块 `/location-codes`
资产存放位置编码管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `location-codes` | 获取位置编码列表 |
| `POST` | `location-codes` | 创建位置编码 |
| `DELETE` | `location-codes/:id` | 删除位置编码 |

### 质量控制模块 `/quality-control`
资产质量控制管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `quality-control` | 获取质检列表 |
| `POST` | `quality-control` | 创建质检 |
| `GET` | `quality-control/:id` | 获取质检详情 |
| `POST` | `quality-control/:id/result` | 提交质检结果 |

### 不良反映模块 `/adverse-reaction`
资产不良反映管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `adverse-reaction` | 获取不良反映列表 |
| `POST` | `adverse-reaction` | 提交不良反映 |
| `GET` | `adverse-reaction/:id` | 获取详情 |
| `PUT` | `adverse-reaction/:id` | 更新不良反映 |

### 租户管理模块 `/tenants`
多租户管理（超级管理员专用）

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `tenants` | 获取租户列表 |
| `POST` | `tenants` | 创建租户 |
| `GET` | `tenants/:id` | 获取租户详情 |
| `PUT` | `tenants/:id` | 更新租户 |

### 审计日志模块 `/audit-logs`
系统操作审计日志

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `audit-logs` | 获取审计日志 |
| `GET` | `audit-logs/:id` | 获取日志详情 |

### 系统配置模块 `/system-config`
系统配置管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `system-config` | 获取配置 |
| `PUT` | `system-config` | 更新配置 |

### 备份恢复模块 `/backup`
数据备份和恢复管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `backup` | 获取备份列表 |
| `POST` | `backup` | 创建备份 |
| `GET` | `backup/:id` | 获取备份详情 |
| `POST` | `backup/:id/restore` | 恢复备份 |
| `DELETE` | `backup/:id` | 删除备份 |

### 增强权限模块 `/enhanced-permissions`
增强型权限管理，支持细粒度权限控制

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `enhanced-permissions` | 获取权限列表 |
| `POST` | `enhanced-permissions` | 创建权限 |
| `PUT` | `enhanced-permissions/:id` | 更新权限 |
| `DELETE` | `enhanced-permissions/:id` | 删除权限 |

### AI资产分析模块 `/asset-ai-analysis`
基于AI的资产智能分析功能

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `asset-ai-analysis/analyze` | AI资产分析 |
| `POST` | `asset-ai-analysis/predict` | 预测分析 |
| `POST` | `asset-ai-analysis/recommend` | 智能推荐 |

### 物资模块 `/materials`
低值易耗品管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `materials` | 获取物资列表 |
| `POST` | `materials` | 创建物资 |
| `PUT` | `materials/:id` | 更新物资 |
| `DELETE` | `materials/:id` | 删除物资 |

### 条码扫描模块 `/barcode-scan`
资产条码扫描和验证，支持批量盘点和扫码操作

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取扫描记录 |
| `GET` | `generate/:asset_code` | 生成资产条码 |
| `POST` | `verify` | 验证条码 |
| `POST` | `inventory` | 扫码盘点 |
| `GET` | `logs` | 获取扫描日志 |

### 盘点计划模块 `/inventory-plans`
盘点计划管理，支持创建、激活、完成、取消盘点计划

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取盘点计划列表 |
| `GET` | `:id` | 获取盘点计划详情 |
| `POST` | `` | 创建盘点计划 |
| `PUT` | `:id` | 更新盘点计划 |
| `DELETE` | `:id` | 删除盘点计划 |
| `PUT` | `:id/activate` | 激活盘点计划 |
| `PUT` | `:id/complete` | 完成盘点计划 |
| `PUT` | `:id/cancel` | 取消盘点计划 |

### 盘点差异模块 `/inventory-discrepancies`
盘点差异记录管理，支持差异处理和批量处理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取盘点差异列表 |
| `GET` | `:id` | 获取差异详情 |
| `PUT` | `:id/handle` | 处理差异 |
| `POST` | `batch-handle` | 批量处理差异 |
| `GET` | `:inventory_id/statistics` | 获取差异统计 |
| `POST` | `generate-from-details` | 生成差异记录 |

### 盘点任务模块 `/inventory-tasks`
盘点任务执行管理，支持任务分配、开始、完成、取消

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取盘点任务列表 |
| `GET` | `:id` | 获取任务详情 |
| `POST` | `` | 创建盘点任务 |
| `PUT` | `:id/assign` | 分配任务 |
| `PUT` | `:id/start` | 开始任务 |
| `PUT` | `:id/complete` | 完成任务 |
| `PUT` | `:id/cancel` | 取消任务 |
| `PUT` | `:id` | 更新任务 |
| `DELETE` | `:id` | 删除任务 |
| `GET` | `my/tasks` | 获取我的任务 |

### 智能告警模块 `/intelligent-alerts`
智能告警管理，支持告警查看、标记已读、处理等

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `overview` | 获取告警概览 |
| `GET` | `` | 获取告警列表 |
| `POST` | `:alertId/read` | 标记已读 |
| `POST` | `:alertId/handle` | 处理告警 |
| `POST` | `:alertId/unhandle` | 取消处理 |
| `POST` | `read-all` | 全部标记已读 |
| `POST` | `handle-all` | 批量处理告警 |
| `GET` | `maintenance` | 维修告警 |
| `GET` | `qualifications` | 资质告警 |
| `GET` | `inspections` | 巡检告警 |
| `GET` | `safety` | 安全告警 |
| `GET` | `uptime` | 运行时间告警 |
| `GET` | `settings` | 获取告警设置 |
| `POST` | `settings` | 更新告警设置 |

### 位置告警模块 `/location-alerts`
资产位置异常告警管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取位置告警列表 |
| `GET` | `stats` | 获取告警统计 |
| `PUT` | `:id/handle` | 处理告警 |
| `DELETE` | `:id` | 删除告警 |
| `POST` | `batch/handle` | 批量处理告警 |

### 采购管理模块 `/procurement`
采购申请管理，支持采购流程审批

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取采购列表 |
| `POST` | `` | 创建采购申请 |
| `PUT` | `:id/approve` | 审批采购 |

### 折旧计算模块 `/depreciation`
资产折旧计算和统计，支持多种折旧方法

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取折旧列表 |
| `GET` | `summary/by-department` | 按部门汇总折旧 |
| `GET` | `summary/by-type` | 按类型汇总折旧 |
| `GET` | `summary/by-month` | 按月统计折旧 |
| `POST` | `calculate` | 计算折旧 |
| `GET` | `export` | 导出折旧数据 |
| `GET` | `methods` | 获取折旧方法 |
| `GET` | `depreciation/:id` | 获取折旧详情 |

### 工作流模块 `/workflow`
资产状态工作流管理，支持状态迁移和流程配置

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取工作流列表 |
| `GET` | `default` | 获取默认工作流 |
| `GET` | `states` | 获取状态列表 |
| `GET` | `transitions` | 获取迁移规则 |
| `POST` | `transition/:assetId` | 执行状态迁移 |

### AI对话模块 `/ai`
AI对话服务，支持资产管理的智能问答

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `chat/completions` | 对话补全 |
| `POST` | `completions` | 补全请求 |
| `GET` | `config` | 获取AI配置 |

### 维修AI模块 `/maintenance-ai`
AI维修助手，支持自然语言处理维修工单

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `init` | 初始化对话 |
| `GET` | `pending` | 获取待处理请求 |
| `POST` | `message` | 发送消息 |
| `POST` | `submit-request` | 提交维修申请 |
| `POST` | `feedback` | 提交反馈 |
| `POST` | `audio` | 语音输入 |
| `GET` | `analysis` | AI分析 |
| `POST` | `test` | 测试AI |
| `GET` | `debug-asset` | 调试资产 |

### 云同步模块 `/cloud-sync`
多端数据云同步服务

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `webhook/:sourceId` | 接收Webhook |
| `GET` | `sources` | 获取同步源 |
| `POST` | `sources` | 创建同步源 |
| `PUT` | `sources/:id` | 更新同步源 |
| `DELETE` | `sources/:id` | 删除同步源 |
| `GET` | `events` | 获取同步事件 |
| `GET` | `events/stream` | 事件流 |

### 仪表板模块 `/dashboard`
仪表板数据接口，提供实时和统计的数据

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取仪表板数据 |
| `GET` | `realtime` | 获取实时数据 |

### 健康检查模块 `/health`
系统健康检查接口，无需认证

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `health` | 健康检查 |
| `GET` | `health/detailed` | 详细健康检查 |
| `GET` | `ready` | 就绪检查 |
| `GET` | `alive` | 存活检查 |
| `GET` | `metrics` | 获取指标 |
| `GET` | `circuit-breakers` | 获取熔断器状态 |
| `POST` | `circuit-breakers/:name/reset` | 重置熔断器 |

### 页面浏览模块 `/page-views`
页面浏览统计，无需认证

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `:pageKey` | 获取页面浏览量 |
| `POST` | `:pageKey` | 记录浏览 |

### 集成渠道模块 `/integration-channels`
第三方集成渠道管理，支持消息推送

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `channels` | 获取渠道列表 |
| `GET` | `channels/:channel` | 获取渠道详情 |
| `POST` | `channels/:channel` | 创建渠道 |
| `DELETE` | `channels/:channel` | 删除渠道 |
| `POST` | `channels/:channel/test` | 测试渠道 |
| `POST` | `channels/:channel/send-test` | 发送测试消息 |
| `GET` | `channels/:channel/templates` | 获取消息模板 |
| `POST` | `channels/:channel/templates` | 创建消息模板 |
| `DELETE` | `channels/:channel/templates/:templateId` | 删除消息模板 |

### 增强审计日志模块 `/audit-logs-enhanced`
增强型审计日志，支持统计、导出、清理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `enhanced` | 获取增强审计日志 |
| `GET` | `statistics` | 获取审计统计 |
| `GET` | `export` | 导出审计日志 |
| `POST` | `cleanup` | 清理审计日志 |
| `GET` | `operations` | 获取操作类型 |
| `GET` | `resource-types` | 获取资源类型 |

### 增强技术文档模块 `/technical-documents-enhanced`
增强型技术文档管理，支持分类、标签、版本、收藏、评论

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `categories` | 获取文档分类 |
| `POST` | `categories` | 创建文档分类 |
| `PUT` | `categories/:id` | 更新文档分类 |
| `DELETE` | `categories/:id` | 删除文档分类 |
| `GET` | `tags` | 获取文档标签 |
| `POST` | `tags` | 创建文档标签 |
| `DELETE` | `tags/:id` | 删除文档标签 |
| `POST` | `documents/:id/tags` | 更新文档标签 |
| `GET` | `documents/:id/tags` | 获取文档标签 |
| `GET` | `documents/:id/versions` | 获取文档版本 |
| `POST` | `documents/:id/versions` | 创建文档版本 |
| `POST` | `documents/:id/favorite` | 收藏文档 |
| `DELETE` | `documents/:id/favorite` | 取消收藏 |
| `GET` | `my/favorites` | 获取我的收藏 |
| `GET` | `documents/:id/comments` | 获取文档评论 |
| `POST` | `documents/:id/comments` | 添加文档评论 |
| `PUT` | `comments/:id/resolve` | 标记评论已解决 |
| `POST` | `documents/:id/view` | 记录文档浏览 |
| `GET` | `my/history` | 获取浏览历史 |
| `GET` | `statistics` | 获取文档统计 |
| `GET` | `templates` | 获取文档模板 |
| `POST` | `templates` | 创建文档模板 |
| `DELETE` | `templates/:id` | 删除文档模板 |
| `POST` | `batch/delete` | 批量删除文档 |
| `POST` | `batch/category` | 批量更新分类 |

### 数据分析模块 `/analysis`
资产数据分析，支持价值分布、折旧分析

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取分析数据 |
| `GET` | `value-distribution` | 获取价值分布 |
| `GET` | `depreciation` | 获取折旧分析 |

### 维修请求模块 `/maintenance/requests`
故障维修申请管理，支持审批、执行、完成

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取维修申请列表 |
| `GET` | `:id` | 获取申请详情 |
| `POST` | `` | 创建维修申请 |
| `POST` | `:id/approve` | 审批维修申请 |
| `POST` | `:id/start` | 开始维修 |
| `POST` | `:id/complete` | 完成维修 |
| `PUT` | `:id` | 更新维修申请 |
| `POST` | `:id/cancel` | 取消维修申请 |
| `DELETE` | `:id` | 删除维修申请 |

### 维修工单模块 `/maintenance/workorders`
维修工单执行管理，支持派工、执行、完工

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取维修工单列表 |
| `GET` | `:id` | 获取工单详情 |
| `POST` | `` | 创建维修工单 |
| `PUT` | `:id` | 更新工单 |
| `POST` | `:id/materials` | 添加工单材料 |
| `DELETE` | `:id` | 删除工单 |
| `POST` | `:id/assign` | 分配工单 |
| `POST` | `:id/start` | 开始工单 |
| `POST` | `:id/complete` | 完工工单 |
| `POST` | `:id/close` | 关闭工单 |
| `POST` | `:id/cancel` | 取消工单 |

### 维修费用模块 `/maintenance/costs`
维修费用统计和分析

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取维修费用列表 |
| `GET` | `trend` | 获取费用趋势 |
| `GET` | `department` | 按部门统计费用 |
| `GET` | `asset-type` | 按资产类型统计 |
| `GET` | `maintenance-type` | 按维修类型统计 |
| `GET` | `high-cost-assets` | 高费用资产 |
| `POST` | `` | 创建费用记录 |
| `PUT` | `:id` | 更新费用记录 |
| `DELETE` | `:id` | 删除费用记录 |
| `GET` | `analysis` | 获取费用分析 |

### 预防性维护计划模块 `/maintenance/plans`
预防性维护计划管理，支持计划制定、执行、记录

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取维护计划列表 |
| `GET` | `:id` | 获取计划详情 |
| `POST` | `` | 创建维护计划 |
| `PUT` | `:id` | 更新维护计划 |
| `POST` | `:id/complete` | 完成维护计划 |
| `DELETE` | `:id` | 删除维护计划 |
| `GET` | `:id/history` | 获取执行历史 |

### 维修日志模块 `/maintenance/logs`
维修记录日志管理，支持附件上传

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取维修日志列表 |
| `POST` | `` | 创建维修日志 |
| `PUT` | `:id` | 更新维修日志 |
| `DELETE` | `:id` | 删除维修日志 |
| `GET` | `:id/attachments` | 获取附件列表 |
| `POST` | `:id/attachments` | 上传附件 |
| `GET` | `:logId/attachments/:attachmentId` | 获取附件 |
| `GET` | `:logId/attachments/:attachmentId/download` | 下载附件 |
| `DELETE` | `:logId/attachments/:attachmentId` | 删除附件 |
| `GET` | `:id` | 获取日志详情 |
| `GET` | `statistics` | 获取维修统计 |

### 维修模板模块 `/maintenance/templates`
维修模板管理，支持模板创建、推荐

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取维修模板列表 |
| `POST` | `` | 创建维修模板 |
| `PUT` | `:id` | 更新维修模板 |
| `DELETE` | `:id` | 删除维修模板 |
| `GET` | `recommend` | 获取推荐模板 |
| `GET` | `recommend-by-asset` | 按资产推荐模板 |

### 资产使用量模块 `/maintenance/usage`
资产使用量追踪和触发维护

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `update` | 更新使用量 |
| `GET` | `history` | 获取使用历史 |
| `GET` | `statistics` | 获取使用统计 |
| `GET` | `check-thresholds` | 检查阈值 |
| `GET` | `usage-records` | 获取使用记录 |
| `POST` | `usage-records` | 创建使用记录 |
| `GET` | `usage-triggered` | 获取触发记录 |
| `POST` | `usage-triggered/:id/process` | 处理触发记录 |
| `POST` | `usage-triggered/check` | 检查触发 |

### 维修效率分析模块 `/maintenance/analytics`
维修效率统计分析

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `efficiency/overview` | 获取效率概览 |
| `GET` | `efficiency/response-time` | 获取响应时间 |
| `GET` | `efficiency/technician` | 获取技术人员统计 |
| `GET` | `efficiency/asset-frequency` | 获取资产频率 |
| `GET` | `analysis/asset-history` | 获取资产历史分析 |
| `GET` | `analysis/effectiveness-stats` | 获取效能统计 |
| `GET` | `analysis/cost-trend` | 获取费用趋势 |
| `GET` | `analysis/technician-performance` | 获取人员绩效 |
| `GET` | `analysis/type-distribution` | 获取类型分布 |
| `GET` | `analysis/frequency` | 获取维修频率 |
| `GET` | `asset-types/secondary` | 获取二级资产类型 |

### 维修评估模块 `/maintenance/evaluations`
维修质量评估管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取维修评估列表 |
| `POST` | `` | 创建维修评估 |
| `PUT` | `:id` | 更新维修评估 |

### 维护提醒模块 `/maintenance/reminders`
维护提醒配置和管理

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `` | 获取维护提醒列表 |
| `POST` | `send` | 发送提醒 |
| `POST` | `config` | 配置提醒 |
| `GET` | `check` | 检查提醒 |
