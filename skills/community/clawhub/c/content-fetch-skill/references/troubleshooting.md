# Twitter/X.com 抓取故障排查

## 常见问题

### 1. Cloudflare 拦截

**症状:**
```
status: 403, message: "<!DOCTYPE html>...Cloudflare...Sorry, you have been blocked"
```

**原因:** 代理 IP 是数据中心 IP，被 Cloudflare 识别为机器人流量。

**解决方案:**
- 使用住宅 IP 代理 (如 IPRoyal, Bright Data, Oxylabs)
- 检查订阅服务是否有住宅 IP 套餐
- 尝试切换不同节点

### 2. 代理连接失败

**症状:**
```
net::ERR_PROXY_CONNECTION_FAILED
```

**解决方案:**
```bash
# 检查代理是否运行
ss -tlnp | grep 7890

# 测试代理连接
curl -x http://127.0.0.1:7890 -s --connect-timeout 10 http://ip.sb

# 测试 X.com 访问
curl -x http://127.0.0.1:7890 -s -o /dev/null -w "%{http_code}" https://x.com

# 如果返回 200 表示代理正常
```

### 3. 登录失败 - 找不到密码框

**症状:**
```
⚠️ 未找到密码框
```

**原因:**
- X 登录流程变化
- 有已保存账户，需要先点击
- 需要邮箱验证

**解决方案:**
1. 脚本会自动检测已保存账户并点击
2. 如果需要验证，提供 `--email` 参数
3. 查看控制台输出的登录流程信息

### 4. 推文数量少

**解决方案:**
- 确保成功登录（查看是否有 "✅ 登录成功" 输出）
- 增加 `--scroll` 参数，建议 30-50 次
- 检查目标用户是否真的有这么多推文

### 5. 推文内容被截断

**症状:** 推文以 "..." 结尾，不完整

**解决方案:**
脚本已内置自动展开功能，会点击 "Show more" / "显示更多" 按钮。查看日志是否有：
```
点击展开: Show more...
```

如果没有看到展开日志，可能是：
- 页面加载太慢，增加 `asyncio.sleep` 时间
- 按钮选择器变化，需要更新脚本

## 代理配置

### Mihomo (Clash Meta) 完整配置

```yaml
# config.yaml
mixed-port: 7890
allow-lan: true
mode: rule
log-level: info
external-controller: 127.0.0.1:9090

proxies:
  - name: "节点1"
    type: ss
    server: xxx
    port: 9901
    cipher: aes-256-gcm
    password: "xxx"

  - name: "节点2"
    type: vmess
    server: xxx
    port: 9901
    uuid: "xxx"
    alterId: 0
    cipher: auto

proxy-groups:
  - name: "Proxy"
    type: select
    proxies:
      - "Auto"
      - "节点1"
      - "节点2"
      - DIRECT

  - name: "Auto"
    type: url-test
    proxies:
      - "节点1"
      - "节点2"
    url: "http://www.gstatic.com/generate_204"
    interval: 300

rules:
  - DOMAIN-SUFFIX,x.com,Proxy
  - DOMAIN-SUFFIX,twitter.com,Proxy
  - DOMAIN-SUFFIX,twimg.com,Proxy
  - MATCH,Proxy
```

### 启动和切换节点

```bash
# 启动 mihomo
cd /home/gem/workspace/agent/workspace/mihomo
./mihomo -d . &

# 切换节点
curl -X PUT "http://127.0.0.1:9090/proxies/Proxy" \
  -H "Content-Type: application/json" \
  -d '{"name":"节点1"}'

# 查看当前节点
curl -s "http://127.0.0.1:9090/proxies/Proxy" | jq '.now'
```

## 完整使用示例

```bash
# 1. 启动代理
cd /home/gem/workspace/agent/workspace/mihomo
nohup ./mihomo -d . > /tmp/mihomo.log 2>&1 &

# 2. 等待代理启动
sleep 3

# 3. 切换到稳定节点
curl -s -X PUT "http://127.0.0.1:9090/proxies/Proxy" \
  -H "Content-Type: application/json" \
  -d '{"name":"JMS-VMess-4"}'

# 4. 运行抓取
python3 /home/gem/workspace/agent/skills/twitter-scraper/scripts/scrape_twitter.py \
  --proxy http://127.0.0.1:7890 \
  --username timy530 \
  --password "your_password" \
  --email "your_email@example.com" \
  --target formnoshape \
  --scroll 40

# 5. 查看结果
cat /home/gem/workspace/agent/workspace/twitter_data/tweets_formnoshape.json | jq '.[0]'
```

## 输出文件结构

```json
[
  {
    "id": "2013244429264650614",
    "text": "推文完整内容...",
    "created_at": "2026-01-19T13:37:30.000Z",
    "url": "https://x.com/status/2013244429264650614",
    "like_count": 232,
    "retweet_count": 27,
    "reply_count": 20
  }
]
```

## 增量更新机制

脚本支持增量更新：
- 读取已有的 JSON 文件
- 与新抓取的推文合并（按 ID 去重）
- 按时间倒序排列
- 显示统计：原有 + 新增 = 合计

这样多次运行不会丢失数据，适合持续监控某个用户。
