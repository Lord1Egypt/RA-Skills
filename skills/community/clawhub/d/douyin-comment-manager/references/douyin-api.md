# 抖音开放平台 - 评论管理 API 参考

> 本文档汇总抖音开放平台官方评论管理相关 API 信息，作为备用方案参考。

## 权限要求

- **权限名称**: 互动管理 (Interaction Management)
- **Scope**: `video.comment`
- **申请路径**: 抖音开放平台 → 管理中心 → 应用管理 → 详情 → 接口权限 → 申请"互动管理"
- **适用账号**: 抖音企业号 / MCN 机构号

## API 接口列表

### 1. 获取视频评论列表

```
GET https://open.douyin.com/video/comment/list/
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `open_id` | string | 是 | 用户 open_id |
| `access_token` | string | 是 | 授权 token |
| `item_id` | string | 是 | 视频 ID |
| `cursor` | int | 否 | 分页游标 |
| `count` | int | 否 | 每页数量（最大 50） |

**返回**: 评论列表 + 分页游标 + 是否有更多

### 2. 获取评论回复列表

```
GET https://open.douyin.com/video/comment/reply/list/
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `open_id` | string | 是 | 用户 open_id |
| `access_token` | string | 是 | 授权 token |
| `item_id` | string | 是 | 视频 ID |
| `comment_id` | string | 是 | 评论 ID |
| `cursor` | int | 否 | 分页游标 |
| `count` | int | 否 | 每页数量（最大 50） |

### 3. 回复视频评论

```
POST https://open.douyin.com/video/comment/reply/
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `open_id` | string | 是 | 用户 open_id |
| `access_token` | string | 是 | 授权 token |
| `item_id` | string | 是 | 视频 ID |
| `comment_id` | string | 是 | 被回复的评论 ID |
| `content` | string | 是 | 回复内容（最长 500 字） |

### 4. 置顶视频评论（仅企业号）

```
POST https://open.douyin.com/video/comment/top/
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `open_id` | string | 是 | 用户 open_id |
| `access_token` | string | 是 | 授权 token |
| `item_id` | string | 是 | 视频 ID |
| `comment_id` | string | 是 | 要置顶的评论 ID |
| `top` | bool | 是 | true=置顶, false=取消置顶 |

## API vs Playwright 对比

| 维度 | API 方案 | Playwright 方案 |
|------|---------|----------------|
| 申请门槛 | 需要企业号 + 审核 | 无需申请 |
| 稳定性 | 官方保证 | 依赖页面结构 |
| 频率限制 | Token 级别 QPS 限制 | 需人工控制 |
| 数据完整性 | 结构化数据 | 需自行解析 |
| 登录管理 | OAuth 令牌 | Cookie/Profile |
| 适用场景 | 中大型 MCN/企业 | 个人创作者 |
| 维护成本 | 低（官方维护） | 中（页面变化需适配） |

## 注意事项

1. API 方案需要经过抖音开放平台审核，个人号通常无法通过
2. OAuth 授权需要用户扫码确认，每次授权有效期有限
3. API 调用有频率限制，批量操作需控制节奏
4. 回复内容不能含引流、外链等违规信息
5. 建议同时备有 API 和 Playwright 两套方案，按场景切换
