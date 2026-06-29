# 图表生成参考

路径信息见 `_meta.json` data_dir 声明 + frontmatter data_dir 字段。

### 方式 A - Python API 调用（推荐）

```python
import sys
sys.path.insert(0, "{SKILLS_DIR}/drawiodo/scripts")
from drawio_templates import *
from pathlib import Path

DATA_DIR = Path.home() / ".workbuddy" / "skills" / ".standardization" / "drawiodo"
OUTPUT_DIR = DATA_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 流程图
builder = create_flowchart(["开始", "处理", "结束"])
builder.save(str(OUTPUT_DIR / "flowchart_example.drawio"))

# 架构图
builder = create_architecture([
    {"name": "Frontend", "components": ["React", "Vue"], "color": Styles.BLUE_NODE},
    {"name": "Backend", "components": ["API", "Auth"], "color": Styles.GREEN_NODE},
])
builder.save(str(OUTPUT_DIR / "architecture_example.drawio"))

# 自定义（完全控制）
from drawio_gen import DrawIOBuilder, Styles
builder = DrawIOBuilder(name="My Diagram")
node1 = builder.add_node("Node1", 100, 100, 120, 60, style=Styles.BLUE_NODE)
node2 = builder.add_node("Node2", 100, 220, 120, 60, style=Styles.GREEN_NODE)
builder.connect(node1, node2, "label")
builder.save(str(OUTPUT_DIR / "custom_example.drawio"))
```

### 方式 B - CLI 调用

```bash
python {SKILL_DIR}/scripts/drawio_agent.py "画一个用户登录流程图：输入账号 → 验证 → 查询数据库 → 返回结果" --output-dir {DATA_DIR}/outputs/
python {SKILL_DIR}/scripts/drawio_agent.py spec.json --output-dir {DATA_DIR}/outputs/
```

### 方式 C - JSON spec 文件

```json
{
  "type": "flowchart",
  "title": "用户登录",
  "steps": ["输入账号", "验证密码", "查询数据库", "返回结果"],
  "output_dir": "{DATA_DIR}/outputs/"
}
```

支持的 type：`flowchart`, `architecture`, `class_diagram`, `er_diagram`, `tree`, `sequence`, `mindmap`, `network`

### 打开预览

```bash
"C:\Program Files\draw.io\draw.io.exe" "{DATA_DIR}/outputs/生成的文件.drawio"
```

---
