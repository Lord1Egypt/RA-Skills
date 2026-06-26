---
name: clawhub-mirror
description: ClawHub镜像源管理技能。智能选择最佳镜像源，优先国内镜像，需要时使用VPN访问国外源。解决国内访问速度慢的问题。
---

# ClawHub 镜像源管理技能

## 使用场景

当用户需要：
- 提高ClawHub技能安装/更新速度
- 解决国内访问国外源慢的问题
- 自动选择最佳镜像源
- 需要VPN访问时自动提示

## 核心功能

### 1. 智能镜像选择
- 自动测试多个镜像源可用性
- 优先选择国内镜像（速度快）
- 国内不可用时自动切换到国外源
- 根据网络延迟选择最佳源

### 2. VPN支持
- 检测是否需要VPN访问
- 提供VPN使用提示
- 支持VPN连接后自动重试

### 3. 配置管理
- 自动保存最佳镜像配置
- 支持会话级和持久化配置
- 提供快速加载脚本

## 使用方法

### 基本使用
```powershell
# 运行智能配置
python skills/clawhub-mirror/scripts/setup-mirror.ps1

# 或直接运行PowerShell脚本
powershell -File skills/clawhub-mirror/scripts/setup-mirror.ps1
```

### 带参数使用
```powershell
# 仅测试不配置
python skills/clawhub-mirror/scripts/setup-mirror.ps1 -TestOnly

# 强制使用官方源（需要VPN）
python skills/clawhub-mirror/scripts/setup-mirror.ps1 -ForceOfficial

# 标记使用VPN
python skills/clawhub-mirror/scripts/setup-mirror.ps1 -UseVPN
```

### 快速加载配置
```powershell
# 加载已保存的最佳配置
. $env:USERPROFILE\.clawhub\load-mirror.ps1
```

## 镜像源策略

### 优先级顺序
1. **中国区官方镜像** (`https://cn.clawhub-mirror.com/`) - OpenClaw中国区官方镜像站，最高优先级
2. **国内镜像1** (`mirror.clawhub.cn`) - 备用国内源
3. **国内镜像2** (`clawhub.gitee.io`) - 备用国内源
4. **官方源** (`clawhub.ai`) - 国外官方源
5. **备用源** (`clawhub.net`) - 国外备用源

### 选择逻辑
1. 测试所有镜像源的可用性
2. 测量网络延迟（如果可能）
3. 优先选择可用的国内镜像
4. 国内不可用时选择延迟最低的国外源
5. 保存选择结果供后续使用

## 配置文件

### 位置
```
%USERPROFILE%\.clawhub\
├── mirror-config.json      # 镜像配置
└── load-mirror.ps1        # 快速加载脚本
```

### 配置示例
```json
{
  "SelectedMirror": {
    "Name": "中国区官方镜像",
    "Site": "https://cn.clawhub-mirror.com",
    "Registry": "https://cn.clawhub-mirror.com",
    "Type": "china_mirror",
    "Priority": 1,
    "Description": "ClawHub 中国区镜像，持续收录和镜像加速高质量 Skill",
    "SelectedAt": "2026-04-02 21:08:00"
  },
  "AvailableMirrors": [
    {
      "Name": "中国区官方镜像",
      "Site": "https://cn.clawhub-mirror.com",
      "Registry": "https://cn.clawhub-mirror.com",
      "Type": "china_mirror",
      "Priority": 1,
      "Description": "ClawHub 中国区镜像，持续收录和镜像加速高质量 Skill",
      "Latency": 35,
      "Available": true
    }
  ]
}
```

## VPN使用指南

### 何时需要VPN
1. 所有国内镜像都不可用时
2. 需要访问官方最新技能时
3. 遇到网络限制或防火墙时

### VPN配置提示
当脚本检测到需要VPN时，会显示：
```
⚠️  需要VPN访问国外源
建议：
1. 连接您的VPN
2. 重新运行脚本：setup-mirror.ps1 -UseVPN
3. 或手动设置环境变量：
   CLAWHUB_SITE=https://clawhub.ai
   CLAWHUB_REGISTRY=https://api.clawhub.ai
```

### 无线VPN访问
如果用户可以通过无线方式访问VPN，脚本会适应这种配置。

## 集成到PowerShell Profile

### 自动加载配置
将以下内容添加到 `$PROFILE` 文件中：

```powershell
# ClawHub 镜像源自动加载
if (Test-Path "$env:USERPROFILE\.clawhub\load-mirror.ps1") {
    . "$env:USERPROFILE\.clawhub\load-mirror.ps1"
}
```

### 创建Profile文件（如果不存在）
```powershell
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}
notepad $PROFILE
```

## 故障排除

### 常见问题

#### 1. 所有镜像都不可用
```powershell
# 检查网络连接
Test-NetConnection -ComputerName clawhub.ai -Port 443

# 尝试使用VPN后重试
setup-mirror.ps1 -UseVPN
```

#### 2. 国内镜像访问慢
```powershell
# 强制使用官方源（需要VPN）
setup-mirror.ps1 -ForceOfficial
```

#### 3. 环境变量不生效
```powershell
# 手动设置环境变量
$env:CLAWHUB_SITE = "https://clawhub.ai"
$env:CLAWHUB_REGISTRY = "https://api.clawhub.ai"

# 验证设置
echo $env:CLAWHUB_SITE
echo $env:CLAWHUB_REGISTRY
```

### 手动配置
如果自动配置失败，可以手动设置：

```powershell
# 中国区官方镜像（最高优先级）
$env:CLAWHUB_SITE = "https://cn.clawhub-mirror.com"
$env:CLAWHUB_REGISTRY = "https://cn.clawhub-mirror.com"

# 国内网络（备用）
$env:CLAWHUB_SITE = "https://mirror.clawhub.cn"
$env:CLAWHUB_REGISTRY = "https://api.mirror.clawhub.cn"

# 或使用官方源（需要VPN）
$env:CLAWHUB_SITE = "https://clawhub.ai"
$env:CLAWHUB_REGISTRY = "https://api.clawhub.ai"
```

## 使用示例

### 示例1：首次配置
```powershell
# 运行智能配置
python skills/clawhub-mirror/scripts/setup-mirror.ps1

# 输出示例：
# ✅ 选择最佳镜像源：国内镜像1 (延迟: 45ms)
# ✅ 配置完成！现在可以使用 clawhub 命令了
```

### 示例2：VPN环境配置
```powershell
# 连接VPN后运行
python skills/clawhub-mirror/scripts/setup-mirror.ps1 -UseVPN

# 或强制使用官方源
python skills/clawhub-mirror/scripts/setup-mirror.ps1 -ForceOfficial
```

### 示例3：日常使用
```powershell
# 新PowerShell会话中快速加载
. $env:USERPROFILE\.clawhub\load-mirror.ps1

# 安装技能（使用最佳镜像）
clawhub install data-analysis-litiao
```

## 注意事项

1. **镜像可用性**：国内镜像可能不稳定，脚本会自动处理
2. **VPN要求**：访问国外源可能需要VPN，脚本会明确提示
3. **网络环境**：不同网络环境可能需要不同配置
4. **定期更新**：建议定期运行脚本更新最佳镜像选择

## 性能优势

- **国内镜像**：延迟通常 <100ms，下载速度快
- **智能选择**：自动避开不可用或慢的镜像
- **持久化配置**：一次配置，多次使用
- **VPN友好**：明确提示VPN需求，避免混淆

通过使用此技能，您可以显著提高ClawHub技能安装和更新的速度，特别是在国内网络环境下。