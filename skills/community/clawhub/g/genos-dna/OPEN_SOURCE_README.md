# Genos DNA 序列分析 - 开源版本

这是一个基于之江实验室 Genos-1.2B 模型的 DNA 序列分析工具，已优化为适合开源分享的版本。

## 文件结构

```
genos_dna/
├── scripts/
│   ├── __init__.py
│   └── genos_dna.py          # 核心脚本
├── requirements.txt          # Python 依赖
├── README.md                 # 详细说明文档
├── example.py               # 使用示例
├── install.sh               # 一键安装脚本
├── config.json.example      # 配置模板
├── LICENSE                  # MIT 许可证
└── SKILL.md                 # Skill 文档
```

## 主要改进

### 1. 配置优化
- ✅ 支持配置文件管理
- ✅ 可自定义模型路径
- ✅ 灵活的设备配置

### 2. 文档完善
- ✅ 详细的 README 文档
- ✅ 多种使用示例
- ✅ 故障排除指南

### 3. 安装简化
- ✅ 一键安装脚本
- ✅ 自动依赖管理
- ✅ 模型下载助手

### 4. 代码优化
- ✅ 模块化设计
- ✅ 类型注解
- ✅ 错误处理

## 快速开始

### 1. 克隆或复制文件

```bash
# 复制到你的项目目录
cp -r genos_dna /path/to/your/project/
cd /path/to/your/project/genos_dna
```

### 2. 运行安装脚本

```bash
./install.sh
```

安装脚本会自动：
- 检查 Python 环境
- 创建虚拟环境
- 安装依赖
- 下载模型（可选）

### 3. 使用示例

```python
from genos_dna import analyze_dna_sequence

# 分析序列
result = analyze_dna_sequence("ACGTACGTACGT")
print(f"GC 含量: {result['gc_content']:.2f}%")
```

## 配置

复制 `config.json.example` 到 `config.json` 并修改：

```json
{
    "model_path": "./models/Genos-1___2B",
    "device_map": "cpu",
    "torch_dtype": "float16",
    "state_file": "./scripts/.model_loaded"
}
```

## 通用 Skill 系统集成

将此技能添加到任意支持 Skill 的系统中：

```bash
cp -r genos_dna /path/to/system/skills/
```

### 配置模型路径

**推荐使用环境变量方式**：

```bash
# 设置模型路径
export GENOS_MODEL_PATH="/path/to/your/model"

# 设置状态文件路径（可选）
export GENOS_STATUS_FILE="/path/to/your/scripts/.model_loaded"
```

**或者使用配置文件方式**：

```bash
# 复制配置模板
cp config.json.example config.json

# 编辑配置文件
vim config.json
```

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。
