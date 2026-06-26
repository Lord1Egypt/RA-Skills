# 大华云开放平台 - 基础通用套件

大华云开放平台基础通用套件客户端，提供设备管理、SD卡、配置、消息订阅等通用接口。

## 快速开始

### 1. 安装依赖

```bash
cd scripts
pip install -r requirements.txt
```

### 2. 配置凭证

**Windows PowerShell (临时)**:
```powershell
$env:DAHUA_CLOUD_PRODUCT_ID='your_product_id'
$env:DAHUA_CLOUD_AK='your_access_key'
$env:DAHUA_CLOUD_SK='your_secret_key'
```

**Windows (永久)**:
```powershell
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

### 3. 使用命令行

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

### 4. 使用Python SDK

在 `scripts/` 目录下运行：

```python
from dahua_iot_client import create_client_from_env

# 从环境变量创建客户端
client = create_client_from_env()

# 添加设备
result = client.add_device(
    device_id='<设备序列号>',
    device_password='admin123',
    category_code='IPC'
)

# 查询设备在线状态
status = client.get_device_online('<设备序列号>')

# 查询设备列表
devices = client.get_device_list(page_num=1, page_size=10)
```

## 主要功能

- ✅ 设备管理（添加/删除/查询）
- ✅ SD卡管理（状态查询/容量查询/格式化）
- ✅ 设备配置（名称修改/使能开关）
- ✅ 消息订阅（回调配置/消息订阅）
- ✅ 自动Token管理
- ✅ 命令行工具
- ✅ Python SDK

## 详细文档

- [QUICKSTART.md](./QUICKSTART.md) - 5 分钟快速入门
- [SKILL.md](./SKILL.md) - 完整使用指南
- [FAQ.md](./FAQ.md) - 常见问题解答
- [references/api_reference.md](./references/api_reference.md) - API 参考文档

## 核心优势

- **单文件实现** - 所有功能集中在 `dahua_iot_client.py`
- **自动 Token 管理** - 无需手动处理 Token 刷新
- **统一客户端** - 封装所有 API 调用
- **环境变量配置** - 支持 GUI 和命令行配置
- **跨平台支持** - Windows/Linux/Mac 完美运行

## 安全提示

⚠️ 不要将真实的 Cloud 凭证提交到 Git！建议使用环境变量存储凭证。

## License

MIT License
