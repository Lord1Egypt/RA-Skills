"""
README 模板生成器
"""


def generate_readme(project_name: str, description: str) -> str:
    return f"""# {project_name}

{description}

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
bash run.sh
```

或直接：

```bash
python src/main.py
```

## 测试

```bash
python -m pytest tests/ -v
```

## 项目结构

```
project_assets/{project_name}/
├── src/                 # 源码目录
│   └── main.py          # 主程序入口
├── tests/               # 测试目录
│   └── test_main.py     # pytest 测试
├── docs/                # 文档目录
│   └── README.md        # 本文件
├── requirements.txt     # 依赖清单
├── run.sh               # 一键运行脚本
├── SKILL.md             # AI 技能元数据
├── ASSET_MANIFEST.md    # 资源地图表
├── manifest.json        # 机器可读资产清单
└── environment.toml     # 环境隔离配置
```

## 环境要求

- Python >= 3.10
- 依赖见 requirements.txt
"""
