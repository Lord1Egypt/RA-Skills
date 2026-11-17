# 重试策略说明

## 指数退避（Exponential Backoff）

当遇到临时错误（TRANSIENT）时，采用指数退避策略进行重试。

### 基本参数

| 参数 | 值 | 说明 |
|------|-----|------|
| BASE_DELAY | 1s | 基础延迟 |
| MAX_RETRIES | 3 | 最大重试次数 |
| 退避公式 | BASE_DELAY × 2^attempt | attempt 从 0 开始 |

### 退避时间线

```
操作失败 → 等待 1s → 第1次重试
         → 等待 2s → 第2次重试
         → 等待 4s → 第3次重试
         → 仍然失败 → 报告用户
```

总等待时间：1 + 2 + 4 = 7 秒

### 为什么选择指数退避

1. **给服务端恢复时间**：临时错误（如限流、服务不可用）通常需要几秒恢复
2. **避免雪崩效应**：固定间隔重试可能加剧服务端压力
3. **平衡速度与耐心**：3 次重试、总计 7 秒等待，既不会太慢也不会放弃太早

### 适用场景

| 错误类型 | 是否重试 | 原因 |
|----------|----------|------|
| timeout / 连接超时 | ✅ 重试 | 网络波动，稍后可能恢复 |
| 429 / 限流 | ✅ 重试 | 等待配额恢复 |
| 503 / 服务不可用 | ✅ 重试 | 服务重启中 |
| connection reset | ✅ 重试 | 临时网络问题 |
| 403 / 权限不足 | ❌ 不重试 | 权限不会自动恢复 |
| 404 / 资源不存在 | ❌ 不重试 | 资源不会凭空出现 |
| syntax error | ❌ 不重试 | 需要修改代码 |
| token limit | ❌ 不重试 | 需要压缩上下文 |

### 扩展：自定义退避参数

```python
class CustomClassifier(ErrorClassifier):
    BASE_DELAY = 2      # 更保守的基础延迟
    MAX_RETRIES = 5     # 更多重试次数
```

### 扩展：抖动（Jitter）

在高并发场景下，可添加随机抖动避免多个客户端同步重试：

```python
import random

def get_retry_delay_with_jitter(self, attempt: int) -> float:
    base = self.get_retry_delay(attempt)
    jitter = random.uniform(0, base * 0.5)
    return base + jitter
```
