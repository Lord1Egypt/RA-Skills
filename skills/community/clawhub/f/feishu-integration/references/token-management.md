# Token 管理详解

## 问题背景

飞书的 `tenant_access_token` 有效期只有 **2 小时**（7200 秒），过期后需要重新获取。

## 解决方案

### 方案 1: 本地缓存（推荐）

使用 `feishu-auth.sh` 脚本自动管理：

```bash
# 获取有效 token（自动处理缓存和刷新）
TOKEN=$(bash feishu-auth.sh get)

# 强制刷新 token
bash feishu-auth.sh refresh
```

**缓存机制**:
- Token 存储在 `/tmp/feishu_token_cache.json`
- 提前 60 秒过期（避免边界情况）
- 过期后自动获取新 token

### 方案 2: 环境变量（简单场景）

```bash
# 手动获取并设置
export FEISHU_TOKEN=$(curl -s ... | jq -r '.tenant_access_token')

# 使用时
curl -H "Authorization: Bearer $FEISHU_TOKEN" ...
```

**缺点**: 需要手动刷新，容易过期。

### 方案 3: 配置中心（生产环境）

对于生产环境，建议使用配置中心或密钥管理服务：

```bash
# 从配置中心获取
curl -X GET "https://config-center/api/feishu/token" \
  -H "Authorization: Bearer ${SERVICE_TOKEN}"
```

## 安全建议

1. **不要硬编码 secret**: 使用环境变量或配置文件
2. **定期轮换 secret**: 建议每 90 天更换一次
3. **最小权限原则**: 只申请需要的权限
4. **监控调用**: 记录 token 获取次数，异常时告警

## 配置示例

### 配置文件 (config/feishu.env)

```bash
FEISHU_APP_ID=cli_a90da2f009f8dbb3
FEISHU_APP_SECRET=$FEISHU_APP_SECRET
```

**权限设置**:
```bash
chmod 600 config/feishu.env
```

### 多应用配置

如需管理多个应用，创建多个配置文件：

```
config/
├── feishu.env          # 默认配置
├── feishu-bot.env      # 机器人应用
└── feishu-admin.env    # 管理应用
```

使用时指定：
```bash
FEISHU_CONFIG=config/feishu-bot.env ./script.sh
```

## 故障排查

### Token 获取失败

```bash
# 检查配置
cat config/feishu.env

# 测试网络
curl -I https://open.feishu.cn

# 手动获取看错误信息
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "cli_a90da2f009f8dbb3",
    "app_secret": "YOUR_SECRET"
  }'
```

### Token 过期

```bash
# 删除缓存强制刷新
rm /tmp/feishu_token_cache.json

# 或调用刷新命令
bash feishu-auth.sh refresh
```

## 扩展: 自动刷新 Cron

如需确保 token 永不过期，可设置定时任务：

```bash
# crontab -e
# 每 30 分钟刷新一次 token
*/30 * * * * /path/to/feishu-auth.sh refresh > /dev/null 2>&1
```

## 扩展: 多租户支持

如需支持多个租户，修改脚本接受 tenant 参数：

```bash
# feishu-auth.sh
get_feishu_token() {
  local tenant=${1:-default}
  local cache_file="/tmp/feishu_token_${tenant}.json"
  # ...
}
```

使用时：
```bash
TOKEN=$(get_feishu_token "company_a")
```
