# Brave Web Search

## 说明

- 用 openclaw 自带的搜索工具的 Brave 配置不方便携带代理信息。
- 另外 openclaw 搜索工具只能同时支持一个搜索引擎，如果需要多引擎搜索，还是要用Skills。
- 最好在 openclaw 的 TOOLS.md 加入类似 **"搜索时请调用brave-search skill，不要用自带的web_search工具功能"** 的指示，否则 openclaw 可能消耗额外的token去尝试工具调用。
- 同时可以在 openclaw.json 中将 web_search 关闭。
```openclaw.json
  "tools": {
    "web": {
      "enabled": false
    }
  }
```

## 前置条件

### Brave API Key

在Brave官网：
https://brave.com/ -> Search API -> Log in/sign up

https://api-dashboard.search.brave.com/app/settings/billing 【Billing】-> Payment method -> 绑定外币信用卡/apple pay外币信用卡

https://api-dashboard.search.brave.com/app/subscriptions/subscribe 【Available plans】-> 开通 Search Plan -> 每月有1000免费额度

https://api-dashboard.search.brave.com/app/keys 【API keys】 -> 创建 API Key


### 配置环境变量

* 当前bash内生效（测试）
```bash
export BRAVE_SEARCH_API_KEY="your_api_key"
```

* openclaw 配置文件
```.openclaw/openclaw.json
"env": {"BRAVE_SEARCH_API_KEY":"your_api_key"}
```

* 环境变量文件
```.openclaw/.env
BRAVE_SEARCH_API_KEY=your_api_key
```

### VPN

* 启动代理，将http端口号写入环境变量

* 当前bash内生效（测试）
```bash
export HTTP_PROXY_PORT=8118
```

* openclaw 配置文件
```.openclaw/openclaw.json
"env": {"HTTP_PROXY_PORT":"8118"}
```

* 环境变量文件
```.openclaw/.env
HTTP_PROXY_PORT=8118
```
