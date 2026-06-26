---
name: dev-productivity-bundle
version: 1.0.0
description: |
  开发者效率套装 - 程序员的AI副驾驶，让开发效率翻倍。整合代码审查、Bug追踪、文档生成、部署监控四大能力。自动化Code Review + 智能化Bug管理。定价¥149/套。
---

# 开发者效率套装 (Developer Productivity Bundle)

> 程序员的AI副驾驶，让开发效率翻倍

## 💼 套装定位

专为软件开发者、技术团队和技术负责人打造，整合代码审查、Bug追踪、文档生成和部署监控四大核心能力，打造AI驱动的开发工作流。

---

## 🎯 包含技能

### 1. 代码审查 (ai-refactoring-assistant / coding-agent)
- **功能**：代码质量分析、重构建议、最佳实践检查
- **适用场景**：PR审查、代码优化、技术债务清理
- **价值**：自动化Code Review，提升代码质量

### 2. Bug追踪 (gh-issues / api-dev)
- **功能**：Issue管理、Bug自动分类、修复建议
- **适用场景**：Bug管理、任务分配、进度追踪
- **价值**：智能化Bug管理

### 3. 文档生成 (academic-writing-refiner / feishu-doc / notion)
- **功能**：代码注释生成、API文档、技术文档
- **适用场景**：项目文档、API文档、README生成
- **价值**：自动化文档维护

### 4. 部署监控 (healthcheck / cron / browser-automation)
- **功能**：服务监控、健康检查、异常告警
- **适用场景**：生产环境监控、CI/CD集成
- **价值**：7x24小时运维保障

---

## 📦 套装内容

```
dev-productivity-bundle/
├── SKILL.md                      # 本文件 - 套装总览
├── config/
│   ├── code-review.yaml          # 代码审查配置
│   ├── bug-tracker.yaml          # Bug追踪配置
│   ├── doc-generator.yaml        # 文档生成配置
│   └── deploy-monitor.yaml       # 部署监控配置
├── examples/
│   ├── code-review-flow.md       # 代码审查流程
│   ├── bug-fix-workflow.md       # Bug修复工作流
│   └── ci-cd-integration.md      # CI/CD集成示例
└── README.md                     # 快速上手指南
```

---

## 🚀 快速开始

### 第一步：安装技能

```powershell
# 代码审查
py -m clawhub install ai-refactoring-assistant
py -m clawhub install coding-agent

# Bug追踪
py -m clawhub install gh-issues
py -m clawhub install api-dev

# 文档生成
py -m clawhub install academic-writing-refiner
py -m clawhub install feishu-doc

# 部署监控
py -m clawhub install healthcheck
py -m clawhub install cron
```

### 第二步：配置GitHub集成

编辑 `config/code-review.yaml`：

```yaml
github:
  token: "${GITHUB_TOKEN}"
  webhook_secret: "${GITHUB_WEBHOOK_SECRET}"
  
repositories:
  - owner: "your-org"
    repo: "your-project"
    code_review:
      enabled: true
      on_pull_request: true
      on_push: false
      rules:
        - "code-quality"
        - "security-check"
        - "performance"
    
    bug_tracker:
      enabled: true
      auto_label: true
      auto_assign: true
    
    doc_generator:
      enabled: true
      generate_on_release: true
      output_format: "markdown"
```

---

## 💡 典型使用场景

### 场景1：自动化代码审查

```
用户：审查这个PR

开发助手：
🔍 PR审查报告 #123

━━━━━━━━━━━━━━━━━━━━━
📊 概览
━━━━━━━━━━━━━━━━━━━━━

PR：修复用户登录问题
作者：@developer
变更：+156/-42 行
文件：5个

━━━━━━━━━━━━━━━━━━━━━
✅ 通过检查（4/5）
━━━━━━━━━━━━━━━━━━━━━

✓ 代码风格检查
✓ 安全漏洞扫描
✓ 单元测试覆盖
✓ 依赖检查

━━━━━━━━━━━━━━━━━━━━━
⚠️ 建议改进（3项）
━━━━━━━━━━━━━━━━━━━━━

1. 性能优化建议
   📄 auth/service.py:45
   问题：数据库查询在循环中执行
   建议：使用批量查询优化
   
   ```python
   # 当前代码
   for user_id in user_ids:
       user = db.query(User).get(user_id)
   
   # 建议优化
   users = db.query(User).filter(User.id.in_(user_ids)).all()
   ```

2. 错误处理
   📄 auth/service.py:78
   问题：异常处理过于宽泛
   建议：细化异常类型
   
   ```python
   # 建议
   try:
       user = authenticate(credentials)
   except InvalidCredentialsError:
       raise AuthenticationError("Invalid credentials")
   except UserNotFoundError:
       raise AuthenticationError("User not found")
   ```

3. 文档注释
   📄 auth/models.py:12
   问题：缺少函数文档
   建议：添加docstring

━━━━━━━━━━━━━━━━━━━━━
🎯 总体评价
━━━━━━━━━━━━━━━━━━━━━

代码质量：B+（良好）
建议：修复性能问题后合并

需要我生成修复建议的代码吗？
```

### 场景2：智能Bug管理

```
用户：分析最近的Bug情况

开发助手：
📊 Bug分析报告（本周）

━━━━━━━━━━━━━━━━━━━━━
📈 数据概览
━━━━━━━━━━━━━━━━━━━━━

新建Bug：23个
已解决：19个
待处理：4个
平均解决时间：1.5天 ⬇️（上周2.3天）

━━━━━━━━━━━━━━━━━━━━━
🎯 Bug分类
━━━━━━━━━━━━━━━━━━━━━

🔴 严重（3个）
   • #234 - 支付接口超时
   • #235 - 数据库连接池耗尽
   • #236 - 用户数据丢失

🟡 中等（12个）
   • UI显示问题（5个）
   • 性能问题（4个）
   • 兼容性问题（3个）

🟢 轻微（8个）
   • 文案问题（4个）
   • 样式微调（4个）

━━━━━━━━━━━━━━━━━━━━━
🔍 趋势分析
━━━━━━━━━━━━━━━━━━━━━

高频问题：
• 支付相关问题 ↑ 40%
• 移动端适配 ↑ 25%

建议：
• 加强支付模块测试
• 增加移动端自动化测试

━━━━━━━━━━━━━━━━━━━━━
👥 团队负载
━━━━━━━━━━━━━━━━━━━━━

@张三：处理中 2个（负载正常）
@李四：处理中 5个 ⚠️（负载较高）
@王五：处理中 1个（可分配更多）

建议：将2个中等优先级Bug分配给@王五

需要我自动分配Bug吗？
```

### 场景3：文档自动生成

```
用户：为这个项目生成API文档

开发助手：
✅ 已生成API文档

━━━━━━━━━━━━━━━━━━━━━
📄 文档概览
━━━━━━━━━━━━━━━━━━━━━

项目：User Service API
版本：v2.1.0
端点：15个
生成时间：2026-03-21 14:30

━━━━━━━━━━━━━━━━━━━━━
🔑 认证
━━━━━━━━━━━━━━━━━━━━━

所有API请求需要在Header中包含：
```
Authorization: Bearer {access_token}
```

━━━━━━━━━━━━━━━━━━━━━
📚 API端点
━━━━━━━━━━━━━━━━━━━━━

### 用户管理

#### POST /api/v2/users
创建新用户

**请求参数：**
```json
{
  "username": "string",     // 用户名，必填，3-20字符
  "email": "string",        // 邮箱，必填，需符合邮箱格式
  "password": "string",     // 密码，必填，8-32字符
  "role": "string"          // 角色，可选，默认"user"
}
```

**响应示例：**
```json
{
  "id": "usr_123456",
  "username": "john_doe",
  "email": "john@example.com",
  "role": "user",
  "created_at": "2026-03-21T14:30:00Z"
}
```

**错误码：**
- 400：请求参数错误
- 409：用户名或邮箱已存在
- 500：服务器内部错误

#### GET /api/v2/users/{id}
获取用户信息

...（完整文档）

━━━━━━━━━━━━━━━━━━━━━
📦 交付文件
━━━━━━━━━━━━━━━━━━━━━

• api-documentation.md（完整文档）
• openapi.yaml（OpenAPI规范）
• postman-collection.json（Postman集合）

文档已保存至：./docs/api/
需要我发布到文档站点吗？
```

### 场景4：部署监控告警

```
用户：查看服务状态

开发助手：
📊 服务健康状态

━━━━━━━━━━━━━━━━━━━━━
🟢 整体状态：健康
━━━━━━━━━━━━━━━━━━━━━

检查时间：2026-03-21 14:35
监控服务：8个
在线服务：8个
可用性：99.95%

━━━━━━━━━━━━━━━━━━━━━
📈 服务详情
━━━━━━━━━━━━━━━━━━━━━

🟢 user-service
   状态：运行中
   响应时间：45ms ⬇️（平均50ms）
   错误率：0.01%
   最后部署：2小时前

🟢 payment-service
   状态：运行中
   响应时间：120ms ⬆️（平均100ms）
   错误率：0.05%
   最后部署：5小时前
   ⚠️ 响应时间略高于平均

🟢 notification-service
   状态：运行中
   响应时间：35ms
   错误率：0.00%
   队列长度：12（正常）

━━━━━━━━━━━━━━━━━━━━━
📊 资源使用
━━━━━━━━━━━━━━━━━━━━━

CPU使用率：42%（正常）
内存使用率：68%（正常）
磁盘使用率：45%（正常）
网络IO：正常

━━━━━━━━━━━━━━━━━━━━━
🔔 最近告警
━━━━━━━━━━━━━━━━━━━━━

过去24小时：
• 14:20 - payment-service响应时间超过阈值（已恢复）
• 08:15 - 数据库连接数接近上限（已处理）

━━━━━━━━━━━━━━━━━━━━━
💡 建议
━━━━━━━━━━━━━━━━━━━━━

• payment-service响应时间有上升趋势，建议关注
• 考虑在高峰时段扩容

需要查看详细监控数据吗？
```

---

## ⚙️ 配置模板

### 代码审查配置

```yaml
# config/code-review.yaml
code_review:
  enabled: true
  
rules:
  code_quality:
    enabled: true
    checks:
      - "complexity"           # 复杂度检查
      - "duplicate"            # 重复代码
      - "naming"               # 命名规范
      - "documentation"        # 文档注释
    
  security:
    enabled: true
    checks:
      - "sql-injection"        # SQL注入
      - "xss"                  # XSS攻击
      - "hardcoded-secrets"    # 硬编码密钥
      - "dependency-vuln"      # 依赖漏洞
    
  performance:
    enabled: true
    checks:
      - "n+1-queries"          # N+1查询
      - "memory-leak"          # 内存泄漏
      - "inefficient-loop"     # 低效循环
      - "unused-imports"       # 未使用导入
  
notification:
  on_failure: true
  on_warning: true
  channels:
    - "github-pr-comment"
    - "slack"
```

### 部署监控配置

```yaml
# config/deploy-monitor.yaml
monitoring:
  interval: 60  # 秒
  
services:
  - name: "user-service"
    url: "https://api.example.com/health"
    check_type: "http"
