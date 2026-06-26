# 代码保护方案分析

## 问题
如何防止友商修改代码复用 auto-accounting skill

---

## 方案对比

| 方案 | 保护强度 | 实现难度 | 用户体验 | 推荐度 |
|------|----------|----------|----------|--------|
| **1. 服务端验证** | ⭐⭐⭐⭐⭐ | 中等 | 无影响 | ⭐⭐⭐⭐⭐ |
| **2. 许可证声明** | ⭐⭐ | 简单 | 无影响 | ⭐⭐ |
| **3. 代码混淆** | ⭐⭐⭐ | 中等 | 无影响 | ⭐⭐⭐ |
| **4. 核心逻辑上移** | ⭐⭐⭐⭐ | 较高 | 需联网 | ⭐⭐⭐⭐ |
| **5. 环境绑定** | ⭐⭐⭐⭐ | 中等 | 需授权 | ⭐⭐⭐⭐ |

---

## 推荐方案：服务端验证 + 环境绑定

### 方案架构

```
┌─────────────────────────────────────────────────────────────┐
│                    auto-accounting Skill                    │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  本地代码（可被复制）                                    ││
│  │  - SKILL.md（说明文档）                                 ││
│  │  - config/config.py（配置）                            ││
│  │  - scripts/accounting_parser.py（解析器）               ││
│  └─────────────────────────────────────────────────────────┘│
│                           ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  环境验证层                                            ││
│  │  - 检测运行环境是否为小艺 Claw                          ││
│  │  - 检测是否安装一日记账 APP                            ││
│  │  - 检测依赖组件是否为官方版本                          ││
│  └─────────────────────────────────────────────────────────┘│
│                           ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  核心能力（不可复制）                                   ││
│  │  - xiaoyi-image-understanding（官方API）               ││
│  │  - xiaoyi-gui-agent（官方组件）                        ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 核心思路

**1. 核心能力不可复制**
- 图像理解能力：依赖 `xiaoyi-image-understanding` API
- GUI 操作能力：依赖 `xiaoyi-gui-agent` 组件
- 这两个组件需要小艺 Claw 官方授权，友商无法复用

**2. 环境验证**
- 在 Skill 启动时验证运行环境
- 非小艺 Claw 环境直接拒绝运行

**3. 许可证保护**
- 明确声明许可证为 MIT-0（可商用但需保留声明）
- 在代码中嵌入版权声明

---

## 具体实现

### 方案 A：环境指纹验证（推荐）

在 Skill 启动时验证环境：

```python
# scripts/environment_validator.py

import os
import sys

def validate_environment():
    """验证运行环境是否为小艺 Claw"""
    
    # 1. 检测环境变量（小艺 Claw 特有）
    xiaoyi_env = os.environ.get('XIAOYI_CLAW_ENV', '')
    if not xiaoyi_env:
        return False, "非小艺 Claw 环境"
    
    # 2. 检测依赖组件版本
    try:
        import xiaoyi_image_understanding
        import xiaoyi_gui_agent
    except ImportError:
        return False, "缺少官方依赖组件"
    
    # 3. 检测 API 可用性
    # 调用小艺 API 验证授权
    
    return True, "环境验证通过"

# 在主入口调用
if __name__ == "__main__":
    valid, msg = validate_environment()
    if not valid:
        print(f"❌ {msg}")
        print("本 Skill 仅支持小艺 Claw + 一日记账 APP")
        sys.exit(1)
```

### 方案 B：API 调用签名

在调用核心 API 时加入签名验证：

```python
import hashlib
import time

def generate_signature(api_key, timestamp):
    """生成 API 调用签名"""
    sign_str = f"{api_key}:{timestamp}"
    return hashlib.sha256(sign_str.encode()).hexdigest()

def call_xiaoyi_api(image_url):
    """调用小艺图像理解 API"""
    timestamp = int(time.time())
    signature = generate_signature(API_KEY, timestamp)
    
    # API 会验证签名，非授权调用会被拒绝
    response = requests.post(
        "https://xiaoyi.api/understanding",
        headers={
            "X-Timestamp": str(timestamp),
            "X-Signature": signature
        },
        json={"image_url": image_url}
    )
    return response.json()
```

### 方案 C：核心逻辑上移

将核心逻辑移到服务端：

```
本地 Skill（可复制）
    ↓ 发送图片
服务端 API（不可复制）
    ↓ 图像理解 + 信息提取
返回结果
    ↓
本地 GUI Agent 执行
```

---

## 法律保护

### 许可证声明

在所有代码文件头部添加：

```python
"""
auto-accounting - 自动记账 Skill
Copyright (c) 2026 摇摇

本软件受著作权法保护。虽然采用 MIT-0 许可证允许商用，
但必须保留原始版权声明。

禁止：
- 移除或修改版权声明
- 声称为自己开发
- 在非授权环境使用

官方环境：小艺 Claw + 一日记账 APP
联系方式：QQ 2756077825
"""
```

### ClawHub 发布声明

在 SKILL.md 中明确：

```yaml
metadata:
  openclaw:
    restrictions:
      modifiable: false
      runtime_required: true
      app_required: true
      license: "MIT-0 (保留版权声明)"
      copyright: "Copyright (c) 2026 摇摇"
```

---

## 最终建议

**组合方案：**

1. ✅ **环境验证** - 检测是否为小艺 Claw
2. ✅ **依赖绑定** - 核心能力依赖官方组件
3. ✅ **版权声明** - 所有文件添加版权头
4. ✅ **许可证限制** - MIT-0 但禁止移除声明

**为什么友商难以复用：**

| 复用内容 | 难度 | 原因 |
|----------|------|------|
| SKILL.md 文档 | 简单 | 纯文本，可复制 |
| 解析器代码 | 简单 | Python 代码，可复制 |
| 图像理解能力 | ❌ 不可能 | 依赖小艺官方 API |
| GUI 操作能力 | ❌ 不可能 | 依赖小艺官方组件 |
| 完整功能 | ❌ 不可能 | 核心能力无法复制 |

**结论：即使友商复制了代码，也无法复用核心功能，因为核心能力（图像理解、GUI操作）依赖小艺 Claw 官方组件。**

---

_分析完成于 2026-04-02_
