# 其他服务端能力

## 游戏礼包 — 核销兑换码

### 接口说明

用户在获取到礼包兑换码进入游戏后，发起核销兑换码的动作，开发者需要使用本接口校验礼包兑换码的有效性。校验通过后才可以发放对应礼包。

### 基本信息

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/gift/receive_reward` |
| HTTP Method | POST |
| Scope | open.ttgame.mgplatform |
| SDK 方法名 | GiftReceiveReward |

### 请求参数

**请求头**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| access-token | String | 是 | 调用 getAccessToken 生成的 token |
| content-type | String | 是 | 固定值 `"application/json"` |

**Body（JSON）**

| 参数名 | 类型 | 必填 | 说明 |
|------|------|------|------|
| gift_code | String | 是 | cdk 兑换码 |
| open_id | String | 是 | 兑奖用户的 OpenID |
| uuid | String | 是 | 开发者厂商侧传入，幂等标识 |
| env_type | String | 否 | 环境类型，通过 tt.getEnvInfoSync 获取 |

### 响应参数

| 参数名 | 类型 | 说明 |
|------|------|------|
| err_no | Int32 | 错误码，0 为成功 |
| err_msg | String | 错误信息 |
| log_id | String | 请求日志 ID |
| gift_info | Struct | 礼包信息 |

**gift_info 结构**：

| 参数名 | 类型 | 说明 |
|------|------|------|
| play_type | Int32 | 玩法类型 |
| name | String | 礼包名称 |
| icon_url | String | 礼包图标 URL |
| gift_id | String | 礼包 ID |
| gift_effective_start_time | Int64 | 礼包生效开始时间（Unix 秒） |
| gift_effective_end_time | Int64 | 礼包生效结束时间（Unix 秒） |
| user_receive_guide | Array\<String\> | 用户领取引导文案 |
| prop_list | Array\<Struct\> | 道具列表 |
| prop_list[].prop_id | String | 道具 ID |
| prop_list[].name | String | 道具名称 |
| prop_list[].icon | String | 道具图标 URL |
| prop_list[].count | Int32 | 道具数量 |

### 错误码

| HTTP 状态码 | 错误码 | 描述 | 排查建议 |
|------|------|------|------|
| 200 | 28001005 | 系统内部错误 | 重试 |
| 200 | 28001003 | access_token 无效 | 重新获取 token |
| 200 | 28001008 | access_token 过期 | 刷新 token |
| 200 | 28001006 | 网络调用错误 | 重试 |
| 200 | 28001007 | 参数错误 | 检查参数 |
| 200 | 28006040 | 礼包码重复核销 | 该券已提交过核销 |
| 200 | 28006041 | 礼包码与 open_id 绑定关系有误 | 确认绑定关系 |

---

## Link 链接

### 生成 Link
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/url_link/generate` |
| HTTP Method | POST |
| SDK 方法名 | AppsUrlLinkGenerate |

### 查询 Link
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/url_link/query_info` |
| HTTP Method | POST |
| SDK 方法名 | AppsUrlLinkQueryInfo |

### 查询 Link 配额
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/url_link/query_quota` |
| HTTP Method | POST |
| SDK 方法名 | AppsUrlLinkQueryQuota |

---

## Schema 链接

### 生成 Schema
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/schema/generate` |
| HTTP Method | POST |
| SDK 方法名 | SchemaGenerate |

### 查询 Schema
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/schema/query_info` |
| HTTP Method | POST |
| SDK 方法名 | SchemaQueryInfo |

### 查询 Schema 配额
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/schema/query_quota` |
| HTTP Method | POST |
| SDK 方法名 | SchemaQueryQuota |

---

## 动态分享

### 生成活动 ID
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/share/create_activity_id` |
| HTTP Method | GET |
| SDK 方法名 | ShareCreateActivityId |

### 更新动态消息
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/share/update_dynamic_message` |
| HTTP Method | POST |
| SDK 方法名 | ShareUpdateDynamicMessage |

---

## 游戏群标签

### 查询用户群标签
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/group_tag/get_user_group_tag` |
| HTTP Method | POST |
| SDK 方法名 | GetUserGroupTag |

### 设置用户群标签
| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/group_tag/set_user_group_tag` |
| HTTP Method | POST |
| SDK 方法名 | SetUserGroupTag |

---

## 公会群解绑

| 属性 | 值 |
|------|------|
| HTTP URL | `https://minigame.zijieapi.com/mgplatform/api/apps/share/unbind_union_group` |
| HTTP Method | POST |
| SDK 方法名 | ShareUnbindUnionGroup |

---

## 赛事相关

### 上报赛事报名用户
| 属性 | 值 |
|------|------|
| URL 路径 | `/mgplatform/api/apps/microgame_competition/upload_player` |

### 选手排名上报
| 属性 | 值 |
|------|------|
| URL 路径 | `/mgplatform/api/apps/microgame_competition/upload_rank` |

---

## 内容安全检测

### 接口说明
用于检测游戏内容（文本、图片等）是否合规。

| 属性 | 值 |
|------|------|
| URL 路径 | `/mgplatform/api/apps/content_safety/check` |

---

## 广告变现数据开放 API

提供广告变现相关数据的服务端查询接口。

> **注意**：上述 Link、Schema、动态分享、群标签、客服消息、赛事上报、内容安全、广告变现等 API 的详细参数和错误码，请参考[官方文档](https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/server/)获取最新信息。

## 通用错误码

| 错误码 | 描述 |
|------|------|
| -1 | 系统错误 |
| 28001003 | access_token 无效 |
| 28001005 | 系统内部错误 |
| 28001006 | 网络调用错误 |
| 28001007 | 参数错误 |
| 28001008 | access_token 过期 |
| 28001038 | 参数错误 |
| 28001039 | 签名不正确 |
| 28005139 | 请求过于频繁 |

## 最佳实践

1. **Token 管理**：使用 genStableAccessToken 进行 token 管理，避免多服务互刷 token
2. **安全原则**：AppSecret 永远只存在服务端，不下发到客户端
3. **签名校验**：涉及用户数据的 API 务必正确生成 signature
4. **频率控制**：注意各 API 的频率限制，合理设置重试策略
5. **错误处理**：针对不同错误码实现差异化处理逻辑
6. **幂等设计**：支付、礼包核销等操作必须使用 uuid 保证幂等
7. **SDK 优先**：优先使用官方 SDK 接入，减少自行实现签名和 token 管理
