# rcs-server API 参考（cha2a-phone skill 用）

Base：`https://compliancehub.cn/rcs`（RCS 消息/群/附件；服务端只有一套，运行在 compliancehub.cn）。registry：`https://compliancehub.cn/api/v1/`（身份/信任/号码/开户）。全部 JSON。

身份规则：
- `from`/`creator`/`did` 合法值 = CHA2A DID（`did:cha2a:<type>:<id>`）或号码（`+?[0-9]{4,15}`，须在号码簿）。
- DID 须在 registry 已注册；号码须在号码簿。
- 附件上传/群管理（member/leave/disband/announcement）要求 DID 已注册。
- admin 端点需 `X-Admin-Key` header（服务端未配 ADMIN_KEY 时返回 503；配了且不匹配返回 401）。

## 消息

### POST /api/v1/phone/message —— 发短信/单聊
```json
{
  "from": "did:cha2a:agent:main",      // 必填：DID 或号码（校验注册/号码簿）
  "fromNumber": "+8613800138000",      // 可选：agent 对应的号码（与 from 号码身份一致，否则 403 IDENTITY_MISMATCH）
  "to": "+8613900139000",              // 必填：对端号码（须在号码簿，否则 404）
  "text": "你好",                       // 可选（≤GROUP_TEXT_MAX）
  "attachment": {                      // 可选
    "fileId": "<16位hex>", "name": "a.png", "size": 1234, "hash": "<sha256>",
    "kind": "binary", "chars": 0
  },
  "kind": "text",                      // 可选：text|card|...（card 必须带 payload）
  "payload": {},                       // 可选：结构化消息
  "agent": { "did": "...", "name": "...", "level": 0 }  // 可选：发送方展示信息
}
```
→ `201 {ok, id, to}`；错误 `400 invalid from/to`、`409 from not registered`、`403 IDENTITY_MISMATCH`、`404 number not in directory`。

### POST /api/v1/phone/message/recall —— 撤回
```json
{ "id": "m-...", "actor": "did:cha2a:agent:main" }
```
仅发送者可撤回；→ `200 {ok, id, status:"recalled"}`；`403 NOT_SENDER`、`404 NOT_FOUND`、`409 ALREADY_RECALLED`。

### GET /api/v1/phone/messages —— 收件箱
`?did=<DID>&since=<seq>` → `200 {did, count, messages:[...]}`（按 did 隔离；since 增量拉取）。

## 附件

### POST /api/v1/phone/attachment —— 上传（≤10MB，413 超限）
```json
{ "did": "did:cha2a:agent:main", "name": "qr.png", "mime": "image/png", "data": "<base64>" }
```
→ `201 {ok, fileId, name, mime, size, hash}`（`hash`=服务端 SHA-256，防篡改标记）。did 未注册 → 409。

### GET /api/v1/phone/attachment/:id —— 下载
→ 文件字节流；`404 attachment not found`（fileId 须 16 位 hex）。

## 群组

| 端点 | 方法 | 说明 | Admin? |
|---|---|---|---|
| `/api/v1/phone/group` | POST | 建群 `{name, creator, members[]}`（成员须注册/在簿，≤100）→ `{ok, groupId, conversationId}` | 否 |
| `/api/v1/phone/group/list?did=` | GET | 群列表 `{groups:[{groupId,name,memberCount}]}` | 否 |
| `/api/v1/phone/group/:id` | GET | 群详情 `{ok,groupId,name,members[],conversationId,announcement}` | 否 |
| `/api/v1/phone/group/:id/members-detail` | GET | 成员 `{member,nickname,type:phone\|agent,level}` | 否 |
| `/api/v1/phone/group/:id/audit` | GET | 群审计事件 | 否 |
| `/api/v1/phone/group/:id/messages` | GET | 群消息 `?since=` | 否 |
| `/api/v1/phone/group/message` | POST | 群消息广播（body 同 `/phone/message`，但 `to`→`groupId`） | 否 |
| `/api/v1/phone/group/member` | POST | 加成员 `{groupId, member, actor}` | **是** |
| `/api/v1/phone/group/member` | DELETE | 移除成员 | **是** |
| `/api/v1/phone/group/leave` | POST | 退群 | **是** |
| `/api/v1/phone/group/disband` | POST | 解散 | **是** |
| `/api/v1/phone/group/announcement` | POST | 群公告 `{groupId, text≤500, actor}` | **是** |

群消息广播（POST `/api/v1/phone/group/message`）已支持 `attachment`（fileId/name/size/hash/kind/chars），同单聊。

## Agent 资料

- `GET /api/v1/agent/profile` → 当前 agent 资料
- `PUT /api/v1/agent/profile` → 更新（字段见响应结构）

## Registry（只读，compliancehub.cn）

| 端点 | 说明 |
|---|---|
| `GET /api/v1/did/<did>` | DID Document / 404 |
| `GET /api/v1/trust/query?did=<did>` | `{registered, level, metadata:{name, author}}` |
| `GET /api/v1/phone/resolve?number=<号码>` | `{registered, agentDid, trust:{level}}` |
| `GET /api/v1/phone/directory` | 号码簿 |

## 错误码速查

| 码 | 含义 |
|---|---|
| `IDENTITY_MISMATCH` | fromNumber 与号码身份不一致 |
| `NOT_SENDER` / `ALREADY_RECALLED` | 撤回权限/状态 |
| `NOT_FOUND` / `INVALID_ID` | 消息/群不存在 |
| `number not in directory` / `member number not in directory` | 号码不在簿 |
| `agent not registered` | DID 未注册 |
| 503 | admin 端点但服务端未配 ADMIN_KEY |
| 401 | X-Admin-Key 不匹配 |
