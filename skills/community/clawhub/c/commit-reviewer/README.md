# Commit Reviewer

一个专门用于**检查 Git 提交是否真正修复需求 / Bug** 的辅助工具。

> ⚠️ 推荐在项目目录内直接使用，无需任何配置

相比只看 commit message，它会基于 **真实 diff + 业务需求** 做逐条判断，更接近真实代码评审。

---

## 适用场景

当你遇到这些情况时可以使用：

- 想确认某个 commit 到底有没有修复 Bug
- 提交看起来改了，但不确定是否改对
- 需要 review 他人提交是否覆盖需求
- 想快速判断是否存在遗漏 / 风险

---

## 使用方式

### 1）自动识别项目（最简单）

```bash
/commit_reviewer <commit1> [commit2] ...
```

---

### 2）指定项目名（需要配置工作目录）

```bash
/commit_reviewer <project> <commit1> [commit2] ...
```

---

### 3）指定项目路径（通用）

```bash
/commit_reviewer /path/to/repo <commit1>
```

---

## 工作目录配置（重要）

### 方式一：在项目目录内使用（推荐）

```bash
cd /path/to/your/repo
/commit_reviewer <commit>
```

无需任何配置，会自动识别当前 Git 仓库。

---

### 方式二：使用项目名（需要配置）

```bash
export COMMIT_REVIEWER_WORK_ROOT=/your/projects/root
```

目录结构示例：

```text
/your/projects/root/
  ├── project-a/
  ├── project-b/
  ├── project-c/
```

工具会在该目录下自动查找对应项目。

---

### 注意

- 未配置工作目录时：
  - 仅支持当前项目模式
- 配置后：
  - 支持项目名模式 + 自动扫描

---

## 使用流程

1. 提供 commit（支持 7~40 位）
2. 提供需求 / Bug 描述
3. 自动分析并输出结论

---

## 输出示例

```
检查结果：

Commit:
- 1f168bc

需求拆解：
1. 修复首页弹窗重复问题

逐项检查：
1. 首页弹窗重复
- 结论：已解决
- 依据：新增去重逻辑

总体结论：
- 已覆盖核心需求

最终判断：
- 已修复
```

---

## 一句话总结

> 不是帮你“看代码改了啥”，而是帮你判断：问题到底有没有被解决。
