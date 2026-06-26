# dingtalk-ai-table-insights - 依赖说明

## 核心依赖

### dingtalk-ai-table skill

**作用：** 用于读取钉钉 AI 表格数据

**GitHub:** https://github.com/aliramw/dingtalk-ai-table

**安装方式:**
```bash
clawhub install dingtalk-ai-table
```

**验证安装:**
```bash
clawhub list
# 应该看到 dingtalk-ai-table 在列表中
```

**使用的功能:**
- `read_table.py` - 读取表格数据脚本
- `search_base_record` - MCP API 查询记录

---

## 环境依赖

### Python 3.7+

**作用：** 运行分析脚本

**验证:**
```bash
python3 --version
# 应该显示 Python 3.7.0 或更高版本
```

**安装 (如需要):**
```bash
# macOS
brew install python@3.9

# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# Windows
# 从 https://www.python.org/downloads/ 下载
```

### 钉钉 AI 表格 MCP Token

**作用：** 认证访问钉钉 AI 表格

**配置方式:**
```bash
export DINGTALK_MCP_TOKEN="your-token-here"
```

**永久配置 (推荐):**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export DINGTALK_MCP_TOKEN="your-token-here"' >> ~/.bashrc
source ~/.bashrc
```

---

## 可选依赖

### mcporter CLI

**作用：** 获取可访问的表格列表（临时方案）

**状态：** ⚠️ 未来将移除，改用 dingtalk-ai-table 的 list 接口

**安装:**
```bash
npm install -g mcporter
```

**配置:**
```bash
# 配置文件位于
/home/admin/openclaw/workspace/config/mcporter.json
```

---

## 依赖关系图

```
dingtalk-ai-table-insights
├── dingtalk-ai-table (必需)
│   └── 钉钉 AI 表格 MCP
├── python3 (必需)
└── mcporter (临时，用于获取表格列表)
    └── 钉钉 AI 表格 MCP
```

---

## 安装检查清单

- [ ] Python 3.7+ 已安装
- [ ] dingtalk-ai-table skill 已安装
- [ ] DINGTALK_MCP_TOKEN 已配置
- [ ] 可以访问钉钉 AI 表格

**快速验证:**
```bash
# 1. 检查 Python
python3 --version

# 2. 检查 skill 安装
clawhub list | grep dingtalk-ai-table

# 3. 检查环境变量
echo $DINGTALK_MCP_TOKEN

# 4. 测试读取表格
python3 ~/.openclaw/skills/dingtalk-ai-table/scripts/read_table.py \
  --doc-id <你的表格 ID> \
  --sheet Sheet1 \
  --limit 5
```

---

## 故障排查

### 问题：找不到 dingtalk-ai-table 脚本

**症状:**
```
FileNotFoundError: [Errno 2] No such file or directory: '~/.openclaw/skills/dingtalk-ai-table/scripts/read_table.py'
```

**解决方案:**
```bash
# 安装 dingtalk-ai-table skill
clawhub install dingtalk-ai-table

# 验证安装位置
ls -la ~/.openclaw/skills/dingtalk-ai-table/scripts/
```

### 问题：权限不足

**症状:**
```
Error: 403 - The access token should be issued by the organization
```

**解决方案:**
1. 确认表格已分享给正确的组织
2. 检查 DINGTALK_MCP_TOKEN 是否有效
3. 联系表格所有者授予访问权限

### 问题：Python 版本过低

**症状:**
```
SyntaxError: invalid syntax
```

**解决方案:**
```bash
# 检查版本
python3 --version

# 升级到 3.7+
# 参考上面的安装指南
```

---

## 依赖版本兼容性

| 依赖 | 最低版本 | 推荐版本 | 备注 |
|------|----------|----------|------|
| Python | 3.7 | 3.9+ | 需要 type hints 支持 |
| dingtalk-ai-table | 1.0.0 | latest | 需要 search_base_record 接口 |
| mcporter | 0.1.0 | latest | 临时依赖 |

---

## 未来规划

### v1.1 计划
- [ ] 移除 mcporter 依赖
- [ ] 使用 dingtalk-ai-table 的 list_tables 接口
- [ ] 减少对临时方案的依赖

### v1.2 计划
- [ ] 支持直接调用 dingtalk-ai-table 的 MCP API
- [ ] 优化数据读取性能
- [ ] 添加缓存机制

---

*技能名称：dingtalk-ai-table-insights*

---

*最后更新：2025-02-28*
