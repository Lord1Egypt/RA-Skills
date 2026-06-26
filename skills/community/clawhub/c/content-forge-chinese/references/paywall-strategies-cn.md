# 付费墙策略国内重排

> 上游 6 层级联在国内网络下大面积失效，本文档给出**国内特化优先级**，被 SKILL.md 主流程引用。

## 国内 vs 海外的关键差异

| 策略 | 海外网络 | 国内网络（裸） | 国内 + 代理 |
|---|---|---|---|
| Layer 1 - r.jina.ai 代理 | 🟢 | 🟡（受限） | 🟢 |
| Layer 2 - Bot UA 伪装 | 🟢 | 🟡 | 🟢 |
| Layer 3 - 通用伪装 | 🟢 | 🟢 | 🟢 |
| Layer 4 - archive.today | 🟢 | 🔴 域名被污染 | 🟡 |
| Layer 5 - Google Cache | 🟢 | 🔴 完全不可达 | 🟢 |
| Layer 6 - agent-fetch 本地 | 🟢 | 🟢 | 🟢 |

## 国内场景重排后的优先级

### 海外付费墙（NYT / WSJ / FT / Economist）

```
P1: r.jina.ai 代理 (Layer 1)         ← 国内+代理可用，速度快
P2: Bot UA 伪装 (Layer 2)             ← 部分站点有效
P3: 通用伪装 (Layer 3)                ← 兜底
P4: agent-fetch 本地 (Layer 6)         ← 终极方案
P5: Google Cache (Layer 5)            ← 仅当代理稳定
P6: archive.today (Layer 4)           ← 不稳定，能不用就不用
```

### 国内付费墙（财新 / 36氪 Pro / 虎嗅 / 得到）

```
P1: 用户 cookie 注入（订阅用户）    ← 唯一 100% 方案
P2: 微信公众号搜一搜镜像             ← 中文站点经常有公众号同步
P3: AMP 页面                          ← caixin / 36kr 有 AMP
P4: 通用伪装 + AMP（Layer 3 子集）
P5: 用户手动复制粘贴                  ← 兜底
```

> ⚠️ 国内站点**不要走海外代理**，否则更容易触发反爬。

### 微信公众号

公众号没"付费墙"概念，但有**反爬**：

```
P1: wexin-read MCP（Playwright 模拟）
P2: 用户提供登录态 cookie
P3: 用户复制粘贴文本
```

公众号原创文章不能批量爬，否则封号。

## 配置文件示例

把这套优先级写到 `~/.workbuddy/skills/neirong-gongfang/scripts/paywall-priority.json`：

```json
{
  "overseas_paywall": [
    {"layer": 1, "method": "jina-proxy", "enabled": true},
    {"layer": 2, "method": "bot-ua", "enabled": true},
    {"layer": 3, "method": "generic-disguise", "enabled": true},
    {"layer": 6, "method": "agent-fetch", "enabled": true},
    {"layer": 5, "method": "google-cache", "enabled": true},
    {"layer": 4, "method": "archive-today", "enabled": false}
  ],
  "domestic_paywall": [
    {"method": "user-cookie", "enabled": true},
    {"method": "wechat-mirror", "enabled": true},
    {"method": "amp-version", "enabled": true},
    {"method": "manual-paste", "enabled": true}
  ]
}
```

AI 在工作流中：
1. 解析 URL → 判断海外/国内
2. 加载对应优先级表
3. 按顺序尝试，成功即停
4. 全部失败 → 提示用户手动复制粘贴
