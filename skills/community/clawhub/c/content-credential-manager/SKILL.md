---
name: content-credential-manager
description: 内容创业凭证管理器。追踪和管理已安装技能的 API 凭证配置状态，引导用户逐步完成每个平台的凭证配置，让内容创作技能从"装好了"到"真正可用"。触发场景：(1) 用户问"哪些技能可以用了"、"凭证配置好了吗"；(2) 开始内容创作前检查环境；(3) 新技能安装后登记凭证状态；(4) 排查"为什么XX技能不能用"。
---

# 内容创业凭证管理器

管理内容创业技能矩阵的凭证状态，解决"技能装了却用不了"的核心问题。

## 凭证状态一览

| 技能 | 凭证 | 状态 | 配置路径 |
|------|------|------|----------|
| wechat-publish-skill | WECHAT_APP_ID + WECHAT_APP_SECRET | ❌ 未配置 | mp.weixin.qq.com → 设置 → 基本设置 |
| other-openclaw-skills（美图） | MEITU_OPENAPI_ACCESS_KEY + MEITU_OPENAPI_SECRET_KEY | ❌ 未配置 |  miraclevision.com/open-claw |
| Auto-Redbook-Skills | XHS_COOKIE | ❌ 未配置 | 浏览器登录 xiaohongshu.com 获取 |
| step-tts | STEPFUN_API_KEY | ❌ 未配置 | platform.stepfun.com → API密钥 |
| tavily-search / openclaw-tavily-search | TAVILY_API_KEY | ❌ 未配置 | app.tavily.com → API Key |
| xhs-analytics-skill | 无需凭证（公开数据） | ✅ 可用 | - |

## 凭证配置文件

所有凭证保存在 `~/.openclaw/credentials.json`：

```json
{
  "wechat": {
    "app_id": "wx_xxxxxxxxxxxx",
    "app_secret": "xxxxxxxxxxxxxxxx"
  },
  "meitu": {
    "access_key": "xxxxxxxx",
    "secret_key": "xxxxxxxx"
  },
  "xiaohongshu": {
    "cookie": "xsecappid=xxx; web_session=xxx; ..."
  },
  "stepfun": {
    "api_key": "sk-xxxxxxxxxxxxxxxx"
  },
  "tavily": {
    "api_key": "tvly-xxxxxxxxxxxxxxxx"
  }
}
```

## 工作流程

### 场景一：检查当前可用性

```bash
# 查看所有技能凭证状态
python3 skills/content-credential-manager/scripts/check_status.py
```

输出示例：
```
📋 凭证状态检查

✅ 可用（无需凭证）：
  - xhs-analytics-skill

❌ 需要配置：
  - wechat-publish-skill: WECHAT_APP_ID + WECHAT_APP_SECRET
  - other-openclaw-skills: MEITU_ACCESS_KEY + MEITU_SECRET_KEY
  - Auto-Redbook-Skills: XHS_COOKIE
  - step-tts: STEPFUN_API_KEY
  - tavily-search: TAVILY_API_KEY

完成度：1/6
```

### 场景二：配置单个凭证

按以下顺序优先配置（从易到难）：

#### 1. Tavily（最容易，5分钟）
1. 去 https://app.tavily.com 注册
2. Get API Key → 复制
3. 告诉我："Tavily API Key 是 tvly-xxxxx"
4. 我帮你写入 `~/.openclaw/credentials.json`

#### 2. 阶跃星辰 TTS（5分钟）
1. 去 https://platform.stepfun.com 注册
2. 开发者中心 → API密钥 → 创建密钥
3. 告诉我："StepFun API Key 是 sk-xxxxx"
4. 我帮你写入配置

#### 3. 美图开放平台（10分钟）
1. 去 https://www.miraclevision.com/open-claw 注册
2. 创建应用 → 获取 AK/SK
3. 告诉我 AK 和 SK
4. 我帮你配置

#### 4. 小红书 Cookie（10分钟，需要浏览器）
1. 电脑浏览器打开 https://www.xiaohongshu.com 登录
2. 按 F12 → Network → 任意请求 → 复制 Request Headers 里的 Cookie
3. 告诉我完整的 Cookie 字符串

#### 5. 微信公众号（需要已认证公众号，15分钟）
1. 去 https://mp.weixin.qq.com 注册/登录
2. 设置 → 基本设置 → 复制 AppID 和 AppSecret
3. 告诉我，我会帮你验证并保存

### 场景三：验证配置是否成功

```bash
# 验证微信凭证
python3 skills/content-credential-manager/scripts/verify_wechat.py

# 验证美图凭证
python3 skills/content-credential-manager/scripts/verify_meitu.py

# 验证小红书Cookie
python3 skills/content-credential-manager/scripts/verify_xhs.py

# 验证TTS
bash skills/step-tts/scripts/tts.sh config
```

### 场景四：开始内容创作前的完整检查

执行以下检查清单：

```
□ Tavily API Key — 搜索功能可用
□ StepFun API Key — 语音合成可用
□ 美图 AK/SK — 图片生成可用
□ 小红书 Cookie — 内容发布可用
□ 微信公众号凭证 — 公众号发布可用
□ xhs-analytics-skill — 数据分析可用（无需凭证）

完成度 X/6 → 开始创作！
```

## 凭证安全原则

- 凭证文件权限：`600`（仅本人可读写）
- 凭证不写入 SKILL.md 或任何公开文件
- 用户通过对话提供凭证，我负责写入本地文件
- 不在日志或回忆中回显完整凭证（只显示前后各2位）

## 凭证写入脚本

用户给出凭证后，执行：

```bash
python3 skills/content-credential-manager/scripts/set_credential.py <platform> <key> <value>
```

例如：
```bash
python3 skills/content-credential-manager/scripts/set_credential.py tavily api_key tvly-xxxxx
```

## 凭证缺失时的降级策略

某个凭证缺失时，内容创作流程的降级方案：

| 技能 | 凭证缺失时的降级 |
|------|----------------|
| Auto-Redbook-Skills | 仍可生成 Markdown + 图片（本地渲染），仅发布功能不可用 |
| wechat-publish-skill | 仅不能自动发布到草稿箱，可导出 HTML 手动复制 |
| step-tts | 跳过语音生成，保留图文版本 |
| other-openclaw-skills | 部分美图功能不可用，可使用其他图像技能替代 |

---

*设计原则：凭证配置是内容创业的最后一公里。本技能让这最后一公里可管理、可执行。*
