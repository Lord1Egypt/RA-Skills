---
name: batch-git-url-replace
description: |
  批量替换指定目录下所有 Git 仓库的远程地址（remote URL）。
  当用户需要将 Git 仓库从一个服务器迁移到另一个服务器时使用。
  触发词：git remote 替换、git url 批量修改、git 仓库迁移、更换 git 地址、批量修改 remote url。
---

# 批量替换 Git 远程地址

## 输入参数

执行前必须从用户处获取以下参数：
- `scanDir`：扫描目录路径（如 D:\ 或 /home/user/projects）
- `oldUrl`：旧 Git 服务器地址
- `newUrl`：新 Git 服务器地址

## 执行步骤

### Windows 系统

使用 PowerShell 执行以下命令（将参数替换为用户提供的实际值）：

```powershell
$scanDir = "<scanDir>"
$oldUrl = "<oldUrl>"
$newUrl = "<newUrl>"

Write-Host "开始扫描 $scanDir 下的所有 .git/config 文件..." -ForegroundColor Cyan
Write-Host "目标：将 $oldUrl 替换为 $newUrl" -ForegroundColor Cyan
Write-Host "----------------------------------------"

$gitDirs = Get-ChildItem -Path $scanDir -Recurse -Directory -Filter ".git" -Force -ErrorAction SilentlyContinue

$countSuccess = 0
$countSkip = 0

foreach ($gitDir in $gitDirs) {
    $configPath = Join-Path $gitDir.FullName "config"
    if (Test-Path $configPath) {
        try {
            $content = Get-Content -Path $configPath -Raw -Encoding UTF8
            if ($content -like "*$oldUrl*") {
                $newContent = $content -replace [regex]::Escape($oldUrl), $newUrl
                Set-Content -Path $configPath -Value $newContent -Encoding UTF8 -NoNewline
                Write-Host "[已修改] $configPath" -ForegroundColor Green
                $countSuccess++
            } else {
                $countSkip++
            }
        } catch {
            Write-Host "[错误] 无法处理 $configPath : $_" -ForegroundColor Red
        }
    }
}

Write-Host "----------------------------------------"
Write-Host "处理完成！成功: $countSuccess, 跳过: $countSkip" -ForegroundColor Yellow
```

### Linux 系统

使用 Bash 执行以下命令：

```bash
SCAN_DIR="<scanDir>"
OLD_URL="<oldUrl>"
NEW_URL="<newUrl>"

echo "开始扫描 $SCAN_DIR 下的所有 .git/config 文件..."
echo "目标：将 $OLD_URL 替换为 $NEW_URL"
echo "----------------------------------------"

count_success=0
count_skip=0

while IFS= read -r gitdir; do
    config="$gitdir/config"
    if [ -f "$config" ] && grep -q "$OLD_URL" "$config" 2>/dev/null; then
        sed -i "s|${OLD_URL}|${NEW_URL}|g" "$config"
        echo "[已修改] $config"
        ((count_success++))
    else
        ((count_skip++))
    fi
done < <(find "$SCAN_DIR" -name ".git" -type d 2>/dev/null)

echo "----------------------------------------"
echo "处理完成！成功: $count_success, 跳过: $count_skip"
```

## 执行后

建议用户进入某个项目目录运行 `git remote -v` 验证是否生效。