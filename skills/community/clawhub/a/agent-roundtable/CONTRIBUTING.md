# Contributing to Roundtable

感谢你对 Roundtable 的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

1. 在 [GitHub Issues](https://github.com/MoyuFamily/agent-roundtable/issues) 中搜索是否已有类似问题
2. 如果没有，创建一个新的 Issue，包含：
   - 问题描述
   - 复现步骤
   - 期望行为 vs 实际行为
   - 环境信息（Python 版本、OS 等）

### 提交功能建议

在 Issues 中创建 Feature Request，描述：
- 你想要的功能
- 使用场景
- 建议的实现方式（可选）

### 提交代码

1. Fork 本仓库
2. 创建你的特性分支：`git checkout -b feat/amazing-feature`
3. 提交你的改动：`git commit -m 'feat: add amazing feature'`
4. 推送到分支：`git push origin feat/amazing-feature`
5. 创建 Pull Request

### Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式（不影响逻辑）
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具链

### 开发环境

```bash
# 克隆仓库
git clone https://github.com/MoyuFamily/agent-roundtable.git
cd roundtable

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 运行 lint
ruff check .
```

### Pull Request 要求

- 确保所有测试通过
- 新功能需要附带测试
- 更新相关文档
- 保持 PR 范围聚焦，一个 PR 解决一个问题

## 行为准则

请参阅 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 许可证

提交代码即表示你同意将代码以 [Apache-2.0](LICENSE) 许可证授权。
