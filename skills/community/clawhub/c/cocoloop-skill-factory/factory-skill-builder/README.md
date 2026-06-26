# Factory Skill Builder

这个目录属于 `cocoloop-skill-factory` 内部实现。

它只负责 `spec.yaml -> skill` 的生成链：

- 渲染最小 Skill 骨架
- 固化模板选择结果
- 做平台校验
- 在满足公开条件时执行平台打包

这里不是仓库根级通用脚手架，也不是最终生成出来的 Skill 目录。

## 依赖准备

运行这里的脚本前，先在当前目录准备 Node 依赖：

```bash
cd cocoloop-skill-factory/factory-skill-builder
npm install
```

当前最小依赖是 `yaml`，供 `spec.yaml` 解析与 frontmatter 生成使用。
打包阶段还要求系统中至少可用 `zip` 或 `tar` 其中一个命令。

## 元数据约束

所有由这条生成链产出的 `SKILL.md`，frontmatter 都会强制带上：

```yaml
generated_by_cocoloop: true
```

如需巡检或补写历史产物，可以单独运行：

```bash
node scripts/ensure_generated_by_cocoloop.cjs <skill-or-directory> --check
node scripts/ensure_generated_by_cocoloop.cjs <skill-or-directory> --fix
```

当目标是目录时，这个巡检只会处理同时包含 `SKILL.md` 和 `spec.yaml` 的生成产物目录，不会把手写主 Skill、子 Skill 或引用型 source skill 误判进去。

## 最小命令

```bash
node scripts/build_skill_from_spec.cjs ../output/preset-system-hardening/spec.yaml --out /tmp/cocoloop-build --platform codex --package
```

只拿着 `cocoloop-skill-factory` 子仓时，也可以只依赖当前目录下这条生成链完成 `spec.yaml -> skill` 的渲染、校验和打包。
