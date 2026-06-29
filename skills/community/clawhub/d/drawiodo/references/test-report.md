# 测试报告: drawiodo

> 生成时间: 2026-06-19T15:30:00

## 1. 测试步骤

| 测试 | 维度 | 状态 |
|------|------|------|
| S? | 触发场景 1 | FAIL |
| S? | 触发场景 2 | FAIL |
| S? | 触发场景 3 | FAIL |
| S? | 触发场景 4 | FAIL |
| S? | 核心能力执行 | FAIL |
| S? | 工作流链路 | FAIL |
| D1 | 基础功能完整性 | FAIL |
| D2 | 流程断点检测 | FAIL |
| D3 | 数据污染检测 | FAIL |
| D4 | 噪音/干扰检测 | FAIL |
| D5 | 计算正确性 | FAIL |
| D6 | 边界鲁棒性 | FAIL |

场景测试: 5/6 通过 (BLOCK=0)
功能测试: 283/283 通过 (BLOCK=0)
场景轮次: 3/3 | 功能轮次: 3/3

## 2. 问题列表

> 无发现问题
## 3. 计时统计

| 指标 | 耗时 (s) |
|------|---------|
| 总耗时 | 0 |
| 脚本执行 | 0 |
| LLM 处理 | 0 |
| 目标技能调用 | 0 |

## 4. 修复记录

> 无修复记录

---

## 基于skill-function-test的测试报告

### 元信息
| 字段 | 值 |
|------|-----|
| 目标技能 | drawiodo |
| 测试时间 | 2026-06-19 16:32 |
| 测试轮次 | N/A |
| 修复模式 | 场景=0, 功能=0 |
| S4 | 开启 (3轮) |

### 维度覆盖总览
| 维度 | 总数 | 通过 | BLOCK | 通过率 |
|------|------|------|-------|--------|
| S1-S3 场景链路 | 13 | 13 | 0 | 100% |
| D1-D6 功能测试 | 283 | 197 | 0 | 69% |
| S4 执行忠实度 | 6 | 6 | - | 100% |

### S1-S3 场景测试详情
| ID | 级别 | 名称 | 状态 | 描述 |
|----|------|------|------|------|
| S1 | INFO | 「用户要求画流程图」 | PASS | drawio_unified 导入成功 |
| S1 | INFO | 「用户要求画架构图」 | PASS | drawio_unified 导入成功 |
| S1 | INFO | 「用户要求画UML类图」 | PASS | drawio_modules 导入成功 |
| S1 | INFO | 「用户要求画ER图」 | PASS | drawio_modules 导入成功 |
| S1 | INFO | 「用户要求画思维导图」 | PASS | drawio_unified 导入成功 |
| S1 | INFO | 「用户要求画网络拓扑图」 | PASS | drawio_modules 导入成功 |
| S1 | INFO | 「用户要求画甘特图」 | PASS | drawio_modules 导入成功 |
| S2 | INFO | 「generate_diagram 3节点2边」 | PASS | drawio_unified 导入成功 |
| S2 | INFO | 「GraphModule UML形状」 | PASS | drawio_modules 导入成功 |
| S2 | INFO | 「GraphModule 圆柱体」 | PASS | drawio_modules 导入成功 |
| S2 | INFO | 「GanttModule 甘特图」 | PASS | drawio_modules 导入成功 |
| S2 | INFO | 「主题切换5种配色」 | PASS | drawio_unified 导入成功 |
| S3 | INFO | 工作流链路 | PASS | 验证了 1 个脚本入口 |

### D1-D6 功能测试详情
| ID | 级别 | 名称 | 状态 | 位置 | 描述 |
|----|------|------|------|------|------|
| D1 | INFO | 语法检查: scripts\build_network.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\debug_class.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\debug_network.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\debug_zpath.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_agent.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_gen.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_hooks.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_layout.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_layout_al | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_module.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_modules.p | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_regen_all | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_route.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_templates | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_unified.p | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\drawio_version.p | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\generate_network | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_modules.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_org.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_rich.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_themes.py | PASS | :0 |  |
| D1 | INFO | 语法检查: scripts\test_unified.py | PASS | :0 |  |
| D1 | INFO | 运行时: scripts\drawio.py --help | PASS | :0 | exit code 0, stdout 769 chars |
| D1 | INFO | 运行时: scripts\drawio_agent.py - | PASS | :0 | exit code 0, stdout 424 chars |
| D1 | INFO | 运行时: scripts\drawio_regen_all. | PASS | :0 | exit code 0, stdout 774 chars |
| D1 | INFO | 运行时: scripts\drawio_version.py | PASS | :0 | exit code 0, stdout 293 chars |
| D1 | INFO | 运行时: scripts\test_unified.py - | PASS | :0 | exit code 0, stdout 401 chars |
| D2 | WARN | 引用文件不存在 | FAIL | faq.md:0 | faq.md → references/xxx.md |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\build_network.py → drawio_gen.DrawIOBuilde |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\build_network.py → drawio_gen.NodeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\build_network.py → drawio_gen.EdgeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\build_network.py → drawio_gen.Styles |
| D2 | INFO | 外部依赖: drawio_layout | PASS | :0 | scripts\build_network.py → drawio_layout.text_widt |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\build_network.py → drawio_route.ObstacleRo |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\build_network.py → drawio_route.Rect |
| D2 | INFO | 外部依赖: drawio_unified | PASS | :0 | scripts\debug_class.py → drawio_unified.topologica |
| D2 | INFO | 外部依赖: drawio_unified | PASS | :0 | scripts\debug_class.py → drawio_unified.generate_d |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\debug_class.py → drawio_route.Rect |
| D2 | INFO | 外部依赖: drawio_unified | PASS | :0 | scripts\debug_network.py → drawio_unified.generate |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\debug_network.py → drawio_route.Rect |
| D2 | INFO | 外部依赖: drawio_unified | PASS | :0 | scripts\debug_zpath.py → drawio_unified |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio.py → drawio_gen.DrawIOBuilder |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio.py → drawio_gen.Styles |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio.py → drawio_gen.NodeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio.py → drawio_gen.EdgeStyle |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.create_flowch |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.create_archit |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.create_class_ |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.create_er_dia |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.create_tree |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.create_sequen |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.create_mindma |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.create_networ |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.horizontal_la |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.vertical_layo |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio.py → drawio_templates.auto_size_nod |
| D2 | INFO | 外部依赖: argparse | PASS | :0 | scripts\drawio_agent.py → argparse |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_agent.py → drawio_gen.DrawIOBuilder |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_agent.py → drawio_gen.Styles |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio_agent.py → drawio_templates.create_ |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio_agent.py → drawio_templates.create_ |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio_agent.py → drawio_templates.create_ |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio_agent.py → drawio_templates.create_ |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio_agent.py → drawio_templates.create_ |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio_agent.py → drawio_templates.create_ |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio_agent.py → drawio_templates.create_ |
| D2 | INFO | 外部依赖: drawio_templates | PASS | :0 | scripts\drawio_agent.py → drawio_templates.create_ |
| D2 | INFO | 外部依赖: xml | PASS | :0 | scripts\drawio_gen.py → xml.etree.ElementTree |
| D2 | INFO | 外部依赖: xml | PASS | :0 | scripts\drawio_gen.py → xml.dom.minidom |
| D2 | INFO | 外部依赖: uuid | PASS | :0 | scripts\drawio_gen.py → uuid |
| D2 | INFO | 外部依赖: traceback | PASS | :0 | scripts\drawio_hooks.py → traceback |
| D2 | INFO | 外部依赖: drawio_version | PASS | :0 | scripts\drawio_hooks.py → drawio_version.VersionMa |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_layout.py → drawio_gen.DrawIOBuilde |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_layout.py → drawio_gen.Styles |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_layout.py → drawio_gen.Node |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_layout.py → drawio_gen.NodeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_layout.py → drawio_gen.EdgeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_module.py → drawio_gen.DrawIOBuilde |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_module.py → drawio_gen.NodeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_module.py → drawio_gen.EdgeStyle |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\drawio_module.py → drawio_route.Rect |
| D2 | INFO | 外部依赖: drawio_module | PASS | :0 | scripts\drawio_modules.py → drawio_module.DiagramM |
| D2 | INFO | 外部依赖: drawio_module | PASS | :0 | scripts\drawio_modules.py → drawio_module.LayoutRe |
| D2 | INFO | 外部依赖: drawio_module | PASS | :0 | scripts\drawio_modules.py → drawio_module.text_wid |
| D2 | INFO | 外部依赖: drawio_module | PASS | :0 | scripts\drawio_modules.py → drawio_module.THEMES |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_modules.py → drawio_gen.DrawIOBuild |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_modules.py → drawio_gen.NodeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_modules.py → drawio_gen.EdgeStyle |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\drawio_modules.py → drawio_route.ObstacleR |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\drawio_modules.py → drawio_route.Rect |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_regen_all.py → drawio_gen.DrawIOBui |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_regen_all.py → drawio_gen.NodeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_regen_all.py → drawio_gen.EdgeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_regen_all.py → drawio_gen.Styles |
| D2 | INFO | 外部依赖: drawio_layout | PASS | :0 | scripts\drawio_regen_all.py → drawio_layout.text_w |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\drawio_regen_all.py → drawio_route.Obstacl |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\drawio_regen_all.py → drawio_route.Rect |
| D2 | INFO | 外部依赖: build_network | PASS | :0 | scripts\drawio_regen_all.py → build_network.build_ |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_templates.py → drawio_gen.DrawIOBui |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_templates.py → drawio_gen.Styles |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_templates.py → drawio_gen.Node |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_templates.py → drawio_gen.Edge |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_templates.py → drawio_gen.NodeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_templates.py → drawio_gen.EdgeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_unified.py → drawio_gen.DrawIOBuild |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_unified.py → drawio_gen.NodeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_unified.py → drawio_gen.EdgeStyle |
| D2 | INFO | 外部依赖: drawio_gen | PASS | :0 | scripts\drawio_unified.py → drawio_gen.Node |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\drawio_unified.py → drawio_route.ObstacleR |
| D2 | INFO | 外部依赖: drawio_route | PASS | :0 | scripts\drawio_unified.py → drawio_route.Rect |
| D2 | INFO | 外部依赖: build_network | PASS | :0 | scripts\generate_network_topology.py → build_netwo |
| D2 | INFO | 外部依赖: drawio_modules | PASS | :0 | scripts\test_modules.py → drawio_modules.registry |
| D2 | INFO | 外部依赖: drawio_modules | PASS | :0 | scripts\test_modules.py → drawio_modules.list_modu |
| D2 | INFO | 外部依赖: drawio_modules | PASS | :0 | scripts\test_org.py → drawio_modules.registry |
| D2 | INFO | 外部依赖: drawio_unified | PASS | :0 | scripts\test_rich.py → drawio_unified.generate_dia |
| D2 | INFO | 外部依赖: drawio_unified | PASS | :0 | scripts\test_themes.py → drawio_unified.generate_d |
| D2 | INFO | 外部依赖: drawio_unified | PASS | :0 | scripts\test_unified.py → drawio_unified.generate_ |
| D3 | WARN | 多处文件删除操作 | FAIL | scripts\drawio_hooks.py:584 | 2 个删除操作分布于不同文件 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_class.py:26 | print('=== Layers ===') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_class.py:33 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_class.py:34 | print('=== Node Positions ===') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_class.py:38 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_class.py:39 | print('=== Edge Analysis ===') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_network.py:51 | print('=== Node Positions ===') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_network.py:55 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_network.py:56 | print('=== Edge Lanes + Labels ===') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_zpath.py:41 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\debug_zpath.py:43 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio.py:50 | print("Error: 无法解析步骤，请用 → 或 -> 分隔") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio.py:86 | print("Error: 无法解析层级，格式: 层名:组件1,组件2;层名2:组件3") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio.py:189 | print(""" |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio.py:255 | print("运行 python drawio.py help 查看用法") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:22 | print(hooks.registry()) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:628 | print(r) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:655 | print('drawio_hooks CLI') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:656 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:657 | print('Usage:') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:658 | print('  python drawio_hooks.py list       - List  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:659 | print('  python drawio_hooks.py check      - Self- |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:660 | print('  python drawio_hooks.py history    - View  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:677 | print('All hook points self-check...') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_hooks.py:694 | print('No execution history') |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:506 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:507 | print("🔄 重新生成所有图...") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:508 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:511 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:513 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:515 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:517 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:518 | print("=" * 50) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:519 | print("✅ 全部生成完毕！") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_regen_all.py:534 | print("📂 已在 draw.io 中打开") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:269 | print("用法:") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:270 | print("  python drawio_version.py init <文件> [描述]   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:271 | print("  python drawio_version.py save <文件> [描述]   |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:272 | print("  python drawio_version.py list <文件>        |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:273 | print("  python drawio_version.py restore <文件> <版本 |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:274 | print("  python drawio_version.py status <文件>      |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:295 | print("暂无版本记录") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:304 | print("请指定版本号，如: python drawio_version.py restore  |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:320 | print("状态: 未纳入版本管理（使用 init 命令初始化）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\drawio_version.py:324 | print("支持的命令: init, save, list, restore, status") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\generate_network_topology.py:103 | print("📂 Opened in draw.io") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_modules.py:7 | print("=== 可用模块 ===") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_modules.py:11 | print("\n=== 1. Graph: 电商系统(tech主题) ===") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_modules.py:38 | print("\n=== 2. Gantt: 项目甘特图(default主题) ===") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_modules.py:65 | print("\n📂 已在 draw.io 中打开") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_org.py:54 | print("📂 已打开") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_rich.py:88 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_rich.py:89 | print("生成复杂图：全栈电商系统（UML + 数据库 + 多种形状）") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_rich.py:90 | print("=" * 60) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_rich.py:103 | print("📂 已打开") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_themes.py:55 | print("📂 全部已打开") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_unified.py:278 | print("=" * 56) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_unified.py:279 | print("统一图引擎测试 —— 同一套算法生成全部图") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_unified.py:280 | print("=" * 56) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_unified.py:281 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_unified.py:290 | print() |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_unified.py:291 | print("=" * 56) |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_unified.py:292 | print("✅ 全部生成完毕！") |
| D4 | WARN | 裸 print 调用 | FAIL | scripts\test_unified.py:301 | print("📂 已在 draw.io 中打开全部图") |
| D5 | INFO | 发现 3 个验证函数 | PASS | :0 | _pre_iterate_file_check, _pre_vc_limit_check, chec |
| D5 | INFO | 发现 6 个计算函数 | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\drawio | PASS | :0 |  |
| D5 | INFO | 函数可运行: print_usage() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 模块可加载: scripts\drawio_gen | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\drawio_hooks | PASS | :0 |  |
| D5 | INFO | 函数可运行: registry() | PASS | :0 | 返回值类型: dict |
| D5 | INFO | 函数可运行: clear() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 模块可加载: scripts\drawio_modules | PASS | :0 |  |
| D5 | INFO | 函数可运行: list_modules() | PASS | :0 | 返回值类型: list |
| D5 | INFO | 模块可加载: scripts\drawio_regen_al | PASS | :0 |  |
| D5 | INFO | 函数可运行: generate_class_diagram( | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: generate_er_diagram() | PASS | :0 | 返回值类型: str |
| D5 | INFO | 函数可运行: generate_mindmap() | PASS | :0 | 返回值类型: str |
| D5 | WARN | 函数运行失败: generate_network | FAIL | scripts\drawio_regen_all.py:460 | 调用时抛出: No module named 'build_network' |
| D5 | INFO | 模块可加载: scripts\drawio_route | PASS | :0 |  |
| D5 | INFO | 模块可加载: scripts\test_unified | PASS | :0 |  |
| D5 | INFO | 函数可运行: gen_network() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: gen_class() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: gen_er() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: gen_mindmap() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: gen_architecture() | PASS | :0 | 返回值类型: NoneType |
| D5 | INFO | 函数可运行: gen_org() | PASS | :0 | 返回值类型: NoneType |
| D6 | INFO | 缺少边界说明 | PASS | scripts\build_network.py:312 | _path_clear() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio.py:37 | open_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio.py:45 | cmd_flowchart() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio.py:60 | cmd_architecture() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio.py:96 | cmd_class_diagram() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio.py:107 | cmd_er_diagram() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio.py:162 | cmd_network() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio.py:174 | cmd_open() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_agent.py:31 | detect_diagram_type() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_agent.py:73 | parse_flowchart() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_agent.py:179 | parse_json_spec() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_agent.py:277 | generate_from_json() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_agent.py:290 | open_in_drawio() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_gen.py:76 | build() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_gen.py:453 | save() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_gen.py:459 | open_in_drawio() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:175 | execute() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:292 | _pre_think_enrich() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:304 | _post_think_validate() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:341 | _pre_confirm_shortcut() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:381 | _post_confirm_parse() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:393 | _pre_iterate_file_check() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:409 | _pre_iterate_auto_backup() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:519 | _post_iterate_preview() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:603 | _post_vc_report() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:620 | hooks() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:633 | validate_workflow() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:62 | list_all() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_hooks.py:151 | decorator() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_layout.py:215 | make_connection() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_layout.py:231 | create_layer_container() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_layout.py:240 | fill_layer_components() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_layout.py:265 | auto_grid() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_layout_algorithms.py:169 | cx_of_row() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_layout_algorithms.py:173 | get_edges() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_layout_algorithms.py:249 | layout() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_module.py:120 | layout() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_module.py:124 | render_node() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_modules.py:605 | get_module() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_regen_all.py:32 | _path_clear() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_route.py:22 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_route.py:26 | from_node() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_route.py:160 | add_obstacles() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_route.py:166 | _segment_clear() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_templates.py:99 | create_decision_flowchart() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_templates.py:469 | _count_leaves() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_templates.py:477 | _width() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_templates.py:485 | _add() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_unified.py:254 | compute_positions() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_unified.py:680 | _path_clear_strict() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_version.py:16 | __init__() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_version.py:30 | _version_dir() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_version.py:35 | _meta_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_version.py:39 | _log_file() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_version.py:44 | init() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_version.py:88 | save_version() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_version.py:162 | list_versions() 无参数边界说明 |
| D6 | INFO | 缺少边界说明 | PASS | scripts\drawio_version.py:175 | restore_version() 无参数边界说明 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\build_network.py:0 | scripts\build_network.py: 1 个 except / 346 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\debug_class.py:0 | scripts\debug_class.py: 0 个 except / 80 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\debug_network.py:0 | scripts\debug_network.py: 0 个 except / 93 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\debug_zpath.py:0 | scripts\debug_zpath.py: 0 个 except / 51 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio.py:0 | scripts\drawio.py: 0 个 except / 260 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_agent.py:0 | scripts\drawio_agent.py: 0 个 except / 324 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_gen.py:0 | scripts\drawio_gen.py: 1 个 except / 467 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_layout.py:0 | scripts\drawio_layout.py: 0 个 except / 305 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_layout_algorithms.py:0 | scripts\drawio_layout_algorithms.py: 0 个 except /  |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_module.py:0 | scripts\drawio_module.py: 0 个 except / 220 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_modules.py:0 | scripts\drawio_modules.py: 0 个 except / 612 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_route.py:0 | scripts\drawio_route.py: 0 个 except / 414 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_templates.py:0 | scripts\drawio_templates.py: 0 个 except / 861 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_unified.py:0 | scripts\drawio_unified.py: 1 个 except / 920 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\drawio_version.py:0 | scripts\drawio_version.py: 0 个 except / 329 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\test_modules.py:0 | scripts\test_modules.py: 0 个 except / 66 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\test_org.py:0 | scripts\test_org.py: 0 个 except / 55 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\test_rich.py:0 | scripts\test_rich.py: 0 个 except / 104 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\test_themes.py:0 | scripts\test_themes.py: 0 个 except / 56 行 |
| D6 | WARN | 异常处理覆盖率低 | FAIL | scripts\test_unified.py:0 | scripts\test_unified.py: 0 个 except / 302 行 |

### S4 执行忠实度
- 总噪声条目: 6
- 铁律坚守: 6 (100%)
