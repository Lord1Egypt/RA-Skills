---
name: dtflow-notify
description: 用钉钉给自己/同事发通知与私信：工作通知（应用消息）、机器人单聊私信、以本人身份私信，支持 text/markdown/文件，失败自动留痕。当需要「钉钉通知 / 钉钉私信 / 工作通知 / 机器人消息 / 把结果推到钉钉 / dingtalk notify / 配置钉钉企业内部应用 AppKey」时使用。
license: MIT
metadata:
  version: 0.1.1
  requires:
    bins: [python3]
---

# dtflow-notify（钉钉联动基座）

其它 `dingtalk-*` 子能力共用的**发送底座**与配置约定。

## 配置（一次性）

凭证按 **环境变量 > `~/.dingtalk-skills/config`** 读取（键=值 文本）：

```
DINGTALK_APP_KEY=<企业内部应用 AppKey>
DINGTALK_APP_SECRET=<AppSecret>
DINGTALK_AGENT_ID=<AgentId>
DINGTALK_MY_USER_ID=<默认接收人 userId>
DINGTALK_MY_NAME=<本人姓名，供「本人私信」用>
```

> 也可用 `DINGTALK_CONFIG` 指向自定义配置文件；日志目录用 `DINGTALK_LOG_DIR`。

## 发送出口（scripts/notify.py）

```bash
python3 scripts/notify.py --text "内容"                 # 工作通知（默认）
python3 scripts/notify.py --markdown "内容" --title "标题"
python3 scripts/notify.py --to <userId> --text "内容"    # 指定接收人
python3 scripts/notify.py --dm --markdown "内容"         # 机器人单聊私信（特殊，少用）
python3 scripts/notify.py --dm-self --text "内容"        # 以本人身份私信（dws chat +dm）
python3 scripts/notify.py --file /abs/path.xlsx          # 文件（工作通知）
```

- 失败**自动写日志**（`DINGTALK_LOG_DIR`，默认 `~/.dingtalk-skills/logs/dingtalk_fail.log`），不静默。
- 依赖：`requests`、（`--dm-self` 需要）`dws`。

## 前置

见套件根 `INSTALL.md`：需自建**钉钉企业内部应用**并开通相应权限、安装并登录 `dws`。

## 限制

- 钉钉「文件」消息**单文件 ≤ 20MB**；超限请**拆分或压缩**后再发（脚本会拒绝并提示）。
