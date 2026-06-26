---
name: "clawtip-paid-skill-guide"
description: >
  ClawTip付费技能创建完整指南 - 包含正确的订单创建、SM4加密、本地测试方法。 based on official developer guide at https://clawtip.jd.com/guide
metadata:
  author: "user-customized"
  category: "openclaw"
  capabilities:
    - "payment.process"
  permissions:
    - "network.outbound"
    - "credential.read"
---

# ClawTip 付费技能创建完整指南

## 核心原则（来自官方开发者指南）

> Skills 负责描述业务意图、发起支付与流程编排（创建订单、发起收款、提供服务）
> ClawTip 全权负责钱包管理、支付执行、提供凭证等底层操作
> Skills 不得干预支付执行方式，不得要求用户创建钱包、输入敏感资产信息

## 技能目录结构

```
skill-name/
├── SKILL.md                    # 技能定义文件
├── configs/
│   └── config.json             # 配置文件（收款信息）
└── scripts/
    ├── create_order.py         # 创建订单脚本
    ├── file_utils.py           # 文件工具模块
    └── xxx_generate.py         # 服务生成脚本
```

## 配置文件格式 (configs/config.json)

```json
{
  "payTo": "你的商户ID",
  "sm4Key": "你的安全密钥",
  "amount": 1,
  "skillName": "技能slug名称",
  "description": "服务描述"
}
```

## 关键实现要点

### 1. file_utils.py - 订单目录必须用这个路径

```python
import platform

def get_orders_dir():
    home_dir = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home_dir, "openclaw", "skills", "orders")
    else:
        return os.path.join(home_dir, ".openclaw", "skills", "orders")
```

**注意：不能用 `/root/...`，macOS上会报只读错误！**

### 2. create_order.py - 本地创建订单 + SM4加密

**重要：不要调用外部API（如CREATE_ORDER_URL）！本地创建即可。**

```python
import sys
import json
import hashlib
import os
import uuid
from datetime import datetime

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()

def generate_order_no() -> str:
    return f"CL{int(datetime.now().timestamp() * 1000)}{uuid.uuid4().hex[:6]}"

def sm4_encrypt(data: str, key: str) -> str:
    """SM4加密"""
    key_bytes = key.encode('utf-8')[:16].ljust(16, b'0')
    iv = b'5f5e5a247f544d77'
    
    data_bytes = data.encode('utf-8')
    padding_length = 16 - len(data_bytes) % 16
    data_bytes += bytes([padding_length] * padding_length)
    
    cipher = Cipher(algorithms.SM4(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data_bytes) + encryptor.finalize()
    
    return base64.b64encode(encrypted).decode('utf-8')

def create_order(question: str, skill_name: str, pay_to: str, amount: int, description: str, sm4_key: str) -> dict:
    order_no = generate_order_no()
    
    # 构建需要加密的数据（注意是JSON字符串）
    data_to_encrypt = {
        "orderNo": order_no,
        "amount": str(amount),
        "payTo": pay_to
    }
    json_str = json.dumps(data_to_encrypt)
    
    # SM4加密
    encrypted_data = sm4_encrypt(json_str, sm4_key)
    
    return {
        "order_no": order_no,
        "amount": amount,
        "question": question,
        "encrypted_data": encrypted_data,
        "pay_to": pay_to,
        "description": description,
        "skill_name": skill_name
    }
```

### 3. 订单文件必须包含的字段

```python
order_info = {
    "skill-id": f"si-{skill_name}",
    "order_no": order_no,
    "amount": amount,
    "question": question,
    "encrypted_data": encrypted_data,  # SM4加密后的JSON
    "pay_to": pay_to,
    "description": description,
    "slug": skill_name,
    "resource_url": "local",  # 使用本地
}
```

### 4. 支付参数说明（来自官方指南）

encryptedData: 用SM4加密的json串，如：
```json
{"orderNo":"交易单号","amount":"金额（分）","payTo":"收款钱包地址"}
```

## 本地测试流程（真实支付）

### 完整步骤：

```bash
# 第1步：创建订单（本地，SM4加密）
cd ~/.hermes/skills/openclaw-imports/你的技能目录
python3 scripts/create_order.py "服务描述"

# 输出示例：
# ORDER_NO=CL1776337909997f8c6da
# AMOUNT=1
# QUESTION=测试
# INDICATOR=ea30c590466d2b0313e13d380db7b8ef

# 第2步：真实支付（调用clawtip技能）
python3 ~/.hermes/skills/openclaw-imports/clawtip/scripts/payment_process.py "订单号" "indicator" "1.0.8"

# 第3步：生成服务
python3 scripts/xxx_generate.py "订单号"
```

### 验证支付是否成功

检查订单文件是否包含 `payCredential` 字段：

```bash
cat ~/.openclaw/skills/orders/<indicator>/<订单号>.json
```

**注意：支付返回"商家信息有误"是正常的，只要订单文件中有payCredential就说明支付成功了！**

## 常见问题

### Q: 支付返回 "商家信息有误"
A: 这是正常的，只要订单文件中有 payCredential 字段就说明支付成功了

### Q: 报 OSError: [Errno 30] Read-only file system
A: 订单目录路径错误，必须用 `~/.openclaw/skills/orders/`

### Q: SM4加密失败
A: 确保安装了 cryptography 库：`pip install cryptography`

### Q: 本地测试想要真实支付
A: 使用 payment_process.py 脚本，不要手动模拟 payCredential

## 经验总结

1. **不要调用外部API**: 不要调用 CREATE_ORDER_URL，本地创建订单
2. **订单目录**: 必须是 `~/.openclaw/skills/orders/`，不能用 `/root/`
3. **参数解析**: 必须用 argparse
4. **SM4加密**: 使用 cryptography 库，sm4Key 从配置文件读取
5. **slug字段**: 订单文件必须包含slug
6. **resource_url**: 设置为 "local"
7. **"商家信息有误"**: 正常现象，支付可能已成功
