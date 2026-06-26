---
name: clawhub-publisher-tool
description: |
  一键发布技能到ClawHub平台。自动完成登录、版本更新、发布全流程。
  适用场景：
  - "帮我发布这个技能"
  - "升级技能到新版本"
  - "把编辑助手发布到ClawHub"
  - "发布技能"
metadata:
  version: 1.0.3
---

# ClawHub Publisher - 技能发布助手

## 功能说明

快速将本地技能发布到 ClawHub 平台，支持版本自动升级。

## 发布步骤

### 1. 准备阶段

确认要发布的技能：
- 技能目录：`~/agents/skills/<技能名>`
- 技能必须包含 `SKILL.md` 文件
- **必须包含 `package.json`** 文件，包含以下字段：
  - `displayName` 或 `display_name`：发布到 ClawHub 显示的名称（**必填**）
  - `version`：当前版本号
  - `name`：技能 slug

**SKILL.md 结构规范**：

SKILL.md 的 frontmatter 部分，**只有 `name` 和 `description` 在顶层**，其他所有属性都放在 `metadata` 下：

```yaml
---
name: skill-name                    # 顶层：技能名
description: |                      # 顶层：描述
  技能描述...
metadata:                           # 所有其他属性放 metadata 下
  version: 1.0.0
  author: your-name
  homepage: https://clawhub.ai/skills/skill-name
  tags:
    - skill
  openclaw:
    requires:
      env.vars: {}
  dependencies: []                  # 依赖技能
  config: {}                        # 配置字段
---
```

❌ **错误示例**（其他属性放在顶层）：
```yaml
---
name: skill-name
description: |
  技能描述
version: 1.0.0                       # ❌ 错误：应放在 metadata 下
dependencies: []                     # ❌ 错误：应放在 metadata 下
config: {}                           # ❌ 错误：应放在 metadata 下
---
```

✅ **正确示例**：
```yaml
---
name: skill-name
description: |
  技能描述
metadata:
  version: 1.0.0
  author: your-name
  # ... 其他属性
---
```

### 2. 确定版本号

**从 `package.json` 读取版本**：

```bash
# 读取 package.json 中的 displayName（用于发布名称，兼容 display_name）
node -p "require('./package.json').displayName || require('./package.json').display_name"

# 读取 package.json 中的 version
node -p "require('./package.json').version"
```

版本号递增规则：
- 修复bug → 补丁版本 +1（1.2.0 → 1.2.1）
- 新功能 → 次版本 +1（1.2.0 → 1.3.0）
- 重大更新 → 主版本 +1（1.2.0 → 2.0.0）

### 3. 更新版本

编辑 `package.json` 更新版本号：

```json
{
  "name": "editor-assistant",
  "displayName": "小编助手",
  "version": "1.4.0",
  "description": "帮你创作超有个人风格的公众号/小红书推文"
}
```

**同时必须更新 `SKILL.md` 中的 `metadata.version`**：

```yaml
---
name: editor-assistant
description: |
  小编助手...
metadata:
  version: 1.4.0
  author: your-name
  homepage: https://clawhub.ai/skills/editor-assistant
---
```

### 4. 登录 ClawHub（如未登录）

```bash
clawhub login --token "<你的token>" --no-browser
```

### 5. 发布技能

**发布前必须校验三处版本一致性，缺一不可：**

1. `package.json` 中的 `version`
2. `SKILL.md` 中 `metadata.version`（或顶级 `version:` 字段）
3. `clawhub publish` 命令的 `--version` 参数

```powershell
SKILL_DIR="~/agents/skills/<技能名>"

# 1. 读取 package.json 版本
$PKG_VERSION = node -p "require('$SKILL_DIR/package.json').version" 2>$null
if ([string]::IsNullOrEmpty($PKG_VERSION)) { $PKG_VERSION = $null }

# 2. 读取 SKILL.md metadata.version（优先）或顶级 version:
$SKILL_META_VERSION = $null
if (Select-String -Path "$SKILL_DIR/SKILL.md" -Pattern "^\s*metadata:" -Quiet) {
    $SKILL_META_VERSION = Select-String -Path "$SKILL_DIR/SKILL.md" -Pattern "^\s+version:" | Select-Object -First 1 | ForEach-Object { ($_ -split ":")[1].Trim() }
}
if ([string]::IsNullOrEmpty($SKILL_META_VERSION)) {
    $SKILL_META_VERSION = Select-String -Path "$SKILL_DIR/SKILL.md" -Pattern "^\s*version:" | Select-Object -First 1 | ForEach-Object { ($_ -split ":")[1].Trim() }
}

# 3. 读取 package.json displayName
$DISPLAY_NAME = node -p "require('$SKILL_DIR/package.json').displayName || require('$SKILL_DIR/package.json').display_name" 2>$null

Write-Host "📋 版本校验（三处必须完全一致）:"
Write-Host "   package.json version:        $PKG_VERSION"
Write-Host "   SKILL.md metadata.version:   $SKILL_META_VERSION"
Write-Host "   displayName:                $DISPLAY_NAME"

# 校验
if ([string]::IsNullOrEmpty($PKG_VERSION) -or [string]::IsNullOrEmpty($SKILL_META_VERSION)) {
    Write-Host "⚠️  错误: 版本信息不完整！"
    Write-Host "   请确保 package.json 和 SKILL.md 都设置了 version。"
    exit 1
}

if ($PKG_VERSION -ne $SKILL_META_VERSION) {
    Write-Host "⚠️  错误: 版本不一致！"
    Write-Host "   package.json version: $PKG_VERSION"
    Write-Host "   SKILL.md metadata.version: $SKILL_META_VERSION"
    Write-Host "   请先修复版本不一致问题，再发布。"
    exit 1
}
Write-Host "✅ 版本校验通过"
```

**修复版本不一致的方法：**

如果发现 package.json 和 SKILL.md 版本不一致，先确定要使用哪个版本（如 1.4.0），然后同时更新两处：

```powershell
# 更新 package.json
$pkg = Get-Content "$SKILL_DIR/package.json" | ConvertFrom-Json
$pkg.version = "1.4.0"
$pkg | ConvertTo-Json | Set-Content "$SKILL_DIR/package.json"

# 更新 SKILL.md metadata.version
(Get-Content "$SKILL_DIR/SKILL.md") -replace '^\s+version:\s*.*', "  version: 1.4.0" | Set-Content "$SKILL_DIR/SKILL.md"
```

**版本一致后，读取配置进行发布：**

```bash
DISPLAY_NAME=$(node -p "require('$SKILL_DIR/package.json').displayName || require('$SKILL_DIR/package.json').display_name")
VERSION=$(node -p "require('$SKILL_DIR/package.json').version")
SKILL_NAME=$(node -p "require('$SKILL_DIR/package.json').name")

clawhub publish "$SKILL_DIR" \
    --slug "$SKILL_NAME" \
    --name "$DISPLAY_NAME" \
    --version "$VERSION" \
    --changelog "<更新说明>"
```

**示例：**
```bash
clawhub publish "~/agents/skills/editor-assistant" \
    --slug editor-assistant \
    --name "小编助手" \
    --version 1.4.0 \
    --changelog "v1.4.0: 添加配置管理和依赖技能说明"
```

### 5.5 使用技能自带的 publish.sh（可选）

如果技能目录包含 `publish.sh`，可以直接运行：

```bash
cd <技能目录>
./publish.sh [版本号] [更新说明]
```

该脚本会自动读取 `package.json` 中的配置。

---

## 常用命令

| 操作 | 命令 |
|------|------|
| 登录 | `clawhub login --token "<token>" --no-browser` |
| 查看当前用户 | `clawhub whoami` |
| 发布技能 | `clawhub publish "<路径>" --slug <slug> --name <显示名> --version <ver> --changelog "<说明>"` |
| 查看帮助 | `clawhub publish --help` |

## Token 配置

Token 存储在配置文件中，首次登录后无需重复登录：
- Windows: `%USERPROFILE%\.clawhub\config.json`
- macOS/Linux: `~/.clawhub/config.json`

## 注意事项

1. **版本号不能降级** - ClawHub 不允许发布低于当前版本的版本
2. **slug 必须唯一** - 如果 slug 已被使用，会发布为新版本
3. **changelog 必填** - 必须提供版本更新说明
4. **路径包含中文** - Windows 路径有中文可能影响，建议使用英文路径
5. **displayName 必填** - package.json 中必须包含 displayName 或 display_name，否则发布后显示名称不正确
6. **三处版本必须一致**：package.json version、SKILL.md metadata.version、clawhub publish --version

---

> 🚀 有了这个技能，发布技能就像发朋友圈一样简单！
