---
name: baidu-pan-per-auth-skill
description: 百度网盘OAuth2.0授权码模式，获取/刷新access_token。触发词：百度网盘授权、baidu pan auth、access_token过期、refresh_token刷新、百度网盘token。适用场景：(1)首次授权获取token (2)token过期后刷新 (3)定时刷新token保活。
---

# 百度网盘个人应用授权

## 前提

已有百度网盘开放平台应用（https://pan.baidu.com/union/doc/al0rwqzzl），.env文件含AppKey和SecretKey。

参考 `assets/example.env` 创建.env文件，填入实际凭据。

## 授权流程

### 首次授权（3步）

**Step 1** — 浏览器打开授权页：

```
https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={AppKey}&redirect_uri=oob&scope=basic,netdisk&device_id={AppID}
```

用户登录→点授权→页面显示授权码code（10分钟有效，仅一次）

**Step 2** — 换取Token：

```bash
python3 scripts/auth.py code <code> </path/to/.env>
```

成功后.env自动更新AccessToken/RefreshToken/ExpiresIn/Scope/AuthDate

**Step 3** — 验证：

```bash
curl -s 'https://pan.baidu.com/rest/2.0/xpan/nas?method=uinfo&access_token={AccessToken}' -H 'User-Agent: pan.baidu.com'
```

返回errno=0即有效。

### 刷新Token（过期后）

access_token有效期30天。过期后用refresh_token刷新：

```bash
python3 scripts/auth.py refresh </path/to/.env>
```

刷新后.env自动更新所有token字段（含新refresh_token）。旧refresh_token立即失效。

### 定时刷新（推荐）

建议每25天自动刷新，避免token过期。通过cron定时任务实现：

```
cron add → schedule: {"kind":"every","everyMs":2160000000}（25天）
         → payload.message: "执行百度网盘token刷新：运行 python3 <skill_path>/scripts/auth.py refresh </path/to/.env>，报告结果"
         → sessionTarget: isolated
```

或用CLI：
```bash
openclaw cron add --name "百度网盘token刷新" --every 25d --session isolated \
  --message "执行百度网盘token刷新：运行 python3 <skill_path>/scripts/auth.py refresh </path/to/.env>，报告结果"
```

## 关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| redirect_uri | `oob` | 必须与开放平台配置一致 |
| code有效期 | 10分钟 | 仅一次 |
| access_token有效期 | 30天 | 刷新后旧token失效 |
| refresh_token有效期 | 10年 | 仅一次使用，刷新后返回新refresh_token |
| scope | `basic,netdisk` | 固定值 |

## 故障排查

- `error: invalid_grant` → code过期或已使用，重新授权
- `error: invalid_refresh_token` → refresh_token已用或过期，需重新授权(Step 1)
- 网络超时 → 国内直连即可，无需代理
