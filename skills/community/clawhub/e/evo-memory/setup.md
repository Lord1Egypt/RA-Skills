# Self-Evolution 安装指南

## 1. 部署 bootstrap hook

```bash
# 创建 hook 目录
mkdir -p ~/.openclaw/hooks/self-evolution

# 复制 hook 文件
cp ~/.openclaw/workspace/self-evolution/hooks/bootstrap.js ~/.openclaw/hooks/self-evolution/handler.js

# 创建 HOOK.md
cat > ~/.openclaw/hooks/self-evolution/HOOK.md << 'EOF'
---
name: self-evolution
description: "Injects self-evolution skill during agent bootstrap"
metadata: {"openclaw":{"emoji":"🧬","events":["agent:bootstrap"]}}
---
# Self-Evolution Bootstrap Hook
Injects SKILL.md on every agent bootstrap for continuous self-improvement.
EOF

# 启用 hook
openclaw hooks enable self-evolution
```

## 2. 赋予脚本执行权限

```bash
chmod +x ~/.openclaw/workspace/self-evolution/hooks/signal-detector.sh
chmod +x ~/.openclaw/workspace/self-evolution/hooks/error-detector.sh
```

## 3. 重启 gateway

```bash
openclaw gateway restart
sleep 3
openclaw status
```

## 4. 验证

```bash
# 检查 hook 是否就绪
openclaw hooks list | grep self-evolution

# 检查技能是否加载
openclaw skills list | grep self-evolution

# 检查目录结构
ls -la ~/.openclaw/workspace/self-evolution/
```
