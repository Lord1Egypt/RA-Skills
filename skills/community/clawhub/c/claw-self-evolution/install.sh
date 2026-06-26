#!/bin/bash
# claw-self-evolution 安装脚本
# 安装完整安全可控自我进化闭环

set -e

echo "🚀 开始安装 claw-self-evolution..."

# 确认工作目录
WORKDIR="/app/working"
FILESDIR="$(dirname "$0")/files"

# 创建必要目录
mkdir -p "$WORKDIR/scripts/system/maintenance"
mkdir -p "$WORKDIR/memory/learnings"

# 复制所有脚本
echo "📝 复制脚本文件..."
for file in "$FILESDIR"/*.py; do
    filename=$(basename "$file")
    cp "$file" "$WORKDIR/scripts/system/maintenance/$filename"
    chmod +x "$WORKDIR/scripts/system/maintenance/$filename"
    echo "  ✓ $filename"
done

# 创建学习记录目录和初始文件
echo "📚 创建学习记录目录..."
cat > "$WORKDIR/memory/learnings/ERRORS.md" << 'EOF'
# 🚨 错误记录 - Self-Improvement Learning Log

记录操作失败、API错误、工具错误等，避免下次再踩坑。

格式：
```
## YYYY-MM-DD - [错误主题]

### 场景：
[发生了什么]

### 错误原因：
[为什么错了]

### 正确做法：
[下次应该怎么做]

### 参见：
- [相关链接/参考]
```

---
EOF

cat > "$WORKDIR/memory/learnings/LEARNINGS.md" << 'EOF'
# 🧠 经验教训 - Self-Improvement Learning Log

记录用户纠正、知识更新、最佳实践。

分类：
- `correction` - 用户纠正了我的错误
- `knowledge_gap` - 我的知识过时了，需要更新
- `best_practice` - 发现了更好的方法

格式：
```
## YYYY-MM-DD - [主题]
**分类**: correction/knowledge_gap/best_practice

### 原来的错误认知/做法：
[错误内容]

### 正确的认知/做法：
[正确内容]

### 为什么这个更好：
[原因]

### 参见：
- [相关链接/参考]
```

---
EOF

cat > "$WORKDIR/memory/learnings/FEATURE_REQUESTS.md" << 'EOF'
# 🚀 功能需求 - Self-Improvement Learning Log

记录用户想要但还没有的功能，每周自省的时候汇总考虑实现。

格式：
```
## YYYY-MM-DD - [功能名称]

### 需求描述：
[用户想要什么功能]

### 使用场景：
[什么时候会用到]

### 优先级：
high/medium/low

### 状态：
- [ ] 未实现
- [ ] 实现中
- [x] 已完成
```

---
EOF

echo "✅ 创建学习记录初始文件完成"

# 添加权限说明
echo ""
echo "=================================================="
echo "✅ 安装完成！"
echo ""
echo "claw-self-evolution 已经安装成功："
echo "  - 脚本位置: $WORKDIR/scripts/system/maintenance/"
echo "  - 学习记录: $WORKDIR/memory/learnings/"
echo ""
echo "📋 功能清单："
echo "  1. 📝 持续学习记录 - 错误/教训/需求分类记录"
echo "  2. 🧹 每日自检 - 自动检查规范一致性、安全基线"
echo "  3. 🚀 每周架构扫描 - 自动发现优化点"
echo "  4. 🧠 每周自省反思 - 自动总结一周工作，提取改进点"
echo "  5. 🧪 安全实验闭环 - 隔离实验，必须批准才合并"
echo "  6. 👤 自动用户画像 - 每天学习用户偏好"
echo "  7. 💓 服务健康检查 - 每15分钟检查，异常自动恢复"
echo "  8. 💾 自动核心备份 - 每天备份核心配置"
echo "  9. 🧹 自动日志清理 - 保留30天，自动清理"
echo "  10. 🔍 目录结构验证 - 保持OpenClaw规范"
echo ""
echo "🔐 安全设计："
echo "  - 所有改进必须走安全实验闭环"
echo "  - 隔离实验，不碰生产直到用户批准"
echo "  - 合并前自动备份，随时可以回滚"
echo "  - 修改核心配置需要二次确认"
echo ""
echo "🎉 享受持续安全进化！"
echo "=================================================="
