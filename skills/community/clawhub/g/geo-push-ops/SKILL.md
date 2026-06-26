# geo-push-ops

推送操作技能。负责飞书消息的构建、发送、重试和投递诊断。

## 功能

- **消息模板**: 分层消息模板（高优先级警报 / 观察推送 / 摘要）
- **飞书发送**: 带重试机制的飞书 webhook 推送
- **频率限制处理**: 自动检测 11232 频率限制错误，递增延迟重试
- **投递诊断**: 详细记录 HTTP 状态、业务码、错误信息
- **死信补投**: 失败消息加入死信队列，支持后续补投

## 飞书配置

```python
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
FEISHU_RETRY_DELAY = 5      # 重试延迟（秒）
FEISHU_MAX_RETRIES = 3      # 最大重试次数
```

## 消息模板

### 高优先级警报（A 类）

```
🚨 宏观地缘高优先级 | 15:00

【事件】
伊朗总统：伊朗将继续进行正当防御

【判断】
偏利多原油、避险升温

【映射】
石油石化 / 国防军工 / 有色金属

【说明】
当前为突发阶段，若后续出现官方确认或进一步升级，影响可能继续扩大。

---
📡 数据源：财联社
🧠 AI 语义分析：已启用
```

### 观察推送（B/C 类）

```
🦾 宏观地缘观察 | 15:00

📰 最新动态
🔥 俄外长称美谋求掌控全球能源市场
⚠️ 黎巴嫩将就以色列军事行动向安理会申诉
○ 伊朗总统：伊朗将继续进行正当防御

📊 市场异动
📈 原油：+2.5%
📈 黄金：+1.8%

---
💡 当前为观察阶段，如有重大升级将单独推送
```

## 使用方法

### Python API

```python
from geo_push_ops import (
    send_to_feishu,
    build_feishu_message,
    DeliveryResult,
    FeishuConfig,
)

# 配置
config = FeishuConfig(
    webhook="https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
    retry_delay=5,
    max_retries=3,
)

# 构建消息
from geo_event_router import Event

events = [event1, event2, event3]
message = build_feishu_message(events, market)

# 发送
result = send_to_feishu(message, config)

if result.delivered:
    print(f"✅ 推送成功（{result.attempts}次尝试，{result.duration_ms}ms）")
else:
    print(f"❌ 推送失败：{result.error} (HTTP {result.http_status})")
```

### DeliveryResult 结构

```python
@dataclass
class DeliveryResult:
    target: str = "feishu"
    attempts: int = 0         # 尝试次数
    http_status: int = 0      # HTTP 状态码
    biz_code: int = 0         # 飞书业务码
    biz_msg: str = ""         # 业务消息
    delivered: bool = False   # 是否成功
    error: str = ""           # 错误信息
    duration_ms: int = 0      # 耗时（毫秒）
```

## 重试策略

| 尝试次数 | 延迟时间 | 说明 |
|:---:|:---:|:---|
| 1 | 0s | 首次尝试 |
| 2 | 5s | 第一次重试 |
| 3 | 10s | 第二次重试 |

检测到频率限制错误码 11232 时，使用递增延迟重试。

## 错误处理

| 错误类型 | HTTP 码 | 业务码 | 处理方式 |
|:---|:---:|:---:|:---|
| 成功 | 200 | 0 | 返回成功 |
| 频率限制 | 200 | 11232 | 递增延迟重试 |
| Webhook 无效 | 200 | 99991504 | 记录错误，不重试 |
| 网络错误 | - | - | 记录错误，加入死信队列 |

## 依赖

- `requests`: HTTP 请求库
- `geo_event_router`: 事件数据结构（可选）
- `geo_market_impact_mapper`: 市场数据（可选）

## 相关文件

- 主模块：`geo_push_ops.py`

## 版本

- **v1.0.0**: 初始版本，从 smart-geo-push.py v2.0 拆分
