# Createrepo Skill - 仓库管理

## 技能描述 | Skill Description

**名称 | Name:** createrepo  
**版本 | Version:** 1.0.0  
**作者 | Author:** OS Build Agent  
**领域 | Domain:** RPM Repository Management  

专业的 RPM 仓库创建和管理技能，支持创建本地 YUM/DNF 仓库、仓库元数据生成、仓库同步等功能。

Professional RPM repository creation and management skill supporting local YUM/DNF repository creation, metadata generation, and repository synchronization.

---

## 功能列表 | Features

### 1. 仓库创建 | Repository Creation
- 创建 YUM/DNF 仓库 | Create YUM/DNF repos
- 生成元数据 | Generate metadata
- 增量更新 | Incremental updates
- 增量元数据 | Incremental metadata

### 2. 仓库管理 | Repository Management
- 添加包 | Add packages
- 删除包 | Remove packages
- 更新元数据 | Update metadata
- 仓库统计 | Repository statistics

### 3. 仓库同步 | Repository Synchronization
- 远程同步 | Remote sync
- 本地镜像 | Local mirror
- 增量同步 | Incremental sync
- 计划同步 | Scheduled sync

### 4. 多架构支持 | Multi-architecture Support
- x86_64 仓库 | x86_64 repos
- aarch64 仓库 | aarch64 repos
- 多架构合并 | Multi-arch merge
- 源码仓库 | Source repos

### 5. 安全功能 | Security Features
- GPG 签名 | GPG signing
- 签名验证 | Signature verification
- 校验和生成 | Checksum generation
- 校验和验证 | Checksum verification

---

## 配置 | Configuration

### 工具安装 | Tool Installation

```bash
# RHEL/Fedora
dnf install createrepo_c deltarpm

# openSUSE
zypper install createrepo_c

# Debian/Ubuntu (交叉编译)
apt-get install createrepo-c
```

### 仓库结构 | Repository Structure

```
/path/to/repo/
├── x86_64/
│   ├── Packages/          # RPM 包
│   ├── repodata/          # 元数据
│   │   ├── primary.xml.gz
│   │   ├── filelists.xml.gz
│   │   ├── other.xml.gz
│   │   └── repomd.xml
│   └── comps.xml          # 包组
├── src/                   # 源码包
└── aarch64/               # 其他架构
```

---

## 使用示例 | Usage Examples

### 基本仓库创建 | Basic Repository Creation

```bash
# 创建基本仓库
# Create basic repository
createrepo /path/to/repo

# 创建仓库（指定输出目录）
# Create repo (specify output dir)
createrepo --outputdir /path/to/output /path/to/packages

# 快速创建（跳过某些元数据）
# Quick create (skip some metadata)
createrepo --skip-stat /path/to/repo

# 带校验和的仓库
# Repository with checksums
createrepo --checksum sha256 /path/to/repo
```

### 增量更新 | Incremental Updates

```bash
# 增量更新元数据
# Incremental metadata update
createrepo --update /path/to/repo

# 增量更新（带数据库）
# Incremental update (with database)
createrepo --update --deltas /path/to/repo

# 仅更新特定包
# Update specific packages only
createrepo --update \
  --pkglist packages.txt \
  /path/to/repo
```

### 包组支持 | Package Groups Support

```bash
# 创建带包组的仓库
# Create repo with package groups
createrepo --groupfile comps.xml /path/to/repo

# 更新包组
# Update package groups
createrepo --update \
  --groupfile comps.xml \
  /path/to/repo

# comps.xml 示例
# comps.xml example
cat > comps.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE comps PUBLIC "-//Red Hat, Inc.//DTD Comps info//EN" "comps.dtd">
<comps>
  <group>
    <id>mygroup</id>
    <name>My Group</name>
    <description>Group description</description>
    <default>true</default>
    <uservisible>true</uservisible>
    <packagelist>
      <packagereq type="mandatory">package1</packagereq>
      <packagereq type="optional">package2</packagereq>
    </packagelist>
  </group>
</comps>
EOF
```

### 多架构仓库 | Multi-architecture Repository

```bash
# 为特定架构创建仓库
# Create repo for specific architecture
createrepo --arch x86_64 /path/to/repo/x86_64

# 创建源码仓库
# Create source repository
createrepo --arch src /path/to/repo/src

# 创建 noarch 仓库
# Create noarch repository
createrepo --arch noarch /path/to/repo/noarch

# 合并多架构
# Merge multi-architecture
createrepo --baseurl http://example.com/repo \
  /path/to/repo
```

### 仓库签名 | Repository Signing

```bash
# 导入 GPG 密钥
# Import GPG key
rpm --import /path/to/RPM-GPG-KEY-myrepo

# 签名所有包
# Sign all packages
for rpm in /path/to/repo/Packages/*.rpm; do
  rpm --addsign "$rpm"
done

# 生成仓库元数据签名
# Generate repo metadata signature
gpg --detach-sign --armor \
  /path/to/repo/repodata/repomd.xml

# 验证仓库
# Verify repository
gpg --verify \
  /path/to/repo/repodata/repomd.xml.asc \
  /path/to/repo/repodata/repomd.xml
```

### 仓库同步 | Repository Synchronization

```bash
# 同步远程仓库
# Sync remote repository
reposync --repoid=fedora \
  --download_path=/path/to/mirror

# 同步特定架构
# Sync specific architecture
reposync --repoid=fedora \
  --arch=x86_64 \
  --download_path=/path/to/mirror

# 同步最新包
# Sync latest packages only
reposync --repoid=fedora \
  --newest-only \
  --download_path=/path/to/mirror

# 同步并生成元数据
# Sync and generate metadata
reposync --repoid=fedora \
  --download_path=/path/to/mirror
createrepo /path/to/mirror/fedora
```

### 仓库查询 | Repository Query

```bash
# 列出仓库信息
# List repo info
repocreate --info /path/to/repo

# 列出国包
# List packages
repoquery --repofrompath="myrepo,/path/to/repo" \
  --list "*"

# 查询包依赖
# Query package dependencies
repoquery --repofrompath="myrepo,/path/to/repo" \
  --requires package-name

# 查询包提供
# Query package provides
repoquery --repofrompath="myrepo,/path/to/repo" \
  --provides package-name
```

---

## DNF 仓库配置 | DNF Repository Configuration

```ini
# /etc/yum.repos.d/myrepo.repo 示例
# /etc/yum.repos.d/myrepo.repo example

[myrepo]
name=My Repository
baseurl=http://example.com/repo/$releasever/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-myrepo
metadata_expire=1h
repo_gpgcheck=1

# 本地仓库示例
# Local repo example

[mylocalrepo]
name=My Local Repository
baseurl=file:///path/to/repo
enabled=1
gpgcheck=0
```

---

## 高级用法 | Advanced Usage

### 增量元数据 | Incremental Metadata

```bash
# 使用旧元数据加速更新
# Use old metadata for faster update
createrepo --update \
  --oldpackagedir /path/to/old/packages \
  /path/to/repo

# 生成增量元数据
# Generate incremental metadata
createrepo --update \
  --retain-old-md 5 \
  /path/to/repo
```

### Delta RPM 生成 | Delta RPM Generation

```bash
# 生成 delta RPM
# Generate delta RPM
deltarpm /path/to/old.rpm \
  /path/to/new.rpm \
  /path/to/delta.rpm

# 创建带 delta 的仓库
# Create repo with deltas
createrepo --deltas \
  --max-delta-rpm-size 100M \
  /path/to/repo

# 仅生成 delta
# Generate deltas only
deltarpm --server \
  --output-dir /path/to/deltas \
  /path/to/packages
```

### 仓库优化 | Repository Optimization

```bash
# 压缩元数据
# Compress metadata
createrepo --compress-type xz \
  /path/to/repo

# 指定校验和类型
# Specify checksum type
createrepo --checksum sha256 \
  /path/to/repo

# 跳过统计信息
# Skip statistics
createrepo --skip-stat \
  /path/to/repo

# 限制 worker 数量
# Limit worker count
createrepo --workers 4 \
  /path/to/repo
```

---

## 命令参考 | Command Reference

### createrepo 选项 | Options

| 选项 | Option | 描述 | Description |
|------|--------|------|-------------|
| `-o` | outputdir | 输出目录 | Output directory |
| `--update` | update | 增量更新 | Incremental update |
| `--deltas` | deltas | 生成 delta RPM | Generate delta RPM |
| `--groupfile` | groupfile | 包组文件 | Package groups file |
| `--checksum` | checksum | 校验和类型 | Checksum type |
| `--compress-type` | compress | 压缩类型 | Compression type |
| `--skip-stat` | skip stat | 跳过统计 | Skip statistics |
| `--workers` | workers | worker 数量 | Worker count |

### reposync 选项 | Options

| 选项 | Option | 描述 | Description |
|------|--------|------|-------------|
| `--repoid` | repo id | 仓库 ID | Repository ID |
| `--download-path` | download path | 下载路径 | Download path |
| `--arch` | architecture | 架构 | Architecture |
| `--newest-only` | newest only | 仅最新包 | Only latest packages |

---

## 最佳实践 | Best Practices

### 1. 仓库组织 | Repository Organization
- 按架构分目录 | Separate directories by architecture
- 定期清理旧包 | Clean old packages regularly
- 使用版本化路径 | Use versioned paths

### 2. 性能优化 | Performance Optimization
- 使用增量更新 | Use incremental updates
- 启用压缩 | Enable compression
- 使用缓存 | Use caching

### 3. 安全性 | Security
- 签名所有包 | Sign all packages
- 启用 GPG 检查 | Enable GPG check
- 定期更新密钥 | Rotate keys regularly

---

## 故障排除 | Troubleshooting

### 元数据错误 | Metadata Error
```bash
# 清理并重新生成
# Clean and regenerate
rm -rf /path/to/repo/repodata
createrepo /path/to/repo

# 验证元数据
# Verify metadata
repomd-check /path/to/repo/repodata/repomd.xml
```

### 包冲突 | Package Conflict
```bash
# 查找冲突包
# Find conflicting packages
repoquery --repofrompath="myrepo,/path/to/repo" \
  --whatprovides <capability>

# 删除冲突包
# Remove conflicting package
rm /path/to/repo/Packages/conflicting-*.rpm
createrepo --update /path/to/repo
```

---

## 参考资料 | References

- [Createrepo 文档 | Createrepo Docs](https://github.com/rpm-software-management/createrepo_c)
- [DNF 仓库指南 | DNF Repo Guide](https://dnf.readthedocs.io/en/latest/)
- [YUM 仓库指南 | YUM Repo Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/creating_customized_rhel_images_using_the_image_builder_creating_rhel_images_in_hybrid_cloud_environments/assembly_creating-repositories_creating-custom-rhel-images)

---

## 许可证 | License

MIT License

---

## 更新日志 | Changelog

### v1.0.0 (2026-03-23)
- 初始版本，完整的仓库管理支持
- Initial release with full repository management support
- 中英文双语文档
- Bilingual documentation (Chinese/English)
