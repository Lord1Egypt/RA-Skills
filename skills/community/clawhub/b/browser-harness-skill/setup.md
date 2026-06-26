# browser-harness 安装

## 系统要求

| 软件 | 最低版本 | 说明 |
|---|---|---|
| Node.js | ≥ 20.6.0 | TS 客户端 + `bhts` CLI 跑在这上面 |
| Python | ≥ 3.10 | 守护进程跑在这上面（通过 `uv tool` 隔离） |
| `uv` | 最新 | Python 包管理器，用来装守护进程到 PATH |
| Chrome / Edge / Brave / Arc / Comet | 任意近一年版本 | 守护进程通过 CDP 接管 |

平台：macOS、Linux、Windows（Windows 通过 TCP loopback 替代 unix socket，自动 fallback）。

## 一键安装

```bash
scripts/run.sh setup
```

这会按顺序：

1. 检查 `node` 是否 ≥ 20.6.0；缺则提示去装 [nodejs.org](https://nodejs.org/) 或 `nvm install 20`
2. 检查 `uv` 是否安装；缺则提示：
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh    # 官方
   # 或
   brew install uv                                     # macOS
   ```
3. `npm install -g browser-harness-ts` —— 把 `bhts` CLI 放到 PATH
4. `uv tool install --force browser-harness` —— 把 Python `browser-harness` 命令放到 PATH（`~/.local/bin/browser-harness`）
5. 提示用户跑 `browser-harness --setup` 接管 Chrome（这一步交互式，必须用户在自己的 Chrome 里点链接）
6. 跑 `scripts/run.sh doctor` 验证

## 手动接管 Chrome

`browser-harness --setup` 是 Browser Use 团队写的交互式脚本，会：

1. 检测当前是否有 Chrome 在跑
2. 如果有：让你新开一个标签到 `chrome://inspect`，引导启用远程调试
3. 如果没有：教你下次怎么带 `--remote-debugging-port=9222` 启动
4. 找到 CDP 端口后，附着第一个真实标签页，把 sessionId 存到守护进程

如果 `chrome://inspect` 那一步卡住，常见原因：

| 现象 | 处置 |
|---|---|
| Chrome M144+ 弹"是否允许远程调试" | 必须**点允许**；不允许就退出，没有解 |
| Chrome 用 default profile | M136+ 锁了 default profile，必须用其他 profile（新建一个 `--profile-directory=Profile 1` 或类似） |
| Chrome 147+ 找不到 `/json/version` | 已知 issue，本 skill 内置 fallback 用 `Browser.getVersion`；如仍失败请升级 `browser-harness`：`uv tool install --force browser-harness@latest` |

## 验证安装

```bash
scripts/run.sh doctor
```

期待输出（实际样子取决于版本）：

```
ok  node v22.11.0
ok  uv 0.5.18
ok  browser-harness 0.x.y on PATH
ok  bhts 0.1.x on PATH
ok  daemon "default" running (pid 12345, sock ~/.cache/browser-harness/default.sock)
ok  attached to Chrome 132.0.6834.x  via 127.0.0.1:9222
ok  current tab: https://...    (title: ...)
```

任意一行 `!!!` / `ERR` 都贴给用户原文，不要瞎猜。

## 卸载

```bash
# 守护
pkill -f 'browser-harness.*daemon'
uv tool uninstall browser-harness

# TS 客户端
npm uninstall -g browser-harness-ts

# 残留
rm -rf ~/.cache/browser-harness/      # socket / pid / log
rm -rf ~/.config/browser-harness/     # 配置（如果有）
```

## 升级

```bash
# 升级 Python 守护
uv tool install --force browser-harness@latest

# 升级 TS 客户端
npm install -g browser-harness-ts@latest

# 重启守护让新版本生效
pkill -f 'browser-harness.*daemon'
browser-harness --setup    # 再接一次 Chrome
```

## 多用户 / 多 Chrome（高级）

```bash
# 给每个 Chrome 实例一个独立 namespace
BU_NAME=work    browser-harness --setup
BU_NAME=personal browser-harness --setup

# 然后任何 scripts/run.sh 调用前指定 namespace
BU_NAME=work scripts/run.sh open https://internal.acme.com
BU_NAME=personal scripts/run.sh shot
```

每个 namespace 有自己的 socket / pid / log，互不干扰。

## 离线 / 公司代理

- npm install 走公司 npm registry：`npm config set registry https://...`
- uv 走公司 PyPI mirror：`UV_INDEX_URL=https://... uv tool install browser-harness`
- Chrome 接管只用 localhost CDP，不走任何外网

## 常见问题

**Q：守护一直起不来？**
A：看日志 `~/.cache/browser-harness/default.log`，90% 的根因在第一屏。把日志贴给用户。

**Q：每次重启 Chrome 都要重新 setup？**
A：是的——CDP 端口和 user-data-dir 是 Chrome 启动参数，每次都要带。建议把 Chrome 启动命令做成 alias 或桌面快捷方式：
```bash
alias chrome='/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --profile-directory="Profile 1"'
```

**Q：能不能装到 Docker 里？**
A：能，但 Chrome 必须和守护进程在同一个 Linux namespace 里。推荐 docker-compose 把 chromium + browser-harness 放一个 service。本 skill 不直接支持，参考上游 `browser-use/browser-harness` 的 README。

**Q：`bhts` 找不到？**
A：检查 `npm bin -g`（npm < 9）或 `npm prefix -g` + `/bin`（npm ≥ 9）有没有进 PATH：
```bash
echo "$PATH" | tr ':' '\n' | grep -i node
# 或加进 PATH：
echo 'export PATH="$(npm prefix -g)/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```
