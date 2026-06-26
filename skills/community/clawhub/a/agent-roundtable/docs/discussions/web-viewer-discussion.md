# 圆桌讨论结论：内置 Web 查看页面

## 摘要
- **参与者**：饼哥（产品总监）、像素姐（设计师）、码飞（开发工程师）
- **轮次**：3 轮
- **日期**：2026-05-21
- **讨论 ID**：rt_36c7dbdd

## 共识点

1. **核心价值**：降低圆桌讨论的分发门槛，让没有配置 channel 的用户也能查看讨论内容
2. **目标用户**：内容创作者/自媒体、内部小团队、外部协作方
3. **部署模式**：集成到 Hermes Agent 主进程（零配置），不独立部署
4. **数据存储**：直接复用 discussion.json 文件，零额外依赖
5. **技术方案**：混合方案（静态骨架 + SSE 增量更新）
6. **隐私安全**：MVP 只做链接撤销（L1），过期时间（L2）和密码（L3）后续迭代

## 分歧点

无阻塞性分歧。三位在各轮讨论中充分对齐，最终确认全部一致。

## 决策

### MVP 功能清单（P0）

| # | 功能 | 说明 |
|---|------|------|
| 1 | 自动 Web 页面 | 讨论开始时自动生成，nanoid(21) token URL |
| 2 | 单页阅读 | 单列时间流布局，品牌蓝 #4F46E5，亮色主题 |
| 3 | SSE 实时更新 | 新发言淡入动画 + 高亮 3 秒，Last-Event-ID 断线续传 |
| 4 | 结论卡片 | 讨论结束后自动追加，发光卡片设计，自动滚动定位 |
| 5 | 移动端适配 | 响应式布局，<768px 单列，最小字号 14px |
| 6 | 链接撤销 | 创作者可一键撤销 token，优雅失效提示 |
| 7 | 页面三态 | 等待中/进行中/已结束，视觉状态清晰区分 |

### 技术架构

```
┌─────────────────────────────────────────────┐
│         Hermes Agent 主进程                  │
│  roundtable-ai (Python)                     │
│    └─ discussion.json ← 唯一数据源           │
│    └─ 启动时 spawn → Web 服务 (8199)         │
├─────────────────────────────────────────────┤
│       Express (Node.js) 单文件               │
│  GET /r/:token         → SPA 页面            │
│  GET /api/:token/data  → JSON 数据           │
│  GET /api/:token/events→ SSE 推送            │
│  POST /api/:token/revoke → 链接撤销          │
└─────────────────────────────────────────────┘
```

### 文件结构

```
roundtable_ai/
  web_publisher.py      # 核心模块：WebPublisher 类
  web/
    index.html          # 单文件 SPA（内联 CSS+JS，Tailwind CDN）
    theme.css           # CSS 变量表
```

### API 接口

| 路径 | 方法 | 说明 |
|------|------|------|
| `/r/:token` | GET | SPA 页面入口 |
| `/api/:token/data` | GET | 返回完整 discussion JSON |
| `/api/:token/events` | GET | SSE 实时推送 |
| `/api/:token/revoke` | POST | L1 链接撤销 |

### Python 集成

```python
class WebPublisher:
    def start(self, discussion_id: str, token: str) -> str:  # 启动 Web 服务
    def on_speech(self, speech: dict):  # Hook: 新发言
    def conclude(self, conclusion: str):  # Hook: 讨论结束
    def revoke(self):  # L1 链接撤销
```

集成点：`Roundtable.run()` 主循环中，每条发言后调 `publisher.on_speech(speech)`，讨论结束时调 `publisher.conclude(conclusion)`。

## 行动项

1. **码飞**：后端开发（WebPublisher + SSE + 端口探测 + 文件锁）— 2 天
2. **像素姐**：前端页面（三态 + 响应式 + 主题变量）— 1 天（可与码飞并行）
3. **协调者**：集成测试 + 微信真机验证 + 验收 — 1 天 buffer

## 验收标准

| 项目 | 标准 |
|------|------|
| 首屏加载 | 3G 网络下 ≤3 秒看到已有发言 |
| 实时延迟 | 新发言从写入到页面展示 ≤2 秒 |
| 移动端 | 微信内置浏览器打开无横向滚动 |
| 断线恢复 | 网络中断 30 秒内重连后自动补齐 |
| 链接撤销 | 撤销后 ≤5 秒页面变为失效提示 |
| 并发 | 单讨论支持 ≥20 同时在线查看 |
| 零配置 | 用户无需额外操作，讨论开始即自动可用 |

## 风险提示

1. **端口冲突**：默认 8199，支持 `--web-port` 参数
2. **文件锁**：多进程读写 discussion.json 需加锁
3. **内存泄漏**：SSE 长连接需处理断开清理
4. **微信兼容**：SSE 可能被拦截，需降级为长轮询
5. **token 泄露**：创建时提示"本讨论将生成公开页面"

## 设计交付物

1. CSS 变量表（`theme.css`）
2. 页面状态原型 × 3（等待中/进行中/已结束）
3. 发言卡片组件规范
4. 移动端适配规则
5. 实时更新动效规范
6. 分享交互稿

## 详细讨论记录

完整讨论记录见圆桌讨论系统（ID: rt_36c7dbdd）
