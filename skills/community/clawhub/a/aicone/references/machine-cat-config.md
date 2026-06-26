# 机器猫克隆配置

## 🐱 机器猫专属文件清单

### 核心身份文件
```
/workspace/SOUL.md          # 人格：温暖、幽默、主动
/workspace/IDENTITY.md      # 身份：机器猫 (Machine Cat)
/workspace/USER.md          # 用户：木头 (高德云图市场运营)
/workspace/MEMORY.md        # 长期记忆和偏好
/workspace/HEARTBEAT.md     # 每日任务机制
/workspace/TOOLS.md         # 本地工具配置
/workspace/AGENTS.md        # Agent 配置
```

### 核心能力目录
```
/workspace/memory/                    # 每日记忆
/workspace/skills/xiaohongshu-mcp/    # 小红书 MCP 技能
/workspace/skills/nano-banana-pro/    # 图片生成技能
/workspace/skills/content-creator/    # 内容创作技能
/workspace/scripts/                   # 自动化脚本
```

### 运营资产
```
/workspace/marketing/images/v3/       # 21 张专属配图
/workspace/projects/xiaohongshu-workflow/  # 小红书工作流
/workspace/docs/                      # 文档资料
```

---

## 📦 机器猫克隆命令

### 快速克隆（推荐）
```bash
cd /home/admin/.openclaw/workspace/skills/ai-clone

# 扫描
python scripts/clone_robot.py --scan /home/admin/.openclaw/workspace

# 创建克隆包
python scripts/clone_robot.py \
  --source /home/admin/.openclaw/workspace \
  --output machine-cat-clone-$(date +%Y%m%d).zip
```

### 精简克隆（仅核心能力）
```bash
python scripts/clone_robot.py \
  --source /home/admin/.openclaw/workspace \
  --output machine-cat-lite.zip \
  --no-optional
```

### 完整克隆（包含所有资产）
```bash
python scripts/clone_robot.py \
  --source /home/admin/.openclaw/workspace \
  --output machine-cat-full.zip
```

---

## 🎯 机器猫核心能力

### 1. 小红书运营能力
- MCP 服务器集成
- 自动发布笔记
- 配图生成和管理
- 数据监控和评论回复

### 2. 内容创作能力
- 文案生成和优化
- SEO 优化
- 品牌 voice 分析
- 多平台内容适配

### 3. 图片生成能力
- 通义万相集成
- Nano Banana Pro 集成
- 专属配图定制
- 批量生成和管理

### 4. 任务执行能力
- HEARTBEAT 机制
- 定时任务管理
- 自动汇报机制
- 记忆和经验积累

---

## 📋 克隆后配置清单

### 必须重新配置
- [ ] API Keys (DASHSCOPE_API_KEY, GEMINI_API_KEY 等)
- [ ] MCP 服务器登录状态
- [ ] 飞书应用配置
- [ ] 环境变量

### 可选配置
- [ ] 自定义技能
- [ ] 本地工具路径
- [ ] 特定项目配置

### 验证步骤
```bash
# 1. 检查核心文件
cat SOUL.md | head -10

# 2. 检查记忆
cat MEMORY.md

# 3. 检查技能
ls skills/

# 4. 启动测试
openclaw status
```

---

## 🔄 版本历史

### v1.0 - 2026-03-04
- 初始版本
- 包含小红书运营全套能力
- 21 张专属配图
- 6 篇发布内容经验
- 自动化发布流程

---

*机器猫 🐱 配置*  
*最后更新：2026-03-04*
