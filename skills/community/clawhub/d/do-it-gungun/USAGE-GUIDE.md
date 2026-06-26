# 🌪️ do-it - 完整使用指南

**Slogan：** 你只管 do it，判断交给滚滚

**版本：** v0.2  
**更新日期：** 2026-03-15

---

## 📖 目录

1. [快速开始](#快速开始)
2. [功能介绍](#功能介绍)
3. [API 服务](#api 服务)
4. [数据管理](#数据管理)
5. [部署指南](#部署指南)
6. [常见问题](#常见问题)

---

## 🚀 快速开始

### 方式 1：仅使用 Web 界面 (最简单)

```bash
# 直接打开网页
open /home/admin/.openclaw/workspace/skills/do-it/web/index.html
```

**说明：** 这种方式会使用模拟数据，适合快速体验界面。

---

### 方式 2：Web + API 完整功能

```bash
# 步骤 1：启动 API 服务
cd /home/admin/.openclaw/workspace/skills/do-it
python3 scripts/api_server.py 5001

# 步骤 2：打开 Web 界面
open web/index.html
# 或在浏览器访问：http://localhost:8080 (如果用了 python -m http.server)
```

**说明：** 这种方式会使用真实数据分析和 AI 判断。

---

## ✨ 功能介绍

### 核心功能

| 功能 | 说明 | 状态 |
|------|------|------|
| 问题输入 | 填写你的纠结问题 | ✅ |
| AI 判断 | 滚滚基于数据分析给出建议 | ✅ |
| 结果展示 | 详细的分析理由和执行建议 | ✅ |
| 用户反馈 | 对判断结果评分 | ✅ |
| 历史记录 | 保存你的所有判断记录 | ✅ |
| 案例库 | 查看他人的真实案例 | 🚧 |

### 支持的问题类型

- ✅ **职业选择** - 跳槽、转行、城市选择
- ✅ **薪资谈判** - offer 选择、谈薪策略
- 🚧 **感情问题** - 恋爱、婚姻、分手
- 🚧 **投资决策** - 理财、创业、副业
- 🚧 **生活选择** - 买房、教育、养老

---

## 🔌 API 服务

### 启动 API

```bash
cd /home/admin/.openclaw/workspace/skills/do-it
python3 scripts/api_server.py 5001
```

**访问：** http://localhost:5001

---

### API 端点

#### 1. 健康检查
```bash
curl http://localhost:5001/api/v1/health
```

**响应：**
```json
{
  "status": "ok",
  "timestamp": "2026-03-15T11:59:17"
}
```

---

#### 2. 提交问题分析
```bash
curl -X POST http://localhost:5001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "title": "38 岁财务 BP，长沙 10K vs 惠州 25K",
    "type": "职业选择",
    "status": "在长沙工作，10K/月",
    "options": "A. 留长沙 B. 去惠州",
    "concerns": "3 年变动频繁，年龄大"
  }'
```

**响应：**
```json
{
  "status": "success",
  "problem_id": "prob_20260315115917",
  "analysis": {
    "recommendation": "去惠州 (骑驴找马策略)",
    "reasoning": [
      "惠州薪资明显高于长沙",
      "可以作为跳板，积累 1-2 年经验",
      "同时看深圳机会，有合适的就跳",
      "设定退出机制，不长期绑定"
    ],
    "action_plan": [...],
    "risk_warning": [...]
  },
  "html": "..."
}
```

---

#### 3. 获取案例列表
```bash
curl http://localhost:5001/api/v1/cases
```

---

### 测试 API

```bash
cd /home/admin/.openclaw/workspace/skills/do-it
python3 scripts/test_api.py
```

---

## 📊 数据管理

### 数据文件位置

```
do-it/data/
├── salary/
│   └── finance_bp_salary.json    # 薪资数据
├── city/
│   └── city_comparison.json      # 城市数据
├── cases/
│   ├── case_records.json         # 手动案例
│   └── web_cases.json            # 网络案例
└── DATA-SUMMARY.json             # 数据摘要
```

---

### 更新数据

```bash
# 一键抓取最新数据
cd /home/admin/.openclaw/workspace/skills/do-it
python3 scripts/crawl_all.py
```

**更新频率建议：**
- 薪资数据：每周
- 城市数据：每月
- 案例数据：每日

---

### 查看数据摘要

```bash
cat data/DATA-SUMMARY.json | jq
```

---

## 🌐 部署指南

### 本地部署 (开发测试)

```bash
# 1. 启动 API
python3 scripts/api_server.py 5001 &

# 2. 启动 Web 服务器
cd web
python3 -m http.server 8080

# 3. 访问 http://localhost:8080
```

---

### Vercel 部署 (免费生产环境)

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 部署
cd web
vercel

# 3. 按提示操作
#    - 选择个人账号
#    - 使用默认配置
#    - 获得免费 HTTPS 链接
```

**注意：** Vercel 部署需要修改 API 调用地址为生产环境地址。

---

### 阿里云部署

```bash
# 1. 购买 ECS 服务器
# 2. 安装 Python 3.6+
# 3. 上传代码
scp -r do-it/ user@your-server:/opt/

# 4. 启动服务
cd /opt/do-it
python3 scripts/api_server.py 5001 &

# 5. 配置 Nginx 反向代理
```

---

## ❓ 常见问题

### Q1: API 服务启动失败？

**A:** 检查端口是否被占用：
```bash
lsof -i:5001
# 如果占用，换个端口
python3 scripts/api_server.py 5002
```

---

### Q2: Web 页面打不开？

**A:** 直接用浏览器打开文件：
```
file:///home/admin/.openclaw/workspace/skills/do-it/web/index.html
```

---

### Q3: 判断结果是模拟的？

**A:** 需要启动 API 服务才能使用真实判断：
```bash
python3 scripts/api_server.py 5001
```

---

### Q4: 历史记录在哪里？

**A:** 存储在浏览器 LocalStorage，点击页面底部"历史记录"链接查看。

---

### Q5: 如何清空历史记录？

**A:** 
- 方式 1：在历史记录页面点击"清空所有记录"
- 方式 2：浏览器控制台执行 `localStorage.removeItem('doit_history')`

---

### Q6: 数据如何更新？

**A:** 运行抓取脚本：
```bash
python3 scripts/crawl_all.py
```

---

## 📞 技术支持

**问题反馈：**
- GitHub Issues (待设置)
- 邮件：support@do-it.ai (待设置)

**文档：**
- [产品设计](PRODUCT-DESIGN.md)
- [产品计划](PRODUCT-PLAN.md)
- [数据说明](data/README.md)
- [部署状态](DEPLOYMENT-STATUS.md)

---

## 🎯 路线图

### v0.1 (已完成) ✅
- [x] Web MVP
- [x] API 服务
- [x] 数据积累
- [x] 历史记录

### v0.2 (进行中) 🚧
- [ ] 案例库页面
- [ ] 数据可视化
- [ ] 分享功能

### v1.0 (计划中) 📋
- [ ] 用户系统
- [ ] 付费功能
- [ ] 小程序版本
- [ ] 部署上线

---

## 💚 滚滚的话

**感谢你使用 do-it！**

**每个纠结都值得被认真对待，**
**每个选择都应该有数据支撑。**

**你只管 do it，**
**判断交给滚滚！** 🌪️✨

---

**创建人：** 滚滚 & 地球人  
**创建时间：** 2026-03-15  
**最后更新：** 2026-03-15 11:59  
**状态：** 🚀 开放使用
