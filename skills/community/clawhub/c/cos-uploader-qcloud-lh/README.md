# COS 照片上传助手

> OpenClaw Skill — 通过微信接收照片，自动上传到腾讯云 COS 低频存储

## 功能特性

- 📷 **微信收图** — 通过 OpenClaw 接收微信发送的照片
- ☁️ **内网上传** — 使用腾讯云内网域名，零流量费用（也支持外网）
- 💰 **灵活存储** — 支持标准/低频/归档存储，按需选择
- 📁 **智能归档** — 按 `年/月/月日_随机数.扩展名` 自动归档
- 🔐 **全量加密** — 桶名、Region、SecretId/SecretKey 全部 Fernet 加密存储，源码零敏感信息
- 📦 **大文件支持** — 超过 20MB 自动切换分块上传

## 前置条件

在安装此 Skill 之前，请确保你已经具备以下条件：

| 条件 | 说明 |
|------|------|
| **腾讯云服务器**（推荐） | 如需使用内网上传（免流量费），服务器需在腾讯云同区域内网中 |
| **OpenClaw 已安装** | 服务器上已安装并运行 OpenClaw，且已绑定微信 Channel |
| **Python 3.6+** | 服务器上已安装 Python 3.6 或更高版本 |
| **腾讯云 COS 桶** | 已创建 COS 存储桶（[前往创建](https://console.cloud.tencent.com/cos/bucket)） |
| **腾讯云 API 密钥** | 已获取 SecretId 和 SecretKey（[前往获取](https://console.cloud.tencent.com/cam/capi)） |

### 如何获取腾讯云 API 密钥

1. 登录 [腾讯云控制台](https://console.cloud.tencent.com/)
2. 进入 **访问管理** → **API 密钥管理**（或直接访问 https://console.cloud.tencent.com/cam/capi）
3. 点击 **新建密钥**，记录 `SecretId` 和 `SecretKey`
4. ⚠️ **强烈建议**：创建子账号密钥，仅授予 COS 写入权限，不要使用主账号密钥

### 如何查看 COS 桶名和 Region

1. 登录 [COS 控制台](https://console.cloud.tencent.com/cos/bucket)
2. 在桶列表中找到你的桶，记录：
   - **桶名称**：格式为 `<自定义名称>-<APPID>`（如 `my-photos-1250000000`）
   - **所属地域**：对应 Region（如广州 → `ap-guangzhou`）

### COS 桶权限建议

为了安全，建议将 COS 桶设置为 **私有读写**：
1. 登录 [COS 控制台](https://console.cloud.tencent.com/cos)
2. 进入桶 → **权限管理** → **存储桶访问权限**
3. 确认为 **私有读写**（默认即是）

## 安装步骤

### 第一步：上传 Skill 包到服务器

**方式 A：从打包文件安装（推荐）**

```bash
# 在本地打包（如果你有源码）
./package.sh

# 上传到服务器
scp cos-photo-uploader-v1.0.0.tar.gz root@<你的服务器IP>:/opt/openclaw/skills/
```

**方式 B：直接克隆/复制源码到服务器**

```bash
# 在服务器上创建 Skill 目录
mkdir -p /opt/openclaw/skills/cos-photo-uploader

# 将整个项目文件复制到服务器（使用 scp 或其他方式）
scp -r ./* root@<你的服务器IP>:/opt/openclaw/skills/cos-photo-uploader/
```

### 第二步：在服务器上解压（仅方式 A 需要）

```bash
# SSH 登录到服务器
ssh root@<你的服务器IP>

# 进入 Skill 目录
cd /opt/openclaw/skills/

# 解压
mkdir -p cos-photo-uploader
tar xzf cos-photo-uploader-v1.0.0.tar.gz -C cos-photo-uploader
```

### 第三步：执行安装脚本

```bash
cd /opt/openclaw/skills/cos-photo-uploader

# 赋予执行权限
chmod +x install.sh run.sh

# 执行安装
./install.sh
```

安装脚本会自动完成以下操作：
- ✅ 检查 Python3 环境
- ✅ 创建 Python 虚拟环境（`venv/`）
- ✅ 安装 pip 依赖（`cos-python-sdk-v5`、`cryptography`）
- ✅ 设置文件权限
- ✅ 创建 `scripts/conf/` 和 `scripts/logs/` 目录

### 第四步：配置 COS（桶信息 + API 密钥）

这是最关键的一步，配置工具会引导你一次性输入所有必要信息：

```bash
# 使用虚拟环境中的 Python 运行配置工具
./venv/bin/python3 scripts/setup_config.py
```

配置工具分 4 步引导你完成：

```
========================================================
  腾讯云 COS 配置工具（桶信息 + 密钥 一站式配置）
========================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📦 第一步：COS 桶信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  请输入 COS 桶名（如 my-bucket-1250000000）: baby-gallery-1301557826
  请输入 COS Region（如 ap-guangzhou）: ap-guangzhou

  存储类型选择：
    1. 标准存储（访问频繁，成本较高）
    2. 低频存储（访问较少，成本较低，推荐） 👈 推荐
    3. 归档存储（极少访问，成本最低，取回需等待）
  请选择存储类型 [1/2/3]（默认 2-低频存储）: 2

  网络模式：
    1. 内网上传（服务器在腾讯云同区域内网，免流量费，推荐）
    2. 外网上传（服务器不在腾讯云内网）
  请选择网络模式 [1/2]（默认 1-内网）: 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔑 第二步：腾讯云 API 密钥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  请输入 SecretId: AKID****
  请输入 SecretKey（输入不可见）:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 第三步：确认配置信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  桶名称:     baby-gallery-1301557826
  Region:     ap-guangzhou
  存储类型:   低频存储（访问较少，成本较低，推荐）
  网络模式:   内网上传
  SecretId:   AKID**...****
  SecretKey:  ****（已隐藏）

  以上信息是否正确？(Y/n): y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💾 第四步：保存并验证
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✅ COS 配置已加密保存
  ✅ 配置文件读取验证成功
  ✅ 桶连通性验证成功

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎉 配置完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

所有配置信息（桶名、Region、存储类型、网络模式、SecretId、SecretKey）都会加密保存到 `scripts/conf/cos_secret.enc`，**源代码中不包含任何敏感信息**。

### 第五步：测试上传

在正式使用前，先测试一下上传功能是否正常：

```bash
# 准备一张测试图片（可以从网上下载一张）
wget -O /tmp/test.jpg https://via.placeholder.com/100

# 使用调试模式直接上传
./run.sh --file /tmp/test.jpg
```

如果一切正常，你会看到：

```
✅ 照片上传成功！
📁 存储路径: 2026/03/0326_a3f8b2.jpg
📦 文件大小: 2.1 KB
🏷️ 存储类型: 低频存储
```

你可以登录 [COS 控制台](https://console.cloud.tencent.com/cos) 确认文件已上传。

### 第六步：注册到 OpenClaw

现在需要告诉 OpenClaw 使用这个 Skill 来处理图片消息。

#### 方法：在 OpenClaw 配置中添加 Skill

根据你的 OpenClaw 版本，在配置文件中添加 Skill 注册信息。通常需要配置：

- **Skill 名称**: `cos-photo-uploader`
- **触发条件**: 当消息包含 `[media attached:` 且 MIME 类型为 `image/*` 时触发
- **执行命令**: `/opt/openclaw/skills/cos-photo-uploader/run.sh`
- **参数传递**: OpenClaw 会将完整的 JSON 消息体作为命令行参数传入

具体配置方式请参考 OpenClaw 官方文档中关于 Skill 注册的部分。

### 第七步：验证完整流程

1. 打开微信，向绑定了 OpenClaw 的微信号发送一张照片
2. 等待几秒钟，你应该会收到类似回复：
   ```
   ✅ 照片上传成功！
   📁 存储路径: 2026/03/0326_a3f8b2.jpg
   📦 文件大小: 1.23 MB
   🏷️ 存储类型: 低频存储
   ```
3. 登录 COS 控制台确认文件已正确上传到对应的年月文件夹中

## 工作流程

```
微信发送照片
    ↓
OpenClaw 接收消息，图片缓存到本地
（路径：/root/.openclaw/media/inbound/xxx.jpg）
    ↓
OpenClaw 调用 run.sh '<JSON消息体>'
    ↓
skill_handler.py 解析消息，提取图片路径
    ↓
cos_uploader.py 从加密配置读取桶信息和密钥
    ↓
通过内网/外网上传到 COS，设置指定存储类型
    ↓
返回上传结果，OpenClaw 回复微信用户
```

## 存储路径规则

| 原始文件 | COS 存储路径 |
|---------|-------------|
| `IMG2762---xxx.jpg` | `2026/03/0326_a3f8b2.jpg` |
| `photo.png` | `2026/03/0326_k9m2x1.png` |

格式：`年份/月份/月日_6位随机字符串.扩展名`

## 配置说明

### 所有配置均加密存储

本项目的所有敏感配置（桶名、Region、存储类型、网络模式、API 密钥）均通过 `setup_config.py` 交互式配置，使用 Fernet 对称加密后存储，**源代码中不包含任何 COS 敏感信息**。

如需修改配置，重新运行配置工具即可：
```bash
./venv/bin/python3 scripts/setup_config.py
```

配置工具支持以下参数：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| COS 桶名 | 格式为 `<名称>-<APPID>` | `baby-gallery-1301557826` |
| COS Region | 桶所在区域 | `ap-guangzhou` |
| 存储类型 | 标准/低频/归档 | `STANDARD_IA`（低频） |
| 网络模式 | 内网（免流量费）或外网 | 内网 |
| SecretId | 腾讯云 API 密钥 ID | `AKID****` |
| SecretKey | 腾讯云 API 密钥 Key | `****` |

### 加密文件说明

| 文件 | 路径 | 权限 | 说明 |
|------|------|------|------|
| 加密配置 | `scripts/conf/cos_secret.enc` | 600 | 加密后的全部 COS 配置 |
| 加密密钥 | `scripts/conf/.encryption_key` | 600 | Fernet 加密密钥 |
| 配置目录 | `scripts/conf/` | 700 | 仅所有者可访问 |

## 支持的图片格式

JPEG、PNG、GIF、BMP、WebP、HEIC、HEIF、TIFF

## 常见问题

### Q: 上传失败，提示"无法连接 COS 服务"

**A:** 如果你在配置时选择了"内网上传"，请确认服务器在腾讯云同区域内网中。如果服务器不在腾讯云内网，请重新运行 `setup_config.py`，在网络模式中选择"外网上传"。

### Q: 上传失败，提示"COS 访问被拒绝"

**A:** 请检查：
1. SecretId/SecretKey 是否正确（重新运行 `setup_config.py`）
2. API 密钥是否有 COS 写入权限
3. 桶名称是否正确

### Q: 如何查看上传日志？

**A:** 日志文件在 `scripts/logs/` 目录下，按日期命名：
```bash
cat scripts/logs/upload_20260326.log
```

### Q: 如何修改存储路径规则？

**A:** 编辑 `scripts/cos_uploader.py` 中的 `_generate_cos_key` 函数。

### Q: 配置文件丢失怎么办？

**A:** 如果 `scripts/conf/.encryption_key` 或 `scripts/conf/cos_secret.enc` 被删除，需要重新运行 `setup_config.py` 重新配置所有信息。

### Q: 如何更换 COS 桶或 Region？

**A:** 直接重新运行配置工具即可，无需修改任何代码：
```bash
./venv/bin/python3 scripts/setup_config.py
```

## 目录结构

```
cos-photo-uploader/
├── SKILL.md                    # 技能清单
├── README.md                   # 本文档
├── run.sh                      # 运行入口（OpenClaw 调用此脚本）
├── install.sh                  # 安装脚本
├── package.sh                  # 打包脚本
├── .gitignore                  # Git 忽略规则
├── scripts/                    # 技能代码
│   ├── skill_handler.py        #   Skill 处理入口
│   ├── cos_uploader.py         #   COS 上传核心模块
│   ├── config.py               #   加密配置管理
│   ├── setup_config.py         #   一站式配置工具（桶信息 + 密钥）
│   ├── requirements.txt        #   Python 依赖
│   ├── conf/                   #   加密配置目录（运行时生成）
│   └── logs/                   #   日志目录（运行时生成）
├── screenshots/                # 截图
│   └── .gitkeep
└── venv/                       # Python 虚拟环境（安装时生成）
```

## COS Python SDK

本项目使用腾讯云官方 COS Python SDK：
- GitHub: https://github.com/tencentyun/cos-python-sdk-v5
- 文档: https://cloud.tencent.com/document/product/436/12269

## 许可证

MIT
