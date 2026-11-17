# ducc-helper

京东 **DUCC 配置中心**（泰山 `taishan.jd.com/ducc`，后端 `console.ducc.jd.com`）的命令行 skill，让 agent / 人在终端直接读写、发布 DUCC 配置。**零配置认证**：从本机京ME客户端自动换出 `sso.jd.com`，无需浏览器、无需手填 token。

## 能力

| 脚本 | 能力 |
| --- | --- |
| `scripts/config.py` | 读：命名空间 / 配置文件 / profile / 配置项（key-value） |
| `scripts/write.py` | 写：新增 / 修改 / 删除配置项、全量发布、灰度分批发布 |

DUCC 结构：**命名空间**(如 `pop_customs_center`) → **配置文件**(如 `center_config`) → **profile / 环境**(如 `dev` / `common`) → **配置项**(key = value)。三级都可传中文 code，脚本自动解析为内部数字 ID。

## 前置条件

1. 本机已安装并登录**京ME桌面客户端**（进程 `JDITDesk`）——唯一前提。
2. `pip install -r requirements.txt`（仅需 `requests`）。

## 快速开始

```bash
# 读
python scripts/config.py namespaces --search customs
python scripts/config.py configs  pop_customs_center
python scripts/config.py profiles pop_customs_center center_config
python scripts/config.py items    pop_customs_center center_config common --search order.trace
python scripts/config.py get       pop_customs_center center_config common ducc.order.trace.merge.read.switch

# 写（增/改/删只改草稿，需 release 才生效）
python scripts/write.py set    pop_customs_center center_config common ducc.foo.switch true
python scripts/write.py set    pop_customs_center center_config common ducc.foo.json '{"a":1}' --format 1
python scripts/write.py delete pop_customs_center center_config common ducc.foo.switch

# 发布（默认预演，加 --confirm 才真下发）
python scripts/write.py release pop_customs_center center_config common ducc.foo.switch --confirm            # 全量
python scripts/write.py orchestrates pop_customs_center                                                       # 列灰度模板
python scripts/write.py release pop_customs_center center_config common ducc.foo.switch \
    --orchestrate "<模板code>" --confirm                                                                      # 灰度分批
```

## 生产 / 预发

`--env online`（生产，默认）/ `--env pre`（预发）。预发未开放时读到空或 `503 环境不存在`。

## 安全约定

- 只读命令直接执行。
- 增 / 改 / 删只影响**草稿**（不影响线上运行），直接执行；**需 `release` 才生效到线上**。
- `release`（发布，真正生效）**默认只预演**，必须显式加 `--confirm` 才下发。生产环境尤其谨慎，灰度优先于全量。灰度发布逐批推进，每批等所有 IP `COMPLETED` 后才发下一批。

## 实现

- `lib/jme_auth.py`：京ME → `sso.jd.com` 零配置认证（复用自 jdos-helper）。
- `lib/ducc_client.py`：公共 HTTP 层（真实域名 `pserve.jd.com`、`config-env` + `x-proxy-opts` 双环境头切换、code→ID 解析）。
- `references/api.md`：全部接口、发布链路与批次语义、发现方法论（抓包实测）。
