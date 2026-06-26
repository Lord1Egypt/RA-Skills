### 技能名称：GitHub 仓库克隆与同步专家

### 技能描述

本技能指导 Agent 熟练掌握使用 Git 工具从 GitHub 获取代码仓库的全过程。它不仅涵盖了基础的 `git clone` 命令，还深入到了认证配置（SSH vs HTTPS）、分支管理、子模块处理以及增量更新等高级场景。Agent 将能够根据用户的网络环境和权限需求，选择最优的克隆策略，确保代码完整、安全地同步到本地环境。

### 核心指令集

#### 1. 环境预检与配置

在执行克隆之前，Agent 必须确保本地环境已准备好。

- **Git 安装检查：** 运行 `git --version`。如果未安装，需引导用户前往 Git 官网或包管理器进行安装。
- **身份认证配置：** 这是克隆私有仓库或进行推送的前提。
    - **SSH 方式（推荐）：** 指导生成 SSH 密钥 (`ssh-keygen`) 并添加到 GitHub 账户。使用 `git@github.com:username/repo.git` 格式。
    - **HTTPS 方式：** 使用 `https://github.com/username/repo.git` 格式。需提醒用户配置凭据管理器或使用 Personal Access Token (PAT) 代替密码。

#### 2. 基础克隆操作

指导用户执行标准的仓库下载。

- **标准克隆：** 使用 `git clone <repository_url>`。这会将远程仓库的所有文件、提交历史和分支信息下载到当前目录下的一个同名文件夹中。
- **指定目录名：** 如果用户希望自定义文件夹名称，使用 `git clone <repository_url> <directory_name>`。

#### 3. 高级克隆策略

针对不同的开发需求，Agent 需掌握特定的克隆参数。

- **浅克隆：** 对于大型仓库或只需最新代码的场景，使用 `git clone --depth 1 <repository_url>`。这仅下载最新的提交记录，极大节省时间和带宽。
- **特定分支克隆：** 若只需特定分支（如 `develop`），使用 `git clone -b <branch_name> <repository_url>`。
- **包含子模块：** 许多项目依赖子模块。必须使用 `git clone --recursive <repository_url>`。如果已克隆但未初始化子模块，需执行 `git submodule update --init --recursive`。

#### 4. 仓库同步与更新

克隆只是开始，Agent 需指导如何保持本地代码与远程同步。

- **拉取更新：** 在已克隆的目录中，运行 `git pull origin <branch_name>` 获取并合并远程变更。
- **变基同步：** 为了保持提交历史整洁，推荐使用 `git pull --rebase`。

#### 5. 故障排查与安全

- **权限被拒绝：** 检查 SSH 密钥是否正确添加到 `ssh-agent`，或 HTTPS 密码是否为 Token。
- **连接超时：** 可能是网络问题，建议检查代理设置或尝试切换 DNS。
- **证书验证失败：** 在企业环境中常见，通常涉及自签名证书，需谨慎处理 `http.sslVerify` 配置。

### 常见问题排查

#### "Permission denied (publickey)"

- **诊断：** 本地没有配置 SSH 密钥，或者公钥未添加到 GitHub 账户。
- **解决：** 运行 `cat ~/.ssh/id_rsa.pub` 查看公钥。如果没有，生成一个新的。将公钥内容复制到 GitHub 的 "SSH and GPG keys" 设置中。

#### "fatal: destination path '...' already exists and is not an empty directory"

- **诊断：** 尝试克隆到一个已经存在且非空的文件夹。
- **解决：** 要么删除该文件夹，要么在 `git clone` 命令后指定一个新的、不存在的文件夹名称。

#### 克隆速度极慢

- **诊断：** 仓库体积过大或网络连接不佳。
- **解决：** 建议使用浅克隆 (`--depth 1`) 仅获取最新代码。如果是网络波动，建议配置全局代理 (`git config --global http.proxy ...`)。

### 技能扩展建议

#### Fork 工作流

扩展技能以指导用户 Fork 仓库到自己的账户，然后克隆自己的 Fork，并配置上游远程仓库 (`git remote add upstream`) 以便同步原项目的更新。

#### GitHub CLI 集成

引入 `gh` 命令行工具，教导用户使用 `gh repo clone <repo>` 进行交互式克隆，这通常比原生 Git 更便捷，且自动处理认证。

#### 镜像克隆

针对需要迁移整个仓库（包括所有引用和refs）的场景，指导使用 `git clone --mirror`，这通常用于备份或迁移到另一个 Git 服务器。

