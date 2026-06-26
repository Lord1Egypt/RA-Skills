# 飞书群管理 OpenClaw Skill

让不懂技术的用户也能用自然语言管理飞书群组。

## 功能

- 🔍 **查看群列表** - 列出所有飞书群
- 👥 **查看群成员** - 查看指定群的成员
- ➕ **拉人进群** - 将成员添加到群组
- ➖ **移除成员** - 将成员从群组移除
- 📢 **发送消息** - 向群组发送消息
- ✏️ **修改群名** - 重命名群组
- 🆕 **创建新群** - 创建群组并邀请成员

## 安装

1. 将整个 `feishu-group-ops/` 目录复制到 `~/.openclaw/skills/`

2. 配置飞书应用凭证：
   ```bash
   openclaw config set FEISHU_APP_ID "your_app_id"
   openclaw config set FEISHU_APP_SECRET "your_app_secret"
   ```

3. 重启 OpenClaw 或等待技能热重载

## 飞书应用配置

需要在[飞书开放平台](https://open.feishu.cn/app)创建应用，并开通以下权限：

| 权限 | 用途 |
|-----|------|
| `im:chat` | 读取/修改群信息 |
| `im:chat.member` | 管理群成员 |
| `im:message` | 发送消息 |
| `contact:user.id:readonly` | 搜索用户 |

## 使用示例

直接用中文告诉 OpenClaw 你想做什么：

- "帮我把张三加到市场群"
- "技术群里都有谁？"
- "给运营群发消息说明天开会"
- "把产品群改名为产品2025群"
- "踢出小明从销售群"
- "新建一个Q2项目群，把李明王芳拉进去"

## 文件结构

```
feishu-group-ops/
├── SKILL.md              # 技能定义（OpenClaw 读取）
├── README.md             # 本文件
├── scripts/
│   └── feishu.py         # 飞书 API 调用脚本
└── examples/
    └── conversations.md  # 对话示例
```

## 注意事项

- 需要 Python 3.6+（通常系统已自带）
- 飞书应用需要企业管理员审批发布
- Token 有效期 2 小时，会自动刷新
