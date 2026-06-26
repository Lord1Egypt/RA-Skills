# 贡献指南

感谢你对AI Company项目的兴趣！

## 如何贡献

### 报告问题
- 在GitHub Issues中报告bug
- 提供详细的复现步骤
- 包含错误日志和环境信息

### 提出新功能
- 在GitHub Discussions中讨论
- 说明功能的使用场景
- 提供实现建议

### 提交代码
1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范
- 遵循PEP 8规范
- 添加文档字符串
- 编写测试用例
- 更新相关文档

### AI员工贡献
你可以贡献新的AI员工：

1. 在`employees/`目录创建新文件
2. 在`prompts/`目录添加提示词模板
3. 更新`config.yaml`配置
4. 提交PR并说明用途

## 开发环境设置

```bash
# 克隆项目
git clone https://github.com/your-username/ai-company.git
cd ai-company

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black .
isort .

# 类型检查
mypy .
```

## 文档贡献

- 改进现有文档的清晰度
- 添加使用示例
- 翻译文档到其他语言
- 修复错别字和错误

## 社区准则

- 尊重所有贡献者
- 建设性的反馈
- 乐于助人
- 开放包容

## 获取帮助

- GitHub Issues: 技术问题
- GitHub Discussions: 一般讨论
- Email: support@ai-company.com

再次感谢你的贡献！
