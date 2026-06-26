# api-rate-limiter 技能

## 概述
全局API请求频率限制器，用于管理API请求的频率，防止触发服务提供商的限流机制。

## 安装

此技能已包含所有必要文件，只需确保在 OpenClaw 系统中正确放置即可。

## 使用方法

### 应用请求延迟
```bash
api-rate-limiter apply-delay [request-type]
```

### 检查限流状态
```bash
api-rate-limiter check-status
```

### 查看当前配置
```bash
api-rate-limiter show-config
```

### 更新配置
```bash
api-rate-limiter update-config --key base_delay_ms --value 1000
```

### 重置为默认配置
```bash
api-rate-limiter reset-config
```

## 配置文件

配置文件位于 `~/.openclaw/workspace/config/api_rate_limiter_config.json`，包含以下参数：

- `base_delay_ms`: 基础延迟毫秒数
- `max_requests_per_minute`: 每分钟最大请求数
- `max_requests_per_hour`: 每小时最大请求数
- `concurrency_limit`: 并发请求数限制
- `retry_count`: 重试次数
- `cache_enabled`: 是否启用缓存
- `request_types`: 不同请求类型的延迟设置

## 请求类型

- `light`: 轻量请求 (默认延迟 300ms)
- `medium`: 中量请求 (默认延迟 600ms)
- `heavy`: 重量请求 (默认延迟 1000ms)
- `custom`: 自定义请求 (默认延迟 500ms)

## 集成

此技能可以轻松集成到其他技能中：

```bash
# 在其他脚本中使用
before_api_call() {
    api-rate-limiter apply-delay heavy
}
```