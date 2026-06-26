# 飞书应用权限配置指南

通过 feishu-quick-setup 扫码创建的飞书应用（archetype: PersonalAgent）会自动包含基础权限。
如需使用高级功能，需在飞书开放平台手动开启对应权限。

## 基础权限（自动包含）

扫码创建的 Bot 默认具备以下能力：
- 接收和发送 IM 消息
- 读取用户基本信息

## 按功能所需权限

### 文档操作（feishu-create-doc / feishu-fetch-doc / feishu-update-doc）

| 权限 | 说明 |
|------|------|
| `docx:document` | 读取文档内容 |
| `docx:document:create` | 创建文档 |
| `docx:document:readonly` | 只读访问文档 |
| `docs:doc` | 旧版文档权限 |

### Wiki（feishu-wiki）

| 权限 | 说明 |
|------|------|
| `wiki:wiki` | Wiki 读写 |
| `wiki:wiki:readonly` | Wiki 只读 |

### 云盘（feishu-drive）

| 权限 | 说明 |
|------|------|
| `drive:drive` | 云盘文件读写 |
| `drive:drive:readonly` | 云盘只读 |

### 消息（feishu-im-read / feishu-chat）

| 权限 | 说明 |
|------|------|
| `im:message` | 发送消息 |
| `im:message:readonly` | 读取消息历史 |
| `im:chat:readonly` | 读取群聊信息 |

### 日历（feishu-calendar）

| 权限 | 说明 |
|------|------|
| `calendar:calendar` | 日历事件读写 |
| `calendar:calendar:readonly` | 日历只读 |

### 任务（feishu-task）

| 权限 | 说明 |
|------|------|
| `task:task` | 任务读写 |
| `task:task:readonly` | 任务只读 |

### 多维表格（feishu-bitable）

| 权限 | 说明 |
|------|------|
| `bitable:app` | 多维表格读写 |

### 通讯录（feishu-search-user）

| 权限 | 说明 |
|------|------|
| `contact:user.base:readonly` | 读取用户基本信息 |
| `contact:contact.base:readonly` | 读取通讯录基本信息 |

## 如何开启权限

1. 登录 [飞书开放平台](https://open.feishu.cn)
2. 进入应用管理 → 找到扫码创建的应用
3. 左侧菜单 → 权限管理
4. 搜索并开启所需权限
5. 如需管理员审批，联系企业管理员

## 注意事项

- PersonalAgent 类型的应用部分高级权限需要管理员审批
- 权限变更后可能需要用户重新授权（通过 feishu-auth 自动触发）
- 建议按需开启权限，不要一次性开启所有权限
