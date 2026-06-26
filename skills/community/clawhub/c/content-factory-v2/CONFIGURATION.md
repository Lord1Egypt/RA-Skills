# 配置管理说明

## 凭证存储位置

所有 API 密钥和凭证现在统一存储在 `.env` 文件中：

```
content-factory/
├── .env                    # 实际配置文件（包含真实凭证，不提交到 Git）
├── .env.example            # 配置模板（可以提交到 Git）
└── scripts/
    ├── generate_cover_photo.py  # 自动加载 .env
    ├── wechat_publish.py        # 自动加载 .env
    └── check_env.py             # 检查配置
```

## 配置项说明

### 必需配置

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| `GLM_API_KEY` | 智谱 AI API 密钥 | https://open.bigmodel.cn/ |

### 可选配置

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| `WECHAT_APP_ID` | 微信公众号 AppID | https://mp.weixin.qq.com/ → 设置与开发 → 基本配置 |
| `WECHAT_APP_SECRET` | 微信公众号 AppSecret | 同上 |

## 配置优先级

脚本按以下优先级读取配置：

### 1. 命令行参数（最高优先级）
```bash
python scripts/generate_cover_photo.py \
  --api-key "your-api-key-here" \
  --title "测试" \
  --theme "测试" \
  --output "test.png"
```

### 2. 环境变量
```bash
# PowerShell
$env:GLM_API_KEY="your-api-key-here"

# Bash
export GLM_API_KEY="your-api-key-here"
```

### 3. .env 文件（推荐）
```env
GLM_API_KEY=your-api-key-here
WECHAT_APP_ID=your-app-id
WECHAT_APP_SECRET=your-app-secret
```

### 4. wechat_config.py（已弃用）
```python
# 旧方式，不推荐使用
APPID = "wxf9400829e3405317"
APPSECRET = "a6800143c01df2e73121c631cac4ec32"
```

### 5. 硬编码默认值（最低优先级）
仅作为后备方案，不应依赖。

## 自动加载机制

### generate_cover_photo.py
```python
# 脚本启动时自动加载 .env
script_dir = Path(__file__).parent.parent
env_path = script_dir / ".env"
if env_path.exists():
    load_env_file(env_path)
```

### wechat_publish.py
```python
# 同样自动加载 .env
script_dir = Path(__file__).parent.parent
env_path = script_dir / ".env"
if env_path.exists():
    load_env_file(env_path)

# 优先级：环境变量 > wechat_config.py > 默认值
APPID = os.environ.get('WECHAT_APP_ID', 'default-value')
APPSECRET = os.environ.get('WECHAT_APP_SECRET', 'default-value')
```

## 配置文件示例

### .env（实际配置）
```env
# GLM-Image API Configuration (Required)
GLM_API_KEY=sk-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

# WeChat Official Account Credentials (Optional)
WECHAT_APP_ID=wxf9400829e3405317
WECHAT_APP_SECRET=a6800143c01df2e73121c631cac4ec32
```

### .env.example（模板）
```env
# GLM-Image API Configuration (Required)
# Get your API key from: https://open.bigmodel.cn/
GLM_API_KEY=your-api-key-here

# WeChat Official Account Credentials (Optional - for auto-publishing)
# Get these from: https://mp.weixin.qq.com/
WECHAT_APP_ID=your-app-id-here
WECHAT_APP_SECRET=your-app-secret-here
```

## 安全最佳实践

### ✅ 推荐做法

1. **使用 .env 文件**
   - 项目级配置，易于管理
   - 不同环境可以使用不同的配置

2. **添加到 .gitignore**
   ```gitignore
   # Environment variables
   .env
   .env.local
   .env.*.local

   # Keep the example file
   !.env.example
   ```

3. **定期轮换密钥**
   - 每 3-6 个月更换一次
   - 怀疑泄露时立即更换

4. **使用环境变量（生产环境）**
   - 服务器部署时使用系统环境变量
   - 不要在服务器上存储 .env 文件

### ❌ 避免做法

1. **不要硬编码**
   ```python
   # ❌ 错误
   API_KEY = "sk-abc123..."

   # ✅ 正确
   API_KEY = os.environ.get('GLM_API_KEY')
   ```

2. **不要提交到 Git**
   ```bash
   # 检查是否误提交
   git status

   # 如果已提交，立即删除
   git rm --cached .env
   git commit -m "Remove .env file"
   ```

3. **不要分享截图**
   - 截图前遮盖敏感信息
   - 不要在公开场合展示配置

## 迁移指南

### 从 wechat_config.py 迁移到 .env

如果你之前使用 `wechat_config.py`：

1. **创建 .env 文件**：
   ```bash
   cd C:\Users\jeffl\.claude\skills\content-factory
   copy .env.example .env
   ```

2. **复制凭证**：
   从 `wechat_config.py` 复制 `APPID` 和 `APPSECRET` 到 `.env`

3. **删除旧文件**（可选）：
   ```bash
   # 备份
   copy scripts\wechat_config.py scripts\wechat_config.py.bak

   # 删除
   del scripts\wechat_config.py
   ```

4. **验证配置**：
   ```bash
   python scripts/check_env.py
   ```

## 故障排除

### 问题：脚本找不到 .env 文件

**原因**：.env 文件位置不对

**解决方案**：
```bash
# .env 应该在 content-factory 根目录
cd C:\Users\jeffl\.claude\skills\content-factory
dir .env

# 如果不存在，创建它
copy .env.example .env
notepad .env
```

### 问题：配置不生效

**原因**：可能被其他优先级更高的配置覆盖

**解决方案**：
```bash
# 检查环境变量
echo $env:GLM_API_KEY

# 清除环境变量
Remove-Item Env:\GLM_API_KEY

# 重新运行脚本
python scripts/check_env.py
```

### 问题：微信发布失败

**原因**：微信凭证未配置或无效

**解决方案**：
1. 检查 `.env` 文件中的 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET`
2. 登录微信公众平台验证凭证是否正确
3. 运行检查脚本：`python scripts/check_env.py`

## 验证配置

### 完整检查
```bash
python scripts/check_env.py
```

**期望输出**：
```
============================================================
🔑 Environment Configuration Checker
============================================================

📄 Loading environment from: C:\Users\jeffl\.claude\skills\content-factory\.env
   ✅ GLM_API_KEY = sk-abc123de...
   ✅ WECHAT_APP_ID = wxf9400829...
   ✅ WECHAT_APP_SECRET = a6800143c0...

🔍 Checking API keys and credentials...

📌 Required:
   ✅ GLM_API_KEY: sk-abc123de...
      (GLM-Image API (required for cover generation))

📌 Optional (for WeChat auto-publishing):
   ✅ WECHAT_APP_ID: wxf9400829...
      (WeChat Official Account AppID (for auto-publishing))
   ✅ WECHAT_APP_SECRET: a6800143c0...
      (WeChat Official Account AppSecret (for auto-publishing))

   ℹ️  WeChat auto-publishing is fully configured!

============================================================
✅ All required API keys are configured!
   You can now use the cover photo generation script.
============================================================
```

### 快速测试
```bash
# 测试封面生成
python scripts/generate_cover_photo.py \
  --title "测试" \
  --theme "测试" \
  --output "output/test.png"

# 测试微信发布（需要 HTML 文件）
python scripts/wechat_publish.py \
  --html "output/test.html" \
  --cover "output/test.png"
```

## 总结

- ✅ **统一配置**：所有凭证存储在 `.env` 文件
- ✅ **自动加载**：脚本启动时自动读取
- ✅ **优先级清晰**：命令行 > 环境变量 > .env > 默认值
- ✅ **安全可靠**：不提交到 Git，易于管理
- ✅ **向后兼容**：仍支持旧的 `wechat_config.py` 方式

**推荐配置方式**：使用 `.env` 文件（简单、安全、易于管理）
