# 配置指南：如何拿到签到接口并写进 config.json

目标是把「人在网页上点一下签到」翻译成「发一个 HTTP 请求」。整个流程只有三步：抓包 → 抄进配置 → 测试。

## 一、抓包（Chrome / Edge）

1. 浏览器登录目标站点，进入签到页面。
2. 按 `F12` 打开开发者工具，切到 **Network（网络）** 面板，勾选 **Preserve log**。
3. 清空面板，然后在页面上**手动点一次签到**。
4. 面板里会冒出新请求。找 `Fetch/XHR` 类型、名字像 `checkin` / `sign` / `signin` / `task` / `daily` / `point` 的那条。
5. 点开它，逐个标签页抄信息：
   - **Headers → General**：`Request URL`、`Request Method`
   - **Headers → Request Headers**：整行 `Cookie`（右键 Copy value）、`Referer`、`Content-Type`、以及任何 `Authorization` / `token` / `x-csrf-token`
   - **Payload / 请求负载**：请求体内容
   - **Response / 响应**：返回的 JSON，这是写判定规则的依据
6. 更省事的方法：在该请求上右键 → **Copy → Copy as cURL (bash)**，粘到任意文本里，URL、方法、全部 header、body 都在里面。

> 要点：Cookie 是登录态，等同密码，不要贴到公开场合。Cookie 一般 3~30 天过期，过期后签到会失败，需要重新复制一次（可用 `claim.py --set-cookie` 快速更新）。

## 二、配置字段说明

```json
{
  "id": "mysite",                      // 英文短名，命令行 --site 用
  "name": "某站点",                     // 中文显示名
  "enabled": true,                     // false 则不执行
  "request": {
    "method": "POST",                  // GET / POST / PUT ...
    "url": "https://x.com/api/checkin",
    "headers": {
      "Cookie": "sid=abc; token=def",  // 必有，除非接口不需要登录
      "User-Agent": "Mozilla/5.0 ...", // 建议带，很多站点缺 UA 会拒绝
      "Referer": "https://x.com/",     // 部分站点做了防盗链，必带
      "Authorization": "Bearer xxx",   // 用 token 鉴权的站点用这个
      "Content-Type": "application/json"
    },
    "body_type": "json",               // json | form | raw | none
    "body": { "date": "{{today}}" }    // json 用对象，form 用对象，raw 用字符串
  },
  "expect": {
    "success_when": [...],             // 命中 → 领取成功
    "already_when": [...],             // 命中 → 今日已领
    "fail_when": [...],                // 命中 → 失败
    "points_path": "data.points",      // 可选，提取积分数量
    "message_path": "msg"              // 可选，提取站点返回的提示语
  }
}
```

`body_type` 对应关系：

| 值 | body 写法 | 适用 |
|---|---|---|
| `json` | `{"a":1}` | Content-Type 为 `application/json` |
| `form` | `{"a":"1"}` → 自动转 `a=1` | `application/x-www-form-urlencoded` |
| `raw` | `"a=1&b=2"` 原样发送 | 特殊格式、GraphQL、protobuf 文本 |
| `none` | 不填 | GET 请求 |

## 三、判定规则怎么写

规则是一个数组，多条为「与」关系，全部满足才算命中。先测 `already_when`，再测 `success_when`，最后 `fail_when`——顺序很重要，因为很多站点重复签到时 `code` 依然是 0，只靠 `msg` 区分。

支持的 `op`：

| op | 含义 | 示例 |
|---|---|---|
| `eq` | 等于（数字/字符串自动兼容） | `{"path":"code","op":"eq","value":0}` |
| `ne` | 不等于 | `{"path":"code","op":"ne","value":0}` |
| `contains` | 文本包含 | `{"path":"msg","op":"contains","value":"已签到"}` |
| `not_contains` | 文本不包含 | |
| `regex` | 正则命中 | `{"path":"msg","op":"regex","value":"已.*签"}` |
| `gt` / `gte` / `lt` / `lte` | 数值比较 | `{"path":"data.days","op":"gte","value":7}` |
| `exists` / `not_exists` | 字段存在与否 | `{"path":"data.reward","op":"exists"}` |

`path` 为空字符串时，匹配整个响应文本（响应不是 JSON 时用这个）。
`path` 支持数组下标：`data.list.0.status`。

典型配置举例：

```json
"expect": {
  "success_when": [{ "path": "code", "op": "eq", "value": 0 }],
  "already_when": [{ "path": "msg", "op": "contains", "value": "已签到" }],
  "fail_when":    [{ "path": "code", "op": "ne", "value": 0 }],
  "points_path": "data.points",
  "message_path": "msg"
}
```

响应是纯文本而不是 JSON 时：

```json
"expect": {
  "success_when": [{ "path": "", "op": "contains", "value": "签到成功" }],
  "already_when": [{ "path": "", "op": "contains", "value": "今天已经签到" }]
}
```

## 四、模板变量

写在 `url`、`headers`、`body` 的任意字符串里，运行时会替换：

| 变量 | 值 |
|---|---|
| `{{today}}` | 2026-10-30 |
| `{{today_compact}}` | 20261030 |
| `{{yesterday}}` / `{{yesterday_compact}}` | 昨天日期 |
| `{{iso}}` | 2026-10-30T08:00:00+08:00 |
| `{{timestamp}}` | 秒级时间戳（字符串） |
| `{{timestamp|int}}` | 秒级时间戳（整数） |
| `{{timestamp_ms}}` | 毫秒时间戳 |
| `{{uuid}}` | 32 位随机 hex |
| `{{random}}` | 6 位随机数字 |
| `{{year}}` `{{month}}` `{{day}}` | 年月日 |

时间统一按**北京时间**计算，不受系统时区影响。

## 五、测试与上线

```bash
python claim.py --check                 # 只校验配置格式
python claim.py --site mysite --dry-run # 看实际会发出什么请求，不真发
python claim.py --site mysite           # 真跑一次
python claim.py --json                  # 机器可读摘要
```

第一次跑建议加 `--dry-run` 核对 URL 和 Cookie 有没有抄错，再真跑。真跑成功后再挂定时任务。

## 六、需要签名的接口

部分站点要求 `sign` 参数（通常是 `md5(参数串 + 密钥)`）。本项目不内置签名算法，两条路：

1. 让 WorkBuddy 根据抓到的请求反推算法，在 `claim.py` 里加一个 `sign_builder` 钩子；
2. 换成固定值——如果服务端不严格校验，直接把抓到的 `sign` 写进 body 硬编码即可（有效期通常较短，不推荐长期依赖）。

遇到这种情况时，把完整的抓包请求（去掉 Cookie 敏感部分）交给 WorkBuddy 分析。
