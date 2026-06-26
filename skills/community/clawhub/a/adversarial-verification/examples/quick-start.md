# 🚀 快速开始

## 安装
```bash
clawhub install adversarial-verification
```

## 基本使用

### 验证前端项目
```bash
openclaw skill adversarial-verification --target frontend --path ./my-app
```

### 验证CLI脚本
```bash
openclaw skill adversarial-verification --target cli --path ./bin/my-tool
```

## 自动集成

### Git提交前验证
```bash
# .git/hooks/pre-commit
#!/bin/bash
openclaw skill adversarial-verification --target frontend --path . || exit 1
```

### 手动验证命令
```bash
# 写完代码后验证
openclaw skill adversarial-verification --target frontend --path ./src

# 修复bug后验证  
openclaw skill adversarial-verification --target frontend --path . --strict
```

## 核心特性

### 🚨 借口识别
检测自我欺骗念头：
- "代码看起来正确"
- "这是个简单变更，应该能工作"
- "测试会发现问题"
- "我时间不够了"

**识别到这些念头，做相反的事！**

### ✅ 真实执行
- 必须跑真实命令，只看代码不算验证
- 前端：检查package.json + 安装依赖 + 构建
- CLI：测试帮助选项 + 空输入处理

### 🎯 明确判决
- **PASS**：所有验证通过
- **FAIL**：任一验证失败
- 不能模糊，必须明确结果

## 立即生效
**安装后**：下次我写代码就会自动使用对抗性验证，确保代码质量！