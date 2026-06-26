# Agent Error Logger - 使用指南

## 🚀 快速开始

### 1. 安装

```bash
# 方法 1: 直接克隆（本地开发）
cd /path/to/your/agent/skills
git clone https://github.com/YOUR_USERNAME/agent-error-logger.git

# 方法 2: 通过 Skill 市场（发布后）
agent-cli skills install agent-error-logger
```

### 2. 配置

编辑配置文件，在 `skills.entries` 中添加：

```json
{
  "skills": {
    "entries": {
      "agent-error-logger": {
        "enabled": true
      }
    }
  }
}
```

### 3. 重启

```bash
sh scripts/restart.sh
```

---

## 📝 记录错误

### 命令行方式

```bash
cd /path/to/agent-error-logger/scripts

python record_error.py \
  --task "发布小红书" \
  --error "图片文件不存在" \
  --cause "用户只提供了 URL，未下载" \
  --fix "发布前先下载 URL 图片" \
  --tags "#文件校验 #图片处理"
```

### 对话方式（推荐）

直接跟 Agent 说：

```
用户：记录一个错误，刚才发布失败了
Agent: 好的，我来记录。请确认以下信息：
- 任务：发布小红书
- 错误：图片文件不存在
- 原因：未提前检查图片
- 修正：发布前验证文件
- 标签：#文件校验

确认记录吗？
用户：确认
Agent: ✓ 错误 #004 已记录
```

---

## 🔍 搜索错误

### 按关键词

```bash
python search_errors.py --keyword "关键词"
python search_errors.py --keyword "发布失败"
python search_errors.py --keyword "网络超时"
```

### 按标签

```bash
python search_errors.py --tag "#文件校验"
python search_errors.py --tag "#网络超时"
python search_errors.py --tag "#浏览器不可用"
```

### 限制结果数

```bash
python search_errors.py --tag "#文件校验" --limit 3
```

---

## 📊 查看模式索引

```bash
cat /home/gem/workspace/agent/workspace/memory/error-patterns.md
```

查看所有错误模式分类和检查清单。

---

## 🔄 主动检查

在以下场景，Agent 会自动检索错误日志：

| 场景 | 自动检查内容 |
|------|-------------|
| 发布内容前 | 检查 #文件校验 #发布前检查 |
| 网络请求前 | 检查 #网络超时 #降级方案 |
| 浏览器操作前 | 检查 #浏览器不可用 |
| 复杂任务前 | 检查相似任务历史 |

### 示例

```
用户：帮我发布这个小红书

Agent: 等一下，我查一下错误日志...
⚠️ 上次发布失败是因为图片文件不存在。

这次请确认：
✓ 图片文件路径：/home/user/pic.jpg (存在)
✓ 文件权限：可读
✓ 视频文件：不需要

确认发布吗？
```

---

## 📈 月度报告

每月初可以生成上月报告：

```bash
# 手动生成（未来功能）
python monthly_report.py --month YYYY-MM
```

报告包含：
- 错误总数
- 错误类型分布
- 高频错误模式
- 改进建议

---

## 💡 最佳实践

### 1. 及时记录

错误发生后立即记录，细节更准确。

```
❌ 错误：发布失败
✅ 错误：图片文件不存在，路径 /tmp/pic.jpg 无此文件
```

### 2. 详细分析

不仅记录现象，还要分析根本原因。

```
❌ 原因：文件不存在
✅ 原因：用户提供了 URL，但脚本未先下载到本地
```

### 3. 标签规范

使用统一标签，便于检索：

- `#文件校验` - 文件/路径问题
- `#网络超时` - 网络请求超时
- `#浏览器不可用` - 浏览器工具失败
- `#权限不足` - API/文件权限问题
- `#参数缺失` - 必需参数未提供

### 4. 定期回顾

每月回顾错误模式：

```bash
# 查看本月所有错误
python search_errors.py --tag "#" --limit 100

# 查看高频模式
cat memory/error-patterns.md
```

### 5. 主动提醒

新任务前主动检索：

```
Agent: 这个任务我之前做过，查一下有没有踩过坑...
```

---

## 🔧 故障排除

### 问题：脚本执行失败

```bash
# 检查 Python 版本
python --version  # 需要 3.10+

# 检查文件权限
chmod +x scripts/*.py

# 检查路径
ls -la /path/to/workspace/memory/
```

### 问题：日志文件不存在

```bash
# 手动创建目录
mkdir -p /path/to/workspace/memory

# 运行一次记录命令会自动创建
python record_error.py --task "测试" --error "测试" --cause "测试" --fix "测试" --tags "#测试"
```

---

## 📚 相关资源

- [Self-Refine 论文](https://arxiv.org/abs/2303.17651)
- [CoVE: Chain of Verification](https://arxiv.org/abs/2309.11495)
- [ClawHub Skill 开发指南](https://clawhub.com/docs)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

GitHub: https://github.com/YOUR_USERNAME/agent-error-logger
