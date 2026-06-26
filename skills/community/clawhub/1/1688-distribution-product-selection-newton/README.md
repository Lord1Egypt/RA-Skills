# 1688-distribution-product-selection

1688 分销选品助手 - 分析市场趋势、竞品数据和利润空间，帮助分销商选择优质商品

## 快速开始

> 温馨提示：AK 鉴权逻辑已封装好，只需在 `scripts/biz/` 下按业务域创建文件夹实现业务逻辑，并修改 `SKILL.md` 描述技能功能即可。

### 0. 环境检查

```bash
python3 examples/check_env.py
```

检查 Python 版本及依赖，缺少时自动安装。

### 1. AK 测试

AK 用于身份认证，userId 由 AK 自动解析，无需手动传入。

```bash
# 检查 AK 是否已配置
python3 examples/check_ak_exist.py

# 设置 AK（首次使用）
python3 examples/set_ak.py
```

- 获取 AK：打开 https://clawhub.1688.com 点击右上角钥匙🔑图标
- 查看已配置的 AK：`~/.openclaw/openclaw.json`

### 2. 实现业务类

在 `scripts/biz/` 下创建业务域文件夹（如 `market_product/`），包含 `service.py` 和 `cmd.py`：

```python
# scripts/biz/market_product/service.py
import sys, os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post

def get_official_product_list(category_id: str = None) -> dict:
    body = {}
    if category_id:
        body["categoryId"] = category_id
    return api_post(tool_name="fx_market_product_get_official_product_list", body=body)
```

通过 `cli.py` 调用：

```bash
python3 scripts/cli.py market_product get_official_product_list --categoryId=123
```

## 项目结构

```
1688-distribution-product-selection/
├── SKILL.md                     # Skill 文档（Agent 使用）
├── README.md                    # 项目说明（开发者阅读）
├── TEST_REPORT.md               # 测试报告（必须 100% 通过）
├── examples/
│   ├── check_env.py            # 环境检查
│   ├── check_ak_exist.py       # 检查 AK 配置
│   ├── set_ak.py               # 设置 AK
│   └── xxx.py                  # 业务测试（需创建）
└── scripts/
    ├── __init__.py
    ├── cli.py                  # 统一命令行入口
    ├── _sys/                   # 系统模块
    │   ├── _http.py            # HTTP 客户端
    │   ├── _auth.py            # 签名认证
    │   ├── _errors.py          # 错误类型
    │   ├── _const.py           # 常量定义
    │   └── _output.py          # 输出工具
    ├── capabilities/
    │   └── configure/          # AK 配置能力
    └── biz/
        ├── __init__.py
        ├── const.py            # 业务常量配置（可修改）
        ├── isv_token/          # ISV Token 管理
        │   ├── cmd.py          # token 命令层
        │   ├── service.py      # token 获取服务
        │   └── token_store.py  # token 本地缓存
        └── product_selection/  # 选品业务域（需实现）
            ├── cmd.py          # 命令定义
            └── service.py      # 业务逻辑
```

## 文件说明

| 文件 | 作用 | 是否修改 |
|------|------|----------|
| `SKILL.md` | Agent 调用入口，描述技能功能和使用方式 | ✅ 必须修改 |
| `README.md` | 项目说明文档 | ✅ 按需修改 |
| `scripts/cli.py` | 统一命令行入口 | ❌ 不修改 |
| `scripts/biz/const.py` | 业务常量配置（如 BASE_URL） | ✅ 可修改 |
| `scripts/biz/*/cmd.py` | 业务命令定义 | ✅ 必须实现 |
| `scripts/biz/*/service.py` | 业务逻辑实现 | ✅ 必须实现 |
| `examples/*.py` | 测试和示例代码 | ✅ 按需添加 |
| `scripts/_sys/*` | 系统模块（HTTP/签名/错误/输出） | ❌ 不修改 |
| `scripts/capabilities/` | AK 配置等通用能力 | ❌ 不修改 |
| `scripts/biz/isv_token/` | ISV Token 获取与缓存 | ❌ 不修改 |

## 开发指南

### 1. 配置常量

修改 `scripts/biz/const.py` 中的配置：

```python
BASE_URL = "https://skills-gateway.1688.com"
```

### 2. 实现业务模块

在 `scripts/biz/` 下创建业务域文件夹（如 `market_product/`）：

**service.py**（业务逻辑）：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post


def your_function(param1: str, param2: str = None) -> dict:
    """
    你的业务函数

    参数：
        param1: 参数说明

    返回：
        api_post 解包后的业务数据（dict）
    异常：
        AuthError / ParamError / ServiceError 等（由 _http.py 统一抛出）
    """
    body = {"param1": param1}
    if param2:
        body["param2"] = param2
    # tool_name 为源舟平台注册的工具 code
    # 注册地址：https://pre-1688bot.alibaba-inc.com/#/tool/list
    return api_post(tool_name="fx_your_api_name", body=body)
```

**cmd.py**（命令定义）：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._output import print_output, print_error
from scripts.biz.your_domain.service import your_function as _your_function


def your_function(param1: str = ""):
    """执行业务并输出标准 JSON"""
    try:
        if not param1:
            print_output(False, "❌ 缺少必填参数 param1", {})
            return
        result = _your_function(param1=param1)
        print_output(True, "✅ 调用成功", result)
    except Exception as e:
        print_error(e)
```

### 3. 测试业务

通过 `cli.py` 测试：

```bash
python3 scripts/cli.py your_domain your_function --param1=test
```

### 4. 更新 SKILL.md

修改 `SKILL.md` 中的：
- `name`: 你的 skill 名称
- `description`: 功能描述
- 使用流程和示例代码

## API 调用

```python
from scripts._sys._http import api_post

result = api_post(
    tool_name="fx_your_api",  # API 名称
    body={"key": "value"}     # 请求参数
)
```

自动处理：HMAC-SHA256 签名、网络重试（3 次）、错误映射、响应解包

## 注意事项

1. **AK 配置**：所有 API 依赖环境变量 `ALI_1688_AK`
2. **userId 无需传入**：AK 经网关自动转换为 userId，业务代码无需关心用户身份
3. **返回格式**：统一返回 `{"success": bool, "markdown": str, "data": dict}`
4. **Tool 注册**：https://pre-1688bot.alibaba-inc.com/#/tool/list?page=1
5. **中文输出**：所有提示信息使用中文
6. **模块导入**：使用 `from scripts._sys.xxx import` 或 `from scripts.biz.xxx import` 格式
7. **业务域拆分**：每个业务域独立文件夹，包含 `cmd.py` + `service.py`
