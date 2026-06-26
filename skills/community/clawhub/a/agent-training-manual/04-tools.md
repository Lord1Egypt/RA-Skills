# 04 — 工具使用指南

> 工具是好工具，但用错了就是凶器。

## 🔧 通用原则

### 工具调用失败 → 立即停止

```
❌ 看到工具报错 → 先忽略继续做别的 → 等用户问了再说
✅ 看到工具报错 → 立即停止 → 分析原因 → 修复或汇报
```

这是最容易犯的错误。工具失败了你还继续往下做，最后跟用户说"搞定了"，用户一看发现根本没搞定。信任瞬间归零。

### 先读文档再用技能

```
❌ 看到技能名字就猜怎么用 → 自己发明配置参数
✅ 先读 SKILL.md → 按文档说明操作
```

### 浏览器用完要关

```
✅ 用完直接 browser stop（关闭整个应用）
❌ 只关标签页（没别人用，直接关应用）
```

## 📄 飞书文档

### 创建流程

```
1. feishu_doc create → 拿到 doc_token
2. feishu_doc write → 写入内容
3. feishu_doc read → 验证内容非空（block_count > 1）
4. 如果需要外部访问 → 设置公开权限
```

### 常见坑

```
❌ create 后不 write（文档永远是空的）
❌ write 后不 read 验证（写入可能静默失败）
❌ 用 markdown 图片语法（飞书不支持，要用 upload_image）
❌ 发给外部用户但没设公开权限（对方打不开）
❌ 用国际版域名发给国内用户（feishu.cn vs larkoffice.com）
```

### 权限设置

发给组织外的人时，必须设置公开权限：
```
external_access_entity: "open"
link_share_entity: "anyone_readable"
```

## 📧 邮件（Gmail / gog）

### 正确用法

```bash
# 使用 wrapper 脚本（如有）
bash scripts/gog-gmail.sh gmail send \
  --to "recipient@example.com" \
  --subject "标题" \
  --body-html "<p>正文</p>"
```

### 常见坑

```
❌ 用 gog auth list 检查状态（WSL2 无 TTY 环境 keyring 不可用）
❌ --to A --to B 发多人（后面覆盖前面，只发给最后一个）
✅ 多人分开发，每人一封
❌ OAuth token 过期后继续尝试发送
✅ token 过期 → 通知用户重新授权
```

### 中文编码

```
发件人中文名：=?UTF-8?B?base64编码?=
邮件主题中文：需要 MIME 编码
```

## 🔍 博查搜索 API

### 配置

```
Endpoint: api.bocha.cn（不是 bochaai.com）
计费：Web Search ¥0.036/次
```

### 省钱策略

```
✅ 每次 count:10，一次搞定不重复搜
✅ 用中文关键词 + 日期更精准
✅ freshness:oneWeek 或 threeDays 限定时间范围
✅ 优先用免费方案（RSS、Reddit JSON API、web_fetch）
❌ site: 语法在博查不好使
```

## 🌐 Reddit

### 免费 JSON API

```bash
# 热帖
curl -H "User-Agent: YourBot/1.0" \
  "https://old.reddit.com/r/subreddit/hot/.json?limit=15"

# 搜索
curl -H "User-Agent: YourBot/1.0" \
  "https://old.reddit.com/r/subreddit/search/.json?q=keyword&sort=new&restrict_sr=on&limit=10"
```

### 注意事项

```
✅ 必须用 old.reddit.com
✅ 必须带 User-Agent header
❌ 不用 www.reddit.com（容易被 bot detection 拦截）
```

## 📊 Mermaid 图表

```bash
# 生成 PNG
mmdc -i input.mmd -o output.png -w 1200 -H 700

# 安装（用国内镜像）
npm config set registry https://registry.npmmirror.com
npm install -g @mermaid-js/mermaid-cli
```

## 🖥️ Git

### 推送前检查

```bash
git status          # 有没有未提交的文件
git remote -v       # remote URL 对不对（token 在这里）
gh auth status      # GitHub CLI 认证状态
```

### 常见坑

```
❌ push 失败了没注意 → 以为已经推上去了
✅ push 后检查返回码
❌ 忘了 git remote URL 里有 token → 说"需要用户配置"
✅ 先 git remote -v 检查已有配置
```

## ⏰ Cron 任务

### 配置规范

```
✅ delivery 必须指定 channel 和 to（不要用 "last"）
✅ schedule 必须指定 tz（时区）
✅ 配置前先 cron list 检查有没有重复任务
✅ agentTurn payload 不要配置 thinking/reasoning 参数
❌ 不要在 cron agentTurn 中配 thinking（会导致模型报错）
```

### 监控

```
每次心跳必须 cron list，检查所有任务的 consecutiveErrors
发现 > 0 立即排查
```

## 🔐 代理/网络

### WSL2 网络

```
✅ 永远用 windows-host hostname，不要硬编码 IP
✅ WSL2 重启后 nameserver IP 会变
✅ /etc/hosts 映射 windows-host → 当前 nameserver IP
```

---

*"工具本身不会出错，出错的是用法。" — 悠悠*
