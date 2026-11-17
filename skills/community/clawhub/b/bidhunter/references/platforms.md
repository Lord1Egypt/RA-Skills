# 支持平台清单与配置

## 内置平台适配器

以下平台已在 `bid_monitor.sh` 中实现采集适配器：

| 平台编码 | 平台名称 | 网址 | 采集方式 | 认证要求 | 状态 |
|---|---|---|---|---|---|
| `cnooc` | 中海油采办业务管理与交易系统 | bid.cnooc.com.cn | API (JSON) | ~~免登录~~ **现需鉴权** | 🔴 **2026-09-02 实测失效** |
| `cebpubservice` | 中国招标投标公共服务平台 | ctbpsp.com | API (JSON POST) | 免登录 | 🔴 **2026-09-02 实测失效**（404） |
| `ccgp` | 中国政府采购网 | ccgp.gov.cn | HTML 解析 | 免登录 | ✅ 可用 |

### ⚠️ 数据源实测状态（2026-09-02 更新）

三个内置源实测结果，**两个已失效**，依赖它们的每日简报会漏标：

| 源 | 实测现象 | 根因 |
|---|---|---|
| `cnooc` | curl 请求稳定返回 **401 Authorization Required**（nginx 层）；真实浏览器访问返回 **502 Bad Gateway**。`/`、`/home/`、`/api/v1/bid/list` 全路径均不可达 | 网关/WAF 拦截（DNS 已 CNAME 至 `bid.cnooc.com.cn.wsdvs.com`），源站对当前网络无响应 |
| `cebpubservice` | POST `/cutomNoticeApi/getNoticeList` → **404** | 上游接口路径已变更 |
| `ccgp` | HTTP 200，可访问 | ✅ 正常。但注意：**中海油/央企属企业招标，不走政采**，搜"海油"关键词返回 0 条，无法作为海油标的替代源 |

**处置建议：**
1. `cnooc` 适配器暂时停用，避免静默返回 0 条造成"今天没标"的误判
2. 中海油标的替代路径：① 用已登录浏览器会话 + 浏览器自动化抓取（需先确认本地网络能否访问）② 第三方招标聚合平台 ③ 海油各子公司自有发布渠道
3. 恢复抓取前，先用 `curl -o /dev/null -w "%{http_code}" https://bid.cnooc.com.cn/` 探活，返回 200 再启用

## 计划适配平台

以下平台已识别但尚未实现适配器，可按"自定义数据源"流程接入：

| 平台类别 | 平台名称 | 网址 | 技术难点 | 优先级 |
|---|---|---|---|---|
| 央企招采 | 中石油电子招标投标平台 | bid.cnpcbidding.com | 需注册账号 | P0 |
| 央企招采 | 中石化物资采购电子商务平台 | sourcing.sinopec.com | 需企业认证 | P0 |
| 央企招采 | 国家电网电子商务平台 | ecp.sgcc.com.cn | 需电子钥匙 | P1 |
| 央企招采 | 中国南方电网阳光电子商务平台 | bidding.csg.cn | 需注册 | P1 |
| 能源电力 | 中国华能集团电子商务平台 | ec.chng.com.cn | 需注册 | P1 |
| 能源电力 | 中国大唐集团电子采购平台 | cdt-ec.com | 需注册 | P1 |
| 能源电力 | 国家电投电子商务平台 | eptp.com.cn | 需注册 | P1 |
| 能源建设 | 中国能建电子采购平台 | ec.ceec.net.cn | 需注册 | P1 |
| 能源建设 | 中国电建招标与采购网 | powerchina.cn | 需注册 | P1 |
| 公共资源 | 全国公共资源交易平台 | ggzyjyw.com | 数据聚合，需解析 | P0 |
| 公共资源 | 各省市公共资源交易中心 | 分省平台 | 模板差异极大 | P1 |
| 行业垂直 | 军队采购网 | plap.mil.cn | 需军队供应商库资质 | P2 |
| 行业垂直 | 铁路建设工程网 | railway.cn | 需注册 | P2 |
| 行业垂直 | 民航专业工程招标投标管理系统 | caac.gov.cn | 访问受限 | P2 |

## 平台适配器开发规范

每个适配器需实现一个 `fetch_<platform>()` bash 函数：

1. **输入**：`$1` = 目标日期 (YYYY-MM-DD)
2. **输出**：JSON lines 到 stdout，每行一条公告
3. **格式**：
   ```json
   {
     "id": "公告唯一标识",
     "title": "项目名称",
     "source": "平台编码",
     "url": "详情页链接",
     "publish_time": "发布时间"
   }
   ```
4. **注意事项**：
   - 翻页时 sleep 2s 防限流
   - 401/403 时冷却 10s 重试一次
   - 过滤结果公示类（中标/成交公告）
   - 只采集当天发布（近似排除已开标标）

## 自定义数据源（v1.5 新增 · 零代码扩平台）

不想写 bash 适配器？用 `sources.json` 配置即可接入任意平台。`bid_monitor.sh` 运行时若发现 `sources.json` 会自动加载。

**步骤**：
1. 复制 `scripts/sources.example.json` → `scripts/sources.json`
2. 按你的平台改 `name` / `url` / `mode` / `fields`
3. 支持三种模式：
   - `json`：接口返回 JSON，`items_path` 指向数组路径，`fields` 映射字段
   - `rss`：标准 RSS/Atom（`item`/`link`/`title`/`pubDate`）
   - `html`：列表页，自动抓取含「招标/采购/投标」等关键词的 `<a>` 链接
4. 测试：`bash bid_monitor.sh --fresh`（会自动包含 custom 源）

> 示例（某gov平台 JSON 接口）：
> ```json
> {"name":"my_gov","mode":"json","url":"https://x/api/notice?date={DATE}",
>  "items_path":"data.list","fields":{"id":"id","title":"title","url":"url"},
>  "url_prefix":"https://x/detail?id="}
> ```

## 计划适配平台（可经自定义数据源或适配器接入）

| 平台类别 | 平台名称 | 网址 | 接入方式 | 优先级 |
|---|---|---|---|---|
| 央企招采 | 中石油电子招标投标平台 | bid.cnpcbidding.com | 账号/自定义json | P0 |
| 央企招采 | 中石化物资采购电子商务平台 | sourcing.sinopec.com | 企业认证/自定义 | P0 |
| 央企招采 | 国家电网电子商务平台 | ecp.sgcc.com.cn | 电子钥匙/自定义 | P1 |
| 央企招采 | 中国南方电网阳光电子商务平台 | bidding.csg.cn | 注册/自定义 | P1 |
| 能源电力 | 中国华能/大唐/国家电投电子商务平台 | 见各官网 | 注册/自定义 | P1 |
| 能源建设 | 中国能建/中国电建招标采购网 | ec.ceec.net.cn / powerchina.cn | 注册/自定义 | P1 |
| 公共资源 | 全国公共资源交易平台 | ggzyjyw.com | 数据聚合/自定义html | P0 |
| 公共资源 | 各省市公共资源交易中心 | 分省平台 | 模板差异大/自定义 | P1 |
| 行业垂直 | 军队采购网 | plap.mil.cn | 军队供应商库 | P2 |
| 行业垂直 | 铁路建设工程网 / 民航专业工程系统 | railway.cn / caac.gov.cn | 注册/受限 | P2 |

> v1.5 起"平台覆盖"短板通过「自定义数据源」机制补强：内置 3 个适配器 + 用户可零代码接入任意公开接口。需要官方内置某平台可在 ClawHub/SkillHub 反馈，我们按 P0 优先级实现。

## 适配器开发规范（进阶）

每个 bash 适配器需实现 `fetch_<platform>()` 函数（详见上文"平台适配器开发规范"）。自定义数据源已覆盖绝大多数场景，仅在接口鉴权复杂时才需写适配器。

## detail_url_template

各平台详情页链接格式：

| 平台 | 模板 |
|---|---|
| cnooc | `https://bid.cnooc.com.cn/home/#/newsAlertDetails?index=0&childrenActive=1&id={ID}&type=null` |
| cebpubservice | `https://ctbpsp.com/#/noticeDetail?id={ID}` |
| ccgp | 从列表页 HTML 中直接提取 |

## 数据源配置项

每个平台适配器支持的配置：

- **启用/停用**：在 `PLATFORMS` 数组中增删
- **监控范围**：在 `fetch_<platform>()` 函数中调整 API 参数
- **采集深度**：标题+摘要（默认）/ 全文+附件列表（需 detail 接口）
- **更新频率**：通过定时任务配置（默认每日）
- **认证配置**：免登录（默认）/ 账号 / CA证书（需自行实现）
