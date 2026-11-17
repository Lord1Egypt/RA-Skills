---
name: ducc-helper
description: 京东 DUCC 配置中心(泰山 taishan.jd.com/ducc、后端 console.ducc.jd.com)统一入口，让 agent 能读写发布 DUCC 配置。零配置认证（本机京ME客户端换 sso.jd.com，无需浏览器/手填token）。当用户想要「查 DUCC 命名空间/应用配置空间」「列某命名空间下的配置文件」「看配置文件有哪些环境/profile(如 dev/common/生产配置/预发配置)」「读某个配置项的值/key value」「查 DUCC 某开关/参数当前配的啥」「改 DUCC 配置项/新增配置项/删除配置项」「发布 DUCC 配置/全量发布/灰度发布/分批发布」「按 10%->30%->60%->100% 灰度」「等前批IP成功再发下一批」，或提到 DUCC、ducc、泰山配置、taishan、命名空间、nsId、配置文件、profile、配置项、consoleducc、灰度发布、编排模板、orchestrate 时，都应使用本技能——即使用户没明确说技能名。命名空间/配置文件/profile 都可传中文 code(如 pop_customs_center / center_config / common)自动解析为内部ID。改/增/删只影响草稿(直接执行)，发布(真正生效到线上)默认只预演，加 --confirm 才下发。
---

# 京东 DUCC 配置中心（读 / 改 / 增删 / 发布）

一个 skill 打通 DUCC（泰山配置中心）的日常：查命名空间/配置文件/环境、读配置项、增删改配置项、全量/灰度发布。**零配置**：认证从本机京ME客户端自动换出 `sso.jd.com`。

| 能力 | 脚本 | 典型场景 |
| --- | --- | --- |
| 配置读取 | `scripts/config.py` | 列命名空间/配置文件/profile、读配置项 key/value |
| 配置写入 | `scripts/write.py` | 新增/修改/删除配置项、全量发布、灰度分批发布 |

## DUCC 结构（理解这个才能用对）

```
命名空间(namespace)          如 pop_customs_center「跨境-赤道-center」，对应一个应用
  └─ 配置文件(config)         如 center_config
       └─ 环境/profile        如 dev(真预发) / common，即"生产配置""预发配置"
            └─ 配置项(item)    key = value，如 ducc.order.trace.merge.read.switch = true
```

- **命名空间**：一个应用一个，有 `code`(pop_customs_center) 和中文名(跨境-赤道-center)。
- **配置文件**：命名空间下有多个（center_config / common 等）。
- **profile**：配置文件下的具体环境，就是 UI 里 `center_config / dev`、`center_config / common`。
- **配置项**：profile 里真正的 key/value，可选「无格式」或「JSON 格式」。

> **只需给 code**：命名空间/配置文件/profile 都可传中文 code，脚本自动调 search 反查内部数字 ID（nsId/cId/profileId）；也可直接传数字 ID。

## 前置条件（开箱即用的关键）

1. **本机已安装并登录京ME桌面客户端**（进程名 `JDITDesk`）。脚本通过本机 `127.0.0.1:8988~9006` 端口换取 token，全自动，无需扫码/填 token。
2. **Python 3** + `requests`：`pip install -r requirements.txt`。
3. 无需浏览器。

> **认证原理**：`lib/jme_auth.py` 从本机京ME客户端零配置换出 `sso.jd.com`（唯一 Cookie），
> 请求真实域名 `pserve.jd.com`，每个请求带两个自定义头 `config-env` + `x-proxy-opts`（见下）。
> token 缓存在 `~/.ducc-helper-cache.json`，过期自动刷新，接口走 **http**。
> 报未登录/401 → 京ME未登录或token过期，加 `--force-refresh`。

## ★ 生产 / 预发环境（关键机制）

DUCC 用 `--env` 区分环境，脚本转成两个配套 header（**必须同时切换**）：

| 环境 | `--env` | `config-env` | `x-proxy-opts` target |
| --- | --- | --- | --- |
| 生产（默认） | `online`/`生产` | `online` | `http://console.ducc.jd.com` |
| 预发 | `pre`/`预发` | `pre` | `http://pre.console.ducc.jd.local` |

- **预发未开放的现象**（很常见）：`profiles`/`items` 在 `--env pre` 下读到空 `data:[]` 或报 `503 环境不存在`。脚本会提示「预发环境未开放或无 profile」。pop_customs_center 当前预发就未开放。
- 命名空间、配置文件列表是**环境无关**的元数据（脚本一律用 online 解析 code→ID），只有 profile 和配置项才随 env 切换。

## 能力一：配置读取

```bash
# 列所有命名空间（--search 按 code/中文名过滤）
python scripts/config.py namespaces --search customs

# 列某命名空间下的配置文件
python scripts/config.py configs pop_customs_center

# 列配置文件下的 profile（生产配置/预发配置，如 dev/common）
python scripts/config.py profiles pop_customs_center center_config

# 列 profile 下的配置项（--search 按 key/描述过滤，--all 翻遍所有分页）
python scripts/config.py items pop_customs_center center_config common
python scripts/config.py items pop_customs_center center_config common --search order.trace

# 读单个配置项的值
python scripts/config.py get pop_customs_center center_config common ducc.order.trace.merge.read.switch

# 读预发环境（未开放会提示）
python scripts/config.py items pop_customs_center center_config common --env pre
```

- `namespaces` 返回 `nsId/code/name/owner`；`configs` 返回 `cId/code/name`；`profiles` 返回 `profileId/code/name/version`。
- `items`/`get` 返回配置项 `key/value/description/dataType/isReleased/updateBy`。
- 找不到配置文件时：可去对应应用的**行云分组配置**里看该应用挂了哪个 DUCC 命名空间/配置文件（装了 jdos-helper 可用 `config.py` 读行云配置文件）。

## 能力二：配置写入（增 / 改 / 删）

```bash
# 新增或覆盖配置项（存在则改，不存在则建）
python scripts/write.py set pop_customs_center center_config common ducc.foo.switch true
python scripts/write.py set pop_customs_center center_config common ducc.foo.json '{"a":1}' --format 1 --desc "说明"

# 仅修改已存在项（不存在报错）
python scripts/write.py update pop_customs_center center_config common ducc.foo.switch false

# 删除配置项
python scripts/write.py delete pop_customs_center center_config common ducc.foo.switch
```

- `--format`：`0`=无格式(纯文本/字符串，默认)，`1`=JSON（value 需是合法 JSON 字符串）。
- **增/改/删只影响「草稿」**（未发布内容，不影响线上运行），所以直接执行、不需 --confirm。
- ⚠ **改完必须 release 才真正生效到线上**。

## 能力三：发布（全量 / 灰度分批）

```bash
# 列可用的灰度编排模板（灰度发布要用）
python scripts/write.py orchestrates pop_customs_center

# 全量发布（默认；不加 --confirm 只预演打印计划）
python scripts/write.py release pop_customs_center center_config common ducc.foo.switch                # 预演
python scripts/write.py release pop_customs_center center_config common ducc.foo.switch --confirm      # 真发
python scripts/write.py release pop_customs_center center_config common k1 k2 k3 --confirm             # 一次发多个key

# 灰度分批发布（--orchestrate 指定编排模板 code）
python scripts/write.py release pop_customs_center center_config common ducc.foo.switch \
    --orchestrate "1731329960745.69139" --confirm
# 只发第一批就停(人工确认再继续)：加 --batch-pause
python scripts/write.py release ... --orchestrate <code> --confirm --batch-pause
```

- **全量发布**：两步（submitAuditKeys 建任务 → release/keys 执行），一次发到所有实例。
- **灰度分批发布**（用户强调的核心）：按编排模板（如 10%→30%→60%→100%）分批。脚本**逐批推进**，**每批发完自动轮询该批所有 IP 状态，等全部 COMPLETED 才发下一批**；某批超时/失败则暂停不再往下发。
- ⚠ **同一 profile 同时只能有 1 个进行中的发布任务**（并行上限1个）。上一个没发完（或卡住）时，新发布会报 `1606 并行任务超上限`。去页面把卡住的任务发完或取消。
- 未加 `--confirm` 只预演（打印发布计划+批次），确认后再加 `--confirm`。

## 输出约定

脚本 stdout 打印 JSON、stderr 打印进度。拿到结果后按用户诉求呈现：清单类先给概览表格；配置项正文/值按需展示。

## 安全约定（重要）

- **只读命令**（namespaces/configs/profiles/items/get/orchestrates）直接执行。
- **增/改/删**只改草稿（不影响线上运行），直接执行；但要提醒用户「需 release 才生效」。
- **发布（release）**让配置真正生效到线上运行实例，风险最高：**默认只预演**，必须显式加 `--confirm` 才下发。生产环境（--env online 默认）尤其谨慎，灰度发布优先于全量。

## 接口与实现参考

底层全部接口（真实域名、config-env/x-proxy-opts 头、code→ID 解析、发布链路与批次语义、发现方法论）见 `references/api.md`，仅在调试或扩展新能力时查阅。`lib/jme_auth.py`(认证) 与 `lib/ducc_client.py`(公共HTTP层：sso认证 + online/pre 双环境头切换 + code→ID 解析) 可被新脚本复用。
