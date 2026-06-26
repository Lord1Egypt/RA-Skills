# 八爪鱼 RPA Webhook 调用工具 (安全增强版)

通过 Webhook 触发八爪鱼 RPA 任务运行，支持自定义参数传递。

## 🔐 安全特性

- ✅ **环境变量支持** - 敏感信息可使用环境变量存储 (优先级高于配置文件)
- ✅ **文件权限保护** - 配置文件自动设置为 600 (仅所有者可读写)
- ✅ **日志脱敏** - 输出自动隐藏敏感信息
- ✅ **安全检查** - `secure-check` 命令帮助发现潜在风险

### 推荐配置方式

| 信息类型 | 推荐存储方式 | 说明 |
|----------|--------------|------|
| 签名密钥 | 环境变量 | `BAZHUAYU_WEBHOOK_KEY` |
| Webhook URL | 环境变量或配置文件 | `BAZHUAYU_WEBHOOK_URL` |
| 参数默认值 | 配置文件或环境变量 | 非敏感值可用配置文件 |

---

## 📦 安装

### 方式一：直接复制

```bash
# 复制整个 skill 目录
cp -r /path/to/bazhuayu-webhook ~/your/path/

# 进入目录
cd ~/your/path/bazhuayu-webhook
```

### 方式二：从 ClawHub 安装（待发布）

```bash
clawhub install bazhuayu-webhook
```

---

## 📖 第一步：获取 Webhook URL 和签名

在配置技能之前，首先需要在八爪鱼 RPA 中创建 Webhook 触发器。

### 步骤 1：创建 Webhook 触发器

1. 登录 [八爪鱼 RPA 控制台](https://rpa.bazhuayu.com/)
2. 进入【触发器】栏目
3. 点击 **"Webhook 触发器"**

### 步骤 2：填写触发器信息

按顺序填写：

1. **触发器名称** → 输入易于识别的名称（如：订单处理、数据采集等）
2. **指定运行的机器人** → 选择要执行任务的机器人
3. **选择要运行的应用** → 选择对应的 RPA 应用
4. 点击 **"确定"**

### 步骤 3：获取 Webhook 信息

创建成功后，会显示 Webhook 的详细信息：

- **Webhook URL** → 复制保存（格式：`https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/xxx/invoke`）
- **签名密钥 (Key)** → 复制保存（用于签名验证）

### 步骤 4：启动触发器

⚠️ **重要**：勾选 **"启动触发器"**，否则 Webhook 不会生效！

---

## ⚙️ 第二步：配置技能

### 方式一：运行配置向导（推荐）

```bash
cd ~/.openclaw/workspace/skills/bazhuayu-webhook
./setup-secure.sh
```

按提示输入 Webhook URL 和签名密钥，脚本会：
- ✅ 生成环境变量配置示例
- ✅ 创建安全的配置文件（权限 600）
- ⚠️ **不会**自动修改 Shell 配置文件（需手动添加）

**配置完成后，请手动将 export 命令添加到 `~/.bashrc` 或 `~/.zshrc`**

### 方式二：手动初始化

```bash
python3 bazhuayu-webhook.py init
```

按提示输入以下信息：

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| **Webhook URL** | 八爪鱼 Webhook 接口地址 | 从八爪鱼 RPA 触发器页面复制 |
| **签名密钥 (Key)** | Webhook 的签名密钥 | 从八爪鱼 RPA 触发器页面复制 |
| **参数名称** | RPA 应用的输入变量名 | 如：A, B 或 参数 1, 参数 2 |
| **默认参数值** | 每个参数的默认值 | 可选，方便快速运行 |

按提示输入以下信息：

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| **Webhook URL** | 八爪鱼 Webhook 接口地址 | 从八爪鱼 RPA 触发器页面复制 |
| **签名密钥 (Key)** | Webhook 的签名密钥 | 从八爪鱼 RPA 触发器页面复制 |
| **参数名称** | RPA 应用的输入变量名 | 如：A, B 或 参数 1, 参数 2 |
| **默认参数值** | 每个参数的默认值 | 可选，方便快速运行 |

---

## 🚀 使用方法

### 运行任务（使用默认参数）

```bash
python3 bazhuayu-webhook.py run
```

### 运行任务（指定参数值）

```bash
python3 bazhuayu-webhook.py run --A=值 1 --B=值 2
```

**参数名根据实际配置而定**，例如：
```bash
# 如果参数名是 参数 1 和 参数 2
python3 bazhuayu-webhook.py run --参数 1=李飞 --参数 2=来了

# 如果参数名是 A 和 B
python3 bazhuayu-webhook.py run --A=aa --B=bb
```

### 测试模式（不实际发送）

```bash
python3 bazhuayu-webhook.py test
```

查看将要发送的请求内容，用于调试。

### 查看当前配置

```bash
python3 bazhuayu-webhook.py config
```

### 安全检查

```bash
python3 bazhuayu-webhook.py secure-check
```

检查项目：
- ✅ 配置文件权限是否为 600
- ✅ 敏感信息是否使用环境变量
- ✅ 是否在版本控制中泄露
- ✅ 日志文件权限是否安全

### 迁移到环境变量（已有配置）

如果已有配置存储在 config.json 中，可运行迁移脚本：

```bash
./migrate-to-env.sh
```

功能：
- 从配置文件提取敏感信息
- 生成环境变量配置示例
- 更新 config.json 移除密钥
- 自动备份原配置
- ⚠️ **不会**自动修改 Shell 配置文件（需手动添加）

**迁移完成后，请手动将 export 命令添加到 `~/.bashrc` 或 `~/.zshrc`**

---

## 📁 文件结构

```
bazhuayu-webhook/
├── README.md              # 使用说明（本文件）
├── QUICKSTART.md          # 5 分钟快速配置指南 ⭐
├── WEBHOOK_SETUP.md       # Webhook 设置图文教程 ⭐
├── SECURITY.md            # 安全指南
├── MANUAL.md              # 详细使用手册
├── MANUAL_SETUP.md        # 手动配置指南 ⭐
├── SKILL.md               # Skill 元数据
├── bazhuayu-webhook.py    # 主程序 (安全增强版 v2.0)
├── bazhuayu-webhook       # Shell 快捷命令
├── setup-secure.sh        # 配置向导脚本（不修改 shell 配置）
├── migrate-to-env.sh      # 迁移到环境变量脚本（不修改 shell 配置）
├── config.json            # 配置文件 (敏感，已加入.gitignore)
├── config.example.json    # 配置模板
├── .gitignore             # Git 忽略规则
├── images/                # 图文教程图片
└── *.log                  # 日志文件 (敏感，已加入.gitignore)
```

---

## 📝 配置文件说明

`config.json` 格式：

```json
{
  "url": "https://api-rpa.bazhuayu.com/api/v1/bots/webhooks/xxx/invoke",
  "key": "你的签名密钥",
  "paramNames": ["A", "B"],
  "defaultParams": {
    "A": "默认值 A",
    "B": "默认值 B"
  }
}
```

| 字段 | 说明 |
|------|------|
| `url` | Webhook 接口地址 |
| `key` | 签名密钥（用于计算请求签名） |
| `paramNames` | 参数名称列表 |
| `defaultParams` | 参数默认值（键值对） |

---

## 🔐 签名算法

根据八爪鱼文档，签名计算方式：

```
string_to_sign = timestamp + "\n" + key
sign = Base64(HmacSHA256(string_to_sign, message=""))
```

本工具已自动处理签名计算，无需手动操作。

---

## 📤 返回结果

### 成功响应（HTTP 200）

```json
{
  "enterpriseId": "企业 ID",
  "flowId": "应用 ID",
  "flowProcessNo": "运行批次号"
}
```

### 失败响应（HTTP 400）

```json
{
  "code": "错误码",
  "description": "错误描述"
}
```

常见错误：
- `SignatureVerificationFailureOrTimestampExpired` - 签名错误或时间戳过期
- 检查系统时间是否准确
- 检查 Key 是否正确

---

## 🛠️ 常见问题

### Q: 参数未设置值？
**A**: 检查 `config.json` 中的参数名是否与 RPA 应用中的变量名**完全一致**（包括空格）。

### Q: 签名验证失败？
**A**: 
1. 检查系统时间是否准确
2. 检查 Key 是否正确复制（无多余空格）

### Q: 如何修改默认参数？
**A**: 直接编辑 `config.json` 中的 `defaultParams` 部分。

---

## 📞 技术支持

如有问题，请联系技能作者或参考八爪鱼官方文档：
- [Webhook 触发任务](https://rpa.bazhuayu.com/helpcenter/docs/skmvua)
- [API 接口文档](https://rpa.bazhuayu.com/helpcenter/docs/rpaapi)
