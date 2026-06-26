---
name: dahua-cloud-open-device-image-analysis
description: 基于大华云开发者平台的 IoT 设备图像分析技能。支持对 Dahua IoT 设备进行抓拍，并调用大模型进行图片分析。可识别监控画面中的人、车辆、物体等，支持安全帽、口罩、烟雾、火焰等检测及摔倒、入侵等行为识别。适用于设备图像分析、安全生产、异常看护、连锁巡检、企业安全管理等场景。
metadata: {"openclaw":{"requires":{"env":["DAHUA_CLOUD_PRODUCT_ID","DAHUA_CLOUD_AK","DAHUA_CLOUD_SK"]},"primaryEnv":"DAHUA_CLOUD_SK","install":[{"id":"requests","kind":"python","package":"requests","label":"Install Python requests"}]}}
tags:
  - 大华云
  - 图像分析
  - 安防监控
  - 设备抓拍
  - 图片分析
  - device-image-analysis
  - dahua-iot
  - dahua-cloud-open
  - AI 图片分析
paths:
  - captured_images/
---

# Dahua AI Device Image Analysis

调用大华云平台大模型进行图像分析。**完整的抓图→AI 分析流程！**

##  完整功能

本技能提供**端到端的大华云图像分析服务**:
- ✅ **设备抓拍** - 实时拍摄监控摄像头画面
- ✅ **本地保存** - 抓拍图片自动下载到本地
- ✅ **AI 分析** - 调用大华云大型模型进行智能分析
- ✅ **零冗余配置** - 仅需 Cloud 凭证（ProductId、AK、SK）即可，无多余参数
- ✅ **图形界面支持** - Windows GUI 方式设置环境变量

---

##  配置凭证

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

如果需要更详细的图文教程，请参考以下操作要点:
- 确保在"用户变量"区域添加，而非"系统变量"
- 变量名必须完全一致（区分大小写）
- 变量值不要有多余空格
- 添加完成后需要重启终端

---

### 方式 2: 命令行快速设置

**适合熟悉命令行的用户！**

**Windows PowerShell (推荐 - 用户级别):**
```powershell
[Environment]::SetEnvironmentVariable("DAHUA_CLOUD_PRODUCT_ID", "your_app_id", "User")
[Environment]::SetEnvironmentVariable("DAHUA_CLOUD_AK", "your_access_key", "User")
[Environment]::SetEnvironmentVariable("DAHUA_CLOUD_SK", "your_secret_key", "User")
```

**Linux/Mac (当前会话临时):**
```bash
export DAHUA_CLOUD_PRODUCT_ID='your_app_id'
export DAHUA_CLOUD_AK='your_access_key'
export DAHUA_CLOUD_SK='your_secret_key'
```

**⚠️ 安全建议**: 避免将凭证写入 `~/.bashrc`、`~/.zshrc` 等启动文件进行长期存储，以防凭证泄露。建议优先使用 Windows 用户环境变量或临时的当前会话导出方式。

---

### 方式 3: 命令行临时设置 

**适合快速测试！**

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

##  快速开始

### 基本使用

```bash
python device_image_analysis.py \
  --device-sn BA5918431 \
  --prompt "请判断这张图片中是否有人"
```

### 完整示例

```bash
# 抓拍并调用 AI 分析（仅需要 Cloud 凭证）
python device_image_analysis.py \
  -d BA5918431 \
  -p "请判断图片中是否有白色轿车。回答格式：有{是} 或 无{否}" \
  -c 0
```

### Python SDK 调用

```python
from device_image_analysis import analyze_device_camera

result = analyze_device_camera(
    device_sn="BA5918431",
    prompt="请判断图中是否有人玩手机",
    channel_no=0
)

print(f"Analysis Result: {result['analysis']['result']}")
```

---

##  工作流程

```
┌─────────────┐
│ 1. 获取 Cloud Token │
│   (AppAccessToken)  │
└──────┬──────┘
       ▼
┌─────────────┐
│ 2. 设备抓图    │
│   setDeviceSnapEnhanced │
└──────┬──────┘
       ▼
┌─────────────┐
│ 3. 等待 OSS    │
│   URL 生效(1s) │
└──────┬──────┘
       ▼
┌─────────────┐
│ 4. 下载保存    │
│   图片到本地   │
│   (支持5次重试) │
└──────┬──────┘
       ▼
┌─────────────┐
│ 5. 调用 AI 分析   │
│   imageAnalysis API │
└──────┬──────┘
       ▼
┌─────────────┐
│ 6. 返回结果    │
│   含分析内容和本地路径    │
└─────────────┘
```

---


##  响应格式

```python
{
    "success": True,
    "device_sn": "BA5918431",
    "channel_no": 0,
    "image_url": "https://oss-cn-hangzhou.aliyuncs.com/...",
    "local_image_path": "./captured_images/BA5918431/ch0_1234567890.jpg",
    "analysis": {
        "success": True,
        "code": "200",
        "message": "操作成功",
        "data": {"content": "图中有 2 个人"},
        "result": "图中有 2 个人"
    }
}
```

---

##  使用场景

### 1️ 人员检测
```bash
python device_image_analysis.py \
  -d YOUR_SN \
  -p "图中是否有人？请回答'有'或'无'"
```

### 2️ 车辆识别
```bash
python device_image_analysis.py \
  -d YOUR_SN \
  -p "图中有多少辆车？分别是什么颜色？"
```

### 3️ 异常行为检测
```bash
python device_image_analysis.py \
  -d YOUR_SN \
  -p "图中是否有打架、摔倒等异常情况？"
```

### 4️ 物体识别
```bash
python device_image_analysis.py \
  -d YOUR_SN \
  -p "识别图中的主要物体，按重要性排序"
```

---

##  技术细节

### API 端点

| 端点 | 路径 | 说明 |
|------|------|------|
| 认证 | `/open-api/api-base/auth/getAppAccessToken` | 获取 AppAccessToken |
| 抓图 | `/open-api/api-iot/device/setDeviceSnapEnhanced` | 设备实时抓图 |
| AI 分析 | `/open-api/api-ai/largeModelDetect/imageAnalysis` | 大模型图像分析 |

### 认证机制

- **SHA512 HMAC 签名** - 两种签名方式：
  - `get_token_sign()` - 获取 Token 签名 (access_key + timestamp + nonce)
  - `business_api_sign()` - 业务 API 签名 (access_key + app_access_token + timestamp + nonce)
- **AppAccessToken 自动刷新** - 1 小时有效期，自动管理
- **依赖 Cloud 凭证** - 使用 ProductId、AccessKey、SecretKey 进行认证

### 代码架构

```
┌─────────────────────────────────────────────────────────────┐
│                    常量配置层 (Constants)                      │
│  - API 端点、超时时间、环境变量名                               │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    工具函数层 (Utilities)                      │
│  - get_token_sign()          获取Token签名                    │
│  - business_api_sign()       业务API签名                      │
│  - verify_image_url_accessible()  URL可访问性验证(备用)        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 DahuaSnapshotClient 类                       │
│  - get_app_access_token()    获取/刷新 Token                 │
│  - capture_snapshot()        设备抓图                       │
│  - download_and_save()       图片下载保存(含1s等待+5次重试)   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   AI 分析函数层                               │
│  - analyze_with_dahua_ai()   调用大模型分析                   │
│  - analyze_device_camera()   完整流程封装                     │
└─────────────────────────────────────────────────────────────┘
```

### 核心函数说明

#### `analyze_device_camera(device_sn, prompt, channel_no=0)`

完整的图像分析流程封装函数。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_sn` | `str` | ✅ | 设备序列号 (SN) |
| `prompt` | `str` | ✅ | AI 分析问题 |
| `channel_no` | `int` | ❌ | 通道号 (默认：0) |

**返回值:** `Dict[str, Any]`
```python
{
    "success": True,           # 整体成功状态
    "device_sn": "BA5918431",  # 设备序列号
    "channel_no": 0,           # 通道号
    "image_url": "...",        # 图片 URL
    "local_image_path": "...", # 本地保存路径
    "analysis": {              # AI 分析结果
        "success": True,
        "code": "200",
        "message": "操作成功",
        "data": {"content": "..."},
        "result": "..."
    }
}
```

#### 请求头结构

**认证请求头** (获取 Token):
```python
{
    "Content-Type": "application/json",
    "AccessKey": access_key,
    "Timestamp": timestamp,
    "Nonce": nonce,
    "X-TraceId-Header": trace_id,
    "Sign": signature,           # get_token_sign() 生成
    "ProductId": app_id,         # DAHUA_CLOUD_PRODUCT_ID
    "Version": "V1",
    "Sign-Type": "simple"
}
```

**业务请求头** (抓图/AI分析):
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
    "AppAccessToken": app_token, # 获取Token后传入
    "ProductId": app_id          # DAHUA_CLOUD_PRODUCT_ID
}
```

#### 可配置常量

| 常量名 | 默认值 | 说明 |
|--------|--------|------|
| `DEFAULT_API_BASE_URL` | `https://open.cloud-dahua.com/` | API 基础地址 |
| `DEFAULT_CHANNEL_NO` | `0` | 默认通道号 |
| `TOKEN_EXPIRY_SECONDS` | `3600` | Token 有效期(秒) |
| `TIMEOUT_AUTH` | `60` | 认证超时(秒) |
| `TIMEOUT_SNAPSHOT` | `60` | 抓图超时(秒) |
| `TIMEOUT_DOWNLOAD` | `300` | 下载超时(秒) |
| `TIMEOUT_ANALYSIS` | `120` | AI分析超时(秒) |
| `URL_VERIFY_RETRIES` | `3` | URL 验证重试次数 |
| `URL_VERIFY_DELAY` | `1` | URL 验证重试间隔(秒) |
| `SNAPSHOT_RETRY_DELAY` | `2` | 抓拍重试间隔(秒) |

#### 命令行参数

| 参数 | 简写 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `--device-sn` | `-d` | `str` | ✅ | 设备序列号 (SN) |
| `--prompt` | `-p` | `str` | ✅ | AI 分析问题 |
| `--channel` | `-c` | `int` | ❌ | 通道号 (默认：0) |

---

##  依赖要求

- Python 3.8+
- requests>=2.31.0

安装依赖:
```bash
pip install requests
```

---

##  安全提示

 **不要将真实的 Cloud 凭证提交到 Git!**

本项目包含 `.gitignore` 文件，会自动忽略敏感配置文件。建议：
- 使用环境变量存储凭证
- 定期轮换密钥
- 限制应用权限范围
- Windows 用户建议使用 GUI 方式设置（更安全）

---

## 目录结构

```
dahua-cloud-open-device-image-analysis/
├── README.md                         # 说明文件
├── SKILL.md                          # 本文件
├── FAQ.md                            # 常见问题解答
├── device_image_analysis.py # 主程序
├── requirements.txt                  # Python 依赖
└── .gitignore                        # Git 忽略规则
```

---

##  核心优势

✅ **极简配置** - 仅需要 3 个必要参数 (SN, Prompt, Channel)  
✅ **代码优化** - 统一的签名/请求头生成，完整类型注解  
✅ **可配置** - 超时、重试等参数通过常量统一管理  
✅ **跨平台支持** - Windows/Linux/Mac 完美运行  
✅ **GUI 友好** - Windows 图形界面设置环境变量  
✅ **轻量依赖** - 仅依赖 requests 库，单文件实现  
✅ **安全可靠** - 标准 API 认证，无密码泄露风险  

---

##  License

MIT License
