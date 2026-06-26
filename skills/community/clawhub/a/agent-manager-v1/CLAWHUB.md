# Agent Manager - 多 Agent 对话管理平台

**版本:** 1.0.0  
**作者:** MSK  
**描述:** 统一管理多个 OpenClaw Agent 的对话平台，支持文字+图片输入，对话历史自动保存

---

## 🎯 功能亮点

- **多 Agent 管理** - 统一管理所有 Agent（Judy/MNK/Fly/Dav/Zhou/PNews 等）
- **Gemini 风格界面** - 现代化左右分栏设计
- **图片输入** - 支持拖拽上传、按钮选择、复制粘贴
- **对话历史** - 自动保存，切换 Agent 不丢失
- **消息隔离** - 每个 Agent 独立对话历史，不会串台
- **本地存储** - 数据保存在浏览器，安全隐私

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd agent-manager
npm install
```

### 2. 启动服务

```bash
node server-gemini.js
```

### 3. 访问界面

打开浏览器访问：
```
http://localhost:3000
```

---

## 📋 功能说明

### 左侧边栏
- 显示所有已注册的 Agent
- 点击切换对话对象
- 支持创建新 Agent

### 右侧对话区
- 宽敞的对话界面
- 支持文字输入
- 支持图片上传（拖拽/按钮/粘贴）
- 对话历史自动保存

### 图片功能
- 点击 📎 按钮选择图片
- 直接拖拽图片到输入框
- 支持多张图片
- 实时预览，可删除

---

## 🔧 配置

### 连接 OpenClaw

编辑 `config.json`:
```json
{
  "openclawGateway": "http://127.0.0.1:18789",
  "openclawToken": "你的 Operator Token"
}
```

### 获取 Operator Token

```bash
cat ~/.openclaw/devices/paired.json | jq '.[].tokens.operator.token'
```

---

## 📁 文件结构

```
agent-manager/
├── server-gemini.js      # 主服务器
├── index.html            # 前端界面
├── package.json          # 依赖配置
├── config.json           # 配置文件
├── cli.js                # 命令行工具
├── README.md             # 详细文档
└── CLAWHUB.md            # 快速开始指南
```

---

## 💡 使用示例

### 与 Agent 对话

1. 左侧选择 Agent（如 Judy）
2. 右侧输入框输入消息
3. 按 Enter 或点击发送
4. 等待 Agent 回复

### 上传图片

1. 点击 📎 按钮选择图片
2. 或直接拖拽图片到输入框
3. 可添加文字说明
4. 点击发送

### 查看历史

1. 切换到其他 Agent
2. 再次切换回来
3. 完整对话记录自动加载

---

## 🎨 界面特点

- **Gemini 风格** - 参考 Google Gemini 设计
- **左右分栏** - 左侧 Agent 列表，右侧对话区
- **响应式设计** - 自适应窗口大小
- **现代配色** - 紫色渐变主题
- **流畅动画** - 消息淡入效果

---

## 📊 支持的 Agent

| Agent | 职责 | 模型 |
|-------|------|------|
| Judy | 营销外展 | qwen3.5-plus |
| MNK | 技术架构 | glm-5 |
| Fly | 日程管理 | qwen3.5-plus |
| Dav | 数据分析 | qwen3.5-plus |
| Zhou | 用户运营 | qwen3.5-plus |
| PNews | 新闻播报 | qwen3.5-plus |

---

## ⚠️ 注意事项

1. **Gateway 必须运行** - 确保 `openclaw gateway status` 显示 running
2. **浏览器隔离** - 不同浏览器历史不互通
3. **隐私模式** - 隐私模式下关闭浏览器会丢失历史
4. **图片大小** - 建议 5MB 以内

---

## 🆘 故障排查

**界面打不开？**
```bash
# 检查服务是否运行
ps aux | grep "node server"

# 重启服务
node server-gemini.js
```

**Agent 未加载？**
```bash
# 检查 OpenClaw Gateway
openclaw gateway status

# 刷新浏览器 Ctrl+Shift+R
```

---

## 📞 支持

- **文档:** 查看 README.md
- **问题:** 提交 Issue
- **更新:** 定期查看 ClawHub 更新

---

## 💰 付费说明

**价格:** $10 USD（一次性购买）

**包含:**
- ✅ 完整源代码
- ✅ 永久使用授权
- ✅ 基础技术支持
- ✅ 未来小版本更新

**支付方式:** PayPal (396554498@qq.com)

**购买后:**
1. 通过 ClawHub 下载技能包
2. 按照本指南安装使用
3. 如有问题请提交 Issue

---

## 📄 许可

**使用权限:**
- ✅ 个人使用
- ✅ 商业使用
- ❌ 转售技能本身
- ❌ 公开分发源码

---

**享受与 Agent 的高效对话！** 🚀
