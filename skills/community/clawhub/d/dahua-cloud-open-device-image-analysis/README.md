# Dahua AI Device Image Analysis

调用大华云平台大模型进行图像分析。**完整的抓图→AI 分析流程！**

##  如何使用本 Skill

### 在 AI IDE 中调用（推荐）

在支持 Skill 的 AI IDE（ 如 OpenClaw Cursor Qoder ）中，有两种调用方式：

#### 方式一：自然语言调用（自动识别）

直接用自然语言描述你的需求，AI 会自动识别并调用相应的 Skill：

**基本格式：**
```
从 <设备SN> 抓一张图，并分析 <你的问题>
```

**示例：**
```
从 BA5918431 抓一张图，并分析有没有人
```

```
从 BA5918431 抓图，判断图中是否有白色车辆
```

```
抓拍设备 BA5918431 的画面，分析是否有异常情况
```

#### 方式二：显式指定 Skill（精确调用）

如果需要明确指定使用该 Skill，可以使用以下格式：

**基本格式：**
```
/dahua-cloud-open-device-image-analysis 从 <设备SN> 抓图并分析 <你的问题>
```

或

```
使用 dahua-cloud-open-device-image-analysis 技能，从 <设备SN> 抓图并分析 <你的问题>
```

**示例：**
```
/dahua-cloud-open-device-image-analysis 从 BA5918431 抓一张图，并分析有没有人
```

```
使用 dahua-cloud-open-device-image-analysis 技能，从 BA5918431 抓图，判断图中是否有白色车辆
```

**适用场景：**
- 当 AI 没有自动识别到你的意图时
- 需要确保使用该特定 Skill 时
- 在多个相似 Skill 中明确选择时

---

### 命令行方式

如果你需要在命令行中直接运行：

```bash
python device_image_analysis.py --device-sn <设备SN> --prompt "<你的问题>"
```

**示例：**
```bash
python device_image_analysis.py \
  --device-sn AD01A01PHACF7AC \
  --prompt "请判断这张图片中是否有人"
```


### 第二步：查看结果

- 图片自动保存到 `captured_images/<设备SN>/` 目录
- AI 分析结果直接显示在对话中

---


##  详细配置指南

**只需要设置 Cloud 凭证**,无需准备设备密码！

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

---

### 方式 2: 命令行快速设置

**适合熟悉命令行的用户！**

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

**适合快速测试！**

**Windows PowerShell (临时):**
```powershell
$env:DAHUA_CLOUD_PRODUCT_ID='your_app_id'
$env:DAHUA_CLOUD_AK='your_access_key'
$env:DAHUA_CLOUD_SK='your_secret_key'
```

**注意**: 仅在当前窗口有效，关闭后失效

---

### 方式 4: Linux/Mac 永久设置

> ⚠️ **安全警告**: 将凭证写入 `~/.bashrc` 会将敏感信息以明文形式持久化存储在磁盘上。建议：
> - 优先使用临时环境变量（方式 3）进行测试
> - 如需永久设置，确保 `~/.bashrc` 文件权限为 600 (`chmod 600 ~/.bashrc`)
> - 定期轮换凭证
> - 不要在共享系统或多用户环境中使用此方法

**添加到启动文件：**

```bash
echo "export DAHUA_CLOUD_PRODUCT_ID='你的 AppID'" >> ~/.bashrc
echo "export DAHUA_CLOUD_AK='你的 AccessKey'" >> ~/.bashrc
echo "export DAHUA_CLOUD_SK='你的 SecretKey'" >> ~/.bashrc
source ~/.bashrc
```

**验证是否生效**:
```bash
echo $DAHUA_CLOUD_PRODUCT_ID
echo $DAHUA_CLOUD_AK
echo $DAHUA_CLOUD_SK
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
- **仅依赖 Cloud 凭证** - 无需设备密码

### 命令行参数

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

##  目录结构

```
skills/dahua-cloud-open-device-image-analysis/
├── README.md                         # 本文件
├── SKILL.md                          # Skill 描述文件（含 GUI 设置指南）
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
