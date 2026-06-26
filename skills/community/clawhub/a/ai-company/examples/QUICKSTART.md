# AI Company 快速开始指南

## 🚀 三步创建你的AI公司

### 第1步：安装依赖

```bash
# 确保你已安装 Python 3.10+
python3 --version

# 安装必要的依赖
pip install anthropic python-dotenv pyyaml requests
```

### 第2步：创建项目

```bash
# 使用初始化脚本创建新项目
cd /path/to/skills/ai-company/examples
python3 init_ai_company.py my-ai-company

# 或者手动创建项目结构
mkdir my-ai-company
cd my-ai-company
mkdir -p employees prompts shared workflows logs
```

### 第3步：配置和运行

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑.env，添加你的API密钥
nano .env  # 或使用你喜欢的编辑器

# 运行示例代码测试
python3 ../examples/simple_ai_employee.py
python3 ../examples/simple_coordinator.py
```

## 📋 项目初始化检查清单

- [ ] Python 3.10+ 已安装
- [ ] 依赖包已安装
- [ ] 项目目录已创建
- [ ] 环境变量已配置
- [ ] 示例代码可以运行
- [ ] 已阅读 SKILL.md 了解功能
- [ ] 已阅读 docs/design.md 了解架构

## 🎯 开始实现

1. **实现第一个AI员工**
   ```bash
   # 复制示例代码
   cp examples/simple_ai_employee.py employees/market_researcher.py

   # 根据需求修改
   nano employees/market_researcher.py
   ```

2. **创建提示词**
   ```bash
   # 创建提示词目录
   mkdir -p prompts/market_researcher/v1.0.md

   # 编辑提示词
   nano prompts/market_researcher/v1.0.md
   ```

3. **定义工作流**
   ```bash
   # 创建工作流文件
   nano workflows/discover_opportunities.yaml
   ```

4. **启动你的AI公司**
   ```bash
   python main.py start
   ```

## 💡 下一步

- 阅读完整的 [SKILL.md](SKILL.md)
- 查看 [设计文档](docs/design.md)
- 参考 [API文档](docs/api.md)
- 运行 [示例代码](examples/)

## 🆘 需要帮助？

- 查看 [FAQ](FAQ.md)
- 阅读 [故障排查指南](docs/TROUBLESHOOTING.md)
- 提交 [GitHub Issue](https://github.com/your-username/ai-company/issues)

---

**祝你的AI公司运营成功！** 🎉
