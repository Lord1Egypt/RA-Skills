---
name: vtag-geo-analytics
description: "AI 引擎里的品牌可见度——GA4 看不到的那一段。查你的网站在豆包、DeepSeek、千问、元宝、文心、Kimi 等 AI 引擎里被提到多少、哪些页面被引用,以及 AI 来源的访客、会话与转化;识别得出的分引擎看,识别不出的如实标「来源未知」,不硬凑。数据来自站点自有埋点与引擎应答采样,公开网页上查不到。可回答「我的品牌在 AI 回答里露出多少」「AI 来源带来多少会话和转化」「哪些页面被 AI 引用」。首次使用会引导你在浏览器里完成一次授权。"
version: 1.0.3
tags: [AI可见度, GEO, 网站分析, 流量归因]
license: 见仓库 LICENSE
---

# Vtag GEO Analytics

## 这是什么

GEO Tag(标签文件 `vtag.js`)是一段贴进网站 `<head>` 的**第一方**分析标签 —— 类比
gtag.js,GA4 式事件模型,自动采集 `page_view` / `session_start` / `click` / `scroll`
等访客行为,SPA 路由自动补发。数据落在站点自己名下,不经过 Google。

它比 GA4 多出来的是**引擎侧**:GEO Tag 定期拿站点自己设定的问题(每站最多 10 条,
客户自己维护,我们不代拟)去问 DeepSeek、通义千问、文心一言、豆包、腾讯元宝五个引擎,
记录回答里提没提到这个品牌、引没引用它的页面,并把**回答原文与全部引用链接留证**。
GA4 的漏斗从「访客到站」才开始,这一段它是盲区。

这个 skill 是上面两套数据的**只读取数口**:14 个端点,数字全部来自服务端固定 SQL,
与控制台报表同源 —— 同一个问题在这里查和在控制台看,应该是同一个数。

## 它能回答什么

- **站点侧**(实测流量):访客 / 会话 / 浏览量 / 事件、按天趋势、来源拆分(可切分引擎)、
  页面排行、参与度与停留时长、转化、近 30 分钟实时;
- **引擎侧**(应答采样):每个引擎采样了多少次、答案提到品牌的比例、引用了自有页面的
  比例,以及每条回答的原文与引用链接;
- **数据质量**:爬虫视角与无效流量(打标不拦截),可下钻到单个会话的事件序列。

## 它不能回答什么 —— 先说清楚,省得白问

- **不做「被引 N 次 → 带来 M 访客」这类换算。** 引擎侧与站点侧并排呈现,各讲各的事实。
  中间那一跳是公开网页,信息在那里就丢了 —— 一次被引对应多少真人看到,我们不知道,
  就不装知道(这是下面口径红线的第 1 条,不是可以商量的口径偏好);
- **「测不到」不是 0。** DeepSeek 这类抹掉来源的引擎,站点侧那栏是「技术上测不到」;
- **一个 token 只绑一个站点**,没有「列出我所有站点」这个能力;
- **只读**,这里没有任何写操作。要改数据去控制台。

数据来自站点自有埋点与引擎应答采样,**公开网页上查不到,只能从这个接口取**。

## 怎么用这份文档

- 端点契约(参数、响应字段):`references/endpoints.md`
- 指标公式与口径红线全文:`references/metrics.md`
- 可选的命令行封装:`scripts/vtag.sh`(需要 shell;没有 shell 就按下面的 HTTP 步骤自己发请求)

## 授权(首次使用)

走 OAuth 设备授权许可(RFC 8628)。基址 `https://geo-analytics.info`,`client_id` 是
`vtag-skill`(公开值,没有 secret)。三步:

1. `POST /api/oauth/device_authorization`  body: `client_id=vtag-skill`
   (`application/x-www-form-urlencoded` 或 JSON 都收)
   → `{device_code, user_code, verification_uri, verification_uri_complete, expires_in, interval}`
2. **把 `user_code` 和 `verification_uri` 显示给用户**,原话告诉他:
   「打开这个网址,输入 XXXX-XXXX,选择要查的站点并批准」。`verification_uri_complete`
   是带码的直达链接,能点就让他点(手输那一步是整个流程唯一会出错的地方)。然后等他说好了。
3. 按 `interval` 秒轮询 `POST /api/oauth/token`
   body: `grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=…&client_id=vtag-skill`
   - `400 {"error":"authorization_pending"}` → 继续等
   - `400 {"error":"slow_down"}` → 把间隔加 5 秒再试
   - `400 {"error":"expired_token"}` → 码过期了(15 分钟),从第 1 步重来
   - `400 {"error":"access_denied"}` → 用户拒绝了,**停止,不要重试**
   - `400 {"error":"invalid_grant"}` → 这个 `device_code` 无效或已经换过 token 了
     (一次性领取),**停止**,要重来就从第 1 步拿新的
   - `200 {"access_token":"vtag_ro_…","token_type":"Bearer","scope":"reports:read","tag_id":"VG-…"}`

拿到之后:**能把 `access_token` 写进本地文件就写**(它长期有效,不会过期),下次直接用;
**写不了就只在本次会话里用**,下个会话重走一次授权——十几秒的事,这是正常的,
不是配置错误,**别让用户以为自己弄错了**。

调用:`Authorization: Bearer <access_token>`,基址 `https://geo-analytics.info/api/reports`。
或用 `scripts/vtag.sh login` / `scripts/vtag.sh <endpoint> [k=v ...]`。

**还没授权时**:可以解释下面的指标定义,**不要给任何具体数字**——
没有数据时编一个数,比不回答坏得多。

## 端点表

日期参数一律 `from` / `to`(YYYY-MM-DD,北京日口径)。`tag_id` 全部必填,
取授权时返回的那个 `tag_id`(token 已绑定它,填别的会 403)。
完整参数与响应字段见 `references/endpoints.md`。

<!-- BEGIN endpoints-table:由 tools/gen_endpoints.py 生成,不要手改 -->
| 端点 | 用途 | 参数(除 `tag_id`/`from`/`to`) |
|---|---|---|
| `/overview` | 概览卡片(访客/会话/浏览量/事件/互动会话占比) | — |
| `/timeseries` | 按天趋势(访客/会话/浏览量) | — |
| `/acquisition` | 来源拆分,维度可切 | `dimension` |
| `/pages` | 页面排行 | `limit`, `dimension` |
| `/pages_timeseries` | TopN 页面按天 | `top` |
| `/events` | 事件名汇总 | — |
| `/bots` | 爬虫视角(常规报表已排除爬虫) | — |
| `/engagement` | 参与度(互动会话、时长;时长看中位数) | — |
| `/conversions` | 转化(金额按币种分组,跨币种不相加) | — |
| `/realtime` | 近 30 分钟滚动窗 ⚠️**无日期参数** | — |
| `/engines` | 引擎侧(应答采样)× 站点侧(实测流量)并排 | — |
| `/probe-events` | 应答采样原始记录(含 answer_text 与 sources) | `limit` |
| `/ivt` | 无效流量报表(打标不拦截) | — |
| `/ivt/session-events` | 单会话事件序列(抽查下钻) ⚠️**无日期参数** | `session_id` |
<!-- END endpoints-table -->

没有「列出我所有站点」这个能力:一个 token 只绑一个站点,要查另一个站就重新授权一次
(第 2 步里用户可以选别的站)。

## 指标定义(不要自己换算)

    整体露出率   count(brand_hit) / count(is_valid),排除 brand/compare 词类
    TOP1露出率   count(brand_rank=1) / count(brand_hit)
    TOP3露出率   count(brand_rank<=3) / count(brand_hit)
    文章引用率   count(cites_owned) / count(is_valid)
    内容中正率   (1 - count(is_negative and brand_hit) / count(brand_hit)) * 100
    品牌声量度   count(brand_hit) / (count(brand_hit) + sum(competitor_count))

后两个依赖语义判定,**没判定就是 NULL,不是 0**。

这些公式写在这里是**供解释用**的:用户问「TOP3 露出率是什么」时照着答。
**不要拿 `/probe-events` 的原始记录自己算指标**——要数就调 `/engines`,口径在服务端。

## 口径红线(违反其一,这个 skill 的输出就不能用)

1. **引擎侧与站点侧不做因果换算。** `/engines` 返回的两列各讲各的事实。禁止任何
   「被引 N 次 → 带来了 M 访客」式的换算、连线、推断。一次被引对应多少真人看到,
   我们不知道,就不装知道;
2. **「测不到」不是 0。** DeepSeek 这类抹掉来源的引擎,站点侧栏是「技术上测不到」
   (`site_measurable="no"`)。0 是测过没有,测不到是没有测量手段——把后者写成 0
   等于向用户撒谎。同理 `probes=0` 时各率返回 `null`,那不是 0%;
3. **引擎侧指标只用上面的名字**(文章引用率 / 露出率),不叫「曝光」「引流」「效果」;
4. **「来源未知」桶保持原样**,不因为引擎侧有 DeepSeek 数据就把未知流量归给它;
5. **不合成评分。** 不要把这些指标加权成一个「GEO 健康分」「AI 可见度总分」——
   合成分掩盖口径,用户没法追到哪个数出了问题;
6. **只读。** 这个 skill 里没有任何写操作。用户要求改数据时,告诉他去控制台。

## 拿不到数据时

401 = token 失效或已被用户吊销 → **重走一次授权**(上面三步),不要反复重试;
403 = tag_id 与 token 绑的站不是同一个;
422 = 参数不合法(日期格式、维度取值、范围);
429 = 触发限速,响应头 `Retry-After` 告诉你等多久。**上限不是一个准数**:
服务端按每进程每分钟 60 次计,而生产是多进程的(2026-08-24 实测约 120 次/分钟)。
别照着上限打 —— 它随部署形态变,而你撞上的那一下是取不到数。

**任何一种失败都直接说失败,不要用先验知识补一个数字上去。**
