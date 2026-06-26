# 内容创业凭证管理器

管理内容创业技能矩阵的 API 凭证配置状态，解决"技能装了却用不了"的核心问题。

## 解决的问题

安装了很多内容创作技能（小红书、微信公众号、美图、TTS），但不知道哪些真正能用、缺什么凭证、去哪里申请。

## 核心功能

- **凭证状态全景图**：一行命令看清 6 个内容创业技能的可用状态
- **配置引导**：每个平台附带申请链接和步骤，按难度排序
- **安全写入**：凭证统一写入 `~/.openclaw/credentials.json`，文件权限 `600`
- **降级策略**：明确缺少某个凭证时对整体流程的影响

## 凭证追踪清单

| 技能 | 凭证 | 状态 |
|------|------|------|
| wechat-publish-skill | WECHAT_APP_ID + WECHAT_APP_SECRET | 需配置 |
| other-openclaw-skills（美图） | MEITU_ACCESS_KEY + MEITU_SECRET_KEY | 需配置 |
| Auto-Redbook-Skills | XHS_COOKIE | 需配置 |
| step-tts | STEPFUN_API_KEY | 需配置 |
| tavily-search | TAVILY_API_KEY | 需配置 |
| xhs-analytics-skill | 无需凭证 | ✅ 可用 |

## 快速开始

```bash
# 查看凭证状态
python3 skills/content-credential-manager/scripts/check_status.py

# 写入凭证
python3 skills/content-credential-manager/scripts/set_credential.py <platform> <field> <value>
```

## 适用场景

- 新技能安装后登记凭证状态
- 开始内容创作前检查环境可用性
- 排查"为什么 XX 技能不能用"
- 追踪凭证配置进度
