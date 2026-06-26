# 权限需求

本技能核心依赖：**用户 OAuth 授权（User Access Token）**

`feishu_im_user_message` 以用户身份发消息，必须用户先完成 OAuth 授权，否则所有发送操作都会失败。

## 授权方式

- **推荐**：`feishu_oauth_batch_auth` — 一次性授权所有已开通的用户权限
- **单次授权**：用户在飞书中点击应用授权弹窗完成

## 必需的用户权限（User Access Token scope）

| 权限 | 用途 | 对应操作 |
|------|------|---------|
| `im:message` | 以用户身份发送群消息 | `feishu_im_user_message` |
| `im:message:readonly` | 读取群消息历史 | `feishu_im_user_get_messages` |
| `im:chat` | 搜索消息、获取群信息 | `feishu_im_user_search_messages` |
| `im:resource` | 上传图片 | 脚本调用 `/im/v1/images` |

## 首次使用检查

其他 agent 首次使用本技能时，**必须先确认用户已 OAuth 授权**：

1. 尝试调用 `feishu_im_user_message` 发送一条测试消息
   - 成功 → 用户已授权，权限就绪
   - 失败且提示授权 → **必须先调用 `feishu_oauth_batch_auth`**，提示用户完成授权后重试
2. 可选：尝试 `feishu_im_user_get_messages` 读取群消息
3. 可选：如需发图，用脚本上传测试图片

## 授权失败时的降级策略

| 权限缺失 | 降级行为 |
|---------|---------|
| OAuth 未授权 | **技能完全不可用**，必须先授权 |
| `im:message` | 无法发送消息 |
| `im:message:readonly` | 无法读取群消息，跳过群监控 |
| `im:resource` | 降级为纯文字模式，不发图片 |
| `im:chat` | 无法搜索消息，仅能按群获取 |
