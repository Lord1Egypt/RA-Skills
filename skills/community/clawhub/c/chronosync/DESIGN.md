# Session Sync - 设计文档

> 跨会话记忆同步与知识沉淀系统

---

## 核心理念

**无感、高效、可扩展**

- 无感运行：30分钟静默同步，不打扰用户
- 高效存储：增量写入，零冗余
- 可扩展：插件化架构，支持知识沉淀、待办同步等场景

---

## 架构设计

```
session-sync/
├── core/                      # 核心引擎
│   ├── sync_engine.py        # 同步引擎
│   ├── change_detector.py    # 变化检测
│   └── file_manager.py       # 文件管理
│
├── plugins/                   # 插件目录
│   ├── knowledge/            # 知识沉淀插件
│   └── todo/                 # 待办同步插件
│
├── output/                    # 输出目录
│   ├── shared_chat.json      # 机器可读格式
│   ├── shared_chat.md        # 人可读格式
│   ├── decisions/            # 决策记录
│   └── todos/                # 待办任务
│
└── session-sync.py           # 主入口
```

---

## 核心流程

### 同步流程

```
1. 定时触发 (30分钟)
2. 读取当前会话历史
3. 计算内容 hash
4. 与上次记录比对
5. 如有变化 → 增量写入
6. 触发插件处理
7. 静默完成
```

### 变化检测

- 使用 SHA256 计算会话内容 hash
- 只存储 hash 变化的部分
- 避免重复写入相同内容

### 文件格式

**JSON 格式** (机器可读)
```json
{
  "last_sync": "2026-03-13T21:30:00+08:00",
  "sessions": [
    {
      "id": "session-xxx",
      "timestamp": "2026-03-13T21:00:00+08:00",
      "hash": "sha256-xxx",
      "messages": [...]
    }
  ]
}
```

**Markdown 格式** (人可读)
```markdown
# Session Sync - 2026-03-13

## 21:00 - 会话主题

**用户:** 我觉得还是......
**AI:** 好思路！

...
```

---

## 插件系统

### 插件接口

```python
class Plugin:
    def on_sync(self, new_messages: list) -> dict:
        """同步后触发，返回处理结果"""
        pass
    
    def on_shutdown(self) -> None:
        """关闭时触发"""
        pass
```

### 知识沉淀插件

- 提取关键决策、结论
- 自动分类到 PARA 结构
- 生成 topic 笔记

### 待办同步插件

- 识别任务项（"我要..."、"记得..."）
- 追踪任务状态
- 跨会话提醒

---

## 配置项

```yaml
# config.yaml
sync:
  interval_minutes: 30
  output_dir: "~/.openclaw/workspace/memory/sync"
  
plugins:
  knowledge:
    enabled: true
    auto_categorize: true
  
  todo:
    enabled: true
    reminder_before_hours: 24
```

---

## 安装与使用

### 安装

```bash
openclaw skills install session-sync
```

### 配置 cron

```bash
openclaw cron add session-sync --interval 30m --command "python -m session_sync"
```

### 手动触发

```bash
python -m session_sync --now
```

---

## 差异化优势

| 现有方案 | Session Sync |
|----------|--------------|
| 被动查询历史 | 主动增量同步 |
| 定时 compaction 触发 | 独立定时，更及时 |
| 单格式存储 | JSON + Markdown 双格式 |
| 固定功能 | 插件化扩展 |
| 可能冗余存储 | hash 去重，零冗余 |

---

## Roadmap

### v1.0 - MVP
- [ ] 核心同步引擎
- [ ] 增量写入 + hash 去重
- [ ] JSON + Markdown 输出
- [ ] cron 自动配置

### v1.1 - 知识沉淀
- [ ] 决策提取
- [ ] PARA 自动分类
- [ ] topic 笔记生成

### v1.2 - 待办同步
- [ ] 任务识别
- [ ] 状态追踪
- [ ] 到期提醒

### v1.3 - 高级功能
- [ ] Web UI 查看器
- [ ] 跨设备同步
- [ ] 团队协作模式

---

*设计时间: 2026-03-13*
