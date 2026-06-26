# 国内镜像源完整列表

## npm / yarn / pnpm

### 推荐源
```
https://registry.npmmirror.com
```

### 备选源
| 名称 | 地址 | 说明 |
|---|---|---|
| 淘宝 npmmirror | `https://registry.npmmirror.com` | 最稳定，同步快 |
| 华为云 | `https://repo.huaweicloud.com/repository/npm/` | 企业级 |
| 腾讯云 | `https://mirrors.cloud.tencent.com/npm/` | 稳定 |

### 配置命令
```bash
# npm
npm config set registry https://registry.npmmirror.com

# yarn
yarn config set registry https://registry.npmmirror.com

# pnpm
pnpm config set registry https://registry.npmmirror.com

# 验证
npm config get registry
```

### 恢复默认
```bash
npm config set registry https://registry.npmjs.org
```

---

## pip (Python)

### 推荐源
```
https://pypi.tuna.tsinghua.edu.cn/simple
```

### 备选源
| 名称 | 地址 |
|---|---|
| 清华 TUNA | `https://pypi.tuna.tsinghua.edu.cn/simple` |
| 阿里云 | `https://mirrors.aliyun.com/pypi/simple/` |
| 中科大 | `https://pypi.mirrors.ustc.edu.cn/simple/` |
| 豆瓣 | `https://pypi.douban.com/simple/` |

### 配置命令
```bash
# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 临时使用
pip install package -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 恢复默认
```bash
pip config unset global.index-url
pip config unset global.trusted-host
```

---

## Go (GOPROXY)

### 推荐源
```
https://goproxy.cn,direct
```

### 备选源
| 名称 | 地址 |
|---|---|
| 七牛 goproxy.cn | `https://goproxy.cn` |
| 阿里云 | `https://mirrors.aliyun.com/goproxy/` |
| 字节 | `https://goproxy.io` |

### 配置命令
```bash
go env -w GOPROXY=https://goproxy.cn,direct
go env -w GOSUMDB=sum.golang.google.cn
go env -w GONOSUMDB=*

# 验证
go env GOPROXY
```

### 恢复默认
```bash
go env -w GOPROXY=https://proxy.golang.org,direct
go env -u GONOSUMDB
```

---

## Docker

### 推荐源
```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me"
  ]
}
```

### 备选源
| 名称 | 地址 | 说明 |
|---|---|---|
| 1ms.run | `https://docker.1ms.run` | 社区维护 |
| xuanyuan | `https://docker.xuanyuan.me` | 稳定 |
| DaoCloud | `https://docker.m.daocloud.io` | 企业级 |
| 南京大学 | `https://docker.nju.edu.cn` | 教育网 |
| 中科大 | `https://docker.mirrors.ustc.edu.cn` | 教育网 |

> ⚠️ 国内 Docker 镜像源变动频繁，部分可能随时失效。建议配置多个备选。

### 配置方法

**Linux:**
```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

**Windows (Docker Desktop):**
Settings → Docker Engine → 编辑 JSON → 添加 registry-mirrors → Apply & Restart

**macOS (Docker Desktop):**
Preferences → Docker Engine → 同上

### 验证
```bash
docker info | grep -A 5 "Registry Mirrors"
```

---

## Cargo (Rust)

### 推荐源
创建或编辑 `~/.cargo/config.toml`:

```toml
[source.crates-io]
replace-with = "tuna"

[source.tuna]
registry = "sparse+https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/"
```

### 备选源
| 名称 | 地址 |
|---|---|
| 清华 TUNA | `sparse+https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/` |
| 中科大 | `sparse+https://mirrors.ustc.edu.cn/crates.io-index/` |
| 字节 | `sparse+https://rsproxy.cn/crates.io-index` |

### 恢复默认
删除 `~/.cargo/config.toml` 中的 source 配置。

---

## Maven

### 推荐源
编辑 `~/.m2/settings.xml`:

```xml
<settings>
  <mirrors>
    <mirror>
      <id>aliyun</id>
      <name>Aliyun Maven Mirror</name>
      <url>https://maven.aliyun.com/repository/public</url>
      <mirrorOf>central</mirrorOf>
    </mirror>
  </mirrors>
</settings>
```

### 备选源
| 名称 | 地址 |
|---|---|
| 阿里云 | `https://maven.aliyun.com/repository/public` |
| 华为云 | `https://repo.huaweicloud.com/repository/maven/` |
| 腾讯云 | `https://mirrors.cloud.tencent.com/nexus/repository/maven-public/` |

---

## Gradle

### 推荐配置
在 `build.gradle` 中:

```groovy
allprojects {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/public' }
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'https://maven.aliyun.com/repository/gradle-plugin' }
        mavenCentral()
    }
}
```

或全局配置 `~/.gradle/init.gradle`:

```groovy
allprojects {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/public' }
        mavenCentral()
    }
}
```

---

## Homebrew (macOS)

### 配置命令
```bash
# 清华 TUNA
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
export HOMEBREW_PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"

# 加入 ~/.zshrc 或 ~/.bashrc 永久生效
```

### 恢复默认
```bash
unset HOMEBREW_API_DOMAIN HOMEBREW_BOTTLE_DOMAIN HOMEBREW_BREW_GIT_REMOTE HOMEBREW_CORE_GIT_REMOTE
```

---

## 测速方法

### npm 测速
```bash
# 测试淘宝源
time npm ping --registry https://registry.npmmirror.com

# 测试默认源
time npm ping --registry https://registry.npmjs.org
```

### pip 测速
```bash
time pip install --dry-run requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Docker 测速
```bash
time docker pull hello-world
```
