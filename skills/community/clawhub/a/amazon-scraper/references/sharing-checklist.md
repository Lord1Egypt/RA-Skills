# 打包分享 amazon-scraper skill 前的检查清单

代理凭证是**付费/专属资源**（消耗流量和额度，出口 IP 被风控会连带影响自己），而且一旦发出去就必须当作已泄露处理。

## 规则：永远不打包真实凭证

没有"对方是自己人所以可以原样发"这个选项。Discord / 微信 / 网盘里的 zip 会被转发、会留在聊天记录里、会被对方的 agent 读到，你无法回收。接收方要用，就让他填自己的凭证，或者你单独通过密码管理器把凭证发给他。

`config/proxies.json` 已经进了 `.gitignore` 和 `.dockerignore`，默认不会被提交也不会进镜像。打包时仍然要显式确认。

## 打包前必做的扫描

```bash
cd /path/to/amazon-scraper

# 1. 凭证文件不该存在于打包内容里
ls config/proxies.json 2>/dev/null && echo "!! 删除或替换成 proxies.example.json 再打包"

# 2. 全目录扫一遍 user:pass@host 形式的凭证（含 references/ 和 scripts/）
grep -rnE '[A-Za-z0-9_.-]+:[^@/[:space:]]{6,}@[A-Za-z0-9.-]+' . \
  --include='*.md' --include='*.json' --include='*.js' --include='*.py' --include='*.sh'

# 3. 扫 token / key / 密码字样
grep -rniE 'password|secret|api[_-]?key|token|base_token' . \
  --include='*.md' --include='*.json' --include='*.js' --include='*.py' --include='*.sh'
```

第 2、3 步的输出必须只剩占位符（`USERNAME`、`PASSWORD`、`YOUR_BASE_TOKEN`、`ENTRY_HOST` 之类）。**`references/` 和脚本注释同样要查** —— 曾经发生过 `proxies.json` 已经替换成占位符，但 `references/oxylabs-proxy-format.md` 的示例和 `sharing-checklist.md` 的"复盘"里还留着真实用户名密码，等于白替换。

## 打包

```bash
cd "$(dirname /path/to/amazon-scraper)"
tar --exclude='config/proxies.json' \
    --exclude='node_modules' --exclude='__pycache__' --exclude='*.db' \
    -czf ~/amazon-scraper-$(date +%Y%m%d).tar.gz amazon-scraper
```

打完再验一遍，确认凭证没混进压缩包：

```bash
tar -xzOf ~/amazon-scraper-*.tar.gz | grep -nE '[A-Za-z0-9_.-]+:[^@/[:space:]]{6,}@' || echo "clean"
```

## 接收方使用步骤

```bash
tar -xzf amazon-scraper-YYYYMMDD.tar.gz && cd amazon-scraper
cp config/proxies.example.json config/proxies.json   # 填自己的凭证
bash scripts/setup.sh
docker run --rm -e AMAZON_PROXIES="http://USER:PASS@HOST:PORT" \
  amazon-scraper node assets/amazon_handler.js \
  "https://www.amazon.com/gp/bestsellers/electronics"
```

## 如果已经把真实凭证发出去了

先轮换，再谈别的。顺序：

1. 到代理商后台改密码 / 重新生成 sub-user 凭证，让旧凭证立即失效。
2. 检查用量账单有没有不是你产生的流量。
3. 如果凭证进过 git 历史或 Docker 镜像层，改密码之后那些副本自然失效 —— 但镜像和历史里的字符串仍然在，该清理就清理（`docker rmi` 旧镜像；git 历史用 `git filter-repo`）。
4. 收回分发渠道里的文件（撤回消息、删网盘链接），当作补充措施，不要当作主要手段。
