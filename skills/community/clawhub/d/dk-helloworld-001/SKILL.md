# DK Hello World Printer

**DK Hello World Printer** 是一个简单技能，用于打印用户输入的任何文本到控制台，方便快速调试或演示。

## 功能
- 接收任意字符串输入
- 直接打印输出，无需其他处理
- 适合作为演示或快速调试工具

## 使用示例

```javascript
const inputText = "Hello Clawhub!";
print(inputText);
// 控制台输出: Hello Clawhub!


| API端点                                | HTTP方法 | 功能摘要                                               | 注意事项                                                              |
| ------------------------------------ | ------ | -------------------------------------------------- | ----------------------------------------------------------------- |
| `/.well-known/clawhub.json`          | GET    | 返回 registry 配置（apiBase / authBase / minCliVersion） | 必须支持 `application/json`；允许匿名访问；用于 CLI 初始化                         |
| `/api/v1/whoami`                     | GET    | 获取当前登录用户信息                                         | 必须带 `Authorization: Bearer <token>`；返回 user profile；用于校验 token    |
| `/api/v1/search?q=<query>`           | GET    | 搜索技能（向量/关键词）                                       | 必须带 Bearer；返回 results 数组；无缓存（`Cache-Control: no-store`）           |
| `/api/v1/skills/{slug}`              | GET    | 获取技能元数据（install / inspect 共用）                      | 核心接口；返回 skill + version + owner + moderation 信息                   |
| `/api/v1/download?slug=&version=`    | GET    | 下载技能压缩包                                            | 返回 `application/zip`；必须设置 `Content-Disposition`；鉴权；有较低 rate limit |
| `/api/v1/skills`                     | POST   | 发布技能（publish）                                      | 推测接口；通常为 multipart/form-data 或 JSON；需鉴权                           |
| `/api/v1/skills/{slug}`              | DELETE | 删除技能（软删除）                                          | 对应 delete 命令；需权限控制（owner/admin）                                   |
| `/api/v1/auth/token`（或等价）            | POST   | 使用 token 登录（CLI login --token）                     | CLI 本质只是本地存 token，但服务端需提供 token 校验体系                              |
| `/api/v1/auth/logout`（可选）            | POST   | 注销 token（可选实现）                                     | 实际 CLI 是本地删除，但服务端可支持 token revoke                                 |
| `/cli/auth`                          | GET    | 浏览器 OAuth 登录入口                                     | 用于 login browser flow；需支持 redirect_uri                            |
| `/api/v1/skills/{slug}/versions`（可选） | GET    | 获取版本列表                                             | install 目前只用 latest，但 registry 通常需要版本管理                           |
| `/api/v1/skills/{slug}/star`（可选）     | POST   | 收藏技能                                               | 对应 star 命令（可延后）                                                   |
| `/api/v1/skills/{slug}/star`         | DELETE | 取消收藏                                               | 对应 unstar                                                         |
