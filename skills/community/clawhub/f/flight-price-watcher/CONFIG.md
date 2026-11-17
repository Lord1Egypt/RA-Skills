# 配置说明

## 环境变量

### DINGTALK_TARGET_ID

**说明**: 钉钉消息接收者 ID

**默认值**: `395111`

**是否必填**: 否

**示例**:
```bash
# 在 .env 文件中配置
DINGTALK_TARGET_ID=395111
```

或在 OpenClaw 配置中设置：
```yaml
skills:
  flight-price-watcher:
    env:
      DINGTALK_TARGET_ID: "你的钉钉用户 ID"
```

## 外部依赖

### FlyAI CLI

**安装命令**:
```bash
npm i @fly-ai/flyai-cli
```

**说明**: 飞猪旅行官方 CLI 工具，用于查询机票价格

**使用权限**:
- `flyai search-flight` - 查询航班价格
- `flyai --help` - 验证安装

## 使用权限

本技能需要以下权限：

| 权限 | 用途 | 说明 |
|------|------|------|
| **消息推送** | 发送降价提醒 | 通过钉钉发送通知 |
| **文件读写** | 存储任务数据 | 读写 `data/tasks.json` |
| **外部命令** | 查询机票价格 | 调用 FlyAI CLI |

## 安全说明

- ✅ 所有外部命令已声明
- ✅ 消息目标通过环境变量配置
- ✅ 本地数据存储在 `data/` 目录
- ✅ 无网络请求（除 CLI 调用外）
- ✅ 无敏感信息硬编码

## 隐私保护

- 用户 ID 通过环境变量配置，不硬编码
- 监控数据本地存储，不上传
- 购票链接来自 FlyAI 官方返回
