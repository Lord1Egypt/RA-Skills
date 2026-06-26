---
name: exec-guard
description: "命令安全守卫。在执行 shell 命令前进行语义分类（READ/WRITE/NETWORK/DESTRUCTIVE），自动放行安全操作，拦截危险操作。灵感来自 Claude Code 的命令语义分类器。触发词：exec guard、命令安全、安全执行、safe exec。"
alwaysLoad: true
---

# Exec Guard — 命令安全守卫

灵感来源：Claude Code 的命令语义分类器（bash command classifier）。

## 核心问题

Agent 需要 exec 权限才能干活，但开了 full 权限又怕翻车。
现有方案要么太松（full：什么都能跑）要么太紧（allowlist：预设白名单太死板）。

**Exec Guard 提供第三条路：语义级安全。**

不是看命令长什么样，而是理解命令**要做什么**。

## 何时生效

始终生效（`alwaysLoad: true`）。

每次准备调用 `exec` 工具时，先在脑中过一遍本 Skill 的分类规则。

## 命令分类体系

### Level 0 — READ（只读）✅ 自动放行

**定义**：只读取信息，不修改任何东西。

```bash
# 典型命令
cat / head / tail / less / more
ls / find / locate / which / where
grep / rg / ag / ack
wc / du / df / free / top / ps
echo / printf / date / whoami / id
git status / git log / git diff / git show
docker ps / docker logs / docker inspect
curl -s [GET] / wget -q -O -
python3 -c "print(...)"
jq / yq（只查询）
```

**判断要点**：
- 没有重定向（`>`、`>>`、`|` 到写命令）
- 没有 `-i`（in-place）/ `-w`（write）标志
- 没有副作用

### Level 1 — WRITE（workspace 内写入）✅ 自动放行

**定义**：在 workspace 目录内创建或修改文件。

```bash
# 典型命令
echo "x" > ./file.txt
mkdir -p ./dir
cp src.txt ./dst.txt
mv ./old.txt ./new.txt
git add / git commit / git push
npm install（在项目目录内）
pip install --user
touch / tee（workspace 内）
sed -i（workspace 内文件）
```

**判断要点**：
- 所有写入目标都在 workspace 或 /tmp 内
- 不影响系统文件
- 可恢复（有 git 或可以重新生成）

### Level 2 — WRITE_SYSTEM（系统级写入）⚠️ 需要确认

**定义**：修改 workspace 外的文件或系统配置。

```bash
# 典型命令
sudo apt install
systemctl start/stop/restart
crontab -e
echo "x" >> ~/.bashrc
cp file /etc/...
chmod / chown（系统目录）
docker run / docker-compose up
npm install -g
```

**处理方式**：
- 告诉用户你要做什么、为什么
- 等用户确认后执行
- 如果用户之前说过"这类操作随便做" → 记住偏好，下次自动放行

### Level 3 — NETWORK（网络操作）⚠️ 需要确认

**定义**：主动发起网络请求（不是读取本地资源）。

```bash
# 典型命令
curl -X POST / PUT / DELETE
wget（下载文件）
ssh / scp / rsync（到远程）
git clone（新仓库）
docker pull
pip install（从 PyPI 下载）
```

**处理方式**：
- GET 请求到已知安全域名 → 自动放行
- POST/PUT/DELETE → 需要确认
- 安全域名白名单：github.com, pypi.org, npmjs.com, api.openai.com 等

### Level 4 — DESTRUCTIVE（破坏性）🚫 必须确认

**定义**：不可逆的删除或破坏操作。

```bash
# 高危命令
rm -rf（尤其是带 / 或 ~）
dd if=... of=...
mkfs / fdisk
> /dev/sda
git reset --hard
git clean -fd
docker system prune
DROP TABLE / DELETE FROM（数据库）
kill -9 / killall
reboot / shutdown
```

**处理方式**：
1. **绝对不自动执行**
2. 告诉用户：这个命令会做什么、影响范围、是否可恢复
3. 建议更安全的替代方案（`trash` 替代 `rm`、`git stash` 替代 `git reset --hard`）
4. 用户明确说"执行"后才执行

## 分类决策树

```
命令 → 是否修改任何东西？
  ├─ 否 → Level 0 (READ) ✅
  └─ 是 → 修改什么？
      ├─ workspace/tmp 内的文件 → Level 1 (WRITE) ✅
      ├─ 系统文件/全局配置 → Level 2 (WRITE_SYSTEM) ⚠️
      ├─ 发起网络请求 → Level 3 (NETWORK)
      │   ├─ GET + 安全域名 → ✅
      │   └─ 其他 → ⚠️
      └─ 不可逆删除/破坏 → Level 4 (DESTRUCTIVE) 🚫
```

## 复合命令处理

管道和链式命令按**最高危险等级**分类：

```bash
# 整体 Level 0（两段都是只读）
cat file.txt | grep "pattern"

# 整体 Level 4（rm 是破坏性的）
find . -name "*.tmp" -exec rm {} \;
# → 建议改为：find . -name "*.tmp" -exec trash {} \;

# 整体 Level 2（写系统文件）
echo "export PATH=..." >> ~/.bashrc && source ~/.bashrc
```

## 用户偏好学习

记住用户的安全偏好：

```
用户："npm install 不用问我"
→ 记住：npm install 在项目目录内 → 自动放行

用户："docker 操作都先问我"
→ 记住：所有 docker 命令 → 需要确认

用户："sudo 随便用"
→ 记住：sudo 命令 → 自动放行（但 DESTRUCTIVE 级别仍然确认）
```

偏好记录到 `memory/` 或 MEMORY.md 中，跨 session 生效。

## 安全底线（不可覆盖）

即使用户说"什么都自动执行"，以下操作**永远需要确认**：

1. `rm -rf /` 或 `rm -rf ~`（或任何删除根目录/home 目录）
2. `dd` 写入块设备
3. `mkfs` 格式化
4. 任何涉及 `sudo` + 删除的组合
5. `:(){ :|:& };:` 或类似 fork bomb

## 输出格式

当需要确认时，用简洁格式：

```
⚠️ 这个命令会 [具体影响]
命令：[完整命令]
风险等级：Level X (TYPE)
更安全的替代：[如果有的话]
要执行吗？
```

## 与 OpenClaw 的配合

- `security: full` 模式下，Exec Guard 作为**软防护**补充（建议但不强制）
- `security: allowlist` 模式下，Exec Guard 帮助**扩展白名单**（自动放行 READ 级别）
- `security: deny` 模式下，Exec Guard 不生效（exec 本身就禁用了）

## 使用示例

```
Agent 内心独白：
"用户要我清理 docker 镜像。命令是 docker system prune -a。
分类：Level 4 (DESTRUCTIVE) — 会删除所有未使用的镜像、容器、网络。
不可自动执行。告诉用户影响，等确认。"

Agent 回复：
"⚠️ docker system prune -a 会删除所有未使用的镜像、容器和网络，释放磁盘空间但无法恢复。
要执行吗？或者我可以先 docker system df 看看占了多少空间。"
```
