# game-valuation

> YY 游戏账号估值 Skill for Claude Code（源码版）

在 Claude Code 对话中直接查询游戏账号估值价格，支持王者荣耀、和平精英、三角洲行动三款游戏。

默认调用估值测试服务：`http://ruliurobot.baizhanlive.com/game_valuation`。

---

## 功能

- 查询游戏账号预估价格、价格区间、超越用户比例、最值钱单品
- 支持王者荣耀（营地 ID 直接查询）
- 支持和平精英、三角洲行动（二维码扫码后查询）
- 自动处理扫码验证流程：二维码生成、打开、轮询、查询估值

## 支持游戏

| 游戏 | 是否扫码 | 必填属性 |
|------|---------|---------|
| 王者荣耀 | 否 | 区服、营地 ID、实名情况、防沉迷 |
| 和平精英 | 是 | 区服、实名情况、防沉迷 |
| 三角洲行动 | 是 | 登录方式、实名情况、安全箱 |

## 依赖

- **bash** — 脚本运行环境
- **python3** — JSON 解析、二维码 base64 解码、报告格式化
- **curl** — HTTP 请求

---

## 安装

```bash
npx skills add https://github.com/Arc-lin/game-valuation-skill --skill game-valuation
```

---

## 使用方式

| 方式 | 示例 |
|------|------|
| 手动调用 | `/game-valuation` |
| 关键词触发 | 说「王者荣耀账号估值」「我的号值多少钱」「和平精英估价」等 |

---

## 脚本命令

```bash
scripts/valuation.sh hok <server> <yingdi_id> <real_name_status> <anti_addiction>
scripts/valuation.sh delta <account_type> <real_name_status> <safety_box>
scripts/valuation.sh pubg <server> <real_name_status> <anti_addiction> [role_id]
```

调试命令：

```bash
scripts/valuation.sh qrcode <game> <account_type>
scripts/valuation.sh poll <login_uuid>
scripts/valuation.sh query '<json_body>'
```

### 参数枚举

- `server`: `android_qq` / `ios_qq` / `android_wx` / `ios_wx`
- `account_type`: `1` QQ / `2` 微信
- `real_name_status`: `re_auth_allowed` 可二次实名 / `re_auth_denied` 不可二次实名
- `anti_addiction`: `yes` 有防沉迷 / `no` 无防沉迷
- `safety_box`: `top` / `advanced` / `intermediate` / `basic`

---

## 示例对话

```text
用户：帮我估一下王者荣耀的号
→ 询问区服、营地 ID、实名情况、防沉迷信息
→ 调用 /api/query，直接返回估值报告

用户：和平精英账号多少钱
→ 询问区服、实名情况、防沉迷信息
→ 调用 /api/qrcode 获取二维码
→ 用户扫码后轮询 /api/poll
→ 调用 /api/query 返回估值报告
```

---

## 服务接口

默认服务前缀可通过环境变量覆盖：

```bash
GAME_VALUATION_BASE_URL="http://ruliurobot.baizhanlive.com/game_valuation"
```

调用接口：

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/qrcode` | POST | 获取扫码二维码 |
| `/api/poll` | GET | 轮询扫码结果 |
| `/api/query` | POST | 查询资产并请求估值 |

---

## 链接

- **YY 游仓**：https://mall.yy.com/?pageId=20000
