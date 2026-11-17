# drawio-diagram-builder

为 AI 助手提供的 draw.io/diagrams.net 技术图表生成技能。支持 XML 手动编写、预览/验证脚本、迭代式精炼工作流。

> 适配自 [Will-hxw/drawio-diagram-builder-skill](https://github.com/Will-hxw/drawio-diagram-builder-skill)

## 安装

### OpenClaw 用户

```bash
clawhub install drawio-diagram-builder
```

或直接放入技能目录：

```bash
git clone https://github.com/holdyounger/drawio-diagram-builder.git ~/.openclaw/skills/drawio-diagram-builder
```

### 目录结构

```
drawio-diagram-builder/
├── SKILL.md                    # 技能主文件（含完整文档）
├── VERSION                     # 版本
├── scripts/                    # Python 工具脚本
│   ├── validate_drawio.py      # XML 结构验证
│   ├── validate_visual_quality.py  # 视觉质量检查
│   ├── make_drawio_preview.py  # 预览 HTML 生成
│   ├── serve_drawio_preview.py # 服务端预览
│   ├── validate_replication_artifacts.py  # 复刻验证
│   └── check_skill_update.py  # 版本检查
├── references/                 # 参考文档
│   ├── xml-authoring.md        # XML 结构、样式、形状、连线指南
│   ├── drawio-workflow.md      # 端到端工作流
│   ├── self-supervision-and-intake.md
│   ├── style-extraction.md     # 从参考图提取风格
│   ├── topconf-paper-style.md  # 顶会论文风格
│   ├── primitive-icons.md      # 可编辑图元图标配方
│   ├── xml-preflight.md        # 截图前静态质量检查
│   └── reference-replication-protocol.md
├── assets/
│   ├── icons/                  # 100+ MIT 许可 Tabler SVG 图标
│   └── reference-images/       # 论文风格参考图
└── examples/                   # .drawio 示例文件
```

## 快速开始

```bash
# 验证 drawio XML
python3 scripts/validate_drawio.py diagram.drawio

# 生成预览 HTML
python3 scripts/make_drawio_preview.py diagram.drawio --out /tmp/preview.html

# 启动预览服务
python3 scripts/serve_drawio_preview.py diagram.drawio --port 8765
```

## 使用场景

- **系统架构图** — 展示模块间通信、数据流和控制流
- **论文方法图** — 顶会风格的研究方法流程图
- **API 关联图谱** — 用分层节点和连线展示依赖关系
- **视觉复刻** — 精确复现参考图的布局、配色和排版

## 许可证

MIT
