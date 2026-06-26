# Aegis Protocol - 发布指南

**最后更新**: 2026-04-05  
**当前版本**: v0.7.0

---

## 📦 发布流程

### 发布前检查清单

- [ ] 更新版本号 (semver: major.minor.patch)
- [ ] 更新 `_meta.json` 中的 version
- [ ] 更新 `SKILL.md` 中的 version
- [ ] 运行测试确保通过
- [ ] 更新 Changelog
- [ ] Git 提交并打 tag

---

## 🐙 GitHub 发布

### 方式 1: 直接推送 (小更新)

```bash
cd /root/.openclaw/workspace/skills/aegis-protocol

# 提交更改
git add -A
git commit -m "fix: 描述你的更改

详细说明..."

# 推送
git push origin main
```

### 方式 2: 打 Tag 发布 (大版本)

```bash
cd /root/.openclaw/workspace/skills/aegis-protocol

# 打 tag
git tag -a v0.8.0 -m "Release v0.8.0

新功能:
- 新功能 1
- 新功能 2

修复:
- Bug 修复 1"

# 推送 tag
git push origin v0.8.0
```

### 方式 3: GitHub Release (正式发行)

1. 访问：https://github.com/ankechenlab-node/aegis-protocol/releases/new
2. Tag version: `v0.8.0`
3. Release title: `Aegis Protocol v0.8.0`
4. 描述更改内容
5. 点击 "Publish release"

---

## 🦞 ClawHub 发布

### 前提条件

**Token 位置**:
- Linux/Mac: `~/.clawhub/token.json`
- Windows: `%USERPROFILE%\.clawhub\token.json`

**Token 格式**:
```json
{"token": "clh_xxxxxxxxxxxx"}
```

### 发布命令

```bash
cd /root/.openclaw/workspace

# 发布新版本
clawhub publish skills/aegis-protocol \
  --slug aegis-protocol \
  --name "Aegis Protocol" \
  --version 0.8.0 \
  --tags "monitoring,stability,self-healing,watchdog,openclaw" \
  --changelog "v0.8.0 - 描述主要改进"
```

### 验证发布

```bash
# 搜索技能
clawhub search aegis-protocol

# 检查详情
clawhub inspect aegis-protocol

# 测试安装
clawhub install aegis-protocol --dry-run
```

---

## 📝 版本号规则 (SemVer)

格式：`MAJOR.MINOR.PATCH` (如：0.7.0)

### 何时增加 MAJOR (主版本)
- 破坏性变更
- 不兼容的 API 修改
- 架构重构

示例：`0.7.0` → `1.0.0`

### 何时增加 MINOR (次版本)
- 新功能 (向后兼容)
- 功能增强
- 新增检查维度

示例：`0.7.0` → `0.8.0`

### 何时增加 PATCH (补丁版本)
- Bug 修复
- 性能优化
- 文档更新

示例：`0.7.0` → `0.7.1`

---

## 🔄 完整发布流程示例

### 场景：发布 v0.8.0 (新功能)

```bash
# 1. 更新版本号
# 编辑以下文件的 version 字段:
# - _meta.json
# - SKILL.md
# - README.md (如有)

# 2. 运行测试
cd /root/.openclaw/workspace/skills/aegis-protocol
python3 -m pytest tests/ -v

# 3. Git 提交
cd /root/.openclaw/workspace
git add -A
git commit -m "feat: 发布 v0.8.0

新功能:
- 新增 XX 检查
- 优化 XX 性能

改进:
- XX 优化"

# 4. GitHub 推送
cd skills/aegis-protocol
git push origin main

# 5. (可选) 打 tag
git tag -a v0.8.0 -m "Release v0.8.0"
git push origin v0.8.0

# 6. ClawHub 发布
cd /root/.openclaw/workspace
clawhub publish skills/aegis-protocol \
  --slug aegis-protocol \
  --version 0.8.0 \
  --tags "monitoring,stability,self-healing,watchdog,openclaw" \
  --changelog "v0.8.0 - 新增 XX 检查，优化 XX 性能"

# 7. 验证
clawhub inspect aegis-protocol
```

---

## 🚨 常见问题

### Q: Token 过期了怎么办？

```bash
# 本地重新登录获取新 Token
clawhub login

# 复制新 Token
cat ~/.clawhub/token.json
```

### Q: 发布失败 "Skill already exists"？

这是正常的，表示是更新而非首次发布。继续执行即可。

### Q: 如何删除已发布的版本？

```bash
# 删除 ClawHub 版本
clawhub delete aegis-protocol --version 0.7.0

# 删除 GitHub tag
cd skills/aegis-protocol
git tag -d v0.7.0
git push origin :refs/tags/v0.7.0
```

### Q: 如何发布紧急 Bug 修复？

```bash
# PATCH 版本更新
# 0.7.0 → 0.7.1

clawhub publish skills/aegis-protocol \
  --version 0.7.1 \
  --changelog "v0.7.1 - 紧急修复 XX 问题"
```

---

## 📊 发布记录

| 版本 | 日期 | 平台 | 状态 |
|------|------|------|------|
| v0.7.0 | 2026-04-05 | GitHub + ClawHub | ✅ 已发布 |

---

## 🔐 Token 安全

- ⚠️ **不要** 将 Token 提交到 Git
- ⚠️ **不要** 在公开场合分享 Token
- ✅ 定期更换 Token
- ✅ 使用 `--label` 标识不同用途的 Token

```bash
# 生成专用 Token
clawhub login --label "aegis-vps-publish"
```

---

*发布指南 - Aegis Protocol* 🛡️
