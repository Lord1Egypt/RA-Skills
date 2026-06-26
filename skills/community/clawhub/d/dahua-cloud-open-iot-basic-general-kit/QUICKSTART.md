# 快速入门指南

## 5分钟快速上手

### 第一步：安装依赖

```bash
cd scripts
pip install -r requirements.txt
```

### 第二步：配置凭证

**Windows PowerShell (推荐)**:
```powershell
# 临时设置（当前窗口有效）
$env:DAHUA_CLOUD_PRODUCT_ID='your_product_id'
$env:DAHUA_CLOUD_AK='your_access_key'
$env:DAHUA_CLOUD_SK='your_secret_key'

# 或永久设置（所有窗口有效）
[Environment]::SetEnvironmentVariable("DAHUA_CLOUD_PRODUCT_ID", "your_product_id", "User")
[Environment]::SetEnvironmentVariable("DAHUA_CLOUD_AK", "your_access_key", "User")
[Environment]::SetEnvironmentVariable("DAHUA_CLOUD_SK", "your_secret_key", "User")
```

**Linux/Mac**:
```bash
export DAHUA_CLOUD_PRODUCT_ID='your_product_id'
export DAHUA_CLOUD_AK='your_access_key'
export DAHUA_CLOUD_SK='your_secret_key'
```

### 第三步：使用客户端

#### 方式一：命令行工具

```bash
# 查看帮助
python dahua_iot_client.py --help

# 添加设备
python dahua_iot_client.py add -d <设备序列号> -p admin123

# 查询设备列表
python dahua_iot_client.py list

# 查询设备在线状态
python dahua_iot_client.py online -d <设备序列号>

# 删除设备
python dahua_iot_client.py delete -d <设备序列号>
```

#### 方式二：Python代码

> 在 `scripts/` 目录下运行，或先将 `scripts/` 加入 PYTHONPATH。

```python
from dahua_iot_client import create_client_from_env

# 创建客户端（自动从环境变量读取凭证）
client = create_client_from_env()
# SDK 集成时可关闭日志：create_client_from_env(verbose=False)

# 添加设备
result = client.add_device(
    device_id='<设备序列号>',
    device_password='admin123',
    category_code='IPC'
)
print(f"添加设备: {result}")

# 查询设备在线状态
status = client.get_device_online('<设备序列号>')
print(f"在线状态: {status}")

# 查询设备列表
devices = client.get_device_list(page_num=1, page_size=10)
print(f"设备列表: {devices}")

# 获取SD卡状态
sd_status = client.get_sd_card_status('<设备序列号>')
print(f"SD卡状态: {sd_status}")
```

## 常用命令速查

### 设备管理

```bash
# 添加设备（AES256加密）
python dahua_iot_client.py add -d <设备序列号> -p <设备密码> -c IPC

# 查询设备列表
python dahua_iot_client.py list -p 1 -s 10

# 查询设备在线状态
python dahua_iot_client.py online -d <设备序列号>

# 删除设备
python dahua_iot_client.py delete -d <设备序列号>
```

### 密码加密

```bash
# 加密设备密码
python dahua_iot_client.py encrypt -p <密码> -s <SecretKey> -m aes256
```

## 常见问题

### Q: 环境变量设置后不生效？

**A**: Windows下需要重新打开命令行窗口，或使用：
```powershell
# 刷新环境变量
$env:DAHUA_CLOUD_PRODUCT_ID = [Environment]::GetEnvironmentVariable("DAHUA_CLOUD_PRODUCT_ID", "User")
$env:DAHUA_CLOUD_AK = [Environment]::GetEnvironmentVariable("DAHUA_CLOUD_AK", "User")
$env:DAHUA_CLOUD_SK = [Environment]::GetEnvironmentVariable("DAHUA_CLOUD_SK", "User")
```

### Q: Token过期怎么办？

**A**: 客户端会自动管理Token，无需手动处理。

### Q: 如何查看API调用详情？

**A**: 客户端会自动打印请求和响应信息：
```
[API] POST /open-api/api-iot/device/addDevice
[DATA] {"deviceId": "<设备序列号>", ...}
[RESP] {"success": true, ...}
```

## 下一步

- 📖 阅读完整文档：[SKILL.md](./SKILL.md)
- 🔍 查看API参考：[references/api_reference.md](./references/api_reference.md)
- ❓ 常见问题：[FAQ.md](./FAQ.md)

## 需要帮助？

如有问题，请查看：
1. [FAQ.md](./FAQ.md) - 常见问题解答
2. [SKILL.md](./SKILL.md) - 完整使用指南
3. [references/api_reference.md](./references/api_reference.md) - 详细 API 说明
