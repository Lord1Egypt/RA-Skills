# Coze CLI 命令速查

> 来源：<https://docs.coze.cn/developer_guides/coze_cli> + <https://docs.coze.cn/developer_guides/coze_cli_quickstart>

---

## 认证

| 命令 | 说明 |
| --- | --- |
| `coze auth login --oauth` | OAuth 登录（自动打开浏览器） |
| `coze auth status` | 查看登录状态 |
| `coze auth logout` | 登出 |

---

## 组织 & 空间

| 命令 | 说明 |
| --- | --- |
| `coze org list` | 列出所有组织 |
| `coze org use <org_id>` | 切换默认组织 |
| `coze space list` | 列出当前组织下所有空间 |
| `coze space use <space_id>` | 切换默认空间 |

---

## 项目管理

| 命令 | 说明 |
| --- | --- |
| `coze code project create --message <描述> --type <类型>` | 通过自然语言创建项目 |
| `coze code project list` | 列出所有项目 |
| `coze code project list --type <type>` | 按类型筛选（可多次使用 `--type`） |
| `coze code project list --name <关键词>` | 按名称搜索 |
| `coze code project list --search-scope 1` | 只看自己创建的项目 |
| `coze code project list --size 20 --cursor-id <cursor>` | 分页查询 |
| `coze code project list --order-by 1 --order-type 1` | 按创建时间升序 |
| `coze code project list --is-fav-filter` | 只看收藏项目 |
| `coze code project get <project_id>` | 查看项目详情 |
| `coze code project delete <project_id>` | 删除项目 |

**支持的项目类型**: `agent`、`workflow`、`app`、`skill`、`web`、`miniprogram`、`assistant`

---

## 消息对话

| 命令 | 说明 |
| --- | --- |
| `coze code message send <消息> -p <project_id>` | 发送消息 |
| `coze code message send <消息> @<本地文件> -p <id>` | 引用本地文件 |
| `coze code message send <消息> -p <id> <file1> <file2>` | 引用多个文件 |
| `cat <file> \| coze code message send <消息> -p <id>` | 通过管道输入 |
| `export COZE_PROJECT_ID=<id>` then `coze code message send <消息>` | 通过环境变量指定项目 |
| `coze code message status -p <project_id>` | 查询消息状态 |
| `coze code message cancel -p <project_id>` | 取消进行中的消息 |

---

## 部署 & 预览

| 命令 | 说明 |
| --- | --- |
| `coze code deploy <project_id>` | 部署项目 |
| `coze code deploy <project_id> --wait` | 部署并等待完成 |
| `coze code deploy status <project_id>` | 查看部署状态（最新记录） |
| `coze code deploy status <project_id> --deploy-id <id>` | 查看指定部署记录 |
| `coze code preview <project_id>` | 获取预览链接 |

---

## 环境变量

| 命令 | 说明 |
| --- | --- |
| `coze code env list -p <project_id>` | 查看开发环境变量 |
| `coze code env list -p <project_id> --env prod` | 查看生产环境变量 |
| `coze code env set <KEY> <VALUE> -p <project_id>` | 设置环境变量 |
| `coze code env delete <KEY> -p <project_id>` | 删除环境变量 |

---

## 自定义域名

| 命令 | 说明 |
| --- | --- |
| `coze code domain list <project_id>` | 查看项目域名 |
| `coze code domain add <domain> -p <project_id>` | 添加自定义域名 |
| `coze code domain remove <domain> -p <project_id>` | 移除自定义域名 |

---

## 项目技能

| 命令 | 说明 |
| --- | --- |
| `coze code skill list -p <project_id>` | 查看项目技能（含安装状态） |
| `coze code skill add <skill_id> -p <project_id>` | 添加技能 |
| `coze code skill remove <skill_id> -p <project_id>` | 移除技能 |

---

## 多媒体生成

### 图像生成

| 命令 | 说明 |
| --- | --- |
| `coze generate image "<prompt>"` | 文生图 |
| `coze generate image "<prompt>" --output-path ./out.png` | 保存到本地 |
| `coze generate image "<prompt>" --size 4K --no-watermark` | 指定分辨率并禁水印 |
| `coze generate image "<prompt>" --image <参考图URL>` | 参考图生成 |

### 音频生成

| 命令 | 说明 |
| --- | --- |
| `coze generate audio "<text>"` | 文本转语音 |
| `coze generate audio "<text>" --output-path ./out.mp3` | 保存为 MP3 |
| `echo "<ssml>" \| coze generate audio --ssml` | SSML 输入 |
| `coze generate audio "<text>" --audio-format ogg_opus --speech-rate 50` | 指定格式和语速 |

### 视频生成

| 命令 | 说明 |
| --- | --- |
| `coze generate video create "<prompt>"` | 创建视频生成任务 |
| `coze generate video create "<prompt>" --wait --output-path ./out.mp4` | 等待完成并保存 |
| `coze generate video create "<prompt>" --resolution 1080p --duration 8` | 指定分辨率和时长 |
| `coze generate video status <task_id>` | 查询任务状态 |

---

## 文件管理

| 命令 | 说明 |
| --- | --- |
| `coze file upload <path>` | 上传本地文件，获取文件链接 |

---

## 配置管理

| 命令 | 说明 |
| --- | --- |
| `coze config list` | 查看所有配置（含来源） |
| `coze config get <key>` | 查看单项配置 |
| `coze config set <key> <value>` | 设置配置 |
| `coze config delete <key>` | 删除配置 |

**配置文件位置**（优先级从高到低）:
1. 环境变量
2. `--config` CLI 参数
3. `COZE_CONFIG_FILE` 环境变量
4. `.cozerc.json`（项目级）
5. `~/.coze/config.json`（全局）

---

## Shell 自动补全

| 命令 | 说明 |
| --- | --- |
| `coze completion --setup` | 安装自动补全脚本 |
| `source ~/.zshrc` 或 `source ~/.bashrc` | 重新加载 |
| `coze completion --cleanup` | 卸载自动补全 |

---

## 版本升级

| 命令 | 说明 |
| --- | --- |
| `coze upgrade` | 检查并升级到最新版本 |
| `coze upgrade --force` | 强制升级 |
| `coze upgrade --tag beta` | 升级到指定标签版本 |

---

## CI/CD 环境变量

| 环境变量 | 说明 |
| --- | --- |
| `COZE_ORG_ID` | 组织 ID |
| `COZE_ENTERPRISE_ID` | 企业 ID |
| `COZE_SPACE_ID` | 空间 ID |
| `COZE_PROJECT_ID` | 项目 ID（用于 message 命令） |
| `COZE_CONFIG_FILE` | 自定义配置文件路径 |
| `COZE_CONFIG_SCOPE` | 配置作用域（global 或 local） |
| `COZE_AUTO_CHECK_UPDATE` | 是否自动检查更新 |

---

## 全局选项

| 选项 | 说明 |
| --- | --- |
| `--format json\|text` | 输出格式 |
| `--no-color` | 禁用彩色输出 |
| `--config <path>` | 指定配置文件 |
| `--org-id <id>` | 临时覆盖组织 ID |
| `--space-id <id>` | 临时覆盖空间 ID |
| `--verbose` | 详细业务流程日志 |
| `--debug` | 全量诊断日志 |
| `--log-file <path>` | 日志输出到文件 |
| `-p <project_id>` | 指定项目 ID |

---

## 快速命令模板

```bash
# 完整初始化流程
npm install -g @coze/cli && \
coze auth login --oauth && \
coze org list && coze org use <org_id> && \
coze space list && coze space use <space_id>

# 创建 + 等待 + 部署
coze code project create --message "<需求描述>" --type <type> --wait && \
coze code deploy <project_id> --wait && \
coze code preview <project_id>

# 批量查询项目
coze code project list --format json | jq '.[] | select(.type=="agent") | .name'

# 代理配置
export HTTPS_PROXY=http://your-proxy:8080
export HTTP_PROXY=http://your-proxy:8080
```
