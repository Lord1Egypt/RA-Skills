---
name: fake-follower-audit
description: |
  CreatiVault official fake-follower and engagement-quality audit skill. MUST be used
  when the user wants to inspect one TikTok, Instagram, or YouTube creator for fake
  followers, suspicious engagement, bot/template comments, audience authenticity,
  interaction quality, creator risk, or account health. Accepts a creator profile URL
  or platform plus username/user ID and calls CreatiVault OpenAPI through
  scripts/fake_follower_audit.mjs. Do not infer fake-follower risk from public web
  pages or follower counts alone.
  Use when: fake follower audit, fake followers, follower authenticity, engagement
  authenticity, suspicious followers, bot comments, creator risk, account health,
  假粉检测, 假粉率, 粉丝真实性, 互动真实性, 刷粉, 刷量, 机器评论, 达人风险,
  账号健康度, 检测这个达人有没有假粉.
compatibility: Node.js 20.6+
metadata:
  layer: audit
  parent: creator-scraper-cv
---

# Fake Follower Audit（达人假粉检测）

## 调用方式

对单个达人执行同步检测：

```bash
# 方式一：达人主页链接
node ../../scripts/fake_follower_audit.mjs '{"profile_url":"https://www.tiktok.com/@creator","lang":"cn"}'

# 方式二：平台 + 达人标识
node ../../scripts/fake_follower_audit.mjs '{"platform":"instagram","platform_user_id":"creator","lang":"en"}'
```

`profile_url` 与 `platform + platform_user_id` 必须且只能选择一组。

## 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `profile_url` | string | 条件必填 | TikTok / Instagram / YouTube 达人主页链接 |
| `platform` | string | 条件必填 | `tiktok` / `instagram` / `youtube` |
| `platform_user_id` | string | 条件必填 | username / union_user_id / sec_user_id |
| `service_level` | string | 否 | `S1` / `S2` / `S3`，后端默认 `S1` |
| `lang` | string | 否 | `cn` / `en`；Navos 国内默认 `cn`，海外和 common 默认 `en` |

不要把视频 URL 当作 `profile_url`。用户只提供视频链接时，先从链接或已有数据中确认达人主页/标识；无法确认时向用户澄清。

## 结果字段

| 字段 | 说明 |
|------|------|
| `quality_score` | 互动质量分，0～100，越高越健康 |
| `fake_follower_rate` | 假粉率，小数形式；`0.12` 表示 12% |
| `risk_level` | `low` / `medium` / `high` / `critical` |
| `conclusion` | 检测结论，语言由 `lang` 控制 |
| `abnormal_types` | 异常类型列表 |
| `signals` | 粉丝、互动率、播放粉丝比和评论质量等检测信号 |
| `creator_profile` | 昵称、头像、粉丝数、关注数及受众画像 |
| `partial_result` | 是否因评论、内容或达人资料不足而降级 |
| `warnings` | 降级和数据缺失告警 |

## 强制解释规则

1. `fake_follower_rate` 是模型和规则综合估算值，不是平台官方粉丝逐账号审计结果。
2. 百分比展示必须乘以 100，例如 `0.2395` 展示为 `23.95%`。
3. `quality_score` 越高越健康，不能反向解释。
4. `risk_level=critical` 也可能表示资料不足导致无法有效检测；必须同时阅读 `conclusion`、`partial_result` 和 `warnings`。
5. `partial_result=true` 时明确标注“部分数据可用”，不要把结果描述为完整审计。
6. 不要根据粉丝量、单条互动率或网页观感自行补充接口未返回的风险结论。
7. 检测失败或无权限时，不要切换网页搜索伪造结果。

## 推荐展示

```text
达人：{creator_profile.nick_name}
平台：{platform}
粉丝：{creator_profile.followers_cnt}
假粉率估算：{fake_follower_rate * 100}%
互动质量分：{quality_score}/100
风险等级：{risk_level}
结论：{conclusion}
异常信号：{abnormal_types}
数据状态：完整 / 部分数据可用
```

`signals` 和受众画像只展示接口实际返回且有值的字段。

## 计费与权限

- 按 `/openapi/v1/fake-follower-audit/run` 后台计费规则和租户套餐扣费，不在 Skill 内写死 credits。
- 仅在后端返回 `40201` 时提示积分不足。
- 返回 `40301` 时提示当前 API Key 未开通假粉检测权限，不要自动重试。
- 相同达人可能命中后端 7 天缓存，但是否扣费仍以后端响应和计费规则为准。

## References

- [API Reference](../../references/api-reference.md)
- [Error Codes](../../references/error-codes.md)
