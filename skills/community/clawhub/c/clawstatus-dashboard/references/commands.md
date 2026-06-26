# ClawStatus commands

## Install or update

```bash
bash scripts/install_or_update.sh ~/ClawStatus
```

## Run in foreground

```bash
clawstatus --host 0.0.0.0 --port 8900 --no-debug
```

## Restart user service

```bash
systemctl --user restart clawstatus.service
systemctl --user status clawstatus.service
```

## Verify reachability

```bash
curl -I http://127.0.0.1:8900/
curl -I http://<lan-ip>:8900/
```

## Verify dashboard pages

```bash
xdg-open http://127.0.0.1:8900/?page=overview
xdg-open http://127.0.0.1:8900/?page=crons
xdg-open http://127.0.0.1:8900/?page=memory
```

Overview / Crons pages now use a modal-based “切换模型” flow; Memory page uses the refreshed grouped layout.
