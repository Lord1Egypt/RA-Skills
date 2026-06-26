# 协作文档监控技能 (Doc-Collaboration-Watcher)

**版本**: v1.0  
**创建**: 2026-04-07  
**作者**: 伊娃  
**状态**: 开发中

---

## 📋 技能概述

实时监控协作文档变更，自动通知所有相关子代理和沟通通道，确保多代理协作信息同步。

**适用场景**：
- 多代理协作项目（如 ESP32 固件 + 前端 + 后端）
- 跨团队接口对齐
- 分布式文档维护
- 需要实时同步的协作场景

---

## 🎯 核心功能

### 1. 文档变更监控
- 监控指定目录下的 Markdown 文件
- 检测文件创建、修改、删除
- 计算文件哈希，避免误报

### 2. 实时通知
- **飞书通道**：发送变更消息
- **微信通道**：发送变更消息
- **iMessage 通道**：发送变更消息
- **WebChat 会话**：发送变更消息

### 3. 变更历史
- 记录所有文档变更
- 保存变更时间、文件、大小
- 支持查询历史变更

### 4. 响应追踪
- 追踪各代理确认状态
- 超时未确认时提醒
- 生成响应统计报告

---

## 📦 安装

```bash
# 1. 克隆技能到 workspace
cd ~/.openclaw/workspace/skills
git clone <repo-url> doc-collaboration-watcher

# 2. 安装依赖
pip3 install watchdog

# 3. 配置监控目录
cp config.example.json config.json
# 编辑 config.json 设置监控目录、通知通道等

# 4. 启动监控
python3 bin/doc-watcher.py
```

---

## ⚙️ 配置

### config.json
```json
{
  "workspace": "/Users/bot-eva/.openclaw/workspace",
  "docs_dir": "docs",
  "log_dir": "logs",
  "watched_files": [
    "esp32-collaboration.md",
    "esp32-collaboration-discussion.md"
  ],
  "notification": {
    "channels": ["feishu", "wechat", "imessage", "webchat"],
    "response_timeout_minutes": 5,
    "evaluation_timeout_minutes": 30
  },
  "agents": [
    {"name": "伊娃 - 固件", "role": "firmware"},
    {"name": "伊娃 - 前端", "role": "frontend"},
    {"name": "伊娃 - 后端", "role": "backend"}
  ]
}
```

---

## 🚀 使用

### 启动监控
```bash
# 后台运行
python3 bin/doc-watcher.py &

# 或使用 systemd（Linux）
sudo systemctl start doc-watcher
```

### 查看变更历史
```bash
cat logs/doc_change_history.json
```

### 测试通知
```bash
# 修改监控文件
echo "# 测试变更" >> docs/esp32-collaboration.md

# 观察通知输出
```

---

## 📊 通知格式

### 飞书/微信/iMessage
```
📢 文档变更通知

文件：esp32-collaboration.md
时间：2026-04-07 20:50:15
变更类型：修改
大小：15.2 KB → 16.8 KB

要求：
✅ 5 分钟内确认收到
✅ 30 分钟内评估影响

查看详情：file:///Users/bot-eva/.openclaw/workspace/docs/esp32-collaboration.md
```

### WebChat
```
🔍 检测到协作文档变更

**文件**: esp32-collaboration.md
**时间**: 2026-04-07 20:50:15
**变更**: v1.0 → v1.1

**影响评估**:
- 接口变更：是/否
- 需要配合：是/否
- 紧急程度：高/中/低

[查看详情] [确认收到] [需要讨论]
```

---

## 🔧 集成 OpenClaw

### 作为 OpenClaw 技能
```yaml
# skill.yaml
name: doc-collaboration-watcher
version: 1.0.0
description: 协作文档实时监控
author: Eva
tools:
  - file:watch
  - message:send
  - cron:schedule
permissions:
  - file:read
  - file:write
  - message:send
```

### OpenClaw 配置
```json
// openclaw.json
{
  "skills": {
    "doc-collaboration-watcher": {
      "enabled": true,
      "config": {
        "docs_dir": "docs",
        "channels": ["feishu", "wechat", "imessage"]
      }
    }
  }
}
```

---

## 📈 监控指标

### 变更统计
- 每日变更次数
- 各文件变更频率
- 平均响应时间

### 响应统计
- 确认率（5 分钟内）
- 评估及时率（30 分钟内）
- 超时次数

### 报告示例
```markdown
## 文档监控周报 (2026-04-01 ~ 2026-04-07)

### 变更统计
- 总变更：23 次
- esp32-collaboration.md: 15 次
- esp32-collaboration-discussion.md: 8 次

### 响应统计
- 确认率：95% (22/23)
- 评估及时率：87% (20/23)
- 超时：1 次（伊娃 - 前端，2026-04-05 14:30）

### 改进建议
- 增加变更摘要（避免频繁查看全文）
- 添加变更对比（diff）功能
```

---

## 🤝 协作流程

### 标准流程
```
1. 伊娃 A 修改文档
   ↓
2. 监控系统检测到变更
   ↓
3. 自动通知所有通道和代理
   ↓
4. 各代理确认收到（5 分钟内）
   ↓
5. 相关代理评估影响（30 分钟内）
   ↓
6. 需要配合 → 调整工作计划
   ↓
7. 无需配合 → 继续原计划
```

### 接口变更流程
```
1. 在文档中修改接口定义
   ↓
2. 更新版本记录表
   ↓
3. 系统自动通知
   ↓
4. 相关方评估（30 分钟）
   ↓
5. 确认无误 → 各自实现
   ↓
6. 有分歧 → 子代理评审 → 老板决策
```

---

## 🧪 测试计划

### 阶段 1：基础监控
- [ ] 文件修改检测
- [ ] 文件创建检测
- [ ] 哈希计算正确
- [ ] 变更历史记录

### 阶段 2：通知功能
- [ ] 飞书通知
- [ ] 微信通知
- [ ] iMessage 通知
- [ ] WebChat 通知

### 阶段 3：响应追踪
- [ ] 确认状态追踪
- [ ] 超时提醒
- [ ] 统计报告

### 阶段 4：OpenClaw 集成
- [ ] 技能打包
- [ ] 配置管理
- [ ] 权限控制
- [ ] ClawHub 发布

---

## 📝 版本记录

| 版本 | 日期 | 变更 | 作者 |
|------|------|------|------|
| v1.0 | 2026-04-07 | 初始版本 | 伊娃 |

---

## 🔗 相关链接

- **主文档**: `/Users/bot-eva/.openclaw/workspace/docs/esp32-collaboration.md`
- **讨论记录**: `/Users/bot-eva/.openclaw/workspace/docs/esp32-collaboration-discussion.md`
- **监控脚本**: `/Users/bot-eva/.openclaw/workspace/bin/doc-watcher.py`
- **ClawHub**: https://clawhub.ai/skills/doc-collaboration-watcher

---

*本技能由伊娃开发，用于多代理协作文档实时监控*
