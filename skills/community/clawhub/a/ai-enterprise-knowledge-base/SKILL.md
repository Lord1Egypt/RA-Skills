# AI Enterprise Knowledge Base

5分钟搭建企业内部问答系统。

## 功能特性

✅ 文档上传：支持 PDF/Word/Markdown/Excel
✅ 智能检索：向量搜索 + 语义理解
✅ 权限管理：部门/角色/用户三级权限
✅ 多渠道接入：飞书/企业微信/钉钉/Slack
✅ 知识图谱：自动提取实体关系
✅ 数据分析：问答统计/知识缺口分析

## 快速开始

### 1. 安装 OpenClaw
```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw && npm install
```

### 2. 配置 Skill
```yaml
name: ai-enterprise-knowledge-base
config:
  # 文档存储路径
  storage: ./knowledge-base
  
  # 向量数据库（可选）
  vectorDb: milvus  # or pinecone/weaviate
  
  # LLM 配置
  llm:
    provider: deepseek
    model: deepseek-chat
    
  # 权限配置
  auth:
    enabled: true
    provider: ldap  # or oauth/saml
```

### 3. 启动服务
```bash
openclaw skills install ai-enterprise-knowledge-base
openclaw start
```

## 使用示例

### 上传文档
```bash
curl -X POST http://localhost:3000/api/documents \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@employee-handbook.pdf" \
  -F "department=hr"
```

### 问答
```bash
curl -X POST http://localhost:3000/api/ask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "question=公司的年假政策是什么？"
```

### 飞书集成
```yaml
# config/channels.yaml
- platform: feishu
  app_id: cli_xxx
  app_secret: xxx
  events:
    - message.receive
```

## 定价

| 套餐 | 价格 | 功能 |
|------|------|------|
| 基础版 | ¥99 | 文档上传 + 智能检索 |
| 专业版 | ¥299 | 权限管理 + 多渠道接入 |
| 企业版 | ¥999 | 知识图谱 + 数据分析 + 定制开发 |

## 企业案例

### 某科技公司（500人）
- 知识库文档：5000+
- 月均问答：50000+
- 新员工培训时间：缩短 60%
- 内部工单：减少 40%

### 某电商公司（200人）
- 客服知识库：自动回答 80% 常见问题
- 客服响应时间：从 5 分钟降至 10 秒
- 客户满意度：提升 25%

## 技术支持

- 📧 Email: contact@openclaw-cn.com
- 💬 Telegram: @openclaw_service
- 📱 微信: openclaw-cn

---

**安装配置服务**：¥99 起，30 分钟搞定！