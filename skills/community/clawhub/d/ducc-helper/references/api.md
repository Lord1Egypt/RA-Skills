# DUCC 接口参考（抓包实测，2026-07-29）

本文件是 ducc-helper 的底层接口依据，全部经 opencli 浏览器探针（注入 fetch/XHR hook，页面真实操作触发）抓取并端到端验证。调试或扩展新能力时查阅。

## 一、认证与请求地基（最关键）

- **真实域名**：`http://pserve.jd.com/api/duccApi`（http，非 https）。
  - ⚠ 页面地址是 `taishan.jd.com/ducc/web/nswork`，但真正的后端 API 在 `pserve.jd.com`。直接打 taishan 会 404。
- **认证 Cookie**：仅需一个 `sso.jd.com`（`.jd.com` 域，跨子域自动带到 pserve）。从京ME客户端零配置换出（复用 jdos-helper 的 jme_auth，链路见 joyclaw-hioffice-auth）。
- **两个必带自定义 header**（决定打到生产还是预发的后端）：
  - `config-env`: `online`(生产) / `pre`(预发)
  - `x-proxy-opts`: 网关代理路由 JSON，`{"target":"<后端>","pathRewrite":{"^/api/duccApi":"/"}}`
    - 生产 target = `http://console.ducc.jd.com`
    - 预发 target = `http://pre.console.ducc.jd.local`
  - **两个头必须配套切换**。这就是 UI 里生产/预发 tab 的实现机制。
- 业务成功判定：响应体 `{"code":200,"status":200,...}`。

### 命令行独立验证（脱离浏览器）

```bash
SSO="<sso.jd.com值>"
PROXY='{"target":"http://console.ducc.jd.com","pathRewrite":{"^/api/duccApi":"/"}}'
curl -s "http://pserve.jd.com/api/duccApi/v1/namespaces/search?page=1&size=5" \
  -H "Cookie: sso.jd.com=$SSO" -H "config-env: online" -H "x-proxy-opts: $PROXY" -H "Accept: application/json"
```

## 二、层级与 code→ID 解析

```
命名空间 namespace (nsId, code, name)      pop_customs_center / 跨境-赤道-center / 6577
  └─ 配置文件 config (cId, code, name)      center_config / 23780
       └─ profile (profileId, code, name)   dev「真预发」/1205477、common/43101
            └─ 配置项 item (id, key, value)  ducc.xxx = value
```

- 用户传 code，脚本自动 search 反查 ID。命名空间/配置文件列表是**环境无关**（一律 online 解析）。

## 三、读接口

| 用途 | 方法 & 路径 | 关键返回字段 |
| --- | --- | --- |
| 当前用户 | `GET /v1/login/user` | `data.code` = erp（发布 submitter 用） |
| 命名空间列表 | `GET /v1/namespaces/search?page=1&size=100` | `data[].{id,code,name,owner.code}`，`pagination.totalRecord` |
| 命名空间详情 | `GET /v1/namespace/{nsId}` | 单个命名空间 |
| 配置文件列表 | `GET /v1/namespace/{nsId}/configs/search?page=1&size=100&dataTypes=0,2&filterNoProfile=true` | `data[].{id,code,name,dataTypeEnum}` |
| 配置文件详情 | `GET /v1/namespace/{nsId}/config/{cId}` | 元信息（不含配置项） |
| profile 列表 | `GET /admin/v2/namespace/{nsId}/profiles/search?page=1&size=100&configType=0` | `data[].{id,code,name,version.name}`；带 config-env 区分生产/预发 |
| profile 详情 | `GET /v1/namespace/{nsId}/config/{cId}/profile/{profileId}?publicInfo=true` | 单 profile |
| **配置项列表** | `GET /admin/v2/namespace/{nsId}/config/{cId}/profile/{profileId}/items/search?size=10&page=1&fromRelease=false&orderField=updateTime&desc=desc` | `data[].{id,key,value,description,dataType,dataVersion,isReleased,updateBy}` |
| 编排模板列表 | `GET /v2/namespace/{nsId}/task_orchestrates?size=100&orderField=updateTime&desc=desc` | `data[].{code,name,batchCount,template.batches[].{batchNum,ipsPercentage}}` |

- **预发未开放**：`--env pre` 下 profiles/search 返回 `data:[]`（totalRecord 0）；items 报 `503 环境不存在！`。
- `isReleased` 字段：0 表示无待发布改动（已发布干净）。

## 四、写接口（增 / 改 / 删）

均基于 profile，路径前缀 `PB=/v1/namespace/{nsId}/config/{cId}/profile/{profileId}`。**只改草稿，不影响线上运行，需 release 才生效。**

| 用途 | 方法 & 路径 | body |
| --- | --- | --- |
| 新增 | `POST {PB}/item` | `{"key":"...","format":0,"value":"1","description":""}` → 返回 `data.id`(itemId) |
| 修改 | `PUT {PB}/item/{itemId}` | `{"format":0,"value":"2","description":""}`（不含 key） |
| 删除 | `DELETE {PB}/item/{itemId}` | 无 body |

- `format`：`0`=无格式，`1`=JSON（value 是 JSON 字符串，如 `{"format":1,"value":"{\n  \"a\":1\n}"}`）。
- 改前先按 key 在 items/search 里查出 itemId。

## 五、发布链路（★ 最复杂，逐条实测）

路径前缀：`AB=/admin/v1/namespace/{nsId}/config/{cId}/profile/{profileId}`，`PB=/v1/namespace/{nsId}/config/{cId}/profile/{profileId}`。

### 5.1 全量发布（两步，无编排）

```
1. POST {AB}/keys?hasInnerKey=true&workflowId=-1              body=["key1","key2"]   预检
   POST {AB}/item_releases/keys?hasInnerKey=true&workflowId=-1 body=["key1"]          预检
2. POST {AB}/submitAuditKeys
      body={"pushType":0,"keys":["key1"],"submitter":"<erp>","description":"","name":"v20260729xxxxxx","appendPreBatch":true}
      → 返回 {"data":{"taskId":<id>,"taskCode":"..."}}
      ⚠ 全量：body 不带 orchestrateCode、不带 batchInterval
3. PUT {PB}/release/keys
      body={"pushType":0,"submitter":"<erp>","description":"","configTaskId":<taskId>,"versionName":"v20260729xxxxxx"}
      → 返回 {"data":{"version":<新版本号>}}，任务直接走到 status:-2(结束)，orchestrateType:-1
      ⚠ 全量：body 不带 orchestrateCode
```

- 全量发布**没有** releaseAction(PRE_BATCH_SKIP) 步骤，submitAuditKeys→release/keys 两步即可，一次到位。
- `name`/`versionName` = `v` + `yyyyMMddHHmmss`。`submitter` = 当前用户 erp（`/v1/login/user` 的 data.code）。

### 5.2 灰度分批发布（多步，带编排模板）

```
1. 预检（同上两个 POST keys）
2. POST {AB}/submitAuditKeys
      body={...,"orchestrateCode":"<模板code>","batchInterval":0,"name":"v...","appendPreBatch":true}
      ⚠ 灰度：带 orchestrateCode(如 "1731329960745.69139")；建出的任务 batchCount=模板批数+预批次, orchestrateType=1
3. PUT {AB}/task/{taskId}/batch/0/releaseAction   body={"action":"PRE_BATCH_SKIP"}   跳过预批次(batch0)
      → 之后 task.releaseStatus=25(就绪), batchNum=1(待发首批)
4. 逐批循环推进：
   for 每批:
     PUT {PB}/release/keys   body={...,"orchestrateCode":1,"configTaskId":<taskId>,"versionName":"v..."}
        （发布当前 task.batchNum 指向的那一批；发完 batchNum 自动 +1）
     轮询 GET {PB}/task/{taskId}/batch/{n}/ips   n=刚发的批号
        → data.result[].{ip,status}，等全部 status=="COMPLETED" 再发下一批
   直到 GET {PB}/task/{taskId} 的 data.status == -2（结束）
```

- **批号语义（易错）**：`task.batchNum` 指向"下一个待发批"。`release/keys` 发布当前 batchNum 那一批，发完 batchNum++。所以查 IP 要查**发之前记下的批号 n**，不是发之后的新 batchNum。
- **每批等 IP 全 COMPLETED 再发下一批**——这是用户强调的核心安全逻辑。IP status 有 `COMPLETED`（成功），失败可能是 `FAILED/ERROR`。
- 编排模板示例：`10%->30%->60%->100%`（4批，code `1731329960745.69139`）；也有按机房分批的模板。
- 每次 `release/keys` 返回 `{"data":{"version":<号>}}`。

### 5.3 任务状态字段（`GET {PB}/task/{taskId}`）

- `status`: `1`=进行中，`-2`=已结束。
- `releaseStatus`: `10`=初始/未推进，`25`=就绪(可 release)，`5`=结束批次。
- `batchNum`/`batchCount`: 当前待发批号 / 总批数。
- `orchestrateType`: `-1`=全量，`1`=灰度编排。

### 5.4 并行任务上限（重要约束）

- **同一 profile 同时只能有 1 个进行中(status:1)的发布任务**。已有进行中任务时，新任务的 releaseAction 报 `1606 进行中的发布任务数量不能超出上限（并行任务上限:1个）`。
- 处理：把卡住的任务发完（继续 release/keys 推到 status:-2）或去页面取消（取消接口未抓，页面操作）。

## 六、发现方法论（扩展新能力照这个来）

1. opencli 打开 `taishan.jd.com/ducc/web/nswork`（登录态自带），注入 fetch/XHR 探针 hook（记 url/method/headers/body/resp，只留含 `duccApi` 的）。
2. **由用户在页面真实操作**（选命名空间/配置文件/profile、增删改、发布），不要自己 fetch 复现（会漏 header、偏离真实路径）。
3. 操作后读 `window.__apiLog`，用 `config-env`/`x-proxy-opts` 区分环境，裁剪最小字段集。
4. ⚠ 页面刷新/跳 about:blank 会清掉探针，需重新打开+重埋。发布类写操作建议用自造测试 key（如 `ducc.test.xxx`）走全流程，用完删除，避免污染真实配置。

## 七、待补充 / 未抓接口

- 取消/终止发布任务（页面有"取消"按钮，接口未抓）。
- 回滚到历史版本。
- 配置项的历史版本 diff、变更审计。
- 新建命名空间/配置文件/profile（本 skill 只覆盖已有结构下的读写发布）。
- 审批流（部分配置文件 approveInfo 开了审批，本次 pop_customs_center/center_config 未开）。
