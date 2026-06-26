# Tool Name: check_workspace_symlinks
# Description:
扫描 OpenClaw 的沙箱工作区（Workspace）目录，检查是否存在恶意的符号链接（Symlink）逃逸。
如果发现指向工作区外部系统目录（如 /etc, /root, /var）的软链接，说明可能存在沙箱被击穿或任意文件读取的风险。

# Parameters:
此工具不需要输入参数。

# Returns:
返回一个 JSON 字符串，包含以下字段：
- `status`: "clean" (无逃逸链接), "risks_found" (发现跨界软链接) 或 "error"。
- `scanned_dir`: 扫描的工作区路径。
- `dangerous_symlinks`: 危险链接的详细列表（源路径 -> 目标越权路径）。