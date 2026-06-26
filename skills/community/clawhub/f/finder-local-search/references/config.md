# Finder Skill 配置说明

这个 skill 不依赖自定义 CLI，直接通过 Finder 开放接口工作。

## 默认地址

- 站点首页：`https://finder.optell.com`
- 访问密钥页面：`https://finder.optell.com/api-key`
- 接口基础地址：`https://finder.optell.com/api`

## 第一次使用

1. 打开 `https://finder.optell.com` 注册或登录。
2. 打开 `https://finder.optell.com/api-key`。
3. 生成并复制访问密钥。
4. 在本地创建 Finder 配置目录和配置文件。

如果用户已经把 key 直接贴给 Codex，优先让 Codex 直接帮用户保存，不要再要求手工重复输入。

更友好的引导话术可以是：

```text
我先帮你把 Finder 配置接起来。
你先去 https://finder.optell.com/api-key 生成一份访问秘钥，拿到后直接发给我，我可以继续帮你创建本地配置文件。
```

## 本地配置文件

- macOS / Linux：`~/.finder/config.json`
- Windows PowerShell：`$HOME/.finder/config.json`

推荐内容：

```json
{
  "base_url": "https://finder.optell.com",
  "api_key": "<你的访问密钥>",
  "last_project_id": null
}
```

## 创建本地配置文件

macOS / Linux:

```bash
mkdir -p "$HOME/.finder"
cat > "$HOME/.finder/config.json" <<EOF
{
  "base_url": "https://finder.optell.com",
  "api_key": "<你的访问密钥>",
  "last_project_id": null
}
EOF
```

Windows PowerShell:

```powershell
$finderDir = Join-Path $HOME ".finder"
$configPath = Join-Path $finderDir "config.json"
New-Item -ItemType Directory -Force -Path $finderDir | Out-Null
$config = @{
  base_url = "https://finder.optell.com"
  api_key = "<你的访问密钥>"
  last_project_id = $null
} | ConvertTo-Json
Set-Content -Path $configPath -Value $config -Encoding UTF8
```

## 校验访问密钥

macOS / Linux:

```bash
KEY=$(python3 - <<'PY'
import json, os
path = os.path.expanduser("~/.finder/config.json")
print(json.load(open(path)).get("api_key", ""))
PY
)
curl -X GET 'https://finder.optell.com/api/user/me' \
  -H "Authorization: Bearer $KEY"
```

Windows PowerShell:

```powershell
$config = Get-Content "$HOME/.finder/config.json" | ConvertFrom-Json
$headers = @{
  Authorization = "Bearer $($config.api_key)"
}

Invoke-RestMethod -Method Get `
  -Uri "https://finder.optell.com/api/user/me" `
  -Headers $headers
```

## 项目相关命令

列出项目：

```bash
KEY=$(python3 - <<'PY'
import json, os
path = os.path.expanduser("~/.finder/config.json")
print(json.load(open(path)).get("api_key", ""))
PY
)
curl -X POST 'https://finder.optell.com/api/project/list' \
  -H "Authorization: Bearer $KEY"
```

```powershell
$config = Get-Content "$HOME/.finder/config.json" | ConvertFrom-Json
$headers = @{
  Authorization = "Bearer $($config.api_key)"
}

Invoke-RestMethod -Method Post `
  -Uri "https://finder.optell.com/api/project/list" `
  -Headers $headers
```

创建默认项目：

```bash
KEY=$(python3 - <<'PY'
import json, os
path = os.path.expanduser("~/.finder/config.json")
print(json.load(open(path)).get("api_key", ""))
PY
)
curl -X POST 'https://finder.optell.com/api/project/create' \
  -H "Authorization: Bearer $KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Finder Skill 默认项目",
    "description": "由 Finder skill 自动创建"
  }'
```

```powershell
$config = Get-Content "$HOME/.finder/config.json" | ConvertFrom-Json
$headers = @{
  Authorization = "Bearer $($config.api_key)"
  "Content-Type" = "application/json"
}

$body = @{
  name = "Finder Skill 默认项目"
  description = "由 Finder skill 自动创建"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "https://finder.optell.com/api/project/create" `
  -Headers $headers `
  -Body $body
```

## 搜索命令模板

macOS / Linux:

```bash
KEY=$(python3 - <<'PY'
import json, os
path = os.path.expanduser("~/.finder/config.json")
print(json.load(open(path)).get("api_key", ""))
PY
)
curl -X POST 'https://finder.optell.com/api/creator/search' \
  -H "Authorization: Bearer $KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "projectId": 123,
    "platform": "TikTok",
    "keyword": "beauty",
    "minFollowerCount": 100000,
    "maxFollowerCount": 500000
  }'
```

Windows PowerShell:

```powershell
$config = Get-Content "$HOME/.finder/config.json" | ConvertFrom-Json
$headers = @{
  Authorization = "Bearer $($config.api_key)"
  "Content-Type" = "application/json"
}

$body = @{
  projectId = 123
  platform = "TikTok"
  keyword = "beauty"
  minFollowerCount = 100000
  maxFollowerCount = 500000
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "https://finder.optell.com/api/creator/search" `
  -Headers $headers `
  -Body $body
```

## 常见错误

- `未设置访问密钥`
  - 先去 `https://finder.optell.com/api-key` 生成密钥，再创建 `~/.finder/config.json`。
- `API Key 无权访问该接口`
  - 说明调用了普通达人搜索白名单之外的接口。
- `搜索次数已超出当前限制。如需增加使用量，请发送邮件至 developer.optell@gmail.com`
  - 说明当前账号的达人搜索次数已达到限制。
  - 引导用户发送邮件到 `developer.optell@gmail.com` 申请增加使用量。
- `没有可用项目`
  - 先调用项目列表接口；如果为空，先创建项目再搜索。
- `已经配置过但还是读不到`
  - 请确认本地存在 `~/.finder/config.json`，并且文件里有 `api_key` 字段。

## 推荐反馈语句

- 保存成功后：

```text
我已经帮你把访问秘钥写到 ~/.finder/config.json 里了，后面就不用再重复输入这串 key 了。
```

- 继续下一步前：

```text
配置已经就绪，我继续帮你检查项目并开始搜索。
```

- 没有项目时：

```text
Finder 会把这次搜索挂在一个项目下面，方便你后面继续查看。你现在还没有项目，要我顺手帮你建一个默认项目吗？
```
