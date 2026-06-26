# clawhealth-garmin

将 Garmin Connect 健康数据同步到本地 SQLite，并以 JSON 接口提供给 OpenClaw / AI Agent 使用。

---

## TL;DR

- 从 Garmin 拉取健康数据 → 存入本地 SQLite
- 提供 JSON 命令 → 可被 OpenClaw / AI Agent 调用
- 通过 ClawHub 安装后即可使用
- 首次使用时，重点是完成 Garmin 登录配置

---

## 这是什么？

`clawhealth-garmin` 是一个 OpenClaw skill，用于把你的 Garmin 健康数据转化为：

- 可查询的数据（SQLite）
- 可调用的 JSON 接口
- 可被 AI Agent 使用的上下文

例如，你的 Agent 可以问：

- “我昨天睡得怎么样？”
- “最近一周 HRV 有什么趋势？”
- “我是不是训练过度了？”

---

## 核心能力

- Garmin 登录（支持 MFA）
- 每日健康数据同步（SQLite）
- HRV / 睡眠 / 训练指标 / 体成分
- 活动数据（列表 + 详情）
- JSON 输出（适合 Agent / 自动化）
- 原始数据持久化（便于后续分析）

---

## 安装方式（ClawHub）

在 OpenClaw 环境中安装本 skill：

```bash
clawhub install clawhealth-garmin
````

安装后，skill 会被下载到你的 workspace，新的 OpenClaw 会话会自动加载它。

---

## 这类 skill 的工作方式

这是一个 **轻量封装（thin wrapper）**：

* 不包含完整 `clawhealth` 源码
* 运行时会从 GitHub 拉取所需的 `src/clawhealth`
* 依赖缺失时，可能按需自动安装

这样设计的目的：

* 保持 skill 体积小
* 把主源码集中放在主仓库维护
* 让 skill 发布和源码迭代分离

---

## 首次使用前：先完成 Garmin 登录配置

ClawHub 安装完成后，真正需要用户处理的重点是：

1. 配置 Garmin 用户名
2. 配置 Garmin 密码或密码文件
3. 完成一次 MFA 登录

---

## 推荐配置方式：密码文件

推荐使用密码文件，而不是把密码直接写在环境变量里。

在 skill 目录下创建 `.env`：

```text
CLAWHEALTH_GARMIN_USERNAME=you@example.com
CLAWHEALTH_GARMIN_PASSWORD_FILE=./garmin_pass.txt
```

然后创建密码文件：

```bash
echo "YOUR_PASSWORD" > garmin_pass.txt
chmod 600 garmin_pass.txt
```

说明：

* 推荐使用 `CLAWHEALTH_GARMIN_PASSWORD_FILE`
* 不建议把密码直接写进明文环境变量
* 相对路径会自动按 skill 目录解析

如果你确实想直接写环境变量，也可以使用：

```text
CLAWHEALTH_GARMIN_USERNAME=you@example.com
CLAWHEALTH_GARMIN_PASSWORD=YOUR_PASSWORD
```

但这不是推荐方式。

---

## Docker 用户怎么配置？

如果你的 OpenClaw 跑在 Docker 里，可以直接在容器内写入 `.env` 和密码文件。

示例：

```bash
docker exec -it openclaw bash -c '
cd ~/.openclaw/workspace/skills/clawhealth-garmin &&
printf "CLAWHEALTH_GARMIN_USERNAME=you@example.com\nCLAWHEALTH_GARMIN_PASSWORD_FILE=./garmin_pass.txt\n" > .env &&
printf "YOUR_PASSWORD" > garmin_pass.txt &&
chmod 600 .env garmin_pass.txt &&
echo "配置完成，请回到聊天界面触发登录。"
'
```

如果你的容器名字不是 `openclaw`，请替换成你自己的容器名。

---

## Garmin 登录流程（MFA）

### 第一步：触发登录

```bash
python {baseDir}/run_clawhealth.py garmin login --username you@example.com --json
```

如果返回 `NEED_MFA`，这是正常行为，表示需要继续第二步。

### 第二步：输入验证码

```bash
python {baseDir}/run_clawhealth.py garmin login --mfa-code 123456 --json
```

完成后，Garmin 登录态会保存在本地配置目录中。

---

## 开始同步数据

登录完成后，可以同步一段时间内的数据：

```bash
python {baseDir}/run_clawhealth.py garmin sync --since 2026-03-01 --until 2026-03-03 --json
```

查询某一天的汇总：

```bash
python {baseDir}/run_clawhealth.py daily-summary --date 2026-03-03 --json
```

---

## 常用命令

### 每日摘要

```bash
python {baseDir}/run_clawhealth.py daily-summary --date 2026-03-03 --json
```

### HRV

```bash
python {baseDir}/run_clawhealth.py garmin hrv-dump --date 2026-03-03 --json
```

### 睡眠分期与睡眠评分

```bash
python {baseDir}/run_clawhealth.py garmin sleep-dump --date 2026-03-03 --json
```

### 训练指标

```bash
python {baseDir}/run_clawhealth.py garmin training-metrics --json
```

### 体成分

```bash
python {baseDir}/run_clawhealth.py garmin body-composition --date 2026-03-03 --json
```

### 活动列表与详情

```bash
python {baseDir}/run_clawhealth.py garmin activities --since 2026-03-01 --until 2026-03-03 --json
python {baseDir}/run_clawhealth.py garmin activity-details --activity-id 123456789 --json
```

---

## 数据保存在哪里？

* 配置 / token：`{baseDir}/config`
* SQLite 数据库：`{baseDir}/data/health.db`

---

## 安全说明

* Garmin 凭证和会话数据只保存在你的本地环境
* 不会把你的健康数据发送给技能作者
* 推荐使用密码文件，而不是明文密码
* 不要把 `.env`、密码文件、数据库提交到 Git

---

## 常见问题

### 1. 安装完了，为什么还不能直接用？

因为 ClawHub 负责把 skill 安装到 workspace，但 Garmin 账号登录仍然需要你自己配置用户名、密码，并完成 MFA。([GitHub][1])

### 2. 返回 `NEED_MFA` 是不是报错？

不是。这表示第一步登录已触发，需要继续输入 MFA 验证码。

### 3. 为什么推荐密码文件？

因为比明文环境变量更安全，也更适合长期运行环境。

### 4. 为什么第一次运行会下载 GitHub 代码？

因为这个 skill 是轻量封装，只发布 skill 包本身；真正的 `clawhealth` 代码会在运行时按需获取。

### 5. 为什么有时会自动安装依赖？

因为 skill 运行时需要 Python 依赖。如果环境中缺失，可能会自动 bootstrap。

---

## 文档

* 英文文档：`README.md`
* Skill 说明：`SKILL.md`

---

## 项目来源

[https://github.com/ernestyu/clawhealth](https://github.com/ernestyu/clawhealth)