# xhs-cli — 小红书搜索工具参考

本 skill 使用 xhs-cli 从小红书获取活动相关的用户攻略笔记和评论内容。
以下仅列出本 skill 实际使用的命令子集（搜索、阅读、评论），完整功能请参考 [xiaohongshu-cli](https://github.com/jackwener/xiaohongshu-cli)。

---

## 安装

```bash
# 推荐：uv tool（快速、隔离环境）
uv tool install xiaohongshu-cli

# 或者：pipx
pipx install xiaohongshu-cli
```

升级到最新版本（建议定期升级以避免 API 调用异常）：

```bash
uv tool upgrade xiaohongshu-cli
# 或：pipx upgrade xiaohongshu-cli
```

> **环境要求：** Python >= 3.10

---

## 认证

xhs-cli 需要小红书 Cookie 才能工作。支持三种认证方式：

1. **已保存 Cookie** — 从 `~/.xiaohongshu-cli/cookies.json` 加载
2. **浏览器 Cookie 自动提取** — 支持 Chrome、Arc、Edge、Firefox、Safari、Brave 等
3. **二维码扫码登录** — 终端显示二维码，用小红书 App 扫码

### 认证命令

```bash
# 检查是否已认证（Agent 优先执行此命令）
xhs status --yaml >/dev/null && echo "AUTH_OK" || echo "AUTH_NEEDED"

# 从浏览器提取 Cookie（自动检测）
xhs login

# 指定浏览器
xhs login --cookie-source chrome

# 二维码扫码登录（浏览器 Cookie 不可用时使用）
xhs login --qrcode

# 验证登录
xhs status
xhs whoami

# 清除 Cookie
xhs logout
```

### 常见认证问题

| 错误 | 处理方式 |
|------|---------|
| `NoCookieError: No 'a1' cookie found` | 引导用户在浏览器中打开 xiaohongshu.com 并登录，然后执行 `xhs login` |
| `NeedVerifyError: Captcha required` | 请用户在浏览器中完成验证码，然后重试 |
| `IpBlockedError: IP blocked` | 建议切换网络（手机热点或 VPN） |
| `SessionExpiredError` | 执行 `xhs login` 刷新 Cookie |

> Cookie 有效期约 **7 天**，过期后自动尝试从浏览器刷新。

---

## 输出格式

所有命令支持 `--json` 和 `--yaml` 结构化输出。非 TTY 环境（如被 Agent 调用时）自动输出 YAML。

**统一信封格式（参见 SCHEMA.md）：**

```yaml
# 成功
ok: true
schema_version: "1"
data: { ... }

# 失败
ok: false
schema_version: "1"
error:
  code: not_authenticated
  message: need login
```

> **Agent 使用建议：** 优先使用 `--yaml` 获取结构化输出，除非需要严格 JSON 才用 `--json`。

---

## 命令参考

### 1. 搜索笔记 — `xhs search`

```bash
xhs search <keyword> [选项]
```

| 选项 | 说明 | 可选值 | 默认值 |
|------|------|--------|--------|
| `--sort` | 排序方式 | `general`（综合）、`popular`（最热）、`latest`（最新） | `general` |
| `--type` | 笔记类型 | `all`（全部）、`video`（视频）、`image`（图文） | `all` |
| `--page` | 页码 | 整数 | `1` |
| `--json` | 输出 JSON | — | — |
| `--yaml` | 输出 YAML | — | — |

**示例：**

```bash
# 搜索演唱会攻略（按热度排序）
xhs search "周杰伦演唱会 上海 攻略" --sort popular --yaml

# 搜索漫展视频攻略
xhs search "CP32 漫展攻略" --type video --yaml

# 翻页搜索
xhs search "livehouse 推荐" --page 2 --yaml
```

**输出字段（data 部分）：**

```yaml
items:
  - id: "笔记ID"
    xsec_token: "token值"
    note_card:
      display_title: "标题"
      type: "normal"  # normal=图文, video=视频
      cover:
        url_default: "封面图URL"
      corner_tag_info:
        - type: publish_time
          text: "2025-02-20"  # 发布日期，有时为相对时间如 "5天前"
      interact_info:
        liked_count: "点赞数"
        collected_count: "收藏数"
        comment_count: "评论数"
      user:
        nickname: "作者昵称"
        user_id: "用户ID"
```

> 搜索后会自动缓存结果的短索引，可直接用 `xhs read 1` 阅读第一条结果。

---

### 2. 阅读笔记详情 — `xhs read`

```bash
xhs read <id_or_url_or_index> [选项]
```

支持三种输入：

- **短索引**：`xhs read 1` — 读取最近一次列表（search/feed/hot）的第 N 条（**从 1 开始，不是 0**）
- **笔记 ID**：`xhs read <note_id>` — 直接通过 API 读取
- **完整 URL**：`xhs read "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"` — 从 URL 提取 token 并读取

| 选项 | 说明 |
|------|------|
| `--xsec-token` | 手动指定安全 token（通常不需要，会自动从缓存获取） |
| `--json` | 输出 JSON |
| `--yaml` | 输出 YAML |

**示例：**

```bash
# 搜索后直接读取第一条结果
xhs search "演唱会攻略" --yaml
xhs read 1 --yaml

# 通过 URL 读取
xhs read "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --yaml
```

**输出关键字段（data 部分）：**

```yaml
title: "笔记标题"
desc: "正文内容（纯文本）"
time: 1732502777000              # 发布时间（Unix 毫秒时间戳）
last_update_time: 1740041732000  # 最后更新时间（Unix 毫秒时间戳）
type: "normal"                   # normal=图文, video=视频
interact_info:
  liked_count: "点赞数"
  collected_count: "收藏数"
  comment_count: "评论数"
image_list:                      # 图片列表
  - url_default: "图片URL"
```

---

### 3. 查看评论 — `xhs comments`

```bash
xhs comments <id_or_url_or_index> [选项]
```

同样支持短索引、笔记 ID、URL 三种输入。

| 选项 | 说明 |
|------|------|
| `--all` | 自动翻页获取全部评论 |
| `--cursor` | 手动分页游标 |
| `--xsec-token` | 手动指定安全 token |
| `--json` | 输出 JSON |
| `--yaml` | 输出 YAML |

**示例：**

```bash
# 获取搜索结果第一条的评论
xhs search "上海演唱会 攻略" --yaml
xhs comments 1 --yaml

# 获取全部评论（自动翻页）
xhs comments 1 --all --yaml

# 通过 URL 获取评论
xhs comments "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --all --yaml
```

**输出字段（`--all` 模式 data 部分）：**

```yaml
comments:
  - id: "评论ID"
    content: "评论内容"
    user_info:
      nickname: "评论者昵称"
    like_count: "点赞数"
    sub_comment_count: "回复数"
    create_time: 1700000000000
total_fetched: 120
pages_fetched: 3
```

---

### 4. 查看子评论 — `xhs sub-comments`

```bash
xhs sub-comments <note_id> <comment_id> [选项]
```

| 选项 | 说明 |
|------|------|
| `--cursor` | 分页游标 |
| `--json` | 输出 JSON |
| `--yaml` | 输出 YAML |

**示例：**

```bash
xhs sub-comments abc123 cmt456 --yaml
```

---

## 典型工作流

### 搜索攻略 → 阅读详情 → 获取评论

```bash
# 1. 搜索相关攻略
xhs search "周杰伦演唱会 上海 攻略" --sort popular --yaml

# 2. 阅读高赞笔记详情（短索引）
xhs read 1 --yaml

# 3. 获取该笔记的全部评论（用户真实反馈）
xhs comments 1 --all --yaml
```

### URL 直接获取内容

```bash
# 用户提供了一个小红书链接
xhs read "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --yaml
xhs comments "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --all --yaml
```

---

## Agent 安全须知

- **不要并行请求** — 内置高斯随机延迟（~1-1.5s）是为了模拟人类浏览行为，避免触发风控
- **批量操作之间加延迟** — 多次 CLI 调用之间建议间隔 2 秒以上
- **验证码恢复** — 触发 `NeedVerifyError` 后客户端会自动冷却（5s→10s→20s→30s），请用户在浏览器中完成验证码后重试
- **Cookie 是敏感信息** — 不要在聊天记录中输出原始 Cookie 值
- **不要绕过限速** — 内置延迟是为了保护用户账号安全

---

## 故障排查

| 问题 | 处理方式 |
|------|---------|
| Cookie 过期 / `SessionExpiredError` | 执行 `xhs login` 重新提取浏览器 Cookie |
| 浏览器 Cookie 提取失败 | 尝试指定浏览器 `xhs login --cookie-source chrome`，或使用 `xhs login --qrcode` 扫码登录 |
| `NoCookieError: No 'a1' cookie found` | 用户需先在浏览器中打开 https://www.xiaohongshu.com 并登录 |
| `NeedVerifyError: Captcha required` | 请用户在浏览器中打开小红书完成验证码，然后重试 |
| `IpBlockedError: IP blocked` | 建议切换网络（手机热点或 VPN） |
| 请求频率过快 | xhs-cli 内置限速（~1-1.5s），不要并行调用；多次调用间隔 2 秒以上 |
