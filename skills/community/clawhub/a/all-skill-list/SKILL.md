---
name: all-skill-list
description: 本地扩展技能目录 - 聚合所有 OpenClaw 本地技能，支持列表查询、描述提取、缓存加速、差异对比、自动更新技能清单
metadata: {"clawbot":{"emoji":"📚","requires":{},"install":[{"id":"local","kind":"dir","path":"/home/node/.openclaw/workspace/skills","label":"本地技能目录"}]}}
---

# 📚 Skill-List - 本地扩展技能目录（智能缓存版）

## 🦀️ 功能介绍
本技能是 OpenClaw 本地技能的聚合管理工具，核心能力：
- ✅ 扫描 `~/.openclaw/workspace/skills` 目录下所有本地技能
- ✅ 自动提取每个技能的名称、功能描述、存储路径
- ✅ 基于 Pickle 缓存加速查询，避免重复全量扫描
- ✅ 智能对比目录变化：仅当技能增/删时更新缓存，无变化直接返回缓存
- ✅ 支持多种输出格式：简单列表、半详细、全详细、JSON、Markdown
- ✅ 支持多种信息详细级别：simple（简单）、half（半详细）、all（完整）

## 🎯 使用方式
### 1. 查看所有技能列表（自动使用缓存）
bash
python3 ~/.openclaw/workspace/skills/all-skill-list/scripts/skill-list.py -V simple

### 2. 强制刷新缓存（无视缓存，重新扫描）
‵‵·bash
python3 ~/.openclaw/workspace/skills/all-skill-list/scripts/skill-list.py --force


### 3. 查看完整技能信息
```bash
#显示简单信息

python3 ~/.openclaw/workspace/skills/all-skill-list/scripts/skill-list.py -V simple
```
```bash
#显示完整SKILL.md内容

python3 ~/.openclaw/workspace/skills/all-skill-list/scripts/skill-list.py -V all
```
```bash
#显示一半信息

python3 ~/.openclaw/workspace/skills/all-skill-list/scripts/skill-list.py -V half
```


### 4. 导出格式
bash
导出为JSON格式

python3 ~/.openclaw/workspace/skills/all-skill-list/scripts/skill-list.py --json

导出为Markdown格式

python3 ~/.openclaw/workspace/skills/all-skill-list/scripts/skill-list.py --md


### 5. 组合使用
bash
强制刷新并显示完整信息

python3 ~/.openclaw/workspace/skills/all-skill-list/scripts/skill-list.py -f -V all

显示完整信息并导出为JSON

python3 ~/.openclaw/workspace/skills/all-skill-list/scripts/skill-list.py -V all --json


## 📊 显示级别说明
| 级别 | 参数 | 显示内容 | 示例 |
|------|------|----------|------|
| 简单 | `-V simple` | 技能名称、状态图标 | `1. ✅ skill-name` |
| 半详细 | `-V half` | 名称、状态、一半描述、路径 | 显示描述前200字符 |
| 完整 | `-V all` | 名称、状态、完整描述、路径 | 显示完整SKILL.md内容 |

## 📝 核心工作流程
OpenClaw 调用本技能时，执行以下逻辑：
1. 读取本地技能根目录：`~/.openclaw/workspace/skills`
2. 检查缓存文件：`~/.openclaw/workspace/skills/all-skill-list/scripts/skills_cache.pickle`
3. 对比缓存中记录的技能目录列表与当前实际目录
   - 目录无变化 → 直接读取并返回缓存内容
   - 目录有变化 → 重新扫描所有技能 → 更新缓存 → 返回新结果
4. 支持通过 `--force` 参数跳过对比，强制刷新缓存
5. 支持通过 `-V` 参数控制输出详细程度

## 📂 缓存与导出文件说明
| 文件 | 格式 | 用途 | 路径 |
|------|------|------|------|
| `skills_cache.pickle` | Pickle | 主缓存文件，加快查询速度 | `all-skill-list/scripts/` |
| `skills_export.json` | JSON | 导出数据，供其他程序使用 | `all-skill-list/scripts/` |
| `all_skills.md` | Markdown | 技能总览文档，包含所有技能描述 | `all-skill-list/scripts/` |

## 🔧 完整命令行参数
```bash
基本参数
用法: python skill-list.py [选项]

选项:
  -f, --force        强制重新扫描
  -v, --verbose      显示详细信息
  -V 级别            显示级别: all(全部)/half(一半)/simple(简单)
  --json             导出为JSON格式
  --md               导出为Markdown格式
  --no-repair        关闭自动修复功能
  --debug            显示调试信息
  -h, --help         显示帮助

自动修复功能:
  当技能的描述为空、路径不存在或信息不完整时，会自动尝试重新获取
  默认开启，可使用 --no-repair 关闭
```
示例:
  python3 skill-list.py                     # 简单列表
  python3 skill-list.py -V all              # 显示完整信息
  python3 skill-list.py --no-repair         # 关闭自动修复
  python3 skill-list.py -f -V all           # 强制刷新并显示全部




## 🎪 使用示例
### 示例1：快速查看所有技能
bash
python3 skill-list.py

输出：

🔍 扫描OpenClaw技能...
📊 OpenClaw技能列表 (共 8 个)
  1. ✅ skill-1
  2. ✅ skill-2
  3. ❌ skill-3
📈 统计: 6/8 个技能有SKILL.md文件


### 示例2：查看技能完整描述
bash
python3 skill-list.py -V all

输出每个技能的完整SKILL.md内容，便于了解技能详情。

### 示例3：导出技能库文档
bash
python3 skill-list.py --md

生成包含所有技能完整描述的Markdown文档，便于分享和查阅。

### 示例4：与其他系统集成
bash
python3 skill-list.py --json > skills.json

导出为JSON格式，便于被其他程序或工具读取。

## 📁 目录结构

~/.openclaw/workspace/skills/
├── skill-1/          # 技能1
│   └── SKILL.md
├── skill-2/          # 技能2
│   └── SKILL.md
└── all-skill-list/       # 当前技能
    ├── SKILL.md      # 本文件
    └── scripts/
        ├── skill-list.py      # 主脚本
        ├── skills_cache.pickle  # 缓存文件
        ├── skills_export.json    # JSON导出文件
        └── all_skills.md         # Markdown导出文件


## 🔄 缓存机制
1. **智能检测**：通过对比技能目录列表变化，决定是否更新缓存
2. **增量更新**：只有技能增删时才重新扫描，提高效率
3. **手动刷新**：支持`--force`参数强制重新扫描
4. **缓存格式**：使用Pickle格式存储，同时支持JSON导出

## 📅 更新日志
| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-03-13 | v1.0 | 初版：基础技能列表查询功能 |
                      新增缓存加速、目录差异对比、JSON输出 |
                      增加-V参数控制显示级别，支持all/half/simple三种模式 |
                      添加--json和--md导出功能，完善帮助文档 |

## 🆕 新功能亮点
1. **灵活的信息显示**：通过`-V`参数控制输出详细程度
2. **多格式导出**：支持JSON和Markdown导出
3. **智能缓存**：自动检测变化，减少不必要的扫描
4. **完整文档**：可生成包含所有技能的详细文档
5. **易于集成**：JSON格式便于与其他工具集成

---

**注意**：本技能会自动排除自身目录（all-skill-list），避免递归扫描问题。所有路径均基于脚本所在位置动态计算，确保在不同环境下都能正常工作。

最后更新：2026-03-20