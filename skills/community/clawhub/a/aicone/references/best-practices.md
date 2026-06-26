# AI 机器人克隆最佳实践

## 🎯 克隆策略

### 完整克隆 vs 精简克隆

**完整克隆**（推荐用于备份）
```bash
python scripts/clone_robot.py \
  --source /path/to/source \
  --output full-clone.zip
```
包含：核心文件 + 所有可选目录

**精简克隆**（推荐用于快速复制）
```bash
python scripts/clone_robot.py \
  --source /path/to/source \
  --output lite-clone.zip \
  --no-optional
```
仅包含：核心文件（SOUL.md, MEMORY.md 等）

---

## 📋 克隆前检查清单

### 源环境准备
- [ ] 确认核心文件完整
- [ ] 清理临时文件和日志
- [ ] 移除敏感 API Keys（或单独备份）
- [ ] 检查记忆文件是否需要精简

### 目标环境准备
- [ ] 确认目标路径有写入权限
- [ ] 备份目标环境现有配置（如有）
- [ ] 准备环境变量配置

---

## 🔐 安全建议

### 敏感信息处理

**方案 A：排除敏感文件**
```bash
# 创建排除列表
cat > exclude.txt << EOF
*.env
*api_key*
*secret*
*token*
EOF

# 使用排除列表（需要自定义脚本）
python scripts/clone_robot.py --exclude exclude.txt ...
```

**方案 B：单独加密备份**
```bash
# 加密敏感配置
gpg -c MEMORY.md  # 创建 MEMORY.md.gpg

# 解密
gpg -d MEMORY.md.gpg > MEMORY.md
```

### 传输安全
- 使用加密通道（SSH/HTTPS）
- 克隆包设置密码保护
- 传输后立即删除临时文件

---

## 🧩 跨平台克隆

### Linux → Linux
```bash
# 直接复制即可
python scripts/clone_robot.py --source /home/user/.workspace --output clone.zip
python scripts/clone_robot.py --unpack clone.zip --target /home/newuser/.workspace
```

### Linux → macOS
```bash
# 注意路径差异
# Linux: /home/user/.openclaw/workspace
# macOS: /Users/user/.openclaw/workspace

# 克隆后更新路径配置
sed -i '' 's|/home/|/Users/|g' TOOLS.md
```

### Linux → Windows (WSL)
```bash
# WSL 路径：/home/user/.openclaw/workspace
# Windows 路径：C:\Users\user\.openclaw\workspace

# 克隆后使用 PowerShell 更新路径
(Get-Content TOOLS.md) -replace '/home/', 'C:\Users\' | Set-Content TOOLS.md
```

---

## 📊 克隆大小优化

### 减小克隆包体积

**1. 排除大文件**
```python
# 修改脚本中的 OPTIONAL_DIRS
OPTIONAL_DIRS = [
    "memory/",           # 保留
    # "skills/",         # 排除（如果太大）
    # "marketing/",      # 排除（图片多）
]
```

**2. 压缩图片资源**
```bash
# 压缩营销图片
find marketing/images -name "*.png" -exec pngquant {} \;
```

**3. 精简记忆文件**
```bash
# 只保留最近 7 天记忆
find memory/ -name "*.md" -mtime +7 -delete
```

---

## 🔄 版本管理

### 克隆包版本命名
```
machine-cat-clone-v1.0-20260304.zip
machine-cat-clone-v1.1-20260315.zip
machine-cat-clone-v2.0-20260401.zip
```

### 变更记录
在克隆包中增加 `CHANGELOG.md`：
```markdown
# 变更日志

## v2.0 - 2026-04-01
- 新增：GIS+AI 趋势分析能力
- 更新：21 张专属配图
- 优化：小红书发布流程

## v1.0 - 2026-03-04
- 初始版本
- 包含核心配置和记忆
```

---

## 🧪 测试验证

### 克隆后验证脚本
```bash
#!/bin/bash
# verify_clone.sh

echo "🔍 验证克隆完整性..."

# 检查核心文件
for file in SOUL.md IDENTITY.md USER.md MEMORY.md HEARTBEAT.md; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (缺失)"
        exit 1
    fi
done

# 检查记忆目录
if [ -d "memory" ]; then
    count=$(ls memory/*.md 2>/dev/null | wc -l)
    echo "  ✅ memory/ ($count 文件)"
else
    echo "  ⚠️  memory/ (不存在)"
fi

# 检查技能包
if [ -d "skills" ]; then
    count=$(ls -d skills/*/ 2>/dev/null | wc -l)
    echo "  ✅ skills/ ($count 技能)"
else
    echo "  ⚠️  skills/ (不存在)"
fi

echo "✅ 验证通过！"
```

---

## 🚀 批量部署

### 多环境同步
```bash
#!/bin/bash
# deploy_to_multiple.sh

CLONE_FILE="machine-cat-clone.zip"
TARGETS=(
    "/home/user1/.openclaw/workspace"
    "/home/user2/.openclaw/workspace"
    "/home/user3/.openclaw/workspace"
)

for target in "${TARGETS[@]}"; do
    echo "📦 部署到：$target"
    python scripts/clone_robot.py \
        --unpack "$CLONE_FILE" \
        --target "$target"
    
    if [ $? -eq 0 ]; then
        echo "  ✅ 成功"
    else
        echo "  ❌ 失败"
    fi
done
```

---

## 📈 性能优化

### 大工作区克隆优化

**增量克隆**（仅复制变更文件）
```bash
# 创建增量包
rsync -av --delete \
    --exclude='.git/' \
    /source/workspace/ \
    /backup/incremental/

# 打包增量
cd /backup/incremental && zip -r incremental-clone.zip .
```

**并行处理**
```bash
# 使用多核压缩
pigz -p 4 large-clone.zip
```

---

## 🛠️ 故障排查

### 常见问题

**Q: 克隆后无法启动**
```bash
# 检查文件权限
chmod -R 755 /path/to/workspace

# 检查 Python 环境
python3 --version
pip3 list | grep openclaw
```

**Q: 记忆文件丢失**
```bash
# 检查克隆包内容
unzip -l clone.zip | grep memory

# 手动解压记忆目录
unzip clone.zip "memory/*" -d /target/path
```

**Q: 技能包不生效**
```bash
# 重新加载技能
openclaw skills reload

# 检查技能目录
ls -la skills/
```

---

*最后更新：2026-03-04*  
*机器猫 🐱 维护*
