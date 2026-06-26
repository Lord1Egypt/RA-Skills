# OpenEuler ↔ RHEL 版本兼容矩阵

用于确定 OpenEuler 系统应对照哪个 RHEL 版本的 CIS Benchmark。

## 映射关系

| OpenEuler 版本 | 对应 RHEL 版本 | CIS Benchmark 版本 | 备注 |
|----------------|----------------|--------------------|------|
| openEuler 22.03 LTS | RHEL 9.0 | CIS RHEL 9.0 Benchmark v2.0.0+ | 主力对应 |
| openEuler 23.09 | RHEL 9.2+ | CIS RHEL 9 Benchmark v3.0.0+ | 较新内核 |
| openEuler 20.03 LTS | RHEL 8.2 | CIS RHEL 8 Benchmark v2.0.0+ | LTS 稳定版 |
| openEuler 24.03 LTS | RHEL 9.4+ | CIS RHEL 9 Benchmark v3.1.0+ | 最新 LTS |
| openEuler 21.09 | RHEL 8.4 | CIS RHEL 8 Benchmark v2.1.0+ | 过渡版本 |

## 确定版本命令

在目标 OpenEuler 系统上执行：

```bash
# 查看 OpenEuler 版本
cat /etc/openEuler-release
cat /etc/openEuler-latest

# 查看内核版本
uname -r

# 查看系统发行版详情
cat /etc/os-release
```

## 注意事项

- 映射基于 syscall 兼容层和软件包版本对齐，并非官方声明
- 部分 CIS 检查项在 OpenEuler 上没有直接等效项，需在 `cis-rhel-benchmark-mapping.md` 中标记为 `N/A` 或 `手动验证`
- 内核参数的默认值可能不同，建议先收集目标系统实际值再做比较
