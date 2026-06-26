---
name: 1688-distribution-procurement-newton
description: 分销采购助手。当用户需要下游出单后自动完成采购、库存同步、价格监控的全链路管理时使用此技能。
metadata: {"openclaw": {"emoji": "📦", "requires": {"bins": ["python3"]}, "primaryEnv": "ALI_1688_AK"}}
---

# 分销采购助手

## 背景说明

AK（Access Key）通过clawhub获取，通过命令(`python3 scripts/capabilities/configure/cmd.py <提取到的AK>`)来设置 ALI_1688_AK。AK 已绑定用户身份，无需任何额外的身份参数。

## 功能概述

- ✅ **店铺绑定** - 绑店状态查询、绑店引导
- ✅ **关联货源** - 将下游商品**直接关联/替换到指定的**1688商品（需已知目标货源ID，不走筛选）
- ✅ **供应链** - 自动换供（三层流水线：场景层→**同款筛选层**→货源替换层；自动找替代货源后执行替换）
- ✅ **订单管理** - 自动跟单、采购下单、订单查询、旺旺催发
- ✅ **ISV 采购能力** - 通过内置 ISV Provider（张飞搬家，appKey=9018264）支持淘宝和抖音双平台的自动下单、售后、关联货源

## 前置检查：确认 AK 已配置

**skill 触发前，第一步必须立即检查 AK，不得先执行任何接口调用。** 运行以下命令：

```bash
python3 scripts/capabilities/configure/cmd.py
```

- **显示 "✅ AK 已配置"**：直接进入后续步骤，不要向用户提及此检查。
- **显示 "❌ 尚未配置 AK"**：输出下方 **AK 引导话术**，然后**停止，等待用户回复，不要做任何其他操作**。
  - 用户回复后，从消息中提取 AK 字符串，执行：
    ```bash
    python3 scripts/capabilities/configure/cmd.py <提取到的AK>
    ```
  - 配置完成后，直接继续执行用户最初的需求，无需额外说明。

### AK 引导话术

``` text
需要先配置 AK，获取方式：
打开 [clawhub.1688.com](https://clawhub.1688.com) 点击右上角**钥匙🔑图标**获取 AK
获取后告诉我：「我的AK是 xxxxxx」
```

## ISV Token（调用外部 ISV skill 时使用）

### 什么时候需要获取 ISV Token？

当业务需要调用 **ISV（独立软件开发商）提供的外部 skill** 进行通信时，必须先获取对应的 ISV Token 作为身份凭证。例如：调用第三方 ISV 的接口服务时，需要携带该 token 进行鉴权。

如果只调用 1688 内部接口（通过 `api_post`），则**不需要** ISV Token。

### 如何获取 ISV Token

通过 `cli.py` 调用：

```bash
# 获取 token（自动缓存，24小时有效，未过期时直接返回本地缓存）
python3 scripts/cli.py isv_token fetch --app_key=你的AppKey

# 强制刷新 token（忽略本地缓存）
python3 scripts/cli.py isv_token fetch --app_key=你的AppKey --force_refresh=true

# 检查 token 状态
python3 scripts/cli.py isv_token status --app_key=你的AppKey
```

在 service.py 中直接调用：

```python
from scripts.biz.isv_token.service import fetch_isv_token, check_token_status

token = fetch_isv_token(app_key="你的AppKey")
status = check_token_status(app_key="你的AppKey")
# 返回：{"exists": bool, "expired": bool, "token": str, "remainingHours": float}
```

### Token 缓存机制

- Token 保存在 `~/.isv_tokens.json`，按 appKey 索引，**多个 skill 共享同一份缓存**
- 默认有效期 24 小时，过期后自动重新获取
- 也支持通过环境变量 `ISV_TOKEN_<APPKEY>` 注入（视为永不过期）

---

## 使用流程

### 步骤 1：调用接口

通过 `cli.py` 统一入口调用业务接口：

```bash
# 基础调用
python3 scripts/cli.py <业务域> <动作> [--参数名=参数值]

# 店铺绑定
python3 scripts/cli.py shop_bind_helper query  # 查询绑定的店铺和工具信息
python3 scripts/cli.py shop_bind_helper app_keys  # 查询 ISV AppKey 信息

# ISV Token（用于调用外部 ISV skill）
python3 scripts/cli.py isv_token fetch --app_key=YOUR_APP_KEY
python3 scripts/cli.py isv_token status --app_key=YOUR_APP_KEY

# ISV Skill 调用
python3 scripts/cli.py isv_skill_helper find_skill --app_key=9018264
python3 scripts/cli.py isv_skill_helper find_skill --skill_name=zhangfei
python3 scripts/cli.py isv_skill_helper list_builtin
python3 scripts/cli.py isv_skill_helper link_supply \
  --skill_path=/path/to/skill --token=xxx \
  --shop_id=123 --shop_nick=店铺名 --local_item_id=456 \
  --source_offer_url=https://detail.1688.com/offer/xxx.html \
  --purchase_account=采购账号 --platform=taobao

# 关联货源（直接关联到指定货源，不走筛选）
python3 scripts/cli.py link_supply_helper link_supply --downstream_item_id=xxx --offer_id=xxx --isv_app_key=xxx --platform=douyin
python3 scripts/cli.py link_supply_helper link_supply --downstream_item_id=xxx --downstream_sku_id=xxx --offer_id=xxx --sku_id=xxx --isv_app_key=xxx --platform=taobao

# 供应链（自动换供 = 自动筛选同款 + 图搜fallback + 执行替换）
python3 scripts/cli.py supply_chain_helper auto_switch_supply --offer_ids=688001234,688005678 --downstream_item_id=xxx
python3 scripts/cli.py supply_chain_helper auto_switch_supply --offer_ids=688001234 --downstream_item_id=xxx --reason=亏损换供
python3 scripts/cli.py supply_chain_helper auto_switch_supply --offer_ids=688001234 --offer_image_url=https://xxx.jpg

# ISV 下游关联货源
python3 scripts/cli.py supply_chain_helper downstream_link \
  --app_key=9018264 --shop_id=12345 --shop_nick=店铺名 \
  --local_item_id=67890 --source_offer_url=https://detail.1688.com/offer/xxx.html \
  --purchase_account=采购账号 --platform=taobao

# 订单查询
python3 scripts/cli.py order_helper query
python3 scripts/cli.py order_helper query --order_id=xxx
python3 scripts/cli.py order_helper query --order_status=waitbuyerreceive

# 旺旺消息
python3 scripts/cli.py order_helper send --question="请尽快发货" --order_ids=xxx
python3 scripts/cli.py order_helper query_reply --task_id=xxx
python3 scripts/cli.py order_helper urge
python3 scripts/cli.py order_helper urge --template=urgent
```

### 步骤 2：处理返回结果

所有命令统一输出 JSON：

```json
{
  "success": true,
  "markdown": "✅ 调用成功",
  "data": { ... }
}
```

- `success=true`：直接使用 `markdown` 展示给用户，`data` 包含结构化数据
- `success=false`：`markdown` 包含错误描述

## 错误处理

常见错误及处理：

| 错误信息 | 原因 | 处理方式 |
|---------|------|----------|
| AK 未配置 | 未设置环境变量 ALI_1688_AK | 执行 AK 配置流程 |
| 参数错误 | 传入的参数不正确 | 检查参数格式 |
| 网络异常 | 接口调用失败 | 稍后重试 |

## 依赖包

```bash
pip install requests
```

## ISV Provider 架构

项目采用可插拔的 ISV Provider 架构（与 `1688-distribution-distribute-offer-newton` 目录分级一致），ISV 统一在 `scripts/isv/` 下管理：

```
scripts/isv/
├── base.py                         # ISV Provider 基类 + 全局注册表
└── providers/
    ├── zhangfei/                    # 张飞搬家（appKey=9018264）
    │   ├── provider.py              # Provider 注册
    │   ├── cli.py                   # CLI 入口（淘宝+抖音）
    │   ├── SKILL.md                 # ISV 业务流程文档
    │   └── scripts/
    │       ├── _api.py              # 中台鉴权
    │       └── procurement.py       # 业务逻辑
    └── <future_isv>/                # 后续新增 ISV
```

新增 ISV：在 `scripts/isv/providers/` 下创建目录，实现 `provider.py` 并注册即可。

## 项目结构

```
1688-distribution-procurement-newton/
├── SKILL.md                     # 技能说明文档（本文档）
├── README.md                    # 项目说明文档
├── examples/                    # 示例代码目录
│   ├── check_env.py            # 环境检查
│   ├── check_ak_exist.py       # 检查 AK 配置
│   └── set_ak.py               # 设置 AK
└── scripts/
    ├── cli.py                   # ⭐ 统一命令行入口
    ├── _sys/                    # 系统模块（不要修改）
    │   ├── _http.py             # HTTP 客户端
    │   ├── _auth.py             # 签名认证
    │   ├── _errors.py           # 错误类型
    │   ├── _const.py            # 全局常量
    │   ├── _output.py           # 输出格式化
    │   └── _skill_discovery.py  # ISV Skill 发现
    ├── capabilities/configure/  # AK 配置能力（不要修改）
    ├── isv/                     # ⭐ ISV Provider 架构
    │   ├── base.py              # Provider 基类 + 注册表
    │   └── providers/           # 各 ISV 实现
    │       └── zhangfei/        # 张飞搬家（appKey=9018264）
    └── biz/                     # ⭐ 业务逻辑（按业务域拆分）
        ├── const.py             # 业务常量配置（可修改）
        ├── isv_token/           # ISV Token 管理
        ├── isv_skill_helper/    # ISV Skill 调用助手
        ├── shop_bind_helper/    # 店铺绑定助手
        ├── link_supply_helper/  # 关联货源助手
        ├── supply_chain_helper/ # 供应链助手
        └── order_helper/        # 订单助手
```

## 语言要求

**⚠️ 重要：本技能的所有输出、提示、消息必须使用中文！**
