# agent-roundtable v2 Sprint 3 PRD — 五大功能需求分析

> **版本**: 1.0
> **日期**: 2026-05-26
> **状态**: 草稿
> **产品负责人**: 饼哥
> **前置依赖**: Sprint 1（流式输出 + 协调者观点展示）✅、Sprint 2（发布自动化 + 讨论回放）🔄
> **分支**: feature/v2-ux-improvements

---

## 1. 背景与目标

### 1.1 迭代回顾

| Sprint | 状态 | 核心交付 |
|--------|------|---------|
| Sprint 1 ✅ | 已完成 | 流式输出 + 协调者观点展示 |
| Sprint 2 🔄 | 开发中 | 发布自动化 + 讨论回放 |
| **Sprint 3 ⬜** | **本次规划** | **UI 体验升级 + 安全增强 + 生态扩展** |

Sprint 1-2 解决了"能用"和"能发布"的问题。Sprint 3 聚焦"好看"、"安全"和"能扩展"——从工具走向产品。

### 1.2 目标

Sprint 3 规划 5 个功能，按优先级分三档：

| 优先级 | 功能 | 核心价值 | 来源 |
|--------|------|---------|------|
| **P1** | Agent 人格可视化 | 增强讨论辨识度，让观众一眼区分谁在说话 | 团队共识 |
| **P1** | 响应式布局优化 | 移动端/桌面端体验对齐，补齐 <768px 断点 | 团队共识 |
| **P1** | Web Viewer 隐私增强 | 链接过期 + 访问密码，补齐安全分层 | 码飞技术分析推荐 |
| **P2** | 插件化适配器 | 支持接入不同 Agent 框架，扩展生态 | 团队共识 |
| **P2** | Landing Page | 静态介绍页用于 GitHub/PyPI 引流 | 码飞技术分析推荐 |

### 1.3 非目标（Sprint 3 不做）

- WebSocket 双向交互
- 讨论实时协作编辑
- 多租户 / 多团队管理
- 讨论模板市场
- 完整的 i18n 框架（仅做对外英文优先，详见 Sprint 2 收尾）

---

## 2. 目标用户

| 用户类型 | 场景 | Sprint 3 痛点 |
|---------|------|--------------|
| 内容创作者 | 分享讨论给读者 | 讨论页面无法区分 Agent 身份，像看匿名聊天 |
| 移动端用户 | 手机上查看讨论 | 布局在小屏上体验不佳 |
| 安全敏感用户 | 分享含敏感内容的讨论 | 链接一旦泄露无法控制访问 |
| 框架开发者 | 想用 Roundtable 但非 Hermes 用户 | 只能通过 Hermes Agent 使用，接入门槛高 |
| 潜在用户 | GitHub/PyPI 首次访问 | 没有统一入口了解产品定位 |

---

## 3. 功能需求

### 3.1 P1 — Agent 人格可视化

#### 3.1.1 用户故事

> 作为讨论观众，我希望在 Web Viewer 中看到每个 Agent 的头像、名称和角色描述，这样我能一眼区分不同 Agent 的发言，增强讨论的沉浸感和辨识度。

#### 3.1.2 功能规格

| 编号 | 功能点 | 说明 | 验收标准 |
|------|--------|------|---------|
| F1.1 | Agent 头像展示 | 每个发言卡片左侧展示 Agent 头像（avatar），支持 emoji 或图片 URL | 头像在所有发言卡片中一致展示 |
| F1.2 | Agent 名称 + 角色标签 | 头像旁显示名称和角色标签（如"产品总监"、"设计师"） | 标签颜色与角色对应（复用现有 role 色板） |
| F1.3 | Agent 信息卡片 | 点击头像或名称弹出详情：角色描述、发言统计、观点关键词 | 弹出卡片可关闭，不遮挡讨论流 |
| F1.4 | 讨论参与者面板 | 页面顶部/侧边展示所有参与者列表，含头像、名称、角色 | 讨论开始前即可看到参与者阵容 |
| F1.5 | 协调者视觉强化 | 协调者（Coordinator）的发言卡片保持金色左边框 + 渐变背景（复用 Sprint 1 设计） | 视觉上与其他角色有明显区分 |

#### 3.1.3 数据模型扩展

discussion.json 中 participants 字段扩展：

```json
{
  "participants": [
    {
      "name": "饼哥",
      "role": "product",
      "avatar": "🥧",
      "title": "产品总监",
      "description": "沉稳靠谱，喜欢用数据和逻辑说服人"
    }
  ]
}
```

新增字段：
- `avatar`: string — emoji 或图片 URL，默认根据 role 生成 emoji
- `title`: string — 角色头衔，如"产品总监"
- `description`: string — 角色简述，用于信息卡片

**技术约束**：avatar 默认值由前端根据 role 映射生成，不引入外部头像服务依赖。

#### 3.1.4 边界条件

- Agent 信息不完整时（缺少 avatar/title），前端使用默认值回退
- 讨论中途新增参与者，SSE 推送 participant_updated 事件
- 移动端信息卡片改为底部抽屉，不用弹窗

#### 3.1.5 验收标准

| 项目 | 标准 |
|------|------|
| 头像展示 | 所有发言卡片均显示对应 Agent 头像 |
| 角色辨识 | 不同角色颜色区分明确，WCAG AA 对比度达标 |
| 信息卡片 | 点击可查看详情，关闭后不影响滚动 |
| 移动端 | 头像和名称在小屏上不换行溢出 |
| 性能 | 头像渲染不影响 SSE 新发言的 2 秒内展示 |

#### 3.1.6 工作量评估

- 后端 participants 字段扩展：0.5 天
- 前端发言卡片重构 + 头像/标签：1 天
- 信息卡片 + 参与者面板：1 天
- 移动端适配 + 测试：0.5 天

**总计：3 天**

---

### 3.2 P1 — 响应式布局优化

#### 3.2.1 用户故事

> 作为移动端用户，我希望在手机上打开讨论链接时获得舒适的阅读体验，不用反复缩放和横向滚动，这样我可以随时随地查看讨论内容。

#### 3.2.2 功能规格

| 编号 | 功能点 | 说明 | 验收标准 |
|------|--------|------|---------|
| F2.1 | 断点体系 | 建立标准响应式断点：mobile (<768px)、tablet (768-1024px)、desktop (>1024px) | 三个断点下布局各自适配 |
| F2.2 | 移动端单列布局 | <768px 时讨论流改为单列全宽，发言卡片去掉左右 margin | 无横向滚动条 |
| F2.3 | 移动端导航优化 | 顶部状态栏折叠为紧凑模式，参与者列表改为底部抽屉 | 操作区域单手可达 |
| F2.4 | 触摸交互优化 | 长按发言卡片弹出操作菜单（复制、分享），左滑返回顶部 | 触摸反馈及时，无误触 |
| F2.5 | 字号保障 | 最小正文字号 14px，标题 16px，确保移动端可读性 | 无需缩放即可阅读 |
| F2.6 | 桌面端宽屏利用 | >1024px 时讨论流居中，max-width 限制在 800px，两侧留白 | 宽屏不拉伸阅读宽度 |

#### 3.2.3 技术约束

- 复用现有 Tailwind CSS 框架，通过 responsive 前缀实现断点适配
- 不引入额外 CSS 框架或布局库
- 保持单文件 SPA 架构（index.html 内联所有样式）

#### 3.2.4 边界条件

- 微信内置浏览器兼容：使用 fallback polling 而非 SSE 时布局不变
- 横屏模式：发言卡片保持可读，不出现极端窄列
- iPad mini (768px)：走 tablet 断点，双列布局（发言流 + 参与者面板）

#### 3.2.5 验收标准

| 项目 | 标准 |
|------|------|
| 移动端 | iPhone SE (375px) 无横向滚动，字号 ≥14px |
| 平板端 | iPad (768px) 布局合理利用屏幕宽度 |
| 桌面端 | 1440px+ 宽屏内容居中，不拉伸 |
| 微信兼容 | 微信内置浏览器打开无布局异常 |
| 性能 | 响应式切换无卡顿，动画流畅 |

#### 3.2.6 工作量评估

- 断点体系 + 移动端布局：1 天
- 触摸交互 + 导航优化：0.5 天
- 桌面端宽屏 + 测试：0.5 天

**总计：2 天**

---

### 3.3 P1 — Web Viewer 隐私增强

#### 3.3.1 用户故事

> 作为讨论创作者，我希望能设置链接过期时间和访问密码，这样即使链接被意外传播，我也能控制谁在什么时间内可以访问我的讨论内容。

#### 3.3.2 安全分层模型

Web Viewer 公开链接安全分为三个层级（L1 已在 Sprint 1 完成）：

| 层级 | 功能 | Sprint | 状态 |
|------|------|--------|------|
| L1 | 链接撤销（Revoke） | Sprint 1 | ✅ 已完成 |
| **L2** | **链接过期（Expires）** | **Sprint 3** | **⬜ 本次开发** |
| **L3** | **访问密码（Password）** | **Sprint 3** | **⬜ 本次开发** |

#### 3.3.3 功能规格

| 编号 | 功能点 | 说明 | 验收标准 |
|------|--------|------|---------|
| F3.1 | 链接过期时间设置 | 创作者可设置链接过期时间（1h/24h/7d/30d/自定义） | 设置后 discussion.json 写入 expires_at |
| F3.2 | 过期状态页 | 过期后访问者看到"链接已过期"提示页，含过期时间 | 页面清晰告知过期原因，不显示讨论内容 |
| F3.3 | 访问密码设置 | 创作者可为讨论设置访问密码（4-32 字符） | 密码使用 PBKDF2 哈希存储，不存明文 |
| F3.4 | 密码输入页 | 需要密码时，访问者看到密码输入页 | 输入正确后可正常查看讨论，错误时提示"密码不正确" |
| F3.5 | 密码认证持久化 | 认证通过后设置 HttpOnly cookie，同会话免重复输入 | cookie 有效期与链接过期时间一致 |
| F3.6 | SSE 状态同步 | 已连接的 SSE 客户端在链接过期/撤销后收到 access_changed 事件 | 收到事件后 ≤5 秒页面切换到对应状态页 |
| F3.7 | CLI 参数支持 | `roundtable publish --expires 24h --password mypass` | 命令行可直接设置过期和密码 |

#### 3.3.4 数据模型变更

discussion.json 引入 schema_version + share 安全字段：

```json
{
  "schema_version": 2,
  "share": {
    "token": "abc123",
    "revoked_tokens": [],
    "expires_at": 1770000000,
    "password_required": true,
    "password_hash": "...",
    "password_salt": "...",
    "auth_version": 1
  }
}
```

**兼容策略**：
- 旧文件无 schema_version 时视为 v1，自动兼容
- v1 的 token/revoked_tokens 顶层字段继续支持
- 写入时升级为 v2 结构，但不破坏旧客户端读取

#### 3.3.5 API 变更

| 端点 | 变更 | 说明 |
|------|------|------|
| GET /api/:token/data | 增加鉴权 | 未过期且无需密码→正常返回；已过期→410 + `{"error":"expired"}`；需密码且未认证→401 + `{"error":"password_required"}` |
| GET /api/:token/events | 增加鉴权 | SSE 建连前执行鉴权；状态变更为 expired/revoked 时推送 access_changed 事件后断开 |
| GET /api/:token/poll | 增加鉴权 | 长轮询同步鉴权规则 |
| POST /api/:token/auth | **新增** | body: `{password: string}`，成功返回 `{success: true}`，失败 401 |
| POST /api/:token/revoke | 权限收紧 | 仅允许本机/owner_secret 操作，防止"访问者撤销创作者链接"的权限漏洞 |

**WebPublisher 新增参数**：

```python
class WebPublisher:
    def start(..., expires_at: int | None = None, password: str | None = None)
    def set_expiration(expires_at: int | None)
    def set_password(password: str | None)
```

#### 3.3.6 技术约束

- 密码哈希使用 Node crypto.pbkdf2Sync（Node 侧）或 Python hashlib.pbkdf2_hmac（Python 侧），不引入 bcrypt/argon2 依赖
- 鉴权逻辑统一在 server.mjs 的 `authorizeRequest(req, token)` 中间层，data/events/poll 共用
- 前端根据 error code 渲染明确状态页（expired / password_required / revoked），不混用通用 error

#### 3.3.7 边界条件

- 无密码无过期的讨论：行为与当前完全一致，零影响
- 同时设置过期和密码：过期优先判断，密码次之
- 密码 cookie 在 localhost / 0.0.0.0 / 公网域名下 SameSite/Secure 策略需分别测试
- 旧 discussion.json 写入 expires_at 时自动升级 schema_version 为 2

#### 3.3.8 验收标准

| 项目 | 标准 |
|------|------|
| 过期生效 | expires_at 到期后 data/events/poll 均返回 410 |
| 密码校验 | 错误密码返回 401，正确密码后可正常访问 |
| 持久化 | 认证后同会话免重复输入密码 |
| SSE 同步 | 过期/撤销后已连接客户端 ≤5 秒收到 access_changed |
| 旧文件兼容 | Sprint 1 产生的 discussion.json 仍可正常打开 |
| 权限收紧 | 非本机/非 owner 无法执行 revoke |

#### 3.3.9 工作量评估

- 后端 schema v2 + WebPublisher：0.5 天
- server.mjs 统一鉴权 + auth cookie/session：1 天
- 前端状态 UI（expired/password/revoked）：0.5-1 天
- 测试 + 旧文件兼容：0.5 天

**总计：2.5-3 天**

---

### 3.4 P2 — 插件化适配器

#### 3.4.1 用户故事

> 作为非 Hermes 框架的 Agent 开发者，我希望通过简单的适配器接口将我的 Agent 接入 Roundtable 圆桌讨论，而不需要重写整个框架，这样我的 Agent 也能参与多智能体协作讨论。

#### 3.4.2 功能规格

| 编号 | 功能点 | 说明 | 验收标准 |
|------|--------|------|---------|
| F4.1 | 适配器接口定义 | 定义 `RoundtableAdapter` 抽象基类，包含 `speak()`、`listen()`、`get_persona()` 三个核心方法 | 接口文档清晰，Type hints 完整 |
| F4.2 | 内置 Hermes 适配器 | 将现有 Hermes Agent 集成逻辑封装为 `HermesAdapter`，作为默认适配器 | 行为与当前完全一致 |
| F4.3 | 适配器注册机制 | 通过 `roundtable.register_adapter(name, adapter_class)` 注册自定义适配器 | 注册后可通过 `--adapter name` 参数选择 |
| F4.4 | 参考实现 | 提供一个最小化的 `SimpleAdapter` 参考实现（基于纯函数，无框架依赖） | 10 行代码即可接入一个新 Agent |
| F4.5 | 适配器文档 | 编写 ADAPTER.md 接口规范文档，含接口定义、生命周期、示例代码 | 新开发者 10 分钟内理解如何接入 |

#### 3.4.3 接口设计

```python
from abc import ABC, abstractmethod

class RoundtableAdapter(ABC):
    """圆桌讨论适配器基类"""

    @abstractmethod
    def get_persona(self) -> dict:
        """返回 Agent 人格信息: name, role, avatar, title, description"""
        ...

    @abstractmethod
    async def speak(self, context: dict) -> str:
        """根据讨论上下文生成发言

        Args:
            context: {
                "history": [...],       # 历史发言
                "topic": str,           # 讨论主题
                "round": int,           # 当前轮次
                "findings": [...],      # 已发现的观点
            }
        Returns:
            发言内容（Markdown 格式）
        """
        ...

    @abstractmethod
    async def listen(self, speech: dict) -> dict | None:
        """听取他人发言，可选返回元数据

        Args:
            speech: {"speaker": str, "content": str, "round": int}
        Returns:
            None（无特殊反应）或 {"reaction": "agree|disagree|question", "note": str}
        """
        ...
```

#### 3.4.4 技术约束

- 适配器接口必须是纯 Python ABC，不引入外部框架依赖
- `speak()` 支持 async，适配不同 Agent 框架的异步特性
- 适配器生命周期由 RoundtableCore 管理，不由适配器自行控制
- 不引入插件发现机制（如 entry_points），保持显式注册

#### 3.4.5 边界条件

- 适配器抛异常时，讨论继续但该 Agent 标记为 error 状态，跳过本轮发言
- 适配器超时（默认 60s）自动跳过，不阻塞讨论进程
- 同一讨论中可混合使用不同适配器（Hermes + 自定义）

#### 3.4.6 验收标准

| 项目 | 标准 |
|------|------|
| 接口完整 | RoundtableAdapter ABC 定义清晰，type hints 覆盖所有方法 |
| 默认兼容 | 不指定 adapter 时行为与当前完全一致 |
| 参考实现 | SimpleAdapter 可独立运行，无需 Hermes 依赖 |
| 文档 | ADAPTER.md 含接口、示例、生命周期说明 |
| 错误处理 | 适配器异常不影响讨论进程 |

#### 3.4.7 工作量评估

- RoundtableAdapter ABC 定义 + HermesAdapter 封装：1 天
- 注册机制 + CLI 参数：0.5 天
- SimpleAdapter 参考实现 + ADAPTER.md：0.5 天
- 测试 + 错误处理：0.5 天

**总计：2.5 天**

---

### 3.5 P2 — Landing Page

#### 3.5.1 用户故事

> 作为首次访问者，我从 GitHub 或 PyPI 点进来时，希望在 10 秒内理解 Roundtable 是什么、解决什么问题，然后 30 秒内找到安装和试用方式，这样我能快速判断是否值得深入。

#### 3.5.2 功能规格

| 编号 | 功能点 | 说明 | 验收标准 |
|------|--------|------|---------|
| F5.1 | 首屏 Hero | 展示产品名称、定位语（"多 Agent 圆桌讨论引擎"）、核心 CTA（pip install + GitHub） | 10 秒内理解产品定位 |
| F5.2 | 特性展示 | 3-4 个核心特性卡片：流式输出、多人协作、Web Viewer、插件化 | 每个特性配图标和一句话说明 |
| F5.3 | 快速开始 | 代码示例展示 3 步上手：install → configure → run | 代码可复制，30 秒内跑通 |
| F5.4 | 渠道链接 | GitHub / PyPI / Docs / Hermes Skill Hub / OpenClaw | 未上线渠道显示 "Coming soon"，不空链接 |
| F5.5 | SEO/OG 配置 | title、description、og:image、twitter:card | 社交分享时显示品牌预览卡 |
| F5.6 | 响应式 | 375px 移动端无横向滚动 | 手机上可正常浏览 |

#### 3.5.3 技术方案

- 纯静态 HTML/CSS/少量 JS，零后端依赖
- 目录结构：`site/index.html` + `site/assets/*`
- 可部署到 GitHub Pages 或 Vercel
- 不依赖 docs/product、docs/design 等内部目录

#### 3.5.4 渠道状态配置

```javascript
const CHANNELS = {
  github:    { url: "https://github.com/MoyuFamily/agent-roundtable", status: "live" },
  pypi:      { url: "https://pypi.org/project/agent-roundtable/", status: "live" },
  docs:      { url: "/docs", status: "planned", label: "Coming soon" },
  hermes:    { url: "#", status: "planned", label: "Coming soon" },
  openclaw:  { url: "#", status: "planned", label: "Coming soon" },
};
```

#### 3.5.5 边界条件

- JS 失败时核心内容仍可读（渐进增强）
- 未上线渠道的 Coming soon 标签不可点击跳转到空页面
- OG 图片尺寸 1200x630，适配 Twitter/微信/飞书预览

#### 3.5.6 验收标准

| 项目 | 标准 |
|------|------|
| 首屏理解 | 新用户 10 秒内理解"这是什么" |
| 行动路径 | 30 秒内找到 pip install 命令 |
| 移动端 | 375px 无横向滚动 |
| SEO | title/description/og 完整 |
| 渠道 | 未上线渠道显示 Coming soon，无空链接 |
| 无 JS | 核心内容仍可阅读 |

#### 3.5.7 工作量评估

- 静态页面首版：0.5-1 天
- SEO/OG/响应式细节：0.5 天
- 部署预览 + 链接校验：0.5 天

**总计：1.5-2 天**

---

## 4. 依赖关系与执行顺序

```
功能1 Agent人格可视化 ──┐
                       ├── 可并行 ──→ 功能5 Landing Page（独立）
功能2 响应式布局优化 ──┘
        │
        ▼
功能3 隐私增强（依赖 schema v2，需先于功能4）
        │
        ▼
功能4 插件化适配器（依赖功能3 的 discussion.json v2）
```

**推荐执行顺序**：

| 阶段 | 功能 | 天数 | 说明 |
|------|------|------|------|
| 阶段一 | 功能1（人格可视化）+ 功能2（响应式） | 3-4 天 | UI 层并行开发，互不阻塞 |
| 阶段二 | 功能3（隐私增强） | 2.5-3 天 | 依赖 schema v2，需阶段一的 index.html 稳定 |
| 阶段三 | 功能4（插件化适配器） | 2.5 天 | 依赖功能3 的 discussion.json v2 结构 |
| 可并行 | 功能5（Landing Page） | 1.5-2 天 | 独立静态页，随时可做 |

**总工时估算：11.5-14 天（约 2.5-3 周）**

---

## 5. 技术约束汇总

| 约束 | 说明 |
|------|------|
| 零重依赖 | 不引入 bcrypt、argon2、Express 以外的 Web 框架、i18n 库等重依赖 |
| 单文件 SPA | index.html 保持内联 CSS/JS 架构，不拆分构建流程 |
| 向后兼容 | 旧 discussion.json 必须可正常读取，schema v2 自动升级 |
| 现有分支 | 所有开发在 feature/v2-ux-improvements 分支进行 |
| Python 3.10+ | 核心代码保持 Python 3.10+ 兼容 |
| PM2 依赖 | Web 服务仍通过 PM2 管理，不引入新的进程管理方案 |

---

## 6. 风险清单

| 风险 | 等级 | 影响 | 缓解措施 |
|------|------|------|---------|
| SSE 鉴权逻辑分叉 | 高 | 过期/密码状态不一致 | 抽 authorizeRequest 单函数复用 |
| revoke 权限过宽 | 高 | 访问者可撤销创作者链接 | 增加 owner_secret 限制 |
| 旧文件兼容性 | 中 | schema v2 破坏旧客户端 | 引入 migration reader + 兼容测试 |
| 微信浏览器兼容 | 中 | 密码 cookie 行为不一致 | 逐域名测试 SameSite 策略 |
| 适配器异常传播 | 中 | 一个适配器崩溃影响讨论 | 超时 + try/except 隔离 |
| Landing Page 渠道状态 | 低 | 空链接影响品牌 | Coming soon + 集中配置 |

---

*文档结束。饼哥 2026-05-26*

