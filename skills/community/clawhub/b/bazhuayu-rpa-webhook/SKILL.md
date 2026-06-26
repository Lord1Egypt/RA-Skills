---
name: bazhuayu-rpa-webhook
description: 八爪鱼 RPA Webhook 调用工具 - 通过 Webhook 触发 RPA 任务运行，支持自定义参数传递
description_en: Octoparse RPA Webhook Tool - Trigger RPA tasks via Webhook with custom parameters
metadata: {"clawdbot":{"emoji":"🐙","requires":{"bins":["python3"],"env":["BAZHUAYU_WEBHOOK_URL","BAZHUAYU_WEBHOOK_KEY"]},"primaryEnv":"BAZHUAYU_WEBHOOK_KEY","install":[{"id":"copy","kind":"copy","label":"复制 Skill 目录","description":"将 bazhuayu-rpa-webhook 目录复制到你的技能目录"}]}}
---

# 八爪鱼 RPA Webhook 调用技能 (Bug 修复版 v2.0.6)

通过 Webhook 触发八爪鱼 RPA 任务运行，支持自定义参数传递。

## ⚠️ 使用前必读

**本技能需要配置以下环境变量才能运行：**

| 变量名 | 说明 | 是否必需 |
|--------|------|----------|
| `BAZHUAYU_WEBHOOK_URL` | 八爪鱼 RPA Webhook 地址 | **必需** |
| `BAZHUAYU_WEBHOOK_KEY` | 签名密钥 | **必需** |

**配置方式（二选一）：**
1. **推荐**：手动添加到 shell 配置文件 (`~/.bashrc` 或 `~/.zshrc`)
2. **临时**：在当前终端会话中使用 `export` 命令

详见下方「🔧 快速配置」章节。

---

## 🔐 安全特性 (v2.0 新增)

- ✅ **环境变量支持** - 敏感信息使用环境变量存储 (优先级高于配置文件)
- ✅ **文件权限保护** - 配置文件自动设置为 600 (仅所有者可读写)
- ✅ **日志脱敏** - 输出自动隐藏敏感信息
- ✅ **安全检查** - `secure-check` 命令帮助发现潜在风险
- ✅ **一键配置** - `setup-secure.sh` 快速安全配置
- ✅ **迁移工具** - `migrate-to-env.sh` 从旧配置迁移

## 📦 安装

### 方式一：从 ClawHub 安装

```bash
clawhub install bazhuayu-webhook
```

### 方式二：手动复制

```bash
# 复制 skill 目录
cp -r ~/.openclaw/workspace/skills/bazhuayu-webhook /你的路径/

# 进入目录
cd /你的路径/bazhuayu-webhook
```

## 🚀 快速配置

### 方式一：运行配置向导（推荐）

```bash
./setup-secure.sh
```

按提示输入 Webhook URL 和签名密钥，脚本会：
- 生成环境变量配置示例
- 更新 `config.json`（密钥留空，从环境变量读取）
- **不会**自动修改你的 shell 配置文件

**配置完成后，请手动将 export 命令添加到 `~/.bashrc` 或 `~/.zshrc`**

### 方式二：手动配置环境变量

编辑 `~/.bashrc` 或 `~/.zshrc`，添加：

```bash
export BAZHUAYU_WEBHOOK_URL="你的 Webhook URL"
export BAZHUAYU_WEBHOOK_KEY="你的签名密钥"
```

然后执行：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

### 方式三：临时配置（仅当前终端会话）

```bash
export BAZHUAYU_WEBHOOK_URL="你的 Webhook URL"
export BAZHUAYU_WEBHOOK_KEY="你的签名密钥"
```

### 验证配置

```bash
python3 bazhuayu-webhook.py secure-check
```

## 🔧 使用方法

### 运行任务（使用默认参数）

```bash
python3 bazhuayu-webhook.py run
```

### 运行任务（指定参数值）

```bash
python3 bazhuayu-webhook.py run --A=新值 --B=新值
```

### 测试模式（不实际发送）

```bash
python3 bazhuayu-webhook.py test
```

### 查看配置

```bash
python3 bazhuayu-webhook.py config
```

### 安全检查 ⭐

```bash
python3 bazhuayu-webhook.py secure-check
```

## 📝 配置文件

`config.json` - 存储 Webhook URL、参数配置（**v2.0 起密钥建议使用环境变量**）

```json
{
  "url": "Webhook 地址",
  "key": "",
  "paramNames": ["A", "B"],
  "defaultParams": {"A": "默认值 A", "B": "默认值 B"},
  "security": {
    "keyFromEnv": true,
    "version": "2.0"
  }
}
```

### 环境变量

| 变量名 | 说明 | 是否必需 | 优先级 |
|--------|------|----------|--------|
| `BAZHUAYU_WEBHOOK_URL` | Webhook URL | **必需** | 高于配置文件 |
| `BAZHUAYU_WEBHOOK_KEY` | 签名密钥 | **必需** | 高于配置文件 |
| `BAZHUAYU_PARAM_*` | 参数默认值 | 可选 | 高于配置文件 |

**如何设置环境变量：**

1. **永久生效**（推荐）：添加到 `~/.bashrc` 或 `~/.zshrc`
   ```bash
   export BAZHUAYU_WEBHOOK_URL="你的 URL"
   export BAZHUAYU_WEBHOOK_KEY="你的密钥"
   ```

2. **临时生效**（仅当前终端）：
   ```bash
   export BAZHUAYU_WEBHOOK_URL="你的 URL"
   export BAZHUAYU_WEBHOOK_KEY="你的密钥"
   ```

## 🔐 签名算法

```
string_to_sign = timestamp + "\n" + key
sign = Base64(HmacSHA256(string_to_sign, message=""))
```

本工具已自动处理签名计算，无需手动操作。

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

## 📁 文件结构

```
bazhuayu-webhook/
├── README.md              # 使用说明
├── QUICKSTART.md          # 5 分钟快速配置指南 ⭐
├── SECURITY.md            # 安全指南
├── MANUAL.md              # 详细使用手册
├── SKILL.md               # 本文件
├── bazhuayu-webhook.py    # 主程序 (安全增强版 v2.0)
├── setup-secure.sh        # 一键安全配置脚本 ⭐
├── migrate-to-env.sh      # 迁移到环境变量脚本
├── config.json            # 配置文件 (敏感，已加入.gitignore)
├── config.example.json    # 配置模板
└── .gitignore             # Git 忽略规则
```

## 📚 文档

- **快速开始**: `QUICKSTART.md` - 5 分钟完成配置
- **详细手册**: `MANUAL.md` - 完整使用指南
- **安全指南**: `SECURITY.md` - 安全最佳实践

## 🆘 常见问题

### Q: 如何配置环境变量？
**A**: 
1. 编辑 `~/.bashrc` 或 `~/.zshrc`
2. 添加 `export BAZHUAYU_WEBHOOK_URL="..."` 和 `export BAZHUAYU_WEBHOOK_KEY="..."`
3. 运行 `source ~/.bashrc` 或 `source ~/.zshrc` 使配置生效
4. 运行 `python3 bazhuayu-webhook.py secure-check` 验证

### Q: 签名验证失败？
**A**: 
1. 检查系统时间是否准确
2. 检查 Key 是否正确（使用环境变量推荐）
3. 运行 `secure-check` 检查配置

### Q: 如何迁移旧配置？
**A**: 运行 `./migrate-to-env.sh` 迁移到环境变量模式，然后手动将生成的 export 命令添加到 shell 配置

### Q: 参数未设置值？
**A**: 检查 `config.json` 中的参数名是否与 RPA 应用中的变量名**完全一致**

### Q: 环境变量不生效？
**A**: 
1. 确认已执行 `source ~/.bashrc` 或 `source ~/.zshrc`
2. 运行 `echo $BAZHUAYU_WEBHOOK_KEY` 检查是否已设置
3. 如使用新终端，需重新执行 source 命令

## 📞 技术支持

- [八爪鱼 RPA 帮助中心](https://rpa.bazhuayu.com/helpcenter)
- [Webhook 触发任务文档](https://rpa.bazhuayu.com/helpcenter/docs/skmvua)
- [API 接口文档](https://rpa.bazhuayu.com/helpcenter/docs/rpaapi)

## 📋 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 2.0.4 | 2026-03-08 | 📸 新增图文教程 - Webhook 设置步骤详解，包含截图示例 |
| 2.0.3 | 2026-03-08 | 🏷️ 名称优化 - 添加 RPA 关键词便于搜索和发现 |
| 2.0.2 | 2026-03-08 | 🔐 日志安全修复 - 新增日志权限自动修复、完善 SKILL.md 元数据环境变量声明 |
| 2.0.1 | 2026-03-08 | 🔧 安全优化 - 修复环境变量元数据、移除脚本自动修改 shell 配置、新增手动配置指南 |
| 2.0.0 | 2026-03-07 | 🔐 安全增强版 - 新增环境变量支持、安全检查、配置脚本 |
| 1.0.1 | 2026-03-07 | 🎉 初始公开发布 |
| 1.0.0 | - | 初始版本（内部迭代） |

## 📄 许可证

MIT License
