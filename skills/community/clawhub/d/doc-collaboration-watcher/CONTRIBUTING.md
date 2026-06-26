# 贡献指南

**欢迎一起优化 Doc-Collaboration-Watcher！** 🎉

---

## 🤝 如何贡献

### 1. 报告问题 🐛

发现 Bug？功能有问题？配置不清楚？

**请提交 Issue**：
1. 访问 https://github.com/lewistouchtech/doc-collaboration-watcher/issues
2. 点击 "New Issue"
3. 选择问题类型（Bug/功能建议/文档改进）
4. 填写详细信息：
   - 问题描述
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息（OpenClaw 版本、系统版本）
   - 错误日志（如有）

**我们会**：
- ✅ 24 小时内响应
- ✅ 确认问题后标记 Bug
- ✅ 安排修复优先级
- ✅ 修复后关闭并通知

---

### 2. 功能建议 💡

有新想法？想要新功能？使用场景特殊？

**请发起 Discussion**：
1. 访问 https://github.com/lewistouchtech/doc-collaboration-watcher/discussions
2. 点击 "New Discussion"
3. 选择 "Ideas" 分类
4. 描述你的想法：
   - 使用场景
   - 期望功能
   - 实现思路（可选）
   - 替代方案（如有）

**我们会**：
- ✅ 评估可行性
- ✅ 社区投票决定优先级
- ✅ 高票功能优先实现
- ✅ 实现后@提议者

---

### 3. 提交代码 🔧

会写代码？想直接贡献？欢迎 PR！

**提交流程**：
```bash
# 1. Fork 仓库
https://github.com/lewistouchtech/doc-collaboration-watcher/fork

# 2. 克隆到本地
git clone https://github.com/YOUR_USERNAME/doc-collaboration-watcher.git
cd doc-collaboration-watcher

# 3. 创建功能分支
git checkout -b feature/your-feature-name

# 4. 开发并测试
# ... 编写代码 ...
# ... 测试功能 ...

# 5. 提交变更
git add .
git commit -m "feat: 添加 XXX 功能"

# 6. 推送到 GitHub
git push origin feature/your-feature-name

# 7. 创建 Pull Request
https://github.com/lewistouchtech/doc-collaboration-watcher/pulls
```

**PR 审核标准**：
- ✅ 代码风格一致
- ✅ 功能测试通过
- ✅ 文档同步更新
- ✅ 无破坏性变更（或明确标注）

**审核流程**：
1. 自动检查（CI/CD）
2. 代码审核（伊娃）
3. 功能测试
4. 合并到 main 分支
5. 发布新版本
6. 感谢贡献者 🎉

---

### 4. 改进文档 📖

文档有错别字？配置说明不清楚？缺少示例？

**欢迎提交文档 PR**：
1. 找到需要修改的文件（README.md / docs/*.md）
2. 点击 "Edit this file"
3. 修改内容
4. 提交 PR 描述变更

**文档改进方向**：
- ✅ 错别字修正
- ✅ 语法优化
- ✅ 配置说明补充
- ✅ 使用示例添加
- ✅ 常见问题解答
- ✅ 翻译（多语言支持）

---

## 📋 开发环境搭建

### 前置要求
- Python 3.10+
- OpenClaw 2026.4.0+
- Git

### 本地开发
```bash
# 1. 克隆仓库
git clone https://github.com/lewistouchtech/doc-collaboration-watcher.git
cd doc-collaboration-watcher

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 config.json
cp examples/config.example.json config.json
# 编辑 config.json 配置你的环境

# 5. 运行测试
python3 bin/doc-watcher.py --test

# 6. 启动监控（开发模式）
python3 bin/doc-watcher.py --debug
```

---

## 🧪 测试规范

### 单元测试
```bash
# 运行所有测试
python3 -m pytest tests/

# 运行特定测试
python3 -m pytest tests/test_watcher.py
```

### 集成测试
```bash
# 创建测试文档
echo "# 测试" >> test-doc.md

# 观察监控输出
python3 bin/doc-watcher.py --test-watch

# 清理测试文件
rm test-doc.md
```

---

## 📝 提交规范

### Commit Message 格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型**：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（不新增功能）
- `test`: 测试相关
- `chore`: 构建/工具/配置

**示例**：
```
feat(watcher): 添加文件创建事件监控

- 监控新创建的.md 文件
- 自动加入监控列表
- 发送创建通知

Closes #123
```

---

## 🌟 贡献者权益

### 感谢名单
所有贡献者都会出现在：
- README.md 贡献者列表
- GitHub 贡献者图表
- 发布说明感谢名单

### 当前贡献者
| 贡献者 | 贡献内容 | 时间 |
|--------|----------|------|
| 伊娃 | 初始版本 | 2026-04-07 |
| 李威 | 产品指导/获客逻辑 | 2026-04-07 |
| 🫵 你？ | 等待你的贡献！ | 现在 |

---

## ❓ 常见问题

### Q: 我没有技术背景，能贡献什么？
A: 当然可以！
- 报告使用问题
- 提出功能建议
- 改进文档说明
- 分享使用案例
- 推荐给其他人

### Q: 我的 PR 多久会被审核？
A: 通常 24-48 小时内。如果超过 3 天没响应，可以@作者提醒。

### Q: 贡献代码需要签署 CLA 吗？
A: 不需要！本项目采用简单的贡献许可，提交代码即表示同意开源。

### Q: 可以贡献商业功能吗？
A: 可以！但需要明确标注为"企业版功能"，核心功能保持开源免费。

---

## 📞 联系我们

- **邮箱**: lewis.touchtech@gmail.com
- **GitHub**: https://github.com/lewistouchtech/doc-collaboration-watcher
- **ClawHub**: https://clawhub.ai/skills/doc-collaboration-watcher

---

## 🎉 开始贡献吧！

**第一步**：Star 仓库支持我们 ⭐  
**第二步**：Fork 仓库开始开发 🍴  
**第三步**：提交第一个 PR 🚀  

**一起打造更好的协作文档监控工具！** 💪

---

*本指南参考 GitHub 开源社区最佳实践 | 欢迎改进本指南本身*
