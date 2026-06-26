---
name: clawhub-retry-fallback
description: ClawHub平台工具调用失败自动重试与降级处理Skill | Automatic retry and fallback handling for ClawHub Agent task failures
---

# ClawHub Retry & Fallback Skill

为ClawHub平台Agent任务提供完整的容错兜底机制，实现「异常可感知、失败可重试、无招可兜底」的闭环。

## 核心功能

| 功能模块 | 说明 | PRD对应 |
|---------|------|---------|
| **全局重试策略配置中心** | 支持指数退避、固定间隔、自定义间隔策略 | 4.1节 |
| **异常类型智能识别引擎** | 自动区分可重试/不可重试异常 | 4.2节 |
| **备用工具自动切换** | 智能匹配备用工具池，自动参数映射 | 4.3节 |
| **三级降级处理机制** | 轻度/中度/重度降级策略 | 4.4节 |
| **全流程执行日志** | 支持导出Excel/PDF，满足审计要求 | 4.5节 |

## 快速开始

```python
from scripts.retry_handler import RetryHandler

handler = RetryHandler()

@handler.with_retry(max_attempts=3, backoff_strategy='exponential')
def my_api_call():
    # 你的API调用
    return requests.get('https://api.example.com/data')

# 自动重试执行
result = my_api_call()
```

## 安装

```bash
pip install -r requirements.txt
```

## 项目结构

```
clawhub-retry-fallback/
├── SKILL.md                 # Skill说明文档
├── README.md                # 完整文档 (API参考+9个示例)
├── requirements.txt         # 依赖列表
├── config/
│   └── retry_policies.yaml  # 重试策略配置
├── scripts/                 # 6个核心模块
│   ├── retry_handler.py     # 重试处理器
│   ├── exception_classifier.py  # 异常分类器
│   ├── fallback_manager.py  # 备用工具管理器
│   ├── degradation_handler.py   # 降级处理器
│   ├── audit_logger.py      # 审计日志
│   └── config_manager.py    # 配置管理器
├── examples/
│   └── basic_usage.py       # 9个使用示例
└── tests/
    └── test_retry_handler.py    # 22个单元测试
```

## 运行测试

```bash
cd tests
python test_retry_handler.py

# 预期输出:
# Ran 22 tests in X.XXXs
# OK
```

## 运行示例

```bash
cd examples
python basic_usage.py

# 输出9个完整示例
```

## 详细文档

请参考 `README.md` 获取：
- 完整API参考文档
- 9个渐进式使用示例
- 配置文件说明
- 异常分类规则库
- 高级用法指南