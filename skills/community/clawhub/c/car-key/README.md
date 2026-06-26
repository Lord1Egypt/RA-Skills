# Tika Digital Key Skill

用于查询车辆位置和车况信息的 Skill 示例项目。  
Sample Skill project for querying vehicle location and vehicle condition data.

## 前置条件 / Prerequisites

使用本 Skill 的前提，是你的爱车已经加装 乘趣 数字钥匙产品。  
To use this Skill, your vehicle must already be equipped with the Tika Digital Key product.

国内乘趣官网 / Official website: `https://www.chengqukey.com/`
海外Tika 官网 / Official website: `https://www.tikakey.com/`

产品加装完成后，请先下载 App 并完成车辆绑定。  
After the product is installed, download the App and complete vehicle binding first.

然后参考这段流程获取 Tika API Key：  
Then use the following process to get your Tika API Key:

在乘趣 App 的「帮助中心 -> 热门功能 -> Skill」中获取完整 API Key，随后即可开始使用。  
In the Tika App, go to `Help Center -> Popular Features -> Skill` to obtain the full API Key, then you can start using this Skill.

## 当前能力 / Features

- 查询车辆当前位置 / Query current vehicle location
- 查询车辆基础车况 / Query vehicle condition
- 输出结构化 JSON 数据 / Output structured JSON data
- 通过缓存文件或命令行参数管理认证信息 / Manage authentication by cache file or CLI arguments
- 支持中英文 CLI 输出 / Support bilingual CLI output in Chinese and English

## 项目结构 / Project Structure

```text
.
├── LICENSE
├── README.md
├── SKILL.md
├── _meta.json
└── query_vehicle.py
```

## 认证信息 / Authentication

推荐的首次配置方式 / Recommended first-time setup:

1. 在 App 中获取完整 `API Key` / Get the full `API Key` from the App
2. 先用环境变量完成首次配置 / Use an environment variable for the first setup
3. 执行查询命令验证是否生效 / Run a query command to confirm it works

推荐命令 / Recommended command:

```bash
export TIKA_API_KEY='your_full_api_key'
python3 query_vehicle.py
python3 query_vehicle.py --check-auth
```

如果你需要长期在本机反复使用，再写入本地缓存。  
If you plan to use the skill repeatedly on the same machine, then save the API Key to local cache.

脚本默认使用以下缓存文件：  
The script uses the following cache file by default:

`~/.skill_carkey_cache.json`

缓存文件示例 / Cache file example:

```json
{
  "apiKey": "your_full_api_key"
}
```

推荐优先通过系统环境变量读取认证信息：  
The recommended approach is to provide authentication through an environment variable:

```bash
export TIKA_API_KEY='your_full_api_key'
python3 query_vehicle.py
```

如果你希望后续免配置使用，也可以通过命令行传入 App 生成的完整 API Key 并写入缓存：  
If you want future runs to work without reconfiguration, you can also pass the full App-generated API Key on the command line and save it to cache:

例如 / Example:

```bash
python3 query_vehicle.py --apikey 'your_full_api_key'
```

传入后脚本会自动把 API Key 写入缓存。  
After you pass it in, the script will automatically save the API Key to the cache.

如果只想保存认证信息，不立即查询：  
If you only want to save the API Key without making a query:

```bash
python3 query_vehicle.py --apikey 'your_full_api_key' --save-token-only
```

检查当前认证状态：  
Check the current authentication status:

```bash
python3 query_vehicle.py --check-auth
```

清理本地认证缓存：  
Clear the local authentication cache:

```bash
python3 query_vehicle.py --clear-auth
```

### OpenClaw 安装提示 / OpenClaw Install Prompt

如果你希望 OpenClaw 代为安装并配置这个 Skill，推荐直接使用下面这类提示语：  
If you want OpenClaw to install and configure this Skill for you, use a prompt like this:

```text
安装这个 skill，并帮我用环境变量 TIKA_API_KEY 配置 API Key。配置完成后执行 python3 query_vehicle.py --check-auth 验证是否生效。
```

如果你愿意让 OpenClaw 直接代填凭证，可以这样说：  
If you want OpenClaw to populate the credential directly, use this form:

```text
安装这个 skill，并帮我用环境变量 TIKA_API_KEY 配置 API Key。我的 API Key 是 xxx。配置完成后执行 python3 query_vehicle.py --check-auth 验证是否生效。
```

## 安全说明 / Security Notes

- API Key 属于高敏感凭证，请勿截图、发群、提交到 Git、写入公开文档。  
  API keys are highly sensitive credentials. Do not screenshot them, share them in chats, commit them to Git, or store them in public docs.
- 推荐优先使用系统环境变量，建议使用单一变量 `TIKA_API_KEY`；不建议把 API Key 长期写入公开配置或仓库文件。  
  Prefer system environment variables, ideally a single `TIKA_API_KEY`; avoid storing API keys long-term in public config files or repositories.
- 缓存文件保存于 `~/.skill_carkey_cache.json`，脚本会尽量将权限收紧为仅当前用户可读写。  
  The cache file is stored at `~/.skill_carkey_cache.json`, and the script attempts to restrict it to the current user only.
- 不再使用时，建议执行 `--clear-auth` 删除本地缓存。  
  When you no longer need the skill, run `--clear-auth` to delete the local cache.

## 使用方式 / Usage

查询全部信息 / Query everything:

```bash
python3 query_vehicle.py
```

默认会返回车辆状态简报，并附带一句自然语言提示。  
By default, the script returns a short vehicle status summary with one natural-language note.

仅查询位置 / Query position only:

```bash
python3 query_vehicle.py -p
```

仅查询车况 / Query condition only:

```bash
python3 query_vehicle.py -c
```

输出完整详细状态 / Show full detailed status:

```bash
python3 query_vehicle.py --detail
```

输出 JSON / Output JSON:

```bash
python3 query_vehicle.py --json
```

使用英文输出 / Use English output:

```bash
python3 query_vehicle.py --lang en
```

## 认证管理 / Authentication Management

- `--apikey`: 传入完整 API Key，并写入缓存 / Provide the full API key and save it to cache
- `--save-token-only`: 只保存 API Key，不发起网络请求 / Save the API key only, do not send a network request
- `--check-auth`: 检查缓存中的认证信息是否存在且格式完整 / Check whether cached auth info exists and is complete
- `--clear-auth`: 删除本地认证缓存 / Delete local authentication cache

## 输出说明 / Output Notes

- 默认输出车辆状态简报，并给出一句自然语言提示 / Default output is a short vehicle summary with one natural-language note
- `--detail` 输出完整详细状态 / `--detail` shows the full detailed status
- `--json` 只输出纯 JSON，适合调试或给其他程序消费 / `--json` outputs pure JSON for debugging or programmatic use
- `--lang zh|en` 可切换中文或英文 CLI 输出 / `--lang zh|en` switches CLI output between Chinese and English
- 位置、门锁、车窗、空调字段兼容当前接口返回格式和旧字段名 / Position, lock, window, and A/C fields support both current API fields and legacy names

## 相关文件 / Related Files

- [SKILL.md](./SKILL.md): Skill 定义与触发说明 / Skill definition and trigger guide
- [_meta.json](./_meta.json): Skill 元数据 / Skill metadata
- [query_vehicle.py](./query_vehicle.py): 查询脚本 / Query script
