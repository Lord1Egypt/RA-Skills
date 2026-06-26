# CLS CLI 安装与使用

## 一、安装（30秒）

直接执行以下命令，一行搞定：

```bash
git clone https://github.com/trumphuang/CLS_CLI.git /tmp/CLS_CLI && cd /tmp/CLS_CLI/cls-cli && go build -o cls-cli . && mv cls-cli /usr/local/bin/ && rm -rf /tmp/CLS_CLI && cls-cli version
```

> 前提：系统已安装 Git 和 Go 1.23+。如果 `/usr/local/bin` 需要权限，把 `mv` 改成 `sudo mv`。

验证安装成功：

```bash
cls-cli version
# 输出: cls-cli version 0.2.0 (darwin/arm64)
```

## 二、配置（10秒）

```bash
cls-cli config init --secret-id <SECRET_ID> --secret-key <SECRET_KEY> --region ap-guangzhou
```

用户需要提供腾讯云 API 密钥，获取地址：https://console.cloud.tencent.com/cam/capi

也支持环境变量（CI/CD 场景推荐）：

```bash
export TENCENTCLOUD_SECRET_ID=xxx
export TENCENTCLOUD_SECRET_KEY=xxx
export CLS_DEFAULT_REGION=ap-guangzhou
```

## 三、升级

```bash
cls-cli upgrade
```

---

## 四、使用教程

### 全局参数

任何命令都可以加：

| 参数 | 说明 |
|---|---|
| `--region ap-beijing` | 临时切换地域，不改配置文件 |
| `--format table` | 输出格式：json / pretty / table / csv |
| `--dry-run` | 预览模式，不实际执行 |
| `-y` | 跳过危险操作确认 |

### 日志检索 `log`

```bash
cls-cli log +search --topic-id <id> --query "level:ERROR" --from "1 hour ago"
cls-cli log +context --topic-id <id> --pkg-id <pkg_id> --pkg-log-id <log_id>
cls-cli log +tail --topic-id <id> --query "*"
cls-cli log +histogram --topic-id <id> --query "*" --from "1 hour ago"
cls-cli log +download --topic-id <id> --query "*" --from "1 hour ago" --output logs.json
```

### 日志主题 `topic`

```bash
cls-cli topic +list
cls-cli topic +create --logset <logset_id> --name "my-topic" --ttl 30
cls-cli topic +info --topic <topic_id>
cls-cli topic +delete --topic <topic_id>
cls-cli topic +logsets                     # 列出日志集
```

### 告警管理 `alarm`

```bash
cls-cli alarm +list
cls-cli alarm +history --from "7 days ago"
cls-cli alarm +create --name "Error Alert" --topic <id> \
  --query "level:ERROR | SELECT COUNT(*) as cnt" \
  --condition '$1.cnt > 100' --period 5
cls-cli alarm +delete --alarm-id <id>
cls-cli alarm +notices                     # 列出通知渠道
```

### 仪表盘 `dashboard`（别名 `dash`）

```bash
cls-cli dash +list
cls-cli dash +info --id <dashboard_id>
cls-cli dash +create --name "运维总览"
cls-cli dash +update --id <id> --name "新名称"
cls-cli dash +delete --id <id>
```

### 机器组 `machinegroup`（别名 `mg`）

```bash
cls-cli mg +list
cls-cli mg +create --name web --type ip --values "10.0.0.1,10.0.0.2"
cls-cli mg +create --name web --type label --values "webserver"
cls-cli mg +status --id <group_id>
cls-cli mg +info --id <group_id>
cls-cli mg +delete --id <group_id>
```

### 采集配置 `collector`（别名 `col`）

```bash
cls-cli col +list
cls-cli col +create --name "app-logs" --topic <id> --type json \
  --path "/var/log/app" --file-pattern "*.log" --group-id <id>
cls-cli col +info --id <config_id>
cls-cli col +delete --id <config_id>
cls-cli col +guide                         # 采集入门指南
```

### LogListener `loglistener`（别名 `ll`）

```bash
cls-cli ll +install                        # 生成安装脚本
cls-cli ll +init --region ap-guangzhou     # 初始化
cls-cli ll +start                          # 启动
cls-cli ll +stop / +restart / +status / +check / +uninstall
```

### 通用 API `api`

以上快捷命令未覆盖的操作，都可以用通用 API 调用（支持全部 150+ CLS API 3.0）：

```bash
cls-cli api <Action> --params '<JSON>'

# 示例
cls-cli api DescribeIndex --params '{"TopicId":"xxx"}'
cls-cli api CreateIndex --params '{"TopicId":"xxx","Rule":{...}}'
```

---

## 五、AI Agent 意图映射

当用户用自然语言描述需求时，按此表匹配命令：

| 用户说 | 执行 |
|---|---|
| 查日志 / 搜错误 / 看看有没有异常 | `log +search` |
| 看这条日志的上下文 | `log +context` |
| 实时看日志 | `log +tail` |
| 有哪些主题 / topic | `topic +list` |
| 有哪些日志集 | `topic +logsets` |
| 看告警 / 最近有没有报警 | `alarm +list` + `alarm +history` |
| 创建告警 | `alarm +create` |
| 看仪表盘 | `dash +list` |
| 机器状态 / 哪些机器挂了 | `mg +status` |
| 配置采集 | `col +guide` → 按指南操作 |
| 切地域查 | 加 `--region ap-beijing` |
| 其他高级操作 | `api <Action>` |

## 六、常见地域

| 地域 | 代码 |
|---|---|
| 广州 | `ap-guangzhou` |
| 上海 | `ap-shanghai` |
| 北京 | `ap-beijing` |
| 成都 | `ap-chengdu` |
| 南京 | `ap-nanjing` |
| 香港 | `ap-hongkong` |
| 新加坡 | `ap-singapore` |
| 硅谷 | `na-siliconvalley` |
