# Playwright 使用重点（含 Ubuntu 25 / 本地安装失败的 Docker 兜底）

## 1. 项目基础建议

- Node 版本建议：18+（LTS 更稳）
- 优先 TypeScript：便于类型提示与维护
- 目录建议：
  - `tests/`：测试用例
  - `playwright.config.ts`：全局配置
  - `test-results/`：执行产物

## 2. Playwright 配置重点

建议开启以下能力：

- `trace: 'on-first-retry'`（重试时自动保留 trace）
- `screenshot: 'only-on-failure'`
- `video: 'retain-on-failure'`
- 合理 `timeout` / `expect.timeout`
- `retries` 在 CI 中可设 1~2，本地可为 0

## 3. 编写用例重点

- 优先使用语义定位：`getByRole`、`getByLabel`
- 每个关键步骤后都要有断言
- 不使用固定 sleep，改用状态等待（如 `toBeVisible`、`toHaveURL`）
- 对网络依赖场景，必要时增加 `waitForResponse` 或 mock

## 4. 本地安装模式（优先）

```bash
npm i -D playwright
npx playwright install chromium
```

若系统依赖安装失败（如 Ubuntu 25 与官方依赖列表不完全匹配），不要卡住，直接切 Docker 模式。

## 5. Docker 兜底模式（推荐在 Ubuntu 25/受限环境使用）

使用官方镜像运行测试，避免本机缺库问题。

### 5.1 一次性运行

```bash
docker run --rm -t \
  -v "$PWD":/work \
  -w /work \
  mcr.microsoft.com/playwright:v1.58.2-jammy \
  bash -lc "npm ci || npm i && npx playwright test"
```

### 5.2 带产物目录

```bash
docker run --rm -t \
  -v "$PWD":/work \
  -w /work \
  mcr.microsoft.com/playwright:v1.58.2-jammy \
  bash -lc "mkdir -p test-results && npm ci || npm i && npx playwright test --reporter=line,html --output=test-results"
```

## 6. 切换规则（必须执行）

当出现以下任一情况，直接使用 Docker 方案：

- `npx playwright install-deps` 失败且短时间无法获取 sudo/root
- 系统仓库缺失关键依赖包（如 Ubuntu 新版本包名变化）
- 本地浏览器启动报缺库错误（`error while loading shared libraries`）

## 7. 报告与证据

- 执行后保留：`run.log`、截图、视频、trace
- 报告中明确注明执行模式：`local` 或 `docker`
- 如果是 Docker 模式，附上镜像版本（如 `v1.58.2-jammy`）
