# 📋 对外发布检查清单

**版本**: v4.1.0  
**最后更新**: 2026-04-07  
**维护者**: Release Agent

---

## 🎯 发布原则

> **只发布必要的开源文件，不包含研发过程文件**

### 核心原则
1. **最小必要** - 只包含运行所需的核心文件
2. **无研发痕迹** - 不包含迭代过程、临时文件、状态数据
3. **无测试数据** - 不包含样本库、测试数据集
4. **无日志配置** - 不包含 logs/, config/, metrics/ 等运行时目录

---

## ✅ 对外发布文件结构

```
agent-security-skill-scanner/
├── src/                          # ✅ 核心扫描器
│   ├── batch_scanner.py
│   ├── benchmark_full_scan.py
│   ├── cli.py
│   ├── engine/
│   │   └── smart_pattern_detector.py
│   ├── fast_batch_scan.py
│   ├── intent_detector_v2.py
│   ├── llm_analyzer.py
│   └── multi_language_scanner_v4.py
│
├── docs/                         # ✅ 文档
│   ├── ARCHITECTURE.md
│   ├── DELIVERY_REPORT.md
│   └── USER_GUIDE.md
│
├── CHECKLIST.md                  # ✅ 发布检查清单
├── LICENSE                       # ✅ 许可证
├── README.md                     # ✅ 使用文档
├── RELEASE_NOTES.md              # ✅ 发布说明
├── SKILL.md                      # ✅ 技能定义
├── package.json                  # ✅ 包配置
├── requirements.txt              # ✅ Python 依赖
├── release_validator.py          # ✅ 发布验证器
├── pre_release_validation.json   # ✅ 预验证报告
└── validation_report.json        # ✅ 验证报告
```

---

## 🚫 禁止发布的文件/目录

| 类别 | 路径 | 原因 |
|------|------|------|
| **样本库** | `samples/` | 测试数据，不对外 |
| **状态数据** | `data/` | 运行时状态文件 |
| **研发工具** | `expert_mode/` | 内部研发工具 |
| **脚本** | `scripts/` | 内部运维脚本 |
| **日志** | `logs/` | 运行日志 |
| **配置** | `config/` | 运行时配置 |
| **指标** | `metrics/` | 性能指标数据 |
| **迭代记录** | `round*/` | 开发过程记录 |
| **临时文件** | `reports/temp/` | 临时报告 |
| **缓存** | `__pycache__/`, `*.pyc` | Python 缓存 |
| **IDE 配置** | `.idea/`, `.vscode/` | 编辑器配置 |
| **Git 数据** | `.git/` | 版本控制数据 |

---

## 📝 发布流程

### 1. 准备阶段

```bash
# 切换到研发分支
cd agent-security-skill-scanner-master
git checkout release/v4.1.0

# 验证发布包
python3 release_validator.py
```

### 2. 清理阶段

```bash
# 删除不应发布的目录
rm -rf logs/ config/ metrics/
rm -rf samples/ data/ expert_mode/ scripts/
rm -rf round*/ reports/temp/
```

### 3. 验证阶段

对照检查清单逐项确认：

- [ ] 只保留 `src/`, `docs/`, 根目录必要文件
- [ ] 删除所有 `samples/`, `data/`, `expert_mode/`
- [ ] 删除所有 `logs/`, `config/`, `metrics/`
- [ ] 删除所有 `round*/`, `scripts/`
- [ ] 验证 `git status` 无多余文件

### 4. 提交阶段

```bash
# 提交发布 commit
git commit -m "release: v4.1.0 对外发布版本

- 替换为 release/v4.1.0 分支内容
- 删除研发过程文件
- 只保留必要的开源文件"

# 推送到对外仓库
git push origin master --force
git push github master --force
```

### 5. 验证阶段

```bash
# 检查 GitHub/Gitee 仓库文件列表
# 确认无 samples/, data/, expert_mode/ 等目录
```

---

## 📊 发布历史经验

### v4.1.0 (2026-04-07) ✅

**问题**: 初始版本包含了研发过程文件
- `samples/` (38 个测试样本)
- `data/*.json` (4 个状态文件)
- `expert_mode/` (18 个研发工具)
- `scripts/` (10 个脚本)

**解决方案**:
1. 从 `release/v4.1.0` 分支重新提取
2. 删除所有研发过程文件
3. 使用 `git filter-branch` 清理历史大文件
4. 强制推送到对外仓库

**教训**:
- ⚠️ 发布前必须对照检查清单
- ⚠️ 大文件 (>100MB) 会导致 GitHub 推送失败
- ⚠️ 需要在研发分支就做好文件隔离

### v2.2.1 (之前版本) ⚠️

**问题**: 
- 包含了 `release/v2.0.0/full-scan-result.json` (251MB)
- GitHub 推送失败

**解决方案**:
```bash
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch release/v2.0.0/full-scan-result.json' \
  --prune-empty --tag-name-filter cat -- --all
```

**教训**:
- ⚠️ 大文件一旦提交到 git 历史，清理很麻烦
- ⚠️ 应该在 `.gitignore` 中就排除大文件
- ⚠️ 发布前用 `git ls-files | xargs du -h` 检查文件大小

---

## 🔧 自动化脚本

### 发布前检查脚本

```bash
#!/bin/bash
# check_release.sh

echo "=== 检查发布文件结构 ==="

# 检查不应存在的目录
for dir in samples data expert_mode scripts logs config metrics; do
  if [ -d "$dir" ]; then
    echo "❌ 发现不应发布的目录：$dir"
    exit 1
  fi
done

# 检查大文件 (>50MB)
echo "检查大文件..."
large_files=$(find . -type f -size +50M -not -path "./.git/*")
if [ -n "$large_files" ]; then
  echo "❌ 发现大文件 (>50MB):"
  echo "$large_files"
  exit 1
fi

# 检查文件总数
file_count=$(git ls-files | wc -l)
echo "✅ 文件总数：$file_count"

# 显示文件结构
echo "=== 文件结构 ==="
git ls-files | head -30

echo "✅ 发布检查通过"
```

### 快速清理脚本

```bash
#!/bin/bash
# cleanup_for_release.sh

echo "清理研发过程文件..."

rm -rf samples/ data/ expert_mode/ scripts/
rm -rf logs/ config/ metrics/
rm -rf round*/ reports/temp/
rm -rf __pycache__/ *.pyc
rm -rf .idea/ .vscode/

echo "✅ 清理完成"
git status
```

---

## 📋 快速检查表

发布前快速对照（30 秒检查）：

| 检查项 | 状态 |
|--------|------|
| ❌ 无 `samples/` 目录 | ☐ |
| ❌ 无 `data/` 目录 | ☐ |
| ❌ 无 `expert_mode/` 目录 | ☐ |
| ❌ 无 `scripts/` 目录 | ☐ |
| ❌ 无 `logs/` 目录 | ☐ |
| ❌ 无 `config/` 目录 | ☐ |
| ❌ 无 `metrics/` 目录 | ☐ |
| ✅ 有 `src/` 目录 | ☐ |
| ✅ 有 `docs/` 目录 | ☐ |
| ✅ 有 `README.md` | ☐ |
| ✅ 有 `LICENSE` | ☐ |
| ✅ 无 >50MB 文件 | ☐ |
| ✅ 文件总数 <50 个 | ☐ |

---

## 🎯 下次发布待办

- [ ] 在研发分支创建 `.gitignore` 排除研发文件
- [ ] 添加 `check_release.sh` 自动化检查
- [ ] 创建 `release/` 分支专门用于发布
- [ ] 添加 CI/CD 自动验证发布结构
- [ ] 记录每次发布的文件清单对比

---

**参考文档**:
- [GitHub 文件限制](https://docs.github.com/en/repositories/working-with-files/managing-large-files)
- [Git LFS](https://git-lfs.github.com/)
- [Git Filter Branch](https://git-scm.com/docs/git-filter-branch)

---

**最后更新**: 2026-04-07  
**版本**: v4.1.0
