# eyun-freight skill

将此 skill 接入 OpenClaw，使 agent 可直接查询 Eyun 运价系统。

## 部署

**1. 复制 skill 目录到 OpenClaw workspace**

```bash
cp -r eyun-freight/ /home/bobofrivia/.openclaw/workspace/skills/
```

**2. 在 `~/.openclaw/openclaw.json` 中注入环境变量**

```json
{
  "skills": {
    "entries": {
      "eyun_freight": {
        "enabled": true,
        "env": {
          "EYUN_BASE_URL": "http://<eyun-server-ip>:8010",
          "EYUN_COMPANY_ID": "<企业 ID 数字>"
        }
      }
    }
  }
}
```

**3. 重启 gateway**

```bash
openclaw gateway restart
```

## EYUN_COMPANY_ID 获取方式

`EYUN_COMPANY_ID` 是该 Openclaw 实例对应的企业 ID（纯数字）。填入后，所有请求以该企业身份访问 Eyun 接口。
