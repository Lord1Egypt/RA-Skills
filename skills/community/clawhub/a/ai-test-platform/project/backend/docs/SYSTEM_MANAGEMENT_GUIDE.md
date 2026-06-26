# 系统管理模块使用指南

## 📖 概述

系统管理模块提供完整的平台管理和运维功能：
- AI模型管理（在线/本地模型）
- 测试环境管理（多环境支持）
- 操作日志审计（完整审计线索）
- 数据备份与恢复（自动化备份）

## 🚀 快速开始

### 1. AI模型配置

#### 配置DeepSeek在线模型

```bash
POST http://localhost:8000/api/system/ai-model

{
  "name": "DeepSeek-Primary",
  "model_type": "online",
  "provider": "deepseek",
  "model_name": "deepseek-chat",
  "api_key": "your_deepseek_api_key_here",
  "api_base_url": "https://api.deepseek.com",
  "max_tokens": 2000,
  "temperature": 70,
  "timeout": 30,
  "max_retries": 2,
  "is_default": true
}
```

#### 配置本地模型（Ollama）

```bash
POST http://localhost:8000/api/system/ai-model

{
  "name": "Ollama-Local",
  "model_type": "local",
  "provider": "ollama",
  "model_name": "qwen:7b",
  "api_base_url": "http://localhost:11434",
  "max_tokens": 2000,
  "temperature": 70,
  "is_default": true
}
```

**配置OpenAI兼容模型：**

```bash
{
  "name": "GPT-4-Compatible",
  "model_type": "online",
  "provider": "local",
  "model_name": "gpt-4",
  "api_base_url": "http://localhost:8001/v1",
  "is_default": true
}
```

#### 查看模型配置列表

```bash
GET http://localhost:8000/api/system/ai-model/list?model_type=online
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "查询成功",
  "data": [
    {
      "id": 1,
      "name": "DeepSeek-Primary",
      "model_type": "online",
      "provider": "deepseek",
      "model_name": "deepseek-chat",
      "api_base_url": "https://api.deepseek.com",
      "max_tokens": 2000,
      "temperature": 70,
      "timeout": 30,
      "is_active": true,
      "is_default": true
    }
  ]
}
```

#### 测试模型配置

```bash
POST http://localhost:8000/api/system/ai-model/1/test
```

### 2. 测试环境管理

#### 创建开发环境

```bash
POST http://localhost:8000/api/system/environment

{
  "name": "dev",
  "env_type": "dev",
  "base_url": "http://localhost:8000",
  "description": "开发环境API服务",
  "headers": {
    "Authorization": "Bearer dev_token"
  },
  "params": {
    "timeout": "30"
  },
  "is_default": true
}
```

#### 创建生产环境

```bash
POST http://localhost:8000/api/system/environment

{
  "name": "prod",
  "env_type": "prod",
  "base_url": "https://api.example.com",
  "description": "生产环境API服务",
  "headers": {
    "Authorization": "Bearer prod_token",
    "X-Environment": "production"
  },
  "is_default": false
}
```

#### 查看环境列表

```bash
GET http://localhost:8000/api/system/environment/list
```

#### 获取默认环境

```bash
GET http://localhost:8000/api/system/environment/default
```

### 3. 操作日志

#### 查询操作日志

```bash
GET http://localhost:8000/api/system/log/list?limit=100
```

**过滤参数：**
- `?user_id=xxx` - 按用户ID过滤
- `?operation_type=execute` - 按操作类型过滤
- `?operation_module=api` - 按模块过滤
- `?start_date=2026-03-01` - 起始日期
- `end_date=2026-03-31` - 结束日期

**日志类型：**
- `generate` - AI生成操作
- `execute` - 测试执行操作
- `api_test` - API测试操作
- `ui_test` - UI测试操作
- `system` - 系统管理操作

### 4. 数据备份

#### 创建全量备份

```bash
POST http://localhost:8000/api/system/backup

{
  "name": "full-backup-2026-03-23",
  "backup_type": "full",
  "backup_scope": "all"
}
```

#### 创建增量备份

```bash
POST http://localhost:8000/api/system/backup

{
  "name": "incremental-backup-2026-03-23",
  "backup_type": "incremental",
  "backup_scope": "database"
}
```

#### 查看待处理的备份

```bash
GET http://localhost:8000/api/system/backup/list?status=completed
```

#### 查看备份详情

```bash
GET http://localhost:8000/api/system/backup/1
```

#### 恢复备份

```bash
POST http://localhost:8000/api/system/backup/restore

{
  "backup_id": 1,
  "restore_scope": "all"
}
```

## 🔧 API 接口列表

### AI模型管理 (8个接口)

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/system/ai-model` | POST | 创建AI模型配置 |
| `/api/system/ai-model/list` | GET | 获取模型配置列表 |
| `/api/system/ai-model/default` | GET | 获取默认模型配置 |
| `/api/system/ai-model/{id}` | GET | 获取模型配置详情 |
| `/api/system/ai-model/{id}` | PUT | 更新模型配置 |
| `/api/system/ai-model/{id}` | DELETE | 删除模型配置 |
| `/api/system/ai-model/{id}/test` | POST | 测试模型连接 |

### 测试环境管理 (7个接口)

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/system/environment` | POST | 创建测试环境 |
| `/api/system/environment/list` | GET | 获取环境列表 |
| `/api/system/environment/default` | GET | 获取默认环境 |
| `/api/system/environment/{id}` | GET | 获取环境详情 |
| `/api/system/environment/{id}` | PUT | 更新环境 |
| `/api/system/environment/{id}` | DELETE | 删除环境 |

### 操作日志 (1个接口)

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/system/log/list` | GET | 获取操作日志列表 |

### 数据备份 (5个接口)

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/system/backup` | POST | 创建备份 |
| `/api/system/backup/list` | GET | 获取备份列表 |
| `/api/system/backup/{id}` | GET | 获取备份详情 |
| `/api/system/backup/{id}` | DELETE | 删除备份 |
| `/api/system/backup/restore` | POST | 恢复备份 |

## 💡 最佳实践

### 1. AI模型配置

**模型选择策略：**

- **在线模型**：适合高准确需求，需要API密钥
- **本地模型**：适合内网环境，离线使用，成本为零

**推荐配置：**

| 场景 | 推荐模型 | 类型 |
|------|---------|------|
| 生产环境 | DeepSeek-Chat | 在线 |
| 开发环境 | Qwen-7B (Ollama) | 本地 |
| 测试环境 | DeepSeek-Chat | 在线 |

**多模型管理：**
- 配置主备模型，主模型故障时自动切换
- 不同任务使用不同模型（生成用例用大模型，简单查询用小模型）

### 2. 测试环境管理

**环境命名规范：**
- `dev` - 开发环境
- `test` - 测试环境
- `staging` - 预发布环境
- `prod` - 生产环境

**关键配置：**
- 不同环境使用不同的base_url
- 包含环境特定的认证信息
- 配置环境变量和敏感信息

### 3. 操作日志

**日志级别：**
- 所有API调用都会记录（除了心跳接口）
- 包含请求/响应详情
- 记录执行时间

**日志保留：**
- 建议保留90天
- 定期导出重要日志
- 用于安全审计

### 4. 数据备份

**备份策略：**
- 每日全量备份
- 每小时增量备份
- 备份文件保留30天

**备份位置：**
- `data/backups/` 备份文件
- 建议备份到异地存储

## 📊 系统监控

### 关键指标

1. **AI模型可用性**
   - 定期测试模型连接
   - 监控API调用成功率
   - 追踪Token使用情况

2. test环境健康度**
   - 测试各环境连通性
   - 监控环境切换频率
   - 环境配置变更审计

3. **系统性能**
   - CPU/内存/磁盘使用
   - 数据库连接池
   - API响应时间

4. **备份完整性**
   - 备份成功率
   - 备份文件大小
   - 恢复测试结果

## 🚨 故障排查

### AI模型配置问题

**无法连接模型：**

```bash
# 1. 测试配置
POST /api/system/ai-model/1/test

# 2. 检查API密钥
# 3. 检查网络连接
# 4. 检查配额限制
```

### 本地模型问题

**本地模型无法启动：**

```bash
# 检查Ollama状态
ollama list

# 启动特定模型
ollama run qwen:7b

# 检查API服务
curl http://localhost:11434/api/generate
```

### 测试环境问题

**环境切换失败：**

```bash
# 1. 确认环境配置正确
# 2. 验证base_url可访问
# 3. 检查认证信息
GET /api/system/environment/{id}
```

### 备份恢复失败

**备份文件损坏：**

```bash
# 检查备份文件
ls -lh data/backups/

# 验证备份完整性
unzip -t data/backups/backup.zip

# 重新创建备份
POST /api/system/backup
```

## 🔄 完整工作流程

```
系统启动
  ↓
配置AI模型 → 设置API密钥 → 测试连接
  ↓
配置测试环境 → 定义多个环境 → 设置默认环境
  ↓
系统运行 → 记录操作日志 → 定期备份
  ↓
监控维护 → 检查健康状态 → 处理异常
  ↓
故障恢复 → 切换模型 → 切换环境 → 恢复数据
```

## 📖 相关文档

- **完整指南**：`docs/SYSTEM_MANAGEMENT_GUIDE.md`
- **API文档**：http://localhost:8000/docs
- **安装指南**：`docs/SETUP_GUIDE.md`
- **运维手册**：`docs/OPERATIONS_GUIDE.md`

---

**版本：** v1.0.0
**更新时间：** 2026-03-23
