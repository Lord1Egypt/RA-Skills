---
name: dahua-cloud-open-iot-basic-general-kit
description: 大华云开放平台IoT设备管理统一客户端，支持摄像头、NVR、DVR等设备的完整生命周期管理。提供设备添加/删除/查询、国标GB28181设备接入、SD卡管理、WiFi配置、消息订阅回调、铃音管理、图片解密等43个API接口。适用于大华云IoT平台设备接入、监控系统集成、智能安防项目开发。使用场景：如何管理大华云设备、批量查询设备状态、获取设备在线状态、配置设备回调消息、国标设备接入平台、摄像头SD卡格式化、修改设备WiFi连接、设备图片解密、IoT设备运维管理。单文件Python实现，支持命令行CLI和SDK调用，自动Token刷新，零冗余配置。
metadata: {"openclaw":{"requires":{"env":["DAHUA_CLOUD_PRODUCT_ID","DAHUA_CLOUD_AK","DAHUA_CLOUD_SK"]},"primaryEnv":"DAHUA_CLOUD_SK","install":[{"id":"requests","kind":"python","package":"requests","label":"Install Python requests"},{"id":"pycryptodome","kind":"python","package":"pycryptodome","label":"Install Python pycryptodome"}]}}
type: executable
paths:
  - scripts/
dependencies:
  - requests
  - pycryptodome
---

# 大华云开放平台 - 基础通用套件

## 概述

本技能提供**大华云开放平台基础通用套件**的统一客户端实现，采用单文件设计：

- ✅ **统一客户端** - 封装所有设备管理API
- ✅ **零冗余配置** - 仅需 Cloud 凭证（ProductId、AK、SK）即可
- ✅ **单文件实现** - 易于维护和部署
- ✅ **环境变量支持** - 支持GUI/命令行配置
- ✅ **命令行工具** - 快速操作无需编写代码
- ✅ **Python SDK** - 可集成到其他应用
- ✅ **自动Token管理** - Token自动刷新，无需手动处理

---

## 完整功能

共 **43 个接口** 全部支持，详见 [API_COVERAGE.md](./API_COVERAGE.md)。

### 1. 设备管理
- 添加设备 `add_device()` / `add`
- 校验设备密码 `verify_device_password()` / `verify`
- 删除设备 `delete_device()` / `delete`
- 查询设备列表 `get_device_list()` / `list`
- 查询设备在线状态 `get_device_online()` / `online`
- 批量查询设备详细信息 `list_device_details()` / `details`
- 查询设备绑定状态 `check_device_bind()` / `bind`
- 查询设备品类 `get_category()` / `category`
- 获取设备通道信息 `get_device_channel_info()` / `channels`
- 修改设备/通道名称 `modify_device_name()`
- 修改设备密码 `modify_dev_code()`

### 2. 国标设备
- 获取国标设备注册信息 `get_sip_info()` / `sip-info`
- 获取国标码列表 `list_gb_code()` / `gb-code`
- 添加国标设备 `add_gb_device()` / `add-gb`
- 修改国标设备信息 `modify_gb_device()` / `modify-gb`
- 国标设备查询详细信息 `list_gb_device_details()` / `gb-details`

### 3. SD卡管理
- 查询SD卡状态 `get_sd_card_status()`
- 查询SD卡容量 `get_sd_card_storage()`
- 获取SD卡列表 `list_sd_card_storage()`
- 格式化SD卡 `format_sd_card()`

### 4. 设备配置
- 获取设备使能开关状态 `get_ability_status()` / `ability`
- 设置设备使能开关 `set_ability_status()`
- 设备校时 `set_current_utc()`

### 5. 铃音管理
- 获取铃声列表 `list_custom_ring()`
- 新增自定义铃声 `add_custom_ring()`
- 删除自定义铃声 `delete_custom_ring()`
- 设置铃声 `set_custom_ring()`

### 6. WiFi 管理
- 获取设备当前连接的热点信息 `current_device_wifi()`
- 获取设备周边热点信息 `wifi_around()`
- 修改设备连接热点 `control_device_wifi()`

### 7. 其他设备能力
- 获取 SIM 信号强度 `get_sim_signal_strength()`
- 图片解密 `image_decrypt()`

### 8. 消息订阅
- 添加回调配置 `add_callback_config()`
- 按设备ID列表订阅消息 `message_subscribe()`
- 分页获取回调配置 `get_all_callback_config()`
- 根据回调配置ID更新设备订阅 `update_subscribe_by_callback_config()`
- 根据回调配置ID更新回调配置 `update_callback_config()`
- 删除回调配置及相关订阅 `delete_callback_config()`
- 根据回调配置ID搜索回调配置信息 `get_callback_config_info()`
- 根据回调配置ID搜索已订阅的设备消息 `get_subscribe_info_by_callback_config()`
- 根据设备ID查询消息订阅信息 `get_subscribe_info_by_device()`
- 按设备类别获取支持的消息类型 `get_message_type_page()`

---

## 配置凭证

**需要设置 Cloud 凭证**（ProductId、AK、SK）！

### 方式 1: 图形界面设置 (Windows GUI)

**最适合初学者和不想用命令行的用户！**

#### 步骤 1: 打开系统设置

1. 按下 `Win + R` 键，输入 `sysdm.cpl` 并回车
2. 或者右键点击"此电脑" → "属性" → "高级系统设置"

#### 步骤 2: 进入环境变量设置

1. 在弹出的"系统属性"窗口中，切换到 **"高级"** 选项卡
2. 点击底部的 **"环境变量(N)..."** 按钮

#### 步骤 3: 创建用户环境变量

在 **"当前用户的变量(U)"** 区域（窗口上半部分），点击 **"新建(W)..."**：

| 变量名 | 变量值 | 说明 |
|--------|--------|------|
| `DAHUA_CLOUD_PRODUCT_ID` | 你的 AppID | 应用 ID |
| `DAHUA_CLOUD_AK` | 你的 AccessKey | 访问密钥 |
| `DAHUA_CLOUD_SK` | 你的 SecretKey | 保密密钥 |

**示例**:
```
变量名：DAHUA_CLOUD_PRODUCT_ID
变量值：138XXXX731

变量名：DAHUA_CLOUD_AK  
变量值：196XXXXXXXXXXXXX808

变量名：DAHUA_CLOUD_SK
变量值：naumXXXXXXXXXXXXXXXXyHxh
```

#### 步骤 4: 确认并保存

1. 每个变量都点击 **"确定"** 保存
2. 关闭所有窗口
3. **重要**: 重新打开命令行窗口才能生效

#### 快速截图指引

如需更详细的图文教程，请参考以下操作要点：
- 确保在"用户变量"区域添加，而非"系统变量"
- 变量名必须完全一致（区分大小写）
- 变量值不要有多余空格
- 添加完成后需要重启终端

---

### 方式 2: 命令行快速设置

**Windows PowerShell:**
```powershell
[Environment]::SetEnvironmentVariable("DAHUA_CLOUD_PRODUCT_ID", "your_app_id", "User")
[Environment]::SetEnvironmentVariable("DAHUA_CLOUD_AK", "your_access_key", "User")
[Environment]::SetEnvironmentVariable("DAHUA_CLOUD_SK", "your_secret_key", "User")
```

**Linux/Mac:**
```bash
export DAHUA_CLOUD_PRODUCT_ID='your_app_id'
export DAHUA_CLOUD_AK='your_access_key'
export DAHUA_CLOUD_SK='your_secret_key'
```

---

### 方式 3: 命令行临时设置

**Windows PowerShell (临时):**
```powershell
$env:DAHUA_CLOUD_PRODUCT_ID='your_app_id'
$env:DAHUA_CLOUD_AK='your_access_key'
$env:DAHUA_CLOUD_SK='your_secret_key'
```

**注意**: 仅在当前窗口有效，关闭后失效

---

### 验证环境变量是否生效

**Linux/Mac:**
```bash
echo $DAHUA_CLOUD_PRODUCT_ID
echo $DAHUA_CLOUD_AK
# 注意：不要打印 SK，避免泄露
```

**Windows PowerShell:**
```powershell
$env:DAHUA_CLOUD_PRODUCT_ID
$env:DAHUA_CLOUD_AK
```

---

## 快速开始

### 基本使用

```bash
# 查看帮助
python scripts/dahua_iot_client.py --help

# 添加设备
python scripts/dahua_iot_client.py add -d <设备序列号> -p admin123 -c IPC

# 查询设备列表
python scripts/dahua_iot_client.py list -p 1 -s 10

# 查询设备在线状态
python scripts/dahua_iot_client.py online -d <设备序列号>

# 校验设备密码（验证密码是否正确）
python scripts/dahua_iot_client.py verify -d <设备序列号> -p admin123 -e aes256

# 删除设备
python scripts/dahua_iot_client.py delete -d <设备序列号>
```

### 完整示例

```bash
# 完整设备接入流程（仅需 Cloud 凭证）
cd scripts
python dahua_iot_client.py add -d <设备序列号> -p admin123 -c IPC -e aes256
python dahua_iot_client.py online -d <设备序列号>
python dahua_iot_client.py list -p 1 -s 20 -d <设备序列号前缀>
```

### Python SDK 调用

> **导入说明**：在 `scripts/` 目录下运行，或将 `scripts/` 加入 `PYTHONPATH` 后使用。

```python
from dahua_iot_client import DahuaIoTClient, create_client_from_env

# 方式1: 从环境变量创建客户端（verbose=True 打印API日志）
client = create_client_from_env()

# SDK 集成时建议关闭日志：create_client_from_env(verbose=False)

# 方式2: 手动创建客户端
client = DahuaIoTClient(
    app_id='your_product_id',
    access_key='your_access_key',
    secret_key='your_secret_key'
)

# 添加设备
result = client.add_device(
    device_id='<设备序列号>',
    device_password='admin123',
    category_code='IPC',
    encrypt_method='aes256'  # 推荐
)

print(f"Add device result: {result}")

# 校验设备密码（验证密码是否正确）
verify_result = client.verify_device_password('<设备序列号>', 'admin123', encrypt_method='aes256')
print(f"Password verify: {verify_result.get('success', False)}")

# 查询设备在线状态
status = client.get_device_online('<设备序列号>')
print(f"Online status: {status}")

# 查询设备列表
devices = client.get_device_list(page_num=1, page_size=10)
print(f"Device list: {devices}")

# 获取SD卡状态
sd_status = client.get_sd_card_status('<设备序列号>')
print(f"SD card status: {sd_status}")

# 设置设备使能开关
result = client.set_ability_status(
    device_id='<设备序列号>',
    ability_type='localRecord',
    status='on',
    channel_id='0'
)
```

---

## 工作流程

```
┌─────────────────────┐
│ 1. 初始化客户端      │
│   (配置凭证)         │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 2. 自动获取 Token    │
│   (AppAccessToken)   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 3. 调用业务API       │
│   (设备管理/配置)    │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 4. 返回结果          │
│   (JSON格式)         │
└─────────────────────┘
```

---

## API 端点

| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| 认证 | `/open-api/api-base/auth/getAppAccessToken` | 获取 AppAccessToken |
| 设备管理 | `/open-api/api-iot/device/*` | addDevice、deleteDevice、verifyDevCode、getDeviceList、deviceOnline、listDeviceDetailsByIds、checkDeviceBindInfo、getCategory、modifyDeviceName、modifyDevCode、getDeviceChannelInfo |
| 国标设备 | `/open-api/api-iot/device/*` | getSipInfo、listGbCode、addGbDevice、modifyGbDevice、deviceInfoDetailAll |
| SD卡/铃音/WiFi | `/open-api/api-aiot/device/*` | getSDCardStatus、getSDCardStorage、listSDCardStorage、formatSDCard、listCustomRing、addCustomRing、deleteCustomRing、setCustomRing、wifiAround、currentDeviceWifi、controlDeviceWifi |
| 设备配置 | `/open-api/api-aiot/device/*` | getAbilityStatus、setAbilityStatus、setCurrentUTC |
| 其他 | `/open-api/api-aiot/device/getSimSignalStrength` | 获取 SIM 信号强度 |
| 图片解密 | `/open-api/api-decrypto/image/decrypto` | 图片解密 |
| 消息订阅 | `/open-api/api-message/*` | addCallbackConfig、getAllCallbackConfigId、messageSubscribeByDeviceIds、getMessageTypePage、getMessageSubscribeInfoByDeviceId、updateSubscribeByCallbackConfigId、updateByCallbackConfigId、deleteCallbackId、getInfoByCallbackConfigId、getSubscribeInfoByCallbackConfigId |

完整 API 参考见 [references/api_reference.md](./references/api_reference.md)。

---

## 认证机制

### 签名算法

**SHA512 HMAC 签名** - 两种签名方式：

1. **get_token_sign()** - 获取 Token 签名
   ```
   签名因子: access_key + timestamp + nonce
   ```

2. **business_api_sign()** - 业务 API 签名
   ```
   签名因子: access_key + app_access_token + timestamp + nonce
   ```

### 请求头结构

**认证请求头** (获取 Token):
```python
{
    "Content-Type": "application/json",
    "AccessKey": access_key,
    "Timestamp": timestamp,
    "Nonce": nonce,
    "X-TraceId-Header": trace_id,
    "Sign": signature,           # get_token_sign() 生成
    "ProductId": app_id,
    "Version": "V1",
    "Sign-Type": "simple"
}
```

**业务请求头** (所有设备管理API):
```python
{
    "Content-Type": "application/json",
    "AccessKey": access_key,
    "Timestamp": timestamp,
    "Nonce": nonce,
    "X-TraceId-Header": trace_id,
    "Sign": signature,           # business_api_sign() 生成
    "Version": "V1",
    "Sign-Type": "simple",
    "AppAccessToken": app_token,
    "ProductId": app_id
}
```

---

## 代码架构

```
┌──────────────────────────────────────────────────────────────────┐
│                    常量配置层 (Constants)                         │
│  - API 端点、超时时间、环境变量名                               │
└──────────────────────────────────────────────────────────────────┘
                              │
┌──────────────────────────────────────────────────────────────────┐
│                    工具函数层 (Utilities)                         │
│  - get_token_sign()          获取 Token 签名                  │
│  - business_api_sign()       业务 API 签名                    │
│  - DeviceCodeEncryptor       设备密码加密（Base64/AES256）        │
└──────────────────────────────────────────────────────────────────┘
                              │
┌──────────────────────────────────────────────────────────────────┐
│                     DahuaIoTClient 类 (43个接口)                   │
│  设备: add/verify/delete/list/details/online/bind/category/channel │
│  国标: get_sip_info/add_gb/list_gb_code/modify_gb/gb_details      │
│  SD卡: get_status/storage/list/format  铃音: list/add/delete/set  │
│  配置: get/set_ability_status/set_current_utc                     │
│  WiFi: wifi_around/current/control  SIM: get_sim_signal_strength  │
│  消息: callback/message_subscribe/update/delete/query             │
│  其他: image_decrypt 图片解密                                      │
└──────────────────────────────────────────────────────────────────┘
                              │
┌──────────────────────────────────────────────────────────────────┐
│                    辅助函数层                                     │
│  - create_client_from_env()  从环境变量创建客户端                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## 设备密码加密

### 方式一：Base64加密

```python
格式："Dolynk_" + Base64(设备密码)
例如：若设备密码为 admin123
Base64(admin123) = YWRtaW4xMjM=
加密后字符串 = Dolynk_YWRtaW4xMjM=
```

### 方式二：AES256加密（推荐）

```python
格式：Base64(Aes256(待加密内容, AesKey, IV初始向量))
加密算法：Aes256/CBC/PKCS7
初始化向量IV：86E2DB6D77B5E9CD
AesKey：Cut32(UpperCase(MD5-32位(UpperCase(sk))))
```

**示例代码**:
```python
from dahua_iot_client import DeviceCodeEncryptor

encryptor = DeviceCodeEncryptor(
    secret_access_key="your_sk",
    device_id="your_device_id"
)

# AES256加密（推荐）
dev_code = encryptor.encrypt_aes256("admin123")

# Base64加密
dev_code = encryptor.encrypt_base64("admin123")
```

---

## 核心类和函数

### `DahuaIoTClient` 类

统一客户端类，封装所有设备管理API。

#### 初始化参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | `str` | ✅ | 产品ID (ProductId) |
| `access_key` | `str` | ✅ | 访问密钥 (AccessKey) |
| `secret_key` | `str` | ✅ | 密钥 (SecretKey) |
| `api_base_url` | `str` | ❌ | API基础地址（默认：https://open.cloud-dahua.com/） |
| `verbose` | `bool` | ❌ | 是否打印API调用日志（默认：True，SDK集成时建议False） |

#### 主要方法（43 个接口）

| 分类 | 方法 | 说明 | CLI |
|------|------|------|-----|
| 设备 | `add_device()` | 添加设备 | `add` |
| 设备 | `verify_device_password()` | 校验设备密码 | `verify` |
| 设备 | `delete_device()` | 删除设备 | `delete` |
| 设备 | `get_device_list()` | 查询设备列表 | `list` |
| 设备 | `get_device_online()` | 查询设备在线状态 | `online` |
| 设备 | `list_device_details()` | 批量查询设备详细信息 | `details` |
| 设备 | `check_device_bind()` | 查询设备绑定状态 | `bind` |
| 设备 | `get_category()` | 查询设备品类 | `category` |
| 设备 | `get_device_channel_info()` | 获取设备通道信息 | `channels` |
| 设备 | `modify_device_name()` | 修改设备/通道名称 | - |
| 设备 | `modify_dev_code()` | 修改设备密码 | - |
| 国标 | `get_sip_info()` | 获取国标设备注册信息 | `sip-info` |
| 国标 | `list_gb_code()` | 获取国标码列表 | `gb-code` |
| 国标 | `add_gb_device()` | 添加国标设备 | `add-gb` |
| 国标 | `modify_gb_device()` | 修改国标设备信息 | `modify-gb` |
| 国标 | `list_gb_device_details()` | 国标设备查询详细信息 | `gb-details` |
| SD卡 | `get_sd_card_status()` | 获取SD卡状态 | - |
| SD卡 | `get_sd_card_storage()` | 查询SD卡容量 | - |
| SD卡 | `list_sd_card_storage()` | 获取SD卡列表 | - |
| SD卡 | `format_sd_card()` | 格式化SD卡 | - |
| 配置 | `get_ability_status()` | 获取设备使能状态 | `ability` |
| 配置 | `set_ability_status()` | 设置设备使能状态 | - |
| 配置 | `set_current_utc()` | 设备校时 | - |
| 铃音 | `list_custom_ring()` | 获取铃声列表 | - |
| 铃音 | `add_custom_ring()` | 新增自定义铃声 | - |
| 铃音 | `delete_custom_ring()` | 删除自定义铃声 | - |
| 铃音 | `set_custom_ring()` | 设置铃声 | - |
| WiFi | `current_device_wifi()` | 获取设备当前连接热点 | - |
| WiFi | `wifi_around()` | 获取设备周边热点 | - |
| WiFi | `control_device_wifi()` | 修改设备连接热点 | - |
| 其他 | `get_sim_signal_strength()` | 获取SIM信号强度 | - |
| 其他 | `image_decrypt()` | 图片解密 | - |
| 消息 | `add_callback_config()` | 添加回调配置 | - |
| 消息 | `message_subscribe()` | 按设备ID订阅消息 | - |
| 消息 | `get_all_callback_config()` | 分页获取回调配置 | - |
| 消息 | `update_subscribe_by_callback_config()` | 根据回调配置更新订阅 | - |
| 消息 | `update_callback_config()` | 更新回调配置 | - |
| 消息 | `delete_callback_config()` | 删除回调配置 | - |
| 消息 | `get_callback_config_info()` | 搜索回调配置信息 | - |
| 消息 | `get_subscribe_info_by_callback_config()` | 搜索已订阅设备消息 | - |
| 消息 | `get_subscribe_info_by_device()` | 按设备ID查询订阅信息 | - |
| 消息 | `get_message_type_page()` | 按设备类别获取消息类型 | - |

### `DeviceCodeEncryptor` 类

设备密码加密工具类。

#### 方法

| 方法 | 说明 |
|------|------|
| `encrypt_base64(password)` | Base64加密 |
| `encrypt_aes256(password)` | AES256加密（推荐） |

---

## 命令行参数

### 通用参数

| 参数 | 简写 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `--help` | `-h` | - | ❌ | 显示帮助信息 |

### 命令行子命令汇总

| 子命令 | 说明 |
|--------|------|
| `add` | 添加设备 |
| `add-gb` | 添加国标设备 |
| `delete` | 删除设备 |
| `verify` | 校验设备密码 |
| `list` | 查询设备列表 |
| `details` | 查询设备详细信息 |
| `online` | 查询设备在线状态 |
| `bind` | 查询设备绑定状态 |
| `category` | 查询设备品类 |
| `channels` | 获取设备通道信息 |
| `ability` | 获取设备使能状态 |
| `gb-code` | 获取国标码列表 |
| `sip-info` | 获取国标设备注册信息 |
| `gb-details` | 查询国标设备详细信息 |
| `modify-gb` | 修改国标设备信息 |
| `encrypt` | 加密设备密码 |

### 子命令详情

#### `add` - 添加设备

| 参数 | 简写 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `--device-id` | `-d` | `str` | ✅ | 设备序列号 |
| `--password` | `-p` | `str` | ✅ | 设备密码 |
| `--category` | `-c` | `str` | ❌ | 设备品类编码（默认：IPC） |
| `--encrypt` | `-e` | `str` | ❌ | 加密方式（base64/aes256，默认：base64） |

#### `delete` - 删除设备

| 参数 | 简写 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `--device-id` | `-d` | `str` | ✅ | 设备序列号 |

#### `list` - 查询设备列表

| 参数 | 简写 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `--page` | `-p` | `int` | ❌ | 页码（默认：1） |
| `--size` | `-s` | `int` | ❌ | 每页条数（默认：10） |
| `--device-id` | `-d` | `str` | ❌ | 设备序列号（模糊查询） |

#### `online` - 查询设备在线状态

| 参数 | 简写 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `--device-id` | `-d` | `str` | ✅ | 设备序列号 |

#### `verify` - 校验设备密码

验证指定设备的密码是否正确（调用 verifyDevCode 接口）。

| 参数 | 简写 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `--device-id` | `-d` | `str` | ✅ | 设备序列号 |
| `--password` | `-p` | `str` | ✅ | 设备密码（明文） |
| `--encrypt` | `-e` | `str` | ❌ | 加密方式（base64/aes256，默认：base64） |

```bash
# 校验设备密码
python scripts/dahua_iot_client.py verify -d <设备序列号> -p admin123 -e aes256
```

#### `details` - 查询设备详细信息

| 参数 | 说明 |
|------|------|
| `device_ids` | 设备序列号（可多个，位置参数） |

```bash
python scripts/dahua_iot_client.py details <设备序列号> <设备序列号2>
```

#### `category` - 查询设备品类

| 参数 | 简写 | 说明 |
|------|------|------|
| `--primary` | `-p` | 1级设备类别代码 |
| `--second` | `-s` | 2级设备类别代码（如 IPC） |
| `--model` | `-m` | 设备型号 |

#### `bind` - 查询设备绑定状态

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--device-id` | `-d` | ✅ | 设备序列号 |

#### `channels` - 获取设备通道信息

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--device-id` | `-d` | ✅ | 设备序列号 |

#### `ability` - 获取设备使能状态

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--device-id` | `-d` | ✅ | 设备序列号 |
| `--ability-type` | `-a` | ✅ | 使能类型（如 localRecord、motionDetect、faceCapture） |
| `--channel-id` | `-c` | ❌ | 通道号（通道级使能需传） |

#### `add-gb` - 添加国标设备

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--gb-code` | `-g` | ✅ | 国标码 |
| `--password` | `-p` | ✅ | 设备注册密码 |
| `--channels` | `-c` | ✅ | 通道总数 |
| `--encrypt` | `-e` | ❌ | 加密方式（base64/aes256，默认 base64） |
| `--manufacturer` | `-m` | ❌ | 厂商（Dahua、HIKVSION、UNKNOW） |
| `--stream-model` | `-s` | ❌ | 拉流协议（TCP/UDP） |
| `--device-class` | `-d` | ❌ | 设备类型（NVR/IPC） |

#### `gb-code` - 获取国标码列表

| 参数 | 简写 | 说明 |
|------|------|------|
| `--count` | `-c` | 查询数量（1-10000，默认 10） |
| `--prefix` | `-p` | 国标码前缀（长度必须 13 位） |

#### `sip-info` - 获取国标设备注册信息

无需参数，返回 Sip 服务器 IP 和端口。

#### `gb-details` - 查询国标设备详细信息

| 参数 | 说明 |
|------|------|
| `device_ids` | 设备序列号（可多个，位置参数） |

#### `modify-gb` - 修改国标设备信息

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--device-id` | `-d` | ✅ | 设备序列号 |
| `--password` | `-p` | ❌ | 新设备密码 |
| `--encrypt` | `-e` | ❌ | 密码加密方式（base64/aes256，默认：base64） |
| `--stream-model` | `-s` | ❌ | 拉流协议（TCP/UDP） |

#### `encrypt` - 加密设备密码

| 参数 | 简写 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `--password` | `-p` | `str` | ✅ | 设备密码 |
| `--secret-key` | `-s` | `str` | ✅ | SecretKey |
| `--device-id` | `-d` | `str` | ❌ | 设备序列号 |
| `--method` | `-m` | `str` | ❌ | 加密方式（base64/aes256，默认：base64） |

---

## 响应格式

所有 API 响应遵循统一格式：

```python
{
    "code": "200",           # 响应状态码
    "success": true,         # 响应状态
    "data": {},             # 响应数据
    "msg": "操作成功"         # 响应消息
}
```

### add_device 响应示例

```python
{
    "success": True,
    "code": "200",
    "msg": "操作成功",
    "data": {
        "deviceId": "<设备序列号>",
        "deviceName": "",
        "channelNum": 1,
        "status": 1
    }
}
```

### get_device_online 响应示例

```python
{
    "success": True,
    "code": "200",
    "msg": "操作成功",
    "data": {
        "deviceId": "<设备序列号>",
        "online": True
    }
}
```

**错误码说明**:
- `200`: 成功
- 其他: 失败，查看 `msg` 字段了解错误原因

---

## 可配置常量

| 常量名 | 默认值 | 说明 |
|--------|--------|------|
| `DEFAULT_API_BASE_URL` | `https://open.cloud-dahua.com/` | API 基础地址 |
| `TOKEN_EXPIRY_SECONDS` | `604800` | Token 有效期(秒) - 7天 |
| `TIMEOUT_AUTH` | `60` | 认证超时(秒) |
| `TIMEOUT_DEVICE` | `60` | 设备管理超时(秒) |
| `TIMEOUT_CONFIG` | `60` | 配置超时(秒) |
| `TIMEOUT_SD_CARD` | `60` | SD卡管理超时(秒) |
| `TIMEOUT_FORMAT_SD` | `120` | SD卡格式化超时(秒) |

---

## 依赖要求

- Python 3.8+
- requests>=2.31.0
- pycryptodome>=3.15.0

安装依赖:
```bash
pip install requests pycryptodome
```

---

## 使用场景

### 1️ 设备接入场景

```bash
# 添加设备
python scripts/dahua_iot_client.py add -d <设备序列号> -p admin123 -c IPC

# 校验设备密码（验证密码是否正确）
python scripts/dahua_iot_client.py verify -d <设备序列号> -p admin123 -e aes256

# 查询设备在线状态
python scripts/dahua_iot_client.py online -d <设备序列号>

# 查询设备列表/详细信息
python scripts/dahua_iot_client.py list -d <设备序列号前缀>
python scripts/dahua_iot_client.py details <设备序列号>
```

### 2️ 设备管理场景

```python
# Python SDK
client = create_client_from_env()

# 获取设备列表
devices = client.get_device_list(page_num=1, page_size=100)

# 批量查询设备详情
device_ids = ['<设备序列号1>', '<设备序列号2>']
details = client.list_device_details(device_ids)

# 删除设备
client.delete_device('<设备序列号>')
```

### 3️ SD卡管理场景

```python
# 查询SD卡状态
status = client.get_sd_card_status('<设备序列号>')

# 查询SD卡容量
storage = client.get_sd_card_storage('<设备序列号>')

# 格式化SD卡
result = client.format_sd_card('<设备序列号>')
```

### 4️ 设备配置场景

```python
# 修改设备名称
client.modify_device_name('<设备序列号>', 'My Camera')

# 启用本地录像
client.set_ability_status(
    device_id='<设备序列号>',
    ability_type='localRecord',
    status='on',
    channel_id='0'
)
```

### 5️ 消息订阅场景

```python
# 添加回调配置（返回的 data 为回调配置ID）
callback = client.add_callback_config(
    callback_url='https://your-server.com/callback',
    is_push=True
)
callback_config_id = callback['data']  # API 返回的 data 即为 callbackConfigId

# 订阅设备消息
client.message_subscribe(
    device_ids=['<设备序列号>'],
    message_type_codes=['online', 'offline', 'videoMotion'],
    category_code='IPC',
    callback_config_id=callback_config_id
)
```

### 6️ 国标设备场景

```bash
# 获取国标码
python scripts/dahua_iot_client.py gb-code -c 5

# 获取 Sip 注册信息
python scripts/dahua_iot_client.py sip-info

# 添加国标设备
python scripts/dahua_iot_client.py add-gb -g 34020000001320000001 -p admin123 -c 4 -e aes256
```

```python
# Python SDK
gb_codes = client.list_gb_code(count=10)
sip_info = client.get_sip_info()
result = client.add_gb_device(gb_code='34020000001320000001', device_password='admin123', channel_number=4)
```

### 7️ 铃音 / WiFi / 图片解密

```python
# 铃音管理
rings = client.list_custom_ring(device_id, relate_type='device')  # relate_type: device/channel
client.add_custom_ring(device_id, name='my_ring', url='https://...', ring_type='custom')

# WiFi 管理
wifi_info = client.current_device_wifi(device_id)
around = client.wifi_around(device_id)
client.control_device_wifi(device_id, ssid='MyWiFi', password='wifi_password')

# 图片解密（image_url 为待解密的图片地址）
decrypted = client.image_decrypt(device_id, image_url='https://...')
```

---

## 安全提示

⚠️ **不要将真实的 Cloud 凭证提交到 Git!**

本项目包含 `.gitignore` 文件，会自动忽略敏感配置文件。建议：
- 使用环境变量存储凭证
- 定期轮换密钥
- 限制应用权限范围
- Windows 用户建议使用 GUI 方式设置（更安全）

---

## 目录结构

```
dahua-cloud-open-iot-basic-general-kit/
├── README.md                        # 快速说明
├── QUICKSTART.md                    # 5分钟快速入门
├── SKILL.md                         # 本文件（完整指南）
├── FAQ.md                           # 常见问题解答
├── .gitignore                       # Git 忽略规则
├── references/
│   └── api_reference.md             # 完整API参考文档（43个接口）
└── scripts/
    ├── dahua_iot_client.py          # 统一客户端（推荐使用）
    ├── sign_helper.py               # 签名工具（旧版，保留兼容）
    ├── device_code_encrypt.py       # 密码加密工具（旧版，保留兼容）
    └── requirements.txt             # Python依赖
```

---

## 核心优势

✅ **极简配置** - 仅需要 3 个环境变量 (ProductId, AK, SK)  
✅ **单文件实现** - 所有功能集中在一个文件，易于维护  
✅ **统一客户端** - 封装所有API，无需关心签名细节  
✅ **自动Token管理** - Token自动刷新，无需手动处理  
✅ **命令行支持** - 快速操作无需编写代码  
✅ **Python SDK** - 可轻松集成到其他应用  
✅ **跨平台支持** - Windows/Linux/Mac 完美运行  
✅ **GUI 友好** - Windows 图形界面设置环境变量  
✅ **轻量依赖** - 仅依赖 requests 和 pycryptodome  
✅ **安全可靠** - 标准 API 认证，无密码泄露风险  

---

## 迁移指南

### 从旧版迁移

如果你之前使用 `sign_helper.py` 和 `device_code_encrypt.py`，可以这样迁移：

**旧版代码**:
```python
from sign_helper import DahuaAPISigner
from device_code_encrypt import DeviceCodeEncryptor

signer = DahuaAPISigner(access_key, secret_key, product_id)
encryptor = DeviceCodeEncryptor(secret_key, device_id)

# 手动管理Token
auth_headers = signer.sign_for_auth_api()
# ... 手动获取Token ...

# 手动构造请求
business_headers = signer.sign_for_business_api(app_token)
# ... 手动调用API ...
```

**新版代码**:
```python
from dahua_iot_client import create_client_from_env

# 自动从环境变量读取配置
client = create_client_from_env()

# 自动管理Token，直接调用API
result = client.add_device(
    device_id='<设备序列号>',
    device_password='admin123'
)
```

---

## 常见问题

### Q1: Token过期怎么办？

**解决方案**: 客户端会自动管理Token，在过期前自动刷新，无需手动处理。

### Q2: 签名验证失败？

**检查清单**:
- [ ] AccessKey、SecretKey、ProductID是否正确
- [ ] 环境变量是否正确设置
- [ ] 是否重新打开了命令行窗口（环境变量需重启终端生效）

### Q3: 设备添加失败？

**可能原因**:
- 设备密码加密方式不正确（推荐使用AES256）
- 设备序列号已存在
- 设备品类编码不正确
- 设备未初始化或未设置密码

### Q4: 如何判断设备是否支持某个功能？

**方法**: 调用 `list_device_details()` 接口，查看返回的 `deviceAbility` 或 `channelAbility` 字段，检查是否包含相应的能力集标识。

### Q5: 如何验证设备密码是否正确？

**方法**: 使用 `verify` 子命令或 `verify_device_password()` 方法调用 verifyDevCode 接口：

```bash
# 命令行
python scripts/dahua_iot_client.py verify -d <设备ID> -p <密码> -e aes256
```

```python
# Python SDK
result = client.verify_device_password(device_id, password, encrypt_method='aes256')
# result['success'] 为 True 表示密码正确
```

更多常见问题请参阅 [FAQ.md](./FAQ.md)。

---

## License

MIT License
