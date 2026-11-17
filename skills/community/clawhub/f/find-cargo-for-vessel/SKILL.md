---
name: find-cargo-for-vessel
description: 为船东按当前港、计划目的港和船舶可载吨位查找并推荐内贸或外贸货盘。用于“船找货”“找货盘”“我的船在某港、准备去某港、能装多少吨”等场景；从航运在线货盘数据源获取列表和详情，按两端港口距离与吨位筛选，并在一次完整查询后记录船东需求。
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🚢"
---

# 租赁-船找货

为 ShippingClaw/OpenClaw 提供船东找货工作流。调用脚本，不要自行猜测货盘、港口坐标、距离或联系方式。

## 必需输入

收集以下三项后立即查询：

- 当前港口：港口名称或 UN/LOCODE。
- 计划目的港：港口名称或 UN/LOCODE。
- 船舶可载吨位：正数，单位为吨。

不要追问船期、航速、船型、舱容、货种、吃水或最低装载率。

## 查询工作流

1. 调用：

```bash
python scripts/find_cargo.py search \
  --current-port "<当前港>" \
  --destination-port "<目的港>" \
  --capacity-tons <吨位> \
  --user-id "<当前登录船东用户ID>"
```

2. 将脚本返回的 `trade_type` 解释为：
   - `domestic`：内贸；当前港和目的港均为中国大陆港口。
   - `international`：外贸；任一端为境外或港澳台港口。
3. 默认展示前 10 条。逐条展示编号、公司、货名、货量、装港、卸港、装货时间、更新日期、当前港至装港距离、卸港至目的港距离。
   - 必须把货盘编号渲染为可点击的 Markdown 链接：`[编号](detail_url)`。
   - 若调用方支持结构化交互，优先将整条记录或“查看详情”按钮绑定到 `detail_action`；该动作只打开站内详情。
4. 仅展示脚本返回的结果。不要把因端点无法解析、距离超限或明确货量超过船舶吨位而排除的货盘说成“匹配”。
5. `quantity_status=manual_confirmation` 表示货量无法可靠换算成吨，保留在结果末尾并明确提示“货量需人工确认”。
6. 查询成功并返回结果后即视为一次完整咨询。脚本会自动提交需求；若后台接口尚未配置，会安全写入本地待同步队列。

## 详情工作流

用户选择或点击某条货盘时，使用搜索结果中的 `solid`：

```bash
python scripts/find_cargo.py detail --solid "<solid>"
```

返回脚本提供的业务详情和公开可见联系方式，不返回原始网页链接。字段为空、被遮罩或明确要求付费后才能查看时，返回空值；不得尝试登录、支付、绕过限制或推断联系方式。

搜索结果同时返回：

- `detail_url`：可直接点击的站内 HTML 详情页。
- `detail_action`：供 ShippingClaw 前端绑定整行或按钮点击的结构化动作。
- `detail_action.api_path`：需要 JSON 数据时使用的站内接口。

部署时设置 `CARGO_MATCHER_PUBLIC_URL` 为用户浏览器能访问到的服务地址，例如 `https://shipping.example.com/cargo-service`；本机开发默认使用 `http://127.0.0.1:8765`。

## 匹配规则

- 内贸：当前港至装港、卸港至目的港均不得超过 150 海里。
- 外贸：两个端点均不得超过 300 海里。
- 距离按港口经纬度的大圆直线距离计算，不代表实际航线里程。
- 货量能解析为吨时，最小可承运量大于船舶可载吨位则排除。
- 区间货量只要区间内存在不超过船舶可载吨位的数量即可保留。
- 不设最低装载率。
- 不能换算为吨的货量保留并排在可解析货量之后。
- 结果按“货量可确认优先、两端距离合计升序”排序。

## 运行服务

安装 `requirements.txt` 后启动：

```bash
uvicorn scripts.service:app --host 0.0.0.0 --port 8765
```

接口为 `GET /health`、`POST /search`、`GET /cargo/{solid}`（JSON）、`GET /cargo/{solid}/view`（站内可点击详情页）。后台需求接口接入说明见 [references/backend-api.md](references/backend-api.md)。
