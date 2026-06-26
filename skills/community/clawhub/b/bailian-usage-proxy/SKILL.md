---
name: bailian-usage-proxy
description: 阿里百炼大模型平台的多人共享账号用量统计代理服务。用于解决公司共用阿里百炼账号时无法区分个人用量的问题。当用户需要：1) 部署阿里百炼用量统计代理，2) 统计多人Token用量和调用次数，3) 管理大模型API调用配额时激活此技能。
---

# 阿里百炼用量统计代理

为阿里百炼（阿里云大模型服务平台）提供多人共享账号场景下的精细化用量统计方案。

## 核心能力

- **API代理转发**：兼容 OpenAI 格式，透明转发到阿里百炼
- **用量实时统计**：按用户、模型、时间维度记录 Token 消耗
- **配额管理**：支持日限额、限流控制
- **管理后台**：用量查询、报表导出

## 使用场景

1. 公司统一申请阿里百炼账号，需要统计每个员工的用量
2. 需要按项目/部门分摊大模型调用成本
3. 需要限制单个用户的日调用配额

## 快速部署

### 1. 环境准备

```bash
# 克隆或复制本项目
cd bailian-proxy

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入阿里百炼主账号 Key 和数据库配置
```

### 2. 数据库初始化

```bash
python scripts/init_db.py
```

### 3. 启动服务

```bash
# 开发模式
python -m app.main

# 生产模式（Docker）
docker-compose up -d
```

### 4. 创建用户

```bash
python scripts/create_user.py --name "张三" --department "算法部" --daily-limit 1000000
```

## 客户端使用

同事只需修改两处配置：

```python
# 原配置
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
api_key = "sk-xxx"  # 阿里百炼的key

# 新配置
base_url = "http://your-proxy-server:8080/v1"
api_key = "internal-key-xxx"  # 代理系统分配的key
```

## 查看用量

### 命令行

```bash
# 今日用量
python scripts/usage_report.py --today

# 指定用户
python scripts/usage_report.py --user-key xxx --start 2026-03-01 --end 2026-03-08

# 导出CSV
python scripts/usage_report.py --export usage.csv
```

### 管理后台

访问 `http://proxy-server:8081` 查看：
- 实时用量仪表盘
- 用户用量排行
- 模型调用分布
- 历史趋势图表

## 技术架构

详见 [references/architecture.md](references/architecture.md)

## API 文档

详见 [references/api.md](references/api.md)

## 数据库结构

详见 [references/database.md](references/database.md)
