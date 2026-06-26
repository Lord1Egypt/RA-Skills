---
name: china-mirrors
description: 自动配置 Python pip、npm、yarn、pnpm、cargo、go mod、NuGet、RubyGems、Conda、Homebrew、Gradle 等包管理器的国内镜像源。使用当用户提到下载慢、安装依赖、配置镜像、加速包下载、设置国内源，或在中国大陆开发需要加速依赖安装时。支持阿里云、腾讯云、清华大学、中科大、华为云等主流镜像。检测到 package.json、requirements.txt、Cargo.toml、go.mod、Gemfile、.nuspec、environment.yml 等文件时主动建议使用此技能。
version: 2.0.0
type: SKILL
license: MIT
author: normdist-ai
---

# 中国国内镜像源配置技能（Agent 自执行版）

> **核心设计理念**：本技能不附带任何预置脚本。Agent 应根据本文档的指导，**直接在用户计算机上编写并执行配置命令**，实现镜像源配置功能。

## 工作流程（Agent 必须遵循）

### Phase 1: 需求检测与环境分析

当触发本技能时，Agent 按以下步骤操作：

**1.1 触发条件识别**
- 用户明确提及：下载慢、安装依赖慢、配置镜像、加速下载、设置国内源
- 检测到项目包含依赖文件：`package.json`、`requirements.txt`、`Cargo.toml`、`go.mod`、`Gemfile`、`.nuspec`、`environment.yml`、`build.gradle`、`pom.xml`、`composer.json`

**1.2 与用户确认**
```
询问内容：
1. 需要配置哪些包管理器？（如未指定，根据项目依赖文件自动判断）
2. 有偏好的镜像源吗？（默认推荐阿里云或华为云）
3. 配置范围：全局配置 or 项目级配置？
```

**1.3 环境检测命令**
Agent 执行以下命令检测已安装的工具：
```powershell
# Windows PowerShell 检测
python --version 2>$null; node --version 2>$null; npm --version 2>$null
cargo --version 2>$null; go version 2>$null; dotnet --version 2>$null
ruby --version 2>$null; conda --version 2>$null; gradle --version 2>$null
brew --version 2>$null
```
```bash
# Linux/Mac Bash 检测
for cmd in python node npm cargo go dotnet ruby conda gradle brew; do
    $cmd --version 2>/dev/null && echo "✓ $cmd available"
done
```

---

### Phase 2: 选择镜像源

根据下表为用户选择最优镜像。**标记 ⭐ 的为当前推荐**。

| 包管理器 | 推荐镜像 | URL | 备选1 | 备选2 |
|---------|---------|-----|-------|-------|
| **pip (Python)** | 阿里云 ⭐ | `https://mirrors.aliyun.com/pypi/simple/` | 清华大学 `https://pypi.tuna.tsinghua.edu.cn/simple/` | 腾讯云 `https://mirrors.cloud.tencent.com/pypi/simple/` |
| **npm/yarn/pnpm** | 华为云 ⭐ | `https://repo.huaweicloud.com/repository/npm/` | 阿里云 `https://registry.npmmirror.com` | 腾讯云 `https://mirrors.cloud.tencent.com/npm/` |
| **cargo (Rust)** | 阿里云 ⭐ | `https://mirrors.aliyun.com/crates.io-index/` | 清华大学 `https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/` | 中科大 `https://mirrors.ustc.edu.cn/crates.io-index/` |
| **go mod (Go)** | 阿里云 ⭐ | `https://mirrors.aliyun.com/goproxy/` | 七牛云 `https://goproxy.cn` | 官方中国 `https://goproxy.io` |
| **Maven (Java)** | 阿里云 ⭐ | `https://maven.aliyun.com/repository/public` | - | - |
| **Gradle (Java/Kotlin)** | 腾讯云 ⭐ | `https://mirrors.cloud.tencent.com/gradle/` | 阿里云 `https://maven.aliyun.com/repository/gradle-plugin/` | - |
| **NuGet (.NET)** | 华为云 ⭐ | `https://repo.huaweicloud.com/repository/nuget/v3/index.json` | 清华大学 `https://mirrors.tuna.tsinghua.edu.cn/nuget/v3/index.json` | - |
| **RubyGems (Ruby)** | 清华大学 ⭐ | `https://mirrors.tuna.tsinghua.edu.cn/rubygems/` | 中科大 `https://mirrors.ustc.edu.cn/rubygems/` | - |
| **Conda (Python)** | 清华大学 ⭐ | `https://mirrors.tuna.tsinghua.edu.cn/anaconda/` | 中科大 `https://mirrors.ustc.edu.cn/anaconda/` | - |
| **Homebrew (macOS)** | 中科大 ⭐ | `https://mirrors.ustc.edu.cn/homebrew-bottles/` | 清华大学 `https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/` | - |
| **Composer (PHP)** | 阿里云 ⭐ | `https://mirrors.aliyun.com/composer/` | - | - |

---

### Phase 3: 执行配置（Agent 直接运行命令）

> **重要**：Agent 根据用户选择的包管理器和镜像，直接在终端执行以下对应命令。
> 不要创建临时脚本文件，直接使用原生命令或 Shell 命令完成配置。

#### 3.1 Python pip 配置

**Windows 全局配置：**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\pip"
Set-Content -Path "$env:USERPROFILE\pip\pip.ini" -Value @"
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com

[install]
trusted-host = mirrors.aliyun.com
"@ -Encoding UTF8
Write-Host "✓ pip 已配置为阿里云镜像"
```

**Linux/Mac 全局配置：**
```bash
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << 'EOF'
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com

[install]
trusted-host = mirrors.aliyun.com
EOF
echo "✓ pip 已配置为阿里云镜像"
```

**项目级配置（在项目根目录）：**
```bash
# 创建 .piprc 或 setup.cfg
cat > pip.conf << 'EOF'
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
EOF
echo "✓ pip 项目级配置已完成"
```

**验证：**
```bash
pip config list
```

---

#### 3.2 Node.js npm/yarn/pnpm 配置

**全局配置：**
```bash
# npm
npm config set registry https://registry.npmmirror.com

# yarn（如已安装）
yarn config set registry https://registry.npmmirror.com 2>/dev/null || true

# pnpm（如已安装）
pnpm config set registry https://registry.npmmirror.com 2>/dev/null || true

echo "✓ Node.js 包管理器已配置"
```

**项目级配置（创建 `.npmrc`）：**
```bash
echo "registry=https://registry.npmmirror.com" > .npmrc
echo "✓ npm 项目级配置已完成"
```

**验证：**
```bash
npm config get registry
```

---

#### 3.3 Rust cargo 配置

**全局配置：**
```bash
mkdir -p ~/.cargo
cat > ~/.cargo/config.toml << 'EOF'
[source.crates-io]
replace-with = 'aliyun'

[source.aliyun]
registry = "https://mirrors.aliyun.com/crates.io-index/"
EOF
echo "✓ cargo 已配置为阿里云镜像"
```

**验证：**
```bash
cat ~/.cargo/config.toml
```

---

#### 3.4 Go mod 配置

**Windows PowerShell：**
```powershell
[Environment]::SetEnvironmentVariable("GOPROXY", "https://mirrors.aliyun.com/goproxy/,direct", "User")
$env:GOPROXY = "https://mirrors.aliyun.com/goproxy/,direct"
Write-Host "✓ Go GOPROXY 已配置"
```

**Linux/Mac：**
```bash
echo 'export GOPROXY=https://mirrors.aliyun.com/goproxy/,direct' >> ~/.bashrc
export GOPROXY=https://mirrors.aliyun.com/goproxy/,direct
echo "✓ Go GOPROXY 已配置"
```

**验证：**
```bash
go env GOPROXY
```

---

#### 3.5 NuGet (.NET) 配置

**Windows：**
```powershell
$nugetPath = "$env:APPDATA\NuGet"
New-Item -ItemType Directory -Force -Path $nugetPath
Set-Content -Path "$nugetPath\NuGet.Config" -Value @"
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="huawei" value="https://repo.huaweicloud.com/repository/nuget/v3/index.json" />
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
  </packageSources>
</configuration>
"@ -Encoding UTF8
Write-Host "✓ NuGet 已配置为华为云镜像"
```

**Linux/Mac：**
```bash
mkdir -p ~/.nuget
cat > ~/.nuget/NuGet.Config << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="huawei" value="https://repo.huaweicloud.com/repository/nuget/v3/index.json" />
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
  </packageSources>
</configuration>
EOF
echo "✓ NuGet 已配置为华为云镜像"
```

**验证：**
```bash
dotnet nuget list source
```

---

#### 3.6 RubyGems 配置

**全局配置：**
```bash
gem sources --remove https://rubygems.org/ 2>/dev/null || true
gem sources -a https://mirrors.tuna.tsinghua.edu.cn/rubygems/
echo "✓ RubyGems 已配置为清华镜像"
```

**Bundler 项目级配置：**
```bash
bundle config mirror.https://rubygems.org https://mirrors.tuna.tsinghua.edu.cn/rubygems/
echo "✓ Bundler 镜像已配置"
```

**验证：**
```bash
gem sources -l
```

---

#### 3.7 Conda 配置

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
echo "✓ Conda 已配置为清华镜像"
```

**验证：**
```bash
conda config --show channels
```

---

#### 3.8 Maven 配置

```bash
mkdir -p ~/.m2
cat > ~/.m2/settings.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<settings>
  <mirrors>
    <mirror>
      <id>aliyun</id>
      <mirrorOf>central</mirrorOf>
      <name>Aliyun Maven</name>
      <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
  </mirrors>
</settings>
EOF
echo "✓ Maven 已配置为阿里云镜像"
```

---

#### 3.9 Gradle 配置

**方式一：环境变量**
```bash
# 添加到 init.gradle 或环境变量
echo 'GRADLE_USER_HOME=~/.gradle' >> ~/.bashrc
mkdir -p ~/.gradle/init.d
cat > ~/.gradle/init.d/mirror.init.gradle << 'EOF'
allprojects {
    repositories {
        all { ArtifactRepository repo ->
            if (repo instanceof MavenArtifactRepository) {
                def url = repo.url.toString()
                if (url.startsWith("https://repo.maven.apache.org/maven2") ||
                    url.startsWith("https://jcenter.bintray.com")) {
                    project.logger.lifecycle "Repository ${repo.url} replaced with Tencent mirror."
                    remove repo
                }
            }
        }
        maven { url 'https://mirrors.cloud.tencent.com/nexus/repository/maven-public/' }
        maven { url 'https://maven.aliyun.com/repository/public' }
        mavenCentral()
    }
}
EOF
echo "✓ Gradle 已配置"
```

**方式二：项目级 `settings.gradle`**
```groovy
dependencyResolutionManagement {
    repositories {
        maven { url = uri('https://mirrors.cloud.tencent.com/gradle/') }
        mavenCentral()
    }
}
```

---

#### 3.10 Homebrew 配置 (macOS)

```bash
export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc
echo "✓ Homebrew 已配置为中科大镜像"
```

---

#### 3.11 Composer 配置 (PHP)

```bash
composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/
echo "✓ Composer 已配置为阿里云镜像"
```

---

### Phase 4: 验证与反馈

**4.1 执行验证命令**

配置完成后，Agent 自动运行对应的验证命令（见各小节末尾），并向用户展示结果。

**4.2 向用户报告**
```
报告格式示例：
─────────────────────────────────────
✅ 配置完成！已为您配置以下镜像源：

  • pip (Python)     → 阿里云 ⚡ 0.02s
  • npm (Node.js)    → 华为云 ⚡ 0.04s  
  • cargo (Rust)     → 阿里云 ⚡ 0.05s

📋 下次操作建议：
  • 运行 pip install / npm install 测试速度
  • 如需恢复默认配置，请告知我
─────────────────────────────────────
```

---

## 常见问题处理（Agent 参考）

| 问题 | 解决方案 |
|------|---------|
| 配置后仍然慢 | 清除缓存：`pip cache purge` / `npm cache clean --force` |
| SSL 证书错误 | 添加 `trusted-host` 配置（已在上述命令中包含） |
| 权限不足 | 使用用户级配置（非系统级），避免 sudo |
| 想恢复默认 | 删除对应配置文件或执行：`npm config delete registry` / `unset GOPROXY` |
| 特定项目需要不同镜像 | 使用项目级配置（`.npmrc` / `.piprc` / `.cargo/config.toml`） |

## 恢复默认配置命令速查

| 包管理器 | 恢复命令 |
|---------|---------|
| pip | `rm -f ~/.pip/pip.conf` 或 `del %USERPROFILE%\pip\pip.ini` |
| npm | `npm config delete registry` |
| yarn | `yarn config delete registry` |
| pnpm | `pnpm config delete registry` |
| cargo | `rm -f ~/.cargo/config.toml` |
| Go | `unset GOPROXY` 并从 shell 配置文件中删除 |
| NuGet | 删除 `%APPDATA%\NuGet\NuGet.Config` |
| RubyGems | `gem sources --remove <mirror-url>` 并添加回 `https://rubygems.org/` |
| Conda | `conda config --remove channels <mirror-url>` |
| Homebrew | `unset HOMEBREW_BOTTLE_DOMAIN` |

---

## Agent 执行规范

1. **直接执行**：不要创建脚本文件，直接运行 Shell 命令
2. **幂等性**：配置命令可重复执行，不会产生副作用
3. **用户确认**：修改前简要告知用户将要做什么
4. **错误处理**：如果某个工具未安装，跳过并告知用户
5. **平台适配**：自动检测操作系统，选择正确的命令格式（PowerShell vs Bash）
