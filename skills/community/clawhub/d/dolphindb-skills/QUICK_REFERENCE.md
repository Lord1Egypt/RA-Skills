# DolphinDB 技能 - 快速参考卡

## 🚀 一键启动（推荐）

```bash
cd ~/.jvs/.openclaw/workspace/skills/dolphindb-skills
source scripts/dolphin_wrapper.sh
dolphin_python your_script.py
```

## 🔍 环境检测

```bash
# 检测环境
python3 scripts/init_dolphindb_env.py

# 导出环境变量
python3 scripts/init_dolphindb_env.py --export
```

## 📦 安装包

```bash
# 使用包装器
dolphin_pip install package_name

# 或直接使用
$DOLPHINDB_PYTHON_BIN -m pip install package_name
```

## 🐛 常见错误

### ModuleNotFoundError: No module named 'dolphindb'

```bash
source scripts/dolphin_wrapper.sh
```

### DOLPHINDB_PYTHON_BIN: command not found

```bash
source scripts/dolphin_wrapper.sh
```

### Connection refused

```bash
docker ps | grep dolphindb
docker start dolphindb
```

## 📁 重要文件

| 文件 | 用途 |
|------|------|
| `scripts/dolphin_wrapper.sh` | 包装器（一键加载） |
| `scripts/init_dolphindb_env.py` | 环境检测 |
| `USAGE_GUIDE.md` | 详细使用指南 |
| `MIGRATION_GUIDE.md` | 迁移指南 |

## 💡 最佳实践

```bash
# ✅ 总是使用包装器
source scripts/dolphin_wrapper.sh
dolphin_python script.py

# ❌ 不要直接使用
python3 script.py
```

## 📞 完整文档

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 使用指南
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - 迁移指南  
- [README_STANDARDIZATION.md](README_STANDARDIZATION.md) - 改造总结
