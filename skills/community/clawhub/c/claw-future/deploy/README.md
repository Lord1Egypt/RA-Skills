# 多账户服务器部署

每个账户是一个完全独立的 daemon 进程和目录。账户之间不共享 CTP flow、状态、运行时任务、幂等账本或日志；agent 通过 `account_id` 选择目标账户并自行调度。

## 初始化 A-E

```bash
cp accounts.example.json accounts.json
python3 scripts/clawtrader.py --registry accounts.json accounts
python3 scripts/clawtrader.py --registry accounts.json --account A setup
python3 scripts/clawtrader.py --registry accounts.json --account B setup
```

随后分别执行 `config`，为每个账户填写自己的 broker、user、password、appid、auth_code 和 md/td 地址。凭据只写入对应的 `accounts/<id>/config.json`，该文件已被 `.gitignore` 忽略。

## 直接启动

```bash
python3 scripts/clawtrader.py --registry accounts.json --account A start
python3 scripts/clawtrader.py --registry accounts.json --account B start
python3 scripts/clawtrader.py --registry accounts.json accounts
```

## systemd

把仓库放到 `/opt/claw-future` 后：

```bash
sudo cp deploy/clawtrader@.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now clawtrader@A clawtrader@B clawtrader@C clawtrader@D clawtrader@E
```

模板中的路径按实际安装目录调整。停止单个账户不会影响其他账户：`sudo systemctl stop clawtrader@C`。

## MCP 与 Web

agent 使用 MCP：

```bash
python3 scripts/mcp_server.py --registry accounts.json --transport streamable-http --port 17880
```

默认只监听 `127.0.0.1`。跨主机监听前设置 `CLAW_MCP_TOKEN` 并在反向代理层做认证。工具均要求显式 `account_id`；写操作要求显式 `idempotency_key`，因此 agent 重试不会重复下单或撤单。

人工操作界面：

```bash
python3 scripts/web_server.py --registry accounts.json --host 127.0.0.1 --port 17890
```

浏览器打开 `http://127.0.0.1:17890/`。部署到非本机地址时必须设置 `CLAW_WEB_TOKEN`，并建议放在 HTTPS 反向代理之后。
