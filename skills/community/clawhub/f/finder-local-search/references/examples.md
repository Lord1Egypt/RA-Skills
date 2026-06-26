# 示例对话

## 首次使用

用户：

```text
帮我搜 TikTok 上美国英语区的美妆达人
```

助手行为：

1. 检查当前环境里是否已有 `~/.finder/config.json`。
2. 如果认证未完成，引导用户：
   - 登录 Finder
   - 打开 `/api-key`
   - 生成并复制访问密钥，然后创建本地配置文件
3. 查询项目列表。
4. 如果没有项目，先询问是否创建默认项目。
5. 用户确认后，创建项目并继续搜索。
6. 如果当前环境能执行命令，直接执行搜索；否则给出命令模板，例如：

更友好的示例回复：

```text
我先帮你检查一下 Finder 配置。
如果还没配好访问秘钥也没关系，你把秘钥发给我，我可以接着帮你创建本地配置文件，然后继续这次搜索，不用你重新描述一遍。
```

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
    "regions": ["美国"],
    "languages": ["英语"],
    "labels": ["美妆"]
  }'
```

## 用户还没有注册或登录

用户：

```text
帮我搜美国美妆达人
```

助手行为：

1. 先检查 `~/.finder/config.json` 是否已配置。
2. 如果发现没有本地配置，直接说明：

```text
我还没有找到 Finder 本地配置文件。
你先注册或登录 Finder，然后打开 https://finder.optell.com/api-key 生成一份访问秘钥。
拿到后你可以直接发给我，我可以继续帮你创建 ~/.finder/config.json，然后接着搜索。
```

3. 用户说“已经配置好了”后，再继续原来的搜索请求，不要求用户重新描述需求。

## 用户直接把访问密钥发到对话里

用户：

```text
这是我的 api key：finder_xxx
```

助手行为：

1. 不重复回显完整 key。
2. 如果当前环境支持命令执行，直接帮用户保存：

macOS / Linux:

```bash
mkdir -p "$HOME/.finder"
cat > "$HOME/.finder/config.json" <<EOF
{
  "base_url": "https://finder.optell.com",
  "api_key": "finder_xxx",
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
  api_key = "finder_xxx"
  last_project_id = $null
} | ConvertTo-Json
Set-Content -Path $configPath -Value $config -Encoding UTF8
```

3. 保存成功后直接继续当前搜索，不要求用户再次输入 key。

保存成功后的推荐回复：

```text
我已经帮你把访问秘钥写到 ~/.finder/config.json 里了，后面就不用再重复输入这串 key 了。
我继续帮你检查项目，然后接着搜。
```

## 日常使用

用户：

```text
帮我找 10 万到 50 万粉丝的 TikTok 母婴达人，美国，英文
```

助手行为：

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
    "regions": ["美国"],
    "languages": ["英语"],
    "labels": ["母婴"],
    "minFollowerCount": 100000,
    "maxFollowerCount": 500000
  }'
```

## 条件不完整时

用户：

```text
帮我找一些适合带货的达人
```

助手只追问必要条件，例如：

```text
你想搜哪个平台？另外要不要限制地区、语言或粉丝量级？
```

## 没有项目时

用户：

```text
继续搜
```

助手行为：

1. 发现当前没有可用项目。
2. 简要说明：

```text
Finder 会把这次搜索挂在一个项目下面，方便你后面继续查看和筛选。
你现在还没有项目，要我顺手帮你建一个默认项目吗？
```

3. 用户确认后调用：

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

## 搜索次数超限时

如果搜索接口返回：

```text
搜索次数已超出当前限制。如需增加使用量，请发送邮件至 developer.optell@gmail.com
```

推荐回复：

```text
你当前的搜索次数已经达到限制了。
如果你想增加使用量，可以发邮件到 developer.optell@gmail.com 申请开通，我也可以顺手帮你整理一段邮件内容。
```
