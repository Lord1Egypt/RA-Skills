# 📊 OpenClaw 仪表盘截图技能

**创建时间：** 2026-03-28
**最后更新：** 2026-03-28
**技能位置：** `~/.openclaw/workspace/skills/dashboard-screenshot/SKILL.md`

---

## 🎯 触发词

- "查看仪表盘"
- "仪表盘状态"
- "OpenClaw 仪表盘"
- "机器人状态"
- "dashboard"
- "截图仪表盘"
- "检查仪表盘并发送截图"

---

## 🔧 工作流程

### 步骤 1：检查服务是否运行

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null
```

**说明：**
- 检查端口 3000 是否响应
- 返回 `200` → 服务已运行，跳至步骤 3
- 返回其他或未响应 → 继续步骤 2

---

### 步骤 2：启动仪表盘服务（如未运行）

```bash
cd ~/.openclaw/OpenClaw-bot-review && npm run dev
```

**说明：**
- 后台运行服务
- 等待 8 秒确保服务完全启动

**工具调用：**
```json
{
  "exec": {
    "command": "cd ~/.openclaw/OpenClaw-bot-review && npm run dev",
    "background": true,
    "yieldMs": 8000
  }
}
```

---

### 步骤 3：打开浏览器

**工具调用：**
```json
{
  "action": "open",
  "url": "http://localhost:3000"
}
```

**说明：**
- 打开仪表盘页面
- 获取 `targetId` 用于后续操作

---

### 步骤 4：等待页面加载

**工具调用：**
```json
{
  "action": "snapshot",
  "targetId": "<targetId>",
  "timeoutMs": 5000
}
```

**说明：**
- 检查页面是否加载完成
- 确认显示机器人卡片、统计信息等

---

### 步骤 5：截取完整页面

**工具调用：**
```json
{
  "action": "screenshot",
  "targetId": "<targetId>",
  "fullPage": true,
  "type": "png"
}
```

**说明：**
- 截取完整滚动页面
- 截图自动保存到 `~/.openclaw/media/browser/<uuid>.png`

---

### 步骤 6：发送截图给用户

**说明：**
- 通过 QQbot 发送截图
- 附带关键状态说明（机器人状态、Token 用量、定时任务等）

---

## 📁 关键路径

| 项目 | 路径 |
|------|------|
| 技能文档 | `~/.openclaw/workspace/skills/dashboard-screenshot/SKILL.md` |
| 项目目录 | `~/.openclaw/OpenClaw-bot-review/` |
| package.json | `~/.openclaw/OpenClaw-bot-review/package.json` |
| 截图保存 | `~/.openclaw/media/browser/<uuid>.png` |

---

## ⚠️ 注意事项

1. **服务自启动** - 如果端口 3000 未响应，自动执行 `npm run dev`
2. **等待时间** - 启动后等待 8 秒确保服务完全就绪
3. **页面加载** - 使用 snapshot 确认页面加载完成再截图
4. **完整页面** - 使用 `fullPage: true` 截取全部内容
5. **后台运行** - npm dev 进程后台运行，不阻塞后续操作
6. **浏览器状态** - 如果浏览器未打开或卡死，先重启浏览器
7. **错误处理** - 如果任何步骤失败，给出明确错误提示

---

## ✅ 成功标准

- [ ] 端口检查通过或成功启动服务
- [ ] 浏览器成功打开且无错误
- [ ] 页面加载完成（snapshot 确认）
- [ ] 截图成功保存（返回 image data）
- [ ] 消息发送成功（无 error）
- [ ] 状态说明清晰完整

---

## 🐛 已知问题

1. **网络问题** - 如果 clawhub 无法访问，无法通过 CLI 安装
2. **浏览器超时** - 如果页面加载缓慢，可能需要调整 timeoutMs
3. **端口占用** - 如果 3000 端口被占用，需要先清理

---

## 📊 响应模板

```
📸 **OpenClaw 仪表盘截图完成！**

## 📊 仪表盘关键信息

**🤖 机器人状态：**
- **呆黄 (main)** - {状态}
  - 模型：{模型名称} ✅
  - 平台：{平台列表}
  - 会话数：{数量} | 消息数：{数量} | Token: {用量}
  - 最近活跃：{时间} | 平均响应：{时间}

- **小黄 (xiaohuang)** - {状态}
  - 模型：{模型名称} {状态}
  - 平台：{平台列表}
  - 会话数：{数量} | 消息数：{数量} | Token: {用量}
  - 最近活跃：{时间} | 平均响应：{时间}

**⏰ 定时任务：**
- {任务列表摘要}

**📈 全局统计：**
- 总 Input Token：{数量}
- 总 Output Token：{数量}
- 总消息数：{数量}

**🦞 Gateway：** {状态}
- 更新于：{时间}

---
Dashboard 已成功启动在 `http://localhost:3000`！🫡
```

---

_此技能由呆黄创建并维护_
_最后更新：2026-03-28_
