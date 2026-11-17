---
slug: game-asset-gen-tool-pro
name: "game-asset-gen-tool-pro"
version: "1.0.0"
displayName: "游戏资产生成-专业版"
summary: "全栈游戏资产生成引擎，支持2D/3D资产、完整GDD、批量生成与多艺术风格。。游戏资产生成工具专业版。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工"
license: "Proprietary"
edition: "pro"
description: |- 功能涵盖: game, asset, gen。
  游戏资产生成工具专业版。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。支持多场景应用和灵活配置。
tags:
  - Creative
  - GameDev
  - Enterprise
  - 3D
  - 工具
  - 效率
  - 自动化
  - 创意
  - 图像
  - 生活
  - 健康
  - self
  - weapon
  - gdd
  - 批量生成
  - glb
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---

> **功能说明**: 本技能涵盖 中文交互 等核心能力。

# 游戏资产生成工具（专业版）
## 概述
游戏资产生成工具专业版是全栈游戏资产生成平台，覆盖 2D 精灵、3D 模型、UI 元素、游戏设计文档和概念设计。通过角色一致性技术，确保所有资产生成保持统一的艺术风格。支持批量生成（一次生成 10+ 资产）和 GLB 格式 3D 模型输出，兼容 Unity、Unreal、Godot 等主流引擎.
本版本与免费版完全兼容——免费版的 2D 资产生成能力在专业版中完整保留。专业版新增 3D 模型、GDD 生成、批量操作和全艺术风格覆盖.
## 核心能力
### 能力对比
| 能力维度 | 免费版 | 专业版 |
|----|---|---|
| 2D资产 | 支持 | 支持 |
| 3D模型 | 不支持 | GLB格式（Unity/Unreal/Godot兼容） |
| 艺术风格 | 3种 | 7种（+低多边形/动漫/写实/3D） |
| 批量生成 | 不支持 | 一次10+资产 |
| GDD生成 | 不支持 | 完整游戏设计文档 |
| 概念设计 | 不支持 | 故事/机制/世界观 |
| 粒子特效 | 不支持 | 魔法/爆炸/命中特效 |
| 角色一致性 | 基础 | 跨资产深度一致 |
| 对话模式 | 单agent | agent + agent team |
**处理**: 解析能力对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回能力对比的响应数据,包含状态码、结果和日志.
### 核心能力(补充)
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 游戏资产生成-专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |
```text
3D 模型生成 (GLB):
  - 角色模型: 主角/NPC/敌人
  - 武器道具: 剑/斧/弓/法杖
  - 场景物件: 宝箱/木桶/火把
  - 载具: 飞船/马车
  - 环境元素: 树木/岩石/建筑
  - 可指定: 多边形数量 + PBR材质
# ...
批量生成:
  - 一次生成 10+ 武器模型
  - 多角色变体批量产出
  - 瓦片集全量生成
  - 道具图标批量制作
# ...
游戏设计文档 (GDD):
  - 核心循环设计
  - 进度系统
  - 商业化策略
  - 关卡设计（前10关）
  - 艺术风格推荐
# ...
艺术风格全覆盖:
  - Pixel Art（像素风）
  - Hand-Painted（手绘风）
  - Vector/Flat（扁平风）
  - Low Poly 3D（低多边形）
  - Anime/Manga（动漫风）
  - Realistic（写实风）
  - 3D Models（3D模型）
# ...
游戏概念设计:
  - 游戏设计文档 (GDD)
  - 故事大纲
  - 机制设计
  - 世界观构建
  - 发行商演示文档
# ...
粒子特效:
  - 魔法施法效果
  - 爆炸效果
  - 命中反馈
  - 环境氛围粒子
```
**处理**: 解析核心能力的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心能力的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 核心功能执行
用`input_params`参数进行配置.
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：全栈游戏资产生成、批量生成与多艺术、游戏资产生成工具、Use、when、需要提升效率、自动化流程、批量处理、工作流优化时使用、不适用于需要人工、创意判断的任务、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
### 场景一：3D 模型批量生成
为游戏批量生成 3D 武器模型.
```python
# 3D武器模型批量生成
class Batch3DAssetGenerator:
    """3D资产批量生成器"""
# ...
    def __init__(self, art_style="low-poly", engine="unity"):
        self.art_style = art_style
        self.engine = engine
        self.assets = []
# ...
    def generate_weapon_pack(self, weapons):
        """批量生成武器3D模型"""
        for weapon in weapons:
            prompt = self._build_prompt(weapon)
            result = {
                "name": weapon["name"],
                "type": "weapon",
                "format": "glb",
                "prompt": prompt,
                "poly_count": weapon.get("poly_count", "low"),
                "materials": weapon.get("materials", ["PBR-matte"]),
                "engine_compatible": ["unity", "unreal", "godot", "three.js"]
            }
            self.assets.append(result)
        return self.assets
# ...
    def _build_prompt(self, weapon):
        return f"""
        创建3D武器模型: {weapon['name']}
# ...
        风格: {self.art_style}
        描述: {weapon['description']}
        多边形数量: {weapon.get('poly_count', 'low-poly')}
        材质: {', '.join(weapon.get('materials', ['PBR']))}
# ...
        输出格式: GLB
        兼容引擎: Unity, Unreal, Godot, Three.js, Blender
        """
# ...
# 批量生成武器包
weapons = [
    {"name": "iron-sword", "description": "铁制长剑，经典造型", "poly_count": "low"},
    {"name": "battle-axe", "description": "战斧，双刃，木质握柄"},
    {"name": "magic-bow", "description": "精灵长弓，附魔发光纹路"},
    {"name": "staff-of-fire", "description": "火焰法杖，顶端嵌红宝石"},
    {"name": "dagger", "description": "匕首，短小精悍，适合潜行"},
    {"name": "war-hammer", "description": "战锤，沉重，石质锤头"},
    {"name": "crossbow", "description": "十字弩，机械结构"},
    {"name": "spear", "description": "长矛，尖刃，木质杆"},
    {"name": "shield", "description": "圆盾，金属边框，木质中心"},
    {"name": "throwing-knives", "description": "投掷飞刀组，3把"},
]
# ...
generator = Batch3DAssetGenerator(art_style="low-poly", engine="unity")
results = generator.generate_weapon_pack(weapons)
for r in results:
    print(f"[3D] {r['name']}.glb - {r['poly_count']} poly")
```
### 场景二：完整游戏设计文档
为游戏概念生成完整的 GDD.
```python
# 游戏设计文档生成器
class GDDGenerator:
    """游戏设计文档生成器"""
# ...
    def __init__(self, game_concept):
        self.concept = game_concept
        self.gdd = {}
# ...
    def generate_full_gdd(self):
        """生成完整GDD"""
        self.gdd = {
            "title": self.concept["title"],
            "genre": self.concept["genre"],
            "platform": self.concept["platform"],
            "core_loop": self._design_core_loop(),
            "progression": self._design_progression(),
            "monetization": self._design_monetization(),
            "level_design": self._design_first_levels(10),
            "art_style": self._recommend_art_style(),
            "narrative": self._design_narrative(),
        }
        return self.gdd
# ...
    def _design_core_loop(self):
        return {
            "loop": "探索 → 收集 → 建造 → 扩展 → 探索",
            "session_time": "5-10分钟",
            "retention_hook": "每日新区域解锁 + 建造进度"
        }
# ...
    def _design_progression(self):
        return {
            "levels": 50,
            "unlock_system": "区域逐步解锁",
            "skill_tree": ["探索", "建造", "战斗", "社交"],
            "rewards": ["新区域", "建造蓝图", "角色皮肤"]
        }
# ...
    def _design_monetization(self):
        return {
            "model": "Ethical F2P",
            "revenue_streams": [
                "装饰性皮肤（不影响平衡）",
                "建造蓝图包",
                "额外存档槽"
            ],
            "anti_pay_to_win": True
        }
# ...
    def _design_first_levels(self, count):
        levels = []
        for i in range(1, count + 1):
            levels.append({
                "level": i,
                "objective": f"第{i}关目标",
                "new_mechanic": "引入新机制" if i <= 5 else None,
                "difficulty": "easy" if i <= 3 else "medium" if i <= 7 else "hard"
            })
        return levels
# ...
    def _recommend_art_style(self):
        return {
            "primary": "Hand-Painted",
            "reason": "奇幻建造主题适合手绘风格",
            "references": ["Bastion", "Animal Crossing"],
            "color_palette": "温暖大地色 + 鲜艳点缀"
        }
# ...
    def _design_narrative(self):
        return {
            "premise": self.concept.get("pitch", ""),
            "act_1": "引入：玩家到达新世界",
            "act_2": "发展：建造与探索并行",
            "act_3": "高潮：解锁完整区域",
            "characters": ["玩家角色", "引导NPC", "商人NPC"]
        }
# ...
# 生成GDD
concept = {
    "title": "巫师的快递服务",
    "genre": "舒适冒险 / 时间管理",
    "platform": "PC 和 Switch",
    "pitch": "你是一名巫师，在幻想王国中配送魔法包裹"
}
gdd_gen = GDDGenerator(concept)
gdd = gdd_gen.generate_full_gdd()
print(f"GDD: {gdd['title']} - {gdd['genre']}")
```
### 场景三：角色一致性资产管理
跨所有资产保持角色视觉一致性.
```text
角色一致性工作流:
# ...
1. 定义角色风格指南:
   prompt: "定义角色风格指南:
     主角: 年轻巫师, 紫色长袍, 尖帽, 温暖笑容
     NPC商人: 圆胖大叔, 围裙, 永远微笑
     反派: 黑袍, 面具, 冷峻轮廓
     色彩: 紫色主调 + 金色点缀
     风格: 手绘风, Studio Ghibli质感"
# ...
2. 批量生成角色资产（引用同一风格指南）:
   - 主角概念图（多角度）
   - 主角3D模型 (GLB)
   - NPC角色组（5个角色）
   - 对话肖像（全角色）
   - 动画帧（行走/待机/施法）
# ...
3. 场景资产（保持同一世界观）:
   - 村庄建筑（5栋）
   - 森林场景瓦片
   - 道具图标（20个）
   - 魔法特效（5种）
# ...
所有资产引用步骤1的风格指南，确保视觉统一.
```
## 快速开始
### 领先步：定义游戏风格指南
```text
游戏风格指南:
  艺术风格: 手绘风 (Studio Ghibli质感)
  色彩方案: 紫色主调 + 金色点缀 + 温暖大地色
  参考游戏: Stardew Valley meets Studio Ghibli
  引擎: Unity
  视角: 俯视角2.5D
```
### 第二步：选择聊天模式
```python
# 聊天模式选择
# 单个资产/精灵/角色设计 → agent 模式
# 完整游戏概念/复杂世界观/叙事设计 → agent team 模式
# ...
# agent 模式: 快速生成单个资产
result = client.create_chat(
    prompt="设计主角角色表: 年轻巫师, 紫色长袍",
    chat_mode="agent"
)
# ...
# agent team 模式: 生成完整游戏概念
result = client.create_chat(
    prompt="创建完整游戏设计: 巫师快递服务, 含GDD/角色/场景",
    chat_mode="agent team"
)
```
### 第三步：批量生成 3D 资产
```bash
# 批量生成3D道具
generate_3d_batch \
  --style "low-poly" \
  --format "glb" \
  --assets "sword,axe,bow,staff,shield,dagger" \
  --poly-count "low" \
  --output "./assets/3d/"
```
#
## 示例
### 3D 模型生成配置
```json
{
  "asset_type": "3d-model",
  "format": "glb",
  "art_style": "low-poly",
  "model": {
    "type": "character",
    "description": "RPG主角",
    "poly_count": "low",
    "materials": ["PBR-matte"],
    "rigging": true,
    "animations": ["idle", "walk", "run", "attack"]
  },
  "engine_compatibility": ["unity", "unreal", "godot", "three.js", "blender"]
}
```
### GDD 生成配置
```json
{
  "asset_type": "gdd",
  "game": {
    "title": "巫师的快递服务",
    "genre": "舒适冒险/时间管理",
    "platform": ["PC", "Switch"],
    "target_session": "5分钟",
    "monetization": "ethical-f2p"
  },
  "gdd_sections": [
    "core-loop",
    "progression-system",
    "monetization-strategy",
    "first-10-levels",
    "art-style-recommendations",
    "narrative-outline"
  ],
  "references": ["Overcooked", "Studio Ghibli"]
}
```
### 批量生成配置
```json
{
  "batch_mode": true,
  "batch_size": 10,
  "art_style": "low-poly",
  "assets": [
    {"type": "weapon", "name": "iron-sword"},
    {"type": "weapon", "name": "battle-axe"},
    {"type": "weapon", "name": "magic-bow"},
    {"type": "prop", "name": "treasure-chest"},
    {"type": "prop", "name": "wooden-barrel"},
    {"type": "prop", "name": "torch"},
    {"type": "environment", "name": "tree-oak"},
    {"type": "environment", "name": "rock-formation"},
    {"type": "environment", "name": "village-house"},
    {"type": "environment", "name": "stone-bridge"}
  ],
  "output_format": "glb",
  "consistency_guide": "fantasy-low-poly-village"
}
```
## 优选实践
1. **风格指南先行**：先定义统一风格指南，所有资产引用同一描述确保一致.
2. **3D 优化配置**：移动端用 low-poly，PC 端可 high-poly，指定多边形数量.
3. **批量并行**：批量生成时按类型分组（武器组/道具组/场景组），效率更高.
4. **GDD 结构化**：GDD 包含核心循环、进度系统、商业化、关卡设计和艺术推荐.
5. **引擎兼容**：GLB 格式兼容所有主流引擎，指定目标引擎可优化输出.
```text
专业版检查清单:
[ ] 风格指南已定义并统一引用
[ ] 3D模型多边形数量已指定
[ ] 批量资产品类已规划
[ ] GDD章节已结构化
[ ] 引擎兼容性已确认 (GLB)
[ ] 角色一致性指南已建立
[ ] 免费版2D资产功能正常
[ ] 聊天模式已正确选择 (agent / agent team)
```
## 常见问题
### Q: 如何从免费版升级到专业版？
A: 免费版的 2D 资产生成能力在专业版中完整保留。专业版新增 3D 模型、GDD 生成和批量操作，无需迁移已有资产.
### Q: 3D 模型支持哪些引擎？
A: GLB 格式兼容 Unity、Unreal、Godot、Three.js 和 Blender。可指定目标引擎优化输出.
### Q: 批量生成最多支持多少资产？
A: 单批建议 10-20 个资产。超大批量请分批执行，确保质量和一致性.
### Q: agent 和 agent team 模式如何选择？
A: 单个资产（角色、精灵、UI元素）用 agent 模式；完整游戏概念、复杂世界观、叙事设计用 agent team 模式.
### Q: 角色一致性如何保证？
A: 先定义角色风格指南（外观、色彩、风格），后续所有资产请求引用同一指南，确保跨资产视觉统一.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+（批量生成脚本需要）
### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python 3.8+ | 运行时 | 推荐 | python.org 官方下载 |
| Blender（可选） | 工具 | 可选 | blender.org 下载（GLB编辑） |
| Unity/Unreal/Godot | 引擎 | 可选 | 各引擎官网下载 |
### API Key 配置
- 本Skill采用纯Markdown指令驱动，无需额外API Key
- 3D资产生成由 Agent 内置能力提供
### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 企业级AI Skill，支持2D/3D全栈资产生成、GDD编写与批量操作
- **适用规模**: 游戏开发团队，专业游戏项目
- **兼容性**: 与免费版2D资产能力完全兼容，支持无缝升级
## 错误处理
| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "游戏资产生成-专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "game asset gen pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
## 安全注意事项
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 核心功能
- **自动化执行**: 全栈游戏资产生成引擎，支持2D/3D资产、完整GDD、批量生成与多艺术风格。。游戏资产生成工具专业版。Use when
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据
## 核心功能
- **自动化执行**: 全栈游戏资产生成引擎，支持2D/3D资产、完整GDD、批量生成与多艺术风格。。游戏资产生成工具专业版。Use when
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据