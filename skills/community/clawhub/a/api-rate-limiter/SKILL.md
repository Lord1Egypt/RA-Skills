# API Rate Limiter

## 概述
全局API请求频率限制器，用于管理API请求的频率，防止触发服务提供商的限流机制。

## 功能特性

### 1. 请求频率控制
- 智能延迟管理
- 并发请求限制
- 时间窗口限流

### 2. 配置管理
- 动态配置加载
- 策略调整
- 状态监控

### 3. 服务集成
- 全局API请求拦截
- 自动限流应用
- 失败重试机制

## 使用方法

### 应用请求延迟
```
api-rate-limiter apply-delay [request-type]
```

### 检查限流状态
```
api-rate-limiter check-status
```

### 查看当前配置
```
api-rate-limiter show-config
```

### 更新配置
```
api-rate-limiter update-config --key value
```

## 支持的请求类型
- light: 轻量请求 (默认延迟 300ms)
- medium: 中量请求 (默认延迟 600ms) 
- heavy: 重量请求 (默认延迟 1000ms)
- custom: 自定义延迟

## 配置项
- base_delay_ms: 基础延迟毫秒数
- max_requests_per_minute: 每分钟最大请求数
- max_requests_per_hour: 每小时最大请求数
- concurrency_limit: 并发请求数限制
- retry_count: 重试次数
- cache_enabled: 是否启用缓存