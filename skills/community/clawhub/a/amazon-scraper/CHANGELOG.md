# Changelog

## 4.0.1

- 确认按 OpenClaw skill 格式加载：`SKILL.md` 有 `name`、`description` 和 `metadata.openclaw.requires.bins: [docker]`。
- 发布包里的安装路径和定时任务改成 OpenClaw：`~/.openclaw/skills`、`~/.openclaw/amazon-scraper/`、`openclaw automations`。

## 4.0.0 — 安全加固版（breaking）

这个版本同时合并了两件事：把此前只存在于本地打包（`3.3.4.1`）里的功能带进仓库，以及修掉一轮安全审计里的 20 条问题。完整审计见 `SECURITY-AUDIT.md`。

> ### ⚠️ 升级前必做：轮换代理凭证
>
> `3.x` 的 `config/proxies.json` 存明文凭证，并且被 `COPY` 进 Docker 镜像层。镜像层是只读历史，改文件甚至在后面的层里删掉它都取不走。只要你用 `3.x` 构建过镜像或把 skill 打包分享过，就要当作凭证已泄露：
>
> 1. 到代理商后台改密码 / 重建 sub-user；
> 2. `docker rmi amazon-scraper` 删掉所有旧镜像;
> 3. 查一遍流量账单。

### Breaking changes

| 变化 | 以前 | 现在 |
|---|---|---|
| 凭证来源 | `config/proxies.json` 烘进镜像 | 运行时注入：`-e AMAZON_PROXIES` 或挂载 `/app/config/proxies.json` |
| 配置优先级 | 文件优先，环境变量在文件非空时**完全失效** | `AMAZON_PROXIES` → `AMAZON_PROXY` → `AMAZON_PROXY_FILE`/`config/proxies.json` |
| 没有代理时 | 静默用宿主机 IP 去爬 | 直接报错退出（要保留旧行为需显式 `AMAZON_ALLOW_DIRECT=1`） |
| 输出状态 | 永远 `SUCCESS` | `SUCCESS` / `PARTIAL` / `ERROR`，退出码 0 / 3 / 2 |
| 容器用户 | root | `pwuser` |
| `Dockerfile` | 与 `Dockerfile.sh` 两份可能不一致的副本 | `Dockerfile.sh` 是唯一源，`setup.sh` 每次构建都重新生成 `Dockerfile`（已 gitignore） |
| `scripts/jev_expand.py` | 存在 | 已删除（从全局可写的 `/tmp` 执行解释器 = 任意代码执行） |
| `scrape_reviews.py` | 每次运行删掉该 ASIN 的历史评论 | 默认追加，要清空得显式 `--reset` |
| cookie / profile 路径 | `/tmp`（全局可写） | `$HOME/.cache/amazon-scraper-chrome`，`0700`/`0600` |

迁移通常只要两步：

```bash
export AMAZON_PROXIES="http://USER:PASS@HOST:PORT"     # 多条用逗号分隔
docker run --rm -e AMAZON_PROXIES -v ~/scrapes:/data amazon-scraper \
  node assets/amazon_handler.js "URL" --output result.json
```

并且**在写库或出报表前先判 `status`**。软拦截会返回 HTTP 200 + 全 null 字段，把它当成"价格没变"比没有数据更糟。

### 安全修复

- **凭证不再进仓库和镜像**：`config/proxies.json` 换成 `proxies.example.json` 模板，真实文件进 `.gitignore` / `.dockerignore` / `.clawhubignore`；`Dockerfile` 不再 `COPY config/`。
- **清理文档里的凭证**：`references/oxylabs-proxy-format.md` 和 `sharing-checklist.md` 各带着一组可用的 Oxylabs 凭证 —— 后者是一份"防泄露检查清单"，却在"真实案例"一节把凭证原样抄了一遍，于是即使 `proxies.json` 换成占位符，打包出去的 `references/` 里仍然有能用的凭证。两处都已替换，清单重写为可执行的全目录扫描，并删掉了「对方是自己人就直接打包原样」这个选项。
- **CDP 不再对任意网页开放**：文档不再教用户加 `--remote-allow-origins=*`（它关掉 WebSocket 的 Origin 校验，使这个浏览器里打开的任意网页都能接管它，而这个浏览器按设计带着真实 Amazon 登录态）和 `--no-sandbox`；调试口绑 `127.0.0.1`；两个 CDP 脚本都自己新开标签页并在结束时关掉，不再劫持用户正在用的标签页。
- **监控面板存储型 XSS**：listing 标题 / 五点 / 卖家名是卖家可控内容，原先被拼进 `innerHTML` 和 `<script>`。改为 `\uXXXX` 转义嵌入 + `createElement`/`textContent` 渲染，class 走白名单。
- `--output` 限制在挂载目录内，不能穿越写到容器其他位置。
- 日志只打 `host:port`，凭证不再出现在 stdout/stderr。
- storageState 按目标域名分 namespace，通用模式不再和 Amazon 共用一个 cookie 罐。

### Bug 修复

- `scripts/asin_monitor.py` 此前是 **SyntaxError，从未运行过**：HTML 模板用了 f-string，而模板里是 JS 模板字面量 `${p.title}`，被当成 Python 替换字段。改为普通字符串 + 占位符。
- 全部代理失败时不再报告 `SUCCESS`；详情页全字段 null 判定为软拦截并换代理重试。
- `-e AMAZON_PROXIES` 现在真的生效（见上表）。此前文档教的"5 容器各用不同出口"实际是 5 个容器打同一个 IP。
- 去掉所有 `docker run -t`：PTY 会把 stderr 合并进 stdout 并改写行尾，破坏被解析的 JSON。
- CDP 调用全部加超时（原先 `while True` + 无 timeout 可永久挂死）；消息 id 改单调递增（原先随机 id 可能错配应答）。
- `asin_price_monitor.py` 的价格历史改为合并而非整体覆盖（原先今天抓失败的 ASIN 会从历史里消失，下次变成"首次记录"）。
- `datetime.utcnow()` → `datetime.now(timezone.utc)`（已废弃且返回 naive 时间，面板按本地时区误读）。
- 三个 monitor 脚本的重复 `scrape_asin` 合并进 `scripts/scraper_client.py`。

### 其他

- Playwright 固定为与基础镜像一致的精确版本，`ARG PLAYWRIGHT_VERSION` 把两者绑在一处；有 lockfile 走 `npm ci`；删掉重复的 `npx playwright install`（基础镜像已自带浏览器）。
- 移除 `playwright-extra` / `puppeteer-extra-plugin-stealth` 依赖（已改为自带指纹模块 `assets/fingerprint.js`）。
- SKILL.md 的触发词收窄到 Amazon 商品/市场数据场景 —— 原先任何「爬取 / 抓取 / scrape」都会拉起这个 skill，用按流量计费的代理去抓无关网站。
- Docker 依赖写在 `SKILL.md` 的 `metadata.openclaw.requires.bins`，这是 OpenClaw 加载 skill 时认的格式。`package.json` 里不再放 `openclaw` 对象，否则当前 ClawHub CLI 会把整个目录当成插件拒绝发布。
- 文档和监控脚本里的旧运行时目录、cron 命令改成 `~/.openclaw/skills`、`~/.openclaw/amazon-scraper/` 和 `openclaw automations`。
- `references/reviews-strategy.md` 顶部新增前置说明：登录态抓评论的账号封禁风险、登录态即凭证、评论正文属第三方个人数据。

### 已知未验证

`Dockerfile` 改动是静态审查，**未经 `docker build` 验证**（审计环境没有 Docker 和可用代理）。升级后请先跑一遍：`bash scripts/setup.sh`、确认 `pwuser` 身份下 `/data` 可写、真实抓一次 BSR/搜索/详情确认 `status` 契约符合预期。

### 下一步建议（本版未做）

- 升级 Playwright / Chrome 基础镜像（当前 1.40.0 / Chrome 119 是 2023 年版本，有已知 CVE）。换大版本要同步改 `fingerprint.js` 的 UA 和 `Sec-Ch-Ua` 并回归选择器。
- 指纹绑定改为按"出口标识"而不是按端口：`BY_PORT` 只覆盖 8001–8005，端口不在表里时会静默走 host 哈希 fallback，所谓"同端口同指纹"并未生效。

---

## 3.4.1 及更早

见 git history。`3.4.1` 仍使用 `playwright-extra` + stealth 插件，没有 `assets/fingerprint.js`、`--asins`/`--queries`/`--bsr` 批量模式、`&page=` 翻页修复，也没有 `references/` 和 `scripts/` 下的 Python 工具。
