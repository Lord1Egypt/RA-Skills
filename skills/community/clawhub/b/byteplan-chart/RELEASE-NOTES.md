# 📦 BytePlan Chart - 发布包

**版本**: 1.0.2  
**发布日期**: 2026-03-13  
**状态**: ✅ 准备就绪

---

## 📁 文件清单

```
byteplan-chart-release/
├── SKILL.md           - 技能文档（ClawHub 必需）
├── README.md          - 用户文档
├── CHANGES.md         - 变更日志
├── INSTALL.md         - 安装指南
├── package.json       - ClawHub 元数据
├── .env.example       - 环境变量示例
├── .gitignore         - Git 忽略文件
├── .clawhubignore     - ClawHub 忽略文件
├── main.py            - 主程序（18 KB）
└── render_chart.py    - 图表渲染（21 KB）
```

**总计**: 10 个文件，约 61 KB

---

## 🚀 发布命令

```bash
# 1. 进入发布文件夹
cd C:\Users\wangshuai\.openclaw\skills\byteplan-chart-release

# 2. 登录 ClawHub（打开浏览器）
clawhub login

# 3. 发布技能
clawhub publish . --slug byteplan-chart --name "BytePlan Chart" --version 1.0.2 --changelog "修复：uv run python 调用，跨平台兼容，依赖管理优化"
```

---

## ✅ 已清理的文件

以下文件已移除，不包含在发布包中：

- ❌ `.venv/` - Python 虚拟环境（用户自行创建）
- ❌ `charts/` - 生成的图表文件
- ❌ `node_modules/` - Node 依赖（不需要）
- ❌ `__pycache__/` - Python 缓存
- ❌ `.env` - 环境变量（包含敏感信息）
- ❌ `.clawhubrc.json` - 本地配置
- ❌ `PUBLISH-GUIDE.md` - 发布指南（内部使用）
- ❌ `prompt.md` - 提示词（内部使用）
- ❌ `yarn.lock` - Yarn 锁定文件
- ❌ `_meta.json` - 元数据（内部使用）

---

## 📋 版本说明

### v1.0.2 (本次发布)

**修复**:
- 🔧 main.py: 渲染脚本调用改为 `uv run python`
- 🔧 render_chart.py: 参数检查从 `< 4` 改为 `< 3`
- 🍎 完整支持 macOS（自动使用 PingFang SC 字体）
- 🐧 完整支持 Linux（自动使用文泉驿字体）

**优化**:
- 📦 依赖管理优化
- 📚 文档完善

### v1.0.1 (已发布)

- 初始发布
- 支持 12 种图表类型

---

## 🎯 功能特性

- ✅ 12 种图表类型（折线图、柱状图、饼图、双轴图等）
- ✅ 自动中文字体检测（Windows/macOS/Linux）
- ✅ BytePlan AI 集成
- ✅ RSA 加密认证
- ✅ 跨平台兼容

---

## 📞 支持

- **作者**: wangshuaiitr-ai
- **许可**: MIT
- **问题反馈**: https://clawhub.com/skills/byteplan-chart

---

**准备就绪，可以直接发布！** ✅
